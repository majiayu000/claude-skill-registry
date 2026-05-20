---
name: api-database-mysql
description: Direct MySQL database access with mysql2 driver -- connection pools, prepared statements, transactions, streaming, typed queries, error handling
---

# MySQL Patterns (mysql2)

> **Quick Guide:** Use **mysql2/promise** for all new code -- it provides async/await support over the mysql2 callback API. Always use `createPool()` (never `createConnection()` in production) with `execute()` for parameterized queries (prepared statements, LRU-cached). Type query results with `RowDataPacket` generics for SELECTs and `ResultSetHeader` for INSERT/UPDATE/DELETE. For transactions, acquire a dedicated connection with `pool.getConnection()`, wrap in try/finally to guarantee `connection.release()`. Never interpolate user input into SQL strings -- always use `?` placeholders. Handle `ER_DUP_ENTRY` and `ER_LOCK_DEADLOCK` explicitly in catch blocks.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST use `execute()` with `?` placeholders for ALL queries containing user input -- NEVER interpolate values into SQL strings with template literals or string concatenation)**

**(You MUST use `pool.getConnection()` for transactions and release the connection in a `finally` block -- pool convenience methods (`pool.execute()`) use a different connection per call and cannot maintain transaction state)**

**(You MUST always import from `mysql2/promise` for async/await code -- the base `mysql2` module returns callback-based objects that do not support `await`)**

**(You MUST handle the pool `error` event -- unhandled connection errors crash the Node.js process)**

</critical_requirements>

---

## Examples

- [Core Patterns](examples/core.md) -- Pool setup, typed queries, prepared statements, connection lifecycle
- [Transactions](examples/transactions.md) -- Manual transactions, savepoints, deadlock retry, nested operations
- [Streaming & Batch](examples/streaming.md) -- Streaming large result sets, batch inserts, multiple statements
- [Error Handling](examples/error-handling.md) -- MySQL error codes, connection errors, retry strategies, graceful degradation
- [Configuration](examples/configuration.md) -- SSL/TLS, named placeholders, pool tuning, monitoring events

**Additional resources:**

- [reference.md](reference.md) -- Type cheat sheet, pool options, error codes, production checklist

---

**Auto-detection:** MySQL, mysql2, mysql2/promise, createPool, createConnection, RowDataPacket, ResultSetHeader, execute, prepared statement, pool.getConnection, beginTransaction, commit, rollback, ER_DUP_ENTRY, ER_LOCK_DEADLOCK, connectionLimit, SHOW TABLES, mysqldump, InnoDB, MariaDB

**When to use:**

- Direct SQL queries against MySQL or MariaDB databases
- Connection pool management for server applications
- Transactions requiring atomicity across multiple queries
- Streaming large result sets without loading all rows into memory
- Typed query results with TypeScript generics
- Batch inserts or multi-statement operations

**Key patterns covered:**

- Pool creation with `mysql2/promise` and proper configuration
- Prepared statements via `execute()` with `?` placeholders
- TypeScript generics with `RowDataPacket` and `ResultSetHeader`
- Transaction lifecycle: `getConnection` -> `beginTransaction` -> `commit`/`rollback` -> `release`
- Streaming with `connection.query().stream()` on the non-promise API
- Error handling for `ER_DUP_ENTRY`, `ER_LOCK_DEADLOCK`, connection failures
- Pool events (`acquire`, `release`, `enqueue`) for monitoring
- SSL/TLS and named placeholders configuration

**When NOT to use:**

- When your project already uses an ORM or query builder for MySQL -- use that tool's skill instead
- For in-memory caching or key-value storage (use a dedicated caching solution)
- For document databases or graph queries (wrong database type)
- For one-off CLI scripts where a single connection suffices and pool overhead is unnecessary

---

<philosophy>

## Philosophy

mysql2 is a **low-level MySQL driver** -- it sends SQL to MySQL and returns typed results. It does not generate SQL, manage migrations, or handle schema changes.

**Core principles:**

