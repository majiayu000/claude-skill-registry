---
name: gh-linking-branches-to-issues
description: Creates and links a development branch to an issue. Use to start implementation work.
---

# Linking Branches to Issues

## Purpose

Manages development branches using the `gh issue develop` command.

## 1. Safety & Verification

- **Mandatory Context**: Ensure `gh-verifying-context` has been run and confirmed by the user.
- **Human-in-the-Loop**: You MUST confirm the branch name and the target issue with the user before creation.
- **Repository Check**: Ensure you are in the correct repository (work vs personal) before creating a branch.

## 2. Common Workflows

### Workflow: Create Linked Branch

Creates a new branch and links it to the issue.

**Command**:

```bash
gh issue develop <issue-number> --name "feature-x"
```
