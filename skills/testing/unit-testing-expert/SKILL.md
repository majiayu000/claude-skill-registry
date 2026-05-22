---
name: unit-testing-expert
description: Comprehensive unit testing expertise covering Vitest, Jest, test-driven development (TDD), mocking strategies, test coverage, snapshot testing, test architecture, testing patterns, dependency injection, test doubles (mocks, stubs, spies, fakes), async testing, error handling tests, parametric testing, test organization, code coverage analysis, mutation testing, and production-grade unit testing best practices. Activates for unit testing, vitest, jest, test-driven development, TDD, red-green-refactor, mocking, stubbing, spying, test doubles, test coverage, snapshot testing, test architecture, dependency injection, async testing, test patterns, code coverage, mutation testing, test isolation, test fixtures, AAA pattern, given-when-then, test organization, testing best practices, vi.fn, vi.mock, vi.spyOn, describe, it, expect, beforeEach, afterEach.
---

# Unit Testing Expert

**Self-contained unit testing expertise for Vitest/Jest in ANY user project.**

---

## Test-Driven Development (TDD)

**Red-Green-Refactor Cycle**:

```typescript
// 1. RED: Write failing test
describe('Calculator', () => {
  it('should add two numbers', () => {
    const calc = new Calculator();
    expect(calc.add(2, 3)).toBe(5);
  });
});

// 2. GREEN: Minimal implementation
class Calculator {
  add(a: number, b: number): number {
    return a + b;
  }
}

// 3. REFACTOR: Improve code
class Calculator {
  add(...numbers: number[]): number {
    return numbers.reduce((sum, n) => sum + n, 0);
  }
}
```

**TDD Benefits**:
- Better design (testable code)
- Living documentation
- Faster debugging
- Higher confidence

---

## Vitest/Jest Fundamentals

### Basic Test Structure

```typescript
import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import { UserService } from './UserService';

describe('UserService', () => {
  let service: UserService;

  beforeEach(() => {
    service = new UserService();
  });

  afterEach(() => {
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
    expect(() => {
      service.create({ name: 'John', email: 'invalid' });
    }).toThrow('Invalid email');
  });
});
```

### Async Testing

```typescript
it('should fetch user from API', async () => {
  const user = await api.fetchUser('user-123');

  expect(user).toEqual({
    id: 'user-123',
    name: 'John Doe'
  });
});

// Testing async errors
it('should handle API errors', async () => {
  await expect(api.fetchUser('invalid')).rejects.toThrow('User not found');
});
```

---

## Mocking Strategies

### 1. Mock Functions

```typescript
// Mock a function
const mockFn = vi.fn();
mockFn.mockReturnValue(42);
expect(mockFn()).toBe(42);

// Mock with implementation
const mockAdd = vi.fn((a, b) => a + b);
expect(mockAdd(2, 3)).toBe(5);

// Verify calls
expect(mockFn).toHaveBeenCalledTimes(1);
expect(mockFn).toHaveBeenCalledWith(expected);
```

### 2. Mock Modules

```typescript
// Mock entire module
vi.mock('./database', () => ({
  query: vi.fn().mockResolvedValue([{ id: 1, name: 'Test' }])
}));

import { query } from './database';

it('should fetch users from database', async () => {
  const users = await query('SELECT * FROM users');
  expect(users).toHaveLength(1);
});
```

### 3. Spies

```typescript
// Spy on existing method
const spy = vi.spyOn(console, 'log');

myFunction();

expect(spy).toHaveBeenCalledWith('Expected message');
spy.mockRestore();
```

### 4. Mock Dependencies

```typescript
class UserService {
  constructor(private db: Database) {}

  async getUser(id: string) {
    return this.db.query('SELECT * FROM users WHERE id = ?', [id]);
  }
}

// Test with mock
const mockDb = {
  query: vi.fn().mockResolvedValue({ id: '123', name: 'John' })
};

const service = new UserService(mockDb);
const user = await service.getUser('123');

expect(mockDb.query).toHaveBeenCalledWith(
  'SELECT * FROM users WHERE id = ?',
  ['123']
);
```

---

## Test Patterns

### AAA Pattern (Arrange-Act-Assert)

```typescript
it('should calculate total price', () => {
  // Arrange
  const cart = new ShoppingCart();
  cart.addItem({ price: 10, quantity: 2 });
  cart.addItem({ price: 5, quantity: 3 });

  // Act
  const total = cart.getTotal();

  // Assert
  expect(total).toBe(35);
});
```

### Given-When-Then (BDD)

```typescript
describe('Shopping Cart', () => {
  it('should apply discount when total exceeds $100', () => {
    // Given: A cart with items totaling $120
    const cart = new ShoppingCart();
    cart.addItem({ price: 120, quantity: 1 });

    // When: Getting the total
    const total = cart.getTotal();

    // Then: 10% discount applied
    expect(total).toBe(108); // $120 - $12 (10%)
  });
});
```

### Parametric Testing

```typescript
describe.each([
  [2, 3, 5],
  [10, 5, 15],
  [-1, 1, 0],
  [0, 0, 0]
])('Calculator.add(%i, %i)', (a, b, expected) => {
  it(`should return ${expected}`, () => {
    const calc = new Calculator();
    expect(calc.add(a, b)).toBe(expected);
  });
});
```

---

## Test Doubles

### Mocks vs Stubs vs Spies vs Fakes

