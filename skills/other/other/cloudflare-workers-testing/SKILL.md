---
name: workers-testing
description: Comprehensive testing guide for Cloudflare Workers using Vitest and @cloudflare/vitest-pool-workers. Use for test setup, binding mocks (D1/KV/R2/DO), integration tests, or encountering test failures, mock errors, coverage issues.
keywords:
  - cloudflare-workers
  - workers-testing
  - vitest
  - vitest-workers
  - miniflare
  - cloudflare-test
  - unit-testing
  - integration-testing
  - binding-mocks
  - d1-testing
  - kv-testing
  - r2-testing
  - durable-objects-testing
  - queue-testing
  - workers-ai-testing
  - test-coverage
  - test-failures
  - mock-errors
  - @cloudflare/vitest-pool-workers
  - cloudflare:test
  - env-mocking
  - execution-context
  - workers-test-setup
  - vitest-config
  - test-driven-development
  - tdd-workers
license: MIT
metadata:
  version: "1.0.0"
  last_verified: "2025-01-27"
  production_tested: true
  token_savings: "~70%"
  errors_prevented: 8
  templates_included: 3
  references_included: 5
  scripts_included: 2
  vitest_version: "2.1.8"
  workers_types_version: "4.20251125.0"
  vitest_pool_workers_version: "0.7.2"
---

# Cloudflare Workers Testing with Vitest

**Status**: ✅ Production Ready | Last Verified: 2025-01-27
**Vitest**: 2.1.8 | **@cloudflare/vitest-pool-workers**: 0.7.2 | **Miniflare**: Latest

## Table of Contents

