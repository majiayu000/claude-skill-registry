---
name: api-database-knex
description: SQL query builder for PostgreSQL, MySQL, SQLite, and MSSQL -- fluent queries, schema builder, migrations, seeds, transactions, raw queries
---

# Knex.js Patterns

> **Quick Guide:** Use Knex.js (v3.x) as a SQL query builder for PostgreSQL, MySQL, SQLite, and MSSQL. Initialize the knex instance **once** per application (it creates a connection pool internally via tarn.js). Set pool `min: 0` so idle connections are released. Always use **parameterized bindings** (`?` for values, `??` for identifiers) in `knex.raw()` -- never interpolate user input. Wrap multi-table writes in `knex.transaction()` and always return or await the promise (otherwise the transaction hangs). Use `.returning()` on PostgreSQL/MSSQL for inserted/updated rows -- it is a no-op on MySQL/SQLite. Call `knex.destroy()` on graceful shutdown to drain the pool.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST initialize the knex instance ONCE per application and reuse it -- creating multiple instances leaks connection pools)**

**(You MUST use parameterized bindings (`?` for values, `??` for identifiers) in ALL `knex.raw()` calls -- string interpolation causes SQL injection)**

**(You MUST return or await the promise inside `knex.transaction()` handlers -- failing to do so causes the transaction connection to hang indefinitely)**

**(You MUST call `knex.destroy()` on graceful shutdown -- orphaned pools prevent the Node.js process from exiting)**

</critical_requirements>

---

## Examples

- [Core Patterns](examples/core.md) -- Initialization, query builder, insert/update/delete, raw queries, TypeScript integration
- [Schema & Migrations](examples/schema-migrations.md) -- Schema builder, createTable, alterTable, migrations, seeds
- [Transactions & Advanced](examples/transactions-advanced.md) -- Transactions, batch insert, subqueries, connection pooling, multi-tenancy

**Additional resources:**

- [reference.md](reference.md) -- Query method cheat sheet, column types, pool options, anti-patterns, production checklist

---

**Auto-detection:** Knex, knex, knexfile, knex.raw, knex.schema, knex.transaction, knex.migrate, knex.seed, batchInsert, query builder, schema builder, SQL query builder, knex.fn.now, knex.ref, knex.destroy, pg, mysql2, sqlite3, better-sqlite3

**When to use:**

- Building SQL queries programmatically with a fluent API
- Database schema creation and modification (createTable, alterTable)
- Running and managing database migrations (up/down)
- Seeding development/test databases
- Wrapping multi-step database operations in transactions
- Writing raw SQL with safe parameter binding
- Batch inserting large datasets with chunking

**Key patterns covered:**

- Knex initialization with connection pool configuration
- Fluent query builder (select, where, join, orderBy, groupBy, having)
- Insert, update, delete with `.returning()` for PostgreSQL/MSSQL
- Schema builder (createTable, alterTable, column types, indexes, foreign keys)
- Migrations (knex migrate:make, up/down, transaction control)
- Seeds (knex seed:make, seed:run)
- Transactions with async/await and isolation levels
- Raw queries with `?` value bindings and `??` identifier bindings
- Subqueries as callbacks or builder instances
- Batch insert with `batchInsert()` and chunking
- TypeScript table type augmentation
- Connection pool tuning (min, max, acquireTimeout, lifetime)

**When NOT to use:**

- You need a full ORM with model relationships, lifecycle hooks, and identity maps -- use your ORM solution instead
- You need database-specific features Knex doesn't abstract (e.g., PostgreSQL LISTEN/NOTIFY, MySQL fulltext indexes) -- use `knex.raw()` for those
- Your project already uses a different query layer or ORM and doesn't need a second one

---

<philosophy>

## Philosophy

Knex is a **SQL query builder**, not an ORM. The core principle: **you write SQL, Knex just makes it safer and more portable.**

**Core principles:**

