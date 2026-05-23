---
name: wt-new
description: Create a new git worktree and branch for feature development. Use when starting a new feature or story that needs isolated development. Creates worktree in tree/ directory with proper branch setup.
---

# /wt:new - Create New Worktree and Branch

## Description
Quick command to activate the Git Worktree Manager skill and start a new feature worktree.

## Usage
```
/wt:new
```

## What It Does

This slash command:
1. Activates the Git Worktree Manager skill (`@git-worktree`)
2. Automatically runs the `*start-feature` command
3. Guides you through creating a new worktree with a new branch

## Workflow

The command will:
1. **Verify git repository** - Ensure you're in a valid git repo
2. **Ask for base branch** - Which branch to start from (e.g., `main`, `develop`)
3. **Ask for feature branch name** - Name for your new branch (e.g., `feature/gallery-123`)
4. **Checkout base branch** - Switch to the base branch
5. **Pull latest changes** - Ensure base is up-to-date
6. **Create worktree directory** - Create `tree/` if it doesn't exist
7. **Create worktree** - Create the new worktree at `tree/{branch-name}`
8. **Confirm success** - Show you the path to your new worktree

## Benefits

✅ **Quick Start** - One command to create a new worktree
✅ **Guided Process** - Interactive prompts for all inputs
✅ **Safe** - Verifies git state before making changes
✅ **Organized** - Keeps all worktrees in `tree/` directory
