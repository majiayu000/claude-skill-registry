---
name: manage-issues
description: Use when creating, updating, or triaging GitHub issues — enforces issue types (not labels), GraphQL relationships, and repo-specific conventions for MQFacultyOfArts/PromptGrimoireTool
user-invocable: false
---

# GitHub Issue Management

Reference for managing issues in this repo. Uses GitHub issue types, native relationships, and GraphQL mutations.

## Issue Types (NOT Labels)

This repo uses **GitHub Issue Types**, not `bug`/`enhancement` labels. Those labels have been deleted.

| Type | When | GraphQL `issueTypeId` |
|------|------|-----------------------|
| Bug | Something is broken | `IT_kwDOAktGus4Ac3IT` |
| Feature | New user-facing capability | `IT_kwDOAktGus4Ac3IX` |
| Task | Internal work: refactors, tests, infra, epics, seams | `IT_kwDOAktGus4Ac3IQ` |

### Set Issue Type

The `gh issue create` CLI does not support `--type` yet. Set type via GraphQL after creation:

```bash
# 1. Get the issue's node ID
gh api graphql -f query='
{
  repository(owner: "MQFacultyOfArts", name: "PromptGrimoireTool") {
    issue(number: 123) { id }
  }
}' --jq '.data.repository.issue.id'

# 2. Set type (example: Bug)
gh api graphql -f query='
mutation {
  updateIssue(input: {
    id: "ISSUE_NODE_ID",
    issueTypeId: "IT_kwDOAktGus4Ac3IT"
  }) { issue { number } }
}'
```

Batch multiple issues in one mutation using aliases:

```bash
gh api graphql -f query='
mutation {
  i1: updateIssue(input: {id: "NODE_ID_1", issueTypeId: "IT_kwDOAktGus4Ac3IX"}) { issue { number } }
  i2: updateIssue(input: {id: "NODE_ID_2", issueTypeId: "IT_kwDOAktGus4Ac3IX"}) { issue { number } }
}'
```

## Relationships

GitHub has **native** blocking and sub-issue relationships. Use GraphQL, not comments.

### Blocking (A blocks B)

```bash
# Get node IDs for both issues
gh api graphql -f query='
{
  repository(owner: "MQFacultyOfArts", name: "PromptGrimoireTool") {
    blocker: issue(number: 186) { id }
    blocked: issue(number: 100) { id }
  }
}'

# Set relationship: 186 blocks 100
gh api graphql -f query='
mutation {
  addBlockedBy(input: {
    issueId: "BLOCKED_NODE_ID",
    blockingIssueId: "BLOCKER_NODE_ID"
  }) { blockedByItems { nodes { id } } }
}'
```

**Field names**: `issueId` = the issue that IS blocked, `blockingIssueId` = the issue doing the blocking.

### Sub-issues (parent/child)

```bash
gh api graphql -f query='
mutation {
  addSubIssue(input: {
    issueId: "PARENT_NODE_ID",
    subIssueId: "CHILD_NODE_ID"
  }) { issue { id } }
}'
```

## Labels

Semantic labels that complement (not duplicate) issue types:

| Category | Labels |
|----------|--------|
| Domain | `domain:workspace-platform`, `domain:case-brief`, `domain:roleplay`, `domain:translation`, `domain:pdf-export` |
| Phase | `phase:mvp`, `phase:post-mvp` |
| Type qualifier | `type:epic`, `type:seam`, `type:perf`, `type:refactor`, `type:prd` |
| Component | `auth`, `database`, `ui`, `parser`, `documentation` |
| Planning | `design-planned`, `implementation-planned`, `spike` |

**Do NOT use**: `bug`, `enhancement` (deleted — use issue types instead).

## Creating Issues

```bash
gh issue create \
  --title "Bug: Description here" \
  --label "domain:workspace-platform,phase:mvp" \
  --milestone "27 Feb - MVP" \
  --body "$(cat <<'EOF'
Issue body here.
EOF
)"
```

Then set the issue type via GraphQL (see above).

## Milestones

Check current milestones with `gh api repos/MQFacultyOfArts/PromptGrimoireTool/milestones --jq '.[].title'`.

Always assign new issues to a milestone.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| `--label "bug"` | Deleted. Set issue type=Bug via GraphQL |
| `--label "enhancement"` | Deleted. Set issue type=Feature via GraphQL |
| Blocking via comments | Use `addBlockedBy` GraphQL mutation |
| Sub-issues via checklist | Use `addSubIssue` GraphQL mutation |
| Wrong field in `addBlockedBy` | `issueId` = blocked issue, `blockingIssueId` = blocker |
