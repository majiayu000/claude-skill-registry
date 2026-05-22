---
name: express
description: |
  Express.js framework guardrails, patterns, and best practices for AI-assisted development.
  Use when working with Express.js projects, or when the user mentions Express.
  Provides middleware patterns, routing, error handling, and REST API guidelines.
license: MIT
metadata:
  author: samuel
  version: "1.0"
  category: framework
  language: typescript
  extensions: ".js,.ts"
---

# Express.js Guide

> Applies to: Express.js 4.x/5.x, TypeScript/JavaScript, REST APIs, Web Servers, Microservices

## Core Principles

1. **Middleware-Centric**: Everything is middleware -- parsing, auth, logging, errors
2. **Layered Architecture**: Controllers -> Services -> Repositories (separation of concerns)
3. **Type Safety**: Use TypeScript for all new Express projects
4. **Security First**: helmet, cors, rate limiting, input validation on every route
5. **Graceful Lifecycle**: Handle startup, shutdown, and uncaught errors properly

## Guardrails

### Project Setup

- Use TypeScript with strict mode enabled
- Install core security packages: `helmet`, `cors`, `express-rate-limit`
- Use `dotenv` for environment configuration (never hardcode secrets)
- Use `zod` or `joi` for request validation at every API boundary
- Use `morgan` or `pino` for structured logging
- Set `express.json({ limit: '10mb' })` to prevent oversized payloads

### Code Style

- Controllers: thin, delegate to services, catch errors via `next(error)`
- Services: business logic only, no `req`/`res` references
- Repositories: data access only, return domain types
- Middleware: single-responsibility, composable
- Routes: declarative, grouped by resource
- No business logic in route files

### Error Handling

- Use a centralized error-handling middleware (4-argument signature)
- Create a custom `AppError` class with `statusCode` and optional `errors` array
- Always call `next(error)` in async handlers -- never swallow errors
- Return generic messages in production, detailed messages in development
- Handle `404` with a dedicated not-found middleware after all routes
- Log all errors with request context (path, method, stack trace)

### Security

- Enable `helmet()` for security headers
- Configure CORS with explicit allowed origins (not `*` in production)
- Implement rate limiting on all routes, stricter on auth endpoints
- Validate and sanitize all user inputs before processing
- Use parameterized queries (Prisma, Knex, or prepared statements)
- Set secure cookie options: `httpOnly`, `secure`, `sameSite`
- Never expose stack traces or internal details in production responses

### Performance

- Use `compression` middleware for response compression
- Implement pagination for list endpoints (never return unbounded results)
- Use connection pooling for database connections
- Set appropriate timeouts on the HTTP server (`readTimeout`, `writeTimeout`)
- Cache expensive computations where appropriate

## Project Structure

```
my-api/
├── src/
│   ├── app.ts                 # Express app setup (middleware, routes, error handling)
│   ├── server.ts              # Entry point (listen, graceful shutdown)
│   ├── config/                # Environment and app configuration
│   │   └── index.ts
│   ├── controllers/           # Route handlers (thin, delegate to services)
│   │   └── user.controller.ts
│   ├── middlewares/           # Custom middleware
│   │   ├── auth.middleware.ts
│   │   ├── error.middleware.ts
│   │   ├── validate.middleware.ts
│   │   └── rateLimit.middleware.ts
│   ├── routes/                # Route definitions (grouped by resource)
│   │   ├── index.ts
│   │   └── user.routes.ts
│   ├── services/              # Business logic (no req/res)
│   │   └── user.service.ts
│   ├── repositories/          # Data access layer
│   │   └── user.repository.ts
│   ├── models/                # Data models / Prisma schema
│   │   └── user.model.ts
│   ├── schemas/               # Zod validation schemas
│   │   └── user.schema.ts
│   ├── types/                 # TypeScript type definitions
│   │   └── index.ts
│   └── utils/                 # Shared utilities
│       ├── errors.ts          # AppError class
│       └── logger.ts          # Logger setup
├── tests/
│   └── user.test.ts
├── .env.example
├── package.json
└── tsconfig.json
```

### Layer Responsibilities

