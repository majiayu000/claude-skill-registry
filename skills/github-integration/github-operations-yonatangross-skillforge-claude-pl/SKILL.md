---
name: github-operations
description: GitHub CLI operations for issues, PRs, milestones, and Projects v2. Covers gh commands, REST API patterns, and automation scripts. Use when managing GitHub issues, PRs, milestones, or Projects with gh.
context: fork
version: 1.0.0
tags: [github, gh, cli, issues, pr, milestones, projects, api]
user-invocable: false
---

# GitHub Operations

Comprehensive GitHub CLI (`gh`) operations for project management, from basic issue creation to advanced Projects v2 integration and milestone tracking via REST API.

## Overview

- Creating and managing GitHub issues and PRs
- Working with GitHub Projects v2 custom fields
- Managing milestones (sprints, releases) via REST API
- Automating bulk operations with `gh`
- Running GraphQL queries for complex operations

---

## Quick Reference

### Issue Operations

```bash
# Create issue with labels and milestone
gh issue create --title "Bug: API returns 500" --body "..." --label "bug" --milestone "Sprint 5"

# List and filter issues
gh issue list --state open --label "backend" --assignee @me

# Edit issue metadata
gh issue edit 123 --add-label "high" --milestone "v2.0"
```

### PR Operations

```bash
# Create PR with reviewers
gh pr create --title "feat: Add search" --body "..." --base dev --reviewer @teammate

# Watch CI status and auto-merge
gh pr checks 456 --watch
gh pr merge 456 --auto --squash --delete-branch
```

### Milestone Operations (REST API)

```bash
# List milestones with progress
gh api repos/:owner/:repo/milestones --jq '.[] | "\(.title): \(.closed_issues)/\(.open_issues + .closed_issues)"'

# Create milestone with due date
gh api -X POST repos/:owner/:repo/milestones \
  -f title="Sprint 8" -f due_on="2026-02-15T00:00:00Z"

# Close milestone
gh api -X PATCH repos/:owner/:repo/milestones/5 -f state=closed
```

### Projects v2 Operations

```bash
# Add issue to project
gh project item-add 1 --owner @me --url https://github.com/org/repo/issues/123

# Set custom field (requires GraphQL)
gh api graphql -f query='mutation {...}' -f projectId="..." -f itemId="..."
```

---

## JSON Output Patterns

```bash
# Get issue numbers matching criteria
gh issue list --json number,labels --jq '[.[] | select(.labels[].name == "bug")] | .[].number'

# PR summary with author
gh pr list --json number,title,author --jq '.[] | "\(.number): \(.title) by \(.author.login)"'

# Find ready-to-merge PRs
gh pr list --json number,reviewDecision,statusCheckRollupState \
  --jq '[.[] | select(.reviewDecision == "APPROVED" and .statusCheckRollupState == "SUCCESS")]'
```

---

## Key Concepts

### Milestone vs Epic

| Milestones | Epics |
|------------|-------|
| Time-based (sprints, releases) | Topic-based (features) |
| Has due date | No due date |
| Progress bar | Task list checkbox |
| Native REST API | Needs workarounds |

**Rule**: Use milestones for "when", use parent issues for "what".

### Projects v2 Custom Fields

Projects v2 uses GraphQL for setting custom fields (Status, Priority, Domain). Basic `gh project` commands work for listing and adding items, but field updates require GraphQL mutations.

---

## Best Practices

1. **Always use `--json` for scripting** - Parse with `--jq` for reliability
2. **Non-interactive mode for automation** - Use `--title`, `--body` flags
3. **Check rate limits before bulk operations** - `gh api rate_limit`
4. **Use heredocs for multi-line content** - `--body "$(cat <<'EOF'...EOF)"`
5. **Link issues in PRs** - `Closes #123`, `Fixes #456`
6. **Use ISO 8601 dates** - `YYYY-MM-DDTHH:MM:SSZ` for milestone due_on
7. **Close milestones, don't delete** - Preserve history

---

## Related Skills

- `create-pr` - Create pull requests with proper formatting and review assignments
- `review-pr` - Comprehensive PR review with specialized agents
- `release-management` - GitHub release workflow with semantic versioning and changelogs
- `stacked-prs` - Manage dependent PRs with rebase coordination
- `issue-progress-tracking` - Automatic issue progress updates from commits

## Key Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| CLI vs API | gh CLI preferred | Simpler auth, better UX, handles pagination automatically |
| Output format | --json with --jq | Reliable parsing for automation, no regex parsing needed |
| Milestones vs Epics | Milestones for time | Milestones have due dates and progress bars, epics for topic grouping |
| Projects v2 fields | GraphQL mutations | gh project commands limited, GraphQL required for custom fields |
| Milestone lifecycle | Close, don't delete | Preserves history and progress tracking |

## References

- [Issue Management](references/issue-management.md) - Bulk operations, templates, sub-issues
- [PR Workflows](references/pr-workflows.md) - Reviews, merge strategies, auto-merge
- [Milestone API](references/milestone-api.md) - REST API patterns for milestone CRUD
- [Projects v2](references/projects-v2.md) - Custom fields, GraphQL mutations
- [GraphQL API](references/graphql-api.md) - Complex queries, pagination, bulk operations

## Examples

- [Automation Scripts](examples/automation-scripts.md) - Ready-to-use scripts for bulk operations, PR automation, milestone management
