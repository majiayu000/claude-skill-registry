---
name: github-prs
description: Use when responding to PR comments, updating PRs, or handling PR feedback as an AI agent. Ensures proper identification and use of MCP tools.
---

# GitHub PRs

## Overview

Guidelines for AI agents handling pull request interactions. Agents must identify themselves and use MCP tools for GitHub operations.

## When to Use

- Responding to PR review comments
- Replying to PR discussion comments
- Updating PR based on feedback
- Checking PR status or reviews

## Agent Identification

**Always identify yourself as an AI agent when commenting on PRs.**

Use this signature at the end of PR comments:

```
— Claude
```

## MCP Tools for PRs

Use the GitHub MCP server tools instead of `gh` CLI when available:

| Task | MCP Tool |
|------|----------|
| Read PR details | `mcp__github__pull_request_read` with `method: "get"` |
| Get PR diff | `mcp__github__pull_request_read` with `method: "get_diff"` |
| Get PR comments | `mcp__github__pull_request_read` with `method: "get_comments"` |
| Get review comments | `mcp__github__pull_request_read` with `method: "get_review_comments"` |
| Get PR checks/status | `mcp__github__pull_request_read` with `method: "get_status"` |
| Add PR comment | `mcp__github__add_issue_comment` (PRs are issues) |
| Create review | `mcp__github__pull_request_review_write` with `method: "create"` |
| Update PR | `mcp__github__update_pull_request` |

## Reporting PR Checks

When asked about PR checks or status, use `pull_request_read` with `method: "get_status"` and display results in a table:

```markdown
| Check | Status | Details |
|-------|--------|---------|
| Validate PR Title | :white_check_mark: Passed | - |
| Build | :white_check_mark: Passed | - |
| Lint | :x: Failed | `src/auth.py:42` - Line too long |
| Tests | :hourglass: Pending | Running... |
```

Status icons:
- `:white_check_mark:` - Passed/Success
- `:x:` - Failed
- `:hourglass:` - Pending/In Progress
- `:warning:` - Skipped or neutral

## Responding to PR Comments

1. **Read the comment** using `pull_request_read` with `method: "get_comments"` or `"get_review_comments"`
2. **Understand the feedback** - what change is being requested?
3. **Make the fix** if it's a code change request
4. **Reply to acknowledge** using `add_issue_comment`
5. **Include agent signature** in your response

### Example Response

```markdown
Thanks for the feedback! I've updated the code to address your concern.

Changes made:
- Fixed the validation logic in `auth.py:45`
- Added the missing error handling

— Claude
```

## Handling Review Feedback

When a PR review requests changes:

1. Read review comments with `pull_request_read` method `"get_review_comments"`
2. Address each comment with code fixes
3. Commit and push fixes
4. Reply to each review thread if possible, or add a summary comment

### Summary Comment Template

```markdown
## Addressed Review Feedback

| Comment | Resolution |
|---------|------------|
| [Brief description] | [What was fixed] |
| [Brief description] | [What was fixed] |

All feedback has been addressed. Ready for re-review.

— Claude
```

## Key Principles

1. **Always identify as AI** - transparency about agent-generated responses
2. **Use MCP tools** - prefer MCP GitHub tools over CLI when available
3. **Acknowledge feedback** - always respond to comments, even if no code change needed
4. **Be concise** - keep responses focused and actionable
5. **Reference changes** - point to specific files/lines when discussing fixes
