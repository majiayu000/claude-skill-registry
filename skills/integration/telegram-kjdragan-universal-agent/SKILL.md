---
name: telegram
description: Send and receive messages via Telegram using a Bot.
metadata: {"requires": ["telegram"]}
---

# Telegram Skill

Use this skill to communicate via Telegram.

## Tools
Access via `mcp__telegram__*`:
- `telegram_send_message(chat_id, text)`: Send a message.
- `telegram_get_updates(limit)`: Check for new messages sent to the bot.

## Configuration
Requires environment variables:
- `TELEGRAM_BOT_TOKEN`: The API token from BotFather.
- `TELEGRAM_ALLOWED_USER_IDS`: Comma-separated list of allowed Chat IDs (security).

## Usage
- **Notifications**: "Send me a summary on Telegram when done."
- **Interactive**: "Check Telegram for my reply."
