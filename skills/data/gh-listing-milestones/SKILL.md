---
name: gh-listing-milestones
description: Lists milestones in a repository. Use to track progress against release goals.
---

# Listing GitHub Milestones

## Purpose

Retrieves milestones using the `gh api` or `gh issue list` (via JSON) as there isn't a direct `gh milestone list`.

## 1. Safety & Verification

- **API Use**: Requires making a GET request to the milestones endpoint.

## 2. Common Workflows

### Workflow: List Active Milestones

Fetches milestones and their states.

**Command**:

```bash
gh api repos/:owner/:repo/milestones --jq '.[] | {number: .number, title: .title, state: .state}'
```
