---
name: iterm-notify
description: macOS desktop notifications and iTerm2 badge management for Claude Code lifecycle events. Not a slash command — this plugin provides hook scripts. See README for wiring instructions.
user-invocable: false
---

# iterm-notify

Provides `notify.sh` — a hook script that fires on Claude Code `Notification` and `Stop` events.

**Not a slash command.** Wire it in `~/.claude/settings.json` — see README.

## What it does

**On `Notification` (Claude needs attention):**
- Bounces the iTerm2 dock icon once
- Sets an iTerm2 badge: `<topic> ⚡` (or just `⚡` if no topic file)
- Sends a macOS desktop notification via `terminal-notifier` with a click-to-focus action

**On `Stop` (Claude finished):**
- Clears the iTerm2 badge

## Prerequisites

- macOS with iTerm2
- `terminal-notifier`: `brew install terminal-notifier`
- `jq`: `brew install jq`

## Wiring

See README for setup instructions.
