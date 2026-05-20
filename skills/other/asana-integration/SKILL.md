---
name: asana-integration
description: |
  Asana integration patterns for work management.
  Covers Personal Access Tokens, webhooks, and task management.
  Use this skill when implementing Asana features or syncing sessions with tasks.
allowed-tools: Read, Glob, Grep, Bash
version: 1.0.0
---

# Asana Integration Skill

Integration patterns for syncing development sessions with Asana tasks.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                       ASANA INTEGRATION                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐     ┌──────────────┐     ┌──────────────┐     │
│  │   Claude    │────►│   REST API   │────►│    Asana     │     │
│  │   Session   │◄────│   Client     │◄────│    Cloud     │     │
│  └─────────────┘     └──────────────┘     └──────────────┘     │
│         │                                        │              │
│         ▼                                        ▼              │
│  ┌─────────────┐                         ┌──────────────┐      │
│  │  Session    │                         │   Webhooks   │      │
│  │  Files      │                         │              │      │
│  └─────────────┘                         └──────────────┘      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## When to Use This Skill

- Setting up Asana integration for the first time
- Syncing development sessions with Asana tasks
- Creating tasks from Claude sessions
- Updating task completion status
- Managing projects and sections

---

## Configuration

### .claude/config/workspace.json

```json
{
  "taskManager": {
    "enabled": true,
    "provider": "asana",
    "syncWithSession": true,
    "autoUpdateStatus": true,
    "config": {
      "accessToken": "${ASANA_ACCESS_TOKEN}",
      "defaultWorkspace": "your-workspace-gid",
      "defaultProject": "your-project-gid"
    }
  }
}
```

### Environment Variables

```bash
# .env.local
ASANA_ACCESS_TOKEN=1/12345678901234:abcdefghijklmnop...
```

---

## Authentication

### Personal Access Token (PAT)

```typescript
// Bearer token authentication
const headers = {
  'Authorization': `Bearer ${process.env.ASANA_ACCESS_TOKEN}`,
  'Content-Type': 'application/json',
  'Accept': 'application/json'
};

// Base URL
const BASE_URL = 'https://app.asana.com/api/1.0';
```

### OAuth 2.0

```typescript
// For OAuth apps
const authUrl = 'https://app.asana.com/-/oauth_authorize';
const tokenUrl = 'https://app.asana.com/-/oauth_token';

// Exchange code for token
const response = await fetch(tokenUrl, {
  method: 'POST',
  headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
  body: new URLSearchParams({
    grant_type: 'authorization_code',
    client_id: process.env.ASANA_CLIENT_ID,
    client_secret: process.env.ASANA_CLIENT_SECRET,
    redirect_uri: 'https://your-app.com/callback',
    code: authorizationCode
  })
});
```

---

## API Patterns

### Common Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/users/me` | GET | Get current user |
| `/workspaces` | GET | List workspaces |
| `/projects` | GET | List projects |
| `/projects/{gid}` | GET | Get project details |
| `/projects/{gid}/tasks` | GET | List tasks in project |
| `/tasks` | POST | Create task |
| `/tasks/{gid}` | GET/PUT/DELETE | Task operations |
| `/tasks/{gid}/stories` | GET/POST | Task comments/activity |
| `/sections` | GET | List sections |

### Task Structure

```typescript
interface AsanaTask {
  gid: string;
  name: string;
  notes: string; // Plain text description
  html_notes: string; // HTML description
  completed: boolean;
  completed_at: string | null;
  due_on: string | null; // YYYY-MM-DD
  due_at: string | null; // ISO datetime
  start_on: string | null;
  assignee: {
    gid: string;
    name: string;
    email: string;
  } | null;
  projects: Array<{
    gid: string;
    name: string;
  }>;
  memberships: Array<{
    project: { gid: string; name: string };
    section: { gid: string; name: string };
  }>;
  tags: Array<{
    gid: string;
    name: string;
    color: string;
  }>;
  custom_fields: Array<{
    gid: string;
    name: string;
    type: string;
    enum_value?: { gid: string; name: string };
    number_value?: number;
    text_value?: string;
  }>;
  permalink_url: string;
}
```

---

## Session Sync Patterns

### Linking Session to Task

```markdown
# In requirements.md

## Asana Task
- **Task GID:** 1234567890123456
- **URL:** https://app.asana.com/0/project-gid/1234567890123456
- **Status:** In Progress (via section)
```

### Task Management

Asana uses sections for status (unlike status fields):

```typescript
// Move task to section (change status)
await fetch(`${BASE_URL}/sections/${sectionGid}/addTask`, {
  method: 'POST',
  headers,
  body: JSON.stringify({
    data: { task: taskGid }
  })
});

// Mark task complete
await fetch(`${BASE_URL}/tasks/${taskGid}`, {
  method: 'PUT',
  headers,
  body: JSON.stringify({
    data: { completed: true }
  })
});
```

### Section Mapping

| Session Event | Asana Action |
|---------------|--------------|
| Session created | Move to "In Progress" section |
| Blocked | Move to "Blocked" section |
| Session closed (success) | Mark completed |
| Session closed (partial) | Move to "Review" section |

### Adding Stories (Comments)

```typescript
// Add comment to task
await fetch(`${BASE_URL}/tasks/${taskGid}/stories`, {
  method: 'POST',
  headers,
  body: JSON.stringify({
    data: {
      text: `
## Session Progress Update

**Phase:** Backend Development
**Progress:** 60%

