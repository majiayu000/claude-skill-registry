---
name: api-baas-turso
description: Edge-hosted SQLite database with libSQL driver and embedded replicas
---

# Turso / libSQL Patterns

> **Quick Guide:** Use `@libsql/client` for all Turso database access. Use `execute()` for single queries, `batch()` for atomic multi-statement operations (preferred over interactive transactions), and `transaction()` only when subsequent queries depend on prior results. For edge/serverless runtimes without filesystem access, import from `@libsql/client/web`. For zero-latency reads, configure embedded replicas with a local file URL + `syncUrl`. All writes are forwarded to the primary -- design for 15-50ms write latency. Turso is SQLite under the hood: single-writer model, no `ALTER TABLE ... ADD CONSTRAINT`, no stored procedures.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST use `batch()` with a transaction mode for multi-statement atomic operations -- it is faster and safer than interactive `transaction()` because it executes in a single round trip)**

**(You MUST import from `@libsql/client/web` in edge/serverless runtimes that lack filesystem access (Cloudflare Workers, Vercel Edge Functions) -- the base `@libsql/client` import pulls in native bindings that fail in these environments)**

**(You MUST specify a transaction mode (`"write"`, `"read"`, or `"deferred"`) as the second argument to `batch()` and `transaction()` -- the default is `"deferred"`, which silently fails to acquire a write lock for INSERT/UPDATE/DELETE)**

**(You MUST call `client.close()` when the client is no longer needed in short-lived processes -- open clients hold connections and file handles)**

**(You MUST NOT access the local embedded replica database file directly while the client is running -- concurrent access causes data corruption)**

</critical_requirements>

---

**Auto-detection:** Turso, libSQL, @libsql/client, createClient, turso.io, embedded replica, syncUrl, syncInterval, turso db, turso group, libsql, .turso.io, TURSO_DATABASE_URL, TURSO_AUTH_TOKEN

**When to use:**

- Querying a Turso-hosted SQLite database from any runtime (Node.js, edge, serverless)
- Setting up embedded replicas for zero-latency local reads synced from a remote primary
- Running atomic multi-statement operations with `batch()` or interactive `transaction()`
- Managing database groups and multi-region placement via the Turso CLI
- Choosing between `@libsql/client` (Node.js / has filesystem) and `@libsql/client/web` (edge / no filesystem)

**Key patterns covered:**

- Client setup with `createClient()` (remote, local, in-memory, embedded replica)
- `execute()` with positional (`?`) and named (`:name`, `@name`, `$name`) parameters
- `batch()` for atomic multi-statement operations in a single round trip
- Interactive `transaction()` for conditional logic between queries
- Embedded replicas: local file + `syncUrl`, `sync()`, read-your-writes semantics
- Import paths: `@libsql/client` vs `@libsql/client/web`
- Turso CLI: `turso db create`, `turso db shell`, `turso group create`

**When NOT to use:**

- Write-heavy workloads requiring strong multi-writer consistency (Turso is single-writer, writes forwarded to primary)
- Complex relational queries needing PostgreSQL features (CTEs with mutating subqueries, stored procedures, advanced constraints)
- Large analytical datasets (SQLite row-size and concurrency limitations apply)

**Detailed Resources:**

- For decision frameworks and quick lookup tables, see [reference.md](reference.md)

**Client & Queries:**

- [examples/core.md](examples/core.md) -- Client setup, execute, batch, transactions, import paths

**Embedded Replicas:**

- [examples/embedded-replicas.md](examples/embedded-replicas.md) -- Local replicas, sync, offline mode, encryption

---

<philosophy>

## Philosophy

Turso brings SQLite to the edge by hosting libSQL (a fork of SQLite) as a managed service with multi-region replication. The `@libsql/client` driver provides a unified API that works identically whether you are connecting to a remote Turso database, a local SQLite file, an in-memory database, or an embedded replica that syncs from a remote primary.

**Core principles:**

