---
name: bun-test-lifecycle
description: 'Use for test lifecycle hooks: beforeAll, afterAll, beforeEach, afterEach,
  fixtures, preload.'
---

---
name: Bun Test Lifecycle
description: Use for test lifecycle hooks: beforeAll, afterAll, beforeEach, afterEach, fixtures, preload.
version: 1.0.0
---

# Bun Test Lifecycle

Bun supports Jest-compatible lifecycle hooks for test setup and teardown.

## Lifecycle Hooks

```typescript
import { test, expect, beforeAll, afterAll, beforeEach, afterEach } from "bun:test";

let db: Database;
let testData: any;

// Runs once before all tests in file
beforeAll(async () => {
  db = await Database.connect();
});

// Runs once after all tests in file
afterAll(async () => {
  await db.close();
});

// Runs before each test
beforeEach(() => {
  testData = { id: 1, name: "test" };
});

// Runs after each test
afterEach(() => {
  testData = null;
});

test("example", () => {
  expect(testData.name).toBe("test");
});
```

## Hook Execution Order

```
beforeAll
  ├── beforeEach
  │   └── test 1
  │   └── afterEach
  ├── beforeEach
  │   └── test 2
  │   └── afterEach
afterAll
```

## Nested Describe Hooks

```typescript
import { describe, test, beforeAll, beforeEach, afterEach, afterAll } from "bun:test";

describe("outer", () => {
  beforeAll(() => console.log("1. outer beforeAll"));
  afterAll(() => console.log("6. outer afterAll"));
  beforeEach(() => console.log("2. outer beforeEach"));
  afterEach(() => console.log("5. outer afterEach"));

  describe("inner", () => {
    beforeEach(() => console.log("3. inner beforeEach"));
    afterEach(() => console.log("4. inner afterEach"));

    test("test", () => {
      console.log("test runs here");
    });
  });
});

// Output:
// 1. outer beforeAll
// 2. outer beforeEach
// 3. inner beforeEach
// test runs here
// 4. inner afterEach
// 5. outer afterEach
// 6. outer afterAll
```

## Async Hooks

```typescript
beforeAll(async () => {
  await setupDatabase();
});

beforeEach(async () => {
  await seedTestData();
});

afterEach(async () => {
  await clearTestData();
});

afterAll(async () => {
  await teardownDatabase();
});
```

## Timeout for Hooks

```typescript
// Set timeout for slow setup
beforeAll(async () => {
  await slowSetup();
}, 30000); // 30 seconds
```

## Preload Scripts

Use `--preload` for global setup across all test files:

```bash
bun test --preload ./setup.ts
```

### setup.ts

```typescript
import { beforeAll, afterAll } from "bun:test";

// Global setup
beforeAll(() => {
  console.log("Global setup runs before all test files");
});

// Global teardown
afterAll(() => {
  console.log("Global teardown runs after all test files");
});

// Set global variables
globalThis.testConfig = {
  apiUrl: "http://localhost:3000",
};
```

### Configure in bunfig.toml

```toml
[test]
preload = ["./test/setup.ts"]
```

## Common Patterns

### Database Setup

```typescript
import { beforeAll, afterAll, beforeEach, afterEach } from "bun:test";

let db: Database;

beforeAll(async () => {
  db = await Database.connect(process.env.TEST_DB_URL);
  await db.migrate();
});

afterAll(async () => {
  await db.close();
});

beforeEach(async () => {
  await db.beginTransaction();
});

afterEach(async () => {
  await db.rollback(); // Reset state
});
```

### Server Setup

```typescript
import { beforeAll, afterAll } from "bun:test";

let server: Server;
let baseUrl: string;

beforeAll(async () => {
  server = Bun.serve({
    port: 0, // Random available port
    fetch: app.fetch,
  });
  baseUrl = `http://localhost:${server.port}`;
});

afterAll(() => {
  server.stop();
});

test("api works", async () => {
  const res = await fetch(`${baseUrl}/api/health`);
  expect(res.ok).toBe(true);
});
```

### Mock Setup

```typescript
import { beforeEach, afterEach, spyOn } from "bun:test";

let fetchSpy: ReturnType<typeof spyOn>;

beforeEach(() => {
  fetchSpy = spyOn(global, "fetch").mockResolvedValue(
    new Response(JSON.stringify({ ok: true }))
  );
});

afterEach(() => {
  fetchSpy.mockRestore();
});
```

### Environment Variables

```typescript
import { beforeAll, afterAll } from "bun:test";

const originalEnv = process.env;

beforeAll(() => {
  process.env = {
    ...originalEnv,
    NODE_ENV: "test",
    API_KEY: "test-key",
  };
});

afterAll(() => {
  process.env = originalEnv;
});
```

## Shared Fixtures

```typescript
// fixtures.ts
export async function createTestUser() {
  return { id: 1, name: "Test User" };
}

export async function cleanupTestUser(user: any) {
  // cleanup logic
}

// test file
import { createTestUser, cleanupTestUser } from "./fixtures";

let user: any;

beforeEach(async () => {
  user = await createTestUser();
});

afterEach(async () => {
  await cleanupTestUser(user);
});
```

## Hook Errors

If a hook throws, all tests in that describe block fail:

```typescript
beforeAll(() => {
  throw new Error("Setup failed");
});

// All tests in this file will fail
test("will fail", () => {
  expect(true).toBe(true);
});
```

## Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `beforeAll timeout` | Slow async setup | Increase timeout |
| `Hook not called` | Wrong scope | Check hook placement |
| `Cleanup not run` | afterAll skipped | Ensure no throws in tests |
| `State leak` | Missing cleanup | Add proper afterEach |

## When to Load References

Load `references/preload-scripts.md` when:
- Complex global setup
- Multiple preload files

Load `references/fixtures.md` when:
- Reusable test fixtures
- Factory patterns
