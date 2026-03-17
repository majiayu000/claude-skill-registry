---
name: unit-test-implementation
description: Best practices for implementing unit tests in this TypeScript monorepo. Use when writing new tests, refactoring existing tests, or fixing failing tests. Covers mocking strategies, test organization, helper functions, and assertion patterns.
---

# Unit Test Implementation Guide

## Mocking Dependencies

### Use jest-mock-extended for External Dependencies

Use `jest-mock-extended` for dependencies that are external to the unit under test:

```typescript
import { mock, mockDeep, mockFn, type MockProxy } from "jest-mock-extended";

let httpClient: MockProxy<HttpClient>;
let database: MockProxy<Database>;

beforeEach(() => {
  httpClient = mock<HttpClient>();
  database = mockDeep<Database>(); // Use mockDeep when mocking nested properties
});
```

### When to Use Real Instances vs Mocks

**Mock external dependencies** that are:

- Difficult to set up and not to relevant to the behavior being tested
- External services or APIs

**Use real instances** for dependencies that are:

- Tightly coupled to the subject (e.g., a config object, a small utility class)
- Pure functions or simple data transformers
- Part of the same module and tested together

**When in doubt, ask the user** which dependencies should be mocked and which should use real instances. The decision depends on what behavior you're trying to test.

### Prefer mockReturnValueOnce Over Complex mockImplementation

```typescript
// ❌ Bad: Counter-based implementation
let callCount = 0;
mock.fetch.mockImplementation(() => {
  callCount++;
  return callCount === 1 ? responseA : responseB;
});

// ✅ Good: Clear sequence of return values
mock.fetch
  .mockReturnValueOnce(responseA)
  .mockReturnValueOnce(responseB)
  .mockReturnValue(defaultResponse);
```

### When Mock Behavior Becomes Too Complex, Create a Mock Class

If mocking requires complex state management (tracking multiple calls, conditional responses based on arguments, etc.), create a proper fake implementation instead:

```typescript
/**
 * A fake implementation for testing. Does NOT use jest mocks internally.
 * Implements the same interface as the real class.
 */
export class MockCache {
  private store = new Map<string, Item>();

  // Track calls for assertions
  public getCalls: string[] = [];
  public setCalls: Array<{ key: string; value: Item }> = [];

  async get(key: string): Promise<Item | undefined> {
    this.getCalls.push(key);
    return this.store.get(key);
  }

  async set(key: string, value: Item): Promise<void> {
    this.setCalls.push({ key, value });
    this.store.set(key, value);
  }

  /** Seed data for testing */
  seed(entries: Array<[string, Item]>): this {
    entries.forEach(([k, v]) => this.store.set(k, v));
    return this;
  }

  /** Reset for reuse */
  reset(): void {
    this.store.clear();
    this.getCalls = [];
    this.setCalls = [];
  }
}
```

## Exposing Internals for Testing

### Use a Derived Test Class

When you need to access or modify internal state, create a test subclass that exposes protected members:

**Base class (production code):**

```typescript
class MyService {
  protected config: Config;

  constructor(config: Config) {
    this.config = config;
  }

  protected async waitUntilReady(): Promise<void> {
    await sleep(1000);
  }

  async execute(): Promise<Result> {
    await this.waitUntilReady();
    // ... implementation
  }
}
```

**Test class (test file):**

```typescript
class TestMyService extends MyService {
  /** Override to skip delays in tests */
  protected override async waitUntilReady(): Promise<void> {
    return Promise.resolve();
  }

  /** Expose config for modification */
  public updateConfig(partial: Partial<Config>): void {
    this.config = { ...this.config, ...partial };
  }

  /** Expose config for assertions */
  public getConfig(): Config {
    return this.config;
  }
}
```

**Note:** This requires the base class to use `protected` (not `private`) for members you need to access. Feel free to modify the base class for this when writing its unit tests.

## Test Organization

### Move Setup Logic to beforeEach

```typescript
describe("MyFeature", () => {
  let subject: TestMyService;
  let dependency: MockProxy<Dependency>;

  beforeEach(() => {
    dependency = mock<Dependency>();
    subject = new TestMyService(dependency);
  });

  // Tests modify subject via update methods, not direct mutation
});
```

### Use Nested beforeEach for Variations

```typescript
describe("with caching enabled", () => {
  beforeEach(() => {
    subject.updateConfig({ cacheEnabled: true });
  });

  it("returns cached results", async () => {
    /* ... */
  });
});

describe("with caching disabled", () => {
  beforeEach(() => {
    subject.updateConfig({ cacheEnabled: false });
  });

  it("always fetches fresh data", async () => {
    /* ... */
  });
});
```

### Avoid Direct Object Mutation

```typescript
// ❌ Bad: Direct mutation
config.maxRetries = 5;

// ✅ Good: Use update methods
subject.updateConfig({ maxRetries: 5 });
```

## Helper Functions for Readability

### Extract Repeated Setup Patterns

