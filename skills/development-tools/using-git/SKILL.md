---
name: using-git
description: ALWAYS load this skill when the user mentions ANY of these git topics — squash, rebase, cherry-pick, merge conflicts, conflict resolution, reflog, recovering lost commits, resetting commits, pre-commit hooks, or fixing broken git state. This skill contains safe, non-interactive git approaches that must be preferred over default git commands. Trigger for squashing commits, rebasing onto main/dev/master, cherry-picking from another branch, resolving rebase conflicts, recovering commits after reset, reflog to find lost work, accidentally committed to wrong branch, pre-commit hook modified files, non-interactive squash before PR, cleaning up commit history, consolidating commits, force push after rebase, or bad reset recovery. Load this skill for ANY git workflow involving history rewriting, commit manipulation, or branch rebasing — even if the request seems straightforward.
---

# Git Workflow

Safe, non-interactive approaches for squashing commits and rebasing feature branches.

> **Tip**: If jj is available (`jj root` succeeds), prefer using-jj -- it's simpler and has automatic safety via oplog.

## Squash N Commits

```bash
git reset --soft HEAD~3
git commit -m "Your consolidated message"
```

That's it. The `--soft` flag keeps your changes staged and ready to commit.

## Rebase Feature Branch

Update dev first, then rebase:

```bash
git fetch origin dev && git checkout dev && git pull
git checkout my-feature
git rebase --committer-date-is-author-date dev
git push -f origin my-feature
```

The `--committer-date-is-author-date` flag puts your feature commits on top chronologically.

## Key Safety Rules

- **Never rebase shared branches** — only rebase local feature branches
- **Check `git status` first** — ensure no uncommitted changes
- **Create a backup branch**: `git branch backup-$(date +%s)`
- **Review changes** before committing: `git diff --cached`

## Pre-Commit Hook Changes

If hooks modify files during commit, stage and amend:

```bash
git add .
git commit --amend --no-edit
```

## When Things Go Wrong

```bash
git rebase --abort              # Stop rebase, go back
git reflog                      # See recent commits
git reset --hard <commit-hash>  # Recovery
```

See REFERENCE.md for detailed workflows and troubleshooting.