1. **One instance, one pool** -- Initialize knex once. The instance manages a connection pool (tarn.js). Never create multiple knex instances pointing at the same database.
2. **Parameterize everything** -- Use `?` bindings for values and `??` for identifiers. Never interpolate strings into queries.
3. **Migrations are the source of truth** -- Schema changes happen through migrations, not ad-hoc `knex.schema` calls in application code.
4. **Transactions for consistency** -- Any operation touching multiple tables or needing atomicity must be wrapped in `knex.transaction()`.
5. **Knex is dialect-aware, not dialect-hiding** -- Knex normalizes common SQL, but database-specific features (e.g., `.returning()` on PostgreSQL, `ON DUPLICATE KEY` on MySQL) must be handled per-dialect.

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Knex Initialization

Initialize once per application. The knex instance manages a connection pool internally. See [examples/core.md](examples/core.md) for full examples.

```typescript
// Good Example -- Proper initialization with pool tuning
import knex from "knex";

const POOL_MIN = 0;
const POOL_MAX = 10;
const ACQUIRE_TIMEOUT_MS = 30_000;

function createDatabase() {
  const connectionString = process.env.DATABASE_URL;
  if (!connectionString) {
    throw new Error("DATABASE_URL environment variable is required");
  }

  return knex({
    client: "pg",
    connection: connectionString,
    pool: { min: POOL_MIN, max: POOL_MAX },
    acquireConnectionTimeout: ACQUIRE_TIMEOUT_MS,
  });
}

export { createDatabase };
```

**Why good:** Single instance, environment variable for connection string, pool min: 0 releases idle connections, named constants

```typescript
// Bad Example -- Multiple instances, hardcoded config
import knex from "knex";

function getUsers() {
  const db = knex({ client: "pg", connection: "postgres://localhost/mydb" });
  return db("users").select("*");
  // Connection pool leaked -- db.destroy() never called
}
```

**Why bad:** Creates a new pool per call (leaks connections), hardcoded connection string, select("\*") fetches unnecessary columns

---

### Pattern 2: Query Builder Basics

Fluent API for building SELECT queries. See [examples/core.md](examples/core.md) for joins, groupBy, having.

```typescript
// Good Example -- Typed query with explicit columns
const ACTIVE_STATUS = "active";
const PAGE_SIZE = 25;

const users = await db<User>("users")
  .select("id", "name", "email")
  .where("status", ACTIVE_STATUS)
  .orderBy("created_at", "desc")
  .limit(PAGE_SIZE);
```

**Why good:** Explicit column selection, typed result, named constants for status and page size

```typescript
// Bad Example -- select(*) with string interpolation
const users = await db("users").select("*").whereRaw(`status = '${status}'`); // SQL INJECTION
```

**Why bad:** `select("*")` fetches unnecessary data, string interpolation in whereRaw creates SQL injection vulnerability

---

### Pattern 3: Insert / Update / Delete with Returning

`.returning()` works on PostgreSQL, MSSQL, CockroachDB, and SQLite 3.35+. MySQL ignores it silently. See [examples/core.md](examples/core.md).

```typescript
// Good Example -- Insert with returning (PostgreSQL)
const [inserted] = await db("users")
  .insert({ name: "Alice", email: "alice@example.com" })
  .returning(["id", "created_at"]);

// Good Example -- Update with returning
const [updated] = await db("users")
  .where("id", userId)
  .update({ name: newName, updated_at: db.fn.now() })
  .returning(["id", "name", "updated_at"]);
```

**Why good:** `.returning()` avoids a separate SELECT, `db.fn.now()` uses database-native timestamp

```typescript
// Bad Example -- Forgetting returning() on PostgreSQL
await db("users").insert({ name: "Alice" });
// Returns [0] on PostgreSQL -- the row count, not the inserted data
// Developer expects the inserted row but gets a useless number
```

**Why bad:** Without `.returning()`, PostgreSQL insert returns row count (not data), forcing an extra SELECT query

---

### Pattern 4: Raw Queries with Safe Bindings

Use `?` for value bindings and `??` for identifier bindings. See [examples/core.md](examples/core.md).

