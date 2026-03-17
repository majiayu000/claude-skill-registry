---
name: git-worktrees
description: Create and manage git worktrees (parallel branches) without stash/switching.
compatibility: opencode
---

## Reference

- `docs/dev/worktrees.md`

## Core commands

From the base repo checkout:

- List worktrees: `git worktree list`
- Create branch + worktree: `git worktree add -b feat/my-change ../drasil-wt/my-change origin/main`
- Add worktree for an existing branch: `git worktree add ../drasil-wt/my-change feat/my-change`
- Remove a worktree: `git worktree remove ../drasil-wt/my-change`
- Prune stale metadata: `git worktree prune`

For layout/deps/.env and integration test DB gotchas, see `docs/dev/worktrees.md`.

## Safety

- Do not remove a worktree if it has uncommitted changes.
- Prefer one issue/feature per worktree.
