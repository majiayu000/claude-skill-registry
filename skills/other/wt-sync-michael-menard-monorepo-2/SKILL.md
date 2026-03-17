---
name: wt-sync
description: Sync current git worktree with upstream remote changes. Use when pulling latest changes from the remote branch. Handles uncommitted changes with stashing, offers rebase or merge.
---

# /wt:sync - Sync Worktree with Upstream

## Description
Quick command to sync the current worktree with upstream changes from the remote repository.

## Usage
```
/wt:sync
```

## What It Does

This slash command:
1. Activates the Git Worktree Manager skill (`@git-worktree`)
2. Automatically runs the `*sync` command
3. Syncs your worktree with the remote branch

## Workflow

The command will:
1. **Check working directory** - Verify it's clean (or offer to stash)
2. **Fetch from origin** - Get latest remote changes
3. **Ask merge preference** - Rebase or merge?
4. **Sync the branch** - Apply the chosen strategy
5. **Show results** - Display what changed

## Benefits

✅ **Stay Updated** - Keep worktree in sync with remote
✅ **Safe Process** - Handles uncommitted changes
✅ **Flexible** - Choose rebase or merge
✅ **Automatic Stash** - Stashes and restores changes

## Notes

- If you have uncommitted changes, they'll be stashed and restored
- You can choose between rebase (cleaner) or merge (safer)
- The command will show you what changed after syncing
