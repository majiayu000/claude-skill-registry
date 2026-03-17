---
name: pull-request-review
description: This skill should be used when checking for code review comments on a pull request and implementing them if required. It fetches PR metadata and comments, generates a brief from unresolved feedback, and bootstraps a project to address the review comments.
allowed-tools: ["Read", "Bash", "Glob", "Grep"]
---

# Review PR Comments

Target PR: $ARGUMENTS

If no argument provided, prompt the user for a PR link or number.

## Step 1: Gather Requirements

1. **Fetch PR metadata and comments** using the GitHub CLI:
   ```bash
   gh pr view $ARGUMENTS --json number,title,body,reviews,comments
   gh api repos/{owner}/{repo}/pulls/{pr_number}/comments
   ```
2. **Extract each unresolved review comment**:
   - Comment ID
   - File path
   - Line number
   - Comment body
   - Author

If no unresolved comments exist, report success and exit.

## Step 2: Create Plan

In plan mode, create a plan that includes the following details:

```markdown
Implement PR review feedback for $ARGUMENTS.

## PR Overview
- Title: [PR title]
- Description: [PR description summary]

## Review Comments to Address (ordered by file)

### 1. [file_path]:[line_number] (Comment ID: [id])
**Reviewer**: [author]
**Comment**: [full comment body]
**Action Required**: [brief description of what needs to change]

### 2. [file_path]:[line_number] (Comment ID: [id])
**Reviewer**: [author]
**Comment**: [full comment body]
**Action Required**: [brief description of what needs to change]

...

## Implementation Guidelines
- Evaluate each comment for validity before implementing
- If a comment is not valid, document the reasoning
- Ensure changes follow project coding standards
- Run relevant tests to verify changes work

## Acceptance Criteria
- All valid review comments addressed
- Tests pass after changes
- `bun run lint` passes

## Verification
Command: `bun run lint && bun run test`
Expected: All checks pass
```