| Layer | Knows About | Never References |
|-------|-------------|-----------------|
| Routes | Controllers, middleware | Services, repositories |
| Controllers | Services, types | Repositories, database |
| Services | Repositories, types | req/res, Express |
| Repositories | Database client, types | Services, controllers |

## Application Setup

### App Configuration (src/app.ts)

```typescript
import express, { Application } from 'express';
import cors from 'cors';
import helmet from 'helmet';
import morgan from 'morgan';
import { errorHandler } from './middlewares/error.middleware';
import { notFoundHandler } from './middlewares/notFound.middleware';
import routes from './routes';

const app: Application = express();

// Security
app.use(helmet());
app.use(cors({ origin: process.env.CORS_ORIGIN || '*', credentials: true }));

// Parsing
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true }));

// Logging (skip in test)
if (process.env.NODE_ENV !== 'test') {
  app.use(morgan('combined'));
}

// Health check
app.get('/health', (_req, res) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

// API routes
app.use('/api/v1', routes);

// Error handling (order matters: 404 first, then error handler)
app.use(notFoundHandler);
app.use(errorHandler);

export default app;
```

### Server Entry Point (src/server.ts)

```typescript
import 'dotenv/config';
import app from './app';
import { logger } from './utils/logger';

const PORT = process.env.PORT || 3000;

const server = app.listen(PORT, () => {
  logger.info(`Server running on port ${PORT}`);
});

// Graceful shutdown
const shutdown = () => {
  logger.info('Shutting down gracefully...');
  server.close(() => process.exit(0));
  setTimeout(() => process.exit(1), 10000); // Force after 10s
};

process.on('SIGTERM', shutdown);
process.on('SIGINT', shutdown);
process.on('unhandledRejection', (reason: Error) => {
  logger.error('Unhandled Rejection:', reason);
  throw reason;
});
process.on('uncaughtException', (error: Error) => {
  logger.error('Uncaught Exception:', error);
  process.exit(1);
});
```

## Routing

### Route Organization

```typescript
// src/routes/index.ts
import { Router } from 'express';
import userRoutes from './user.routes';
import authRoutes from './auth.routes';

const router = Router();

router.use('/auth', authRoutes);
router.use('/users', userRoutes);

export default router;
```

### Resource Routes

```typescript
// src/routes/user.routes.ts
import { Router } from 'express';
import { UserController } from '../controllers/user.controller';
import { authMiddleware } from '../middlewares/auth.middleware';
import { validate } from '../middlewares/validate.middleware';
import { createUserSchema, updateUserSchema } from '../schemas/user.schema';

const router = Router();
const controller = new UserController();

router.get('/', controller.getAll);
router.get('/:id', controller.getById);
router.post('/', validate(createUserSchema), controller.create);
router.put('/:id', authMiddleware, validate(updateUserSchema), controller.update);
router.delete('/:id', authMiddleware, controller.delete);

export default router;
```

### Route Conventions

- Group routes by resource under `/api/v1/`
- Use plural nouns for resource names (`/users`, `/products`)
- HTTP verbs map to CRUD: GET (read), POST (create), PUT/PATCH (update), DELETE (remove)
- Apply auth middleware selectively (not on public routes)
- Apply validation middleware before the controller handler

## Middleware

### Middleware Order (in app.ts)

1. `helmet()` -- security headers
2. `cors()` -- cross-origin requests
3. `express.json()` -- body parsing
4. `morgan()` -- request logging
5. Route-level middleware (auth, validation, rate limiting)
6. Routes
7. `notFoundHandler` -- catch unmatched routes
8. `errorHandler` -- centralized error handling

### Custom AppError

```typescript
// src/utils/errors.ts
export class AppError extends Error {
  constructor(
    message: string,
    public statusCode: number = 500,
    public errors?: any[]
  ) {
    super(message);
    this.name = 'AppError';
    Error.captureStackTrace(this, this.constructor);
  }
}
```

### Error Handler

