---
name: email-integration
description: Implement email functionality using FastAPI-Mail for password reset, notifications, and transactional emails. Use when setting up email services or notification systems.
allowed-tools: Read, Write, Edit, Bash, Glob
---

You implement email functionality for the QA Team Portal using FastAPI-Mail.

## Requirements from PROJECT_PLAN.md

- Email service for password reset flow
- Transactional emails for notifications
- SMTP configuration
- Email templates
- Queue handling (optional)

## Implementation

### 1. Install Dependencies

```bash
cd backend
uv pip install fastapi-mail python-multipart jinja2
```

### 2. Email Configuration

**Location:** `backend/app/core/config.py`

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Email Configuration
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: int = 587
    MAIL_SERVER: str
    MAIL_FROM_NAME: str = "QA Team Portal"
    MAIL_TLS: bool = True
    MAIL_SSL: bool = False
    USE_CREDENTIALS: bool = True
    VALIDATE_CERTS: bool = True

    class Config:
        env_file = ".env"

settings = Settings()
```

**Environment Variables (.env):**

```bash
# Email Configuration
MAIL_USERNAME=noreply@evoketech.com
MAIL_PASSWORD=your-smtp-password
MAIL_FROM=noreply@evoketech.com
MAIL_PORT=587
MAIL_SERVER=smtp.gmail.com
MAIL_FROM_NAME=QA Team Portal
MAIL_TLS=true
MAIL_SSL=false
```

### 3. Email Service

**Location:** `backend/app/services/email_service.py`

```python
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from fastapi import BackgroundTasks
from pathlib import Path
from typing import List, Dict, Any
from app.core.config import settings
from jinja2 import Environment, FileSystemLoader
import logging

logger = logging.getLogger(__name__)

# Email configuration
conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
    MAIL_STARTTLS=settings.MAIL_TLS,
    MAIL_SSL_TLS=settings.MAIL_SSL,
    USE_CREDENTIALS=settings.USE_CREDENTIALS,
    VALIDATE_CERTS=settings.VALIDATE_CERTS,
    TEMPLATE_FOLDER=Path(__file__).parent.parent / 'templates' / 'email'
)

fm = FastMail(conf)

