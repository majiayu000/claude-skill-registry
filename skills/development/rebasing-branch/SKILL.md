---
name: rebasing-branch
description: 'Standard workflow for all rebase operations (''rebase branch'', ''rebase
  on main'', ''rebase onto''): replaces bash-based git rebase workflows with Git Safety
  Protocol—syncs base branch first, prevents main'
---

---
name: rebasing-branch
description: Standard workflow for all rebase operations ('rebase branch', 'rebase on main', 'rebase onto'): replaces bash-based git rebase workflows with Git Safety Protocol—syncs base branch first, prevents mainline rebase errors, preserves working state, provides conflict resolution guidance. Canonical rebase implementation for git-workflows.
---

# Skill: Rebasing a Branch

## When to Use This Skill

Use this skill for rebase requests: "rebase my branch", "rebase on main", "rebase onto X", "update my branch with main".

Use other skills for: syncing (syncing-branch for fetch+merge), viewing status (git status directly).

## Workflow Description

Rebases feature branch onto updated mainline, rewriting commit history. Handles state preservation, conflict resolution, optional author date reset.

Extract from user request: target branch (if specified, else mainline), author date preference ("keep dates"/"preserve dates" → preserve, default reset)

---

## Phase 1: Pre-flight Checks

**Objective**: Verify environment is ready for rebase operation.

**Step 1: Get current branch**

Get current branch:

```bash
git branch --show-current
```

Capture: current_branch

**Step 2: Check if on mainline**

Run `../../scripts/get-mainline-branch.sh` with the current branch as parameter

Parse JSON response:

- Extract `mainline_branch` field
- Extract `is_mainline` flag (true if current branch matches mainline)
- Store both for later phases

**Step 3: Check working tree status**

Check status:

```bash
git status --porcelain
```

Capture: working tree clean status (empty = clean)

**Validation Gate: Safe to Rebase**

IF is_mainline = true:
  STOP immediately
  EXPLAIN: "Cannot rebase the mainline branch. Mainline should never be rebased as it's the stable reference point for all feature branches."
  INFORM: "Rebasing mainline would rewrite its history and break all feature branches based on it."
  PROPOSE: "Create a feature branch first if you need to test changes"
  EXIT workflow

IF is_mainline = false AND working tree not clean (status output not empty):
  INFORM: "Uncommitted changes detected - creating commit first"
  INVOKE: creating-commit skill
  WAIT for creating-commit to complete

  IF creating-commit succeeded:
    VERIFY: Working tree is now clean
    PROCEED to Phase 2

  IF creating-commit failed:
    STOP immediately
    EXPLAIN: "Cannot rebase without committing changes"
    EXIT workflow

IF is_mainline = false AND working tree clean:
  PROCEED to Phase 2

**Save State**: Store saved_branch = current_branch (preserve through all phases)

Phase 1 complete. Continue to Phase 2.

---

## Phase 2: Determine Rebase Base

**Objective**: Identify which branch to rebase onto.

**Step 1: Check user request for rebase target**

Analyze user's request for target branch specification:

- Look for phrases like: "rebase onto <branch>", "rebase on <branch>", "rebase against <branch>"
- Common branch names: main, master, develop, staging, release, etc.

IF target branch specified in user request:
  Use specified branch as rebase base

IF no target branch mentioned:
  Use mainline_branch from Phase 1 as rebase base

Store rebase_base for later phases.

Phase 2 complete. Continue to Phase 3.

---

## Phase 3: Checkout Base Branch

**Objective**: Switch to base branch for syncing.

**Step 1: Checkout base branch**

Checkout rebase base:

```bash
git checkout <rebase_base from Phase 2>
```

**Error Handling**

IF checkout succeeds:
  PROCEED to Phase 4

IF checkout fails:
  STOP immediately

  Analyze and explain error:

