---
name: entity-api
description: |
  Dynamic entity API patterns for CRUD operations.
  Covers entity resolution, query parameters, response formats, child entities, and metadata.
  Use this skill when consuming entity APIs or understanding dynamic endpoint behavior.
allowed-tools: Read, Glob, Grep
version: 1.0.0
---

# Entity API Skill

Patterns for consuming the dynamic entity API system.

## Architecture Overview

```
app/api/v1/
├── [entity]/route.ts                              # LIST (GET), CREATE (POST)
├── [entity]/[id]/route.ts                         # READ (GET), UPDATE (PATCH), DELETE
├── [entity]/[id]/child/[childType]/route.ts       # Child LIST/CREATE
└── [entity]/[id]/child/[childType]/[childId]/route.ts  # Child UPDATE/DELETE

core/lib/api/entity/
├── generic-handler.ts                             # CRUD handlers
├── resolver.ts                                    # Entity resolution
└── helpers.ts                                     # Metadata, response formatting
```

## When to Use This Skill

- Consuming entity endpoints in frontend code
- Understanding API response formats
- Working with query parameters (filtering, pagination, search)
- Implementing child entity operations
- Working with metadata (metas) system

## Entity Resolution Order

When a request hits `/api/v1/{entity}`:

1. **Extract slug** - `/api/v1/products` → `products`
2. **Check core path** - Skip if: users, api-keys, auth, system, health, internal, admin, debug
3. **Registry lookup** - `entityRegistry.getBySlug('products')`
4. **Custom override check** - Look for `app/api/v1/(contents)/products/route.ts`
5. **Return resolution** - `{ entityConfig, hasCustomOverride, isValidEntity }`

```typescript
// If custom override exists, generic handler is skipped
if (existsSync('app/api/v1/(contents)/products/route.ts')) {
  return { hasCustomOverride: true, isValidEntity: false }
}
```

## Query Parameters

### Pagination

```
GET /api/v1/tasks?page=1&limit=10
```

### Field Selection

```
GET /api/v1/tasks?fields=id,name,slug
GET /api/v1/tasks?fields=status&distinct=true    # Distinct values
```

### Multiple IDs

```
GET /api/v1/tasks?ids=id1,id2,id3
GET /api/v1/tasks?ids=id1&ids=id2    # Alternative syntax
```

### Filtering (Field-Based)

```
GET /api/v1/tasks?status=published
GET /api/v1/tasks?status=draft,published    # OR logic
GET /api/v1/tasks?status=draft&priority=high    # AND logic
```

### Search

```
GET /api/v1/tasks?search=keyword    # Searches: name, title, slug, content
```

### Date Range

```
GET /api/v1/tasks?dateField=createdAt&from=2025-01-01&to=2025-12-31
```

### Taxonomy Filtering

```
GET /api/v1/tasks?taxonomyId=tax-123&taxonomyType=category
GET /api/v1/tasks?categoryId=tax-123    # Legacy convenience
```

### Metadata

```
GET /api/v1/tasks?metas=all              # Include all metadata
GET /api/v1/tasks?metas=key1,key2,key3   # Specific keys only
```

### Child Entities

```
GET /api/v1/clients/123?child=all              # Include all children
GET /api/v1/clients/123?child=audiences,products    # Specific types
```

### Sorting

```
GET /api/v1/tasks?sortBy=createdAt&sortOrder=DESC
GET /api/v1/tasks?sortBy=name&sortOrder=ASC
```

## Response Formats

### List Success (200)

```typescript
{
  success: true,
  data: [
    { id: "1", name: "Task 1", status: "active", createdAt: "2025-01-01T..." },
    { id: "2", name: "Task 2", status: "done", createdAt: "2025-01-02T..." }
  ],
  info: {
    timestamp: "2025-12-30T...",
    total: 42,
    page: 1,
    limit: 10,
    totalPages: 5,
    hasNextPage: true,
    hasPrevPage: false
  }
}
```

### Single Entity Success (200)

```typescript
{
  success: true,
  data: {
    id: "1",
    name: "Task 1",
    status: "active",
    createdAt: "2025-01-01T...",
    updatedAt: "2025-01-01T..."
  },
  info: {
    timestamp: "2025-12-30T..."
  }
}
```

### Create Success (201)

```typescript
{
  success: true,
  data: {
    id: "newly-created-id",
    name: "New Task",
    // ... all fields
  },
  info: {
    timestamp: "2025-12-30T..."
  }
}
```

### Error Response

```typescript
{
  success: false,
  error: "Entity not found",
  code: "NOT_FOUND",
  details: { entityType: "tasks", id: "invalid-id" },
  info: {
    timestamp: "2025-12-30T..."
  }
}
```

### With Metadata

```typescript
{
  success: true,
  data: {
    id: "1",
    name: "Task 1",
    metas: {
      seo_title: "Custom Title",
      seo_description: "Meta description",
      custom_key: { nested: "value" }
    }
  },
  info: { ... }
}
```

### With Children

```typescript
{
  success: true,
  data: {
    id: "client-123",
    name: "Acme Corp",
    child: {
      audiences: [
        { id: "aud-1", name: "Enterprise", parentId: "client-123" },
        { id: "aud-2", name: "SMB", parentId: "client-123" }
      ],
      products: [
        { id: "prod-1", name: "Product A", parentId: "client-123" }
      ]
    }
  },
  info: { ... }
}
```

## Child Entities

### List Child Entities

