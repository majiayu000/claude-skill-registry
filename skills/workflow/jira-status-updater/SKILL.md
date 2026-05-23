---
name: jira-status-updater
description: Automate JIRA ticket status transitions after pull requests are merged, ensuring proper workflow closure
license: Apache-2.0
compatibility: opencode
metadata:
  audience: developers
  workflow: jira-status-transition
---

## What I do

I provide automated JIRA ticket status transitions to ensure proper workflow completion after PR merges:

1. **Detect JIRA Ticket**: Extract JIRA ticket key from PR title, commits, or branch name
2. **Query Available Transitions**: Use Atlassian API to get valid status transitions for the ticket
3. **Identify Target Status**: Find "Done" or "Closed" status transition
4. **Execute Status Transition**: Update JIRA ticket status using transition API
5. **Add Merge Comment**: Post final comment with PR merge details
6. **Handle Edge Cases**: Gracefully handle missing transitions, permissions, already-done status
7. **Log Status**: Provide clear feedback on transition success/failure

## When to use me

Use this framework when:
- A PR has been successfully merged
- You need to update the linked JIRA ticket status
- You want to ensure JIRA tickets are properly closed after work completion
- You're building a workflow that includes PR merge handling
- You need automated JIRA workflow management

This is a **framework skill** - it provides JIRA status transition functionality that other skills use.

## Core Workflow Steps

### Step 1: Detect JIRA Ticket Reference

**Purpose**: Extract JIRA ticket key from PR or commit information

**Detection Methods** (in priority order):

| Source | Detection Pattern | Example | Command |
|--------|------------------|----------|---------|
| PR Title | Regex for JIRA key | `feat: Add login [IBIS-101]` | Extract from `gh pr view` |
| Commit Messages | Regex for JIRA key | `[IBIS-123] Fix bug` | `git log --oneline` |
| Branch Name | Parse ticket key | `IBIS-101-add-feature` | `git branch --show-current` |
| PLAN.md | Search for references | `JIRA Reference: IBIS-456` | Read PLAN.md |

**Detection Logic**:
```bash
# Method 1: Extract from PR title (if available)
if command -v gh &>/dev/null; then
  PR_TITLE=$(gh pr view --json title --jq '.title')
  JIRA_TICKET=$(echo "$PR_TITLE" | grep -oE '[A-Z]+-[0-9]+' | head -1)
fi

# Method 2: Extract from latest commit
if [ -z "$JIRA_TICKET" ]; then
  JIRA_TICKET=$(git log --oneline -1 | grep -oE '[A-Z]+-[0-9]+' | head -1)
fi

# Method 3: Extract from branch name
if [ -z "$JIRA_TICKET" ]; then
  BRANCH_NAME=$(git branch --show-current)
  JIRA_TICKET=$(echo "$BRANCH_NAME" | grep -oE '[A-Z]+-[0-9]+' | head -1)
fi

# Method 4: Extract from PLAN.md
if [ -z "$JIRA_TICKET" ] && [ -f "PLAN.md" ]; then
  JIRA_TICKET=$(grep -oE '[A-Z]+-[0-9]+' PLAN.md | head -1)
fi

# Validate ticket format
if [ -n "$JIRA_TICKET" ]; then
  echo "✅ Detected JIRA ticket: $JIRA_TICKET"
else
  echo "⚠️  No JIRA ticket reference found"
  return 1
fi
```

### Step 2: Get Available Transitions

**Purpose**: Query Atlassian API to get valid status transitions for the ticket

**Tools Used**: `atlassian_getTransitionsForJiraIssue`

```bash
# Get cloud ID
CLOUD_ID="${ATLASSIAN_CLOUD_ID:-<default-cloud-id>}"

# Query available transitions
TRANSITIONS=$(atlassian_getTransitionsForJiraIssue \
  --cloudId "$CLOUD_ID" \
  --issueIdOrKey "$JIRA_TICKET")

# Parse transitions
echo "Available transitions for $JIRA_TICKET:"
echo "$TRANSITIONS" | jq -r '.transitions[] | "- \(.name) → \(.to.name)"'
```

