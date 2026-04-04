---
name: worktree-parallel
description: Create and manage a git worktree for parallel feature development, then open the new worktree in the editor (code/Cursor) for a second Codex session. Use when the user asks to work on another feature simultaneously, spin up a parallel workspace, or open a new worktree even if they do not mention worktree explicitly.
---

# Worktree Parallel

## Workflow

1. Confirm the repo root (use current working directory unless the user specifies another repo).
2. Determine a feature slug and branch name.
   - Default branch pattern: `feat/<slug>`.
   - If the user already has a branch name, use it.
3. Choose a base directory for linked worktrees.
   - Default for this repo: `../<project_name>-wt` (create it if missing).
4. Create the worktree.
   - New branch: `git worktree add -b feat/<slug> <base>/<slug>`
   - Existing branch: `git worktree add <base>/<slug> <branch>`
5. Open the worktree in the editor.
   - Use `code -n <path>` (Cursor supports the `code` CLI).
   - If `code` is unavailable, ask for the preferred editor command (e.g., `cursor -n`, `code`, or another).
6. Suggest a parallel Codex session in the new worktree.
   - `cd <path> && codex`
7. Confirm with `git worktree list` if needed.

## Safety

- Do not use `--force` unless the user explicitly asks.
- Do not remove existing worktrees unless the user requests cleanup.

## Optional Cleanup (only if asked)

- `git worktree remove <path>`
- `git branch -d <branch>`
