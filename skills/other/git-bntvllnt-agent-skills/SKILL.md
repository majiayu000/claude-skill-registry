---
name: git
description: |
  Unified git workflow for branch-first development: status/diff review, security-first commits,
  worktrees, and PR creation/review via gh.
  Auto-activates on: "commit", "push", "branch", "worktree", "pr", "pull request", "merge", "rebase", "git".
license: MIT
compatibility: Requires git. PR workflows may use GitHub + gh CLI (optional). Worktree workflows create local directories under WORKTREES_DIR.
metadata:
  version: "1.0"
---

# Git

Clear, repeatable git workflow with a bias toward safety.

## Router

Use the smallest workflow that matches the user intent.

| User says | Load reference | Do |
|---|---|---|
| status / what changed (no "worktree" prefix) | `references/read-only.md` | read-only inspection |
| help / usage / man | `references/cli-help.md` | show CLI help safely |
| commit / stage | `references/commit-workflow.md` | stage + commit safely |
| branch / switch | `references/branch-workflow.md` | branch operations |
| worktree create/remove/list | `references/worktree-workflow.md` | worktree operations |
| worktree cleanup / normalize / consolidate | `references/worktree-maintenance.md` | auto-clean + consolidate worktrees |
| worktree summary / worktree status / show worktrees | `references/worktree-summary.md` | proactive analysis: PR status, change classification, safe-to-delete verdicts |
| tag / version | `references/tag-workflow.md` | create/list/inspect tags |
| pr / pull request | `references/pr-workflow.md` | create/update PR via gh |
| pr review / fix pr comments / threads | `references/pr-review-workflow.md` | review + respond + fix |
| merge / rebase / reset / revert | `references/advanced-workflows.md` | advanced/recovery (confirm first) |

## Config (Edit Here)

Worktree working directories (the folders you `cd` into) live outside `.git/`.

Set this once and use it everywhere:

```text
WORKTREES_DIR=./.worktrees
WORKTREE_PATH=$WORKTREES_DIR/<topic>
```

If you want a different location (e.g. `../.worktrees` or `~/worktrees/<repo>`), update `WORKTREES_DIR` above and follow the same shape in `references/worktree-workflow.md`.

## Resilience Rules (Worktrees)

- If multiple worktree root folders are detected (example: both `./.worktrees/` and `../repo-feature-x/` exist), do not delete anything by default.
- Prefer consolidating into `WORKTREES_DIR` using `git worktree move` (when possible) or a remove+re-add plan.
- If stale metadata exists, propose a cleanup plan: `git worktree prune` + remove/quarantine orphan directories (with confirmation).

## Global Safety Rules (Never Violate)

- Never force push to main/master.
- Never commit secrets (env files, keys, credentials).
- Never rewrite history that is already pushed unless explicitly requested.
- Always show what will change before an irreversible action.

## Confirmation Policy

Read-only commands are always OK.

Everything that changes state/history/remote requires explicit user confirmation:
- `git add`, `git commit`, `git push`
- `git merge`, `git rebase`, `git reset`, `git revert`
- `git worktree add`, `git worktree remove`
- `git tag` (create/delete)
- `git branch -d/-D`

## Quick Start

```bash
# Read-only
git status
git diff

# Commit
git diff --cached
git commit -m "feat(scope): why"

# Worktrees
git worktree list
```
