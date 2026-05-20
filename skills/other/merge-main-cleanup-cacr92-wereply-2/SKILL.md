---
name: merge-main-cleanup
description: This skill should be used when the user requests merging work into main and then deleting all other local and remote branches, keeping only main.
---

# Merge Main Cleanup

## Overview
Perform a full merge into main and then delete all other branches locally and on the default remote. Remove any worktrees tied to deleted branches.

## When to Use
- User says to merge into main and keep only main.
- User wants a one-step cleanup of branches after merge.

## Workflow

### 1) Validate repository state
- Run `git status --porcelain` and stop if there are uncommitted changes.
- Run `git rev-parse --show-toplevel` and work from that root.
- Run `git fetch --all --prune` to sync branch state.

### 2) Determine base branch
- Prefer `main`; if missing, use `master`.
- Command: `git branch --list main master`

### 3) Merge current branch into base
- Get current branch: `git branch --show-current`.
- If already on base, skip merge.
- Otherwise:
  - `git checkout <base>`
  - `git pull --ff-only`
  - `git merge <current-branch>`
  - Resolve conflicts if any, then complete the merge.

### 4) Push base to remote
- Push base: `git push origin <base>`

### 5) Remove worktrees for non-base branches
- List worktrees: `git worktree list`.
- For each worktree whose branch is not `<base>`, remove it:
  - `git worktree remove <path>`

### 6) Delete all non-base branches (local + remote)
- Local branches (force delete, as requested):
  - List: `git branch --format='%(refname:short)'`
  - For each branch not `<base>`, run: `git branch -D <branch>`
- Remote branches (origin):
  - List: `git branch -r --format='%(refname:short)' | rg '^origin/'`
  - For each remote branch not `origin/<base>`, run: `git push origin --delete <branch>`

### 7) Verify only base remains
- `git branch -vv` should show only `<base>`.
- `git branch -r` should show only `origin/<base>`.

## Notes
- This skill is intentionally destructive: it deletes all branches except base.
- If the remote is not named `origin`, replace it accordingly.
- If deletion of worktree files is blocked by policy, report and ask the user to remove them manually.
