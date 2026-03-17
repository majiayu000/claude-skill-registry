---
name: git-recovery
description: Safety practices and recovery techniques for Git. Covers reflog usage, reset vs revert strategies, recovering lost commits, undoing mistakes, and preventing data loss. Helps AI agents safely navigate Git operations and recover from errors.
---

# Git Safety and Recovery

**Purpose:** This skill teaches AI agents to work safely with Git and recover from common mistakes without losing work.

## Core Principles

1. **Git Rarely Deletes** - Almost everything is recoverable via reflog
2. **Understand Before Destroying** - Know what `--hard`, `--force` do
3. **Backup Before Risky Operations** - Use stash or branches
4. **Revert, Don't Reset** - For shared branches

## Understanding Git's Safety Net

### The Reflog (Your Safety Net)

**What is reflog?**
Git's reflog records every HEAD movement. It's your "undo history" for Git operations.

```bash
# ✓ View reflog
git reflog

# Output shows every commit, checkout, reset, rebase, etc:
abc123 HEAD@{0}: commit: feat(auth): add login
def456 HEAD@{1}: checkout: moving from main to feature
ghi789 HEAD@{2}: pull: fast-forward
jkl012 HEAD@{3}: reset: moving to HEAD~1
mno345 HEAD@{4}: commit: fix(bug): temporary fix
```

**How long does reflog keep data?**
- Default: 90 days for reachable commits
- 30 days for unreachable commits
- Configurable via `gc.reflogExpire`

### What Can Be Recovered?

```bash
# ✓ CAN RECOVER:
- Deleted branches (if deleted recently)
- Reset commits (within 90 days)
- Amended commits (original still in reflog)
- Rebased commits (original still in reflog)
- Dropped stashes (if recent)

# ✗ CANNOT RECOVER:
- Unstaged changes that were never committed
- Untracked files that were never added
- Commits older than gc.reflogExpire
- Files explicitly removed with git clean -f
```

## Common Mistakes and Fixes

### Mistake 1: Accidentally Deleted Branch

```bash
# ✗ MISTAKE: Deleted wrong branch
git branch -D feature/important-work
# Deleted branch feature/important-work (was abc123).

# ✓ FIX: Recover from reflog
git reflog | grep "important-work"
# abc123 HEAD@{5}: commit: Last commit on important-work

# Recreate branch at that commit
git switch -c feature/important-work abc123

# Or use branch -C to force create
git branch feature/important-work abc123
git switch feature/important-work
```

### Mistake 2: Reset Too Far

```bash
# ✗ MISTAKE: Reset and lost commits
git reset --hard HEAD~3
# Now 3 commits are "gone"

# ✓ FIX: Find commits in reflog
git reflog
# abc123 HEAD@{0}: reset: moving to HEAD~3
# def456 HEAD@{1}: commit: feat(auth): important feature  ← Want this!

# Reset back to before the mistake
git reset --hard def456
# Or
git reset --hard HEAD@{1}
```

### Mistake 3: Committed to Wrong Branch

```bash
# ✗ MISTAKE: Committed to main instead of feature branch
git switch main
git add src/feature.js
git commit -m "feat(feature): add new feature"
# Oops! This should be on feature branch

# ✓ FIX: Move commit to correct branch

# Create feature branch (includes the commit)
git switch -c feature/new-feature

# Go back to main and remove the commit
git switch main
git reset --hard HEAD~1

# Now:
# - feature/new-feature has the commit
# - main is back to previous state
```

### Mistake 4: Amended Wrong Commit

```bash
# ✗ MISTAKE: Amended commit that shouldn't be changed
git commit --amend -m "New message"
# Oops! Original commit was important

# ✓ FIX: Find original commit in reflog
git reflog
# abc123 HEAD@{0}: commit (amend): New message
# def456 HEAD@{1}: commit: Original message  ← Want this!

# Reset to original commit
git reset --hard def456
```

### Mistake 5: Rebased and Lost Commits

