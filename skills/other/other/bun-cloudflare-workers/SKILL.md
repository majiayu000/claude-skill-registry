---
name: Bun Cloudflare Workers
description: This skill should be used when the user asks about "Cloudflare Workers with Bun", "deploying Bun to Workers", "wrangler with Bun", "edge deployment", "Bun to Cloudflare", or building and deploying applications to Cloudflare Workers using Bun.
---

# Bun Cloudflare Workers

Build and deploy Cloudflare Workers using Bun for development.

## Quick Start

```bash
# Create new Workers project
bunx create-cloudflare my-worker
cd my-worker

# Install dependencies
bun install

# Development
bun run dev

# Deploy
bun run deploy
```

## Project Setup

### package.json

```json
{
  "scripts": {
    "dev": "wrangler dev",
    "deploy": "wrangler deploy",
    "build": "bun build src/index.ts --outdir=dist --target=browser"
  },
  "devDependencies": {
    "@cloudflare/workers-types": "^4.20250906.0",
    "wrangler": "^4.54.0"
  }
}
```

### wrangler.toml

```toml
name = "my-worker"
main = "src/index.ts"
compatibility_date = "2024-01-01"

# Use Bun for local dev
[dev]
local_protocol = "http"

# Bindings
[[kv_namespaces]]
binding = "KV"
id = "xxx"

[[d1_databases]]
binding = "DB"
database_name = "my-db"
database_id = "xxx"
```

## Basic Worker

```typescript
// src/index.ts
export default {
  async fetch(request: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
    const url = new URL(request.url);

    if (url.pathname === "/") {
      return new Response("Hello from Cloudflare Workers!");
    }

    if (url.pathname === "/api/data") {
      return Response.json({ message: "Hello" });
    }

    return new Response("Not Found", { status: 404 });
  },
};

interface Env {
  KV: KVNamespace;
  DB: D1Database;
}
```

## Using Hono

```typescript
// src/index.ts
import { Hono } from "hono";

type Bindings = {
  KV: KVNamespace;
  DB: D1Database;
};

const app = new Hono<{ Bindings: Bindings }>();

app.get("/", (c) => c.text("Hello Hono!"));

app.get("/api/users", async (c) => {
  const users = await c.env.DB.prepare("SELECT * FROM users").all();
  return c.json(users.results);
});

app.post("/api/users", async (c) => {
  const { name } = await c.req.json();
  await c.env.DB.prepare("INSERT INTO users (name) VALUES (?)").bind(name).run();
  return c.json({ success: true });
});

export default app;
```

## KV Storage

```typescript
export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);
    const key = url.searchParams.get("key");

    if (request.method === "GET" && key) {
      const value = await env.KV.get(key);
      return Response.json({ key, value });
    }

    if (request.method === "PUT" && key) {
      const value = await request.text();
      await env.KV.put(key, value, { expirationTtl: 3600 });
      return Response.json({ success: true });
    }

    return new Response("Bad Request", { status: 400 });
  },
};
```

## D1 Database

```typescript
export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    // Query
    const { results } = await env.DB.prepare(
      "SELECT * FROM users WHERE active = ?"
    ).bind(1).all();

    // Insert
    const info = await env.DB.prepare(
      "INSERT INTO users (name, email) VALUES (?, ?)"
    ).bind("Alice", "alice@example.com").run();

    // Transaction
    const batch = await env.DB.batch([
      env.DB.prepare("INSERT INTO users (name) VALUES (?)").bind("Bob"),
      env.DB.prepare("INSERT INTO users (name) VALUES (?)").bind("Charlie"),
    ]);

    return Response.json(results);
  },
};
```

## Durable Objects

```typescript
// src/counter.ts
export class Counter {
  private state: DurableObjectState;
  private value = 0;

  constructor(state: DurableObjectState) {
    this.state = state;
    this.state.blockConcurrencyWhile(async () => {
      this.value = (await this.state.storage.get("value")) || 0;
    });
  }

  async fetch(request: Request): Promise<Response> {
    const url = new URL(request.url);

    if (url.pathname === "/increment") {
      this.value++;
      await this.state.storage.put("value", this.value);
    }

    return Response.json({ value: this.value });
  }
}

// src/index.ts
export { Counter } from "./counter";

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const id = env.COUNTER.idFromName("global");
    const stub = env.COUNTER.get(id);
    return stub.fetch(request);
  },
};
```

