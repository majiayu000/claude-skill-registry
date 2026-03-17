---
name: board-sync
description: Automated project board synchronization for GitHub Projects and Notion
triggers:
  - board sync
  - sync boards
  - project board
  - notion sync
  - github sync
  - sync status
---

# Board Sync Automation Skill

Comprehensive workflow automation that keeps GitHub Projects and Notion boards in sync with code changes.

## Overview

This skill provides automatic synchronization of project tracking boards whenever code changes occur. It integrates with:

- **Claude Code hooks** (post-edit, task-complete, session-end)
- **Git hooks** (post-commit, post-merge, post-checkout)
- **Shell scripts** (start.sh, stop.sh, run-tests.sh)

## Quick Commands

```bash
# Manual sync (full)
./sync-boards.sh

# Sync GitHub Projects only
./sync-boards.sh github

# Sync Notion only
./sync-boards.sh notion

# Check sync status
./sync-boards.sh status

# View sync logs
./sync-boards.sh logs

# Force sync (bypass debounce)
./sync-boards.sh --force
```

## Automatic Triggers

### Claude Code Hooks

| Event | Behavior |
|-------|----------|
| Post-Edit | Queues sync (non-blocking, batched) |
| Task-Complete | Triggers immediate sync in background |
| Session-End | Forces sync in foreground (ensures completion) |

### Git Hooks

| Hook | Trigger |
|------|---------|
| post-commit | After each commit |
| post-merge | After merges (including git pull) |
| post-checkout | After branch switches |

### Script Hooks

| Script | Trigger |
|--------|---------|
| start.sh | After services start |
| stop.sh | After services stop |
| run-tests.sh | After test completion |

## Features

### Debounce Protection
- Default: 30 seconds between syncs
- Prevents rapid consecutive syncs
- Use `--force` to bypass

### Lock File
- Prevents concurrent sync processes
- Auto-cleanup of stale locks
- PID tracking for status reporting

### Queue System
- Post-edit hooks queue instead of immediate sync
- Queue processed on session-end or task-complete
- Prevents sync storm during rapid editing

### Logging
- All sync operations logged to `.claude/logs/board-sync.log`
- Includes timestamps, trigger source, and results
- View with `./sync-boards.sh logs`

## Configuration

### Files

| File | Purpose |
|------|---------|
| `.claude/hooks/board-sync/sync-boards.sh` | Main sync orchestrator |
| `.claude/hooks/board-sync/post-edit-sync.sh` | Post-edit hook |
| `.claude/hooks/board-sync/post-task-sync.sh` | Post-task hook |
| `.claude/hooks/board-sync/session-end-sync.sh` | Session-end hook |
| `.git/hooks/post-commit` | Git post-commit hook |
| `.git/hooks/post-merge` | Git post-merge hook |
| `.git/hooks/post-checkout` | Git post-checkout hook |

### State Files

| File | Purpose |
|------|---------|
| `.claude/.board-sync.lock` | Process lock file |
| `.claude/.board-sync.last` | Last sync timestamp |
| `.claude/.board-sync-queue` | Queued sync requests |

## Troubleshooting

### Sync Not Running

1. Check status: `./sync-boards.sh status`
2. Check if locked: `cat .claude/.board-sync.lock`
3. Force sync: `./sync-boards.sh --force`

### Stale Lock

```bash
rm .claude/.board-sync.lock
./sync-boards.sh --force
```

### View Errors

```bash
./sync-boards.sh logs
# or
tail -100 .claude/logs/board-sync.log
```

### Missing Prerequisites

```bash
# GitHub CLI auth
gh auth login
gh auth refresh -s project

# Notion API key
mkdir -p ~/.config/notion
echo 'your-api-key' > ~/.config/notion/api_key
```

## Integration Points

- **GitHub Projects**: Uses `./board-sync.sh sync` (wrapper for `scripts/github-board-sync.sh`)
- **Notion**: Uses `./notion-sync.sh push` (wrapper for `scripts/notion_sync.py`)
- **TODO.md**: Parsed by GitHub sync to create issues
