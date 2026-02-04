---
name: gh-commenting-on-issues
description: Adds a comment to a GitHub issue. Use to provide updates, ask questions, or link related work.
---

# Commenting on Issues

## Purpose

Posts updates to an existing issue using the `gh issue comment` command.

## 1. Safety & Verification

- **Mandatory Context**: Ensure `gh-verifying-context` has been run and confirmed by the user.
- **Human-in-the-Loop**: You MUST present the proposed comment body and the target issue number/URL to the user before execution.
- **Sensitivity Check**: Do not include internal credentials or proprietary details in comments.

## 2. Common Workflows

### Workflow: Post Update

Adds a simple text comment.

**Command**:

```bash
gh issue comment <issue-number> --body "Updated the implementation."
```

### Workflow: Multi-line Comment

Use quotes for the body string.

**Command**:

```bash
gh issue comment <issue-number> --body "Line 1
Line 2"
```

## 3. Best Practices

Be concise and clear in your updates.
