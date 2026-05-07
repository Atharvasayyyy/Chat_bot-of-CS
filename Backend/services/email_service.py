# services/email_service.py
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def send_email(to, subject, content, html_content=None):
    """
    Send email using SendGrid API
    
    Args:
        to (str): Recipient email address
        subject (str): Email subject
        content (str): Plain text content
        html_content (str, optional): HTML content for email
        
    Returns:
        dict: Response status and details, or error info
    """
    try:
        # Validate required environment variable
        api_key = os.environ.get('SENDGRID_API_KEY')
        if not api_key:
            print("Error: SENDGRID_API_KEY environment variable not set")
            return {"success": False, "error": "Missing SENDGRID_API_KEY"}
        
        from_email = os.environ.get('FROM_EMAIL', 'noreply@example.com')
        
        message = Mail(
            from_email=from_email,
            to_emails=to,
            subject=subject,
            plain_text_content=content,
            html_content=html_content
        )

        sg = SendGridAPIClient(api_key)
        # Uncomment the line below if you are sending mail using a regional EU subuser
        # sg.set_sendgrid_data_residency("eu")
        response = sg.send(message)
        
        return {
            "success": True,
            "status_code": response.status_code,
            "message": "Email sent successfully"
        }
        
    except Exception as e:
        print(f"Email Error: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }
        