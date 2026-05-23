---
name: git-cm
description: Commit changes to git with a descriptive conventional commit message. Use when ready to commit staged or unstaged changes.
argument-hint: "[optional commit message]"
disable-model-invocation: true
allowed-tools: Bash(git:*)
---

# Git Commit

Commit changes with a conventional commit message.

1. Check the current git status to understand what has changed.
   - Command: `git status`

2. View the diff if necessary to understand the changes better.
   - Command: `git diff --staged` or `git diff`

3. Add all changes to the staging area (unless specific files are requested).
   - Command: `git add .`

4. Commit the changes with a descriptive and conventional commit message.
   - Command: `git commit -m "<type>: <subject>"`
   - Ensure the message follows conventional commit standards (e.g., feat, fix, chore, docs, refactor).
