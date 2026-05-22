---
name: commit
description: "Use when user says 'commit', 'save changes', 'wrap up', 'done with changes', or wants to create a git commit. Analyzes staged/unstaged changes and generates conventional commit messages based on project history."
disable-model-invocation: true
allowed-tools: Bash, Read, AskUserQuestion
---

# /commit

This skill analyzes code changes and generates a high-quality commit message that follows the project's existing style.

## Pre-fetched Context

- **Recent commits:** !`git log --oneline -15 2>/dev/null || echo "No git history"`
- **Current branch:** !`git branch --show-current 2>/dev/null`
- **Staged changes:** !`git diff --staged --stat 2>/dev/null | head -30`
- **Unstaged changes:** !`git diff --stat 2>/dev/null | head -20`
- **File status:** !`git status -s 2>/dev/null | head -20`

## Actions

1. **Step 1: Analyze Context**
   - Review the pre-fetched git information above.
   - If there are no changes (both staged and unstaged empty), inform the user and stop.

2. **Step 2: Handle Unstaged Changes**
   - If there are only unstaged changes, ask the user if they want to stage files first.
   - Use `AskUserQuestion` to present options: stage all, stage specific files, or cancel.

3. **Step 3: Analyze Changes**
   - Read the actual diff content for staged changes: `git diff --staged`
   - Understand what was changed and why.

4. **Step 4: Generate Commit Message**
   - Based on the project's historical commit style (from pre-fetched context), generate a message that:
     - Follows the project's format (conventional commits, emoji usage, etc.)
     - Accurately and concisely describes the changes
     - Explains the "why" behind the change, not just the "what"

5. **Step 5: Propose and Commit**
   - Use `AskUserQuestion` to present the generated message.
   - Options: use as-is, edit, or cancel.
   - If confirmed, run `git commit -m "<message>"`.
