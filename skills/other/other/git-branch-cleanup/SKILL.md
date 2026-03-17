---
name: git-branch-cleanup
description: |
  Analyzes and safely cleans up local Git branches. Categorizes branches by merge status,
  staleness, and remote tracking. Provides interactive selection with safety guards.
  Use when the user wants to clean up branches, delete old branches, organize Git branches,
  or asks about which branches can be safely deleted.
compatibility: Requires git 2.17+ (for worktree support). Git 2.22+ recommended for `git branch --show-current`.
---

# Git Branch Cleanup

Safely organize and clean up local Git branches. Categorizes branches by merge status, staleness, and remote tracking, then guides users through safe deletion.

## Contents

- Quick Start
- Workflow (Steps 1-5)
- Commands Reference
- Dry Run Mode
- Safety Checklist

## Quick Start

1. Analyze branches (Step 1)
2. Categorize by safety level (Step 2)
3. Display results and ask user which to delete (Step 3)
4. Verify against safety guards (Step 4)
5. Execute deletion after confirmation (Step 5)

## Workflow

### Step 1: Branch Analysis

Collect information with these commands:

```bash
# Decide base branch (prefer auto-detect; fallback to main)
BASE_BRANCH="$(
  git symbolic-ref --quiet --short refs/remotes/origin/HEAD 2>/dev/null | sed 's@^origin/@@'
)"
[ -n "$BASE_BRANCH" ] || BASE_BRANCH=main

# List all branches with last commit date
git for-each-ref --sort=-committerdate refs/heads/ \
  --format='%(refname:short)|%(committerdate:relative)|%(upstream:trackshort)|%(contents:subject)'

# Merged branches (against base)
git branch --merged "$BASE_BRANCH"

# Unmerged branches
git branch --no-merged "$BASE_BRANCH"

# Branches whose upstream is gone (remote deleted)
git branch -vv | grep -F ': gone]' || true

# List worktrees (branches with '+' prefix in git branch -v have worktrees)
git worktree list

# Branches with worktrees ('+' prefix indicates worktree association)
git branch -v | grep '^+' || true

# Branches ahead of upstream (have unpushed commits)
git for-each-ref refs/heads \
  --format='%(refname:short) %(upstream:trackshort)' \
  | grep '>' || true
```

### Step 2: Categorization

Categorize branches by safety level:

| Category | Description | Safety |
|----------|-------------|--------|
| **Merged (Safe)** | Already merged to base branch | Safe to delete |
| **Gone Remote** | Remote branch deleted | Review recommended |
| **Stale** | No commits for 30+ days | Needs review |
| **Has Worktree** | Branch checked out in a worktree (`+` prefix in `git branch -v`) | Remove worktree first |
| **Ahead of Upstream** | Has unpushed commits | ⚠️ Do not delete |
| **Unmerged** | Active work in progress | Use caution |

> **Note**: 30 days is a reasonable default for stale detection. Adjust based on team's sprint cycle if needed (e.g., 14 days for 2-week sprints).

### Step 3: Display Format

```
## Branch Analysis Results

### Safe to Delete (Merged)
  - feature/login (3 weeks ago) - Add login feature
  - fix/typo (2 months ago) - Fix typo in readme

### Remote Deleted
  - feature/old-api (1 month ago) - Remote branch no longer exists

### ⚠️ Ahead of Upstream (DO NOT DELETE)
  - feature/wip (1 day ago) - Has 3 unpushed commits

### Stale Branches (30+ days)
  - experiment/cache (2 months ago) - Unmerged

### Active (Unmerged)
  - feature/new-dashboard (2 days ago) - Work in progress

---
Which categories would you like to delete?
1. Merged only (safest)
2. Merged + remote deleted
3. Select individually
```

### Step 4: Safety Guards

**Never delete these branches:**
- `main`
- `master`
- `trunk`
- `develop`
- `development`
- Currently checked out branch

Always confirm before deletion:
```
The following branches will be deleted:
  - feature/login
  - fix/typo

Continue? (y/N)
```

### Step 5: Execute Deletion

```bash
# After confirmation
git branch -d <branch-name>  # For merged branches
git branch -D <branch-name>  # Force delete (unmerged)
```

**For branches with worktrees**, remove the worktree first:

