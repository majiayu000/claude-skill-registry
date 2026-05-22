---
name: api-database-postgresql
description: Direct PostgreSQL access with node-postgres (pg) -- connection pools, parameterized queries, transactions, streaming, LISTEN/NOTIFY, error handling
---

# PostgreSQL Patterns (node-postgres)

> **Quick Guide:** Use the `pg` package (v8.x) for direct PostgreSQL access. **Always use `Pool`** -- never create individual `Client` instances in application code. Use **parameterized queries** (`$1`, `$2`) for ALL user input -- never interpolate strings into SQL. For transactions, check out a dedicated client with `pool.connect()` and use `BEGIN`/`COMMIT`/`ROLLBACK` in a `try`/`catch`/`finally` that always calls `client.release()`. Handle the pool `error` event to prevent process crashes from idle client errors. Use `pg-query-stream` for large result sets to avoid loading everything into memory.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST use parameterized queries (`$1`, `$2`, ...) for ALL values -- NEVER concatenate or interpolate user input into SQL strings)**

**(You MUST use `Pool` for all database access -- NEVER create standalone `Client` instances in application code)**

**(You MUST release clients back to the pool in a `finally` block after `pool.connect()` -- leaked clients exhaust the pool and hang the application)**

**(You MUST handle the `error` event on Pool instances -- unhandled idle client errors crash the Node.js process)**

</critical_requirements>

---

## Examples

- [Core Patterns](examples/core.md) -- Pool setup, parameterized queries, type-safe results, error handling
- [Transactions](examples/transactions.md) -- BEGIN/COMMIT/ROLLBACK, savepoints, retry logic, advisory locks
- [Streaming](examples/streaming.md) -- Cursors, pg-query-stream, LISTEN/NOTIFY for real-time
- [Advanced](examples/advanced.md) -- SSL/TLS, prepared statements, migrations, testing patterns

**Additional resources:**

- [reference.md](reference.md) -- Pool options, error codes, QueryResult properties, production checklist

---

**Auto-detection:** PostgreSQL, pg, node-postgres, Pool, Client, pool.query, pool.connect, client.query, $1, parameterized query, BEGIN, COMMIT, ROLLBACK, LISTEN, NOTIFY, pg_notify, pg-query-stream, pg-cursor, Cursor, QueryResult, QueryResultRow, connectionString, PGHOST, PGDATABASE, unique_violation, 23505, deadlock, 40P01, advisory lock

**When to use:**

- Direct SQL queries against PostgreSQL (not behind an ORM)
- Connection pool management for Node.js/PostgreSQL applications
- Transactions spanning multiple queries that must be atomic
- Streaming large result sets without loading everything into memory
- Real-time change notifications via LISTEN/NOTIFY
- Integration testing with transaction rollback isolation

**Key patterns covered:**

- Pool configuration and lifecycle (creation, error handling, graceful shutdown)
- Parameterized queries with `$1`-style placeholders (SQL injection prevention)
- Type-safe query results using TypeScript generics
- Transaction management with dedicated clients
- Streaming with pg-cursor and pg-query-stream
- LISTEN/NOTIFY for real-time PostgreSQL event handling
- PostgreSQL error code handling (constraint violations, deadlocks, serialization failures)
- SSL/TLS connection configuration
- Testing with transaction rollback isolation

**When NOT to use:**

- You need an ORM or query builder -- use your ORM/query builder skill instead
- You need in-memory caching -- use a caching solution
- You need document storage without relational constraints -- use a document database
- Simple key-value lookups at sub-millisecond latency -- use an in-memory data store

---

<philosophy>

## Philosophy

`pg` (node-postgres) is a **low-level PostgreSQL client** that gives you full control over SQL, connections, and transactions. The core principle: **write SQL directly, let PostgreSQL do the heavy lifting.**

**Core principles:**

1. **Pool, never Client** -- Application code should always use `Pool`. The pool manages connections, handles reconnection, and prevents connection exhaustion. Use `pool.query()` for single queries, `pool.connect()` when you need a dedicated client (transactions).
2. **Parameterized everything** -- Never build SQL by string concatenation. Use `$1`, `$2` placeholders. This prevents SQL injection AND enables PostgreSQL query plan caching.
3. **Release in finally** -- Any client obtained via `pool.connect()` must be released in a `finally` block. A leaked client sits checked out forever, and once `max` clients leak, the pool deadlocks.
4. **Fail loudly** -- Handle the pool's `error` event. Handle query errors with specific PostgreSQL error codes. Never swallow errors silently.
5. **Stream large results** -- Don't `SELECT *` a million rows into memory. Use `pg-cursor` or `pg-query-stream` for large result sets.

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Pool Setup

