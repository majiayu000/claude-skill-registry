---
name: worktree-cleanup
description: Clean up completed worktrees after feature is merged
---

# Cleanup Git Worktree

Remove a git worktree and associated files after feature is merged.

## When to Use

Use this when:
- Feature branch has been merged to main
- Worktree is no longer needed
- Want to clean up disk space
- Abandoning a feature/experiment

## Usage

```
/worktree-cleanup <feature-name> [--force]
```

**Arguments:**
- `feature-name` - Name of the worktree to remove
- `--force` - Skip safety checks, force removal

## Instructions

### Step 1: Validate Input

```bash
if [ -z "$1" ]; then
  echo "Error: Feature name required"
  echo "Usage: /worktree-cleanup <feature-name> [--force]"
  echo ""
  echo "Available worktrees:"
  git worktree list
  exit 1
fi

FEATURE_NAME="$1"
FORCE_MODE=false

if [ "$2" == "--force" ]; then
  FORCE_MODE=true
fi

WORKTREE_PATH="worktrees/$FEATURE_NAME"
BRANCH_NAME="feature/$FEATURE_NAME"
PLAN_DIR="plans/active/$FEATURE_NAME"
```

### Step 2: Verify Worktree Exists

```bash
if [ ! -d "$WORKTREE_PATH" ]; then
  echo "❌ Error: Worktree not found: $WORKTREE_PATH"
  echo ""
  echo "Available worktrees:"
  git worktree list
  exit 1
fi

echo "Found worktree: $WORKTREE_PATH"
```

### Step 3: Safety Checks (Unless --force)

```bash
if [ "$FORCE_MODE" = false ]; then
  # Check if currently in the worktree being removed
  CURRENT_DIR=$(pwd)
  if [[ "$CURRENT_DIR" == *"$WORKTREE_PATH"* ]]; then
    echo "❌ Error: Cannot remove current worktree"
    echo "Please navigate to a different directory first"
    exit 1
  fi

  # Check if branch is merged
  cd "$WORKTREE_PATH"

  # Determine base branch
  if git show-ref --verify --quiet refs/remotes/origin/main; then
    BASE_BRANCH="main"
  else
    BASE_BRANCH="master"
  fi

  # Check if branch is merged into base
  if ! git branch -r --merged "origin/$BASE_BRANCH" | grep -q "$BRANCH_NAME"; then
    echo "⚠️  Warning: Branch may not be merged into $BASE_BRANCH"
    echo ""
    git log --oneline "$BRANCH_NAME" ^"origin/$BASE_BRANCH" | head -5
    echo ""
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
      echo "Cleanup cancelled"
      exit 1
    fi
  else
    echo "✅ Branch is merged into $BASE_BRANCH"
  fi

  # Check for uncommitted changes
  if ! git diff-index --quiet HEAD --; then
    echo "⚠️  Warning: Uncommitted changes detected:"
    echo ""
    git status --short
    echo ""
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
      echo "Cleanup cancelled"
      exit 1
    fi
  fi

  cd - > /dev/null
fi
```

### Step 4: Archive Plan (Optional)

```bash
if [ -d "$PLAN_DIR" ]; then
  echo ""
  read -p "Archive plan to plans/archived/? (y/n) " -n 1 -r
  echo
  if [[ $REPLY =~ ^[Yy]$ ]]; then
    mkdir -p plans/archived
    mv "$PLAN_DIR" "plans/archived/$FEATURE_NAME-$(date +%Y%m%d)"
    echo "✅ Plan archived to plans/archived/$FEATURE_NAME-$(date +%Y%m%d)"
  else
    rm -rf "$PLAN_DIR"
    echo "✅ Plan removed"
  fi
fi
```

### Step 5: Remove Worktree

```bash
echo ""
echo "Removing worktree: $WORKTREE_PATH"

# Remove the worktree
git worktree remove "$WORKTREE_PATH"

if [ $? -eq 0 ]; then
  echo "✅ Worktree removed"
else
  echo "❌ Failed to remove worktree"
  echo "Try: git worktree remove --force $WORKTREE_PATH"
  exit 1
fi
```

### Step 6: Delete Remote Branch (Optional)