**Expected Output**:
```json
{
  "transitions": [
    {
      "id": "121",
      "name": "Done",
      "to": {
        "id": "101",
        "name": "Done",
        "statusCategory": {
          "id": "3",
          "key": "done",
          "colorName": "green"
        }
      }
    },
    {
      "id": "131",
      "name": "In Review",
      "to": {
        "id": "103",
        "name": "In Review",
        "statusCategory": {
          "id": "4",
          "key": "inprogress",
          "colorName": "blue"
        }
      }
    }
  ]
}
```

### Step 3: Identify Target Status Transition

**Purpose**: Find the transition that leads to "Done" or "Closed" status

**Target Status Priority**:
1. **Done** - Most common final status
2. **Closed** - Alternative final status
3. **Custom status** - Any status with category "done"

**Detection Logic**:
```bash
# Try to find "Done" transition
TARGET_TRANSITION=$(echo "$TRANSITIONS" | \
  jq -r '.transitions[] | select(.to.name == "Done") | {id: .id, name: .name}')

# If no "Done", try "Closed"
if [ -z "$TARGET_TRANSITION" ]; then
  TARGET_TRANSITION=$(echo "$TRANSITIONS" | \
    jq -r '.transitions[] | select(.to.name == "Closed") | {id: .id, name: .name}')
fi

# If no specific status found, try any "done" category status
if [ -z "$TARGET_TRANSITION" ]; then
  TARGET_TRANSITION=$(echo "$TRANSITIONS" | \
    jq -r '.transitions[] | select(.to.statusCategory.key == "done") | {id: .id, name: .name} | first')
fi

# Extract transition ID and name
TRANSITION_ID=$(echo "$TARGET_TRANSITION" | jq -r '.id')
TRANSITION_NAME=$(echo "$TARGET_TRANSITION" | jq -r '.name')

if [ -n "$TRANSITION_ID" ]; then
  echo "✅ Found target transition: $TRANSITION_NAME (ID: $TRANSITION_ID)"
else
  echo "⚠️  No 'Done' or 'Closed' transition available for $JIRA_TICKET"
  return 1
fi
```

**Alternative Status Handling**:
Some JIRA workflows use different final status names:
- `Done`, `Closed`, `Complete`, `Finished`, `Resolved`
- Use statusCategory.key == "done" to find any done-category status

### Step 4: Check Current Status

**Purpose**: Avoid unnecessary transitions if ticket is already in target status

**Tools Used**: `atlassian_getJiraIssue`

```bash
# Get current ticket status
TICKET_DETAILS=$(atlassian_getJiraIssue \
  --cloudId "$CLOUD_ID" \
  --issueIdOrKey "$JIRA_TICKET")

CURRENT_STATUS=$(echo "$TICKET_DETAILS" | jq -r '.fields.status.name')

echo "Current status: $CURRENT_STATUS"
echo "Target status: $TRANSITION_NAME"

# Check if already in target status
if [ "$CURRENT_STATUS" = "$TRANSITION_NAME" ]; then
  echo "✅ Ticket already in target status: $TRANSITION_NAME"
  echo "No transition needed"
  return 0
fi

# Check if status category is already "done"
CURRENT_CATEGORY=$(echo "$TICKET_DETAILS" | jq -r '.fields.status.statusCategory.key')
if [ "$CURRENT_CATEGORY" = "done" ]; then
  echo "✅ Ticket already in done category: $CURRENT_STATUS"
  echo "No transition needed"
  return 0
fi
```

### Step 5: Execute Status Transition

**Purpose**: Update JIRA ticket status to target status

**Tools Used**: `atlassian_transitionJiraIssue`

```bash
# Execute transition
echo "Transitioning $JIRA_TICKET from $CURRENT_STATUS to $TRANSITION_NAME..."

TRANSITION_RESULT=$(atlassian_transitionJiraIssue \
  --cloudId "$CLOUD_ID" \
  --issueIdOrKey "$JIRA_TICKET" \
  --transition "{\"id\": \"$TRANSITION_ID\"}")

# Check if transition was successful
if [ $? -eq 0 ]; then
  echo "✅ Successfully transitioned $JIRA_TICKET to $TRANSITION_NAME"
  STATUS="success"
else
  echo "❌ Failed to transition $JIRA_TICKET"
  STATUS="failed"
fi
```

