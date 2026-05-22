---
name: Property Testing
description: Property-based testing with fast-check for business logic validation
---

# Property Testing

LivestockAI uses property-based testing (PBT) with fast-check to validate business logic invariants.

## What is Property Testing?

Instead of testing specific examples, property tests verify that properties hold for ALL possible inputs:

```typescript
// Example-based test
it('calculates FCR correctly', () => {
  expect(calculateFCR(150, 100)).toBe(1.5)
})

// Property-based test
it('FCR is always positive when inputs are positive', () => {
  fc.assert(
    fc.property(
      fc.float({ min: 0.1, max: 10000 }),
      fc.float({ min: 0.1, max: 10000 }),
      (feed, weight) => {
        const fcr = calculateFCR(feed, weight)
        return fcr === null || fcr > 0
      },
    ),
  )
})
```

## fast-check Basics

```typescript
import { describe, it, expect } from 'vitest'
import * as fc from 'fast-check'

describe('Property Tests', () => {
  it('property holds for all inputs', () => {
    fc.assert(
      fc.property(fc.integer({ min: 1, max: 100000 }), (quantity) => {
        // Property must return true or throw
        return quantity > 0
      }),
      { numRuns: 100 },
    )
  })
})
```

## Common Arbitraries

```typescript
// Integers
fc.integer({ min: 1, max: 100000 })
fc.nat() // Non-negative integer

// Floats
fc.float({ min: 0, max: 10000 })

// Strings
fc.string()
fc.uuid()

// Arrays
fc.array(fc.integer(), { minLength: 0, maxLength: 20 })

// Objects
fc.record({
  quantity: fc.integer({ min: 1, max: 1000 }),
  price: fc.float({ min: 0, max: 10000 }),
})
```

## Inventory Invariant Example

From `tests/features/batches/batches.property.test.ts`:

```typescript
/**
 * Property 4: Inventory Invariant
 * For any batch, current_quantity SHALL always equal:
 * initial_quantity - sum(mortality) - sum(sales)
 */
describe('Property 4: Inventory Invariant', () => {
  it('current_quantity equals initial - mortalities - sales', () => {
    fc.assert(
      fc.property(
        fc.integer({ min: 1, max: 100000 }),
        fc.array(fc.integer({ min: 1, max: 1000 })),
        fc.array(fc.integer({ min: 1, max: 1000 })),
        (initial, mortalities, sales) => {
          const { constrained } = constrainQuantities(
            initial,
            mortalities,
            sales,
          )
          const current = calculateCurrentQuantity(initial, constrained)

          expect(current).toBeGreaterThanOrEqual(0)
          expect(current).toBeLessThanOrEqual(initial)
        },
      ),
      { numRuns: 100 },
    )
  })
})
```

## Linking to Requirements

Annotate tests with requirement links:

```typescript
/**
 * **Validates: Requirements 3.2, 4.2, 8.2**
 */
it('inventory invariant holds', () => {
  // ...
})
```

## When to Use Property Testing

- Mathematical calculations (FCR, mortality rate, profit)
- Invariants (quantity never negative, totals match)
- State transitions (batch status changes)
- Data transformations (currency conversion)

## Related Skills

- `vitest-patterns` - Unit testing basics
- `three-layer-architecture` - Service layer testing
