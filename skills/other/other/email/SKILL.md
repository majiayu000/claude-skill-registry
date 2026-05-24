---
name: email
version: 0.0.2
author: 7Sageer, Claude
description: |
  Email operations skill for sending, fetching, and reading emails via IMAP/SMTP.
  Uses curl with OpenSSL/LibreSSL for reliable TLS compatibility with Tencent Enterprise Mail and other providers.
  Credentials are securely stored in macOS Keychain.
when_to_use: |
  Use this skill when the user requests email-related operations:
  - Sending emails ("send an email to...", "email X about...", "发邮件给...")
  - Checking emails ("check my email", "any new emails?", "查看邮件")
  - Reading specific emails ("read email #5", "show me the latest email", "读取邮件")
  - Email automation tasks ("notify me when...", "forward this to...")
---

# Email Operations Skill

## Overview

This skill provides email capabilities through direct IMAP/SMTP protocol access using curl. It supports:
- **Sending emails** via SMTP with TLS
- **Fetching email lists** via IMAP
- **Reading email content** by ID
- **Multi-account support** with secure credential storage

## Architecture

- **Protocol**: Direct IMAP (port 993) and SMTP (port 465) over TLS
- **Security**: Passwords stored in macOS Keychain, never in config files
- **Compatibility**: Uses curl with OpenSSL/LibreSSL (better Tencent Enterprise Mail support than rustls)
- **Configuration**: YAML-based account management in `references/accounts.yaml`

## Available Scripts

### 1. Send Email (`send-email.sh`)

Send emails via SMTP with support for inline or file-based content.

**Usage:**
```bash
./scripts/send-email.sh -t recipient@example.com -s "Subject" -b "Message"
./scripts/send-email.sh -t recipient@example.com -s "Subject" -f message.txt
./scripts/send-email.sh -t recipient@example.com -c another@example.com -s "Subject" -b "Message"
```

**Parameters:**
- `-a ACCOUNT` - Account name (default: from accounts.yaml)
- `-t EMAIL` - Recipient email (required)
- `-c EMAIL` - CC recipient (optional)
- `-s TEXT` - Email subject (required)
- `-b TEXT` - Email body inline (required if no -f)
- `-f FILE` - Email body from file (required if no -b)

### 2. Fetch Emails (`fetch-emails.sh`)

Retrieve email headers from a mailbox.

**Usage:**
```bash
./scripts/fetch-emails.sh                    # Fetch 10 latest from INBOX
./scripts/fetch-emails.sh -n 20              # Fetch 20 latest
./scripts/fetch-emails.sh -m "Sent"          # Fetch from Sent folder
```

**Parameters:**
- `-a ACCOUNT` - Account name (default: from accounts.yaml)
- `-m FOLDER` - Mailbox folder (default: INBOX)
- `-n N` - Number of emails to fetch (default: 10)

### 3. Read Email (`read-email.sh`)

Read full content of a specific email by ID.

**Usage:**
```bash
./scripts/read-email.sh 123                   # Read full email
./scripts/read-email.sh -p HEADER 123         # Headers only
./scripts/read-email.sh -p BODY 123           # Body only
```

**Parameters:**
- `-a ACCOUNT` - Account name (default: from accounts.yaml)
- `-m FOLDER` - Mailbox folder (default: INBOX)
- `-p PART` - Part to retrieve: HEADER, BODY, or TEXT (default: TEXT)
- `EMAIL_ID` - Email ID (required, positional argument)

## Configuration

### Account Setup

Edit `references/accounts.yaml` to add email accounts:

```yaml
default_account: SUSTech

accounts:
  SUSTech:
    email: qihr2022@mail.sustech.edu.cn
    display_name: Hanrui Qi
    imap:
      host: imap.exmail.qq.com
      port: 993
      login: qihr2022@mail.sustech.edu.cn
      protocol: imaps
    smtp:
      host: smtp.exmail.qq.com
      port: 465
      login: qihr2022@mail.sustech.edu.cn
      protocol: smtps
```

### Password Management

Passwords are stored in macOS Keychain. Set them using:

```bash
# IMAP password
security add-generic-password \
  -a "qihr2022@mail.sustech.edu.cn" \
  -s "email-imap-sustech" \
  -w "your-password" \
  -U

# SMTP password
security add-generic-password \
  -a "qihr2022@mail.sustech.edu.cn" \
  -s "email-smtp-sustech" \
  -w "your-password" \
  -U
```

**Keychain service naming convention:**
- IMAP: `email-imap-{account_name_lowercase}`
- SMTP: `email-smtp-{account_name_lowercase}`

## Common Use Cases

### 1. Send a Quick Email

When user says: "Send an email to alice@example.com about the meeting"

