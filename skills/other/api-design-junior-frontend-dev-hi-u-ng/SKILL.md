---
name: api-design
description: Design RESTful APIs following conventions with proper error
  handling, versioning, and documentation. Use when creating or modifying
  API endpoints.
---

# API Design Skill

## Purpose
Create consistent, well-designed APIs.

## REST Conventions
Reference: [standards/rest-conventions.md](standards/rest-conventions.md)

### HTTP Methods
| Method | Use Case | Idempotent |
|--------|----------|------------|
| GET | Retrieve resource | Yes |
| POST | Create resource | No |
| PUT | Replace resource | Yes |
| PATCH | Partial update | No |
| DELETE | Remove resource | Yes |

### URL Patterns
```
GET    /users           # List users
GET    /users/:id       # Get user
POST   /users           # Create user
PUT    /users/:id       # Replace user
PATCH  /users/:id       # Update user
DELETE /users/:id       # Delete user

GET    /users/:id/posts # Nested resource
```

### Response Status Codes
| Code | Meaning | Use When |
|------|---------|----------|
| 200 | OK | Successful GET, PUT, PATCH |
| 201 | Created | Successful POST |
| 204 | No Content | Successful DELETE |
| 400 | Bad Request | Validation error |
| 401 | Unauthorized | Auth required |
| 403 | Forbidden | Auth insufficient |
| 404 | Not Found | Resource doesn't exist |
| 422 | Unprocessable | Business rule violation |
| 500 | Server Error | Unexpected error |

## Error Response Format
Reference: [standards/error-responses.md](standards/error-responses.md)

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Validation failed",
    "details": [
      {
        "field": "email",
        "message": "Invalid email format"
      }
    ]
  }
}
```

## Versioning
Reference: [standards/versioning.md](standards/versioning.md)

Options:
- URL: `/api/v1/users`
- Header: `Accept: application/vnd.api.v1+json`

Recommendation: URL versioning for simplicity

## Endpoint Documentation
Use template: [templates/endpoint-doc.md](templates/endpoint-doc.md)
