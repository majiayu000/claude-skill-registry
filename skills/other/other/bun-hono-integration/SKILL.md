---
name: Bun Hono Integration
description: Use when building APIs with Hono framework on Bun, including routing, middleware, REST APIs, context handling, or web framework features.
version: 1.0.0
---

# Bun Hono Integration

Hono is a fast, lightweight web framework optimized for Bun.

## Quick Start

```bash
bun create hono my-app
cd my-app
bun install
bun run dev
```

## Basic Setup

```typescript
import { Hono } from "hono";

const app = new Hono();

app.get("/", (c) => c.text("Hello Hono!"));

app.get("/json", (c) => c.json({ message: "Hello" }));

export default app;
```

## Routing

```typescript
import { Hono } from "hono";

const app = new Hono();

// HTTP methods
app.get("/users", (c) => c.json([]));
app.post("/users", (c) => c.json({ created: true }));
app.put("/users/:id", (c) => c.json({ updated: true }));
app.delete("/users/:id", (c) => c.json({ deleted: true }));

// All methods
app.all("/any", (c) => c.text("Any method"));

// Path parameters
app.get("/users/:id", (c) => {
  const id = c.req.param("id");
  return c.json({ id });
});

// Multiple parameters
app.get("/posts/:postId/comments/:commentId", (c) => {
  const { postId, commentId } = c.req.param();
  return c.json({ postId, commentId });
});

// Wildcards
app.get("/files/*", (c) => {
  const path = c.req.path;
  return c.text(`File: ${path}`);
});

// Regex-like patterns
app.get("/user/:id{[0-9]+}", (c) => c.json({ id: c.req.param("id") }));

export default app;
```

## Route Groups

```typescript
import { Hono } from "hono";

const app = new Hono();

// Group routes
const api = new Hono();
api.get("/users", (c) => c.json([]));
api.get("/posts", (c) => c.json([]));

app.route("/api/v1", api);

// Basepath
const app2 = new Hono().basePath("/api/v2");
app2.get("/users", (c) => c.json([])); // /api/v2/users

export default app;
```

## Request Handling

```typescript
app.post("/submit", async (c) => {
  // URL and method
  console.log(c.req.url);
  console.log(c.req.method);

  // Headers
  const auth = c.req.header("Authorization");

  // Query params
  const page = c.req.query("page");
  const { limit, offset } = c.req.query();

  // Body parsing
  const json = await c.req.json();
  const text = await c.req.text();
  const form = await c.req.formData();
  const arrayBuffer = await c.req.arrayBuffer();

  // Parsed body (with validator)
  const body = c.req.valid("json");

  return c.json({ received: true });
});
```

## Response Types

```typescript
app.get("/responses", (c) => {
  // Text
  return c.text("Hello");

  // JSON
  return c.json({ data: "value" });

  // HTML
  return c.html("<h1>Hello</h1>");

  // Redirect
  return c.redirect("/other", 302);

  // Not Found
  return c.notFound();

  // Custom response
  return c.body("Raw body", 200, {
    "Content-Type": "text/plain",
  });

  // Status
  return c.json({ error: "Not found" }, 404);

  // Headers
  c.header("X-Custom", "value");
  return c.json({ ok: true });
});
```

## Middleware

```typescript
import { Hono } from "hono";

const app = new Hono();

// Global middleware
app.use("*", async (c, next) => {
  console.log(`${c.req.method} ${c.req.url}`);
  await next();
});

// Path-specific middleware
app.use("/api/*", async (c, next) => {
  const auth = c.req.header("Authorization");
  if (!auth) {
    return c.json({ error: "Unauthorized" }, 401);
  }
  await next();
});

// Multiple middleware
app.use("/admin/*", authMiddleware, adminMiddleware);

app.get("/api/data", (c) => c.json({ data: "protected" }));

export default app;
```

## Built-in Middleware

