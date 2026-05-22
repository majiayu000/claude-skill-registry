---
name: backend-coding
description: Expert backend development guidance covering Node.js, Python, Java, Go, API design (REST/GraphQL/gRPC), database patterns, authentication, caching, message queues, microservices, and testing. Produces production-ready, scalable, and secure backend code with industry best practices. Use when building APIs, implementing business logic, designing data models, integrating services, or when users mention backend development, server-side code, APIs, databases, or microservices.
---

# Backend Coding

Build production-ready backend services with proper architecture, security, performance optimization, and testing.

## Core Development Workflow

Follow this systematic approach for backend implementation:

## 1. Design API Endpoints

Define clear, RESTful API contracts before implementation.

**REST API Design Pattern:**

```
Resource-based URLs (use plural nouns):
✅ GET    /api/v1/users              - List users (paginated)
✅ GET    /api/v1/users/:id          - Get user by ID
✅ POST   /api/v1/users              - Create new user
✅ PUT    /api/v1/users/:id          - Replace entire user
✅ PATCH  /api/v1/users/:id          - Update user fields
✅ DELETE /api/v1/users/:id          - Delete user

❌ Avoid verb-based URLs:
❌ /api/v1/getUsers
❌ /api/v1/createUser
```

**Basic Example (Express.js):**

```typescript
router.get('/users',
  query('page').optional().isInt({ min: 1 }).toInt(),
  query('limit').optional().isInt({ min: 1, max: 100 }).toInt(),
  async (req, res, next) => {
    try {
      const errors = validationResult(req);
      if (!errors.isEmpty()) {
        return res.status(400).json({ errors: errors.array() });
      }

      const page = req.query.page as number || 1;
      const limit = req.query.limit as number || 20;
      const offset = (page - 1) * limit;

      const { users, total } = await userService.findAll({ 
        limit, offset 
      });

      res.json({
        data: users,
        pagination: { page, limit, total }
      });
    } catch (error) {
      next(error);
    }
  }
);
```

**For complete patterns:** [api-design.md](references/api-design.md)

### 2. Implement Database Layer

Use repository pattern for clean separation and testability.

**Repository Pattern (TypeORM):**

```typescript
export class UserRepository {
  private repository: Repository<User>;

  async findAll(params: { search?: string; limit: number; offset: number }) {
    const queryBuilder = this.repository
      .createQueryBuilder('user')
      .orderBy('user.createdAt', 'DESC');

    if (params.search) {
      queryBuilder.where(
        'user.name ILIKE :search OR user.email ILIKE :search',
        { search: `%${params.search}%` }
      );
    }

    return queryBuilder
      .take(params.limit)
      .skip(params.offset)
      .getManyAndCount();
  }

  async create(userData: UserCreate): Promise<User> {
    const hashedPassword = await bcrypt.hash(userData.password, 12);
    const user = this.repository.create({
      ...userData,
      password: hashedPassword
    });
    return this.repository.save(user);
  }
}
```

**For detailed patterns:** [database-patterns.md](references/database-patterns.md)

### 3. Implement Authentication

Secure JWT-based authentication with refresh tokens.

**JWT Authentication Pattern:**

```typescript
export class AuthService {
  private readonly JWT_SECRET = process.env.JWT_SECRET!;
  private readonly ACCESS_TOKEN_EXPIRY = '15m';
  private readonly REFRESH_TOKEN_EXPIRY = '7d';

  async login(email: string, password: string) {
    const user = await userRepository.findByEmail(email);
    if (!user || !await bcrypt.compare(password, user.password)) {
      throw new UnauthorizedError('Invalid credentials');
    }

    const accessToken = this.generateAccessToken(user);
    const refreshToken = this.generateRefreshToken(user);

    await tokenRepository.create({
      userId: user.id,
      token: refreshToken,
      expiresAt: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000)
    });

    return { accessToken, refreshToken, user };
  }

  generateAccessToken(user: User): string {
    return jwt.sign(
      { userId: user.id, email: user.email, role: user.role },
      this.JWT_SECRET,
      { expiresIn: this.ACCESS_TOKEN_EXPIRY }
    );
  }
}

// Middleware
export const authenticate = async (req, res, next) => {
  const token = req.headers.authorization?.substring(7);
  if (!token) {
    return res.status(401).json({ error: 'Missing token' });
  }
  
  try {
    req.user = authService.verifyAccessToken(token);
    next();
  } catch (error) {
    res.status(401).json({ error: 'Invalid token' });
  }
};
```

**For complete implementation:** [authentication-and-authorization.md](references/authentication-and-authorization.md)

### 4. Implement Caching

Use Redis for performance optimization with cache-aside pattern.

**Caching Pattern:**

```typescript
export class CacheService {
  private redis: Redis;
  private readonly DEFAULT_TTL = 3600; // 1 hour

  async getOrSet<T>(
    key: string,
    fetchFn: () => Promise<T>,
    ttl: number = this.DEFAULT_TTL
  ): Promise<T> {
    // Try cache first
    const cached = await this.redis.get(key);
    if (cached) return JSON.parse(cached);

    // Fetch from database
    const data = await fetchFn();
    await this.redis.setex(key, ttl, JSON.stringify(data));
    
    return data;
  }

  async invalidate(pattern: string): Promise<void> {
    const keys = await this.redis.keys(pattern);
    if (keys.length > 0) await this.redis.del(...keys);
  }
}

// Usage in service
export class UserService {
  async findById(id: string): Promise<User | null> {
    return cache.getOrSet(
      `user:${id}`,
      () => repository.findById(id),
      3600
    );
  }

  async update(id: string, updates: Partial<User>): Promise<User | null> {
    const user = await repository.update(id, updates);
    await cache.invalidate(`user:${id}`);
    await cache.invalidate(`users:list:*`);
    return user;
  }
}
```

