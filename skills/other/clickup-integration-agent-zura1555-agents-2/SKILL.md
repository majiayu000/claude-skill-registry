---
name: clickup-integration-agent
description: "Specialized agent for ClickUp integration using the @taazkareem/clickup-mcp-server. Handles task management, time tracking, and workspace operations through 36 MCP tools."
version: 1.0.0
author: "Thuong-Tuan Tran"
tags: [clickup, task-management, mcp, time-tracking]
---

# ClickUp Integration Agent

## Overview

The **ClickUp Integration Agent** provides comprehensive ClickUp functionality through the `@taazkareem/clickup-mcp-server` MCP server. It enables monitoring, reporting, and issue management workflows with full access to ClickUp's features.

## Core Capabilities

This agent leverages **36 MCP tools** provided by the ClickUp MCP server:

### Task Management
- **create_task**: Create new tasks with assignees, tags, due dates
- **update_task**: Update task properties (name, description, status, priority)
- **get_task**: Retrieve task details and metadata
- **get_tasks**: List tasks from lists or workspace with filtering
- **create_bulk_tasks**: Create multiple tasks efficiently
- **update_bulk_tasks**: Update multiple tasks simultaneously
- **move_task**: Move tasks between lists
- **duplicate_task**: Duplicate existing tasks
- **delete_task**: Remove tasks
- **get_task_comments**: Retrieve task comments
- **create_task_comment**: Add comments to tasks
- **attach_task_file**: Upload file attachments

### Workspace Management
- **get_workspace_hierarchy**: Navigate spaces, folders, lists structure
- **create_list**: Create new lists
- **create_list_in_folder**: Create lists within folders
- **get_list**: Retrieve list details
- **update_list**: Modify list properties
- **delete_list**: Remove lists
- **create_folder**: Create new folders
- **get_folder**: Retrieve folder details
- **update_folder**: Modify folder properties
- **delete_folder**: Remove folders

### Time Tracking
- **get_task_time_entries**: View time tracking entries
- **start_time_tracking**: Start timer on tasks
- **stop_time_tracking**: Stop active timers
- **add_time_entry**: Manual time entry
- **delete_time_entry**: Remove time entries
- **get_current_time_entry**: Check active timer

### Tag Management
- **get_space_tags**: List workspace tags
- **create_space_tag**: Create new tags
- **update_space_tag**: Modify tags
- **delete_space_tag**: Remove tags
- **add_tag_to_task**: Add tags to tasks
- **remove_tag_from_task**: Remove tags from tasks

### Member Management
- **get_workspace_members**: List team members
- **find_member_by_name**: Find users by name/email
- **resolve_assignees**: Convert names/emails to user IDs

### Document Management
- **create_document**: Create ClickUp docs
- **get_document**: Retrieve document content
- **list_documents**: List workspace documents
- **list_document_pages**: View document structure
- **get_document_pages**: Get page content
- **create_document_pages**: Create new pages
- **update_document_page**: Modify page content

## MCP Server Configuration

### Environment Variables Required

```bash
CLICKUP_API_KEY="your-api-key"
CLICKUP_TEAM_ID="your-team-id"
ENABLED_TOOLS="create_task,get_task,update_task,get_workspace_hierarchy,get_tasks,create_task_comment,get_task_time_entries"
DOCUMENT_SUPPORT="true"
```

### MCP Server Connection

The agent connects to the ClickUp MCP server using:

```json
{
  "mcpServers": {
    "ClickUp": {
      "command": "npx",
      "args": ["-y", "@taazkareem/clickup-mcp-server@latest"],
      "env": {
        "CLICKUP_API_KEY": "your-api-key",
        "CLICKUP_TEAM_ID": "your-team-id"
      }
    }
  }
}
```

## Usage in Workflow

### Phase 1: Discovery & Data Collection

**Purpose:** Collect ClickUp workspace data

**Tools Used:**
1. `get_workspace_hierarchy` - Get all spaces, folders, lists
2. `get_tasks` - Fetch tasks from relevant lists
3. `get_workspace_members` - Get team member data
4. `get_task_time_entries` - Retrieve time tracking data

**Example Usage:**
```bash
# Get workspace structure
mcp__clickup__get_workspace_hierarchy

# Get all tasks from a list
mcp__clickup__get_tasks --list_id "list-123"

# Get team members
mcp__clickup__get_workspace_members
```

**Output:**
```json
{
  "spaces": [...],
  "folders": [...],
  "lists": [...],
  "tasks": [...],
  "members": [...],
  "timeEntries": [...]
}
```

### Phase 2: Analysis

**Purpose:** Process and analyze collected data

