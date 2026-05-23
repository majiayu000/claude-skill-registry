---
name: gh-labeling-issues
description: Manages labels on a GitHub issue. Use for triage and categorization.
---

# Labeling Issues

## Purpose

Updates labels using the `gh issue edit` command.

## 1. Safety & Verification

- **Mandatory Context**: Ensure `gh-verifying-context` has been run and confirmed by the user.
- **Human-in-the-Loop**: You MUST present the proposed labels to be added or removed to the user before execution.
- **Existing Labels**: Verify the labels exist in the repo first using `gh-listing-labels`.

## 2. Common Workflows

### Workflow: Add Labels

Attaches new categories to an issue.

**Command**:

```bash
gh issue edit <issue-number> --add-label "bug,triage"
```

### Workflow: Remove Labels

Detaches labels from an issue.

**Command**:

```bash
gh issue edit <issue-number> --remove-label "needs-investigation"
```
