---
name: email-service
description: Email sending patterns for transactional and marketing emails. Use when implementing email sending, templates, SMTP configuration, or email services like SendGrid, Resend, or Mailgun.
---

# Email Service Patterns

## Setup (Resend — recommended)
```python
# email.py
import resend

resend.api_key = settings.RESEND_API_KEY

async def send_email(
    to: str | list[str],
    subject: str,
    html: str,
    from_email: str = "noreply@yourdomain.com",
) -> str:
    """Send transactional email, return message ID."""
    params = resend.Emails.SendParams(
        from_=from_email,
        to=[to] if isinstance(to, str) else to,
        subject=subject,
        html=html,
    )
    email = resend.Emails.send(params)
    return email["id"]
```

```typescript
// lib/email.ts
import { Resend } from 'resend'
const resend = new Resend(process.env.RESEND_API_KEY)

export async function sendEmail(params: {
  to: string | string[]
  subject: string
  html: string
  from?: string
}) {
  const { data, error } = await resend.emails.send({
    from: params.from ?? 'noreply@yourdomain.com',
    to: Array.isArray(params.to) ? params.to : [params.to],
    subject: params.subject,
    html: params.html,
  })
  if (error) throw new Error(error.message)
  return data
}
```

## Setup (SendGrid)
```python
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def send_email_sendgrid(to: str, subject: str, html: str):
    message = Mail(
        from_email="noreply@yourdomain.com",
        to_emails=to,
        subject=subject,
        html_content=html,
    )
    client = SendGridAPIClient(settings.SENDGRID_API_KEY)
    response = client.send(message)
    return response.status_code
```

## HTML Email Templates (React Email)
```tsx
// emails/WelcomeEmail.tsx
import { Html, Head, Body, Container, Text, Button, Hr } from '@react-email/components'

interface WelcomeEmailProps {
  username: string
  verifyUrl: string
}

export function WelcomeEmail({ username, verifyUrl }: WelcomeEmailProps) {
  return (
    <Html>
      <Head />
      <Body style={{ fontFamily: 'Arial, sans-serif', backgroundColor: '#f4f4f4' }}>
        <Container style={{ maxWidth: '600px', margin: '0 auto', padding: '20px' }}>
          <Text style={{ fontSize: '24px', fontWeight: 'bold', color: '#333' }}>
            Welcome, {username}! 👋
          </Text>
          <Text style={{ color: '#666', lineHeight: '1.6' }}>
            Thanks for signing up. Please verify your email address to get started.
          </Text>
          <Button
            href={verifyUrl}
            style={{
              backgroundColor: '#3b82f6',
              color: '#fff',
              padding: '12px 24px',
              borderRadius: '6px',
              textDecoration: 'none',
              display: 'inline-block',
            }}
          >
            Verify Email
          </Button>
          <Hr />
          <Text style={{ color: '#999', fontSize: '12px' }}>
            If you didn't create an account, you can safely ignore this email.
          </Text>
        </Container>
      </Body>
    </Html>
  )
}

// Render to HTML for sending
import { render } from '@react-email/render'
const html = render(<WelcomeEmail username="Alice" verifyUrl="https://..." />)
```

## Common Email Types
```python
# email_service.py
from .templates import render_template

async def send_welcome_email(user_email: str, username: str, verify_token: str):
    verify_url = f"{BASE_URL}/verify?token={verify_token}"
    html = render_template("welcome.html", username=username, verify_url=verify_url)
    await send_email(user_email, f"Welcome to MyApp, {username}!", html)

async def send_password_reset(email: str, reset_token: str):
    reset_url = f"{BASE_URL}/reset-password?token={reset_token}"
    html = render_template("password_reset.html", reset_url=reset_url)
    await send_email(email, "Reset your password", html)

async def send_invoice(email: str, invoice_data: dict):
    html = render_template("invoice.html", **invoice_data)
    await send_email(email, f"Invoice #{invoice_data['invoice_number']}", html)

async def send_notification(email: str, title: str, message: str):
    html = f"""
    <div style="font-family: Arial; padding: 20px;">
      <h2>{title}</h2>
      <p>{message}</p>
    </div>
    """
    await send_email(email, title, html)
```

## Jinja2 Templates (Python)
```python
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader("templates/emails"))

def render_template(template_name: str, **context) -> str:
    template = env.get_template(template_name)
    return template.render(**context)
```

```html
<!-- templates/emails/welcome.html -->
<!DOCTYPE html>
<html>
<body style="font-family: Arial; background: #f4f4f4; padding: 20px;">
  <div style="max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px;">
    <h1 style="color: #1a1a1a;">Welcome, {{ username }}! 👋</h1>
    <p style="color: #666;">Click below to verify your email:</p>
    <a href="{{ verify_url }}"
       style="background: #3b82f6; color: white; padding: 12px 24px; border-radius: 6px; text-decoration: none;">
      Verify Email
    </a>
    <p style="color: #999; font-size: 12px; margin-top: 20px;">
      This link expires in 24 hours.
    </p>
  </div>
</body>
</html>
```

## Email Queue (Background with Celery)
```python
from celery import Celery

celery = Celery("tasks", broker=settings.REDIS_URL)

@celery.task(bind=True, max_retries=3, default_retry_delay=60)
def send_email_task(self, to: str, subject: str, html: str):
    try:
        send_email_sync(to, subject, html)
    except Exception as exc:
        raise self.retry(exc=exc)

# Usage — don't block the request
send_email_task.delay(user.email, "Welcome!", welcome_html)
```

## SMTP (nodemailer / standard SMTP)
```typescript
import nodemailer from 'nodemailer'

const transporter = nodemailer.createTransport({
  host: process.env.SMTP_HOST,
  port: 587,
  secure: false,
  auth: {
    user: process.env.SMTP_USER,
    pass: process.env.SMTP_PASS,
  },
})

export async function sendEmail(to: string, subject: string, html: string) {
  await transporter.sendMail({
    from: '"MyApp" <noreply@myapp.com>',
    to,
    subject,
    html,
  })
}
```

## Rules
- Use a transactional email service (Resend, SendGrid, Mailgun) — NEVER raw SMTP in production
- Always queue emails (Celery/background task) — never send synchronously in request handler
- Verify sender domain with SPF, DKIM, DMARC records (deliverability)
- Never build HTML emails with `f-strings` with user input (XSS in email clients)
- Include unsubscribe link in marketing emails (CAN-SPAM / GDPR)
- Test email rendering with Litmus or Email on Acid before launch
- Rate limit: max 1 email per minute per recipient to avoid spam classification
- Use separate API keys for transactional vs marketing emails
- Log email send attempts (ID, recipient, template, status) in your DB
