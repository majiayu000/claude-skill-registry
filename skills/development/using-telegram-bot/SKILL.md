---
name: using-telegram-bot
description: Build and run Telegram bots in Node.js using Telegraf with practical command patterns.
---

# Telegram (Telegraf) Skill — Node.js

Short guide to build Telegram bots with `telegraf` (Node.js).

## Overview
- Library: https://github.com/telegraf/telegraf
- Install: `npm install telegraf`
- Get a bot token from BotFather and store it in `BOT_TOKEN`.

## Minimal polling bot

```javascript
// bot.js
const { Telegraf, Markup } = require('telegraf');
const bot = new Telegraf(process.env.BOT_TOKEN);

bot.start(ctx => ctx.reply('Welcome! I can help with commands.'));

bot.command('echo', ctx => {
  const text = ctx.message.text.split(' ').slice(1).join(' ');
  ctx.reply(text || 'usage: /echo your message');
});

bot.on('text', ctx => ctx.reply(`You said: ${ctx.message.text}`));

bot.launch();

process.once('SIGINT', () => bot.stop('SIGINT'));
process.once('SIGTERM', () => bot.stop('SIGTERM'));
```

Run:

```bash
BOT_TOKEN=123:ABC node bot.js
```

## Send media and files

```javascript
// send photo
await ctx.replyWithPhoto('https://example.com/image.jpg', { caption: 'Nice pic' });

// send document
await ctx.replyWithDocument('https://example.com/file.pdf');
```

## Inline keyboards and callbacks

```javascript
// show inline buttons
await ctx.reply('Choose:', Markup.inlineKeyboard([
  Markup.button.callback('OK', 'ok'),
  Markup.button.callback('Cancel', 'cancel')
]));

bot.action('ok', ctx => ctx.reply('You pressed OK'));
bot.action('cancel', ctx => ctx.reply('Cancelled'));
```

## Webhook (Express) example

```javascript
const express = require('express');
const { Telegraf } = require('telegraf');
const bot = new Telegraf(process.env.BOT_TOKEN);
const app = express();

app.use(bot.webhookCallback('/telegraf'));
bot.telegram.setWebhook(`${process.env.PUBLIC_URL}/telegraf`);

app.listen(process.env.PORT || 3000);
```

Use webhooks for production deployments (faster, lower resource use).

## Error handling

```javascript
bot.catch((err, ctx) => {
  console.error('Bot error', err);
});
```

## Tips
- Use environment variables for tokens and URLs.
- Respect Telegram rate limits (avoid flooding large groups).
- For local testing, use polling; for deployment use webhooks behind HTTPS.
- Add `NODE_ENV=production` and graceful shutdown hooks for reliability.

---

This doc shows the most common Telegraf patterns: start/command handlers, text handlers, media, inline buttons, webhook setup, and error handling.