```toml
# wrangler.toml
[[durable_objects.bindings]]
name = "COUNTER"
class_name = "Counter"

[[migrations]]
tag = "v1"
new_classes = ["Counter"]
```

## R2 Storage

```typescript
export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);
    const key = url.pathname.slice(1);

    if (request.method === "GET") {
      const object = await env.BUCKET.get(key);
      if (!object) {
        return new Response("Not Found", { status: 404 });
      }
      return new Response(object.body, {
        headers: { "Content-Type": object.httpMetadata?.contentType || "application/octet-stream" },
      });
    }

    if (request.method === "PUT") {
      await env.BUCKET.put(key, request.body, {
        httpMetadata: { contentType: request.headers.get("Content-Type") || undefined },
      });
      return Response.json({ success: true });
    }

    return new Response("Method Not Allowed", { status: 405 });
  },
};
```

## Development with Bun

### Local Development

```bash
# Run with wrangler (uses Bun for TypeScript)
bun run dev

# Or directly
bunx wrangler dev
```

### Testing with Bun

```typescript
// src/index.test.ts
import { describe, test, expect } from "bun:test";

// Mock worker
const worker = {
  async fetch(request: Request) {
    return new Response("Hello");
  },
};

describe("Worker", () => {
  test("returns hello", async () => {
    const request = new Request("http://localhost/");
    const response = await worker.fetch(request);
    expect(await response.text()).toBe("Hello");
  });
});
```

### Miniflare for Testing

```typescript
import { Miniflare } from "miniflare";

const mf = new Miniflare({
  script: await Bun.file("./dist/index.js").text(),
  kvNamespaces: ["KV"],
});

const response = await mf.dispatchFetch("http://localhost/");
console.log(await response.text());
```

## Build for Production

```typescript
// build.ts
await Bun.build({
  entrypoints: ["./src/index.ts"],
  outdir: "./dist",
  target: "browser", // Workers use browser APIs
  minify: true,
  sourcemap: "external",
});
```

```bash
bun run build.ts
bunx wrangler deploy
```

## Environment Variables

```toml
# wrangler.toml
[vars]
API_URL = "https://api.example.com"

# Secrets (set via CLI)
# wrangler secret put API_KEY
```

```typescript
export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    console.log(env.API_URL);    // From vars
    console.log(env.API_KEY);    // From secrets
    return new Response("OK");
  },
};
```

## Scheduled Workers (Cron)

```typescript
export default {
  async scheduled(event: ScheduledEvent, env: Env, ctx: ExecutionContext): Promise<void> {
    console.log("Cron triggered at:", event.scheduledTime);
    // Perform scheduled task
    await env.DB.prepare("DELETE FROM logs WHERE created_at < ?")
      .bind(Date.now() - 7 * 24 * 60 * 60 * 1000)
      .run();
  },

  async fetch(request: Request, env: Env): Promise<Response> {
    return new Response("OK");
  },
};
```

```toml
# wrangler.toml
[triggers]
crons = ["0 * * * *"]  # Every hour
```

## Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `Bun API not available` | Workers use V8 | Use Web APIs only |
| `Module not found` | Build issue | Check bundler config |
| `Script too large` | Exceeds 10MB | Optimize bundle |
| `CPU time exceeded` | Long execution | Optimize or use queues |

## API Compatibility

Workers support Web APIs, NOT Bun-specific APIs:

| Available | Not Available |
|-----------|---------------|
| fetch() | Bun.file() |
| Response | Bun.serve() |
| Request | bun:sqlite |
| URL | bun:ffi |
| crypto | fs |
| TextEncoder | child_process |

## When to Load References

Load `references/bindings.md` when:
- Advanced KV/D1/R2 patterns
- Queue workers
- Service bindings

Load `references/performance.md` when:
- Bundle optimization
- Cold start reduction
- Caching strategies
