---
name: gh-creating-issues
description: Creates a new GitHub issue. Use when a new task, bug, or feature request needs to be tracked.
---

# Creating GitHub Issues

## Purpose

Enables the creation of new issues using the `gh issue create` command.

## 1. Safety & Verification

- **Mandatory Context**: Ensure `gh-verifying-context` has been run and confirmed by the user.
- **Human-in-the-Loop**: You MUST present the full command and the issue content (Title, Body) to the user before execution.
- **Repository Check**: Confirm the target repository name and owner with the user.
- **Sensitivity Check**: Do not include internal credentials, server IPs, or proprietary snippets in the issue body.

## 2. Common Workflows

### Workflow: Create Basic Issue

Creates an issue with a title and body.

**Command**:

```bash
gh issue create --title "My Title" --body "My Description"
```

### Workflow: Create with Labels, Assignees, and Projects

Sets metadata and links to a project board at creation time.

**Command**:

```bash
gh issue create --title "Bug Report" --body "Steps to repro..." --label "bug" --assignee "@me" --project "Roadmap"
```

### Workflow: Create and Link as Sub-issue

Creates a new issue and immediately links it as a sub-issue to an existing parent.

**Command**:

```bash
# 1. Create the issue and get its numeric ID
NEW_ISSUE_ID=$(gh issue create --title "Sub-task" --body "Details..." --json id -q .id)

# 2. Link it to the parent
gh api --method POST /repos/{owner}/{repo}/issues/{parent_number}/sub_issues \
  -F sub_issue_id=$NEW_ISSUE_ID
```

## 3. Output Handling

Returns the URL of the created issue.
