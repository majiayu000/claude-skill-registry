---
name: bknd-testing
description: Use when writing tests for Bknd applications, setting up test infrastructure, creating unit/integration tests, or testing API endpoints. Covers in-memory database setup, test helpers, mocking, and test patterns.
---

# Testing Bknd Applications

Write and run tests for Bknd applications using Bun Test or Vitest with in-memory databases for isolation.

## Prerequisites

- Bknd project set up locally
- Test runner installed (Bun or Vitest)
- Understanding of async/await patterns

## When to Use UI Mode

- Manual integration testing via admin panel
- Verifying data after test runs
- Quick smoke testing

## When to Use Code Mode

- Automated unit tests
- Integration tests
- CI/CD pipelines
- Regression testing

## Test Runner Setup

### Bun (Recommended)

Bun has a built-in test runner:

```bash
# Run all tests
bun test

# Run specific file
bun test tests/posts.test.ts

# Watch mode
bun test --watch
```

### Vitest

```bash
# Install
bun add -D vitest

# Configure vitest.config.ts
import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    globals: true,
  },
});

# Run
npx vitest
```

## In-Memory Database Setup

Use in-memory SQLite for fast, isolated tests.

### Test Helper Module

Create `tests/helper.ts`:

```typescript
import { App, createApp as baseCreateApp } from "bknd";
import { em, entity, text, number, boolean } from "bknd";
import Database from "libsql";

// Schema for tests
export const testSchema = em({
  posts: entity("posts", {
    title: text().required(),
    content: text(),
    published: boolean(),
  }),
  comments: entity("comments", {
    body: text().required(),
    author: text(),
  }),
}, (fn, s) => {
  fn.relation(s.comments).manyToOne(s.posts);
});

// Create isolated test app with in-memory DB
export async function createTestApp(options?: {
  seed?: (app: App) => Promise<void>;
}) {
  const db = new Database(":memory:");

  const app = new App({
    connection: { database: db },
    schema: testSchema,
  });

  await app.build();

  if (options?.seed) {
    await options.seed(app);
  }

  return {
    app,
    cleanup: () => {
      db.close();
    },
  };
}

// Create test API client
export async function createTestClient(app: App) {
  const baseUrl = "http://localhost:0"; // Placeholder

  return {
    data: app.modules.data,
    auth: app.modules.auth,
  };
}
```

### Bun-Specific Helper

For Bun's native SQLite:

```typescript
import { bunSqlite } from "bknd/adapter/bun";
import { Database } from "bun:sqlite";

export function createTestConnection() {
  const db = new Database(":memory:");
  return bunSqlite({ database: db });
}
```

## Unit Testing Patterns

### Testing Entity Operations

```typescript
import { describe, test, expect, beforeEach, afterEach } from "bun:test";
import { createTestApp } from "./helper";

describe("Posts", () => {
  let app: Awaited<ReturnType<typeof createTestApp>>;

  beforeEach(async () => {
    app = await createTestApp();
  });

  afterEach(() => {
    app.cleanup();
  });

  test("creates a post", async () => {
    const result = await app.app.em
      .mutator("posts")
      .insertOne({ title: "Test Post", content: "Hello" });

    expect(result.id).toBeDefined();
    expect(result.title).toBe("Test Post");
  });

  test("reads posts", async () => {
    // Seed data
    await app.app.em.mutator("posts").insertOne({ title: "Post 1" });
    await app.app.em.mutator("posts").insertOne({ title: "Post 2" });

    const posts = await app.app.em.repo("posts").findMany();

    expect(posts).toHaveLength(2);
  });

  test("updates a post", async () => {
    const created = await app.app.em
      .mutator("posts")
      .insertOne({ title: "Original" });

    const updated = await app.app.em
      .mutator("posts")
      .updateOne(created.id, { title: "Updated" });

    expect(updated.title).toBe("Updated");
  });

  test("deletes a post", async () => {
    const created = await app.app.em
      .mutator("posts")
      .insertOne({ title: "To Delete" });

    await app.app.em.mutator("posts").deleteOne(created.id);

    const found = await app.app.em.repo("posts").findOne(created.id);
    expect(found).toBeNull();
  });
});
```

### Testing Relationships

```typescript
describe("Comments", () => {
  let app: Awaited<ReturnType<typeof createTestApp>>;

  beforeEach(async () => {
    app = await createTestApp();
  });

  afterEach(() => app.cleanup());

  test("creates comment with relation", async () => {
    const post = await app.app.em
      .mutator("posts")
      .insertOne({ title: "Parent Post" });

    const comment = await app.app.em
      .mutator("comments")
      .insertOne({
        body: "Great post!",
        posts_id: post.id,
      });

    expect(comment.posts_id).toBe(post.id);
  });

  test("loads comments with post", async () => {
    const post = await app.app.em
      .mutator("posts")
      .insertOne({ title: "Post" });

    await app.app.em.mutator("comments").insertOne({
      body: "Comment 1",
      posts_id: post.id,
    });

    const comments = await app.app.em.repo("comments").findMany({
      with: { posts: true },
    });

    expect(comments[0].posts).toBeDefined();
    expect(comments[0].posts.title).toBe("Post");
  });
});
```

