---
description: Unit testing and TDD expert for Vitest/Jest. Red-green-refactor workflow, mocking strategies, coverage analysis, and ESM mocking patterns. Use for writing tests, implementing TDD, or setting up test coverage.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
model: opus
context: fork
---

# Unit Testing & TDD Expert - Vitest/Jest

## Test-Driven Development (TDD)

### Red-Green-Refactor Cycle

```typescript
// 1. RED: Write failing test
describe('Calculator', () => {
  it('should add two numbers', () => {
    const calc = new Calculator();
    expect(calc.add(2, 3)).toBe(5); // FAILS - doesn't exist
  });
});

// 2. GREEN: Minimal implementation
class Calculator {
  add(a: number, b: number): number {
    return a + b;
  }
}

// 3. REFACTOR: Improve design
class Calculator {
  add(...numbers: number[]): number {
    return numbers.reduce((sum, n) => sum + n, 0);
  }
}
```

### TDD Checklist

- [ ] RED: Test fails for the RIGHT reason
- [ ] GREEN: Simplest code that passes
- [ ] REFACTOR: All tests still green

## Basic Test Structure

```typescript
import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';

describe('UserService', () => {
  let service: UserService;

  beforeEach(() => {
    service = new UserService();
    vi.clearAllMocks();
  });

  it('should create user', () => {
    const user = service.create({ name: 'John', email: 'john@test.com' });

    expect(user).toMatchObject({
      id: expect.any(String),
      name: 'John',
      email: 'john@test.com'
    });
  });

  it('should throw for invalid email', () => {
    expect(() => service.create({ email: 'invalid' })).toThrow('Invalid email');
  });
});
```

## Mocking Strategies

### 1. Mock Functions

```typescript
const mockFn = vi.fn();
mockFn.mockReturnValue(42);
expect(mockFn()).toBe(42);
expect(mockFn).toHaveBeenCalledTimes(1);
```

### 2. Mock Modules

```typescript
vi.mock('./database', () => ({
  query: vi.fn().mockResolvedValue([{ id: 1 }])
}));

import { query } from './database';
```

### 3. ESM Mocking with vi.hoisted()

**CRITICAL for ESM modules**:

```typescript
// ✅ Define mocks in hoisted context FIRST
const { mockFn } = vi.hoisted(() => ({
  mockFn: vi.fn()
}));

vi.mock('./module', () => ({
  myFunc: mockFn
}));

import { myFunc } from './module';
```

### 4. Dependency Injection

```typescript
class UserService {
  constructor(private db: Database) {}
}

// Test with mock
const mockDb = { query: vi.fn().mockResolvedValue({ id: '123' }) };
const service = new UserService(mockDb);
```

## Test Patterns

### AAA Pattern (Arrange-Act-Assert)

```typescript
it('should calculate total', () => {
  // Arrange
  const cart = new ShoppingCart();
  cart.addItem({ price: 10, quantity: 2 });

  // Act
  const total = cart.getTotal();

  // Assert
  expect(total).toBe(20);
});
```

### Parametric Testing

```typescript
describe.each([
  [2, 3, 5],
  [10, 5, 15],
  [-1, 1, 0],
])('add(%i, %i)', (a, b, expected) => {
  it(`should return ${expected}`, () => {
    expect(add(a, b)).toBe(expected);
  });
});
```

## Coverage Analysis

```javascript
// vitest.config.ts
export default {
  test: {
    coverage: {
      provider: 'v8',
      reporter: ['text', 'html', 'lcov'],
      lines: 80,
      functions: 80,
      branches: 80,
    }
  }
};
```

## Async Testing

```typescript
it('should fetch user', async () => {
  const user = await api.fetchUser('123');
  expect(user).toEqual({ id: '123', name: 'John' });
});

it('should handle API errors', async () => {
  await expect(api.fetchUser('invalid')).rejects.toThrow('Not found');
});
```

## VSCode Debug Mode Fix

When tests spawn child processes, use clean environment:

```typescript
function getCleanEnv(): NodeJS.ProcessEnv {
  const cleanEnv = { ...process.env };
  delete cleanEnv.NODE_OPTIONS;
  delete cleanEnv.NODE_INSPECT;
  delete cleanEnv.VSCODE_INSPECTOR_OPTIONS;
  return cleanEnv;
}

// Usage
execSync('node cli.js', { env: getCleanEnv() });
```

## Isolated Temp Directories

```typescript
import * as os from 'os';

const TEST_ROOT = path.join(os.tmpdir(), `test-${Date.now()}`);

beforeEach(() => fs.mkdir(TEST_ROOT, { recursive: true }));
afterEach(() => fs.rm(TEST_ROOT, { recursive: true, force: true }));
```

## Best Practices

1. **Test behavior, not implementation**
2. **One assertion per test** (when possible)
3. **Independent tests** (no shared state)
4. **Fast tests** (<100ms each)
5. **Clear test names** (should...)
6. **Mock external dependencies** only

## Quick Reference

### Assertions

```typescript
expect(value).toBe(expected);           // ===
expect(value).toEqual(expected);        // Deep equality
expect(array).toContain(item);          // Array includes
expect(string).toMatch(/pattern/);      // Regex
expect(fn).toThrow(Error);              // Throws
expect(obj).toHaveProperty('key');      // Has property
```

### Mock Utilities

```typescript
vi.fn()                           // Create mock
vi.fn().mockReturnValue(x)        // Return value
vi.fn().mockResolvedValue(x)      // Async return
vi.mock('./module')               // Mock module
vi.spyOn(obj, 'method')           // Spy on method
vi.clearAllMocks()                // Clear history
```

## Related Skills

- `qa-engineer` - Overall test strategy
- `e2e-testing` - E2E and visual tests