```bash
# ✗ MISTAKE: Rebase went wrong, some commits disappeared
git rebase -i HEAD~5
# Accidentally dropped important commits

# ✓ FIX: Abort or recover from reflog

# If still in rebase:
git rebase --abort

# If rebase already finished:
git reflog
# Find "rebase (start)" entry
# abc123 HEAD@{10}: rebase (start): checkout main
# def456 HEAD@{11}: commit: Important commit  ← Before rebase started

# Reset to before rebase
git reset --hard def456
```

### Mistake 6: Force Pushed Wrong Branch

```bash
# ✗ MISTAKE: Force pushed and overwrote remote commits
git push --force origin main
# Overwrote teammate's commits!

# ✓ FIX: Depends on situation

# If you still have local copy of correct state:
git reflog
git reset --hard <correct-commit>
git push --force-with-lease origin main

# If you don't have it, ask teammate to push their version:
# Teammate runs:
git push --force origin main

# Or restore from remote reflog (if server keeps it):
git fetch origin
git log origin/main@{1}  # One state ago
```

### Mistake 7: Accidentally Removed Staged Changes

```bash
# ✗ MISTAKE: Used git restore --staged and lost work
git restore --staged src/important.js
git restore src/important.js  # Oops! Lost changes

# ✓ PREVENTION: Check before restoring
git diff src/important.js  # See what will be lost
git stash push src/important.js  # Safer alternative

# ✗ CANNOT FIX: Unstaged changes cannot be recovered
# Prevention is key!
```

## Reset vs Revert vs Restore

### Decision Tree

```
What do you want to undo?
├─ Local changes not committed yet
│  └─> git restore <file>
│
├─ Staging area (unstage)
│  └─> git restore --staged <file>
│
├─ Last commit (not pushed)
│  ├─ Keep changes in working directory
│  │  └─> git reset --soft HEAD~1
│  │
│  └─ Discard changes completely
│     └─> git reset --hard HEAD~1
│
└─ Commit already pushed
   └─> git revert <commit>  (creates new commit)
```

### Git Reset (For Local Changes)

```bash
# Three modes of reset:

# 1. --soft: Move HEAD, keep staged and working directory
git reset --soft HEAD~1
# Use case: Undo commit, keep all changes staged
# Safe: Yes (changes preserved)

# 2. --mixed (default): Move HEAD, unstage, keep working directory
git reset HEAD~1
# OR
git reset --mixed HEAD~1
# Use case: Undo commit, keep changes but unstaged
# Safe: Yes (changes preserved in working directory)

# 3. --hard: Move HEAD, discard staged and working directory
git reset --hard HEAD~1
# Use case: Completely undo commit and discard changes
# Safe: NO (changes lost, but recoverable from reflog)
```

### Reset Examples

```bash
# ✓ SAFE: Undo last commit, keep changes
git reset --soft HEAD~1
# Now changes are staged, ready to re-commit differently

# ✓ SAFE: Undo last commit, unstage changes
git reset HEAD~1
# Now changes are in working directory, unstaged

# ✗ DESTRUCTIVE: Undo commit and discard all changes
git reset --hard HEAD~1
# Changes are "gone" (but recoverable from reflog)

# ✓ SAFE: Reset to specific commit
git reset --soft abc123
# All commits after abc123 are undone, changes staged

# ✓ VISUAL: See what would be reset
git log HEAD~3..HEAD  # Shows commits that would be undone
git diff HEAD~3  # Shows changes that would be affected
```

### Git Revert (For Shared Branches)

```bash
# ✓ SAFE: Undo commit on shared branch
git revert abc123

# Creates NEW commit that undoes changes:
#   * Revert "feat(auth): add OAuth"  ← New commit
#   * feat(auth): add OAuth           ← Original commit
#   * Previous commit

# Why use revert instead of reset?
# - Doesn't rewrite history
# - Safe for shared branches
# - Preserves audit trail
```

### Revert Examples

```bash
# ✓ Revert single commit
git revert abc123
# Opens editor for revert commit message

# ✓ Revert without opening editor
git revert abc123 --no-edit

# ✓ Revert multiple commits
git revert abc123 def456 ghi789

# ✓ Revert range of commits
git revert HEAD~3..HEAD

# ✓ Revert merge commit
git revert -m 1 abc123
# -m 1 means keep first parent (usually main)
```

### Comparison Table

