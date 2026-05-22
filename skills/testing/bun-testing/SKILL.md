---
name: jutsu-bun:bun-testing
description: Use when writing tests with Bun's built-in test runner. Covers test organization, assertions, mocking, and snapshot testing using Bun's fast test infrastructure.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
---

# Bun Testing

Use this skill when writing tests with Bun's built-in test runner, which provides Jest-compatible APIs with significantly faster execution.

## Key Concepts

### Test Runner Basics

Bun includes a built-in test runner that works out of the box:

```typescript
import { test, expect, describe, beforeAll, afterAll } from "bun:test";

describe("Math operations", () => {
  test("addition", () => {
    expect(1 + 1).toBe(2);
  });

  test("subtraction", () => {
    expect(5 - 3).toBe(2);
  });
});
```

### Running Tests

```bash
# Run all tests
bun test

# Run specific test file
bun test ./src/utils.test.ts

# Run with coverage
bun test --coverage

# Watch mode
bun test --watch
```

### Matchers and Assertions

Bun supports Jest-compatible matchers:

```typescript
import { test, expect } from "bun:test";

test("matchers", () => {
  // Equality
  expect(42).toBe(42);
  expect({ a: 1 }).toEqual({ a: 1 });

  // Truthiness
  expect(true).toBeTruthy();
  expect(false).toBeFalsy();
  expect(null).toBeNull();
  expect(undefined).toBeUndefined();

  // Numbers
  expect(10).toBeGreaterThan(5);
  expect(3).toBeLessThan(5);
  expect(3.14).toBeCloseTo(3.1, 1);

  // Strings
  expect("hello world").toContain("hello");
  expect("test@example.com").toMatch(/^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$/);

  // Arrays
  expect([1, 2, 3]).toContain(2);
  expect([1, 2, 3]).toHaveLength(3);

  // Objects
  expect({ a: 1, b: 2 }).toHaveProperty("a");
  expect({ a: 1, b: 2 }).toMatchObject({ a: 1 });

  // Errors
  expect(() => {
    throw new Error("Test error");
  }).toThrow("Test error");
});
```

## Best Practices

### Organize Tests with describe/test

Structure tests in a clear hierarchy:

```typescript
import { describe, test, expect } from "bun:test";

describe("UserService", () => {
  describe("createUser", () => {
    test("creates user with valid data", () => {
      // Test implementation
    });

    test("throws error with invalid email", () => {
      // Test implementation
    });
  });

  describe("findUser", () => {
    test("finds existing user by id", () => {
      // Test implementation
    });

    test("returns null for non-existent user", () => {
      // Test implementation
    });
  });
});
```

### Use Setup and Teardown Hooks

Clean up state between tests:

```typescript
import { describe, test, beforeAll, afterAll, beforeEach, afterEach } from "bun:test";

describe("Database tests", () => {
  beforeAll(() => {
    // Run once before all tests
    console.log("Setting up test database");
  });

  afterAll(() => {
    // Run once after all tests
    console.log("Tearing down test database");
  });

  beforeEach(() => {
    // Run before each test
    console.log("Resetting test data");
  });

  afterEach(() => {
    // Run after each test
    console.log("Cleaning up test data");
  });

  test("example test", () => {
    expect(true).toBe(true);
  });
});
```

### Mocking with Bun

Use Bun's built-in mocking:

```typescript
import { test, expect, mock } from "bun:test";

test("mocking functions", () => {
  const mockFn = mock((x: number) => x * 2);

  mockFn(2);
  mockFn(3);

  expect(mockFn).toHaveBeenCalledTimes(2);
  expect(mockFn).toHaveBeenCalledWith(2);
  expect(mockFn).toHaveBeenCalledWith(3);
  expect(mockFn.mock.results[0].value).toBe(4);
});

test("mocking modules", async () => {
  // Mock a module
  mock.module("./api", () => ({
    fetchData: mock(() => Promise.resolve({ data: "mocked" })),
  }));

  const { fetchData } = await import("./api");
  const result = await fetchData();

  expect(result).toEqual({ data: "mocked" });
});
```

### Async Testing

Handle asynchronous code properly:

