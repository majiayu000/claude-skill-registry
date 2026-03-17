---
name: setup-mongodb
description: Configure MongoDB connection and test infrastructure. Use when adding MongoDB support to the project. Triggers on "setup mongodb", "add mongodb", "configure database", "mongodb connection".
---

# Setup MongoDB

Configures MongoDB connection with the native driver (not Mongoose), including graceful shutdown and test infrastructure.

## Quick Reference

**Files created**:

- `src/config/mongodb.setup.ts` - Connection management
- `tests/config/mongodb.global.ts` - Test server lifecycle
- `tests/config/mongodb.setup.ts` - Test mocks and helpers

**When to use**: Before creating MongoDB repository implementations

## Prerequisites

- Project bootstrapped with base structure
- Node.js 18+ with pnpm

## Instructions

### Phase 1: Install Dependencies

#### Step 1: Install MongoDB Driver

```bash
pnpm add mongodb
```

#### Step 2: Install Test Dependencies

```bash
pnpm add -D mongodb-memory-server
```

### Phase 2: Environment Configuration

#### Step 3: Add Environment Variables

Update `src/env.ts` (add to schema and mappedEnv, using the `getEnv()` helper):

```typescript
const envSchema = z.object({
  // ... existing variables ...

  // MongoDB Configuration
  MONGODB_URI: z.string().url().optional(),
  MONGODB_DATABASE: z.string().default("my-app-db"),
});

const mappedEnv = {
  // ... existing mappings ...
  MONGODB_URI: getEnv("MONGODB_URI"),
  MONGODB_DATABASE: getEnv("MONGODB_DATABASE"),
};
```

Update `.env.example` (using the `BT_` prefix):

```bash
# MongoDB Configuration
BT_MONGODB_URI=mongodb://localhost:27017
BT_MONGODB_DATABASE=my-app-db
```

Update `.env`:

```bash
BT_MONGODB_URI=mongodb://localhost:27017
BT_MONGODB_DATABASE=my-app-db
```

### Phase 3: Connection Setup

#### Step 4: Create Connection Manager

Create `src/config/mongodb.setup.ts`:

```typescript
import { MongoClient, type Db } from "mongodb";
import { env } from "@/env";

let client: MongoClient | null = null;
let db: Db | null = null;

export async function connectToDatabase(): Promise<Db> {
  if (db) {
    return db;
  }

  const uri = env.MONGODB_URI;
  if (!uri) {
    throw new Error("MONGODB_URI environment variable is not set");
  }

  try {
    client = new MongoClient(uri);
    await client.connect();
    db = client.db(env.MONGODB_DATABASE);
    console.log(`Connected to MongoDB database: ${env.MONGODB_DATABASE}`);
    return db;
  } catch (error) {
    console.error("Failed to connect to MongoDB:", error);
    throw error;
  }
}

export async function disconnectFromDatabase(): Promise<void> {
  if (client) {
    await client.close();
    client = null;
    db = null;
    console.log("Disconnected from MongoDB");
  }
}

export async function getDatabase(): Promise<Db> {
  if (!db) {
    return connectToDatabase();
  }
  return db;
}

// Graceful shutdown handlers
process.on("SIGINT", async () => {
  await disconnectFromDatabase();
  process.exit(0);
});

process.on("SIGTERM", async () => {
  await disconnectFromDatabase();
  process.exit(0);
});
```

### Phase 4: Test Infrastructure

#### Step 5: Update Vitest Config

Update `vitest.config.ts`:

```typescript
import { defineConfig } from "vitest/config";
import path from "path";

export default defineConfig({
  test: {
    include: ["tests/**/*.test.ts"],
    globals: false,
    environment: "node",
    // MongoDB test configuration
    globalSetup: ["./tests/config/mongodb.global.ts"],
    setupFiles: ["./tests/config/mongodb.setup.ts"],
    pool: "forks", // Prevents database conflicts between tests
    coverage: {
      provider: "v8",
      reporter: ["text", "html"],
      exclude: ["node_modules/", "tests/", "dist/"],
    },
  },
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
});
```

#### Step 6: Create Global Setup

Create `tests/config/mongodb.global.ts`:

```typescript
import { MongoMemoryServer } from "mongodb-memory-server";

let mongoServer: MongoMemoryServer | null = null;

export async function setup() {
  console.log("\n🚀 Starting MongoDB Memory Server...");

  mongoServer = await MongoMemoryServer.create({
    instance: {
      dbName: "test-db",
    },
  });

  const uri = mongoServer.getUri();
  process.env.MONGODB_URI = uri;
  process.env.MONGODB_DATABASE = "test-db";

  console.log(`✅ MongoDB Memory Server started at: ${uri}`);
}

export async function teardown() {
  console.log("\n🛑 Stopping MongoDB Memory Server...");

  if (mongoServer) {
    await mongoServer.stop();
    mongoServer = null;
  }

  console.log("✅ MongoDB Memory Server stopped");
}
```

#### Step 7: Create Test Setup

Create `tests/config/mongodb.setup.ts`:

