---
name: creating-pull-request
description: 'Standard workflow for all PR operations (''create PR'', ''open PR'',
  ''pull request'', ''commit and PR''): replaces bash-based gh/git workflows with
  end-to-end orchestration—handles uncommitted changes (auto-'
---

---
name: creating-pull-request
description: Standard workflow for all PR operations ('create PR', 'open PR', 'pull request', 'commit and PR'): replaces bash-based gh/git workflows with end-to-end orchestration—handles uncommitted changes (auto-invokes creating-commit/creating-branch), analyzes commit history, generates convention-aware content, detects fork/origin. Canonical PR implementation for git-workflows.
---

# Skill: Creating a Pull Request

## When to Use This Skill

Use this skill for pull request creation requests: "create a PR", "open a PR", "submit for review", or similar.

Use other skills for: viewing existing PRs (GitHub MCP directly), updating PRs (GitHub MCP update), or only committing changes (creating-commit).

## Workflow Description

Creates GitHub pull requests with automatic commit handling, repository detection, PR content generation, branch pushing, and GitHub PR creation via MCP.

Extract from user request: draft status ("draft"/"WIP" → true, default false), PR title/description (if provided), target branch (if specified, else mainline)

---

## Phase 1: Gather Context (Optimized)

**Objective**: Collect all PR context and validate prerequisites in a single atomic operation.

**Steps**:

1. **Determine base branch** from user request (optional):
   - Analyze user request for target branch specification
   - Look for phrases like: "create PR to <branch>", "base on <branch>", "merge into <branch>", "target <branch>"
   - Common branch names: develop, staging, main, master, release, etc.
   - Store base_branch if found, otherwise let script detect mainline

2. Run `../../scripts/gather-pr-context.sh` (optionally pass base_branch parameter if determined in step 1)

3. **Parse the JSON response and handle results**:

**IF `success: false`**:

Handle error based on `error_type`:

- **`not_git_repo`**:
  - STOP: "Not in a git repository"
  - Display: `message` and `suggested_action` from response
  - EXIT workflow

- **`on_base_branch`**:
  - STOP: "Cannot create PR from base branch with no new commits"
  - Display: `message` from response
  - EXPLAIN: "This should rarely occur - if you had uncommitted changes, creating-commit would have been invoked first and handled branch creation"
  - PROPOSE: "Create a feature branch manually or make changes first"
  - EXIT workflow

- **`no_commits`**:
  - STOP: "Branch has no commits to include in PR"
  - Display: `message` and `suggested_action` from response
  - EXIT workflow

- **Other errors**:
  - STOP: Display error details
  - EXIT workflow

**IF `success: true`**:

Extract and store context:

```json
{
  "current_branch": "feature-branch",
  "base_branch": "main",
  "is_fork": true,
  "repository": {
    "upstream_owner": "owner",
    "upstream_repo": "repo",
    "origin_owner": "user",
    "origin_repo": "repo"
  },
  "branch_validation": {
    "is_feature_branch": true,
    "has_uncommitted_changes": false
  },
  "uncommitted_files": [],
  "commit_history": [...],
  "diff_summary": {...},
  "uses_conventional_commits": true
}
```

### Validation Gate: Uncommitted Changes

IF `branch_validation.has_uncommitted_changes: true`:
  List files from `uncommitted_files` array
  INFORM: "Uncommitted changes detected - creating commit first"
  INVOKE: creating-commit skill (handles mainline detection internally)
  WAIT for creating-commit to complete

  IF creating-commit succeeded:
    RE-RUN Phase 1 (gather context again after commit)
    Continue to Phase 2

  IF creating-commit failed:
    STOP immediately
    EXPLAIN: "Cannot create PR without committing changes"
    EXIT workflow

IF no uncommitted changes:
  Continue to Phase 2

Phase 1 complete. Continue to Phase 2.

---

## Phase 2: Verify PR Base Branch

**Objective**: Confirm target branch for pull request.

**Steps**:

1. Use `base_branch` from Phase 1 context (already detected mainline)

2. IF user specified different target branch in Step 1 of Phase 1:
   - Override with user-specified branch
   - INFORM: "Using <user_branch> as PR base (overriding default <detected_mainline>)"

3. Store `pr_base` for later phases

Phase 2 complete. Continue to Phase 3.

---

## Phase 3: Generate PR Content

**Objective**: Create compelling PR title and description using context from Phase 1.

**Generate PR content considering:**

- Commit history and diff summary from Phase 1 context
- `commit_history` array (contains hash, subject, body for each commit)
- `diff_summary` object (files_changed, insertions, deletions)
- `uses_conventional_commits` flag for title format
- Purpose, scope, key changes, breaking changes
- Title (<72 chars, imperative) and description
- Quality and completeness

**Steps**:

1. Check user request for explicit title/description; use if provided
2. If not provided:
   - Title: Use Conventional Commits format if `uses_conventional_commits: true` from context
   - Description: Generate with sections (Summary, Changes, Motivation, Testing, Additional Notes)
3. Populate from `commit_history` and `diff_summary` in context

**Context Available** for PR content generation:

- `commit_history`: Array of commits with hash, subject, body
- `diff_summary`: Files changed, insertions, deletions
- `uses_conventional_commits`: Whether to use conventional format for title
- `base_branch`: Target branch for PR
- `current_branch`: Source branch for PR

Continue to Phase 4.

---

## Phase 4: PR Content Review

**Objective**: Present generated PR content for user review and approval.

**Steps**:

1. Present: Generated PR title and description from Phase 3
2. Request approval using AskUserQuestion tool:
   - Question: "How would you like to proceed with this pull request?"
   - Header: "PR Content"
   - Options:
     - **Proceed**: "Create PR with this title and description" - Continues to Phase 5
     - **Edit title**: "Modify the PR title" - Allows title customization
     - **Edit description**: "Modify the PR description" - Allows description customization
     - **Edit both**: "Modify both title and description" - Allows full customization

### Validation Gate: Content Approval

HANDLE user selection:

- IF "Proceed": Continue to Phase 5
- IF "Edit title":
  - User provides custom title via "Other" option
  - Validate: Title ≤ 72 chars, non-empty
  - IF invalid: Re-prompt with validation message
  - Update title, return to Step 1 to show updated PR
- IF "Edit description":
  - User provides custom description via "Other" option
  - Validate: Non-empty, markdown formatted
  - Update description, return to Step 1 to show updated PR
- IF "Edit both":
  - User provides custom title and description via "Other" option
  - Format expected: "TITLE: <title>\n\nDESCRIPTION:\n<description>"
  - Validate both components
  - Update both, return to Step 1 to show updated PR

Continue to Phase 5.

---

## Phase 5: Push to Remote

**Objective**: Push current branch to remote.

**Plan Mode**: Auto-enforced read-only if active

**Steps**:

1. Use `current_branch` from Phase 1 context (no need to query git)

2. Push branch with upstream tracking:

   ```bash
   git push -u origin <current_branch>
   ```

### Validation Gate: Push Failure

IF push fails:

- Analyze error:
  - "fatal: could not read Username": Authentication required
  - "error: failed to push": Rejected, may need force
  - "error: src refspec": Branch doesn't exist
  - Network errors: Connection issues
- Explain error clearly
- Propose solution:
  - Auth: "Set GITHUB_TOKEN or configure git credentials"
  - Rejected: "Check branch protection rules, may need PR approval"
  - Network: "Check internet connection and retry"
- Wait for user to resolve

Continue to Phase 6.

---

## Phase 6: Create Pull Request

**Objective**: Create PR on GitHub using MCP.

**Plan Mode**: Auto-enforced read-only if active

**Steps**:

1. Prepare parameters from Phase 1 context:
   - owner, repo: From `repository` object
   - head: `current_branch`
   - base: `pr_base` (from Phase 2)
   - title/body: Generated in Phase 3, approved in Phase 4

2. Determine draft: Check user request for "draft", "WIP", "work in progress"

3. Create: `mcp__github__create_pull_request` with all parameters

**Error Handling**: IF failure:

- Analyze error to determine cause: auth, permissions, invalid params, duplicate PR, rate limit, or network
- Explain clearly to user
- Propose solution and wait for retry approval

Continue to Phase 7.

---

## Phase 7: Return PR URL

**Objective**: Provide PR URL and confirm success with standardized output.

**Steps**:

1. Extract from Phase 6: PR number, URL, state, title

2. Format output using standardized template:

   ```markdown
   ✓ Pull Request Created Successfully

   **PR Number:** #<number> \
   **Title:** <title> \
   **URL:** <pr_url> \
   **Status:** <Open|Draft> \
   **Base Branch:** <base_branch> \
   **Head Branch:** <head_branch>

   [If draft: **Notes:** Mark as 'Ready for review' when ready]
   [If open: **Notes:** The pull request is ready for review]
   ```

Workflow complete.
