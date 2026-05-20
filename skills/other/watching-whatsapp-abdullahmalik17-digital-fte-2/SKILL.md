---
name: watching-whatsapp
description: |
  Monitor WhatsApp Web for new messages using Playwright browser automation.
  Use when setting up WhatsApp monitoring, processing unread chats, sending messages,
  or configuring auto-reply behavior.
  Requires manual QR code scan on first run.
  NOT when using WhatsApp Business API (different architecture).
---

# WhatsApp Watcher Skill

Monitors WhatsApp Web and creates task files for important messages.

## Quick Start

```bash
# Start watcher (visible browser)
python src/watchers/whatsapp_watcher.py

# Or via MCP server (for sending)
python src/mcp_servers/whatsapp_server.py
```

## Architecture

```
MCP Server (whatsapp_server.py)
        │
        ▼ Creates queue file
Vault/WhatsApp_Queue/SEND_to_*.md
        │
        ▼ Watcher picks up
Watcher (whatsapp_watcher.py)
        │
        ▼ Browser automation
WhatsApp Web → Message sent
```

**Why queues?** MCP doesn't drive browser directly to prevent session locking.

## First Run

1. Browser opens automatically
2. Scan QR code with WhatsApp mobile (120 second timeout)
3. Session persists in `config/whatsapp_data/`
4. On auth failure: Creates alert in `Vault/Needs_Action/`

## Production Gotchas ⚠️

### Contact Name Must Match Exactly
The `to` parameter must match the contact name in your phone EXACTLY (case-sensitive):
```python
# ✗ FAILS - Different case
send_whatsapp_message(to="john doe", message="Hello")

# ✓ WORKS - Exact match
send_whatsapp_message(to="John Doe", message="Hello")
```

### Priority Classification System
Messages are auto-classified by keywords:

| Priority | Keywords | Action |
|----------|----------|--------|
| Urgent | urgent, asap, emergency, critical | Immediate escalation |
| High | important, invoice, payment, deadline | Same-day review |
| Medium | question, request, update | Standard queue |
| Low | thanks, ok, noted | Archive |

### Known Contacts Get Priority Boost
Known contacts (from `config/known_senders.json`) get automatic priority upgrade:
- Medium → High for known contacts
- Unknown + High = ESCALATION (special handling)

### WhatsApp Web Selector Changes
WhatsApp updates their DOM frequently. Multiple fallback selectors are used:
```python
# Primary input selector
input_selector = 'div[contenteditable="true"][data-tab="10"]'

# Fallback
input_selector = 'div[data-testid="conversation-compose-box-input"]'
```

### QR Code Timeout
Only 120 seconds to scan QR code. After that:
- Auth fails
- Debug screenshot saved to `Vault/Logs/`
- Alert task created in `Vault/Needs_Action/`

### PII Redaction in Logs
Phone numbers are automatically redacted in audit logs:
```
+1 234 567 8900 → [REDACTED]
```

## Auto-Reply Feature

Enable automatic responses based on priority:

```bash
WHATSAPP_AUTO_REPLY=true
WHATSAPP_AUTO_REPLY_THRESHOLD=high  # Options: urgent, high, medium, low
```

Only messages at or above threshold get auto-reply.

## MCP Tools

Via `whatsapp_server.py`:

1. `send_whatsapp_message(to, message, requires_approval)` - Queue message for sending

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `WHATSAPP_POLL_INTERVAL` | 30 | Seconds between checks |
| `WHATSAPP_HEADLESS` | false | Run browser hidden |
| `WHATSAPP_AUTO_REPLY` | false | Enable auto-reply |
| `WHATSAPP_AUTO_REPLY_THRESHOLD` | high | Minimum priority for auto-reply |
| `DRY_RUN` | false | Test mode (no actual sends) |

## Sending Messages

### With Approval (Default)
```python
send_whatsapp_message(
    to="John Doe",
    message="Your invoice is ready",
    requires_approval=True  # Creates file in Pending_Approval/
)
```

Move file to `Vault/WhatsApp_Queue/` renamed as `SEND_to_*.md` to send.

### Direct Send (Trusted)
```python
send_whatsapp_message(
    to="John Doe",
    message="Quick update",
    requires_approval=False  # Goes directly to queue
)
```

## Verification

Run: `python scripts/verify.py`

## Related Skills

- `sending-emails` - Email sending patterns
- `digital-fte-orchestrator` - Task processing loop
