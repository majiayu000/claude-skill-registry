---
name: api-framework-hono
description: Hono routes, OpenAPI, Zod validation
---

# API Development with Hono + OpenAPI

> **Quick Guide:** Use Hono with @hono/zod-openapi for type-safe REST APIs that auto-generate OpenAPI specs. Zod schemas provide validation AND documentation. Export your Hono app for spec generation to enable client code generation.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST call `extendZodWithOpenApi(z)` BEFORE defining ANY Zod schemas)**

**(You MUST export the `app` instance for OpenAPI spec generation)**

**(You MUST include `operationId` in every route for clean client generation)**

</critical_requirements>

---

**Auto-detection:** Hono, @hono/zod-openapi, OpenAPIHono, createRoute, Zod schemas with .openapi(), app.route(), createMiddleware, rate limiting, CORS configuration, health checks, hc client, RPC mode, getContext, tryGetContext, contextStorage, some/every/except middleware

**When to use:**

- Building type-safe REST APIs in Next.js API routes with Hono
- Defining OpenAPI specifications with automatic validation
- Creating standardized error responses with proper status codes
- Implementing filtering, pagination, and sorting patterns
- Need public or multi-client API with documentation
- Production APIs requiring rate limiting, CORS, health checks

**When NOT to use:**

- Simple CRUD operations with no external consumers (use Server Actions instead)
- Internal-only APIs without documentation requirements (simpler approaches exist)
- Forms that don't need complex validation (React Hook Form + Server Actions)
- When building GraphQL APIs (use Apollo Server or similar)
- Single-use endpoints with no schema reuse (over-engineering)

**Key patterns covered:**

- Hono API route setup with OpenAPI integration
- Zod schema definition with OpenAPI metadata (.openapi() method)
- Route definition with createRoute (operationId, tags, responses)
- Standardized error handling with error codes and constants
- Filtering with multiple values (comma-separated, case-insensitive)
- Pagination patterns (offset-based with proper constants)
- Data transformation utilities (date formatting, object mapping)
- OpenAPI spec generation at build time
- Authentication middleware with type-safe variables
- Rate limiting with response headers and 429 handling
- CORS configuration with origin allowlisting
- Health check endpoints (shallow and deep)
- Request/response logging with PII sanitization
- Caching strategies (Cache-Control, ETags)
- RPC client (hc) with end-to-end type safety (v4.11.0+)
- Context Storage for accessing context outside handlers (v4.6.0+)
- Combine Middleware (some/every/except) for complex auth logic (v4.x)

**Detailed Resources:**

- For code examples, see [examples/](examples/) (core.md, validation.md, routes.md, middleware.md, etc.)
- For decision frameworks and anti-patterns, see [reference.md](reference.md)

---

<philosophy>

## Philosophy

**Type safety + documentation from code.** Zod schemas serve both validation AND OpenAPI spec generation. Single source of truth flows to frontend via your chosen client code generator.

**Use Hono + OpenAPI when:** Building public/multi-client APIs, need auto-generated documentation, require formal OpenAPI specs.

**Use Server Actions when:** Simple CRUD, internal-only, no external API consumers, no complex validation.

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: API Route Setup

Structure API routes in `/app/api/` using catch-all route pattern. Use `app.route()` for modularization.

**File: `/app/api/[[...route]]/route.ts`**

```typescript
// Import order: External deps -> Relative imports
import { OpenAPIHono } from "@hono/zod-openapi";
import { handle } from "hono/vercel";

import { jobsRoutes } from "../routes/jobs";
import { companiesRoutes } from "../routes/companies";

// Create main app with base path
const app = new OpenAPIHono().basePath("/api");

// Mount route modules using app.route()
app.route("/", jobsRoutes);
app.route("/", companiesRoutes);

// REQUIRED: Export app for OpenAPI spec generation
export { app };

// Export handlers for Next.js (all HTTP methods)
export const GET = handle(app);
export const POST = handle(app);
export const PUT = handle(app);
export const PATCH = handle(app);
export const DELETE = handle(app);
```

**Why good:** app.route() prevents God files, app export enables build-time spec generation, named exports follow project convention

---

### Pattern 2: Zod Schema Definition with OpenAPI

Schemas serve both validation AND documentation via `.openapi()` method.

**File: `/app/api/schemas.ts`**

```typescript
import { z } from "zod";
import { extendZodWithOpenApi } from "@hono/zod-openapi";

// REQUIRED: Extend Zod with OpenAPI methods BEFORE defining schemas
extendZodWithOpenApi(z);

const MIN_SALARY = 0;
const CURRENCY_CODE_LENGTH = 3;
const MIN_TITLE_LENGTH = 1;
const MAX_TITLE_LENGTH = 255;
const DEFAULT_LIMIT = "50";

export const SalarySchema = z
  .object({
    min: z.number().min(MIN_SALARY),
    max: z.number().min(MIN_SALARY),
    currency: z.string().length(CURRENCY_CODE_LENGTH),
  })
  .openapi("Salary", {
    example: { min: 60000, max: 90000, currency: "EUR" },
  });

export const JobSchema = z
  .object({
    id: z.string().uuid(),
    title: z.string().min(MIN_TITLE_LENGTH).max(MAX_TITLE_LENGTH),
    description: z.string(),
    employmentType: z.string().nullable(),
    salary: SalarySchema.nullable(),
  })
  .openapi("Job");

export type Job = z.infer<typeof JobSchema>;
```