```typescript
// Good Example -- Parameterized raw query
const MIN_ORDER_COUNT = 5;

const results = await db.raw(
  `SELECT ??, COUNT(*) as order_count
   FROM ??
   WHERE ?? > ?
   GROUP BY ??
   HAVING COUNT(*) >= ?`,
  [
    "users.id",
    "orders",
    "orders.created_at",
    cutoffDate,
    "users.id",
    MIN_ORDER_COUNT,
  ],
);
```

**Why good:** `??` for identifiers, `?` for values, all user input parameterized

```typescript
// Bad Example -- String concatenation in raw query
const results = await db.raw(`SELECT * FROM users WHERE name = '${name}'`);
// SQL INJECTION: name = "'; DROP TABLE users; --"
```

**Why bad:** String interpolation allows SQL injection, attacker can execute arbitrary SQL

---

### Pattern 5: Transactions

Wrap multi-step operations in transactions. Return or await the promise -- otherwise the connection hangs. See [examples/transactions-advanced.md](examples/transactions-advanced.md).

```typescript
// Good Example -- Async/await transaction
const result = await db.transaction(async (trx) => {
  const [order] = await trx("orders")
    .insert({ user_id: userId, total: amount })
    .returning("id");

  await trx("order_items").insert(
    items.map((item) => ({ order_id: order.id, ...item })),
  );

  await trx("inventory")
    .whereIn(
      "product_id",
      items.map((i) => i.product_id),
    )
    .decrement("quantity", 1);

  return order;
});
// Transaction auto-commits on success, auto-rolls-back on thrown error
```

**Why good:** All operations atomic, auto-commit on success, auto-rollback on error, returns value from transaction

```typescript
// Bad Example -- Forgetting to return/await inside transaction
await db.transaction((trx) => {
  trx("orders").insert({ user_id: userId }); // NOT returned/awaited
  trx("items").insert({ order_id: 1 }); // NOT returned/awaited
  // Transaction handler returns undefined -- trx NEVER commits or rolls back
  // Connection hangs until acquireConnectionTimeout fires
});
```

**Why bad:** Without returning a promise, Knex cannot detect completion, transaction hangs indefinitely consuming a pool connection

---

### Pattern 6: Schema Builder

Create and modify tables. Use in migrations, not application code. See [examples/schema-migrations.md](examples/schema-migrations.md).

```typescript
// Good Example -- Migration creating a table
export async function up(knex: Knex): Promise<void> {
  await knex.schema.createTable("orders", (table) => {
    table.increments("id").primary();
    table
      .integer("user_id")
      .unsigned()
      .notNullable()
      .references("id")
      .inTable("users")
      .onDelete("CASCADE");
    table.decimal("total", 10, 2).notNullable();
    table
      .enum("status", ["pending", "paid", "shipped", "cancelled"])
      .notNullable()
      .defaultTo("pending");
    table.timestamps(true, true); // created_at, updated_at with defaults
    table.index(["user_id", "status"]);
  });
}

export async function down(knex: Knex): Promise<void> {
  await knex.schema.dropTable("orders");
}
```

**Why good:** Foreign key with cascade, composite index, enum constraint, timestamps with defaults, reversible down migration

</patterns>

---

<decision_framework>

## Decision Framework

### Knex Method Selection

```
What kind of database operation?
-- SELECT query -> db("table").select().where()
-- INSERT -> db("table").insert(data).returning()
-- UPDATE -> db("table").where().update(data).returning()
-- DELETE -> db("table").where().del()
-- Schema change -> db.schema.createTable() / .alterTable() (in migrations only)
-- Complex SQL -> db.raw("SQL", bindings)
-- Batch insert -> db.batchInsert("table", rows, chunkSize)
-- Multi-table atomic write -> db.transaction(async (trx) => { ... })
```

### When to Use Raw Queries

```
Can the query builder express this?
-- YES -> Use the query builder (portable, type-safe)
-- NO -> Does it use database-specific syntax?
    -- YES -> Use db.raw() with parameterized bindings
    -- NO -> Is it a performance-critical query needing exact SQL?
        -- YES -> Use db.raw() with parameterized bindings
        -- NO -> File an issue or use a subquery callback
```

### Transaction vs No Transaction

