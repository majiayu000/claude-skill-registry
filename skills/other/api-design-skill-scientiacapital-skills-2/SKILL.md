---
name: "api-design"
description: "REST/GraphQL API design patterns - resource naming, HTTP methods, error handling, pagination, versioning. Use when: design API, REST endpoints, GraphQL schema, error responses, pagination, rate limiting, API documentation."
---

<objective>
Comprehensive API design skill covering RESTful conventions, error handling, pagination, versioning, and documentation. Focuses on building consistent, intuitive, and maintainable APIs.

Good API design makes the right thing easy and the wrong thing hard. This skill helps you create APIs that are a pleasure to use and maintain.
</objective>

<quick_start>
**Resource naming:** Nouns, plural, lowercase, hyphenated (`/users`, `/blog-posts`)

**HTTP methods:** GET (read), POST (create), PUT (replace), PATCH (update), DELETE (remove)

**Status codes:** 200 OK, 201 Created, 204 No Content, 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found, 429 Rate Limited

**Pagination:** Prefer cursor-based for real-time data; use `?limit=20&cursor=xxx`

**Versioning:** URL path (`/api/v1/`) is clearest approach
</quick_start>

<success_criteria>
API design is successful when:
- Resources use plural nouns with consistent naming
- HTTP methods match semantics (GET=read, POST=create, etc.)
- Error responses follow consistent format with code, message, details, requestId
- Pagination implemented (cursor or offset based)
- Rate limiting headers included (X-RateLimit-Limit, Remaining, Reset)
- Versioning strategy defined before breaking changes needed
</success_criteria>

<core_principles>
## API Design Principles

1. **Consistency** - Same patterns everywhere (naming, errors, pagination)
2. **Predictability** - Developers can guess how things work
3. **Simplicity** - Easy cases should be easy, complex cases possible
4. **Backwards compatibility** - Don't break existing clients
5. **Self-documenting** - Clear naming, helpful error messages
</core_principles>

<rest_basics>
## RESTful Conventions

### Resource Naming

```
# GOOD: Nouns, plural, lowercase, hyphenated
GET    /users
GET    /users/{id}
GET    /users/{id}/posts
GET    /blog-posts
GET    /api/v1/user-preferences

# BAD: Verbs, singular, mixed case, underscores
GET    /getUser
GET    /user/{id}
GET    /User/{id}/getPosts
GET    /blog_posts
```

### HTTP Methods

| Method | Purpose | Idempotent | Safe | Request Body |
|--------|---------|------------|------|--------------|
| GET | Read resource | Yes | Yes | No |
| POST | Create resource | No | No | Yes |
| PUT | Replace resource | Yes | No | Yes |
| PATCH | Partial update | No* | No | Yes |
| DELETE | Remove resource | Yes | No | No |

*PATCH is idempotent if you apply the same patch

### CRUD Operations

```
# Collection operations
GET    /users           # List all users
POST   /users           # Create a user

# Single resource operations
GET    /users/{id}      # Get one user
PUT    /users/{id}      # Replace user
PATCH  /users/{id}      # Update user fields
DELETE /users/{id}      # Delete user

# Nested resources
GET    /users/{id}/posts       # User's posts
POST   /users/{id}/posts       # Create post for user
GET    /posts/{id}/comments    # Post's comments
```

### Actions (Non-CRUD Operations)

```
# When you need actions, use verbs as sub-resources
POST   /users/{id}/activate
POST   /users/{id}/deactivate
POST   /orders/{id}/cancel
POST   /invoices/{id}/send
POST   /auth/login
POST   /auth/logout
POST   /auth/refresh
```

### Status Codes

| Code | Meaning | When to Use |
|------|---------|-------------|
| 200 | OK | Successful GET, PUT, PATCH |
| 201 | Created | Successful POST that creates |
| 204 | No Content | Successful DELETE |
| 400 | Bad Request | Invalid input, validation error |
| 401 | Unauthorized | Missing/invalid authentication |
| 403 | Forbidden | Authenticated but not authorized |
| 404 | Not Found | Resource doesn't exist |
| 409 | Conflict | Duplicate, state conflict |
| 422 | Unprocessable | Validation failed (alternative to 400) |
| 429 | Too Many Requests | Rate limited |
| 500 | Server Error | Unexpected server error |
</rest_basics>

