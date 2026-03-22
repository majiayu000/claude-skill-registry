---
name: whatsapp-evo
description: "Manage WhatsApp via Evolution API (v2.x): list chats with unread messages and reply."
---

# WhatsApp (Evolution API)

## Requirements
- Environment variables:
  - `EVOLUTION_API_URL` (optional if config)
  - `EVOLUTION_API_TOKEN`
  - `EVOLUTION_INSTANCE` (optional if config)
- Configure `api_url` and `instance` in `~/.config/skills/config.json` under `whatsapp_evo` (recommended). The token must be set via env var.

Example:
```json
{
  "whatsapp_evo": {
    "api_url": "https://evo.example.com",
    "instance": "MyInstance"
  }
}
```

## Commands (from the skill folder)

### 1) Inbox (unread)
```
scripts/whatsapp-inbox --json-out /tmp/whatsapp-inbox.json
```
- Shows a clean numbered list.
- Saves metadata for later actions.
- Note: the inbox is computed from the last incoming message without `READ` status in the API (it may not match "mark as unread" in the app).
- Saves local state in `~/.cache/whatsapp-evo/inbox-state.json` to avoid repeating chats (override with `--state` or `WHATSAPP_EVO_STATE_PATH`).
- Use `--no-update-state` if you want to list the same chats again.
- Use `--since-days N` to ignore old messages in the first pass (default 7).
- Use `--pending-reply` to list conversations from the last N days where the latest message is not yours (ignores local state).

### 2) Reply (with user confirmation)
```
scripts/whatsapp-reply --index <n> --text "reply"
```
- Replies to the chat at the given index using `message/sendText`.
- For direct chats use the number; for groups use `remote_jid` if needed.
- Optional: `--delay <ms>`, `--link-preview`, `--instance`, `--url`.

### 3) Conversation history
```
scripts/whatsapp-history --index <n> --limit 50
```
- Use `--jid` or `--number` if you don’t have an index.
- Filter by date with `--since 2025-01-01` or `--since 2025-01-01T10:00:00Z` and `--until`.
- Use `--incoming-only` to show only inbound messages.

## Metadata format
`/tmp/whatsapp-inbox.json` contains:
- `index`
- `name`
- `remote_jid`
- `number`
- `unread_count`
- `last_message_id`
- `last_message_from_me`
- `last_message_text`
- `last_message_timestamp`
- `last_message_sender`

## Rules
- Show the user only the clean list; never show tokens.
- Before replying, ask for confirmation.
- If the JSON is stale or missing, re-run inbox.
