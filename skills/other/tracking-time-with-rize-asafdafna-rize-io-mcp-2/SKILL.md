---
name: tracking-time-with-rize
description: Track time, manage clients/projects/tasks, and analyze productivity using Rize.io via MCP. Use when the user mentions time tracking, logging work hours, productivity analysis, focus time, or managing Rize entities (clients, projects, tasks).
---

# Rize Time Tracking Skill

This skill enables AI agents to interact with Rize.io for time tracking and productivity management through the Rize MCP server.

## When to Use This Skill

- User asks about time tracking or logging hours
- User wants to create/update/delete clients, projects, or tasks
- User asks about productivity, focus time, or work summaries
- User mentions Rize explicitly
- User wants to analyze how time was spent

## MCP Server Reference

Server name: `rize` (may vary based on user configuration)

## Available Tools

### Reading Data

| Tool | Purpose | When to Use |
|------|---------|-------------|
| `rize:rize_get_current_user` | Get authenticated user info | Verify connection, get user details |
| `rize:rize_list_clients` | List all clients | Before creating entities, to check existing |
| `rize:rize_list_projects` | List all projects | Find project IDs, check what exists |
| `rize:rize_list_tasks` | List all tasks | Find task IDs for time logging |
| `rize:rize_get_time_entries` | Get time entries for date range | Review logged time, calculate totals |
| `rize:rize_get_summaries` | Get focus/meeting/break time | Productivity analysis, capacity checks |
| `rize:rize_get_current_session` | Get active tracking session | Check what's currently being tracked |
| `rize:rize_get_sessions` | Get all sessions for date range | Detailed work pattern analysis |

### Creating Entities

| Tool | Purpose | Required Params |
|------|---------|-----------------|
| `rize:rize_create_client` | Create new client | `name`, `teamName` |
| `rize:rize_create_project` | Create new project | `name`, optional `clientName`, `teamName` |
| `rize:rize_create_task` | Create new task | `name`, optional `projectName`, `teamName` |
| `rize:rize_create_task_time_entry` | Log time to task | `taskId`, `startTime`, `endTime` |

### Updating Entities

| Tool | Purpose | Required Params |
|------|---------|-----------------|
| `rize:rize_update_client` | Update client | `id`, optional `name`, `status` |
| `rize:rize_update_project` | Update project | `id`, optional `name`, `clientName`, `status` |
| `rize:rize_update_task` | Update task | `id`, optional `name`, `projectName`, `status` |

### Deleting Entities

| Tool | Purpose | Required Params |
|------|---------|-----------------|
| `rize:rize_delete_client` | Delete client | `id` |
| `rize:rize_delete_project` | Delete project | `id` |
| `rize:rize_delete_task` | Delete task | `id` |

## Entity Hierarchy

```
Team
  └── Client (business relationship)
        └── Project (work stream)
              └── Task (trackable unit of work)
```

## Common Workflows

### Check Existing Before Creating

Always check if an entity exists before creating:

```
1. Use rize:rize_list_clients to check existing clients
2. Use rize:rize_list_projects to check existing projects
3. Only create if the entity doesn't exist
```

### Log Time to a Task

```
1. Use rize:rize_list_tasks to find the task ID
2. Use rize:rize_create_task_time_entry with:
   - taskId: the task's ID
   - startTime: ISO8601 format (e.g., "2026-01-15T09:00:00Z")
   - endTime: ISO8601 format (e.g., "2026-01-15T10:30:00Z")
   - description: optional work description
   - billable: optional boolean
```

### Analyze Productivity

```
1. Use rize:rize_get_summaries with date range and bucketSize (day/week/month)
2. Returns: focusTime, meetingTime, breakTime, trackedTime, workHours (in seconds)
3. Convert seconds to hours: divide by 3600
```

### Get Time Breakdown by Client

```
1. Use rize:rize_get_time_entries with date range
2. Group entries by task.project.client.name
3. Sum durations (in seconds) per client
```

## Important Notes

### Team Name Parameter

Most create/update operations require `teamName`. This is the Rize team the user belongs to. If unknown, use `rize:rize_list_clients` first - the team name appears in the response.

### Time Formats

- Dates: `YYYY-MM-DD` (e.g., "2026-01-15")
- DateTimes: ISO8601 (e.g., "2026-01-15T09:00:00Z")
- Durations in responses: seconds (divide by 3600 for hours)

### Approved vs Pending Entries

The API only returns **approved** time entries. Suggested/pending entries from Rize's auto-tracking must be approved in the Rize app before they appear via API.

### Status Values

For update operations, valid status values are typically:
- `active` - Entity is in use
- `archived` - Entity is hidden but preserved

## Error Handling

If a tool returns an error:
1. Check that required parameters are provided
2. Verify IDs exist using list tools
3. Ensure teamName is correct for create operations
4. Check date formats are valid

## Reference Files

For detailed examples and advanced patterns, see:
- [examples.md](./examples.md) - Common usage patterns with sample responses