1. **Pools, not connections** -- Production applications should always use `createPool()`. Pools manage connection lifecycle, handle reconnection, and prevent connection exhaustion. `createConnection()` is only appropriate for one-off scripts.
2. **Prepared statements always** -- `execute()` sends parameterized queries to MySQL's prepared statement protocol. The driver caches prepared statements in an LRU cache, so repeated queries skip the preparation step. Never use `query()` with string interpolation.
3. **Type your results** -- MySQL2's TypeScript generics (`RowDataPacket`, `ResultSetHeader`) eliminate `any` from query results. Define interfaces extending `RowDataPacket` for each table shape.
4. **Transactions need dedicated connections** -- Pool convenience methods (`pool.execute()`, `pool.query()`) may use different connections for each call. Transactions require `pool.getConnection()` to pin a single connection, with `connection.release()` in a `finally` block.
5. **Fail explicitly** -- MySQL errors carry structured `code` fields (`ER_DUP_ENTRY`, `ER_LOCK_DEADLOCK`). Check `error.code` in catch blocks rather than parsing message strings.

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Pool Setup with mysql2/promise

Create a connection pool with environment-based configuration and error handling. See [examples/core.md](examples/core.md) for the complete setup pattern.

```typescript
// Good Example - Production pool setup
import mysql from "mysql2/promise";
import type { Pool } from "mysql2/promise";

const DEFAULT_CONNECTION_LIMIT = 10;
const DEFAULT_IDLE_TIMEOUT_MS = 60_000;

function createDatabasePool(): Pool {
  const url = process.env.DATABASE_URL;
  if (!url) {
    throw new Error("DATABASE_URL environment variable is required");
  }

  return mysql.createPool({
    uri: url,
    waitForConnections: true,
    connectionLimit: DEFAULT_CONNECTION_LIMIT,
    maxIdle: DEFAULT_CONNECTION_LIMIT,
    idleTimeout: DEFAULT_IDLE_TIMEOUT_MS,
    enableKeepAlive: true,
    keepAliveInitialDelay: 0,
  });
}

export { createDatabasePool };
```

**Why good:** Environment variable validation, named constants for limits, `waitForConnections: true` queues requests instead of throwing, `enableKeepAlive` prevents stale connections

```typescript
// Bad Example - Hardcoded single connection
import mysql from "mysql2/promise";

const connection = await mysql.createConnection({
  host: "localhost",
  user: "root",
  password: "password123",
  database: "mydb",
});
// Hardcoded credentials, single connection exhausts under load, no pool
```

**Why bad:** Hardcoded credentials leak in version control, single connection cannot handle concurrent requests, no automatic reconnection

---

### Pattern 2: Typed Queries with Generics

Use `RowDataPacket` for SELECTs and `ResultSetHeader` for mutations. See [examples/core.md](examples/core.md) for all type patterns.

```typescript
// Good Example - Typed SELECT and INSERT
import type { Pool, RowDataPacket, ResultSetHeader } from "mysql2/promise";

interface UserRow extends RowDataPacket {
  id: number;
  email: string;
  name: string;
  created_at: Date;
}

async function getUserById(
  pool: Pool,
  userId: number,
): Promise<UserRow | null> {
  const [rows] = await pool.execute<UserRow[]>(
    "SELECT id, email, name, created_at FROM users WHERE id = ?",
    [userId],
  );
  return rows[0] ?? null;
}

async function createUser(
  pool: Pool,
  email: string,
  name: string,
): Promise<number> {
  const [result] = await pool.execute<ResultSetHeader>(
    "INSERT INTO users (email, name) VALUES (?, ?)",
    [email, name],
  );
  return result.insertId;
}
```

**Why good:** Interface extends `RowDataPacket` for type safety, `execute()` uses prepared statements, destructured `[rows]` skips field metadata, null check for missing rows

```typescript
// Bad Example - Untyped query with interpolation
const [rows] = await pool.query(`SELECT * FROM users WHERE id = ${userId}`);
// SQL injection vulnerability, untyped results, query() skips prepared statements
```

**Why bad:** SQL injection via string interpolation, `any`-typed results, `query()` does not use prepared statement protocol

---

### Pattern 3: Transaction with Dedicated Connection

Transactions require a single connection from the pool. See [examples/transactions.md](examples/transactions.md) for savepoints, deadlock retry, and nested operations.

```typescript
// Good Example - Transfer with transaction
async function transferFunds(
  pool: Pool,
  fromId: number,
  toId: number,
  amount: number,
): Promise<void> {
  const connection = await pool.getConnection();
  try {
    await connection.beginTransaction();

    await connection.execute(
      "UPDATE accounts SET balance = balance - ? WHERE id = ? AND balance >= ?",
      [amount, fromId, amount],
    );
    await connection.execute(
      "UPDATE accounts SET balance = balance + ? WHERE id = ?",
      [amount, toId],
    );

    await connection.commit();
  } catch (error) {
    await connection.rollback();
    throw error;
  } finally {
    connection.release();
  }
}
```

