# tools/db_user_tool.py
# We need to verify that the user who enters is correct ( user id )

from langchain.tools import tool
from services.db_service import get_connection

@tool
def get_user_info(user_id: str) -> str:
    """
    Use this after verifying purchase.

    Returns:
    - email (for notifications)
    - complaint_count (for risk detection)
    - name (for personalized communication)

    If complaint_count is high → treat as high risk.
    """

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT name, email, complaint_count
        FROM users
        WHERE user_id = %s
    """, (user_id,))

    result = cur.fetchone()

    cur.close()
    conn.close()

    if not result:
        return "User not found"

    name, email, complaints = result

    return f"""
User Name: {name}
Email: {email}
Complaint Count: {complaints}
"""