**Activities:**
- Calculate velocity metrics
- Identify bottlenecks
- Analyze time tracking patterns
- Detect blockers and issues

### Phase 3: Action Execution

**Monitoring:**
- `get_tasks` with filtering for changes
- `get_task_comments` for activity tracking
- `get_current_time_entry` for active work

**Issue Management:**
- `create_task` - Create new tasks
- `update_task` - Update task status/properties
- `move_task` - Reorganize tasks
- `add_tag_to_task` - Categorize tasks
- `create_task_comment` - Add comments/updates

**Time Tracking:**
- `get_task_time_entries` - Report on time spent
- `start_time_tracking` / `stop_time_tracking` - Manage timers
- `add_time_entry` - Manual time logging

**Examples:**
```bash
# Create a task
mcp__clickup__create_task \
  --list_id "list-123" \
  --name "Implement new feature" \
  --description "Feature description" \
  --assignees ["user@example.com"] \
  --priority 1

# Update task status
mcp__clickup__update_task \
  --task_id "task-456" \
  --status "in_progress"

# Add comment
mcp__clickup__create_task_comment \
  --task_id "task-456" \
  --comment_text "Update: Working on this now"
```

## Integration with Orchestrator

The orchestrator (`project-master-orchestrator`) calls this agent through file-based communication:

**Input:** ClickUp-specific parameters from `global-state.json`
**Output:** ClickUp data and operation results in `data/clickup-collected.json`

### Request Format
```json
{
  "action": "collect|update|manage",
  "list_id": "list-123",
  "task_data": {
    "name": "Task name",
    "description": "Description",
    "assignees": ["user@example.com"]
  }
}
```

### Response Format
```json
{
  "status": "success|error",
  "data": {...},
  "errors": [...],
  "metrics": {
    "tasks_processed": 10,
    "api_calls_made": 5,
    "execution_time": 2.3
  }
}
```

## State Management

### State File Location
`project-workspace/active-projects/{workflow-id}/data/clickup-collected.json`

### State Contents
```json
{
  "timestamp": "2025-12-02T14:30:22.000Z",
  "workspace": {
    "spaces": [...],
    "folders": [...],
    "lists": [...]
  },
  "tasks": {
    "total": 50,
    "by_status": {
      "todo": 10,
      "in_progress": 15,
      "review": 5,
      "done": 20
    },
    "recent_changes": [...]
  },
  "time_tracking": {
    "total_hours": 120,
    "by_user": {...},
    "by_task": {...}
  },
  "team": {
    "members": [...],
    "activity": {...}
  }
}
```

## Error Handling

### Common Errors

**Authentication Error:**
- **Issue:** Invalid CLICKUP_API_KEY or CLICKUP_TEAM_ID
- **Solution:** Verify credentials in MCP server configuration
- **Retry:** Yes (up to 3 attempts with backoff)

**Rate Limiting:**
- **Issue:** API rate limits exceeded
- **Solution:** Implement exponential backoff
- **Retry:** Yes (automatic in MCP server)

**Resource Not Found:**
- **Issue:** Invalid task_id, list_id, or other ID
- **Solution:** Verify IDs in workspace
- **Retry:** No (fix input data)

**Network Error:**
- **Issue:** Connection to MCP server failed
- **Solution:** Verify MCP server is running
- **Retry:** Yes (up to 3 attempts)

### Error Response Format
```json
{
  "status": "error",
  "error_type": "authentication|rate_limit|not_found|network",
  "error_message": "Detailed error description",
  "retry_count": 0,
  "timestamp": "2025-12-02T14:30:22.000Z"
}
```

## Monitoring Features

### Real-Time Event Tracking

The agent can track:
- Task creation/updates/deletions
- Status changes
- Comment additions
- Time tracking events
- Assignment changes

### Usage for Monitoring
```bash
# Get recent tasks
mcp__clickup__get_tasks --list_id "list-123"

# Filter for recent changes (client-side processing)
# Monitor active time entries
mcp__clickup__get_current_time_entry --task_id "task-456"

# Check task comments for updates
mcp__clickup__get_task_comments --task_id "task-456"
```

## Performance Characteristics

### Execution Time
- **get_workspace_hierarchy**: ~1-2 seconds
- **get_tasks** (list): ~2-3 seconds
- **get_task_time_entries**: ~2-4 seconds
- **create_task**: ~1-2 seconds
- **update_task**: ~1-2 seconds

### Rate Limits
- Handled automatically by MCP server
- No manual rate limiting needed
- Exponential backoff on 429 responses

### Batch Operations
- **create_bulk_tasks**: Up to 100 tasks per request
- **update_bulk_tasks**: Up to 100 tasks per request
- Significantly faster than individual calls

