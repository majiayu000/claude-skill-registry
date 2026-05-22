---
name: "Bun Nuxt"
description: Use when running Nuxt 3 with Bun runtime, building Vue/Nuxt apps with Bun, or configuring Nuxt projects to use Bun for development and production.
---

# Bun Nuxt

Run Nuxt 3 applications with Bun for faster development.

## Quick Start

```bash
# Create new Nuxt project
bunx nuxi@latest init my-app
cd my-app

# Install dependencies
bun install

# Development
bun run dev

# Build
bun run build

# Preview production
bun run preview
```

## Project Setup

### package.json

```json
{
  "scripts": {
    "dev": "nuxt dev",
    "build": "nuxt build",
    "generate": "nuxt generate",
    "preview": "nuxt preview",
    "postinstall": "nuxt prepare"
  },
  "dependencies": {
    "nuxt": "^4.0.0",
    "vue": "^3.5.0"
  }
}
```

### Use Bun Runtime

```json
{
  "scripts": {
    "dev": "bun --bun nuxt dev",
    "build": "bun --bun nuxt build",
    "preview": "bun --bun .output/server/index.mjs"
  }
}
```

## Configuration

### nuxt.config.ts

```typescript
export default defineNuxtConfig({
  // Enable SSR
  ssr: true,

  // Nitro configuration
  nitro: {
    // Use Bun preset
    preset: "bun",

    // External packages
    externals: {
      external: ["bun:sqlite"],
    },
  },

  // Development
  devServer: {
    port: 3000,
  },

  // Modules
  modules: ["@nuxt/ui", "@pinia/nuxt"],
});
```

## Using Bun APIs

### Server Routes

```typescript
// server/api/users.ts
import { Database } from "bun:sqlite";

export default defineEventHandler(async (event) => {
  const db = new Database("data.sqlite");
  const users = db.query("SELECT * FROM users").all();
  db.close();

  return users;
});
```

### Server Middleware

```typescript
// server/middleware/auth.ts
export default defineEventHandler(async (event) => {
  const token = getHeader(event, "Authorization");

  if (!token && event.path.startsWith("/api/protected")) {
    throw createError({
      statusCode: 401,
      message: "Unauthorized",
    });
  }
});
```

### File Operations

```typescript
// server/api/files/[name].ts
export default defineEventHandler(async (event) => {
  const name = getRouterParam(event, "name");
  const file = Bun.file(`./data/${name}`);

  if (!(await file.exists())) {
    throw createError({
      statusCode: 404,
      message: "File not found",
    });
  }

  return file.text();
});
```

## Composables

### useFetch with Server Data

```vue
<script setup lang="ts">
// Fetches from server/api/users.ts
const { data: users, pending, error } = await useFetch("/api/users");
</script>

<template>
  <div v-if="pending">Loading...</div>
  <div v-else-if="error">Error: {{ error.message }}</div>
  <ul v-else>
    <li v-for="user in users" :key="user.id">{{ user.name }}</li>
  </ul>
</template>
```

### Server-Only Composables

```typescript
// composables/useDatabase.ts
export const useDatabase = () => {
  // Only runs on server
  if (process.server) {
    const { Database } = require("bun:sqlite");
    return new Database("data.sqlite");
  }
  return null;
};
```

## Server Utilities

### H3 Event Handling

```typescript
// server/api/users.post.ts
export default defineEventHandler(async (event) => {
  // Read body
  const body = await readBody(event);

  // Get query params
  const query = getQuery(event);

  // Get headers
  const auth = getHeader(event, "Authorization");

  // Get cookies
  const session = getCookie(event, "session");

  // Set cookie
  setCookie(event, "visited", "true", {
    httpOnly: true,
    maxAge: 60 * 60 * 24,
  });

  return { success: true };
});
```

### Database Utility

```typescript
// server/utils/db.ts
import { Database } from "bun:sqlite";

let db: Database | null = null;

export function getDb() {
  if (!db) {
    db = new Database("data.sqlite");
    db.run(`
      CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL
      )
    `);
  }
  return db;
}
```

```typescript
// server/api/users.ts
export default defineEventHandler(() => {
  const db = getDb();
  return db.query("SELECT * FROM users").all();
});
```

## Nitro Features

### Server Plugins

```typescript
// server/plugins/database.ts
export default defineNitroPlugin((nitroApp) => {
  // Initialize on startup
  console.log("Database initialized");

  // Cleanup on shutdown
  nitroApp.hooks.hook("close", () => {
    console.log("Closing database");
  });
});
```

### Scheduled Tasks

```typescript
// server/tasks/cleanup.ts
export default defineTask({
  meta: {
    name: "cleanup",
    description: "Clean old data",
  },
  run() {
    const db = getDb();
    db.run("DELETE FROM logs WHERE created_at < ?", [
      Date.now() - 7 * 24 * 60 * 60 * 1000,
    ]);
    return { result: "Cleaned" };
  },
});
```

## Deployment

### Build for Bun

```bash
# Build with Bun preset
NITRO_PRESET=bun bun run build

# Run production server
bun .output/server/index.mjs
```

### Docker

```dockerfile
FROM oven/bun:1 AS builder

WORKDIR /app
COPY package.json bun.lockb ./
RUN bun install --frozen-lockfile

COPY . .
RUN bun run build

FROM oven/bun:1

WORKDIR /app
COPY --from=builder /app/.output /app/.output

EXPOSE 3000

CMD ["bun", ".output/server/index.mjs"]
```

### Environment Variables

```bash
# .env
NUXT_PUBLIC_API_URL=https://api.example.com
DATABASE_URL=./data.sqlite
```

```typescript
// Access in code
const config = useRuntimeConfig();
console.log(config.public.apiUrl);
console.log(config.databaseUrl); // Server only
```

```typescript
// nuxt.config.ts
export default defineNuxtConfig({
  runtimeConfig: {
    databaseUrl: "",
    public: {
      apiUrl: "",
    },
  },
});
```

## Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `Cannot find bun:sqlite` | Wrong preset | Set `nitro.preset: "bun"` |
| `Module parse failed` | Build issue | Clear `.nuxt` and rebuild |
| `Hydration mismatch` | Server/client diff | Check async data |
| `EADDRINUSE` | Port in use | Change port or kill process |

## When to Load References

Load `references/nitro.md` when:
- Advanced Nitro configuration
- Storage drivers
- Cache handlers

Load `references/deployment.md` when:
- Edge deployment
- Cloudflare Workers
- Vercel/Netlify
