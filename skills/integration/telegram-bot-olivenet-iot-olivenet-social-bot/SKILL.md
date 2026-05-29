---
name: telegram-bot
description: Telegram bot komutlari ve handler referansi. Use when working with Telegram bot commands, callbacks, or approval workflows.
---

# Telegram Bot Reference

## Commands

| Command | Description |
|---------|-------------|
| /start | Ana menu |
| /status | Sistem durumu |
| /manual | Manuel icerik |
| /stats | Analytics ozeti |
| /next | Siradaki icerik |
| /schedule | Haftalik takvim |
| /sync | Insights sync |

## Main Menu

```
[Gunluk Icerik] [Reels]
[Carousel] [Otonom]
[Siradaki] [Analytics]
[Sync] [Yardim]
```

## Key Callbacks

| Callback | Action |
|----------|--------|
| start_daily | Gunluk pipeline |
| create_reels | Reels pipeline |
| approve_topic | Konu onayla |
| approve_content | Icerik onayla |
| approve_visual | Gorsel onayla |
| publish_now | Hemen yayinla |
| regenerate_* | Yeniden uret |
| cancel | Iptal |

## Approval Flow

```
1. Topic → [Onayla] [Baska Oner] [Iptal]
2. Content → [Onayla] [Yeniden Yaz] [Iptal]
3. Visual → [Onayla] [Yeniden Uret] [Iptal]
4. Final → [YAYINLA] [Zamanla] [Iptal]
```

## Pipeline Integration

```python
pipeline.set_approval({
    "action": "approve_topic",
    "edited_topic": "...",  # optional
    "feedback": "..."       # optional
})
```

## Send Message

```python
await update.message.reply_text("*Bold*", parse_mode="Markdown")

# With buttons
keyboard = [[InlineKeyboardButton("OK", callback_data="ok")]]
await update.message.reply_text("?", reply_markup=InlineKeyboardMarkup(keyboard))
```

## Error Handling

```python
try:
    await bot.send_message(text, parse_mode="Markdown")
except:
    await bot.send_message(text.replace("*", ""))  # Fallback
```

## Environment

```bash
TELEGRAM_BOT_TOKEN=...
TELEGRAM_ADMIN_CHAT_ID=...
TELEGRAM_ADMIN_USER_IDS=123,456  # Optional extra admins
```

## Deep Links

- `app/telegram_pipeline.py` - Bot + handlers
- `app/scheduler/pipeline.py` - Pipeline integration
