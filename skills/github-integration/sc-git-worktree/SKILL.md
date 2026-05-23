---
name: sc-managing-worktrees
description: >
  Create, manage, scan, update, and clean up git worktrees for parallel development with protected branch safeguards.
  Use when working on multiple branches simultaneously, isolating experiments, updating protected branches (main/develop),
  or when user mentions "worktree", "parallel branches", "feature isolation", "branch cleanup", "worktree status", or "update main/develop".
version: 0.8.0
entry_point: /sc-git-worktree
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
| Update | `sc-worktree-update` | JSON: success, commits_pulled, conflicts (if any) |

To invoke an agent, use the Task tool with:
- Prompt file: `.claude/agents/<agent-name>.md`
- Parameters as documented in each agent's Inputs section

## Standards and paths
- Repo root: current directory.
- Default worktree base: `../{{REPO_NAME}}-worktrees`.
- Worktrees live in `<worktree_base>/<branch>`.
- Tracking document (if used): `<worktree_base>/worktree-tracking.md` must be updated on create/scan/cleanup/abandon. Allow a toggle to disable tracking for repos that don't use it.
- Naming: worktree directory = branch name; branch naming follows repo policy (e.g., master release; develop/DevBranch integration; feature from integration; hotfix from master; release branches as needed).
- Branch protections/hooks: no direct commits to protected branches; ensure hooks/branch protections are respected across worktrees.
- Cleanliness: worktrees must be removed and tracking updated when work is complete or branch is merged.

## Protected Branch Configuration

Protected branches (main, develop, master, etc.) require special handling to prevent accidental deletion:

```yaml
# Configuration (typically in repo .claude/config or passed to agents)
git_flow:
  enabled: true  # boolean: whether git-flow workflow is used
  main_branch: "main"  # or "master" - the primary production branch
  develop_branch: "develop"  # only if git_flow.enabled = true

protected_branches:
  - "main"
  - "develop"
  - "master"
  # Can include additional patterns: "release/*", "hotfix/*"
```

**Protected Branch Rules:**
- If `git_flow.enabled: false` → protect only `main_branch`
- If `git_flow.enabled: true` → protect `main_branch` + `develop_branch`
- Additional branches can be added to `protected_branches` array
- **Cleanup/abort agents NEVER delete protected branches** (local or remote)
- Protected branches can only be removed from worktrees, never deleted
- Use `--update` to safely pull changes for protected branches in worktrees

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
1) **Check if branch is protected**: If branch is in protected_branches list, ONLY remove worktree, NEVER delete the branch.
2) If `git status` is not clean, stop and request explicit approval/coordination.
3) Ensure all work is committed/pushed or explicitly confirmed to discard.
4) Confirm target branch merged or otherwise approved for removal.
5) Remove worktree: `git worktree remove <path>` (use `--force` only with approval).
6) For **non-protected branches**: If merged and no unique commits, delete the branch locally (`git branch -d <branch>`) and remotely (`git push origin --delete <branch>`) by default; only skip if the user explicitly opts out. If the remote branch is already absent, continue without error. If not merged, only delete with explicit approval.
7) For **protected branches**: Only remove worktree, preserve branch locally and remotely. Update tracking to note "worktree removed, branch preserved (protected)".
8) If tracking enabled, update tracking doc to remove/mark cleaned with merge SHA/date.
9) Agent option: delegate to `sc-worktree-cleanup` agent; it returns structured JSON.

### Abandon worktree (discard work)
1) **Check if branch is protected**: If branch is in protected_branches list, ONLY remove worktree, NEVER delete the branch.
2) If `git status` is not clean, stop and request explicit approval/coordination.
3) Confirm user approval to discard local changes and optionally delete the branch.
4) Remove worktree: `git worktree remove <path>` (force only with approval).
5) For **non-protected branches**: If instructed, delete the branch locally (`git branch -D <branch>`) and remotely (`git push origin --delete <branch>`).
6) For **protected branches**: Only remove worktree, preserve branch locally and remotely. Require confirmation: "Branch is protected. Remove worktree but preserve branch?"
7) If tracking enabled, update tracking doc to remove the entry and note abandonment.
8) Agent option: delegate to `sc-worktree-abort` agent; it returns structured JSON.

### Update protected branch (pull latest changes)
1) **Verify branch is protected**: Only operates on branches in protected_branches list. If no branch is specified, update all protected branches that have worktrees.
2) Check if worktree exists at expected path; error if missing.
3) If `git status` is not clean, stop and report dirty state.
4) Fetch and pull: `git fetch origin <branch>` then `git pull origin <branch>`.
5) **If merge conflicts occur**:
   - Collect conflicted files: `git diff --name-only --diff-filter=U`
   - Return control to main agent with conflict details
   - Main agent coordinates with user to resolve conflicts
   - After resolution, user commits and continues
6) **If clean pull**: Update tracking with last_checked timestamp and commits pulled count.
7) Agent option: delegate to `sc-worktree-update` agent; it returns structured JSON with success or conflict details.

## Safety and reminders
- **NEVER delete protected branches** (main, develop, master) under any circumstances.
- Protected branches can only be removed from worktrees; the branch itself must always be preserved.
- Never delete branches or force-remove worktrees without explicit approval.
- Never clean/abandon a worktree with uncommitted changes unless explicitly approved.
- Keep tracking doc in sync on every operation when enabled.
- Respect branch protections and hooks; no direct commits to protected branches.
- Use background agents for long scans/cleanups; keep the main context focused on decisions and summaries.
- When updating protected branches in worktrees, handle merge conflicts by returning control to main agent for user coordination.
