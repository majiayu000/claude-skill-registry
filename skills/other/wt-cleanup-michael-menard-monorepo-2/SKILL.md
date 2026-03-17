---
name: wt-cleanup
description: Identify and remove merged or stale git worktrees. Use for housekeeping, removes worktrees for branches that have been merged to main. Frees disk space.
---

# /wt:cleanup - Clean Up Merged Worktrees

## Description
Quick command to identify and remove merged or stale worktrees.

## Usage
```
/wt:cleanup
```

## What It Does

This slash command:
1. Activates the Git Worktree Manager skill (`@git-worktree`)
2. Automatically runs the `*cleanup` command
3. Helps you clean up old worktrees

## Workflow

The command will:
1. **List all worktrees** - Show all active worktrees
2. **Identify merged branches** - Find branches already merged to main/develop
3. **Ask which to remove** - Interactive selection
4. **Remove selected worktrees** - Safely delete worktrees
5. **Prune worktree references** - Clean up git metadata

## Benefits

✅ **Smart Detection** - Identifies merged branches automatically
✅ **Safe Cleanup** - Only suggests merged branches
✅ **Selective Removal** - Choose which to remove
✅ **Complete Cleanup** - Removes worktrees and branches

## Notes

- Only suggests worktrees with merged branches
- You can choose which ones to remove
- Warns about unmerged branches
- Prunes git metadata after cleanup
