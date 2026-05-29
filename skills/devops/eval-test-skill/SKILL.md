---
name: eval-test-skill
description: Git branch cleanup utility. Lists and deletes branches that have been merged to main. Use when user wants to clean up old branches, delete merged branches, or tidy up their git repository.
---

# Git Branch Cleanup

Clean up merged git branches from local repository.

## Workflow

1. **List merged branches** - Show branches already merged to main
2. **Confirm deletion** - Ask user which branches to delete
3. **Delete branches** - Remove selected merged branches

## Commands

### List merged branches

```bash
git branch --merged main | grep -v "^\*\|main\|master"
```

### Delete a single branch

```bash
git branch -d <branch-name>
```

### Delete all merged branches (except main/master)

```bash
git branch --merged main | grep -v "^\*\|main\|master" | xargs -r git branch -d
```

## Safety

- Only delete branches merged to main (use `-d` not `-D`)
- Never delete `main` or `master`
- Never delete currently checked out branch
- Show list before deletion for user confirmation
