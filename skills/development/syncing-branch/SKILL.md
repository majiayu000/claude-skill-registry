---
name: syncing-branch
description: 'Standard workflow for all sync operations (''sync branch'', ''pull latest'',
  ''get latest changes'', ''sync with upstream''): replaces bash-based git fetch/pull/merge
  workflows—detects fork vs origin, fetches'
---

---
name: syncing-branch
description: Standard workflow for all sync operations ('sync branch', 'pull latest', 'get latest changes', 'sync with upstream'): replaces bash-based git fetch/pull/merge workflows—detects fork vs origin, fetches from correct remotes, safely merges with fast-forward checks. Canonical branch synchronization implementation for git-workflows.
---

# Skill: Syncing a Branch

## When to Use This Skill

Use this skill for sync requests: "sync my branch", "pull latest", "sync with remote", "update my branch", "get latest from origin/upstream".

Use other skills for: rebasing (rebasing-branch), creating PRs (creating-pull-request), viewing remotes (git commands).

## Workflow Description

Updates branch with remote changes, auto-detecting fork vs origin scenarios.

Extract from user request: target branch (if specified, else current)

---

## Phase 1: Branch Identification and Checkout

**Objective**: Determine which branch to sync and switch to it if needed.

**Steps**:

1. **Determine target branch** from user request:
   - Check for specific branch (e.g., "sync main", "sync the develop branch")
   - IF branch specified: use specified branch
   - IF not specified: get current branch to use as default

2. **Checkout target branch** if specified and different from current:

   ```bash
   git checkout <target-branch>
   ```

**Validation Gate**: IF checkout fails:

- Analyze error:
  - "error: pathspec '...' did not match": Branch doesn't exist
  - "error: Your local changes": Dirty working tree (will be caught by Phase 2)
  - Other: Permission issues
- Explain error
- Propose solution:
  - Doesn't exist: "Create branch first or verify name"
  - Permission: "Check repository access"
- Wait for user to resolve

Continue to Phase 2.

---

## Phase 2: Execute Sync (Optimized)

**Objective**: Perform fork-aware branch synchronization in a single atomic operation.

**Plan Mode**: Auto-enforced read-only if active

**Steps**:

1. Run `../../scripts/sync-branch.sh` (optionally pass target-branch parameter if user specified a branch in Phase 1, otherwise omit to sync current branch)

2. **Parse the JSON response and handle results**:

**IF `success: false`**:

Handle error based on `error_type`:

- **`not_git_repo`**:
  - STOP: "Not in a git repository"
  - Display: `message` and `suggested_action` from response
  - EXIT workflow

- **`branch_not_found`**:
  - STOP: "Branch not found"
  - Display: `message` and `suggested_action` from response
  - Explain: The branch may not exist locally
  - EXIT workflow

- **`uncommitted_changes`**:
  - Display: `message` from response
  - List files from `uncommitted_files` array
  - INFORM: "Uncommitted changes detected - creating commit first"
  - INVOKE: creating-commit skill
  - WAIT for creating-commit to complete

  IF creating-commit succeeded:
    RE-RUN Phase 2 (sync again after commit)
    Continue to Phase 3

  IF creating-commit failed:
    STOP immediately
    EXPLAIN: "Cannot sync without committing changes"
    EXIT workflow

- **`sync_conflict`**:
  - STOP: "Conflict encountered during sync"
  - Display: `message` and `suggested_action` from response
  - EXPLAIN: "Conflicts must be resolved manually"
  - EXIT workflow

- **`branch_diverged`**:
  - STOP: "Local branch has diverged from remote"
  - Display: `message` from response
  - EXPLAIN: "Cannot fast-forward merge - branch histories have diverged"
  - PROPOSE: "Use rebase to reconcile changes (rebasing-branch skill)"
  - EXIT workflow

- **`repo_type_detection_failed`**:
  - STOP: "Could not detect repository type"
  - Display: `message` and `suggested_action` from response
  - EXIT workflow

- **Other errors**:
  - STOP: Display error details
  - EXIT workflow

**IF `success: true`**:

Extract sync results:

```json
{
  "success": true,
  "branch": "main",
  "is_fork": true,
  "operations_performed": [
    "fetched_all",
    "rebased_on_upstream",
    "pushed_to_origin"
  ],
  "commits_pulled": 3,
  "status": "up_to_date"
}
```

Continue to Phase 3.

---

## Phase 3: Report Results

**Objective**: Confirm sync completed successfully with standardized output.

**Steps**:

1. **Format status message** based on sync results:
   - Use `branch`, `commits_pulled`, and `status` from Phase 2 response
   - Determine repository type from `is_fork` flag
   - List operations from `operations_performed` array

2. **Report using standardized template**:

   ```markdown
   ✓ Branch Synced Successfully

   **Branch:** <branch> \
   **Repository Type:** <Fork|Origin-only> \
   **Commits Pulled:** <commits_pulled> \
   **Status:** <status description> \
   **Operations:** <operations_performed as list>
   ```

   Status descriptions:
   - `up_to_date`: "Branch is in sync with remote"
   - `no_upstream`: "No upstream tracking branch configured"
   - `upstream_missing_branch`: "Upstream doesn't have this branch"
   - `push_failed`: "Rebased on upstream but push to origin failed"
   - `sync_conflict`: "Encountered conflicts during sync"

Workflow complete.
