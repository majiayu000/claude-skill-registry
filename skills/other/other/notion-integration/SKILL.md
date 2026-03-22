---
name: notion-integration
description: |
  Notion integration patterns for knowledge management.
  Covers API, databases, pages, and blocks.
  Use this skill when implementing Notion features or syncing sessions with databases.
allowed-tools: Read, Glob, Grep, Bash
version: 1.0.0
---

# Notion Integration Skill

Integration patterns for syncing development sessions with Notion databases and pages.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                      NOTION INTEGRATION                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐     ┌──────────────┐     ┌──────────────┐     │
│  │   Claude    │────►│   REST API   │────►│   Notion     │     │
│  │   Session   │◄────│   Client     │◄────│    API       │     │
│  └─────────────┘     └──────────────┘     └──────────────┘     │
│         │                                        │              │
│         ▼                                        ▼              │
│  ┌─────────────┐                         ┌──────────────┐      │
│  │  Session    │                         │  Databases   │      │
│  │  Files      │                         │   & Pages    │      │
│  └─────────────┘                         └──────────────┘      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## When to Use This Skill

- Setting up Notion integration for the first time
- Syncing development sessions with Notion databases
- Creating database entries from Claude sessions
- Updating page properties and content
- Managing documentation in Notion

---

## Configuration

### .claude/config/workspace.json

```json
{
  "taskManager": {
    "enabled": true,
    "provider": "notion",
    "syncWithSession": true,
    "autoUpdateStatus": true,
    "config": {
      "integrationToken": "${NOTION_TOKEN}",
      "tasksDatabaseId": "your-database-id",
      "defaultWorkspace": "your-workspace-id"
    }
  }
}
```

### Environment Variables

```bash
# .env.local
NOTION_TOKEN=secret_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

---

## Authentication

### Integration Token

```typescript
// Bearer token authentication
const headers = {
  'Authorization': `Bearer ${process.env.NOTION_TOKEN}`,
  'Content-Type': 'application/json',
  'Notion-Version': '2022-06-28' // Required API version
};

// Base URL
const BASE_URL = 'https://api.notion.com/v1';
```

### Integration Setup

1. Go to https://www.notion.so/my-integrations
2. Create new integration
3. Copy the "Internal Integration Token"
4. Share databases/pages with the integration

---

## API Patterns

### Common Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/users/me` | GET | Get bot user |
| `/users` | GET | List users |
| `/databases/{id}` | GET | Get database |
| `/databases/{id}/query` | POST | Query database |
| `/pages` | POST | Create page |
| `/pages/{id}` | GET/PATCH | Page operations |
| `/pages/{id}/properties/{id}` | GET | Get property value |
| `/blocks/{id}` | GET/PATCH/DELETE | Block operations |
| `/blocks/{id}/children` | GET/PATCH | Block children |
| `/search` | POST | Search pages/databases |

### Database Entry (Page) Structure

```typescript
interface NotionPage {
  id: string;
  object: 'page';
  parent: {
    type: 'database_id';
    database_id: string;
  };
  properties: {
    // Title property (required)
    Name: {
      title: Array<{
        type: 'text';
        text: { content: string };
      }>;
    };
    // Select property
    Status: {
      select: {
        name: string;
        color: string;
      } | null;
    };
    // Multi-select property
    Tags: {
      multi_select: Array<{
        name: string;
        color: string;
      }>;
    };
    // Date property
    'Due Date': {
      date: {
        start: string;
        end: string | null;
      } | null;
    };
    // Person property
    Assignee: {
      people: Array<{
        id: string;
        name: string;
      }>;
    };
    // Checkbox property
    Completed: {
      checkbox: boolean;
    };
    // URL property
    URL: {
      url: string | null;
    };
    // Rich text property
    Description: {
      rich_text: Array<{
        type: 'text';
        text: { content: string };
      }>;
    };
  };
  url: string;
}
```

---

## Database Operations

### Query Database

```typescript
// Query with filter and sort
const response = await fetch(`${BASE_URL}/databases/${databaseId}/query`, {
  method: 'POST',
  headers,
  body: JSON.stringify({
    filter: {
      and: [
        {
          property: 'Status',
          select: { equals: 'In Progress' }
        },
        {
          property: 'Assignee',
          people: { contains: userId }
        }
      ]
    },
    sorts: [
      { property: 'Due Date', direction: 'ascending' }
    ],
    page_size: 100
  })
});

const { results, has_more, next_cursor } = await response.json();
```

