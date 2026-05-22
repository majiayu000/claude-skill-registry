---
name: solid-core-rendering-ssr
description: "SolidJS rendering and SSR: render() for client, hydrate() for SSR hydration, renderToString/renderToStream for server rendering, isServer check."
---

# Rendering and SSR

## Client-Side Rendering

### render()

Mounts Solid app to DOM. Browser entry point for SPAs.

```tsx
import { render } from "solid-js/web";

const dispose = render(() => <App />, document.getElementById("app")!);
```

**Critical:** First argument must be a function, not JSX directly.

```tsx
// ✅ Correct
render(() => <App />, element)

// ❌ Wrong - calls App before render sets up tracking
render(<App />, element)
```

Returns dispose function to unmount app:

```tsx
const dispose = render(() => <App />, element);
// Later...
dispose();
```

## Server-Side Rendering

### hydrate()

Hydrates server-rendered HTML. Client entry point for SSR apps.

```tsx
import { hydrate } from "solid-js/web";

const dispose = hydrate(() => <App />, document.getElementById("app")!);
```

Attempts to rehydrate DOM that was already rendered on server. Must match server output.

### renderToString()

Renders component to HTML string (synchronous).

```tsx
import { renderToString } from "solid-js/web";

const html = renderToString(() => <App />);
```

### renderToStringAsync()

Renders component to HTML string (asynchronous). Handles Suspense boundaries.

```tsx
import { renderToStringAsync } from "solid-js/web";

const html = await renderToStringAsync(() => <App />);
```

**Use when:**
- App has async data fetching
- Suspense boundaries need resolution
- Server-side data loading required

### renderToStream()

Streams HTML to response. Progressive rendering for better performance.

```tsx
import { renderToStream } from "solid-js/web";

const stream = renderToStream(() => <App />);

// Pipe to response
stream.pipeTo(response.writable);
```

**Benefits:**
- Faster Time to First Byte (TTFB)
- Progressive HTML delivery
- Better perceived performance

### HydrationScript

Bootstrap hydration before Solid runtime loads. Captures events before JS loads.

```tsx
import { HydrationScript, generateHydrationScript } from "solid-js/web";

// As component (JSX)
<HydrationScript 
  nonce={nonce}
  eventNames={["click", "input"]}
/>

// As function (HTML string)
const script = generateHydrationScript({
  nonce: nonce,
  eventNames: ["click", "input"]
});
```

**Options:**
- `nonce`: CSP nonce for script tag
- `eventNames`: Events to capture before JS loads (default: `["click", "input"]`)

**Use case:** Progressive enhancement - capture user interactions before hydration completes.

## Server Detection

### isServer

Check if code is running on server.

```tsx
import { isServer } from "solid-js/web";

if (isServer) {
  // Server-only code
  console.log("Running on server");
} else {
  // Client-only code
  console.log("Running on client");
}
```

**Use cases:**
- Conditional imports
- Server-only initialization
- Platform-specific code

**Note:** Bundlers eliminate dead code based on this constant.

### DEV

Development-only features. Removed in production builds.

```tsx
import { DEV } from "solid-js";
import { isServer } from "solid-js/web";

// Only runs in development (client-side)
if (DEV && !isServer) {
  console.log("Development mode");
}
```

**Use cases:**
- Development debugging
- Dev-only features
- Library development
- Conditional code for dev/prod

**Note:** `DEV` is always defined on server, so combine with `isServer` check for client-only dev code.

## SSR Best Practices

1. **Match server and client output:**
   - Use `hydrate()` with matching server-rendered HTML
   - Ensure component order is identical

2. **Handle async data:**
   - Use `renderToStringAsync()` for Suspense
   - Preload data on server when possible

3. **Streaming:**
   - Use `renderToStream()` for better performance
   - Progressive rendering improves TTFB

4. **Avoid hydration mismatches:**
   - Don't use `Math.random()` or `Date.now()` in render
   - Use `createUniqueId()` for stable IDs
   - Check `isServer` for platform-specific code

5. **NoHydration for static content:**
   - Wrap static content in `<NoHydration>` to skip hydration
   - Reduces client-side JavaScript

## Example: Full SSR Setup

**Server (entry-server.tsx):**
```tsx
import { renderToStream } from "solid-js/web";
import App from "./App";

export async function handler(request: Request) {
  const stream = renderToStream(() => <App />);
  return new Response(stream, {
    headers: { "Content-Type": "text/html" }
  });
}
```

**Client (entry-client.tsx):**
```tsx
import { hydrate } from "solid-js/web";
import App from "./App";

hydrate(() => <App />, document.getElementById("app")!);
```

