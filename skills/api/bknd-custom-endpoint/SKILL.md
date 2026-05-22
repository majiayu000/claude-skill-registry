---
name: bknd-custom-endpoint
description: Use when creating custom API endpoints in Bknd. Covers HTTP triggers with Flows, plugin routes via onServerInit, request/response handling, sync vs async modes, accessing request data, and returning custom responses.
---

# Custom Endpoint

Create custom API endpoints beyond Bknd's auto-generated CRUD routes.

## Prerequisites

- Running Bknd instance
- Basic understanding of HTTP methods and REST APIs
- Familiarity with TypeScript/JavaScript

## When to Use UI Mode

Custom endpoints require code configuration. No UI approach available.

## When to Use Code Mode

- Creating webhooks for external services
- Building custom business logic endpoints
- Adding endpoints that combine multiple operations
- Integrating with third-party APIs
- Creating public endpoints without entity CRUD

## Two Approaches

Bknd offers two ways to create custom endpoints:

| Approach | Best For | Complexity |
|----------|----------|------------|
| **Flows + HTTP Triggers** | Business logic, webhooks, multi-step processes | Medium |
| **Plugin Routes** | Simple endpoints, middleware, direct Hono access | Low |

## Approach 1: Flows with HTTP Triggers

### Step 1: Create a Basic Flow Endpoint

```typescript
import { App, Flow, HttpTrigger, LogTask } from "bknd";

// Define a flow with tasks
const helloFlow = new Flow("hello-endpoint", [
  new LogTask("log", { message: "Hello endpoint called!" }),
]);

// Attach HTTP trigger
helloFlow.setTrigger(
  new HttpTrigger({
    path: "/api/custom/hello",
    method: "GET",
  })
);

// Register in app config
const app = new App({
  flows: {
    flows: [helloFlow],
  },
});
```

**Test:**

```bash
curl http://localhost:7654/api/custom/hello
# Returns: { "success": true }
```

### Step 2: Create Endpoint with Response

Use `setRespondingTask()` to return data from a specific task:

```typescript
import { App, Flow, HttpTrigger, FetchTask } from "bknd";

const fetchTask = new FetchTask("fetch-data", {
  url: "https://api.example.com/data",
  method: "GET",
});

const apiFlow = new Flow("external-api", [fetchTask]);

// This task's output becomes the response
apiFlow.setRespondingTask(fetchTask);

apiFlow.setTrigger(
  new HttpTrigger({
    path: "/api/custom/external",
    method: "GET",
    response_type: "json",  // "json" | "text" | "html"
  })
);
```

### Step 3: Handle POST with Request Body

Access request data in tasks:

```typescript
import { App, Flow, HttpTrigger, Task } from "bknd";
import { s } from "bknd/utils";

// Custom task to process request
class ProcessTask extends Task<typeof ProcessTask.schema> {
  override type = "process";

  static override schema = s.strictObject({
    // Define expected params (can use template syntax)
  });

  override async execute(input: Request) {
    // input is the raw Request object
    const body = await input.json();

    return {
      received: body,
      processed: true,
      timestamp: new Date().toISOString(),
    };
  }
}

const processTask = new ProcessTask("process-input", {});

const postFlow = new Flow("process-data", [processTask]);
postFlow.setRespondingTask(processTask);

postFlow.setTrigger(
  new HttpTrigger({
    path: "/api/custom/process",
    method: "POST",
    response_type: "json",
  })
);
```

**Test:**

```bash
curl -X POST http://localhost:7654/api/custom/process \
  -H "Content-Type: application/json" \
  -d '{"name": "test", "value": 42}'
```

### Step 4: Sync vs Async Mode

```typescript
// Sync (default): Wait for flow completion, return result
new HttpTrigger({
  path: "/api/custom/sync",
  method: "POST",
  mode: "sync",  // Wait for completion
});

// Async: Return immediately, process in background
new HttpTrigger({
  path: "/api/custom/async",
  method: "POST",
  mode: "async",  // Fire and forget
});
// Returns: { "success": true } immediately
```

**Use async for:**
- Long-running operations
- Webhook receivers
- Background jobs

### Step 5: Multi-Task Flow with Connections

```typescript
import { Flow, HttpTrigger, FetchTask, LogTask, Condition } from "bknd";

const validateTask = new FetchTask("validate", {
  url: "https://api.example.com/validate",
  method: "POST",
});

const successTask = new LogTask("success", {
  message: "Validation passed!",
});

const failTask = new LogTask("fail", {
  message: "Validation failed!",
});

const flow = new Flow("validation-flow", [
  validateTask,
  successTask,
  failTask,
]);

// Connect tasks with conditions
flow.task(validateTask)
  .asInputFor(successTask, Condition.success())
  .asInputFor(failTask, Condition.error());

flow.setRespondingTask(successTask);

flow.setTrigger(
  new HttpTrigger({
    path: "/api/custom/validate",
    method: "POST",
  })
);
```

