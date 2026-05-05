from logic.intent import detect_intent
from logic.evidence import analyze_evidence
from logic.risk import classify_risk
from logic.decision import decide_flow
from logic.image_pipeline import process_image

from logic.chains.query_chain import query_flow

from logic.product_extractor import extract_product
from tools.db_order_tool import get_user_orders
from tools.db_verification_tool import verify_purchase
from tools.refund_tool import process_refund
from tools.exchange_tool import create_exchange
from tools.ticket_tool import create_ticket
from services.db_service import fetch_one
from services.vision_service import validate_image

import re


# ==================================================
# 🧠 LIGHTWEIGHT CONVERSATION MEMORY
# ==================================================
CONVERSATION_STATE = {}


# ==================================================
# 🔧 HELPERS
# ==================================================

def extract_order_id(verification_text):
    match = re.search(r"Order ID:\s*(\w+)", verification_text)
    return match.group(1) if match else None


# ==================================================
# 🔥 RESPONSE CLEANER (VERY IMPORTANT)
# ==================================================

def clean_response(text):
    banned = [
        "status",
        "explanation",
        "upload in process",
        "image received",
        "analysis complete",
        "amazon"
    ]

    for word in banned:
        if word in text.lower():
            return "Please upload a clearer image."

    return text


def normalize_status(value):
    return str(value or "").strip().lower()


def get_user_profile(user_id):
    return fetch_one(
        "SELECT complaint_count FROM users WHERE user_id = %s",
        (user_id,)
    ) or {}


def get_order_for_product(user_id, product_name):
    return fetch_one(
        """
        SELECT order_id, product_name, price, status
        FROM orders
        WHERE user_id = %s AND LOWER(product_name) = LOWER(%s)
        LIMIT 1
        """,
        (user_id, product_name)
    )


def get_order_by_id(user_id, order_id):
    return fetch_one(
        """
        SELECT order_id, product_name, price, status
        FROM orders
        WHERE user_id = %s AND order_id = %s
        LIMIT 1
        """,
        (user_id, order_id)
    )


def build_risk_context(user_id, order=None, evidence=None):
    user_profile = get_user_profile(user_id)
    complaint_count = user_profile.get("complaint_count", 0) or 0

    return {
        "price": float(order.get("price", 0) or 0) if order else 0,
        "kb_found": True,
        "user_history": complaint_count,
        "has_image": bool((evidence or {}).get("has_image")),
    }


def is_duplicate_order(order):
    status = normalize_status(order.get("status"))
    return status in {"refunded", "exchanged"}


def get_state(user_id):
    return CONVERSATION_STATE.setdefault(
        str(user_id),
        {
            "last_input": "",
            "last_intent": None,
            "last_product": None,
            "awaiting_product": False,
            "awaiting_image": False,
        },
    )


def update_state(user_id, **changes):
    state = get_state(user_id)
    state.update(changes)
    return state


# ==================================================
# 🚀 MAIN HANDLER
# ==================================================

