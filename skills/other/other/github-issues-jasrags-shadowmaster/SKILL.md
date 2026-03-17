---
name: github-issues
description: Guide for GitHub issue management including epics, sub-issues, milestones, and relationships. Use when creating issues, organizing work into epics, linking related issues, or using gh CLI and GraphQL API for issue operations.
allowed-tools: Bash, Read, Grep, Glob
---

# GitHub Issues Management

Use this skill when working with GitHub issues, epics, milestones, and issue relationships. Covers `gh` CLI usage, GraphQL API for advanced operations, and best practices for issue organization.

## Tool Selection

| Task                      | Preferred Tool        | Notes                                |
| ------------------------- | --------------------- | ------------------------------------ |
| Create/edit/close issues  | `gh issue` CLI        | Simple, reliable                     |
| Add labels, milestones    | `gh issue edit`       | Use `--add-label`, `--milestone`     |
| Sub-issues (parent/child) | GraphQL `addSubIssue` | Progress tracking on epics           |
| List/search issues        | `gh issue list`       | Filter with `--label`, `--milestone` |
| Complex queries           | `gh api graphql`      | For relationships, bulk operations   |
| View issue details        | `gh issue view`       | Add `--json` for structured data     |

> **Note:** The GitHub MCP server has authentication issues. Always prefer `gh` CLI via Bash.

## Quick Reference Commands

### Basic Issue Operations

```bash
# Create issue with milestone and labels
gh issue create --repo OWNER/REPO \
  --title "Issue title" \
  --body "Issue body" \
  --milestone "v0.9 - Creation Complete" \
  --label "security" --label "enhancement"

# Edit existing issue
gh issue edit ISSUE_NUMBER --repo OWNER/REPO \
  --add-label "epic" \
  --milestone "v0.9 - Creation Complete"

# List issues by milestone
gh issue list --repo OWNER/REPO --milestone "v0.9 - Creation Complete"

# List issues by label
gh issue list --repo OWNER/REPO --label "security"

# View issue details
gh issue view ISSUE_NUMBER --repo OWNER/REPO

# Close issue
gh issue close ISSUE_NUMBER --repo OWNER/REPO
```

### Creating Issues with Heredoc (for complex bodies)

```bash
gh issue create --repo OWNER/REPO \
  --title "[EPIC] Feature Name" \
  --milestone "v0.9 - Creation Complete" \
  --label "epic" \
  --body "$(cat <<'EOF'
## Overview
Description here.

## Sub-tasks
- [ ] Task 1
- [ ] Task 2

## Acceptance Criteria
- [ ] Criterion 1
EOF
)"
```

## Epic Management

### Epic Structure

Epics are regular issues with:

1. `epic` label
2. `[EPIC]` prefix in title
3. Checklist of child issues in body
4. Sub-issues linked via GraphQL API (provides progress tracking)

### Creating an Epic with Children

```bash
# 1. Create the epic issue
EPIC_URL=$(gh issue create --repo OWNER/REPO \
  --title "[EPIC] Feature Name" \
  --label "epic" --label "enhancement" \
  --milestone "v0.9 - Creation Complete" \
  --body "$(cat <<'EOF'
## Overview
Epic description.

## Child Issues
- [ ] #TBD - First task
- [ ] #TBD - Second task

## Acceptance Criteria
- [ ] All child issues completed
EOF
)")
EPIC_NUM=$(echo $EPIC_URL | grep -oE '[0-9]+$')

# 2. Create child issues (reference the epic)
gh issue create --repo OWNER/REPO \
  --title "First task" \
  --milestone "v0.9 - Creation Complete" \
  --body "## Parent Epic
Part of #$EPIC_NUM"

# 3. Link as sub-issues (see Sub-Issues section below)
```

## Sub-Issues (Parent/Child Relationships)

GitHub's sub-issues feature provides:

- Progress tracking (X of Y completed) shown as badge
- Visual hierarchy in issue view
- Automatic progress bar on epic

### Getting Issue Node IDs

```bash
# Get node ID for a single issue
gh api graphql -f query='
query {
  repository(owner: "OWNER", name: "REPO") {
    issue(number: ISSUE_NUMBER) {
      id
      number
      title
    }
  }
}' --jq '.data.repository.issue.id'

# Get multiple issue IDs
for num in 168 169 170; do
  gh api graphql -f query="
    query {
      repository(owner: \"OWNER\", name: \"REPO\") {
        issue(number: $num) {
          id
          number
        }
      }
    }" --jq ".data.repository.issue | \"\(.number): \(.id)\""
done
```

