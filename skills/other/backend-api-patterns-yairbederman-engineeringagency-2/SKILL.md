---
name: backend-api-patterns
description: Backend API implementation patterns for scalability, security, and maintainability. Use when building APIs, services, and backend systems.
---

# Backend API Patterns

Implementation patterns for scalable, secure, and maintainable backend systems.

## When to Use

- Building new API endpoints
- Implementing service layer logic
- Database operations and queries
- Authentication and authorization

## Service Layer Patterns

### Repository Pattern

```typescript
// Separate data access from business logic
interface UserRepository {
  findById(id: string): Promise<User | null>
  findByEmail(email: string): Promise<User | null>
  create(data: CreateUserDto): Promise<User>
  update(id: string, data: UpdateUserDto): Promise<User>
  delete(id: string): Promise<void>
}

class UserService {
  constructor(private readonly userRepo: UserRepository) {}
  
  async createUser(dto: CreateUserDto): Promise<User> {
    // Business logic here
    const existing = await this.userRepo.findByEmail(dto.email)
    if (existing) throw new ConflictError('Email already exists')
    return this.userRepo.create(dto)
  }
}
```

### Unit of Work Pattern

```typescript
// Manage transactions across repositories
interface UnitOfWork {
  users: UserRepository
  orders: OrderRepository
  commit(): Promise<void>
  rollback(): Promise<void>
}

async function createOrderWithUser(uow: UnitOfWork, data: OrderData) {
  try {
    const user = await uow.users.create(data.user)
    const order = await uow.orders.create({ ...data.order, userId: user.id })
    await uow.commit()
    return { user, order }
  } catch (error) {
    await uow.rollback()
    throw error
  }
}
```

## Error Handling

### Custom Error Classes

```typescript
abstract class AppError extends Error {
  abstract statusCode: number
  abstract code: string
}

class NotFoundError extends AppError {
  statusCode = 404
  code = 'NOT_FOUND'
  constructor(resource: string, id: string) {
    super(`${resource} with id ${id} not found`)
  }
}

class ValidationError extends AppError {
  statusCode = 422
  code = 'VALIDATION_ERROR'
  constructor(public errors: FieldError[]) {
    super('Validation failed')
  }
}
```

### Global Error Handler

```typescript
function errorHandler(error: Error, req: Request, res: Response, next: Next) {
  if (error instanceof AppError) {
    return res.status(error.statusCode).json({
      error: {
        code: error.code,
        message: error.message,
        details: error instanceof ValidationError ? error.errors : undefined
      }
    })
  }
  
  // Log unexpected errors
  logger.error('Unexpected error', { error, requestId: req.id })
  
  return res.status(500).json({
    error: { code: 'INTERNAL_ERROR', message: 'An unexpected error occurred' }
  })
}
```

## Database Patterns

### Query Optimization

```typescript
// ❌ N+1 Query Problem
const users = await db.users.findMany()
for (const user of users) {
  user.orders = await db.orders.findMany({ where: { userId: user.id } })
}

// ✅ Eager Loading
const users = await db.users.findMany({
  include: { orders: true }
})

// ✅ Or batch loading
const users = await db.users.findMany()
const orders = await db.orders.findMany({
  where: { userId: { in: users.map(u => u.id) } }
})
```

### Connection Pooling

```typescript
const pool = {
  min: 2,
  max: 10,
  idleTimeoutMs: 30000,
  acquireTimeoutMs: 30000
}
```

## Security Patterns

### Input Validation

```typescript
// Always validate at the boundary
const CreateUserSchema = z.object({
  email: z.string().email(),
  name: z.string().min(2).max(100),
  password: z.string().min(8).regex(/[A-Z]/).regex(/[0-9]/)
})

async function createUser(req: Request) {
  const validated = CreateUserSchema.parse(req.body)
  // Safe to use validated data
}
```

### Authorization

```typescript
// Resource-level authorization
async function getOrder(userId: string, orderId: string) {
  const order = await orderRepo.findById(orderId)
  if (!order) throw new NotFoundError('Order', orderId)
  if (order.userId !== userId) throw new ForbiddenError()
  return order
}
```

## Performance Patterns

### Caching Strategy

```typescript
async function getUserById(id: string): Promise<User> {
  // Check cache first
  const cached = await cache.get(`user:${id}`)
  if (cached) return JSON.parse(cached)
  
  // Fetch from database
  const user = await userRepo.findById(id)
  if (!user) throw new NotFoundError('User', id)
  
  // Store in cache with TTL
  await cache.set(`user:${id}`, JSON.stringify(user), 'EX', 3600)
  return user
}
```

### Rate Limiting

```typescript
const rateLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // limit each IP to 100 requests per window
  message: { error: { code: 'RATE_LIMITED', message: 'Too many requests' } }
})
```

## Logging Standards

```typescript
// Structured logging
logger.info('User created', {
  userId: user.id,
  email: user.email,
  requestId: req.id,
  duration: Date.now() - startTime
})

// Log levels
logger.debug() // Development details
logger.info()  // Business events
logger.warn()  // Potential issues
logger.error() // Errors needing attention
```

## Checklist

Before completing backend implementation:

- [ ] Input validated with schema
- [ ] Errors properly categorized
- [ ] Database queries optimized (no N+1)
- [ ] Authorization checks in place
- [ ] Sensitive data not logged
- [ ] Transaction boundaries defined
- [ ] Caching strategy considered
- [ ] Rate limiting configured
