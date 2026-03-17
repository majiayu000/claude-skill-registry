---
name: rebase
description: Rebases current branch onto target with conflict resolution. Use when user wants to rebase, update branch base, or linearize history.
disable-model-invocation: true
---

# Rebase

Fetch and rebase current branch onto: $ARGUMENTS (default: origin/main).

## Task

Rebase the current branch onto the target branch. Resolve conflicts if any occur.

```bash
git fetch origin
git rebase $ARGUMENTS
# or default:
git rebase origin/main
```

If conflicts occur, analyze and resolve them, then continue the rebase.
