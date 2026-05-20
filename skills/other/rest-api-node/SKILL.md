---
name: rest-api-node
description: >
  RESTful API design conventions for Node.js including resource naming, pagination, filtering,
  sorting, HATEOAS links, versioning, and content negotiation. Use when the user is designing
  REST APIs, asking about pagination or filtering patterns, implementing API versioning, or
  building CRUD endpoints. Trigger on mentions of REST API design, API pagination, query
  parameters, HATEOAS, API versioning, or RESTful conventions.
---

# RESTful API Design for Node.js

Conventions and patterns for designing consistent, scalable REST APIs.

## When to Use
- User is designing REST API endpoints
- User needs pagination, filtering, or sorting
- User asks about API versioning strategies
- User wants consistent response formats
- User mentions HATEOAS or API discoverability

## Core Patterns

### Resource Naming Conventions

Use plural nouns for collections. Nest sub-resources to express relationships. Keep URLs shallow (max 2 levels of nesting).

```
GET    /api/v1/users              -- List users
POST   /api/v1/users              -- Create user
GET    /api/v1/users/:id          -- Get user
PUT    /api/v1/users/:id          -- Replace user
PATCH  /api/v1/users/:id          -- Partial update
DELETE /api/v1/users/:id          -- Delete user

GET    /api/v1/users/:id/orders   -- List user's orders
POST   /api/v1/users/:id/orders   -- Create order for user

-- Actions that don't map to CRUD use verbs as sub-resources
POST   /api/v1/users/:id/activate
POST   /api/v1/orders/:id/cancel
```

### Pagination

Return paginated results with metadata. Support both offset-based and cursor-based pagination.

```typescript
import { Request, Response } from 'express'

interface PaginationQuery {
  page?: string
  limit?: string
  cursor?: string
}

async function listUsers(req: Request, res: Response) {
  const page = Math.max(1, parseInt(req.query.page as string) || 1)
  const limit = Math.min(100, Math.max(1, parseInt(req.query.limit as string) || 20))
  const offset = (page - 1) * limit

  const [users, total] = await Promise.all([
    db.user.findMany({ skip: offset, take: limit, orderBy: { createdAt: 'desc' } }),
    db.user.count(),
  ])

  const totalPages = Math.ceil(total / limit)
  const baseUrl = `${req.protocol}://${req.get('host')}${req.baseUrl}${req.path}`

  res.json({
    data: users,
    meta: { page, limit, total, totalPages },
    links: {
      self: `${baseUrl}?page=${page}&limit=${limit}`,
      first: `${baseUrl}?page=1&limit=${limit}`,
      last: `${baseUrl}?page=${totalPages}&limit=${limit}`,
      ...(page > 1 && { prev: `${baseUrl}?page=${page - 1}&limit=${limit}` }),
      ...(page < totalPages && { next: `${baseUrl}?page=${page + 1}&limit=${limit}` }),
    },
  })
}
```

### Filtering and Sorting

Accept filters and sort via query parameters. Validate allowed fields.

```typescript
const ALLOWED_FILTERS = new Set(['status', 'role', 'createdAfter', 'createdBefore'])
const ALLOWED_SORT_FIELDS = new Set(['name', 'email', 'createdAt'])

function parseFilters(query: Record<string, string>) {
  const where: Record<string, unknown> = {}

  if (query.status && ALLOWED_FILTERS.has('status')) {
    where.status = query.status
  }
  if (query.role && ALLOWED_FILTERS.has('role')) {
    where.role = query.role
  }
  if (query.createdAfter) {
    where.createdAt = { ...(where.createdAt as object), gte: new Date(query.createdAfter) }
  }
  if (query.createdBefore) {
    where.createdAt = { ...(where.createdAt as object), lte: new Date(query.createdBefore) }
  }

  return where
}

function parseSortParam(sort: string | undefined) {
  if (!sort) return { createdAt: 'desc' as const }

  const desc = sort.startsWith('-')
  const field = desc ? sort.slice(1) : sort

  if (!ALLOWED_SORT_FIELDS.has(field)) return { createdAt: 'desc' as const }
  return { [field]: desc ? 'desc' : 'asc' }
}

// Usage: GET /api/v1/users?status=active&sort=-createdAt&page=2
router.get('/users', asyncHandler(async (req, res) => {
  const where = parseFilters(req.query as Record<string, string>)
  const orderBy = parseSortParam(req.query.sort as string)
  // ... paginate with where and orderBy
}))
```

### API Versioning

Use URL path versioning for simplicity and clarity. Each version is an explicit contract.

```typescript
import { Router } from 'express'

const v1Router = Router()
v1Router.use('/users', userRoutesV1)
v1Router.use('/orders', orderRoutesV1)

const v2Router = Router()
v2Router.use('/users', userRoutesV2)
v2Router.use('/orders', orderRoutesV2)

app.use('/api/v1', v1Router)
app.use('/api/v2', v2Router)
```

### Consistent Response Format

Use a uniform response envelope across all endpoints.

```typescript
interface ApiResponse<T> {
  data: T
  meta?: {
    page: number
    limit: number
    total: number
    totalPages: number
  }
  links?: Record<string, string>
}

interface ApiErrorResponse {
  error: string
  details?: Record<string, string[]>
}

// Success
res.status(200).json({ data: user })

// Created
res.status(201).json({ data: newUser })

// No Content (delete)
res.status(204).end()

// Error
res.status(400).json({ error: 'Validation failed', details: { email: ['Invalid'] } })
```

### Content Negotiation

Respond in the format the client requests via the Accept header.

```typescript
function negotiateResponse(req: Request, res: Response, data: unknown) {
  res.format({
    'application/json': () => res.json({ data }),
    'text/csv': () => {
      const csv = convertToCsv(data)
      res.type('text/csv').send(csv)
    },
    default: () => res.status(406).json({ error: 'Not Acceptable' }),
  })
}
```

## Anti-Patterns

- **Using verbs in resource URLs** -- `/api/getUsers` violates REST conventions. Use `GET /api/users` instead. HTTP methods convey the action.
- **Returning 200 for errors** -- Always use appropriate HTTP status codes. 200 means success. Use 4xx for client errors, 5xx for server errors.
- **Unbounded list endpoints** -- Always paginate collection endpoints. Returning all records causes memory exhaustion and slow responses.
- **Exposing database IDs or internal structure** -- Use UUIDs instead of sequential IDs. Do not leak table names or column names in error messages.
- **Inconsistent response formats** -- Sometimes returning `{ user: ... }`, sometimes `{ data: ... }`. Pick one envelope format and use it everywhere.

## Quick Reference

```
HTTP Methods:
  GET     -- Read (idempotent, safe)
  POST    -- Create (not idempotent)
  PUT     -- Replace (idempotent)
  PATCH   -- Partial update (idempotent)
  DELETE  -- Remove (idempotent)

Status Codes:
  200 OK              -- Success
  201 Created         -- Resource created
  204 No Content      -- Successful delete
  400 Bad Request     -- Validation error
  401 Unauthorized    -- Missing/invalid auth
  403 Forbidden       -- Insufficient permissions
  404 Not Found       -- Resource doesn't exist
  409 Conflict        -- Duplicate/conflict
  429 Too Many Reqs   -- Rate limited
  500 Internal Error  -- Server bug

Query patterns:
  ?page=2&limit=20           -- Pagination
  ?sort=-createdAt           -- Sort desc
  ?status=active&role=admin  -- Filters
  ?fields=id,name,email      -- Sparse fields
```
