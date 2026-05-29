---
name: worktree-sync
description: Sync current worktree with base branch to keep feature branch up to date
---

# Sync Git Worktree

Sync the current feature worktree with its base branch to incorporate latest changes.

## When to Use

Use this when:
- Your feature branch is behind the base branch
- You want to incorporate latest changes from main/master
- Before creating a pull request
- Regularly during long-running feature development

## Usage

```
/worktree-sync [base-branch]
```

**Arguments:**
- `base-branch` - Optional, defaults to main/master

## Instructions

### Step 1: Verify Current Location

```bash
# Check if we're in a worktree
CURRENT_DIR=$(pwd)
if [[ ! "$CURRENT_DIR" == *"/worktrees/"* ]]; then
  echo "⚠️  Warning: Not in a worktree directory"
  echo "Current: $CURRENT_DIR"
  read -p "Continue anyway? (y/n) " -n 1 -r
  echo
  if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    exit 1
  fi
fi

# Get current branch
CURRENT_BRANCH=$(git branch --show-current)
echo "Current branch: $CURRENT_BRANCH"
```

### Step 2: Determine Base Branch

```bash
# Use provided base or detect default branch
if [ -n "$1" ]; then
  BASE_BRANCH="$1"
else
  # Detect if main or master
  if git show-ref --verify --quiet refs/remotes/origin/main; then
    BASE_BRANCH="main"
  elif git show-ref --verify --quiet refs/remotes/origin/master; then
    BASE_BRANCH="master"
  else
    echo "Error: Could not determine base branch"
    exit 1
  fi
fi

echo "Base branch: $BASE_BRANCH"
```

### Step 3: Check for Uncommitted Changes

```bash
# Check working directory status
if ! git diff-index --quiet HEAD --; then
  echo ""
  echo "❌ Error: Uncommitted changes detected"
  echo ""
  git status --short
  echo ""
  echo "Please commit or stash changes before syncing:"
  echo "  git add ."
  echo "  git commit -m 'Your message'"
  echo "  OR"
  echo "  git stash"
  exit 1
fi

echo "✅ Working directory clean"
```

### Step 4: Fetch Latest Changes

```bash
echo ""
echo "Fetching latest from origin..."
git fetch origin

# Show how many commits behind/ahead
BEHIND=$(git rev-list --count HEAD..origin/$BASE_BRANCH)
AHEAD=$(git rev-list --count origin/$BASE_BRANCH..HEAD)

echo "Your branch is:"
echo "  $AHEAD commit(s) ahead of origin/$BASE_BRANCH"
echo "  $BEHIND commit(s) behind origin/$BASE_BRANCH"

if [ "$BEHIND" -eq 0 ]; then
  echo ""
  echo "✅ Already up to date with origin/$BASE_BRANCH"
  exit 0
fi
```

### Step 5: Rebase on Base Branch

```bash
echo ""
echo "Rebasing $CURRENT_BRANCH on origin/$BASE_BRANCH..."
echo ""

# Attempt rebase
if git rebase "origin/$BASE_BRANCH"; then
  echo ""
  echo "✅ Rebase successful!"
  echo ""
  echo "Your branch is now up to date with origin/$BASE_BRANCH"
  echo ""
  echo "Next steps:"
  echo "1. Test your changes still work"
  echo "2. Push with: git push --force-with-lease origin $CURRENT_BRANCH"
else
  echo ""
  echo "❌ Rebase failed with conflicts"
  echo ""
  echo "Conflicts in:"
  git diff --name-only --diff-filter=U
  echo ""
  echo "To resolve:"
  echo "1. Fix conflicts in the files above"
  echo "2. git add <resolved-files>"
  echo "3. git rebase --continue"
  echo ""
  echo "To abort:"
  echo "  git rebase --abort"
  exit 1
fi
```

### Step 6: Verify After Rebase

```bash
# Run tests if test command exists
if [ -f "package.json" ] && grep -q "\"test\":" package.json; then
  echo ""
  read -p "Run tests to verify? (y/n) " -n 1 -r
  echo
  if [[ $REPLY =~ ^[Yy]$ ]]; then
    npm test
  fi
fi

echo ""
echo "Sync complete! 🎉"
```

## Example Usage

**Basic sync:**
```bash
cd worktrees/user-authentication
/worktree-sync
```

Output:
```
Current branch: feature/user-authentication
Base branch: main
✅ Working directory clean

Fetching latest from origin...
Your branch is:
  3 commit(s) ahead of origin/main
  5 commit(s) behind origin/main

Rebasing feature/user-authentication on origin/main...

✅ Rebase successful!

Your branch is now up to date with origin/main

Next steps:
1. Test your changes still work
2. Push with: git push --force-with-lease origin feature/user-authentication
```

**Sync with specific branch:**
```bash
/worktree-sync develop
```

## Conflict Resolution Guide

### When Conflicts Occur

1. **Identify conflicting files:**
   ```bash
   git status
   ```

2. **Open each file and look for conflict markers:**
   ```
   <<<<<<< HEAD (your changes)
   your code
   =======
   their changes
   >>>>>>> origin/main
   ```

3. **Resolve conflicts:**
   - Keep your changes, their changes, or combine both
   - Remove conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`)
   - Test that code works

4. **Mark as resolved:**
   ```bash
   git add <file>
   ```

5. **Continue rebase:**
   ```bash
   git rebase --continue
   ```

### Common Conflict Scenarios

**Both modified same function:**
- Review both versions
- Combine best parts of each
- Ensure functionality preserved

**Deleted file vs modified file:**
- Decide if deletion or modification is correct
- `git rm <file>` to accept deletion
- `git add <file>` to keep modifications

**Renamed file conflicts:**
- Git usually handles this
- If not, manually rename and add

## Best Practices

**Sync Regularly:**
- Daily for active base branches
- Before starting each work session
- Before creating pull request

**Before Syncing:**
- Commit or stash all changes
- Ensure tests pass
- Review what you're rebasing onto

**After Syncing:**
- Run full test suite
- Check that features still work
- Use `--force-with-lease` when pushing (safer than `--force`)

**Communication:**
- Let team know if you're force-pushing
- Coordinate with others working on same branch

## Troubleshooting

**Error: "cannot rebase: You have unstaged changes"**
- Solution: Commit or stash changes first

**Error: "refusing to pull with rebase"**
- Solution: This is a sync operation, not pull
- Use this skill from within the worktree

**Rebase feels stuck:**
- Check `git status` for instructions
- Look for conflict markers in files
- Use `git rebase --abort` to start over

**After force push, others can't pull:**
- They need to: `git fetch && git reset --hard origin/branch-name`
- Coordinate force pushes with team
