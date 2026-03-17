---
name: hono
description: >-
  Build type-safe REST APIs with Hono framework in FTC Metrics.
  Use when creating API routes, implementing middleware, handling authentication,
  configuring CORS, or working with packages/api.
license: MIT
compatibility: [Claude Code]
metadata:
  author: ftcmetrics
  version: "1.0.0"
  category: api
---

# Hono API Framework Guide

Hono is a lightweight, ultrafast web framework for building APIs. FTC Metrics uses Hono with Node.js adapter for the backend API.

## Quick Start

### Main App Setup

```typescript
// packages/api/src/index.ts
import { serve } from "@hono/node-server";
import { Hono } from "hono";
import { cors } from "hono/cors";
import { logger } from "hono/logger";

const app = new Hono();

// Global middleware
app.use("*", logger());
app.use("*", cors({
  origin: process.env.CORS_ORIGIN || "http://localhost:3000",
  credentials: true,
}));

// Health check
app.get("/", (c) => c.json({ status: "ok" }));

// Mount routes
app.route("/api/events", eventsRouter);
app.route("/api/teams", teamsRouter);

// Start server
serve({ fetch: app.fetch, port: 3001 });
```

## Route Definition Patterns

### Basic Route Handler

```typescript
import { Hono } from "hono";

const router = new Hono();

// GET with path parameter
router.get("/:id", async (c) => {
  const id = c.req.param("id");
  return c.json({ success: true, data: { id } });
});

// GET with query parameters
router.get("/", async (c) => {
  const page = c.req.query("page") || "1";
  const limit = c.req.query("limit") || "10";
  return c.json({ success: true, data: [], page, limit });
});

// POST with JSON body
router.post("/", async (c) => {
  const body = await c.req.json();
  const { name, value } = body;

  if (!name) {
    return c.json({ success: false, error: "Name required" }, 400);
  }

  return c.json({ success: true, data: { name, value } });
});

// PATCH for updates
router.patch("/:id", async (c) => {
  const id = c.req.param("id");
  const body = await c.req.json();
  return c.json({ success: true, data: { id, ...body } });
});

// DELETE
router.delete("/:id", async (c) => {
  const id = c.req.param("id");
  return c.json({ success: true });
});

export default router;
```

### Nested Routes

```typescript
// Route with sub-resources
router.get("/:teamId/members", async (c) => {
  const teamId = c.req.param("teamId");
  // Fetch members for team
  return c.json({ success: true, data: members });
});

router.post("/:teamId/members", async (c) => {
  const teamId = c.req.param("teamId");
  const body = await c.req.json();
  // Add member to team
  return c.json({ success: true, data: newMember });
});
```

## Response Patterns

### Standard Success Response

```typescript
return c.json({
  success: true,
  data: result,
});
```

### Error Responses

```typescript
// 400 Bad Request
return c.json({ success: false, error: "Invalid input" }, 400);

// 401 Unauthorized
return c.json({ success: false, error: "Authentication required" }, 401);

// 403 Forbidden
return c.json({ success: false, error: "Permission denied" }, 403);

// 404 Not Found
return c.json({ success: false, error: "Resource not found" }, 404);

// 409 Conflict
return c.json({ success: false, error: "Resource already exists" }, 409);

// 500 Internal Server Error
return c.json({ success: false, error: "Internal server error" }, 500);
```

### Empty Results

```typescript
if (results.length === 0) {
  return c.json({
    success: true,
    data: {
      items: [],
      count: 0,
    },
  });
}
```

## Middleware Patterns

### Authentication Middleware

```typescript
import { Context, Next } from "hono";
import { prisma } from "@ftcmetrics/db";

export async function authMiddleware(c: Context, next: Next) {
  const userId = c.req.header("X-User-Id");

  if (!userId) {
    return c.json({ success: false, error: "Authentication required" }, 401);
  }

  try {
    const user = await prisma.user.findUnique({
      where: { id: userId },
      select: { id: true, name: true, email: true },
    });

    if (!user) {
      return c.json({ success: false, error: "Invalid user" }, 401);
    }

    // Attach user to context
    c.set("user", user);
    c.set("userId", userId);

    await next();
  } catch (error) {
    console.error("Auth middleware error:", error);
    return c.json({ success: false, error: "Authentication failed" }, 500);
  }
}
```

### Role-Based Access Control

```typescript
export function requireTeamMembership(paramName: string = "teamId") {
  return async (c: Context, next: Next) => {
    const userId = c.get("userId");
    const teamId = c.req.param(paramName);

    if (!userId) {
      return c.json({ success: false, error: "Authentication required" }, 401);
    }

    const membership = await prisma.teamMember.findUnique({
      where: { userId_teamId: { userId, teamId } },
    });

    if (!membership) {
      return c.json({ success: false, error: "Not a team member" }, 403);
    }

    c.set("membership", membership);
    c.set("teamRole", membership.role);

    await next();
  };
}

export async function requireMentorRole(c: Context, next: Next) {
  const role = c.get("teamRole");

  if (role !== "MENTOR") {
    return c.json({ success: false, error: "Mentor access required" }, 403);
  }

  await next();
}
```

