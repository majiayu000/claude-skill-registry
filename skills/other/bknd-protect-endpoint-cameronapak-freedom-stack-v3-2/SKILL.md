---
name: bknd-protect-endpoint
description: Use when securing specific API endpoints in Bknd. Covers protecting custom HTTP triggers, plugin routes, auth middleware for Flows, checking permissions in custom endpoints, and role-based endpoint access.
---

# Protect Endpoint

Secure specific API endpoints with authentication and authorization checks.

## Prerequisites

- Bknd project with code-first configuration
- Auth enabled (`auth: { enabled: true }`)
- Guard enabled for authorization (`guard: { enabled: true }`)
- Roles defined (see **bknd-create-role**)

## When to Use UI Mode

- Viewing registered routes: Admin Panel > System > Debug
- Inspecting role permissions

**Note:** Endpoint protection requires code mode. UI is read-only.

## When to Use Code Mode

- Creating protected custom endpoints
- Adding auth checks to HTTP triggers
- Building protected plugin routes
- Implementing endpoint-specific permissions

## Code Approach

### Understanding Endpoint Types

Bknd has several endpoint types to protect:

| Type | Path Pattern | How to Protect |
|------|--------------|----------------|
| Data API | `/api/data/*` | Guard permissions (automatic) |
| Auth API | `/api/auth/*` | Built-in protection |
| Media API | `/api/media/*` | Guard permissions (automatic) |
| HTTP Triggers | Custom paths | Manual auth check |
| Plugin Routes | Custom paths | Manual auth check |

### Step 1: Protect HTTP Trigger (Flow)

Add authentication to a custom endpoint via FunctionTask:

```typescript
import { serve } from "bknd/adapter/bun";
import { Flow, HttpTrigger, FunctionTask } from "bknd";

// Protected endpoint flow
const protectedFlow = new Flow("protected-endpoint", [
  new FunctionTask({
    name: "checkAuth",
    handler: async (input, ctx) => {
      // ctx.app gives access to modules
      const authModule = ctx.app.modules.get("auth");
      const user = await authModule.authenticator.getUserFromRequest(input);

      if (!user) {
        throw new Response(JSON.stringify({ error: "Unauthorized" }), {
          status: 401,
          headers: { "Content-Type": "application/json" },
        });
      }

      // Pass user to next task
      return { user, body: await input.json() };
    },
  }),
  new FunctionTask({
    name: "processRequest",
    handler: async (input) => {
      // input contains { user, body } from previous task
      return {
        message: `Hello ${input.user.email}`,
        data: input.body,
      };
    },
  }),
]);

protectedFlow.setTrigger(
  new HttpTrigger({
    path: "/api/custom/protected",
    method: "POST",
    respondWith: "processRequest",
  })
);

serve({
  connection: { url: "file:data.db" },
  config: {
    flows: {
      flows: [protectedFlow],
    },
  },
});
```

### Step 2: Protect Plugin Route

Add auth check in plugin's `onServerInit`:

```typescript
import { serve } from "bknd/adapter/bun";
import { createPlugin } from "bknd";

const protectedPlugin = createPlugin({
  name: "protected-routes",

  onServerInit: (server) => {
    // Protected endpoint
    server.post("/api/custom/data", async (c) => {
      // Get app from context
      const app = c.get("app");
      const authModule = app.modules.get("auth");

      // Resolve user from request
      const user = await authModule.authenticator.getUserFromRequest(c.req.raw);

      if (!user) {
        return c.json({ error: "Unauthorized" }, 401);
      }

      // Proceed with protected logic
      const body = await c.req.json();
      return c.json({
        message: "Protected data",
        user: user.email,
        received: body,
      });
    });

    // Public endpoint (no auth check)
    server.get("/api/custom/public", (c) => {
      return c.json({ message: "Public data" });
    });
  },
});

serve({
  connection: { url: "file:data.db" },
  plugins: [protectedPlugin],
});
```

### Step 3: Role-Based Endpoint Protection

Check user's role for specific permissions:

```typescript
const roleProtectedPlugin = createPlugin({
  name: "role-protected",

  onServerInit: (server) => {
    // Admin-only endpoint
    server.delete("/api/admin/users/:id", async (c) => {
      const app = c.get("app");
      const authModule = app.modules.get("auth");
      const user = await authModule.authenticator.getUserFromRequest(c.req.raw);

      // Check authentication
      if (!user) {
        return c.json({ error: "Unauthorized" }, 401);
      }

      // Check role
      if (user.role !== "admin") {
        return c.json({ error: "Forbidden: Admin role required" }, 403);
      }

      // Proceed with admin action
      const userId = c.req.param("id");
      // ... delete user logic
      return c.json({ deleted: userId });
    });
  },
});
```

### Step 4: Permission-Based Protection with Guard

Use Guard for granular permission checks:

```typescript
import { createPlugin, DataPermissions } from "bknd";

const guardProtectedPlugin = createPlugin({
  name: "guard-protected",

  onServerInit: (server) => {
    server.post("/api/custom/sync", async (c) => {
      const app = c.get("app");
      const authModule = app.modules.get("auth");
      const guard = authModule.guard;

      const user = await authModule.authenticator.getUserFromRequest(c.req.raw);

      if (!user) {
        return c.json({ error: "Unauthorized" }, 401);
      }

      // Check specific permission using Guard
      try {
        guard.granted(
          DataPermissions.databaseSync,  // Permission to check
          { role: user.role },           // User context
          {}                             // Permission context
        );
      } catch (error) {
        return c.json({
          error: "Forbidden",
          message: error.message,
        }, 403);
      }

      // User has permission - proceed
      return c.json({ status: "sync started" });
    });
  },
});
```

### Step 5: Entity-Specific Permission Check

Check permissions for specific entity operations:

```typescript
server.post("/api/custom/posts/batch", async (c) => {
  const app = c.get("app");
  const authModule = app.modules.get("auth");
  const guard = authModule.guard;

  const user = await authModule.authenticator.getUserFromRequest(c.req.raw);

  if (!user) {
    return c.json({ error: "Unauthorized" }, 401);
  }

  // Check create permission for posts entity
  try {
    guard.granted(
      DataPermissions.entityCreate,
      { role: user.role },
      { entity: "posts" }  // Entity-specific context
    );
  } catch (error) {
    return c.json({
      error: "Cannot create posts",
      message: error.message,
    }, 403);
  }

  // Proceed with batch creation
  const body = await c.req.json();
  // ... create posts
  return c.json({ created: body.length });
});
```

### Step 6: Reusable Auth Middleware

Create a helper for consistent auth checks:

```typescript
// auth-middleware.ts
type AuthContext = {
  user: any;
  role: string;
};

export async function requireAuth(
  c: any,
  app: any
): Promise<AuthContext | Response> {
  const authModule = app.modules.get("auth");
  const user = await authModule.authenticator.getUserFromRequest(c.req.raw);

  if (!user) {
    return c.json({ error: "Unauthorized" }, 401);
  }

  return { user, role: user.role };
}

export async function requireRole(
  c: any,
  app: any,
  allowedRoles: string[]
): Promise<AuthContext | Response> {
  const result = await requireAuth(c, app);

  if (result instanceof Response) {
    return result;
  }

  if (!allowedRoles.includes(result.role)) {
    return c.json({
      error: "Forbidden",
      required: allowedRoles,
      current: result.role,
    }, 403);
  }

  return result;
}

// Usage in plugin
server.get("/api/reports/admin", async (c) => {
  const app = c.get("app");
  const auth = await requireRole(c, app, ["admin", "manager"]);

  if (auth instanceof Response) return auth;

  // auth.user available
  return c.json({ reports: [] });
});
```

### Step 7: Protecting Flow with Auth Task

Create reusable auth task for Flows:

```typescript
import { Flow, HttpTrigger, FunctionTask } from "bknd";

// Reusable auth task
const authTask = new FunctionTask({
  name: "requireAuth",
  handler: async (input, ctx) => {
    const authModule = ctx.app.modules.get("auth");
    const user = await authModule.authenticator.getUserFromRequest(input);

    if (!user) {
      throw new Response(
        JSON.stringify({ error: "Unauthorized" }),
        { status: 401, headers: { "Content-Type": "application/json" } }
      );
    }

    return { request: input, user };
  },
});

// Reusable role check task
const requireAdmin = new FunctionTask({
  name: "requireAdmin",
  handler: async (input) => {
    if (input.user.role !== "admin") {
      throw new Response(
        JSON.stringify({ error: "Admin required" }),
        { status: 403, headers: { "Content-Type": "application/json" } }
      );
    }
    return input;
  },
});

// Protected flow
const adminFlow = new Flow("admin-action", [
  authTask,
  requireAdmin,
  new FunctionTask({
    name: "performAction",
    handler: async (input) => {
      return { success: true, admin: input.user.email };
    },
  }),
]);

adminFlow.setTrigger(
  new HttpTrigger({
    path: "/api/admin/action",
    method: "POST",
    respondWith: "performAction",
  })
);
```

## Common Patterns

### Optional Auth (Public with Extra Features)

```typescript
server.get("/api/posts", async (c) => {
  const app = c.get("app");
  const authModule = app.modules.get("auth");
  const api = app.getApi();

  // Try to get user (may be null)
  const user = await authModule.authenticator.getUserFromRequest(c.req.raw);

  if (user) {
    // Authenticated: show all posts including drafts
    const posts = await api.data.readMany("posts", {
      where: {
        $or: [
          { status: "published" },
          { author_id: user.id },
        ],
      },
    });
    return c.json(posts.data);
  } else {
    // Anonymous: show only published
    const posts = await api.data.readMany("posts", {
      where: { status: "published" },
    });
    return c.json(posts.data);
  }
});
```

### Rate-Limited Protected Endpoint

