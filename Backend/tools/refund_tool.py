from langchain.tools import tool
from services.db_service import execute_query, fetch_one
from services.email_service import send_email


@tool
def process_refund(user_id: str, order_id: str, reason: str) -> str:
    """
    Process a refund for a given user and order.

    Args:
        user_id (str): ID of the user
        order_id (str): Order ID to refund
        reason (str): Reason for refund

    Returns:
        str: Confirmation message after refund processing
    """

    # 🔥 Fetch user email
    user_query = "SELECT email FROM users WHERE user_id = %s"
    user = fetch_one(user_query, (user_id,))

    if not user:
        return "User not found"

    email = user["email"]

    # 🔥 Fetch order
    order_query = """
    SELECT product_name, price, status
    FROM orders
    WHERE order_id = %s AND user_id = %s
    """
    order = fetch_one(order_query, (order_id, user_id))

    if not order:
        return "Order not found"

    if str(order["status"]).upper() == "REFUNDED":
        return "Refund already processed"

    product = order["product_name"]
    amount = order["price"]

    # 🔥 Insert refund record
    execute_query(
        "INSERT INTO refunds (user_id, order_id, reason, status) VALUES (%s, %s, %s, %s)",
        (user_id, order_id, reason, "APPROVED")
    )

    # 🔥 Update order
    execute_query(
        "UPDATE orders SET status = 'REFUNDED' WHERE order_id = %s",
        (order_id,)
    )
    
    # AFTER inserting refund

    # 🔥 Send email
    send_email(
        to=email,
        subject="Refund Approved",
        content=f"Refund for {product} (₹{amount}) has been processed."
    )

    return f"Refund of ₹{amount} processed successfully"