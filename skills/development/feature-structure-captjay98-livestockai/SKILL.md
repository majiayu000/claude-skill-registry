---
name: Feature Structure
description: How to organize features in LivestockAI
---

# Feature Structure

Each major feature in LivestockAI has its own directory in `app/features/`.

## Directory Layout

```
app/features/batches/
├── server.ts        # Server functions (createServerFn)
├── service.ts       # Pure business logic
├── repository.ts    # Database operations
├── types.ts         # TypeScript interfaces
├── constants.ts     # Feature constants
└── index.ts         # Public exports
```

## File Purposes

### server.ts

Server functions that handle auth, validation, and orchestration:

```typescript
export const createBatchFn = createServerFn({ method: 'POST' })
  .inputValidator(schema)
  .handler(async ({ data }) => {
    const session = await requireAuth()
    const error = validateBatchData(data)
    if (error) throw new AppError('VALIDATION_ERROR')
    return insertBatch(db, data)
  })
```

### service.ts

Pure business logic functions (no side effects):

```typescript
export function calculateFCR(
  feedKg: number,
  weightGain: number,
): number | null {
  if (feedKg <= 0 || weightGain <= 0) return null
  return Math.round((feedKg / weightGain) * 100) / 100
}

export function validateBatchData(data: CreateBatchData): string | null {
  if (data.initialQuantity <= 0) return 'Quantity must be positive'
  return null
}
```

### repository.ts

Database operations only:

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

### types.ts

TypeScript interfaces:

```typescript
export interface CreateBatchData {
  farmId: string
  species: string
  initialQuantity: number
  costPerUnit: number
}

export interface BatchStats {
  mortality: { rate: number; total: number }
  feed: { totalKg: number; fcr: number | null }
  sales: { totalRevenue: number }
}
```

### index.ts

Public exports:

```typescript
export { createBatchFn, getBatchesFn } from './server'
export { calculateFCR, validateBatchData } from './service'
export type { CreateBatchData, BatchStats } from './types'
```

## Component Organization

UI components go in `app/components/`:

```
app/components/
├── ui/              # Base components (shadcn/ui)
├── dialogs/         # Create/edit modal dialogs
├── layout/          # Layout components
└── batches/         # Feature-specific components
    ├── batch-columns.tsx
    ├── batch-filters.tsx
    └── batches-skeleton.tsx
```

## Route Organization

Routes go in `app/routes/`:

```
app/routes/
├── _auth/           # Protected routes
│   ├── batches/
│   │   ├── index.tsx
│   │   └── $batchId.tsx
│   └── dashboard.tsx
└── index.tsx        # Public landing
```

## Related Skills

- `three-layer-architecture` - Layer responsibilities
- `tanstack-router` - Route organization
- `tanstack-start` - Server function patterns