### HTTP Trigger Options Reference

```typescript
type HttpTriggerOptions = {
  path: string;           // URL path (must start with /)
  method?: string;        // "GET" | "POST" | "PUT" | "PATCH" | "DELETE"
  response_type?: string; // "json" | "text" | "html" (default: "json")
  mode?: string;          // "sync" | "async" (default: "sync")
};
```

## Approach 2: Plugin Routes (Direct Hono)

For simpler endpoints, use plugins with `onServerInit`:

### Step 1: Create Plugin with Routes

```typescript
import { App, createPlugin } from "bknd";
import type { Hono } from "hono";

const customRoutes = createPlugin({
  name: "custom-routes",

  onServerInit: (server: Hono) => {
    // Simple GET endpoint
    server.get("/api/custom/status", (c) => {
      return c.json({ status: "ok", timestamp: Date.now() });
    });

    // POST endpoint with body
    server.post("/api/custom/echo", async (c) => {
      const body = await c.req.json();
      return c.json({ echo: body });
    });

    // With path parameters
    server.get("/api/custom/users/:id", (c) => {
      const id = c.req.param("id");
      return c.json({ userId: id });
    });

    // With query parameters
    server.get("/api/custom/search", (c) => {
      const query = c.req.query("q");
      const limit = c.req.query("limit") || "10";
      return c.json({ query, limit: parseInt(limit) });
    });
  },
});

const app = new App({
  plugins: [customRoutes],
});
```

### Step 2: Access App Context in Plugin Routes

```typescript
import { App, createPlugin } from "bknd";

const apiPlugin = createPlugin({
  name: "api-plugin",

  onServerInit: (server, { app }) => {
    server.get("/api/custom/posts-count", async (c) => {
      // Access data API
      const em = app.modules.data?.em;
      if (!em) {
        return c.json({ error: "Data module not available" }, 500);
      }

      const count = await em.repo("posts").count();
      return c.json({ count });
    });

    server.post("/api/custom/create-post", async (c) => {
      const body = await c.req.json();
      const em = app.modules.data?.em;

      const post = await em.repo("posts").insertOne({
        title: body.title,
        content: body.content,
      });

      return c.json({ created: post }, 201);
    });
  },
});
```

### Step 3: Protected Plugin Routes

```typescript
import { createPlugin } from "bknd";

const protectedPlugin = createPlugin({
  name: "protected-routes",

  onServerInit: (server, { app }) => {
    // Middleware for auth check
    const requireAuth = async (c, next) => {
      const auth = app.modules.auth;
      const user = await auth?.authenticator?.verify(c.req.raw);

      if (!user) {
        return c.json({ error: "Unauthorized" }, 401);
      }

      c.set("user", user);
      return next();
    };

    // Protected endpoint
    server.get("/api/custom/profile", requireAuth, (c) => {
      const user = c.get("user");
      return c.json({ user });
    });

    // Admin-only endpoint
    server.delete("/api/custom/admin/clear-cache", requireAuth, async (c) => {
      const user = c.get("user");

      if (user.role !== "admin") {
        return c.json({ error: "Forbidden" }, 403);
      }

      // Clear cache logic...
      return c.json({ cleared: true });
    });
  },
});
```

### Step 4: Plugin with Sub-Router

```typescript
import { createPlugin } from "bknd";
import { Hono } from "hono";

const webhooksPlugin = createPlugin({
  name: "webhooks",

  onServerInit: (server) => {
    const webhooks = new Hono();

    webhooks.post("/stripe", async (c) => {
      const payload = await c.req.text();
      const sig = c.req.header("stripe-signature");
      // Verify and process Stripe webhook...
      return c.json({ received: true });
    });

    webhooks.post("/github", async (c) => {
      const event = c.req.header("x-github-event");
      const body = await c.req.json();
      // Process GitHub webhook...
      return c.json({ received: true });
    });

    // Mount sub-router
    server.route("/api/webhooks", webhooks);
  },
});
```

## Accessing Request Data

### In Flow Tasks (via input)

```typescript
class MyTask extends Task {
  async execute(input: Request) {
    // Body
    const json = await input.json();
    const text = await input.text();
    const form = await input.formData();

    // Headers
    const auth = input.headers.get("authorization");
    const contentType = input.headers.get("content-type");

    // URL info
    const url = new URL(input.url);
    const searchParams = url.searchParams;

    return { processed: true };
  }
}
```

### In Plugin Routes (via Hono context)

```typescript
server.post("/api/custom/upload", async (c) => {
  // Body
  const json = await c.req.json();
  const text = await c.req.text();
  const form = await c.req.formData();

  // Headers
  const auth = c.req.header("authorization");

  // Query params
  const format = c.req.query("format");

  // Path params (if route has :param)
  const id = c.req.param("id");

  // Raw request
  const raw = c.req.raw;

  return c.json({ received: true });
});
```

