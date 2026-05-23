---
name: github-integration
description: Use when creating GitHub issues, managing PRs, updating issue states, or searching repositories - provides bash scripts to interact with GitHub REST API without writing API calls directly
---

# GitHub Integration

## Overview

Interact with GitHub repositories through simple bash scripts. All scripts handle REST API authentication and requests internally - you just provide repository details and arguments.

**Core principle:** Agents can manage GitHub issues and PRs without learning API endpoints or authentication flows.

## When to Use

- Creating issues from conversations or bug reports
- Managing pull requests
- Updating issue labels or states
- Searching code across repositories
- Closing or reopening issues

## Quick Reference

| Script | Purpose | Key Arguments |
|--------|---------|---------------|
| `gh-create-issue.sh` | Create new issue | `--owner`, `--repo`, `--title` |
| `gh-list-issues.sh` | List repository issues | `--owner`, `--repo`, `--state` |
| `gh-update-issue.sh` | Update issue | `--owner`, `--repo`, `--number` |
| `gh-create-pr.sh` | Create pull request | `--owner`, `--repo`, `--title`, `--head` |
| `gh-search-code.sh` | Search code | `--query`, `--owner`, `--repo` |

## Environment Setup

Required variable (set in `/experiments/skills/.env`):
```bash
GITHUB_TOKEN=ghp_xxx
```

Scripts automatically source the `.env` file from parent directory.

## Common Operations

### Create Issue
```bash
# Simple issue
scripts/gh-create-issue.sh \
  --owner myorg \
  --repo myrepo \
  --title "Fix login bug"

# With description and labels
scripts/gh-create-issue.sh \
  --owner myorg \
  --repo myrepo \
  --title "Add feature" \
  --body "Feature details here" \
  --labels "enhancement,priority"

# Assign to users
scripts/gh-create-issue.sh \
  --owner myorg \
  --repo myrepo \
  --title "Task" \
  --assignees "username1,username2"
```

### List Issues
```bash
# All open issues
scripts/gh-list-issues.sh --owner myorg --repo myrepo

# All issues (open and closed)
scripts/gh-list-issues.sh \
  --owner myorg \
  --repo myrepo \
  --state all \
  --limit 50

# Filter by label and assignee
scripts/gh-list-issues.sh \
  --owner myorg \
  --repo myrepo \
  --labels "bug" \
  --assignee "username"
```

### Update Issue
```bash
# Change title
scripts/gh-update-issue.sh \
  --owner myorg \
  --repo myrepo \
  --number 42 \
  --title "Updated title"

# Close issue
scripts/gh-update-issue.sh \
  --owner myorg \
  --repo myrepo \
  --number 42 \
  --state closed

# Update labels (replaces existing)
scripts/gh-update-issue.sh \
  --owner myorg \
  --repo myrepo \
  --number 42 \
  --labels "bug,priority,in-progress"
```

### Create Pull Request
```bash
# Simple PR
scripts/gh-create-pr.sh \
  --owner myorg \
  --repo myrepo \
  --title "Fix bug" \
  --head feature-branch

# With description and custom base
scripts/gh-create-pr.sh \
  --owner myorg \
  --repo myrepo \
  --title "New feature" \
  --head feat-branch \
  --base develop \
  --body "Feature description"

# Draft PR
scripts/gh-create-pr.sh \
  --owner myorg \
  --repo myrepo \
  --title "WIP: Feature" \
  --head feat-branch \
  --draft
```

### Search Code
```bash
# Search across all repos
scripts/gh-search-code.sh --query "function authenticate"

# Search in specific organization
scripts/gh-search-code.sh \
  --query "class User" \
  --owner myorg

# Search in specific repo
scripts/gh-search-code.sh \
  --query "TODO" \
  --owner myorg \
  --repo myrepo \
  --limit 10
```

## Output Format

All scripts return JSON with relevant data:

```json
{
  "id": 123456,
  "number": 42,
  "title": "Issue title",
  "state": "open",
  "url": "https://github.com/owner/repo/issues/42",
  "api_url": "https://api.github.com/repos/owner/repo/issues/42"
}
```

## Common Mistakes

**Missing owner or repo**
- ❌ GitHub token alone isn't enough
- ✅ Always specify `--owner` and `--repo` for repository operations

**Using gh CLI syntax**
- ❌ Don't: `gh issue create --title "Title"`
- ✅ Do: `gh-create-issue.sh --owner org --repo repo --title "Title"`

**Forgetting issue numbers are not IDs**
- Use `--number` (the visible number like #42)
- Don't use the internal `id` field from API responses

**Labels replace instead of append**
- `--labels "bug,new"` replaces all existing labels
- To preserve labels, fetch current labels first and include them

**Personal access token permissions**
- Token needs `repo` scope for private repositories
- Token needs `public_repo` scope for public repositories
- Error "Not Found" often means insufficient permissions

## Script Location

Scripts are located in the `scripts/` directory within this skill. They can be called from any directory as they auto-source the parent `.env` file.