```bash
cd /Users/seven/Claude/.claude/skills/email
./scripts/send-email.sh \
  -t alice@example.com \
  -s "Meeting Discussion" \
  -b "Hi Alice, I wanted to follow up on our meeting..."
```

### 2. Check Recent Emails

When user says: "Check my email" or "Any new emails?"

```bash
cd /Users/seven/Claude/.claude/skills/email
./scripts/fetch-emails.sh -n 5
```

Parse the output and summarize for the user.

#### Search / Filter (Pipe + grep/rg)

This is a lightweight way to "search" within the recent emails that `fetch-emails.sh` fetched (headers only: From/Subject/Date).

```bash
cd /Users/seven/Claude/.claude/skills/email

# 任意关键字（例如 github），同时保留邮件 ID 行（便于后续 read）
./scripts/fetch-emails.sh -n 200 | rg -i "github" -B 2

# 主题关键字（建议用 rg；没有 rg 就用 grep -E）
./scripts/fetch-emails.sh -n 200 | rg "主题:.*会议" -B 2
./scripts/fetch-emails.sh -n 200 | grep -E "主题:.*会议" -B 2

# 发件人关键字
./scripts/fetch-emails.sh -n 200 | rg "发件人:.*alice" -B 1

# 提取匹配到的邮件 ID，然后读取正文（取第一个匹配）
email_id="$(
  ./scripts/fetch-emails.sh -n 200 |
    rg -i "github" -B 2 |
    sed -nE 's/.*邮件 #([0-9]+).*/\1/p' |
    head -n 1
)"
./scripts/read-email.sh "$email_id"
```

If `email_id` is empty, increase `-n` (fetch more recent emails) or adjust the keyword/regex.

### 3. Read Specific Email

When user says: "Read email #3" or "Show me the latest email"

```bash
cd /Users/seven/Claude/.claude/skills/email
./scripts/read-email.sh 3
```

### 4. Email Automation

Combine with other skills for automation:
- Check calendar → Send reminder emails
- Monitor inbox → Create system notifications
- Fetch emails → Parse and extract information

## Error Handling

### Common Issues

1. **Authentication Failed**
   - Verify Keychain passwords are set correctly
   - Check if IMAP/SMTP is enabled in email provider settings
   - For Tencent Enterprise Mail, use app-specific password

2. **Connection Timeout**
   - Verify network connectivity
   - Check firewall settings for ports 993 (IMAP) and 465 (SMTP)
   - Confirm host and port in accounts.yaml

3. **TLS Handshake Failed**
   - This skill uses curl with OpenSSL/LibreSSL for better compatibility
   - If issues persist, check email provider's TLS requirements

## Security Considerations

- **Never log or display passwords** - they're in Keychain only
- **Confirm before sending** - especially for important emails
- **Validate recipients** - check email addresses before sending
- **Respect privacy** - don't read emails unless explicitly requested

## Provider-Specific Notes

### Tencent Enterprise Mail (exmail.qq.com)
- IMAP: imap.exmail.qq.com:993 (SSL/TLS)
- SMTP: smtp.exmail.qq.com:465 (SSL/TLS)
- Requires IMAP/SMTP enabled in settings
- Recommend using app-specific password
- Note: IMAP `SEARCH` for string criteria (e.g. `SUBJECT`/`FROM`/`HEADER`) may be unreliable on some Tencent Exmail servers; prefer client-side filtering via `fetch-emails.sh | rg/grep`.

### Gmail
- IMAP: imap.gmail.com:993
- SMTP: smtp.gmail.com:587 (STARTTLS)
- Requires "Less secure app access" or App Password
- May need OAuth2 for enhanced security

### Outlook/Office 365
- IMAP: outlook.office365.com:993
- SMTP: smtp.office365.com:587
- Requires modern authentication

## Technical Details

### Why curl instead of rustls?

The rustls TLS library has compatibility issues with some email providers (notably Tencent Enterprise Mail). curl with OpenSSL/LibreSSL provides:
- Better TLS handshake compatibility
- Wider cipher suite support
- Proven reliability with enterprise email systems

### IMAP vs POP3

This skill uses IMAP (not POP3) because:
- IMAP supports folder management
- Messages remain on server
- Better for multi-device access
- More flexible search and filtering

## Future Enhancements

Potential improvements (not yet implemented):
- Server-side IMAP SEARCH (subject/sender/date; provider-dependent)
- Attachment handling
- HTML email composition
- Email filtering and rules
- OAuth2 authentication support
- Batch operations

## References

- [RFC 3501 - IMAP4rev1](https://tools.ietf.org/html/rfc3501)
- [RFC 5321 - SMTP](https://tools.ietf.org/html/rfc5321)
- [curl IMAP documentation](https://curl.se/docs/manual.html)
- [macOS Keychain security command](https://ss64.com/osx/security.html)
