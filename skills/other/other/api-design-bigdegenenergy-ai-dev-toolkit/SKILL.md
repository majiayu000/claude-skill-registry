---
name: api-design
description: RESTful API and GraphQL design best practices. Auto-triggers when designing endpoints, handling HTTP methods, or structuring API responses.
---

# API Design Skill

## REST Design Principles

### Resource Naming
- Use nouns, not verbs: `/users` not `/getUsers`
- Use plural for collections: `/users`, `/orders`
- Use kebab-case: `/user-profiles`
- Nest for relationships: `/users/{id}/orders`
- Maximum 3 levels deep

### HTTP Methods

| Method | Purpose | Idempotent | Safe |
|--------|---------|------------|------|
| GET | Read resource | Yes | Yes |
| POST | Create resource | No | No |
| PUT | Replace resource | Yes | No |
| PATCH | Partial update | No | No |
| DELETE | Remove resource | Yes | No |

### Status Codes

```
2xx Success
  200 OK - General success
  201 Created - Resource created (return Location header)
  204 No Content - Success with no body (DELETE)

4xx Client Error
  400 Bad Request - Invalid input
  401 Unauthorized - Authentication required
  403 Forbidden - Authenticated but not permitted
  404 Not Found - Resource doesn't exist
  409 Conflict - State conflict (duplicate)
  422 Unprocessable Entity - Validation failed
  429 Too Many Requests - Rate limited

5xx Server Error
  500 Internal Server Error - Unexpected failure
  502 Bad Gateway - Upstream failure
  503 Service Unavailable - Temporary unavailability
```

### Response Structure

```json
// Success (single resource)
{
  "data": { "id": "123", "name": "Example" },
  "meta": { "requestId": "abc-123" }
}

// Success (collection)
{
  "data": [{ "id": "1" }, { "id": "2" }],
  "meta": { "total": 100, "page": 1, "perPage": 20 }
}

// Error
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid email format",
    "details": [
      { "field": "email", "message": "Must be valid email" }
    ]
  }
}
```

### Pagination

```
# Offset-based (simple, not scalable)
GET /users?page=2&per_page=20

# Cursor-based (scalable, recommended)
GET /users?cursor=eyJpZCI6MTAwfQ&limit=20
```

### Filtering & Sorting

```
# Filtering
GET /users?status=active&role=admin

# Sorting
GET /users?sort=created_at:desc,name:asc

# Field selection
GET /users?fields=id,name,email
```

### Versioning

```
# URL versioning (recommended)
GET /v1/users

# Header versioning
Accept: application/vnd.api+json; version=1
```

## GraphQL Best Practices

### Schema Design
- Use specific types over generic ones
- Prefer nullable fields (explicit over implicit)
- Use enums for fixed sets
- Add descriptions to all types

### Query Patterns
```graphql
# Good: Specific query
query GetUserOrders($userId: ID!, $limit: Int = 10) {
  user(id: $userId) {
    orders(first: $limit) {
      edges {
        node { id, total, status }
      }
      pageInfo { hasNextPage, endCursor }
    }
  }
}
```

### Mutation Patterns
```graphql
# Good: Input types and payloads
mutation CreateUser($input: CreateUserInput!) {
  createUser(input: $input) {
    user { id, name }
    errors { field, message }
  }
}
```

## Rate Limiting

```
# Response headers
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1609459200
Retry-After: 3600
```

## Authentication

- Use Bearer tokens in Authorization header
- Short-lived access tokens (15 min)
- Long-lived refresh tokens (7-30 days)
- Never pass tokens in URLs
