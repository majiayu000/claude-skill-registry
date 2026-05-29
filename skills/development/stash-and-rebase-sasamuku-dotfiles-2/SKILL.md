---
name: stash-and-rebase
description: Stash changes, rebase onto latest main, and reapply stash
disable-model-invocation: true
---

# Stash and Rebase

Stash current changes, rebase onto latest main, and reapply stash.

## Steps

1. Stash all current changes including untracked files:
   ```bash
   git stash push -u -m "Auto-stash before rebase"
   ```

2. Fetch the latest changes from remote:
   ```bash
   git fetch origin
   ```

3. Rebase the current branch onto the latest main:
   ```bash
   git rebase origin/main
   ```

4. Reapply the stashed changes:
   ```bash
   git stash pop
   ```

If the rebase encounters conflicts, pause and inform the user so they can resolve them before attempting to pop the stash.