**Error Handling**:
```bash
# Check for common errors
if echo "$TRANSITION_RESULT" | grep -q "permission"; then
  echo "❌ Permission denied: You don't have permission to transition this ticket"
  STATUS="permission_denied"
elif echo "$TRANSITION_RESULT" | grep -q "transition does not exist"; then
  echo "❌ Invalid transition: The selected transition is not available"
  STATUS="invalid_transition"
elif echo "$TRANSITION_RESULT" | grep -q "issue does not exist"; then
  echo "❌ Invalid ticket: $JIRA_TICKET does not exist"
  STATUS="invalid_ticket"
fi
```

### Step 6: Add Merge Comment to JIRA

**Purpose**: Document the PR merge with details for traceability

**Tools Used**: `atlassian_addCommentToJiraIssue`

```bash
# Get PR details
PR_NUMBER=$(gh pr view --json number --jq '.number')
PR_URL=$(gh pr view --json url --jq '.url')
PR_TITLE=$(gh pr view --json title --jq '.title')
MERGED_BY=$(gh pr view --json mergedBy --jq '.mergedBy.login')
MERGED_AT=$(gh pr view --json mergedAt --jq '.mergedAt')

# Extract commit details
COMMIT_HASH=$(git log -1 --pretty=%H)
COMMIT_MSG=$(git log -1 --pretty=%s)
COMMIT_AUTHOR=$(git log -1 --pretty=%an)
COMMIT_DATE=$(git log -1 --date=iso8601 --pretty=%aI)

# Create comment body
COMMENT_BODY=$(cat <<EOF
## Pull Request Merged

**PR**: #$PR_NUMBER - $PR_TITLE
**URL**: $PR_URL
**Merged By**: @$MERGED_BY
**Merged At**: $MERGED_AT

### Status Update
✅ Ticket transitioned from **$CURRENT_STATUS** to **$TRANSITION_NAME**

### Merge Details
- **Commit**: \`$COMMIT_HASH\`
- **Author**: $COMMIT_AUTHOR
- **Date**: $COMMIT_DATE
- **Message**: $COMMIT_MSG

### Files Changed
\`\`\`
$(git diff --stat HEAD~1 HEAD)
\`\`\`

### Work Completed
The pull request has been successfully merged and the ticket has been closed.
EOF
)

# Add comment to JIRA ticket
atlassian_addCommentToJiraIssue \
  --cloudId "$CLOUD_ID" \
  --issueIdOrKey "$JIRA_TICKET" \
  --commentBody "$COMMENT_BODY"

if [ $? -eq 0 ]; then
  echo "✅ Added merge comment to $JIRA_TICKET"
else
  echo "⚠️  Failed to add comment to $JIRA_TICKET"
fi
```

### Step 7: Provide Summary

**Purpose**: Display clear summary of transition operation

```bash
echo ""
echo "=========================================="
echo "📊 JIRA Status Update Summary"
echo "=========================================="
echo ""

if [ "$STATUS" = "success" ]; then
  echo "✅ Status Update: SUCCESS"
  echo ""
  echo "🎫 Ticket: $JIRA_TICKET"
  echo "🔄 Transition: $CURRENT_STATUS → $TRANSITION_NAME"
  echo "👤 Transitioned By: $COMMIT_AUTHOR"
  echo "📅 Date: $COMMIT_DATE"
  echo ""
  echo "🔗 JIRA Ticket: https://<company>.atlassian.net/browse/$JIRA_TICKET"
  echo "🔗 PR: $PR_URL"
elif [ "$STATUS" = "permission_denied" ]; then
  echo "❌ Status Update: FAILED - Permission Denied"
  echo ""
  echo "⚠️  You don't have permission to transition this ticket"
  echo "🔗 JIRA Ticket: https://<company>.atlassian.net/browse/$JIRA_TICKET"
  echo ""
  echo "💡 Solution: Contact your JIRA administrator for permissions"
elif [ "$STATUS" = "invalid_transition" ]; then
  echo "❌ Status Update: FAILED - Invalid Transition"
  echo ""
  echo "⚠️  The selected transition is not available for this ticket"
  echo "🔗 JIRA Ticket: https://<company>.atlassian.net/browse/$JIRA_TICKET"
  echo ""
  echo "💡 Solution: Check available transitions and try a different status"
elif [ "$STATUS" = "invalid_ticket" ]; then
  echo "❌ Status Update: FAILED - Invalid Ticket"
  echo ""
  echo "⚠️  The JIRA ticket '$JIRA_TICKET' does not exist"
  echo ""
  echo "💡 Solution: Verify the ticket key is correct"
fi

echo "=========================================="
echo ""
```