**Why good:** extendZodWithOpenApi first (required for .openapi() to exist), named constants prevent magic number bugs, reusable sub-schemas reduce duplication

---

### Pattern 3: Route Definition with createRoute

Define routes with OpenAPI metadata using `createRoute` and `app.openapi()`.

**File: `/app/api/routes/jobs.ts`**

```typescript
import { OpenAPIHono, createRoute, z } from "@hono/zod-openapi";
import { and, eq, desc, isNull } from "drizzle-orm";

import { db, jobs, companies } from "@/lib/db";
import {
  JobsQuerySchema,
  JobsResponseSchema,
  ErrorResponseSchema,
} from "../schemas";

const DEFAULT_QUERY_LIMIT = 100;
const app = new OpenAPIHono();

const getJobsRoute = createRoute({
  method: "get",
  path: "/jobs",
  operationId: "getJobs", // Used for generated client method names
  tags: ["Jobs"], // Groups endpoints in documentation
  summary: "Get all jobs",
  description: "Retrieve active job postings with optional filters",
  request: {
    query: JobsQuerySchema,
  },
  responses: {
    200: {
      description: "List of jobs",
      content: { "application/json": { schema: JobsResponseSchema } },
    },
    500: {
      description: "Internal server error",
      content: { "application/json": { schema: ErrorResponseSchema } },
    },
  },
});

app.openapi(getJobsRoute, async (c) => {
  try {
    const { country, employment_type } = c.req.valid("query");
    const conditions = [eq(jobs.isActive, true), isNull(jobs.deletedAt)];

    if (country) {
      conditions.push(eq(jobs.country, country));
    }

    const results = await db
      .select()
      .from(jobs)
      .where(and(...conditions))
      .orderBy(desc(jobs.createdAt))
      .limit(DEFAULT_QUERY_LIMIT);

    return c.json({ jobs: results, total: results.length }, 200);
  } catch (error) {
    console.error("Error fetching jobs:", error);
    return c.json(
      {
        error: "Failed to fetch jobs",
        message: error instanceof Error ? error.message : "Unknown error",
      },
      500,
    );
  }
});

// Named export (project convention - no default exports)
export { app as jobsRoutes };
```

**Why good:** operationId becomes client method name (getJobs vs get_api_jobs), c.req.valid() enforces schema validation, soft delete checks prevent exposing deleted data

---

### Pattern 4: Standardized Error Handling

Consistent error responses with named error codes across all routes.

```typescript
import { z } from "zod";
import type { Context } from "hono";

const HTTP_STATUS_UNPROCESSABLE_ENTITY = 422;
const HTTP_STATUS_CONFLICT = 409;
const HTTP_STATUS_INTERNAL_ERROR = 500;

export const ErrorCodes = {
  VALIDATION_ERROR: "validation_error",
  NOT_FOUND: "not_found",
  UNAUTHORIZED: "unauthorized",
  FORBIDDEN: "forbidden",
  INTERNAL_ERROR: "internal_error",
  DATABASE_ERROR: "database_error",
} as const;

export const handleRouteError = (error: unknown, c: Context) => {
  console.error("Route error:", error);

  if (error instanceof z.ZodError) {
    return c.json(
      {
        error: ErrorCodes.VALIDATION_ERROR,
        message: "Validation failed",
        statusCode: HTTP_STATUS_UNPROCESSABLE_ENTITY,
        details: error.errors,
      },
      HTTP_STATUS_UNPROCESSABLE_ENTITY,
    );
  }

  if (error instanceof Error) {
    if (error.message.includes("unique constraint")) {
      return c.json(
        {
          error: ErrorCodes.VALIDATION_ERROR,
          message: "Resource already exists",
          statusCode: HTTP_STATUS_CONFLICT,
        },
        HTTP_STATUS_CONFLICT,
      );
    }

    return c.json(
      {
        error: ErrorCodes.INTERNAL_ERROR,
        message: error.message,
        statusCode: HTTP_STATUS_INTERNAL_ERROR,
      },
      HTTP_STATUS_INTERNAL_ERROR,
    );
  }

  return c.json(
    {
      error: ErrorCodes.INTERNAL_ERROR,
      message: "An unexpected error occurred",
      statusCode: HTTP_STATUS_INTERNAL_ERROR,
    },
    HTTP_STATUS_INTERNAL_ERROR,
  );
};
```

**Why good:** Named error codes enable frontend handling (switch on code), Zod error details show which field failed, consistent shape = predictable client parsing

</patterns>

---

<critical_reminders>

## CRITICAL REMINDERS

**Before you implement ANY Hono API route, verify these requirements are met:**

> **All code must follow project conventions in CLAUDE.md**

**(You MUST call `extendZodWithOpenApi(z)` BEFORE defining ANY Zod schemas)**

**(You MUST export the `app` instance for OpenAPI spec generation)**

**(You MUST include `operationId` in every route for clean client generation)**

**Failure to follow these rules will break OpenAPI spec generation.**

</critical_reminders>