## Integration Testing

### HTTP API Testing

Test the full HTTP stack:

```typescript
import { describe, test, expect, beforeAll, afterAll } from "bun:test";
import { serve } from "bknd/adapter/bun";

describe("API Integration", () => {
  let server: ReturnType<typeof Bun.serve>;
  const port = 3999;
  const baseUrl = `http://localhost:${port}`;

  beforeAll(async () => {
    server = Bun.serve({
      port,
      fetch: (await serve({
        connection: { url: ":memory:" },
        schema: testSchema,
      })).fetch,
    });
  });

  afterAll(() => {
    server.stop();
  });

  test("GET /api/data/posts returns 200", async () => {
    const res = await fetch(`${baseUrl}/api/data/posts`);
    expect(res.status).toBe(200);

    const data = await res.json();
    expect(data).toEqual({ data: [] });
  });

  test("POST /api/data/posts creates record", async () => {
    const res = await fetch(`${baseUrl}/api/data/posts`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title: "API Test" }),
    });

    expect(res.status).toBe(201);

    const { data } = await res.json();
    expect(data.title).toBe("API Test");
  });
});
```

### Testing with SDK Client

```typescript
import { Api } from "bknd/client";

describe("SDK Integration", () => {
  let api: Api;
  let server: ReturnType<typeof Bun.serve>;

  beforeAll(async () => {
    // Start test server
    server = await startTestServer();
    api = new Api({ host: "http://localhost:3999" });
  });

  afterAll(() => server.stop());

  test("creates and reads via SDK", async () => {
    const created = await api.data.createOne("posts", {
      title: "SDK Test",
    });

    expect(created.ok).toBe(true);

    const read = await api.data.readOne("posts", created.data.id);
    expect(read.data.title).toBe("SDK Test");
  });
});
```

## Testing Authentication

### Auth Flow Testing

```typescript
describe("Authentication", () => {
  let app: Awaited<ReturnType<typeof createTestApp>>;

  beforeEach(async () => {
    app = await createTestApp({
      auth: {
        enabled: true,
        strategies: {
          password: {
            hashing: "plain", // Only for tests!
          },
        },
      },
    });
  });

  afterEach(() => app.cleanup());

  test("registers a user", async () => {
    const auth = app.app.modules.auth;

    const result = await auth.register({
      email: "test@example.com",
      password: "password123",
    });

    expect(result.user).toBeDefined();
    expect(result.user.email).toBe("test@example.com");
  });

  test("login with correct password", async () => {
    const auth = app.app.modules.auth;

    // Register first
    await auth.register({
      email: "test@example.com",
      password: "password123",
    });

    // Then login
    const result = await auth.login({
      email: "test@example.com",
      password: "password123",
    });

    expect(result.token).toBeDefined();
  });

  test("login with wrong password fails", async () => {
    const auth = app.app.modules.auth;

    await auth.register({
      email: "test@example.com",
      password: "correct",
    });

    await expect(
      auth.login({
        email: "test@example.com",
        password: "wrong",
      })
    ).rejects.toThrow();
  });
});
```

## Mocking Patterns

### Mocking Fetch

```typescript
import { mock, jest } from "bun:test";

describe("External API calls", () => {
  let originalFetch: typeof fetch;

  beforeAll(() => {
    originalFetch = global.fetch;
    // @ts-ignore
    global.fetch = jest.fn(() =>
      Promise.resolve(
        new Response(JSON.stringify({ success: true }), {
          status: 200,
          headers: { "Content-Type": "application/json" },
        })
      )
    );
  });

  afterAll(() => {
    global.fetch = originalFetch;
  });

  test("FetchTask uses mocked fetch", async () => {
    const task = new FetchTask("test", {
      url: "https://api.example.com/data",
      method: "GET",
    });

    const result = await task.run();
    expect(result.success).toBe(true);
    expect(global.fetch).toHaveBeenCalled();
  });
});
```

### Mocking Drivers

```typescript
describe("Email sending", () => {
  test("uses mock email driver", async () => {
    const sentEmails: any[] = [];

    const app = await createTestApp({
      drivers: {
        email: {
          send: async (to, subject, body) => {
            sentEmails.push({ to, subject, body });
            return { id: "mock-id" };
          },
        },
      },
    });

    // Trigger something that sends email
    await app.app.drivers.email.send(
      "user@example.com",
      "Test",
      "Body"
    );

    expect(sentEmails).toHaveLength(1);
    expect(sentEmails[0].to).toBe("user@example.com");

    app.cleanup();
  });
});
```

## Test Data Factories

Create reusable factories for test data:

```typescript
// tests/factories.ts
let counter = 0;