class EmailService:
    """Service for sending emails."""

    @staticmethod
    async def send_email(
        recipients: List[str],
        subject: str,
        body: str,
        html: str = None,
        background_tasks: BackgroundTasks = None
    ):
        """
        Send email to recipients.

        Args:
            recipients: List of recipient email addresses
            subject: Email subject
            body: Plain text body
            html: HTML body (optional)
            background_tasks: FastAPI background tasks
        """
        message = MessageSchema(
            subject=subject,
            recipients=recipients,
            body=body,
            subtype=MessageType.html if html else MessageType.plain
        )

        try:
            if background_tasks:
                background_tasks.add_task(fm.send_message, message)
            else:
                await fm.send_message(message)

            logger.info(f"Email sent to {', '.join(recipients)}: {subject}")
            return True
        except Exception as e:
            logger.error(f"Failed to send email: {str(e)}")
            return False

    @staticmethod
    async def send_template_email(
        recipients: List[str],
        subject: str,
        template_name: str,
        template_data: Dict[str, Any],
        background_tasks: BackgroundTasks = None
    ):
        """
        Send email using Jinja2 template.

        Args:
            recipients: List of recipient email addresses
            subject: Email subject
            template_name: Template filename (e.g., 'password_reset.html')
            template_data: Data to pass to template
            background_tasks: FastAPI background tasks
        """
        message = MessageSchema(
            subject=subject,
            recipients=recipients,
            template_body=template_data,
            subtype=MessageType.html
        )

        try:
            if background_tasks:
                background_tasks.add_task(
                    fm.send_message,
                    message,
                    template_name=template_name
                )
            else:
                await fm.send_message(message, template_name=template_name)

            logger.info(f"Template email sent to {', '.join(recipients)}: {subject}")
            return True
        except Exception as e:
            logger.error(f"Failed to send template email: {str(e)}")
            return False

    @staticmethod
    async def send_password_reset_email(
        email: str,
        reset_token: str,
        background_tasks: BackgroundTasks = None
    ):
        """Send password reset email with link."""
        reset_url = f"{settings.FRONTEND_URL}/reset-password?token={reset_token}"

        template_data = {
            "reset_url": reset_url,
            "expiry_minutes": 15,
            "support_email": settings.MAIL_FROM
        }

        return await EmailService.send_template_email(
            recipients=[email],
            subject="Password Reset Request",
            template_name="password_reset.html",
            template_data=template_data,
            background_tasks=background_tasks
        )

    @staticmethod
    async def send_welcome_email(
        email: str,
        name: str,
        background_tasks: BackgroundTasks = None
    ):
        """Send welcome email to new user."""
        template_data = {
            "name": name,
            "login_url": f"{settings.FRONTEND_URL}/admin/login",
            "support_email": settings.MAIL_FROM
        }

        return await EmailService.send_template_email(
            recipients=[email],
            subject="Welcome to QA Team Portal",
            template_name="welcome.html",
            template_data=template_data,
            background_tasks=background_tasks
        )

    @staticmethod
    async def send_account_locked_email(
        email: str,
        name: str,
        background_tasks: BackgroundTasks = None
    ):
        """Send email when account is locked."""
        template_data = {
            "name": name,
            "unlock_time": "30 minutes",
            "support_email": settings.MAIL_FROM
        }

        return await EmailService.send_template_email(
            recipients=[email],
            subject="Account Locked - QA Team Portal",
            template_name="account_locked.html",
            template_data=template_data,
            background_tasks=background_tasks
        )

    @staticmethod
    async def send_test_email(recipient: str):
        """Send test email to verify configuration."""
        return await EmailService.send_email(
            recipients=[recipient],
            subject="Test Email - QA Team Portal",
            body="This is a test email from QA Team Portal. Email configuration is working correctly!"
        )
