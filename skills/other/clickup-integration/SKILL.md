---
name: clickup-integration
description: |
  ClickUp integration patterns for task management.
  Covers API authentication, webhooks, task sync, and MCP integration.
  Use this skill when implementing ClickUp features or syncing sessions with tasks.
allowed-tools: Read, Glob, Grep, Bash
version: 1.0.0
---

# ClickUp Integration Skill

Integration patterns for syncing development sessions with ClickUp tasks.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                     CLICKUP INTEGRATION                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐     ┌──────────────┐     ┌──────────────┐     │
│  │   Claude    │────►│  MCP Server  │────►│   ClickUp    │     │
│  │   Session   │◄────│  (clickup)   │◄────│     API      │     │
│  └─────────────┘     └──────────────┘     └──────────────┘     │
│         │                                        │              │
│         ▼                                        ▼              │
│  ┌─────────────┐                         ┌──────────────┐      │
│  │  Session    │                         │   Webhooks   │      │
│  │  Files      │                         │  (optional)  │      │
│  └─────────────┘                         └──────────────┘      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## When to Use This Skill

- Setting up ClickUp integration for the first time
- Syncing development sessions with ClickUp tasks
- Creating tasks from Claude sessions
- Updating task status automatically
- Reading task details and comments

---

## Configuration

### .claude/config/workspace.json

```json
{
  "taskManager": {
    "enabled": true,
    "provider": "clickup",
    "syncWithSession": true,
    "autoUpdateStatus": true,
    "config": {
      "apiKey": "${CLICKUP_API_KEY}",
      "workspaceId": "your-workspace-id",
      "defaultSpace": "your-default-space-id",
      "useMcp": true,
      "mcpFallback": true
    }
  }
}
```

### Environment Variables

```bash
# .env.local
CLICKUP_API_KEY=pk_xxxxxxxx_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

---

## MCP Server Integration

ClickUp provides an MCP server for Claude Code integration.

### Setup

```bash
# Add MCP server to Claude Code
claude mcp add clickup
```

### Available MCP Tools

| Tool | Description | Parameters |
|------|-------------|------------|
| `clickup_get_task` | Get task details | `task_id` |
| `clickup_create_task` | Create new task | `list_id`, `name`, `description`, etc. |
| `clickup_update_task` | Update task | `task_id`, fields to update |
| `clickup_create_task_comment` | Add comment | `task_id`, `comment_text` |
| `clickup_get_lists` | Get lists in folder | `folder_id` |
| `clickup_get_folders` | Get folders in space | `space_id` |

### Example Usage

```typescript
// Get task details via MCP
const task = await mcp.clickup.get_task({ task_id: "abc123" });

// Create task via MCP
const newTask = await mcp.clickup.create_task({
  list_id: "12345678",
  name: "Implement user authentication",
  description: "Add OAuth2 support",
  priority: 2,
  tags: ["feature", "auth"]
});
```

---

## API Patterns

### Authentication

```typescript
// API Key authentication
const headers = {
  'Authorization': process.env.CLICKUP_API_KEY,
  'Content-Type': 'application/json'
};

// Base URL
const BASE_URL = 'https://api.clickup.com/api/v2';
```

### Common Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/team` | GET | Get authorized teams/workspaces |
| `/team/{team_id}/space` | GET | Get spaces in workspace |
| `/space/{space_id}/folder` | GET | Get folders in space |
| `/folder/{folder_id}/list` | GET | Get lists in folder |
| `/list/{list_id}/task` | GET/POST | Get/Create tasks |
| `/task/{task_id}` | GET/PUT/DELETE | Task operations |
| `/task/{task_id}/comment` | GET/POST | Task comments |

### Task Structure

```typescript
interface ClickUpTask {
  id: string;
  custom_id: string | null;
  name: string;
  description: string;
  status: {
    status: string;
    color: string;
    type: string;
  };
  priority: {
    id: string;
    priority: string;
    color: string;
  };
  assignees: Array<{
    id: number;
    username: string;
    email: string;
  }>;
  tags: Array<{
    name: string;
    tag_fg: string;
    tag_bg: string;
  }>;
  due_date: string | null;
  start_date: string | null;
  time_estimate: number | null;
  custom_fields: Array<{
    id: string;
    name: string;
    value: any;
  }>;
  url: string;
}
```

---

## Session Sync Patterns

### Linking Session to Task

```markdown
# In requirements.md

## ClickUp Task
- **Task ID:** abc123
- **URL:** https://app.clickup.com/t/abc123
- **Status:** In Progress
```

### Auto-Update Status

When `autoUpdateStatus: true`, Claude updates task status:

