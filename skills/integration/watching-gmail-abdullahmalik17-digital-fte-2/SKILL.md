---
name: watching-gmail
description: |
  Monitor Gmail inbox for new emails, classify by priority, and create task files.
  Use when setting up email monitoring, processing unread messages, or configuring
  email-based task creation. NOT when sending emails (use sending-emails skill).
---

# Gmail Watcher Skill

Monitors Gmail inbox and creates task files in Obsidian vault.

## Quick Start

```bash
python scripts/run.py
```

## Configuration

Required in `config/`:
- `credentials.json` - Google OAuth client credentials
- `token.json` - Auto-created on first run

Environment variables:
- `GMAIL_POLL_INTERVAL` - Seconds between checks (default: 60)
- `DRY_RUN` - Test mode (default: false)

## Priority Classification

| Priority | Keywords |
|----------|----------|
| Urgent | urgent, asap, emergency, critical |
| High | important, invoice, payment, deadline |
| Medium | question, request, update |
| Low | thanks, fyi, newsletter |

## Verification

Run: `python scripts/verify.py`