1. **Batch over transaction** -- `batch()` sends all statements in a single round trip and executes them in an implicit transaction. Interactive `transaction()` requires multiple round trips and holds a database lock (5-second timeout). Use `batch()` unless you need conditional logic between queries.
2. **Writes always hit the primary** -- Even with embedded replicas, writes are forwarded to the remote primary database. Write latency is 15-50ms depending on distance to the primary region. Design for this: optimistic UI, background sync, avoid write-heavy hot paths.
3. **Embedded replicas for reads** -- A local SQLite file synced from the remote primary. Reads are microsecond-level. Writes forward to remote. The local file updates after a successful write (read-your-writes semantics).
4. **Two import paths** -- `@libsql/client` includes native SQLite bindings for Node.js and supports `file:` URLs. `@libsql/client/web` is pure JS/WASM for edge runtimes (Cloudflare Workers, Vercel Edge Functions) and cannot open local files.
5. **SQLite semantics** -- Turso is SQLite. No `ADD CONSTRAINT`, no stored procedures, no `LISTEN/NOTIFY`, single-writer WAL mode. Know SQLite's limitations before choosing Turso.

**When to use Turso:**

- Read-heavy workloads benefiting from edge-local reads (embedded replicas)
- Multi-tenant SaaS with database-per-tenant (Turso supports millions of databases)
- Serverless/edge functions needing a database without connection pooling complexity
- Applications benefiting from SQLite's simplicity and zero-config nature

**When NOT to use:**

- Write-heavy workloads (single-writer bottleneck, all writes forwarded to primary)
- Complex distributed transactions across multiple databases
- Workloads requiring PostgreSQL-specific features (jsonb operators, array types, window functions with advanced frames)
- Large datasets exceeding SQLite's practical limits (~281 TB theoretical, but performance degrades much earlier)

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Client Setup

Create a client with `createClient()`. The `url` determines the connection type.

```typescript
import { createClient } from "@libsql/client";

// Remote Turso database
const client = createClient({
  url: "libsql://my-database-my-org.turso.io",
  authToken: process.env.TURSO_AUTH_TOKEN,
});

// Local SQLite file (Node.js only -- not available in @libsql/client/web)
const localClient = createClient({
  url: "file:local.db",
});

// In-memory database (useful for tests)
const memoryClient = createClient({
  url: ":memory:",
});
```

**Why good:** Single `createClient` API for all connection types, environment variable for auth token (not hardcoded), clear distinction between remote/local/memory

```typescript
// BAD: Hardcoded credentials
const client = createClient({
  url: "libsql://my-database-my-org.turso.io",
  authToken: "eyJhbGciOiJFZERTQSIsInR5cCI6IkpXVCJ9...", // Leaked credential
});
```

**Why bad:** Auth token committed to source code, will be exposed in version control

---

### Pattern 2: Executing Queries

`execute()` runs a single SQL statement with automatic parameterization.

```typescript
// Positional parameters with ?
const userId = "usr_123";
const result = await client.execute({
  sql: "SELECT id, name, email FROM users WHERE id = ?",
  args: [userId],
});
// result.rows: Array<Row>, result.columns: ["id", "name", "email"]
// result.rowsAffected: 0 (for SELECT), result.lastInsertRowid: undefined

// Named parameters with : prefix
const insertResult = await client.execute({
  sql: "INSERT INTO users (name, email) VALUES (:name, :email)",
  args: { name: "Alice", email: "alice@example.com" },
});
// insertResult.lastInsertRowid: bigint of the new row's rowid
```

**Why good:** Parameterized queries prevent SQL injection, named parameters are self-documenting for inserts/updates, Row objects support both index and column-name access

```typescript
// BAD: String interpolation -- SQL injection
const name = userInput;
await client.execute(`SELECT * FROM users WHERE name = '${name}'`);
```

**Why bad:** User input interpolated directly into SQL string, trivial SQL injection vector

#### Supported Parameter Prefixes

Named parameters accept `:name`, `@name`, or `$name` syntax interchangeably. The args object uses the bare name without the prefix: `{ name: "Alice" }` matches `:name`, `@name`, and `$name`.

---

### Pattern 3: Batch Operations

`batch()` executes multiple statements atomically in a single round trip. All succeed or all roll back.