**Why good:** `getConnection()` pins one connection, `finally` guarantees release even on error, `rollback()` in catch prevents partial commits, balance check in SQL prevents overdraft

---

### Pattern 4: Streaming Large Result Sets

Use the callback-based API for streaming -- the promise API does not support `.stream()`. See [examples/streaming.md](examples/streaming.md) for backpressure handling and transform streams.

```typescript
// Good Example - Stream rows without loading all into memory
import mysql from "mysql2";

function streamUsers(
  pool: ReturnType<typeof mysql.createPool>,
): NodeJS.ReadableStream {
  return pool
    .query("SELECT * FROM users WHERE active = 1")
    .stream({ highWaterMark: 100 });
}
```

**Why good:** `highWaterMark` controls buffer size, rows are emitted one at a time via Node.js stream interface, constant memory usage regardless of result set size

**When to use:** Result sets with 10K+ rows, ETL pipelines, CSV exports, data migrations

---

### Pattern 5: Error Code Handling

MySQL errors carry structured `code` and `errno` fields. See [examples/error-handling.md](examples/error-handling.md) for retry strategies and connection error handling.

```typescript
// Good Example - Structured error handling
import type { Pool, ResultSetHeader } from "mysql2/promise";

const MYSQL_ER_DUP_ENTRY = "ER_DUP_ENTRY";

interface MysqlError extends Error {
  code: string;
  errno: number;
  sqlState: string;
  sqlMessage: string;
}

function isMysqlError(error: unknown): error is MysqlError {
  return error instanceof Error && "code" in error && "errno" in error;
}

async function createUserSafe(
  pool: Pool,
  email: string,
  name: string,
): Promise<{ insertId: number } | { duplicate: true }> {
  try {
    const [result] = await pool.execute<ResultSetHeader>(
      "INSERT INTO users (email, name) VALUES (?, ?)",
      [email, name],
    );
    return { insertId: result.insertId };
  } catch (error) {
    if (isMysqlError(error) && error.code === MYSQL_ER_DUP_ENTRY) {
      return { duplicate: true };
    }
    throw error;
  }
}
```

**Why good:** Type guard for MySQL errors, named constant for error code, returns discriminated union instead of throwing on expected errors, re-throws unexpected errors

</patterns>

---

<performance>

## Performance Optimization

### execute() vs query()

`execute()` uses MySQL's binary prepared statement protocol with an LRU cache. The first call prepares the statement; subsequent calls with the same SQL reuse the cached preparation, skipping the parse step. Use `execute()` for all parameterized queries.

