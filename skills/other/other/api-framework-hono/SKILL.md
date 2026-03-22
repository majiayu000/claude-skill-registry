---
name: api-framework-hono
description: Hono routes, OpenAPI, Zod validation
---

# API Development with Hono + OpenAPI

> **Quick Guide:** Use Hono with `@hono/zod-openapi` for type-safe REST APIs that auto-generate OpenAPI specs. Import `z` from `@hono/zod-openapi` (NOT from `zod`) so `.openapi()` is available on all schemas. Always include `operationId` in routes and export the `app` instance for spec generation.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST import `z` from `@hono/zod-openapi`, NOT from `zod` -- this gives Zod the `.openapi()` method)**

**(You MUST export the `app` instance for OpenAPI spec generation)**

**(You MUST include `operationId` in every route for clean client generation)**

</critical_requirements>

---

**Auto-detection:** Hono, @hono/zod-openapi, OpenAPIHono, createRoute, Zod schemas with .openapi(), app.route(), createMiddleware, rate limiting, CORS configuration, health checks, hc client, RPC mode, getContext, tryGetContext, contextStorage, some/every/except middleware

**When to use:**

- Building type-safe REST APIs with auto-generated OpenAPI specs
- Defining OpenAPI specifications with automatic Zod validation
- Creating standardized error responses with proper status codes
- Implementing filtering, pagination, and sorting patterns
- Public or multi-client APIs needing formal documentation
- Production APIs requiring rate limiting, CORS, health checks

**When NOT to use:**

- Simple CRUD with no external consumers (Server Actions are simpler)
- Internal-only APIs without documentation requirements
- Single-use endpoints with no schema reuse (over-engineering)

**Key patterns covered:**

- Modular route setup with `app.route()` and `OpenAPIHono`
- Zod schema definitions with `.openapi()` metadata
- Route definition with `createRoute` (operationId, tags, responses)
- Error handling with named error codes
- Filtering, pagination, and data transformation
- Auth, rate limiting, CORS, logging, caching middleware
- Health check endpoints (shallow and deep)
- RPC client (`hc`) with end-to-end type safety
- Context Storage for out-of-handler context access
- Combine Middleware (`some`/`every`/`except`) for declarative auth

**Detailed Resources:**

- [examples/core.md](examples/core.md) - Route setup, list/detail endpoints
- [examples/validation.md](examples/validation.md) - Zod schema definitions with OpenAPI
- [examples/routes.md](examples/routes.md) - Filtering, pagination, data transformation
- [examples/middleware.md](examples/middleware.md) - Auth, rate limiting, CORS, logging, caching
- [examples/error-handling.md](examples/error-handling.md) - Standardized error responses
- [examples/openapi.md](examples/openapi.md) - Spec generation (build-time and endpoint)
- [examples/health-checks.md](examples/health-checks.md) - Liveness and readiness checks
- [examples/advanced-v4.md](examples/advanced-v4.md) - RPC, Context Storage, Combine Middleware
- [reference.md](reference.md) - Decision frameworks, anti-patterns, production checklist

---

<philosophy>

## Philosophy

**Type safety + documentation from code.** Zod schemas serve both validation AND OpenAPI spec generation. Single source of truth flows to clients via generated SDKs or Hono's RPC client.

**Use Hono + OpenAPI when:** Building public/multi-client APIs, need auto-generated documentation, require formal OpenAPI specs, want type-safe validation.

**Use simpler approaches when:** Internal-only CRUD, no external API consumers, no documentation needs.

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Modular Route Setup

Structure routes using `app.route()` for modularization. Export the `app` instance for spec generation.

```typescript
import { OpenAPIHono } from "@hono/zod-openapi";

const app = new OpenAPIHono().basePath("/api");

app.route("/", jobsRoutes);
app.route("/", companiesRoutes);

// REQUIRED: Export app for spec generation
export { app };
```

**Why good:** `app.route()` prevents God files, app export enables build-time spec generation

See [examples/core.md](examples/core.md) for complete setup with framework adapter exports.

---

### Pattern 2: Zod Schemas with OpenAPI Metadata

Import `z` from `@hono/zod-openapi` (not `zod`). Use `.openapi()` for schema registration and documentation.

```typescript
import { z } from "@hono/zod-openapi";

const MIN_SALARY = 0;
const CURRENCY_CODE_LENGTH = 3;

export const SalarySchema = z
  .object({
    min: z.number().min(MIN_SALARY),
    max: z.number().min(MIN_SALARY),
    currency: z.string().length(CURRENCY_CODE_LENGTH),
  })
  .openapi("Salary", {
    example: { min: 60000, max: 90000, currency: "EUR" },
  });
```

