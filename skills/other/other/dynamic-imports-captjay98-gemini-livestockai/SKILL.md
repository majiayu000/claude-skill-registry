---
name: Dynamic Imports
description: Why and how to use dynamic imports in LivestockAI server functions for Cloudflare Workers compatibility
---

# Dynamic Imports

LivestockAI requires dynamic imports in server functions for Cloudflare Workers compatibility. This skill explains the pattern and why it's necessary.

## The Problem

Cloudflare Workers doesn't support `process.env` at module load time. Environment variables are only available through the `env` binding from `cloudflare:workers`, and that binding is only accessible during request handling.

```typescript
// ❌ This fails on Cloudflare Workers
// The import runs at module load time, before env is available
import { db } from '~/lib/db'

export const fn = createServerFn().handler(async () => {
  return db.selectFrom('users').execute() // db is undefined or throws
})
```

## The Solution

Use dynamic imports inside the handler function:

```typescript
// ✅ This works on Cloudflare Workers
export const fn = createServerFn().handler(async () => {
  const { getDb } = await import('~/lib/db')
  const db = await getDb()
  return db.selectFrom('users').execute()
})
```

## The `getDb()` Function

The `getDb()` function in `app/lib/db/index.ts` handles environment detection:

```typescript
async function getDatabaseUrl(): Promise<string | undefined> {
  // Try process.env first (Node.js, Bun, Vite dev server)
  if (typeof process !== 'undefined' && process.env?.DATABASE_URL) {
    return process.env.DATABASE_URL
  }

  // Fall back to Cloudflare Workers env binding
  try {
    const { env } = await import('cloudflare:workers')
    return env.DATABASE_URL
  } catch {
    return undefined
  }
}

export async function getDb(): Promise<Kysely<Database>> {
  if (!dbInstance) {
    const databaseUrl = await getDatabaseUrl()
    if (!databaseUrl) {
      throw new Error('DATABASE_URL not set')
    }
    dbInstance = new Kysely<Database>({
      dialect: new NeonDialect({ neon: neon(databaseUrl) }),
    })
  }
  return dbInstance
}
```

## When to Use Dynamic Imports

### Server Functions (ALWAYS)

```typescript
export const createBatchFn = createServerFn({ method: 'POST' })
  .inputValidator(schema)
  .handler(async ({ data }) => {
    // Dynamic import for auth
    const { requireAuth } = await import('../auth/server-middleware')
    const session = await requireAuth()

    // Dynamic import for database
    const { getDb } = await import('~/lib/db')
    const db = await getDb()

    // Dynamic import for utilities that need env
    const { checkFarmAccess } = await import('../auth/utils')
    await checkFarmAccess(session.user.id, data.farmId)

    return insertBatch(db, data)
  })
```

### CLI Scripts (NOT NEEDED)

For seeders, migrations, and CLI scripts running in Node.js/Bun, use static imports:

```typescript
// seeders/production.ts - runs in Node.js/Bun
import { db } from '~/lib/db'

await db.insertInto('users').values({...}).execute()
```

## Common Patterns

### Auth Middleware

```typescript
const { requireAuth } = await import('../auth/server-middleware')
const session = await requireAuth()
```

### Farm Access Check

```typescript
const { checkFarmAccess, getUserFarms } = await import('../auth/utils')
const hasAccess = await checkFarmAccess(userId, farmId)
```

### Database Operations

```typescript
const { getDb } = await import('~/lib/db')
const db = await getDb()
```

## Anti-Patterns

```typescript
// ❌ Static import of db
import { db } from '~/lib/db'

// ❌ Old pattern - doesn't work
const { db } = await import('~/lib/db')

// ❌ Accessing process.env directly
const url = process.env.DATABASE_URL
```

## Performance Note

Dynamic imports are cached by the JavaScript runtime. The first import loads the module, subsequent imports return the cached module. The `getDb()` function also maintains a singleton database instance.

## Related Skills

- `neon-database` - Database connection details
- `cloudflare-workers` - Deployment environment
- `tanstack-start` - Server function patterns
