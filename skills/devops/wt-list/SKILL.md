---
name: wt-list
description: List all active git worktrees with their status. Use when checking what worktrees exist, their branches, and which has uncommitted changes. Quick overview command.
---

# /wt:list - List All Worktrees

## Description
Quick command to show all active git worktrees in your repository.

## Usage
```
/wt:list
```

## What It Does

This slash command:
1. Activates the Git Worktree Manager skill (`@git-worktree`)
2. Automatically runs the `*list` command
3. Shows all active worktrees with their status

## Output

The command will display:
- **Worktree path** - Full path to each worktree
- **Branch name** - The branch checked out in that worktree
- **Commit** - Current commit hash
- **Status** - Clean, modified, or other git status

## Benefits

✅ **Quick Overview** - See all worktrees at a glance
✅ **Status Check** - Know which worktrees have uncommitted changes
✅ **Easy Navigation** - See paths to switch to
