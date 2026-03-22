---
name: af-linear-api-expertise
description: Use when interacting with Linear for issue tracking, workflow management, or team operations. Prefer linearis CLI for common operations; GraphQL for advanced queries.

# AgentFlow documentation fields
title: Linear API Expertise
created: 2026-02-05
updated: 2026-02-05
last_checked: 2026-02-05
tags: [skill, expertise, linear, api, cli, graphql, issues, workflow]
parent: ../README.md
related:
  - ./af-work-management-expertise/SKILL.md
  - ../../docs/guides/work-management.md
---

# Linear API Expertise

## Tool Preference Order

1. **`linearis` CLI** (recommended) - Simple, handles state name→UUID automatically
2. **GraphQL API** - For operations the CLI doesn't support
3. **Linear MCP** - Avoid, currently flaky

### CLI vs GraphQL Capabilities

| Operation | linearis CLI | GraphQL API |
|-----------|--------------|-------------|
| Read/search issues | ✅ | ✅ |
| Update issue state | ✅ | ✅ |
| Create issues | ✅ | ✅ |
| Add comments | ✅ | ✅ |
| List teams | ✅ | ✅ |
| **Create teams** | ❌ | ✅ |
| **Create workflow states** | ❌ | ✅ |
| **Delete/archive states** | ❌ | ✅ |
| **Issue relations** | ❌ | ✅ |
| **Issue history** | ❌ | ✅ |
| **Create labels** | ❌ | ✅ |
| **Team setup scripts** | ❌ | ✅ |

Use CLI for day-to-day operations. Use GraphQL for team/project setup and advanced queries.

## When to Use This Skill

Load this skill when you need to:
- Create, read, update, or search Linear issues
- Transition issues through workflow states
- Add comments to issues
- Manage workflow states (create custom statuses)
- Query team information

## Quick Reference - linearis CLI

For most common operations, use the CLI:

```bash
# Read issue
linearis issues read AF-96

# Update state
linearis issues update AF-96 --state "In Progress"
linearis issues update AF-96 --state "Waiting for Feedback"

# Add comment
linearis issues comment AF-96 "Progress update: completed implementation"

# Create issue - ALWAYS use team UUID, not abbreviation (abbreviations route to wrong team)
# Look up UUID: project-registry <project> linear.team_id
linearis issues create --team "79b48ab6-d677-4f3a-8228-86e30ce923a3" "[Feature] New capability" -d "Details..."

# Search
linearis issues search "team:AF state:\"In Progress\""
```

## GraphQL API (for advanced queries)

Use GraphQL when the CLI doesn't support the operation (e.g., history, relations, team setup).

### API Endpoint

```
https://api.linear.app/graphql
```

### Authentication

```bash
# Via environment variable (recommended)
curl -X POST https://api.linear.app/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: $LINEAR_API_KEY" \
  -d '{"query": "..."}'
```

**Get your API key:** Linear Settings → Security & Access → API → Personal API keys

### Issue ID Formats

- **UUID**: `2d40be5c-72ea-432e-a222-e169c7e8e21d` (internal)
- **Identifier**: `AF-96` (human-readable, works in most queries)

---

## Part 1: Reading Data

### Get Single Issue

```bash
curl -s -X POST https://api.linear.app/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: $LINEAR_API_KEY" \
  -d '{
    "query": "query GetIssue($id: String!) { issue(id: $id) { id identifier title description state { name } assignee { name } team { key name } labels { nodes { name } } comments { nodes { body createdAt user { name } } } } }",
    "variables": { "id": "AF-96" }
  }' | jq
```

### Search Issues

```bash
curl -s -X POST https://api.linear.app/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: $LINEAR_API_KEY" \
  -d '{
    "query": "query SearchIssues($query: String!, $first: Int) { searchIssues(query: $query, first: $first) { nodes { id identifier title state { name } } } }",
    "variables": { "query": "team:AF state:\"In Progress\"", "first": 10 }
  }' | jq
```

**Search syntax:**
- `team:AF` - Filter by team key
- `state:"In Progress"` - Filter by state name
- `assignee:@me` - Assigned to current user
- `label:bug` - Has specific label

### List Teams

```bash
curl -s -X POST https://api.linear.app/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: $LINEAR_API_KEY" \
  -d '{
    "query": "{ teams { nodes { id key name } } }"
  }' | jq
```

### Get Workflow States for a Team