**Mock**: Verifies behavior (calls, arguments)
```typescript
const mock = vi.fn();
mock('test');
expect(mock).toHaveBeenCalledWith('test');
```

**Stub**: Returns predefined values
```typescript
const stub = vi.fn().mockReturnValue(42);
expect(stub()).toBe(42);
```

**Spy**: Observes real function
```typescript
const spy = vi.spyOn(obj, 'method');
obj.method();
expect(spy).toHaveBeenCalled();
```

**Fake**: Working implementation (simplified)
```typescript
class FakeDatabase {
  private data = new Map();

  async save(key, value) {
    this.data.set(key, value);
  }

  async get(key) {
    return this.data.get(key);
  }
}
```

---

## Coverage Analysis

### Running Coverage

```bash
# Vitest
vitest --coverage

# Jest
jest --coverage
```

### Coverage Thresholds

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
      statements: 80
    }
  }
};
```

### Coverage Best Practices

**✅ DO**:
- Aim for 80-90% coverage
- Focus on business logic
- Test edge cases
- Test error paths

**❌ DON'T**:
- Chase 100% coverage
- Test getters/setters only
- Test framework code
- Write tests just for coverage

---

## Snapshot Testing

### When to Use Snapshots

**Good use cases**:
- UI component output
- API responses
- Configuration objects
- Error messages

```typescript
it('should render user card', () => {
  const card = renderUserCard({ name: 'John', role: 'Admin' });
  expect(card).toMatchSnapshot();
});

// Update snapshots: vitest -u
```

**Avoid snapshots for**:
- Dates/timestamps
- Random values
- Large objects (prefer specific assertions)

---

## Test Organization

### File Structure

```
src/
├── services/
│   ├── UserService.ts
│   └── UserService.test.ts      ← Co-located
tests/
├── unit/
│   └── utils.test.ts
├── integration/
│   └── api.test.ts
└── fixtures/
    └── users.json
```

### Test Naming

**✅ GOOD**:
```typescript
describe('UserService.create', () => {
  it('should create user with valid email', () => {});
  it('should throw error for invalid email', () => {});
  it('should generate unique ID', () => {});
});
```

**❌ BAD**:
```typescript
describe('UserService', () => {
  it('test1', () => {});
  it('should work', () => {});
});
```

---

## Error Handling Tests

```typescript
// Synchronous errors
it('should throw for negative numbers', () => {
  expect(() => sqrt(-1)).toThrow('Cannot compute square root of negative');
});

// Async errors
it('should reject for invalid ID', async () => {
  await expect(fetchUser('invalid')).rejects.toThrow('Invalid ID');
});

// Error types
it('should throw TypeError', () => {
  expect(() => doSomething()).toThrow(TypeError);
});

// Custom errors
it('should throw ValidationError', () => {
  expect(() => validate()).toThrow(ValidationError);
});
```

---

## Test Isolation

### Reset State Between Tests

```typescript
let service: UserService;

beforeEach(() => {
  service = new UserService();
  vi.clearAllMocks();
});

afterEach(() => {
  vi.restoreAllMocks();
});
```

### Avoid Test Interdependence

**❌ BAD**:
```typescript
let user;

it('should create user', () => {
  user = createUser(); // Shared state
});

it('should update user', () => {
  updateUser(user); // Depends on previous test
});
```

**✅ GOOD**:
```typescript
it('should update user', () => {
  const user = createUser();
  updateUser(user);
  expect(user.updated).toBe(true);
});
```

---

## Best Practices Summary

**✅ DO**:
- Write tests before code (TDD)
- Test behavior, not implementation
- One assertion per test (when possible)
- Clear test names (should...)
- Mock external dependencies
- Test edge cases and errors
- Keep tests fast (<100ms each)
- Use descriptive variable names
- Clean up after tests

**❌ DON'T**:
- Test private methods directly
- Share state between tests
- Use real databases/APIs
- Test framework code
- Write fragile tests (implementation-dependent)
- Skip error cases
- Use magic numbers
- Leave commented-out tests

---

## Quick Reference

### Assertions
```typescript
expect(value).toBe(expected);              // ===
expect(value).toEqual(expected);           // Deep equality
expect(value).toBeTruthy();                // Boolean true
expect(value).toBeFalsy();                 // Boolean false
expect(array).toHaveLength(3);             // Array length
expect(array).toContain(item);             // Array includes
expect(string).toMatch(/pattern/);         // Regex match
expect(fn).toThrow(Error);                 // Throws error
expect(obj).toHaveProperty('key');         // Has property
expect(value).toBeCloseTo(0.3, 5);        // Float comparison
```

### Lifecycle Hooks
```typescript
beforeAll(() => {});      // Once before all tests
beforeEach(() => {});     // Before each test
afterEach(() => {});      // After each test
afterAll(() => {});       // Once after all tests
```

### Mock Utilities
```typescript
vi.fn()                           // Create mock
vi.fn().mockReturnValue(x)        // Return value
vi.fn().mockResolvedValue(x)      // Async return
vi.fn().mockRejectedValue(e)      // Async error
vi.mock('./module')               // Mock module
vi.spyOn(obj, 'method')           // Spy on method
vi.clearAllMocks()                // Clear call history
vi.resetAllMocks()                // Reset + clear
vi.restoreAllMocks()              // Restore originals
```

---

**This skill is self-contained and works in ANY user project with Vitest/Jest.**
