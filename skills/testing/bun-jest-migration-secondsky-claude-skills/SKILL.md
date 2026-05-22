---
name: Bun Jest Migration
description: Use when migrating from Jest to Bun's test runner, import compatibility, mocks, and config.
version: 1.0.0
---

# Bun Jest Migration

Bun's test runner is Jest-compatible. Most Jest tests run without changes.

## Quick Migration

```bash
# 1. Remove Jest dependencies
bun remove jest ts-jest @types/jest babel-jest

# 2. Update test script
# package.json: "test": "bun test"

# 3. Run tests
bun test
```

## Import Changes

```typescript
// Before (Jest)
import { describe, it, expect, jest } from '@jest/globals';

// After (Bun) - No import needed, or explicit:
import { describe, test, expect, mock, spyOn } from "bun:test";
```

## API Compatibility

### Fully Compatible

| Jest | Bun | Notes |
|------|-----|-------|
| `describe()` | `describe()` | Identical |
| `it()` / `test()` | `test()` | Use `test()` |
| `expect()` | `expect()` | Same matchers |
| `beforeAll/Each` | `beforeAll/Each` | Identical |
| `afterAll/Each` | `afterAll/Each` | Identical |
| `jest.fn()` | `mock()` | Use `mock()` |
| `jest.spyOn()` | `spyOn()` | Identical |

### Requires Changes

| Jest | Bun Equivalent |
|------|----------------|
| `jest.mock('module')` | `mock.module('module', () => {...})` |
| `jest.useFakeTimers()` | `import { setSystemTime } from "bun:test"` |
| `jest.setTimeout()` | Third argument to `test()` |
| `jest.clearAllMocks()` | Call `.mockClear()` on each mock |

## Mock Migration

### Mock Functions

```typescript
// Jest
const fn = jest.fn().mockReturnValue('value');

// Bun
const fn = mock(() => 'value');
// Or for compatibility:
import { jest } from "bun:test";
const fn = jest.fn(() => 'value');
```

### Module Mocking

```typescript
// Jest (top-level hoisting)
jest.mock('./utils', () => ({
  helper: jest.fn(() => 'mocked')
}));

// Bun (inline, no hoisting)
import { mock } from "bun:test";
mock.module('./utils', () => ({
  helper: mock(() => 'mocked')
}));
```

### Spy Migration

```typescript
// Jest
jest.spyOn(console, 'log').mockImplementation(() => {});

// Bun (identical)
spyOn(console, 'log').mockImplementation(() => {});
```

## Timer Migration

```typescript
// Jest
jest.useFakeTimers();
jest.setSystemTime(new Date('2024-01-01'));
jest.advanceTimersByTime(1000);

// Bun - supports Jest-compatible timer APIs
import { setSystemTime } from "bun:test";
import { jest } from "bun:test";

jest.useFakeTimers();
jest.setSystemTime(new Date('2024-01-01'));
jest.advanceTimersByTime(1000);  // Now supported
```

## Snapshot Testing

```typescript
// Jest
expect(component).toMatchSnapshot();
expect(data).toMatchInlineSnapshot(`"expected"`);

// Bun (identical)
expect(component).toMatchSnapshot();
expect(data).toMatchInlineSnapshot(`"expected"`);
```

Update snapshots:
```bash
bun test --update-snapshots
```

## Configuration Migration

### jest.config.js → bunfig.toml

```javascript
// jest.config.js (before)
module.exports = {
  testMatch: ['**/*.test.ts'],
  testTimeout: 10000,
  setupFilesAfterEnv: ['./jest.setup.ts'],
  collectCoverage: true,
  coverageThreshold: { global: { lines: 80 } }
};
```

```toml
# bunfig.toml (after)
[test]
root = "./"
preload = ["./jest.setup.ts"]
timeout = 10000
coverage = true
coverageThreshold = 0.8
```

## Common Migration Issues

### Issue: `jest.mock` Not Working

```typescript
// Jest mock hoisting doesn't exist in Bun
// Move mock.module before imports or use dynamic imports

// Solution 1: Use mock.module at top
mock.module('./api', () => ({ fetch: mock() }));
import { fetch } from './api';

// Solution 2: Dynamic import
const mockFetch = mock();
mock.module('./api', () => ({ fetch: mockFetch }));
const { fetch } = await import('./api');
```

### Issue: Timer Functions Missing

```typescript
// Bun timer support is limited
// Use setSystemTime for date mocking
import { setSystemTime } from "bun:test";

beforeEach(() => {
  setSystemTime(new Date('2024-01-01'));
});

afterEach(() => {
  setSystemTime(); // Reset to real time
});
```

### Issue: Custom Matchers

```typescript
// Jest
expect.extend({ toBeWithinRange(received, floor, ceiling) {...} });

// Bun (same API)
import { expect } from "bun:test";
expect.extend({
  toBeWithinRange(received, floor, ceiling) {
    const pass = received >= floor && received <= ceiling;
    return {
      pass,
      message: () => `expected ${received} to be within ${floor}-${ceiling}`
    };
  }
});
```

## Step-by-Step Migration

1. **Remove Jest packages**
   ```bash
   bun remove jest ts-jest @types/jest babel-jest jest-environment-jsdom
   ```

2. **Update package.json**
   ```json
   {
     "scripts": {
       "test": "bun test",
       "test:watch": "bun test --watch",
       "test:coverage": "bun test --coverage"
     }
   }
   ```

3. **Convert jest.config.js to bunfig.toml**

4. **Update imports in test files**
   - Find/replace `@jest/globals` → `bun:test`
   - Find/replace `jest.fn()` → `mock()`
   - Find/replace `jest.mock()` → `mock.module()`

5. **Run and fix**
   ```bash
   bun test 2>&1 | head -50  # Check first errors
   ```

## Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `Cannot find module '@jest/globals'` | Old import | Use `bun:test` |
| `jest is not defined` | Global jest | Import from `bun:test` |
| `mock.module is not a function` | Wrong import | `import { mock } from "bun:test"` |
| `Snapshot mismatch` | Different serialization | Update with `--update-snapshots` |

## When to Load References

Load `references/compatibility-matrix.md` when:
- Full Jest API compatibility details
- Unsupported features list
- Workarounds for missing features
