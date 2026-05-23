---
name: linear-pm
description: Linear project management - issues, projects, cycles, and roadmaps. Use for Linear-related tasks like managing issues, tracking sprints, and organizing projects.
allowed-tools: read, bash, webfetch
---

# Linear PM Skill

## Overview

This skill provides comprehensive Linear project management capabilities with progressive disclosure for optimal context usage.

**Context Savings**: ~92% reduction

- **Direct API Mode**: ~15,000 tokens for full API documentation
- **Skill Mode**: ~300 tokens metadata + on-demand loading

## Requirements

- `LINEAR_API_KEY` environment variable set
- Internet connectivity for Linear API access

## Toolsets

The skill provides 18+ tools across 5 toolsets:

| Toolset    | Description                                      |
| ---------- | ------------------------------------------------ |
| `issues`   | Issue creation, updates, comments, state changes |
| `projects` | Project management and issue association         |
| `cycles`   | Sprint/cycle management and planning             |
| `teams`    | Team structure and member management             |
| `labels`   | Label and workflow state management              |

## Quick Reference

```bash
# List issues
linear-pm list-issues --team-id "TEAM-123" --state "In Progress"

# Get issue details
linear-pm get-issue --issue-id "ISSUE-456"

# Create new issue
linear-pm create-issue --title "Bug fix" --description "Details" --team-id "TEAM-123"

# Update issue
linear-pm update-issue --issue-id "ISSUE-456" --state "Done"

# Add comment
linear-pm add-comment --issue-id "ISSUE-456" --comment "Fixed in PR #123"

# List projects
linear-pm list-projects --team-id "TEAM-123"

# Get current cycle
linear-pm current-cycle --team-id "TEAM-123"

# List cycle issues
linear-pm cycle-issues --cycle-id "CYCLE-789"
```

## Tools by Category

### Issue Operations (Confirmation Required for Mutations)

| Tool            | Description                                       | Confirmation |
| --------------- | ------------------------------------------------- | ------------ |
| `list-issues`   | List issues with filters (state, assignee, label) | No           |
| `get-issue`     | Get detailed issue information                    | No           |
| `create-issue`  | Create new issue with title, description, team    | Yes          |
| `update-issue`  | Update issue fields (state, assignee, priority)   | Yes          |
| `add-comment`   | Add comment to an issue                           | Yes          |
| `search-issues` | Search issues by text query                       | No           |
| `assign-issue`  | Assign issue to team member                       | Yes          |
| `set-priority`  | Set issue priority (urgent, high, medium, low)    | Yes          |
| `add-label`     | Add label to issue                                | Yes          |

### Project Operations

| Tool             | Description                      | Confirmation |
| ---------------- | -------------------------------- | ------------ |
| `list-projects`  | List all projects for a team     | No           |
| `get-project`    | Get project details and metadata | No           |
| `project-issues` | Get all issues in a project      | No           |
| `create-project` | Create new project               | Yes          |
| `update-project` | Update project details           | Yes          |

### Cycle Operations (Sprints)

| Tool             | Description                    | Confirmation |
| ---------------- | ------------------------------ | ------------ |
| `list-cycles`    | List cycles for a team         | No           |
| `current-cycle`  | Get current active cycle       | No           |
| `cycle-issues`   | Get issues in a specific cycle | No           |
| `cycle-progress` | Get cycle completion metrics   | No           |

### Team Operations

| Tool           | Description                 | Confirmation |
| -------------- | --------------------------- | ------------ |
| `list-teams`   | List all teams in workspace | No           |
| `get-team`     | Get team details            | No           |
| `team-members` | List team members           | No           |

### Label & State Operations

| Tool           | Description                                             | Confirmation |
| -------------- | ------------------------------------------------------- | ------------ |
| `list-labels`  | List all labels for a team                              | No           |
| `list-states`  | List workflow states (backlog, todo, in progress, done) | No           |
| `create-label` | Create new label                                        | Yes          |

## Implementation

### Tool Execution Pattern

All tools use the Linear GraphQL API with progressive disclosure:

```bash
#!/usr/bin/env bash
# Example: list-issues tool

LINEAR_API_KEY="${LINEAR_API_KEY}"
if [[ -z "$LINEAR_API_KEY" ]]; then
  echo "Error: LINEAR_API_KEY environment variable not set"
  exit 1
fi

QUERY='query {
  issues(filter: { state: { name: { eq: "In Progress" } } }) {
    nodes {
      id
      title
      state { name }
      assignee { name }
      priority
      createdAt
    }
  }
}'

curl -X POST https://api.linear.app/graphql \
  -H "Authorization: $LINEAR_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"query\": \"$QUERY\"}"
```

### Common Filters

**Issue Filters**:

- `state`: Filter by workflow state (e.g., "In Progress", "Done")
- `assignee`: Filter by assigned user ID
- `priority`: Filter by priority (0=none, 1=urgent, 2=high, 3=medium, 4=low)
- `label`: Filter by label name
- `team`: Filter by team ID

**Project Filters**:

- `state`: Filter by project state (planned, started, paused, completed)
- `lead`: Filter by project lead user ID

**Cycle Filters**:

- `isActive`: Get only active cycles
- `team`: Filter by team ID

## Security

**API Key Protection**:

- Never expose `LINEAR_API_KEY` in logs or output
- API key should have minimal required permissions
- Use read-only API key when possible for queries

**Mutation Confirmation**:
All tools that modify data require confirmation:

- Issue creation/updates
- Comment additions
- Project modifications
- Label creation

**Read-Only Operations** (No Confirmation):

- Listing issues, projects, cycles
- Getting details
- Searching

## Error Handling

If tool execution fails:

1. **Verify API Key**: Check `LINEAR_API_KEY` is set correctly

   ```bash
   echo $LINEAR_API_KEY
   ```

2. **Check API Rate Limits**: Linear enforces rate limits
   - GraphQL: 1500 requests per hour per API key
   - REST: 500 requests per hour per API key

3. **Validate Query Syntax**: Ensure GraphQL queries are well-formed

4. **Check Team/Issue IDs**: Verify IDs exist and are accessible

## Agent Integration

**Primary Agents**:

- `pm` - Product management and backlog prioritization
- `analyst` - Issue analysis and sprint planning

**Secondary Agents**:

- `developer` - Issue implementation and status updates
- `architect` - Technical issue decomposition
- `qa` - Issue testing and validation

## Common Workflows

### Sprint Planning

1. `current-cycle` - Get current sprint
2. `list-issues --state "Backlog"` - Get backlog items
3. `update-issue --cycle-id "..."` - Assign issues to sprint

### Issue Triage

1. `list-issues --state "Backlog"` - Get unplanned issues
2. `set-priority --issue-id "..." --priority 2` - Set priority
3. `add-label --issue-id "..." --label "bug"` - Categorize

### Project Tracking

1. `list-projects --team-id "..."` - Get all projects
2. `project-issues --project-id "..."` - Get project issues
3. `cycle-progress --cycle-id "..."` - Check sprint progress

## Related

- Official Linear API Documentation: https://developers.linear.app/docs/graphql/working-with-the-graphql-api
- Linear GraphQL Explorer: https://studio.apollographql.com/public/Linear-API/home
- Linear Webhook Documentation: https://developers.linear.app/docs/graphql/webhooks
