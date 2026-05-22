---
name: bun
description: "Bun JavaScript/TypeScript runtime and all-in-one toolkit. Covers runtime, package manager, bundler, test runner, HTTP server, WebSockets, SQLite, S3, Redis, file I/O, shell scripting, FFI, Markdown parser. Keywords: bun, bunx, bun install, bun run, bun test, bun build, Bun.serve, Bun.file, bun:sqlite, Bun.markdown."
version: "1.3.8"
release_date: "2026-01-29"
---

# Bun

All-in-one JavaScript/TypeScript toolkit: runtime, package manager, test runner, bundler.

## Quick Navigation

| Topic             | Reference                            |
| ----------------- | ------------------------------------ |
| Package Manager   | `references/package-manager.md`      |
| Project Setup     | `references/project-scaffolding.md`  |
| Development       | `references/development.md`          |
| Module System     | `references/module-system.md`        |
| TypeScript & JSX  | `references/typescript-jsx.md`       |
| Configuration     | `references/bunfig.md`               |
| HTTP Server       | `references/http-server.md`          |
| WebSockets        | `references/websockets.md`           |
| File I/O          | `references/file-io.md`              |
| SQLite            | `references/sqlite.md`               |
| S3 Storage        | `references/s3.md`                   |
| Redis             | `references/redis.md`                |
| Low-Level Network | `references/networking-low-level.md` |
| Fetch API         | `references/fetch.md`                |
| Shell Scripts     | `references/shell.md`                |
| Spawn Process     | `references/spawn.md`                |
| Workers           | `references/workers.md`              |
| Native FFI        | `references/native-interop.md`       |
| C/C++ Compile     | `references/cc.md`                   |
| Transpiler        | `references/transpiler.md`           |
| Plugins           | `references/plugins.md`              |
| FS Router         | `references/file-system-router.md`   |
| Environment Vars  | `references/env.md`                  |
| Utilities         | `references/utilities.md`            |
| Node.js Compat    | `references/nodejs-compat.md`        |

## When to Use Bun

- Running TypeScript/JSX without build step
- Fast HTTP server with native routing
- SQLite database (embedded, no deps)
- WebSocket server/client
- S3-compatible storage (AWS, R2, MinIO)
- Redis caching/pub-sub
- Cross-platform shell scripts
- **Markdown parsing** (v1.3.8+)
- Native library calls via FFI

## Core Advantages

- **4x faster startup** than Node.js
- **Native TypeScript/JSX** — no tsconfig needed
- **ESM + CommonJS** — both work seamlessly
- **Web APIs built-in** — fetch, WebSocket, etc.
- **30x faster installs** than npm

## Quick Start

```bash
# Run TypeScript directly
bun run index.ts

# Install packages
bun install

# Run package.json script
bun run dev

# Execute package binary
bunx cowsay "Hello"

# Run tests
bun test

# Build for production
bun build ./index.ts --outdir ./dist

# Bundle analysis for LLMs (v1.3.8+)
bun build ./index.ts --metafile-md --outdir ./dist
```

## Critical Rules

| Don't                  | Do                       |
| ---------------------- | ------------------------ |
| `http.createServer()`  | `Bun.serve()`            |
| `fs.readFileSync()`    | `Bun.file().text()`      |
| `better-sqlite3`       | `bun:sqlite`             |
| `child_process.exec()` | `Bun.$` or `Bun.spawn()` |
| `dotenv`               | Built-in `.env` support  |

## Essential Recipes

### HTTP Server

```ts
Bun.serve({
  port: 3000,
  fetch(req) {
    const url = new URL(req.url);
    if (url.pathname === "/api/data") {
      return Response.json({ ok: true });
    }
    return new Response("Not Found", { status: 404 });
  },
});
```

### File Operations

```ts
// Read
const content = await Bun.file("data.txt").text();

// Write
await Bun.write("output.txt", "Hello World");

// JSON
const config = await Bun.file("config.json").json();
```

### SQLite

```ts
import { Database } from "bun:sqlite";

const db = new Database("app.db");
db.run("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)");

const insert = db.prepare("INSERT INTO users (name) VALUES (?)");
insert.run("Alice");

const users = db.query("SELECT * FROM users").all();
```

### WebSocket Server

```ts
Bun.serve({
  fetch(req, server) {
    if (server.upgrade(req)) return;
    return new Response("Upgrade failed", { status: 400 });
  },
  websocket: {
    message(ws, message) {
      ws.send(`Echo: ${message}`);
    },
  },
});
```

### Shell Commands

```ts
import { $ } from "bun";

// Simple command
const files = await $`ls -la`.text();

// With variables (auto-escaped)
const name = "my file.txt";
await $`cat ${name}`;

// Piping
await $`cat data.csv | grep "pattern" | wc -l`;
```

### S3 Storage

```ts
import { s3 } from "bun";

// Upload
await s3.file("uploads/doc.pdf").write(data);

// Download
const content = await s3.file("uploads/doc.pdf").text();

// Presigned URL
const url = s3.presign("uploads/doc.pdf", { expiresIn: 3600 });
```

### Redis

```ts
import { redis } from "bun";

await redis.set("key", "value");
const value = await redis.get("key");
await redis.expire("key", 3600);
```

### Testing

```ts
import { expect, test, describe } from "bun:test";

describe("math", () => {
  test("2 + 2 = 4", () => {
    expect(2 + 2).toBe(4);
  });
});
```

## Configuration (bunfig.toml)

```toml
[run]
watch = true

[install]
registry = "https://registry.npmjs.org"

[test]
coverage = true
```

## Environment Variables

```bash
# .env files loaded automatically
DATABASE_URL=postgres://localhost/mydb
```

```ts
// Access
Bun.env.DATABASE_URL
process.env.DATABASE_URL
import.meta.env.DATABASE_URL
```

## Links

- [Documentation](https://bun.sh/docs)
- [GitHub](https://github.com/oven-sh/bun)
- [Discord](https://bun.sh/discord)