## Security Considerations

### Authentication
- API keys stored in environment variables
- Never commit credentials to version control
- Rotate API keys regularly (every 90 days)

### Access Control
- Verify team membership before operations
- Respect ClickUp permissions
- Use least-privilege principle

### Data Privacy
- Don't log sensitive task content
- Sanitize logs of PII
- Follow ClickUp's data handling policies

## Testing

### Test Coverage
- All task operations
- Workspace navigation
- Time tracking features
- Tag management
- Member management

### Test Scenarios
1. **Happy Path:**
   - Create task, update, add comment, delete
   - Fetch workspace hierarchy
   - Time tracking lifecycle

2. **Error Handling:**
   - Invalid IDs
   - Authentication failures
   - Rate limiting scenarios

3. **Edge Cases:**
   - Empty lists/folders
   - Large task sets (pagination)
   - Concurrent updates

## Best Practices

### Task Management
1. Always validate assignee emails exist using `find_member_by_name`
2. Use `create_bulk_tasks` for creating multiple tasks
3. Include meaningful descriptions
4. Use consistent naming conventions

### Time Tracking
1. Start/stop timers promptly
2. Add manual entries for missed time
3. Use consistent tracking granularity (hours vs days)

### Workspace Organization
1. Keep list structure simple (< 3 levels deep)
2. Use tags for flexible categorization
3. Document list purposes and conventions

### Performance
1. Use batch operations when possible
2. Cache frequently accessed data (lists, members)
3. Paginate through large task sets
4. Avoid N+1 query patterns

## Integration Examples

### Example 1: Daily Standup Report
```bash
# Collect data
mcp__clickup__get_workspace_hierarchy
mcp__clickup__get_tasks --list_id "daily-standup-list"

# Analyze
# - Completed tasks (status: "done")
# - In-progress tasks (status: "in_progress")
# - Blocked tasks (no assignee or overdue)

# Generate report
```

### Example 2: Sprint Planning
```bash
# Get backlog tasks
mcp__clickup__get_tasks --list_id "backlog" --status "todo"

# Get team capacity
mcp__clickup__get_workspace_members

# Create sprint tasks
mcp__clickup__create_bulk_tasks --list_id "sprint-24" --tasks [...]

# Assign tasks
# (Batch assignment via update_bulk_tasks)
```

### Example 3: Weekly Report
```bash
# Time tracking summary
for task_id in sprint_tasks:
    mcp__clickup__get_task_time_entries --task_id task_id

# Calculate velocity
# - Tasks completed this week
# - Points/story points completed
# - Team member contributions

# Generate metrics
```

## Future Enhancements

**Planned Features:**
- Custom field support
- Webhook integration for real-time updates
- Advanced filtering and search
- Automation rule support
- Integration with other ClickUp features (goals, etc.)

**Version History:**
- v1.0.0 - Initial release with 36 MCP tools
- v1.1.0 - (Planned) Enhanced filtering
- v1.2.0 - (Planned) Webhook support

## Resources

### MCP Server
- GitHub: https://github.com/taazkareem/clickup-mcp-server
- Smithery: https://smithery.ai/server/@taazkareem/clickup-mcp-server

### ClickUp API Documentation
- Official ClickUp API Docs: https://clickup.com/api
- ClickUp Help Center: https://help.clickup.com

### Tools Reference
- Full tool list: 36 tools available
- Task Management: 12 tools
- Workspace Management: 10 tools
- Time Tracking: 6 tools
- Tag Management: 6 tools
- Member Management: 3 tools
- Document Management: 7 tools

## Troubleshooting

### Common Issues

**Issue:** "MCP server not found"
- **Solution:** Verify npx installation and server availability
- **Check:** `npm list -g @taazkareem/clickup-mcp-server`

**Issue:** "Invalid API Key"
- **Solution:** Verify CLICKUP_API_KEY environment variable
- **Check:** API key permissions in ClickUp

**Issue:** "Team ID not found"
- **Solution:** Verify CLICKUP_TEAM_ID
- **Find:** In ClickUp workspace URL or Settings

**Issue:** Tools not responding
- **Solution:** Check MCP server logs
- **Restart:** Kill and restart MCP server process

**Issue:** Rate limiting errors
- **Solution:** None needed - MCP server handles automatically
- **Monitor:** Check rate limit status with MCP tools

### Debug Mode
Enable verbose logging:
```bash
export CLICKUP_DEBUG=true
# Restart MCP server
```

---

**Author:** Thuong-Tuan Tran
**Version:** 1.0.0
**Last Updated:** 2025-12-02
