---
name: getting-started
description: Use when setting up a new Bknd project, configuring the initial schema, starting the development server, and understanding the core concepts. Covers project initialization, configuration modes, and the basic architecture.
---

# Getting Started with Bknd

Bknd is a lightweight, embeddable backend framework that provides an instant REST API, authentication, database management, and admin UI. It integrates directly into your application or runs standalone.

## What You'll Learn

- Create a new Bknd project with popular frameworks
- Configure your database and schema
- Start the development server
- Access the Admin UI
- Choose the right configuration mode

## Quick Start

The fastest way to explore Bknd:

```bash
npx bknd run
```

This starts a temporary instance with:
- In-memory SQLite database
- Admin UI at `http://localhost:3000`
- REST API at `http://localhost:3000/api`

**Note:** This is for exploration only. For a real project, follow the steps below.

## Project Setup

### Step 1: Create a Framework Project

Bknd works with any JavaScript framework. Here are common starting points:

**Vite + React:**
```bash
npx bknd create my-bknd-app --integration vite --template react
cd my-bknd-app
```

**Next.js:**
```bash
npx create-next-app@latest my-bknd-app
cd my-bknd-app
npm install bknd
```

**Bun (Standalone):**
```bash
npx bknd create my-bknd-app --integration bun
cd my-bknd-app
```

### Step 2: Create Configuration File

Create `bknd.config.ts` in your project root:

```typescript
import { createApp, em, entity, text, boolean } from "bknd";
import type { ViteBkndConfig } from "bknd/adapter/vite";

// Define your data model (Code Mode)
const schema = em({
  todos: entity("todos", {
    title: text().required(),
    done: boolean(),
  }),
});

export default {
  connection: {
    url: "file:data.db",
  },
  config: {
    data: schema.toJSON(),
  },
} satisfies ViteBkndConfig;
```

This configures:
- **Database**: SQLite stored in `data.db`
- **Schema**: A `todos` entity with `title` (text) and `done` (boolean) fields
- **Auto-generated**: Bknd automatically adds an `id` field (string/uuid)

### Step 3: Start the Development Server

**Vite + React:**

Create `server.ts`:
```typescript
import { serve } from "bknd/adapter/vite";
import config from "./bknd.config";

export default serve(config);
```

Update `vite.config.ts`:
```typescript
import { devServer } from "bknd/adapter/vite";
import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

export default defineConfig({
  plugins: [
    react(),
    devServer({
      entry: "./server.ts",
    }),
  ],
});
```

Start the server:
```bash
npm run dev
```

**Next.js:**

Create `app/api/[[...bknd]]/route.ts`:
```typescript
import { serve } from "bknd/adapter/nextjs";
import config from "@/bknd.config";

export const runtime = "nodejs";

const { handler } = serve(config);

export { handler as GET, handler as POST, handler as PUT, handler as DELETE };
```

Start the server:
```bash
npm run dev
```

**Bun (Standalone):**

Create `server.ts`:
```typescript
import { serve } from "bknd/adapter/bun";
import config from "./bknd.config";

export default {
  port: 3000,
  fetch: serve(config),
};
```

Start the server:
```bash
bun run server.ts
```

### Step 4: Verify Setup

Visit `http://localhost:3000/api/system/config` to confirm the API is running. You should see JSON configuration output.

## Accessing the Admin UI

The Admin UI provides a visual interface for managing your data and configuration.

**Mounting the Admin UI:**

**Vite + React (replace App.tsx):**
```typescript
import { Admin } from "bknd/ui";
import "bknd/dist/styles.css";

export default function App() {
  return <Admin withProvider />;
}
```

**Next.js (create app/admin/page.tsx):**
```typescript
"use client";

import { Admin } from "bknd/ui";
import "bknd/dist/styles.css";

export default function AdminPage() {
  return <Admin />;
}
```

**Bun (requires separate frontend):**

Use the Admin UI by creating a separate React app or integrating with an existing one.

Access the Admin UI at `http://localhost:3000/` (or `http://localhost:3000/admin` for Next.js).

## Configuration Modes

Bknd supports three configuration modes. Choose based on your workflow:

| Mode | Schema Definition | Type Generation | Performance | Best For |
|------|-------------------|-----------------|-------------|----------|
| **Code Mode** | TypeScript code | Static, generated once | Fastest | Production, version-controlled schemas |
| **Hybrid Mode** | Code + Admin UI | Synced on changes | Balanced | Development with UI flexibility |
| **UI Mode** | Admin UI only | Dynamic (per request) | Slowest | Prototyping, non-technical users |

