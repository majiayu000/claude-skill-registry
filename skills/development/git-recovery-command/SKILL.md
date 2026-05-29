---
name: git-recovery
description: Quick recovery from common git mistakes including undo commits, recover branches, and reflog operations. Use when you need to undo, recover, or fix Git history.
context: inherit
version: 1.0.0
author: SkillForge
tags: [git, recovery, undo, reflog, reset]
user-invocable: true
---

# Git Recovery

Interactive recovery from common git mistakes. Safe operations with verification steps.

## Quick Start

```bash
/git-recovery
```

## Recovery Scenarios

When invoked, present these options to the user:

### Option 1: Undo Last Commit (Keep Changes)

**Scenario**: You committed but want to modify the changes before recommitting.

```bash
# Check current state first
git log --oneline -3
git status

# Undo commit, keep changes staged
git reset --soft HEAD~1

# Verify
git status  # Changes should be staged
git log --oneline -1  # Previous commit is now HEAD
```

**Safety**: Non-destructive. All changes remain staged.

---

### Option 2: Undo Last Commit (Discard Changes)

**Scenario**: You committed something completely wrong and want to throw it away.

**WARNING: DESTRUCTIVE - Changes will be lost!**

```bash
# CRITICAL: First, save a backup reference
BACKUP_REF=$(git rev-parse HEAD)
echo "Backup ref: $BACKUP_REF (save this to recover if needed)"

# Show what will be lost
git show HEAD --stat

# Confirm with user before proceeding
# Then execute:
git reset --hard HEAD~1

# Verify
git log --oneline -3
git status  # Should be clean
```

**Recovery**: If you made a mistake, run `git reset --hard $BACKUP_REF`

---

### Option 3: Recover Deleted Branch

**Scenario**: You deleted a branch and need it back.

```bash
# Find the branch's last commit in reflog
git reflog | grep -i "branch-name"
# Or search all recent activity:
git reflog --all | head -30

# Once you find the commit hash (e.g., abc1234):
git checkout -b recovered-branch abc1234

# Verify
git log --oneline -5
git branch -v | grep recovered
```

**Note**: Reflog keeps entries for ~90 days by default.

---

### Option 4: Reset File to Last Commit

**Scenario**: You modified a file and want to discard local changes.

**WARNING: DESTRUCTIVE - Uncommitted changes to file will be lost!**

```bash
# Show current changes to file
git diff path/to/file

# Confirm with user before proceeding
# Then restore:
git checkout HEAD -- path/to/file

# Or using newer git restore (Git 2.23+):
git restore path/to/file

# Verify
git status path/to/file  # Should show no changes
git diff path/to/file    # Should be empty
```

---

### Option 5: Undo a Rebase

**Scenario**: A rebase went wrong and you want to return to pre-rebase state.

```bash
# Find the pre-rebase state
git reflog | head -20
# Look for entry like: "rebase (start): checkout main"
# The entry BEFORE that is your pre-rebase state

# Alternative: ORIG_HEAD is set automatically before rebase
git log --oneline ORIG_HEAD -3

# Reset to pre-rebase state
git reset --hard ORIG_HEAD

# Verify
git log --oneline -5
git status
```

**Safety**: ORIG_HEAD is overwritten by other operations, use reflog if ORIG_HEAD is stale.

---

### Option 6: Undo a Merge

**Scenario**: You merged a branch and want to undo it.

```bash
# If merge commit exists and NOT pushed:
git log --oneline -5  # Find the merge commit

# Reset to before merge
git reset --hard HEAD~1

# If you need to specify which parent:
git reset --hard ORIG_HEAD

# Verify
git log --oneline -5
git branch -v
```

**WARNING**: If already pushed, use `git revert -m 1 <merge-commit>` instead to create a new commit that undoes the merge.

---

### Option 7: Find Lost Commits (Reflog Deep Dive)

**Scenario**: You lost commits and need to find them.

```bash
# View full reflog with dates
git reflog --date=relative

# Search for specific text in commit messages
git reflog | xargs -I {} git log -1 --format="%h %s" {} 2>/dev/null | grep "search-term"

# Show reflog for specific branch
git reflog show branch-name

# Once found (e.g., abc1234), examine it:
git show abc1234

# Recover by creating a branch or cherry-picking:
git branch recovered-work abc1234
# Or:
git cherry-pick abc1234
```

---

### Option 8: Unstage Files (Keep Changes)

**Scenario**: You staged files you didn't mean to stage.

```bash
# Unstage specific file
git reset HEAD path/to/file

# Or using newer git restore (Git 2.23+):
git restore --staged path/to/file

# Unstage all files
git reset HEAD

# Verify
git status  # Files should be unstaged but modified
```

**Safety**: Non-destructive. Changes remain in working directory.

---

## Interactive Workflow

When `/git-recovery` is invoked:

1. **Show current git state**:
   ```bash
   git status
   git log --oneline -5
   ```

2. **Present recovery options**:
   ```
   Git Recovery Options:
   1. Undo last commit (keep changes staged)
   2. Undo last commit (discard changes) [DESTRUCTIVE]
   3. Recover deleted branch
   4. Reset file to last commit [DESTRUCTIVE]
   5. Undo a rebase
   6. Undo a merge
   7. Find lost commits (reflog search)
   8. Unstage files

   Which scenario? (1-8):
   ```

3. **For destructive operations**:
   - Always show what will be lost
   - Provide backup command
   - Require explicit confirmation

4. **After recovery**:
   - Run verification commands
   - Show new state
   - Confirm success

## Safety Rules

1. **NEVER use `--force` on shared branches** without explicit user confirmation
2. **ALWAYS show backup reference** before destructive operations
3. **ALWAYS verify** after each recovery operation
4. **Check if changes are pushed** before suggesting reset vs revert

## Common Gotchas

| Problem | Wrong Approach | Right Approach |
|---------|---------------|----------------|
| Undo pushed commit | `git reset --hard` | `git revert <commit>` |
| Recover deleted branch | Panic | `git reflog` + checkout |
| Undo rebase on shared branch | `git reset` | `git revert` each commit |
| Lost commits after reset | Assume lost | `git reflog` saves the day |

## Related Skills

- commit: Create commits with validation
- stacked-prs: Manage PR stacks safely
- release-management: Handle release branch operations

## References

- [Git Reflog Documentation](https://git-scm.com/docs/git-reflog)
- [Git Reset Documentation](https://git-scm.com/docs/git-reset)
