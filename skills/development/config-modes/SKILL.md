---
name: config-modes
description: Use when choosing a Bknd configuration mode (UI-only, Code-only, Hybrid), setting up mode switching between development and production, running Bknd CLI commands with TypeScript config files, or using mode helpers for automated syncing. Covers when to use each mode, setup patterns, CLI execution (bknd run, bknd sync), and v0.20.0 improvements.
---

# Configuration Modes

Bknd supports three configuration modes that determine where and how your application's configuration (entity schemas, auth settings, media config) is stored and managed.

## What You'll Learn

- Choose between UI-only, Code-only, and Hybrid modes
- Set up mode switching for development vs production
- Use mode helpers for automated syncing
- Understand v0.20.0 improvements

## Quick Reference

| Mode | Config Storage | Best For | Read-Only |
|------|---------------|----------|-----------|
| UI-only (`"db"`) | Database (`__bknd` table) | Prototyping, content apps | No |
| Code-only (`"code"`) | TypeScript config file | Production, serverless | Yes |
| Hybrid | File-based (dev) + Code (prod) | Visual dev + code prod | Yes (prod) |

## UI-Only Mode (Default)

Configuration is stored in the database and can be modified at runtime through the Admin UI.

**When to use:**
- Rapid prototyping and iteration
- Content management systems (non-technical users manage schemas)
- Quick starts without strict version control

**Setup:**

```typescript
import type { BkndConfig } from "bknd";

export default {
  config: { /* ... */ },  // Applied only if database is empty
  options: {
    mode: "db"  // This is the default
  }
} satisfies BkndConfig;
```

**Benefits:**
- Visual configuration through Admin UI
- Runtime changes without code deployment
- Automatic database migrations
- Configuration versioning in database

**Trade-offs:**
- Configuration changes not tracked in git
- Configuration drift between environments
- Harder to audit changes

## Code-Only Mode

Configuration is loaded from your TypeScript config and treated as immutable. The app runs in read-only mode by default.

**When to use:**
- Production environments requiring strict version control
- Serverless/Edge deployments with restricted database writes
- Multi-tenant SaaS requiring predictable configuration
- Compliance requiring code review for changes

**Setup:**

```typescript
import type { BkndConfig } from "bknd";
import { em, entity, text, boolean } from "bknd";
import { secureRandomString } from "bknd/utils";

const schema = em({
  todos: entity("todos", {
    title: text(),
    done: boolean(),
  }),
});

export default {
  config: {
    data: schema.toJSON(),
    auth: {
      enabled: true,
      jwt: {
        secret: secureRandomString(64),
      },
    }
  },
  options: {
    mode: "code",  // Configuration is always applied
  }
} satisfies BkndConfig;
```

**Benefits:**
- Configuration is version-controlled in git
- Changes require code review and deployment
- Prevents accidental configuration changes
- Easier to audit and roll back

**Trade-offs:**
- No runtime configuration changes
- Requires deployment for configuration updates
- Admin UI becomes read-only for configuration
- Must manually sync schema: `npx bknd sync --force`

## Hybrid Mode

Configure your backend visually while in development, and use a read-only configuration in production. This provides the best of both worlds.

**When to use:**
- Teams that want visual development with production safety
- Applications with separate dev/prod workflows
- Projects needing flexibility in development but stability in production

**Setup:**

```typescript
import type { BkndConfig } from "bknd";
import appConfig from "./appconfig.json" with { type: "json" };

export default {
  config: appConfig,
  options: {
    mode: process.env.NODE_ENV === "development" ? "db" : "code",
    manager: {
      secrets: process.env
    }
  }
} satisfies BkndConfig;
```

## Mode Helpers

Bknd provides `code()` and `hybrid()` helpers that automate syncing and mode switching.

### Code Mode Helper

For serverless deployments requiring schema in code:

```typescript
import { code, type CodeMode } from "bknd/modes";
import { type BunBkndConfig, writer } from "bknd/adapter/bun";

const config = {
  connection: { url: "file:test.db" },
  writer,  // Required for type syncing
  isProduction: Bun.env.NODE_ENV === "production",
  typesFilePath: "bknd-types.d.ts",
  syncSchema: {
    force: true,
    drop: true,
  }
} satisfies CodeMode<BunBkndConfig>;

export default code(config);
```

