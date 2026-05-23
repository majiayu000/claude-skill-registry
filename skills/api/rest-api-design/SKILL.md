---
name: rest-api-design
description: Designs RESTful APIs with proper resource naming, HTTP methods, status codes, and response formats. Use when building new APIs, establishing API conventions, or designing developer-friendly interfaces.
---

# REST API Design

Design RESTful APIs with proper conventions and developer experience.

## Resource Naming

```
# Good - nouns, plural, hierarchical
GET    /api/users
GET    /api/users/123
GET    /api/users/123/orders
POST   /api/users
PATCH  /api/users/123
DELETE /api/users/123

# Bad - verbs, actions in URL
GET    /api/getUsers
POST   /api/createUser
POST   /api/users/123/delete
```

## HTTP Methods

| Method | Purpose | Idempotent |
|--------|---------|------------|
| GET | Read resource | Yes |
| POST | Create resource | No |
| PUT | Replace resource | Yes |
| PATCH | Partial update | Yes |
| DELETE | Remove resource | Yes |

## Status Codes

| Code | Meaning | Use For |
|------|---------|---------|
| 200 | OK | Successful GET, PATCH |
| 201 | Created | Successful POST |
| 204 | No Content | Successful DELETE |
| 400 | Bad Request | Validation errors |
| 401 | Unauthorized | Missing auth |
| 403 | Forbidden | Insufficient permissions |
| 404 | Not Found | Resource doesn't exist |
| 429 | Too Many Requests | Rate limited |

## Response Format

```json
{
  "data": {
    "id": "123",
    "type": "user",
    "attributes": {
      "name": "John",
      "email": "john@example.com"
    }
  },
  "meta": {
    "requestId": "req_abc123"
  }
}
```

## Collection Response

```json
{
  "data": [...],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 150,
    "totalPages": 8
  },
  "links": {
    "self": "/api/users?page=1",
    "next": "/api/users?page=2"
  }
}
```

## Query Parameters

```
GET /api/products?category=electronics    # Filtering
GET /api/products?sort=-price,name        # Sorting
GET /api/products?page=2&limit=20         # Pagination
GET /api/products?fields=id,name,price    # Field selection
```

## Best Practices

- Use nouns for resources, not verbs
- Version API via URL path (`/api/v1/`)
- Return appropriate status codes
- Include pagination for collections
- Document with OpenAPI/Swagger