## Integration with Other Skills

### Skills That Should Use jira-status-updater

- **pr-creation-workflow**: Update JIRA status after PR merge
- **git-pr-creator**: Optionally update JIRA status after PR merge
- **jira-git-workflow**: Document the complete workflow including status updates
- **nextjs-pr-workflow**: Update JIRA status after Next.js PR merge

### Integration Pattern

```bash
# In pr-creation-workflow or git-pr-creator
# After successful PR merge:

# Step 1: Check if JIRA integration is enabled
if [ "$ENABLE_JIRA_STATUS_UPDATE" = "true" ]; then

  # Step 2: Call jira-status-updater
  jira-status-updater \
    --ticket "$JIRA_TICKET" \
    --cloudId "$CLOUD_ID" \
    --target-status "Done"

  # Step 3: Check result
  if [ $? -eq 0 ]; then
    echo "✅ JIRA ticket status updated successfully"
  else
    echo "⚠️  JIRA ticket status update failed"
  fi
fi
```

## Best Practices

### Transition Detection

- **Dynamic Query**: Always query available transitions, don't hardcode status names
- **Status Category**: Use `statusCategory.key == "done"` to find any done-category status
- **Multiple Targets**: Support "Done", "Closed", and other final status names
- **Priority Order**: Prefer "Done" → "Closed" → Any done-category status

### Error Handling

- **Current Status Check**: Always check current status before transitioning
- **Graceful Failure**: Don't fail entire workflow if status update fails
- **Clear Messages**: Provide specific error messages for different failure modes
- **User Guidance**: Suggest next steps for common errors

### Documentation

- **Comment Addition**: Always add a merge comment for traceability
- **PR Details**: Include PR number, URL, and merge details in comments
- **Commit Info**: Add commit hash, author, and date for audit trail
- **Files Changed**: Include file statistics in merge comments

### Configuration

- **Enable/Disable**: Make JIRA status updates optional via configuration
- **Default Status**: Allow configuration of default target status
- **Cloud ID**: Support cloud ID configuration via environment variable
- **Fallback Behavior**: Continue workflow even if status update fails

## Common Issues

### No JIRA Ticket Reference Found

**Issue**: Cannot extract JIRA ticket key from PR or commits

**Solution**:
```bash
# Ask user to specify ticket
read -p "Enter JIRA ticket key (e.g., IBIS-101): " JIRA_TICKET

# Or skip status update
read -p "Skip JIRA status update? (y/n): " SKIP_UPDATE
if [ "$SKIP_UPDATE" = "y" ]; then
  echo "Skipping JIRA status update"
fi
```

### Transition Not Available

**Issue**: Target status transition not available for ticket

**Solution**:
```bash
# List available transitions
echo "Available transitions:"
echo "$TRANSITIONS" | jq -r '.transitions[] | "- \(.name)"'

# Ask user to select
read -p "Select transition (or skip): " USER_TRANSITION

if [ -n "$USER_TRANSITION" ]; then
  TRANSITION_ID=$(echo "$TRANSITIONS" | jq -r ".transitions[] | select(.name == \"$USER_TRANSITION\") | .id")
else
  echo "Skipping status update"
fi
```

### Permission Denied

**Issue**: User lacks permission to transition ticket status

**Solution**:
```bash
# Provide clear error message
echo "❌ Permission denied: You don't have permission to transition this ticket"
echo ""
echo "🔗 JIRA Ticket: https://<company>.atlassian.net/browse/$JIRA_TICKET"
echo ""
echo "💡 Next steps:"
echo "   1. Contact your JIRA administrator"
echo "   2. Request transition permissions for this project"
echo "   3. Manually update ticket status in JIRA"
```

### Ticket Already Done

**Issue**: Ticket is already in target status

**Solution**:
```bash
# Skip transition but add comment
if [ "$CURRENT_STATUS" = "$TRANSITION_NAME" ]; then
  echo "✅ Ticket already in target status: $TRANSITION_NAME"
  echo "Adding merge comment only..."
  # Add merge comment without transitioning
fi
```

### Cloud ID Not Configured

**Issue**: ATLASSIAN_CLOUD_ID environment variable not set

