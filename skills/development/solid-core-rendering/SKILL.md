---
name: solid-core-rendering
description: "SolidJS rendering: render for client apps, hydrate for SSR, renderToString for server rendering, renderToStream for streaming, isServer checks."
metadata:
  globs:
    - "**/entry-*.tsx"
    - "**/*render*"
---

# SolidJS Rendering Utilities

Complete guide to rendering SolidJS applications. Understand client-side rendering, SSR, hydration, and streaming.

## render - Client-Side Rendering

Mount your Solid app to the DOM. Essential browser entry point for SPAs.

```tsx
import { render } from "solid-js/web";

const dispose = render(() => <App />, document.getElementById("app")!);

// Later, unmount
dispose();
```

**Key points:**
- First argument must be a **function** (not JSX directly)
- Element should be empty (render appends, dispose removes all)
- Returns dispose function to unmount

**Correct usage:**
```tsx
// ✅ Correct - function
render(() => <App />, element);

// ❌ Wrong - JSX directly
render(<App />, element);
```

## hydrate - SSR Hydration

Hydrate server-rendered HTML with client-side code. Essential for SSR apps.

```tsx
import { hydrate } from "solid-js/web";

const dispose = hydrate(() => <App />, document.getElementById("app")!);
```

**Key points:**
- Rehydrates existing DOM
- Matches server-rendered structure
- Attaches interactivity
- Used in SSR applications

**Options:**
```tsx
hydrate(() => <App />, element, {
  renderId: "app", // Optional render ID
  owner: undefined, // Optional owner context
});
```

## renderToString - Server Rendering

Render components to HTML string for SSR.

```tsx
import { renderToString } from "solid-js/web";

const html = renderToString(() => <App />);
// Returns: "<div>...</div>"
```

**Use cases:**
- SSR initial render
- Static site generation
- Email templates
- Server-side HTML generation

## renderToStringAsync - Async Rendering

Render components with async data to HTML string.

```tsx
import { renderToStringAsync } from "solid-js/web";

const html = await renderToStringAsync(() => <App />);
// Waits for async resources
```

**Use cases:**
- SSR with async data
- Resources and Suspense
- Async components

## renderToStream - Streaming SSR

Stream HTML to client for faster time-to-first-byte.

```tsx
import { renderToStream } from "solid-js/web";

const stream = renderToStream(() => <App />);

// Pipe to response
stream.pipeTo(response);
```

**Benefits:**
- Faster initial render
- Progressive HTML delivery
- Better perceived performance

## HydrationScript / generateHydrationScript

Bootstrap hydration before Solid runtime loads.

```tsx
import { HydrationScript, generateHydrationScript } from "solid-js/web";

// As component (JSX)
<HydrationScript nonce={nonce} eventNames={["click", "input"]} />

// As string (manual HTML)
const script = generateHydrationScript({
  nonce,
  eventNames: ["click", "input"],
});
```

**Purpose:**
- Sets up hydration on client
- Required for SSR apps
- Place once in `<head>` or before closing `</body>`

## isServer - Environment Check

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
- Conditional server/client code
- Environment-specific logic
- Avoiding browser APIs on server

## Common Patterns

### Client Entry Point

```tsx
// entry-client.tsx
import { render } from "solid-js/web";
import App from "./App";

render(() => <App />, document.getElementById("app")!);
```

### SSR Entry Point

```tsx
// entry-server.tsx
import { renderToString, generateHydrationScript } from "solid-js/web";
import App from "./App";

export default function handler(req, res) {
  const html = renderToString(() => <App />);
  
  res.send(`
    <!DOCTYPE html>
    <html>
      <head>
        ${generateHydrationScript()}
      </head>
      <body>
        <div id="app">${html}</div>
      </body>
    </html>
  `);
}
```

### Client Hydration

```tsx
// entry-client.tsx
import { hydrate } from "solid-js/web";
import App from "./App";

hydrate(() => <App />, document.getElementById("app")!);
```

### Streaming SSR

```tsx
import { renderToStream } from "solid-js/web";

export default async function handler(req, res) {
  const stream = renderToStream(() => <App />);
  
  res.setHeader("Content-Type", "text/html");
  stream.pipeTo(res);
}
```

### Environment-Specific Code

```tsx
import { isServer } from "solid-js/web";

function Component() {
  if (isServer) {
    // Server-only initialization
    return <div>Server rendered</div>;
  }
  
  // Client-only code
  const [mounted, setMounted] = createSignal(false);
  onMount(() => setMounted(true));
  
  return <div>Client: {mounted()}</div>;
}
```

## Best Practices

1. **Always use function form:**
   - `render(() => <App />, element)`
   - Not `render(<App />, element)`

2. **Empty mount element:**
   - Element should be empty
   - Render appends, dispose removes all

3. **Hydration matching:**
   - Server and client must match
   - Same structure and content

4. **Use isServer checks:**
   - Avoid browser APIs on server
   - Conditional logic when needed

5. **Streaming for performance:**
   - Use renderToStream for SSR
   - Faster time-to-first-byte

## Summary

- **render**: Client-side mounting
- **hydrate**: SSR hydration
- **renderToString**: Server HTML generation
- **renderToStringAsync**: Async server rendering
- **renderToStream**: Streaming SSR
- **HydrationScript / generateHydrationScript**: Hydration setup
- **isServer**: Environment detection
