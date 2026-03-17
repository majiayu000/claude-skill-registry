---
name: git:rebase
description: Rebase branches onto upstream main with automatic base detection
---

# Git Rebase

Rebase the current branch onto the upstream main branch. Uses a pattern that auto-detects the correct upstream remote and main branch.

## When to Use

- Before creating a PR (ensure clean history)
- After upstream main has new commits
- During TDD iterations when CI requires a rebase
- When PR has merge conflicts

## Quick Rebase (gfur alias)

The `gfur` alias automatically finds the upstream remote and main branch:

```bash
# Define gfur (add to ~/.bashrc or ~/.zshrc)
alias gfur='git fetch upstream && git rebase upstream/$(git symbolic-ref refs/remotes/upstream/HEAD | sed "s@^refs/remotes/upstream/@@")'
```

Use it:

```bash
gfur
```

If upstream/HEAD is not set:

```bash
git remote set-head upstream -a
```

## Manual Rebase

```bash
git fetch upstream main
```

```bash
git rebase upstream/main
```

## Rebase Conflicts

If conflicts occur during rebase:

```bash
# Check which files conflict
git status
```

Fix the conflicts, then:

```bash
git add <fixed-files>
```

```bash
git rebase --continue
```

To abort:

```bash
git rebase --abort
```

## Sign All Commits After Rebase

After rebasing, ensure all commits are signed (required by Kagenti):

```bash
git rebase --signoff HEAD~$(git rev-list --count upstream/main..HEAD)
```

## Related Skills

- `git:commit` - Commit format conventions
- `git:worktree` - Parallel development with worktrees
- `tdd:ci` - TDD workflow that needs rebase before push
- `repo:commit` - Repository-specific commit format