| Session Event | ClickUp Status |
|---------------|----------------|
| Session created | "In Progress" |
| Blocked | "Blocked" |
| Session closed (success) | "Complete" |
| Session closed (partial) | "Review" |

### Comment Sync

```typescript
// Post session progress as comment
await mcp.clickup.create_task_comment({
  task_id: "abc123",
  comment_text: `
## Session Progress Update

**Phase:** Backend Development
**Progress:** 60%

### Completed
- API endpoints created
- Tests written

### In Progress
- Frontend components

### Blocked
- None
  `.trim()
});
```

---

## Webhook Configuration

### Setting Up Webhooks

```typescript
// Create webhook for task updates
POST /team/{team_id}/webhook
{
  "endpoint": "https://your-app.com/api/webhooks/clickup",
  "events": [
    "taskCreated",
    "taskUpdated",
    "taskDeleted",
    "taskStatusUpdated",
    "taskCommentPosted"
  ]
}
```

### Webhook Events

| Event | Trigger |
|-------|---------|
| `taskCreated` | New task created |
| `taskUpdated` | Task details changed |
| `taskStatusUpdated` | Status changed |
| `taskCommentPosted` | New comment added |
| `taskAssigneeUpdated` | Assignee changed |
| `taskDueDateUpdated` | Due date changed |

### Handling Webhooks

```typescript
// app/api/webhooks/clickup/route.ts
export async function POST(request: Request) {
  const payload = await request.json();

  switch (payload.event) {
    case 'taskStatusUpdated':
      // Handle status change
      break;
    case 'taskCommentPosted':
      // Handle new comment
      break;
  }

  return Response.json({ received: true });
}
```

---

## Rate Limiting

### Limits

| Plan | Rate Limit |
|------|------------|
| Free | 100 requests/minute |
| Unlimited | 100 requests/minute |
| Business | 100 requests/minute |
| Enterprise | 1000 requests/minute |

### Handling Rate Limits

```typescript
// Check rate limit headers
const remaining = response.headers.get('X-RateLimit-Remaining');
const reset = response.headers.get('X-RateLimit-Reset');

if (remaining === '0') {
  const waitTime = parseInt(reset) - Date.now();
  await sleep(waitTime);
}
```

---

## Error Handling

### Common Error Codes

| Code | Description | Resolution |
|------|-------------|------------|
| 401 | Unauthorized | Check API key |
| 403 | Forbidden | Check permissions |
| 404 | Not found | Verify task/list ID |
| 429 | Rate limited | Wait and retry |
| 500 | Server error | Retry with backoff |

### Error Response Format

```json
{
  "err": "Task not found",
  "ECODE": "TASK_024"
}
```

---

## Testing Patterns

### Mock API Responses

```typescript
// __mocks__/clickup.ts
export const mockTask = {
  id: "abc123",
  name: "Test Task",
  status: { status: "Open", color: "#d3d3d3" },
  priority: { priority: "normal" }
};

export const mockGetTask = jest.fn().mockResolvedValue(mockTask);
```

### Integration Tests

```typescript
describe('ClickUp Integration', () => {
  it('should fetch task details', async () => {
    const task = await clickup.getTask('abc123');
    expect(task.name).toBeDefined();
  });

  it('should create task', async () => {
    const task = await clickup.createTask({
      listId: '12345',
      name: 'New Task'
    });
    expect(task.id).toBeDefined();
  });
});
```

---

## Anti-Patterns

### DON'T: Hardcode API Keys

```typescript
// BAD
const apiKey = 'pk_12345_abcdef';

// GOOD
const apiKey = process.env.CLICKUP_API_KEY;
```

### DON'T: Ignore Rate Limits

```typescript
// BAD
for (const task of tasks) {
  await updateTask(task);
}

// GOOD
for (const task of tasks) {
  await updateTask(task);
  await sleep(100); // Respect rate limits
}
```

### DON'T: Store Sensitive Data in Tasks

```typescript
// BAD - Don't put secrets in task descriptions
description: `API Key: ${apiKey}`

// GOOD - Reference environment variables
description: `Uses API key from CLICKUP_API_KEY env var`
```

---

## Checklist

Before using ClickUp integration:

- [ ] API key configured in environment
- [ ] Workspace ID set in `.claude/config/workspace.json`
- [ ] Default space configured
- [ ] MCP server added (if using MCP)
- [ ] Webhook endpoint set up (if using webhooks)
- [ ] Error handling implemented
- [ ] Rate limiting considered

---

## Related Skills

- `session-management` - Session lifecycle
- `scheduled-actions` - Background task processing
- `service-layer` - API implementation patterns
