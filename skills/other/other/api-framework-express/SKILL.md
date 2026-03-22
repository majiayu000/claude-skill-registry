---
name: api-framework-express
description: Express.js routes, middleware, error handling, request/response patterns
---

# API Development with Express.js

> **Quick Guide:** Express uses middleware-based request processing. The three non-negotiable patterns: modular routing via `express.Router()`, centralized error handling with 4-argument middleware `(err, req, res, next)`, and correct middleware ordering (security first, error handler last). Express 5 (now stable, default on npm) auto-forwards async errors; Express 4 requires manual `next(err)` or a wrapper.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST define error-handling middleware with 4 arguments: `(err, req, res, next)` - Express identifies error handlers by arity)**

**(You MUST register error handlers AFTER all routes and other middleware)**

**(You MUST call `next(err)` to forward async errors in Express 4 - Express 5 auto-forwards rejected promises)**

**(You MUST use `express.json()` and `express.urlencoded()` for body parsing - `req.body` is undefined without them)**

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

- Need auto-generated OpenAPI documentation from schemas
- Building edge/serverless functions where cold start matters
- Need strict end-to-end type safety with schema validation
- GraphQL APIs (use a dedicated GraphQL server)

**Key patterns covered:**

- Middleware chain with `app.use()` and `next()`
- Modular routes with `express.Router()`
- Error handling with 4-argument middleware
- Async error forwarding (Express 4 vs 5)
- Request validation middleware
- Route parameters and query string handling
- Route guards for authentication/authorization
- Middleware ordering (security, CORS, rate limit, parsing, routes, errors)

**Detailed Resources:**

- [examples/core.md](examples/core.md) - App setup, error handler, async handler, body parsing
- [examples/middleware.md](examples/middleware.md) - Logging, validation, auth guards, middleware ordering
- [examples/routing.md](examples/routing.md) - Modular routes, parameters, response helpers, versioned APIs
- [reference.md](reference.md) - Decision frameworks, anti-patterns, production checklist

---

<philosophy>

## Philosophy

**Middleware-first architecture.** Express processes requests through a chain of middleware functions. Each middleware can modify request/response objects, end the response, or call `next()` to continue the chain. Everything in Express is middleware - body parsers, auth guards, loggers, error handlers.

**Express 4 vs 5:** Express 5 (stable since 2025, now default on npm) auto-forwards errors from rejected promises in async handlers. Express 4 requires explicit `try/catch` + `next(err)` or a wrapper utility. Both versions require the 4-argument signature for error handlers.

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Application Setup

Register body parsers early, mount route modules, register error handler last. See [examples/core.md](examples/core.md) for full implementation.

```typescript
const app: Express = express();

// Body parsing
app.use(express.json({ limit: JSON_LIMIT }));
app.use(express.urlencoded({ extended: true }));

// Mount route modules
app.use("/api/users", userRoutes);
app.use("/api/products", productRoutes);

// Error handler MUST be last
app.use(errorHandler);

export { app };
```

**Why good:** Body parsers before routes so `req.body` is populated, error handler last to catch all errors, modular route mounting

---

### Pattern 2: Modular Routes with express.Router()

One Router per resource, mounted at a path prefix. See [examples/routing.md](examples/routing.md) for CRUD examples with parameters.

```typescript
// src/routes/user-routes.ts
const router = Router();

router.get("/", async (req, res, next) => {
  try {
    const users = await getUsersFromDatabase();
    res.status(HTTP_OK).json({ data: users });
  } catch (error) {
    next(error);
  }
});

export { router as userRoutes };
```

**Why good:** Router isolates related routes, named export, explicit error forwarding

---

### Pattern 3: Error Handling Middleware (4 Arguments)

Express identifies error handlers by the 4-argument signature `(err, req, res, next)`. This is the most critical Express pattern to get right. See [examples/core.md](examples/core.md) for full implementation.

```typescript
// CRITICAL: Must have exactly 4 arguments
const errorHandler = (
  err: AppError,
  req: Request,
  res: Response,
  next: NextFunction,
): void => {
  if (res.headersSent) {
    next(err);
    return;
  }

  const statusCode = err.statusCode || HTTP_INTERNAL_ERROR;
  res.status(statusCode).json({
    error: { message: err.message, code: err.code || "INTERNAL_ERROR" },
  });
};
```

**Why good:** 4 arguments for Express to recognize as error handler, checks `headersSent` to avoid double-response, consistent error shape

**Common mistake:** 3-argument function `(err, req, res)` is treated as regular middleware - `err` becomes `req`, completely wrong behavior

---

### Pattern 4: Async Error Handling

Express 5 auto-forwards rejected promises. Express 4 requires explicit forwarding. See [examples/core.md](examples/core.md) for the asyncHandler wrapper.

```typescript
// Express 5: async errors auto-forwarded
router.get("/:id", async (req, res) => {
  const product = await getProductById(req.params.id);
  res.status(HTTP_OK).json({ data: product });
});

// Express 4: MUST forward manually
router.get("/:id", async (req, res, next) => {
  try {
    const product = await getProductById(req.params.id);
    res.status(HTTP_OK).json({ data: product });
  } catch (error) {
    next(error); // Required in Express 4
  }
});
```

**Why this matters:** In Express 4, unhandled async rejections cause the request to hang until timeout. Express 5 fixes this but many projects still run Express 4.

---

### Pattern 5: Request Validation Middleware

Validate `req.body` in middleware before the route handler processes it. See [examples/middleware.md](examples/middleware.md) for full validation patterns.

