---
name: test-generator
description: Generate comprehensive unit tests for code. Use when creating tests, improving test coverage, or setting up testing frameworks.
allowed-tools: Bash, Read, Write, Grep, Glob
---

# Test Generator

**Version**: 1.0.0
**Purpose**: Generate comprehensive tests with high coverage

---

## Triggers

| Trigger | Examples |
|---------|----------|
| Test creation | "write tests", "テスト作成", "add unit tests" |
| Coverage | "improve coverage", "カバレッジ向上" |
| TDD | "test first", "TDDで" |

---

## Testing Stack

| Framework | Purpose |
|-----------|---------|
| Vitest | Unit/Integration tests |
| Playwright | E2E tests |
| Testing Library | Component tests |

---

## Test Structure (AAA Pattern)

```typescript
describe('functionName', () => {
  it('should [expected behavior] when [condition]', () => {
    // Arrange
    const input = createTestInput();

    // Act
    const result = functionName(input);

    // Assert
    expect(result).toBe(expectedValue);
  });
});
```

---

## Test Categories

### 1. Happy Path

```typescript
it('should return sum when given valid numbers', () => {
  expect(add(2, 3)).toBe(5);
});
```

### 2. Edge Cases

```typescript
it('should handle empty array', () => {
  expect(sum([])).toBe(0);
});

it('should handle single element', () => {
  expect(sum([5])).toBe(5);
});

it('should handle negative numbers', () => {
  expect(sum([-1, 1])).toBe(0);
});
```

### 3. Error Cases

```typescript
it('should throw on invalid input', () => {
  expect(() => divide(10, 0)).toThrow('Division by zero');
});

it('should throw on null input', () => {
  expect(() => process(null)).toThrow(TypeError);
});
```

### 4. Async Tests

```typescript
it('should fetch user data', async () => {
  const user = await fetchUser(1);
  expect(user.name).toBe('John');
});

it('should handle API errors', async () => {
  await expect(fetchUser(-1)).rejects.toThrow('Not found');
});
```

---

## Mocking

### Mock Functions

```typescript
import { vi } from 'vitest';

const mockFn = vi.fn();
mockFn.mockReturnValue(42);
mockFn.mockResolvedValue({ data: 'test' });
```

### Mock Modules

```typescript
vi.mock('./database', () => ({
  query: vi.fn().mockResolvedValue([{ id: 1 }]),
}));
```

### Spies

```typescript
const spy = vi.spyOn(console, 'log');
doSomething();
expect(spy).toHaveBeenCalledWith('expected message');
```

---

## Coverage Requirements

| Metric | Target |
|--------|--------|
| Statements | 80% |
| Branches | 80% |
| Functions | 80% |
| Lines | 80% |

```bash
# Run with coverage
npm test -- --coverage
```

---

## Test File Naming

```
src/
├── utils/
│   ├── helper.ts
│   └── helper.test.ts      # Co-located
└── __tests__/
    └── integration.test.ts  # Integration tests
```

---

## Template

```typescript
import { describe, it, expect, beforeEach, vi } from 'vitest';
import { functionName } from './module';

describe('functionName', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  describe('when input is valid', () => {
    it('should return expected result', () => {
      // Arrange
      const input = { /* ... */ };

      // Act
      const result = functionName(input);

      // Assert
      expect(result).toEqual(expected);
    });
  });

  describe('when input is invalid', () => {
    it('should throw error', () => {
      expect(() => functionName(null)).toThrow();
    });
  });

  describe('edge cases', () => {
    it.each([
      [[], 0],
      [[1], 1],
      [[1, 2], 3],
    ])('sum(%j) = %i', (input, expected) => {
      expect(sum(input)).toBe(expected);
    });
  });
});
```

---

## Checklist

- [ ] All public functions have tests
- [ ] Happy path covered
- [ ] Edge cases covered
- [ ] Error cases covered
- [ ] Async behavior tested
- [ ] Mocks properly cleaned up
- [ ] Coverage meets threshold