## Response Patterns

### In Plugin Routes

```typescript
server.get("/api/custom/demo", (c) => {
  // JSON response
  return c.json({ data: "value" });

  // JSON with status
  return c.json({ error: "Not found" }, 404);

  // Text response
  return c.text("Hello, World!");

  // HTML response
  return c.html("<h1>Hello</h1>");

  // Redirect
  return c.redirect("/other-path");

  // Custom response
  return new Response(body, {
    status: 200,
    headers: { "X-Custom": "header" },
  });
});
```

## Complete Example: Webhook Receiver

```typescript
import { App, createPlugin, Flow, HttpTrigger, Task } from "bknd";
import { s } from "bknd/utils";

// Option 1: Using Flows
class WebhookTask extends Task<typeof WebhookTask.schema> {
  override type = "webhook-processor";
  static override schema = s.strictObject({});

  override async execute(input: Request) {
    const event = input.headers.get("x-webhook-event");
    const body = await input.json();

    // Process webhook based on event type
    switch (event) {
      case "user.created":
        console.log("New user:", body.user);
        break;
      case "order.completed":
        console.log("Order completed:", body.order);
        break;
    }

    return { processed: true, event };
  }
}

const webhookFlow = new Flow("webhook-handler", [
  new WebhookTask("process", {}),
]);
webhookFlow.setRespondingTask(webhookFlow.tasks[0]);
webhookFlow.setTrigger(
  new HttpTrigger({
    path: "/api/webhooks/external",
    method: "POST",
    mode: "async",  // Return immediately
  })
);

// Option 2: Using Plugin (simpler)
const webhookPlugin = createPlugin({
  name: "webhook-handler",
  onServerInit: (server) => {
    server.post("/api/webhooks/simple", async (c) => {
      const event = c.req.header("x-webhook-event");
      const body = await c.req.json();

      // Queue for background processing
      queueMicrotask(async () => {
        // Process webhook...
      });

      return c.json({ received: true });
    });
  },
});

const app = new App({
  flows: { flows: [webhookFlow] },
  plugins: [webhookPlugin],
});
```

## Listing Custom Endpoints

```bash
# List all registered routes including custom ones
bknd debug routes
```

## Common Pitfalls

### Flow Not Responding

**Problem:** Endpoint returns `{ success: true }` but no data

**Fix:** Set responding task:

```typescript
// WRONG - no response data
const flow = new Flow("my-flow", [task]);
flow.setTrigger(new HttpTrigger({ path: "/api/test" }));

// CORRECT - task output becomes response
const flow = new Flow("my-flow", [task]);
flow.setRespondingTask(task);  // Add this!
flow.setTrigger(new HttpTrigger({ path: "/api/test" }));
```

### Path Conflicts

**Problem:** Custom endpoint conflicts with built-in routes

**Fix:** Use unique path prefixes:

```typescript
// WRONG - conflicts with data API
new HttpTrigger({ path: "/api/data/custom" });

// CORRECT - unique namespace
new HttpTrigger({ path: "/api/custom/data" });
new HttpTrigger({ path: "/api/v1/custom" });
new HttpTrigger({ path: "/webhooks/stripe" });
```

### Missing Content-Type in Response

**Problem:** Client can't parse response

**Fix:** Use Hono's response helpers:

```typescript
// WRONG
return new Response(JSON.stringify(data));

// CORRECT
return c.json(data);  // Sets Content-Type automatically
```

### Async Mode Confusion

**Problem:** Expecting data from async endpoint

**Fix:** Understand async returns immediately:

```typescript
// Async mode - returns { success: true } immediately
new HttpTrigger({ path: "/api/job", mode: "async" });

// For data responses, use sync (default)
new HttpTrigger({ path: "/api/query", mode: "sync" });
```

### Plugin Not Loading

**Problem:** Custom routes return 404

**Fix:** Ensure plugin is registered:

```typescript
const app = new App({
  plugins: [myPlugin],  // Must include plugin here
});
```

## DOs and DON'Ts

**DO:**
- Use Flows for complex multi-step operations
- Use plugins for simple CRUD-style endpoints
- Set `mode: "async"` for webhooks and long operations
- Use unique path prefixes (`/api/custom/`, `/webhooks/`)
- Call `setRespondingTask()` when you need response data
- Validate request bodies before processing

**DON'T:**
- Conflict with built-in paths (`/api/data/`, `/api/auth/`)
- Forget to register flows/plugins in App config
- Use sync mode for long-running operations
- Return raw Response without Content-Type
- Expose sensitive operations without auth checks

## Related Skills

- **bknd-api-discovery** - Explore auto-generated endpoints
- **bknd-webhooks** - Configure webhook integrations
- **bknd-protect-endpoint** - Secure custom endpoints
- **bknd-client-setup** - Call custom endpoints from frontend
