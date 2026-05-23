---
model: haiku
name: gh-cli-agentic
description: GitHub CLI commands optimized for AI agent workflows with JSON output and deterministic execution patterns.
allowed-tools: Bash(gh pr:*), Bash(gh run:*), Bash(gh issue:*), Bash(gh repo:*), Bash(gh workflow:*), Bash(gh api:*), Read
---

# GitHub CLI Agentic Patterns

Optimized `gh` commands for AI agent consumption using JSON output and structured field selection.

## Core Principle

Always use `--json <fields>` for machine-readable output. The `--jq` filter is built-in (no jq installation required).

## Pull Request Operations

### Check Status

```bash
# Get all check statuses
gh pr checks $PR_NUMBER --json name,state,conclusion,detailsUrl

# Filter to failed only
gh pr checks $PR_NUMBER --json name,state,conclusion --jq '.[] | select(.conclusion == "FAILURE")'
```

**Fields**: `name`, `state`, `conclusion`, `detailsUrl`, `startedAt`, `completedAt`

### PR Details

```bash
# Essential PR info
gh pr view $PR_NUMBER --json number,title,state,mergeable,statusCheckRollup

# Full context
gh pr view $PR_NUMBER --json number,title,body,state,author,labels,assignees,reviewDecision,mergeable,statusCheckRollup
```

**Key Fields**:

| Field | Description |
|-------|-------------|
| `mergeable` | `MERGEABLE`, `CONFLICTING`, `UNKNOWN` |
| `reviewDecision` | `APPROVED`, `CHANGES_REQUESTED`, `REVIEW_REQUIRED` |
| `statusCheckRollup` | Array of check statuses |

### List PRs

```bash
# Open PRs
gh pr list --json number,title,author,labels

# PRs by author
gh pr list --author @me --json number,title,state

# PRs needing review
gh pr list --search "review-requested:@me" --json number,title
```

## Workflow Run Operations

### Run Details

```bash
# Get run status with jobs
gh run view $RUN_ID --json conclusion,status,jobs,createdAt,updatedAt

# List recent runs
gh run list --json databaseId,status,conclusion,name,createdAt -L 10
```

**Status Values**: `queued`, `in_progress`, `completed`
**Conclusion Values**: `success`, `failure`, `cancelled`, `skipped`, `neutral`

### Watch Run Until Completion

```bash
# Watch and wait for run to complete (blocking, no timeout needed)
gh run watch $RUN_ID --compact --exit-status

# Find and watch latest run
RUN_ID=$(gh run list -L 1 --json databaseId --jq '.[0].databaseId')
gh run watch $RUN_ID --compact --exit-status
```

See **gh-workflow-monitoring** skill for comprehensive workflow watching patterns.

### Failed Logs

```bash
# Get only failed step logs (most useful for debugging)
gh run view $RUN_ID --log-failed

# Full logs (verbose)
gh run view $RUN_ID --log
```

### Workflow Triggers

```bash
# Trigger workflow manually
gh workflow run $WORKFLOW_NAME

# Trigger with inputs
gh workflow run $WORKFLOW_NAME -f param1=value1 -f param2=value2

# List workflows
gh workflow list --json name,state,path
```

## Issue Operations

### Issue Details

```bash
# Full issue context
gh issue view $ISSUE_NUMBER --json number,title,body,state,labels,assignees,comments

# Minimal
gh issue view $ISSUE_NUMBER --json number,title,state,labels
```

### List Issues

```bash
# Open issues
gh issue list --json number,title,labels,assignees

# By label
gh issue list --label "bug" --json number,title

# Assigned to me
gh issue list --assignee @me --json number,title,state
```

## Repository Operations

```bash
# Get repo info
gh repo view --json nameWithOwner,defaultBranchRef,description

# Just owner/name
gh repo view --json nameWithOwner --jq '.nameWithOwner'
```

## API Direct Access

For operations not covered by subcommands:

```bash
# Get specific data
gh api repos/{owner}/{repo}/actions/runs --jq '.workflow_runs[:5]'

# With pagination
gh api repos/{owner}/{repo}/issues --paginate --jq '.[].number'
```

## Agentic Optimizations

| Context | Command |
|---------|---------|
| CI diagnosis | `gh pr checks $N --json name,state,conclusion,detailsUrl` |
| Get failure logs | `gh run view $ID --log-failed` |
| PR merge status | `gh pr view $N --json mergeable,reviewDecision,statusCheckRollup` |
| Quick issue list | `gh issue list --json number,title,labels -L 10` |
| Workflow trigger | `gh workflow run $NAME` |

## Error Handling in Context

Always include fallback for context expressions:

```markdown
- PR checks: !`gh pr checks $PR --json name,state,conclusion 2>/dev/null || echo "[]"`
- Run status: !`gh run view $ID --json status,conclusion 2>/dev/null || echo "{}"`
```

## Field Reference

### PR Fields

`number`, `title`, `body`, `state`, `author`, `labels`, `assignees`, `reviewDecision`, `mergeable`, `statusCheckRollup`, `headRefName`, `baseRefName`, `isDraft`, `url`, `createdAt`, `updatedAt`

### Issue Fields

`number`, `title`, `body`, `state`, `author`, `labels`, `assignees`, `comments`, `milestone`, `url`, `createdAt`, `updatedAt`, `closedAt`

### Run Fields

`databaseId`, `name`, `status`, `conclusion`, `jobs`, `createdAt`, `updatedAt`, `url`, `headBranch`, `headSha`, `event`

### Job Fields (within runs)

`name`, `status`, `conclusion`, `startedAt`, `completedAt`, `steps`
