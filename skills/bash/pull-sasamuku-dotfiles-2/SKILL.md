---
name: pull
description: Pulls latest changes from remote with conflict resolution. Use when user wants to pull, fetch changes, or update from remote.
disable-model-invocation: true
---

# Pull

Pull the latest changes from branch: $ARGUMENTS (default: origin main).

## Task

Fetch and merge the latest changes. Resolve conflicts if any occur.

```bash
git pull $ARGUMENTS
# or default:
git pull origin main
```

If conflicts occur, analyze and resolve them, then complete the merge.
