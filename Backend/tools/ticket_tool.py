from langchain.tools import tool
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


def _get_next_ticket_id():
    row = fetch_one("SELECT COALESCE(MAX(ticket_id), 0) + 1 AS next_ticket_id FROM tickets")
    return int(row["next_ticket_id"]) if row and row.get("next_ticket_id") is not None else 1


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

    # Align schema first for compatibility with older deployments.
    try:
        _ensure_ticket_columns()
    except Exception as exc:
        print("❌ Ticket schema sync failed:", exc)

    # Persist first; only return success when insertion actually works.
    try:
        ticket_id = _get_next_ticket_id()
        created_ticket = execute_query(
            """
            INSERT INTO tickets (ticket_id, user_id, order_id, issue, status, priority)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING ticket_id, status, priority
            """,
            (ticket_id, user_id, order_id, issue, "UNDER_REVIEW", priority),
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