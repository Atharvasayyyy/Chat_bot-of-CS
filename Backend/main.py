import os
import shutil
from uuid import uuid4

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from services.db_service import execute_query, fetch_one, fetch_all
from tools.refund_tool import process_refund
from logic.router import handle_request

app = FastAPI()

# ==================================================
# 🌐 CORS (FOR REACT)
# ==================================================
# Get allowed origins from environment or use defaults
allowed_origins = [
    origin.strip().rstrip("/")
    for origin in os.getenv(
        "ALLOWED_ORIGINS",
        "http://localhost:3000,http://localhost:5173",
    ).split(",")
    if origin.strip()
]
# Always allow the frontend URL if provided
frontend_url = os.getenv("FRONTEND_URL")
if frontend_url:
    allowed_origins.append(frontend_url.strip().rstrip("/"))

for port in (3000, 5173):
    allowed_origins.append(f"http://127.0.0.1:{port}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=sorted(set(allowed_origins)),  # Remove duplicates
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "service": "customer-support-api",
        "status": "ok",
        "endpoints": [
            "/health",
            "/chat",
            "/dashboard",
            "/database",
            "/orders/{user_id}",
            "/admin/ticket/update",
            "/admin/exchange/update",
            "/profile",
        ],
    }

# ==================================================
# 📂 IMAGE STORAGE
# ==================================================
UPLOAD_DIR = "temp"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# ==================================================
# � HEALTH CHECK ENDPOINT
# ==================================================
@app.get("/health")
def health_check():
    """
    Simple health check to verify backend and database are accessible.
    """
    import logging
    logger = logging.getLogger(__name__)
    
    try:
        # Try to execute a simple query
        result = fetch_one("SELECT 1 as ok")
        
        if result:
            logger.info("✓ Database connection OK")
            return {
                "status": "ok",
                "service": "customer-support-api",
                "database": "connected"
            }
        else:
            logger.warning("Database query returned no result")
            return {
                "status": "degraded",
                "service": "customer-support-api",
                "database": "query_empty"
            }
    except Exception as e:
        logger.exception("Health check failed: %s", e)
        return {
            "status": "error",
            "service": "customer-support-api",
            "database": "disconnected",
            "error": str(e)
        }


# ==================================================
# 🔐 PROFILE (LIGHTWEIGHT)
# ==================================================
@app.get("/profile")
def profile():
    # Minimal profile endpoint to support frontend profile-refresh logic.
    # Returns no user when unauthenticated; frontends can adapt accordingly.
    return {
        "user": None,
        "authenticated": False,
        "message": "No active session"
    }

# ==================================================
# �🚀 CHAT ENDPOINT (JSON + IMAGE SUPPORT)
# ==================================================
@app.post("/chat")
async def chat(request: Request):
    try:
        content_type = request.headers.get("content-type", "")
        user_id = None
        message = None
        image_url = None
        selected_order_id = None
        selected_product = None
        selected_action = None

        if "multipart/form-data" in content_type:
            form = await request.form()
            user_id = form.get("user_id")
            message = form.get("message")
            selected_order_id = form.get("selected_order_id")
            selected_product = form.get("selected_product")
            selected_action = form.get("selected_action")
            image = form.get("image")

            if image and getattr(image, "filename", None):
                ext = image.filename.split(".")[-1]
                filename = f"{uuid4()}.{ext}"
                file_path = os.path.join(UPLOAD_DIR, filename)

                with open(file_path, "wb") as buffer:
                    shutil.copyfileobj(image.file, buffer)

                image_url = file_path
                print("📸 Image saved:", image_url)
        else:
            payload = await request.json()
            user_id = payload.get("user_id")
            message = payload.get("message")
            selected_order_id = payload.get("selected_order_id")
            selected_product = payload.get("selected_product")
            selected_action = payload.get("selected_action")

        response = handle_request(
            user_id=user_id,
            user_input=message,
            image_path=image_url,
            selected_order_id=selected_order_id,
            selected_product=selected_product,
            selected_action=selected_action,
        )

        if isinstance(response, dict):
            return response

        return {
            "type": "text",
            "message": response
        }

    except Exception as e:
        print("❌ API Error:", e)
        return {
            "type": "error",
            "message": "Something went wrong on the server."
        }


