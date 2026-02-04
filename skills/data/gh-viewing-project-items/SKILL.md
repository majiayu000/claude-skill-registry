---
name: gh-viewing-project-items
description: Lists items within a GitHub Project. Use when you need to see which issues or PRs are on a board.
---

# Viewing Project Items

## Purpose

Retrieves all items in a project using the `gh project item-list` command.

## 1. Safety & Verification

- **Project Number**: Requires the project's numeric ID (not the UUID).

## 2. Common Workflows

### Workflow: List All Items

Retrieves titles and internal IDs of project items.

**Command**:

```bash
gh project item-list <project-number> --owner <owner> --json id,title,content
```

## 3. Output Handling

The internal item ID is required for updating or deleting items.