When you find yourself repeating the same 3-4 setup calls across multiple tests, extract them:

```typescript
// ❌ Bad: Repeated in every test
it("test 1", async () => {
  const items = await Promise.all([createItem(1), createItem(2)]);
  mockSource.getItems.mockResolvedValue(items);
  mockValidator.validate.mockResolvedValue(true);
  // ... actual test
});

it("test 2", async () => {
  const items = await Promise.all([createItem(1), createItem(2)]);
  mockSource.getItems.mockResolvedValue(items);
  mockValidator.validate.mockResolvedValue(true);
  // ... actual test
});

// ✅ Good: Extracted helper
async function setupValidItems(count: number) {
  const items = await Promise.all(times(count, (i) => createItem(i)));
  mockSource.getItems.mockResolvedValue(items);
  mockValidator.validate.mockResolvedValue(true);
  return items;
}

it("test 1", async () => {
  const items = await setupValidItems(2);
  // ... actual test
});
```

### Extract Repeated Assertion Patterns

When the same assertion sequence appears in multiple tests:

```typescript
// ❌ Bad: Repeated in every test
it("test 1", async () => {
  await subject.publish();

  expect(publisher.enqueue).toHaveBeenCalledTimes(1);
  expect(publisher.enqueue).toHaveBeenCalledWith(
    expect.objectContaining({ type: "proposal" }),
    expect.any(Date)
  );
  expect(publisher.send).toHaveBeenCalled();
});

// ✅ Good: Extracted helper
const expectPublished = () => {
  expect(publisher.enqueue).toHaveBeenCalledTimes(1);
  expect(publisher.enqueue).toHaveBeenCalledWith(
    expect.objectContaining({ type: "proposal" }),
    expect.any(Date)
  );
  expect(publisher.send).toHaveBeenCalled();
};

it("test 1", async () => {
  await subject.publish();
  expectPublished();
});
```

**Note:** Only extract when the pattern repeats across multiple tests. A single complex assertion block doesn't need extraction.

### Helper Location

- **Suite-specific helpers:** Define inside the describe block
- **Package-shared helpers:** Move to `src/test/utils.ts`
- **Cross-package helpers:** Consider if they belong in a shared testing package

## Assertions

### Be Specific

```typescript
// ❌ Too generic - doesn't verify actual behavior
expect(mock.save).toHaveBeenCalledWith(expect.anything());

// ✅ Specific - verifies the important parts
expect(mock.save).toHaveBeenCalledWith(
  expect.objectContaining({
    id: expectedId,
    status: "active",
  })
);
```

### Use Mock Class Properties for Assertions

When using custom mock classes, assert on tracked properties:

```typescript
expect(mockCache.getCalls).toEqual(["key1", "key2"]);
expect(mockCache.setCalls).toHaveLength(1);
expect(mockCache.setCalls[0]).toEqual({ key: "key1", value: expectedValue });
```

## Reusable Test Suites

For testing multiple implementations of the same interface (e.g., in-memory vs persistent storage), create a shared test suite:

```typescript
// cache_test_suite.ts
export function describeCacheImplementation(
  name: string,
  createCache: () => Cache
) {
  describe(name, () => {
    let cache: Cache;

    beforeEach(() => {
      cache = createCache();
    });

    it("stores and retrieves values", async () => {
      await cache.set("key", "value");
      expect(await cache.get("key")).toBe("value");
    });

    it("returns undefined for missing keys", async () => {
      expect(await cache.get("missing")).toBeUndefined();
    });
  });
}

// memory_cache.test.ts
describeCacheImplementation("MemoryCache", () => new MemoryCache());

// redis_cache.test.ts
describeCacheImplementation("RedisCache", () => new RedisCache(mockClient));
```

## Testing Async Operations

### Use Promise.allSettled for Multiple Outcomes

```typescript
it("handles mixed success and failure", async () => {
  const results = await Promise.allSettled([
    subject.processValid(),
    subject.processInvalid(),
  ]);

  expect(results).toEqual([
    { status: "fulfilled", value: expectedValue },
    {
      status: "rejected",
      reason: expect.objectContaining({ message: "Invalid" }),
    },
  ]);
});
```

### Control Time in Tests

```typescript
beforeEach(() => {
  jest.useFakeTimers();
});

afterEach(() => {
  jest.useRealTimers();
});

it("retries after delay", async () => {
  mock.fetch.mockRejectedValueOnce(new Error("fail")).mockResolvedValue(data);

  const promise = subject.fetchWithRetry();

  await jest.advanceTimersByTimeAsync(1000);

  await expect(promise).resolves.toEqual(data);
});
```

## Running Tests

```bash
yarn build                                                              # Always compile first (from yarn-project root)
yarn workspace @aztec/<package-name> test my-class.test.ts              # Run specific test file
yarn workspace @aztec/<package-name> test my-class.test.ts -t 'test name'  # Run specific test
LOG_LEVEL=verbose yarn workspace @aztec/<package-name> test my-class.test.ts  # With debug logging
```
