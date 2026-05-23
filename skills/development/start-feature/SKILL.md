---
name: start-feature
description: Commit or stash current work, then start a new feature using worktree workflow. Use when beginning work on a new story or feature, ensures clean state before starting new work.
---

# /start-feature - Commit and Start New Feature

## Description
Commits or stashes current work, then invokes the Dev agent to start a new feature using the worktree workflow.

## Usage
```
/start-feature
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
# User provides: "WIP: feature implementation"

# Stage all changes
git add -A

# Commit
git commit -m "{user_message}"

# Push to current branch
git push origin HEAD
```

**Option 2: Stash Changes**
```bash
# Ask for stash message (optional)
# User provides: "WIP on gallery feature"

# Stash with message
git stash push -m "{user_message}"

# Confirm
echo "✅ Changes stashed. Use 'git stash pop' to restore."
```

**Option 3: Discard Changes**
```bash
# Warn user
echo "⚠️  WARNING: This will permanently delete all uncommitted changes!"
echo "Are you sure? (yes/no)"

# If yes:
git reset --hard HEAD
git clean -fd

echo "✅ All changes discarded."
```

**Option 4: Cancel**
```
❌ Operation cancelled. Your changes are untouched.
```

### Step 3: Invoke Dev Agent

After changes are handled (or if there were no changes):

```
✅ Working directory is clean!

Invoking Dev agent to start new feature...

@dev
*start-work
```

Then the Dev agent takes over and runs the `start-worktree-from-story` task.

## Benefits

✅ **Safe Workflow** - Never lose uncommitted work
✅ **Clean State** - Start new features from clean working directory
✅ **One Command** - Handles commit + agent invocation
✅ **Flexible** - Choose commit, stash, or discard
✅ **Seamless** - Automatically transitions to Dev agent

## Notes

- This is a **slash command** (one-shot operation)
- After handling changes, it **invokes the Dev skill** (`@dev`)
- The Dev skill then runs the `*start-work` command
- This creates a smooth transition from current work to new feature