```bash
curl -s -X POST https://api.linear.app/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: $LINEAR_API_KEY" \
  -d '{
    "query": "query GetStates($teamId: String!) { team(id: $teamId) { states { nodes { id name type position color } } } }",
    "variables": { "teamId": "TEAM_UUID" }
  }' | jq
```

**State types:** `backlog`, `unstarted`, `started`, `completed`, `canceled`

---

## Part 2: Writing Data

### Update Issue State

```bash
curl -s -X POST https://api.linear.app/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: $LINEAR_API_KEY" \
  -d '{
    "query": "mutation UpdateIssue($id: String!, $stateId: String!) { issueUpdate(id: $id, input: { stateId: $stateId }) { success issue { id identifier state { name } } } }",
    "variables": { "id": "AF-96", "stateId": "STATE_UUID" }
  }' | jq
```

**To find state UUID**, query workflow states for the team first.

### Create Issue

```bash
curl -s -X POST https://api.linear.app/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: $LINEAR_API_KEY" \
  -d '{
    "query": "mutation CreateIssue($title: String!, $teamId: String!, $description: String) { issueCreate(input: { title: $title, teamId: $teamId, description: $description }) { success issue { id identifier url } } }",
    "variables": {
      "title": "[Feature] - New capability description",
      "teamId": "TEAM_UUID",
      "description": "## Business Context\n\n## Acceptance Criteria\n- [ ] Criterion 1"
    }
  }' | jq
```

### Add Comment to Issue

```bash
curl -s -X POST https://api.linear.app/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: $LINEAR_API_KEY" \
  -d '{
    "query": "mutation AddComment($issueId: String!, $body: String!) { commentCreate(input: { issueId: $issueId, body: $body }) { success comment { id body } } }",
    "variables": {
      "issueId": "AF-96",
      "body": "Progress update:\n- Completed initial implementation\n- Tests passing"
    }
  }' | jq
```

### Create Workflow State

```bash
curl -s -X POST https://api.linear.app/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: $LINEAR_API_KEY" \
  -d '{
    "query": "mutation CreateState($teamId: String!, $name: String!, $type: String!, $color: String!) { workflowStateCreate(input: { teamId: $teamId, name: $name, type: $type, color: $color }) { success workflowState { id name type color } } }",
    "variables": {
      "teamId": "TEAM_UUID",
      "name": "Waiting for Feedback",
      "type": "started",
      "color": "#f59e0b"
    }
  }' | jq
```

**State types:**
- `backlog` - Not started, low priority
- `unstarted` - Not started, scheduled
- `started` - In progress
- `completed` - Done successfully
- `canceled` - Won't do

---

## Part 3: Helper Scripts

### Get State ID by Name

```bash
# Get the UUID for a state by name (e.g., "In Progress")
get_state_id() {
  local team_id="$1"
  local state_name="$2"
  curl -s -X POST https://api.linear.app/graphql \
    -H "Content-Type: application/json" \
    -H "Authorization: $LINEAR_API_KEY" \
    -d "{
      \"query\": \"query { team(id: \\\"$team_id\\\") { states { nodes { id name } } } }\"
    }" | jq -r ".data.team.states.nodes[] | select(.name == \"$state_name\") | .id"
}

# Usage: get_state_id "TEAM_UUID" "In Progress"
```

### Update Issue State by Name

```bash
# Combined: update issue to a named state
update_issue_state() {
  local issue_id="$1"
  local state_name="$2"

  # First get the issue's team
  local team_id=$(curl -s -X POST https://api.linear.app/graphql \
    -H "Content-Type: application/json" \
    -H "Authorization: $LINEAR_API_KEY" \
    -d "{\"query\": \"{ issue(id: \\\"$issue_id\\\") { team { id } } }\"}" \
    | jq -r '.data.issue.team.id')

  # Get the state ID
  local state_id=$(get_state_id "$team_id" "$state_name")

  # Update the issue
  curl -s -X POST https://api.linear.app/graphql \
    -H "Content-Type: application/json" \
    -H "Authorization: $LINEAR_API_KEY" \
    -d "{
      \"query\": \"mutation { issueUpdate(id: \\\"$issue_id\\\", input: { stateId: \\\"$state_id\\\" }) { success } }\"
    }" | jq
}

# Usage: update_issue_state "AF-96" "In Progress"
```

---

## Part 4: AgentFlow Workflow Patterns

### Linear States in AgentFlow

