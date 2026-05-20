---
name: slack
description: "Slack workspace integration: 7 on-demand scripts (post, read, search, react, upload, channels, users) + Session Bridge (connect any Claude Code session to Slack via background listener + inbox.jsonl). Daemon, soul engine, and memory system live in Claudicle (github.com/tdimino/claudicle)."
---

# Slack Skill

Slack workspace integration with two components:
1. **Scripts** — 7 Python scripts for on-demand Slack operations (bundled here)
2. **Session Bridge** — connect THIS Claude Code session to Slack (background listener + inbox file, no extra API costs)

> **Daemon & Soul Engine**: The Claudicle daemon (unified launcher, soul engine, cognitive pipeline, three-tier memory, Soul Monitor TUI) now lives in its own repo: **[github.com/tdimino/claudicle](https://github.com/tdimino/claudicle)**. Install Claudicle separately for daemon features.

## When to Use This Skill

### Scripts (on-demand)
- Posting messages to Slack channels or threads
- Reading channel history or thread replies
- Searching messages or files across the workspace
- Adding or managing reactions on messages
- Uploading files or code snippets
- Listing channels, getting channel info, or joining channels
- Looking up users by name, ID, or email

### Session Bridge (recommended)
- Connecting any running Claude Code session to Slack
- Responding to @mentions and DMs with full tool access (this session IS the brain)
- No extra API costs — messages processed in the current session context
- Auto-notification of new messages via UserPromptSubmit hook
- Personality as Claudicle via soul.md instructions (no XML machinery needed)

## Prerequisites

All scripts require the `SLACK_BOT_TOKEN` environment variable (a Bot User OAuth Token starting with `xoxb-`). Scripts also require `requests` (`uv pip install --system requests`).

```bash
# Verify token is set
echo $SLACK_BOT_TOKEN
```

### First-Time Setup

1. Go to [api.slack.com/apps](https://api.slack.com/apps) -> Create New App -> From Scratch
2. Name it "Claude Code" -> select your workspace
3. **OAuth & Permissions** -> Bot Token Scopes -> add all:
   - `app_mentions:read`
   - `channels:history`, `groups:history`, `im:history`, `mpim:history`
   - `channels:read`, `groups:read`, `im:read`, `im:write`
   - `chat:write`
   - `files:write`, `files:read`
   - `reactions:write`, `reactions:read`
   - `search:read`
   - `users:read`, `users:read.email`
   - `users:write` (optional — enables green presence dot)
4. **Settings -> Socket Mode** -> toggle **ON** -> generate an App-Level Token:
   - Name: `socket-mode`
   - Scope: `connections:write`
   - Copy the `xapp-` token
5. **Event Subscriptions** -> toggle **ON** (no Request URL needed with Socket Mode) -> **Subscribe to Bot Events** -> add:
   - `app_mention` — channel @mentions
   - `message.im` — direct messages (required for DMs to work)
   - `app_home_opened` — App Home tab rendering
6. **App Home** -> Show Tabs -> enable **"Allow users to send Slash commands and messages from the messages tab"**
7. **Install to Workspace** -> approve permissions -> copy Bot User OAuth Token
8. Set environment variables (add to shell profile):
   ```bash
   export SLACK_BOT_TOKEN=xoxb-...   # Bot User OAuth Token
   export SLACK_APP_TOKEN=xapp-...   # App-Level Token (Socket Mode)
   ```
9. Invite the bot to channels: `/invite @Claude Code`

**After any scope or event subscription change**: reinstall the app (Install App -> Reinstall to Workspace) and restart the listener.

---

## Quick Start

```bash
# Post a message
python3 ~/.claude/skills/slack/scripts/slack_post.py "#general" "Hello from Claude"

# Read recent messages
python3 ~/.claude/skills/slack/scripts/slack_read.py "#general" -n 10

# Search the workspace
python3 ~/.claude/skills/slack/scripts/slack_search.py "deployment status"

# Connect this session to Slack via Claudicle Session Bridge
# (requires Claudicle installed — see github.com/tdimino/claudicle)
cd ~/.claudicle/daemon && python3 slack_listen.py --bg
python3 ~/.claude/skills/slack/scripts/slack_check.py
```

---

## Session Bridge

Connect any running Claude Code session to Slack. A background listener catches @mentions and DMs -> `inbox.jsonl`. This session reads the inbox, processes with full tool access, posts responses back. No extra API costs.

Requires Claudicle daemon installed — see [github.com/tdimino/claudicle](https://github.com/tdimino/claudicle).

```bash
# Connect
cd ~/.claudicle/daemon && python3 slack_listen.py --bg

# Check messages
python3 ~/.claude/skills/slack/scripts/slack_check.py

# Respond to thread, remove hourglass, mark handled
python3 ~/.claude/skills/slack/scripts/slack_post.py "C12345" "response" --thread "TS"
python3 ~/.claude/skills/slack/scripts/slack_react.py "C12345" "TS" "hourglass_flowing_sand" --remove
python3 ~/.claude/skills/slack/scripts/slack_check.py --ack 1

# Disconnect
cd ~/.claudicle/daemon && python3 slack_listen.py --stop
```

**Soul Formatter** (optional): `scripts/slack_format.py` adds Open Souls cognitive step formatting — perception framing, dialogue extraction, monologue logging.

```bash
python3 slack_format.py perception "Tom" "What's the status?"   # -> Tom said, "..."
echo "$raw" | python3 slack_format.py extract                   # -> external dialogue only
echo "$raw" | python3 slack_format.py extract --narrate --log   # -> narrated + logged
python3 slack_format.py instructions                            # -> cognitive step XML format
```

**Automated Respond**: `/slack-respond` processes all pending messages as Claudicle with full cognitive steps — perception, monologue, dialogue, post, ack — in a single invocation. See `~/.claude/skills/slack-respond/SKILL.md`.

For full installation, architecture, inbox format, auto-notification hook, and troubleshooting, see `references/session-bridge.md`.

---

## Script Selection Guide

| Task | Script | Example |
|------|--------|---------|
| Post a message | `slack_post.py` | `slack_post.py "#general" "Hello"` |
| Reply to a thread | `slack_post.py` | `slack_post.py "#ch" "reply" --thread TS` |
| Schedule a message | `slack_post.py` | `slack_post.py "#ch" "msg" --schedule ISO` |
| Read channel history | `slack_read.py` | `slack_read.py "#general" -n 20` |
| Read thread | `slack_read.py` | `slack_read.py "#ch" --thread TS` |
| Search messages | `slack_search.py` | `slack_search.py "query"` |
| Search files | `slack_search.py` | `slack_search.py "query" --files` |
| Add reaction | `slack_react.py` | `slack_react.py "#ch" TS emoji` |
| Upload file | `slack_upload.py` | `slack_upload.py "#ch" ./file.pdf` |
| Share code snippet | `slack_upload.py` | `slack_upload.py "#ch" --snippet CODE` |
| List channels | `slack_channels.py` | `slack_channels.py` |
| Join channel | `slack_channels.py` | `slack_channels.py --join "#ch"` |
| Find user by email | `slack_users.py` | `slack_users.py --email user@co.com` |

For full script documentation (all parameters, examples, test suite, common workflows), see `references/scripts-reference.md`.

---

## Rate Limit Awareness

| Tier | Rate | Key Methods |
|------|------|-------------|
| **Tier 1** | **1/min** | `conversations.history`, `conversations.replies` |
| Tier 2 | 20/min | `conversations.list`, `users.list`, `search.messages` |
| Tier 3 | 50/min | `reactions.*`, `conversations.info`, `chat.update` |
| Tier 4 | 100+/min | `files.getUploadURLExternal`, `files.completeUploadExternal` |
| Special | 1/sec/channel | `chat.postMessage` |

All scripts handle rate limits automatically via `_slack_utils.py` (local cooldown + retry with `Retry-After`). See `references/rate-limits.md` for full details.

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Bot not responding to @mentions | Enable Socket Mode; verify `SLACK_APP_TOKEN` (xapp-) is exported |
| "missing_scope" error | Add the missing scope in OAuth & Permissions -> reinstall app |
| No search results | Invite bot to channels with `/invite @Claude Code`, or use user token (`xoxp-`) |
| Rate limited (429) | Scripts auto-retry; reduce batch sizes |
| "Sending messages turned off" | App Home -> enable "Allow users to send Slash commands and messages from the messages tab" |
| No green presence dot | Add `users:write` scope -> reinstall app |
| App Home tab blank | Subscribe to `app_home_opened` event |

For daemon-specific troubleshooting (soul engine, memory, launcher), see [Claudicle docs](https://github.com/tdimino/claudicle).

---

## File Structure

```
scripts/
├── slack_check.py       # Session Bridge: read/ack inbox messages
├── slack_inbox_hook.py  # Session Bridge: UserPromptSubmit auto-check hook
├── slack_format.py      # Soul formatter: perception/extract/instructions (Open Souls paradigm)
├── slack_post.py        # Post messages to channels/threads
├── slack_read.py        # Read channel history or threads
├── slack_search.py      # Search messages or files
├── slack_react.py       # Add/remove reactions
├── slack_upload.py      # Upload files or snippets
├── slack_channels.py    # List/join channels
├── slack_users.py       # Look up users
└── _slack_utils.py      # Shared auth, rate limiting, API calls
```

---

## Reference Index

| Reference | Contents |
|-----------|----------|
| `references/session-bridge.md` | Session Bridge: installation, architecture, inbox format, usage workflow, soul formatter, troubleshooting |
| `references/unified-launcher-architecture.md` | Unified launcher: installation, architecture, per-channel sessions, SDK integration, data flows, threading model |
| `references/daemon-architecture.md` | Soul engine cognitive steps, memory tiers, XML format, App Home, Soul Monitor TUI |
| `references/scripts-reference.md` | Full documentation for all 7 scripts, test suite, common workflows |
| `references/onboarding-guide.md` | User model interview, CLAUDE.md generation, export commands |
| `references/rate-limits.md` | Slack API rate limit tiers and handling strategy |

## Assets

- `assets/app-icon.png` — Slack app icon for bot configuration