**For advanced strategies:** [caching-strategies.md](references/caching-strategies.md)

### 5. Implement Error Handling

Global error handling with custom error classes.

**Error Handling Pattern:**

```typescript
// Custom error classes
export class AppError extends Error {
  constructor(
    public statusCode: number,
    message: string,
    public isOperational: boolean = true
  ) {
    super(message);
    Error.captureStackTrace(this, this.constructor);
  }
}

export class ValidationError extends AppError {
  constructor(message: string, public errors: any[]) {
    super(400, message);
  }
}

export class UnauthorizedError extends AppError {
  constructor(message: string = 'Unauthorized') {
    super(401, message);
  }
}

export class NotFoundError extends AppError {
  constructor(message: string = 'Resource not found') {
    super(404, message);
  }
}

// Global error handler middleware
export const errorHandler = (err: Error, req: Request, res: Response, next: NextFunction) => {
  if (err instanceof AppError) {
    return res.status(err.statusCode).json({
      error: { message: err.message }
    });
  }

  console.error('Unexpected error:', err);
  res.status(500).json({ error: { message: 'Internal server error' } });
};

// Async handler wrapper
export const asyncHandler = (fn: Function) => {
  return (req: Request, res: Response, next: NextFunction) => {
    Promise.resolve(fn(req, res, next)).catch(next);
  };
};
```

### 6. Write Tests

Write comprehensive unit and integration tests.

**Testing Pattern:**

```typescript
describe('User API', () => {
  beforeAll(async () => {
    await AppDataSource.initialize();
  });

  afterAll(async () => {
    await AppDataSource.destroy();
  });

  beforeEach(async () => {
    await AppDataSource.synchronize(true);
  });

  describe('POST /api/v1/users', () => {
    it('should create a new user', async () => {
      const response = await request(app)
        .post('/api/v1/users')
        .send({
          email: 'test@example.com',
          password: 'SecurePass123!',
          name: 'Test User'
        })
        .expect(201);

      expect(response.body.data).toMatchObject({
        email: 'test@example.com',
        name: 'Test User'
      });
      expect(response.body.data.password).toBeUndefined();
    });

    it('should return 400 for invalid email', async () => {
      await request(app)
        .post('/api/v1/users')
        .send({
          email: 'invalid-email',
          password: 'SecurePass123!',
          name: 'Test User'
        })
        .expect(400);
    });
  });
});
```

## Framework-Specific Guides

Load detailed implementation guides for specific frameworks:

- **[nodejs-development.md](references/nodejs-development.md)** - Express, NestJS, Fastify, middleware, async handling
- **[python-development.md](references/python-development.md)** - Django, Flask, FastAPI, async/await, decorators

## Technology-Specific Patterns

Load detailed patterns for specific technologies:

- **[api-design.md](references/api-design.md)** - REST, GraphQL, gRPC, versioning, documentation
- **[database-patterns.md](references/database-patterns.md)** - ORMs, query optimization, transactions, migrations
- **[authentication-and-authorization.md](references/authentication-and-authorization.md)** - JWT, OAuth, RBAC, session management
- **[caching-strategies.md](references/caching-strategies.md)** - Redis patterns, cache invalidation, distributed caching
- **[microservices.md](references/microservices.md)** - Service communication, API gateways, circuit breakers

## Production-Ready Checklist

Before deployment, verify:

**Security:**

```
☐ Input validation on all endpoints (express-validator, Pydantic)
☐ SQL injection prevention (parameterized queries only)
☐ Password hashing with bcrypt/argon2 (cost factor ≥12)
☐ JWT tokens expire within 15 minutes, refresh tokens within 7 days
☐ Rate limiting: 100 req/min per user, 1000 req/min per IP
☐ CORS configured (not '*' in production)
☐ Environment variables for all secrets
☐ HTTPS only (TLS 1.3 minimum)
```

**Performance:**

```
☐ Database indexes on query columns
☐ Connection pooling configured (10-20 connections)
☐ Caching frequently accessed data (Redis, 1-hour TTL)
☐ Pagination for large result sets (limit ≤100 items)
☐ Async operations for I/O (non-blocking)
```

**Code Quality:**

```
☐ Repository pattern for data access
☐ Dependency injection for testability
☐ Global error handling with custom error classes
☐ Structured logging with request IDs
☐ Test coverage ≥80% (unit + integration)
☐ API documentation (OpenAPI/Swagger)
☐ Health check endpoint (/health)
☐ Graceful shutdown handling
```

## Critical Security Principles

**Never trust user input** - Validate everything
**Use parameterized queries** - Prevent SQL injection
**Hash passwords** - bcrypt with cost factor 12+, never store plain text
**Expire tokens quickly** - 15min access tokens, 7day refresh tokens
**Use HTTPS only** - TLS 1.3 minimum

## Critical Performance Principles

**Cache frequently accessed data** - Redis with appropriate TTL (typically 1 hour)
**Use database indexes** - On all query columns
**Paginate large result sets** - Max 100 items per page
**Use connection pooling** - 10-20 connections
**Async operations for I/O** - Don't block the event loop