```typescript
// src/middlewares/error.middleware.ts
import { Request, Response, NextFunction } from 'express';
import { AppError } from '../utils/errors';
import { logger } from '../utils/logger';

export const errorHandler = (
  error: Error, req: Request, res: Response, _next: NextFunction
) => {
  logger.error('Error:', { message: error.message, path: req.path, method: req.method });

  if (error instanceof AppError) {
    return res.status(error.statusCode).json({
      status: 'error',
      message: error.message,
      ...(error.errors && { errors: error.errors }),
    });
  }

  res.status(500).json({
    status: 'error',
    message: process.env.NODE_ENV === 'production'
      ? 'Internal server error'
      : error.message,
  });
};
```

### Validation Middleware (Zod)

```typescript
// src/middlewares/validate.middleware.ts
import { Request, Response, NextFunction } from 'express';
import { ZodSchema, ZodError } from 'zod';
import { AppError } from '../utils/errors';

export const validate = (schema: ZodSchema) => {
  return (req: Request, _res: Response, next: NextFunction) => {
    try {
      schema.parse({ body: req.body, query: req.query, params: req.params });
      next();
    } catch (error) {
      if (error instanceof ZodError) {
        const errors = error.errors.map((e) => ({
          field: e.path.join('.'),
          message: e.message,
        }));
        next(new AppError('Validation failed', 400, errors));
      } else {
        next(error);
      }
    }
  };
};
```

## Testing

### Testing Stack

- **Jest** for test runner and assertions
- **Supertest** for HTTP integration tests
- Use `app` (not `server`) for supertest -- avoids port conflicts

### Integration Test Pattern

```typescript
import request from 'supertest';
import app from '../src/app';

describe('GET /api/v1/users', () => {
  it('should return 200 with user list', async () => {
    const response = await request(app)
      .get('/api/v1/users')
      .expect('Content-Type', /json/)
      .expect(200);

    expect(response.body.data).toBeDefined();
    expect(response.body.meta).toBeDefined();
  });

  it('should return 400 for invalid query params', async () => {
    await request(app)
      .get('/api/v1/users?page=-1')
      .expect(400);
  });
});
```

### Test Organization

- One test file per resource/feature
- Group by HTTP method and route using `describe` blocks
- Test both success and error paths
- Test validation, auth, and edge cases
- Use `beforeEach`/`afterEach` for database cleanup

## Tooling

### Essential Commands

```bash
# Development
npm run dev              # Start with hot-reload (ts-node-dev)

# Build
npm run build            # Compile TypeScript
npm start                # Run compiled JS

# Testing
npm test                 # Run all tests
npm run test:watch       # Watch mode
npm run test:cov         # With coverage

# Quality
npm run lint             # ESLint
npm run lint:fix         # Auto-fix lint issues
```

### Configuration (tsconfig.json)

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "commonjs",
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "resolveJsonModule": true,
    "declaration": true,
    "sourceMap": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

### Package Scripts

```json
{
  "scripts": {
    "dev": "ts-node-dev --respawn --transpile-only src/server.ts",
    "build": "tsc",
    "start": "node dist/server.js",
    "test": "jest",
    "lint": "eslint src/**/*.ts"
  }
}
```

## Dependencies

### Core

| Package | Purpose |
|---------|---------|
| `express` | Web framework |
| `cors` | Cross-origin resource sharing |
| `helmet` | Security headers |
| `morgan` | HTTP request logging |
| `dotenv` | Environment variables |
| `zod` | Input validation |

### Auth & Security

| Package | Purpose |
|---------|---------|
| `jsonwebtoken` | JWT authentication |
| `bcryptjs` | Password hashing |
| `express-rate-limit` | Rate limiting |

### Database

| Package | Purpose |
|---------|---------|
| `@prisma/client` | ORM / database client |

### Dev

| Package | Purpose |
|---------|---------|
| `typescript` | Type system |
| `ts-node-dev` | Dev server with hot reload |
| `jest` | Test runner |
| `supertest` | HTTP testing |
| `@types/express` | Express type definitions |

## Advanced Topics

For detailed code examples and advanced patterns, see:

- [references/patterns.md](references/patterns.md) -- Controller patterns, service layer, authentication, database integration, rate limiting, testing examples

## External References

- [Express.js Documentation](https://expressjs.com/)
- [Express Security Best Practices](https://expressjs.com/en/advanced/best-practice-security.html)
- [Prisma with Express](https://www.prisma.io/express)
- [Zod Documentation](https://zod.dev/)
