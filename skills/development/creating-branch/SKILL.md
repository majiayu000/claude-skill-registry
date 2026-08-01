---
name: creating-branch
description: 'Standard workflow for all branch operations (''create branch'', ''new
  branch'', ''start branch for''): replaces bash-based git checkout/branch workflows—determines
  base branch, generates convention-based na'
---

---
name: creating-branch
description: Standard workflow for all branch operations ('create branch', 'new branch', 'start branch for'): replaces bash-based git checkout/branch workflows—determines base branch, generates convention-based names, preserves uncommitted changes, enforces mainline protection. Canonical branch creation implementation for git-workflows.
---

# Skill: Creating a Branch

## When to Use This Skill

Use this skill for branch creation: "create a branch", "new branch", "start a branch for X", "create branch called X".

Use other tools for: switching branches (`git checkout`), listing branches (`git branch`).

## Workflow Description

Creates feature branches from current state, preserving uncommitted changes. Generates conventional names, validates uniqueness.

Extract from user request: purpose/description, explicit name (if provided), base branch (if specified, else mainline)

---

## Phase 1: Current State Validation

**Objective**: Check current branch state.

**Steps**:

1. Get current branch:

   ```bash
   git branch --show-current
   ```

2. Check working tree status:

   ```bash
   git status --porcelain
   ```

3. Note state:
   - current_branch: Captured branch name
   - has_uncommitted: true if status output not empty, false otherwise

Continue to Phase 2.

---

## Phase 2: Determine Base Branch

**Objective**: Identify which branch to create from.

**Step 1: Check user request for base branch**

Analyze user's request for base branch specification:

- Look for phrases like: "from <branch>", "based on <branch>", "branch off <branch>"
- Common branch names: develop, staging, main, master, release, etc.

IF base branch specified in user request:
  Use specified branch as base
  Continue to Phase 3

IF no base branch mentioned:
  Run `../../scripts/get-mainline-branch.sh` to detect mainline branch
  Parse JSON response and extract `mainline_branch` field
  Use detected mainline as base
  Continue to Phase 3

**Validation Gate: Base Branch Determined**

IF base branch successfully determined:
  PROCEED to Phase 3

IF cannot determine base branch:
  STOP immediately
  EXPLAIN: "Cannot determine which branch to create from"
  ASK: "Please specify base branch (e.g., 'from develop' or 'based on main')"
  WAIT for user input

Phase 2 complete. Continue to Phase 3.

---

## Phase 3: Branch Naming

**Objective**: Generate or use branch name following conventions.

**Steps**:

1. Check if user provided explicit branch name:
   - Look for phrases: "called <name>", "named <name>", "create branch <name>"
   - IF explicit name found: Use it, skip to uniqueness check (Step 5)

2. IF no explicit name: Run `../../scripts/detect-conventions.sh` to detect commit conventions
   Parse JSON response and extract `uses_conventional_commits` flag

3. Extract description from user request:
   - Example: "create branch for adding metrics" → "adding metrics"
   - Example: "new branch to fix auth bug" → "fix auth bug"

4. Generate branch name:
   - Transform to kebab-case (lowercase, hyphens, alphanumerics only)
   - IF uses_conventional_commits = true: Add type prefix based on keywords
     - "fix", "bug", "error" → fix/
     - "add", "new", "feature" → feat/
     - "docs", "documentation" → docs/
     - "test", "testing" → test/
     - "refactor", "cleanup" → refactor/
     - "perf", "performance" → perf/
     - "ci", "build", "deploy" → ci/
     - "chore", "maintenance" → chore/
   - IF standard format: Use description without prefix
   - Truncate to 47 chars if > 50, append "..."

5. Check uniqueness:

   ```bash
   git rev-parse --verify <branch-name> 2>/dev/null
   ```

   - Exit 0: Branch exists
   - Exit 128: Branch does not exist (good)

**Validation Gate: Branch Availability**

IF branch does not exist:
  Continue to Phase 4

IF branch exists:
  EXPLAIN: "Branch '<branch-name>' already exists locally"
  PROPOSE: Generate alternative with numeric suffix (e.g., feat/auth-2)
  Generate alternative:
    - Append "-2", check again
    - If exists, increment: "-3", "-4", etc.
    - Stop at "-9", ask user for custom name
  Use alternative name
  Continue to Phase 4

Phase 3 complete. Continue to Phase 4.

---

## Phase 4: Branch Creation

**Objective**: Create and checkout new feature branch.

**Plan Mode**: Auto-enforced read-only if active

**Steps**:

1. Create and checkout branch:

   ```bash
   git checkout -b <branch-name>
   ```

   This creates the branch from current HEAD and checks it out.
   Uncommitted changes automatically carry forward.

**Error Handling**: IF failure:

- Explain error:
  - "fatal: A branch named '...' already exists": Branch exists (shouldn't happen after uniqueness check)
  - "error: pathspec '...' did not match": Invalid branch name characters
  - Other: Permission issues or repository problems
- Propose solution and wait for retry approval

Continue to Phase 5.

---

## Phase 5: Verification

**Objective**: Confirm new branch was created and checked out.

**Steps**:

1. Verify current branch:

   ```bash
   git branch --show-current
   ```

2. Compare to expected branch name from Phase 3

3. Report using template:

   ```markdown
   ✓ Branch Created Successfully

   **Branch:** <branch_name> \
   **Created from:** <base_branch> \
   **Uncommitted changes:** <Preserved|None>
   ```

**Validation Gate**: IF current branch does not match expected:

- STOP: "Branch creation verification failed"
- SHOW: Expected vs actual branch
- PROPOSE: "Manually checkout branch with: `git checkout <expected-branch>`"

Workflow complete.
