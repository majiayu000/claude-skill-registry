---
name: solidstart-advanced-server
description: "SolidStart advanced server: getRequestEvent for request context, static assets handling, returning responses, request events and nativeEvent access."
metadata:
  globs:
    - "src/routes/**/*"
    - "public/**/*"
---

# SolidStart Advanced Server Patterns

## getRequestEvent

Access server request context anywhere on server. Uses Async Local Storage.

```tsx
import { getRequestEvent } from "solid-js/web";

const event = getRequestEvent();
if (event) {
  const auth = event.request.headers.get("Authorization");
  const url = event.request.url;
}
```

### Request

Access Web Request object:

```tsx
const event = getRequestEvent();
if (event) {
  // Access request properties
  const url = event.request.url;
  const headers = event.request.headers;
  const method = event.request.method;
}
```

### Response

Read/write response headers and status:

```tsx
const event = getRequestEvent();
if (event) {
  event.response.headers.set("X-Custom-Header", "value");
  event.response.status = 200;
}
```

### Locals

Access typed locals (from middleware):

```tsx
// Typed in global.d.ts
declare module "App" {
  interface RequestEventLocals {
    user?: { id: string; name: string };
  }
}

// In server function
const event = getRequestEvent();
const user = event?.locals?.user;
```

### nativeEvent

Access underlying Vinxi/H3 event:

```tsx
const event = getRequestEvent();
const nativeEvent = event?.nativeEvent;
// Pass to Vinxi HTTP helpers
```

**Note:** Vinxi HTTP helpers don't treeshake - only import in server-only files.

## Static Assets

### Public Directory

Place assets in `/public` directory:

```
public/
├── favicon.ico          -> /favicon.ico
├── images/
│   └── logo.png        -> /images/logo.png
└── documents/
    └── report.pdf      -> /documents/report.pdf
```

Reference with absolute paths:

```tsx
<img src="/images/logo.png" alt="Logo" />
```

**Use for:**
- Documents
- Service workers
- Media files (images, audio, video)
- Manifest files
- Metadata files (robots.txt, sitemaps)
- Favicon

### Importing Assets

Import assets directly (Vite hashes filenames):

```tsx
import logo from "./logo.png";

<img src={logo} alt="Logo" />
// Renders as: /assets/logo.2d8efhg.png
```

**Benefits:**
- Automatic cache busting
- Build-time optimization
- Type safety

## Returning Responses

Return Response objects from server functions. TypeScript-aware.

```tsx
import { json, redirect } from "@solidjs/router";

// JSON response - typed correctly
const hello = query(async (name: string) => {
  "use server";
  return json(
    { hello: name },
    { headers: { "cache-control": "max-age=60" } }
  );
}, "hello");

// Redirect - returns 'never' type
const getUser = query(async () => {
  "use server";
  const session = await getSession();
  if (!session.data.userId) {
    throw redirect("/login"); // Type is Promise<User>, not Promise<never>
  }
  return await db.getUser(session.data.userId);
}, "user");
```

**Response helpers:**
- `json()` - JSON response with headers
- `redirect()` - Returns `never` type
- `reload()` - Returns `never` type

## Request Events Context

Use `event.locals` for request-scoped data:

```tsx
// Middleware
export default createMiddleware({
  onRequest: (event) => {
    event.locals.user = { id: "123", name: "John" };
    event.locals.startTime = Date.now();
  }
});

// Server function
const getData = query(async () => {
  "use server";
  const event = getRequestEvent();
  const user = event?.locals?.user;
  // Use user data
}, "data");
```

## HttpHeader

Set custom HTTP headers in responses:

```tsx
import { HttpHeader } from "@solidjs/start";

<HttpHeader name="x-robots-tag" value="noindex" />
```

**Use cases:**
- Security headers
- CORS configuration
- Cache control
- SEO headers

**Note:** With streaming, headers must be set before stream first flushes. Use `deferStream: true` for resources that need to load before responding.

## HttpStatusCode

Set HTTP status codes for pages:

```tsx
import { HttpStatusCode } from "@solidjs/start";

// 404 page
export default function NotFound() {
  return (
    <>
      <HttpStatusCode code={404} />
      <h1>Page not found</h1>
    </>
  );
}

// Dynamic status with ErrorBoundary
<ErrorBoundary
  fallback={(e) => (
    <Show when={e.message === "Not found"}>
      <HttpStatusCode code={404} />
    </Show>
  )}
>
  <Content />
</ErrorBoundary>
```

**Use cases:**
- Error pages (404, 500, etc.)
- Dynamic status based on data
- SEO optimization

**Note:** With streaming, status codes must be set before stream first flushes.

## getServerFunctionMeta

Get stable function ID across parallel instances (multi-core/workers):

```tsx
import { getServerFunctionMeta } from "@solidjs/start";

const counter = async () => {
  "use server";
  const { id } = getServerFunctionMeta()!;
  const key = `counter_${id}`;
  appCache[key] = appCache[key] ?? 0;
  appCache[key]++;
  return appCache[key] as number;
};
```

**Use case:** Caching or state management in multi-core SolidStart apps.

**Note:** The `id` can change between builds.

## Best Practices

1. Use `getRequestEvent()` for accessing request context in server functions
2. Type `locals` in `global.d.ts` for better TypeScript support
3. Use public directory for stable asset references
4. Import assets for cache-busting and optimization
5. Return typed responses using `json`, `redirect`, `reload`
6. Access `nativeEvent` only when necessary (Vinxi helpers don't treeshake)
7. Set HTTP headers and status codes before streaming starts
8. Use `HttpStatusCode` with ErrorBoundary for dynamic status codes

