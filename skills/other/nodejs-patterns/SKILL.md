---
model: standard
description: |
  WHAT: Production-ready Node.js backend patterns - Express/Fastify setup, layered architecture, 
  middleware, error handling, validation, database integration, authentication, and caching.
  
  WHEN: User is building REST APIs, setting up Node.js servers, implementing authentication, 
  integrating databases, adding validation/caching, or structuring backend applications.
  
  KEYWORDS: nodejs, node, express, fastify, typescript, api, rest, middleware, authentication, 
  jwt, validation, zod, postgres, mongodb, redis, caching, rate limiting, error handling
---

# Node.js Backend Patterns

Patterns for building scalable, maintainable Node.js backend applications with TypeScript.


## Installation

### OpenClaw / Moltbot / Clawbot

```bash
npx clawhub@latest install nodejs-patterns
```


## NEVER

- **NEVER store secrets in code** - Use environment variables, never hardcode credentials
- **NEVER skip input validation** - Validate all input at the middleware layer with Zod/Joi
- **NEVER expose error details in production** - Return generic messages, log details server-side
- **NEVER use `any` type** - TypeScript types prevent runtime errors
- **NEVER skip error handling** - Always wrap async handlers, use global error middleware
- **NEVER use sync operations** - Use async/await for I/O, never `fs.readFileSync` in handlers
- **NEVER trust client input** - Sanitize, validate, and parameterize all queries

## When to Use

- Building REST APIs with Express or Fastify
- Setting up middleware pipelines and error handling
- Implementing authentication and authorization
- Integrating databases with connection pooling and transactions
- Adding validation, caching, and rate limiting

## Project Structure — Layered Architecture

```
src/
├── controllers/     # Handle HTTP requests/responses
├── services/        # Business logic
├── repositories/    # Data access layer
├── models/          # Data models and types
├── middleware/      # Auth, validation, logging, errors
├── routes/          # Route definitions
├── config/          # Database, cache, env configuration
└── utils/           # Helpers, custom errors, response formatting
```

Controllers handle HTTP concerns, services contain business logic, repositories abstract data access. Each layer only calls the layer below it.

## Express Setup

```typescript
import express from "express";
import helmet from "helmet";
import cors from "cors";
import compression from "compression";

const app = express();

app.use(helmet());
app.use(cors({ origin: process.env.ALLOWED_ORIGINS?.split(",") }));
app.use(compression());
app.use(express.json({ limit: "10mb" }));
app.use(express.urlencoded({ extended: true, limit: "10mb" }));
```

## Fastify Setup

```typescript
import Fastify from "fastify";
import helmet from "@fastify/helmet";
import cors from "@fastify/cors";

const fastify = Fastify({
  logger: { level: process.env.LOG_LEVEL || "info" },
});

await fastify.register(helmet);
await fastify.register(cors, { origin: true });

// Type-safe routes with built-in schema validation
fastify.post<{ Body: { name: string; email: string } }>(
  "/users",
  {
    schema: {
      body: {
        type: "object",
        required: ["name", "email"],
        properties: {
          name: { type: "string", minLength: 1 },
          email: { type: "string", format: "email" },
        },
      },
    },
  },
  async (request) => {
    const { name, email } = request.body;
    return { id: "123", name };
  },
);
```

## Error Handling

### Custom Error Classes

```typescript
export class AppError extends Error {
  constructor(
    public message: string,
    public statusCode: number = 500,
    public isOperational: boolean = true,
  ) {
    super(message);
    Object.setPrototypeOf(this, AppError.prototype);
    Error.captureStackTrace(this, this.constructor);
  }
}

export class ValidationError extends AppError {
  constructor(message: string, public errors?: any[]) { super(message, 400); }
}
export class NotFoundError extends AppError {
  constructor(message = "Resource not found") { super(message, 404); }
}
export class UnauthorizedError extends AppError {
  constructor(message = "Unauthorized") { super(message, 401); }
}
export class ForbiddenError extends AppError {
  constructor(message = "Forbidden") { super(message, 403); }
}
```

### Global Error Handler

```typescript
import { Request, Response, NextFunction } from "express";
import { AppError, ValidationError } from "../utils/errors";

export const errorHandler = (
  err: Error, req: Request, res: Response, next: NextFunction,
) => {
  if (err instanceof AppError) {
    return res.status(err.statusCode).json({
      status: "error",
      message: err.message,
      ...(err instanceof ValidationError && { errors: err.errors }),
    });
  }

  // Don't leak details in production
  const message = process.env.NODE_ENV === "production"
    ? "Internal server error"
    : err.message;

  res.status(500).json({ status: "error", message });
};

// Wrap async route handlers to forward errors
export const asyncHandler = (
  fn: (req: Request, res: Response, next: NextFunction) => Promise<any>,
) => (req: Request, res: Response, next: NextFunction) => {
  Promise.resolve(fn(req, res, next)).catch(next);
};
```

## Validation Middleware (Zod)

```typescript
import { AnyZodObject, ZodError } from "zod";

export const validate = (schema: AnyZodObject) => {
  return async (req: Request, res: Response, next: NextFunction) => {
    try {
      await schema.parseAsync({
        body: req.body,
        query: req.query,
        params: req.params,
      });
      next();
    } catch (error) {
      if (error instanceof ZodError) {
        const errors = error.errors.map((e) => ({
          field: e.path.join("."),
          message: e.message,
        }));
        next(new ValidationError("Validation failed", errors));
      } else {
        next(error);
      }
    }
  };
};

// Usage
import { z } from "zod";
const createUserSchema = z.object({
  body: z.object({
    name: z.string().min(1),
    email: z.string().email(),
    password: z.string().min(8),
  }),
});
router.post("/users", validate(createUserSchema), userController.createUser);
```

