---
name: sync-plan
description: Sync PLANS.md content to linked GitHub issue comment. Use when PLANS.md is updated and changes need to be reflected in the GitHub issue.
disable-model-invocation: true
---

# Sync Plan

Synchronize PLANS.md with its linked GitHub issue comment.

## Prerequisites

- PLANS.md must exist in the project root
- PLANS.md must have frontmatter with `issue:` field

## Workflow

### 1. Read Issue Metadata from PLANS.md

Extract `issue:` and `issue_url:` from frontmatter.

If no `issue:` field:
```
Error: No issue linked to PLANS.md
Create an issue-linked plan with: /create-plan <issue-number>
```

### 2. Get Repository Information

```bash
gh repo view --json owner,name
```

### 3. Find Existing Sync Comment

```bash
gh api repos/{owner}/{name}/issues/{issue}/comments \
  --jq '.[] | select(.body | contains("PLANS_SYNC_MARKER")) | .id'
```

### 4. Update or Create Comment

```bash
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
CONTENT="<!-- PLANS_SYNC_MARKER:${TIMESTAMP} -->

$(tail -n +5 PLANS.md)"
```

**If comment exists**:
```bash
gh api -X PATCH repos/{owner}/{name}/issues/comments/{comment_id} \
  -f body="$CONTENT"
```

**If no comment exists**:
```bash
gh issue comment {issue} --body "$CONTENT"
```

### 5. Update PLANS.md Frontmatter

Update `last_synced` field with new timestamp.

### 6. Confirm Success

```
✓ Synced PLANS.md to issue #123
  Timestamp: 2025-11-12T10:30:00Z
```

## Notes

- Sync is one-directional: PLANS.md → GitHub Issue
- Manual edits to GitHub comment will be overwritten
