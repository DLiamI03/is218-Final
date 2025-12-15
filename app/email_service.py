"""
Email Service for User Verification
Supports both real email (SendGrid/Mailgun) and mock mode for development
"""
import os
import secrets
from datetime import datetime, timedelta
from typing import Optional
import logging

logger = logging.getLogger(__name__)

# Email configuration
EMAIL_ENABLED = os.getenv("EMAIL_ENABLED", "false").lower() == "true"
EMAIL_PROVIDER = os.getenv("EMAIL_PROVIDER", "mock")  # "sendgrid", "mailgun", or "mock"
FROM_EMAIL = os.getenv("FROM_EMAIL", "noreply@fittrack.app")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:8000")

# Verification token storage (in-memory for demo, use Redis in production)
_verification_tokens = {}


def generate_verification_token(user_id: str) -> str:
    """Generate a secure verification token for user."""
    token = secrets.token_urlsafe(32)
    expires_at = datetime.utcnow() + timedelta(hours=24)
    
    _verification_tokens[token] = {
        "user_id": user_id,
        "expires_at": expires_at,
        "used": False
    }
    
    return token


def verify_token(token: str) -> Optional[str]:
    """Verify a token and return user_id if valid."""
    token_data = _verification_tokens.get(token)
    
    if not token_data:
        return None
    
    if token_data["used"]:
        logger.warning(f"Token already used: {token}")
        return None
    
    if datetime.utcnow() > token_data["expires_at"]:
        logger.warning(f"Token expired: {token}")
        return None
    
    # Mark token as used
    token_data["used"] = True
    
    return token_data["user_id"]


def send_verification_email(email: str, username: str, token: str) -> bool:
    """Send verification email to user."""
    verification_url = f"{FRONTEND_URL}/verify?token={token}"
    
    subject = "Verify your FitTrack account"
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%); color: white; padding: 30px; text-align: center; border-radius: 8px 8px 0 0; }}
            .content {{ background: #f8f9fa; padding: 30px; border-radius: 0 0 8px 8px; }}
            .button {{ display: inline-block; background: #6366f1; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
            .footer {{ text-align: center; margin-top: 20px; color: #6b7280; font-size: 14px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🏋️ Welcome to FitTrack!</h1>
            </div>
            <div class="content">
                <p>Hi <strong>{username}</strong>,</p>
                <p>Thanks for signing up! Please verify your email address to activate your account.</p>
                <p style="text-align: center;">
                    <a href="{verification_url}" class="button">Verify Email Address</a>
                </p>
                <p>Or copy and paste this link into your browser:</p>
                <p style="word-break: break-all; background: white; padding: 10px; border-radius: 5px;">{verification_url}</p>
                <p><strong>This link will expire in 24 hours.</strong></p>
                <p>If you didn't create an account with FitTrack, you can safely ignore this email.</p>
            </div>
            <div class="footer">
                <p>FitTrack - AI-Powered Fitness & Nutrition Tracker</p>
                <p>© 2025 FitTrack. All rights reserved.</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    if not EMAIL_ENABLED or EMAIL_PROVIDER == "mock":
        # Mock mode - just log the email
        logger.info(f"📧 [MOCK EMAIL] To: {email}")
        logger.info(f"Subject: {subject}")
        logger.info(f"Verification URL: {verification_url}")
        logger.info("Email sending is in MOCK mode. Set EMAIL_ENABLED=true to send real emails.")
        return True
    
    elif EMAIL_PROVIDER == "sendgrid":
        return _send_via_sendgrid(email, subject, html_content)
    
    elif EMAIL_PROVIDER == "mailgun":
        return _send_via_mailgun(email, subject, html_content)
    
    else:
        logger.error(f"Unknown email provider: {EMAIL_PROVIDER}")
        return False


def _send_via_sendgrid(to_email: str, subject: str, html_content: str) -> bool:
    """Send email via SendGrid."""
    try:
        import sendgrid
        from sendgrid.helpers.mail import Mail, Email, To, Content
        
        sg = sendgrid.SendGridAPIClient(api_key=os.getenv("SENDGRID_API_KEY"))
        
        message = Mail(
            from_email=Email(FROM_EMAIL),
            to_emails=To(to_email),
            subject=subject,
            html_content=Content("text/html", html_content)
        )
        
        response = sg.send(message)
        logger.info(f"Email sent via SendGrid: {response.status_code}")
        return response.status_code == 202
        
    except Exception as e:
        logger.error(f"SendGrid error: {e}")
        return False


def _send_via_mailgun(to_email: str, subject: str, html_content: str) -> bool:
    """Send email via Mailgun."""
    try:
        import requests
        
        domain = os.getenv("MAILGUN_DOMAIN")
        api_key = os.getenv("MAILGUN_API_KEY")
        
        response = requests.post(
            f"https://api.mailgun.net/v3/{domain}/messages",
            auth=("api", api_key),
            data={
                "from": FROM_EMAIL,
                "to": to_email,
                "subject": subject,
                "html": html_content
            }
        )
        
        logger.info(f"Email sent via Mailgun: {response.status_code}")
        return response.status_code == 200
        
    except Exception as e:
        logger.error(f"Mailgun error: {e}")
        return False


def send_password_reset_email(email: str, username: str, token: str) -> bool:
    """Send password reset email to user."""
    reset_url = f"{FRONTEND_URL}/reset-password?token={token}"
    
    subject = "Reset your FitTrack password"
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%); color: white; padding: 30px; text-align: center; border-radius: 8px 8px 0 0; }}
            .content {{ background: #f8f9fa; padding: 30px; border-radius: 0 0 8px 8px; }}
            .button {{ display: inline-block; background: #6366f1; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
            .footer {{ text-align: center; margin-top: 20px; color: #6b7280; font-size: 14px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🔐 Password Reset Request</h1>
            </div>
            <div class="content">
                <p>Hi <strong>{username}</strong>,</p>
                <p>We received a request to reset your password. Click the button below to create a new password:</p>
                <p style="text-align: center;">
                    <a href="{reset_url}" class="button">Reset Password</a>
                </p>
                <p>Or copy and paste this link into your browser:</p>
                <p style="word-break: break-all; background: white; padding: 10px; border-radius: 5px;">{reset_url}</p>
                <p><strong>This link will expire in 24 hours.</strong></p>
                <p>If you didn't request a password reset, you can safely ignore this email.</p>
            </div>
            <div class="footer">
                <p>FitTrack - AI-Powered Fitness & Nutrition Tracker</p>
                <p>© 2025 FitTrack. All rights reserved.</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    if not EMAIL_ENABLED or EMAIL_PROVIDER == "mock":
        logger.info(f"📧 [MOCK EMAIL] Password Reset To: {email}")
        logger.info(f"Reset URL: {reset_url}")
        return True
    
    elif EMAIL_PROVIDER == "sendgrid":
        return _send_via_sendgrid(email, subject, html_content)
    
    elif EMAIL_PROVIDER == "mailgun":
        return _send_via_mailgun(email, subject, html_content)
    
    return False