```bash
echo ""
read -p "Delete remote branch origin/$BRANCH_NAME? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
  git push origin --delete "$BRANCH_NAME"
  echo "✅ Remote branch deleted"
fi
```

### Step 7: Delete Local Branch

```bash
echo ""
echo "Deleting local branch: $BRANCH_NAME"
git branch -d "$BRANCH_NAME"

if [ $? -ne 0 ]; then
  echo ""
  read -p "Force delete unmerged branch? (y/n) " -n 1 -r
  echo
  if [[ $REPLY =~ ^[Yy]$ ]]; then
    git branch -D "$BRANCH_NAME"
    echo "✅ Branch force deleted"
  fi
fi
```

### Step 8: Summary

```bash
echo ""
echo "✅ Cleanup complete!"
echo ""
echo "Removed:"
echo "  📁 Worktree: $WORKTREE_PATH"
echo "  🌿 Branch: $BRANCH_NAME"
if [ -d "plans/archived/$FEATURE_NAME-"* ] 2>/dev/null; then
  echo "  📋 Plan: Archived"
else
  echo "  📋 Plan: Removed"
fi
echo ""
echo "Remaining worktrees:"
git worktree list
```

## Example Usage

**Clean up merged feature:**
```bash
/worktree-cleanup user-authentication
```

Output:
```
Found worktree: worktrees/user-authentication
✅ Branch is merged into main

Archive plan to plans/archived/? (y/n) y
✅ Plan archived to plans/archived/user-authentication-20260204

Removing worktree: worktrees/user-authentication
✅ Worktree removed

Delete remote branch origin/feature/user-authentication? (y/n) y
✅ Remote branch deleted

Deleting local branch: feature/user-authentication
✅ Branch deleted

✅ Cleanup complete!

Removed:
  📁 Worktree: worktrees/user-authentication
  🌿 Branch: feature/user-authentication
  📋 Plan: Archived

Remaining worktrees:
/path/to/project  abc123 [main]
```

**Force cleanup:**
```bash
/worktree-cleanup abandoned-experiment --force
```

## Clean Up All Merged Worktrees

To clean up all merged worktrees at once:

```bash
# List merged branches
git branch --merged main | grep "feature/"

# For each merged feature branch
for branch in $(git branch --merged main | grep "feature/"); do
  feature_name=$(echo $branch | sed 's/feature\///')
  if [ -d "worktrees/$feature_name" ]; then
    /worktree-cleanup "$feature_name"
  fi
done
```

## Best Practices

**Before Cleanup:**
- Ensure PR is merged
- Verify all changes are in main/master
- Archive plan if you want to keep it
- Inform team if shared branch

**When to Clean Up:**
- Immediately after PR merge
- Weekly cleanup of old branches
- Before starting new features (keep workspace tidy)

**What Gets Removed:**
- Worktree directory and all files
- Local feature branch
- Optionally: remote branch, plan files

**What's Preserved:**
- Commits (they're in main/master)
- PR history on GitHub
- Archived plans (if chosen)

## Troubleshooting

**Error: "fatal: 'worktrees/X' is not a working tree"**
- Worktree already removed or path incorrect
- Solution: Check `git worktree list`

**Error: "fatal: 'worktrees/X' contains modified or untracked files"**
- Uncommitted changes in worktree
- Solution: Use `--force` or commit/stash changes first

**Cannot delete branch:**
- Branch not fully merged
- Solution: Use `git branch -D` (force delete) if you're sure

**Worktree removed but directory remains:**
- Directory not empty or permission issue
- Solution: Manually `rm -rf worktrees/feature-name`

## Recovery

If you accidentally deleted a worktree:

**Branch still exists:**
```bash
# Recreate worktree from existing branch
git worktree add worktrees/feature-name feature/feature-name
```

**Branch deleted but not merged:**
```bash
# Find the commit
git reflog | grep feature-name

# Recreate branch
git branch feature/feature-name <commit-hash>

# Recreate worktree
git worktree add worktrees/feature-name feature/feature-name
```

**Everything deleted:**
- Commits are lost if not pushed to remote
- Check GitHub PR if it existed
- Restore from local backup if available
