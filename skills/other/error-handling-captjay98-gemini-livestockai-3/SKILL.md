---
name: Error Handling
description: Structured error handling with AppError in LivestockAI
---

# Error Handling

LivestockAI uses a structured `AppError` class for consistent error handling across the application.

## AppError Class

Located in `app/lib/errors/app-error.ts`:

```typescript
import { AppError } from '~/lib/errors'

// Throwing errors
throw new AppError('BATCH_NOT_FOUND', {
  metadata: { batchId: '123' },
})

throw new AppError('VALIDATION_ERROR', {
  message: 'Custom message',
  metadata: { field: 'quantity' },
})

throw new AppError('ACCESS_DENIED', {
  metadata: { farmId: 'abc' },
})
```

## Error Codes

Common error codes defined in `app/lib/errors/error-map.ts`:

| Code             | HTTP Status | Category   | Usage               |
| ---------------- | ----------- | ---------- | ------------------- |
| VALIDATION_ERROR | 400         | validation | Invalid input       |
| ACCESS_DENIED    | 403         | auth       | No permission       |
| BATCH_NOT_FOUND  | 404         | not_found  | Resource missing    |
| DATABASE_ERROR   | 500         | database   | DB operation failed |

## AppError Structure

```typescript
class AppError extends Error {
  reason: ReasonCode // e.g., 'BATCH_NOT_FOUND'
  code: number // Internal code
  httpStatus: number // HTTP status code
  category: string // Error category
  metadata: ErrorMetadata // Additional context
}
```

## Using in Server Functions

```typescript
export const getBatchFn = createServerFn({ method: 'GET' })
  .inputValidator(z.object({ batchId: z.string().uuid() }))
  .handler(async ({ data }) => {
    const { requireAuth } = await import('../auth/server-middleware')
    const session = await requireAuth()

    const { getDb } = await import('~/lib/db')
    const db = await getDb()

    const batch = await getBatchById(db, data.batchId)
    if (!batch) {
      throw new AppError('BATCH_NOT_FOUND', {
        metadata: { batchId: data.batchId },
      })
    }

    const hasAccess = await checkFarmAccess(session.user.id, batch.farmId)
    if (!hasAccess) {
      throw new AppError('ACCESS_DENIED', {
        metadata: { farmId: batch.farmId },
      })
    }

    return batch
  })
```

## Error Handling Pattern

```typescript
try {
  // Operation
} catch (error) {
  if (error instanceof AppError) {
    // Re-throw known errors
    throw error
  }
  // Wrap unknown errors
  throw new AppError('DATABASE_ERROR', {
    message: 'Failed to complete operation',
    cause: error,
  })
}
```

## Type Checking

```typescript
if (AppError.isAppError(error)) {
  console.log(error.reason) // 'BATCH_NOT_FOUND'
  console.log(error.httpStatus) // 404
  console.log(error.metadata) // { batchId: '123' }
}
```

## JSON Serialization

```typescript
const json = error.toJSON()
// {
//   name: 'AppError',
//   reason: 'BATCH_NOT_FOUND',
//   code: 1001,
//   httpStatus: 404,
//   category: 'not_found',
//   message: 'Batch not found',
//   metadata: { batchId: '123' }
// }

const restored = AppError.fromJSON(json)
```

## Client-Side Error Handling

```typescript
import { useMutation } from '@tanstack/react-query'
import { toast } from 'sonner'

const mutation = useMutation({
  mutationFn: createBatchFn,
  onError: (error) => {
    if (error.message.includes('ACCESS_DENIED')) {
      toast.error('You do not have access to this farm')
    } else if (error.message.includes('VALIDATION_ERROR')) {
      toast.error('Please check your input')
    } else {
      toast.error('An error occurred. Please try again.')
    }
  },
})
```

## Related Skills

- `three-layer-architecture` - Error handling in layers
- `tanstack-start` - Server function error handling