- "error: pathspec '...' did not match": Base branch doesn't exist locally
- "error: Your local changes": Working tree not clean (shouldn't happen after Phase 1)
- Other: Permission issues

  Propose solution:

- Doesn't exist: "Verify branch name with `git branch --all` or create it"
- Permission: "Check repository access and file permissions"

  WAIT for user decision

Phase 3 complete. Continue to Phase 4.

---

## Phase 4: Sync Base Branch

**Objective**: Ensure base branch is up-to-date with remote.

**Plan Mode Handling**

Plan mode is automatically enforced by the system. IF currently in plan mode:

- Sync operation will be read-only
- Skills invoked will operate in read-only mode
- Continue through workflow for demonstration purposes

**Step 1: Invoke syncing-branch skill**

INVOKE: syncing-branch skill
WAIT for skill completion

**Validation Gate: Sync Success**

IF syncing-branch skill succeeded:
  INFORM: "Base branch synced successfully with remote"
  PROCEED to Phase 5

IF syncing-branch skill failed:
  STOP immediately
  EXPLAIN: "Failed to sync base branch with remote"
  SHOW: Error reported by syncing-branch skill
  PROPOSE solution:
    - "Check network connectivity"
    - "Review remote branch status"
    - "Retry sync operation"
  WAIT for user decision

Phase 4 complete. Continue to Phase 5.

---

## Phase 5: Return to Feature Branch

**Objective**: Switch back to feature branch for rebase.

**CRITICAL: Use Saved State**

Retrieve saved_branch from Phase 1 (NOT current branch - we're on base branch now)

**Step 1: Checkout feature branch**

Checkout saved branch:

```bash
git checkout <saved_branch from Phase 1>
```

**Error Handling**

IF checkout succeeds:
  PROCEED to Phase 6

IF checkout fails:
  STOP immediately (CRITICAL FAILURE)

  EXPLAIN: "Cannot return to feature branch - workflow interrupted mid-operation"
  INFORM: "You are currently on base branch: <rebase_base from Phase 2>"
  INFORM: "Your feature branch: <saved_branch from Phase 1>"
  PROPOSE: "Manually checkout your feature branch with: `git checkout <saved_branch>`"

  WORKFLOW FAILED - Manual intervention required

Phase 5 complete. Continue to Phase 6.

---

## Phase 6: Rebase Execution

**Objective**: Perform the actual rebase operation.

**Plan Mode**: Auto-enforced read-only if active

**Steps**:

1. Execute: `git rebase <rebase-base>` (from Phase 2)
2. Check exit code

**Validation Gate**:

- IF success (exit 0): Continue to Phase 7
- IF conflicts: PAUSE workflow (normal, not failure)
  - Guide: Edit files, remove markers, `git add`, `git rebase --continue` or `--abort`
  - Wait for user resolution
- IF other error: Explain and propose solution

**Note**: Conflicts are normal, not failures. Workflow PAUSED ≠ FAILED.

Continue to Phase 7.

---

## Phase 7: Reset Author Dates (Conditional)

**Objective**: Update author dates to current time.

**Skip**: IF user requested preserving dates

**Plan Mode**: Auto-enforced read-only if active

**Steps**:

1. Find fork point: `git merge-base --fork-point <rebase-base>` (from Phase 2)
2. Reset dates: `git rebase <fork-point> --reset-author-date`
3. Check exit code

**Validation Gate**: IF reset fails:

- Warn: Rebase succeeded but date reset failed
- Ask to continue without reset or abort

Continue to Phase 8.

---

## Phase 8: Verification

**Objective**: Confirm rebase completed successfully.

**Steps**:

1. Verify current branch:

   ```bash
   git branch --show-current
   ```

2. Compare to saved_branch from Phase 1

3. Check status:

   ```bash
   git status --porcelain
   ```

   Verify clean (empty output)

4. Get recent commits:

   ```bash
   git log --oneline -5
   ```

5. Report using template:

   ```markdown
   ✓ Branch Rebased Successfully

   **Branch:** <saved_branch> \
   **Rebased onto:** <rebase_base> \
   **Author dates:** <Reset|Preserved> \
   **Working tree:** <Clean|Dirty>

   **⚠ Important:** Force push required

   Run: `git push --force-with-lease origin <saved_branch>`
   ```

**Validation Gate**: IF current branch ≠ saved_branch:

- STOP: "Branch state inconsistent after rebase"
- SHOW: Expected (<saved_branch>) vs Actual
- PROPOSE: "Manually checkout with: `git checkout <saved_branch>`"

Workflow complete.
