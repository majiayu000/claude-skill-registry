---
name: backend-api-development
description: Build and optimize Node.js, Express, and Python backend services. USE THIS for API design, server setup, middleware, authentication, database connection, error handling, and microservices. Include when user mentions backend, API endpoints, server setup, database queries, authentication, or building REST/GraphQL APIs.
---

# Backend & API Development Skill

Build production-grade backend services with best practices in mind.

## Your Backend Stack

### Node.js/Express
- **Framework**: Express.js
- **Runtime**: Node.js 18+
- **Language**: JavaScript/TypeScript
- **Database**: PostgreSQL, MongoDB, or SQLite (context-dependent)
- **Authentication**: JWT or session-based

### Python
- **Web Framework**: Flask or FastAPI
- **Runtime**: Python 3.9+
- **Async Support**: asyncio/aiohttp
- **Database**: Same as Node stack

## Key Responsibilities

### API Design
```javascript
// RESTful conventions
GET    /api/resource      // List all
GET    /api/resource/:id  // Get one
POST   /api/resource      // Create
PUT    /api/resource/:id  // Update
DELETE /api/resource/:id  // Delete
```

### Error Handling & Responses
```javascript
// Consistent response format
{
  status: 'success' | 'error',
  data: {},           // For successful responses
  error: {            // For errors
    code: 'ERROR_CODE',
    message: 'Human readable',
    details: {}
  },
  timestamp: ISO8601
}
```

### Middleware Pattern
```javascript
// Standard Express middleware order:
1. Body parser
2. CORS / Security headers
3. Request logging
4. Authentication
5. Route handlers
6. Error handling (last)
```

### Database Queries
- Use parameterized queries (prevent SQL injection)
- Implement connection pooling
- Add query logging for debugging
- Cache frequently accessed data

### Authentication & Security
- JWT tokens with expiration
- Secure password hashing (bcrypt/argon2)
- CORS properly configured
- Rate limiting on sensitive endpoints
- Environment variables for secrets

## Code Quality Standards

### TypeScript Preference
```typescript
// Type all endpoints
interface APIResponse<T> {
  status: 'success' | 'error'
  data?: T
  error?: APIError
}

// Handler typing
app.get('/api/users/:id', 
  async (req: Request, res: Response<APIResponse<User>>) => {
    // typed response
  }
)
```

### Error Handling
```javascript
// Global error handler (Express)
app.use((err, req, res, next) => {
  console.error(err)
  res.status(err.status || 500).json({
    status: 'error',
    error: {
      code: err.code || 'INTERNAL_ERROR',
      message: err.message
    }
  })
})
```

### Logging Strategy
- INFO: API requests, cache hits/misses
- WARN: Deprecated endpoint usage, slow queries
- ERROR: Failed operations, exceptions
- DEBUG: Variable states, flow tracking

## Performance Best Practices

- Connection pooling for databases
- Response caching with appropriate headers
- Pagination for large datasets
- Compression (gzip) for responses
- Database indexes on frequently queried fields
- Query optimization and explain plans

## Testing

- Unit tests for business logic
- Integration tests for API endpoints
- Mock external services
- Test database fixtures
- Error case testing

## Deployment Considerations

- Environment configuration (dev/staging/prod)
- Health check endpoints (`/health`)
- Graceful shutdown handling
- Database migration strategy
- Monitoring and alerting setup

---

**Output**: Production-ready backend code with type safety, clear error handling, and scalable architecture.
