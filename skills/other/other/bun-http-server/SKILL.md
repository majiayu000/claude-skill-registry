---
name: Bun HTTP Server
description: Use when building HTTP servers with Bun.serve, handling requests/responses, implementing routing, creating REST APIs, or configuring fetch handlers.
version: 1.0.0
---

# Bun HTTP Server

Bun has a built-in high-performance HTTP server via `Bun.serve()`.

## Quick Start

```typescript
const server = Bun.serve({
  port: 3000,
  fetch(req) {
    return new Response("Hello World!");
  },
});

console.log(`Server running at http://localhost:${server.port}`);
```

## Request Handling

```typescript
Bun.serve({
  fetch(req) {
    const url = new URL(req.url);

    // Method
    console.log(req.method); // GET, POST, etc.

    // Path
    console.log(url.pathname); // /api/users

    // Query params
    console.log(url.searchParams.get("id")); // ?id=123

    // Headers
    console.log(req.headers.get("Content-Type"));

    return new Response("OK");
  },
});
```

## Body Parsing

```typescript
Bun.serve({
  async fetch(req) {
    // JSON
    const json = await req.json();

    // Form data
    const form = await req.formData();

    // Text
    const text = await req.text();

    // ArrayBuffer
    const buffer = await req.arrayBuffer();

    // Blob
    const blob = await req.blob();

    return new Response("Received");
  },
});
```

## Response Types

```typescript
Bun.serve({
  fetch(req) {
    const url = new URL(req.url);

    switch (url.pathname) {
      case "/json":
        return Response.json({ message: "Hello" });

      case "/html":
        return new Response("<h1>Hello</h1>", {
          headers: { "Content-Type": "text/html" },
        });

      case "/redirect":
        return Response.redirect("/new-location", 302);

      case "/file":
        return new Response(Bun.file("./image.png"));

      case "/stream":
        return new Response(
          new ReadableStream({
            start(controller) {
              controller.enqueue("chunk1");
              controller.enqueue("chunk2");
              controller.close();
            },
          })
        );

      default:
        return new Response("Not Found", { status: 404 });
    }
  },
});
```

## Simple Routing

```typescript
Bun.serve({
  fetch(req) {
    const url = new URL(req.url);
    const path = url.pathname;
    const method = req.method;

    // Static routes
    if (method === "GET" && path === "/") {
      return new Response("Home");
    }

    if (method === "GET" && path === "/api/users") {
      return Response.json([{ id: 1, name: "Alice" }]);
    }

    // Dynamic routes
    const userMatch = path.match(/^\/api\/users\/(\d+)$/);
    if (method === "GET" && userMatch) {
      const userId = userMatch[1];
      return Response.json({ id: userId });
    }

    // 404
    return new Response("Not Found", { status: 404 });
  },
});
```

## Error Handling

```typescript
Bun.serve({
  fetch(req) {
    try {
      // Handle request
      throw new Error("Something went wrong");
    } catch (error) {
      return new Response(
        JSON.stringify({ error: error.message }),
        {
          status: 500,
          headers: { "Content-Type": "application/json" }
        }
      );
    }
  },
  error(error) {
    // Global error handler
    return new Response(`Error: ${error.message}`, { status: 500 });
  },
});
```

## Server Options

```typescript
const server = Bun.serve({
  port: 3000,           // Default: 3000
  hostname: "0.0.0.0",  // Default: "0.0.0.0"

  development: true,    // Pretty errors in browser

  // TLS/HTTPS
  tls: {
    key: Bun.file("./key.pem"),
    cert: Bun.file("./cert.pem"),
  },

  // Unix socket
  unix: "/tmp/my-socket.sock",

  // Max request body size (default 128MB)
  maxRequestBodySize: 1024 * 1024 * 10, // 10MB

  fetch(req) {
    return new Response("OK");
  },
});
```

## Server Methods

```typescript
const server = Bun.serve({ ... });

// Server info
console.log(server.port);        // 3000
console.log(server.hostname);    // "0.0.0.0"
console.log(server.url);         // URL object

// Stop server
server.stop();

// Reload with new config
server.reload({
  fetch(req) {
    return new Response("Updated!");
  },
});

// Pending requests count
console.log(server.pendingRequests);
```

## Static Files

```typescript
Bun.serve({
  fetch(req) {
    const url = new URL(req.url);

    // Serve static files from public/
    if (url.pathname.startsWith("/static/")) {
      const filePath = `./public${url.pathname.replace("/static", "")}`;
      const file = Bun.file(filePath);

      if (await file.exists()) {
        return new Response(file);
      }
      return new Response("Not Found", { status: 404 });
    }

    return new Response("API");
  },
});
```

## CORS

```typescript
function corsHeaders() {
  return {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type, Authorization",
  };
}

Bun.serve({
  fetch(req) {
    // Handle preflight
    if (req.method === "OPTIONS") {
      return new Response(null, { headers: corsHeaders() });
    }

    // Add CORS headers to response
    return new Response("OK", { headers: corsHeaders() });
  },
});
```

## Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `EADDRINUSE` | Port in use | Use different port or kill process |
| `Cannot read body` | Body already consumed | Read body once only |
| `CORS error` | Missing headers | Add CORS headers |
| `413 Payload Too Large` | Body exceeds limit | Increase maxRequestBodySize |

## When to Load References

Load `references/tls-config.md` when:
- HTTPS/TLS setup
- Certificate configuration
- mTLS authentication

Load `references/streaming.md` when:
- Server-sent events
- Streaming responses
- Chunked transfer encoding