# ==================================================
# 📊 DASHBOARD (UNIFIED)
# ==================================================
@app.get("/dashboard")
def get_dashboard():
    tickets = fetch_all("SELECT * FROM tickets ORDER BY created_at DESC")
    refunds = fetch_all("SELECT * FROM refunds ORDER BY created_at DESC")
    exchanges = fetch_all("SELECT * FROM exchanges ORDER BY created_at DESC")

    return {
        "tickets": tickets,
        "refunds": refunds,
        "exchanges": exchanges
    }


# ==================================================
# 🗃️ DATABASE TABLES (ADMIN VIEW)
# ==================================================
@app.get("/database")
def get_database_tables():
    users = fetch_all("SELECT * FROM users ORDER BY created_at DESC")
    orders = fetch_all("SELECT * FROM orders ORDER BY created_at DESC")
    tickets = fetch_all("SELECT * FROM tickets ORDER BY created_at DESC")
    exchanges = fetch_all("SELECT * FROM exchanges ORDER BY created_at DESC")
    refunds = fetch_all("SELECT * FROM refunds ORDER BY created_at DESC")

    return {
        "users": users,
        "orders": orders,
        "tickets": tickets,
        "exchanges": exchanges,
        "refunds": refunds,
    }


# ==================================================
# 📦 ORDERS BY USER (WIZARD FLOW)
# ==================================================
@app.get("/orders/{user_id}")
def get_orders_by_user(user_id: str):
    orders = fetch_all(
        """
        SELECT order_id, product_name, price, status, created_at
        FROM orders
        WHERE user_id = %s
        ORDER BY created_at DESC
        """,
        (user_id,)
    )

    return {
        "user_id": user_id,
        "orders": orders,
    }


# ==================================================
# 🎫 TICKET UPDATE (ADMIN)
# ==================================================
@app.post("/admin/ticket/update")
def update_ticket(ticket_id: str, status: str):

    ticket = fetch_one(
        "SELECT order_id FROM tickets WHERE ticket_id = %s",
        (ticket_id,)
    )

    if not ticket:
        return {"message": "Ticket not found"}

    order_id = ticket["order_id"]

    order = fetch_one(
        "SELECT user_id FROM orders WHERE order_id = %s",
        (order_id,)
    )
    user_id = order["user_id"] if order else None

    # 🔥 Update status
    execute_query(
        "UPDATE tickets SET status = %s WHERE ticket_id = %s",
        (status, ticket_id)
    )

    # ==================================================
    # 🔥 AUTO REFUND ON APPROVAL
    # ==================================================
    if status == "APPROVED" and user_id:

        refund_result = process_refund.run({
            "user_id": user_id,
            "order_id": order_id,
            "reason": "Approved by admin"
        })

        return {
            "type": "refund_processed",
            "message": "Ticket approved & refund processed",
            "refund": refund_result
        }

    if status == "APPROVED" and not user_id:
        return {
            "type": "ticket_update",
            "message": "Ticket approved, but refund could not be auto-processed (missing user mapping)."
        }

    return {
        "type": "ticket_update",
        "message": f"Ticket {status.lower()}"
    }


# ==================================================
# 📦 EXCHANGE UPDATE (ADMIN)
# ==================================================
@app.post("/admin/exchange/update")
def update_exchange(exchange_id: int, status: str):

    exchange = fetch_one(
        "SELECT user_id, order_id, new_product FROM exchanges WHERE exchange_id = %s",
        (exchange_id,)
    )

    if not exchange:
        return {"message": "Exchange not found"}

    execute_query(
        "UPDATE exchanges SET status = %s WHERE exchange_id = %s",
        (status, exchange_id)
    )

    return {
        "type": "exchange_update",
        "message": f"Exchange {status.lower()}",
        "exchange": {
            "exchange_id": exchange_id,
            "user_id": exchange["user_id"],
            "order_id": exchange["order_id"],
            "new_product": exchange["new_product"],
            "status": status,
        }
    }