```

### 4. Email Templates

**Location:** `backend/app/templates/email/base.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ subject }}</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
        }
        .header {
            background: linear-gradient(135deg, #0066CC 0%, #0052A3 100%);
            color: white;
            padding: 30px;
            text-align: center;
            border-radius: 8px 8px 0 0;
        }
        .content {
            background: #ffffff;
            padding: 30px;
            border: 1px solid #e5e7eb;
            border-top: none;
        }
        .button {
            display: inline-block;
            background: #0066CC;
            color: white !important;
            padding: 12px 24px;
            text-decoration: none;
            border-radius: 6px;
            margin: 20px 0;
            font-weight: 600;
        }
        .button:hover {
            background: #0052A3;
        }
        .footer {
            background: #f9fafb;
            padding: 20px;
            text-align: center;
            font-size: 12px;
            color: #6b7280;
            border-radius: 0 0 8px 8px;
        }
        .divider {
            border-top: 1px solid #e5e7eb;
            margin: 20px 0;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1 style="margin: 0;">QA Team Portal</h1>
        <p style="margin: 10px 0 0 0; opacity: 0.9;">Evoke Technologies</p>
    </div>
    <div class="content">
        {% block content %}{% endblock %}
    </div>
    <div class="footer">
        <p>This email was sent by QA Team Portal</p>
        <p>If you have questions, contact us at {{ support_email }}</p>
        <div class="divider"></div>
        <p>&copy; 2025 Evoke Technologies. All rights reserved.</p>
    </div>
</body>
</html>
```

**Location:** `backend/app/templates/email/password_reset.html`

```html
{% extends "base.html" %}

{% block content %}
<h2 style="color: #0066CC; margin-top: 0;">Password Reset Request</h2>

<p>Hello,</p>

<p>We received a request to reset your password for your QA Team Portal account.</p>

<p>Click the button below to reset your password:</p>

<center>
    <a href="{{ reset_url }}" class="button">Reset Password</a>
</center>

<p><strong>This link will expire in {{ expiry_minutes }} minutes.</strong></p>

<div class="divider"></div>

<p style="font-size: 14px; color: #6b7280;">
    If you didn't request a password reset, you can safely ignore this email. Your password will not be changed.
</p>

<p style="font-size: 14px; color: #6b7280;">
    If the button doesn't work, copy and paste this link into your browser:<br>
    <a href="{{ reset_url }}" style="color: #0066CC; word-break: break-all;">{{ reset_url }}</a>
</p>
{% endblock %}
```

**Location:** `backend/app/templates/email/welcome.html`

```html
{% extends "base.html" %}

{% block content %}
<h2 style="color: #0066CC; margin-top: 0;">Welcome to QA Team Portal!</h2>

<p>Hi {{ name }},</p>

<p>Welcome to the QA Team Portal! Your account has been successfully created.</p>

<p>You can now access the admin portal to manage team members, tools, resources, and more.</p>

<center>
    <a href="{{ login_url }}" class="button">Go to Admin Portal</a>
</center>

<h3 style="color: #333; font-size: 18px;">What you can do:</h3>
<ul>
    <li>Manage team member profiles</li>
    <li>Post latest updates and announcements</li>
    <li>Organize QA tools by category</li>
    <li>Share resources and documentation</li>
    <li>Publish research and findings</li>
</ul>

<div class="divider"></div>

<p>If you have any questions or need assistance, don't hesitate to reach out to our support team.</p>

<p>Best regards,<br>QA Team Portal Team</p>
{% endblock %}
```

**Location:** `backend/app/templates/email/account_locked.html`

```html
{% extends "base.html" %}

{% block content %}
<h2 style="color: #EF4444; margin-top: 0;">Account Locked</h2>

<p>Hi {{ name }},</p>

<p>Your QA Team Portal account has been temporarily locked due to multiple failed login attempts.</p>

<p><strong>Your account will be automatically unlocked in {{ unlock_time }}.</strong></p>

<div class="divider"></div>

<h3 style="color: #333; font-size: 18px;">What happened?</h3>
<p>For your security, we lock accounts after 5 failed login attempts. This helps protect your account from unauthorized access.</p>

<h3 style="color: #333; font-size: 18px;">What should I do?</h3>
<ul>
    <li>Wait for the lockout period to expire ({{ unlock_time }})</li>
    <li>If you forgot your password, use the "Forgot Password" link on the login page</li>
    <li>If you didn't attempt to login, contact our support team immediately</li>
</ul>

<div class="divider"></div>

<p style="font-size: 14px; color: #6b7280;">
    If you believe this was a mistake or need immediate access, please contact support at {{ support_email }}.
</p>
{% endblock %}
```

### 5. Usage in Auth Endpoints

**Location:** `backend/app/api/v1/endpoints/auth.py`

```python
from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from sqlalchemy.orm import Session
from app.services.email_service import EmailService
from app.api.deps import get_db
from app.crud.user import user as user_crud
import secrets

router = APIRouter()

@router.post("/forgot-password")
async def forgot_password(
    email: str,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Send password reset email."""
    user = await user_crud.get_by_email(db, email=email)

    # Don't reveal if user exists
    if not user:
        return {"message": "If the email exists, a reset link has been sent"}

    # Generate reset token
    reset_token = secrets.token_urlsafe(32)
    expires = datetime.utcnow() + timedelta(minutes=15)

    # Store token in database
    await user_crud.set_reset_token(
        db,
        user_id=user.id,
        token=reset_token,
        expires=expires
    )

    # Send email in background
    await EmailService.send_password_reset_email(
        email=user.email,
        reset_token=reset_token,
        background_tasks=background_tasks
    )

    return {"message": "If the email exists, a reset link has been sent"}

@router.post("/test-email")
async def test_email(
    recipient: str,
    current_user: User = Depends(get_current_admin)
):
    """Test email configuration (admin only)."""
    success = await EmailService.send_test_email(recipient)

    if success:
        return {"message": f"Test email sent to {recipient}"}
    else:
        raise HTTPException(500, "Failed to send test email")
```

### 6. Email Queue (Optional - for High Volume)

**Using Celery for Email Queue:**

```python
# backend/app/tasks/email_tasks.py
from celery import Celery
from app.services.email_service import EmailService

celery_app = Celery('tasks', broker='redis://localhost:6379/0')

@celery_app.task
def send_email_task(recipients, subject, body, html=None):
    """Background task to send email."""
    import asyncio
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(
        EmailService.send_email(recipients, subject, body, html)
    )

@celery_app.task
def send_password_reset_task(email, reset_token):
    """Background task to send password reset email."""
    import asyncio
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(
        EmailService.send_password_reset_email(email, reset_token)
    )
```

### 7. Testing Email Service

```python
# tests/test_email_service.py
import pytest
from app.services.email_service import EmailService

@pytest.mark.asyncio
async def test_send_test_email():
    """Test sending a simple email."""
    success = await EmailService.send_test_email("test@example.com")
    assert success is True

@pytest.mark.asyncio
async def test_send_password_reset_email():
    """Test password reset email."""
    success = await EmailService.send_password_reset_email(
        email="user@example.com",
        reset_token="test-token-123"
    )
    assert success is True

@pytest.mark.asyncio
async def test_send_welcome_email():
    """Test welcome email."""
    success = await EmailService.send_welcome_email(
        email="newuser@example.com",
        name="New User"
    )
    assert success is True
```

## SMTP Provider Setup

### Gmail Configuration

1. Enable 2-Factor Authentication
2. Generate App Password: https://myaccount.google.com/apppasswords
3. Use App Password in MAIL_PASSWORD

```env
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

### SendGrid Configuration

```env
MAIL_SERVER=smtp.sendgrid.net
MAIL_PORT=587
MAIL_USERNAME=apikey
MAIL_PASSWORD=your-sendgrid-api-key
```

### AWS SES Configuration

```env
MAIL_SERVER=email-smtp.us-east-1.amazonaws.com
MAIL_PORT=587
MAIL_USERNAME=your-smtp-username
MAIL_PASSWORD=your-smtp-password
```

## Best Practices

1. **Use Background Tasks**: Send emails in background to avoid blocking requests
2. **Error Handling**: Log email failures, retry if needed
3. **Rate Limiting**: Implement rate limits to prevent abuse
4. **Unsubscribe Links**: Include unsubscribe option for notification emails
5. **Test Mode**: Use mailtrap.io or similar for development testing
6. **Template Versioning**: Version email templates for A/B testing
7. **Email Validation**: Validate email addresses before sending
8. **Bounce Handling**: Monitor bounced emails and update records

## Troubleshooting

**Email not sending:**
- Check SMTP credentials
- Verify firewall allows port 587/465
- Check spam folder
- Enable "Less secure app access" (Gmail) or use App Password
- Check email service logs

**Template not found:**
- Verify TEMPLATE_FOLDER path
- Check template filename matches
- Ensure templates directory exists

**Authentication failed:**
- Double-check MAIL_USERNAME and MAIL_PASSWORD
- For Gmail, use App Password, not account password
- Verify 2FA is enabled (required for App Passwords)

## Report

✅ Email service configured (FastAPI-Mail)
✅ SMTP connection established
✅ Password reset email template created
✅ Welcome email template created
✅ Account locked email template created
✅ Background tasks integrated
✅ Test endpoint created
✅ Error logging implemented
✅ Templates use responsive HTML
✅ All emails tested successfully
