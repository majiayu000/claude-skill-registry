---
name: fullstack-backend-master
description: Master-level fullstack software engineering with deep backend expertise.
  Use when building production-grade APIs, database architectures, authentication
  systems, microservices, or any backend-heavy ap
---

---
name: fullstack-backend-master
description: Master-level fullstack software engineering with deep backend expertise. Use when building production-grade APIs, database architectures, authentication systems, microservices, or any backend-heavy application. Triggers on: (1) API design and implementation, (2) Database schema design and optimization, (3) Authentication/authorization systems, (4) System architecture decisions, (5) Performance optimization, (6) Error handling and logging, (7) Testing strategies, (8) DevOps and deployment, (9) Security hardening.
---

# Fullstack Backend Master

Expert-level guidance for building robust, scalable, production-ready backend systems.

## Core Philosophy

**Build for the unhappy path first.** Errors, edge cases, and failures define production quality.

**Optimize for debuggability.** Structured logging, correlation IDs, and clear error messages save hours.

**Security is non-negotiable.** Input validation, parameterized queries, and principle of least privilege always.

## API Design

### REST Conventions

```
GET    /resources          → List (paginated)
GET    /resources/:id      → Get one
POST   /resources          → Create
PUT    /resources/:id      → Full update
PATCH  /resources/:id      → Partial update
DELETE /resources/:id      → Delete

# Nested resources
GET    /users/:userId/posts
POST   /users/:userId/posts

# Actions (when CRUD doesn't fit)
POST   /orders/:id/cancel
POST   /users/:id/verify-email
```

### Response Structure

```json
// Success
{
  "data": { ... },
  "meta": { "page": 1, "total": 100 }
}

// Error
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Email is required",
    "details": [{ "field": "email", "issue": "required" }]
  }
}
```

### Status Codes

