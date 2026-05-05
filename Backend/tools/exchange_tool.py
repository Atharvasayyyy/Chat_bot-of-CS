from langchain.tools import tool
from services.db_service import execute_query, fetch_one
from services.email_service import send_email


@tool
def create_exchange(user_id: str, order_id: str, new_product: str) -> str:
    """
    Create an exchange request for a user.

    Args:
        user_id (str): user id
        order_id (str): order id
        new_product (str): product requested for exchange

    Returns:
        str: confirmation message
    """

    # 🔥 Fetch user email
    user = fetch_one("SELECT email FROM users WHERE user_id = %s", (user_id,))
    if not user:
        return "User not found"

    email = user["email"]

    # 🔥 Insert exchange request
    execute_query(
        """
        INSERT INTO exchanges (user_id, order_id, new_product, status)
        VALUES (%s, %s, %s, %s)
        """,
        (user_id, order_id, new_product, "PENDING")
    )

    # 🔥 Update order status immediately for the exchange flow
    execute_query(
        "UPDATE orders SET status = 'EXCHANGED' WHERE order_id = %s",
        (order_id,)
    )

    # 🔥 Notify merchant (for now simulate)
    print(f"📦 Exchange request sent to merchant for order {order_id}")

    # 🔥 Email user
    send_email(
        to=email,
        subject="Exchange Request Created",
        content=f"""
Your exchange request has been created.

Order ID: {order_id}
Requested Product: {new_product}

Status: PENDING
"""
    )

    return f"Exchange request created successfully. Status: PENDING"