---
name: testing-jest
description: Apply when writing unit tests with Jest: assertions, mocking, async tests, and test organization.
version: 1.0.0
tokens: ~650
confidence: high
sources:
  - https://jestjs.io/docs/getting-started
  - https://jestjs.io/docs/mock-functions
last_validated: 2025-01-10
next_review: 2025-01-24
tags: [testing, jest, unit-tests, mocking]
---

## When to Use

Apply when writing unit tests with Jest: assertions, mocking, async tests, and test organization.

## Patterns

### Pattern 1: Basic Test Structure
```typescript
// Source: https://jestjs.io/docs/getting-started
describe('Calculator', () => {
  describe('add', () => {
    it('should add two positive numbers', () => {
      expect(add(2, 3)).toBe(5);
    });

    it('should handle negative numbers', () => {
      expect(add(-1, 5)).toBe(4);
    });
  });
});
```

### Pattern 2: Common Matchers
```typescript
// Source: https://jestjs.io/docs/expect
// Equality
expect(value).toBe(5);              // Strict ===
expect(obj).toEqual({ a: 1 });      // Deep equality
expect(value).toBeNull();
expect(value).toBeDefined();

// Truthiness
expect(value).toBeTruthy();
expect(value).toBeFalsy();

// Numbers
expect(value).toBeGreaterThan(3);
expect(value).toBeCloseTo(0.3, 5);  // Floating point

// Strings
expect(str).toMatch(/pattern/);

// Arrays/Objects
expect(array).toContain('item');
expect(obj).toHaveProperty('key', 'value');

// Errors
expect(() => fn()).toThrow('error message');
expect(() => fn()).toThrow(CustomError);
```

### Pattern 3: Mocking Functions
```typescript
// Source: https://jestjs.io/docs/mock-functions
// Mock function
const mockFn = jest.fn();
mockFn.mockReturnValue(42);
mockFn.mockResolvedValue({ data: [] }); // Async

// Verify calls
expect(mockFn).toHaveBeenCalled();
expect(mockFn).toHaveBeenCalledWith('arg1', 'arg2');
expect(mockFn).toHaveBeenCalledTimes(2);

// Mock module
jest.mock('./api', () => ({
  fetchUser: jest.fn().mockResolvedValue({ id: '1', name: 'Test' }),
}));
```

### Pattern 4: Async Tests
```typescript
// Source: https://jestjs.io/docs/asynchronous
// Async/await (preferred)
it('should fetch data', async () => {
  const data = await fetchData();
  expect(data).toEqual({ id: 1 });
});

// Resolves/Rejects
it('should resolve with data', async () => {
  await expect(fetchData()).resolves.toEqual({ id: 1 });
});

it('should reject with error', async () => {
  await expect(failingFn()).rejects.toThrow('Network error');
});
```

### Pattern 5: Setup and Teardown
```typescript
// Source: https://jestjs.io/docs/setup-teardown
describe('Database tests', () => {
  let db: Database;

  beforeAll(async () => {
    db = await createTestDatabase();
  });

  afterAll(async () => {
    await db.close();
  });

  beforeEach(async () => {
    await db.clear();
  });

  it('should insert record', async () => {
    await db.insert({ id: 1 });
    expect(await db.count()).toBe(1);
  });
});
```

### Pattern 6: Snapshot Testing
```typescript
// Source: https://jestjs.io/docs/snapshot-testing
it('should match snapshot', () => {
  const component = render(<Button>Click</Button>);
  expect(component).toMatchSnapshot();
});

// Inline snapshot
expect(format(date)).toMatchInlineSnapshot(`"2025-01-10"`);
```

## Anti-Patterns

- **Testing implementation** - Test behavior, not internal details
- **Shared mutable state** - Reset in beforeEach
- **No assertion** - Every test needs expect()
- **Over-mocking** - Test real code when possible

## Verification Checklist

- [ ] Tests isolated (no shared state)
- [ ] Mocks reset between tests
- [ ] Async tests properly awaited
- [ ] Descriptive test names
- [ ] Arrange-Act-Assert pattern
