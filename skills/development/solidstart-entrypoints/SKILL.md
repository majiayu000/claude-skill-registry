---
name: solidstart-entrypoints
description: "SolidStart entrypoints: app.tsx for isomorphic root, entry-client.tsx for browser initialization, entry-server.tsx for SSR setup, app.config.ts for build configuration."
metadata:
  globs:
    - "src/app.tsx"
    - "src/entry-*.tsx"
    - "app.config.ts"
    - "**/app.config.*"
---

# SolidStart Entrypoints

Complete guide to customizing SolidStart entrypoints. Entrypoints control how your app initializes on both client and server.

## app.tsx - Isomorphic Root

The `App` component is the isomorphic (shared on server and browser) entry point. This is where code runs on both sides.

### Basic Example (with Routing)

```tsx
import { A, Router } from "@solidjs/router";
import { FileRoutes } from "@solidjs/start/router";
import { Suspense } from "solid-js";

export default function App() {
  return (
    <Router
      root={(props) => (
        <>
          <nav>
            <A href="/">Index</A>
            <A href="/about">About</A>
          </nav>
          <Suspense>{props.children}</Suspense>
        </>
      )}
    >
      <FileRoutes />
    </Router>
  );
}
```

**Critical:** Always wrap router root with `<Suspense>` - routes are lazy-loaded.

### Bare Example (no routing)

```tsx
export default function App() {
  return (
    <main>
      <h1>Hello world!</h1>
    </main>
  );
}
```

**Key points:**
- Runs on both server and client
- Define router setup here
- Add global layouts, providers, context
- Shared initialization logic

## entry-client.tsx - Browser Entry

`entry-client.tsx` is where the application starts in the browser. It mounts the app to the DOM.

### Basic Setup

```tsx
import { mount, StartClient } from "@solidjs/start/client";

mount(() => <StartClient />, document.getElementById("app")!);
```

### Custom Client Initialization

```tsx
import { mount, StartClient } from "@solidjs/start/client";

// Register service workers
if ("serviceWorker" in navigator) {
  navigator.serviceWorker.register("/sw.js");
}

// Client-only initialization
console.log("Client starting");

mount(() => <StartClient />, document.getElementById("app")!);
```

**Use cases:**
- Service worker registration
- Client-only initialization
- Browser API setup
- Analytics initialization
- Client-side routing setup

**Important:** This file runs only in the browser, not on the server.

## entry-server.tsx - Server Entry

`entry-server.tsx` is where the application starts on the server. It defines the HTML document structure.

### Basic Setup

```tsx
import { createHandler, StartServer } from "@solidjs/start/server";

export default createHandler(() => (
  <StartServer
    document={({ assets, children, scripts }) => (
      <html lang="en">
        <head>
          <meta charset="utf-8" />
          <meta name="viewport" content="width=device-width, initial-scale=1" />
          <link rel="icon" href="/favicon.ico" />
          {assets}
        </head>
        <body>
          <div id="app">{children}</div>
          {scripts}
        </body>
      </html>
    )}
  />
));
```

### Custom Document Structure

```tsx
import { createHandler, StartServer } from "@solidjs/start/server";

export default createHandler(() => (
  <StartServer
    document={({ assets, children, scripts }) => (
      <html lang="en">
        <head>
          <meta charset="utf-8" />
          <meta name="viewport" content="width=device-width, initial-scale=1" />
          <meta name="description" content="My SolidStart app" />
          <link rel="icon" href="/favicon.ico" />
          <link rel="stylesheet" href="/styles.css" />
          {assets}
        </head>
        <body>
          <noscript>You need to enable JavaScript to run this app.</noscript>
          <div id="app">{children}</div>
          {scripts}
        </body>
      </html>
    )}
  />
));
```

### SSR Modes

Configure SSR mode in `createHandler`:

```tsx
import { createHandler, StartServer } from "@solidjs/start/server";

// Sync SSR (default)
export default createHandler(() => <StartServer document={...} />);

// Async SSR
export default createHandler(
  () => <StartServer document={...} />,
  { mode: "async" }
);

// Streaming SSR
export default createHandler(
  () => <StartServer document={...} />,
  { mode: "stream" }
);
```

**Document props:**
- `assets`: CSS and other asset links
- `children`: Rendered app content
- `scripts`: JavaScript bundles

## app.config.ts - Build Configuration

