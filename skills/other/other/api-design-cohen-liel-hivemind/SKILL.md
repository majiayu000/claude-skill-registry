---
name: api-design
description: REST API design principles and best practices. Use when designing API endpoints, request/response schemas, versioning, error formats, or reviewing API design.
---

# REST API Design Patterns

## URL Structure
```
# Resources (nouns, plural, lowercase-kebab)
GET    /api/v1/users           # List users
POST   /api/v1/users           # Create user
GET    /api/v1/users/{id}      # Get user
PUT    /api/v1/users/{id}      # Replace user
PATCH  /api/v1/users/{id}      # Update user partially
DELETE /api/v1/users/{id}      # Delete user

# Nested resources
GET    /api/v1/users/{id}/posts        # User's posts
POST   /api/v1/users/{id}/posts        # Create post for user

# Actions (when CRUD doesn't fit)
POST   /api/v1/users/{id}/activate
POST   /api/v1/auth/login
POST   /api/v1/auth/logout
POST   /api/v1/auth/refresh

# Search / filtering
GET    /api/v1/posts?status=published&author=123&sort=-created_at&page=2&limit=20
```

## Status Codes
```
200 OK              — GET/PATCH/PUT success with body
201 Created         — POST success (include Location header)
204 No Content      — DELETE success
400 Bad Request     — Invalid input (validation error)
401 Unauthorized    — Not authenticated (no/invalid token)
403 Forbidden       — Authenticated but not allowed
404 Not Found       — Resource doesn't exist
409 Conflict        — Duplicate email, version conflict
422 Unprocessable   — Semantically invalid (used by FastAPI for validation)
429 Too Many Reqs   — Rate limit exceeded
500 Server Error    — Unexpected error (never expose details)
```

## Request / Response Format
```json
// List response with pagination
{
  "data": [...],
  "pagination": {
    "total": 248,
    "page": 2,
    "limit": 20,
    "has_next": true
  }
}

// Single resource
{
  "data": { "id": 1, "email": "user@example.com", "name": "Alice" }
}

// Error response (consistent across ALL endpoints)
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input",
    "details": [
      { "field": "email", "message": "Invalid email format" },
      { "field": "password", "message": "Must be at least 8 characters" }
    ]
  }
}
```

## Filtering & Pagination
```
# Filtering
GET /posts?status=published&tag=python&author_id=123

# Sorting (- prefix for DESC)
GET /posts?sort=-created_at,title

# Pagination
GET /posts?page=2&limit=20

# Field selection (reduce payload)
GET /users?fields=id,name,email

# Search
GET /posts?q=fastapi+tutorial
```

## Versioning
```
# URL path versioning (simplest, most visible)
/api/v1/users
/api/v2/users

# When to version: breaking changes only
# Non-breaking changes (adding fields, new endpoints) = no new version needed
```

## Response Headers
```
Content-Type: application/json
X-Request-ID: uuid  # For distributed tracing
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 87
X-RateLimit-Reset: 1711234567
Location: /api/v1/users/123  # After POST 201
```

## Rules
- Use nouns for resources, verbs only for actions
- Be consistent: same error format everywhere
- Always version the API
- Never expose internal IDs in public APIs (use UUIDs or slugs)
- Include created_at/updated_at in all resource responses
- Use ISO 8601 for all dates: 2024-03-15T10:30:00Z
- Paginate ALL list endpoints (even if only 10 items now)
- Document with OpenAPI/Swagger (FastAPI auto-generates this)
- Make POST idempotent with client-provided idempotency keys for payments
