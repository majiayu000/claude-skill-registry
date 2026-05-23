---
name: sending-emails
description: |
  Send emails via Gmail API using FastMCP server with approval workflows.
  Use when configuring email sending, troubleshooting email delivery,
  setting up email templates, or managing email rate limits.
  NOT when reading emails (use watching-gmail skill).
---

# Email Sender MCP Skill

FastMCP server for sending emails via Gmail API.

## Quick Start

```bash
# Start MCP server
python scripts/run.py
```

## MCP Tools

1. `send_email(to, subject, body, requires_approval)`
2. `send_from_template(template_name, to, variables)`

## Rate Limits

- 10 emails per hour
- 100 emails per day

## Approval Workflow

Set `requires_approval=True` to queue email for human review.

## Configuration

Required in `config/`:
- `credentials.json` - Google OAuth credentials
- `token_email.json` - Gmail send token (separate from read)

## Verification

Run: `python scripts/verify.py`
