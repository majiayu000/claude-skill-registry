---
name: git-workflows
description: Advanced git operations - branching strategies, interactive rebase, conflict resolution, stash management, and disaster recovery. Auto-triggers for complex git tasks.
---

# Git Workflows Skill

## Branching Strategies

### GitHub Flow (Recommended for Most Projects)

```
main ──────●────────●────────●──────
            \      /          \    /
feature-1    ●──●──           ●──●
                           feature-2
```

1. Branch from `main`
2. Make changes, commit
3. Open PR, get review
4. Merge to `main`, delete branch

### Branch Naming

```bash
# Pattern: type/description
feature/oauth-login
fix/null-pointer-user-profile
refactor/extract-auth-module
docs/api-endpoints
chore/upgrade-dependencies
```

## Interactive Rebase

### Clean Up Before PR

```bash
# Rebase last 4 commits
git rebase -i HEAD~4

# In editor:
pick abc1234 feat: add user model
squash def5678 fix typo in user model      # Combine with previous
pick ghi9012 feat: add user API endpoint
fixup jkl3456 cleanup                       # Combine, discard message
```

| Command  | Effect                                |
| -------- | ------------------------------------- |
| `pick`   | Keep commit as-is                     |
| `squash` | Merge into previous, combine messages |
| `fixup`  | Merge into previous, discard message  |
| `reword` | Keep commit, edit message             |
| `drop`   | Delete commit entirely                |
| `edit`   | Pause to amend commit                 |

### Rebase onto Updated Main

```bash
# Update main
git fetch origin main

# Rebase feature branch onto latest main
git rebase origin/main

# If conflicts: resolve, then continue
git add .
git rebase --continue

# Abort if things go wrong
git rebase --abort
```

## Conflict Resolution

### Step-by-Step

```bash
# 1. See what conflicts exist
git status

# 2. Open conflicted file - markers look like:
<<<<<<< HEAD
current_change()
=======
incoming_change()
>>>>>>> feature-branch

# 3. Resolve by keeping correct code (remove markers)
resolved_change()

# 4. Mark as resolved
git add <resolved-file>

# 5. Continue the operation
git rebase --continue  # or git merge --continue
```

### Conflict Prevention

- Rebase feature branches onto main frequently
- Keep PRs small and focused
- Communicate about shared files
- Use `.gitattributes` for merge strategies on generated files

```
# .gitattributes - always use ours for lock files
uv.lock merge=ours
package-lock.json merge=ours
```

## Stash Management

```bash
# Stash current changes with description
git stash push -m "WIP: auth refactor"

# List stashes
git stash list

# Apply most recent stash (keep in stash list)
git stash apply

# Apply and remove from stash list
git stash pop

# Apply specific stash
git stash apply stash@{2}

# Stash specific files
git stash push -m "partial work" src/auth.py src/middleware.py

# Stash including untracked files
git stash push -u -m "including new files"

# Drop a stash
git stash drop stash@{0}

# Clear all stashes
git stash clear
```

## Cherry-Pick

```bash
# Apply a specific commit to current branch
git cherry-pick abc1234

# Cherry-pick without committing (stage only)
git cherry-pick --no-commit abc1234

# Cherry-pick a range
git cherry-pick abc1234..def5678

# If conflicts during cherry-pick
git cherry-pick --continue  # after resolving
git cherry-pick --abort     # to cancel
```

## Disaster Recovery

### Undo Last Commit (Keep Changes)

```bash
git reset --soft HEAD~1
```

### Recover Deleted Branch

```bash
# Find the commit hash from reflog
git reflog | grep "branch-name"

# Recreate the branch
git branch recovered-branch abc1234
```

### Recover Lost Commits

```bash
# View full history including orphaned commits
git reflog

# Find the commit you need and checkout/cherry-pick
git cherry-pick abc1234
```

### Undo a Bad Merge

```bash
# Revert a merge commit (keeps history clean)
git revert -m 1 <merge-commit-hash>
```

### Find When a Bug Was Introduced

```bash
# Start bisect
git bisect start

# Mark current as bad
git bisect bad

# Mark a known good commit
git bisect good v1.0.0

# Git checks out a middle commit - test it, then:
git bisect good  # or git bisect bad

# Repeat until git finds the culprit
# When done:
git bisect reset
```

### Automated Bisect

```bash
# Run a test script at each step
git bisect start HEAD v1.0.0
git bisect run pytest tests/test_auth.py
```

## Worktrees (Parallel Branches)

```bash
# Work on two branches simultaneously
git worktree add ../my-project-hotfix hotfix/urgent-fix

# List worktrees
git worktree list

# Remove when done
git worktree remove ../my-project-hotfix
```

## Useful Aliases

```bash
# Add to ~/.gitconfig
[alias]
    lg = log --oneline --graph --all --decorate
    st = status -sb
    unstage = reset HEAD --
    last = log -1 HEAD --stat
    branches = branch -a --sort=-committerdate
    amend = commit --amend --no-edit
```

## Activation Triggers

This skill auto-activates when prompts contain:

- "rebase", "cherry-pick", "stash"
- "merge conflict", "resolve conflict"
- "git bisect", "git reflog", "recover"
- "branch strategy", "branching"
- "worktree", "git reset"

## Integration

- **conventional-commits** skill: Commit message formatting
- **/merge-resolve** command: Conflict resolution
- **/ship** command: Push and PR workflow