```typescript
import { test, expect } from "bun:test";

test("async function", async () => {
  const data = await fetchData();
  expect(data).toBeDefined();
});

test("promises", () => {
  return fetchData().then((data) => {
    expect(data).toBeDefined();
  });
});

test("async/await with error", async () => {
  await expect(async () => {
    await fetchInvalidData();
  }).toThrow("Invalid data");
});
```

## Common Patterns

### Testing HTTP Endpoints

```typescript
import { describe, test, expect } from "bun:test";

describe("API endpoints", () => {
  test("GET /api/users returns users list", async () => {
    const response = await fetch("http://localhost:3000/api/users");
    const users = await response.json();

    expect(response.status).toBe(200);
    expect(Array.isArray(users)).toBe(true);
  });

  test("POST /api/users creates new user", async () => {
    const newUser = { name: "Alice", email: "alice@example.com" };

    const response = await fetch("http://localhost:3000/api/users", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(newUser),
    });

    expect(response.status).toBe(201);

    const user = await response.json();
    expect(user).toMatchObject(newUser);
    expect(user.id).toBeDefined();
  });
});
```

### Testing File Operations

```typescript
import { test, expect, beforeEach, afterEach } from "bun:test";
import { unlink } from "fs/promises";

describe("File operations", () => {
  const testFile = "./test-output.txt";

  afterEach(async () => {
    try {
      await unlink(testFile);
    } catch {}
  });

  test("writes file successfully", async () => {
    await Bun.write(testFile, "test content");

    const file = Bun.file(testFile);
    expect(await file.exists()).toBe(true);

    const content = await file.text();
    expect(content).toBe("test content");
  });
});
```

### Snapshot Testing

```typescript
import { test, expect } from "bun:test";

test("snapshot test", () => {
  const data = {
    id: 1,
    name: "Alice",
    email: "alice@example.com",
  };

  expect(data).toMatchSnapshot();
});
```

### Parameterized Tests

```typescript
import { test, expect } from "bun:test";

const testCases = [
  { input: 1, expected: 2 },
  { input: 2, expected: 4 },
  { input: 3, expected: 6 },
];

testCases.forEach(({ input, expected }) => {
  test(`double(${input}) should equal ${expected}`, () => {
    expect(double(input)).toBe(expected);
  });
});
```

### Testing with Timers

```typescript
import { test, expect } from "bun:test";

test("delayed execution", async () => {
  let executed = false;

  setTimeout(() => {
    executed = true;
  }, 100);

  await new Promise((resolve) => setTimeout(resolve, 150));

  expect(executed).toBe(true);
});
```

## Anti-Patterns

### Don't Use External Test Runners

```typescript
// Bad - Installing Jest or other test runners
// package.json
{
  "devDependencies": {
    "jest": "^29.0.0"
  }
}

// Good - Use Bun's built-in test runner
bun test
```

### Don't Forget to Clean Up

```typescript
// Bad - Test pollution
test("test 1", () => {
  globalState.value = 10;
  expect(globalState.value).toBe(10);
});

test("test 2", () => {
  // May fail due to test 1's state
  expect(globalState.value).toBe(0);
});

// Good - Clean state
import { beforeEach } from "bun:test";

beforeEach(() => {
  globalState.value = 0;
});
```

### Don't Test Implementation Details

```typescript
// Bad - Testing private methods
test("private method", () => {
  const instance = new MyClass();
  expect(instance._privateMethod()).toBe(true);
});

// Good - Test public API
test("public behavior", () => {
  const instance = new MyClass();
  const result = instance.publicMethod();
  expect(result).toBe(expectedValue);
});
```

### Don't Write Flaky Tests

```typescript
// Bad - Timing-dependent test
test("flaky test", () => {
  setTimeout(() => {
    expect(value).toBe(10);
  }, 50); // May fail on slow systems
});

// Good - Deterministic test
test("reliable test", async () => {
  await performAsyncOperation();
  expect(value).toBe(10);
});
```

## Related Skills

- **bun-runtime**: Core Bun runtime APIs and functionality
- **bun-package-manager**: Managing test dependencies
- **bun-bundler**: Building test files for different environments