### Rate Limiting

```typescript
const rateLimitStore = new Map<string, { count: number; resetAt: number }>();

export function rateLimit(maxRequests: number = 100, windowMs: number = 60000) {
  return async (c: Context, next: Next) => {
    const identifier = c.req.header("X-User-Id") ||
                       c.req.header("X-Forwarded-For") ||
                       "anonymous";
    const now = Date.now();
    const key = `${identifier}:${c.req.path}`;

    const entry = rateLimitStore.get(key);

    if (!entry || now > entry.resetAt) {
      rateLimitStore.set(key, { count: 1, resetAt: now + windowMs });
    } else if (entry.count >= maxRequests) {
      return c.json({
        success: false,
        error: "Rate limit exceeded",
        retryAfter: Math.ceil((entry.resetAt - now) / 1000),
      }, 429);
    } else {
      entry.count++;
    }

    await next();
  };
}
```

## Applying Middleware

### Global Middleware

```typescript
// Apply to all routes
app.use("*", logger());
app.use("*", cors({ origin: "http://localhost:3000", credentials: true }));

// Apply to API routes only
app.use("/api/*", rateLimit(100, 60000));
app.use("/api/*", sanitizeInput);
```

### Route-Specific Middleware

```typescript
// Single middleware
router.get("/protected", authMiddleware, async (c) => {
  const user = c.get("user");
  return c.json({ success: true, data: user });
});

// Chained middleware
router.patch(
  "/:teamId",
  authMiddleware,
  requireTeamMembership("teamId"),
  requireMentorRole,
  async (c) => {
    // Only mentors reach here
    const teamId = c.req.param("teamId");
    return c.json({ success: true });
  }
);
```

## Error Handling

### Try-Catch Pattern

```typescript
router.get("/:id", async (c) => {
  const id = c.req.param("id");

  try {
    const result = await prisma.item.findUnique({ where: { id } });

    if (!result) {
      return c.json({ success: false, error: "Not found" }, 404);
    }

    return c.json({ success: true, data: result });
  } catch (error) {
    console.error("Error fetching item:", error);
    return c.json({ success: false, error: "Failed to fetch item" }, 500);
  }
});
```

### Validation

```typescript
router.post("/", async (c) => {
  try {
    const body = await c.req.json();
    const { teamNumber, name } = body;

    // Type validation
    if (!teamNumber || typeof teamNumber !== "number") {
      return c.json({ success: false, error: "Team number required" }, 400);
    }

    // Range validation
    if (teamNumber < 1 || teamNumber > 99999) {
      return c.json({ success: false, error: "Invalid team number" }, 400);
    }

    // Parse numeric params
    const parsed = parseInt(c.req.param("id"), 10);
    if (isNaN(parsed)) {
      return c.json({ success: false, error: "Invalid ID" }, 400);
    }

    // Continue with valid data
    return c.json({ success: true });
  } catch (error) {
    return c.json({ success: false, error: "Invalid request body" }, 400);
  }
});
```

## Project Structure

```
packages/api/
  src/
    index.ts              # Main app, server startup
    routes/
      analytics.ts        # /api/analytics routes
      events.ts           # /api/events routes
      scouting.ts         # /api/scouting routes
      teams.ts            # /api/teams routes (FTC API)
      user-teams.ts       # /api/user-teams routes (app teams)
    middleware/
      auth.ts             # Auth, rate limit, sanitization
    lib/
      ftc-api.ts          # FTC Events API client
      stats/              # Analytics calculations
```

## Common Patterns

### Parallel API Calls

```typescript
const [matches, scores] = await Promise.all([
  api.getMatches(eventCode),
  api.getScores(eventCode),
]);
```

### Query String Parsing

```typescript
// Parse array from comma-separated string
const teams = c.req.query("teams")?.split(",").map(Number);
if (!teams || teams.some(isNaN)) {
  return c.json({ success: false, error: "Invalid teams" }, 400);
}

// Parse enum/limited values
const level = c.req.query("level") === "playoff" ? "playoff" : "qual";
```

### Dynamic Prisma Filters

```typescript
const where: Record<string, unknown> = {};

if (eventCode) {
  where.eventCode = eventCode;
}

if (teamNumber) {
  where.scoutedTeam = { teamNumber: parseInt(teamNumber, 10) };
}

const results = await prisma.scoutingEntry.findMany({ where });
```

## Anti-Patterns

- Do not use `app.all()` for specific routes
- Do not forget error handling in async routes
- Do not mutate context variables directly
- Do not hardcode status codes in response bodies
- Do not skip authentication checks on protected routes
- Do not return sensitive data without filtering

## References

- [Hono Documentation](https://hono.dev/)
- [Hono Node.js Adapter](https://hono.dev/docs/getting-started/nodejs)
- [Hono Middleware](https://hono.dev/docs/middleware/builtin)
