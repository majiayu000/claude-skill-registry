---
name: wt-prune
description: Clean up stale git worktree references and metadata. Use when git shows worktrees that no longer exist, or after manually deleting worktree directories. Fixes inconsistencies.
---

# /wt:prune - Prune Stale Worktree References

## Description
Quick command to clean up stale worktree administrative files and references.

## Usage
```
/wt:prune
```

## What It Does

This slash command:
1. Runs `git worktree prune` to remove stale worktree metadata
2. Cleans up references to worktrees that no longer exist on disk
3. Shows what was cleaned up

## When to Use

Use `/wt:prune` when:
- You manually deleted a worktree directory (without using git commands)
- Git shows worktrees that don't actually exist anymore
- You want to clean up orphaned worktree references
- After moving or renaming worktree directories

## Workflow

The command will:
1. **Check for stale references** - Find worktrees that don't exist on disk
2. **Show what will be pruned** - List stale references
3. **Run prune command** - Execute `git worktree prune`
4. **Confirm cleanup** - Show what was removed

## Benefits

✅ **Clean Metadata** - Removes orphaned references
✅ **Fix Inconsistencies** - Resolves git worktree list issues
✅ **Safe Operation** - Only removes references, not actual files
✅ **Quick Fix** - Solves common worktree problems

## Notes

- This command is **safe** - it only removes metadata, not actual files
- If you manually deleted a worktree directory, this cleans up git's records
- Different from `/wt:cleanup` which removes actual worktrees
- Automatically run as part of `/wt:cleanup`
