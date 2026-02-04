---
name: gh-listing-project-fields
description: Lists custom fields in a GitHub Project. Use to discover field IDs like "Status" or "Priority".
---

# Listing Project Fields

## Purpose

Retrieves metadata about project fields using the `gh project field-list` command.

## 1. Safety & Verification

- **Output Format**: Use `--format json` for detailed field info including option IDs for single-select fields.

## 2. Common Workflows

### Workflow: Discover Field IDs

Finds the internal IDs required for editing item values.

**Command**:

```bash
gh project field-list <project-number> --owner <owner> --format json
```