| Code | Use Case |
|------|----------|
| 200 | Success with body |
| 201 | Created (return created resource) |
| 204 | Success, no content (DELETE) |
| 400 | Validation error (client's fault) |
| 401 | Not authenticated |
| 403 | Authenticated but not authorized |
| 404 | Resource not found |
| 409 | Conflict (duplicate, state conflict) |
| 422 | Unprocessable (valid JSON, invalid semantics) |
| 429 | Rate limited |
| 500 | Server error (never expose stack traces) |

## Database Design

### Schema Principles

1. **Always include audit columns**: `created_at`, `updated_at`, `deleted_at` (soft delete)
2. **UUID vs Integer IDs**: UUIDs for distributed systems, integers for simplicity
3. **Normalize first, denormalize for performance**: Start with 3NF, add caching/denormalization when measured
4. **Index strategically**: Index foreign keys, frequently queried columns, composite indexes for multi-column WHERE

### Migration Patterns

```sql
-- Always reversible migrations
-- UP
ALTER TABLE users ADD COLUMN phone VARCHAR(20);

-- DOWN
ALTER TABLE users DROP COLUMN phone;
```

### Query Optimization

- Use `EXPLAIN ANALYZE` before production
- Avoid `SELECT *` in application code
- Use connection pooling (pgbouncer, HikariCP)
- Implement pagination with cursor-based (keyset) for large datasets

## Authentication & Authorization

### Token Strategy

```
Access Token:  Short-lived (15-60 min), stateless JWT
Refresh Token: Long-lived (7-30 days), stored server-side, rotatable
```

### JWT Best Practices

- Sign with RS256 (asymmetric) for microservices, HS256 for monoliths
- Include: `sub`, `exp`, `iat`, `iss`, roles/permissions
- Never include: passwords, PII, sensitive data
- Validate: signature, expiry, issuer, audience

### Authorization Patterns

```typescript
// Role-Based Access Control (RBAC)
interface Permission {
  resource: string;   // "posts"
  action: string;     // "create" | "read" | "update" | "delete"
}

// Attribute-Based Access Control (ABAC) - for complex rules
canEdit = (user.id === resource.ownerId) || user.roles.includes('admin');
```

## Error Handling

### Layered Error Strategy

```typescript
// 1. Domain errors (business logic)
class InsufficientFundsError extends DomainError {
  constructor(public available: number, public requested: number) {
    super(`Insufficient funds: ${available} < ${requested}`);
  }
}

// 2. Application errors (mapped to HTTP)
class NotFoundError extends ApplicationError {
  statusCode = 404;
}

// 3. Global error handler
app.use((err, req, res, next) => {
  logger.error({ err, requestId: req.id, path: req.path });

  if (err instanceof ApplicationError) {
    return res.status(err.statusCode).json({ error: err.toJSON() });
  }

  // Never expose internal errors
  res.status(500).json({ error: { code: 'INTERNAL_ERROR', message: 'Something went wrong' } });
});
```

## Logging & Observability

### Structured Logging

```typescript
// Always structured, never string concatenation
logger.info({
  event: 'order_created',
  orderId: order.id,
  userId: user.id,
  amount: order.total,
  duration: Date.now() - startTime
});

// Correlation ID for request tracing
const requestId = req.headers['x-request-id'] || uuid();
logger.child({ requestId });
```

### Key Metrics

- **Latency**: p50, p95, p99 response times
- **Error rate**: 5xx / total requests
- **Throughput**: requests/second
- **Saturation**: CPU, memory, DB connections

## Security Checklist

| Category | Requirement |
|----------|-------------|
| Input | Validate & sanitize all input (zod, joi) |
| SQL | Parameterized queries ONLY, never string concat |
| Auth | Hash passwords (bcrypt/argon2, cost ≥ 10) |
| HTTPS | TLS 1.2+ everywhere, HSTS headers |
| Headers | CSP, X-Frame-Options, X-Content-Type-Options |
| Secrets | Environment variables, never in code |
| Rate Limit | All endpoints, stricter on auth endpoints |
| CORS | Whitelist specific origins, never `*` in prod |

## Testing Strategy

### Test Pyramid

```
         /\
        /  \  E2E (few, slow, high confidence)
       /----\
      /      \ Integration (API, DB, external services)
     /--------\
    /          \ Unit (many, fast, isolated)
   /--------------\
```

### Backend Test Patterns

```typescript
// Unit: Pure functions, business logic
test('calculateDiscount applies 10% for orders over $100', () => {
  expect(calculateDiscount({ total: 150 })).toBe(15);
});

// Integration: Real DB, mocked external services
test('POST /orders creates order in database', async () => {
  const res = await request(app).post('/orders').send(orderData);
  expect(res.status).toBe(201);

  const order = await db.orders.findById(res.body.data.id);
  expect(order.total).toBe(orderData.total);
});
```

## Performance Patterns

### Caching Layers

1. **Application cache**: In-memory (Redis) for hot data
2. **Database cache**: Query result caching, materialized views
3. **HTTP cache**: ETags, Cache-Control headers

### Async Processing

```typescript
// Offload slow operations to queue
await queue.add('send-email', { to: user.email, template: 'welcome' });
await queue.add('generate-report', { reportId }, { delay: 5000 });

// Process in workers
queue.process('send-email', async (job) => {
  await emailService.send(job.data);
});
```

### Database Connection Pooling

```typescript
// Node.js example
const pool = new Pool({
  max: 20,              // Max connections
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000,
});
```

## Architecture Patterns

### Monolith First

Start monolithic, extract services ONLY when:
- Team size requires independent deployability
- Specific component has vastly different scaling needs
- Clear bounded context with minimal cross-service calls

### Service Communication

| Pattern | Use Case |
|---------|----------|
| REST/HTTP | Synchronous, simple CRUD |
| gRPC | High-performance, internal services |
| Message Queue | Async, decoupled, retry-able |
| Event Sourcing | Audit trail, complex state |

## File Organization

```
src/
├── api/
│   ├── routes/           # Route definitions
│   ├── controllers/      # Request handling
│   ├── middleware/       # Auth, validation, logging
│   └── validators/       # Request validation schemas
├── services/             # Business logic
├── repositories/         # Data access layer
├── models/               # Database models/entities
├── utils/                # Shared utilities
├── config/               # Environment config
└── types/                # TypeScript types

tests/
├── unit/
├── integration/
└── fixtures/
```

## Quick References

- **Database optimization**: See `references/database-patterns.md`
- **Auth implementation**: See `references/auth-patterns.md`
- **Deployment checklist**: See `references/deployment.md`
