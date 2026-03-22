---
name: resend
description: >
  Manage Resend email service via REST API. List sent emails, check domain verification,
  manage API keys, send test emails, and debug email delivery issues.
  Use for any email-related administration task.
allowed-tools: Bash, Read, Grep, Glob
---

# Resend REST API

Manage FuzzyCat's email delivery via the Resend API.

## Authentication

```bash
RESEND_API_KEY=$(grep RESEND_API_KEY .env.local | cut -d'"' -f2)
# All curl commands use: -H "Authorization: Bearer $RESEND_API_KEY"
```

## Common Commands

### Domains

```bash
# List domains
curl -s "https://api.resend.com/domains" \
  -H "Authorization: Bearer $RESEND_API_KEY" | python3 -m json.tool

# Add a domain
curl -s -X POST "https://api.resend.com/domains" \
  -H "Authorization: Bearer $RESEND_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name": "fuzzycatapp.com"}' | python3 -m json.tool

# Verify a domain (trigger DNS check)
curl -s -X POST "https://api.resend.com/domains/<domain-id>/verify" \
  -H "Authorization: Bearer $RESEND_API_KEY" | python3 -m json.tool

# Get domain details (check verification status)
curl -s "https://api.resend.com/domains/<domain-id>" \
  -H "Authorization: Bearer $RESEND_API_KEY" | python3 -m json.tool

# Delete a domain
curl -s -X DELETE "https://api.resend.com/domains/<domain-id>" \
  -H "Authorization: Bearer $RESEND_API_KEY"
```

### Emails

```bash
# List recent emails
curl -s "https://api.resend.com/emails" \
  -H "Authorization: Bearer $RESEND_API_KEY" | python3 -m json.tool

# Get email details
curl -s "https://api.resend.com/emails/<email-id>" \
  -H "Authorization: Bearer $RESEND_API_KEY" | python3 -m json.tool

# Send a test email
curl -s -X POST "https://api.resend.com/emails" \
  -H "Authorization: Bearer $RESEND_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "FuzzyCat <noreply@fuzzycatapp.com>",
    "to": ["test@example.com"],
    "subject": "Test Email",
    "html": "<p>Hello from FuzzyCat!</p>"
  }' | python3 -m json.tool
```

### API Keys

```bash
# List API keys
curl -s "https://api.resend.com/api-keys" \
  -H "Authorization: Bearer $RESEND_API_KEY" | python3 -m json.tool

# Create an API key
curl -s -X POST "https://api.resend.com/api-keys" \
  -H "Authorization: Bearer $RESEND_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name": "my-key"}' | python3 -m json.tool
```

## SMTP (for Supabase Auth integration)

Once `fuzzycatapp.com` is verified, configure Supabase to send via Resend SMTP:

```bash
# SMTP Settings for Supabase
Host: smtp.resend.com
Port: 465 (SSL) or 587 (STARTTLS)
Username: resend
Password: <RESEND_API_KEY>
From: noreply@fuzzycatapp.com
Sender Name: FuzzyCat
```

## FuzzyCat-Specific

- **From address**: `FuzzyCat <noreply@fuzzycatapp.com>`
- **Domain**: `fuzzycatapp.com` (needs DNS verification — see domain records)
- **Templates**: React Email components in `server/emails/`
- **Key files**: `server/services/email.ts`, `lib/resend.ts`
- **Active emails**: clinic-welcome, soft-collection-day1/7/14
