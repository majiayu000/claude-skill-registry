---
name: api-framework-express
description: Express.js routes, middleware, error handling, request/response patterns
---

# API Development with Express.js

> **Quick Guide:** Use Express.js for building REST APIs with middleware-based request processing. The framework excels at composable middleware chains, modular routing via `express.Router()`, and centralized error handling with 4-argument error middleware `(err, req, res, next)`.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST define error-handling middleware with 4 arguments: `(err, req, res, next)`)**

**(You MUST register error handlers AFTER all routes and other middleware)**

**(You MUST call `next(err)` to forward async errors in Express 4 - Express 5 handles this automatically)**

**(You MUST use `express.json()` and `express.urlencoded()` for body parsing)**

</critical_requirements>

---

**Auto-detection:** Express.js, express, app.use, app.get, app.post, app.put, app.delete, express.Router, req.params, req.query, req.body, res.json, res.status, middleware, next(), error handler, router.use, express.static, express.json, express.urlencoded

**When to use:**

- Building REST APIs with composable middleware patterns
- Need modular route organization with `express.Router()`
- Require centralized error handling across all routes
- Building APIs that need body parsing, static files, or cookie handling
- Creating route guards for authentication/authorization

**When NOT to use:**

- Need auto-generated OpenAPI documentation (consider Hono + OpenAPI or Fastify + Swagger)
- Building edge/serverless functions where cold start matters (consider Hono)
- Need strict type safety with Zod validation built-in (consider Hono + zod-openapi)
- GraphQL APIs (use Apollo Server or similar)

**Key patterns covered:**

- Middleware chain with `app.use()` and `next()`
- Routing with `app.get/post/put/delete` and route parameters
- Modular routes with `express.Router()`
- Error handling with 4-argument middleware
- Async/await error forwarding patterns
- Request validation and parsing
- Response patterns with `res.json()` and `res.status()`
- Static file serving with `express.static()`
- Route guards for authentication/authorization

**Detailed Resources:**

- For code examples:
  - [middleware.md](examples/middleware.md) - Middleware chains, error handling, validation, auth guards
  - [routing.md](examples/routing.md) - Modular routes, parameters, response patterns
- For decision frameworks and anti-patterns, see [reference.md](reference.md)

---

<philosophy>

## Philosophy

**Middleware-first architecture.** Express processes requests through a chain of middleware functions. Each middleware can modify request/response objects, end the response, or call `next()` to continue the chain.

**Use Express when:** Need mature ecosystem with extensive middleware library, building traditional REST APIs, team familiarity with Express patterns.

**Use alternatives when:** Need OpenAPI generation (Hono), edge deployment (Hono/Fastify), strict type safety with schema validation (tRPC).

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Application Setup with Built-in Middleware

Set up Express with body parsing middleware and basic configuration.

#### Constants

```typescript
const PORT = 3000;
const JSON_LIMIT = "10mb";
```

#### Implementation

```typescript
// src/app.ts
import express from "express";
import type { Express } from "express";

import { userRoutes } from "./routes/user-routes";
import { productRoutes } from "./routes/product-routes";
import { errorHandler } from "./middleware/error-handler";

const app: Express = express();

// Built-in middleware for body parsing
app.use(express.json({ limit: JSON_LIMIT }));
app.use(express.urlencoded({ extended: true }));

// Mount route modules
app.use("/api/users", userRoutes);
app.use("/api/products", productRoutes);

// Error handler MUST be last
app.use(errorHandler);

export { app };
```

**Why good:** Named constants for configuration, built-in body parsers registered early, error handler registered last, modular route mounting

```typescript
// WRONG: Magic strings and error handler in wrong position
const app = express();
app.use(errorHandler); // Error handler too early - won't catch route errors
app.use(express.json({ limit: "10mb" })); // Magic string
app.use("/api/users", userRoutes);
```

**Why bad:** Error handler before routes means it never catches errors, magic strings make configuration hard to maintain

---

### Pattern 2: Modular Routes with express.Router()

Create modular, mountable route handlers for better organization.