<error_handling>
## Error Responses

### Consistent Error Format

```typescript
// Standard error response
interface ErrorResponse {
  error: {
    code: string;           // Machine-readable code
    message: string;        // Human-readable message
    details?: ErrorDetail[]; // Field-level errors
    requestId?: string;     // For support/debugging
  };
}

interface ErrorDetail {
  field: string;
  message: string;
  code: string;
}
```

### Examples

```json
// 400 Bad Request - Validation error
{
  "error": {
    "code": "validation_error",
    "message": "Invalid request parameters",
    "details": [
      { "field": "email", "message": "Invalid email format", "code": "invalid_format" },
      { "field": "age", "message": "Must be at least 13", "code": "min_value" }
    ],
    "requestId": "req_abc123"
  }
}

// 401 Unauthorized
{
  "error": {
    "code": "unauthorized",
    "message": "Invalid or expired authentication token",
    "requestId": "req_abc123"
  }
}

// 403 Forbidden
{
  "error": {
    "code": "forbidden",
    "message": "You don't have permission to access this resource",
    "requestId": "req_abc123"
  }
}

// 404 Not Found
{
  "error": {
    "code": "not_found",
    "message": "User not found",
    "requestId": "req_abc123"
  }
}

// 429 Rate Limited
{
  "error": {
    "code": "rate_limited",
    "message": "Too many requests. Please retry after 60 seconds",
    "requestId": "req_abc123"
  }
}
```

### Implementation

```typescript
// Error class
class ApiError extends Error {
  constructor(
    public statusCode: number,
    public code: string,
    message: string,
    public details?: ErrorDetail[]
  ) {
    super(message);
  }
}

// Error handler middleware
function errorHandler(error: Error, req: Request, res: Response) {
  const requestId = req.headers['x-request-id'] || crypto.randomUUID();

  if (error instanceof ApiError) {
    return res.status(error.statusCode).json({
      error: {
        code: error.code,
        message: error.message,
        details: error.details,
        requestId,
      },
    });
  }

  // Log unexpected errors
  logger.error('Unexpected error', { error, requestId });

  // Don't expose internal details
  return res.status(500).json({
    error: {
      code: 'internal_error',
      message: 'An unexpected error occurred',
      requestId,
    },
  });
}
```
</error_handling>

<pagination>
## Pagination

### Cursor-Based (Recommended)

```typescript
// Request
GET /posts?limit=20&cursor=eyJpZCI6MTAwfQ

// Response
{
  "data": [...],
  "pagination": {
    "hasMore": true,
    "nextCursor": "eyJpZCI6MTIwfQ",
    "prevCursor": "eyJpZCI6MTAwfQ"
  }
}
```

**Pros:** Consistent results, handles real-time data
**Cons:** Can't jump to page N

### Offset-Based

```typescript
// Request
GET /posts?page=2&limit=20
// or
GET /posts?offset=20&limit=20

// Response
{
  "data": [...],
  "pagination": {
    "page": 2,
    "limit": 20,
    "total": 150,
    "totalPages": 8
  }
}
```

**Pros:** Can jump to any page
**Cons:** Inconsistent with real-time data, slow on large tables

### Implementation (Cursor)

```typescript
// Encode/decode cursor
function encodeCursor(data: object): string {
  return Buffer.from(JSON.stringify(data)).toString('base64url');
}

function decodeCursor(cursor: string): object {
  return JSON.parse(Buffer.from(cursor, 'base64url').toString());
}

// Query with cursor
async function getPosts(limit: number, cursor?: string) {
  const where: any = {};

  if (cursor) {
    const { id } = decodeCursor(cursor);
    where.id = { lt: id };
  }

  const posts = await db.post.findMany({
    where,
    orderBy: { id: 'desc' },
    take: limit + 1, // Fetch one extra to check hasMore
  });

  const hasMore = posts.length > limit;
  const data = hasMore ? posts.slice(0, -1) : posts;

  return {
    data,
    pagination: {
      hasMore,
      nextCursor: hasMore ? encodeCursor({ id: data[data.length - 1].id }) : null,
    },
  };
}
```
</pagination>

<filtering>
## Filtering and Sorting

### Query Parameters

