---
name: merge
description: Merges a branch into current branch with conflict resolution. Use when user wants to merge, combine branches, or integrate changes.
disable-model-invocation: true
---

# Merge

Merge branch: $ARGUMENTS (default: origin main) into current branch.

## Task

Merge the specified branch into the current branch. Resolve conflicts if any occur.

```bash
git merge $ARGUMENTS
# or default:
git merge origin main
```

If conflicts occur, analyze and resolve them, then complete the merge.
