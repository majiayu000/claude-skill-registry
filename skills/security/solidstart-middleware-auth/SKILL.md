---
name: solidstart-middleware-auth
description: "SolidStart middleware, sessions, authentication: createMiddleware with onRequest/onBeforeResponse, useSession for cookies, protected routes, WebSocket endpoints."
metadata:
  globs:
    - "src/middleware/**/*"
    - "**/*auth*"
    - "**/*session*"
---

# SolidStart Middleware, Sessions & Auth

## Middleware

Configure in `app.config.ts`:
```ts
export default defineConfig({
  middleware: "src/middleware/index.ts"
});
```

### When to Use Middleware (and When Not To)

Use middleware for:
- Request/response header management (CSP, cache control, CORS)
- Request-scoped data via `event.locals` (trace IDs, feature flags, auth hints)
- Early redirects (legacy URLs, locale routing, maintenance mode)
- Lightweight preprocessing (normalizing headers, basic validation)

Avoid middleware for:
- Authorization (middleware does not run on every client-side navigation)
- Heavy computation or database calls (keep it fast and side-effect light)
- Business logic that depends on user state (put checks in queries/actions/API)

### Basic Middleware

```ts
// src/middleware/index.ts
import { createMiddleware } from "@solidjs/start/middleware";

export default createMiddleware({
  onRequest: (event) => {
    console.log("Request:", event.request.url);
    event.locals.startTime = Date.now();
  },
  onBeforeResponse: (event) => {
    const duration = Date.now() - event.locals.startTime;
    console.log(`Request took ${duration}ms`);
  }
});
```

### Lifecycle Events

- `onRequest`: Before route handler (modify headers, store in locals)
- `onBeforeResponse`: After route handler (modify response, logging)

Returning a `Response` from either hook short-circuits the pipeline and skips
remaining middleware and route handlers.

```ts
export default createMiddleware({
  onRequest: (event) => {
    event.locals.userAgent = event.request.headers.get("user-agent");
  },
  onBeforeResponse: (event) => {
    event.response.headers.set("X-Response-Time", "100ms");
  }
});
```

### Accessing Locals

Store in middleware, access with `getRequestEvent`:

```ts
// middleware/index.ts
export default createMiddleware({
  onRequest: (event) => {
    event.locals.user = { id: "123", name: "John" };
  }
});

// In server function
import { getRequestEvent } from "solid-js/web";

const getUser = query(async () => {
  "use server";
  const event = getRequestEvent();
  return event?.locals?.user;
}, "user");
```

### Typing Locals

```ts
// global.d.ts
/// <reference types="@solidjs/start/env" />
declare module "App" {
  interface RequestEventLocals {
    user?: { id: string; name: string };
    startTime?: number;
  }
}
```

### Headers & Cookies

```ts
import { getCookie, setCookie } from "vinxi/http";

export default createMiddleware({
  onRequest: (event) => {
    // Read headers
    const userAgent = event.request.headers.get("user-agent");
    
    // Set headers
    event.request.headers.set("x-custom-header", "value");
    event.response.headers.set("Cache-Control", "max-age=3600");
    
    // Cookies
    const theme = getCookie(event.nativeEvent, "theme");
    setCookie(event.nativeEvent, "session", "abc123", {
      httpOnly: true,
      secure: true,
      maxAge: 60 * 60 * 24
    });
  }
});
```

### Custom Responses & Short-Circuiting

Only `Response` objects can be returned from middleware.

```ts
import { json, redirect } from "@solidjs/router";

export default createMiddleware({
  onRequest: (event) => {
    const { pathname } = new URL(event.request.url);
    if (pathname === "/old-path") {
      return redirect("/new-path", 301);
    }

    const authHeader = event.request.headers.get("Authorization");
    if (!authHeader) {
      return json({ error: "Unauthorized" }, { status: 401 });
    }
  }
});
```

### Building Custom Middleware (Composable Functions)

Prefer small, focused functions and compose them in order.

```ts
import type { FetchEvent } from "@solidjs/start/server";

function withRequestId() {
  return (event: FetchEvent) => {
    const id = crypto.randomUUID();
    event.locals.requestId = id;
    event.response.headers.set("x-request-id", id);
  };
}

function withTiming() {
  return (event: FetchEvent) => {
    event.locals.startTime = Date.now();
  };
}

function withTimingResponse() {
  return (event: FetchEvent) => {
    const ms = Date.now() - event.locals.startTime;
    event.response.headers.set("x-response-time", `${ms}ms`);
  };
}

export default createMiddleware({
  onRequest: [withRequestId(), withTiming()],
  onBeforeResponse: [withTimingResponse()]
});
```

### Extending Existing Middleware

Export shared middleware arrays, then extend them in route-specific configs.

```ts
// src/middleware/base.ts
import type { FetchEvent } from "@solidjs/start/server";

export const baseOnRequest: Array<(e: FetchEvent) => void> = [
  (event) => {
    event.locals.userAgent = event.request.headers.get("user-agent");
  }
];
```

