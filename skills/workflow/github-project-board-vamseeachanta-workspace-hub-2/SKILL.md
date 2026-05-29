---
name: github-project-board
description: Synchronize AI swarms with GitHub Projects for visual task management and progress tracking. Use for project board automation, task synchronization, sprint management, and team coordination with GitHub Projects.
---

# GitHub Project Board Sync Skill

## Overview

This skill enables synchronization between AI swarms and GitHub Projects for visual task management, progress tracking, and team coordination. It provides bidirectional sync, automated card management, and comprehensive project analytics.

**Key Capabilities:**
- Bidirectional sync between swarm tasks and project cards
- Automated card movement based on task status
- Real-time progress tracking and visualization
- Sprint management and velocity tracking
- Team workload distribution and analytics

## Quick Start

```bash
# List your GitHub Projects
gh project list --owner @me

# Get project ID
PROJECT_ID=$(gh project list --owner @me --format json | \
  jq -r '.projects[] | select(.title == "Development Board") | .number')

# Add an issue to the project
gh project item-add $PROJECT_ID --owner @me \
  --url "https://github.com/$REPO/issues/123"

# List project items
gh project item-list $PROJECT_ID --owner @me --format json
```

## When to Use

- **Task Visualization**: Creating visual boards for swarm tasks
- **Sprint Planning**: Managing sprints with automated tracking
- **Progress Tracking**: Real-time updates on task completion
- **Team Coordination**: Distributing work across team members
- **Reporting**: Generating analytics and status reports

## Usage Examples

### 1. Board Initialization

```bash
# Create a new project board
gh project create --owner @me --title "Development Board"

# Get the project number
PROJECT_NUM=$(gh project list --owner @me --format json | \
  jq -r '.projects[] | select(.title == "Development Board") | .number')

# Add custom fields for swarm tracking
gh project field-create $PROJECT_NUM --owner @me \
  --name "Swarm Status" \
  --data-type "SINGLE_SELECT" \
  --single-select-options "pending,in_progress,review,completed"

gh project field-create $PROJECT_NUM --owner @me \
  --name "Agent Type" \
  --data-type "SINGLE_SELECT" \
  --single-select-options "coder,tester,analyst,architect,reviewer"

gh project field-create $PROJECT_NUM --owner @me \
  --name "Priority" \
  --data-type "SINGLE_SELECT" \
  --single-select-options "critical,high,medium,low"
```

### 2. Task Synchronization

```bash
# Import issues with specific label to project
gh issue list --label "enhancement" --json number,title,url | \
  jq -r '.[].url' | while read -r url; do
    gh project item-add $PROJECT_NUM --owner @me --url "$url"
  done

# Update item status based on issue state
gh project item-list $PROJECT_NUM --owner @me --format json | \
  jq -r '.items[] | select(.content.type == "Issue") | "\(.id) \(.content.number)"' | \
  while read -r item_id issue_num; do
    STATE=$(gh issue view $issue_num --json state --jq '.state')
    if [ "$STATE" == "CLOSED" ]; then
      gh project item-edit --project-id $PROJECT_ID --id $item_id \
        --field-id $STATUS_FIELD_ID --single-select-option-id $COMPLETED_ID
    fi
  done
```

### 3. Progress Tracking

```bash
# Get project progress summary
gh project item-list $PROJECT_NUM --owner @me --format json | \
  jq '{
    total: .items | length,
    completed: [.items[] | select(.fieldValues[]?.name == "completed")] | length,
    in_progress: [.items[] | select(.fieldValues[]?.name == "in_progress")] | length,
    pending: [.items[] | select(.fieldValues[]?.name == "pending")] | length
  }'

# Post progress comment to tracking issue
PROGRESS=$(gh project item-list $PROJECT_NUM --owner @me --format json | \
  jq -r '"## Sprint Progress\n- Total: \(.items | length)\n- Completed: \([.items[] | select(.status == "Done")] | length)"')

gh issue comment $TRACKING_ISSUE --body "$PROGRESS"
```

### 4. Sprint Management

```bash
# Create sprint milestone
gh api repos/:owner/:repo/milestones \
  -f title="Sprint 24" \
  -f description="Sprint 24 - Jan 6-19, 2026" \
  -f due_on="2026-01-19T23:59:59Z"

# Assign issues to sprint
gh issue edit 123 --milestone "Sprint 24"
gh issue edit 124 --milestone "Sprint 24"

# Get sprint burndown data
gh issue list --milestone "Sprint 24" --state all --json number,state,closedAt,createdAt | \
  jq 'group_by(.state) | map({state: .[0].state, count: length})'
```

## Board Configuration

### Status Mapping

```yaml
# .github/board-sync.yml
version: 1
project:
  name: "Development Board"
  number: 1

mapping:
  status:
    pending: "Backlog"
    assigned: "Ready"
    in_progress: "In Progress"
    review: "Review"
    completed: "Done"
    blocked: "Blocked"

  agents:
    coder: "Development"
    tester: "Testing"
    analyst: "Analysis"
    designer: "Design"
    architect: "Architecture"

  priority:
    critical: "P0 - Critical"
    high: "P1 - High"
    medium: "P2 - Medium"
    low: "P3 - Low"
```

### View Configuration

