---
name: git-sync
description: Sync with remote repository using pull --rebase. Use when you need to update your local branch with remote changes.
disable-model-invocation: true
allowed-tools: Bash(git:*)
---

# Git Sync

Sync local branch with remote using rebase.

1. Fetch the latest changes from the remote repository.
   - Command: `git fetch origin`

2. Pull and rebase the current branch on top of the remote branch.
   - Command: `git pull origin HEAD --rebase`
   - If there are conflicts, resolve them, then `git rebase --continue`.
