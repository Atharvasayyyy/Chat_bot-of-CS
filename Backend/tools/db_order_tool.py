# tools/db_order_tool.py
# these will helpl me to attach thaat order details to the ticket and exchange tool

from langchain.tools import tool
from services.db_service import get_connection

@tool
def get_user_orders(user_id: str) -> str:
    """
    Fetch all orders for a user.
    """

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT order_id, product_name, price, status
        FROM orders
        WHERE user_id = %s
    """, (user_id,))

    rows = cur.fetchall()

    cur.close()
    conn.close()

    if not rows:
        return "No orders found"

    output = "User Orders:\n"

    for r in rows:
        output += f"""
Order ID: {r[0]}
Product: {r[1]}
Price: {r[2]}
Status: {r[3]}
"""

    return output