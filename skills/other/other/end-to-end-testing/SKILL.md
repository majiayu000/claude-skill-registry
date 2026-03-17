---
name: end-to-end-testing
description: End-to-end testing workflow for gh-pr-linear-issue-linker. Tests GitHub webhook integration with Linear ticket matching and Slack notifications.
---

# End-to-End Testing Workflow

## Overview

This skill runs a complete end-to-end test of the gh-pr-linear-issue-linker service by:

1. Creating a test branch in the test repository
2. Finding an in-progress Linear ticket
3. Creating a dummy file change related to the ticket
4. Creating a pull request to trigger the webhook
5. Verifying Slack notifications in #pull-requests-agent
6. Interacting with the Gupri bot in the Slack thread

## Test Repository

- **Repository**: https://github.com/Deway-AI/test-hook/
- **Target Branch**: `main`
- **Slack Channel**: #pull-requests-agent (ID: C0AE54YFY5T)

## Prerequisites

Before running E2E tests:

1. **GitHub CLI (`gh`)** must be authenticated:
   ```bash
   gh auth status
   ```

2. **Linear MCP** must be configured with valid API key

3. **Slack MCP** must be configured with bot token and permissions

4. **Service must be deployed** and receiving webhooks:
   ```bash
   # Check service is running
   gcloud run services describe gh-pr-linear-issue-linker \
     --region=us-central1 \
     --format="value(status.url)"
   ```

## E2E Test Workflow

### Step 1: Create Test Branch

```bash
# Generate unique branch name with timestamp
BRANCH_NAME="e2e-test-$(date +%s)"

# Create branch in test repository
gh api repos/Deway-AI/test-hook/git/refs/heads/main | \
  jq -r '.object.sha' | \
  xargs -I {} gh api \
    --method POST \
    repos/Deway-AI/test-hook/git/refs \
    -f ref="refs/heads/$BRANCH_NAME" \
    -f sha={}

echo "Created branch: $BRANCH_NAME"
```

### Step 2: Find Linear Ticket

Use Linear MCP to find an in-progress ticket:

```bash
# Query for in-progress tickets
# Use mcp__linear__list_issues with state filter
```

Expected output: Linear ticket identifier (e.g., `ENG-456`)

### Step 3: Create Dummy File Change

Create a dummy implementation file related to the Linear ticket:

```bash
# Get ticket details to generate relevant filename
TICKET_ID="ENG-456"
FILE_PATH="src/features/${TICKET_ID,,}_implementation.py"

# Create file content
FILE_CONTENT=$(cat <<EOF
"""
Implementation for ${TICKET_ID}

This is a dummy file created for E2E testing.
"""

def placeholder_function():
    """Placeholder function for testing."""
    pass
EOF
)

# Base64 encode content
ENCODED_CONTENT=$(echo "$FILE_CONTENT" | base64)

# Create file via GitHub API
gh api \
  --method PUT \
  repos/Deway-AI/test-hook/contents/"$FILE_PATH" \
  -f message="Add implementation for $TICKET_ID" \
  -f content="$ENCODED_CONTENT" \
  -f branch="$BRANCH_NAME"
```

### Step 4: Create Pull Request

```bash
# Create PR with ticket reference in title
PR_TITLE="[$TICKET_ID] E2E Test - $(date +%Y-%m-%d)"
PR_BODY="This is an automated E2E test for the gh-pr-linear-issue-linker service.

Related Linear ticket: $TICKET_ID

**Test Details:**
- Branch: $BRANCH_NAME
- Created: $(date -u +%Y-%m-%dT%H:%M:%SZ)
- Purpose: Verify webhook integration, ticket matching, and Slack notifications

This PR will be closed automatically after testing."

# Create PR and capture PR number
PR_NUMBER=$(gh pr create \
  --repo Deway-AI/test-hook \
  --base main \
  --head "$BRANCH_NAME" \
  --title "$PR_TITLE" \
  --body "$PR_BODY" \
  --json number \
  --jq '.number')

echo "Created PR #$PR_NUMBER"
```

### Step 5: Monitor Slack Notifications

Wait for webhook processing and verify Slack message:

```bash
# Wait for webhook processing (typically < 5 seconds)
sleep 10

# Use Slack MCP to get recent messages in #pull-requests-agent
# Filter for messages from our PR
```

**Expected Slack message structure:**
```
🔍  Gupri matched a ticket
test-hook | PR #{PR_NUMBER} | by @{github-user}
{PR_TITLE}

Matched 1 ticket: {TICKET_ID}
```

### Step 6: Interact with Gupri Bot

Post a test message mentioning the Gupri bot:

