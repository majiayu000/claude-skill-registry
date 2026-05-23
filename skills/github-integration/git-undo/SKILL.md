---
name: git-undo
description: Undo the last commit while keeping changes staged. Use when you need to fix a commit message or add missing files.
disable-model-invocation: true
allowed-tools: Bash(git:*)
---

# Git Undo

Undo the last commit but keep changes staged.

1. Undo the last commit but keep the file changes in the staging area.
   - Command: `git reset --soft HEAD~1`
   - This allows you to fix the commit message or add missing files before committing again.
