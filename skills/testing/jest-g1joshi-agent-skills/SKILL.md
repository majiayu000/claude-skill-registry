---
name: jest
description: Jest JavaScript testing framework with snapshots. Use for JS testing.
---

# Jest

Jest is a delightful JavaScript Testing Framework with a focus on simplicity. It works with projects using: Babel, TypeScript, Node, React, Angular, Vue, and more.

## When to Use

- **React Apps**: The default and most supported runner for Create React App / Next.js (historically).
- **Snapshot Testing**: When you want to ensure UI or JSON structures haven't changed unexpectedly.
- **Legacy/Standard**: Extensive community plugins and support.

## Quick Start

```javascript
// sum.js
function sum(a, b) {
  return a + b;
}
module.exports = sum;

// sum.test.js
const sum = require("./sum");

test("adds 1 + 2 to equal 3", () => {
  expect(sum(1, 2)).toBe(3);
});
```

## Core Concepts

### Matchers

Jest uses "matchers" to test values.

- `toBe(value)`: Exact equality (Object.is).
- `toEqual(value)`: Recursive equality (great for Objects/Arrays).
- `toContain(item)`: Checks if an array contains an item.

### Mock Functions

`jest.fn()` creates a mock function. You can track calls, arguments, and instances.

```javascript
const mockCallback = jest.fn((x) => 42 + x);
forEach([0, 1], mockCallback);
expect(mockCallback.mock.calls.length).toBe(2);
```

### Async Testing

Jest supports `async/await`.

```javascript
test("data is peanut butter", async () => {
  const data = await fetchData();
  expect(data).toBe("peanut butter");
});
```

## Best Practices (2025)

**Do**:

- **Use `test.each`**: For data-driven tests. Avoid writing valid/invalid test cases manually 10 times.
- **Isolate Tests**: Tests should not depend on each other. Jest runs them in parallel.
- **Mock External APIs**: Never hit real APIs in unit tests. Use `jest.mock`.

**Don't**:

- **Don't overuse Snapshots**: Large snapshots are impossible to review. Use them for small, critical structures.
- **Don't ignore "Unhandled Promise Rejection"**: It usually means a test finished before an async operation completed.

## References

- [Jest Documentation](https://jestjs.io/)
