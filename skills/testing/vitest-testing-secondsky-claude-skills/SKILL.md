---
name: vitest-testing
description: Modern TypeScript/JavaScript testing with Vitest. Fast unit and integration tests, native ESM support, Vite-powered HMR, and comprehensive mocking. Use for testing TS/JS projects.
allowed-tools: Bash, Read, Edit, Write, Grep, Glob, TodoWrite
---

# Vitest Testing

Expert knowledge for testing JavaScript/TypeScript projects using Vitest - a blazingly fast testing framework powered by Vite.

## Quick Start

### Installation

```bash
# Using Bun (recommended)
bun add -d vitest

# Using npm
npm install -D vitest
```

### Configuration

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config'

export default defineConfig({
  test: {
    globals: true,
    environment: 'node', // or 'jsdom'
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
      thresholds: { lines: 80, functions: 80, branches: 80 },
    },
    include: ['**/*.{test,spec}.{js,ts,jsx,tsx}'],
  },
})
```

## Running Tests

```bash
# Run all tests (prefer bun)
bun test

# Watch mode (default)
bun test --watch

# Run once (CI mode)
bun test --run

# With coverage
bun test --coverage

# Specific file
bun test src/utils/math.test.ts

# Pattern matching
bun test --grep="calculates sum"

# UI mode (interactive)
bun test --ui

# Verbose output
bun test --reporter=verbose
```

## Writing Tests

### Basic Structure

```typescript
import { describe, it, expect, beforeEach, afterEach } from 'vitest'
import { add, subtract } from './math'

describe('Math utilities', () => {
  beforeEach(() => {
    // Setup before each test
  })

  it('adds two numbers correctly', () => {
    expect(add(2, 3)).toBe(5)
  })

  it('subtracts two numbers correctly', () => {
    expect(subtract(5, 3)).toBe(2)
  })
})
```

### Parametrized Tests

```typescript
describe.each([
  { input: 2, expected: 4 },
  { input: 3, expected: 9 },
])('square function', ({ input, expected }) => {
  it(`squares ${input} to ${expected}`, () => {
    expect(square(input)).toBe(expected)
  })
})
```

## Assertions

```typescript
// Equality
expect(value).toBe(expected)
expect(value).toEqual(expected)

// Truthiness
expect(value).toBeTruthy()
expect(value).toBeNull()
expect(value).toBeDefined()

// Numbers
expect(number).toBeGreaterThan(3)
expect(number).toBeCloseTo(0.3, 1)

// Strings/Arrays
expect(string).toMatch(/pattern/)
expect(array).toContain(item)

// Objects
expect(object).toHaveProperty('key')
expect(object).toMatchObject({ a: 1 })

// Exceptions
expect(() => throwError()).toThrow('message')

// Promises
await expect(promise).resolves.toBe(value)
await expect(promise).rejects.toThrow()
```

## Mocking

### Function Mocks

```typescript
import { vi } from 'vitest'

const mockFn = vi.fn()
mockFn.mockReturnValue(42)
mockFn.mockResolvedValue('async result')
mockFn.mockImplementation((x) => x * 2)

expect(mockFn).toHaveBeenCalled()
expect(mockFn).toHaveBeenCalledWith('arg')
```

### Module Mocking

```typescript
vi.mock('./api', () => ({
  fetchUser: vi.fn(() => ({ id: 1, name: 'Test User' })),
}))

import { fetchUser } from './api'

beforeEach(() => {
  vi.clearAllMocks()
})
```

### Timers

```typescript
beforeEach(() => vi.useFakeTimers())
afterEach(() => vi.restoreAllMocks())

it('advances timers', () => {
  const callback = vi.fn()
  setTimeout(callback, 1000)
  vi.advanceTimersByTime(1000)
  expect(callback).toHaveBeenCalledOnce()
})

it('mocks dates', () => {
  const date = new Date('2024-01-01')
  vi.setSystemTime(date)
  expect(Date.now()).toBe(date.getTime())
})
```

## Coverage

```bash
# Generate coverage report
bun test --coverage

# HTML report
bun test --coverage --coverage.reporter=html
open coverage/index.html

# Check against thresholds
bun test --coverage --coverage.thresholds.lines=90
```

## Integration Testing

```typescript
import request from 'supertest'
import { app } from './app'

describe('API endpoints', () => {
  it('creates a user', async () => {
    const response = await request(app)
      .post('/api/users')
      .send({ name: 'John' })
      .expect(201)

    expect(response.body).toMatchObject({
      id: expect.any(Number),
      name: 'John',
    })
  })
})
```

## Best Practices

- One test file per source file: `math.ts` → `math.test.ts`
- Group related tests with `describe()` blocks
- Use descriptive test names
- Mock only external dependencies
- Use `concurrent` tests for independent async tests
- Share expensive fixtures with `beforeAll()`
- Aim for 80%+ coverage but don't chase 100%

## See Also

- `test-quality-analysis` - Detecting test smells
- `playwright-testing` - E2E testing
- `mutation-testing` - Validate test effectiveness
