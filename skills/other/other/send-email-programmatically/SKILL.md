---
name: send-email-programmatically
description: "Send emails via SMTP, free APIs, or privacy-focused services. Use when: (1) Sending notifications and alerts, (2) Automated reports and summaries, (3) User communication workflows, or (4) Error logging via email."
---

# Send Email Programmatically

Send emails via SMTP, free APIs (Mailgun, SendGrid free tier), or privacy-focused services. Essential for notifications, alerts, automated reports, and user communication.

## When to use

- Use case 1: When the user asks to send email notifications or alerts
- Use case 2: When you need to deliver automated reports or summaries
- Use case 3: For error logging and monitoring alerts
- Use case 4: When building user communication workflows (confirmations, updates)

## Required tools / APIs

- **curl** — For API-based email sending (pre-installed on most systems)
- **sendmail** / **msmtp** — For SMTP email sending
- **Mailgun API** — Free tier: 5,000 emails/month (requires API key)
- **SendGrid API** — Free tier: 100 emails/day (requires API key)
- **mail.tm** — Temporary email API (no API key required)

Install options:

```bash
# Ubuntu/Debian
sudo apt-get install -y curl msmtp msmtp-mta

# macOS (postfix is pre-installed, or use msmtp)
brew install msmtp

# Node.js
npm install nodemailer
```

## Skills

### send_email_via_smtp_curl

Send email using SMTP via curl (works with Gmail, Outlook, custom SMTP servers).

```bash
# Gmail SMTP example (requires app password)
SMTP_SERVER="smtp.gmail.com:587"
FROM_EMAIL="your-email@gmail.com"
TO_EMAIL="recipient@example.com"
SUBJECT="Test Email"
BODY="This is a test email sent via SMTP."
APP_PASSWORD="your-app-password"

# Send email
curl -v --url "smtp://${SMTP_SERVER}" \
  --mail-from "${FROM_EMAIL}" \
  --mail-rcpt "${TO_EMAIL}" \
  --user "${FROM_EMAIL}:${APP_PASSWORD}" \
  --upload-file - <<EOF
From: ${FROM_EMAIL}
To: ${TO_EMAIL}
Subject: ${SUBJECT}

${BODY}
EOF

# Outlook/Office365 SMTP
curl --url "smtp://smtp.office365.com:587" \
  --mail-from "your-email@outlook.com" \
  --mail-rcpt "recipient@example.com" \
  --user "your-email@outlook.com:your-password" \
  --ssl-reqd \
  --upload-file - <<EOF
From: your-email@outlook.com
To: recipient@example.com
Subject: Hello from Outlook

This is an automated email.
EOF
```

### send_email_via_mailgun_api

Send email using Mailgun free tier (5,000 emails/month, no credit card required for sandbox).

```bash
# Set your Mailgun credentials
MAILGUN_API_KEY="your-mailgun-api-key"
MAILGUN_DOMAIN="sandbox123.mailgun.org"  # or your verified domain

# Send email
curl -s --user "api:${MAILGUN_API_KEY}" \
  "https://api.mailgun.net/v3/${MAILGUN_DOMAIN}/messages" \
  -F from="Sender Name <mailgun@${MAILGUN_DOMAIN}>" \
  -F to="recipient@example.com" \
  -F subject="Hello from Mailgun" \
  -F text="This is the plain text body" \
  -F html="<h1>HTML Email</h1><p>This is the HTML body</p>"

# Send with attachment
curl -s --user "api:${MAILGUN_API_KEY}" \
  "https://api.mailgun.net/v3/${MAILGUN_DOMAIN}/messages" \
  -F from="notifications@${MAILGUN_DOMAIN}" \
  -F to="user@example.com" \
  -F subject="Report Attached" \
  -F text="Please find the report attached." \
  -F attachment=@./report.pdf
```

**Node.js:**

```javascript
async function sendEmailMailgun(options) {
  const { apiKey, domain, from, to, subject, text, html } = options;
  
  const formData = new URLSearchParams({
    from,
    to,
    subject,
    text: text || '',
    html: html || ''
  });
  
  const auth = 'Basic ' + Buffer.from(`api:${apiKey}`).toString('base64');
  
  const res = await fetch(`https://api.mailgun.net/v3/${domain}/messages`, {
    method: 'POST',
    headers: {
      'Authorization': auth,
      'Content-Type': 'application/x-www-form-urlencoded'
    },
    body: formData
  });
  
  if (!res.ok) {
    const error = await res.text();
    throw new Error(`Mailgun API error: ${error}`);
  }
  
  return await res.json();
}