**Solution**:
```bash
# Try to auto-detect
if [ -z "$ATLASSIAN_CLOUD_ID" ]; then
  echo "Detecting cloud ID..."
  CLOUD_ID=$(atlassian_getAccessibleAtlassianResources | jq -r '.[0].id')
  export ATLASSIAN_CLOUD_ID="$CLOUD_ID"
  echo "✅ Detected cloud ID: $ATLASSIAN_CLOUD_ID"
fi

# Or ask user
if [ -z "$ATLASSIAN_CLOUD_ID" ]; then
  read -p "Enter Atlassian cloud ID: " CLOUD_ID
  export ATLASSIAN_CLOUD_ID="$CLOUD_ID"
fi
```

## Troubleshooting Checklist

Before updating JIRA status:
- [ ] JIRA ticket key is valid (e.g., IBIS-101)
- [ ] Atlassian cloud ID is configured
- [ ] Atlassian MCP tools are available
- [ ] User has permission to transition tickets
- [ ] Current status is not already target status

After updating JIRA status:
- [ ] Status transition was successful
- [ ] Merge comment was added to ticket
- [ ] Ticket URL is accessible
- [ ] Summary is displayed to user

## Examples

### Example 1: Successful Status Update

**Scenario**: PR for IBIS-101 is merged, ticket transitions from "In Progress" to "Done"

**Output**:
```
✅ Detected JIRA ticket: IBIS-101
Available transitions for IBIS-101:
- In Review → In Review
- Done → Done
- Cancel → Cancelled

Current status: In Progress
Target status: Done

Transitioning IBIS-101 from In Progress to Done...
✅ Successfully transitioned IBIS-101 to Done
✅ Added merge comment to IBIS-101

==========================================
📊 JIRA Status Update Summary
==========================================

✅ Status Update: SUCCESS

🎫 Ticket: IBIS-101
🔄 Transition: In Progress → Done
👤 Transitioned By: John Doe
📅 Date: 2024-01-26T21:30:00+08:00

🔗 JIRA Ticket: https://company.atlassian.net/browse/IBIS-101
🔗 PR: https://github.com/org/repo/pull/42
==========================================
```

### Example 2: Ticket Already Done

**Scenario**: PR for IBIS-102 is merged, but ticket is already in "Done" status

**Output**:
```
✅ Detected JIRA ticket: IBIS-102
Current status: Done
Target status: Done

✅ Ticket already in target status: Done
No transition needed
✅ Added merge comment to IBIS-102

==========================================
📊 JIRA Status Update Summary
==========================================

✅ Status Update: SUCCESS (No Transition Needed)

🎫 Ticket: IBIS-102
🔄 Transition: Done → Done (Skipped - Already Done)
👤 By: John Doe
📅 Date: 2024-01-26T21:30:00+08:00

🔗 JIRA Ticket: https://company.atlassian.net/browse/IBIS-102
🔗 PR: https://github.com/org/repo/pull/43
==========================================
```

### Example 3: Permission Denied

**Scenario**: User lacks permission to transition IBIS-103

**Output**:
```
✅ Detected JIRA ticket: IBIS-103
Available transitions for IBIS-103:
- In Review → In Review

Current status: In Progress
Target status: Done
⚠️  No 'Done' or 'Closed' transition available for IBIS-103

❌ Status Update: FAILED - Invalid Transition

⚠️  The selected transition is not available for this ticket
🔗 JIRA Ticket: https://company.atlassian.net/browse/IBIS-103

💡 Solution: Check available transitions and try a different status
==========================================
```

## Related Skills

- **JIRA Integration**:
  - `jira-git-integration` - Provides JIRA utilities and API tools
- **Git Frameworks**:
  - `pr-creation-workflow` - PR creation framework (uses jira-status-updater)
  - `git-pr-creator` - PR creation with JIRA (uses jira-status-updater)
  - `git-issue-updater` - Adds progress comments to JIRA
- **JIRA Workflows**:
  - `jira-git-workflow` - Complete JIRA ticket creation and branching workflow

## References

- [Atlassian JIRA API - Issue Transitions](https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issues/#transition-issue)
- [Atlassian JIRA API - Get Transitions](https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issues/#get-transitions)
- [JIRA Workflow Configuration](https://confluence.atlassian.com/adminjiracloud/configuring-workflow-9458355.html)
