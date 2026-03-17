---
name: TanStack Start
description: Server-side rendering and server functions with TanStack Start in LivestockAI
---

# TanStack Start

LivestockAI uses [TanStack Start](https://tanstack.com/start) for server-side rendering (SSR) and server functions. It provides a full-stack React framework built on TanStack Router.

## Server Functions

Server functions are the primary way to interact with the database. They run on the server and are type-safe end-to-end.

### Basic Pattern

```typescript
import { createServerFn } from '@tanstack/react-start'
import { z } from 'zod'

export const getBatchesFn = createServerFn({ method: 'GET' })
  .inputValidator(
    z.object({
      farmId: z.string().uuid().optional(),
      status: z.enum(['active', 'depleted', 'sold']).optional(),
    }),
  )
  .handler(async ({ data }) => {
    // Auth check
    const { requireAuth } = await import('../auth/server-middleware')
    const session = await requireAuth()

    // Database access (dynamic import for Cloudflare)
    const { getDb } = await import('~/lib/db')
    const db = await getDb()

    return db.selectFrom('batches').where('farmId', '=', data.farmId).execute()
  })
```

### Three-Layer Architecture

Server functions orchestrate the three layers:

```typescript
// server.ts - Orchestration layer
export const createBatchFn = createServerFn({ method: 'POST' })
  .inputValidator(createBatchSchema)
  .handler(async ({ data }) => {
    // 1. Auth
    const { requireAuth } = await import('../auth/server-middleware')
    const session = await requireAuth()

    // 2. Business logic (service layer)
    const validationError = validateBatchData(data.batch)
    if (validationError) {
      throw new AppError('VALIDATION_ERROR', {
        metadata: { error: validationError },
      })
    }

    // 3. Database (repository layer)
    const { getDb } = await import('~/lib/db')
    const db = await getDb()
    return insertBatch(db, data.batch)
  })
```

## Input Validation

**ALWAYS use Zod validators**, not identity functions:

```typescript
// ✅ Correct - Zod validation
.inputValidator(z.object({
  farmId: z.string().uuid(),
  quantity: z.number().int().positive(),
  date: z.coerce.date(),
}))

// ❌ Wrong - No validation
.inputValidator((data: { farmId: string }) => data)
```

### Common Zod Patterns

```typescript
// UUID
farmId: z.string().uuid()

// Optional UUID
farmId: z.string().uuid().optional()

// Enum
status: z.enum(['active', 'depleted', 'sold'])

// Numbers
page: z.number().int().positive()
amount: z.number().nonnegative()

// Dates
date: z.coerce.date()

// Strings
name: z.string().min(1).max(100)
notes: z.string().max(500).nullish()
```

## Calling Server Functions

### From Route Loaders

```typescript
export const Route = createFileRoute('/_auth/batches/')({
  loader: async ({ deps }) => {
    return getBatchesForFarmFn({ data: deps })
  },
})
```

### From Components (Mutations)

```typescript
import { useMutation } from '@tanstack/react-query'

function BatchForm() {
  const mutation = useMutation({
    mutationFn: (data) => createBatchFn({ data: { batch: data } }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['batches'] })
    },
  })

  return <form onSubmit={() => mutation.mutate(formData)}>...</form>
}
```

## Error Handling

Use the `AppError` class for structured errors:

```typescript
import { AppError } from '~/lib/errors'

.handler(async ({ data }) => {
  const batch = await getBatchById(data.batchId)
  if (!batch) {
    throw new AppError('BATCH_NOT_FOUND', { metadata: { batchId: data.batchId } })
  }

  const hasAccess = await checkFarmAccess(userId, batch.farmId)
  if (!hasAccess) {
    throw new AppError('ACCESS_DENIED', { metadata: { farmId: batch.farmId } })
  }
})
```

## File Organization

```
app/features/batches/
├── server.ts      # Server functions (createServerFn)
├── service.ts     # Pure business logic
├── repository.ts  # Database operations
└── types.ts       # TypeScript interfaces
```

## Related Skills

- `tanstack-router` - Route definitions and loaders
- `tanstack-query` - Client-side data fetching
- `zod-validation` - Input validation patterns
- `three-layer-architecture` - Server/Service/Repository pattern