```typescript
// src/routes/user-routes.ts
import { Router } from "express";
import type { Request, Response, NextFunction } from "express";

const router = Router();

const HTTP_OK = 200;
const HTTP_CREATED = 201;
const HTTP_NOT_FOUND = 404;

// GET /api/users
router.get("/", async (req: Request, res: Response, next: NextFunction) => {
  try {
    const users = await getUsersFromDatabase();
    res.status(HTTP_OK).json({ data: users });
  } catch (error) {
    next(error); // Forward to error handler
  }
});

// GET /api/users/:id
router.get("/:id", async (req: Request, res: Response, next: NextFunction) => {
  try {
    const { id } = req.params;
    const user = await getUserById(id);

    if (!user) {
      res.status(HTTP_NOT_FOUND).json({ error: "User not found" });
      return;
    }

    res.status(HTTP_OK).json({ data: user });
  } catch (error) {
    next(error);
  }
});

// POST /api/users
router.post("/", async (req: Request, res: Response, next: NextFunction) => {
  try {
    const userData = req.body;
    const newUser = await createUser(userData);
    res.status(HTTP_CREATED).json({ data: newUser });
  } catch (error) {
    next(error);
  }
});

// Named export (project convention)
export { router as userRoutes };
```

**Why good:** Router isolates related routes, named HTTP status constants, explicit error forwarding with next(error), named export follows convention

```typescript
// WRONG: All routes in main app file
const app = express();
app.get("/api/users", (req, res) => {
  /* ... */
});
app.get("/api/users/:id", (req, res) => {
  /* ... */
});
app.post("/api/users", (req, res) => {
  /* ... */
});
app.get("/api/products", (req, res) => {
  /* ... */
});
// ... hundreds more lines

export default app; // Default export
```

**Why bad:** God file with all routes, no separation of concerns, default export violates convention

---

### Pattern 3: Error Handling Middleware (4 Arguments)

Error handlers MUST have 4 arguments: `(err, req, res, next)`.

```typescript
// src/middleware/error-handler.ts
import type { Request, Response, NextFunction } from "express";

const HTTP_BAD_REQUEST = 400;
const HTTP_INTERNAL_ERROR = 500;

interface AppError extends Error {
  statusCode?: number;
  code?: string;
}

const errorHandler = (
  err: AppError,
  req: Request,
  res: Response,
  next: NextFunction,
): void => {
  console.error(`[Error] ${req.method} ${req.path}:`, err.message);

  // Already sent response - delegate to default handler
  if (res.headersSent) {
    next(err);
    return;
  }

  const statusCode = err.statusCode || HTTP_INTERNAL_ERROR;
  const message = err.message || "Internal server error";

  res.status(statusCode).json({
    error: {
      message,
      code: err.code || "INTERNAL_ERROR",
      path: req.path,
    },
  });
};

export { errorHandler };
```

**Why good:** 4 arguments identifies this as error middleware, checks headersSent to avoid double-response, logs with request context, consistent error shape

```typescript
// WRONG: Only 3 arguments - Express won't recognize as error handler
const errorHandler = (err, req, res) => {
  res.status(500).send("Error"); // Magic number
};

// WRONG: Not checking headersSent
const errorHandler = (err, req, res, next) => {
  res.status(500).json({ error: err.message }); // May crash if headers sent
};
```

**Why bad:** 3-argument function treated as regular middleware (ignores err), not checking headersSent causes "headers already sent" crashes

---

### Pattern 4: Async Error Handling

Forward errors from async functions to the error handler.

#### Express 4 Pattern (Manual Forwarding)

```typescript
// src/routes/product-routes.ts
import { Router } from "express";
import type { Request, Response, NextFunction } from "express";

const router = Router();
const HTTP_OK = 200;

// Option 1: try/catch with next(error)
router.get("/:id", async (req: Request, res: Response, next: NextFunction) => {
  try {
    const product = await getProductById(req.params.id);
    res.status(HTTP_OK).json({ data: product });
  } catch (error) {
    next(error); // REQUIRED in Express 4
  }
});

// Option 2: Promise .catch(next)
router.get("/featured", (req: Request, res: Response, next: NextFunction) => {
  getFeaturedProducts()
    .then((products) => res.status(HTTP_OK).json({ data: products }))
    .catch(next);
});

export { router as productRoutes };
```

