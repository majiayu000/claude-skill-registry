---
name: git-recovery
description: Recover from confusing git states. Use when git status is unexpected, commits seem lost, you have a detached HEAD, or merge conflicts are overwhelming.
---

# Git State Recovery

## When to Use

Use this skill when git state is confusing, commits seem lost, or you need to recover from a problematic git situation.

## First Response: STOP and Assess

**Do NOT run any git commands until you understand the current state.**
In particular, do not run any command that discards changes (`git restore`, `git checkout --`), especially in bulk.

```bash
git status
git log --oneline -10
git branch -vv
scripts/git/writer-lock.sh status
```

Share this output with the user before proceeding.

## Recovery Scenarios

### Scenario 1: Lost Uncommitted Work

If work was lost due to `reset --hard` or similar:

1. **Check reflog** (saves commits for ~30 days):
   ```bash
   git reflog
   ```

2. **Find the lost commit**:
   ```bash
   git reflog | grep -i "commit message keyword"
   ```

3. **Recover by creating a branch**:
   ```bash
   git branch recovery-branch <commit-hash>
   ```

### Scenario 2: Detached HEAD

If `git status` shows "HEAD detached":

1. **Check what you have**:
   ```bash
   git log --oneline -5
   ```

2. **If you have work you want to keep, create a branch to attach it**:
   ```bash
   git checkout -b recovery-branch
   ```

### Scenario 3: Merge Conflict Overwhelm

If conflicts are too complex:

1. **Abort the merge** (safe, no data loss):
   ```bash
   git merge --abort
   ```

2. **Don’t “fix” this by rewriting history.** Prefer a plain merge (or ask for human guidance):
   ```bash
   git fetch origin --prune
   git merge <target-branch>
   ```

### Scenario 4: Wrong Commits on Branch

If commits ended up on wrong branch:

1. **Note the commit hashes**:
   ```bash
   git log --oneline -5
   ```

2. **Cherry-pick to correct branch**:
   ```bash
   git checkout correct-branch
   git cherry-pick <commit-hash>
   ```

3. **Clean up the wrong branch safely**:
   - Prefer abandoning the wrong branch and continuing on the correct one, or
   - Revert the commits on the wrong branch:
     ```bash
     git checkout wrong-branch
     git revert <commit-hash>
     ```

## Safe Commands (Always OK)

| Command | Purpose |
|---------|---------|
| `git status` | See current state |
| `git log` | See commit history |
| `git reflog` | See all recent HEAD movements |
| `git branch -a` | List all branches |
| `git diff` | See uncommitted changes |

## Dangerous Commands (Agents: Never)

Never run these as an agent in Base-Shop. If one seems necessary, STOP and ask for human guidance.

| Command | Danger |
|---------|--------|
| `git reset --hard` | Loses uncommitted work |
| `git clean -fd` | Deletes untracked files |
| `git push --force` / `-f` / `--force-with-lease` | Overwrites remote history |
| `git checkout -- .` / `git restore .` | Discards local modifications |
| `git restore -- <pathspec...>` / `git checkout -- <pathspec...>` | Bulk discards local modifications (multiple paths, directories, or globs) |
| `git stash drop` / `git stash clear` | Permanently deletes stashed work |
| `git rebase` (incl. `-i`) | Rewrites history (often leads to force-push pressure) |
| `git commit --amend` | Rewrites the last commit (dangerous after push) |

## Common Pitfalls

- Don't panic and run commands without understanding state
- Don't use `reset --hard` to "fix" things
- Don't force push to fix local issues
- Do run `git status` and share output first
- Do create a recovery branch (or checkpoint commit) to protect work
- Do check `git reflog` for recovery options
