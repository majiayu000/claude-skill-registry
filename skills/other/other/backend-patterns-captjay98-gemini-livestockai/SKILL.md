---
name: backend-patterns
description: |
  Backend development patterns for LivestockAI. Use when implementing server functions,
  database operations, Kysely queries, or working with the three-layer architecture
  (server → service → repository).
---

# Backend Development Patterns

You are a backend specialist for LivestockAI, expert in TanStack Start, Kysely ORM, and Cloudflare Workers.

## Critical: Database Access Pattern

**Cloudflare Workers does NOT support `process.env`**. Always use async `getDb()`:

```typescript
// ✅ CORRECT - Works on Cloudflare Workers
export const myFunction = createServerFn({ method: 'POST' })
  .inputValidator(schema)
  .handler(async ({ data }) => {
    const { getDb } = await import('~/lib/db')
    const db = await getDb()
    // ... use db
  })

// ❌ WRONG - Breaks on Cloudflare
import { db } from '~/lib/db'
```

## Three-Layer Architecture

### Layer 1: Server (server.ts)

- Auth middleware via `requireAuth()`
- Input validation with Zod
- Orchestrates service and repository calls
- Error handling with AppError

```typescript
export const createBatchFn = createServerFn({ method: 'POST' })
  .inputValidator(createBatchSchema)
  .handler(async ({ data }) => {
    const { requireAuth } = await import('../auth/server-middleware')
    const session = await requireAuth()

    // Validate business rules (service layer)
    const error = validateBatchData(data)
    if (error) throw new AppError('VALIDATION_ERROR', error)

    // Database operation (repository layer)
    const { getDb } = await import('~/lib/db')
    const db = await getDb()
    return insertBatch(db, { ...data, userId: session.user.id })
  })
```

### Layer 2: Service (service.ts)

- Pure functions (no side effects)
- Business logic and calculations
- Easy to unit test

```typescript
export function calculateFCR(feedKg: number, weightGain: number): number {
  if (weightGain <= 0) return 0
  return Number((feedKg / weightGain).toFixed(2))
}

export function validateBatchData(data: CreateBatchData): string | null {
  if (data.initialQuantity <= 0) return 'Quantity must be positive'
  if (data.costPerUnit < 0) return 'Cost cannot be negative'
  return null
}
```

### Layer 3: Repository (repository.ts)

- Database operations only
- Receives `db` as parameter
- No business logic

```typescript
export async function insertBatch(
  db: Kysely<Database>,
  data: BatchInsert,
): Promise<string> {
  const result = await db
    .insertInto('batches')
    .values(data)
    .returning('id')
    .executeTakeFirstOrThrow()
  return result.id
}
```

## Zod Validation Patterns

```typescript
// Always use Zod, never identity functions
const schema = z.object({
  farmId: z.string().uuid(),
  batchName: z.string().min(1).max(100),
  quantity: z.number().int().positive(),
  status: z.enum(['active', 'depleted', 'sold']),
  date: z.coerce.date(),
  notes: z.string().max(500).nullish(),
})
```

## Kysely Query Patterns

```typescript
// Prefer explicit columns
const batches = await db
  .selectFrom('batches')
  .select(['id', 'batchName', 'status', 'quantity'])
  .where('farmId', '=', farmId)
  .where('deletedAt', 'is', null) // Soft delete
  .orderBy('createdAt', 'desc')
  .execute()

// Joins
const batchesWithFarm = await db
  .selectFrom('batches')
  .leftJoin('farms', 'farms.id', 'batches.farmId')
  .select(['batches.id', 'batches.batchName', 'farms.name as farmName'])
  .execute()

// Transactions
await db.transaction().execute(async (trx) => {
  await trx.insertInto('mortality_records').values(data).execute()
  await trx
    .updateTable('batches')
    .set({ quantity: sql`quantity - ${data.count}` })
    .where('id', '=', data.batchId)
    .execute()
})
```

## Error Handling

```typescript
import { AppError } from '~/lib/errors'

// Throw structured errors
throw new AppError('NOT_FOUND', 'Batch not found')
throw new AppError('UNAUTHORIZED', 'Access denied')
throw new AppError('VALIDATION_ERROR', 'Invalid input')
```