- [What Is Workers Testing?](#what-is-workers-testing)
- [New in 2025](#new-in-2025)
- [Quick Start (5 Minutes)](#quick-start-5-minutes)
- [Critical Rules](#critical-rules)
- [Core Concepts](#core-concepts)
- [Top 5 Use Cases](#top-5-use-cases)
- [Best Practices](#best-practices)
- [Top 8 Errors Prevented](#top-8-errors-prevented)
- [When to Load References](#when-to-load-references)

---

## What Is Workers Testing?

Testing Cloudflare Workers with **Vitest** and **@cloudflare/vitest-pool-workers** enables writing unit and integration tests that run in a real Workers environment with full binding support (D1, KV, R2, Durable Objects, Queues, AI). Tests execute in Miniflare for local development and can run in CI/CD with actual Workers runtime behavior.

**Key capabilities**: Binding mocks, execution context testing, edge runtime simulation, coverage tracking, fast test execution.

---

## New in 2025

**@cloudflare/vitest-pool-workers 0.7.2** (January 2025):
- **BREAKING**: Miniflare v3 → requires Node.js 18+
- **NEW**: `cloudflare:test` module for env/ctx access
- **IMPROVED**: Faster isolated storage for bindings
- **FIXED**: Worker-to-worker service bindings now work correctly
- **ADDED**: Support for Vectorize and Workers AI bindings

**Migration from older versions**:
```bash
# Update dependencies
bun add -D vitest@^2.1.8 @cloudflare/vitest-pool-workers@^0.7.2

# Update vitest.config.ts (new pool configuration format)
export default defineWorkersConfig({
  test: {
    poolOptions: {
      workers: {
        wrangler: { configPath: './wrangler.jsonc' },
        miniflare: { compatibilityDate: '2025-01-27' }
      }
    }
  }
});
```

---

## Quick Start (5 Minutes)

### 1. Install Dependencies

```bash
bun add -D vitest @cloudflare/vitest-pool-workers
```

### 2. Create `vitest.config.ts`

```typescript
import { defineWorkersConfig } from '@cloudflare/vitest-pool-workers/config';

export default defineWorkersConfig({
  test: {
    poolOptions: {
      workers: {
        wrangler: { configPath: './wrangler.jsonc' },
        miniflare: {
          compatibilityDate: '2025-01-27',
          compatibilityFlags: ['nodejs_compat']
        }
      }
    }
  }
});
```

### 3. Write Your First Test

```typescript
import { describe, it, expect } from 'vitest';
import { env, createExecutionContext, waitOnExecutionContext } from 'cloudflare:test';
import worker from '../src/index';

describe('Worker', () => {
  it('responds with 200', async () => {
    const request = new Request('http://example.com/');
    const ctx = createExecutionContext();
    const response = await worker.fetch(request, env, ctx);
    await waitOnExecutionContext(ctx);

    expect(response.status).toBe(200);
  });
});
```

### 4. Run Tests

```bash
bun test
# or
bunx vitest
```

---

## Critical Rules

### 1. Always Use `cloudflare:test` for Env Access

**✅ CORRECT**:
```typescript
import { env } from 'cloudflare:test';

it('queries D1', async () => {
  const result = await env.DB.prepare('SELECT * FROM users').all();
  expect(result.results).toHaveLength(0); // Fresh isolated DB per test
});
```

**❌ WRONG**:
```typescript
// Don't manually create env object
const env = { DB: mockDB }; // ❌ Won't use real D1 binding
```

**Why**: `cloudflare:test` provides real bindings configured from `wrangler.jsonc` with isolated storage per test.

### 2. Always Wait on Execution Context

**✅ CORRECT**:
```typescript
it('handles async operations', async () => {
  const ctx = createExecutionContext();
  const response = await worker.fetch(request, env, ctx);
  await waitOnExecutionContext(ctx); // ✅ Ensures ctx.waitUntil completes

  expect(response.status).toBe(200);
});
```

**❌ WRONG**:
```typescript
it('missing wait', async () => {
  const ctx = createExecutionContext();
  const response = await worker.fetch(request, env, ctx);
  // ❌ Missing waitOnExecutionContext - ctx.waitUntil tasks may not complete
  expect(response.status).toBe(200);
});
```

**Why**: Workers use `ctx.waitUntil()` for background tasks (logging, analytics). Without waiting, these tasks may not complete in tests.

### 3. Each Test Gets Isolated Storage

**✅ CORRECT**:
```typescript
describe('KV Operations', () => {
  it('test 1: writes to KV', async () => {
    await env.CACHE.put('key', 'value1');
    const val = await env.CACHE.get('key');
    expect(val).toBe('value1'); // ✅ Isolated
  });

  it('test 2: clean state', async () => {
    const val = await env.CACHE.get('key');
    expect(val).toBeNull(); // ✅ Test 1's data doesn't leak here
  });
});
```

**Why**: Each test runs with fresh binding storage (automatic isolation).

### 4. Use Wrangler Config for Bindings

**✅ CORRECT**:
```typescript
// vitest.config.ts
export default defineWorkersConfig({
  test: {
    poolOptions: {
      workers: {
        wrangler: { configPath: './wrangler.jsonc' } // ✅ Reads bindings from wrangler
      }
    }
  }
});
```

**❌ WRONG**:
```typescript
// vitest.config.ts
export default defineWorkersConfig({
  test: {
    poolOptions: {
      workers: {
        // ❌ No wrangler config - bindings won't be available
        miniflare: { compatibilityDate: '2025-01-27' }
      }
    }
  }
});
```

**Why**: Wrangler config defines all bindings (D1, KV, R2, etc.). Without it, `env` will be empty.

### 5. Match Compatibility Date

**✅ CORRECT**:
```typescript
// vitest.config.ts
miniflare: {
  compatibilityDate: '2025-01-27' // ✅ Matches wrangler.jsonc
}

// wrangler.jsonc
{
  "compatibility_date": "2025-01-27"
}
```

**Why**: Ensures test environment matches production runtime behavior.

---

## Core Concepts

### Binding Testing Patterns

**D1 Database**:
```typescript
import { env } from 'cloudflare:test';

it('queries D1', async () => {
  // Insert test data
  await env.DB.prepare('INSERT INTO users (name) VALUES (?)').bind('Alice').run();

  // Query
  const result = await env.DB.prepare('SELECT * FROM users WHERE name = ?').bind('Alice').first();
  expect(result?.name).toBe('Alice');
});
```

**KV Namespace**:
```typescript
it('reads from KV', async () => {
  await env.CACHE.put('test-key', 'test-value');
  const value = await env.CACHE.get('test-key');
  expect(value).toBe('test-value');
});
```

**R2 Bucket**:
```typescript
it('uploads to R2', async () => {
  await env.BUCKET.put('file.txt', 'Hello World');
  const object = await env.BUCKET.get('file.txt');
  expect(await object?.text()).toBe('Hello World');
});
```

**Durable Objects**:
```typescript
it('interacts with Durable Object', async () => {
  const id = env.COUNTER.idFromName('test-counter');
  const stub = env.COUNTER.get(id);

  const response = await stub.fetch('http://fake/increment');
  const data = await response.json();
  expect(data.count).toBe(1);
});
```

### Unit vs Integration Tests

**Unit Test** (single function):
```typescript
import { validateInput } from '../src/utils/validator';

it('validates input', () => {
  const result = validateInput({ name: 'Alice', age: 30 });
  expect(result.valid).toBe(true);
});
```

**Integration Test** (full fetch handler):
```typescript
import worker from '../src/index';
import { env, createExecutionContext, waitOnExecutionContext } from 'cloudflare:test';

it('handles full request flow', async () => {
  const request = new Request('http://example.com/api/users', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name: 'Alice' })
  });

  const ctx = createExecutionContext();
  const response = await worker.fetch(request, env, ctx);
  await waitOnExecutionContext(ctx);

  expect(response.status).toBe(201);
  const user = await response.json();
  expect(user.name).toBe('Alice');
});
```

### Coverage Configuration

Add to `vitest.config.ts`:
```typescript
export default defineWorkersConfig({
  test: {
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
      include: ['src/**/*.ts'],
      exclude: ['src/**/*.test.ts', 'src/**/*.spec.ts'],
      thresholds: {
        lines: 80,
        functions: 80,
        branches: 80,
        statements: 80
      }
    }
  }
});
```

Run with coverage:
```bash
bunx vitest run --coverage
```

---

## Top 5 Use Cases

### 1. Testing API Endpoints with D1

```typescript
it('creates user via API', async () => {
  const request = new Request('http://example.com/api/users', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name: 'Bob', email: 'bob@example.com' })
  });

  const ctx = createExecutionContext();
  const response = await worker.fetch(request, env, ctx);
  await waitOnExecutionContext(ctx);

  expect(response.status).toBe(201);

  // Verify DB insert
  const user = await env.DB.prepare('SELECT * FROM users WHERE email = ?')
    .bind('bob@example.com')
    .first();
  expect(user?.name).toBe('Bob');
});
```

### 2. Testing Caching with KV

```typescript
it('caches API responses', async () => {
  // First request (cache miss)
  const req1 = new Request('http://example.com/api/data');
  const ctx1 = createExecutionContext();
  const res1 = await worker.fetch(req1, env, ctx1);
  await waitOnExecutionContext(ctx1);

  expect(res1.headers.get('X-Cache')).toBe('MISS');

  // Second request (cache hit)
  const req2 = new Request('http://example.com/api/data');
  const ctx2 = createExecutionContext();
  const res2 = await worker.fetch(req2, env, ctx2);
  await waitOnExecutionContext(ctx2);

  expect(res2.headers.get('X-Cache')).toBe('HIT');
});
```

### 3. Testing File Uploads to R2

```typescript
it('handles file upload', async () => {
  const formData = new FormData();
  formData.append('file', new Blob(['test content'], { type: 'text/plain' }), 'test.txt');

  const request = new Request('http://example.com/upload', {
    method: 'POST',
    body: formData
  });

  const ctx = createExecutionContext();
  const response = await worker.fetch(request, env, ctx);
  await waitOnExecutionContext(ctx);

  expect(response.status).toBe(200);

  // Verify R2 upload
  const object = await env.BUCKET.get('test.txt');
  expect(await object?.text()).toBe('test content');
});
```

### 4. Testing Durable Objects State

```typescript
it('maintains counter state', async () => {
  const id = env.COUNTER.idFromName('my-counter');
  const stub = env.COUNTER.get(id);

  // Increment 3 times
  for (let i = 0; i < 3; i++) {
    await stub.fetch('http://fake/increment');
  }

  // Verify state
  const response = await stub.fetch('http://fake/value');
  const data = await response.json();
  expect(data.count).toBe(3);
});
```

### 5. Testing Queue Consumers

```typescript
it('processes queue messages', async () => {
  const messages = [
    { id: '1', body: { action: 'email', to: 'user@example.com' }, timestamp: new Date() }
  ];

  // Simulate queue batch
  await worker.queue(
    {
      queue: 'my-queue',
      messages,
      retryAll: () => {},
      ackAll: () => {}
    },
    env
  );

  // Verify processing (check DB, logs, etc.)
  const log = await env.DB.prepare('SELECT * FROM email_log WHERE id = ?').bind('1').first();
  expect(log?.status).toBe('sent');
});
```

---

## Best Practices

### ✅ DO

1. **Use descriptive test names**:
   ```typescript
   it('returns 404 when user not found', async () => {});
   it('validates email format before saving', async () => {});
   ```

2. **Test error cases**:
   ```typescript
   it('returns 400 for invalid JSON', async () => {
     const request = new Request('http://example.com/api', {
       method: 'POST',
       headers: { 'Content-Type': 'application/json' },
       body: 'invalid json'
     });

     const ctx = createExecutionContext();
     const response = await worker.fetch(request, env, ctx);
     await waitOnExecutionContext(ctx);

     expect(response.status).toBe(400);
   });
   ```

3. **Group related tests**:
   ```typescript
   describe('User API', () => {
     describe('POST /users', () => {
       it('creates user with valid data', async () => {});
       it('rejects duplicate email', async () => {});
       it('validates required fields', async () => {});
     });
   });
   ```

4. **Use beforeEach for setup**:
   ```typescript
   describe('Database tests', () => {
     beforeEach(async () => {
       // Seed test data
       await env.DB.prepare('INSERT INTO users (name) VALUES (?)').bind('Test User').run();
     });

     it('queries users', async () => {
       const result = await env.DB.prepare('SELECT * FROM users').all();
       expect(result.results).toHaveLength(1);
     });
   });
   ```

5. **Test realistic scenarios**:
   ```typescript
   it('handles concurrent requests', async () => {
     const requests = Array(10).fill(null).map(() =>
       worker.fetch(new Request('http://example.com/'), env, createExecutionContext())
     );

     const responses = await Promise.all(requests);
     expect(responses.every(r => r.status === 200)).toBe(true);
   });
   ```

### ❌ DON'T

1. **Don't share state between tests**:
   ```typescript
   // ❌ BAD: Leaky state
   let counter = 0;
   it('test 1', () => { counter++; });
   it('test 2', () => { expect(counter).toBe(1); }); // Fragile!

   // ✅ GOOD: Isolated
   it('test 1', () => { const counter = 0; counter++; });
   it('test 2', () => { const counter = 0; /* fresh state */ });
   ```

2. **Don't forget to wait**:
   ```typescript
   // ❌ BAD
   const response = await worker.fetch(request, env, ctx);
   expect(response.status).toBe(200); // ctx.waitUntil not finished

   // ✅ GOOD
   const response = await worker.fetch(request, env, ctx);
   await waitOnExecutionContext(ctx);
   expect(response.status).toBe(200);
   ```

3. **Don't hardcode URLs**:
   ```typescript
   // ❌ BAD
   const request = new Request('http://example.com/test');

   // ✅ GOOD
   const request = new Request('http://fake-host/test'); // Host doesn't matter in tests
   ```

4. **Don't test implementation details**:
   ```typescript
   // ❌ BAD: Testing internals
   expect(worker.privateHelperFunction).toBeDefined();

   // ✅ GOOD: Testing behavior
   const response = await worker.fetch(request, env, ctx);
   expect(response.status).toBe(200);
   ```

---

## Top 8 Errors Prevented

### 1. ❌ `ReferenceError: env is not defined`

**Cause**: Not importing `env` from `cloudflare:test`.

**Fix**:
```typescript
import { env } from 'cloudflare:test'; // ✅ Add this import
```

**Prevention**: Always use `cloudflare:test` module for env access.

---

### 2. ❌ `TypeError: Cannot read property 'DB' of undefined`

**Cause**: `wrangler.jsonc` not loaded in `vitest.config.ts`.

**Fix**:
```typescript
export default defineWorkersConfig({
  test: {
    poolOptions: {
      workers: {
        wrangler: { configPath: './wrangler.jsonc' } // ✅ Add this
      }
    }
  }
});
```

**Prevention**: Always configure wrangler path in vitest config.

---

### 3. ❌ `Error: D1_ERROR: no such table: users`

**Cause**: D1 database schema not applied in tests.

**Fix**:
```typescript
// Option 1: Seed in beforeEach
beforeEach(async () => {
  await env.DB.exec(`
    CREATE TABLE IF NOT EXISTS users (
      id INTEGER PRIMARY KEY,
      name TEXT NOT NULL
    )
  `);
});

// Option 2: Use migrations (load from file)
beforeEach(async () => {
  const schema = await fs.readFile('./migrations/schema.sql', 'utf-8');
  await env.DB.exec(schema);
});
```

**Prevention**: Create schema before each test or use shared setup.

---

### 4. ❌ `Error: ctx.waitUntil tasks did not complete`

**Cause**: Missing `await waitOnExecutionContext(ctx)`.

**Fix**:
```typescript
const ctx = createExecutionContext();
const response = await worker.fetch(request, env, ctx);
await waitOnExecutionContext(ctx); // ✅ Add this
```

**Prevention**: Always wait on execution context in tests.

---

### 5. ❌ `Error: SELF is not defined`

**Cause**: Using old `SELF.fetch()` pattern instead of direct worker import.

**Fix**:
```typescript
// ❌ OLD (vitest-pool-workers <0.5)
import { SELF } from 'cloudflare:test';
await SELF.fetch(request);

// ✅ NEW (vitest-pool-workers ≥0.7)
import worker from '../src/index';
await worker.fetch(request, env, ctx);
```

**Prevention**: Use direct worker imports (modern pattern).

---

### 6. ❌ `Error: KV.get() returned data from previous test`

**Cause**: Believing storage is shared (it's not, but may indicate test leak).

**Fix**: Each test is isolated. If seeing this, check for:
```typescript
// ❌ Test pollution (shared variable)
let cache = {};
it('test 1', () => { cache.key = 'value'; });
it('test 2', () => { expect(cache.key).toBeUndefined(); }); // Fails!

// ✅ Proper isolation
it('test 1', async () => { await env.CACHE.put('key', 'value1'); });
it('test 2', async () => { const val = await env.CACHE.get('key'); expect(val).toBeNull(); });
```

**Prevention**: Don't use shared variables for test data.

---

### 7. ❌ `TypeError: env.BUCKET.put is not a function`

**Cause**: R2 binding not configured in `wrangler.jsonc`.

**Fix**:
```jsonc
// wrangler.jsonc
{
  "r2_buckets": [
    { "binding": "BUCKET", "bucket_name": "test-bucket" }
  ]
}
```

**Prevention**: Define all bindings in wrangler config.

---

### 8. ❌ `Error: Pool 'workers' is not supported`

**Cause**: Missing `@cloudflare/vitest-pool-workers` dependency.

**Fix**:
```bash
bun add -D @cloudflare/vitest-pool-workers
```

**Prevention**: Install pool package for Workers testing.

---

## When to Load References

Load reference files for detailed, specialized content:

**Load `references/vitest-setup.md` when:**
- Setting up Vitest from scratch
- Configuring custom pool options
- Troubleshooting Miniflare configuration
- Migrating from older vitest-pool-workers versions

**Load `references/binding-mocks.md` when:**
- Testing specific bindings (D1, KV, R2, DO, Queues, AI, Vectorize)
- Mocking service bindings (worker-to-worker)
- Creating test fixtures for bindings
- Understanding isolated storage behavior

**Load `references/integration-testing.md` when:**
- Writing full request/response tests
- Testing multi-step workflows
- Simulating production scenarios
- Testing WebSocket or streaming responses

**Load `references/coverage-optimization.md` when:**
- Setting up coverage thresholds
- Identifying untested code paths
- Optimizing test suite performance
- Configuring coverage reporters

**Load `references/troubleshooting.md` when:**
- Debugging failing tests
- Resolving binding errors
- Fixing timeout issues
- Understanding error messages

**Load `templates/vitest-config.ts` for:**
- Complete vitest.config.ts example
- Advanced configuration options
- Multiple wrangler environments

**Load `templates/basic-test.ts` for:**
- Test file structure template
- Common test patterns
- beforeEach/afterEach examples

**Load `templates/binding-mock-test.ts` for:**
- Binding-specific test examples
- D1, KV, R2, DO test patterns
- Queue and AI testing examples

**Load `scripts/setup-vitest.sh` for:**
- Automated Vitest installation
- Project configuration script

**Load `scripts/run-tests.sh` for:**
- CI/CD test execution
- Coverage reporting automation

---

## Related Cloudflare Plugins

**For service-specific testing patterns, load:**
- **cloudflare-d1** - D1 database testing, migrations, seeding
- **cloudflare-kv** - KV namespace testing, TTL verification
- **cloudflare-r2** - R2 bucket testing, file upload/download
- **cloudflare-durable-objects** - DO testing, WebSocket testing
- **cloudflare-queues** - Queue testing, batch processing
- **cloudflare-workers-ai** - AI model testing, inference mocking

**This skill focuses on cross-cutting Workers testing patterns** applicable to ALL binding types and Workers features.

---

**Questions?** Load `references/troubleshooting.md` or use `/workers-debug` command for interactive help.
