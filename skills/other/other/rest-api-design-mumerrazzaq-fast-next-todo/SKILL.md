---
name: rest-api-design
description: |
  RESTful API design and OpenAPI specification generation. Use when: (1) Designing new REST API endpoints, (2) Creating OpenAPI/Swagger specifications, (3) Choosing HTTP methods, status codes, or URL patterns, (4) Implementing pagination, filtering, or sorting, (5) Planning API versioning strategy, (6) Reviewing API design for best practices, (7) Generating API documentation templates.
---

# REST API Design

Design RESTful APIs following industry standards and generate OpenAPI 3.0 specifications.

## Quick Reference

### Endpoint Pattern
```
GET    /resources           # List
POST   /resources           # Create
GET    /resources/{id}      # Read
PUT    /resources/{id}      # Replace
PATCH  /resources/{id}      # Update
DELETE /resources/{id}      # Delete
```

### Status Code Selection
```
Success:  200 OK | 201 Created | 204 No Content
Client:   400 Bad Request | 401 Unauthorized | 403 Forbidden
          404 Not Found | 409 Conflict | 422 Validation Error
Server:   500 Internal Error | 503 Unavailable
```

### URL Naming Rules
- Plural nouns: `/users`, `/products`
- Lowercase with hyphens: `/user-profiles`
- No verbs in paths (HTTP methods are verbs)
- Max 2-3 nesting levels

## Workflow

### 1. Design Endpoints
Define resources and their relationships:
```yaml
# Core resource
/items                    # Collection
/items/{itemId}           # Instance

# Sub-resources (if tightly coupled)
/items/{itemId}/comments  # Nested collection
```

See [naming-conventions.md](references/naming-conventions.md) for complete patterns.

### 2. Select HTTP Methods
Choose based on operation semantics:

| Operation | Method | Idempotent |
|-----------|--------|------------|
| Fetch data | GET | Yes |
| Create new | POST | No |
| Replace all | PUT | Yes |
| Update partial | PATCH | No |
| Remove | DELETE | Yes |

See [http-methods.md](references/http-methods.md) for decision tree.

### 3. Define Status Codes
Match response to outcome:

```
Creating resource?     → 201 + Location header
Deleting resource?     → 204 (no body)
Validation failed?     → 422 + error details
Auth missing?          → 401
Auth insufficient?     → 403
Not found?             → 404
```

See [status-codes.md](references/status-codes.md) for complete decision tree.

### 4. Add Pagination & Filtering
For collection endpoints:

```yaml
parameters:
  - name: page
    in: query
    schema: { type: integer, default: 1 }
  - name: limit
    in: query
    schema: { type: integer, default: 20, maximum: 100 }
  - name: sort
    in: query
    schema: { type: string }
    description: "field:direction (e.g., created_at:desc)"
```

See [pagination-filtering-sorting.md](references/pagination-filtering-sorting.md) for patterns.

### 5. Choose Versioning Strategy
Recommended: URI path versioning

```
https://api.example.com/v1/users
https://api.example.com/v2/users
```

See [versioning.md](references/versioning.md) for alternatives.

### 6. Generate OpenAPI Spec
Use the template at [assets/openapi-template.yaml](assets/openapi-template.yaml).

Replace placeholders:
- `${API_TITLE}` - Your API name
- `${API_DESCRIPTION}` - API overview
- `${API_VERSION}` - Semantic version

### 7. Validate Design
Run through [validation-checklist.md](references/validation-checklist.md).

## Common Patterns

### Error Response
```yaml
Error:
  type: object
  required: [code, message]
  properties:
    code:
      type: string
      example: VALIDATION_ERROR
    message:
      type: string
      example: Validation failed
    details:
      type: array
      items:
        type: object
        properties:
          field: { type: string }
          message: { type: string }
    requestId:
      type: string
```

### Pagination Response
```yaml
ListResponse:
  type: object
  properties:
    data:
      type: array
      items: { $ref: '#/components/schemas/Resource' }
    pagination:
      type: object
      properties:
        page: { type: integer }
        limit: { type: integer }
        totalItems: { type: integer }
        totalPages: { type: integer }
```

### Resource with Timestamps
```yaml
Resource:
  type: object
  required: [id, createdAt, updatedAt]
  properties:
    id:
      type: string
      format: uuid
      readOnly: true
    createdAt:
      type: string
      format: date-time
      readOnly: true
    updatedAt:
      type: string
      format: date-time
      readOnly: true
```

## Resources

| File | Purpose |
|------|---------|
| [openapi-template.yaml](assets/openapi-template.yaml) | Complete OpenAPI 3.0 template with sample CRUD API |
| [naming-conventions.md](references/naming-conventions.md) | URL patterns, resource naming, query parameters |
| [http-methods.md](references/http-methods.md) | Method selection guide, PUT vs PATCH |
| [status-codes.md](references/status-codes.md) | Status code decision tree, error format |
| [pagination-filtering-sorting.md](references/pagination-filtering-sorting.md) | Collection query patterns |
| [versioning.md](references/versioning.md) | API versioning strategies |
| [validation-checklist.md](references/validation-checklist.md) | Pre-implementation review checklist |
