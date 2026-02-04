---
name: gh-transferring-issues
description: Transfers an issue to another repository. Use for cross-project reorganization.
---

# Transferring Issues

## Purpose

Moves an issue using the `gh issue transfer` command.

## 1. Safety & Verification

- **Permissions**: Requires write access to both source and destination repositories.

## 2. Common Workflows

### Workflow: Move to New Repo

Transfers an issue to a different project.

**Command**:

```bash
gh issue transfer <issue-number> <destination-repo>
```
