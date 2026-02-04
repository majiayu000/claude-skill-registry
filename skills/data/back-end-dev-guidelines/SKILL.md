---
name: back-end-dev-guidelines
description: Comprehensive backend development guidelines covering API design, database patterns, security, performance, and production-ready code standards.
version: 1.0.0
author: Perry
---

# Backend Development Guidelines

You are a senior backend engineer focused on building scalable, maintainable, and secure server-side applications.

## Core Principles

1. **Security First** - Never trust user input, always validate and sanitize
2. **Fail Fast** - Validate early, return meaningful errors
3. **Idempotency** - Design operations that can be safely retried
4. **Observability** - Log, monitor, and trace everything important
5. **Simplicity** - Prefer boring, proven technology over shiny and new

## API Design Standards

### RESTful Conventions

```
GET    /resources          # List resources
GET    /resources/:id      # Get single resource
POST   /resources          # Create resource
PUT    /resources/:id      # Replace resource
PATCH  /resources/:id      # Partial update
DELETE /resources/:id      # Delete resource
```

### Naming Conventions
- Use plural nouns for resources: `/users`, `/orders`
- Use kebab-case for multi-word: `/order-items`
- Nest for relationships: `/users/:id/orders`
- Use query params for filtering: `/users?status=active&role=admin`

### Response Format

```json
{
  "success": true,
  "data": { },
  "meta": {
    "page": 1,
    "limit": 20,
    "total": 100
  }
}
```

### Error Response Format

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": [
      { "field": "email", "message": "Invalid email format" }
    ]
  }
}
```

### HTTP Status Codes
- `200` - Success
- `201` - Created
- `204` - No Content (successful delete)
- `400` - Bad Request (validation error)
- `401` - Unauthorized (not authenticated)
- `403` - Forbidden (not authorized)
- `404` - Not Found
- `409` - Conflict (duplicate resource)
- `422` - Unprocessable Entity
- `429` - Too Many Requests
- `500` - Internal Server Error

## Database Patterns

### Query Optimization
- Always use indexes for frequently queried columns
- Avoid SELECT * - specify needed columns
- Use EXPLAIN to analyze query performance
- Implement pagination for list endpoints
- Use database connection pooling

### Transaction Patterns

```typescript
async function transferFunds(fromId: string, toId: string, amount: number) {
  const client = await pool.connect();
  try {
    await client.query('BEGIN');

    await client.query(
      'UPDATE accounts SET balance = balance - $1 WHERE id = $2',
      [amount, fromId]
    );

    await client.query(
      'UPDATE accounts SET balance = balance + $1 WHERE id = $2',
      [amount, toId]
    );

    await client.query('COMMIT');
  } catch (error) {
    await client.query('ROLLBACK');
    throw error;
  } finally {
    client.release();
  }
}
```

### Migration Best Practices
- Always write reversible migrations
- Never modify production data in migrations
- Test migrations against production-like data
- Use transactions for schema changes when possible

## Security Checklist

### Authentication
- [ ] Use secure password hashing (bcrypt, argon2)
- [ ] Implement rate limiting on auth endpoints
- [ ] Use short-lived JWTs with refresh tokens
- [ ] Invalidate tokens on password change
- [ ] Implement account lockout after failed attempts

### Authorization
- [ ] Implement role-based access control (RBAC)
- [ ] Check permissions at service layer
- [ ] Never expose internal IDs if possible (use UUIDs)
- [ ] Validate ownership before operations

### Input Validation
- [ ] Validate all input at API boundary
- [ ] Use parameterized queries (prevent SQL injection)
- [ ] Sanitize output (prevent XSS)
- [ ] Validate file uploads (type, size, content)
- [ ] Implement request size limits

### Data Protection
- [ ] Encrypt sensitive data at rest
- [ ] Use TLS for all connections
- [ ] Never log sensitive data (passwords, tokens, PII)
- [ ] Implement proper CORS policies
- [ ] Set security headers (HSTS, CSP, etc.)

## Error Handling

### Structured Error Classes

```typescript
class AppError extends Error {
  constructor(
    public code: string,
    public message: string,
    public statusCode: number = 500,
    public details?: unknown
  ) {
    super(message);
  }
}

class ValidationError extends AppError {
  constructor(details: Array<{ field: string; message: string }>) {
    super('VALIDATION_ERROR', 'Invalid input data', 400, details);
  }
}

class NotFoundError extends AppError {
  constructor(resource: string) {
    super('NOT_FOUND', `${resource} not found`, 404);
  }
}

class UnauthorizedError extends AppError {
  constructor(message = 'Authentication required') {
    super('UNAUTHORIZED', message, 401);
  }
}
```

### Error Handling Middleware

```typescript
function errorHandler(err: Error, req: Request, res: Response, next: NextFunction) {
  if (err instanceof AppError) {
    return res.status(err.statusCode).json({
      success: false,
      error: {
        code: err.code,
        message: err.message,
        details: err.details
      }
    });
  }

  // Log unexpected errors
  logger.error('Unexpected error', { error: err, requestId: req.id });

  return res.status(500).json({
    success: false,
    error: {
      code: 'INTERNAL_ERROR',
      message: 'An unexpected error occurred'
    }
  });
}
```

## Logging Standards

### What to Log
- Request/response metadata (method, path, status, duration)
- Authentication events (login, logout, failed attempts)
- Authorization failures
- Business-critical operations
- Errors with full context

### Log Format

```json
{
  "timestamp": "2024-01-15T10:30:00.000Z",
  "level": "info",
  "message": "Request completed",
  "requestId": "abc-123",
  "userId": "user-456",
  "method": "POST",
  "path": "/api/orders",
  "statusCode": 201,
  "duration": 145
}
```

### Never Log
- Passwords or tokens
- Full credit card numbers
- Social security numbers
- Personal health information
- Raw request bodies with sensitive data

## Performance Guidelines

### Caching Strategy
- Cache expensive computations
- Use Redis for session/token storage
- Implement cache invalidation strategy
- Set appropriate TTLs
- Consider cache warming for critical data

### Async Patterns
- Use message queues for long-running tasks
- Implement retry with exponential backoff
- Set timeouts on external calls
- Use circuit breakers for unreliable services

### Database Performance
- Connection pooling (min/max connections)
- Read replicas for heavy read workloads
- Implement database-level caching
- Regular VACUUM/ANALYZE for PostgreSQL
- Monitor slow queries

## Testing Requirements

### Unit Tests
- Test business logic in isolation
- Mock external dependencies
- Aim for 80%+ coverage on critical paths

### Integration Tests
- Test API endpoints end-to-end
- Use test database with fixtures
- Test error scenarios

### Load Tests
- Baseline performance metrics
- Test under expected peak load
- Identify breaking points

## Code Review Checklist

- [ ] Input validation present
- [ ] Error handling implemented
- [ ] Logging added for important operations
- [ ] Database queries optimized
- [ ] No sensitive data exposed
- [ ] Tests cover happy path and errors
- [ ] Documentation updated
