---
document_name: "api-development.skill.md"
location: ".claude/skills/api-development.skill.md"
codebook_id: "CB-SKILL-APIDEV-001"
version: "1.0.0"
date_created: "2026-01-04"
date_last_edited: "2026-01-04"
document_type: "skill"
purpose: "Procedures for API design and implementation"
skill_metadata:
  category: "development"
  complexity: "intermediate"
  estimated_time: "varies"
  prerequisites:
    - "Backend framework knowledge"
    - "HTTP fundamentals"
category: "skills"
status: "active"
tags:
  - "skill"
  - "backend"
  - "api"
  - "rest"
  - "graphql"
ai_parser_instructions: |
  This skill defines procedures for API development.
  Used by Backend Engineer agent.
---

# API Development Skill

=== PURPOSE ===

Procedures for designing and implementing RESTful and GraphQL APIs.

=== USED BY ===

| Agent | Purpose |
|-------|---------|
| @agent(backend-engineer) @ref(CB-AGENT-BACKEND-001) | Primary skill for API work |

=== PROCEDURE: REST Endpoint Design ===

**URL Structure:**
```
GET    /api/v1/{resource}           # List
GET    /api/v1/{resource}/{id}      # Get one
POST   /api/v1/{resource}           # Create
PUT    /api/v1/{resource}/{id}      # Replace
PATCH  /api/v1/{resource}/{id}      # Update
DELETE /api/v1/{resource}/{id}      # Delete
```

**Nested Resources:**
```
GET    /api/v1/users/{userId}/posts     # User's posts
POST   /api/v1/users/{userId}/posts     # Create user's post
```

**Query Parameters:**
```
?page=1&limit=20          # Pagination
?sort=createdAt:desc      # Sorting
?filter[status]=active    # Filtering
?include=author,comments  # Eager loading
```

=== PROCEDURE: Response Format ===

**Success Response:**
```json
{
  "success": true,
  "data": {
    "id": "123",
    "type": "user",
    "attributes": {}
  },
  "meta": {
    "timestamp": "2026-01-04T12:00:00Z"
  }
}
```

**List Response:**
```json
{
  "success": true,
  "data": [],
  "meta": {
    "pagination": {
      "page": 1,
      "limit": 20,
      "total": 100,
      "totalPages": 5
    }
  }
}
```

**Error Response:**
```json
{
  "success": false,
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

=== PROCEDURE: HTTP Status Codes ===

| Code | Meaning | When to Use |
|------|---------|-------------|
| 200 | OK | Successful GET, PUT, PATCH |
| 201 | Created | Successful POST |
| 204 | No Content | Successful DELETE |
| 400 | Bad Request | Validation errors |
| 401 | Unauthorized | Missing/invalid auth |
| 403 | Forbidden | Valid auth, no permission |
| 404 | Not Found | Resource doesn't exist |
| 409 | Conflict | Duplicate, constraint violation |
| 422 | Unprocessable | Semantic validation error |
| 500 | Server Error | Unexpected error |

=== PROCEDURE: Input Validation ===

**Validation Layers:**
1. Schema validation (request body structure)
2. Type validation (data types correct)
3. Business validation (rules met)
4. Authorization (user can perform action)

**Example (Zod/TypeScript):**
```typescript
const createUserSchema = z.object({
  email: z.string().email(),
  name: z.string().min(1).max(100),
  role: z.enum(['user', 'admin']).optional(),
});

// In controller
const result = createUserSchema.safeParse(req.body);
if (!result.success) {
  return res.status(400).json({
    success: false,
    error: {
      code: 'VALIDATION_ERROR',
      details: result.error.issues
    }
  });
}
```

=== PROCEDURE: Authentication ===

**JWT Pattern:**
```
Authorization: Bearer <token>
```

**Middleware Structure:**
```typescript
export const authenticate = async (req, res, next) => {
  const token = req.headers.authorization?.replace('Bearer ', '');

  if (!token) {
    return res.status(401).json({
      success: false,
      error: { code: 'UNAUTHORIZED', message: 'Token required' }
    });
  }

  try {
    const payload = verifyToken(token);
    req.user = payload;
    next();
  } catch {
    return res.status(401).json({
      success: false,
      error: { code: 'INVALID_TOKEN', message: 'Invalid token' }
    });
  }
};
```

=== PROCEDURE: Error Handling ===

**Global Error Handler:**
```typescript
export const errorHandler = (err, req, res, next) => {
  // Log error (never expose internals)
  console.error(err);

  // Known errors
  if (err instanceof ValidationError) {
    return res.status(400).json({
      success: false,
      error: { code: 'VALIDATION_ERROR', message: err.message }
    });
  }

  // Unknown errors
  res.status(500).json({
    success: false,
    error: { code: 'INTERNAL_ERROR', message: 'Internal server error' }
  });
};
```

=== PROCEDURE: API Versioning ===

**URL Versioning (Recommended):**
```
/api/v1/users
/api/v2/users
```

**Version Deprecation:**
1. Announce deprecation 90 days in advance
2. Add `Deprecation` header to responses
3. Log usage of deprecated endpoints
4. Remove after migration period

=== RELATED SKILLS ===

| Skill | Relationship |
|-------|--------------|
| @skill(backend-patterns) | Architecture context |
| @skill(security-review) | Security requirements |
