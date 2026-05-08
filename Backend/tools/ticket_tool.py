from langchain.tools import tool
from uuid import uuid4
from services.db_service import execute_query, fetch_one
from services.email_service import send_email


def _ensure_ticket_columns():
    # Handle legacy DBs where tickets table exists without newer columns.
    execute_query("ALTER TABLE tickets ADD COLUMN IF NOT EXISTS user_id VARCHAR")
    execute_query("ALTER TABLE tickets ADD COLUMN IF NOT EXISTS order_id VARCHAR")
    execute_query("ALTER TABLE tickets ADD COLUMN IF NOT EXISTS issue TEXT")
    execute_query("ALTER TABLE tickets ADD COLUMN IF NOT EXISTS status VARCHAR")
    execute_query("ALTER TABLE tickets ADD COLUMN IF NOT EXISTS priority VARCHAR")
    execute_query("ALTER TABLE tickets ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP")


def _generate_ticket_id() -> str:
    return str(uuid4())


@tool
def create_ticket(
    user_id: str,
    order_id: str,
    issue: str,
    priority: str,
    customer_id: str = None,
    image_url: str = None,
    ai_verdict: str = None,
    confidence: float = None,
    refund_amount: float = None,
) -> str:
    """
    Create a support ticket for high-risk cases.

    Args:
        user_id (str)
        order_id (str)
        issue (str)
        priority (str)
        customer_id (str, optional)
        image_url (str, optional)
        ai_verdict (str, optional)
        confidence (float, optional)
        refund_amount (float, optional)

    Returns:
        str
    """

    # Align schema first for compatibility with older deployments.
    try:
        _ensure_ticket_columns()
    except Exception as exc:
        print("❌ Ticket schema sync failed:", exc)

    # Persist first; only return success when insertion actually works.
    try:
        ticket_id = _generate_ticket_id()
        created_ticket = execute_query(
            """
            INSERT INTO tickets (
                ticket_id, user_id, order_id, issue, status, priority,
                customer_id, image_url, ai_verdict, confidence, refund_amount, created_at
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
            RETURNING ticket_id, status, priority
            """,
            (
                ticket_id,
                user_id,
                order_id,
                issue,
                "UNDER_REVIEW",
                priority,
                customer_id or user_id,
                image_url,
                ai_verdict,
                confidence,
                refund_amount,
            ),
            fetch_result=True,
        )
    except Exception as exc:
        print("❌ Ticket creation failed:", exc)
        return "Unable to create support ticket right now. Please try again shortly."

    if not created_ticket:
        return "Unable to create support ticket right now. Please try again shortly."

    ticket_id, status, priority_value = created_ticket

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

    return f"Support ticket #{ticket_id} created. Status: {status} | Priority: {priority_value}"