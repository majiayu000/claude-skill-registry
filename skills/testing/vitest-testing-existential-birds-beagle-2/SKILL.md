---
name: vitest-testing
description: Vitest testing framework patterns and best practices. Use when writing unit tests, integration tests, configuring vitest.config, mocking with vi.mock/vi.fn, using snapshots, or setting up test coverage. Triggers on describe, it, expect, vi.mock, vi.fn, beforeEach, afterEach, vitest.
---

# Vitest Best Practices

## Quick Reference

```ts
import { describe, it, expect, beforeEach, vi } from 'vitest'

describe('feature name', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('should do something specific', () => {
    expect(actual).toBe(expected)
  })

  it.todo('planned test')
  it.skip('temporarily disabled')
  it.only('run only this during dev')
})
```

## Common Assertions

```ts
// Equality
expect(value).toBe(42)                    // Strict (===)
expect(obj).toEqual({ a: 1 })             // Deep equality
expect(obj).toStrictEqual({ a: 1 })       // Strict deep (checks types)

// Truthiness
expect(value).toBeTruthy()
expect(value).toBeFalsy()
expect(value).toBeNull()
expect(value).toBeUndefined()

// Numbers
expect(0.1 + 0.2).toBeCloseTo(0.3)
expect(value).toBeGreaterThan(5)

// Strings/Arrays
expect(str).toMatch(/pattern/)
expect(str).toContain('substring')
expect(array).toContain(item)
expect(array).toHaveLength(3)

// Objects
expect(obj).toHaveProperty('key')
expect(obj).toHaveProperty('nested.key', 'value')
expect(obj).toMatchObject({ subset: 'of properties' })

// Exceptions
expect(() => fn()).toThrow()
expect(() => fn()).toThrow('error message')
expect(() => fn()).toThrow(/pattern/)
```

## Async Testing

```ts
// Async/await (preferred)
it('fetches data', async () => {
  const data = await fetchData()
  expect(data).toEqual({ id: 1 })
})

// Promise matchers - ALWAYS await these
await expect(fetchData()).resolves.toEqual({ id: 1 })
await expect(fetchData()).rejects.toThrow('Error')

// Wrong - creates false positive
expect(promise).resolves.toBe(value)  // Missing await!
```

## Quick Mock Reference

```ts
const mockFn = vi.fn()
mockFn.mockReturnValue(42)
mockFn.mockResolvedValue({ data: 'value' })

expect(mockFn).toHaveBeenCalled()
expect(mockFn).toHaveBeenCalledWith('arg1', 'arg2')
expect(mockFn).toHaveBeenCalledTimes(2)
```

## Additional Documentation

- **Mocking**: See [references/mocking.md](references/mocking.md) for module mocking, spying, cleanup
- **Configuration**: See [references/config.md](references/config.md) for vitest.config, setup files, coverage
- **Patterns**: See [references/patterns.md](references/patterns.md) for timers, snapshots, anti-patterns

## Test Methods Quick Reference

| Method | Purpose |
|--------|---------|
| `it()` / `test()` | Define test |
| `describe()` | Group tests |
| `beforeEach()` / `afterEach()` | Per-test hooks |
| `beforeAll()` / `afterAll()` | Per-suite hooks |
| `.skip` | Skip test/suite |
| `.only` | Run only this |
| `.todo` | Placeholder |
| `.concurrent` | Parallel execution |
| `.each([...])` | Parameterized tests |
