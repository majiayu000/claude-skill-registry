---
name: express
description: Express.js framework patterns including routing, middleware, request/response handling, and Express-specific APIs. Use when working with Express routes, middleware, or Express applications.
---

# Express.js Framework Patterns

## Purpose

Essential Express.js patterns for building scalable backend APIs, emphasizing clean routing, middleware composition, and proper request/response handling.

## When to Use This Skill

- Creating or modifying Express routes
- Building middleware (auth, validation, error handling)
- Working with Express Request/Response objects
- Implementing BaseController pattern
- Error handling in Express

---

## Clean Route Pattern

### Routes Only Route

**Routes should ONLY:**
- ✅ Define route paths
- ✅ Register middleware
- ✅ Delegate to controllers

**Routes should NEVER:**
- ❌ Contain business logic
- ❌ Access database directly
- ❌ Implement validation logic
- ❌ Format complex responses

```typescript
import { Router } from 'express';
import { UserController } from '../controllers/UserController';
import { SSOMiddlewareClient } from '../middleware/SSOMiddleware';

const router = Router();
const controller = new UserController();

// Clean delegation - no business logic
router.get('/:id',
    SSOMiddlewareClient.verifyLoginStatus,
    async (req, res) => controller.getUser(req, res)
);

router.post('/',
    SSOMiddlewareClient.verifyLoginStatus,
    async (req, res) => controller.createUser(req, res)
);

export default router;
```

---

## BaseController Pattern

### Implementation

```typescript
import * as Sentry from '@sentry/node';
import { Response } from 'express';

export abstract class BaseController {
    protected handleError(
        error: unknown,
        res: Response,
        context: string,
        statusCode = 500
    ): void {
        Sentry.withScope((scope) => {
            scope.setTag('controller', this.constructor.name);
            scope.setTag('operation', context);
            Sentry.captureException(error);
        });

        res.status(statusCode).json({
            success: false,
            error: {
                message: error instanceof Error ? error.message : 'An error occurred',
                code: statusCode,
            },
        });
    }

    protected handleSuccess<T>(
        res: Response,
        data: T,
        message?: string,
        statusCode = 200
    ): void {
        res.status(statusCode).json({
            success: true,
            message,
            data,
        });
    }

    protected async withTransaction<T>(
        name: string,
        operation: string,
        callback: () => Promise<T>
    ): Promise<T> {
        return await Sentry.startSpan({ name, op: operation }, callback);
    }

    protected addBreadcrumb(
        message: string,
        category: string,
        data?: Record<string, any>
    ): void {
        Sentry.addBreadcrumb({ message, category, level: 'info', data });
    }
}
```

### Using BaseController

```typescript
import { Request, Response } from 'express';
import { BaseController } from './BaseController';
import { UserService } from '../services/userService';
import { createUserSchema } from '../validators/userSchemas';

export class UserController extends BaseController {
    private userService: UserService;

    constructor() {
        super();
        this.userService = new UserService();
    }

    async getUser(req: Request, res: Response): Promise<void> {
        try {
            this.addBreadcrumb('Fetching user', 'user_controller', {
                userId: req.params.id
            });

            const user = await this.userService.findById(req.params.id);

            if (!user) {
                return this.handleError(
                    new Error('User not found'),
                    res,
                    'getUser',
                    404
                );
            }

            this.handleSuccess(res, user);
        } catch (error) {
            this.handleError(error, res, 'getUser');
        }
    }

    async createUser(req: Request, res: Response): Promise<void> {
        try {
            const validated = createUserSchema.parse(req.body);

            const user = await this.withTransaction(
                'user.create',
                'db.query',
                () => this.userService.create(validated)
            );

            this.handleSuccess(res, user, 'User created successfully', 201);
        } catch (error) {
            this.handleError(error, res, 'createUser');
        }
    }
}
```

---

## Middleware Patterns

### Authentication

```typescript
import { Request, Response, NextFunction } from 'express';
import jwt from 'jsonwebtoken';
import { config } from '../config/unifiedConfig';

export class SSOMiddlewareClient {
    static verifyLoginStatus(req: Request, res: Response, next: NextFunction): void {
        const token = req.cookies.refresh_token;

        if (!token) {
            return res.status(401).json({ error: 'Not authenticated' });
        }

        try {
            const decoded = jwt.verify(token, config.tokens.jwt);
            res.locals.claims = decoded;
            res.locals.effectiveUserId = decoded.sub;
            next();
        } catch (error) {
            res.status(401).json({ error: 'Invalid token' });
        }
    }
}
```

### Audit with AsyncLocalStorage