```typescript
const ACTIVE_STATUS = "active";

const results = await client.batch(
  [
    {
      sql: "INSERT INTO users (name, email, status) VALUES (?, ?, ?)",
      args: ["Alice", "alice@example.com", ACTIVE_STATUS],
    },
    {
      sql: "INSERT INTO audit_log (action, entity, entity_id) VALUES (?, ?, last_insert_rowid())",
      args: ["user_created", "users"],
    },
  ],
  "write",
);
// results[0].lastInsertRowid -- the new user's rowid
// results[1].lastInsertRowid -- the new audit log entry's rowid
```

**Why good:** Single round trip for multiple statements, implicit transaction (all-or-nothing), `"write"` mode required for INSERT/UPDATE/DELETE, `last_insert_rowid()` works across statements in the same batch

```typescript
// BAD: Multiple execute() calls instead of batch()
await client.execute({ sql: "INSERT INTO users ...", args: [...] });
await client.execute({ sql: "INSERT INTO audit_log ...", args: [...] });
// Two round trips, NOT atomic -- if second fails, first is already committed
```

**Why bad:** Separate execute() calls are not atomic, each is a separate round trip with independent latency, partial failure leaves inconsistent data

#### Transaction Modes for batch()

Use `"write"` for any INSERT/UPDATE/DELETE, `"read"` for SELECT-only (allows parallel reads), `"deferred"` starts read-only and escalates. See [reference.md](reference.md) for the full comparison table.

---

### Pattern 4: Interactive Transactions

Use `transaction()` only when subsequent queries depend on results of earlier queries. It holds a database lock and requires multiple round trips.

```typescript
async function transferCredits(fromId: string, toId: string, amount: number) {
  const MIN_TRANSFER = 0;
  if (amount <= MIN_TRANSFER) {
    throw new Error("Amount must be positive");
  }

  const tx = await client.transaction("write");

  try {
    const { rows } = await tx.execute({
      sql: "SELECT balance FROM accounts WHERE id = ?",
      args: [fromId],
    });

    if (rows.length === 0) {
      throw new Error("Account not found");
    }

    const balance = rows[0].balance as number;
    if (balance < amount) {
      throw new Error("Insufficient balance");
    }

    // These depend on the SELECT result above -- interactive transaction required
    await tx.execute({
      sql: "UPDATE accounts SET balance = balance - ? WHERE id = ?",
      args: [amount, fromId],
    });
    await tx.execute({
      sql: "UPDATE accounts SET balance = balance + ? WHERE id = ?",
      args: [amount, toId],
    });

    await tx.commit();
  } catch (error) {
    await tx.rollback();
    throw error;
  }
}
```

**Why good:** Interactive transaction needed because UPDATE depends on SELECT result, explicit commit/rollback, named constant for validation, proper error propagation

**When to use:** Only when later statements depend on results of earlier statements within the same transaction. If all statements are known upfront, use `batch()` instead.

---

### Pattern 5: Import Paths for Different Runtimes

```typescript
// Node.js, Bun, Deno (has filesystem access, native bindings)
import { createClient } from "@libsql/client";

// Edge/serverless runtimes WITHOUT filesystem (Cloudflare Workers, Vercel Edge)
import { createClient } from "@libsql/client/web";
```

**Why good:** Correct import for the runtime, `@libsql/client/web` is pure JS/WASM and works in any environment, base package includes native SQLite bindings that fail in edge runtimes

```typescript
// BAD: Using base import in Cloudflare Worker
import { createClient } from "@libsql/client"; // FAILS -- native bindings not available

export default {
  async fetch(request: Request, env: Env) {
    const client = createClient({
      url: env.TURSO_URL,
      authToken: env.TURSO_TOKEN,
    });
    // Runtime error: native module not found
  },
};
```

**Why bad:** Base `@libsql/client` bundles native SQLite bindings via `libsql` (Rust compiled to native), which edge runtimes cannot load

#### Quick Decision

