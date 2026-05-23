---
name: gh-assigning-issues
description: Manages assignees on a GitHub issue. Use to indicate ownership or request review.
---

# Assigning Issues

## Purpose

Edits issue assignees using the `gh issue edit` command.

## 1. Safety & Verification

- **Collaborators**: Users must have appropriate permissions to be assigned.

## 2. Common Workflows

### Workflow: Assign to Self

Sets yourself as the owner.

**Command**:

```bash
gh issue edit <issue-number> --add-assignee "@me"
```

### Workflow: Add Multiple Assignees

Comma-separated list of usernames.

**Command**:

```bash
gh issue edit <issue-number> --add-assignee "user1,user2"
```
