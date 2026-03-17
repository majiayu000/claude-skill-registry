---
name: api-design
description: REST API design best practices for consistent, intuitive APIs
---

# API Design Principles

Design APIs that are intuitive, consistent, and a joy to use.

## URL Structure

### Resources as Nouns
```
# GOOD - nouns
GET /users
GET /users/123
GET /users/123/orders

# BAD - verbs
GET /getUsers
GET /fetchUserById/123
POST /createNewUser
```

### Plural Resource Names
```
# GOOD - plural
GET /users
GET /orders
GET /products

# BAD - singular
GET /user
GET /order
```

### Hierarchical Relationships
```
# Parent-child relationships
GET /users/123/orders          # Orders for user 123
GET /orders/456/items          # Items in order 456

# Avoid deep nesting (max 2 levels)
# BAD
GET /users/123/orders/456/items/789/reviews

# GOOD - flatten when needed
GET /order-items/789/reviews
```

## HTTP Methods

| Method | Usage | Idempotent | Safe |
|--------|-------|------------|------|
| GET | Read resource | Yes | Yes |
| POST | Create resource | No | No |
| PUT | Replace resource | Yes | No |
| PATCH | Partial update | Yes | No |
| DELETE | Remove resource | Yes | No |

```
GET    /users          # List users
POST   /users          # Create user
GET    /users/123      # Get user 123
PUT    /users/123      # Replace user 123
PATCH  /users/123      # Update user 123
DELETE /users/123      # Delete user 123
```

## Request/Response Format

### Consistent JSON Structure
```json
// Success response
{
  "data": {
    "id": "123",
    "name": "John Doe",
    "email": "john@example.com"
  }
}

// Collection response
{
  "data": [
    { "id": "123", "name": "John" },
    { "id": "456", "name": "Jane" }
  ],
  "meta": {
    "total": 100,
    "page": 1,
    "perPage": 20
  }
}

// Error response
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid email format",
    "details": [
      { "field": "email", "message": "Must be a valid email" }
    ]
  }
}
```

### Use camelCase
```json
// GOOD
{
  "firstName": "John",
  "lastName": "Doe",
  "emailAddress": "john@example.com"
}

// BAD - inconsistent
{
  "first_name": "John",
  "LastName": "Doe",
  "email-address": "john@example.com"
}
```

## Status Codes

### Success (2xx)
```
200 OK           - GET, PUT, PATCH success
201 Created      - POST success (include Location header)
204 No Content   - DELETE success
```

### Client Errors (4xx)
```
400 Bad Request     - Invalid syntax, validation error
401 Unauthorized    - No/invalid authentication
403 Forbidden       - Authenticated but not allowed
404 Not Found       - Resource doesn't exist
409 Conflict        - State conflict (duplicate, version)
422 Unprocessable   - Valid syntax but semantic error
429 Too Many Requests - Rate limited
```

### Server Errors (5xx)
```
500 Internal Server Error - Unexpected error
502 Bad Gateway          - Upstream service failed
503 Service Unavailable  - Temporarily unavailable
504 Gateway Timeout      - Upstream timeout
```

## Pagination

### Offset-based (simple)
```
GET /users?page=2&perPage=20

Response:
{
  "data": [...],
  "meta": {
    "total": 100,
    "page": 2,
    "perPage": 20,
    "totalPages": 5
  },
  "links": {
    "first": "/users?page=1&perPage=20",
    "prev": "/users?page=1&perPage=20",
    "next": "/users?page=3&perPage=20",
    "last": "/users?page=5&perPage=20"
  }
}
```

### Cursor-based (scalable)
```
GET /users?cursor=eyJpZCI6MTIzfQ&limit=20

Response:
{
  "data": [...],
  "meta": {
    "hasMore": true,
    "nextCursor": "eyJpZCI6MTQzfQ"
  }
}
```

## Filtering & Sorting

### Filtering
```
GET /users?status=active
GET /users?role=admin&status=active
GET /users?createdAt[gte]=2024-01-01
GET /users?name[contains]=john
```

### Sorting
```
GET /users?sort=name           # Ascending
GET /users?sort=-createdAt     # Descending (prefix -)
GET /users?sort=lastName,firstName
```

### Field Selection
```
GET /users?fields=id,name,email
GET /users/123?fields=id,name,email
```

## Versioning

### URL Path (recommended)
```
GET /v1/users
GET /v2/users
```

### Header
```
GET /users
Accept: application/vnd.api+json;version=2
```

## Authentication

### Bearer Token
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

### API Key
```
X-API-Key: sk_live_abc123
# Or in query (less secure)
GET /users?api_key=sk_live_abc123
```

## Rate Limiting

Include headers:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1640995200
Retry-After: 60
```

## Documentation

Every endpoint needs:
- Description of what it does
- Request parameters with types
- Request body schema
- Response schema for each status code
- Example request/response
- Error cases

```yaml
# OpenAPI example
/users:
  post:
    summary: Create a new user
    requestBody:
      required: true
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/CreateUser'
    responses:
      '201':
        description: User created
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/User'
      '400':
        description: Validation error
```

## Common Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| Verbs in URLs | `/getUser` | Use `/users/:id` |
| Inconsistent naming | Mix of cases | Pick one (camelCase) |
| Wrong status codes | 200 for errors | Use 4xx/5xx appropriately |
| No pagination | Memory issues | Always paginate collections |
| Breaking changes | Clients break | Version your API |
| No rate limiting | Abuse | Implement limits |
| Exposing internals | Security risk | Transform responses |

## Checklist

- [ ] URLs use nouns, not verbs
- [ ] HTTP methods used correctly
- [ ] Consistent response format
- [ ] Appropriate status codes
- [ ] Pagination for collections
- [ ] Filtering and sorting support
- [ ] Rate limiting implemented
- [ ] Authentication documented
- [ ] Errors are descriptive
- [ ] API is versioned
