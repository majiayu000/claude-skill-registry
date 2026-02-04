---
name: gh-listing-projects
description: Lists GitHub Projects (v2). Use when you need to find project IDs or view available boards.
---

# Listing GitHub Projects

## Purpose

Retrieves projects associated with an owner using the `gh project list` command.

## 1. Safety & Verification

- **Owner Flag**: The `--owner` flag is mandatory for organization-level projects.

## 2. Common Workflows

### Workflow: List Personal Projects

Lists projects for the current user.

**Command**:

```bash
gh project list --owner "@me"
```

### Workflow: List Org Projects

Lists projects for a specific organization.

**Command**:

```bash
gh project list --owner "my-org" --json number,title,id
```
