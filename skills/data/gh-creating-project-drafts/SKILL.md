---
name: gh-creating-project-drafts
description: Creates a draft issue item in a GitHub Project. Use for items that don't yet have a corresponding repository issue.
---

# Creating Project Drafts

## Purpose

Adds a draft item to a project using the `gh project item-create` command.

## 1. Safety & Verification

- **Content**: Requires a title and optionally a body.

## 2. Common Workflows

### Workflow: Create Simple Draft

Adds a note or placeholder to a board.

**Command**:

```bash
gh project item-create <project-number> --owner <owner> --title "Draft Title" --body "Draft Body"
```
