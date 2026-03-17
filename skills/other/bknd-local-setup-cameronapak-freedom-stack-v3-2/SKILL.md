---
name: bknd-local-setup
description: Use when setting up a new Bknd project locally or configuring local development environment. Covers CLI installation, project creation, runtime adapters, config file setup, and development server options.
---

# Local Development Setup

Set up a Bknd local development environment from scratch.

## Prerequisites

- Node.js 18+ or Bun 1.0+
- npm, yarn, pnpm, or bun package manager
- Terminal/command line access

## When to Use UI Mode

- Browsing admin panel at `http://localhost:3000/admin`
- Exploring entities and data visually
- Testing auth flows manually

**Note:** Initial project setup requires CLI/code.

## When to Use Code Mode

- Creating new Bknd project
- Configuring database connection
- Defining schema
- Running development server
- All initial setup tasks

## Code Approach

### Step 1: Create New Project (Interactive)

Quickest way to start:

```bash
# Interactive project creation
npx bknd create my-app

# Follow prompts:
# - Project name
# - Database type (SQLite recommended for local dev)
# - Include example schema?
```

This creates project structure with:
- `bknd.config.ts` - Main configuration
- `package.json` - Dependencies
- `.env` - Environment variables template

### Step 2: Install Dependencies

```bash
cd my-app

# npm
npm install

# bun (faster)
bun install

# pnpm
pnpm install
```

### Step 3: Run Development Server

```bash
# Default (port 3000, file-based SQLite)
npx bknd run

# In-memory database (fastest for prototyping, data lost on restart)
npx bknd run --memory

# Custom port
npx bknd run --port 8080

# Don't auto-open browser
npx bknd run --no-open

# Specify runtime explicitly
npx bknd run --server bun
npx bknd run --server node
```

Server starts at `http://localhost:3000` with:
- API: `/api/data/*`, `/api/auth/*`, `/api/media/*`
- Admin UI: `/admin`

## Alternative: Manual Setup

### Step 1: Initialize Package

```bash
mkdir my-bknd-app && cd my-bknd-app
npm init -y
npm install bknd
```

### Step 2: Create Config File

Create `bknd.config.ts`:

```typescript
import type { CliBkndConfig } from "bknd";
import { em, entity, text, boolean } from "bknd";

// Define schema
const schema = em({
  todos: entity("todos", {
    title: text().required(),
    done: boolean(),
  }),
});

// Register types
type Database = (typeof schema)["DB"];
declare module "bknd" {
  interface DB extends Database {}
}

export default {
  app: (env) => ({
    connection: {
      url: env.DB_URL ?? "file:data.db",
    },
    schema,
  }),
} satisfies CliBkndConfig;
```

### Step 3: Create Entry File (Optional)

For programmatic control, create `index.ts`:

```typescript
import { serve } from "bknd/adapter/bun";
import { em, entity, text, boolean } from "bknd";

const schema = em({
  todos: entity("todos", {
    title: text().required(),
    done: boolean(),
  }),
});

serve({
  connection: { url: "file:data.db" },
  config: {
    data: schema.toJSON(),
  },
});
```

Run with:

```bash
# Bun
bun run index.ts

# Node (requires tsx or ts-node)
npx tsx index.ts
```

## Runtime Adapters

### Bun (Recommended for Speed)

```typescript
import { serve } from "bknd/adapter/bun";

serve({
  connection: { url: "file:data.db" },
});
```

### Node.js

```typescript
import { serve } from "bknd/adapter/node";

serve({
  connection: { url: "file:data.db" },
});
```

### Framework Integrations

**Next.js:**
```typescript
// app/api/bknd/[[...bknd]]/route.ts
import { createHandler } from "bknd/adapter/nextjs";
export const { GET, POST, PUT, DELETE, PATCH } = createHandler(config);
```

**Astro:**
```typescript
// src/pages/api/[...bknd].ts
import { createHandler } from "bknd/adapter/astro";
export const ALL = createHandler(config);
```

**React Router (Remix):**
```typescript
// app/routes/api.$.tsx
import { createHandler } from "bknd/adapter/react-router";
export const loader = createHandler(config);
export const action = createHandler(config);
```

## CLI Options Reference

| Option | Description | Default |
|--------|-------------|---------|
| `-p, --port <port>` | Server port | 3000 |
| `-m, --memory` | Use in-memory database | - |
| `--server <server>` | Runtime: `node` or `bun` | Auto-detected |
| `--no-open` | Don't auto-open browser | Opens by default |
| `-c, --config <path>` | Config file path | Auto-detected |
| `--db-url <url>` | Database URL override | - |

## Config File Detection

Bknd auto-detects config files (in order):
- `bknd.config.ts`
- `bknd.config.js`
- `bknd.config.mjs`
- `bknd.config.cjs`
- `bknd.config.json`

## Project Structure

### Recommended Layout