Create a single pool per database at application startup. See [examples/core.md](examples/core.md) for full configuration examples.

```typescript
// ✅ Good Example - Pool with error handling
import pg from "pg";

const POOL_MAX_CLIENTS = 20;
const IDLE_TIMEOUT_MS = 30_000;
const CONNECTION_TIMEOUT_MS = 5_000;

function createPool(): pg.Pool {
  const pool = new pg.Pool({
    connectionString: process.env.DATABASE_URL,
    max: POOL_MAX_CLIENTS,
    idleTimeoutMillis: IDLE_TIMEOUT_MS,
    connectionTimeoutMillis: CONNECTION_TIMEOUT_MS,
  });

  pool.on("error", (err) => {
    console.error("Unexpected idle client error:", err.message);
  });

  return pool;
}

export { createPool };
```

**Why good:** Named constants for pool config, environment variable for connection string, error handler prevents process crash from idle client errors

```typescript
// ❌ Bad Example - No pool, standalone client
import pg from "pg";

const client = new pg.Client("postgres://localhost/mydb");
await client.connect();
// One connection for entire app -- no pooling, no reconnection,
// no concurrency. If client disconnects, app crashes.
```

**Why bad:** Standalone Client has no connection pooling, no automatic reconnection, no concurrency -- every query blocks on a single connection

---

### Pattern 2: Parameterized Queries

Always use `$1`-style placeholders. See [examples/core.md](examples/core.md) for typed query helpers.

```typescript
// ✅ Good Example - Parameterized query with typed result
interface UserRow {
  id: number;
  name: string;
  email: string;
}

const result = await pool.query<UserRow>(
  "SELECT id, name, email FROM users WHERE id = $1",
  [userId],
);

const user = result.rows[0]; // UserRow | undefined
```

**Why good:** `$1` placeholder prevents SQL injection, generic `<UserRow>` types the `rows` array, result is properly typed

```typescript
// ❌ Bad Example - String interpolation (SQL INJECTION!)
const result = await pool.query(
  `SELECT * FROM users WHERE name = '${userName}'`,
);
// userName = "'; DROP TABLE users; --" -> catastrophic
```

**Why bad:** String interpolation allows SQL injection, no type safety on result rows, `SELECT *` returns untyped columns

---

### Pattern 3: Transactions

Use `pool.connect()` to get a dedicated client for the transaction. See [examples/transactions.md](examples/transactions.md) for savepoints, retries, and advisory locks.

```typescript
// ✅ Good Example - Transaction with proper cleanup
async function transferFunds(
  pool: pg.Pool,
  fromId: number,
  toId: number,
  amount: number,
): Promise<void> {
  const client = await pool.connect();
  try {
    await client.query("BEGIN");
    await client.query(
      "UPDATE accounts SET balance = balance - $1 WHERE id = $2",
      [amount, fromId],
    );
    await client.query(
      "UPDATE accounts SET balance = balance + $1 WHERE id = $2",
      [amount, toId],
    );
    await client.query("COMMIT");
  } catch (err) {
    await client.query("ROLLBACK");
    throw err;
  } finally {
    client.release();
  }
}
```

**Why good:** Dedicated client via `pool.connect()`, `ROLLBACK` on error, `client.release()` in `finally` guarantees the client returns to the pool

```typescript
// ❌ Bad Example - Transaction with pool.query()
await pool.query("BEGIN");
await pool.query("UPDATE accounts SET balance = balance - 100 WHERE id = 1");
await pool.query("UPDATE accounts SET balance = balance + 100 WHERE id = 2");
await pool.query("COMMIT");
// Each pool.query() may use a DIFFERENT client -- the BEGIN/COMMIT
// execute on different connections, so there is no transaction at all
```

**Why bad:** `pool.query()` checks out a random client each time -- BEGIN, UPDATEs, and COMMIT may run on different connections, so there is no actual transaction

---

### Pattern 4: Error Handling with PostgreSQL Error Codes