### Adding Sub-Issues

```bash
EPIC_ID="I_kwDO..."  # Parent issue node ID
CHILD_ID="I_kwDO..." # Child issue node ID

gh api graphql -f query="
mutation {
  addSubIssue(input: {issueId: \"$EPIC_ID\", subIssueId: \"$CHILD_ID\"}) {
    issue {
      number
    }
    subIssue {
      number
    }
  }
}"
```

### Bulk Add Sub-Issues

```bash
EPIC_ID="I_kwDO..."

for CHILD_ID in I_kwDO...1 I_kwDO...2 I_kwDO...3; do
  gh api graphql -f query="
    mutation {
      addSubIssue(input: {issueId: \"$EPIC_ID\", subIssueId: \"$CHILD_ID\"}) {
        issue { number }
        subIssue { number }
      }
    }" 2>&1 | head -1
done
```

### Removing Sub-Issues

```bash
gh api graphql -f query="
mutation {
  removeSubIssue(input: {issueId: \"$EPIC_ID\", subIssueId: \"$CHILD_ID\"}) {
    issue { number }
    subIssue { number }
  }
}"
```

### Querying Sub-Issues

```bash
gh api graphql -f query='
query {
  repository(owner: "OWNER", name: "REPO") {
    issue(number: EPIC_NUMBER) {
      title
      subIssues(first: 50) {
        nodes {
          number
          title
          state
        }
      }
      subIssuesSummary {
        total
        completed
        percentCompleted
      }
    }
  }
}' --jq '.data.repository.issue'
```

## Relationship Types

| Type                      | API Support                 | UI Location                        | How to Add  |
| ------------------------- | --------------------------- | ---------------------------------- | ----------- |
| Sub-issues (parent/child) | `addSubIssue` mutation      | Progress badge, Sub-issues section | GraphQL API |
| Tracked by/Tracks         | Read-only (`trackedIssues`) | Relationships sidebar              | **UI only** |
| Blocking/Blocked by       | Read-only                   | Relationships sidebar              | **UI only** |
| Duplicate of              | `markIssueAsDuplicate`      | Issue banner                       | GraphQL API |

> **Important:** "Tracked by" and "Blocking" relationships can only be added via GitHub web UI, not via API.

## Labels and Milestones

### List Available Labels

```bash
gh label list --repo OWNER/REPO
```

### Create Label

```bash
gh label create "security" --repo OWNER/REPO \
  --description "Security-related issues" \
  --color "FF0000"
```

### List Milestones

```bash
gh api repos/OWNER/REPO/milestones --jq '.[] | "\(.number): \(.title)"'
```

### Create Milestone

```bash
gh api repos/OWNER/REPO/milestones \
  --method POST \
  -f title="v1.0 - Release" \
  -f description="First major release" \
  -f due_on="2024-12-31T23:59:59Z"
```

## Issue Templates

### Security Issue Template

```markdown
## Parent Epic

Part of #EPIC_NUMBER - Epic Title

## Priority

**HIGH/MEDIUM/LOW** - Brief rationale (Priority X of Y)

## Problem

Description of the security issue.

\`\`\`typescript
// Code showing the problem
\`\`\`

## Risk

- Bullet points of risks

## Solution

Proposed fix with code examples.

## Files to Modify

- \`path/to/file.ts\` - Description of changes

## Acceptance Criteria

- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Unit tests added
```

### Feature Issue Template

```markdown
## Overview

Brief description of the feature.

## User Story

As a [role], I want [feature] so that [benefit].

## Requirements

- Requirement 1
- Requirement 2

## Technical Design

Implementation approach.

## Files to Create/Modify

- \`path/to/file.ts\` - Description

## Acceptance Criteria

- [ ] Criterion 1
- [ ] Criterion 2
```

## GraphQL API Reference

### Available Issue Fields

