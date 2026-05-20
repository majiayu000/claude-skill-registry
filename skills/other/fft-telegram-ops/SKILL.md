---
name: fft-telegram-ops
description: Operate FFT_nano Telegram workflows including main chat claiming, command safety boundaries, admin panel usage, media intake behavior, and Telegram-first deployment patterns.
---

# FFT Telegram Ops

Use this skill for Telegram onboarding, operations, and safe admin command handling.

## Guardrails

- Never run destructive git commands unless explicitly requested.
- Preserve unrelated worktree changes.
- Main-chat-only enforcement is mandatory for admin/delegation operations.

## Enable Telegram

1. Set host env:
   - `TELEGRAM_BOT_TOKEN=...`
2. Optional for secure main claiming:
   - `TELEGRAM_ADMIN_SECRET=...`
3. Recommended Telegram-only dev mode:
   - `WHATSAPP_ENABLED=0 ./scripts/start.sh dev telegram-only`

## Main Chat Setup

1. DM the bot and run `/id`.
2. Claim main chat:
   - `/main <secret>` (requires `TELEGRAM_ADMIN_SECRET`)
3. Alternative: set `TELEGRAM_MAIN_CHAT_ID` and restart.

## Command Policy

Available everywhere:

- `/help`
- `/status`
- `/id`

Main/admin chat only:

- `/main <secret>`
- `/tasks`
- `/task_pause <id>`
- `/task_resume <id>`
- `/task_cancel <id>`
- `/groups`
- `/reload`
- `/panel`
- `/coder <task>`
- `/coder-plan <task>`

## Messaging Behavior

- Main chat responds to all messages.
- Non-main chats require trigger prefix `@<ASSISTANT_NAME>` (default `@FarmFriend`).
- Coder delegation is rejected in non-main chats.

## Media Intake

- Telegram uploads are persisted under:
  - `groups/<group>/inbox/telegram/`
- Agent sees uploaded files as:
  - `/workspace/group/inbox/telegram/...`
- Size limit controlled by `TELEGRAM_MEDIA_MAX_MB`.

## Operational Checks

- Run `/status` in Telegram to confirm runtime and channel state.
- Use `/panel` in main chat for task/group/coder quick actions.
- If polling conflicts occur, stop duplicate FFT_nano instances.
