---
name: api-design-restful
description: RESTful API design patterns, error handling, and documentation
license: MIT
compatibility: nodejs 18+, express 4+, fastify 4+
allowed-tools: read_file write_file apply_patch search_with_context run_command
---

# RESTful API Design

## Core Principles

1. **Resource-Oriented** - URLs represent nouns, not verbs
2. **Stateless** - Each request contains all necessary information
3. **Consistent** - Use standard HTTP methods and status codes
4. **Versioned** - Support API evolution without breaking clients

## URL Structure

```
# Collection resources
GET    /api/v1/users           # List users
POST   /api/v1/users           # Create user

# Individual resources
GET    /api/v1/users/:id       # Get user
PUT    /api/v1/users/:id       # Replace user
PATCH  /api/v1/users/:id       # Update user
DELETE /api/v1/users/:id       # Delete user

# Nested resources
GET    /api/v1/users/:id/posts # User's posts
POST   /api/v1/users/:id/posts # Create post for user

# Filtering, sorting, pagination
GET    /api/v1/users?status=active&sort=-createdAt&page=2&limit=20
```

## Response Structure

### Success Response
```typescript
interface SuccessResponse<T> {
  success: true;
  data: T;
  meta?: {
    page?: number;
    limit?: number;
    total?: number;
    totalPages?: number;
  };
}

// Example
{
  "success": true,
  "data": { "id": "123", "name": "John" },
  "meta": { "requestId": "abc-123" }
}
```

### Error Response
```typescript
interface ErrorResponse {
  success: false;
  error: {
    code: string;        // Machine-readable code
    message: string;     // Human-readable message
    details?: unknown;   // Field-level errors
  };
}

// Example
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid request body",
    "details": {
      "email": "Invalid email format",
      "age": "Must be a positive number"
    }
  }
}
```

## HTTP Status Codes

```typescript
// Success
200 OK              // Successful GET, PUT, PATCH
201 Created         // Successful POST
204 No Content      // Successful DELETE

// Client Errors
400 Bad Request     // Validation errors
401 Unauthorized    // Missing/invalid auth
403 Forbidden       // Insufficient permissions
404 Not Found       // Resource doesn't exist
409 Conflict        // Duplicate/state conflict
422 Unprocessable   // Semantic errors
429 Too Many Reqs   // Rate limited

// Server Errors
500 Internal Error  // Unexpected server error
503 Unavailable     // Service temporarily down
```

## Express.js Implementation

```typescript
import express from 'express';

const app = express();

// Async handler wrapper
const asyncHandler = (fn: RequestHandler) => (req, res, next) =>
  Promise.resolve(fn(req, res, next)).catch(next);

// Controller
const getUsers = asyncHandler(async (req, res) => {
  const { page = 1, limit = 20, status } = req.query;
  const { users, total } = await userService.findAll({ page, limit, status });

  res.json({
    success: true,
    data: users,
    meta: { page, limit, total, totalPages: Math.ceil(total / limit) }
  });
});

// Error handler middleware
app.use((err, req, res, next) => {
  const status = err.status || 500;
  res.status(status).json({
    success: false,
    error: {
      code: err.code || 'INTERNAL_ERROR',
      message: err.message || 'Something went wrong',
      ...(process.env.NODE_ENV === 'development' && { stack: err.stack })
    }
  });
});
```

## Validation with Zod

```typescript
import { z } from 'zod';

const createUserSchema = z.object({
  email: z.string().email(),
  name: z.string().min(2).max(100),
  role: z.enum(['user', 'admin']).default('user'),
});

// Middleware
const validate = (schema: z.ZodSchema) => (req, res, next) => {
  const result = schema.safeParse(req.body);
  if (!result.success) {
    return res.status(400).json({
      success: false,
      error: {
        code: 'VALIDATION_ERROR',
        message: 'Invalid request body',
        details: result.error.flatten().fieldErrors
      }
    });
  }
  req.body = result.data;
  next();
};

app.post('/users', validate(createUserSchema), createUser);
```

## Authentication

```typescript
// JWT middleware
const authenticate = asyncHandler(async (req, res, next) => {
  const token = req.headers.authorization?.replace('Bearer ', '');
  if (!token) {
    throw new ApiError(401, 'UNAUTHORIZED', 'Missing auth token');
  }

  const payload = await verifyToken(token);
  req.user = payload;
  next();
});

// Role-based authorization
const authorize = (...roles: string[]) => (req, res, next) => {
  if (!roles.includes(req.user.role)) {
    throw new ApiError(403, 'FORBIDDEN', 'Insufficient permissions');
  }
  next();
};

app.delete('/users/:id', authenticate, authorize('admin'), deleteUser);
```

## Rate Limiting

```typescript
import rateLimit from 'express-rate-limit';

const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100,
  standardHeaders: true,
  legacyHeaders: false,
  handler: (req, res) => {
    res.status(429).json({
      success: false,
      error: {
        code: 'RATE_LIMITED',
        message: 'Too many requests, please try again later'
      }
    });
  }
});

app.use('/api/', limiter);
```

## Best Practices

1. **Use plural nouns** for resources (`/users` not `/user`)
2. **Version your API** from day one (`/api/v1/`)
3. **Return appropriate status codes** for every response
4. **Include request IDs** in responses for debugging
5. **Document with OpenAPI/Swagger** specification
6. **Implement pagination** for list endpoints
7. **Use consistent error format** across all endpoints
8. **Log all requests** with correlation IDs
