---
name: gh-listing-labels
description: Lists available labels in a repository. Use to discover valid labels for triage.
---

# Listing GitHub Labels

## Purpose

Retrieves repository labels using the `gh label list` command.

## 1. Safety & Verification

- **Output**: Returns names, descriptions, and colors.

## 2. Common Workflows

### Workflow: Get All Labels

Lists labels to use for categorization.

**Command**:

```bash
gh label list --json name,description
```