// Usage
// sendEmailMailgun({
//   apiKey: 'your-mailgun-api-key',
//   domain: 'sandbox123.mailgun.org',
//   from: 'Sender <mailgun@sandbox123.mailgun.org>',
//   to: 'recipient@example.com',
//   subject: 'Test Email',
//   text: 'Plain text body',
//   html: '<h1>HTML body</h1>'
// }).then(result => console.log('Email sent:', result));
```

### send_email_via_sendgrid_api

Send email using SendGrid free tier (100 emails/day).

```bash
# Set your SendGrid API key
SENDGRID_API_KEY="your-sendgrid-api-key"

# Send email
curl -s --request POST \
  --url "https://api.sendgrid.com/v3/mail/send" \
  --header "Authorization: Bearer ${SENDGRID_API_KEY}" \
  --header "Content-Type: application/json" \
  --data '{
    "personalizations": [{
      "to": [{"email": "recipient@example.com"}],
      "subject": "Hello from SendGrid"
    }],
    "from": {"email": "sender@example.com", "name": "Sender Name"},
    "content": [{
      "type": "text/plain",
      "value": "This is the email body."
    }]
  }'

# Send HTML email with attachment
curl -s --request POST \
  --url "https://api.sendgrid.com/v3/mail/send" \
  --header "Authorization: Bearer ${SENDGRID_API_KEY}" \
  --header "Content-Type: application/json" \
  --data '{
    "personalizations": [{
      "to": [{"email": "user@example.com"}]
    }],
    "from": {"email": "notifications@example.com"},
    "subject": "Weekly Report",
    "content": [{
      "type": "text/html",
      "value": "<h1>Weekly Report</h1><p>Attached is your report.</p>"
    }],
    "attachments": [{
      "content": "'"$(base64 -w 0 report.pdf)"'",
      "filename": "report.pdf",
      "type": "application/pdf"
    }]
  }'
```

**Node.js:**

```javascript
async function sendEmailSendGrid(options) {
  const { apiKey, from, to, subject, text, html, attachments = [] } = options;
  
  const payload = {
    personalizations: [{
      to: [{ email: to }],
      subject
    }],
    from: { email: from },
    content: [{
      type: html ? 'text/html' : 'text/plain',
      value: html || text
    }]
  };
  
  if (attachments.length > 0) {
    payload.attachments = attachments.map(att => ({
      content: att.content,  // base64 string
      filename: att.filename,
      type: att.type || 'application/octet-stream'
    }));
  }
  
  const res = await fetch('https://api.sendgrid.com/v3/mail/send', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${apiKey}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(payload)
  });
  
  if (!res.ok) {
    const error = await res.text();
    throw new Error(`SendGrid API error: ${error}`);
  }
  
  return { success: true, status: res.status };
}

// Usage
// sendEmailSendGrid({
//   apiKey: 'your-sendgrid-api-key',
//   from: 'sender@example.com',
//   to: 'recipient@example.com',
//   subject: 'Test Email',
//   html: '<h1>Hello</h1><p>This is a test.</p>'
// }).then(result => console.log('Email sent:', result));
```

### send_email_via_msmtp

Send email using msmtp (lightweight SMTP client, good for automation).

```bash
# Configure msmtp (one-time setup)
cat > ~/.msmtprc <<EOF
defaults
auth           on
tls            on
tls_trust_file /etc/ssl/certs/ca-certificates.crt
logfile        ~/.msmtp.log

# Gmail account
account        gmail
host           smtp.gmail.com
port           587
from           your-email@gmail.com
user           your-email@gmail.com
password       your-app-password

# Set default account
account default : gmail
EOF

chmod 600 ~/.msmtprc

# Send email
echo -e "Subject: Test Email\nFrom: your-email@gmail.com\nTo: recipient@example.com\n\nThis is the email body." | msmtp recipient@example.com

# Send email with file content
cat report.txt | msmtp -t <<EOF
To: recipient@example.com
From: sender@gmail.com
Subject: Daily Report

$(cat report.txt)
EOF

