# services/email_service.py
# tehse servicce is not active as i do not get the api of these so kindly check
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def send_email(to, subject, content):
    try:
        message = Mail(
            from_email=os.getenv("FROM_EMAIL"),
            to_emails=to,
            subject=subject,
            plain_text_content=content
        )

        sg = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))
        sg.send(message)

        return True
    except Exception as e:
        print("Email Error:", e)
        return False