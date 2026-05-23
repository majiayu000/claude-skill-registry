---
name: git-recovery
description: Recover from Git mistakes safely. Undo commits, recover lost work, fix rebase disasters, and use reflog effectively.
context: inherit
version: 1.0.0
author: SkillForge
tags: [git, recovery, undo, reflog, reset, revert]
user-invocable: false
---

# Git Recovery

Every Git mistake is recoverable. Use these patterns to undo errors safely.

## When to Use

- Accidentally committed to wrong branch
- Need to undo a commit
- Lost commits after rebase
- Need to recover deleted branch
- Made a mistake with reset

## Quick Reference: The Safety Net

```bash
# ALWAYS check reflog first - it has everything
git reflog

# Shows ALL recent HEAD movements
# Even "deleted" commits live here for 90 days
```

---

## Undo Last Commit

### Keep Changes (Most Common)

```bash
# Undo commit, keep changes staged
git reset --soft HEAD~1

# Undo commit, keep changes unstaged
git reset --mixed HEAD~1  # or just: git reset HEAD~1

# Now you can re-commit correctly
git add -p
git commit -m "Better commit message"
```

### Discard Changes Completely

```bash
# DANGER: Loses all changes in last commit
git reset --hard HEAD~1

# Recover if needed
git reflog
git reset --hard <sha>
```

### Already Pushed? Use Revert

```bash
# Creates new commit that undoes the changes
# Safe for shared branches
git revert HEAD

# Revert specific commit
git revert abc1234

# Revert without auto-commit (edit first)
git revert --no-commit abc1234
```

---

## Committed to Wrong Branch

### Haven't Pushed Yet

```bash
# On wrong branch (e.g., main)
# 1. Note the commit SHA
git log -1  # abc1234

# 2. Undo on wrong branch
git reset --hard HEAD~1

# 3. Apply to correct branch
git checkout correct-branch
git cherry-pick abc1234
```

### Already Pushed to Wrong Branch

```bash
# 1. Cherry-pick to correct branch
git checkout correct-branch
git cherry-pick abc1234
git push origin correct-branch

# 2. Revert on wrong branch
git checkout wrong-branch
git revert abc1234
git push origin wrong-branch
```

---

## Recover Lost Commits

### After Bad Reset

```bash
# Find lost commits in reflog
git reflog

# Output shows:
# abc1234 HEAD@{0}: reset: moving to HEAD~3
# def5678 HEAD@{1}: commit: Important work  <-- This is lost!
# ghi9012 HEAD@{2}: commit: More work       <-- This too!

# Recover by resetting to before the bad reset
git reset --hard HEAD@{1}

# Or cherry-pick specific commits
git cherry-pick def5678
```

### After Bad Rebase

```bash
# Find pre-rebase state
git reflog

# Look for "rebase: start" entry
# abc1234 HEAD@{5}: rebase: start  <-- State before rebase
# def5678 HEAD@{6}: commit: Work   <-- Your commits before rebase

# Abort if still rebasing
git rebase --abort

# Or recover pre-rebase state
git reset --hard HEAD@{6}
```

---

## Recover Deleted Branch

```bash
# Find the branch's last commit
git reflog | grep "checkout: moving from deleted-branch"

# Or search by commit message
git reflog | grep "your commit message"

# Recreate branch at that commit
git checkout -b recovered-branch abc1234
```

---

## Fix Rebase Disasters

### Mid-Rebase Conflict Hell

```bash
# Option 1: Abort and retry
git rebase --abort

# Option 2: Skip problematic commit
git rebase --skip

# Option 3: Continue after fixing
git add .
git rebase --continue
```

### Rebase Went Wrong, Already Pushed

```bash
# Find pre-rebase state
git reflog

# Reset to pre-rebase
git reset --hard HEAD@{N}  # Where N is before rebase

# Force push (ONLY on feature branches!)
git push --force-with-lease
```

---

## Undo Merge

### Before Push

```bash
# Undo merge commit
git reset --hard HEAD~1
```

### After Push

```bash
# Revert the merge (keeps history)
# -m 1 means keep first parent (your branch)
git revert -m 1 <merge-commit-sha>
git push
```

---

## Recover Stashed Changes

```bash
# List all stashes
git stash list

# Apply most recent stash
git stash pop

# Apply specific stash
git stash apply stash@{2}

# Recover accidentally dropped stash
# (within ~2 weeks)
git fsck --unreachable | grep commit | cut -d' ' -f3 | \
  xargs git log --oneline --merges --no-walk

# Or use reflog
git reflog | grep "WIP on"
```

---

## The Nuclear Options (Last Resort)

### Reset Everything to Remote

```bash
# DANGER: Loses all local changes
git fetch origin
git reset --hard origin/main
```

### Clean Untracked Files

```bash
# Preview what will be deleted
git clean -n

# Delete untracked files
git clean -f

# Delete untracked files AND directories
git clean -fd

# Delete ignored files too (fresh start)
git clean -fdx
```

---

## Recovery Decision Tree

```
What happened?
│
├─ Committed to wrong branch?
│  ├─ Not pushed → cherry-pick + reset
│  └─ Pushed → cherry-pick + revert
│
├─ Need to undo commit?
│  ├─ Keep changes → git reset --soft HEAD~1
│  ├─ Discard changes → git reset --hard HEAD~1
│  └─ Already pushed → git revert HEAD
│
├─ Lost commits?
│  └─ Check reflog → git reset --hard HEAD@{N}
│
├─ Deleted branch?
│  └─ Check reflog → git checkout -b name SHA
│
├─ Bad merge?
│  ├─ Not pushed → git reset --hard HEAD~1
│  └─ Pushed → git revert -m 1 SHA
│
└─ Rebase disaster?
   ├─ Still rebasing → git rebase --abort
   └─ Completed → reflog → reset
```

---

## Prevention Tips

```bash
# 1. Backup before dangerous operations
git branch backup-before-rebase

# 2. Use --force-with-lease instead of --force
git push --force-with-lease  # Safer, fails if remote changed

# 3. Set up pre-push hook for main branch
# See branch-strategy skill

# 4. Commit early, commit often
# More recovery points = easier recovery
```

---

## Best Practices

1. **Check reflog first** - It's your undo history
2. **Use reset --soft** - Keeps your work safe
3. **Revert for pushed commits** - Don't rewrite public history
4. **Force-with-lease** - Safer than force push
5. **Backup branches** - Before risky operations
6. **Stay calm** - Git almost never loses data permanently

## Related Skills

- atomic-commits: Prevention through good habits
- branch-strategy: Safe workflows
- stacked-prs: Managing complex branches

## References

- [Reflog Deep Dive](references/reflog.md)
- [Reset vs Revert](references/reset-vs-revert.md)
