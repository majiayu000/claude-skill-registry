---
name: sc-managing-worktrees
description: >
  Create, manage, scan, and clean up git worktrees for parallel development.
  Use when working on multiple branches simultaneously, isolating experiments,
  or when user mentions "worktree", "parallel branches", "feature isolation",
  "branch cleanup", or "worktree status".
---

# Managing Git Worktrees

Use this skill to manage worktrees with a standard structure and tracking. Use the `/sc-git-worktree` command to invoke this skill.

## Agent Delegation

This skill delegates to specialized agents via the **Task tool**:

| Operation | Agent | Returns |
|-----------|-------|---------|
| Create | `sc-worktree-create` | JSON: success, path, branch, tracking_row |
| Scan | `sc-worktree-scan` | JSON: success, worktrees list, recommendations |
| Cleanup | `sc-worktree-cleanup` | JSON: success, branch_deleted, tracking_update |
| Abort | `sc-worktree-abort` | JSON: success, worktree_removed, tracking_update |

To invoke an agent, use the Task tool with:
- Prompt file: `.claude/agents/<agent-name>.md`
- Parameters as documented in each agent's Inputs section

## Standards and paths
- Repo root: current directory.
- Default worktree base: `../synaptic-canvas-worktrees`.
- Worktrees live in `<worktree_base>/<branch>`.
- Tracking document (if used): `<worktree_base>/worktree-tracking.md` must be updated on create/scan/cleanup/abandon. Allow a toggle to disable tracking for repos that don’t use it.
- Naming: worktree directory = branch name; branch naming follows repo policy (e.g., master release; develop/DevBranch integration; feature from integration; hotfix from master; release branches as needed).
- Branch protections/hooks: no direct commits to protected branches; ensure hooks/branch protections are respected across worktrees.
- Cleanliness: worktrees must be removed and tracking updated when work is complete or branch is merged.

## Workflows

### Scaffolding (if missing)
- Ensure base path exists: `<worktree_base>`. If missing, create it.
- If tracking is enabled, ensure tracking doc exists with headers.

### Create worktree (and branch)
1) Inputs: `--branch <name>`, `--base <master|develop|...>`, optional `--path`.
2) Ensure scaffolding/tracking doc exists (if enabled); fetch all: `git fetch --all --prune`.
3) Confirm base branch exists and is up to date.
4) Determine path: default `<worktree_base>/<branch>` (or override).
5) Create branch/worktree:
   - If branch does not yet exist: `git worktree add -b <branch> <path> <base>`.
   - If branch exists: `git worktree add <path> <branch>`.
6) In the new worktree, ensure hooks apply and verify status is clean.
7) If tracking enabled, add/refresh entry in tracking doc (branch, path, base, purpose, owner, created date, status).
8) Agent option: delegate to `sc-worktree-create` agent; it returns structured JSON (tracking row, status).

### Scan/verify worktrees
1) List worktrees: `git worktree list --porcelain`.
2) Cross-check tracking doc (if enabled); flag missing/stale entries or extra rows.
3) For each worktree, check status and merge state:
   - `git -C <path> status --short`
   - `git -C <path> fetch`
   - `git branch --remotes --contains <branch>` to see if merged.
4) Identify issues: untracked changes, diverged branches, merged-but-not-cleaned worktrees, missing tracking entries.
5) Update tracking doc with current state and issues (if enabled); propose cleanup where appropriate.
6) Agent option: delegate to `sc-worktree-scan` agent; it returns structured JSON.

### Clean-up worktree (post-merge or finished work)
1) If `git status` is not clean, stop and request explicit approval/coordination.
2) Ensure all work is committed/pushed or explicitly confirmed to discard.
3) Confirm target branch merged or otherwise approved for removal.
4) Remove worktree: `git worktree remove <path>` (use `--force` only with approval).
5) If merged and no unique commits, delete the branch locally (`git branch -d <branch>`) and remotely (`git push origin --delete <branch>`) by default; only skip if the user explicitly opts out. If the remote branch is already absent, continue without error. If not merged, only delete with explicit approval.
6) If tracking enabled, update tracking doc to remove/mark cleaned with merge SHA/date.
7) Agent option: delegate to `sc-worktree-cleanup` agent; it returns structured JSON.

### Abandon worktree (discard work)
1) If `git status` is not clean, stop and request explicit approval/coordination.
2) Confirm user approval to discard local changes and optionally delete the branch.
2) Remove worktree: `git worktree remove <path>` (force only with approval).
3) If instructed, delete the branch locally (`git branch -D <branch>`) and remotely (`git push origin --delete <branch>`).
4) If tracking enabled, update tracking doc to remove the entry and note abandonment.
5) Agent option: delegate to `sc-worktree-abort` agent; it returns structured JSON.

## Safety and reminders
- Never delete branches or force-remove worktrees without explicit approval.
- Never clean/abandon a worktree with uncommitted changes unless explicitly approved.
- Keep tracking doc in sync on every operation when enabled.
- Respect branch protections and hooks; no direct commits to protected branches.
- Use background agents for long scans/cleanups; keep the main context focused on decisions and summaries.