```json
{
  "views": [
    {
      "name": "Swarm Overview",
      "type": "board",
      "groupBy": "status",
      "filters": ["is:open"],
      "sort": "priority:desc"
    },
    {
      "name": "Agent Workload",
      "type": "table",
      "groupBy": "assignedAgent",
      "columns": ["title", "status", "priority", "eta"],
      "sort": "eta:asc"
    },
    {
      "name": "Sprint Roadmap",
      "type": "roadmap",
      "dateField": "dueDate",
      "groupBy": "milestone"
    }
  ]
}
```

## MCP Tool Integration

### Swarm-Board Synchronization

```javascript
// Initialize project board sync swarm

// Store board configuration
  action: "store",
  key: "board/config",
  value: {
    projectId: "PVT_xxx",
    statusMapping: {
      "pending": "Backlog",
      "in_progress": "In Progress",
      "completed": "Done"
    },
    syncInterval: "5m"
  }
}

// Create sync workflow
  name: "Board Sync Workflow",
  steps: [
    { name: "Fetch swarm tasks", agent: "coordinator" },
    { name: "Update board cards", agent: "coordinator" },
    { name: "Analyze progress", agent: "analyst" },
    { name: "Report status", agent: "monitor" }
  ],
  triggers: ["on_task_update", "scheduled_5min"]
}
```

### GitHub Integration

```javascript
// Analyze repository for project setup
  repo: "owner/repo",
  analysis_type: "code_quality"
}

// Track issues
  repo: "owner/repo",
  action: "list"
}

// Get repository metrics
  repo: "owner/repo"
}
```

## Automation Features

### Auto-Assignment Rules

```bash
# Assign cards based on labels
gh project item-list $PROJECT_NUM --owner @me --format json | \
  jq -r '.items[] | select(.content.labels[]?.name == "frontend") | .id' | \
  while read -r item_id; do
    # Update assignment field
    gh project item-edit --project-id $PROJECT_ID --id $item_id \
      --field-id $ASSIGNEE_FIELD_ID --text "frontend-team"
  done
```

### Smart Card Movement

```bash
# Auto-move cards when PR is merged
gh pr list --state merged --json number,headRefName | \
  jq -r '.[] | select(.headRefName | startswith("feature/")) | .number' | \
  while read -r pr_num; do
    # Find linked issue and update project card
    ISSUE=$(gh pr view $pr_num --json body --jq '.body' | grep -oE '#[0-9]+' | head -1)
    if [ -n "$ISSUE" ]; then
      # Update card status to Done
      echo "Moving card for issue $ISSUE to Done"
    fi
  done
```

## Analytics and Reporting

### Generate Board Analytics

```bash
# Collect metrics
METRICS=$(gh project item-list $PROJECT_NUM --owner @me --format json | jq '{
  total_items: .items | length,
  by_status: .items | group_by(.status) | map({status: .[0].status, count: length}),
  by_assignee: .items | group_by(.assignee) | map({assignee: .[0].assignee, count: length}),
  avg_cycle_time: "5.2 days"
}')

# Create analytics report
cat << EOF > sprint-report.md
# Sprint Analytics Report

## Summary
$(echo "$METRICS" | jq -r '"- Total Items: \(.total_items)"')

## Status Distribution
$(echo "$METRICS" | jq -r '.by_status[] | "- \(.status): \(.count)"')

## Workload Distribution
$(echo "$METRICS" | jq -r '.by_assignee[] | "- \(.assignee): \(.count)"')

---
Generated: $(date)
EOF
```

### KPI Tracking

```bash
# Track key performance indicators
gh api graphql -f query='
  query($project: Int!, $owner: String!) {
    user(login: $owner) {
      projectV2(number: $project) {
        items(first: 100) {
          nodes {
            fieldValues(first: 10) {
              nodes {
                ... on ProjectV2ItemFieldSingleSelectValue {
                  name
                  field { ... on ProjectV2SingleSelectField { name } }
                }
              }
            }
          }
        }
      }
    }
  }
' -f owner="@me" -f project="$PROJECT_NUM"
```

## Best Practices

### 1. Board Organization
- Define clear column/status definitions
- Use consistent labeling system
- Regular board grooming (weekly)
- Set WIP limits for each column

### 2. Data Integrity
- Bidirectional sync validation
- Conflict resolution strategies
- Regular backups of board state
- Audit trail for changes

### 3. Team Adoption
- Provide training materials
- Define clear workflows
- Regular retrospectives
- Feedback collection mechanisms

### 4. Performance
- Archive completed items regularly
- Limit items per view
- Use field indexes
- Cache frequently accessed data

## Troubleshooting

### Common Issues

**Issue: Cards not syncing**
```bash
# Check project permissions
gh project view $PROJECT_NUM --owner @me

# Verify webhook configuration
gh api repos/:owner/:repo/hooks
```

**Issue: Field values not updating**
```bash
# List available fields
gh project field-list $PROJECT_NUM --owner @me

# Check field IDs
gh api graphql -f query='
  query { viewer { projectV2(number: 1) { fields(first: 20) { nodes { ... on ProjectV2SingleSelectField { id name options { id name } } } } } } }
'
```

## Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| sync-mode | string | "bidirectional" | Sync direction |
| update-frequency | string | "5m" | Sync interval |
| auto-archive | boolean | true | Archive completed items |
| wip-limits | object | {} | WIP limits per column |

## Related Skills

- [github-swarm-issue](../github-swarm-issue/SKILL.md) - Issue-based coordination
- [github-swarm-pr](../github-swarm-pr/SKILL.md) - PR management
- [github-sync](../github-sync/SKILL.md) - Repository synchronization

---

## Version History

- **1.0.0** (2026-01-02): Initial skill conversion from project-board-sync agent
