---
name: Three-Layer Architecture
description: Server → Service → Repository pattern for feature organization
---

# Three-Layer Architecture

LivestockAI features follow a Server → Service → Repository pattern for clean separation of concerns.

## Layer Structure

```
app/features/batches/
├── server.ts      # Auth, validation, orchestration
├── service.ts     # Pure business logic
├── repository.ts  # Database operations
├── types.ts       # TypeScript interfaces
└── index.ts       # Public exports
```

## Layer Responsibilities

| Layer      | Responsibility                  | Side Effects   |
| ---------- | ------------------------------- | -------------- |
| Server     | Auth, validation, orchestration | Yes (auth, DB) |
| Service    | Business logic, calculations    | No (pure)      |
| Repository | Database CRUD operations        | Yes (DB)       |

## Server Layer (server.ts)

Handles authentication, input validation, and orchestrates service/repository calls:

```typescript
import { createServerFn } from '@tanstack/react-start'
import { z } from 'zod'
import { validateBatchData } from './service'
import { insertBatch } from './repository'
import { AppError } from '~/lib/errors'

export const createBatchFn = createServerFn({ method: 'POST' })
  .inputValidator(
    z.object({
      farmId: z.string().uuid(),
      species: z.string().min(1),
      initialQuantity: z.number().int().positive(),
    }),
  )
  .handler(async ({ data }) => {
    // 1. Auth
    const { requireAuth } = await import('../auth/server-middleware')
    const session = await requireAuth()

    // 2. Business logic validation (service layer)
    const validationError = validateBatchData(data)
    if (validationError) {
      throw new AppError('VALIDATION_ERROR', {
        metadata: { error: validationError },
      })
    }

    // 3. Database operation (repository layer)
    const { getDb } = await import('~/lib/db')
    const db = await getDb()
    return insertBatch(db, data)
  })
```

## Service Layer (service.ts)

Pure functions with no side effects - easy to test:

```typescript
import type { CreateBatchData } from './server'
import { multiply, toDbString } from '~/features/settings/currency'

/**
 * Calculate total cost for a batch
 * Pure function - no side effects
 */
export function calculateBatchTotalCost(
  initialQuantity: number,
  costPerUnit: number,
): string {
  if (initialQuantity <= 0 || costPerUnit < 0) {
    return toDbString(0)
  }
  return toDbString(multiply(initialQuantity, costPerUnit))
}

/**
 * Validate batch data before creation
 * Returns error message or null if valid
 */
export function validateBatchData(data: CreateBatchData): string | null {
  if (data.initialQuantity <= 0) {
    return 'Initial quantity must be greater than 0'
  }
  if (data.costPerUnit < 0) {
    return 'Cost per unit cannot be negative'
  }
  return null
}

/**
 * Calculate Feed Conversion Ratio
 */
export function calculateFCR(
  totalFeedKg: number,
  weightGainKg: number,
): number | null {
  if (totalFeedKg <= 0 || weightGainKg <= 0) {
    return null
  }
  return Math.round((totalFeedKg / weightGainKg) * 100) / 100
}
```

## Repository Layer (repository.ts)

Database operations only - no business logic:

```typescript
import type { Kysely } from 'kysely'
import type { Database } from '~/lib/db/types'

export interface BatchInsert {
  farmId: string
  species: string
  initialQuantity: number
  currentQuantity: number
  status: 'active' | 'depleted' | 'sold'
}

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

export async function updateBatch(
  db: Kysely<Database>,
  id: string,
  data: Partial<BatchInsert>,
) {
  return db
    .updateTable('batches')
    .set({ ...data, updatedAt: new Date() })
    .where('id', '=', id)
    .execute()
}
```

## Benefits

1. **Testability**: Service layer is pure functions, easy to unit test
2. **Separation**: Clear boundaries between auth, logic, and data
3. **Reusability**: Repository functions can be shared across server functions
4. **Maintainability**: Changes to one layer don't affect others

## Related Skills

- `tanstack-start` - Server function patterns
- `kysely-orm` - Repository layer queries
- `property-testing` - Testing service layer
