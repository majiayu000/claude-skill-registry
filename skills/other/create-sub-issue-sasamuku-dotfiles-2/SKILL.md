---
name: create-sub-issue
description: Create a sub-issue linked to a parent GitHub issue
disable-model-invocation: true
---

# Create Sub-Issue

Create a sub-issue linked to a parent GitHub issue using the sub-issue API.

## Arguments

- Parent issue number (e.g., `123` or `#123`)
- Parent issue URL
- Sub-issue description (optional)

$ARGUMENTS

## Process

### 1. Get Parent Issue Context

```bash
gh issue view <issue-number> --json number,title,body,url
```

Find PLANS_SYNC_MARKER comment for detailed context.

### 2. Create Sub-Issue

Follow create-issue guidelines with:
- **REQUIRED**: Start body with `Part of #{parent-issue-number}`
- Create focused, actionable issue

### 3. Link to Parent

```bash
ISSUE_URL=$(gh issue create --title "$TITLE" --body "$BODY" --label "sub-issue")
ISSUE_NUMBER=$(echo $ISSUE_URL | grep -o '[0-9]*$')
# IMPORTANT: Use .id (integer), NOT .node_id (string)
SUB_ISSUE_ID=$(gh api /repos/{owner}/{repo}/issues/$ISSUE_NUMBER --jq .id)
gh api --method POST /repos/{owner}/{repo}/issues/{parent-number}/sub_issues \
  -F "sub_issue_id=$SUB_ISSUE_ID"
```

### 4. Order Multiple Sub-Issues (if creating several)

```bash
gh api --method PATCH /repos/{owner}/{repo}/issues/{parent-number}/sub_issues/priority \
  --input - <<< '{"sub_issue_id": '$SUB_ISSUE_ID', "after_id": '$PREV_SUB_ISSUE_ID'}'
```

## Body Format

```markdown
Part of #{parent-issue-number}

[Template content or standard structure]
```

## Best Practices

- Use parent issue body + PLANS_SYNC_MARKER comment for context
- Keep sub-issues focused and independently completable
- Apply consistent labels
