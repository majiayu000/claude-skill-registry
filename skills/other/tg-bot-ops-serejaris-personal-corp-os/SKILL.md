---
name: tg-bot-ops
description: Use when operating, debugging, deploying, or monitoring a Telegram bot or Telegram-to-agent gateway. Triggers on "telegram bot down", "bot not responding", "debug bot", "check webhook", "polling vs webhook", "restart bot", "deploy bot", "bot logs", "agent gateway", "Telegram Bot API error", "send test message", "бот не отвечает", "проверь бота", "логи бота", "перезапусти бота". Covers health checks, logs, webhook/polling diagnostics, environment validation, safe restart/deploy checklists, Bot API smoke tests, forum topic delivery, privacy mode, gateway routing, and incident notes.
---

# Telegram Bot Ops

Use this skill when the real question is whether a Telegram bot is receiving
updates, processing them in the intended runtime, and sending visible responses
to the right chat, user, or forum topic.

## Public Safety

- Default to read-only diagnostics.
- Do not print tokens, `.env` values, connection strings, raw logs, private DMs,
  payment payloads, session files, or full user records.
- Use placeholders in notes and examples: `<TELEGRAM_BOT_TOKEN>`,
  `<TELEGRAM_USER_ID>`, `<CHAT_ID>`, `<TOPIC_ID>`, `<WEBHOOK_URL>`.
- Do not send Telegram messages, restart production services, change webhooks,
  edit BotFather settings, or deploy until the user has authorized that exact
  action.
- If any real secret appears in the repo, logs, or prompt, stop and tell the
  user it must be rotated before public release.

## Intake

If the repo or runtime is unclear, identify:

- bot repo and language/runtime;
- deployment target: local, Docker, VPS/systemd, Railway, Render, Fly, Vercel, or other;
- update mode: webhook, polling, or unknown;
- env source for `TELEGRAM_BOT_TOKEN`;
- expected symptom, chat surface, and timestamp;
- whether production restart/deploy is allowed.

## Diagnostic Flow

1. **Repo and runtime** — inspect entrypoints, process manager, deploy files, and
   current git state.
2. **Environment** — verify required env var names exist without printing values.
3. **Update intake** — classify runtime: HTTP Bot API webhook, HTTP Bot API
   polling, MTProto bot session, or MTProto user session.
4. **Bot API identity** — for Bot API-token runtimes, run `getMe` using a masked token path.
5. **Webhook/polling mode** — for Bot API-token runtimes, run `getWebhookInfo`
   and inspect runtime logs.
6. **Single update owner** — resolve `409 Conflict` by reading the error text:
   webhook conflict means webhook/deleteWebhook path; competing `getUpdates`
   means find the polling owner.
7. **Telegram delivery** — use a fresh nonce for Bot API or Telethon/user-session
   E2E when user-visible behavior matters.
8. **Handler/runtime** — prove the runtime received and processed the update.
9. **Outbound response** — prove the bot sent to the expected chat/topic.
10. **Incident note** — report symptom, evidence, root cause, fix, and residual risk.

## Telegram-To-Agent Gateways

When the bot is a gateway from Telegram into an agent runtime, read
[references/hermes-gateway.md](references/hermes-gateway.md). The reference is
Hermes-compatible but intentionally generic: bot handle, host, service name,
home directory, chat ids, topic ids, env paths, and logs must be placeholders or
redacted.

## Bot API vs Telethon / MTProto

- Bot API is Telegram's HTTP interface for bot tokens: `getUpdates`, webhooks,
  `sendMessage`, `getMe`, callbacks, payments, and join requests.
- Telethon is an MTProto client. It can be a bot-account runtime with
  `start(bot_token=...)` or a user-session E2E harness for what a Telegram user
  sees.
- Pick one primary intake per bot token/account: Bot API webhook, Bot API
  polling, MTProto bot session, or MTProto user session. Do not mix without a
  clear deduplication plan.

## Webhook And Polling Checks

Safe read-only checks should avoid putting the token-bearing URL in shell
history, process listings, or copied logs. Prefer a tiny local helper:

```python
import json, os, urllib.request

token = os.environ["TELEGRAM_BOT_TOKEN"]
for method in ("getMe", "getWebhookInfo"):
    with urllib.request.urlopen(f"https://api.telegram.org/bot{token}/{method}") as response:
        data = json.load(response)
    print(method, {"ok": data.get("ok"), "result_keys": sorted((data.get("result") or {}).keys())})
```

Do not paste the token-bearing URL into notes or issues. In reports, write:

```text
getWebhookInfo: webhook_url=<set|empty>, pending_update_count=<n>, last_error=<redacted>
```

Direct `getUpdates` diagnostics can consume pending updates. Use it only with a
fresh nonce, short timeout, known update owner, and restore plan.

## Forum Topics And Privacy

- Non-General forum topics require preserving `message_thread_id`.
- General topic is normally sent like an ordinary supergroup message: omit
  `message_thread_id`. Preserve `message_thread_id` for non-General topics.
- With privacy mode enabled, bots see targeted commands, replies to the bot,
  inline messages via the bot, service messages, private chats, and channel
  messages where they are a member. Admin bots can receive all group messages.
- Disabling privacy or removing/re-adding a bot affects group visibility and
  requires explicit user authorization.

## Restart / Deploy Gate

Before restarting or deploying:

- identify the exact production owner/process;
- capture current status and rollback command;
- state expected downtime or risk;
- confirm the user authorized the action;
- run post-restart `getMe`, webhook/polling, and one visible smoke test.

## Output Format

Answer with:

1. **Status** — `not checked`, `local only`, `runtime checked`, `verified in Telegram`, or `blocked`.
2. **Evidence** — commands/logs checked, with secrets redacted.
3. **Finding** — the failing layer or confirmed healthy layer.
4. **Action** — what changed or the next safe step.
5. **Public safety** — note if any secret, user data, or private payload was found.

## Anti-Patterns

- Claiming "bot works" from unit tests only.
- Printing raw bot tokens, `.env`, logs, user messages, payment payloads, or DB rows.
- Changing webhook/polling mode without knowing the current production owner.
- Running a local polling process with a production token while production is active.
- Ignoring `message_thread_id` when the bot lives in Telegram forum topics.
