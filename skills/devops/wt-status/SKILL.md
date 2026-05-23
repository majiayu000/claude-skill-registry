---
name: wt-status
description: Show comprehensive status of current and all git worktrees. Use when checking uncommitted changes, sync status, or getting overview of all active worktrees.
---

# /wt:status - Show Worktree Status

## Description
Quick command to show comprehensive status of the current worktree and all worktrees.

## Usage
```
/wt:status
```

## What It Does

This slash command:
1. Activates the Git Worktree Manager skill (`@git-worktree`)
2. Automatically runs the `*status` command
3. Shows detailed status information

## Information Displayed

The command shows:
- **Current worktree location** - Where you are now
- **All worktrees and their states** - Overview of all worktrees
- **Uncommitted changes** - Files modified, staged, untracked
- **Branches ahead/behind origin** - Sync status with remote

## Benefits

✅ **Complete Overview** - See everything at a glance
✅ **Sync Awareness** - Know what needs pushing/pulling
✅ **Change Tracking** - See all uncommitted work
✅ **Multi-Worktree View** - Status of all worktrees