```typescript
import { Hono } from "hono";
import { cors } from "hono/cors";
import { logger } from "hono/logger";
import { basicAuth } from "hono/basic-auth";
import { bearerAuth } from "hono/bearer-auth";
import { compress } from "hono/compress";
import { etag } from "hono/etag";
import { secureHeaders } from "hono/secure-headers";

const app = new Hono();

// CORS
app.use("*", cors());
app.use("/api/*", cors({
  origin: "https://example.com",
  allowMethods: ["GET", "POST"],
}));

// Logger
app.use("*", logger());

// Basic Auth
app.use("/admin/*", basicAuth({
  username: "admin",
  password: "secret",
}));

// Bearer Token
app.use("/api/*", bearerAuth({
  token: "my-token",
}));

// Compression
app.use("*", compress());

// ETag
app.use("*", etag());

// Security headers
app.use("*", secureHeaders());

export default app;
```

## Validation with Zod

```typescript
import { Hono } from "hono";
import { zValidator } from "@hono/zod-validator";
import { z } from "zod";

const app = new Hono();

const userSchema = z.object({
  name: z.string().min(1),
  email: z.string().email(),
  age: z.number().min(0).optional(),
});

app.post(
  "/users",
  zValidator("json", userSchema),
  (c) => {
    const user = c.req.valid("json");
    // user is typed and validated
    return c.json({ created: user });
  }
);

// Query validation
const querySchema = z.object({
  page: z.string().regex(/^\d+$/).optional(),
  limit: z.string().regex(/^\d+$/).optional(),
});

app.get(
  "/items",
  zValidator("query", querySchema),
  (c) => {
    const { page, limit } = c.req.valid("query");
    return c.json({ page, limit });
  }
);

export default app;
```

## Context Variables

```typescript
import { Hono } from "hono";

type Variables = {
  userId: string;
  isAdmin: boolean;
};

const app = new Hono<{ Variables: Variables }>();

app.use("*", async (c, next) => {
  c.set("userId", "123");
  c.set("isAdmin", true);
  await next();
});

app.get("/profile", (c) => {
  const userId = c.get("userId");
  const isAdmin = c.get("isAdmin");
  return c.json({ userId, isAdmin });
});

export default app;
```

## Error Handling

```typescript
import { Hono } from "hono";
import { HTTPException } from "hono/http-exception";

const app = new Hono();

// Throw HTTP error
app.get("/error", (c) => {
  throw new HTTPException(401, { message: "Unauthorized" });
});

// Global error handler
app.onError((err, c) => {
  if (err instanceof HTTPException) {
    return err.getResponse();
  }
  console.error(err);
  return c.json({ error: "Internal Server Error" }, 500);
});

// Not found handler
app.notFound((c) => {
  return c.json({ error: "Not Found" }, 404);
});

export default app;
```

## RPC Mode (Type-safe Client)

```typescript
// server.ts
import { Hono } from "hono";
import { hc } from "hono/client";

const app = new Hono()
  .get("/users", (c) => c.json([{ id: 1, name: "Alice" }]))
  .post("/users", async (c) => {
    const body = await c.req.json();
    return c.json({ created: body });
  });

export type AppType = typeof app;
export default app;

// client.ts
import { hc } from "hono/client";
import type { AppType } from "./server";

const client = hc<AppType>("http://localhost:3000");

// Type-safe calls
const res = await client.users.$get();
const users = await res.json(); // Typed!

const created = await client.users.$post({
  json: { name: "Bob" },
});
```

## Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `Route not found` | Wrong path | Check route registration |
| `Body already read` | Double parsing | Read body once |
| `Validator error` | Invalid input | Check schema definition |
| `Middleware order` | Wrong execution | Register middleware first |

## When to Load References

Load `references/middleware-list.md` when:
- Complete middleware reference
- Custom middleware patterns

Load `references/openapi.md` when:
- OpenAPI/Swagger integration
- API documentation generation