```
Does your runtime have filesystem access and native module support?
+-- YES --> @libsql/client (Node.js, Bun, Deno, VMs)
+-- NO  --> @libsql/client/web (Cloudflare Workers, Vercel Edge, browsers)
```

---

### Pattern 6: Embedded Replicas

A local SQLite file that syncs from a remote Turso primary. Reads are local (microseconds), writes forward to remote (15-50ms).

```typescript
const client = createClient({
  url: "file:local-replica.db",
  syncUrl: process.env.TURSO_DATABASE_URL,
  authToken: process.env.TURSO_AUTH_TOKEN,
  syncInterval: 60, // Auto-sync every 60 seconds
});
await client.sync(); // Populate local replica before first read
```

Key points: `file:` URL for local replica, `syncUrl` for remote primary, call `sync()` on startup, reads are local, writes forward to remote with read-your-writes semantics.

**When to use:** VMs, VPS, containers, or any long-running process with filesystem access. Not available in serverless/edge runtimes without filesystem. See [examples/embedded-replicas.md](examples/embedded-replicas.md) for full patterns including manual sync, offline mode, and encryption.

---

### Pattern 7: Database Groups and Multi-Region

Turso organizes databases into groups. Each group has a primary region and optional replica locations.

```bash
# Create a group with explicit primary location
turso group create my-group --location iad

# Add replica locations to the group
turso group locations add my-group ord
turso group locations add my-group lhr

# Create a database in the group (inherits all group locations)
turso db create my-app --group my-group

# List databases
turso db list

# Get connection URL
turso db show my-app --url
```

**Why good:** Groups define replication topology once, all databases in the group inherit locations, explicit primary location for predictable write latency

#### How Writes Work with Groups

All writes go to the primary region regardless of which replica handles the read. Adding more locations improves read latency globally but does not reduce write latency. Write latency is determined by distance to the primary region.

</patterns>

---

<decision_framework>

## Decision Framework

### batch() vs transaction()

```
Are all SQL statements known upfront (no conditional logic between them)?
+-- YES --> Use batch() (single round trip, implicit transaction, preferred)
+-- NO  --> Do later statements depend on results of earlier statements?
    +-- YES --> Use transaction() (interactive, multiple round trips, holds lock)
    +-- NO  --> Use batch()
```

### Import Path Selection

```
What runtime environment?
+-- Node.js / Bun / Deno / VM / container
|   +-- Need embedded replicas (local file)?
|   |   +-- YES --> @libsql/client with file: URL + syncUrl
|   |   +-- NO  --> @libsql/client with libsql:// URL
+-- Cloudflare Workers / Vercel Edge / browser / serverless without filesystem
    +-- @libsql/client/web (remote connections only, no file: URLs)
```

### Embedded Replica vs Remote-Only

```
Is the process long-lived with filesystem access?
+-- YES --> Do you need sub-millisecond read latency?
|   +-- YES --> Embedded replica (file: URL + syncUrl)
|   +-- NO  --> Remote-only is simpler (libsql:// URL)
+-- NO (serverless, edge, short-lived)
    +-- Remote-only (@libsql/client/web, libsql:// URL)
```

### Transaction Mode Selection

```
What operations will the batch/transaction perform?
+-- Only SELECT queries --> "read" (allows parallel execution on replicas)
+-- Any INSERT / UPDATE / DELETE --> "write" (acquires exclusive lock)
+-- Unsure at call time --> "deferred" (starts read, escalates if needed)
```

</decision_framework>

---

<red_flags>

## RED FLAGS

**High Priority Issues:**

- **Missing transaction mode in `batch()`/`transaction()`** -- Omitting the second argument defaults to `"deferred"`, which starts read-only and may silently fail to acquire a write lock for INSERT/UPDATE/DELETE. Always specify the mode explicitly.
- **Using `@libsql/client` in edge runtimes** -- The base package bundles native SQLite bindings that fail in Cloudflare Workers, Vercel Edge Functions, and similar environments. Use `@libsql/client/web` instead.
- **String interpolation in SQL** -- `execute(\`SELECT \* FROM users WHERE id = '${id}'\`)`is a SQL injection vulnerability. Always use parameterized queries with`args`.
- **Accessing embedded replica file directly** -- Opening the local `.db` file with another SQLite client while the libSQL client is running causes data corruption. Only access through the client.

