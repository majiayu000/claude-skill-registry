---
name: asana
version: 0.1.0
description: Manage Asana tasks, projects, and workspaces via MCP
triggers:
  - asana
  - task management
  - project management
  - todo list
  - assign task
  - create task
metadata:
  openclaw:
    emoji: "📋"
    apiKey:
      env: ASANA_ACCESS_TOKEN
      getFrom: https://app.asana.com/0/my-apps
---

# Asana 📋

Task and project management via the Asana MCP server.

## Setup

### 1. Get API Token

1. Go to https://app.asana.com/0/my-apps
2. Click "Create new token"
3. Name it (e.g., "OpenClaw")
4. Copy the token

### 2. Configure Gateway

Add to your OpenClaw config:

```json
{
  "env": {
    "ASANA_ACCESS_TOKEN": "your-token-here"
  }
}
```

### 3. Configure MCP Server

```bash
mcporter config add asana \
  --command "npx" \
  --arg "-y" \
  --arg "@roychri/mcp-server-asana" \
  --env "ASANA_ACCESS_TOKEN=your-token-here" \
  --scope home
```

## MCP Tools Reference

### Workspaces

```bash
# List all workspaces
mcporter call asana.asana_list_workspaces
```

### Projects

```bash
# Search projects by name pattern
mcporter call asana.asana_search_projects workspace=<workspace_gid> name_pattern=".*"

# Get project details
mcporter call asana.asana_get_project project_id=<project_gid>

# Get project sections
mcporter call asana.asana_get_project_sections project_id=<project_gid>

# Get project task counts
mcporter call asana.asana_get_project_task_counts project_id=<project_gid>
```

### Tasks

```bash
# Create task
mcporter call asana.asana_create_task \
  project_id=<project_gid> \
  name="Task name" \
  notes="Description" \
  due_on="2026-02-10" \
  assignee="me"

# Get task details
mcporter call asana.asana_get_task task_id=<task_gid>

# Update task
mcporter call asana.asana_update_task \
  task_id=<task_gid> \
  name="New name" \
  completed=true

# Create subtask
mcporter call asana.asana_create_subtask \
  parent_task_id=<task_gid> \
  name="Subtask name"

# Get multiple tasks
mcporter call asana.asana_get_multiple_tasks_by_gid task_ids='["gid1","gid2"]'
```

### Comments/Stories

```bash
# Add comment to task
mcporter call asana.asana_create_task_story \
  task_id=<task_gid> \
  text="Progress update: completed phase 1"

# Get task comments/stories
mcporter call asana.asana_get_task_stories task_id=<task_gid>
```

### Dependencies

```bash
# Add dependencies (tasks this task depends on)
mcporter call asana.asana_add_task_dependencies \
  task_id=<task_gid> \
  dependencies='["dep_gid1","dep_gid2"]'

# Add dependents (tasks that depend on this task)
mcporter call asana.asana_add_task_dependents \
  task_id=<task_gid> \
  dependents='["dep_gid1"]'
```

### Tags

```bash
# Get tags in workspace
mcporter call asana.asana_get_tags_for_workspace workspace_gid=<workspace_gid>

# Get tasks with tag
mcporter call asana.asana_get_tasks_for_tag tag_gid=<tag_gid>
```

## Direct API (for operations MCP doesn't support)

### Create Section

```bash
curl -X POST "https://app.asana.com/api/1.0/projects/<project_gid>/sections" \
  -H "Authorization: Bearer $ASANA_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"data": {"name": "Section Name"}}'
```

### Move Task to Section

```bash
curl -X POST "https://app.asana.com/api/1.0/sections/<section_gid>/addTask" \
  -H "Authorization: Bearer $ASANA_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"data": {"task": "<task_gid>"}}'
```

### Add Tag to Task

```bash
curl -X POST "https://app.asana.com/api/1.0/tasks/<task_gid>/addTag" \
  -H "Authorization: Bearer $ASANA_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"data": {"tag": "<tag_gid>"}}'
```

### Remove Tag from Task

```bash
curl -X POST "https://app.asana.com/api/1.0/tasks/<task_gid>/removeTag" \
  -H "Authorization: Bearer $ASANA_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"data": {"tag": "<tag_gid>"}}'
```

### Search Tasks (requires paid plan)

```bash
mcporter call asana.asana_search_tasks \
  workspace=<workspace_gid> \
  text="search term" \
  completed=false
```

## Local Configuration

Store your specific workspace/project IDs in `TOOLS.md`:

```markdown
## Asana

### Workspace & Project

- **Workspace:** Your Workspace (`<workspace_gid>`)
- **Project:** Your Project (`<project_gid>`)

### Sections

| Section     | GID             |
| ----------- | --------------- |
| TODO        | `<section_gid>` |
| IN PROGRESS | `<section_gid>` |
| DONE        | `<section_gid>` |

### Tags

| Tag     | GID         |
| ------- | ----------- |
| urgent  | `<tag_gid>` |
| blocked | `<tag_gid>` |
```

## Workflow Integration

This skill is designed to work with the `task-steward` workflow. See
`workflows/task-steward/AGENT.md` for:

- Task classification (Q&A vs delegated task)
- Work execution with incremental comments
- Quality verification before delivery
- Periodic task review and nudging
