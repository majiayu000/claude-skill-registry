---
name: Vitest Patterns
description: Unit testing patterns with Vitest in LivestockAI
---

# Vitest Patterns

LivestockAI uses Vitest for fast unit testing with TypeScript support.

## Running Tests

```bash
# Run unit tests (IMPORTANT: use "bun run test" not "bun test")
bun run test

# Run specific file
bun run test tests/features/batches/batches.property.test.ts

# Run with coverage
bun run test:coverage

# Run integration tests
bun run test:integration

# Run all tests
bun run test:all
```

**Note:** `bun run test` uses Vitest (respects config), while `bun test` uses Bun's built-in runner (ignores Vitest config).

## Test File Organization

```
tests/
├── features/           # Feature tests
│   ├── batches/
│   │   ├── batches.property.test.ts
│   │   └── batches.test.ts
│   └── sales/
├── integration/        # Database tests
│   └── batches.integration.test.ts
├── components/         # Component tests
└── helpers/            # Test utilities
    ├── db-integration.ts
    └── db-mock.ts
```

## Test Naming

- Unit tests: `feature.test.ts`
- Property tests: `feature.property.test.ts`
- Integration tests: `feature.integration.test.ts`

## Basic Test Structure

```typescript
import { describe, it, expect, beforeEach, afterEach } from 'vitest'

describe('calculateFCR', () => {
  it('returns correct FCR for valid inputs', () => {
    expect(calculateFCR(150, 100)).toBe(1.5)
  })

  it('returns null for zero weight gain', () => {
    expect(calculateFCR(150, 0)).toBeNull()
  })

  it('returns null for negative inputs', () => {
    expect(calculateFCR(-150, 100)).toBeNull()
  })
})
```

## Mocking

```typescript
import { vi } from 'vitest'

// Mock a module
vi.mock('~/lib/db', () => ({
  getDb: vi.fn().mockResolvedValue(mockDb),
}))

// Mock a function
const mockFn = vi.fn().mockReturnValue('result')

// Spy on a function
const spy = vi.spyOn(module, 'function')
```

## Testing Service Layer

Service functions are pure and easy to test:

```typescript
import { calculateBatchTotalCost, validateBatchData } from './service'

describe('calculateBatchTotalCost', () => {
  it('multiplies quantity by cost', () => {
    expect(calculateBatchTotalCost(100, 5.5)).toBe('550.00')
  })

  it('returns zero for invalid inputs', () => {
    expect(calculateBatchTotalCost(0, 5.5)).toBe('0.00')
    expect(calculateBatchTotalCost(100, -5)).toBe('0.00')
  })
})
```

## Coverage Requirements

- Minimum 80% for business logic
- 100% for financial calculations
- Critical path testing for offline functionality

## Related Skills

- `property-testing` - Property-based tests
- `integration-testing` - Database tests
- `three-layer-architecture` - Service layer testing