def handle_request(user_id, user_input, image_path=None, selected_order_id=None, selected_product=None, selected_action=None):
    state = get_state(user_id)

    # ==================================================
    # 🔥 CLEAN INPUT
    # ==================================================
    clean_input = str(user_input or "").strip()

    # Allow image-only follow-ups when the conversation already has context.
    if (not clean_input or clean_input.lower() == "text") and image_path:
        clean_input = state.get("last_input") or "User uploaded an image."

    if not clean_input or clean_input.lower() == "text":
        return "Please describe your issue."

    # ==================================================
    # INTENT + EVIDENCE
    # ==================================================
    intent = detect_intent(clean_input)
    if selected_action and selected_action in {"refund", "exchange", "query"}:
        intent = selected_action
    evidence = analyze_evidence(clean_input, image_path)

    # If the user is replying with just a product name after a pending refund/exchange,
    # treat it as the missing product rather than a new standalone message.
    if state.get("awaiting_product") and clean_input.lower() not in {"refund", "exchange", "query"}:
        hinted_product = extract_product(clean_input, f"Product: {clean_input}") or clean_input
        update_state(
            user_id,
            last_input=clean_input,
            last_product=hinted_product,
            awaiting_product=False,
            awaiting_image=True,
            last_intent=state.get("last_intent") or intent,
        )
    else:
        update_state(user_id, last_input=clean_input, last_intent=intent)

    # ==================================================
    # 🔥 IMAGE PROCESSING
    # ==================================================
    image_data = None

    if image_path:
        image_validation = validate_image(image_path)
        if image_validation.get("type") == "image_rejected":
            return image_validation["message"]

        if image_validation.get("type") == "image_fake":
            return image_validation["message"]

        print("📸 Processing image:", image_path)
        image_data = process_image(image_path)
        print("🧠 Image Data:", image_data)

        if not image_data.get("object"):
            return "No clear object detected. Please upload a clearer image."

    # ==================================================
    # RISK + DECISION
    # ==================================================
    risk = classify_risk(evidence, image_data or {}, build_risk_context(user_id))
    decision = decide_flow(intent, risk)

    print("Intent:", intent)
    print("Risk:", risk)
    print("Decision:", decision)

    # ==================================================
    # PRODUCT EXTRACTION
    # ==================================================
    product = None
    order = None

    if selected_order_id:
        order = get_order_by_id(user_id, selected_order_id)

    if selected_product:
        product = selected_product
        if not order:
            order = get_order_for_product(user_id, selected_product)

    if decision in ["refund", "exchange"]:
        try:
            if not product:
                orders = get_user_orders.run(user_id)
                product = extract_product(clean_input, orders)
                if product:
                    order = get_order_for_product(user_id, product)
                    update_state(user_id, last_product=product)
                print("🧾 Product:", product)
        except Exception as e:
            print("❌ Product extraction error:", e)

        if not product and state.get("last_product"):
            product = state.get("last_product")
            order = get_order_for_product(user_id, product)

    if decision == "query":
        response = query_flow(clean_input)
        update_state(user_id, awaiting_product=False, awaiting_image=False)
        return clean_response(response)

    # ==================================================
    # 🔥 IMAGE ↔ PRODUCT MATCH
    # ==================================================
    if image_data and product:
        detected = image_data.get("object")

        # Product-to-YOLO-class mapping for fuzzy matching
        product_label_map = {
            "Shoes": ["shoe", "sneaker", "boot", "sandal", "slipper", "loafer", "pump", "footwear", "flip flop", "oxford"],
            "Laptop": ["laptop", "computer", "notebook", "monitor", "keyboard"],
            "Phone": ["phone", "smartphone", "mobile", "cell phone", "iphone"],
            "Headphones": ["headphones", "earbuds", "headset", "earmuffs", "earphone"],
            "Fan": ["fan"]
        }

        allowed_labels = product_label_map.get(product, [product.lower()])
        detected_lower = detected.lower() if detected else ""
        
        # Check if detected label matches any allowed label (either exact word or substring)
        is_match = any(label in detected_lower for label in allowed_labels) if detected else False
        
        if detected and not is_match:
            return f"Image does not match {product}. Detected: {detected}. Please upload a clear image of the product."

    # ==================================================
    # 💰 REFUND FLOW (NO LLM)
    # ==================================================
    if decision == "refund":

        if not product:
            update_state(user_id, awaiting_product=True, awaiting_image=False)
            return "Which product are you referring to?"

        verification = verify_purchase.run({"user_id": user_id, "product_name": product})

        if "not found" in verification.lower():
            update_state(user_id, awaiting_product=False, awaiting_image=False)
            return "Product not found in your orders."

        if not order:
            order = get_order_for_product(user_id, product)

        if order and is_duplicate_order(order):
            status = normalize_status(order.get("status"))
            update_state(user_id, awaiting_product=False, awaiting_image=False)
            return f"This order has already been {status}."

        if not evidence.get("has_image"):
            update_state(user_id, awaiting_product=False, awaiting_image=True, last_product=product)
            return f"Please upload an image of the {product}."

        order_id = extract_order_id(verification)

        if risk == "low":
            result = process_refund.run({
                "user_id": user_id,
                "order_id": order_id,
                "reason": "Damaged product"
            })
            update_state(user_id, awaiting_product=False, awaiting_image=False)
            return result

        result = create_ticket.run({
            "user_id": user_id,
            "order_id": order_id,
            "issue": clean_input,
            "priority": "HIGH" if risk == "high" else "MEDIUM"
        })
        update_state(user_id, awaiting_product=False, awaiting_image=False)
        return result

    # ==================================================
    # 🔁 EXCHANGE FLOW (NO LLM)
    # ==================================================
    if decision == "exchange":

        if not product:
            update_state(user_id, awaiting_product=True, awaiting_image=False)
            return "Which product do you want to exchange?"

        verification = verify_purchase.run({"user_id": user_id, "product_name": product})

        if "not found" in verification.lower():
            update_state(user_id, awaiting_product=False, awaiting_image=False)
            return "Product not found in your orders."

        if not order:
            order = get_order_for_product(user_id, product)

        if order and is_duplicate_order(order):
            status = normalize_status(order.get("status"))
            update_state(user_id, awaiting_product=False, awaiting_image=False)
            return f"This order has already been {status}."

        if not evidence.get("has_image"):
            update_state(user_id, awaiting_product=False, awaiting_image=True, last_product=product)
            return f"Please upload an image of the {product}."

        order_id = extract_order_id(verification)

        create_exchange.run({
            "user_id": user_id,
            "order_id": order_id,
            "new_product": product
        })

        update_state(user_id, awaiting_product=False, awaiting_image=False)
        return "Your exchange request has been created."

    # ==================================================
    # 🔥 FALLBACK
    # ==================================================
    update_state(user_id, awaiting_product=False, awaiting_image=False)
    return "I couldn't understand your request. Please try again."