```
GET /api/v1/clients/{parentId}/child/audiences
GET /api/v1/clients/{parentId}/child/audiences?page=1&limit=20
```

### Create Child Entity

```
POST /api/v1/clients/{parentId}/child/audiences
Content-Type: application/json

{
  "name": "New Audience",
  "description": "Target audience description",
  "status": "active"
}
```

Response includes `parentId`:

```typescript
{
  success: true,
  data: {
    id: "aud-xyz",
    parentId: "client-123",    // Automatically set
    name: "New Audience",
    // ...
  }
}
```

### Update Child Entity

```
PATCH /api/v1/clients/{parentId}/child/audiences/{childId}
Content-Type: application/json

{
  "name": "Updated Name"
}
```

### Delete Child Entity

```
DELETE /api/v1/clients/{parentId}/child/audiences/{childId}
```

## Metadata System

### Reading Metadata

```typescript
// Include all metas
const response = await fetch('/api/v1/tasks/123?metas=all')

// Include specific metas
const response = await fetch('/api/v1/tasks/123?metas=seo_title,color_label')
```

### Writing Metadata

Include `metas` in request body:

```typescript
// Create with metas
await fetch('/api/v1/tasks', {
  method: 'POST',
  body: JSON.stringify({
    name: 'Task Name',
    status: 'active',
    metas: {
      seo_title: 'Custom SEO Title',
      custom_field: { nested: 'value' }
    }
  })
})

// Update metas (merge behavior)
await fetch('/api/v1/tasks/123', {
  method: 'PATCH',
  body: JSON.stringify({
    metas: {
      seo_title: 'Updated Title'  // Other metas preserved
    }
  })
})
```

**Metadata Behavior:**

- Stored separately from entity data
- Security inherited from parent entity via RLS
- Objects are merged, primitive types are replaced
- Lazy loaded only when requested

## Authentication

### Required Headers

```typescript
// Team context (REQUIRED for team entities)
headers: {
  'x-team-id': 'team-uuid'
}

// API key auth (optional)
headers: {
  'Authorization': 'Bearer sk_...',
  // OR
  'x-api-key': 'sk_...'
}

// Builder source (enables blocks field)
headers: {
  'x-builder-source': 'true'
}
```

### Scope Requirements

| Operation | Required Scope |
|-----------|---------------|
| GET (list/read) | `{entity}:read` |
| POST (create) | `{entity}:write` |
| PATCH (update) | `{entity}:write` |
| DELETE | `{entity}:delete` or `{entity}:write` |

## Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `AUTHENTICATION_REQUIRED` | 401 | No auth credentials |
| `INVALID_API_KEY` | 401 | API key invalid/expired |
| `TEAM_CONTEXT_REQUIRED` | 400 | Missing x-team-id header |
| `INSUFFICIENT_PERMISSIONS` | 403 | User lacks required scope |
| `NOT_FOUND` | 404 | Entity doesn't exist |
| `VALIDATION_ERROR` | 400 | Request body validation failed |
| `CONFLICT` | 409 | Duplicate or constraint violation |

## Frontend Integration

### TanStack Query Example

```typescript
import { useQuery } from '@tanstack/react-query'

function useTaskList(filters: TaskFilters) {
  return useQuery({
    queryKey: ['entity', 'tasks', filters],
    queryFn: async () => {
      const params = new URLSearchParams({
        page: String(filters.page),
        limit: String(filters.limit),
        ...(filters.status && { status: filters.status }),
        ...(filters.search && { search: filters.search }),
      })

      const response = await fetch(`/api/v1/tasks?${params}`)
      if (!response.ok) throw new Error('Failed to fetch')
      return response.json()
    },
  })
}
```

### Mutation Example

```typescript
import { useMutation, useQueryClient } from '@tanstack/react-query'

function useCreateTask() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: async (data: CreateTaskData) => {
      const response = await fetch('/api/v1/tasks', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      })
      if (!response.ok) throw new Error('Failed to create')
      return response.json()
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['entity', 'tasks'] })
    },
  })
}
```

## Anti-Patterns

```typescript
// NEVER: Hardcode entity names in URLs
const endpoint = '/api/v1/tasks'

// CORRECT: Use entity config
const endpoint = `/api/v1/${entityConfig.slug}`

// NEVER: Skip team context for team entities
fetch('/api/v1/tasks')  // Missing x-team-id!

// CORRECT: Always include team context
fetch('/api/v1/tasks', {
  headers: { 'x-team-id': teamId }
})

// NEVER: Assume all entities have same fields
if (entity.status === 'active') { ... }  // Not all entities have status!

// CORRECT: Check entity config for available fields
const hasStatus = entityConfig.fields.some(f => f.name === 'status')

// NEVER: Ignore pagination info
const allTasks = response.data  // Could be truncated!

// CORRECT: Handle pagination
const { data, info } = response
if (info.hasNextPage) {
  // Load more or show pagination
}
```

## Checklist

Before finalizing entity API integration:

- [ ] Include `x-team-id` header for team entities
- [ ] Handle pagination (`info.hasNextPage`, `info.totalPages`)
- [ ] Use correct query parameters for filtering
- [ ] Check `success` field in response
- [ ] Handle error responses with appropriate UI feedback
- [ ] Use `metas` parameter only when metadata needed
- [ ] Invalidate queries after mutations
- [ ] Use proper HTTP methods (GET, POST, PATCH, DELETE)

## Related Skills

- `entity-system` - Entity definition (config, fields, types)
- `tanstack-query` - Data fetching patterns
- `better-auth` - Authentication patterns