| Command | Changes History? | Safe for Shared? | Recoverable? | Use Case |
|---------|------------------|------------------|--------------|----------|
| `git restore` | No | Yes | No (working dir changes lost) | Undo local file changes |
| `git reset --soft` | Yes | No | Yes (via reflog) | Undo commit, keep changes staged |
| `git reset --mixed` | Yes | No | Yes (via reflog) | Undo commit, keep changes unstaged |
| `git reset --hard` | Yes | No | Yes (via reflog) | Undo commit, discard changes |
| `git revert` | No | Yes | N/A (creates new commit) | Undo commit on shared branch |

## Recovery Workflows

### Workflow 1: Find and Recover Lost Commit

```bash
# 1. Search reflog for lost commit
git reflog | grep -i "search term"

# OR view all reflog
git reflog

# 2. Examine commit content
git show abc123

# 3. Recover options:

# Option A: Create new branch at that commit
git switch -c recovered-work abc123

# Option B: Cherry-pick the commit
git cherry-pick abc123

# Option C: Reset current branch to that commit
git reset --hard abc123
```

### Workflow 2: Recover Deleted Branch

```bash
# 1. Find branch in reflog
git reflog | grep "branch-name"
# OR
git reflog | grep "checkout"

# 2. Find last commit on that branch
# abc123 HEAD@{5}: commit: Last commit on branch-name

# 3. Recreate branch
git switch -c branch-name abc123

# 4. Verify
git log
```

### Workflow 3: Undo Bad Merge

```bash
# Just merged, but it was wrong

# ✓ OPTION 1: Reset (if not pushed)
git reset --hard HEAD~1

# ✓ OPTION 2: Revert (if already pushed)
git revert -m 1 HEAD
# -m 1 keeps the main branch parent

# ✓ OPTION 3: Abort (if still in merge)
git merge --abort
```

### Workflow 4: Recover from Bad Rebase

```bash
# Rebase went wrong

# ✓ OPTION 1: Abort (if still in rebase)
git rebase --abort

# ✓ OPTION 2: Recover from reflog (if already finished)
git reflog
# Find entry before rebase started:
# abc123 HEAD@{10}: checkout: moving from feature to main
# def456 HEAD@{11}: commit: Last commit before rebase

git reset --hard def456
```

### Workflow 5: Recover Dropped Stash

```bash
# Accidentally dropped stash

# 1. Find stash in reflog
git reflog | grep stash
# abc123 WIP on main: Previous stash
# def456 index on main: Another stash

# 2. Create branch from stash commit
git switch -c recovered-stash abc123

# 3. Apply the stash
git stash apply abc123

# OR directly apply from reflog
git stash apply abc123
```

## Preventive Measures

### Before Risky Operations

```bash
# ✓ BACKUP 1: Create safety branch
git switch -c backup-before-rebase
git switch feature-branch
# Do risky operation
# If successful, delete backup:
git branch -d backup-before-rebase

# ✓ BACKUP 2: Use stash
git stash push -m "Backup before risky operation"
# Do risky operation
# If successful:
git stash drop
# If failed:
git stash pop

# ✓ BACKUP 3: Tag current state
git tag backup-$(date +%Y%m%d-%H%M%S)
# Do risky operation
# If successful:
git tag -d backup-20240115-143000
```

### Configure Safety Settings

```bash
# ✓ Require confirmation for destructive operations
git config --global alias.yolo '!echo "Are you sure? Use git reset --hard if certain"'

# ✓ Increase reflog retention
git config --global gc.reflogExpire 180  # 180 days instead of 90
git config --global gc.reflogExpireUnreachable 60  # 60 days instead of 30

# ✓ Always use --force-with-lease
git config --global alias.pushf 'push --force-with-lease'

# ✓ Protect against accidental git clean
git config --global clean.requireForce true
```

### Pre-operation Checklist

Before running destructive commands:

- [ ] Do I have a backup? (branch, tag, or stash)
- [ ] Is this branch pushed to remote? (additional backup)
- [ ] Have I verified what will be changed? (git diff, git log)
- [ ] Do I understand what this command does?
- [ ] Can I recover using reflog if something goes wrong?