```typescript
import { vi, beforeAll, afterAll } from "vitest";
import { MongoClient, type Db } from "mongodb";

// Store test database connection
let testClient: MongoClient | null = null;
let testDb: Db | null = null;

// Mock the mongodb.setup module
vi.mock("@/config/mongodb.setup", () => ({
  getDatabase: vi.fn(async () => {
    if (!testDb) {
      const uri = process.env.MONGODB_URI;
      if (!uri) {
        throw new Error("MONGODB_URI not set by global setup");
      }
      testClient = new MongoClient(uri);
      await testClient.connect();
      testDb = testClient.db(process.env.MONGODB_DATABASE || "test-db");
    }
    return testDb;
  }),
  connectToDatabase: vi.fn(async () => {
    const { getDatabase } = await import("@/config/mongodb.setup");
    return getDatabase();
  }),
  disconnectFromDatabase: vi.fn(async () => {
    if (testClient) {
      await testClient.close();
      testClient = null;
      testDb = null;
    }
  }),
}));

// Global test helpers
declare global {
  function setupTestDatabase(): Promise<{ db: Db; client: MongoClient }>;
  function cleanupTestDatabase(client: MongoClient): Promise<void>;
}

globalThis.setupTestDatabase = async () => {
  const uri = process.env.MONGODB_URI;
  if (!uri) {
    throw new Error("MONGODB_URI not set");
  }
  const client = new MongoClient(uri);
  await client.connect();
  const db = client.db(process.env.MONGODB_DATABASE || "test-db");
  return { db, client };
};

globalThis.cleanupTestDatabase = async (client: MongoClient) => {
  if (client) {
    await client.close();
  }
};

// Cleanup after all tests
afterAll(async () => {
  if (testClient) {
    await testClient.close();
    testClient = null;
    testDb = null;
  }
});
```

### Phase 5: Server Integration (Optional)

#### Step 8: Connect on Server Start

If you want to connect to MongoDB when the server starts, update `src/server.ts`:

```typescript
import { serve } from "@hono/node-server";
import { app } from "./app";
import { env } from "./env";
import { connectToDatabase } from "./config/mongodb.setup";

const port = env.PORT;

async function startServer() {
  // Connect to MongoDB if URI is configured
  if (env.MONGODB_URI) {
    try {
      await connectToDatabase();
      console.log("MongoDB connection established");
    } catch (error) {
      console.error("Failed to connect to MongoDB:", error);
      // Decide: exit or continue with MockDB fallback
      // process.exit(1);
    }
  }

  console.log(`Server starting on port ${port}...`);

  serve({
    fetch: app.fetch,
    port,
  });

  console.log(`Server running at http://localhost:${port}`);
}

startServer();
```

### Phase 6: Verification

#### Step 9: Test MongoDB Setup

Create a simple test to verify the setup works:

Create `tests/config/mongodb.connection.test.ts`:

```typescript
import { describe, it, expect, beforeAll, afterAll } from "vitest";
import type { MongoClient, Db } from "mongodb";

describe("MongoDB Connection", () => {
  let testClient: MongoClient;
  let testDb: Db;

  beforeAll(async () => {
    const { db, client } = await setupTestDatabase();
    testDb = db;
    testClient = client;
  });

  afterAll(async () => {
    await cleanupTestDatabase(testClient);
  });

  it("connects to test database", async () => {
    expect(testDb).toBeDefined();
    expect(testDb.databaseName).toBe("test-db");
  });

  it("can perform basic operations", async () => {
    const collection = testDb.collection("test-collection");

    // Insert
    const insertResult = await collection.insertOne({ test: "data" });
    expect(insertResult.insertedId).toBeDefined();

    // Find
    const doc = await collection.findOne({ test: "data" });
    expect(doc).not.toBeNull();
    expect(doc?.test).toBe("data");

    // Cleanup
    await collection.deleteMany({});
  });
});
```

Run the test:

```bash
pnpm test -- tests/config/mongodb.connection.test.ts
```

## Connection Patterns

### Lazy Connection (Default)

Connection is established on first database access:

```typescript
// In repository
private async getCollection() {
  if (!this.collection) {
    const db = await getDatabase(); // Connects if needed
    this.collection = db.collection("entities");
  }
  return this.collection;
}
```

### Eager Connection

Connect explicitly at startup:

```typescript
// In server.ts
await connectToDatabase();
```

### Connection Pooling

The MongoDB driver handles connection pooling automatically. Default pool size is 100 connections.

To customize:

```typescript
const client = new MongoClient(uri, {
  maxPoolSize: 50,
  minPoolSize: 5,
});
```

## Files Created Summary

```
src/
└── config/
    └── mongodb.setup.ts      # Connection manager

tests/
└── config/
    ├── mongodb.global.ts     # Memory server lifecycle
    ├── mongodb.setup.ts      # Test mocks and helpers
    └── mongodb.connection.test.ts  # Verification test
```

## Troubleshooting

### "MONGODB_URI not set" Error

- Check `.env` file has the variable
- Verify `env.ts` includes the mapping
- For tests, ensure `globalSetup` runs before tests

### Memory Server Fails to Start

- Check available memory (needs ~500MB)
- Try specifying a version: `MongoMemoryServer.create({ binary: { version: '6.0.0' } })`
- On M1 Macs, ensure Rosetta is installed

### Tests Hang

- Ensure `pool: "forks"` is set in vitest.config.ts
- Check for unclosed connections in afterAll hooks
- Verify global teardown runs

## What NOT to Do

- Do NOT use Mongoose (use native driver for transparency)
- Do NOT connect in module scope (use async initialization)
- Do NOT forget graceful shutdown handlers
- Do NOT skip the `pool: "forks"` setting for tests
- Do NOT hardcode connection strings (use env variables)

## See Also

- `create-mongodb-repository` - Create MongoDB repository implementation
- `test-mongodb-repository` - Test MongoDB repository
- `add-env-variable` - Add more environment variables
