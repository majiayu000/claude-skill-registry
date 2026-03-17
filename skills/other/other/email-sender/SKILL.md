---
name: email-sender
description: 使用SMTP发送带附件的邮件，支持HTML模板、多收件人和文件附件。基于nodemailer。
metadata:
  short-description: 通过SMTP发送邮件
source:
  repository: https://github.com/nodemailer/nodemailer
  license: MIT
---

# Email Sender Tool

## Description
Send emails with HTML content, attachments, and multiple recipients via SMTP.

## Trigger
- `/send-email` command
- User requests to send email
- User needs email notification

## Usage

```bash
# Send simple email
python scripts/send_email.py --to "user@example.com" --subject "Hello" --body "Message content"

# Send with attachment
python scripts/send_email.py --to "user@example.com" --subject "Report" --body "See attached" --attachment "report.pdf"

# Send HTML email
python scripts/send_email.py --to "user@example.com" --subject "Newsletter" --html "template.html"
```

## Environment Variables

```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASS=your-app-password
SMTP_FROM=Your Name <your-email@gmail.com>
```

## Tags
`email`, `smtp`, `notification`, `automation`

## Compatibility
- Codex: ✅
- Claude Code: ✅
