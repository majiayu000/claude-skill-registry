---
name: todoist
description: Manage tasks, projects, and productivity in Todoist. View tasks, add new items, check completed work, and organize projects.
---

# Todoist Task Management

This skill provides access to Todoist via the REST API.

## Setup Required

**Get your API token:**

1. Go to Todoist Settings → Integrations → Developer
2. Or visit: https://todoist.com/app/settings/integrations/developer
3. Copy your API token

Set as environment variable:
```bash
export TODOIST_TOKEN="your-api-token"
```

## When to Use

Use this skill when the user:
- Asks about their tasks, TODOs, or what they need to do
- Wants to add a new task or reminder
- Asks about completed tasks or productivity
- Wants to organize projects or sections
- Mentions "Todoist" or their task list

## API Endpoints

Base URL: `https://api.todoist.com/rest/v2`

All requests need:
```bash
-H "Authorization: Bearer $(printenv TODOIST_TOKEN)"
```

**Important:** Use `$(printenv TODOIST_TOKEN)` to ensure the token expands correctly in all shell contexts (zsh eval can lose variable values).

### Tasks

**Get All Tasks**:
```bash
curl -s "https://api.todoist.com/rest/v2/tasks" \
  -H "Authorization: Bearer $(printenv TODOIST_TOKEN)"
```

**Get Tasks by Filter**:
```bash
curl -s -G "https://api.todoist.com/rest/v2/tasks" \
  --data-urlencode "filter=today" \
  -H "Authorization: Bearer $(printenv TODOIST_TOKEN)"
```

**Get Single Task**:
```bash
curl -s "https://api.todoist.com/rest/v2/tasks/{TASK_ID}" \
  -H "Authorization: Bearer $(printenv TODOIST_TOKEN)"
```

**Create Task**:
```bash
curl -s -X POST "https://api.todoist.com/rest/v2/tasks" \
  -H "Authorization: Bearer $(printenv TODOIST_TOKEN)" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Task name",
    "due_string": "tomorrow",
    "priority": 2
  }'
```

**Complete Task**:
```bash
curl -s -X POST "https://api.todoist.com/rest/v2/tasks/{TASK_ID}/close" \
  -H "Authorization: Bearer $(printenv TODOIST_TOKEN)"
```

### Projects

**Get All Projects**:
```bash
curl -s "https://api.todoist.com/rest/v2/projects" \
  -H "Authorization: Bearer $(printenv TODOIST_TOKEN)"
```

**Get Project**:
```bash
curl -s "https://api.todoist.com/rest/v2/projects/{PROJECT_ID}" \
  -H "Authorization: Bearer $(printenv TODOIST_TOKEN)"
```

### Sections

**Get Sections**:
```bash
curl -s "https://api.todoist.com/rest/v2/sections" \
  -H "Authorization: Bearer $(printenv TODOIST_TOKEN)"
```

**Get Sections in Project**:
```bash
curl -s "https://api.todoist.com/rest/v2/sections?project_id={PROJECT_ID}" \
  -H "Authorization: Bearer $(printenv TODOIST_TOKEN)"
```

### Labels

**Get All Labels**:
```bash
curl -s "https://api.todoist.com/rest/v2/labels" \
  -H "Authorization: Bearer $(printenv TODOIST_TOKEN)"
```

### Comments

**Get Comments on Task**:
```bash
curl -s "https://api.todoist.com/rest/v2/comments?task_id={TASK_ID}" \
  -H "Authorization: Bearer $(printenv TODOIST_TOKEN)"
```

**Add Comment**:
```bash
curl -s -X POST "https://api.todoist.com/rest/v2/comments" \
  -H "Authorization: Bearer $(printenv TODOIST_TOKEN)" \
  -H "Content-Type: application/json" \
  -d '{
    "task_id": "TASK_ID",
    "content": "Comment text"
  }'
```

## Filter Syntax

The `filter` parameter accepts Todoist filter syntax:

| Filter | Description |
|--------|-------------|
| `today` | Due today |
| `tomorrow` | Due tomorrow |
| `overdue` | Past due |
| `7 days` or `next 7 days` | Due in next 7 days |
| `no date` | No due date |
| `p1` | Priority 1 (urgent) |
| `@label_name` | Has label |
| `#project_name` | In project |
| `/section_name` | In section |
| `assigned to: me` | Assigned to you |
| `today & p1` | Combine with & |
| `today | tomorrow` | Combine with | (or) |

## Common Workflows

### Get Today's Tasks
```bash
curl -s -G "https://api.todoist.com/rest/v2/tasks" \
  --data-urlencode "filter=today" \
  -H "Authorization: Bearer $(printenv TODOIST_TOKEN)" | jq '.[] | {content, due: .due.string, priority}'
```

### Get Overdue Tasks
```bash
curl -s -G "https://api.todoist.com/rest/v2/tasks" \
  --data-urlencode "filter=overdue" \
  -H "Authorization: Bearer $(printenv TODOIST_TOKEN)"
```

### Add a Task for Tomorrow
```bash
curl -s -X POST "https://api.todoist.com/rest/v2/tasks" \
  -H "Authorization: Bearer $(printenv TODOIST_TOKEN)" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Review the PR",
    "due_string": "tomorrow",
    "priority": 2
  }'
```

### Get All Tasks in a Project
```bash
# First, find project ID
curl -s "https://api.todoist.com/rest/v2/projects" \
  -H "Authorization: Bearer $(printenv TODOIST_TOKEN)" | jq '.[] | {name, id}'

# Then get tasks
curl -s "https://api.todoist.com/rest/v2/tasks?project_id={PROJECT_ID}" \
  -H "Authorization: Bearer $(printenv TODOIST_TOKEN)"
```

### Get High Priority Tasks
```bash
curl -s -G "https://api.todoist.com/rest/v2/tasks" \
  --data-urlencode "filter=p1 | p2" \
  -H "Authorization: Bearer $(printenv TODOIST_TOKEN)"
```

### List Projects with Task Counts
```bash
curl -s "https://api.todoist.com/rest/v2/projects" \
  -H "Authorization: Bearer $(printenv TODOIST_TOKEN)" | jq '.[] | {name, id}'
```

## Task Properties

When creating tasks:
- **content**: Task text (required)
- **description**: Additional details
- **due_string**: Natural language date ("tomorrow", "every monday")
- **due_date**: Specific date (YYYY-MM-DD)
- **due_datetime**: With time (RFC3339)
- **priority**: 1 (urgent) to 4 (normal) - note: API uses 1=urgent, opposite of UI
- **project_id**: Project to add to
- **section_id**: Section within project
- **labels**: Array of label names
- **assignee_id**: For shared projects

## Notes

- API rate limit: 1000 requests per 15 minutes per user
- Priority in API: 1 = urgent (p1 in UI), 4 = normal
- Due strings support natural language in multiple languages
- Get your token at: https://todoist.com/app/settings/integrations/developer

## Sources

- [Todoist REST API Reference](https://developer.todoist.com/rest/v2/)
- [Find your API token](https://www.todoist.com/help/articles/find-your-api-token-Jpzx9IIlB)
