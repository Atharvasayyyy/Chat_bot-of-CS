from langchain.tools import tool
from services.db_service import execute_query, fetch_one
from services.email_service import send_email


@tool
def create_ticket(user_id: str, order_id: str, issue: str, priority: str) -> str:
    """
    Create a support ticket for high-risk cases.

    Args:
        user_id (str)
        order_id (str)
        issue (str)
        priority (str)

    Returns:
        str
    """

    # 🔥 Insert ticket
    execute_query(
        """
        INSERT INTO tickets (user_id, order_id, issue, status, priority)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (user_id, order_id, issue, "UNDER_REVIEW", priority)
    )

    # 🔥 Get user email
    user = fetch_one("SELECT email FROM users WHERE user_id = %s", (user_id,))
    email = user["email"] if user else None

    # 🔥 Send email (user)
    if email:
        send_email(
            to=email,
            subject="Support Ticket Created",
            content=f"""
Your request is under review.

Order ID: {order_id}
Issue: {issue}
Priority: {priority}

Our team will contact you shortly.
"""
        )

    # 🔥 Notify merchant (for now log)
    print(f"📩 Merchant notified for ticket: {order_id}")

    return f"Support ticket created. Status: UNDER REVIEW | Priority: {priority}"