PostgreSQL errors include a `code` field with the SQLSTATE error code. See [reference.md](reference.md) for the full error code table.

```typescript
// ✅ Good Example - Handling specific PostgreSQL errors
const PG_UNIQUE_VIOLATION = "23505";
const PG_FOREIGN_KEY_VIOLATION = "23503";
const PG_DEADLOCK_DETECTED = "40P01";
const PG_SERIALIZATION_FAILURE = "40001";

interface PgError extends Error {
  code: string;
  constraint?: string;
  detail?: string;
  table?: string;
  column?: string;
}

function isPgError(err: unknown): err is PgError {
  return err instanceof Error && "code" in err;
}

try {
  await pool.query("INSERT INTO users (email) VALUES ($1)", [email]);
} catch (err) {
  if (isPgError(err) && err.code === PG_UNIQUE_VIOLATION) {
    throw new ConflictError(`Email already exists: ${err.constraint}`);
  }
  if (isPgError(err) && err.code === PG_DEADLOCK_DETECTED) {
    // Retry the operation
  }
  throw err;
}
```

**Why good:** Named constants for error codes (no magic strings), type guard for safe property access, specific handling per error type, re-throws unknown errors

---

### Pattern 5: Streaming Large Result Sets

Use `pg-cursor` or `pg-query-stream` for queries returning many rows. See [examples/streaming.md](examples/streaming.md) for full streaming patterns.

```typescript
// ✅ Good Example - Cursor for batch processing
import Cursor from "pg-cursor";

const BATCH_SIZE = 100;

async function processAllOrders(pool: pg.Pool): Promise<void> {
  const client = await pool.connect();
  try {
    const cursor = client.query(
      new Cursor("SELECT * FROM orders WHERE status = $1", ["pending"]),
    );

    let rows = await cursor.read(BATCH_SIZE);
    while (rows.length > 0) {
      await processBatch(rows);
      rows = await cursor.read(BATCH_SIZE);
    }

    await cursor.close();
  } finally {
    client.release();
  }
}
```

**Why good:** Processes rows in fixed-size batches without loading entire result set into memory, proper client release in `finally`

---

### Pattern 6: LISTEN/NOTIFY

PostgreSQL can push real-time notifications to connected clients. See [examples/streaming.md](examples/streaming.md) for full examples.

```typescript
// ✅ Good Example - LISTEN/NOTIFY with dedicated client
const CHANNEL = "order_updates";

async function listenForUpdates(pool: pg.Pool): Promise<pg.PoolClient> {
  const client = await pool.connect();

  client.on("notification", (msg) => {
    if (msg.channel === CHANNEL && msg.payload) {
      const data = JSON.parse(msg.payload);
      handleOrderUpdate(data);
    }
  });

  await client.query(`LISTEN ${CHANNEL}`);
  return client; // Caller is responsible for release on shutdown
}

// Publishing from another connection
await pool.query("SELECT pg_notify($1, $2)", [CHANNEL, JSON.stringify(data)]);
```

**Why good:** Dedicated client stays checked out for the lifetime of the listener, `pg_notify()` with parameterized channel/payload prevents injection, JSON payload for structured data

**When to use:** Real-time notifications where sub-second latency matters and the volume is low-to-moderate (hundreds per second). For high-throughput streaming, use a dedicated message broker.

</patterns>

---

<decision_framework>

## Decision Framework

### pool.query() vs pool.connect()

```
Do I need a dedicated client?
├─ Single query, no transaction? -> pool.query() (auto-releases)
├─ Multiple queries in a transaction? -> pool.connect() + BEGIN/COMMIT/ROLLBACK
├─ LISTEN for notifications? -> pool.connect() (keep client for lifetime of listener)
├─ Cursor/streaming? -> pool.connect() (cursor binds to a connection)
└─ Prepared statements across queries? -> pool.connect() (plan caches per connection)
```

### Error Handling Strategy

```
What kind of PostgreSQL error?
├─ 23505 (unique_violation)? -> Map to 409 Conflict, include constraint name
├─ 23503 (foreign_key_violation)? -> Map to 400 Bad Request, entity not found
├─ 23502 (not_null_violation)? -> Map to 400 Bad Request, missing required field
├─ 23514 (check_violation)? -> Map to 400 Bad Request, validation failed
├─ 40P01 (deadlock_detected)? -> Retry with backoff (safe to retry)
├─ 40001 (serialization_failure)? -> Retry with backoff (safe to retry)
├─ 57014 (query_canceled)? -> Timeout, consider increasing statement_timeout
├─ 08xxx (connection_exception)? -> Pool handles reconnection, log and retry
└─ Other? -> Log full error, return 500
```

