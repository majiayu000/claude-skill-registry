---
name: Zod Validation
description: Input validation patterns with Zod in LivestockAI server functions
---

# Zod Validation

LivestockAI uses [Zod](https://zod.dev) for runtime input validation in server functions.

## Server Function Validation

**ALWAYS use Zod validators**, not identity functions:

```typescript
import { createServerFn } from '@tanstack/react-start'
import { z } from 'zod'

// ✅ Correct - Zod validation
export const createBatchFn = createServerFn({ method: 'POST' })
  .inputValidator(
    z.object({
      farmId: z.string().uuid(),
      species: z.string().min(1).max(100),
      quantity: z.number().int().positive(),
    }),
  )
  .handler(async ({ data }) => {
    // data is fully typed and validated
  })

  // ❌ Wrong - No validation
  .inputValidator((data: { farmId: string }) => data)
```

## Common Patterns

### UUIDs

```typescript
farmId: z.string().uuid()
farmId: z.string().uuid().optional()
```

### Enums

```typescript
status: z.enum(['active', 'depleted', 'sold'])
livestockType: z.enum(['poultry', 'fish', 'cattle', 'goats', 'sheep', 'bees'])
```

### Numbers

```typescript
page: z.number().int().positive()
quantity: z.number().int().positive()
amount: z.number().nonnegative()
percentage: z.number().min(0).max(100)
```

### Dates

```typescript
date: z.coerce.date()
targetDate: z.coerce.date().optional()
```

### Strings

```typescript
name: z.string().min(1).max(100)
email: z.string().email()
notes: z.string().max(500).nullish()
```

### Nullable/Optional

```typescript
// Optional (can be undefined)
notes: z.string().optional()

// Nullable (can be null)
notes: z.string().nullable()

// Both (can be undefined or null)
notes: z.string().nullish()
```

## Complete Schema Example

```typescript
const createBatchSchema = z.object({
  farmId: z.string().uuid(),
  livestockType: z.enum([
    'poultry',
    'fish',
    'cattle',
    'goats',
    'sheep',
    'bees',
  ]),
  species: z.string().min(1).max(100),
  breedId: z.string().uuid().nullish(),
  initialQuantity: z.number().int().positive(),
  acquisitionDate: z.coerce.date(),
  costPerUnit: z.number().nonnegative(),
  batchName: z.string().max(100).nullish(),
  targetHarvestDate: z.coerce.date().nullish(),
  notes: z.string().max(500).nullish(),
})
```

## Pagination Schema

```typescript
const paginatedQuerySchema = z.object({
  page: z.number().int().positive().optional().default(1),
  pageSize: z.number().int().positive().max(100).optional().default(10),
  sortBy: z.string().optional(),
  sortOrder: z.enum(['asc', 'desc']).optional(),
  search: z.string().optional(),
})
```

## Related Skills

- `tanstack-start` - Server function patterns
- `error-handling` - Validation error handling
