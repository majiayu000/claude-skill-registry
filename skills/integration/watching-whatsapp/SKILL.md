---
name: watching-whatsapp
description: |
  Monitor WhatsApp Web for new messages using Playwright browser automation.
  Use when setting up WhatsApp monitoring or processing unread chats.
  Requires manual QR code scan on first run.
---

# WhatsApp Watcher Skill

Monitors WhatsApp Web and creates task files for important messages.

## Quick Start

```bash
python scripts/run.py
```

## First Run

1. Browser opens automatically
2. Scan QR code with WhatsApp mobile
3. Session persists in `config/whatsapp_data/`

## Configuration

- `WHATSAPP_POLL_INTERVAL` - Seconds between checks (default: 30)
- `WHATSAPP_HEADLESS` - Headless mode (default: false)
- `DRY_RUN` - Test mode (default: false)

## Verification

Run: `python scripts/verify.py`