```
# Simple filters
GET /users?status=active
GET /users?role=admin&status=active

# Range filters
GET /orders?created_after=2024-01-01
GET /orders?total_min=100&total_max=500

# Search
GET /products?search=keyboard
GET /products?q=wireless+keyboard

# Sorting
GET /posts?sort=created_at&order=desc
GET /posts?sort=-created_at  # Prefix with - for desc

# Multiple sorts
GET /posts?sort=status,-created_at

# Field selection (sparse fieldsets)
GET /users?fields=id,name,email
GET /users/{id}?include=posts,comments
```

### Implementation

```typescript
const filterSchema = z.object({
  status: z.enum(['active', 'inactive', 'all']).optional(),
  search: z.string().max(100).optional(),
  created_after: z.coerce.date().optional(),
  created_before: z.coerce.date().optional(),
  sort: z.string().optional(),
  order: z.enum(['asc', 'desc']).default('desc'),
  fields: z.string().optional(),
});

function buildQuery(filters: z.infer<typeof filterSchema>) {
  const where: any = {};

  if (filters.status && filters.status !== 'all') {
    where.status = filters.status;
  }

  if (filters.search) {
    where.OR = [
      { name: { contains: filters.search, mode: 'insensitive' } },
      { email: { contains: filters.search, mode: 'insensitive' } },
    ];
  }

  if (filters.created_after) {
    where.createdAt = { gte: filters.created_after };
  }

  return where;
}
```
</filtering>

<versioning>
## API Versioning

### URL Path Versioning (Recommended)

```
GET /api/v1/users
GET /api/v2/users
```

**Pros:** Clear, easy to understand
**Cons:** More maintenance

### Header Versioning

```
GET /api/users
Accept: application/vnd.api+json; version=2
```

**Pros:** Clean URLs
**Cons:** Hidden, harder to test

### When to Version

Create a new version when:
- Removing fields from responses
- Changing field types or formats
- Removing endpoints
- Changing authentication

Don't create a new version for:
- Adding new optional fields
- Adding new endpoints
- Adding new optional parameters
- Bug fixes
</versioning>

<rate_limiting>
## Rate Limiting

### Headers

```
X-RateLimit-Limit: 100        # Max requests per window
X-RateLimit-Remaining: 95     # Requests remaining
X-RateLimit-Reset: 1640000000 # Unix timestamp when limit resets
Retry-After: 60               # Seconds until can retry (on 429)
```

### Tiers

| Tier | Limit | Window |
|------|-------|--------|
| Anonymous | 60 req | 1 hour |
| Free | 100 req | 1 minute |
| Pro | 1000 req | 1 minute |
| Enterprise | 10000 req | 1 minute |

### Implementation

```typescript
import { Ratelimit } from '@upstash/ratelimit';

const ratelimit = new Ratelimit({
  redis,
  limiter: Ratelimit.slidingWindow(100, '1 m'),
});

async function rateLimitMiddleware(req: Request) {
  const identifier = req.headers.get('authorization') || req.ip;
  const { success, limit, remaining, reset } = await ratelimit.limit(identifier);

  const headers = {
    'X-RateLimit-Limit': limit.toString(),
    'X-RateLimit-Remaining': remaining.toString(),
    'X-RateLimit-Reset': reset.toString(),
  };

  if (!success) {
    return new Response(
      JSON.stringify({
        error: {
          code: 'rate_limited',
          message: 'Too many requests',
        },
      }),
      {
        status: 429,
        headers: {
          ...headers,
          'Retry-After': Math.ceil((reset - Date.now()) / 1000).toString(),
        },
      }
    );
  }

  return { headers };
}
```
</rate_limiting>

<references>
For detailed patterns, load the appropriate reference:

| Topic | Reference File | When to Load |
|-------|----------------|--------------|
| REST patterns | `reference/rest-patterns.md` | Endpoint design |
| Error handling | `reference/error-handling.md` | Error responses |
| Pagination | `reference/pagination.md` | List endpoints |
| Versioning | `reference/versioning.md` | API evolution |
| Documentation | `reference/documentation.md` | OpenAPI, docs |
| Checklist | `reference/checklist.md` | Pre-launch validation |

**To load:** Ask for the specific topic or check if context suggests it.
</references>

