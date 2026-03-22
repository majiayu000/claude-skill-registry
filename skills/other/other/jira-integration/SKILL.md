---
name: jira-integration
description: |
  Jira integration patterns for project management.
  Covers REST API, webhooks, JQL queries, and automation.
  Use this skill when implementing Jira features or syncing sessions with issues.
allowed-tools: Read, Glob, Grep, Bash
version: 1.0.0
---

# Jira Integration Skill

Integration patterns for syncing development sessions with Jira issues.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                       JIRA INTEGRATION                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐     ┌──────────────┐     ┌──────────────┐     │
│  │   Claude    │────►│   REST API   │────►│    Jira      │     │
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

- Setting up Jira integration for the first time
- Syncing development sessions with Jira issues
- Creating issues from Claude sessions
- Updating issue status via transitions
- Querying issues with JQL

---

## Configuration

### .claude/config/workspace.json

```json
{
  "taskManager": {
    "enabled": true,
    "provider": "jira",
    "syncWithSession": true,
    "autoUpdateStatus": true,
    "config": {
      "domain": "your-domain.atlassian.net",
      "email": "${JIRA_EMAIL}",
      "apiToken": "${JIRA_API_TOKEN}",
      "defaultProject": "PROJ"
    }
  }
}
```

### Environment Variables

```bash
# .env.local
JIRA_EMAIL=your-email@company.com
JIRA_API_TOKEN=ATATT3xFfGF0...
JIRA_DOMAIN=your-domain.atlassian.net
```

---

## Authentication

### API Token Authentication

```typescript
// Basic auth with email:token
const auth = Buffer.from(
  `${process.env.JIRA_EMAIL}:${process.env.JIRA_API_TOKEN}`
).toString('base64');

const headers = {
  'Authorization': `Basic ${auth}`,
  'Content-Type': 'application/json',
  'Accept': 'application/json'
};

// Base URL
const BASE_URL = `https://${process.env.JIRA_DOMAIN}/rest/api/3`;
```

### OAuth 2.0 (Atlassian Connect)

```typescript
// For Atlassian Connect apps
const headers = {
  'Authorization': `Bearer ${accessToken}`,
  'Content-Type': 'application/json'
};
```

---

## API Patterns

### Common Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/myself` | GET | Get current user |
| `/project` | GET | List all projects |
| `/project/{key}` | GET | Get project details |
| `/search` | GET/POST | Search issues (JQL) |
| `/issue` | POST | Create issue |
| `/issue/{issueKey}` | GET/PUT/DELETE | Issue operations |
| `/issue/{issueKey}/transitions` | GET/POST | Get/Execute transitions |
| `/issue/{issueKey}/comment` | GET/POST | Issue comments |

### Issue Structure

```typescript
interface JiraIssue {
  id: string;
  key: string;
  self: string;
  fields: {
    summary: string;
    description: {
      type: 'doc';
      version: 1;
      content: Array<any>; // Atlassian Document Format
    };
    issuetype: {
      id: string;
      name: string;
    };
    status: {
      id: string;
      name: string;
      statusCategory: {
        key: string;
        name: string;
      };
    };
    priority: {
      id: string;
      name: string;
    };
    assignee: {
      accountId: string;
      displayName: string;
      emailAddress: string;
    } | null;
    reporter: {
      accountId: string;
      displayName: string;
    };
    labels: string[];
    customfield_XXXXX: any; // Custom fields
  };
}
```

---

## JQL Query Patterns

### Basic Queries

```jql
-- Issues in project
project = PROJ

-- My open issues
assignee = currentUser() AND status != Done

-- Recent issues
created >= -7d

-- By status category
statusCategory = "In Progress"

-- With labels
labels in (feature, urgent)
```

### Complex Queries

```jql
-- Issues for sprint
project = PROJ
  AND sprint in openSprints()
  AND status != Done
  ORDER BY priority DESC

-- Blocked issues
project = PROJ
  AND status = Blocked
  AND updated <= -2d

-- Search in text
project = PROJ
  AND (summary ~ "authentication" OR description ~ "authentication")
```

### API Usage

```typescript
// Search with JQL
const response = await fetch(
  `${BASE_URL}/search?jql=${encodeURIComponent(jql)}&maxResults=50`,
  { headers }
);
const { issues, total } = await response.json();
```

---

## Session Sync Patterns

### Linking Session to Issue

```markdown
# In requirements.md

## Jira Issue
- **Issue Key:** PROJ-123
- **URL:** https://your-domain.atlassian.net/browse/PROJ-123
- **Status:** In Progress
```

### Status Transitions

```typescript
// Get available transitions
const transitions = await fetch(
  `${BASE_URL}/issue/PROJ-123/transitions`,
  { headers }
);

// Execute transition
await fetch(
  `${BASE_URL}/issue/PROJ-123/transitions`,
  {
    method: 'POST',
    headers,
    body: JSON.stringify({
      transition: { id: "31" }, // "In Progress" transition ID
      fields: {
        // Optional: update fields during transition
        assignee: { accountId: "xxx" }
      },
      update: {
        comment: [{
          add: {
            body: {
              type: "doc",
              version: 1,
              content: [{
                type: "paragraph",
                content: [{
                  type: "text",
                  text: "Started development session"
                }]
              }]
            }
          }
        }]
      }
    })
  }
);
```

