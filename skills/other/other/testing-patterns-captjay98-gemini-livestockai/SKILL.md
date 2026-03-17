---
name: testing-patterns
description: |
  Testing patterns for LivestockAI. Use when writing unit tests, property-based tests
  with fast-check, or integration tests with the test database.
---

# Testing Patterns

You are a QA specialist for LivestockAI, expert in Vitest, fast-check, and integration testing.

## Test Commands

```bash
# IMPORTANT: Use "bun run test" not "bun test"
bun run test              # Unit tests (vitest)
bun run test:integration  # Integration tests (requires DATABASE_URL_TEST)
bun run test:all          # All tests
bun run test:coverage     # Coverage report
```

## Property-Based Tests (fast-check)

Use for mathematical invariants and business logic:

```typescript
import { describe, it, expect } from 'vitest'
import * as fc from 'fast-check'

describe('calculateFCR', () => {
  it('should always be positive when inputs are positive', () => {
    fc.assert(
      fc.property(
        fc.double({ min: 0.01, max: 10000, noNaN: true }),
        fc.double({ min: 0.01, max: 10000, noNaN: true }),
        (feed, gain) => {
          const fcr = calculateFCR(feed, gain)
          expect(fcr).toBeGreaterThan(0)
        },
      ),
    )
  })

  it('should return 0 when weight gain is 0 or negative', () => {
    fc.assert(
      fc.property(
        fc.double({ min: 0.01, max: 10000, noNaN: true }),
        fc.double({ max: 0, noNaN: true }),
        (feed, gain) => {
          expect(calculateFCR(feed, gain)).toBe(0)
        },
      ),
    )
  })
})
```

### fast-check Best Practices

```typescript
// Always use noNaN: true for doubles
fc.double({ min: 0, max: 1000, noNaN: true })

// Always use noInvalidDate: true for dates
fc.date({
  min: new Date('2020-01-01'),
  max: new Date('2030-01-01'),
  noInvalidDate: true,
})

// Constrain longitude to avoid date line issues
fc.double({ min: -170, max: 170, noNaN: true })
```

## Integration Tests

### Setup Pattern

```typescript
import { afterAll, afterEach, beforeEach, describe, expect, it } from 'vitest'
import {
  closeTestDb,
  getTestDb,
  resetTestDb,
  seedTestUser,
  seedTestFarm,
  truncateAllTables,
} from '../../helpers/db-integration'

describe('Batch Integration Tests', () => {
  beforeEach(async () => {
    await truncateAllTables() // Clean slate
  })

  afterEach(() => {
    resetTestDb() // Clear transaction state (NOT closeTestDb!)
  })

  afterAll(async () => {
    await closeTestDb() // Only here!
  })

  it('should create batch', async () => {
    // Use unique identifiers
    const { userId } = await seedTestUser({
      email: `test-${Date.now()}@example.com`,
    })
    const { farmId } = await seedTestFarm(userId)

    const db = getTestDb()
    // ... test code
  })
})
```

### Critical Rules

1. **Use `truncateAllTables()` in `beforeEach()`** - Reset database state
2. **Use `resetTestDb()` in `afterEach()`** - Clear transaction state
3. **Use `closeTestDb()` in `afterAll()` ONLY** - Don't destroy connection early
4. **Use unique identifiers** - Prevent duplicate key errors

## Unit Tests

```typescript
import { describe, it, expect } from 'vitest'

describe('validateBatchData', () => {
  it('should return null for valid data', () => {
    const result = validateBatchData({
      batchName: 'Test Batch',
      initialQuantity: 100,
      costPerUnit: 50,
    })
    expect(result).toBeNull()
  })

  it('should return error for negative quantity', () => {
    const result = validateBatchData({
      batchName: 'Test',
      initialQuantity: -1,
      costPerUnit: 50,
    })
    expect(result).toBe('Quantity must be positive')
  })
})
```

## Test File Organization

```
tests/
├── features/
│   ├── batches/
│   │   ├── batches.test.ts           # Unit tests
│   │   └── batches.property.test.ts  # Property tests
│   └── ...
├── integration/
│   ├── batches.integration.test.ts   # DB tests
│   └── ...
└── helpers/
    ├── db-integration.ts             # Test DB helpers
    └── db-mock.ts                    # Mock helpers
```

## Mocking Patterns

```typescript
import { vi } from 'vitest'

// Mock server function
vi.mock('~/features/batches/server', () => ({
  getBatchesFn: vi.fn().mockResolvedValue([]),
}))

// Mock database
vi.mock('~/lib/db', () => ({
  getDb: vi.fn().mockResolvedValue(mockDb),
}))
```
