---
name: discord
description: Build and automate Discord integrations (bots, webhooks, slash commands, and REST API workflows). Use when the user mentions Discord, a Discord server/guild, channels, webhooks, bot tokens, slash commands/application commands, discord.js, or discord.py.
triggers:
  - discord
  - discord api
  - discord bot
  - discord webhook
  - discord.js
  - discord.py
---

# Discord

Use this skill when implementing or automating Discord integrations.

## Pick the right approach

1. **Incoming webhooks (best for one-way posting)**
   - Good for CI notifications, alerts, build status, etc.
   - No bot user needed.
   - See: https://discord.com/developers/docs/resources/webhook#execute-webhook

2. **Bot token + REST API (two-way / richer automation)**
   - Use when you need to post as a bot, manage channels, read history, moderate, etc.
   - REST API base: `https://discord.com/api/v10`
   - Most REST calls use `Authorization: Bot <token>`.

3. **Interactions / slash commands (user-invoked commands)**
   - Use application commands and interaction webhooks.
   - Typically requires running a web server to receive interactions and respond quickly.

## Secrets & safety

- **Never hard-code tokens**. Use environment variables:
  - `DISCORD_WEBHOOK_URL` for incoming webhooks
  - `DISCORD_BOT_TOKEN` for bot REST API calls
- Treat webhook URLs as secrets (they include a token).
- Do **not** automate normal user accounts (“self-bots”). Use official bot/OAuth flows.

## Footguns / safety notes (read this)

- **Webhook URLs are secrets** (the token is embedded in the URL). Don’t paste them into issues, logs, CI output, or chat.
- **Mentions are dangerous by default**: always set `allowed_mentions` to something strict (these examples use `{"parse": []}`) to avoid accidentally pinging `@everyone` / roles.
- **Watch for accidental secret logging**:
  - If you build your own scripts, avoid including full webhook URLs in exception messages.
  - The bundled scripts sanitize webhook URLs in error output, but you should still avoid printing the URL yourself.
- **Rate limits**: handle HTTP 429 with `retry_after`/`Retry-After`, and don’t retry forever.

## Quick recipes

### Post a message via an incoming webhook (recommended)

Discord requires at least one of `content`, `embeds`, `components`, `file`, or `poll`.

```bash
curl -sS -X POST \
  -H 'Content-Type: application/json' \
  -d '{"content":"Hello from OpenHands","allowed_mentions":{"parse":[]}}' \
  "$DISCORD_WEBHOOK_URL"
```

### Post a message to a channel with a bot token

Endpoint: `POST /channels/{channel_id}/messages` (Create Message)

```bash
CHANNEL_ID="..."

curl -sS -X POST "https://discord.com/api/v10/channels/${CHANNEL_ID}/messages" \
  -H "Authorization: Bot $DISCORD_BOT_TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{"content":"Hello from my bot","allowed_mentions":{"parse":[]}}'
```

Docs: https://discord.com/developers/docs/resources/channel#create-message

## Automation scripts (bundled)

These scripts are self-contained and only use the Python standard library.

- Post to a webhook:
  ```bash
  python3 -m skills.discord.scripts.post_webhook --content "Build finished" --wait
  ```

- Post to a channel using a bot token:
  ```bash
  python3 -m skills.discord.scripts.send_message --channel-id "$CHANNEL_ID" --content "Hello"
  ```

## Rate limits

- Don’t hard-code limits. Use Discord’s `Retry-After` / `retry_after` and rate-limit headers when present.
- On HTTP **429**, wait for the provided delay (clamp to a sane maximum, add small jitter), then retry.

Docs: https://discord.com/developers/docs/topics/rate-limits

## Slash commands / application commands

- Use **guild commands** for fast iteration (instant updates).
- Use **global commands** when ready; propagation can take longer.

Docs: https://discord.com/developers/docs/interactions/application-commands

## Reference

For more details (OAuth2 flows, command registration endpoints, troubleshooting), see:
- [references/REFERENCE.md](references/REFERENCE.md)