```
my-bknd-app/
├── bknd.config.ts      # Main configuration
├── bknd-types.d.ts     # Generated types (run: npx bknd types)
├── .env                # Environment variables
├── .dev.vars           # Dev-specific overrides (optional)
├── data.db             # SQLite file (auto-created)
├── uploads/            # Local media storage (if using local adapter)
└── package.json
```

### Framework Integration Layout

```
my-nextjs-app/
├── app/
│   ├── api/
│   │   └── bknd/
│   │       └── [[...bknd]]/
│   │           └── route.ts
│   └── admin/
│       └── page.tsx
├── bknd.config.ts
├── bknd-types.d.ts
└── .env.local
```

## Generate TypeScript Types

After defining schema, generate types for IDE support:

```bash
# Generate to bknd-types.d.ts (default)
npx bknd types

# Custom output
npx bknd types -o types/bknd.d.ts

# Print to console (debug)
npx bknd types --dump
```

## Database Options for Local Dev

| Database | URL Format | Best For |
|----------|------------|----------|
| In-memory SQLite | `:memory:` or `--memory` flag | Quick prototyping |
| File SQLite | `file:data.db` | Persistent local dev |
| LibSQL (Turso) | `libsql://your-db.turso.io` | Remote dev database |

### In-Memory (Ephemeral)

```bash
npx bknd run --memory
```

Data resets on server restart. Best for rapid prototyping.

### File-Based SQLite (Persistent)

```bash
npx bknd run
# or explicitly:
npx bknd run --db-url "file:data.db"
```

Data persists in `data.db` file.

### Reset Database

```bash
# Delete SQLite file for fresh start
rm data.db

# Then restart server
npx bknd run
```

## Hot Reload

Schema changes require server restart. Use watch mode:

```bash
# Bun
bun --watch index.ts

# Node with nodemon
npx nodemon --exec "npx bknd run"
```

## Debug Commands

```bash
# Show internal paths
npx bknd debug paths

# Show all registered routes
npx bknd debug routes

# CLI help
npx bknd --help
npx bknd run --help
```

## Verification

After setup, verify everything works:

**1. Server running:**
```bash
curl http://localhost:3000/api/data
# Should return entity list
```

**2. Admin panel accessible:**
Open `http://localhost:3000/admin` in browser

**3. Types generated:**
```bash
npx bknd types
# Check bknd-types.d.ts created
```

## Common Pitfalls

### Config File Not Found

**Problem:** `Config file could not be resolved` error

**Fix:** Ensure config file exists with correct extension:
```bash
# Check file exists
ls bknd.config.*

# Or specify explicitly
npx bknd run -c ./bknd.config.ts
```

### Port Already in Use

**Problem:** `EADDRINUSE: address already in use`

**Fix:** Use different port or kill existing process:
```bash
# Use different port
npx bknd run --port 3001

# Or find and kill process
lsof -i :3000
kill -9 <PID>
```

### Database Permission Error

**Problem:** `SQLITE_CANTOPEN: unable to open database file`

**Fix:** Ensure write permissions in directory:
```bash
# Check permissions
ls -la

# Fix permissions
chmod 755 .
```

### TypeScript Errors with em()

**Problem:** Type errors when using `em()` return value

**Fix:** Remember `em()` returns schema definition, not EntityManager:
```typescript
// WRONG - em() is schema builder only
const em = em({ ... });
em.repo("posts").find();  // ERROR

// CORRECT - use api.data for queries
const api = new Api({ url: "http://localhost:3000" });
api.data.readMany("posts");
```

### Bun Not Found

**Problem:** `bun: command not found`

**Fix:** Install Bun or use Node:
```bash
# Install Bun
curl -fsSL https://bun.sh/install | bash

# Or use Node runtime
npx bknd run --server node
```

### Windows Path Issues

**Problem:** File paths not resolving on Windows

**Fix:** Use forward slashes:
```typescript
// WRONG
connection: { url: "file:C:\\data\\my.db" }

// CORRECT
connection: { url: "file:C:/data/my.db" }
// or relative
connection: { url: "file:data.db" }
```

## DOs and DON'Ts

**DO:**
- Use `--memory` flag for quick experiments
- Use `file:data.db` for persistent development
- Generate types after schema changes
- Commit `bknd.config.ts` to version control
- Use `.env` for environment-specific values

**DON'T:**
- Commit `data.db` to version control (add to `.gitignore`)
- Commit `.env` with secrets (use `.env.example` template)
- Use in-memory database when you need data persistence
- Forget to restart server after schema changes
- Try to use `em()` result as EntityManager

## Related Skills

- **bknd-env-config** - Configure environment variables
- **bknd-create-entity** - Create entities in your schema
- **bknd-client-setup** - Set up SDK in frontend
- **bknd-debugging** - Debug common issues
- **bknd-deploy-hosting** - Deploy to production
