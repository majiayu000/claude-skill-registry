---
name: session-history
description: Access session history to continue work, see what happened, or search past sessions. Use this instead of relying on memory - the raw data is always more accurate.
---

# Session History

**Core principle:** Less context stuffing, more lookup. Your memory degrades (context rot), but the raw session data doesn't.

## Quick Commands

```bash
# Helper script location
SH=~/.claude/skills/session-history/session.sh

# What's the status? (current + previous summaries)
$SH status

# List all sessions for this project
$SH list

# Last N messages from current session (see what you ACTUALLY did)
$SH tail 10

# All user prompts from current session (intent trail)
$SH prompts

# Summaries from a session (auto-generated)
$SH summaries

# Search across all sessions
$SH grep "search term"

# Files touched in a session
$SH files
```

## Commands Reference

| Command          | Description                                    |
| ---------------- | ---------------------------------------------- |
| `status`         | Overview: current + previous session summaries |
| `list`           | All sessions with first prompt and summaries   |
| `current`        | Print current session ID                       |
| `previous`       | Print previous session ID                      |
| `tail [n] [id]`  | Last N messages (default: 10, current session) |
| `prompts [id]`   | All user prompts from session                  |
| `summaries [id]` | Auto-generated summaries                       |
| `grep <term>`    | Search across all project sessions             |
| `files [id]`     | Files touched (from tool calls)                |

## When to Use

1. **Starting work** → `$SH status` to see where things left off
2. **Context rot** → `$SH tail 20` to see what you ACTUALLY did recently
3. **Continue previous** → `$SH prompts $(session.sh previous)`
4. **Find past work** → `$SH grep "feature name"`

## How It Works

**Adhoc sessions** (you just ran `claude`):

- Derives project from current working directory
- Sessions stored in `~/.claude/projects/<encoded-cwd>/`

**Worker agents** (HumanWork orchestrated):

- Context injected via `HW_SESSION_DIR` and `HW_SESSION_ID`
- Same commands, explicit context

## Data Location

```
~/.claude/projects/<encoded-cwd>/
├── <session-id>.jsonl  ← each session
└── ...

JSONL contains:
- type: "user" → user prompts
- type: "assistant" → responses (with tool calls)
- type: "summary" → auto-generated summaries
- type: "file-history-snapshot" → file state
```

## Example: Continue From Last Session

```bash
SH=~/.claude/skills/session-history/session.sh

# See what happened
$SH status

# Get the previous session's prompts
$SH prompts $($SH previous)

# See files that were modified
$SH files $($SH previous)
```
