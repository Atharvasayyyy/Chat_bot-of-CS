# tools/db_verification_tool.py
#  i will give u the user id and the product name that will help me to check it it exsist and remove the required data

from langchain.tools import tool
from services.db_service import get_connection

@tool
def verify_purchase(user_id: str, product_name: str) -> str:
    """
    MUST be used before any refund or exchange.

    Use this to check if the user has actually purchased the product.
    
    If purchase is not found:
    - DO NOT proceed with refund
    - Inform user politely
    """

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT order_id, price
        FROM orders
        WHERE user_id = %s AND LOWER(product_name) = LOWER(%s)
        LIMIT 1
    """, (user_id, product_name))

    result = cur.fetchone()

    cur.close()
    conn.close()

    if not result:
        return "Purchase not found"

    order_id, price = result

    return f"""
Purchase Verified
Order ID: {order_id}
Product: {product_name}
Price: {price}
"""