export function createPostData(overrides = {}) {
  counter++;
  return {
    title: `Test Post ${counter}`,
    content: `Content for post ${counter}`,
    published: false,
    ...overrides,
  };
}

export function createUserData(overrides = {}) {
  counter++;
  return {
    email: `user${counter}@test.com`,
    password: "password123",
    ...overrides,
  };
}

// Usage in tests
test("creates multiple posts", async () => {
  const posts = await Promise.all([
    app.em.mutator("posts").insertOne(createPostData()),
    app.em.mutator("posts").insertOne(createPostData({ published: true })),
    app.em.mutator("posts").insertOne(createPostData()),
  ]);

  expect(posts).toHaveLength(3);
});
```

## Testing Flows

```typescript
import { Flow, FetchTask, Condition } from "bknd/flows";

describe("Flows", () => {
  test("executes flow with tasks", async () => {
    const task1 = new FetchTask("fetch", {
      url: "https://example.com/api",
      method: "GET",
    });

    const flow = new Flow("testFlow", [task1]);

    const execution = await flow.start({ input: "value" });

    expect(execution.hasErrors()).toBe(false);
    expect(execution.getResponse()).toBeDefined();
  });

  test("handles task errors", async () => {
    const failingTask = new FetchTask("fail", {
      url: "https://invalid-url-that-fails.test",
      method: "GET",
    });

    const flow = new Flow("failFlow", [failingTask]);
    const execution = await flow.start({});

    expect(execution.hasErrors()).toBe(true);
    expect(execution.getErrors()).toHaveLength(1);
  });
});
```

## CI/CD Configuration

### GitHub Actions

```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: oven-sh/setup-bun@v1
        with:
          bun-version: latest

      - run: bun install
      - run: bun test
```

### Pre-commit Hook

```bash
# .husky/pre-commit
#!/bin/sh
bun test --bail
```

## Project Structure

```
my-bknd-app/
├── src/
│   └── ...
├── tests/
│   ├── helper.ts          # Test utilities
│   ├── factories.ts       # Data factories
│   ├── unit/
│   │   ├── posts.test.ts
│   │   └── auth.test.ts
│   └── integration/
│       ├── api.test.ts
│       └── flows.test.ts
├── bknd.config.ts
└── package.json
```

## Common Pitfalls

### Database Not Isolated

**Problem:** Tests share state, causing flaky tests.

**Solution:** Create fresh in-memory DB per test:

```typescript
beforeEach(async () => {
  app = await createTestApp();  // New DB each time
});

afterEach(() => {
  app.cleanup();  // Close connection
});
```

### Async Cleanup Issues

**Problem:** Tests hang or leak resources.

**Solution:** Always await cleanup:

```typescript
afterEach(async () => {
  await app.cleanup();
});

afterAll(async () => {
  await server.stop();
});
```

### Missing await on Assertions

**Problem:** Test passes before async operation completes.

**Solution:** Always await async operations:

```typescript
// WRONG
test("fails silently", () => {
  expect(api.data.readMany("posts")).resolves.toBeDefined();
});

// CORRECT
test("properly awaited", async () => {
  const result = await api.data.readMany("posts");
  expect(result).toBeDefined();
});
```

### Testing Against Production DB

**Problem:** Tests modify real data.

**Solution:** Always use `:memory:` or test-specific file:

```typescript
// SAFE
connection: { url: ":memory:" }

// ALSO SAFE
connection: { url: "file:test-${Date.now()}.db" }

// DANGEROUS - never in tests
connection: { url: process.env.DB_URL }
```

## DOs and DON'Ts

**DO:**
- Use in-memory databases for speed and isolation
- Clean up resources in afterEach/afterAll
- Create test helpers and factories
- Test both success and error paths
- Use meaningful test descriptions
- Keep tests independent of each other

**DON'T:**
- Share database state between tests
- Use production credentials in tests
- Skip await on async operations
- Write tests that depend on execution order
- Use `plain` password hashing outside tests
- Commit test database files

## Related Skills

- **bknd-local-setup** - Development environment setup
- **bknd-debugging** - Troubleshooting test failures
- **bknd-seed-data** - Creating test data patterns
- **bknd-crud-create** - Understanding data operations
- **bknd-setup-auth** - Auth configuration for tests
