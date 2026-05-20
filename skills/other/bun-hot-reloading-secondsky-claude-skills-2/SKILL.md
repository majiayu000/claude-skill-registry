---
name: Bun Hot Reloading
description: Use when implementing hot reloading with Bun (--hot, --watch), HMR, or automatic code reloading during development. Covers watch mode, hot mode, and HTTP server reload.
version: 1.0.0
---

# Bun Hot Reloading

Bun provides built-in hot reloading for faster development cycles.

## Watch Mode vs Hot Mode

| Feature | `--watch` | `--hot` |
|---------|-----------|---------|
| Behavior | Restart process | Reload modules |
| State | Lost on reload | Preserved |
| Speed | ~20ms restart | Instant reload |
| Use case | Any file type | Bun.serve HTTP |

## Watch Mode (--watch)

Restarts the entire process when files change.

```bash
# Basic watch mode
bun --watch run src/index.ts

# Watch specific script
bun --watch run dev

# Watch with test runner
bun --watch test
```

### package.json Scripts

```json
{
  "scripts": {
    "dev": "bun --watch run src/index.ts",
    "dev:server": "bun --watch run src/server.ts",
    "test:watch": "bun --watch test"
  }
}
```

### Watch Behavior

- Watches imported files automatically
- Triggers on any `.ts`, `.tsx`, `.js`, `.jsx` change
- Also watches `.json` imports
- Restarts with fresh state

## Hot Mode (--hot)

Reloads modules in-place without restarting the process.

```bash
bun --hot run src/server.ts
```

### HTTP Server Hot Reload

```typescript
// src/server.ts
let counter = 0; // State preserved across hot reloads

export default {
  port: 3000,
  fetch(req: Request) {
    counter++;
    return new Response(`Request #${counter}`);
  },
};
```

```bash
bun --hot run src/server.ts
```

When you modify `server.ts`, the module reloads instantly while `counter` keeps its value.

### Bun.serve with Hot Reload

```typescript
// src/server.ts
const server = Bun.serve({
  port: 3000,
  fetch(req) {
    return new Response("Hello!");
  },
});

// Hot reload handler
if (import.meta.hot) {
  import.meta.hot.accept(() => {
    console.log("Hot reload!");
  });
}

console.log(`Server running on port ${server.port}`);
```

## import.meta.hot API

```typescript
// Check if hot reload is available
if (import.meta.hot) {
  // Accept updates to this module
  import.meta.hot.accept();

  // Accept with callback
  import.meta.hot.accept((newModule) => {
    console.log("Module updated:", newModule);
  });

  // Cleanup before reload
  import.meta.hot.dispose(() => {
    // Close connections, clear intervals, etc.
    clearInterval(myInterval);
  });

  // Decline hot reload (force full restart)
  import.meta.hot.decline();

  // Invalidate this module (trigger parent reload)
  import.meta.hot.invalidate();
}
```

## HTTP Server Patterns

### Express-like Pattern

```typescript
// src/server.ts
import { createApp } from "./app";

const app = createApp();

const server = Bun.serve({
  port: 3000,
  fetch: app.fetch,
});

// Hot reload: recreate app
if (import.meta.hot) {
  import.meta.hot.accept((newModule) => {
    // Reload with new fetch handler
    server.reload({
      fetch: newModule.default.fetch,
    });
  });
}
```

### Stateful Server

```typescript
// src/server.ts
// Store in globalThis to survive reloads
globalThis.connections ??= new Set();

const server = Bun.serve({
  port: 3000,
  fetch(req) {
    return new Response(`Connections: ${globalThis.connections.size}`);
  },
  websocket: {
    open(ws) {
      globalThis.connections.add(ws);
    },
    close(ws) {
      globalThis.connections.delete(ws);
    },
  },
});

if (import.meta.hot) {
  import.meta.hot.accept();
}
```

## Custom Watch Implementation

```typescript
// dev-server.ts
import { watch } from "fs";

const srcDir = "./src";
let server: ReturnType<typeof Bun.serve> | null = null;

async function startServer() {
  // Dynamic import with cache busting
  const module = await import(`./src/server.ts?t=${Date.now()}`);

  if (server) {
    server.stop();
  }

  server = Bun.serve(module.default);
  console.log(`Server started on port ${server.port}`);
}

// Initial start
await startServer();

// Watch for changes
watch(srcDir, { recursive: true }, async (event, filename) => {
  if (filename?.endsWith(".ts") || filename?.endsWith(".tsx")) {
    console.log(`\n[${event}] ${filename}`);
    await startServer();
  }
});

console.log("Watching for changes...");
```

## WebSocket Live Reload

### Server

```typescript
// src/dev-server.ts
const clients = new Set<ServerWebSocket>();

const server = Bun.serve({
  port: 3000,
  fetch(req, server) {
    if (req.headers.get("upgrade") === "websocket") {
      server.upgrade(req);
      return;
    }

    // Inject reload script in dev
    const html = `
      <!DOCTYPE html>
      <html>
        <body>
          <h1>Hello!</h1>
          <script>
            const ws = new WebSocket('ws://localhost:3000');
            ws.onmessage = (e) => {
              if (e.data === 'reload') location.reload();
            };
          </script>
        </body>
      </html>
    `;
    return new Response(html, {
      headers: { "Content-Type": "text/html" },
    });
  },
  websocket: {
    open(ws) {
      clients.add(ws);
    },
    close(ws) {
      clients.delete(ws);
    },
  },
});

// Notify clients on file change
watch("./src", { recursive: true }, () => {
  clients.forEach((ws) => ws.send("reload"));
});
```

## Vite Integration

For frontend development with HMR:

```typescript
// vite.config.ts
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    hmr: true,
  },
});
```

```bash
# Use Bun to run Vite
bunx --bun vite
```

## Testing with Watch

```bash
# Watch tests
bun --watch test

# Watch specific file
bun --watch test src/utils.test.ts

# With bail (stop on first failure)
bun --watch test --bail
```

## Environment Detection

```typescript
// Check if running with --hot
const isHot = !!import.meta.hot;

// Check if running with --watch
const isWatch = process.env.BUN_WATCH === "1";

// Development mode
const isDev = process.env.NODE_ENV !== "production";

if (isDev) {
  console.log("Running in development mode");
  console.log(`Hot reload: ${isHot}`);
  console.log(`Watch mode: ${isWatch}`);
}
```

## Common Issues

### State Not Preserved

```typescript
// ❌ State lost on hot reload
let cache = new Map();

// ✅ State preserved on hot reload
globalThis.cache ??= new Map();
const cache = globalThis.cache;
```

### Cleanup Not Running

```typescript
// ❌ Interval keeps running after reload
setInterval(() => console.log("tick"), 1000);

// ✅ Clean up on dispose
const interval = setInterval(() => console.log("tick"), 1000);

if (import.meta.hot) {
  import.meta.hot.dispose(() => {
    clearInterval(interval);
  });
}
```

### Module Not Reloading

```typescript
// ❌ Import not watched
const config = require("./config.json");

// ✅ Use import for watching
import config from "./config.json";
```

## Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `Changes not detected` | File not imported | Check import chain |
| `State lost` | Using `--watch` | Use `--hot` or globalThis |
| `Port in use` | Server not stopped | Implement server.stop() |
| `Memory leak` | No cleanup | Use dispose callback |

## When to Load References

Load `references/advanced-hmr.md` when:
- Custom HMR protocols
- Module federation
- Complex state management

Load `references/debugging.md` when:
- HMR not working
- State issues
- Performance debugging