### Auto-Update Status Map

| Session Event | Jira Transition |
|---------------|-----------------|
| Session created | "Start Progress" |
| Blocked | "Flag" or custom |
| Session closed (success) | "Done" |
| Session closed (partial) | "In Review" |

---

## Atlassian Document Format (ADF)

Jira uses ADF for rich text fields.

### Basic Structure

```typescript
const adfContent = {
  type: "doc",
  version: 1,
  content: [
    {
      type: "paragraph",
      content: [
        { type: "text", text: "Hello " },
        { type: "text", text: "world", marks: [{ type: "strong" }] }
      ]
    },
    {
      type: "bulletList",
      content: [
        {
          type: "listItem",
          content: [
            {
              type: "paragraph",
              content: [{ type: "text", text: "Item 1" }]
            }
          ]
        }
      ]
    }
  ]
};
```

### Common Node Types

| Type | Usage |
|------|-------|
| `paragraph` | Text block |
| `heading` | H1-H6 headers |
| `bulletList` | Unordered list |
| `orderedList` | Numbered list |
| `codeBlock` | Code snippet |
| `table` | Table structure |
| `mention` | @mention user |

---

## Webhook Configuration

### Setting Up Webhooks

Jira webhooks are configured in Project Settings > Webhooks.

```typescript
// Webhook payload structure
interface JiraWebhook {
  timestamp: number;
  webhookEvent: string;
  issue_event_type_name: string;
  user: {
    accountId: string;
    displayName: string;
  };
  issue: JiraIssue;
  changelog?: {
    items: Array<{
      field: string;
      fromString: string;
      toString: string;
    }>;
  };
}
```

### Webhook Events

| Event | Trigger |
|-------|---------|
| `jira:issue_created` | Issue created |
| `jira:issue_updated` | Issue updated |
| `jira:issue_deleted` | Issue deleted |
| `comment_created` | Comment added |
| `sprint_started` | Sprint started |
| `sprint_closed` | Sprint ended |

### Handling Webhooks

```typescript
// app/api/webhooks/jira/route.ts
export async function POST(request: Request) {
  const payload: JiraWebhook = await request.json();

  switch (payload.webhookEvent) {
    case 'jira:issue_updated':
      if (payload.changelog?.items.some(i => i.field === 'status')) {
        // Handle status change
      }
      break;
    case 'comment_created':
      // Handle new comment
      break;
  }

  return Response.json({ received: true });
}
```

---

## Rate Limiting

### Limits

| Type | Limit |
|------|-------|
| REST API | 100 requests/minute (varies by plan) |
| Concurrent | 10 concurrent requests |
| Bulk operations | 1000 issues/request |

### Headers

```typescript
// Check rate limit headers
const remaining = response.headers.get('X-RateLimit-Remaining');
const limit = response.headers.get('X-RateLimit-Limit');
```

---

## Error Handling

### Common Error Codes

| Code | Description | Resolution |
|------|-------------|------------|
| 400 | Bad request | Check request body |
| 401 | Unauthorized | Check credentials |
| 403 | Forbidden | Check permissions |
| 404 | Not found | Verify issue key |
| 429 | Rate limited | Wait and retry |

### Error Response Format

```json
{
  "errorMessages": ["Issue does not exist or you do not have permission to see it."],
  "errors": {}
}
```

---

## Testing Patterns

### Mock API Responses

```typescript
// __mocks__/jira.ts
export const mockIssue = {
  key: "PROJ-123",
  fields: {
    summary: "Test Issue",
    status: { name: "Open" }
  }
};

export const mockGetIssue = jest.fn().mockResolvedValue(mockIssue);
```

### Integration Tests

```typescript
describe('Jira Integration', () => {
  it('should fetch issue details', async () => {
    const issue = await jira.getIssue('PROJ-123');
    expect(issue.key).toBe('PROJ-123');
  });

  it('should transition issue', async () => {
    await jira.transitionIssue('PROJ-123', 'In Progress');
    const issue = await jira.getIssue('PROJ-123');
    expect(issue.fields.status.name).toBe('In Progress');
  });
});
```

---

## Anti-Patterns

### DON'T: Use Basic Auth in Frontend

```typescript
// BAD - Exposes credentials
fetch('/api/jira', {
  headers: { 'Authorization': `Basic ${btoa(email + ':' + token)}` }
});

// GOOD - Use backend proxy
fetch('/api/jira/issue/PROJ-123');
```

### DON'T: Ignore Pagination

```typescript
// BAD
const { issues } = await searchIssues(jql);

// GOOD
async function* getAllIssues(jql: string) {
  let startAt = 0;
  const maxResults = 100;

  while (true) {
    const { issues, total } = await searchIssues(jql, startAt, maxResults);
    yield* issues;
    startAt += issues.length;
    if (startAt >= total) break;
  }
}
```

---

## Checklist

Before using Jira integration:

- [ ] API token generated in Atlassian account
- [ ] Domain configured in `.claude/config/workspace.json`
- [ ] Default project set
- [ ] Transition IDs mapped for your workflow
- [ ] Webhooks configured (if needed)
- [ ] ADF formatting implemented for descriptions
- [ ] Error handling for all API calls

---

## Related Skills

- `session-management` - Session lifecycle
- `scheduled-actions` - Background task processing
- `service-layer` - API implementation patterns
