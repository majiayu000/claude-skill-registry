---
name: test-mongodb-repository
description: Write tests for MongoDB repository implementations. Use when testing MongoDB repositories, setting up MongoDB test infrastructure, or testing database operations. Triggers on "test mongodb", "mongodb tests", "test mongo repository", "mongodb test setup".
---

# Test MongoDB Repository

Write Vitest tests for MongoDB repository implementations. Requires test infrastructure setup with `mongodb-memory-server`.

## Quick Reference

**Location**: `tests/repositories/{entity-name}.mongodb.repository.test.ts`
**Run tests**: `pnpm test -- tests/repositories/{entity-name}.mongodb.repository.test.ts`

## Prerequisites

### 1. Install Dependencies

```bash
pnpm add -D mongodb-memory-server
```

### 2. Configure Vitest

Update `vitest.config.ts`:

```typescript
export default defineConfig({
  test: {
    include: ["tests/**/*.test.ts"],
    globalSetup: ["./tests/config/mongodb.global.ts"],
    setupFiles: ["./tests/config/mongodb.setup.ts"],
    pool: "forks", // Avoid database conflicts
    // ... other config
  },
});
```

### 3. Create Test Config Files

You need two configuration files. See [REFERENCE.md](REFERENCE.md) for complete files:

- `tests/config/mongodb.global.ts` - Starts/stops MongoDB Memory Server
- `tests/config/mongodb.setup.ts` - Mocks database connection, provides test helpers

## Test Structure

```typescript
import {
  describe,
  it,
  expect,
  beforeEach,
  afterEach,
  beforeAll,
  afterAll,
} from "vitest";
import { MongoDb{Entity}Repository } from "@/repositories/mongodb/{entity-name}.mongodb.repository";
import type { MongoClient, Db } from "mongodb";
import type {
  Create{Entity}Type,
  Update{Entity}Type,
  {Entity}QueryParamsType,
} from "@/schemas/{entity-name}.schema";

describe("MongoDb{Entity}Repository", () => {
  let repository: MongoDb{Entity}Repository;
  let testClient: MongoClient;
  let testDb: Db;
  const testUserId = "test-user-123";

  beforeAll(async () => {
    // Global helper from mongodb.setup.ts
    const { db, client } = await setupTestDatabase();
    testDb = db;
    testClient = client;
  });

  afterAll(async () => {
    await cleanupTestDatabase(testClient);
  });

  beforeEach(async () => {
    repository = new MongoDb{Entity}Repository();
    await repository.clear();
  });

  afterEach(async () => {
    await repository.clear();
  });

  // Test cases...
});
```

## Test Cases

### CRUD Operations

Same patterns as MockDB tests. See `test-mockdb-repository` skill for:

- create
- findById
- findAll (with filtering, pagination, sorting)
- update
- remove

### MongoDB-Specific: Data Validation

```typescript
describe("data validation", () => {
  it("validates data using Zod schema when mapping from document", async () => {
    const data: Create{Entity}Type = { content: "Valid content" };
    const result = await repository.create(data, testUserId);

    // Zod validation ensures proper types
    expect(result.id).toBeTruthy();
    expect(result.createdAt).toBeInstanceOf(Date);
    expect(result.updatedAt).toBeInstanceOf(Date);
  });
});
```

### MongoDB-Specific: Database Indexes

```typescript
describe("database indexes", () => {
  it("creates proper indexes for performance", async () => {
    // Create entity to trigger collection initialization
    await repository.create({ content: "Test" }, testUserId);
    const stats = await repository.getStats();

    expect(stats.indexes).toContain("_id_");
    expect(stats.indexes).toContain("{entities}_createdBy");
    expect(stats.indexes).toContain("{entities}_createdAt_desc");
    expect(stats.indexes).toContain("{entities}_{field}_text");
  });
});
```

### MongoDB-Specific: Helper Methods

```typescript
describe("helper methods", () => {
  beforeEach(async () => {
    await repository.create({ content: "Test 1" }, testUserId);
    await repository.create({ content: "Test 2" }, testUserId);
  });

  it("clears all entities", async () => {
    await repository.clear();
    const result = await repository.findAll({});
    expect(result.data).toHaveLength(0);
  });

  it("returns collection stats", async () => {
    const stats = await repository.getStats();
    expect(stats.count).toBe(2);
    expect(stats.indexes).toEqual(expect.any(Array));
  });
});
```

## What to Test

| Category       | Test Cases                                                 |
| -------------- | ---------------------------------------------------------- |
| **CRUD**       | Same as MockDB (create, findById, findAll, update, remove) |
| **Validation** | Zod schema validation when reading from DB                 |
| **Indexes**    | Proper indexes created for performance                     |
| **Helpers**    | clear() and getStats() work correctly                      |
| **ObjectId**   | Invalid IDs return null (not throw)                        |

## Test Infrastructure Explained

### vitest.config.ts

| Setting         | Purpose                                                      |
| --------------- | ------------------------------------------------------------ |
| `globalSetup`   | Runs once before all tests - starts MongoDB Memory Server    |
| `setupFiles`    | Runs before each test file - sets up mocks and helpers       |
| `pool: "forks"` | Runs tests in separate processes to avoid database conflicts |

### mongodb.global.ts

- Starts `mongodb-memory-server` once for entire test run
- Stores URI and database name in `process.env`
- Tears down when all tests complete

### mongodb.setup.ts

- Mocks `@/config/mongodb.setup` module
- Provides global `setupTestDatabase()` and `cleanupTestDatabase()` helpers
- Redirects repository database calls to the in-memory server

## Complete Example

See [REFERENCE.md](REFERENCE.md) for:

- Complete MongoDB repository test file
- `vitest.config.ts` configuration
- `tests/config/mongodb.global.ts`
- `tests/config/mongodb.setup.ts`

## What NOT to Do

- Do NOT forget to set up the test infrastructure files
- Do NOT run MongoDB tests in parallel (use `pool: "forks"`)
- Do NOT forget `beforeAll`/`afterAll` for database setup/teardown
- Do NOT forget to call `repository.clear()` in `beforeEach`/`afterEach`
- Do NOT skip index tests - they verify performance optimization