```bash
# Check if branch has a worktree
git worktree list | grep "\\[$branch\\]"

# Remove worktree before deleting branch
git worktree remove --force /path/to/worktree
git branch -D <branch-name>
```

**Bulk delete [gone] branches with worktree handling:**

```bash
# Process all [gone] branches, handling worktrees automatically
git branch -v | grep '\[gone\]' | sed 's/^[+* ]//' | awk '{print $1}' | while read branch; do
  echo "Processing branch: $branch"
  # Find and remove worktree if it exists
  worktree=$(git worktree list | grep "\\[$branch\\]" | awk '{print $1}')
  if [ ! -z "$worktree" ] && [ "$worktree" != "$(git rev-parse --show-toplevel)" ]; then
    echo "  Removing worktree: $worktree"
    git worktree remove --force "$worktree"
  fi
  # Delete the branch
  echo "  Deleting branch: $branch"
  git branch -D "$branch"
done
```

## Commands Reference

```bash
# Bulk delete merged branches (excluding protected branches and current branch)
# Notes:
# - Uses for loop + case for bash/zsh compatibility (avoids `while IFS= read` issues in zsh).
# - Uses case statement for exact-name matching (avoids grep regex edge cases).
# - Always exclude the current branch to prevent accidental self-deletion.
BASE_BRANCH="$(git symbolic-ref --quiet --short refs/remotes/origin/HEAD 2>/dev/null | sed 's@^origin/@@')"
[ -n "$BASE_BRANCH" ] || BASE_BRANCH=main
CURRENT_BRANCH="$(git branch --show-current)"
for branch in $(git branch --merged "$BASE_BRANCH" | sed 's/^[* ]*//'); do
  case "$branch" in
    main|master|trunk|develop|development|"$CURRENT_BRANCH"|"") continue ;;
    *) git branch -d "$branch" ;;
  esac
done

# Prune remote-tracking references (requires network access)
# Note: This may fail if offline or remote is unreachable.
# If it fails, skip this step - branch analysis still works with cached remote data.
git fetch --prune || echo "Warning: Could not reach remote. Using cached data."

# List oldest branches (30+ days)
git for-each-ref --sort=committerdate refs/heads/ \
  --format='%(committerdate:short) %(refname:short)' | head -20

# Worktree commands
git worktree list                              # List all worktrees
git worktree remove /path/to/worktree          # Remove a worktree
git worktree remove --force /path/to/worktree  # Force remove (even if dirty)
git worktree prune                             # Clean up stale worktree refs
```

## Dry Run Mode

Preview deletions without executing:

```bash
# Preview only
BASE_BRANCH="$(git symbolic-ref --quiet --short refs/remotes/origin/HEAD 2>/dev/null | sed 's@^origin/@@')"
[ -n "$BASE_BRANCH" ] || BASE_BRANCH=main
CURRENT_BRANCH="$(git branch --show-current)"
for branch in $(git branch --merged "$BASE_BRANCH" | sed 's/^[* ]*//'); do
  case "$branch" in
    main|master|trunk|develop|development|"$CURRENT_BRANCH"|"") ;;
    *) echo "$branch" ;;
  esac
done
```

Trigger dry-run mode if user says "--dry-run", "preview", or "just show me".

## Safety Checklist

Before deletion, verify:
- [ ] Not the current branch
- [ ] Not a protected branch (base/main/master/trunk/develop)
- [ ] No unpushed commits (ahead of upstream)
- [ ] Worktree removed first (if branch has associated worktree)
- [ ] User confirmation obtained

### Quick safety commands

```bash
# Show "ahead/behind" vs upstream for each local branch
git for-each-ref refs/heads \
  --format='%(refname:short)|%(upstream:short)|%(upstream:trackshort)|%(committerdate:relative)|%(contents:subject)' \
  --sort=-committerdate

# For a specific branch, confirm it's not ahead of upstream (if upstream exists)
# (Empty output => nothing unpushed)
git log --oneline @{u}..HEAD 2>/dev/null || echo "No upstream configured for this branch"

# Check if a branch has an associated worktree
# ('+' prefix in git branch -v output indicates worktree)
git branch -v | grep "^+" | awk '{print $2}'

# Find worktree path for a specific branch
git worktree list | grep "\\[branch-name\\]"
```
