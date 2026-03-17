---
name: git-safety-hooks
description: Set up Claude Code hooks to block dangerous git commands (push, reset --hard, clean, branch -D, etc.) before they execute. Use when user wants to prevent destructive git operations or add git safety guardrails.
---

# Git Safety Hooks

Sets up PreToolUse hook that intercepts and blocks dangerous git commands before Claude executes them.

## Blocked Commands

- `git push` (all variants including `--force`)
- `git reset --hard`
- `git clean -f` / `git clean -fd`
- `git branch -D`
- `git checkout .` / `git restore .`

When blocked, Claude sees message that it doesn't have authority to run these commands.

## Installation

### 1. Ask Scope
Ask user: install for **this project** (`.claude/settings.json`) or **all projects** (`~/.claude/settings.json`)?

### 2. Copy Hook Script
From: `scripts/block-dangerous-git.sh`

To:
- **Project**: `.claude/hooks/block-dangerous-git.sh`
- **Global**: `~/.claude/hooks/block-dangerous-git.sh`

Make executable: `chmod +x <path>`

### 3. Add to Settings
See `configuration.md` for settings JSON examples

### 4. Verify
Test by asking Claude to run `git push` - should be blocked

## Customization

Edit blocked commands list in hook script.