#### Wrapper Function for Cleaner Code

```typescript
// src/utils/async-handler.ts
import type { Request, Response, NextFunction, RequestHandler } from "express";

type AsyncHandler = (
  req: Request,
  res: Response,
  next: NextFunction,
) => Promise<void>;

const asyncHandler = (fn: AsyncHandler): RequestHandler => {
  return (req, res, next) => {
    Promise.resolve(fn(req, res, next)).catch(next);
  };
};

export { asyncHandler };
```

```typescript
// Usage with wrapper
import { asyncHandler } from "../utils/async-handler";

router.get(
  "/:id",
  asyncHandler(async (req, res) => {
    const product = await getProductById(req.params.id);
    res.status(HTTP_OK).json({ data: product });
    // Errors automatically forwarded to error handler
  }),
);
```

**Why good:** asyncHandler removes try/catch boilerplate, errors automatically forwarded, cleaner route definitions

```typescript
// WRONG: Missing error forwarding in Express 4
router.get("/:id", async (req, res) => {
  const product = await getProductById(req.params.id); // Error = unhandled rejection
  res.json({ data: product });
});
```

**Why bad:** Async errors not caught by Express 4, causes unhandled promise rejection and request hangs

---

### Pattern 5: Request Validation Middleware

Validate request data before handlers process it.

```typescript
// src/middleware/validate-request.ts
import type { Request, Response, NextFunction } from "express";

const HTTP_BAD_REQUEST = 400;
const MIN_NAME_LENGTH = 1;
const MAX_NAME_LENGTH = 100;

interface UserCreateBody {
  name: string;
  email: string;
}

const validateUserCreate = (
  req: Request,
  res: Response,
  next: NextFunction,
): void => {
  const { name, email } = req.body as UserCreateBody;
  const errors: string[] = [];

  if (!name || name.length < MIN_NAME_LENGTH || name.length > MAX_NAME_LENGTH) {
    errors.push(
      `Name must be between ${MIN_NAME_LENGTH} and ${MAX_NAME_LENGTH} characters`,
    );
  }

  if (!email || !email.includes("@")) {
    errors.push("Valid email is required");
  }

  if (errors.length > 0) {
    res.status(HTTP_BAD_REQUEST).json({
      error: {
        message: "Validation failed",
        details: errors,
      },
    });
    return;
  }

  next();
};

export { validateUserCreate };
```

```typescript
// Apply validation middleware to route
router.post("/", validateUserCreate, async (req, res, next) => {
  try {
    // req.body is validated at this point
    const user = await createUser(req.body);
    res.status(HTTP_CREATED).json({ data: user });
  } catch (error) {
    next(error);
  }
});
```

**Why good:** Validation separated from business logic, named constants for limits, early return on validation failure, reusable across routes

---

### Pattern 6: Route Parameters and Query Strings

Access dynamic URL segments and query parameters.

```typescript
// src/routes/search-routes.ts
import { Router } from "express";
import type { Request, Response, NextFunction } from "express";

const router = Router();
const HTTP_OK = 200;
const DEFAULT_PAGE = 1;
const DEFAULT_LIMIT = 20;
const MAX_LIMIT = 100;

interface SearchQuery {
  q?: string;
  page?: string;
  limit?: string;
  sort?: string;
}

// GET /api/search?q=term&page=1&limit=20&sort=date
router.get("/", async (req: Request, res: Response, next: NextFunction) => {
  try {
    const { q, page, limit, sort } = req.query as SearchQuery;

    const pageNum = parseInt(page || String(DEFAULT_PAGE), 10);
    const limitNum = Math.min(
      parseInt(limit || String(DEFAULT_LIMIT), 10),
      MAX_LIMIT,
    );

    const results = await searchItems({
      query: q || "",
      page: pageNum,
      limit: limitNum,
      sort: sort || "relevance",
    });

    res.status(HTTP_OK).json({
      data: results.items,
      pagination: {
        page: pageNum,
        limit: limitNum,
        total: results.total,
      },
    });
  } catch (error) {
    next(error);
  }
});

// Route parameters: GET /api/users/:userId/posts/:postId
router.get(
  "/users/:userId/posts/:postId",
  async (req: Request, res: Response, next: NextFunction) => {
    try {
      const { userId, postId } = req.params;
      const post = await getPostByUserAndId(userId, postId);
      res.status(HTTP_OK).json({ data: post });
    } catch (error) {
      next(error);
    }
  },
);

export { router as searchRoutes };
```

