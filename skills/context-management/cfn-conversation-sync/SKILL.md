---
name: conversation-sync
description: Sync conversation history from .codex/sessions to .claude.json for context preservation
version: 1.0.1
tags: [conversations, sync, backup, context]
status: production
triggers:
  - copy conversations
  - sync conversations
  - import sessions
  - conversation backup
author: Claude Code
---

# Conversation Sync Skill

This skill copies Claude Code conversation session files from `.codex/sessions` to the repository's `.claude.json` file for context preservation and backup.

## Purpose

When working across different environments (e.g., after WSL/Docker crashes), conversation history stored in `.codex/sessions` can be referenced in `.claude.json` to maintain context continuity.

## Usage

```bash
# Sync conversations from last N days (default: 7)
./.claude/skills/conversation-sync/sync-conversations.sh --days 7

# Sync conversations from a specific project
./.claude/skills/conversation-sync/sync-conversations.sh --project claude-flow-novice

# Sync conversations from a specific date range
./.claude/skills/conversation-sync/sync-conversations.sh --from 2025-11-20 --to 2025-11-26

# Dry run (show what would be copied)
./.claude/skills/conversation-sync/sync-conversations.sh --dry-run
```

## What It Does

1. Searches `.codex/sessions` for conversation JSONL files
2. Filters by project working directory (if specified)
3. Filters by date range
4. Creates/updates `.claude.json` with references to conversation files
5. Preserves existing conversations in `.claude.json`

## Output Format

The skill updates `.claude.json` with this structure:

```json
{
  "conversations": [
    {
      "session_id": "rollout-2025-11-24T10-24-43-019ab71c-699f-7052-8ce1-892b6208ba94",
      "date": "2025/11/24",
      "file": "/mnt/c/Users/masha/.codex/sessions/2025/11/24/rollout-2025-11-24T10-24-43-019ab71c-699f-7052-8ce1-892b6208ba94.jsonl"
    }
  ]
}
```

## Notes

- Conversation files remain in their original locations
- Only references are added to `.claude.json`
- Supports both Windows (`/mnt/c/Users/...`) and Linux paths with automatic normalization
- Safe to run multiple times (idempotent)
- Path normalization handles both backslashes (`\`) and forward slashes (`/`)
- Case-insensitive matching for project filtering (works with mixed-case paths)

## Location of Conversation Data

- **Primary**: `/mnt/c/Users/{username}/.codex/sessions/YYYY/MM/DD/*.jsonl`
- **Alternate**: `~/.codex/sessions/YYYY/MM/DD/*.jsonl`
- **Docker mounts**: `/mnt/wsl/docker-desktop-bind-mounts/` (if applicable)

## Requirements

- `jq` - JSON processing
- `bash` 4.0+
- Access to `.codex/sessions` directory