The `app.config.ts` is the root configuration file for SolidStart, Vinxi, Vite, and Nitro.

### Basic Configuration

```tsx
import { defineConfig } from "@solidjs/start/config";

export default defineConfig({});
```

### Advanced Configuration

```tsx
import { defineConfig } from "@solidjs/start/config";

export default defineConfig({
  server: {
    preset: "node-server", // or "vercel", "netlify", etc.
  },
  vite: {
    // Vite configuration
    build: {
      target: "esnext",
    },
  },
  nitro: {
    // Nitro configuration
    preset: "node-server",
  },
});
```

**Configuration options:**
- `server`: Server preset and settings
- `vite`: Vite build configuration
- `nitro`: Nitro server configuration
- `router`: Router configuration
- `ssr`: SSR mode settings

## Common Patterns

### Adding Global Providers

```tsx
// app.tsx
import { Router } from "@solidjs/router";
import { FileRoutes } from "@solidjs/start/router";
import { Suspense } from "solid-js";
import { ThemeProvider } from "./contexts/ThemeContext";

export default function App() {
  return (
    <ThemeProvider>
      <Router root={(props) => <Suspense>{props.children}</Suspense>}>
        <FileRoutes />
      </Router>
    </ThemeProvider>
  );
}
```

### Custom Error Boundaries

```tsx
// app.tsx
import { ErrorBoundary } from "solid-js";
import { Router } from "@solidjs/router";
import { FileRoutes } from "@solidjs/start/router";

export default function App() {
  return (
    <ErrorBoundary fallback={(err) => <div>Error: {err.toString()}</div>}>
      <Router root={(props) => <Suspense>{props.children}</Suspense>}>
        <FileRoutes />
      </Router>
    </ErrorBoundary>
  );
}
```

### Service Worker Registration

```tsx
// entry-client.tsx
import { mount, StartClient } from "@solidjs/start/client";

if ("serviceWorker" in navigator) {
  window.addEventListener("load", () => {
    navigator.serviceWorker
      .register("/sw.js")
      .then((registration) => {
        console.log("SW registered:", registration);
      })
      .catch((error) => {
        console.log("SW registration failed:", error);
      });
  });
}

mount(() => <StartClient />, document.getElementById("app")!);
```

### Custom HTML Document

```tsx
// entry-server.tsx
import { createHandler, StartServer } from "@solidjs/start/server";

export default createHandler(() => (
  <StartServer
    document={({ assets, children, scripts }) => (
      <html lang="en" data-theme="dark">
        <head>
          <meta charset="utf-8" />
          <meta name="viewport" content="width=device-width, initial-scale=1" />
          <title>My App</title>
          <link rel="icon" href="/favicon.ico" />
          <link rel="preconnect" href="https://fonts.googleapis.com" />
          {assets}
        </head>
        <body>
          <div id="app">{children}</div>
          {scripts}
        </body>
      </html>
    )}
  />
));
```

### Environment-Specific Configuration

```tsx
// app.config.ts
import { defineConfig } from "@solidjs/start/config";

export default defineConfig({
  server: {
    preset: process.env.NODE_ENV === "production" 
      ? "node-server" 
      : "node-dev",
  },
  vite: {
    server: {
      port: process.env.PORT ? parseInt(process.env.PORT) : 3000,
    },
  },
});
```

## File Structure

```
src/
├── app.tsx              # Isomorphic root component
├── entry-client.tsx     # Browser entry point
├── entry-server.tsx     # Server entry point
app.config.ts            # Build configuration
```

## Best Practices

1. **Keep app.tsx isomorphic:**
   - Don't use browser-only APIs
   - Use `isServer` checks if needed
   - Shared logic only

2. **Client-only code in entry-client.tsx:**
   - Service workers
   - Browser APIs
   - Client-side analytics

3. **Server-only code in entry-server.tsx:**
   - HTML document structure
   - Meta tags
   - Server-side initialization

4. **Configuration in app.config.ts:**
   - Build settings
   - Server presets
   - Vite/Nitro config

5. **Always wrap router with Suspense:**
   - Routes are lazy-loaded
   - Suspense handles loading states

## Summary

- **app.tsx**: Isomorphic root, router setup, global providers
- **entry-client.tsx**: Browser initialization, service workers
- **entry-server.tsx**: HTML document structure, SSR setup
- **app.config.ts**: Build and server configuration

