---
name: git-issue-updater
description: Update GitHub issues and JIRA tickets with commit progress including user, date, time, and consistent documentation formatting for traceability
license: Apache-2.0
compatibility: opencode
metadata:
  audience: developers, maintainers
  workflow: issue-tracking
---

## What I do

I provide automatic issue progress updates for both GitHub and JIRA after commits are made:

1. **Extract Commit Details**: Get latest commit info: hash, message, author, date, time, files changed
2. **Determine Issue Reference**: Extract GitHub issue number (#123) or JIRA ticket key (PROJECT-123) from commit message
3. **Format Update Comment**: Create consistent documentation with user, date, time, changes summary
4. **Support Multiple Platforms**: Add comments to GitHub issues or JIRA tickets
5. **Include Metadata**: Add commit link (GitHub) or hash (JIRA), user info, timestamp
6. **Handle Incremental Updates**: Support multiple commits with cumulative or per-commit updates
7. **Verify Updates**: Confirm comment was successfully added to issue/ticket

## When to use me

Use this framework when:
- You need to track commit progress in GitHub issues or JIRA tickets
- You've made commits and want to update the associated issue/ticket
- You want consistent documentation of progress with timestamps and user info
- You're creating a workflow that makes commits and should update issues
- You need traceability between commits and issues
- You want to maintain consistency in issue/ticket comments
- You're working with teams that require progress updates in issues

This is a **framework skill** - it provides issue update functionality that other skills use.

## Core Workflow Steps

### Step 1: Extract Latest Commit Information

**Purpose**: Get all relevant details from the most recent commit

**Git Commands for Commit Info**:
```bash
# Get latest commit hash
COMMIT_HASH=$(git rev-parse HEAD)

# Get commit message (subject and body)
COMMIT_MSG=$(git log -1 --pretty=%B)

# Get commit author
COMMIT_AUTHOR=$(git log -1 --pretty=%an)

# Get commit author email
COMMIT_EMAIL=$(git log -1 --pretty=%ae)

# Get commit date and time in ISO 8601 format
COMMIT_DATE=$(git log -1 --date=iso8601 --pretty=%aI)

# Get commit date in human-readable format
COMMIT_DATE_HUMAN=$(git log -1 --date=short --pretty=%aI)

# Get commit time (24-hour format with timezone)
COMMIT_TIME=$(git log -1 --date=format:%H:%M%z --pretty=%aI)

# Get list of changed files
CHANGED_FILES=$(git show --name-only --pretty=format: HEAD | grep -v "^$")

# Get file change statistics
FILE_STATS=$(git diff --stat HEAD~1 HEAD)
```

**Expected Output Example**:
```
COMMIT_HASH: "5f3a2b1c4d5e6f7"
COMMIT_MSG: "feat(auth): add OAuth2 support"
COMMIT_AUTHOR: "John Doe"
COMMIT_EMAIL: "john.doe@example.com"
COMMIT_DATE: "2024-01-25T14:30:45+08:00"
COMMIT_DATE_HUMAN: "2024-01-25"
COMMIT_TIME: "14:30+0800"
CHANGED_FILES: "src/auth/oauth.ts
src/auth/token.ts
src/api/auth.ts"
```

### Step 2: Determine Issue Reference

**Purpose**: Extract GitHub issue number or JIRA ticket key from commit message

**GitHub Issue Detection**:
```bash
# Extract issue number from commit message (format: #123)
ISSUE_NUM=$(echo "$COMMIT_MSG" | grep -oE '#[0-9]+' | head -1 | sed 's/#//')

if [ -n "$ISSUE_NUM" ]; then
  ISSUE_TYPE="github"
  ISSUE_REF="#$ISSUE_NUM"
  ISSUE_URL="https://github.com/$REPO_OWNER/$REPO_NAME/issues/$ISSUE_NUM"
fi
```

**JIRA Ticket Detection**:
```bash
# Extract JIRA ticket key from commit message (format: PROJECT-123)
TICKET_KEY=$(echo "$COMMIT_MSG" | grep -oE '[A-Z]+-[0-9]+' | head -1)

if [ -n "$TICKET_KEY" ]; then
  ISSUE_TYPE="jira"
  ISSUE_REF="$TICKET_KEY"
  TICKET_URL="https://company.atlassian.net/browse/$TICKET_KEY"
fi
```

**Combined Detection Logic**:
```bash
# Try GitHub first
ISSUE_NUM=$(echo "$COMMIT_MSG" | grep -oE '#[0-9]+' | head -1 | sed 's/#//')

# If no GitHub issue, try JIRA
if [ -z "$ISSUE_NUM" ]; then
  TICKET_KEY=$(echo "$COMMIT_MSG" | grep -oE '[A-Z]+-[0-9]+' | head -1)
  
  if [ -n "$TICKET_KEY" ]; then
    ISSUE_TYPE="jira"
    ISSUE_REF="$TICKET_KEY"
  fi
else
  ISSUE_TYPE="github"
  ISSUE_REF="#$ISSUE_NUM"
fi

# If neither found, ask user or use branch name
if [ -z "$ISSUE_TYPE" ]; then
  BRANCH_NAME=$(git branch --show-current)
  
  # Check if branch name contains issue reference
  if echo "$BRANCH_NAME" | grep -qE '^[0-9]+$'; then
    ISSUE_TYPE="github"
    ISSUE_REF="#$BRANCH_NAME"
  elif echo "$BRANCH_NAME" | grep -qE '[A-Z]+-[0-9]+$'; then
    ISSUE_TYPE="jira"
    ISSUE_REF="$BRANCH_NAME"
  else
    echo "⚠️  No issue reference found in commit message or branch name"
    echo "   Please manually specify issue to update"
    read -p "Enter issue/ticket reference: " ISSUE_REF
  fi
fi

echo "Detected issue type: $ISSUE_TYPE"
echo "Issue reference: $ISSUE_REF"
```

### Step 3: Format Update Comment

**Purpose**: Create a consistent, well-formatted progress update

**Comment Template**:
```markdown
## Progress Update - <Date> at <Time>

**Commit**: `<commit-hash>`
**Author**: `<user>` (<email>)
**Commit Message**: `<commit-message>`

### Changes Made
- [ ] <file1> - <brief description>
- [ ] <file2> - <brief description>
- [ ] <file3> - <brief description>

### Statistics
- Files changed: <count>
- Lines added: <+count>
- Lines removed: <-count>

### Commit Link
<platform-specific-link>

### Files Changed
```

**Filled Example**:
```markdown
## Progress Update - 2024-01-25 at 14:30 (UTC+08:00)

**Commit**: `5f3a2b1c4d5e6f7`
**Author**: John Doe (john.doe@example.com)
**Commit Message**: feat(auth): add OAuth2 support for third-party providers

### Changes Made
- [x] `src/auth/oauth.ts` - Implement OAuth2 authentication flow
- [x] `src/auth/token.ts` - Add token refresh mechanism
- [x] `src/api/auth.ts` - Update API endpoints for OAuth

### Statistics
- Files changed: 3
- Lines added: +245
- Lines removed: -12

### Commit Link
[View on GitHub](https://github.com/org/repo/commit/5f3a2b1c4d5e6f7)

### Files Changed
- `src/auth/oauth.ts` (+150 lines)
- `src/auth/token.ts` (+95 lines)
- `src/api/auth.ts` (-12 lines, +12 lines)
```

**JIRA Comment Template**:
```markdown
## Progress Update

**Commit**: `5f3a2b1c4d5e6f7`
**Date**: 2024-01-25 14:30 UTC+08:00
**Author**: John Doe (john.doe@example.com)

### Work Completed
- [x] Implement OAuth2 authentication flow
- [x] Add token refresh mechanism
- [x] Update API endpoints

### Files Changed
- `src/auth/oauth.ts`
- `src/auth/token.ts`
- `src/api/auth.ts`

### Statistics
Files changed: 3
Lines added: +245
Lines removed: -12

### Next Steps
1. Add error handling for OAuth failures
2. Write integration tests
3. Update documentation
```

### Step 4: Update GitHub Issue

**Purpose**: Add progress comment to GitHub issue

**GitHub CLI Command**:
```bash
# Get repository info
REPO_OWNER=$(gh repo view --json ownerLogin --jq '.ownerLogin')
REPO_NAME=$(gh repo view --json name --jq '.name')

# Construct commit URL
COMMIT_URL="https://github.com/${REPO_OWNER}/${REPO_NAME}/commit/${COMMIT_HASH}"

# Add comment to GitHub issue
gh issue comment "$ISSUE_NUM" --body "$COMMENT_BODY"

echo "✅ Comment added to GitHub issue #$ISSUE_NUM"
```

**GitHub Comment Script**:
```bash
#!/bin/bash
# update-github-issue.sh

# Extract commit info
COMMIT_HASH=$(git rev-parse HEAD)
COMMIT_MSG=$(git log -1 --pretty=%s)
COMMIT_AUTHOR=$(git log -1 --pretty=%an)
COMMIT_EMAIL=$(git log -1 --pretty=%ae)
COMMIT_DATE=$(git log -1 --date=short --pretty=%aI)
COMMIT_TIME=$(git log -1 --date=format:%H:%M --pretty=%aI)

# Extract issue number
ISSUE_NUM=$(echo "$COMMIT_MSG" | grep -oE '#[0-9]+' | head -1 | sed 's/#//')

if [ -z "$ISSUE_NUM" ]; then
  echo "❌ No GitHub issue number found in commit message"
  exit 1
fi

# Get repository info
REPO_OWNER=$(gh repo view --json ownerLogin --jq '.ownerLogin')
REPO_NAME=$(gh repo view --json name --jq '.name')
COMMIT_URL="https://github.com/${REPO_OWNER}/${REPO_NAME}/commit/${COMMIT_HASH}"

# Get file statistics
FILE_STATS=$(git diff --stat HEAD~1 HEAD)

# Create comment body
COMMENT_BODY=$(cat <<EOF
## Progress Update - ${COMMIT_DATE} at ${COMMIT_TIME}

**Commit**: \`$COMMIT_HASH\`
**Author**: $COMMIT_AUTHOR ($COMMIT_EMAIL)
**Commit Message**: $COMMIT_MSG

### Files Changed
\`\`\`
$FILE_STATS
\`\`\`

### Commit Link
[View on GitHub]($COMMIT_URL)

### File List
$(git show --name-only --pretty=format: HEAD | grep -v "^$" | sed 's/^/- /')
EOF
)

# Add comment to issue
gh issue comment "$ISSUE_NUM" --body "$COMMENT_BODY"

if [ $? -eq 0 ]; then
  echo "✅ Successfully updated GitHub issue #$ISSUE_NUM"
  echo "   Comment URL: https://github.com/${REPO_OWNER}/${REPO_NAME}/issues/${ISSUE_NUM}"
else
  echo "❌ Failed to update GitHub issue"
  exit 1
fi
```

### Step 5: Update JIRA Ticket

**Purpose**: Add progress comment to JIRA ticket

**JIRA API Command**:
```bash
# Cloud ID (get from environment or use default)
CLOUD_ID="${ATLASSIAN_CLOUD_ID:-<your-cloud-id>}"

# Ticket key (extracted from commit message)
TICKET_KEY="$ISSUE_REF"

# Add comment to JIRA ticket
atlassian_addCommentToJiraIssue \
  --cloudId "$CLOUD_ID" \
  --issueIdOrKey "$TICKET_KEY" \
  --commentBody "$COMMENT_BODY"

echo "✅ Comment added to JIRA ticket $TICKET_KEY"
```

**JIRA Comment Script**:
```bash
#!/bin/bash
# update-jira-ticket.sh

# Extract commit info
COMMIT_HASH=$(git rev-parse HEAD)
COMMIT_MSG=$(git log -1 --pretty=%s)
COMMIT_AUTHOR=$(git log -1 --pretty=%an)
COMMIT_EMAIL=$(git log -1 --pretty=%ae)
COMMIT_DATE=$(git log -1 --date=short --pretty=%aI)
COMMIT_TIME=$(git log -1 --date=format:%H:%M --pretty=%aI)

# Extract ticket key
TICKET_KEY=$(echo "$COMMIT_MSG" | grep -oE '[A-Z]+-[0-9]+' | head -1)

if [ -z "$TICKET_KEY" ]; then
  echo "❌ No JIRA ticket key found in commit message"
  exit 1
fi

# Get file statistics
FILE_STATS=$(git diff --stat HEAD~1 HEAD)

# Cloud ID
CLOUD_ID="${ATLASSIAN_CLOUD_ID:-<your-cloud-id>}"

# Create comment body
COMMENT_BODY=$(cat <<EOF
## Progress Update

**Commit**: \`$COMMIT_HASH\`
**Date**: $COMMIT_DATE $COMMIT_TIME UTC
**Author**: $COMMIT_AUTHOR ($COMMIT_EMAIL)

### Work Completed
$COMMIT_MSG

### Files Changed
\`\`\`
$FILE_STATS
\`\`\`

### File List
$(git show --name-only --pretty=format: HEAD | grep -v "^$" | sed 's/^/- /')

### Commit Details
- **Branch**: $(git branch --show-current)
- **Repository**: $(git remote get-url origin)
- **Timestamp**: $COMMIT_DATE $COMMIT_TIME
EOF
)

# Add comment to JIRA ticket
atlassian_addCommentToJiraIssue \
  --cloudId "$CLOUD_ID" \
  --issueIdOrKey "$TICKET_KEY" \
  --commentBody "$COMMENT_BODY"

if [ $? -eq 0 ]; then
  echo "✅ Successfully updated JIRA ticket $TICKET_KEY"
  echo "   Ticket URL: https://company.atlassian.net/browse/$TICKET_KEY"
else
  echo "❌ Failed to update JIRA ticket"
  exit 1
fi
```

### Step 6: Handle Incremental Updates

**Purpose**: Support multiple commits with appropriate update strategy

**Update Strategies**:

**Strategy 1: Per-Commit Updates**
```bash
# Each commit gets its own comment
# Use after each commit
git-commit-update  # Calls the appropriate update script
```

**Strategy 2: Cumulative Updates**
```bash
# Combine multiple commits into one update
# Use at the end of a session or before PR
git-session-update
```

**Strategy 3: Checkpoint Updates**
```bash
# Update at specific milestones (e.g., after completing a phase)
# Use manual triggers or CI/CD milestones
git-checkpoint-update
```

**Incremental Update Example**:
```markdown
## Progress Update #2 - 2024-01-25 at 16:45

Since the last update, the following work has been completed:

### Commits Made
1. **feat(auth): add OAuth2 support** (14:30)
2. **fix(auth): handle token refresh errors** (15:15)
3. **test(auth): add OAuth integration tests** (16:30)

### Files Changed
- `src/auth/oauth.ts` (+245 lines)
- `src/auth/token.ts` (+150 lines, -50 lines)
- `src/api/auth.ts` (+95 lines, -12 lines)
- `src/auth/__tests__/oauth.test.ts` (+180 lines)

### Total Statistics
- Commits: 3
- Files changed: 4
- Total lines added: +670
- Total lines removed: -62

### Next Steps
- [ ] Update documentation for OAuth flow
- [ ] Code review
- [ ] Create pull request
```

### Step 7: Verify Update

**Purpose**: Confirm comment was successfully added

**GitHub Verification**:
```bash
# List recent comments on issue
gh issue view "$ISSUE_NUM" --json comments --jq '.comments | length'

# View last comment
gh issue view "$ISSUE_NUM" --json comments --jq '.comments[-1]'

# Verify comment content contains commit hash
gh issue view "$ISSUE_NUM" --json comments --jq \
  '.comments[] | select(.body | contains("$COMMIT_HASH")) | length'
```

**JIRA Verification**:
```bash
# Get issue details including comments
atlassian_getJiraIssue \
  --cloudId "$CLOUD_ID" \
  --issueIdOrKey "$TICKET_KEY" \
  --expand comments

# Check if comment was added
# Verify the last comment matches the commit hash
```

## Comment Format Standards

### Required Fields

Every issue update must include:

| Field | Description | Example |
|--------|-------------|----------|
| Date | ISO 8601 or readable format | 2024-01-25 |
| Time | 24-hour format with timezone | 14:30 (UTC+08:00) |
| User | Commit author name | John Doe |
| Email | Author email (optional) | john.doe@example.com |
| Commit Hash | Full SHA or short SHA | 5f3a2b1c4d5e6f7 |
| Commit Message | Subject line or full message | feat(auth): add OAuth2 |
| Files Changed | List of modified files | src/auth/oauth.ts |
| Statistics | Files changed, +lines, -lines | Files: 3, +245, -12 |

### Date and Time Formats

**ISO 8601 Format (Recommended)**:
```
2024-01-25T14:30:45+08:00
```

**Human-Readable Format**:
```
2024-01-25 at 14:30 (UTC+08:00)
```

**Timezone Handling**:
- Use consistent timezone (UTC is recommended)
- Include timezone offset for clarity
- Consider team's primary timezone for consistency

### Formatting Examples

**GitHub Issue Update**:
```markdown
## Progress Update - 2024-01-25 at 14:30 UTC

**Commit**: [`5f3a2b1c`](https://github.com/org/repo/commit/5f3a2b1c)
**Author**: John Doe (john.doe@example.com)
**Commit Message**: feat(auth): add OAuth2 support

### Changes
- [x] Implement OAuth2 authentication flow
- [x] Add token refresh mechanism
- [x] Update API endpoints

### Files Changed
\`\`\`
src/auth/oauth.ts    | 150 +++++++++++
src/auth/token.ts    |  95 ++++++++
src/api/auth.ts      | -12 ---

3 files changed, 245 insertions(+), 12 deletions(-)
\`\`\`
```

**JIRA Ticket Update**:
```markdown
## Progress Update

**Commit**: \`5f3a2b1c4d5e6f7\`
**Date**: 2024-01-25 14:30 UTC
**Author**: John Doe (john.doe@example.com)

### Work Completed
feat(auth): add OAuth2 support for third-party providers

### Details
Implemented OAuth2 authentication flow with support for Google and GitHub.
Added token refresh mechanism and error handling for expired tokens.

### Files Changed
- src/auth/oauth.ts
- src/auth/token.ts
- src/api/auth.ts

### Commit Link
View commit in repository

### Next Steps
- Add unit tests
- Update documentation
- Code review
```

## Integration with Other Skills

### Skills That Should Use git-issue-updater

- **git-issue-creator**: Update issue after creating PLAN.md commit
- **ticket-branch-workflow**: Update ticket after creating PLAN.md commit
- **jira-git-workflow**: Update JIRA ticket after creating PLAN.md commit
- **git-pr-creator**: Update issue when PR is created/merged
- **nextjs-pr-workflow**: Update issue when Next.js PR is ready
- **pr-creation-workflow**: Update linked issues after PR creation

### Integration Pattern

```bash
# After making a commit
git add .
git commit -m "feat(api): add user registration"

# Update issue with commit details
git-issue-updater --platform github --issue #123

# Or for JIRA
git-issue-updater --platform jira --ticket IBIS-101
```

### Workflow Integration Example

**git-issue-creator Workflow**:
1. Create GitHub issue
2. Create branch
3. Create PLAN.md
4. Commit PLAN.md → **CALL git-issue-updater**
5. Push branch

**ticket-branch-workflow Workflow**:
1. Identify JIRA project
2. Create JIRA ticket
3. Create branch
4. Create PLAN.md
5. Commit PLAN.md → **CALL git-issue-updater**
6. Push branch

## Best Practices

### Update Timing

- **Immediate updates**: Update immediately after each commit
- **Batch updates**: Combine multiple commits into one update (end of session)
- **Checkpoint updates**: Update at specific milestones (feature completion, bug fix)
- **PR updates**: Update when creating or merging PR

### User Information

- Always include commit author name
- Include email if needed for attribution
- Use consistent user format across all updates
- Handle co-authored commits appropriately

### Date and Time

- Use ISO 8601 format for machine readability
- Include timezone for clarity
- Be consistent with timezone across team
- Consider using UTC as standard timezone

### Content Quality

- Provide clear summary of changes
- Include file statistics when relevant
- Link to commits for reference
- Keep updates concise but informative
- Use markdown formatting for readability

### Consistency

- Use consistent comment templates
- Maintain standard field order
- Use consistent date/time format
- Keep formatting aligned with team conventions

## Common Issues

### Issue Reference Not Found

**Issue**: Commit message doesn't contain issue number/ticket key

**Solution**:
```bash
# Ask user to specify issue
echo "No issue reference found in commit message"
read -p "Enter issue/ticket reference: " ISSUE_REF

# Use branch name as fallback
BRANCH_NAME=$(git branch --show-current)
echo "Using branch name: $BRANCH_NAME"
```

### Comment Add Fails

**Issue**: Unable to add comment to issue/ticket

**GitHub Solution**:
```bash
# Verify GitHub CLI authentication
gh auth status

# Check issue exists
gh issue view "$ISSUE_NUM"

# Verify write permissions
gh auth refresh
```

**JIRA Solution**:
```bash
# Verify Atlassian MCP tools are available
# Check cloud ID is set
echo $ATLASSIAN_CLOUD_ID

# Verify ticket exists
atlassian_getJiraIssue --cloudId "$CLOUD_ID" --issueIdOrKey "$TICKET_KEY"
```

### Duplicate Updates

**Issue**: Multiple commits creating duplicate comments

**Solution**:
```bash
# Implement batching strategy
# Track updates in session file
SESSION_FILE=".git-issue-updater-session"

# Add commit to session
echo "$COMMIT_HASH,$COMMIT_DATE,$COMMIT_MSG" >> "$SESSION_FILE"

# Update with cumulative comment at end
if [ "$UPDATE_STRATEGY" = "batch" ]; then
  git-issue-updater --batch "$SESSION_FILE"
  rm "$SESSION_FILE"
fi
```

### Timezone Issues

**Issue**: Inconsistent timezone handling across team

**Solution**:
```bash
# Use UTC as standard timezone
export GIT_TZ="UTC"

# Or store timezone in git config
git config issue-updater.timezone "UTC"

# Use in comments
COMMIT_TIME=$(git log -1 --date=format:%H:%M --pretty=%aI)
```

## Automation Options

### Git Commit Hook

**Automatically update issue after commit**:
```bash
#!/bin/bash
# .git/hooks/post-commit

# Extract commit info
COMMIT_HASH=$(git rev-parse HEAD)
COMMIT_MSG=$(git log -1 --pretty=%B)

# Extract issue reference
ISSUE_REF=$(echo "$COMMIT_MSG" | grep -oE '#[0-9]+|[A-Z]+-[0-9]+' | head -1)

# Update issue if reference found
if [ -n "$ISSUE_REF" ]; then
  # Call update script in background to not block commit
  git-issue-updater "$ISSUE_REF" &
fi
```

### CI/CD Integration

**Update issues in CI pipeline**:
```yaml
# .github/workflows/update-issue.yml
name: Update Issue on Commit

on:
  push:
    branches: [main, develop]

jobs:
  update-issue:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Extract issue reference
        id: extract
        run: |
          MSG=$(git log -1 --pretty=%s)
          REF=$(echo "$MSG" | grep -oE '#[0-9]+|[A-Z]+-[0-9]+' | head -1)
          echo "ref=$REF" >> $GITHUB_OUTPUT
          
      - name: Update GitHub issue
        if: steps.extract.outputs.ref != ''
        uses: peter-evans/create-or-update-comment@v2
        with:
          issue-number: ${{ steps.extract.outputs.ref }}
          body: |
            ## Progress Update
            **Commit**: ${{ github.sha }}
            **Date**: ${{ github.event.head_commit.timestamp }}
            **Author**: ${{ github.actor }}
```

## Verification Commands

After updating an issue:

```bash
# GitHub: Verify comment was added
gh issue view "$ISSUE_NUM" --json comments --jq '.comments | length'

# JIRA: Verify comment was added
atlassian_getJiraIssue \
  --cloudId "$CLOUD_ID" \
  --issueIdOrKey "$TICKET_KEY" \
  --expand comments | jq '.fields.comment.comments | length'

# Check last update timestamp
gh issue view "$ISSUE_NUM" --json updatedAt --jq '.updatedAt'

# View issue timeline for updates
gh issue view "$ISSUE_NUM" --json timeline --jq '.timeline'
```

## Related Skills

- **git-semantic-commits**: For formatting commit messages that are referenced in updates
- **git-issue-labeler**: For labeling issues before updates are added
- **git-issue-creator**: For creating issues that receive progress updates
- **ticket-branch-workflow`: For JIRA tickets that receive progress updates
- **jira-git-integration**: For JIRA API operations used by this skill
- **jira-status-updater**: For automated JIRA ticket status transitions after PR merge
- **pr-creation-workflow**: For PR creation that triggers issue updates

## References

- [GitHub CLI Documentation](https://cli.github.com/manual/)
- [Git Log Formats](https://git-scm.com/docs/git-log#_pretty_formats)
- [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601)
- [Atlassian API Documentation](https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issue-comments)