**Medium Priority Issues:**

- **Using `transaction()` when `batch()` suffices** -- Interactive transactions hold a database lock with a 5-second timeout, require multiple round trips, and block other writers. Use `batch()` for predetermined statement sets.
- **Not calling `client.close()`** -- In short-lived processes (CLI scripts, test teardown), forgetting to close the client leaves connections and file handles open.
- **Ignoring write latency with embedded replicas** -- Reads are microseconds (local), but writes are 15-50ms (forwarded to remote primary). Design accordingly -- avoid tight write loops.
- **Setting `syncInterval` too low** -- Each sync pulls all changed frames (4KB each). Sub-second intervals on write-heavy databases generate significant network and I/O overhead.

**Common Mistakes:**

- **Wrong package name** -- The package is `@libsql/client`, not `libsql-client`, `@turso/client`, or `turso-client`.
- **Named parameter prefix in args object** -- Args use bare names: `{ name: "Alice" }` matches `:name`, `@name`, and `$name` in SQL. Do not include the prefix: `{ ":name": "Alice" }` will not match.
- **Expecting `lastInsertRowid` to be a number** -- It is `bigint | undefined`. If you need a number, explicitly convert: `Number(result.lastInsertRowid)`, but be aware of precision loss for very large rowids.
- **Using `executeMultiple()` for atomic operations** -- `executeMultiple()` runs raw SQL text (semicolon-separated) with no parameterization and no implicit transaction. Use `batch()` for atomic parameterized operations.

**Gotchas & Edge Cases:**

- **`batch()` statements share a transaction but are NOT parallel** -- They execute sequentially. `last_insert_rowid()` in a later statement reflects the previous statement's insert.
- **`transaction()` has a 5-second idle timeout** -- If no statement is executed within 5 seconds after the last one, the transaction is automatically rolled back. This matters on high-latency connections.
- **Embedded replica `sync()` is not atomic with reads** -- If you read immediately after `sync()`, another sync could start. The client handles this internally, but be aware that `syncInterval` syncs happen in the background.
- **Frame-based sync overhead** -- Embedded replica sync operates in 4KB frames. A 1-byte write still transfers a full 4KB frame. B-tree splits and WAL checkpoint operations can trigger unexpectedly large sync payloads.
- **`intMode` affects how SQLite integers are returned** -- Default is `"number"`, which loses precision for integers > 2^53. Use `"bigint"` for large IDs or counters, or `"string"` for universal safety.
- **SQLite type affinity** -- Turso is SQLite. A `TEXT` column will happily store an integer without error. There is no strict type enforcement unless you use `STRICT` tables.
- **No `ALTER TABLE ... ADD CONSTRAINT`** -- SQLite (and Turso) do not support adding constraints after table creation. You must recreate the table.
- **Single-writer model** -- Only one write transaction can execute at a time across all clients. Concurrent write attempts queue behind the current writer. This is fundamental to SQLite/libSQL, not a Turso limitation.

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST use `batch()` with a transaction mode for multi-statement atomic operations -- it is faster and safer than interactive `transaction()` because it executes in a single round trip)**

**(You MUST import from `@libsql/client/web` in edge/serverless runtimes that lack filesystem access (Cloudflare Workers, Vercel Edge Functions) -- the base `@libsql/client` import pulls in native bindings that fail in these environments)**

**(You MUST specify a transaction mode (`"write"`, `"read"`, or `"deferred"`) as the second argument to `batch()` and `transaction()` -- the default is `"deferred"`, which silently fails to acquire a write lock for INSERT/UPDATE/DELETE)**

**(You MUST call `client.close()` when the client is no longer needed in short-lived processes -- open clients hold connections and file handles)**

**(You MUST NOT access the local embedded replica database file directly while the client is running -- concurrent access causes data corruption)**

**Failure to follow these rules will cause data corruption, runtime crashes in edge environments, or silent data inconsistency.**

</critical_reminders>
