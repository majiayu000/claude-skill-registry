---
name: notify-telegram
description: Enable Telegram notifications for this Claude Code session. Use when the user runs /notify-telegram or wants to be notified on their phone when Claude finishes tasks.
allowed-tools: [Bash, Read]
---

# Enable Telegram Notifications

Register this session for Telegram notifications when tasks complete.

## Quick Start

Run the registration script with your label:

```bash
~/.claude/skills/notify-telegram/register.sh "$ARGUMENTS"
```

Replace `$ARGUMENTS` with the label (e.g., "myproject"). If empty, uses current directory name.

## What This Does

1. Finds current session ID from transcript file
2. Registers session with webhook daemon (`/session-start`)
3. Enables notifications (`/sessions/enable-notify`)
4. Creates `~/.claude/runtime/sessions/<id>/notify_label` for hooks
5. Registers with nvim if running in nvim terminal

## Prerequisites

The webhook daemon must be running on port 4731:
```bash
curl -s http://localhost:4731/health
```

If not running, start it (on devbox):
```bash
cd ~/projects/claude-code-remote && node start-telegram-webhook.js
```

## Verification

After registration, confirm:
```bash
curl -s http://localhost:4731/sessions | jq '.sessions[] | {label, session_id}'
```

## Troubleshooting

**"Session not found"**: The daemon needs the session registered first. The script handles this, but if it fails, manually register:
```bash
curl -s -X POST http://localhost:4731/session-start \
  -H "Content-Type: application/json" \
  -d '{"session_id": "<ID>", "cwd": "'$PWD'"}'
```

**Daemon not running**: Check `lsof -i :4731`. Start it if needed.

**Can't find session ID**: Look for most recent transcript:
```bash
ls -lt ~/.claude/projects/-$(pwd | tr '/' '-')/*.jsonl | head -1
```
