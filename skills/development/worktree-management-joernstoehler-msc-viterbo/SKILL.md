---
name: worktree-management
description: Manage git worktrees for this repo. Use when creating/removing/inspecting worktrees or when isolating work into a new path/branch via scripts/worktree-*.sh.
---

# Worktree Management

## Use the repo scripts (preferred)

- Create: `scripts/worktree-new.sh [--force] [--no-hydrate] <path> <branch>`
  - Creates worktree and branch (from `main` if missing).
  - Use `--no-hydrate` to skip toolchain hydration.
- Remove: `scripts/worktree-remove.sh <path> [--force]`
  - Removes the worktree (branch is kept).
- List: `git worktree list`

## Notes

- Worktrees live under `/workspaces/worktrees/`.
- Shared build cache lives under `/workspaces/worktrees/shared/` (notably Rust `target/`).
