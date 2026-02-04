---
name: gh-listing-issues
description: Lists GitHub issues with optional filtering. Use when you need to browse open, closed, or specifically labeled issues in a repository.
---

# Listing GitHub Issues

## Purpose

Provides a standard way to retrieve a list of issues from a repository using the `gh issue list` command.

## 1. Safety & Verification

- **Repository Context**: Ensure you are in a git repository or use the `-R owner/repo` flag.
- **JSON Output**: Always prefer `--json` for structured data.

## 2. Common Workflows

### Workflow: List Open Issues

Retrieves the most recent open issues with relevant metadata.

**Command**:

```bash
gh issue list --state open --json number,title,labels,updatedAt
```

### Workflow: Filter by Label

Lists issues that have specific labels.

**Command**:

```bash
gh issue list --label "bug,help wanted" --json number,title,state
```

### Workflow: Advanced Search for Sub-issues

Filters issues based on their hierarchical status.

**Command**:

```bash
# List all issues that have sub-issues
gh issue list --search "has:sub-issue" --json number,title

# List all issues that do NOT have a parent (top-level issues)
gh issue list --search "no:parent-issue" --json number,title
```

## 3. Output Handling

Use `jq` to extract specific values if needed for further automation.

**Example**:

```bash
gh issue list --state open --json number --jq '.[].number'
```
