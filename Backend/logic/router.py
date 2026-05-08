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

from services.db_service import fetch_one, execute_query
from services.vision_service import validate_image

import re


# ==================================================
# 🧠 LIGHTWEIGHT MEMORY
# ==================================================

CONVERSATION_STATE = {}


# ==================================================
# 🔧 HELPERS
# ==================================================

def extract_order_id(verification_text):
    match = re.search(r"Order ID:\s*(\w+)", verification_text)
    return match.group(1) if match else None


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
        if word.lower() in text.lower():
            return "Please upload a clearer image."

    return text


def normalize_status(value):
    return str(value or "").strip().lower()


def get_state(user_id):

    return CONVERSATION_STATE.setdefault(
        str(user_id),
        {
            "last_input": "",
            "last_intent": None,
            "last_product": None,
            "awaiting_product": False,
            "awaiting_image": False,
        }
    )


def update_state(user_id, **changes):

    state = get_state(user_id)
    state.update(changes)

    return state


# ==================================================
# 🧾 DATABASE HELPERS
# ==================================================

def get_user_profile(user_id):

    return fetch_one(
        """
        SELECT complaint_count
        FROM users
        WHERE user_id = %s
        """,
        (user_id,)
    ) or {}


def get_order_for_product(user_id, product_name):

    return fetch_one(
        """
        SELECT order_id, product_name, price, status
        FROM orders
        WHERE user_id = %s
        AND LOWER(product_name) = LOWER(%s)
        LIMIT 1
        """,
        (user_id, product_name)
    )


def get_order_by_id(user_id, order_id):

    return fetch_one(
        """
        SELECT order_id, product_name, price, status
        FROM orders
        WHERE user_id = %s
        AND order_id = %s
        LIMIT 1
        """,
        (user_id, order_id)
    )


def build_risk_context(user_id, order=None, evidence=None):

    user_profile = get_user_profile(user_id)

    complaint_count = user_profile.get("complaint_count", 0) or 0

    return {
        "price": float(order.get("price", 0) or 0) if order else 0,
        "user_history": complaint_count,
        "has_image": bool((evidence or {}).get("has_image")),
        "kb_found": True,
    }


def is_duplicate_order(order):

    status = normalize_status(order.get("status"))

    return status in ["refunded", "exchanged"]


# ==================================================
# 🔄 UPDATE ORDER STATUS
# ==================================================

def update_order_status(order_id, new_status):
    """Update the order status in the database"""
    try:
        execute_query(
            """
            UPDATE orders
            SET status = %s
            WHERE order_id = %s
            """,
            (new_status, order_id)
        )
        print(f"✅ Order {order_id} status updated to: {new_status}")
        return True
    except Exception as e:
        print(f"❌ Error updating order status: {e}")
        return False


# ==================================================
# 🔥 QUERY PROTECTION
# ==================================================

def contains_action_keywords(text):

    keywords = [
        "refund",
        "exchange",
        "return",
        "damaged",
        "broken"
    ]

    text = text.lower()

    return any(k in text for k in keywords)


# ==================================================
# 🚀 MAIN HANDLER
# ==================================================