**Why good:** Query params typed, default values with named constants, parseInt with radix 10, limit capped at MAX_LIMIT to prevent abuse

---

### Pattern 7: Route Guards (Authentication/Authorization)

Protect routes with middleware that validates access.

```typescript
// src/middleware/auth-guard.ts
import type { Request, Response, NextFunction } from "express";

const HTTP_UNAUTHORIZED = 401;
const HTTP_FORBIDDEN = 403;

interface AuthenticatedRequest extends Request {
  user?: {
    id: string;
    role: string;
  };
}

const requireAuth = (
  req: AuthenticatedRequest,
  res: Response,
  next: NextFunction,
): void => {
  const token = req.headers.authorization?.replace("Bearer ", "");

  if (!token) {
    res.status(HTTP_UNAUTHORIZED).json({
      error: { message: "Authentication required" },
    });
    return;
  }

  try {
    // Verify token with your auth solution
    const user = verifyToken(token);
    req.user = user;
    next();
  } catch {
    res.status(HTTP_UNAUTHORIZED).json({
      error: { message: "Invalid token" },
    });
  }
};

const requireRole = (allowedRoles: string[]) => {
  return (
    req: AuthenticatedRequest,
    res: Response,
    next: NextFunction,
  ): void => {
    if (!req.user) {
      res.status(HTTP_UNAUTHORIZED).json({
        error: { message: "Authentication required" },
      });
      return;
    }

    if (!allowedRoles.includes(req.user.role)) {
      res.status(HTTP_FORBIDDEN).json({
        error: { message: "Insufficient permissions" },
      });
      return;
    }

    next();
  };
};

export { requireAuth, requireRole };
export type { AuthenticatedRequest };
```

```typescript
// Apply guards to routes
import { requireAuth, requireRole } from "../middleware/auth-guard";

// All routes in this router require authentication
router.use(requireAuth);

// Only admins can delete users
router.delete("/:id", requireRole(["admin"]), async (req, res, next) => {
  try {
    await deleteUser(req.params.id);
    res.status(HTTP_OK).json({ message: "User deleted" });
  } catch (error) {
    next(error);
  }
});
```

**Why good:** Auth middleware reusable, role-based guard configurable, extends Request type for type safety, clear separation of auth concerns

---

### Pattern 8: Static Files and Built-in Middleware

Serve static assets and use Express built-in middleware.

```typescript
// src/app.ts
import express from "express";
import path from "path";

const app = express();

const STATIC_MAX_AGE_MS = 86400000; // 1 day in milliseconds

// Serve static files from 'public' directory
app.use(
  express.static(path.join(__dirname, "public"), {
    maxAge: STATIC_MAX_AGE_MS,
    etag: true,
  }),
);

// Serve uploaded files from 'uploads' with restricted access
app.use(
  "/uploads",
  requireAuth, // Protect uploads
  express.static(path.join(__dirname, "uploads")),
);

export { app };
```

**Why good:** Caching configured with named constant, path.join for cross-platform compatibility, protected static route with auth middleware

---

### Pattern 9: Response Patterns with Consistent Shape

Standardize API responses for predictable client consumption.