### Create Database Entry

```typescript
// Create new page in database
const page = await fetch(`${BASE_URL}/pages`, {
  method: 'POST',
  headers,
  body: JSON.stringify({
    parent: { database_id: databaseId },
    properties: {
      Name: {
        title: [{ text: { content: 'New Feature: User Auth' } }]
      },
      Status: {
        select: { name: 'In Progress' }
      },
      Tags: {
        multi_select: [
          { name: 'feature' },
          { name: 'backend' }
        ]
      },
      'Due Date': {
        date: { start: '2024-01-15' }
      },
      Description: {
        rich_text: [{ text: { content: 'Implement OAuth2 support' } }]
      }
    }
  })
});
```

### Update Properties

```typescript
// Update page properties
await fetch(`${BASE_URL}/pages/${pageId}`, {
  method: 'PATCH',
  headers,
  body: JSON.stringify({
    properties: {
      Status: {
        select: { name: 'Done' }
      },
      Completed: {
        checkbox: true
      }
    }
  })
});
```

---

## Block Operations

Notion pages consist of blocks. Common block types:

### Block Types

| Type | Description |
|------|-------------|
| `paragraph` | Text paragraph |
| `heading_1/2/3` | Headings |
| `bulleted_list_item` | Bullet point |
| `numbered_list_item` | Numbered item |
| `to_do` | Checkbox item |
| `toggle` | Collapsible block |
| `code` | Code block |
| `callout` | Callout box |
| `quote` | Quote block |
| `divider` | Horizontal line |
| `table` | Table |
| `table_row` | Table row |

### Adding Content to Page

```typescript
// Append blocks to page
await fetch(`${BASE_URL}/blocks/${pageId}/children`, {
  method: 'PATCH',
  headers,
  body: JSON.stringify({
    children: [
      {
        object: 'block',
        type: 'heading_2',
        heading_2: {
          rich_text: [{ type: 'text', text: { content: 'Session Progress' } }]
        }
      },
      {
        object: 'block',
        type: 'paragraph',
        paragraph: {
          rich_text: [{ type: 'text', text: { content: 'Phase: Backend Development' } }]
        }
      },
      {
        object: 'block',
        type: 'to_do',
        to_do: {
          rich_text: [{ type: 'text', text: { content: 'API endpoints' } }],
          checked: true
        }
      },
      {
        object: 'block',
        type: 'to_do',
        to_do: {
          rich_text: [{ type: 'text', text: { content: 'Frontend components' } }],
          checked: false
        }
      },
      {
        object: 'block',
        type: 'code',
        code: {
          rich_text: [{ type: 'text', text: { content: 'npm run test' } }],
          language: 'bash'
        }
      }
    ]
  })
});
```

---

## Session Sync Patterns

### Linking Session to Database Entry

```markdown
# In requirements.md

## Notion Task
- **Page ID:** abc123-def456-...
- **URL:** https://notion.so/workspace/Task-Name-abc123def456
- **Status:** In Progress
```

### Status Mapping

| Session Event | Notion Status |
|---------------|---------------|
| Session created | "In Progress" |
| Blocked | "Blocked" |
| Session closed (success) | "Done" |
| Session closed (partial) | "In Review" |

### Progress Updates

```typescript
// Update page with progress
const progressBlocks = [
  {
    object: 'block',
    type: 'divider',
    divider: {}
  },
  {
    object: 'block',
    type: 'heading_3',
    heading_3: {
      rich_text: [{
        type: 'text',
        text: { content: `Update: ${new Date().toISOString().split('T')[0]}` }
      }]
    }
  },
  {
    object: 'block',
    type: 'bulleted_list_item',
    bulleted_list_item: {
      rich_text: [{ type: 'text', text: { content: 'API endpoints completed' } }]
    }
  },
  {
    object: 'block',
    type: 'bulleted_list_item',
    bulleted_list_item: {
      rich_text: [{ type: 'text', text: { content: 'Tests written and passing' } }]
    }
  }
];

await fetch(`${BASE_URL}/blocks/${pageId}/children`, {
  method: 'PATCH',
  headers,
  body: JSON.stringify({ children: progressBlocks })
});
```

---

## Rich Text Formatting

### Text with Formatting