```graphql
query {
  repository(owner: "OWNER", name: "REPO") {
    issue(number: NUMBER) {
      id # Node ID for mutations
      number
      title
      body
      state # OPEN, CLOSED
      stateReason # COMPLETED, NOT_PLANNED, REOPENED
      labels(first: 10) {
        nodes {
          name
        }
      }
      milestone {
        title
      }
      assignees(first: 5) {
        nodes {
          login
        }
      }

      # Relationships
      parent {
        number
        title
      }
      subIssues(first: 50) {
        nodes {
          number
          title
          state
        }
      }
      subIssuesSummary {
        total
        completed
        percentCompleted
      }
      trackedIssues(first: 10) {
        nodes {
          number
        }
      }
      trackedInIssues(first: 10) {
        nodes {
          number
        }
      }
    }
  }
}
```

### Available Mutations

| Mutation                  | Purpose                  |
| ------------------------- | ------------------------ |
| `createIssue`             | Create new issue         |
| `updateIssue`             | Update issue fields      |
| `closeIssue`              | Close an issue           |
| `reopenIssue`             | Reopen closed issue      |
| `addSubIssue`             | Link child to parent     |
| `removeSubIssue`          | Unlink child from parent |
| `reprioritizeSubIssue`    | Reorder sub-issues       |
| `pinIssue` / `unpinIssue` | Pin/unpin to repo        |
| `markIssueAsDuplicate`    | Mark as duplicate        |

## Best Practices

### Epic Organization

1. Use `[EPIC]` prefix for easy identification
2. Add `epic` label
3. List all child issues in epic body with checkboxes
4. Link sub-issues via GraphQL for progress tracking
5. Update epic body when adding/completing child issues

### Issue Hygiene

1. Always assign to a milestone
2. Use consistent label taxonomy
3. Reference parent epic in child issue body (`Part of #123`)
4. Keep issue bodies updated as work progresses
5. Close issues with reason (completed vs not planned)

### Bulk Operations

1. Get all node IDs first, then loop mutations
2. Use `--jq` for clean output parsing
3. Check for errors in mutation responses
4. Consider rate limits for large operations (5000 points/hour)

## Common Patterns

### Complete Epic Workflow

```bash
REPO="Jasrags/ShadowMaster"
MILESTONE="v0.9 - Creation Complete"

# 1. Create epic
EPIC_URL=$(gh issue create --repo $REPO \
  --title "[EPIC] New Feature" \
  --label "epic" \
  --milestone "$MILESTONE" \
  --body "## Overview
Feature description.

## Child Issues
(to be added)")
EPIC_NUM=$(echo $EPIC_URL | grep -oE '[0-9]+$')
echo "Created epic #$EPIC_NUM"

# 2. Create child issues
CHILD1=$(gh issue create --repo $REPO --title "Task 1" --milestone "$MILESTONE" \
  --body "Part of #$EPIC_NUM" | grep -oE '[0-9]+$')
CHILD2=$(gh issue create --repo $REPO --title "Task 2" --milestone "$MILESTONE" \
  --body "Part of #$EPIC_NUM" | grep -oE '[0-9]+$')

# 3. Get node IDs
EPIC_ID=$(gh api graphql -f query="query { repository(owner:\"${REPO%/*}\", name:\"${REPO#*/}\") { issue(number:$EPIC_NUM) { id } } }" --jq '.data.repository.issue.id')

for num in $CHILD1 $CHILD2; do
  CHILD_ID=$(gh api graphql -f query="query { repository(owner:\"${REPO%/*}\", name:\"${REPO#*/}\") { issue(number:$num) { id } } }" --jq '.data.repository.issue.id')

  # 4. Link as sub-issues
  gh api graphql -f query="mutation { addSubIssue(input:{issueId:\"$EPIC_ID\",subIssueId:\"$CHILD_ID\"}) { issue{number} subIssue{number} } }"
done

# 5. Update epic body with issue numbers
gh issue edit $EPIC_NUM --repo $REPO --body "## Overview
Feature description.

## Child Issues
- [ ] #$CHILD1 - Task 1
- [ ] #$CHILD2 - Task 2"
```

### Find Issues Without Milestone

```bash
gh issue list --repo OWNER/REPO --milestone "" --state open
```

### Move Issues to Different Milestone

```bash
for issue in 1 2 3; do
  gh issue edit $issue --repo OWNER/REPO --milestone "New Milestone"
done
```

### Search Issues

```bash
# By text
gh issue list --repo OWNER/REPO --search "authentication"

# By author
gh issue list --repo OWNER/REPO --author "username"

# Combined filters
gh issue list --repo OWNER/REPO --label "bug" --state open --milestone "v1.0"
```