### Completed
- API endpoints created
- Tests written

### In Progress
- Frontend components
      `.trim()
    }
  })
});
```

---

## Webhook Configuration

### Creating Webhooks

```typescript
// Create webhook
const webhook = await fetch(`${BASE_URL}/webhooks`, {
  method: 'POST',
  headers,
  body: JSON.stringify({
    data: {
      resource: projectGid, // What to watch
      target: 'https://your-app.com/api/webhooks/asana',
      filters: [
        { resource_type: 'task', action: 'changed' },
        { resource_type: 'task', action: 'added' },
        { resource_type: 'story', action: 'added' }
      ]
    }
  })
});
```

### Webhook Handshake

Asana requires a handshake to verify webhook endpoint:

```typescript
// app/api/webhooks/asana/route.ts
export async function POST(request: Request) {
  // Handle handshake
  const hookSecret = request.headers.get('X-Hook-Secret');
  if (hookSecret) {
    return new Response(null, {
      status: 200,
      headers: { 'X-Hook-Secret': hookSecret }
    });
  }

  // Verify signature
  const signature = request.headers.get('X-Hook-Signature');
  const body = await request.text();
  // Verify HMAC-SHA256 signature...

  const payload = JSON.parse(body);

  for (const event of payload.events) {
    switch (event.action) {
      case 'changed':
        // Handle task update
        break;
      case 'added':
        // Handle new task/comment
        break;
    }
  }

  return Response.json({ received: true });
}
```

### Event Types

| Resource | Action | Trigger |
|----------|--------|---------|
| task | added | Task created |
| task | changed | Task updated |
| task | removed | Task deleted |
| task | undeleted | Task restored |
| story | added | Comment/activity added |

---

## Custom Fields

### Reading Custom Fields

```typescript
// Get task with custom fields
const response = await fetch(
  `${BASE_URL}/tasks/${taskGid}?opt_fields=custom_fields,custom_fields.name,custom_fields.enum_value`,
  { headers }
);
const { data: task } = await response.json();

// Find specific field
const statusField = task.custom_fields.find(f => f.name === 'Status');
console.log(statusField.enum_value?.name); // "In Progress"
```

### Updating Custom Fields

```typescript
// Update custom field value
await fetch(`${BASE_URL}/tasks/${taskGid}`, {
  method: 'PUT',
  headers,
  body: JSON.stringify({
    data: {
      custom_fields: {
        [customFieldGid]: enumOptionGid // For enum fields
        // or
        [customFieldGid]: 42 // For number fields
        // or
        [customFieldGid]: "text value" // For text fields
      }
    }
  })
});
```

---

## Rate Limiting

### Limits

| Type | Limit |
|------|-------|
| Standard | 1500 requests/minute |
| Free tier | 150 requests/minute |
| Per-user | Based on plan |

### Headers

```typescript
// Asana uses retry-after for rate limits
const retryAfter = response.headers.get('Retry-After');
if (response.status === 429) {
  await sleep(parseInt(retryAfter) * 1000);
  // Retry request
}
```

---

## Error Handling

### Common Error Codes

| Code | Description | Resolution |
|------|-------------|------------|
| 400 | Bad request | Check request body |
| 401 | Unauthorized | Check token |
| 403 | Forbidden | Check permissions |
| 404 | Not found | Verify GID |
| 429 | Rate limited | Wait and retry |
| 500 | Server error | Retry with backoff |

### Error Response Format

```json
{
  "errors": [
    {
      "message": "task: Unknown object: 1234567890",
      "help": "For more information on API status codes..."
    }
  ]
}
```

---

## Testing Patterns

### Mock API Responses

```typescript
// __mocks__/asana.ts
export const mockTask = {
  gid: "1234567890123456",
  name: "Test Task",
  completed: false,
  assignee: { gid: "user-gid", name: "Test User" }
};

export const mockGetTask = jest.fn().mockResolvedValue({ data: mockTask });
```

### Integration Tests

```typescript
describe('Asana Integration', () => {
  it('should fetch task details', async () => {
    const task = await asana.getTask('1234567890123456');
    expect(task.name).toBeDefined();
  });

  it('should complete task', async () => {
    await asana.completeTask('1234567890123456');
    const task = await asana.getTask('1234567890123456');
    expect(task.completed).toBe(true);
  });
});
```

---

## Anti-Patterns

### DON'T: Forget opt_fields

```typescript
// BAD - Returns minimal data
const task = await fetch(`${BASE_URL}/tasks/${gid}`);

// GOOD - Request needed fields
const task = await fetch(
  `${BASE_URL}/tasks/${gid}?opt_fields=name,notes,assignee,completed,custom_fields`
);
```

### DON'T: Poll for Changes

```typescript
// BAD - Polling wastes resources
setInterval(async () => {
  const tasks = await getTasks();
  // Check for changes...
}, 5000);

// GOOD - Use webhooks
await createWebhook(projectGid, callbackUrl);
```

---

## Checklist

Before using Asana integration:

- [ ] Personal Access Token generated
- [ ] Workspace GID configured
- [ ] Default project set
- [ ] Section GIDs mapped for status workflow
- [ ] Custom field GIDs identified (if used)
- [ ] Webhook endpoint set up (if needed)
- [ ] Webhook handshake implemented
- [ ] opt_fields used in all requests

---

## Related Skills

- `session-management` - Session lifecycle
- `scheduled-actions` - Background task processing
- `service-layer` - API implementation patterns
