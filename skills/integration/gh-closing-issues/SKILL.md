---
name: gh-closing-issues
description: Closes a GitHub issue. Use when a task is completed or an issue is resolved.
---

# Closing GitHub Issues

## Purpose

Resolves an issue using the `gh issue close` command.

## 1. Safety & Verification

- **Mandatory Context**: Ensure `gh-verifying-context` has been run and confirmed by the user.
- **Human-in-the-Loop**: You MUST confirm with the user before closing any issue. State the issue number and title clearly.
- **Verification**: Ensure the issue is actually resolved according to the user's criteria.

## 2. Common Workflows

### Workflow: Close as Completed

Default closing behavior.

**Command**:

```bash
gh issue close <issue-number> --reason completed
```

### Workflow: Close with Comment

It's often good practice to add a comment explaining why the issue is being closed.

**Command**:

```bash
gh issue comment <issue-number> --body "Closing as this is resolved." && gh issue close <issue-number>
```