**Why good:** importing `z` from `@hono/zod-openapi` provides `.openapi()` automatically, named constants prevent magic number bugs, `.openapi("Name")` registers as `#/components/schemas/Name`

See [examples/validation.md](examples/validation.md) for complete schema patterns.

---

### Pattern 3: Route Definition with createRoute

Define routes with `createRoute` and implement with `app.openapi()`. Always include `operationId`.

```typescript
import { OpenAPIHono, createRoute, z } from "@hono/zod-openapi";

const getJobsRoute = createRoute({
  method: "get",
  path: "/jobs",
  operationId: "getJobs", // Becomes client method name
  tags: ["Jobs"],
  request: { query: JobsQuerySchema },
  responses: {
    200: {
      description: "List of jobs",
      content: { "application/json": { schema: JobsResponseSchema } },
    },
  },
});

app.openapi(getJobsRoute, async (c) => {
  const { country } = c.req.valid("query"); // Type-safe validated params
  // ... handler logic
  return c.json({ jobs: results }, 200);
});
```

**Why good:** `operationId` becomes clean client method name (`getJobs` vs `get_api_jobs`), `c.req.valid()` enforces schema validation with types

See [examples/core.md](examples/core.md) for list/detail endpoint examples.

---

### Pattern 4: Error Handling with Named Codes

Use named error code constants for consistent, machine-parseable error responses.

```typescript
export const ErrorCodes = {
  VALIDATION_ERROR: "validation_error",
  NOT_FOUND: "not_found",
  UNAUTHORIZED: "unauthorized",
  INTERNAL_ERROR: "internal_error",
} as const;
```

**Why good:** Named codes enable frontend `switch` handling, consistent shape across all endpoints

See [examples/error-handling.md](examples/error-handling.md) for the full `handleRouteError` utility.

---

### Pattern 5: JWT Authentication with Explicit Algorithm

Always specify the `alg` option on JWT/JWK middleware to prevent algorithm confusion attacks (CVE-2026-22817, CVE-2026-22818, patched in v4.11.4+).

```typescript
import { verify } from "hono/jwt";

const JWT_ALGORITHM = "HS256";

const payload = await verify(token, secret, JWT_ALGORITHM);
```

**Why good:** explicit algorithm prevents attackers from switching to symmetric verification with known public keys

See [examples/middleware.md](examples/middleware.md) for complete auth middleware with type-safe variables.

</patterns>

---

<red_flags>

## RED FLAGS

**High Priority:**

- Importing `z` from `"zod"` instead of `"@hono/zod-openapi"` -- `.openapi()` won't be available
- Missing `operationId` in routes -- generated client has ugly method names
- Not exporting `app` instance -- can't generate OpenAPI spec at build time
- JWT/JWK without explicit `alg` option -- algorithm confusion vulnerability (CVE-2026-22817/22818)

**Medium Priority:**

- Using `c.req.param()` / `c.req.query()` instead of `c.req.valid()` -- bypasses Zod validation
- No pagination limits on list endpoints -- returns massive datasets
- Generating spec at runtime instead of build time -- wasted CPU per request
- Not returning proper status codes -- always specify (200, 404, 500)
- Wildcard CORS (`"*"`) with `credentials: true` -- browsers reject this (spec violation)

**Gotchas & Edge Cases:**

- `c.req.valid("param")` uses singular `"param"`, not `"params"` -- easy to mistype
- In-memory rate limiting doesn't work across multiple instances -- use a shared store
- CORS middleware must be registered before auth middleware -- OPTIONS preflight bypasses auth
- ETags should not be used for user-specific data (generates unique ETag per user)
- RPC routes must be chained (`.openapi(r1, h1).openapi(r2, h2)`) for type inference -- separate calls break it
- Both client and server `tsconfig.json` need `"strict": true` for RPC type inference
- `contextStorage()` middleware must be registered before any code calls `getContext()`
- Use `tryGetContext()` (v4.11.0+) in code that may run outside request context (tests, background jobs)
- Middleware `next()` never throws in Hono -- wrapping `await next()` in try/catch is unnecessary
- `getConnInfo` is adapter-specific -- import from `hono/bun`, `hono/deno`, `@hono/node-server/conninfo`, etc. (NOT from `hono/ip-restriction`)

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md**

**(You MUST import `z` from `@hono/zod-openapi`, NOT from `zod` -- this gives Zod the `.openapi()` method)**

**(You MUST export the `app` instance for OpenAPI spec generation)**

**(You MUST include `operationId` in every route for clean client generation)**

**Failure to follow these rules will break OpenAPI spec generation and type safety.**

</critical_reminders>
