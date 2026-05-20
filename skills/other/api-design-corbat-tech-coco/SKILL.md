---
name: api-design
description: Design and review REST/GraphQL APIs for correctness, consistency, and security. Generates OpenAPI specs, validates endpoint design, and checks for common API pitfalls.
allowed-tools: Read, Write, Grep, Glob
---

# API Design

Design and review APIs for the project being built.

## REST API Design Principles

### URL Structure
```
# ✅ Resource-based, plural, lowercase
GET    /api/v1/users           # list users
POST   /api/v1/users           # create user
GET    /api/v1/users/:id       # get user
PUT    /api/v1/users/:id       # replace user
PATCH  /api/v1/users/:id       # partial update
DELETE /api/v1/users/:id       # delete user

# Nested resources
GET    /api/v1/users/:id/posts # user's posts
POST   /api/v1/users/:id/posts # create post for user

# ❌ Avoid verbs in URLs
POST /api/v1/createUser        # wrong
GET  /api/v1/getUserById       # wrong
```

### HTTP Status Codes
| Code | When |
|------|------|
| 200 | Success (GET, PUT, PATCH) |
| 201 | Created (POST) |
| 204 | No content (DELETE) |
| 400 | Bad request (validation error) |
| 401 | Unauthenticated |
| 403 | Unauthorized (authenticated but no permission) |
| 404 | Not found |
| 409 | Conflict (duplicate) |
| 422 | Unprocessable entity |
| 429 | Rate limited |
| 500 | Internal server error |

### Response Format
```json
// Success
{ "data": { ... }, "meta": { "total": 100, "page": 1 } }

// Error
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Email is invalid",
    "details": [{ "field": "email", "message": "Must be valid email" }]
  }
}
```

### Versioning
```
/api/v1/...   ← current stable
/api/v2/...   ← next major (when breaking changes needed)
```

## Security Checklist

- [ ] Authentication required for all non-public endpoints
- [ ] Authorization checked (user owns resource)
- [ ] Input validated (Zod/Pydantic/Bean Validation)
- [ ] Rate limiting on auth endpoints
- [ ] No sensitive data in URLs (use POST body)
- [ ] Pagination for list endpoints (no unlimited returns)
- [ ] CORS configured correctly
- [ ] API versioning strategy defined

## OpenAPI Spec Template

```yaml
openapi: 3.0.0
info:
  title: [Project] API
  version: 1.0.0
paths:
  /api/v1/resources:
    get:
      summary: List resources
      parameters:
        - name: page
          in: query
          schema: { type: integer, default: 1 }
        - name: limit
          in: query
          schema: { type: integer, default: 20, maximum: 100 }
      responses:
        "200":
          description: Success
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ResourceList'
```

## Usage

```
/api-design          # review existing API design
/api-design new      # design new API from scratch
/api-design openapi  # generate OpenAPI spec
```