```
Discovered → Refining → Approved → In Progress → In Review → Dev → Test → Live
    │           │          │             │            │         │      │      │
 backlog     started   unstarted      started      started   ←── completed ──→
```

### State Transitions

| From | To | When |
|------|-------|------|
| Discovered | Refining | Starting requirements analysis |
| Refining | Approved | Human approves mini-PRD |
| Approved | In Progress | Developer starts work |
| In Progress | In Review | PR created |
| In Review | Dev | PR merged to develop |
| Dev | Test | Deployed to test |
| Test | Live | Deployed to production |

### Common Patterns

**Starting work:**
```bash
# Update to "In Progress"
curl -s -X POST https://api.linear.app/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: $LINEAR_API_KEY" \
  -d '{"query": "mutation { issueUpdate(id: \"AF-96\", input: { stateId: \"STATE_UUID_FOR_IN_PROGRESS\" }) { success } }"}'
```

**Waiting for feedback:**
```bash
# Update to "Waiting for Feedback" (custom state)
# Add comment explaining what's needed
curl -s -X POST https://api.linear.app/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: $LINEAR_API_KEY" \
  -d '{"query": "mutation { commentCreate(input: { issueId: \"AF-96\", body: \"Waiting for approval on approach\" }) { success } }"}'
```

**PR created:**
```bash
# Update to "In Review" and add PR link
curl -s -X POST https://api.linear.app/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: $LINEAR_API_KEY" \
  -d '{"query": "mutation { issueUpdate(id: \"AF-96\", input: { stateId: \"STATE_UUID_FOR_IN_REVIEW\" }) { success } }"}'

curl -s -X POST https://api.linear.app/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: $LINEAR_API_KEY" \
  -d '{"query": "mutation { commentCreate(input: { issueId: \"AF-96\", body: \"PR created: https://github.com/...\" }) { success } }"}'
```

**Applying approval labels:**
```bash
# Get label ID by name
LABEL_ID=$(curl -s -X POST https://api.linear.app/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: $LINEAR_API_KEY" \
  -d '{"query": "{ issueLabels(filter: { name: { eq: \"approval:bdd-pending\" } }) { nodes { id name } } }"}' \
  | jq -r '.data.issueLabels.nodes[0].id')

# Apply label to issue (adds to existing labels)
curl -s -X POST https://api.linear.app/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: $LINEAR_API_KEY" \
  -d "{\"query\": \"mutation { issueAddLabel(id: \\\"ISSUE_ID\\\", labelId: \\\"$LABEL_ID\\\") { success } }\"}"

# Remove label from issue
curl -s -X POST https://api.linear.app/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: $LINEAR_API_KEY" \
  -d "{\"query\": \"mutation { issueRemoveLabel(id: \\\"ISSUE_ID\\\", labelId: \\\"$LABEL_ID\\\") { success } }\"}"
```

---

## Part 5: Team Setup

### AgentFlow Workflow State Definitions

AgentFlow uses a standardized set of workflow states. Colors are from the reference implementation (MIN project).

| State | Type | Color | Position | Purpose |
|-------|------|-------|----------|---------|
| Discovered | backlog | #bec2c8 | 0 | New feature identified, needs exploration |
| Refining | started | #5e6ad2 | 1 | Refinement phase in progress |
| Approved | unstarted | #bec2c8 | 2 | Refinement approved, ready for implementation |
| In Progress | started | #f2c94c | 3 | Active development |
| Waiting for Feedback | started | #eb5757 | 4 | Blocked on human input (agent automation) |
| In Review | started | #0f783c | 5 | PR created, code review |
| Dev | completed | #f2c94c | 6 | Merged to develop (feature branch only) |
| Test | completed | #26b5ce | 7 | Deployed to test environment (feature branch only) |
| Live | completed | #5e6ad2 | 8 | Released to production |
| Canceled | canceled | #95a2b3 | 9 | Won't do |
| Duplicate | canceled | #95a2b3 | 10 | Duplicate of another issue |

### Development Model States

**Trunk-based development** (single environment):
- All states except Dev and Test
- Flow: ... → In Review → Live

**Feature branch development** (multiple environments):
- All states including Dev and Test
- Flow: ... → In Review → Dev → Test → Live

### Create Team

```bash
curl -s -X POST https://api.linear.app/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: $LINEAR_API_KEY" \
  -d '{
    "query": "mutation CreateTeam($name: String!, $key: String!, $cyclesEnabled: Boolean) { teamCreate(input: { name: $name, key: $key, cyclesEnabled: $cyclesEnabled }) { success team { id key name } } }",
    "variables": {
      "name": "My Project",
      "key": "MPR",
      "cyclesEnabled": true
    }
  }' | jq
```