```typescript
const richText = [
  { type: 'text', text: { content: 'Normal text, ' } },
  {
    type: 'text',
    text: { content: 'bold text' },
    annotations: { bold: true }
  },
  { type: 'text', text: { content: ', ' } },
  {
    type: 'text',
    text: { content: 'italic' },
    annotations: { italic: true }
  },
  { type: 'text', text: { content: ', ' } },
  {
    type: 'text',
    text: { content: 'code' },
    annotations: { code: true }
  },
  { type: 'text', text: { content: ', and ' } },
  {
    type: 'text',
    text: { content: 'link', link: { url: 'https://example.com' } }
  }
];
```

### Available Annotations

```typescript
interface Annotations {
  bold: boolean;
  italic: boolean;
  strikethrough: boolean;
  underline: boolean;
  code: boolean;
  color: 'default' | 'gray' | 'brown' | 'orange' | 'yellow' |
         'green' | 'blue' | 'purple' | 'pink' | 'red' |
         'gray_background' | 'brown_background' | /* etc */;
}
```

---

## Rate Limiting

### Limits

| Type | Limit |
|------|-------|
| Requests | 3 requests/second average |
| Burst | Short bursts allowed |

### Handling Rate Limits

```typescript
// Notion returns 429 with Retry-After header
if (response.status === 429) {
  const retryAfter = response.headers.get('Retry-After') || '1';
  await sleep(parseInt(retryAfter) * 1000);
  // Retry request
}

// Implement exponential backoff
async function fetchWithRetry(url: string, options: RequestInit, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    const response = await fetch(url, options);
    if (response.status !== 429) return response;

    const delay = Math.pow(2, i) * 1000;
    await sleep(delay);
  }
  throw new Error('Max retries exceeded');
}
```

---

## Error Handling

### Common Error Codes

| Code | Description | Resolution |
|------|-------------|------------|
| 400 | Invalid request | Check body format |
| 401 | Unauthorized | Check token |
| 403 | No access | Share page with integration |
| 404 | Not found | Verify page/database ID |
| 409 | Conflict | Transaction conflict, retry |
| 429 | Rate limited | Wait and retry |

### Error Response Format

```json
{
  "object": "error",
  "status": 400,
  "code": "validation_error",
  "message": "body failed validation..."
}
```

---

## Testing Patterns

### Mock API Responses

```typescript
// __mocks__/notion.ts
export const mockPage = {
  id: "abc123-def456",
  object: "page",
  properties: {
    Name: { title: [{ text: { content: "Test Task" } }] },
    Status: { select: { name: "In Progress" } }
  }
};

export const mockQueryDatabase = jest.fn().mockResolvedValue({
  results: [mockPage],
  has_more: false
});
```

### Integration Tests

```typescript
describe('Notion Integration', () => {
  it('should query database', async () => {
    const results = await notion.queryDatabase(databaseId, {
      filter: { property: 'Status', select: { equals: 'In Progress' } }
    });
    expect(results.length).toBeGreaterThan(0);
  });

  it('should create page', async () => {
    const page = await notion.createPage({
      parent: { database_id: databaseId },
      properties: {
        Name: { title: [{ text: { content: 'Test' } }] }
      }
    });
    expect(page.id).toBeDefined();
  });
});
```

---

## Anti-Patterns

### DON'T: Forget Notion-Version Header

```typescript
// BAD - Missing version header
fetch(url, {
  headers: { 'Authorization': `Bearer ${token}` }
});

// GOOD - Include version
fetch(url, {
  headers: {
    'Authorization': `Bearer ${token}`,
    'Notion-Version': '2022-06-28'
  }
});
```

### DON'T: Assume Integration Has Access

```typescript
// BAD - Assume access exists
const page = await notion.getPage(pageId);

// GOOD - Handle access errors
try {
  const page = await notion.getPage(pageId);
} catch (error) {
  if (error.code === 'object_not_found') {
    console.error('Page not shared with integration');
    // Guide user to share the page
  }
}
```

### DON'T: Send Empty Arrays

```typescript
// BAD - Empty arrays can cause errors
properties: {
  Tags: { multi_select: [] } // Remove tags
}

// GOOD - Omit property or use null where supported
properties: {
  // Don't include Tags to keep existing values
}
```

---

## Checklist

Before using Notion integration:

- [ ] Integration created at notion.so/my-integrations
- [ ] Token stored in environment variables
- [ ] Database shared with integration
- [ ] Notion-Version header set (2022-06-28)
- [ ] Property names match database schema exactly
- [ ] Rate limiting handled
- [ ] Error handling for 403/404

---

## Related Skills

- `session-management` - Session lifecycle
- `scheduled-actions` - Background task processing
- `service-layer` - API implementation patterns