## Authentication — JWT

### Auth Middleware

```typescript
import jwt from "jsonwebtoken";

interface JWTPayload { userId: string; email: string; }

export const authenticate = async (
  req: Request, res: Response, next: NextFunction,
) => {
  try {
    const token = req.headers.authorization?.replace("Bearer ", "");
    if (!token) throw new UnauthorizedError("No token provided");

    req.user = jwt.verify(token, process.env.JWT_SECRET!) as JWTPayload;
    next();
  } catch {
    next(new UnauthorizedError("Invalid token"));
  }
};

export const authorize = (...roles: string[]) => {
  return (req: Request, res: Response, next: NextFunction) => {
    if (!req.user) return next(new UnauthorizedError("Not authenticated"));
    if (!roles.some((r) => req.user?.roles?.includes(r))) {
      return next(new ForbiddenError("Insufficient permissions"));
    }
    next();
  };
};
```

### Auth Service

```typescript
export class AuthService {
  constructor(private userRepository: UserRepository) {}

  async login(email: string, password: string) {
    const user = await this.userRepository.findByEmail(email);
    if (!user || !(await bcrypt.compare(password, user.password))) {
      throw new UnauthorizedError("Invalid credentials");
    }

    return {
      token: jwt.sign(
        { userId: user.id, email: user.email },
        process.env.JWT_SECRET!,
        { expiresIn: "15m" },
      ),
      refreshToken: jwt.sign(
        { userId: user.id },
        process.env.REFRESH_TOKEN_SECRET!,
        { expiresIn: "7d" },
      ),
      user: { id: user.id, name: user.name, email: user.email },
    };
  }
}
```

## Database Patterns

### PostgreSQL Connection Pool

```typescript
import { Pool, PoolConfig } from "pg";

const pool = new Pool({
  host: process.env.DB_HOST,
  port: parseInt(process.env.DB_PORT || "5432"),
  database: process.env.DB_NAME,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  max: 20,
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000,
});

pool.on("error", (err) => {
  console.error("Unexpected database error", err);
  process.exit(-1);
});

export const closeDatabase = async () => { await pool.end(); };
```

### Transaction Pattern

```typescript
async createOrder(userId: string, items: OrderItem[]) {
  const client = await this.db.connect();
  try {
    await client.query("BEGIN");

    const { rows } = await client.query(
      "INSERT INTO orders (user_id, total) VALUES ($1, $2) RETURNING id",
      [userId, calculateTotal(items)],
    );
    const orderId = rows[0].id;

    for (const item of items) {
      await client.query(
        "INSERT INTO order_items (order_id, product_id, quantity, price) VALUES ($1, $2, $3, $4)",
        [orderId, item.productId, item.quantity, item.price],
      );
      await client.query(
        "UPDATE products SET stock = stock - $1 WHERE id = $2",
        [item.quantity, item.productId],
      );
    }

    await client.query("COMMIT");
    return orderId;
  } catch (error) {
    await client.query("ROLLBACK");
    throw error;
  } finally {
    client.release();
  }
}
```

## Rate Limiting

```typescript
import rateLimit from "express-rate-limit";
import RedisStore from "rate-limit-redis";
import Redis from "ioredis";

const redis = new Redis({ host: process.env.REDIS_HOST });

export const apiLimiter = rateLimit({
  store: new RedisStore({ client: redis, prefix: "rl:" }),
  windowMs: 15 * 60 * 1000,
  max: 100,
  standardHeaders: true,
  legacyHeaders: false,
});

export const authLimiter = rateLimit({
  store: new RedisStore({ client: redis, prefix: "rl:auth:" }),
  windowMs: 15 * 60 * 1000,
  max: 5,
  skipSuccessfulRequests: true,
});
```

## Caching with Redis

```typescript
import Redis from "ioredis";

const redis = new Redis({
  host: process.env.REDIS_HOST,
  retryStrategy: (times) => Math.min(times * 50, 2000),
});

export class CacheService {
  async get<T>(key: string): Promise<T | null> {
    const data = await redis.get(key);
    return data ? JSON.parse(data) : null;
  }

  async set(key: string, value: any, ttl?: number): Promise<void> {
    const serialized = JSON.stringify(value);
    ttl ? await redis.setex(key, ttl, serialized) : await redis.set(key, serialized);
  }

  async delete(key: string): Promise<void> { await redis.del(key); }

  async invalidatePattern(pattern: string): Promise<void> {
    const keys = await redis.keys(pattern);
    if (keys.length) await redis.del(...keys);
  }
}
```

## API Response Helpers

```typescript
export class ApiResponse {
  static success<T>(res: Response, data: T, message?: string, statusCode = 200) {
    return res.status(statusCode).json({ status: "success", message, data });
  }

  static paginated<T>(res: Response, data: T[], page: number, limit: number, total: number) {
    return res.json({
      status: "success",
      data,
      pagination: { page, limit, total, pages: Math.ceil(total / limit) },
    });
  }
}
```

## Best Practices

1. **Use TypeScript** — type safety prevents runtime errors
2. **Validate all input** — Zod or Joi at the middleware layer
3. **Custom error classes** — map to HTTP status codes, use global handler
4. **Never hardcode secrets** — use environment variables
5. **Structured logging** — Pino or Winston with request context
6. **Rate limiting** — Redis-backed for distributed deployments
7. **Connection pooling** — always for databases
8. **Dependency injection** — constructor injection for testability
9. **Graceful shutdown** — close DB pools, drain connections on SIGTERM
10. **Health checks** — `/health` endpoint for liveness/readiness probes
