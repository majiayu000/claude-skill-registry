---
name: typescript-testing
description: Jest and Vitest testing policies for TypeScript/JavaScript. Use when writing or reviewing TS/JS test code. Do NOT use for application code -- use typescript-patterns instead.
durability: encoded-preference
---

# TypeScript/JavaScript Testing Policies

## Test Structure (AAA Pattern)

```typescript
describe('UserService', () => {
  describe('createUser', () => {
    it('creates user with valid input', async () => {
      // Arrange
      const input = { name: 'Alice', email: 'alice@example.com' }
      // Act
      const user = await userService.createUser(input)
      // Assert
      expect(user.id).toBeDefined()
    })
  })
})
```

## Mocking Policies

### Mock Cleanup (REQUIRED)

```typescript
afterEach(() => {
  jest.clearAllMocks()  // Vitest: vi.clearAllMocks()
  jest.restoreAllMocks() // Vitest: vi.restoreAllMocks()
})
```

### Prefer spyOn Over Full Mocks

```typescript
// GOOD: Spy on specific method
const spy = jest.spyOn(service, 'save')

// AVOID: Full module mock when not needed
jest.mock('./service')
```

## Async Testing

```typescript
// Use async/await
it('fetches data', async () => {
  const data = await fetchData()
  expect(data).toBeDefined()
})

// Use rejects for error cases
await expect(fetchData()).rejects.toThrow('Network error')
```

## Coverage Targets

| Metric | Target |
|--------|--------|
| Lines | 80%+ |
| Branches | 80%+ |
| Functions | 80%+ |

## Commands

**See `makefile-first` skill** for command execution policy.

## Vitest Bench

```bash
vitest bench                    # Run all benchmarks
vitest bench --reporter=verbose # Detailed output
```

### When to Write Benchmarks

- Comparing alternative implementations (data structures, algorithms)
- Validating that an optimization actually improved performance
- Establishing baseline for performance-critical paths
- Preventing regression in hot paths

### Benchmark Options

```typescript
bench('operation', () => { /* code */ }, {
  time: 1000,       // ms to run (default: 100)
  iterations: 100,  // minimum iterations
  warmupTime: 200,  // warmup before measuring
})
```