```typescript
import { Request, Response, NextFunction } from 'express';
import { AsyncLocalStorage } from 'async_hooks';
import { v4 as uuidv4 } from 'uuid';

export interface AuditContext {
    userId: string;
    userName?: string;
    requestId: string;
    timestamp: Date;
}

export const auditContextStorage = new AsyncLocalStorage<AuditContext>();

export function auditMiddleware(req: Request, res: Response, next: NextFunction): void {
    const context: AuditContext = {
        userId: res.locals.effectiveUserId || 'anonymous',
        userName: res.locals.claims?.preferred_username,
        timestamp: new Date(),
        requestId: req.id || uuidv4(),
    };

    auditContextStorage.run(context, () => next());
}

export function getAuditContext(): AuditContext | null {
    return auditContextStorage.getStore() || null;
}
```

### Error Boundary

```typescript
import { Request, Response, NextFunction } from 'express';
import * as Sentry from '@sentry/node';

export function errorBoundary(
    error: Error,
    req: Request,
    res: Response,
    next: NextFunction
): void {
    const statusCode = error.statusCode || 500;

    Sentry.captureException(error);

    res.status(statusCode).json({
        success: false,
        error: {
            message: error.message,
            code: error.name,
        },
    });
}

// Async wrapper
export function asyncErrorWrapper(
    handler: (req: Request, res: Response, next: NextFunction) => Promise<any>
) {
    return async (req: Request, res: Response, next: NextFunction) => {
        try {
            await handler(req, res, next);
        } catch (error) {
            next(error);
        }
    };
}
```

---

## Middleware Ordering

### Critical Order

```typescript
import express from 'express';
import * as Sentry from '@sentry/node';

const app = express();

// 1. Sentry request handler (FIRST)
app.use(Sentry.Handlers.requestHandler());

// 2. Body/cookie parsing
app.use(express.json());
app.use(cookieParser());

// 3. Routes
app.use('/api/users', userRoutes);

// 4. Error handler (AFTER routes)
app.use(errorBoundary);

// 5. Sentry error handler (LAST)
app.use(Sentry.Handlers.errorHandler());
```

**Rules:**
- Sentry request handler FIRST
- Body/cookie parsers before routes
- Error handlers AFTER all routes
- Sentry error handler LAST

---

## Request/Response Handling

### Typed Requests

```typescript
interface CreateUserRequest {
    email: string;
    name: string;
    password: string;
}

async function createUser(
    req: Request<{}, {}, CreateUserRequest>,
    res: Response
): Promise<void> {
    const { email, name, password } = req.body; // Typed
}
```

### Response Patterns

```typescript
// Success (200)
res.json({ success: true, data: user });

// Created (201)
res.status(201).json({ success: true, data: user });

// Error (400/500)
res.status(400).json({ success: false, error: { message: 'Invalid input' } });
```

### HTTP Status Codes

| Code | Use Case |
|------|----------|
| 200 | Success (GET, PUT) |
| 201 | Created (POST) |
| 204 | No Content (DELETE) |
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 500 | Server Error |

---

## Common Mistakes

### 1. Business Logic in Routes

```typescript
// ❌ Never do this
router.post('/submit', async (req, res) => {
    // 100+ lines of logic
    const user = await db.user.create(req.body);
    const workflow = await processWorkflow(user);
    res.json(workflow);
});

// ✅ Do this
router.post('/submit', (req, res) => controller.submit(req, res));
```

### 2. Wrong Middleware Order

```typescript
// ❌ Error handler before routes
app.use(errorBoundary);
app.use('/api', routes); // Won't catch errors

// ✅ Error handler after routes
app.use('/api', routes);
app.use(errorBoundary);
```

### 3. No Error Handling

```typescript
// ❌ Unhandled errors crash server
router.get('/user/:id', async (req, res) => {
    const user = await userService.get(req.params.id); // May throw
    res.json(user);
});

// ✅ Proper error handling
async getUser(req: Request, res: Response): Promise<void> {
    try {
        const user = await this.userService.get(req.params.id);
        this.handleSuccess(res, user);
    } catch (error) {
        this.handleError(error, res, 'getUser');
    }
}
```

---

## Common Imports

```typescript
// Express core
import express, { Request, Response, NextFunction, Router } from 'express';

// Middleware
import cookieParser from 'cookie-parser';
import cors from 'cors';

// Sentry
import * as Sentry from '@sentry/node';

// Utilities
import { AsyncLocalStorage } from 'async_hooks';
```

---

## Best Practices

1. **Keep Routes Clean** - Routes only route, delegate to controllers
2. **Use BaseController** - Consistent error handling and response formatting
3. **Proper Middleware Order** - Sentry → Parsers → Routes → Error handlers
4. **Type Everything** - Use TypeScript for Request/Response types
5. **Handle All Errors** - Use try-catch in controllers, error boundaries globally

---

**Related Skills:**
- **nodejs** - Core Node.js patterns and async handling
- **backend-dev-guidelines** - Complete backend architecture guide
- **prisma** - Database patterns with Prisma ORM