## Advanced Recovery

### Recover Specific Files from History

```bash
# ✓ Restore file from specific commit
git restore --source=abc123 src/important.js

# ✓ Restore file from before it was deleted
git log --all --full-history -- src/deleted-file.js
# Find commit where it existed
git restore --source=abc123 src/deleted-file.js

# ✓ Restore file from stash
git show stash@{0}:src/file.js > src/file.js
```

### Recover from git clean

```bash
# ✗ PROBLEM: Ran git clean and deleted untracked files
git clean -fd
# Deleted important-file.js (untracked)

# ✓ LIMITED RECOVERY OPTIONS:

# Option 1: Check editor auto-save
# Many editors keep unsaved file backups

# Option 2: Check OS trash/recycle bin
# Some Git GUIs move files to trash instead of deleting

# Option 3: File recovery tools
# Use OS-level file recovery (PhotoRec, TestDisk, etc.)

# ✗ PREVENTION: Always use -n first
git clean -nfd  # -n = dry run, shows what would be deleted
# Review output
git clean -fd   # Actually delete
```

### Recover from Rewritten History

```bash
# Someone force-pushed and rewrote history

# ✓ Find old commits in local reflog
git reflog
git log --all --oneline

# ✓ Recovery options:

# Option 1: Push your version (if yours is correct)
git push --force-with-lease origin main

# Option 2: Merge both versions
git fetch origin
git merge origin/main
# Resolve conflicts
git push

# Option 3: Cherry-pick missing commits
git cherry-pick abc123 def456
git push
```

## Common Dangerous Commands

### Commands to Use Carefully

```bash
# ✗ DANGEROUS: Can lose work

git reset --hard <commit>
# Discards all changes in working directory
# Prevention: git stash first

git clean -fd
# Deletes untracked files permanently
# Prevention: git clean -nfd first (dry run)

git push --force
# Overwrites remote, can lose others' work
# Prevention: Use --force-with-lease instead

git rebase -i
# Can drop/edit commits, complex conflicts
# Prevention: Create backup branch first

git branch -D <branch>
# Deletes branch even if not merged
# Prevention: Use -d first (safer), recover from reflog if needed
```

### Safe Alternatives

```bash
# ✓ SAFER ALTERNATIVES:

# Instead of: git reset --hard
git stash  # Or git stash push -u to include untracked

# Instead of: git push --force
git push --force-with-lease

# Instead of: git clean -fd
git clean -nfd  # Dry run first
git stash push -u  # Stash untracked files

# Instead of: git branch -D
git branch -d  # Refuses if not merged
git merge --no-ff <branch>  # Merge first, then delete

# Instead of: git reset --hard HEAD~3
git reset --soft HEAD~3  # Keep changes
git restore --staged .   # Unstage if needed
```

## Quick Reference

### Recovery Commands

```bash
# View reflog
git reflog
git reflog show <branch>

# Recover deleted branch
git switch -c <branch> <commit-hash>

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Undo last commit (discard changes)
git reset --hard HEAD~1
git reflog  # Can still recover

# Revert commit (safe for shared branches)
git revert <commit>

# Recover from bad merge
git reset --hard HEAD~1  # If not pushed
git revert -m 1 HEAD     # If pushed

# Find deleted file
git log --all --full-history -- <file>
git restore --source=<commit> <file>

# Recover dropped stash
git reflog | grep stash
git stash apply <stash-hash>
```

## Summary

**Key Principles:**
1. **Git rarely deletes** - Reflog keeps 90 days of history
2. **Backup before risky operations** - Branch, tag, or stash
3. **Use revert for shared branches** - Never reset public history
4. **Check before destroying** - Dry runs, diffs, logs
5. **Force-with-lease, not force** - Prevents accidental overwrites

**Essential Commands:**
```bash
git reflog                    # Your safety net
git reset --soft HEAD~1       # Undo commit, keep changes
git reset --hard <commit>     # Dangerous! Backup first
git revert <commit>           # Safe undo for shared branches
git switch -c name <hash>     # Recover deleted branch
```

**Remember:** Almost every mistake is recoverable. Stay calm, check reflog, and understand what each command does before running it.
