---
name: commit
description: Create a git commit with a contextual message based on current changes, then push the branch.
allowed-tools: [Bash]
---

## Context

- Current git status: !`git status`
- Current git diff (staged and unstaged changes): !`git diff HEAD`
- Current branch: !`git branch --show-current`
- Recent commits: !`git log --oneline -10`

## Your task

Based on the above changes, stage everything, create one commit with a contextual message, and push the current branch.

Required sequence:
1. Stage changes.
2. Create a single commit.
3. Push the current branch to origin (use `--set-upstream origin <branch>` if needed).

Do not use interactive commands and do not output extra commentary.