```bash
# Get thread_ts from parent message
THREAD_TS="1234567890.123456"

# Post reply mentioning Gupri bot
# Note: Gupri bot Slack user ID may need to be resolved
MESSAGE="<@GUPRI_BOT_ID> This is an E2E test - verifying bot interaction"

# Use Slack MCP to post thread reply
```

Expected: Bot should respond or acknowledge the mention

### Step 7: Cleanup

```bash
# Close PR
gh pr close "$PR_NUMBER" \
  --repo Deway-AI/test-hook \
  --comment "E2E test completed - closing test PR"

# Delete test branch
gh api \
  --method DELETE \
  repos/Deway-AI/test-hook/git/refs/heads/"$BRANCH_NAME"

echo "Cleanup complete"
```

## Verification Checklist

After running E2E test, verify:

- [x] Test branch created successfully
- [x] Linear ticket found with "In Progress" state
- [x] Dummy file created with ticket reference
- [x] PR created with ticket in title
- [x] Webhook triggered (check Cloud Logging)
- [x] Slack message posted to #pull-requests-agent
- [x] Slack message contains correct PR details
- [x] Slack message matches expected ticket
- [x] Thread reply posted successfully
- [x] Gupri bot mentioned correctly
- [x] PR closed and branch deleted

## Debugging E2E Failures

### Webhook Not Triggered

Check GitHub webhook deliveries:
```bash
# View webhook deliveries for test-hook repository
gh api repos/Deway-AI/test-hook/hooks | \
  jq -r '.[].id' | \
  xargs -I {} gh api repos/Deway-AI/test-hook/hooks/{}/deliveries | \
  jq '.[] | select(.status_code != 200)'
```

Check Cloud Logging:
```bash
gcloud logging read "resource.type=cloud_run_revision AND textPayload=~'webhook'" \
  --limit=20 \
  --format=json
```

### Ticket Matching Failed

Check Logfire for ticket matcher traces:
1. Find trace for the PR webhook event
2. Review `match_linear_tickets` span
3. Check GraphQL query and results

Verify Linear ticket state:
```bash
# Use Linear MCP to verify ticket is "In Progress"
```

### Slack Notification Not Posted

Check Cloud Logging for Slack API errors:
```bash
gcloud logging read "resource.type=cloud_run_revision AND severity>=ERROR AND textPayload=~'slack'" \
  --limit=20
```

Verify Slack channel permissions:
- Bot must be a member of #pull-requests-agent
- Bot must have `chat:write` and `chat:write.public` scopes

### Thread Reply Failed

Verify `thread_ts` was stored in Firestore:
```bash
# Check Firestore PR state collection
# Use gcloud firestore to query PR state
```

## Error Recovery

If E2E test fails partway through:

1. **Manual PR Cleanup**:
   ```bash
   # List open PRs in test-hook
   gh pr list --repo Deway-AI/test-hook --author "@me"

   # Close specific PR
   gh pr close <PR_NUMBER> --repo Deway-AI/test-hook
   ```

2. **Manual Branch Cleanup**:
   ```bash
   # List branches matching pattern
   gh api repos/Deway-AI/test-hook/git/refs/heads | \
     jq -r '.[] | select(.ref | contains("e2e-test")) | .ref'

   # Delete specific branch
   gh api --method DELETE repos/Deway-AI/test-hook/git/refs/heads/e2e-test-XXXXXX
   ```

3. **Slack Message Cleanup**:
   - Manually delete test messages in #pull-requests-agent
   - Or leave them as historical test records

## Automation Script

For convenience, use the provided script:

```bash
./scripts/e2e-test.sh
```

This script automates steps 1-7 and provides detailed output at each stage.

## Success Criteria

E2E test is considered successful when:

1. ✅ PR created in test-hook repository
2. ✅ Webhook received by Cloud Run service (200 status)
3. ✅ Linear ticket matched correctly
4. ✅ Slack message posted to #pull-requests-agent channel
5. ✅ Slack message contains expected PR and ticket details
6. ✅ Thread reply with Gupri bot mention posted successfully
7. ✅ No errors in Cloud Logging
8. ✅ Cleanup completed (PR closed, branch deleted)

## Running E2E Tests Regularly

**Recommended frequency**: Before major releases or after significant changes to:
- Webhook handler logic
- Linear ticket matching
- Slack notification formatting
- GitHub App permissions
- Cloud Run configuration

**When to skip E2E tests**:
- Pure infrastructure changes (Terraform only)
- Documentation updates
- Minor configuration tweaks
- Unit test additions (without code changes)

## Related Skills

- `gcp-debugging` - For investigating webhook delivery and Cloud Run logs
- `deployment-workflow` - For deploying service changes before E2E testing
- `slack-messaging` - For understanding Slack notification format expectations
