---
name: resend
description: "Send transactional or notification emails via the Resend API — text and HTML content, multiple recipients, CC/BCC, reply-to, and file attachments. Single Python script with stdin pipe support. Triggers on 'send email', 'transactional email', 'email notification', 'Resend API', 'send via Resend'."
---

# Resend Email Skill

Send emails via the Resend transactional email API.

## IMPORTANT: Confirm Before Sending

**Always confirm with the user before sending an email.** Show them the recipient(s), subject, and body content and get explicit approval. Email is not reversible.

## When to Use This Skill

- Sending a transactional or notification email
- Sending HTML email (inline or from a file)
- Sending email with attachments
- Piping content from another command into an email body

## Prerequisites

1. **API Key**: Get a Resend API key at https://resend.com/api-keys (format: `re_xxxxxxxxx`)
2. **Add to secrets**: Add `export RESEND_API_KEY=re_xxxxxxxxx` to `~/.config/env/secrets.env`
3. **Verify domain** (optional): By default, send from `onboarding@resend.dev` (test only). For production, verify a domain at https://resend.com/domains
4. **Install requests**: `uv pip install --system requests`

Credentials checked in order: `RESEND_API_KEY` env var > `~/.config/env/secrets.env` > `~/.claude.json`

## Quick Start

```bash
# Simple text email
python3 ~/.claude/skills/resend/scripts/send.py \
  --to "recipient@example.com" \
  --subject "Hello from Claude" \
  --body "This is a test email."

# HTML email from a file
python3 ~/.claude/skills/resend/scripts/send.py \
  --to "recipient@example.com" \
  --subject "Weekly Report" \
  --html report.html

# Pipe content as body
echo "Pipeline output here" | python3 ~/.claude/skills/resend/scripts/send.py \
  --to "recipient@example.com" \
  --subject "Build Results"

# Multiple recipients with CC
python3 ~/.claude/skills/resend/scripts/send.py \
  --to "alice@example.com" "bob@example.com" \
  --cc "manager@example.com" \
  --subject "Meeting Notes" \
  --body "Attached are the notes from today."

# With attachments
python3 ~/.claude/skills/resend/scripts/send.py \
  --to "recipient@example.com" \
  --subject "Invoice" \
  --body "Please find the invoice attached." \
  --attachments invoice.pdf

# Custom from address (requires verified domain)
python3 ~/.claude/skills/resend/scripts/send.py \
  --from "tom@minoanmystery.org" \
  --to "recipient@example.com" \
  --subject "Test" \
  --body "Sent from a verified domain."

# Inline HTML string
python3 ~/.claude/skills/resend/scripts/send.py \
  --to "recipient@example.com" \
  --subject "Styled Email" \
  --html "<h1>Hello</h1><p>This is <strong>bold</strong>.</p>"

# Dry run (print payload without sending)
python3 ~/.claude/skills/resend/scripts/send.py \
  --to "recipient@example.com" \
  --subject "Test" \
  --body "Hello" \
  --dry-run
```

## Parameters

```bash
python3 ~/.claude/skills/resend/scripts/send.py [OPTIONS]
```

| Flag | Description | Required |
|------|-------------|----------|
| `--to EMAIL [EMAIL...]` | Recipient email address(es) | Yes |
| `--subject TEXT` | Email subject line | Yes |
| `--body TEXT` | Plain text body (or pipe via stdin) | One of --body, --html, or stdin |
| `--html FILE_OR_STRING` | HTML body: path to .html file, or inline HTML string | One of --body, --html, or stdin |
| `--from EMAIL` | Sender address (default: `Tom di Mino <tom@send.minoanmystery.org>`) | No |
| `--cc EMAIL [EMAIL...]` | CC recipients | No |
| `--bcc EMAIL [EMAIL...]` | BCC recipients | No |
| `--reply-to EMAIL` | Reply-to address | No |
| `--attachments FILE [FILE...]` | File paths to attach | No |
| `--dry-run` | Print the payload without sending | No |

**Body resolution**: `--body` and `--html` can be combined for multipart email (text + HTML). If neither is provided, stdin is used as plain text. `--body ""` sends an empty text part.

## Sender Aliases

Use `--from ALIAS` as a shorthand for named senders:

| Alias | Expands to |
|-------|------------|
| `tom` | `Tom di Mino <tom@send.minoanmystery.org>` |
| `kothar` | `Kothar wa Khasis <kothar@send.minoanmystery.org>` |
| `claudius` | `Claudius, Artifex Maximus <claudius@send.minoanmystery.org>` |
| `minoan` | `Minoan Mystery <contact@send.minoanmystery.org>` |

```bash
# Send as Kothar
--from kothar

# Send as Claudius
--from claudius
```

If `--from` doesn't match an alias, it's used as-is (full email or `Name <email>` format).

## Test Addresses

Resend provides test addresses that don't affect domain reputation:
- `delivered@resend.dev` — simulates successful delivery
- `bounced@resend.dev` — simulates a bounce

## Rate Limits

Resend enforces **2 requests per second**. The script does not batch or retry — if sending multiple emails, add a 1-second delay between invocations.

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `RESEND_API_KEY not found` | Add `export RESEND_API_KEY=re_xxx` to `~/.config/env/secrets.env` |
| `missing_required_field` | Ensure `--to` and `--subject` are provided, plus body content |
| `validation_error` on from | Default `onboarding@resend.dev` only works for test sends. Verify a domain at resend.com/domains |
| `rate_limit_exceeded` | Wait 1 second between sends (2 req/s limit) |
| Attachment not found | Use absolute paths or paths relative to CWD |