### Code Mode (Recommended for Production)

Schema is defined in `bknd.config.ts`:
```typescript
const schema = em({
  todos: entity("todos", {
    title: text().required(),
    done: boolean(),
  }),
});

export default {
  config: {
    data: schema.toJSON(),
  },
} satisfies BkndConfig;
```

**Benefits:**
- Version-controlled schema
- Type-safe code
- Fastest performance (no database lookups)
- Ideal for CI/CD

### UI Mode

Remove the `config.data` object from your config:
```typescript
export default {
  connection: {
    url: "file:data.db",
  },
} satisfies BkndConfig;
```

Define entities through the Admin UI at `http://localhost:3000/`.

**Benefits:**
- Visual schema creation
- No code changes for schema updates
- Ideal for prototyping

**Trade-offs:**
- Slower performance (database reads per request)
- Not version-controlled
- Requires separate type generation step

### Hybrid Mode

Use both code and UI. Set `sync_required` in config:
```typescript
const schema = em({
  todos: entity("todos", {
    title: text().required(),
    done: boolean(),
  }),
});

export default {
  config: {
    data: schema.toJSON(),
    sync_required: true,
  },
} satisfies BkndConfig;
```

**Benefits:**
- Code defines baseline schema
- UI overrides allowed in development
- Production uses code (enforced sync)

**Workflow:**
1. Define schema in code
2. Make changes in Admin UI (development only)
3. Sync changes back to code with `npx bknd sync`

## Common CLI Commands

```bash
# Start interactive mode
npx bknd run

# Generate TypeScript types from schema
npx bknd types

# Sync UI mode changes to code (Hybrid mode)
npx bknd sync

# Start MCP server for AI integration
npx bknd mcp
```

## Database Options

Bknd supports multiple database backends:

**SQLite (Default):**
```typescript
import { nodeSqlite } from "bknd/adapter/node";

export default {
  connection: nodeSqlite({
    url: "file:data.db",
  }),
} satisfies NodeBkndConfig;
```

**PostgreSQL:**
```typescript
import { pg } from "bknd";

export default {
  connection: pg({
    url: "postgres://user:pass@host:5432/dbname",
  }),
} satisfies BkndConfig;
```

**Cloudflare D1:**
```typescript
import { d1 } from "bknd/adapter/cloudflare";

export default {
  connection: d1({
    binding: "DB", // From wrangler.toml
  }),
} satisfies D1BkndConfig;
```

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     Your Application                         │
│                  (Next.js / Astro / Remix)                   │
└──────────────────────┬──────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                        Bknd                                  │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │   Auth   │  │   Data   │  │  Media   │  │  Flows   │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              REST API (Hono)                         │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │           Admin UI (React)                            │  │
│  └──────────────────────────────────────────────────────┘  │
└──────────────────────────────┬───────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────┐
│                      Database                                │
│              (SQLite / PostgreSQL / D1 / Turso)              │
└─────────────────────────────────────────────────────────────┘
```

## Next Steps

- **[Data Schema](data-schema)** - Define entities, field types, and relationships
- **[Query](query)** - Learn the query system (where, sort, with)
- **[Auth](auth)** - Implement authentication strategies
- **[Permissions](permissions)** - Configure access control

## DOs and DON'Ts

**DO:**
- Use Code Mode for production applications
- Generate types with `npx bknd types` for type safety
- Start with `npx bknd run` to explore the Admin UI
- Use SQLite for development, switch to PostgreSQL for production

**DON'T:**
- Deploy with UI Mode in production (slow performance)
- Skip type generation (you lose TypeScript benefits)
- Define the same entity twice in `em()`
- Commit `data.db` to version control

## Common Issues

**"Module not found" errors:**
- Ensure you installed the adapter package (e.g., `@hono/vite-dev-server`)
- Check your import paths match your adapter

**Admin UI not loading:**
- Verify you imported the CSS: `import "bknd/dist/styles.css"`
- Ensure the server is running on the correct port

**Database locked errors (SQLite):**
- Enable WAL mode for better concurrent access:
  ```typescript
  nodeSqlite({
    url: "file:data.db",
    onCreateConnection: (db) => db.exec("PRAGMA journal_mode = WAL;"),
  })
  ```