# Send HTML email
msmtp recipient@example.com <<EOF
To: recipient@example.com
From: sender@gmail.com
Subject: HTML Email
Content-Type: text/html

<html>
<body>
  <h1>Hello</h1>
  <p>This is an HTML email.</p>
</body>
</html>
EOF
```

### send_email_nodejs_nodemailer

Send email using Node.js nodemailer library (supports all SMTP servers).

**Node.js:**

```javascript
const nodemailer = require('nodemailer');

async function sendEmail(config) {
  const {
    smtpHost,
    smtpPort,
    smtpUser,
    smtpPassword,
    from,
    to,
    subject,
    text,
    html,
    attachments = []
  } = config;
  
  // Create transporter
  const transporter = nodemailer.createTransport({
    host: smtpHost,
    port: smtpPort,
    secure: smtpPort === 465, // true for 465, false for other ports
    auth: {
      user: smtpUser,
      pass: smtpPassword
    },
    connectionTimeout: 10000
  });
  
  // Send email
  const info = await transporter.sendMail({
    from,
    to,
    subject,
    text,
    html,
    attachments: attachments.map(att => ({
      filename: att.filename,
      path: att.path || undefined,
      content: att.content || undefined
    }))
  });
  
  return {
    success: true,
    messageId: info.messageId,
    response: info.response
  };
}

// Usage - Gmail
// sendEmail({
//   smtpHost: 'smtp.gmail.com',
//   smtpPort: 587,
//   smtpUser: 'your-email@gmail.com',
//   smtpPassword: 'your-app-password',
//   from: '"Sender Name" <your-email@gmail.com>',
//   to: 'recipient@example.com',
//   subject: 'Hello',
//   text: 'Plain text body',
//   html: '<b>HTML body</b>',
//   attachments: [
//     { filename: 'report.pdf', path: './report.pdf' }
//   ]
// }).then(result => console.log('Email sent:', result));

// Usage - Outlook
// sendEmail({
//   smtpHost: 'smtp.office365.com',
//   smtpPort: 587,
//   smtpUser: 'your-email@outlook.com',
//   smtpPassword: 'your-password',
//   from: 'your-email@outlook.com',
//   to: 'recipient@example.com',
//   subject: 'Test',
//   text: 'This is a test email'
// });
```

### advanced_email_with_retry

Production-ready email sending with retry logic and error handling.

```bash
#!/bin/bash
send_email_with_retry() {
  local TO="$1"
  local SUBJECT="$2"
  local BODY="$3"
  local MAX_RETRIES=3
  local RETRY_DELAY=5
  
  for i in $(seq 1 $MAX_RETRIES); do
    if curl -fsS --max-time 30 \
      --url "smtp://smtp.gmail.com:587" \
      --mail-from "sender@gmail.com" \
      --mail-rcpt "$TO" \
      --user "sender@gmail.com:app-password" \
      --upload-file - <<EOF
From: sender@gmail.com
To: $TO
Subject: $SUBJECT

$BODY
EOF
    then
      echo "Email sent successfully to $TO"
      return 0
    else
      echo "Attempt $i failed, retrying in ${RETRY_DELAY}s..." >&2
      sleep $RETRY_DELAY
    fi
  done
  
  echo "Failed to send email after $MAX_RETRIES attempts" >&2
  return 1
}

# Usage
send_email_with_retry "user@example.com" "Alert" "System CPU usage is high"
```

**Node.js:**

```javascript
async function sendEmailWithRetry(config, maxRetries = 3) {
  const { provider, ...emailConfig } = config;
  
  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      let result;
      
      if (provider === 'mailgun') {
        result = await sendEmailMailgun(emailConfig);
      } else if (provider === 'sendgrid') {
        result = await sendEmailSendGrid(emailConfig);
      } else {
        throw new Error(`Unknown provider: ${provider}`);
      }
      
      return { success: true, attempt, result };
      
    } catch (err) {
      console.error(`Attempt ${attempt} failed:`, err.message);
      
      if (attempt === maxRetries) {
        throw new Error(`Failed to send email after ${maxRetries} attempts: ${err.message}`);
      }
      
      // Exponential backoff
      const delayMs = Math.min(1000 * Math.pow(2, attempt - 1), 10000);
      await new Promise(resolve => setTimeout(resolve, delayMs));
    }
  }
}