def handle_request(
    user_id,
    user_input,
    image_path=None,
    selected_order_id=None,
    selected_product=None,
    selected_action=None
):

    state = get_state(user_id)

    # ==================================================
    # 🔥 CLEAN INPUT
    # ==================================================

    clean_input = str(user_input or "").strip()

    if (not clean_input or clean_input.lower() == "text") and image_path:
        clean_input = state.get("last_input") or "User uploaded an image."

    if not clean_input or clean_input.lower() == "text":
        return "Please describe your issue."

    # ==================================================
    # 🔥 DETECT INTENT
    # ==================================================

    intent = detect_intent(clean_input)

    if selected_action in ["refund", "exchange", "query"]:
        intent = selected_action

    evidence = analyze_evidence(clean_input, image_path)

    update_state(
        user_id,
        last_input=clean_input,
        last_intent=intent
    )

    # ==================================================
    # 🔥 IMAGE PROCESSING
    # ==================================================

    image_data = None

    if image_path:

        validation = validate_image(image_path)
        suspicious_message = validation.get(
            "message",
            "Image appears to be edited, AI-generated, or unclear. Please upload a real product photo."
        )

        if validation.get("type") == "image_rejected":
            return suspicious_message

        if validation.get("type") == "image_fake":
            return suspicious_message

        print("📸 Processing image:", image_path)

        image_data = process_image(image_path)

        print("🧠 Image Data:", image_data)

        if image_data.get("type") == "vision_unavailable":
            image_data = None

        # 🔥 ONLY BLOCK IF OBJECT MISSING
        if image_data and not image_data.get("object"):
            return suspicious_message

    # ==================================================
    # 🔥 PRODUCT EXTRACTION
    # ==================================================

    product = None
    order = None

    # selected order
    if selected_order_id:
        order = get_order_by_id(user_id, selected_order_id)

    # selected product
    if selected_product:
        product = selected_product

        if not order:
            order = get_order_for_product(user_id, selected_product)

    # extract dynamically
    if intent in ["refund", "exchange"]:

        try:

            if not product:

                orders = get_user_orders.run(user_id)

                product = extract_product(clean_input, orders)

                print("🧾 Product:", product)

                if product:
                    order = get_order_for_product(user_id, product)

                    update_state(
                        user_id,
                        last_product=product
                    )

        except Exception as e:
            print("❌ Product extraction error:", e)

        # fallback from memory
        if not product and state.get("last_product"):
            product = state.get("last_product")
            order = get_order_for_product(user_id, product)

    # ==================================================
    # 🔥 RISK ENGINE (AFTER ORDER)
    # ==================================================

    risk_context = build_risk_context(
        user_id=user_id,
        order=order,
        evidence=evidence
    )

    risk = classify_risk(
        evidence,
        image_data or {},
        risk_context
    )

    decision = decide_flow(intent, risk)

    print("Intent:", intent)
    print("Risk:", risk)
    print("Decision:", decision)

    # ==================================================
    # 🔥 PROTECT QUERY FLOW
    # ==================================================

    if decision == "query":

        if contains_action_keywords(clean_input):
            return "Please specify the product."

        response = query_flow(clean_input)

        # Update order status if a specific order was selected
        if selected_order_id:
            update_order_status(selected_order_id, "query_answered")

        update_state(
            user_id,
            awaiting_product=False,
            awaiting_image=False
        )

        return clean_response(response)

    # ==================================================
    # 🔥 IMAGE ↔ PRODUCT MATCHING
    # ==================================================

    if image_data and product:

        detected = image_data.get("object", "").lower()

        product_label_map = {
            "fan": ["fan", "scissors", "propeller"],
            "laptop": ["laptop", "computer", "keyboard"],
            "phone": ["phone", "smartphone", "iphone"],
            "headphones": ["headphones", "earbuds", "headset"],
            "shoes": ["shoe", "sneaker", "boot", "sandal"]
        }

        allowed_labels = product_label_map.get(
            product.lower(),
            [product.lower()]
        )

        is_match = any(
            label == detected or label in detected
            for label in allowed_labels
        )

        if detected and not is_match:
            if image_data.get("confidence", 0) < 0.4:
                return suspicious_message

            return (
                f"Image does not match {product}. "
                f"Detected: {detected}. "
                f"Please upload the correct product image."
            )

    # ==================================================
    # 💰 REFUND FLOW
    # ==================================================

    if decision == "refund":

        # missing product
        if not product:

            update_state(
                user_id,
                awaiting_product=True,
                awaiting_image=False
            )

            return "Which product are you referring to?"

        # no order
        if not order:

            verification = verify_purchase.run({
                "user_id": user_id,
                "product_name": product
            })

            if "not found" in verification.lower():

                update_state(
                    user_id,
                    awaiting_product=False,
                    awaiting_image=False
                )

                return "Product not found in your orders."

            order_id = extract_order_id(verification)

        else:

            verification = f"""
Order ID: {order['order_id']}
Product: {order['product_name']}
Status: {order['status']}
"""

            order_id = order["order_id"]

        # duplicate protection
        if order and is_duplicate_order(order):

            status = normalize_status(order.get("status"))

            update_state(
                user_id,
                awaiting_product=False,
                awaiting_image=False
            )

            return f"This order has already been {status}."

        # image required
        if not evidence.get("has_image"):

            update_state(
                user_id,
                awaiting_product=False,
                awaiting_image=True,
                last_product=product
            )

            return f"Please upload an image of the {product}."

        # LOW RISK → AUTO REFUND
        if risk == "low":

            result = process_refund.run({
                "user_id": user_id,
                "order_id": order_id,
                "reason": "Damaged product"
            })

            # Update order status to refunded
            update_order_status(order_id, "refunded")

            update_state(
                user_id,
                awaiting_product=False,
                awaiting_image=False
            )

            return result

        # HIGH/MEDIUM → TICKET
        # ensure ai_verdict is a string and confidence is a float to satisfy validators
        ai_verdict_val = ""
        confidence_val = 0.0
        if image_data:
            ai_verdict_val = str(image_data.get("object") or "")
            try:
                confidence_val = float(image_data.get("confidence") or 0.0)
            except Exception:
                confidence_val = 0.0

        refund_val = 0.0
        try:
            refund_val = float(order["price"]) if order and order.get("price") is not None else 0.0
        except Exception:
            refund_val = 0.0

        image_url_val = str(image_path) if image_path else ""

        result = create_ticket.run({
            "user_id": user_id,
            "order_id": order_id,
            "issue": clean_input,
            "priority": "HIGH" if risk == "high" else "MEDIUM",
            "customer_id": user_id,
            "image_url": image_url_val,
            "ai_verdict": ai_verdict_val,
            "confidence": confidence_val,
            "refund_amount": refund_val,
        })

        # Update order status to pending refund
        update_order_status(order_id, "pending_refund")

        update_state(
            user_id,
            awaiting_product=False,
            awaiting_image=False
        )

        return result

    # ==================================================
    # 🔁 EXCHANGE FLOW
    # ==================================================

    if decision == "exchange":

        # missing product
        if not product:

            update_state(
                user_id,
                awaiting_product=True,
                awaiting_image=False
            )

            return "Which product do you want to exchange?"

        # no order
        if not order:

            verification = verify_purchase.run({
                "user_id": user_id,
                "product_name": product
            })

            if "not found" in verification.lower():

                update_state(
                    user_id,
                    awaiting_product=False,
                    awaiting_image=False
                )

                return "Product not found in your orders."

            order_id = extract_order_id(verification)

        else:

            verification = f"""
Order ID: {order['order_id']}
Product: {order['product_name']}
Status: {order['status']}
"""

            order_id = order["order_id"]

        # duplicate protection
        if order and is_duplicate_order(order):

            status = normalize_status(order.get("status"))

            update_state(
                user_id,
                awaiting_product=False,
                awaiting_image=False
            )

            return f"This order has already been {status}."

        # image required
        if not evidence.get("has_image"):

            update_state(
                user_id,
                awaiting_product=False,
                awaiting_image=True,
                last_product=product
            )

            return f"Please upload an image of the {product}."

        # create exchange
        create_exchange.run({
            "user_id": user_id,
            "order_id": order_id,
            "new_product": product
        })

        # Update order status to exchanged
        update_order_status(order_id, "exchanged")

        update_state(
            user_id,
            awaiting_product=False,
            awaiting_image=False
        )

        return "Your exchange request has been created."

    # ==================================================
    # 🔥 FALLBACK
    # ==================================================

    update_state(
        user_id,
        awaiting_product=False,
        awaiting_image=False
    )

    return "I couldn't understand your request."