```typescript
const rateLimits = new Map<string, { count: number; reset: number }>();

server.post("/api/expensive-operation", async (c) => {
  const app = c.get("app");
  const authModule = app.modules.get("auth");
  const user = await authModule.authenticator.getUserFromRequest(c.req.raw);

  if (!user) {
    return c.json({ error: "Unauthorized" }, 401);
  }

  // Simple rate limiting by user
  const key = `user:${user.id}`;
  const now = Date.now();
  const limit = rateLimits.get(key);

  if (limit && limit.reset > now && limit.count >= 10) {
    return c.json({
      error: "Rate limit exceeded",
      retryAfter: Math.ceil((limit.reset - now) / 1000),
    }, 429);
  }

  // Update rate limit
  if (!limit || limit.reset < now) {
    rateLimits.set(key, { count: 1, reset: now + 60000 });
  } else {
    limit.count++;
  }

  // Proceed
  return c.json({ result: "success" });
});
```

### API Key Authentication

For service-to-service or external API access:

```typescript
const API_KEYS = new Set([
  process.env.SERVICE_API_KEY,
  process.env.PARTNER_API_KEY,
]);

server.post("/api/webhook/external", async (c) => {
  const apiKey = c.req.header("X-API-Key");

  if (!apiKey || !API_KEYS.has(apiKey)) {
    return c.json({ error: "Invalid API key" }, 401);
  }

  // Proceed with webhook handling
  const body = await c.req.json();
  return c.json({ received: true });
});
```

## Verification

### 1. Test Unauthenticated Access

```bash
# Should return 401
curl -X POST http://localhost:7654/api/custom/protected \
  -H "Content-Type: application/json" \
  -d '{"test": "data"}'
```

### 2. Test Authenticated Access

```bash
# Login first
TOKEN=$(curl -s -X POST http://localhost:7654/api/auth/password/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@test.com", "password": "pass123"}' | jq -r '.token')

# Access protected endpoint
curl -X POST http://localhost:7654/api/custom/protected \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"test": "data"}'
```

### 3. Test Role Restriction

```bash
# Login as non-admin
TOKEN=$(curl -s -X POST http://localhost:7654/api/auth/password/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@test.com", "password": "pass123"}' | jq -r '.token')

# Should return 403
curl -X DELETE http://localhost:7654/api/admin/users/1 \
  -H "Authorization: Bearer $TOKEN"
```

### 4. Verify with Admin Role

```bash
# Login as admin
ADMIN_TOKEN=$(curl -s -X POST http://localhost:7654/api/auth/password/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@test.com", "password": "admin123"}' | jq -r '.token')

# Should succeed
curl -X DELETE http://localhost:7654/api/admin/users/1 \
  -H "Authorization: Bearer $ADMIN_TOKEN"
```

## Common Pitfalls

### User Always Null

**Problem:** `getUserFromRequest()` returns null even with valid token

**Fix:** Ensure token is sent correctly:

```typescript
// Header auth
fetch("/api/custom/protected", {
  headers: { "Authorization": `Bearer ${token}` }
});

// OR cookie auth (if using cookies)
fetch("/api/custom/protected", {
  credentials: "include"  // Send cookies
});
```

### Guard Not Available

**Problem:** `authModule.guard` is undefined

**Fix:** Ensure guard is enabled:

```typescript
{
  auth: {
    enabled: true,
    guard: { enabled: true },  // Required!
  },
}
```

### Permission Check Throws Wrong Error

**Problem:** Guard throws unexpected error type

**Fix:** Catch specific exception:

```typescript
import { GuardPermissionsException } from "bknd";

try {
  guard.granted(permission, context, permContext);
} catch (error) {
  if (error instanceof GuardPermissionsException) {
    return c.json({ error: error.message }, 403);
  }
  throw error;  // Re-throw unexpected errors
}
```

### CORS Blocking Auth Header

**Problem:** Preflight fails for Authorization header

**Fix:** Configure CORS:

```typescript
serve({
  // ...
  config: {
    server: {
      cors: {
        origin: ["http://localhost:3000"],
        credentials: true,
        allowHeaders: ["Authorization", "Content-Type"],
      },
    },
  },
});
```

### Flow Task Doesn't Have App Context

**Problem:** `ctx.app` undefined in FunctionTask

**Fix:** Access via execution context:

```typescript
new FunctionTask({
  name: "withApp",
  handler: async (input, ctx) => {
    // ctx.app is available in FunctionTask
    const app = ctx.app;
    // ...
  },
});
```

## DOs and DON'Ts

**DO:**
- Always check auth before processing sensitive requests
- Use Guard for permission checks (consistent with Bknd's system)
- Return appropriate HTTP status codes (401, 403)
- Create reusable auth helpers for consistency
- Log auth failures for security monitoring

**DON'T:**
- Trust client-provided user IDs without verification
- Expose detailed error messages about auth failures
- Skip auth checks assuming "internal" endpoints are safe
- Store sensitive data in JWT payload (use user ID only)
- Forget to handle both header and cookie auth methods

## Related Skills

- **bknd-create-role** - Define roles for authorization
- **bknd-assign-permissions** - Configure role permissions
- **bknd-public-vs-auth** - Public vs authenticated access
- **bknd-row-level-security** - Data-level access control
- **bknd-custom-endpoint** - Create custom API endpoints
