# tools/notification_tool.py
from langchain.tools import tool
from services.email_service import send_email

@tool
def send_notification(to: str, subject: str, message: str) -> str:
    """
    Send email notification.
    """

    send_email(to, subject, message)

    return "Notification sent"