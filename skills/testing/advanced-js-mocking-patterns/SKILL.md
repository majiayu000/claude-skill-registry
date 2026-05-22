---
name: advanced-js-mocking-patterns
version: "1.0"
description: >
  Advanced mocking patterns for Jest and Vitest including module mocking, spies, and fake timers.
  PROACTIVELY activate for: (1) Module mocking, (2) Partial mocking with spies,
  (3) Mock lifecycle management, (4) Fake timers for time-dependent code, (5) Complex mock implementations.
  Triggers: "jest.mock", "vi.mock", "spyOn", "fakeTimers", "mockImplementation", "mockReturnValue", "mock lifecycle"
core-integration:
  techniques:
    primary: ["exhaustive_edge_case_enumeration"]
    secondary: ["completeness_verification"]
  contracts:
    input: "none"
    output: "none"
  patterns: "none"
  rubrics: "none"
---

# Advanced JS Mocking Patterns Skill

## Metadata (Tier 1)

**Keywords**: jest.mock, vi.mock, spyOn, fakeTimers, mockImplementation

**File Patterns**: *.test.ts, *.spec.js

**Modes**: testing_frontend, testing_backend

---

## Instructions (Tier 2)

### Module Mocking

```typescript
// Mock entire module
jest.mock('axios');

import axios from 'axios';

test('fetches data', async () => {
  (axios.get as jest.Mock).mockResolvedValue({ data: { id: 1 } });

  const result = await fetchUser(1);

  expect(result).toEqual({ id: 1 });
});
```

### Spies (Partial Mocking)

```typescript
const obj = {
  method1: () => 'original',
  method2: () => 'original'
};

const spy = jest.spyOn(obj, 'method1');
spy.mockReturnValue('mocked');

obj.method1(); // 'mocked'
obj.method2(); // 'original' (not mocked)

expect(spy).toHaveBeenCalled();
```

### Mock Lifecycle

```typescript
beforeEach(() => {
  jest.clearAllMocks();  // Reset call counts
});

afterEach(() => {
  jest.restoreAllMocks();  // Restore original implementations
});
```

### Fake Timers

```typescript
jest.useFakeTimers();

test('debounce function', () => {
  const callback = jest.fn();
  const debounced = debounce(callback, 1000);

  debounced();
  debounced();
  debounced();

  jest.advanceTimersByTime(1000);

  expect(callback).toHaveBeenCalledTimes(1);  // Only last call
});
```

### Mock Implementations

```typescript
const mock = jest.fn()
  .mockImplementationOnce(() => 'first')
  .mockImplementationOnce(() => 'second')
  .mockImplementation(() => 'default');

mock(); // 'first'
mock(); // 'second'
mock(); // 'default'
```

### Anti-Patterns

- Not clearing mocks between tests
- Over-mocking (testing implementation)
- Mocking internal modules
- Forgetting to restore timers