// Usage
// sendEmailWithRetry({
//   provider: 'mailgun',
//   apiKey: 'your-api-key',
//   domain: 'sandbox123.mailgun.org',
//   from: 'sender@sandbox123.mailgun.org',
//   to: 'recipient@example.com',
//   subject: 'Critical Alert',
//   text: 'System requires attention'
// }, 3).then(result => console.log('Email sent:', result));
```

## Rate limits / Best practices

- ✅ **Use app passwords** — For Gmail/Outlook, create app-specific passwords instead of account passwords
- ✅ **Free tier limits** — Mailgun: 5,000/month, SendGrid: 100/day, Gmail: 500/day
- ✅ **Retry logic** — Implement exponential backoff for failed sends
- ✅ **Error handling** — Catch and log errors, don't expose credentials in logs
- ✅ **Validate emails** — Check recipient email format before sending
- ✅ **SPF/DKIM** — Configure DNS records for custom domains to avoid spam
- ⚠️ **Never hardcode credentials** — Use environment variables or secure vaults
- ⚠️ **Rate limiting** — Add delays between bulk sends (1-2 seconds)
- ⚠️ **Bounce handling** — Monitor bounces and remove invalid addresses

## Agent prompt

```text
You have email sending capability via SMTP and free APIs. When a user asks to send an email:

1. Choose the best method based on requirements:
   - **curl + SMTP** — For simple emails with Gmail/Outlook (requires app password)
   - **Mailgun API** — For higher volume (5,000/month free, requires API key)
   - **SendGrid API** — For moderate volume (100/day free, requires API key)
   - **msmtp** — For automated scripts and cron jobs
   - **nodemailer** — For Node.js applications with full SMTP support

2. For Gmail/Outlook SMTP:
   - Gmail: smtp.gmail.com:587 (requires app password from Google Account settings)
   - Outlook: smtp.office365.com:587
   - Always use app passwords, never account passwords

3. For Mailgun:
   - Free sandbox domain: 5,000 emails/month to authorized recipients
   - Verified domain: Unlimited recipients (within free tier limits)
   - No credit card required for sandbox

4. For SendGrid:
   - Free tier: 100 emails/day
   - Requires account signup and API key

5. Always:
   - Validate recipient email format
   - Use environment variables for credentials
   - Implement retry logic (3 attempts with exponential backoff)
   - Handle errors gracefully with clear messages
   - Never log credentials or sensitive data

6. Security:
   - Store SMTP passwords in ~/.msmtprc (chmod 600) or environment variables
   - Use TLS/SSL for all SMTP connections
   - Validate and sanitize email content to prevent injection
```

## Troubleshooting

**Error: "authentication failed" (Gmail)**
- Symptom: SMTP auth fails with Gmail account password
- Solution: Generate an app password at https://myaccount.google.com/apppasswords (requires 2FA enabled)

**Error: "530 5.7.0 Must issue a STARTTLS command first"**
- Symptom: Server requires TLS encryption
- Solution: Add `--ssl-reqd` to curl command or use port 587/465

**Error: "554 5.7.1 Relay access denied"**
- Symptom: SMTP server rejects email relay
- Solution: Authenticate with correct credentials, ensure FROM email matches authenticated account

**Mailgun: "Free accounts are for test purposes only"**
- Symptom: Mailgun sandbox restricts recipients
- Solution: Add authorized recipients in Mailgun dashboard, or verify a custom domain

**SendGrid: "403 Forbidden"**
- Symptom: API key lacks permissions
- Solution: Create new API key with "Mail Send" permissions in SendGrid dashboard

**Emails going to spam:**
- Symptom: Recipients don't receive emails or they're in spam folder
- Solution: Configure SPF, DKIM, DMARC DNS records for custom domains; use verified sender emails

**Timeout errors:**
- Symptom: SMTP connection hangs or times out
- Solution: Check firewall allows outbound connections on ports 587/465; increase timeout to 30 seconds

## See also

- [../using-telegram-bot/SKILL.md](../using-telegram-bot/SKILL.md) — Alternative notification method via Telegram
- [../nostr-logging-system/SKILL.md](../nostr-logging-system/SKILL.md) — Decentralized logging alternative
- [../user-aks-for-report/SKILL.md](../user-aks-for-report/SKILL.md) — Generate reports that can be emailed
