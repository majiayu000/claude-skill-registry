---
name: qqmail
description: Manage QQ Mail (QQ邮箱) via IMAP/SMTP. Use when the user wants to read, send, search, or manage emails from their QQ mailbox. Supports reading inbox, sending emails with attachments, searching by subject/sender/date, and listing folders.
metadata: {"openclaw": {"requires": {"bins": ["python3"]}, "os": ["win32", "linux", "darwin"], "primaryEnv": "QQMAIL_AUTH_CODE"}}
---

# QQ Mail Manager

Manage QQ邮箱 via standard IMAP/SMTP protocols using Python scripts.

## Prerequisites

The user must enable IMAP/SMTP in QQ Mail settings and obtain an authorization code (授权码):
1. Log in to mail.qq.com → Settings (设置) → Account (账户)
2. Enable IMAP/SMTP service
3. Generate an authorization code (授权码) — this is NOT the QQ password

## Configuration

The skill reads credentials from environment variables:
- `QQMAIL_USER` — QQ email address (e.g. `123456789@qq.com`)
- `QQMAIL_AUTH_CODE` — Authorization code from QQ Mail settings (授权码)

## Available Operations

### Read recent emails
```bash
python3 {baseDir}/scripts/qqmail.py inbox --limit 10
```
Shows: sender, subject, date, and a text preview of each email.

### Read a specific email by index
```bash
python3 {baseDir}/scripts/qqmail.py read --index 1
```
Shows the full email content (text body).

### Send an email
```bash
python3 {baseDir}/scripts/qqmail.py send --to "recipient@example.com" --subject "Hello" --body "Email content here"
```

### Send with attachment
```bash
python3 {baseDir}/scripts/qqmail.py send --to "recipient@example.com" --subject "Report" --body "See attached" --attachment "/path/to/file.pdf"
```

### Search emails
```bash
python3 {baseDir}/scripts/qqmail.py search --subject "keyword"
python3 {baseDir}/scripts/qqmail.py search --from "sender@example.com"
python3 {baseDir}/scripts/qqmail.py search --since "2026-01-01"
python3 {baseDir}/scripts/qqmail.py search --subject "meeting" --since "2026-02-01" --limit 5
```

### List mail folders
```bash
python3 {baseDir}/scripts/qqmail.py folders
```

### Read from a specific folder
```bash
python3 {baseDir}/scripts/qqmail.py inbox --folder "Sent Messages" --limit 5
```

## Error Handling

- If authentication fails: verify QQMAIL_USER and QQMAIL_AUTH_CODE are set correctly.
- If IMAP is not enabled: guide the user to enable it in QQ Mail settings.
- Connection errors may indicate network issues or proxy requirements.

## Notes

- QQ Mail IMAP server: `imap.qq.com:993` (SSL)
- QQ Mail SMTP server: `smtp.qq.com:465` (SSL)
- All scripts use Python 3 standard library only (no pip install needed).
- Email content is decoded with charset detection for proper Chinese display.