```ts
// src/middleware/index.ts
import { createMiddleware } from "@solidjs/start/middleware";
import { baseOnRequest } from "./base";
import type { FetchEvent } from "@solidjs/start/server";

function withMaintenanceMode() {
  return (event: FetchEvent) => {
    if (process.env.MAINTENANCE === "true") {
      return new Response("Maintenance", { status: 503 });
    }
  };
}

export default createMiddleware({
  onRequest: [...baseOnRequest, withMaintenanceMode()]
});
```

### Redirects & Responses

```ts
import { redirect, json } from "@solidjs/router";

export default createMiddleware({
  onRequest: (event) => {
    const { pathname } = new URL(event.request.url);
    if (pathname === "/old-path") {
      return redirect("/new-path", 301);
    }
    
    const authHeader = event.request.headers.get("Authorization");
    if (!authHeader) {
      return json({ error: "Unauthorized" }, { status: 401 });
    }
  }
});
```

### Chaining Middleware

```ts
function middleware1(event: FetchEvent) {
  event.request.headers.set("x-header1", "value1");
}

function middleware2(event: FetchEvent) {
  event.request.headers.set("x-header2", "value2");
}

export default createMiddleware({
  onRequest: [middleware1, middleware2]
});
```

Order matters: middleware runs in array order; dependencies must come first.

## Sessions

### Basic Session

```ts
// src/lib/session.ts
import { useSession } from "vinxi/http";

type SessionData = {
  userId?: string;
  theme?: "light" | "dark";
};

export async function useAppSession() {
  "use server";
  const session = await useSession<SessionData>({
    password: process.env.SESSION_SECRET!, // Must be 32+ chars
    name: "app-session"
  });
  return session;
}

// Generate: openssl rand -base64 32
```

### Session Operations

```ts
// Get session data
export async function getSessionUserId() {
  "use server";
  const session = await useAppSession();
  return session.data.userId;
}

// Update session
export async function updateSession(updates: Partial<SessionData>) {
  "use server";
  const session = await useAppSession();
  await session.update(updates);
}

// Clear session
export async function clearSession() {
  "use server";
  const session = await useAppSession();
  await session.clear();
}
```

### Using with Queries

```ts
const getCurrentUser = query(async () => {
  "use server";
  const session = await useAppSession();
  if (!session.data.userId) {
    throw redirect("/login");
  }
  return await db.getUser(session.data.userId);
}, "currentUser");
```

## Authentication

### Protected Routes

```tsx
// routes/admin.tsx
import { query, redirect, createAsync } from "@solidjs/router";

const getAdminData = query(async () => {
  "use server";
  const session = await useAppSession();
  if (!session.data.userId) {
    throw redirect("/login");
  }
  
  const user = await db.getUser(session.data.userId);
  if (!user.isAdmin) {
    throw redirect("/");
  }
  
  return await db.getAdminData();
}, "adminData");

export default function AdminPage() {
  const data = createAsync(() => getAdminData(), { deferStream: true });
  return <div>{data()}</div>;
}
```

**Important:** Use `deferStream: true` - server-side redirects can't occur after streaming starts.

### Login Action

```tsx
const loginAction = action(async (formData: FormData) => {
  "use server";
  const email = formData.get("email")?.toString();
  const password = formData.get("password")?.toString();
  
  const user = await db.verifyUser(email, password);
  if (!user) {
    return { error: "Invalid credentials" };
  }
  
  const session = await useAppSession();
  await session.update({ userId: user.id });
  
  throw redirect("/dashboard");
}, "login");
```

### Logout Action

```tsx
const logoutAction = action(async () => {
  "use server";
  const session = await useAppSession();
  await session.clear();
  throw redirect("/");
}, "logout");
```

## WebSocket Endpoints

**Experimental** - use with caution.

### Configuration

```ts
// app.config.ts
export default defineConfig({
  server: {
    experimental: { websocket: true }
  }
}).addRouter({
  name: "ws",
  type: "http",
  handler: "./src/ws.ts",
  target: "server",
  base: "/ws"
});
```

### WebSocket Handler

```ts
// src/ws.ts
import { eventHandler } from "vinxi/http";

export default eventHandler({
  handler() {},
  websocket: {
    async open(peer) {
      console.log("Connection:", peer.id);
    },
    async message(peer, msg) {
      const message = msg.text();
      peer.send(message); // Broadcast
    },
    async close(peer, details) {
      console.log("Closed:", peer.id);
    },
    async error(peer, error) {
      console.error("Error:", error);
    }
  }
});
```

## Best Practices

1. Keep middleware lightweight - no heavy computation
2. Use sessions for auth state - secure, encrypted cookies
3. Use `deferStream: true` for protected routes
4. Type your locals for better TypeScript support
5. Don't rely on middleware for authorization (doesn't run on all requests)
6. Return a `Response` only when you want to terminate the pipeline
7. Compose small middleware functions and keep ordering explicit
