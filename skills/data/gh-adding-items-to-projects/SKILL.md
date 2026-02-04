---
name: gh-adding-items-to-projects
description: Adds an issue or PR to a GitHub Project. Use to link repository work to a project board.
---

# Adding Items to Projects

## Purpose

Links a resource to a project using the `gh project item-add` command.

## 1. Safety & Verification

- **Mandatory Context**: Ensure `gh-verifying-context` has been run and confirmed by the user.
- **Human-in-the-Loop**: You MUST confirm the target project (name and number) and the item being added with the user.
- **Verification**: Use `gh-listing-projects` to ensure the project is the intended one.

## 2. Common Workflows

### Workflow: Add Issue

Links an issue to a project.

**Command**:

```bash
gh project item-add <project-number> --owner <owner> --url <issue-url>
```
