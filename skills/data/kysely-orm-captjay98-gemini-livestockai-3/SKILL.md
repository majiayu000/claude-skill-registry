---
name: Kysely ORM
description: Type-safe SQL query building with Kysely in LivestockAI
---

# Kysely ORM

LivestockAI uses [Kysely](https://kysely.dev) as its type-safe SQL query builder. Kysely provides compile-time SQL validation and full TypeScript inference.

## Database Types

The database schema is defined in `app/lib/db/types.ts`:

```typescript
export interface Database {
  users: UsersTable
  batches: BatchesTable
  farms: FarmsTable
  sales: SalesTable
  // ... 23+ tables
}

export interface BatchesTable {
  id: Generated<string>
  farmId: string
  livestockType: 'poultry' | 'fish' | 'cattle' | 'goats' | 'sheep' | 'bees'
  species: string
  initialQuantity: number
  currentQuantity: number
  status: 'active' | 'depleted' | 'sold'
  createdAt: Generated<Date>
  updatedAt: Generated<Date>
}
```

## Query Patterns

### Select with Explicit Columns

```typescript
// Prefer explicit columns over selectAll()
const batches = await db
  .selectFrom('batches')
  .select(['id', 'species', 'currentQuantity', 'status'])
  .where('farmId', '=', farmId)
  .execute()
```

### Joins

```typescript
const batchesWithFarm = await db
  .selectFrom('batches')
  .leftJoin('farms', 'farms.id', 'batches.farmId')
  .leftJoin('breeds', 'breeds.id', 'batches.breedId')
  .select([
    'batches.id',
    'batches.species',
    'farms.name as farmName',
    'breeds.displayName as breedName',
  ])
  .where('batches.status', '=', 'active')
  .execute()
```

### Insert with Returning

```typescript
const result = await db
  .insertInto('batches')
  .values({
    farmId,
    livestockType: 'poultry',
    species: 'Broiler',
    initialQuantity: 500,
    currentQuantity: 500,
    status: 'active',
  })
  .returning('id')
  .executeTakeFirstOrThrow()

console.log(result.id) // UUID of new batch
```

### Update

```typescript
await db
  .updateTable('batches')
  .set({
    currentQuantity: newQuantity,
    status: 'depleted',
    updatedAt: new Date(),
  })
  .where('id', '=', batchId)
  .execute()
```

### Delete

```typescript
await db.deleteFrom('batches').where('id', '=', batchId).execute()
```

### Aggregations

```typescript
import { sql } from 'kysely'

const stats = await db
  .selectFrom('sales')
  .select([
    sql<number>`count(*)`.as('totalSales'),
    sql<number>`sum(quantity)`.as('totalQuantity'),
    sql<string>`sum(total_amount)`.as('totalRevenue'),
  ])
  .where('batchId', '=', batchId)
  .executeTakeFirst()
```

### Complex Filters

```typescript
const batches = await db
  .selectFrom('batches')
  .selectAll()
  .where((eb) =>
    eb.or([
      eb('species', 'ilike', `%${search}%`),
      eb('batchName', 'ilike', `%${search}%`),
    ]),
  )
  .where('status', '=', 'active')
  .orderBy('acquisitionDate', 'desc')
  .limit(pageSize)
  .offset((page - 1) * pageSize)
  .execute()
```

### Subqueries

```typescript
const batchesWithStats = await db
  .selectFrom('batches')
  .select([
    'batches.id',
    'batches.species',
    db
      .selectFrom('mortality_records')
      .select(sql<number>`sum(quantity)`.as('total'))
      .whereRef('mortality_records.batchId', '=', 'batches.id')
      .as('totalMortality'),
  ])
  .execute()
```

## Repository Pattern

Database operations are isolated in repository files:

```typescript
// app/features/batches/repository.ts
import type { Kysely } from 'kysely'
import type { Database } from '~/lib/db/types'

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

export async function getBatchById(db: Kysely<Database>, id: string) {
  return db
    .selectFrom('batches')
    .selectAll()
    .where('id', '=', id)
    .executeTakeFirst()
}
```

## Type Helpers

```typescript
import type { Insertable, Selectable, Updateable } from 'kysely'
import type { BatchesTable } from '~/lib/db/types'

// For insert operations
type BatchInsert = Insertable<BatchesTable>

// For select results
type Batch = Selectable<BatchesTable>

// For update operations
type BatchUpdate = Updateable<BatchesTable>
```

## Transactions

```typescript
await db.transaction().execute(async (trx) => {
  // All operations use trx instead of db
  await trx.insertInto('sales').values(saleData).execute()
  await trx
    .updateTable('batches')
    .set({ currentQuantity: newQuantity })
    .where('id', '=', batchId)
    .execute()
})
```

## Related Skills

- `neon-database` - Database connection
- `three-layer-architecture` - Repository layer
- `dynamic-imports` - Database access in server functions
