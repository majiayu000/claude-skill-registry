---
name: github-cli-patterns
description: Use when working with gh CLI. Provides patterns for PRs, issues, reviews, and repository operations.
version: "1.0.0"
author: "JacobPEvans"
---

# GitHub CLI Patterns

Common GitHub CLI (gh) command patterns. Single source of truth to reduce duplication across commands and agents.

## PR Operations

### List and View

```bash
# List: gh pr list [--state STATE] [--author USER] [--label LABEL] [--limit N] [--json FIELDS]
gh pr list --state open --json number,title,headRefName
gh pr list --author @me --state open --json number,title,mergeable,statusCheckRollup

# View: gh pr view <PR_NUMBER> [--json FIELDS]
gh pr view <PR_NUMBER> --json title,body,state,mergeable
gh pr view <PR_NUMBER> --json number,title,state,mergeable,statusCheckRollup,reviews,reviewDecision,headRefName
gh pr view <PR_NUMBER> --json headRefName --jq '.headRefName'  # Get branch name
```

### Create

```bash
# Template: gh pr create [--title TEXT] [--body TEXT] [--draft] [--base BRANCH]
gh pr create --fill  # Auto-fill from commits
gh pr create --draft --title "WIP: Feature" --body "Not ready for review"
gh pr create --base develop --title "Hotfix" --body "Emergency fix"
```

### Check Status

```bash
gh pr checks <PR_NUMBER>  # View status
gh pr checks <PR_NUMBER> --watch  # Wait for completion
gh pr checks <PR_NUMBER> --watch --fail-fast  # Exit on first failure
```

### Other Operations

```bash
gh pr checkout <PR_NUMBER>  # Checkout locally
gh pr diff <PR_NUMBER>  # Show changes
gh pr view <PR_NUMBER> --json files --jq '.files[].path'  # Get changed files
```

## Issue Operations

```bash
# List: gh issue list [--state STATE] [--label LABEL] [--assignee USER] [--limit N] [--json FIELDS]
gh issue list --state open --json number,title,labels,state,createdAt
gh issue list --search "-label:ai:created" --limit 20  # Exclude AI-created

# View: gh issue view <ISSUE_NUMBER> [--json FIELDS]
gh issue view <ISSUE_NUMBER> --json title,body,labels,comments

# Create: gh issue create [--title TEXT] [--body TEXT] [--label LABELS]
gh issue create --title "Bug" --body "Description" --label "bug,priority:high"
gh issue create --title "..." --body "..." --label "ai:created"  # AI-created (requires human review)

# Close: gh issue close <ISSUE_NUMBER> [--comment TEXT]
gh issue close <ISSUE_NUMBER> --comment "Fixed in PR #123"

# Comment
gh issue comment <ISSUE_NUMBER> --body "Comment text"
```

## Review Operations

```bash
# Submit review
gh pr review <PR_NUMBER> --approve [--body TEXT]
gh pr review <PR_NUMBER> --request-changes --body "Please address..."
gh pr review <PR_NUMBER> --comment --body "Looks good overall"

# View reviews
gh pr view <PR_NUMBER> --json reviews,reviewDecision

# Add comment
gh pr comment <PR_NUMBER> --body "Comment text"

# Line-level comments (via API)
gh api repos/<OWNER>/<REPO>/pulls/<PR_NUMBER>/comments \
  -f body="Comment" -F commit_id="<SHA>" -F path="file.js" -F line=42
```

## Repository Operations

```bash
# View current repo
gh repo view --json nameWithOwner,description,defaultBranchRef
gh repo view --json nameWithOwner --jq '.nameWithOwner'  # Get owner/repo
gh repo view --json defaultBranchRef --jq '.defaultBranchRef.name'  # Get default branch

# List repos
gh repo list <USERNAME> --limit 100 --json name,description,updatedAt
```

## Workflow and Check Operations

```bash
# List runs
gh run list --limit 20

# View run
gh run view <RUN_ID>  # Details
gh run view <RUN_ID> --log  # Logs
gh run watch <RUN_ID>  # Wait for completion

# Rerun
gh run rerun <RUN_ID> --failed  # Failed jobs only
gh run rerun <RUN_ID>  # Entire workflow
```

## API Operations

For GraphQL operations, use the github-graphql skill.

**IMPORTANT**: `gh pr view --json` does NOT support `reviewThreads`. Use GraphQL instead:

```bash
# GraphQL (required for reviewThreads) - see github-graphql skill for full patterns
gh api graphql --raw-field 'query=query { repository(owner: "{OWNER}", name: "{REPO}") { pullRequest(number: {NUMBER}) { reviewThreads(last: 100) { ... } } } }'

# REST API
gh api repos/<OWNER>/<REPO>/pulls/<PR_NUMBER>
gh api repos/<OWNER>/<REPO>/issues/<ISSUE_NUMBER>
```

## JSON Processing

```bash
# Extract field: --jq '.field'
gh pr view <PR_NUMBER> --json state --jq '.state'

# Extract array: --jq '.[] | "\(.field1): \(.field2)"'
gh pr list --json number,title --jq '.[] | "\(.number): \(.title)"'

# Filter: --jq '.[] | select(.field == "VALUE") | .field'
gh pr list --json number,state --jq '.[] | select(.state == "OPEN") | .number'

# Count: --jq '. | length'
gh pr list --json number --jq '. | length'
```

## Common Patterns

### Check PR Merge-Readiness

```bash
gh pr view <PR_NUMBER> --json state,mergeable,statusCheckRollup,reviewDecision

STATE=$(gh pr view <PR_NUMBER> --json mergeable --jq '.mergeable')
if [ "$STATE" = "MERGEABLE" ]; then echo "Ready to merge"; fi
```

### Get PR Author

```bash
gh pr view <PR_NUMBER> --json author --jq '.author.login'
```

### Watch CI with Exit Code

```bash
gh pr checks <PR_NUMBER> --watch
if [ $? -eq 0 ]; then echo "Passed"; else echo "Failed"; fi
```

## Authentication

```bash
gh auth status  # Check auth (safe for automation)
gh auth login  # Login interactively
```

## Error Handling

| Error | Meaning | Solution |
| ----- | ------- | -------- |
| `HTTP 404: Not Found` | PR/issue doesn't exist | Verify number |
| `HTTP 401: Unauthorized` | Not authenticated | Run `gh auth login` |
| `HTTP 403: Forbidden` | Insufficient permissions | Check repo access |
| `Resource not found` | Invalid owner/repo | Verify repository name |
| `GraphQL error` | Invalid query | Check syntax |

## Best Practices

1. Use `--json` for programmatic parsing
2. Use `jq` for extraction, not text parsing
3. Check auth before operations: `gh auth status`
4. Use specific field queries to reduce data transfer
5. Use `--watch` for long-running ops
6. Handle errors with exit code checking
7. Use `--limit` when listing to control size
8. Filter at query time when possible

## Related Skills

- github-graphql - GraphQL query patterns
- pr-health-check - PR status validation
- pr-thread-resolution-enforcement - Review thread resolution
