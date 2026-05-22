---
name: solidstart-request-events
description: "SolidStart request events: getRequestEvent for server context, event.locals for typed data, nativeEvent for Vinxi access, request handling."
metadata:
  globs:
    - "**/routes/**/*"
    - "**/*server*"
---

# SolidStart Request Events

Complete guide to accessing request events and context in SolidStart server functions. Type-safe locals and native event handling.

## getRequestEvent

Access the current request event anywhere on the server.

```tsx
import { getRequestEvent } from "solid-js/web";

"use server";

export async function getData() {
  const event = getRequestEvent();
  const url = event.request.url;
  const headers = event.request.headers;
  
  // Access request data
  return { url, headers };
}
```

## event.locals - Typed Context

Use `event.locals` to pass typed data around the request.

### Type Definition

```tsx
// global.d.ts
/// <reference types="@solidjs/start/env" />
declare module App {
  interface RequestEventLocals {
    userId: string;
    session: Session;
    nonce: string;
  }
}
```

### Setting Locals

```tsx
// middleware/index.ts
import { createMiddleware } from "@solidjs/start/middleware";

export default createMiddleware({
  onRequest: (event) => {
    // Set typed locals
    event.locals.userId = "123";
    event.locals.session = getSession(event);
    event.locals.nonce = generateNonce();
  },
});
```

### Accessing Locals

```tsx
"use server";

export async function getUser() {
  const event = getRequestEvent();
  const userId = event.locals.userId; // Typed!
  const session = event.locals.session; // Typed!
  
  return fetchUser(userId);
}
```

## nativeEvent - Vinxi Access

Access the underlying Vinxi/H3 event for advanced use cases.

```tsx
import { getRequestEvent } from "solid-js/web";

"use server";

export async function advancedHandler() {
  const event = getRequestEvent();
  const nativeEvent = event.nativeEvent; // H3Event
  
  // Use H3 helpers
  // Note: Only import in server-only files
}
```

**Important:** Vinxi HTTP helpers don't treeshake. Only import in server-only files.

## Common Patterns

### Authentication

```tsx
// middleware/auth.ts
export default createMiddleware({
  onRequest: (event) => {
    const token = event.request.headers.get("Authorization");
    const user = verifyToken(token);
    event.locals.user = user;
  },
});

// routes/protected.tsx
"use server";

export async function getProtectedData() {
  const event = getRequestEvent();
  const user = event.locals.user; // Typed!
  
  if (!user) {
    throw new Error("Unauthorized");
  }
  
  return fetchUserData(user.id);
}
```

### Request Metadata

```tsx
"use server";

export async function logRequest() {
  const event = getRequestEvent();
  const url = new URL(event.request.url);
  const ip = event.request.headers.get("x-forwarded-for");
  const userAgent = event.request.headers.get("user-agent");
  
  console.log({ url: url.pathname, ip, userAgent });
}
```

### Response Manipulation

```tsx
"use server";

export async function setCustomHeader() {
  const event = getRequestEvent();
  
  event.response.headers.set("X-Custom-Header", "value");
  
  return { data: "..." };
}
```

### Session Management

```tsx
// middleware/session.ts
export default createMiddleware({
  onRequest: (event) => {
    const sessionId = getSessionId(event);
    event.locals.session = getSession(sessionId);
  },
});

// routes/api.tsx
"use server";

export async function updateSession(data: any) {
  const event = getRequestEvent();
  const session = event.locals.session;
  
  session.data = data;
  await saveSession(session);
}
```

## Best Practices

1. **Type your locals:**
   - Define in `global.d.ts`
   - Get autocomplete and type safety

2. **Set locals in middleware:**
   - Centralized setup
   - Available to all routes

3. **Use getRequestEvent:**
   - Access anywhere on server
   - Type-safe locals

4. **Avoid nativeEvent unless needed:**
   - Prefer SolidStart APIs
   - Only for advanced cases

5. **Server-only imports:**
   - Vinxi helpers in server files only
   - Avoid treeshake issues

## Summary

- **getRequestEvent**: Access current request
- **event.locals**: Typed request context
- **nativeEvent**: Underlying H3 event
- **Type safety**: Define locals in global.d.ts
- **Middleware**: Set locals centrally