`query()` sends the full SQL text each time. Use `query()` only for dynamic SQL where the statement text itself changes (e.g., dynamic column lists), or when streaming (`.stream()` is not available on the promise API's execute).

### Pool Sizing

```
connectionLimit = (number of CPU cores * 2) + number of disk spindles
```

For cloud databases, start with `connectionLimit: 10` and increase under load testing. The MySQL server's `max_connections` must accommodate all application instances' pools combined.

### enableKeepAlive

Set `enableKeepAlive: true` to prevent firewalls and load balancers from dropping idle connections. Without this, connections that idle for longer than the intermediary's timeout are silently dropped, causing `ECONNRESET` errors on the next query.

### Batch Inserts

For inserting many rows, use a single `INSERT ... VALUES (...), (...), (...)` statement instead of individual inserts -- see [examples/streaming.md](examples/streaming.md).

</performance>

---

<decision_framework>

## Decision Framework

### Pool vs Connection

```
What am I building?
-- Production server handling concurrent requests? -> createPool()
-- One-off CLI script or migration? -> createConnection() is acceptable
-- Serverless function (Lambda, Vercel)? -> createPool() with connectionLimit: 1
```

### execute() vs query()

```
Does the SQL have user-provided parameters?
-- YES -> execute() with ? placeholders (ALWAYS)
-- NO, but same SQL runs repeatedly? -> execute() (benefits from LRU cache)
-- NO, SQL text itself is dynamic? -> query() (cannot prepare dynamic SQL)
-- Need to stream results? -> query().stream() on the callback API
```

### Pool method vs getConnection()

```
Is this a single query?
-- YES -> pool.execute() or pool.query() (auto-acquires and releases)
-- NO, multiple queries needing same connection? -> pool.getConnection()
-- Transaction? -> pool.getConnection() (REQUIRED)
```

### Error Handling Strategy

```
What MySQL error did I get?
-- ER_DUP_ENTRY (1062) -> Handle as business logic (return conflict, not throw)
-- ER_LOCK_DEADLOCK (1213) -> Retry the entire transaction (MySQL rolled it back)
-- ER_LOCK_WAIT_TIMEOUT (1205) -> Retry or fail with timeout message
-- ECONNREFUSED / PROTOCOL_CONNECTION_LOST -> Connection issue, pool will reconnect
-- ER_ACCESS_DENIED_ERROR (1045) -> Configuration error, fail fast
```

</decision_framework>

---

<red_flags>

## RED FLAGS

**High Priority Issues:**

- Interpolating user input into SQL strings (`\`SELECT \* FROM users WHERE id = ${id}\``) -- SQL injection vulnerability, always use `?`placeholders with`execute()`
- Using `pool.execute()` or `pool.query()` for transactions -- each call may use a different connection, breaking transaction isolation; use `pool.getConnection()`
- Importing from `mysql2` instead of `mysql2/promise` for async/await code -- the base module returns callback-based objects, `await` will not work as expected
- Not releasing connections acquired with `pool.getConnection()` -- connection leak exhausts the pool; always release in a `finally` block

**Medium Priority Issues:**

- Using `query()` instead of `execute()` for parameterized queries -- misses prepared statement caching and binary protocol efficiency
- Missing pool `error` event handler -- unhandled connection errors crash the Node.js process
- Setting `connectionLimit` too high -- each MySQL connection uses ~10 MB of server memory; 10-20 is usually sufficient
- Not setting `enableKeepAlive: true` -- idle connections get dropped by firewalls/load balancers causing `ECONNRESET`

**Common Mistakes:**

- Expecting `pool.end()` to wait for active queries -- it immediately destroys all connections; drain queries first
- Using `rows.length` to check if an UPDATE affected rows -- use `result.affectedRows` from `ResultSetHeader` instead
- Assuming `insertId` is always the auto-increment value -- for `INSERT ... ON DUPLICATE KEY UPDATE`, `insertId` is `0` if the existing row was updated, not inserted
- Calling `connection.release()` after `connection.destroy()` -- destroy removes the connection from the pool entirely; release returns it
- Treating `null` and `undefined` as interchangeable in parameter arrays -- mysql2 converts `null` to SQL `NULL` but `undefined` causes a protocol error

**Gotchas & Edge Cases:**

- `DECIMAL` and `BIGINT` columns are returned as strings by default to avoid JavaScript floating-point precision loss -- parse explicitly if you need numbers
- `DATE` columns return JavaScript `Date` objects, but `DATETIME` precision beyond milliseconds is truncated -- MySQL supports microsecond precision, JavaScript `Date` does not
- `execute()` with named placeholders requires `namedPlaceholders: true` on the pool/connection config -- the default is unnamed `?` only
- `multipleStatements: true` is a security risk -- it enables SQL injection via `;` in user input if combined with `query()`; only enable when needed and never with user-provided SQL
- Pool `waitForConnections: false` throws immediately when all connections are in use instead of queuing -- the default `true` is almost always what you want
- `ResultSetHeader.warningStatus` indicates server warnings -- check it after DDL operations (the deprecated `OkPacket` type had a separate `warningCount` field; `ResultSetHeader` has always used `warningStatus`)

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST use `execute()` with `?` placeholders for ALL queries containing user input -- NEVER interpolate values into SQL strings with template literals or string concatenation)**

**(You MUST use `pool.getConnection()` for transactions and release the connection in a `finally` block -- pool convenience methods (`pool.execute()`) use a different connection per call and cannot maintain transaction state)**

**(You MUST always import from `mysql2/promise` for async/await code -- the base `mysql2` module returns callback-based objects that do not support `await`)**

**(You MUST handle the pool `error` event -- unhandled connection errors crash the Node.js process)**

**Failure to follow these rules will cause SQL injection vulnerabilities, transaction corruption, connection pool exhaustion, and application crashes.**

</critical_reminders>