```typescript
// src/utils/response-helpers.ts
import type { Response } from "express";

const HTTP_OK = 200;
const HTTP_CREATED = 201;
const HTTP_NO_CONTENT = 204;
const HTTP_BAD_REQUEST = 400;
const HTTP_NOT_FOUND = 404;

interface SuccessResponse<T> {
  success: true;
  data: T;
  meta?: Record<string, unknown>;
}

interface ErrorResponse {
  success: false;
  error: {
    message: string;
    code?: string;
    details?: unknown;
  };
}

const sendSuccess = <T>(
  res: Response,
  data: T,
  statusCode: number = HTTP_OK,
  meta?: Record<string, unknown>,
): void => {
  const response: SuccessResponse<T> = { success: true, data };
  if (meta) {
    response.meta = meta;
  }
  res.status(statusCode).json(response);
};

const sendCreated = <T>(res: Response, data: T): void => {
  sendSuccess(res, data, HTTP_CREATED);
};

const sendNoContent = (res: Response): void => {
  res.status(HTTP_NO_CONTENT).send();
};

const sendError = (
  res: Response,
  message: string,
  statusCode: number = HTTP_BAD_REQUEST,
  code?: string,
  details?: unknown,
): void => {
  const response: ErrorResponse = {
    success: false,
    error: { message, code, details },
  };
  res.status(statusCode).json(response);
};

const sendNotFound = (res: Response, resource: string = "Resource"): void => {
  sendError(res, `${resource} not found`, HTTP_NOT_FOUND, "NOT_FOUND");
};

export { sendSuccess, sendCreated, sendNoContent, sendError, sendNotFound };
```

```typescript
// Usage in routes
import {
  sendSuccess,
  sendCreated,
  sendNotFound,
} from "../utils/response-helpers";

router.get("/:id", async (req, res, next) => {
  try {
    const user = await getUserById(req.params.id);
    if (!user) {
      sendNotFound(res, "User");
      return;
    }
    sendSuccess(res, user);
  } catch (error) {
    next(error);
  }
});
```

**Why good:** Consistent response shape, typed responses, reusable helpers reduce boilerplate, status codes as named constants

---

### Pattern 10: Middleware Order Best Practices

Order matters for security, parsing, and error handling.

```typescript
// src/app.ts
import express from "express";
import helmet from "helmet";
import cors from "cors";
import rateLimit from "express-rate-limit";

const app = express();

const RATE_LIMIT_WINDOW_MS = 900000; // 15 minutes
const RATE_LIMIT_MAX_REQUESTS = 100;
const JSON_LIMIT = "10mb";

// 1. Security headers FIRST
app.use(helmet());

// 2. CORS configuration
app.use(
  cors({
    origin: process.env.ALLOWED_ORIGINS?.split(",") || [],
    credentials: true,
  }),
);

// 3. Rate limiting (before body parsing to save resources)
app.use(
  rateLimit({
    windowMs: RATE_LIMIT_WINDOW_MS,
    max: RATE_LIMIT_MAX_REQUESTS,
    standardHeaders: true,
    legacyHeaders: false,
  }),
);

// 4. Body parsing
app.use(express.json({ limit: JSON_LIMIT }));
app.use(express.urlencoded({ extended: true }));

// 5. Request logging (after parsing, before routes)
app.use(requestLogger);

// 6. Routes
app.use("/api/users", userRoutes);
app.use("/api/products", productRoutes);

// 7. 404 handler (after all routes)
app.use((req, res) => {
  res.status(404).json({ error: { message: "Route not found" } });
});

// 8. Error handler LAST
app.use(errorHandler);

export { app };
```

**Why good:** Security (helmet) first, rate limiting before expensive body parsing, error handler absolutely last, 404 handler catches unmatched routes

</patterns>

---

<integration>

## Integration Guide

**Works with:**

- **Your validation library**: Validate `req.body` in middleware before handlers
- **Your database solution**: Query in route handlers, forward errors with `next(error)`
- **Your authentication solution**: Implement as route guard middleware
- **Your logging solution**: Add request/error logging middleware

**Replaces / Conflicts with:**

- **Hono**: Both are HTTP frameworks - choose one per project
- **Fastify**: Both are HTTP frameworks - choose one per project
- **Koa**: Both are HTTP frameworks - choose one per project

</integration>

---

<critical_reminders>

## CRITICAL REMINDERS

**Before implementing ANY Express route, verify these requirements are met:**

> **All code must follow project conventions in CLAUDE.md**

**(You MUST define error-handling middleware with 4 arguments: `(err, req, res, next)`)**

**(You MUST register error handlers AFTER all routes and other middleware)**

**(You MUST call `next(err)` to forward async errors in Express 4 - Express 5 handles this automatically)**

**(You MUST use `express.json()` and `express.urlencoded()` for body parsing)**

**Failure to follow these rules will cause unhandled errors and broken middleware chains.**

</critical_reminders>