**Features:**
- Built-in type file generation
- Automatic schema syncing when `syncSchema.force: true`
- Production mode detection

### Hybrid Mode Helper

**v0.20.0 Improvements:**
- Reader returns objects directly (no `JSON.parse()` needed)
- Automatic schema syncing when `sync_required` flag triggered
- Faster production startup (validation skipped)

```typescript
import { hybrid, type HybridMode } from "bknd/modes";
import { type BunBkndConfig, writer, reader } from "bknd/adapter/bun";

const config = {
  connection: { url: "file:test.db" },
  writer,  // Required for type/config syncing
  reader,  // Reader can return string OR object
  secrets: await Bun.file(".env.local").json(),
  isProduction: Bun.env.NODE_ENV === "production",
  typesFilePath: "bknd-types.d.ts",
  configFilePath: "bknd-config.json",
  syncSecrets: {
    outFile: ".env.local",
    format: "env",
    includeSecrets: true,
  },
  syncSchema: {
    force: true,  // Syncs schema when sync_required flag is true
    drop: true,
  },
} satisfies HybridMode<BunBkndConfig>;

export default hybrid(config);
```

**Features:**
- Automatic mode switching (db → code)
- Built-in syncing of config, types, and secrets
- Automatic schema sync in development
- Object-based config loading (no JSON.parse needed)
- Production validation skip for performance

## Running CLI with TypeScript Config

If your config file uses a `.ts` extension (e.g., `bknd.config.ts`), the CLI requires a TypeScript-aware runtime.

### Node.js (>=v22.6.0)

```bash
node --experimental-strip-types node_modules/.bin/bknd run
node --experimental-strip-types node_modules/.bin/bknd sync --force
```

### Using tsx

```bash
npx tsx node_modules/.bin/bknd run
npx tsx node_modules/.bin/bknd sync --force
```

### Using Bun

Required if your config uses Bun-specific APIs or the Bun adapter:

```bash
bun node_modules/.bin/bknd run
bun node_modules/.bin/bknd sync --seed --force
```

**Note:** Standard `npx bknd` commands work if your config is `.js` or `.mjs`.

## Recommended Workflow

Use UI-only mode in development, Code-only mode in production (Hybrid).

### Development (UI-only)

```bash
# Start with Admin UI and runtime configuration
npx bknd run
# Or in your framework app with mode: "db"
```

1. Use Admin UI to experiment with schemas
2. Test different configurations
3. Export configuration when ready for production

### Export for Production

```bash
# Export configuration
npx bknd config --out appconfig.json

# Export secrets to environment file
npx bknd secrets --out .env.local --format env

# Generate types for your schema
npx bknd types --out bknd-types.d.ts
```

### Production (Code-only)

```typescript
import appConfig from "./appconfig.json" with { type: "json" };

export default {
  config: appConfig,
  options: {
    mode: "code",
    manager: {
      secrets: process.env
    }
  }
} satisfies BkndConfig;
```

### Sync Database (if needed)

```bash
npx bknd sync --force
```

## Decision Tree

Choose your configuration mode:

```
Need runtime configuration changes?
├─ Yes → Use UI-only mode
│   └─ Development or content-managed apps
└─ No → Need strict version control?
    ├─ Yes → Use Code-only mode
    │   └─ Production or compliant environments
    └─ No → Want best of both worlds?
        ├─ Yes → Use Hybrid mode
        │   └─ Visual dev + code production
        └─ No → Use UI-only mode (default)
            └─ Simple prototypes
```

## DOs and DON'Ts

### DO
- Use UI-only mode for rapid prototyping
- Use Code-only mode for production deployments
- Use Hybrid mode to switch between dev/prod workflows
- Export config/secrets/types when moving from dev to production
- Use mode helpers (`code()`, `hybrid()`) for automated syncing
- Track configuration changes in git for Code-only mode
- Set `implicit_allow: false` for production roles

### DON'T
- Use UI-only mode in production (configuration not versioned)
- Forget to sync database with `npx bknd sync --force` in Code mode
- Skip exporting secrets when moving to production
- Use Hybrid mode if you only need one mode (simpler is better)
- Forget to set `writer` in mode helpers (required for syncing)
- Ignore `sync_required` flag in Hybrid mode (triggers auto-sync)

## Related Skills

- `getting-started` - Project setup and initial configuration
- `database` - Database connection and adapter configuration
- `deploy` - Production deployment strategies