**Key rules:**
- `key` must be 2-5 uppercase letters
- `key` must be unique across the organization
- `cyclesEnabled: true` recommended for sprint planning

### Delete Default Workflow State

After creating a team, Linear adds default states (Backlog, Todo, In Progress, Done, Canceled). Delete the ones that conflict with AgentFlow states.

```bash
curl -s -X POST https://api.linear.app/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: $LINEAR_API_KEY" \
  -d '{
    "query": "mutation DeleteState($stateId: String!) { workflowStateArchive(id: $stateId) { success } }",
    "variables": { "stateId": "STATE_UUID_TO_DELETE" }
  }' | jq
```

**Note:** You cannot delete a state if issues are assigned to it. Move issues first or use `workflowStateArchive` instead.

### Create Label

```bash
curl -s -X POST https://api.linear.app/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: $LINEAR_API_KEY" \
  -d '{
    "query": "mutation CreateLabel($teamId: String!, $name: String!, $color: String) { issueLabelCreate(input: { teamId: $teamId, name: $name, color: $color }) { success issueLabel { id name } } }",
    "variables": {
      "teamId": "TEAM_UUID",
      "name": "phase:discovery",
      "color": "#5e6ad2"
    }
  }' | jq
```

### AgentFlow Standard Labels

| Label | Color | Purpose |
|-------|-------|---------|
| phase:setup | #95a2b3 | Setup phase work |
| phase:discovery | #5e6ad2 | Discovery phase work |
| phase:requirements | #f2c94c | Refinement phase work |
| phase:delivery | #0f783c | Delivery phase work |
| type:feature | #5e6ad2 | New functionality |
| type:bug | #eb5757 | Bug fix |
| type:improvement | #26b5ce | Enhancement to existing |
| type:documentation | #bec2c8 | Documentation work |
| approval:bdd-pending | #f59e0b | BDD scenarios pending review |
| approval:bdd-approved | #0f783c | BDD scenarios approved |
| approval:ux-pending | #f59e0b | UX design pending review |
| approval:ux-approved | #0f783c | UX design approved |

### Complete Team Setup Script

