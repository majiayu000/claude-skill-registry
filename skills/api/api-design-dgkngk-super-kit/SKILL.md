---
name: api-design
description: RESTful API patterns, GraphQL design, and API best practices. Use when designing APIs, choosing between REST/GraphQL/tRPC, structuring endpoints, versioning, or documenting APIs.
---

# API Design Skill

## Overview
RESTful API patterns, GraphQL design, and API best practices.

## RESTful Design Principles

### 1. Resource Naming
```
✅ Good:
GET    /users          # List users
GET    /users/123      # Get user
POST   /users          # Create user
PUT    /users/123      # Update user
DELETE /users/123      # Delete user

❌ Bad:
GET /getUsers
POST /createUser
GET /user/delete/123
```

### 2. HTTP Status Codes
```typescript
// Success
200 OK           - Successful GET/PUT
201 Created      - Successful POST
204 No Content   - Successful DELETE

// Client Errors
400 Bad Request      - Invalid input
401 Unauthorized     - Auth required
403 Forbidden        - No permission
404 Not Found        - Resource doesn't exist
422 Unprocessable    - Validation failed

// Server Errors
500 Internal Error   - Server bug
503 Service Unavailable - Maintenance
```

### 3. Response Format
```typescript
// Success response
{
  "data": {
    "id": "123",
    "name": "John",
    "email": "john@example.com"
  }
}

// Error response
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Email is required",
    "details": [
      { "field": "email", "message": "This field is required" }
    ]
  }
}

// List with pagination
{
  "data": [...],
  "meta": {
    "page": 1,
    "perPage": 20,
    "total": 150,
    "totalPages": 8
  }
}
```

### 4. Pagination
```typescript
// Offset-based
GET /posts?page=2&limit=20

// Cursor-based (better for large datasets)
GET /posts?cursor=abc123&limit=20
```

### 5. Filtering & Sorting
```typescript
// Filtering
GET /posts?status=published&author=123

// Sorting
GET /posts?sort=-createdAt,title  // - for DESC
```

## API Versioning
```typescript
// URL versioning (recommended)
GET /api/v1/users

// Header versioning
GET /api/users
Accept: application/vnd.myapp.v1+json
```

## Rate Limiting
```typescript
import rateLimit from 'express-rate-limit';

const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // 100 requests per window
  message: { error: 'Too many requests' },
});

app.use('/api/', limiter);
```

## Input Validation
```typescript
import { z } from 'zod';

const CreateUserSchema = z.object({
  name: z.string().min(2).max(100),
  email: z.string().email(),
  age: z.number().int().min(0).max(150).optional(),
});

function createUser(req, res) {
  const result = CreateUserSchema.safeParse(req.body);
  if (!result.success) {
    return res.status(422).json({ error: result.error });
  }
  // Process validated data
}
```