### Streaming Decision

```
How many rows will the query return?
├─ < 1,000 rows? -> pool.query() is fine (result fits in memory)
├─ 1,000 - 100,000 rows? -> pg-cursor with batch processing
├─ 100,000+ rows? -> pg-query-stream piped to a writable stream
└─ Need to export to file? -> pg-query-stream piped to file write stream
```

</decision_framework>

---

<red_flags>

## RED FLAGS

**High Priority Issues:**

- Using string interpolation/concatenation for SQL values -- this is SQL injection, the most dangerous vulnerability in database code
- Using `pool.query()` for transactions -- each call may use a different connection, so BEGIN/COMMIT have no effect
- Not releasing clients after `pool.connect()` -- leaked clients exhaust the pool; once `max` clients leak, the app deadlocks on `pool.connect()`
- Missing `pool.on("error")` handler -- idle client errors are emitted on the pool; unhandled, they crash the Node.js process
- Using standalone `Client` in application code -- no pooling, no reconnection, no concurrency

**Medium Priority Issues:**

- `SELECT *` in production queries -- returns unnecessary columns, breaks when schema changes, prevents index-only scans
- Loading millions of rows with `pool.query()` instead of streaming -- causes memory exhaustion and GC pressure
- Hardcoded connection strings -- prevents environment-specific configuration, risks credential leaks in version control
- Not handling specific PostgreSQL error codes -- generic error handling loses valuable information (which constraint, which column)
- Using `LISTEN` with `pool.query()` -- notifications bind to a specific connection; pool.query releases the connection immediately

**Common Mistakes:**

- Forgetting that `result.rows[0]` can be `undefined` when no rows match -- always check before accessing
- Assuming `result.rowCount` tells you how many rows a `SELECT` returned -- for `SELECT`, check `result.rows.length` instead; `rowCount` is from the command tag
- Using `$1` inside string literals in SQL -- `'$1'` is a literal string, not a parameter; use `$1` outside quotes
- Forgetting that PostgreSQL arrays in parameters are automatically converted -- `[1, 2, 3]` becomes `{1,2,3}` which works for `= ANY($1)` but not for `IN ($1)` (use `= ANY($1::int[])` instead of `IN`)
- Calling `client.release(true)` routinely -- passing `true` destroys the client instead of returning it to the pool; only use after unrecoverable errors

**Gotchas & Edge Cases:**

- Pool `error` event vs query errors: Pool `error` fires for idle client backend disconnections (e.g., server restart). Query errors are thrown/rejected from the query call itself. You need both handlers.
- `connectionTimeoutMillis: 0` (default) means **no timeout** -- connections wait forever if the pool is exhausted. Always set a timeout in production.
- `idleTimeoutMillis` only affects clients that have been returned to the pool -- a checked-out client that is never released will never be cleaned up.
- PostgreSQL `numeric`/`decimal` types are returned as **strings** by default (to avoid JavaScript floating-point precision loss). Parse them explicitly if you need numbers.
- `LISTEN` survives transactions -- if you `BEGIN`, `LISTEN channel`, `ROLLBACK`, the listener is still active. LISTEN is not transactional.
- `pool.end()` waits for all checked-out clients to be released. If a client is leaked (never released), `pool.end()` hangs forever.
- SSL connections: if you set `ssl: true` in the config AND pass `sslmode=require` in the connection string, the connection string's SSL parameters overwrite your config object.

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST use parameterized queries (`$1`, `$2`, ...) for ALL values -- NEVER concatenate or interpolate user input into SQL strings)**

**(You MUST use `Pool` for all database access -- NEVER create standalone `Client` instances in application code)**

**(You MUST release clients back to the pool in a `finally` block after `pool.connect()` -- leaked clients exhaust the pool and hang the application)**

**(You MUST handle the `error` event on Pool instances -- unhandled idle client errors crash the Node.js process)**

**Failure to follow these rules will cause SQL injection vulnerabilities, connection pool exhaustion, application hangs, and process crashes.**

</critical_reminders>
