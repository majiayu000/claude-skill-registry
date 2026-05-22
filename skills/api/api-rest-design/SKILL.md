---
name: api-rest-design
description: Apply when designing RESTful APIs, defining endpoints, HTTP methods, status codes, and response formats.
version: 1.1.0
tokens: ~700
confidence: high
sources:
  - https://restfulapi.net/
  - https://www.rfc-editor.org/rfc/rfc9110
last_validated: 2025-12-10
next_review: 2025-12-24
tags: [api, rest, backend, design]
---

## When to Use

Apply when designing RESTful APIs, defining endpoints, HTTP methods, status codes, and response formats.

## Patterns

### Pattern 1: Resource Naming
```
# Source: https://restfulapi.net/resource-naming/
GOOD:
GET    /users              # List users
GET    /users/123          # Get user 123
POST   /users              # Create user
PUT    /users/123          # Update user 123
DELETE /users/123          # Delete user 123
GET    /users/123/orders   # User's orders (nested resource)

BAD:
GET    /getUsers           # Verb in URL
POST   /createUser         # Verb in URL
GET    /user/123           # Singular (use plural)
```

### Pattern 2: HTTP Status Codes
```
# Source: https://www.rfc-editor.org/rfc/rfc9110
Success:
200 OK           - GET/PUT success with body
201 Created      - POST success, include Location header
204 No Content   - DELETE success, no body

Client Errors:
400 Bad Request  - Invalid input/payload
401 Unauthorized - Missing/invalid auth
403 Forbidden    - Auth valid, no permission
404 Not Found    - Resource doesn't exist
409 Conflict     - Resource state conflict
422 Unprocessable - Validation failed

Server Errors:
500 Internal     - Unexpected server error
503 Unavailable  - Service temporarily down
```

### Pattern 3: Response Format
```typescript
// Source: https://restfulapi.net/
// Success response
{
  "data": { "id": 123, "name": "John" },
  "meta": { "timestamp": "2025-12-10T12:00:00Z" }
}

// Error response
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid email format",
    "details": [{ "field": "email", "message": "Must be valid email" }]
  }
}

// List with pagination
{
  "data": [...],
  "meta": { "total": 100, "page": 1, "limit": 20 }
}
```

### Pattern 4: Filtering & Pagination
```
# Source: https://restfulapi.net/
GET /users?status=active&role=admin     # Filter
GET /users?sort=created_at:desc         # Sort
GET /users?page=2&limit=20              # Pagination
GET /users?fields=id,name,email         # Field selection
```

### Pattern 5: Versioning
```
# Source: https://restfulapi.net/versioning/
URL path (recommended):
GET /api/v1/users

Header (alternative):
Accept: application/vnd.api+json;version=1
```

## Anti-Patterns

- **Verbs in URLs** - Use nouns: `/users` not `/getUsers`
- **Wrong status codes** - Don't return 200 for errors
- **Inconsistent responses** - Same format for all endpoints
- **Missing pagination** - Always paginate lists
- **No versioning** - Plan for API evolution

## Verification Checklist

- [ ] Resource URLs use plural nouns
- [ ] Correct HTTP methods (GET read, POST create, etc.)
- [ ] Appropriate status codes returned
- [ ] Consistent error response format
- [ ] Pagination on list endpoints
- [ ] API versioning strategy defined
