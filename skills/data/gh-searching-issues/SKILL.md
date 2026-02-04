---
name: gh-searching-issues
description: Performs advanced searches for issues. Use when looking for duplicates or specific keywords across repositories.
---

# Searching GitHub Issues

## Purpose

Finds issues using the `gh search issues` command with powerful qualifiers.

## 1. Safety & Verification

- **Qualifiers**: Supports `label:`, `state:`, `author:`, etc.

## 2. Common Workflows

### Workflow: Search by Keyword

Finds open issues matching a string.

**Command**:

```bash
gh search issues "bug" --state open --json number,title,repository
```

### Workflow: Find Unprojected Issues

Finds issues that are not in any project.

**Command**:

```bash
gh search issues --no-project --state open --json number,title
```
