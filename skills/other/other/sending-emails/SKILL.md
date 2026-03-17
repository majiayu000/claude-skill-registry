---
name: sending-emails
description: |
  Send emails via Gmail API using FastMCP server with approval workflows.
  Use when configuring email sending, troubleshooting email delivery,
  setting up email templates, or managing email rate limits.
  NOT when reading emails (use watching-gmail skill).
  NOT when categorizing emails (use watching-gmail skill).
---

# Email Sender MCP Skill

FastMCP server for sending emails via Gmail API.

## Quick Start

```bash
# Start MCP server
python src/mcp_servers/email_sender.py

# Or via scripts
python scripts/run.py
```

## MCP Tools

1. `send_email(to, subject, body, cc, bcc, requires_approval)` - Send or queue email
2. `send_from_template(template_name, to, variables, requires_approval)` - Template-based send
3. `archive_email(message_id)` - Archive sent email

## Production Gotchas ⚠️

### Cloud Mode Forces Approval
When `FTE_ROLE=cloud`, ALL emails are forced to approval workflow regardless of `requires_approval` flag:
```python
if role == "cloud":
    requires_approval = True  # Always enforced
```

### Recipient Limit (FR-003)
Maximum 5 total recipients (to + cc + bcc combined). Exceeding returns error:
```
Error: Recipient limit exceeded. Max 5 allowed, got {count}.
```

### Separate Token Files
Sending requires **different token** than reading:
- `token_email.json` - For sending (gmail.send scope)
- `token.json` - For reading (gmail.readonly scope)

### Template Subject Required
When using `send_from_template`, variables MUST include `subject`:
```python
# ✗ FAILS
send_from_template("welcome.j2", "user@example.com", {"name": "John"})

# ✓ WORKS
send_from_template("welcome.j2", "user@example.com", {"name": "John", "subject": "Welcome!"})
```

### Rate Limit Fail-Safe
When audit log read fails, rate limiting **blocks** (fail-safe):
```python
except Exception:
    return False  # Block on error, not allow
```

## Rate Limits

| Limit | Value |
|-------|-------|
| Hourly | 10 emails |
| Daily | 100 emails |

Tracked via `Vault/Logs/email_audit_log.md`.

## Approval Workflow

Set `requires_approval=True` to queue email for human review.

Approval files created in `Vault/Pending_Approval/`:
- Move to `Vault/Approved/` to send
- Delete to reject

## Configuration

Required in `config/`:
- `credentials.json` - Google OAuth credentials
- `token_email.json` - Gmail send token (separate from read)

Templates directory: `src/templates/email/`

## Environment Variables

```bash
FTE_ROLE=local|cloud  # cloud forces approval for all sends
```

## Verification

Run: `python scripts/verify.py`

## Related Skills

- `watching-gmail` - Read and categorize incoming emails
- `digital-fte-orchestrator` - Approval workflow processing