```
Does this operation modify multiple tables?
-- YES -> Use db.transaction()
Does this read need snapshot isolation?
-- YES -> Use db.transaction({ isolationLevel: "repeatable read" })
Is this a single INSERT/UPDATE/DELETE?
-- YES -> No transaction needed (single statement is atomic)
```

### .returning() Behavior by Database

```
Which database are you targeting?
-- PostgreSQL -> .returning() works, returns array of objects
-- MSSQL -> .returning() works, returns array of objects
-- SQLite 3.35+ -> .returning() works
-- MySQL -> .returning() is silently ignored, insert returns [insertId]
-- Oracle -> .returning() works
```

</decision_framework>

---

<red_flags>

## RED FLAGS

**High Priority Issues:**

- String interpolation in `knex.raw()` or `.whereRaw()` -- SQL injection vulnerability; always use `?` / `??` bindings
- Creating multiple knex instances pointing at the same database -- leaks connection pools, exhausts database connections
- Not returning/awaiting the promise inside `knex.transaction()` handler -- transaction connection hangs indefinitely
- Missing `knex.destroy()` on shutdown -- orphaned pool prevents process exit, connections leak
- Running `knex.schema` calls in application code instead of migrations -- schema state becomes unpredictable across environments

**Medium Priority Issues:**

- Using `select("*")` in production queries -- fetches unnecessary data, increases memory usage, breaks when columns are added
- Forgetting `.returning()` on PostgreSQL inserts -- returns useless row count `[0]` instead of inserted data
- Not setting pool `min: 0` -- default `min: 2` keeps stale connections alive during low-traffic periods
- Missing `WHERE` clause on `.update()` or `.del()` -- updates/deletes ALL rows in the table
- Using `KEYS`-style patterns without pagination -- `db("table").select()` with no limit loads entire table into memory

**Common Mistakes:**

- Expecting `.returning()` to work on MySQL -- it is silently ignored; use `insertId` from the result instead
- Using `.timeout()` on the query without `{ cancel: true }` -- times out the Node.js side but the query keeps running on the database server
- Running migrations with `disableTransactions: true` and assuming rollback works -- without a transaction, a failed migration leaves the database in a partial state
- Assuming `knex.schema.hasTable()` and `knex.schema.createTable()` are atomic -- another process can create the table between the check and the create
- Calling `trx.commit()` or `trx.rollback()` AND returning a promise -- double-completion causes unpredictable behavior

**Gotchas & Edge Cases:**

- `knex.raw()` returns a `{ rows, fields }` object on PostgreSQL but a flat array on MySQL -- access `.rows` for PostgreSQL or destructure accordingly
- `.timestamps(true, true)` creates `created_at` and `updated_at` with `defaultTo(knex.fn.now())` -- but `updated_at` is NOT automatically updated on row changes; you must set it yourself in UPDATE queries or use a database trigger
- `.first()` returns `undefined` (not `null`) when no row matches -- check with `if (!result)` not `if (result === null)`
- `knex.batchInsert()` wraps all chunks in a single transaction by default -- if one chunk fails, all previous chunks are rolled back
- Column names in `.returning()` must match the database column names exactly (case-sensitive on PostgreSQL)
- `.whereIn("id", [])` with an empty array generates `WHERE 1 = 0` (always false) -- Knex handles it but it can be surprising in logs
- Migrations run in filename-sorted order -- ensure timestamps are consistent (don't mix manual names with generated timestamps)
- `knex.fn.now()` is evaluated by the database server, not Node.js -- useful for consistency but means you can't mock it in tests without stubbing the query

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST initialize the knex instance ONCE per application and reuse it -- creating multiple instances leaks connection pools)**

**(You MUST use parameterized bindings (`?` for values, `??` for identifiers) in ALL `knex.raw()` calls -- string interpolation causes SQL injection)**

**(You MUST return or await the promise inside `knex.transaction()` handlers -- failing to do so causes the transaction connection to hang indefinitely)**

**(You MUST call `knex.destroy()` on graceful shutdown -- orphaned pools prevent the Node.js process from exiting)**

**Failure to follow these rules will cause SQL injection vulnerabilities, connection pool exhaustion, hanging transactions, and zombie processes.**

</critical_reminders>
