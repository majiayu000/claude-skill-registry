---
name: switch-feature
description: Commit or stash current work, then switch to another existing worktree. Use when switching between features or stories, ensures changes are saved before switching.
---

# /switch-feature - Commit and Switch to Another Worktree

## Description
Commits or stashes current work, then helps you switch to another existing worktree.

## Usage
```
/switch-feature
```

## What It Does

### Step 1: Check Git Status
```bash
git status --porcelain
```

### Step 2: Handle Uncommitted Changes

**If there are uncommitted changes:**

Ask user:
```
⚠️  You have uncommitted changes. What would you like to do?

1. Commit changes
2. Stash changes
3. Discard changes (dangerous!)
4. Cancel
```

**Option 1: Commit Changes**
```bash
# Show current changes
git status

# Ask for commit message
git add -A
git commit -m "{user_message}"
git push origin HEAD
```

**Option 2: Stash Changes**
```bash
# Stash with message
git stash push -m "{user_message}"
```

**Option 3: Discard Changes**
```bash
# Warn and confirm
git reset --hard HEAD
git clean -fd
```

**Option 4: Cancel**
```
❌ Operation cancelled.
```

### Step 3: List Available Worktrees

```bash
git worktree list
```

Display to user:
```
Available worktrees:

1. /Users/user/project (main) [main branch]
2. /Users/user/project/tree/feature/gallery-123 [feature/gallery-123]
3. /Users/user/project/tree/bug/main-app-456 [bug/main-app-456]
4. /Users/user/project/tree/feature/auth-567 [feature/auth-567]

Which worktree would you like to switch to? (1-4)
```

### Step 4: Provide Switch Instructions

After user selects worktree #2:

```
✅ To switch to feature/gallery-123:

cd tree/feature/gallery-123

Or use this command to switch and open in new terminal:
cd tree/feature/gallery-123 && exec $SHELL

Your current changes have been committed/stashed safely.
```

## Benefits

✅ **Safe Switching** - Never lose uncommitted work
✅ **Quick Navigation** - See all worktrees at a glance
✅ **Clean Transitions** - Proper commit/stash before switching
✅ **Simple** - One command to handle everything

## Notes

- This is a **slash command** (one-shot operation)
- It doesn't actually change your terminal's directory (can't do that)
- Instead, it provides the `cd` command for you to run
- Your changes are safely committed or stashed before switching