```bash
#!/bin/bash
# Setup AgentFlow team in Linear
# Usage: ./setup-linear-team.sh "Project Name" "KEY" [trunk|feature]

PROJECT_NAME="$1"
TEAM_KEY="$2"
DEV_MODEL="${3:-feature}"  # Default to feature branch

# 1. Create team
echo "Creating team: $PROJECT_NAME ($TEAM_KEY)..."
TEAM_RESULT=$(curl -s -X POST https://api.linear.app/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: $LINEAR_API_KEY" \
  -d "{
    \"query\": \"mutation { teamCreate(input: { name: \\\"$PROJECT_NAME\\\", key: \\\"$TEAM_KEY\\\", cyclesEnabled: true }) { success team { id } } }\"
  }")

TEAM_ID=$(echo "$TEAM_RESULT" | jq -r '.data.teamCreate.team.id')
if [ "$TEAM_ID" == "null" ]; then
  echo "Error creating team: $(echo "$TEAM_RESULT" | jq -r '.errors[0].message')"
  exit 1
fi
echo "Created team with ID: $TEAM_ID"

# 2. Get and archive default states
echo "Archiving default states..."
DEFAULT_STATES=$(curl -s -X POST https://api.linear.app/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: $LINEAR_API_KEY" \
  -d "{\"query\": \"{ team(id: \\\"$TEAM_ID\\\") { states { nodes { id name } } } }\"}" \
  | jq -r '.data.team.states.nodes[] | "\(.id)|\(.name)"')

while IFS='|' read -r state_id state_name; do
  echo "  Archiving: $state_name"
  curl -s -X POST https://api.linear.app/graphql \
    -H "Content-Type: application/json" \
    -H "Authorization: $LINEAR_API_KEY" \
    -d "{\"query\": \"mutation { workflowStateArchive(id: \\\"$state_id\\\") { success } }\"}" > /dev/null
done <<< "$DEFAULT_STATES"

# 3. Create AgentFlow states
echo "Creating AgentFlow workflow states..."

create_state() {
  local name="$1" type="$2" color="$3" position="$4"
  curl -s -X POST https://api.linear.app/graphql \
    -H "Content-Type: application/json" \
    -H "Authorization: $LINEAR_API_KEY" \
    -d "{
      \"query\": \"mutation { workflowStateCreate(input: { teamId: \\\"$TEAM_ID\\\", name: \\\"$name\\\", type: \\\"$type\\\", color: \\\"$color\\\", position: $position }) { success } }\"
    }" > /dev/null
  echo "  Created: $name"
}

create_state "Discovered" "backlog" "#bec2c8" 0
create_state "Refining" "started" "#5e6ad2" 1
create_state "Approved" "unstarted" "#bec2c8" 2
create_state "In Progress" "started" "#f2c94c" 3
create_state "Waiting for Feedback" "started" "#eb5757" 4
create_state "In Review" "started" "#0f783c" 5

if [ "$DEV_MODEL" == "feature" ]; then
  create_state "Dev" "completed" "#f2c94c" 6
  create_state "Test" "completed" "#26b5ce" 7
fi

create_state "Live" "completed" "#5e6ad2" 8
create_state "Canceled" "canceled" "#95a2b3" 9
create_state "Duplicate" "canceled" "#95a2b3" 10

# 4. Create labels
echo "Creating labels..."

create_label() {
  local name="$1" color="$2"
  curl -s -X POST https://api.linear.app/graphql \
    -H "Content-Type: application/json" \
    -H "Authorization: $LINEAR_API_KEY" \
    -d "{
      \"query\": \"mutation { issueLabelCreate(input: { teamId: \\\"$TEAM_ID\\\", name: \\\"$name\\\", color: \\\"$color\\\" }) { success } }\"
    }" > /dev/null
  echo "  Created: $name"
}

create_label "phase:setup" "#95a2b3"
create_label "phase:discovery" "#5e6ad2"
create_label "phase:requirements" "#f2c94c"
create_label "phase:delivery" "#0f783c"
create_label "type:feature" "#5e6ad2"
create_label "type:bug" "#eb5757"
create_label "type:improvement" "#26b5ce"
create_label "type:documentation" "#bec2c8"
create_label "approval:bdd-pending" "#f59e0b"
create_label "approval:bdd-approved" "#0f783c"
create_label "approval:ux-pending" "#f59e0b"
create_label "approval:ux-approved" "#0f783c"

echo ""
echo "✅ Team setup complete!"
echo "   Team: $PROJECT_NAME ($TEAM_KEY)"
echo "   ID: $TEAM_ID"
echo "   Model: $DEV_MODEL"
echo ""
echo "Add to project registry:"
echo "  linear:"
echo "    team_key: \"$TEAM_KEY\""
echo "    team_id: \"$TEAM_ID\""
```

---

## Best Practices

### For AI Agents

1. **Cache team and state UUIDs** - Query once at session start, reuse throughout
2. **Use issue identifiers** (e.g., `AF-96`) not UUIDs for readability
3. **Add comments for audit trail** - Document decisions and progress
4. **Check response success** - Always verify `success: true` in mutations
5. **Use search for discovery** - `searchIssues` is powerful for finding related work

### Error Handling

```bash
# Check for errors in response
response=$(curl -s -X POST https://api.linear.app/graphql ...)
if echo "$response" | jq -e '.errors' > /dev/null; then
  echo "Error: $(echo "$response" | jq -r '.errors[0].message')"
  exit 1
fi
```

### Rate Limits

- Linear has rate limits (currently generous for most use cases)
- Batch operations when possible (`issueBatchUpdate`)
- Cache responses when data doesn't change frequently

---

## Troubleshooting

### "Entity not found"
- Check issue identifier is correct (case-sensitive)
- Ensure you have access to the team

### "Invalid state transition"
- Some Linear workflows enforce state ordering
- Check team's workflow settings

### "Unauthorized"
- Verify `LINEAR_API_KEY` is set and valid
- Check API key has required scopes

---

## Essential Reading

- [Linear GraphQL API Docs](https://linear.app/developers)
- [Work Management Guide](../../docs/guides/work-management.md)
- [Work Management Expertise](./af-work-management-expertise/SKILL.md)

---

**Remember:**
1. **Prefer `linearis` CLI** for common operations (read, update state, comment, create)
2. **Use GraphQL API** only for advanced operations (history, relations, team setup)
3. **Avoid Linear MCP** - currently flaky
4. Issue identifiers (e.g., `AF-96`) work in CLI and most GraphQL queries
5. Always add comments for traceability
