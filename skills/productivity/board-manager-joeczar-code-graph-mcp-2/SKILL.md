---
name: board-manager
description: Manage GitHub Project board items - add issues, update status, move between columns. Use when user asks to add issues to board, change status, or organize the project.
allowed-tools: Bash, Read
---

# Board Manager Skill

## Purpose

Add issues to the project board and update their status. This skill has **write permissions** for board operations.

## When to Use This

- User asks "add this issue to the board"
- User asks "move #X to In Progress"
- User asks "update status of issue"
- After creating a new issue (auto-add to board)
- After completing work (move to Done)

## Project Board Configuration

**Project:** code-graph-mcp Development (#8)
**URL:** https://github.com/users/joeczar/projects/8

### IDs Reference

| Resource | ID |
|----------|-----|
| Project ID | `PVT_kwHOAbYJAM4BM5GY` |
| Status Field ID | `PVTSSF_lAHOAbYJAM4BM5GYzg8C2zk` |

### Status Option IDs

| Status | Option ID | Description |
|--------|-----------|-------------|
| Todo | `f75ad846` | Not started |
| In Progress | `47fc9ee4` | Currently working |
| Done | `98236657` | Completed |

## Commands

### Add Issue to Project Board

```bash
gh project item-add 8 --owner joeczar --url https://github.com/joeczar/code-graph-mcp/issues/<number>
```

### Get Item ID for an Issue

```bash
gh project item-list 8 --owner joeczar --format json | \
  jq -r '.items[] | select(.content.number == <issue-number>) | .id'
```

Or via GraphQL:

```bash
gh api graphql -f query='
  query {
    user(login: "joeczar") {
      projectV2(number: 8) {
        items(first: 100) {
          nodes {
            id
            content { ... on Issue { number } }
          }
        }
      }
    }
  }' | jq -r '.data.user.projectV2.items.nodes[] | select(.content.number == <issue-number>) | .id'
```

### Update Issue Status

```bash
gh api graphql \
  -f projectId="PVT_kwHOAbYJAM4BM5GY" \
  -f itemId="<item-id>" \
  -f fieldId="PVTSSF_lAHOAbYJAM4BM5GYzg8C2zk" \
  -f optionId="<option-id>" \
  -f query='mutation($projectId: ID!, $itemId: ID!, $fieldId: ID!, $optionId: String!) {
    updateProjectV2ItemFieldValue(input: {
      projectId: $projectId
      itemId: $itemId
      fieldId: $fieldId
      value: { singleSelectOptionId: $optionId }
    }) {
      projectV2Item { id }
    }
  }'
```

### Remove Issue from Project

```bash
gh project item-delete 8 --owner joeczar --id <item-id>
```

## Helper Functions

### Move Issue to Status

```bash
move_issue_status() {
  local issue_number=$1
  local option_id=$2  # f75ad846=Todo, 47fc9ee4=InProgress, 98236657=Done
  local status_name=$3

  # Get item ID
  local item_id=$(gh project item-list 8 --owner joeczar --format json | \
    jq -r '.items[] | select(.content.number == '$issue_number') | .id')

  if [ -z "$item_id" ]; then
    echo "Issue #$issue_number not found on project board"
    return 1
  fi

  # Update status
  gh api graphql \
    -f projectId="PVT_kwHOAbYJAM4BM5GY" \
    -f itemId="$item_id" \
    -f fieldId="PVTSSF_lAHOAbYJAM4BM5GYzg8C2zk" \
    -f optionId="$option_id" \
    -f query='mutation($projectId: ID!, $itemId: ID!, $fieldId: ID!, $optionId: String!) {
      updateProjectV2ItemFieldValue(input: {
        projectId: $projectId
        itemId: $itemId
        fieldId: $fieldId
        value: { singleSelectOptionId: $optionId }
      }) { projectV2Item { id } }
    }'

  echo "Moved #$issue_number to $status_name"
}

# Usage:
# move_issue_status 12 "47fc9ee4" "In Progress"
# move_issue_status 12 "98236657" "Done"
```

## Workflow Integration

### Start Working on Issue

1. Add issue to project (if not already)
2. Set status to "In Progress"

```bash
# Add to project
gh project item-add 8 --owner joeczar --url "https://github.com/joeczar/code-graph-mcp/issues/<number>"

# Get item ID and move to In Progress
ITEM_ID=$(gh project item-list 8 --owner joeczar --format json | \
  jq -r '.items[] | select(.content.number == <number>) | .id')

gh api graphql \
  -f projectId="PVT_kwHOAbYJAM4BM5GY" \
  -f itemId="$ITEM_ID" \
  -f fieldId="PVTSSF_lAHOAbYJAM4BM5GYzg8C2zk" \
  -f optionId="47fc9ee4" \
  -f query='mutation($projectId: ID!, $itemId: ID!, $fieldId: ID!, $optionId: String!) {
    updateProjectV2ItemFieldValue(input: {
      projectId: $projectId
      itemId: $itemId
      fieldId: $fieldId
      value: { singleSelectOptionId: $optionId }
    }) { projectV2Item { id } }
  }'
```

### Complete Issue

Set status to "Done" (PR merge will auto-close issue).

## Status Mapping

| Action | Status | Option ID |
|--------|--------|-----------|
| New issue, not started | Todo | `f75ad846` |
| Started work | In Progress | `47fc9ee4` |
| PR merged | Done | `98236657` |

## Query Current IDs (if they change)

```bash
gh api graphql -f query='
query {
  user(login: "joeczar") {
    projectV2(number: 8) {
      id
      field(name: "Status") {
        ... on ProjectV2SingleSelectField {
          id
          options { id name }
        }
      }
    }
  }
}'
```

## Output Format

After operations, confirm:

```markdown
**Board Update:** Issue #X moved to [Status]
**URL:** https://github.com/users/joeczar/projects/8
```
