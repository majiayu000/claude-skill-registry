---
name: slack
description: "Manage unread Slack messages across the workspace: list, open, and reply with confirmation. Stores metadata for later actions."
---

# Slack (inbox + reply)

## Requirements
- Environment variable: `SLACK_USER_TOKEN` (user token).
- Recommended scopes: `channels:read`, `groups:read`, `im:read`, `mpim:read`, `channels:history`, `groups:history`, `im:history`, `mpim:history`, `users:read`, `chat:write`.
- To mark as read (granular scopes): `channels:write`, `groups:write`, `im:write`, `mpim:write` (depends on conversation type).

## Commands (from the skill folder)

### 1) Inbox (unread)
```
scripts/slack-inbox --json-out /tmp/slack-inbox.json
```
- Shows a clean numbered list.
- Saves metadata for later actions.

### 2) Open a message
```
scripts/slack-open --index <n>
```
- Uses `/tmp/slack-inbox.json` to resolve IDs.
- Writes `/tmp/slack-open.json`.

### 3) Reply (with user confirmation)
```
scripts/slack-reply --index <n> --text "reply"
```
- In channels: replies in thread if it exists (default).
- In DMs: use `--no-thread` to reply as a new message.
- After replying, mark as read with `scripts/slack-mark-read --index <n>`.

### 4) Mark as read
```
scripts/slack-mark-read --index <n>
```

## Metadata format
`/tmp/slack-inbox.json` contains:
- `index`
- `id` (channel id)
- `name`
- `type`
- `last_read`
- `latest_ts`
- `latest_text`
- `latest_user_id`
- `latest_user_name`
- `unread_count`
- `unread_has_more`

## Rules
- Show the user only the clean list; do not show IDs.
- Before replying, ask for confirmation.
- If the JSON is stale or missing, re-run inbox.
- In DMs, always reply with `--no-thread` and then mark as read.
- After replying (channels or DMs), mark as read to clear pending items.
