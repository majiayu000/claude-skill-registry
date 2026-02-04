---
name: gh-managing-sub-issues
description: Manages GitHub sub-issues (parent-child relationships) using the GitHub REST API. Use when you need to list, add, remove, or reprioritize sub-issues for a parent issue.
---

# Managing GitHub Sub-issues

## Purpose

Provides a standardized way to manage hierarchical relationships between issues using the GitHub Sub-issues REST API. Since sub-issues are not yet first-class flags in the `gh issue` commands, this skill uses `gh api` for direct interaction.

## 1. Safety & Verification

Before executing any commands, the agent must:

1.  **Context Verification**: Ensure `gh-verifying-context` has been run and confirmed.
2.  **Human-in-the-Loop**: Preview all state-changing commands (`POST`, `DELETE`, `PATCH`) to the user for approval.
3.  **Repository Confirmation**: Ensure you are targeting the correct repository and issue numbers.

## 2. Common Workflows

### Workflow: List Sub-issues

Lists all sub-issues associated with a specific parent issue.

**Command**:

```bash
gh api /repos/{owner}/{repo}/issues/{issue_number}/sub_issues
```

### Workflow: Add Sub-issue

Links an existing issue as a sub-issue to a parent issue.

**Command**:

```bash
gh api --method POST /repos/{owner}/{repo}/issues/{parent_number}/sub_issues \
  -F sub_issue_id={sub_issue_id}
```

_Note: `sub_issue_id` is the database ID of the issue, not the issue number. You can find this in the output of `gh issue view` or by querying the API._

### Workflow: Remove Sub-issue

Unlinks a sub-issue from its parent issue.

**Command**:

```bash
gh api --method DELETE /repos/{owner}/{repo}/issues/{parent_number}/sub_issue \
  -F sub_issue_id={sub_issue_id}
```

### Workflow: Reprioritize Sub-issue

Changes the order of a sub-issue within its parent's list.

**Command**:

```bash
# Move sub-issue after another sub-issue
gh api --method PATCH /repos/{owner}/{repo}/issues/{parent_number}/sub_issues/priority \
  -F sub_issue_id={sub_issue_id} \
  -F after_id={after_id}

# Move sub-issue before another sub-issue
gh api --method PATCH /repos/{owner}/{repo}/issues/{parent_number}/sub_issues/priority \
  -F sub_issue_id={sub_issue_id} \
  -F before_id={before_id}
```

## 3. Error Handling

- **Invalid ID**: If the API returns a 404 or validation error, double-check that you are using the `id` (integer) and not the `number`.
- **Permissions**: Ensure the token has `write` access to the repository for state-changing operations.
- **Limit Exceeded**: GitHub currently allows up to 100 sub-issues per parent and up to 8 levels of nesting.
