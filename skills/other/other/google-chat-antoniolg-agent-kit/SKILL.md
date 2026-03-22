---
name: google-chat
description: Read Google Chat spaces/threads via the Chat API, create/refresh OAuth tokens, parse Gmail Chat URLs, and list spaces. Use when asked to look up or verify messages in Google Chat or when you need API access to Chat from the CLI.
---

# Google Chat

## Overview

Use this skill to read Google Chat messages from specific spaces or threads using local OAuth credentials.

## Quick start

1) Create/refresh the Chat OAuth token:

```bash
python scripts/chat_auth.py
```

2) Fetch messages from a space:

```bash
python scripts/chat_fetch.py \
  --space AAAAAAA... \
  --limit 50
```

3) Fetch messages from a Gmail Chat URL (auto-extracts space/thread):

```bash
python scripts/chat_fetch.py \
  --space "https://mail.google.com/chat/u/0/#chat/space/..." \
  --limit 50
```

## Common tasks

### Authenticate or refresh token

- Run `scripts/chat_auth.py`.
- If browser login is blocked, pass `--no-browser` to use the console flow.
- Token is stored at `~/.config/google-chat/token.json` by default.

### List spaces

```bash
python scripts/chat_list_spaces.py
```

### Fetch messages from a thread

```bash
python scripts/chat_fetch.py \
  --space AAAAAAA... \
  --thread THREAD_ID \
  --limit 50
```

### Output formats

- Default output is `text` (timestamp | sender | text | message name).
- Use `--format json` to get a JSON payload with `messages` and `nextPageToken`.

## Notes

- If a Chat URL is provided, extract the space/thread IDs and use them directly.
- Keep output scoped to what the user asked for; avoid dumping full histories by default.
- Default client secret path is `~/.config/skills/client_secret.json`. If missing, pass `--client-secret` explicitly (recommended to document the path in `AGENTS.md`).

## References

- `references/setup.md`
