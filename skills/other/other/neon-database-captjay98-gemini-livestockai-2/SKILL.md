---
name: Neon Database
description: Serverless PostgreSQL database patterns for LivestockAI using Neon and Kysely ORM
---

# Neon Database

LivestockAI uses [Neon](https://neon.tech) as its serverless PostgreSQL database, accessed through the Kysely query builder for type-safe SQL.

## Connection Pattern

The database connection is managed through `app/lib/db/index.ts` with two access patterns:

### Server Functions (Cloudflare Workers)

**ALWAYS use `getDb()` in server functions** - this is critical for Cloudflare Workers compatibility:

```typescript
export const myServerFn = createServerFn({ method: 'GET' }).handler(
  async () => {
    const { getDb } = await import('~/lib/db')
    const db = await getDb()
    return db.selectFrom('batches').execute()
  },
)
```

### CLI Scripts (Node.js/Bun)

For seeders, migrations, and CLI scripts, use the direct export:

```typescript
import { db } from '~/lib/db'
await db.insertInto('users').values({...}).execute()
```

## Why `getDb()`?

Cloudflare Workers doesn't support `process.env`. Environment variables come from the `env` binding via `cloudflare:workers`, which is only available during request handling. The `getDb()` function:

1. Tries `process.env.DATABASE_URL` first (Node.js/Bun)
2. Falls back to `cloudflare:workers` env binding
3. Creates a singleton Kysely instance

## Common Mistakes

```typescript
// ❌ WRONG - breaks on Cloudflare Workers
import { db } from '~/lib/db'
export const fn = createServerFn().handler(async () => {
  return db.selectFrom('users').execute()
})

// ❌ WRONG - old pattern, doesn't work
const { db } = await import('~/lib/db')

// ✅ CORRECT
const { getDb } = await import('~/lib/db')
const db = await getDb()
```

## Environment Variables

```bash
# Local development (.env or .dev.vars)
DATABASE_URL=postgres://user:pass@ep-xxx.region.neon.tech/livestockai?sslmode=require

# Production (Cloudflare secrets)
wrangler secret put DATABASE_URL

# Test database
DATABASE_URL_TEST=postgres://user:pass@ep-xxx.region.neon.tech/livestockai_test?sslmode=require
```

## Database Schema

The schema is defined in `app/lib/db/types.ts` with 23+ tables including:

| Table               | Purpose                                 |
| ------------------- | --------------------------------------- |
| `users`             | User accounts (Better Auth)             |
| `user_settings`     | Preferences (currency, units, language) |
| `farms`             | Farm entities                           |
| `farm_modules`      | Enabled livestock types per farm        |
| `batches`           | Livestock batches (all 6 types)         |
| `mortality_records` | Death tracking                          |
| `feed_records`      | Feed consumption                        |
| `weight_samples`    | Growth tracking                         |
| `sales`             | Revenue records                         |
| `expenses`          | Cost tracking                           |
| `invoices`          | Customer invoices                       |

## Migrations

Migrations are in `app/lib/db/migrations/`:

```bash
# Run migrations
bun run db:migrate

# Rollback
bun run db:rollback

# Reset (drop all + migrate)
bun run db:reset
```

Migration naming: `YYYY-MM-DD-NNN-description.ts`

## Kysely Query Examples

```typescript
// Select with joins
const batches = await db
  .selectFrom('batches')
  .leftJoin('farms', 'farms.id', 'batches.farmId')
  .select(['batches.id', 'batches.species', 'farms.name as farmName'])
  .where('batches.status', '=', 'active')
  .execute()

// Insert with returning
const result = await db
  .insertInto('batches')
  .values({ farmId, species, initialQuantity })
  .returning('id')
  .executeTakeFirstOrThrow()

// Update
await db
  .updateTable('batches')
  .set({ status: 'depleted' })
  .where('id', '=', batchId)
  .execute()

// Aggregate
const stats = await db
  .selectFrom('sales')
  .select(sql<number>`sum(quantity)`.as('totalSold'))
  .where('batchId', '=', batchId)
  .executeTakeFirst()
```

## Related Skills

- `kysely-orm` - Detailed Kysely patterns
- `cloudflare-workers` - Deployment environment
- `three-layer-architecture` - Repository layer patterns
