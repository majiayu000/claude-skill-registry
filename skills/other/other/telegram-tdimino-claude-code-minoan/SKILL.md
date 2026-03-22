---
name: telegram
description: Send, read, and respond to Telegram messages as Claudicle with persistent memory and cognitive pipeline integration.
---

# Telegram

Send, read, and respond to Telegram messages via the Claudicle daemon adapter. Thin skill layer on top of the existing `python-telegram-bot` v22 polling adapter at `~/.claudicle/daemon/adapters/telegram_adapter.py`.

## When to Use This Skill

- Sending a Telegram message from a Claude Code session
- Checking for unhandled Telegram messages in the inbox
- Processing Telegram messages through the `/telegram-respond` cognitive pipeline
- Managing Telegram memory context (working memory, user models, soul state)

## Prerequisites

- `python-telegram-bot` v21+ installed (`pip install python-telegram-bot`)
- `TELEGRAM_BOT_TOKEN` in `~/.config/env/secrets.env`
- Bot: `@claudicle_bot` (ID: 8646522411)
- Tom's Telegram ID: `633125581`

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `TELEGRAM_BOT_TOKEN` | -- | Bot token from @BotFather |
| `CLAUDICLE_TELEGRAM_ALLOWED_USERS` | -- | Comma-separated user IDs allowed to DM (empty = deny all) |
| `CLAUDICLE_TELEGRAM_ALLOWED_CHATS` | -- | Comma-separated chat IDs for groups (empty = all) |
| `CLAUDICLE_TELEGRAM_RESPOND_TO_DMS` | `true` | Respond to private messages (filtered by allowed users) |
| `CLAUDICLE_TELEGRAM_RESPOND_TO_MENTIONS` | `true` | Respond to @mentions in groups |

## Quick Start

```bash
# Start the listener (background daemon)
python3 ~/.claudicle/adapters/telegram/telegram_listen.py --bg

# Check for unhandled messages
cd ~/.claude/skills/telegram/scripts && python3 telegram_check.py

# Send a message
cd ~/.claude/skills/telegram/scripts && python3 telegram_send.py 633125581 "Hello from Claudicle!"

# Process inbox through cognitive pipeline
/telegram-respond
```

## Available Scripts

### `telegram_send.py` -- Send a Telegram message

```bash
python3 ~/.claudicle/adapters/telegram/telegram_post.py CHAT_ID "Hello!"
python3 telegram_send.py CHAT_ID "Reply to this" --reply-to 42
python3 telegram_send.py CHAT_ID --stdin    # Read text from stdin
python3 telegram_send.py --help
```

### `telegram_check.py` -- Check inbox for unhandled messages

```bash
python3 telegram_check.py                    # Unhandled telegram:* entries
python3 telegram_check.py --all              # All entries (including handled)
python3 telegram_check.py --limit 5          # Last 5
python3 telegram_check.py --mark-read MSG_ID # Mark entry as handled
python3 telegram_check.py --mark-all-read    # Mark all as handled
```

Reads from `~/.claudicle/daemon/inbox.jsonl` (shared with Slack/Discord).

### `telegram_memory.py` -- Memory context CLI

```bash
python3 telegram_memory.py load-context 633125581
python3 telegram_memory.py user-model tg:633125581
python3 telegram_memory.py soul-state
```

Thin CLI over `~/.claudicle/adapters/shared/claudicle_memory.py`.

## Listener Management

The listener is the existing Claudicle adapter script (not duplicated):

```bash
python3 ~/.claudicle/adapters/telegram/telegram_listen.py --bg      # Start
python3 ~/.claudicle/adapters/telegram/telegram_listen.py --status   # Check
python3 ~/.claudicle/adapters/telegram/telegram_listen.py --stop     # Stop
```

## Channel Format

`telegram:{chat_id}` -- e.g., `telegram:633125581` (private), `telegram:-100123456789` (group)

## Architecture

```
Claude Code session
  |
  |-- /telegram-respond  (cognitive pipeline: 6 XML tags)
  |-- telegram_send.py   (wraps Bot API send_message)
  |-- telegram_check.py  (reads shared inbox.jsonl)
  |-- telegram_memory.py (thin CLI over claudicle_memory)
  |
  v
~/.claudicle/adapters/telegram/     (existing, not duplicated)
  telegram_listen.py                 (polling daemon)
  telegram_post.py                   (CLI post)
  _telegram_utils.py                 (split_message, config)
  |
  v
~/.claudicle/adapters/shared/claudicle_memory.py  (3-tier memory routing)
```

## Security

- **DM access is DENY-by-default.** Set `CLAUDICLE_TELEGRAM_ALLOWED_USERS=633125581` to allow Tom.
- User input is sanitized for XML tags before cognitive pipeline processing.
- `WebFetch` removed from allowed tools in daemon mode subprocess.