```typescript
const validateUserCreate = (
  req: Request,
  res: Response,
  next: NextFunction,
): void => {
  const { name, email } = req.body;
  const errors: string[] = [];

  if (!name || name.length < MIN_NAME_LENGTH) errors.push("Name is required");
  if (!email || !email.includes("@")) errors.push("Valid email is required");

  if (errors.length > 0) {
    res
      .status(HTTP_BAD_REQUEST)
      .json({ error: { message: "Validation failed", details: errors } });
    return;
  }
  next();
};

// Apply: router.post("/", validateUserCreate, createHandler);
```

**Why good:** Validation separated from business logic, early return on failure, reusable across routes

---

### Pattern 6: Route Guards (Authentication/Authorization)

Protect routes with middleware that validates access. See [examples/middleware.md](examples/middleware.md) for full auth guard implementation.

```typescript
// Extend Request with user data
interface AuthenticatedRequest extends Request {
  user?: { id: string; role: string };
}

const requireAuth = (
  req: AuthenticatedRequest,
  res: Response,
  next: NextFunction,
): void => {
  const token = req.headers.authorization?.replace("Bearer ", "");
  if (!token) {
    res
      .status(HTTP_UNAUTHORIZED)
      .json({ error: { message: "Authentication required" } });
    return;
  }
  req.user = verifyToken(token);
  next();
};

// Apply to all routes in router: router.use(requireAuth);
// Apply to specific route: router.delete("/:id", requireAuth, requireRole("admin"), handler);
```

**Why good:** Auth middleware reusable, role guard configurable, extends Request type for type safety

---

### Pattern 7: Middleware Ordering

Order matters. Security first, error handler last. See [examples/middleware.md](examples/middleware.md) for complete ordering example.

```
1. Security headers (helmet)
2. CORS
3. Rate limiting (before body parsing to save resources)
4. Body parsing (express.json, express.urlencoded)
5. Request logging
6. Routes
7. 404 handler (after all routes)
8. Error handler (LAST)
```

**Why this order:** Security rejects bad requests early. Rate limiting before parsing saves CPU on abusive requests. Error handler must be last to catch all errors from routes.

---

### Pattern 8: Response Helpers

Standardize API responses with typed helpers. See [examples/routing.md](examples/routing.md) for full implementation.

```typescript
const sendSuccess = <T>(res: Response, data: T, statusCode = HTTP_OK): void => {
  res.status(statusCode).json({ success: true, data });
};

const sendNotFound = (res: Response, resource = "Resource"): void => {
  res
    .status(HTTP_NOT_FOUND)
    .json({ success: false, error: { message: `${resource} not found` } });
};
```

**Why good:** Consistent response shape across all routes, typed helpers reduce boilerplate

---

### Express 5 Migration Notes

Express 5 is the default on npm since March 2025. Key changes from Express 4:

| Change                | Express 4          | Express 5                                      |
| --------------------- | ------------------ | ---------------------------------------------- |
| Async errors          | Manual `next(err)` | Auto-forwarded                                 |
| `req.body` (unparsed) | `{}`               | `undefined`                                    |
| `req.query`           | Writable           | Read-only getter                               |
| Wildcard routes       | `/*`               | `/*splat` (no root) or `/{*splat}` (with root) |
| Optional params       | `/:file.:ext?`     | `/:file{.:ext}`                                |
| `urlencoded` default  | `extended: true`   | `extended: false`                              |
| `req.host`            | Strips port        | Includes port                                  |
| Minimum Node.js       | Any                | 18+                                            |

**Removed in Express 5:** `req.param()`, `res.send(body, status)`, `res.send(status)` (use `res.sendStatus()`), `res.json(obj, status)`, `res.redirect(url, status)`, `res.redirect('back')` (use `req.get('Referrer') || '/'`), `res.sendfile()` (use `res.sendFile()`), `app.del()` (use `app.delete()`).

</patterns>

---

<red_flags>

## RED FLAGS

**High Priority:**

- **Error handler has only 3 arguments** - Express treats it as regular middleware, errors silently ignored
- **Error handler registered before routes** - Never catches route errors
- **Missing `next(error)` in async handlers (Express 4)** - Unhandled promise rejection, request hangs
- **Not using `express.json()` middleware** - `req.body` is undefined for JSON requests
- **Magic HTTP status codes** - Use named constants (`HTTP_OK = 200`, `HTTP_NOT_FOUND = 404`)

**Medium Priority:**

- **All routes in single file** - Creates unmaintainable God file, use `express.Router()`
- **Not checking `res.headersSent` in error handler** - Causes "headers already sent" crashes
- **Default exports on route modules** - Violates project conventions
- **Wildcard CORS with credentials** - Browsers reject `origin: "*"` with `credentials: true`
- **Missing rate limiting on public APIs** - Vulnerable to abuse

**Gotchas & Edge Cases:**

- **`next('route')` vs `next(error)`** - String `'route'` skips to next route handler; anything else triggers error handler
- **`req.query` values are always strings** - Parse numbers with `parseInt(val, 10)`
- **`express.static` without auth** - Files publicly accessible unless middleware guards them
- **Router `mergeParams: true`** - Required to access parent route params in nested routers
- **Express 5: `req.body` is `undefined` when unparsed** - was `{}` in Express 4, may break `if (!req.body)` checks

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

**Before implementing ANY Express route, verify these requirements are met:**

> **All code must follow project conventions in CLAUDE.md**

**(You MUST define error-handling middleware with 4 arguments: `(err, req, res, next)` - Express identifies error handlers by arity)**

**(You MUST register error handlers AFTER all routes and other middleware)**

**(You MUST call `next(err)` to forward async errors in Express 4 - Express 5 auto-forwards rejected promises)**

**(You MUST use `express.json()` and `express.urlencoded()` for body parsing - `req.body` is undefined without them)**

**Failure to follow these rules will cause unhandled errors and broken middleware chains.**

</critical_reminders>
