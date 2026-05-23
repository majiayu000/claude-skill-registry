---
name: wt-finish
description: Finish a feature by merging it to the base branch and cleaning up the worktree. Use when completing a feature or story, handles merge, push, and cleanup automatically.
---

# /wt:finish - Finish Feature and Merge

## Description
Quick command to finish a feature, merge it back to the base branch, and clean up the worktree.

## Usage
```
/wt:finish
```

## What It Does

This slash command:
1. Activates the Git Worktree Manager skill (`@git-worktree`)
2. Automatically runs the `*finish-feature` command
3. Guides you through merging and cleanup

## Workflow

The command will:
1. **Verify clean state** - Ensure all changes are committed
2. **Ask for base branch** - Which branch to merge into (e.g., `main`)
3. **Run tests** - Optional: run tests before merging
4. **Checkout base branch** - Switch to the target branch
5. **Merge feature** - Merge your feature branch
6. **Push changes** - Push the merged changes
7. **Remove worktree** - Clean up the feature worktree
8. **Delete branch** - Optionally delete the feature branch

## Benefits

✅ **Complete Workflow** - Handles entire merge process
✅ **Safe Merging** - Verifies tests and clean state
✅ **Automatic Cleanup** - Removes worktree and branch
✅ **Guided Process** - Interactive prompts for all steps

## Notes

- Ensures all changes are committed before merging
- Optionally runs tests before merging
- Cleans up both worktree and branch
- Returns you to the base branch
