---
name: pr-merge
description: Safely merge GitHub pull requests using comprehensive pre-merge validation. Use this skill when the user asks to merge a PR, complete a PR workflow, or check if a PR is ready to merge. Validates CI/CD status, reviews, and conflicts before merging with the appropriate strategy.
---

# PR Merge

## Overview

This skill enables safe and comprehensive pull request merging workflows using GitHub MCP tools. It automates the complete pre-merge validation process, checks CI/CD status, verifies reviews, and executes merges with the appropriate merge strategy.

## When to Use This Skill

Use this skill when the user requests:
- "Merge PR #123"
- "Can we merge this pull request?"
- "Check if PR is ready to merge"
- "Complete the PR workflow"
- "Merge this feature branch"
- "Is PR #456 ready to be merged?"

## Pre-Merge Validation Workflow

Before merging any PR, execute the complete validation workflow to ensure safety and quality.

### Step 1: Fetch PR Details

Use `mcp__github-mcp__get_pull_request` to retrieve:
- PR title and description
- Base and head branches
- Draft status
- Current state (open/closed)

**Required parameters:**
- `owner`: Repository owner
- `repo`: Repository name
- `pullNumber`: PR number

### Step 2: Check CI/CD Status

Use `mcp__github-mcp__get_pull_request_status` to verify:
- All required checks are passing
- No failed CI/CD workflows
- Branch protection rules are satisfied

**Block merge if:**
- Any required checks are failing
- Checks are still pending (inform user to wait)
- Branch protection rules are not met

### Step 3: Verify Reviews

Use `mcp__github-mcp__get_pull_request_reviews` to confirm:
- Sufficient approved reviews exist
- No requested changes are outstanding
- Review requirements are met per branch protection

**Block merge if:**
- Required reviews are missing
- Any reviewer has requested changes
- Review dismissals need to be addressed

### Step 4: Check for Conflicts

Use `mcp__github-mcp__get_pull_request_diff` to identify:
- Merge conflicts with base branch
- File-level conflicts that need resolution

**Block merge if:**
- Merge conflicts are present (instruct user to resolve)
- Base branch needs to be updated first

### Step 5: Review Changes (Optional)

For additional safety, use `mcp__github-mcp__get_pull_request_files` to:
- Review changed files
- Identify potential issues
- Confirm changes align with PR description

## Merge Execution

Once all validations pass, execute the merge using `mcp__github-mcp__merge_pull_request`.

### Selecting Merge Method

Choose the appropriate merge method based on project conventions and commit history:

**Squash Merge (`squash`):**
- Use for: Feature branches with messy commit history
- Benefits: Clean, single commit in main branch
- When: Multiple small commits, WIP commits, or iterative development
- Example: PR with 15 commits like "fix typo", "address review", "fix tests"

**Merge Commit (`merge`):**
- Use for: Preserving complete commit history
- Benefits: Full audit trail, maintains original commits
- When: Well-structured commits with meaningful messages
- Example: PR with clean, atomic commits following conventional commit style

**Rebase Merge (`rebase`):**
- Use for: Linear history without merge commits
- Benefits: Clean, linear git history
- When: Small PRs with few commits
- Example: Single-commit PRs or small bug fixes

**Default recommendation:** Use `squash` unless project conventions dictate otherwise.

### Merge Parameters

**Required:**
- `owner`: Repository owner
- `repo`: Repository name
- `pullNumber`: PR number

**Optional:**
- `merge_method`: "merge", "squash", or "rebase" (default: merge)
- `commit_title`: Custom commit title for squash/merge
- `commit_message`: Additional commit message details

### Example Merge Execution

```
Use mcp__github-mcp__merge_pull_request with:
- owner: "user"
- repo: "project"
- pullNumber: 123
- merge_method: "squash"
- commit_title: "feat: add user authentication system"
```

## Post-Merge Actions

After successful merge, inform the user:
1. Confirm merge completion
2. Show resulting commit SHA
3. Note which branch was merged
4. Suggest deleting the head branch if appropriate

**Do not automatically delete branches** - let the user decide or check repository settings.

## Safety Guidelines

Always follow these safety rules:

1. **Never force merge** - All checks must pass
2. **Never bypass reviews** - Required approvals must exist
3. **Never merge with conflicts** - Conflicts must be resolved first
4. **Never merge draft PRs** - Must be marked as ready for review
5. **Always inform the user** - Provide clear feedback on validation status

## Validation Failure Responses

When pre-merge validation fails, provide clear, actionable feedback:

**CI/CD Failures:**
- List which checks are failing
- Suggest using `mcp__github-mcp__get_job_logs` with `failed_only=true` to diagnose
- Recommend reviewing workflow files

**Review Issues:**
- List missing required reviews
- Identify reviewers who requested changes
- Suggest addressing review comments first

**Merge Conflicts:**
- Identify conflicting files
- Recommend updating base branch with `mcp__github-mcp__update_pull_request_branch`
- Suggest resolving conflicts locally if needed

**Branch Protection:**
- List unmet protection rules
- Explain which requirements are blocking
- Suggest how to satisfy requirements

## Advanced Features

### Request Automated Review

Before merging, optionally use `mcp__github-mcp__request_copilot_review` to:
- Get AI-powered code review
- Identify potential issues
- Supplement human reviews

### Update Branch Before Merge

If the base branch has advanced, use `mcp__github-mcp__update_pull_request_branch` to:
- Sync PR branch with latest base
- Trigger CI/CD re-runs
- Ensure up-to-date merge

### Check Multiple PRs

For workflow automation, can validate multiple PRs in sequence:
1. Use `mcp__github-mcp__list_pull_requests` to find open PRs
2. Filter for PRs ready to merge
3. Execute validation workflow for each
4. Present merge candidates to user

## Complete Workflow Example

**User request:** "Merge PR #42"

**Execution sequence:**

1. Fetch PR details → Confirm it's open, not draft
2. Check CI/CD status → All checks passing ✓
3. Verify reviews → 2 approvals, no requested changes ✓
4. Check conflicts → No conflicts ✓
5. Select merge method → Choose squash (clean commit history)
6. Execute merge → `merge_pull_request` with squash method
7. Confirm success → "PR #42 successfully merged with squash merge"

## Error Handling

Handle common errors gracefully:

- **404 Not Found:** PR doesn't exist, verify PR number
- **405 Method Not Allowed:** PR already merged or closed
- **409 Conflict:** Merge conflict exists, need resolution
- **422 Validation Failed:** Branch protection rules not met

Provide clear error messages and next steps for resolution.

## Resources

This skill uses GitHub MCP tools exclusively and does not require additional scripts, references, or assets. All functionality is provided through the MCP integration.
