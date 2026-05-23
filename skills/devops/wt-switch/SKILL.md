---
name: wt-switch
description: Switch development context to a different git worktree. Use when moving between different features or stories. Shows all available worktrees and provides navigation commands.
---

# /wt:switch - Switch to Another Worktree

## Description
Quick command to switch development context to a different worktree.

## Usage
```
/wt:switch
```

## What It Does

This slash command:
1. Activates the Git Worktree Manager skill (`@git-worktree`)
2. Automatically runs the `*switch` command
3. Shows available worktrees and helps you switch

## Workflow

The command will:
1. **List available worktrees** - Show all worktrees with numbers
2. **Ask which to switch to** - Interactive selection
3. **Provide cd command** - Give you the command to switch
4. **Show branch status** - Display current branch and status of target worktree

## Benefits

✅ **Quick Navigation** - See all worktrees and switch easily
✅ **Context Aware** - Shows current worktree
✅ **Status Preview** - See what's in the target worktree before switching

## Notes

- The command provides the `cd` command for you to run
- It cannot actually change your terminal's directory (shell limitation)
- Copy and paste the provided command to switch
