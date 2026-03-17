---
name: mailapp-send-email
description: Send emails through the macOS Mail app using AppleScript. Use when a task requires composing or sending email via Mail.app (including to/cc/bcc, subject, body, or attachments), or when the user asks for Mail app automation or osascript-based email sending.
---

# Mail.app Send Email

## Overview
Use the bundled AppleScript to compose and optionally send Mail.app messages with structured inputs (to/cc/bcc/subject/body/attachments).

## Quick Start
Run the AppleScript via `osascript` with `--to`, `--subject`, and `--body`. Pass comma-separated lists for multiple recipients or attachments.

```bash
osascript /Users/ivancampos/.codex/skills/mailapp-send-email/scripts/send_mail.applescript \
  --to "test@test.com" \
  --subject "hello" \
  --body "testing"
```

## Inputs
Use these flags. Only `--to`, `--subject`, and `--body` are required.
- `--to` single email or comma-separated list
- `--cc` optional comma-separated list
- `--bcc` optional comma-separated list
- `--subject` subject line
- `--body` message body
- `--attach` optional comma-separated POSIX file paths
- `--send` optional `true|false` (default `true`, send immediately)

## Behavior
- Create a new outgoing message in Mail.app.
- By default send immediately. If `--send false`, leave the draft visible for review.
- If `--attach` is provided, add each file path as an attachment.

## Troubleshooting
- If Mail.app automation prompts appear, grant permissions in System Settings -> Privacy & Security -> Automation.
- If attachments fail, ensure paths are absolute POSIX paths and the files exist.

## Resources
### scripts/
- `scripts/send_mail.applescript` Create a Mail.app message with optional cc/bcc/attachments and optional immediate send.
