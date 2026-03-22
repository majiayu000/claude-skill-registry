---
name: api-baas-neon
description: Serverless PostgreSQL with branching, autoscaling, and edge-compatible driver
---

# Neon Serverless PostgreSQL Patterns

> **Quick Guide:** Use `@neondatabase/serverless` for edge/serverless database access. Prefer the `neon()` HTTP function for single queries (faster, stateless) and `Pool`/`Client` for interactive transactions. Use pooled connection strings (`-pooler` suffix) for serverless workloads, direct connections only for migrations. Branch your database for dev/preview environments using copy-on-write semantics. Always handle cold starts from scale-to-zero (200-500ms wake-up).

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST use the `neon()` HTTP function for single queries in edge/serverless runtimes -- it is 2-3x faster than WebSocket for one-shot operations)**

**(You MUST close `Pool`/`Client` connections within the same request handler in serverless environments -- WebSocket connections cannot outlive a single request)**

**(You MUST use pooled connection strings (`-pooler` suffix) for serverless workloads -- direct connections exhaust the limited connection slots)**

**(You MUST handle scale-to-zero wake-up latency (200-500ms) with appropriate connection timeouts and retry logic)**

**(You MUST use `sql.unsafe()` only for trusted, known-safe strings like table/column names -- never for user input)**

</critical_requirements>

---

**Auto-detection:** Neon, @neondatabase/serverless, neon(), neonConfig, neon serverless driver, neon database, neon branch, neonctl, neon connection pooling, neon scale-to-zero, neon autoscaling, neon postgres, ep-\*-pooler

**When to use:**

- Querying Postgres from edge/serverless functions (edge runtimes, serverless platforms)
- Setting up connection strings (pooled vs direct) for different workloads
- Creating database branches for dev, preview, or CI environments
- Managing scale-to-zero behavior and cold start optimization
- Running transactions in serverless contexts (HTTP batch or WebSocket)
- Programmatic branch management via Neon API or neonctl CLI

**Key patterns covered:**

- `neon()` HTTP queries with SQL tagged templates and composable fragments
- `Pool`/`Client` WebSocket connections with proper lifecycle management
- Pooled (`-pooler`) vs direct connection strings and when to use each
- Database branching (dev branches, PR preview branches, schema-only branches)
- Scale-to-zero behavior, cold start mitigation, and autoscaling
- `sql.transaction()` for non-interactive HTTP transactions
- Neon API and neonctl CLI for programmatic branch management

**When NOT to use:**

- Traditional long-lived server connections (use standard `pg` driver with TCP)
- Complex ORM-specific patterns (use your ORM's own skill)
- General PostgreSQL query syntax (use a SQL/Postgres skill)

**Detailed Resources:**

- For decision frameworks and quick lookup tables, see [reference.md](reference.md)

**Driver & Queries:**

- [examples/core.md](examples/core.md) -- Driver setup, HTTP queries, WebSocket connections, transactions

**Branching & Operations:**

- [examples/branching.md](examples/branching.md) -- Dev branches, PR previews, neonctl CLI, Neon API, CI/CD workflows

---

<philosophy>

## Philosophy

Neon separates storage and compute for PostgreSQL, enabling serverless features impossible with traditional Postgres: scale-to-zero, instant branching, and autoscaling. The `@neondatabase/serverless` driver replaces TCP with HTTP and WebSockets, making Postgres accessible from edge runtimes that lack TCP support.

**Core principles:**

1. **HTTP for speed, WebSocket for sessions** -- The `neon()` function uses HTTP fetch (~3 round trips) for single queries. `Pool`/`Client` use WebSockets (~8 round trips) when you need sessions or interactive transactions. Pick the right transport for the job.
2. **Pooled by default** -- Pooled connections route through PgBouncer (transaction mode), handling up to 10,000 concurrent clients. Direct connections are limited by compute size (100-4,000) and should only be used for migrations or features requiring session state.
3. **Branches are cheap** -- Copy-on-write means a branch of a 500GB database allocates no extra storage until data diverges. Use branches freely for dev, preview, testing, and CI.
4. **Scale-to-zero is the default** -- Computes suspend after 5 minutes of inactivity. Cold starts take 200-500ms. Design for this with timeouts, retries, and connection pooling.
5. **SQL injection safety built in** -- The tagged template function parameterizes automatically. Since v1.0, calling `neon()` as a regular function is a type error, preventing accidental injection.

**When to use Neon serverless driver:**

- Edge/serverless functions that cannot open TCP connections
- Applications benefiting from database branching (preview environments per PR)
- Cost-sensitive workloads that benefit from scale-to-zero
- High-concurrency serverless apps needing connection pooling

**When NOT to use:**

- Long-running server processes with persistent connections (use standard `pg` over TCP)
- Workloads requiring session-level features through PgBouncer (LISTEN/NOTIFY, SET, temporary tables)
- Databases larger than 16 CU that need always-on compute (scale-to-zero not available above 16 CU)

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: HTTP Queries with `neon()`

The `neon()` function creates an HTTP-based query function using SQL tagged templates. It is the fastest path for single, non-interactive queries.

```typescript
import { neon } from "@neondatabase/serverless";

const DATABASE_URL = process.env.DATABASE_URL!;
const sql = neon(DATABASE_URL);

// Tagged template -- parameters are auto-parameterized (safe from injection)
const userId = "abc-123";
const posts =
  await sql`SELECT id, title FROM posts WHERE author_id = ${userId}`;
```

**Why good:** Tagged template auto-parameterizes values preventing SQL injection, HTTP is ~3 round trips vs ~8 for WebSocket, stateless (no connection to manage)

```typescript
// BAD: Calling neon() as a regular function (v1.0+ type error)
const sql = neon(DATABASE_URL);
const result = await sql(`SELECT * FROM posts WHERE id = ${id}`); // TYPE ERROR + SQL injection risk
```

**Why bad:** Since v1.0, calling the query function as a regular function (not a tagged template) is a runtime and type error -- this was changed specifically to prevent SQL injection from string interpolation

---

### Pattern 2: Composable Query Fragments

Template queries support composition with automatic parameter numbering across fragments.

```typescript
import { neon } from "@neondatabase/serverless";

const sql = neon(DATABASE_URL);

// Build queries from reusable fragments
const whereClause = sql`WHERE status = ${"active"} AND role = ${"admin"}`;
const orderClause = sql`ORDER BY created_at DESC`;
const PAGE_SIZE = 20;
const limitClause = sql`LIMIT ${PAGE_SIZE}`;

const users =
  await sql`SELECT id, name, email FROM users ${whereClause} ${orderClause} ${limitClause}`;
```

**Why good:** Parameters are renumbered automatically across composed fragments, named constant for page size, fragments are reusable across queries

#### Dynamic Table/Column Names with `sql.unsafe()`

```typescript
// ONLY for trusted, known-safe values -- never user input
const TABLE_NAME = "posts";
const results =
  await sql`SELECT * FROM ${sql.unsafe(TABLE_NAME)} WHERE id = ${postId}`;
```

**When to use:** Only when you need to interpolate trusted identifiers (table names, column names) that cannot be parameterized in SQL. Never pass user-supplied values to `sql.unsafe()`.

---

### Pattern 3: HTTP Transactions with `sql.transaction()`

Execute multiple queries atomically via HTTP without needing a WebSocket connection.

```typescript
import { neon } from "@neondatabase/serverless";

const sql = neon(DATABASE_URL);

// Array form -- all queries execute in a single HTTP round trip
const [posts, totalCount] = await sql.transaction([
  sql`SELECT id, title FROM posts ORDER BY created_at DESC LIMIT 10`,
  sql`SELECT count(*) FROM posts`,
]);

// Function form with transaction options
const [, transferResult] = await sql.transaction(
  (txn) => [
    txn`UPDATE accounts SET balance = balance - ${amount} WHERE id = ${fromId}`,
    txn`UPDATE accounts SET balance = balance + ${amount} WHERE id = ${toId}`,
  ],
  { isolationLevel: "Serializable" },
);
```

**Why good:** Atomic execution without WebSocket overhead, array form is concise for read-only batches, function form supports transaction options, isolation level controls consistency guarantees

```typescript
// BAD: Running related queries as separate HTTP requests
const posts = await sql`SELECT * FROM posts WHERE author_id = ${authorId}`;
const author = await sql`SELECT * FROM users WHERE id = ${authorId}`;
// Two separate HTTP round trips, not atomic, race conditions possible
```

**Why bad:** Separate HTTP calls are not atomic, data can change between queries, double the network latency

#### Transaction Options

- `isolationLevel`: `ReadUncommitted` | `ReadCommitted` | `RepeatableRead` | `Serializable`
- `readOnly`: boolean (default `false`)
- `deferrable`: boolean (default `false`, only effective with `readOnly: true` + `Serializable`)

---

### Pattern 4: WebSocket Connections with `Pool`/`Client`

Use `Pool` and `Client` for interactive transactions or `node-postgres` API compatibility. In serverless environments, connections must be created and closed within a single request handler.

```typescript
import { Pool } from "@neondatabase/serverless";

export async function handleRequest(request: Request): Promise<Response> {
  const pool = new Pool({ connectionString: process.env.DATABASE_URL });
  try {
    // ... queries ...
  } finally {
    await pool.end(); // ALWAYS close within the same request
  }
}
```

**Key rule:** Create Pool inside the handler, close with `pool.end()` in `finally`. A global Pool leaks WebSocket connections between serverless invocations.

See [examples/core.md](examples/core.md) -- Patterns 5-7 for request-scoped pools, interactive transactions, and Node.js WebSocket configuration.

---

### Pattern 5: Connection String Setup

Neon provides two connection string formats: pooled (via PgBouncer) and direct.

```bash
# Pooled connection (note: -pooler suffix on endpoint ID)
# Use for: serverless functions, web apps, high-concurrency workloads
DATABASE_URL=postgresql://user:pass@ep-cool-dawn-123456-pooler.us-east-2.aws.neon.tech/dbname?sslmode=require

# Direct connection (no -pooler suffix)
# Use for: migrations, pg_dump, LISTEN/NOTIFY, session-level features
DIRECT_DATABASE_URL=postgresql://user:pass@ep-cool-dawn-123456.us-east-2.aws.neon.tech/dbname?sslmode=require
```

**Why good:** Pooled handles up to 10,000 concurrent clients via PgBouncer in transaction mode, direct provides full session features for admin tasks, separate env vars make the distinction explicit

#### PgBouncer Transaction Mode Limitations

The pooled connection runs PgBouncer in **transaction mode**, which means connections return to the pool after each transaction. This prohibits:

- `SET` / `RESET` statements (use `ALTER ROLE ... SET` instead)
- `LISTEN` / `NOTIFY`
- `WITH HOLD CURSOR`
- SQL-level `PREPARE` / `DEALLOCATE` (protocol-level prepared statements up to 1,000 are supported)
- Temporary tables with `PRESERVE` / `DELETE ROWS`
- Session-level advisory locks

---

### Pattern 6: Cold Start and Scale-to-Zero Handling

Neon computes auto-suspend after 5 minutes of inactivity (default). Cold starts take 200-500ms. Design for this with appropriate timeouts and retry logic.

```typescript
const CONNECTION_TIMEOUT_MS = 10_000;
const sql = neon(process.env.DATABASE_URL!, {
  fetchOptions: { signal: AbortSignal.timeout(CONNECTION_TIMEOUT_MS) },
});
```

**Key rule:** Set explicit timeouts (10-15s) to accommodate cold start latency. Use exponential backoff retries for reliability.

See [examples/core.md](examples/core.md) -- Pattern 8 for full timeout configuration and retry patterns.

#### Scale-to-Zero Facts

- Default auto-suspend: 5 minutes of inactivity
- Cold start latency: ~200-500ms (varies by region and compute size)
- Only available for computes up to 16 CU (larger computes stay always-on)
- Paid plans can adjust suspend timeout (up to 7 days) or disable entirely
- Active logical replication subscribers prevent suspension

---

### Pattern 7: Database Branching

Neon branches use copy-on-write semantics -- branching a 500GB database is instant and allocates no extra storage until data diverges.

```bash
# Install neonctl
npm install -g neonctl

# Create a dev branch from main
neonctl branches create --name dev-alice --project-id <project-id>

# Create a branch with automatic expiration (for CI/preview)
neonctl branches create --name preview/pr-42 --project-id <project-id> --expires-at "2025-04-01T00:00:00Z"

# Create schema-only branch (no data copied -- for sensitive environments)
neonctl branches create --name ci-test --schema-only --project-id <project-id>

# Reset a dev branch to match current production
neonctl branches reset dev-alice --parent --project-id <project-id>

# Delete a branch
neonctl branches delete preview/pr-42 --project-id <project-id>
```

**Why good:** Named branches map to git workflow, TTL expiration auto-cleans CI branches, schema-only branching protects sensitive data, reset syncs dev with production without recreating

#### Branch Connection Strings

Each branch gets its own endpoint. The branch connection string follows the same format but with a different endpoint ID:

```bash
# Main branch
postgresql://user:pass@ep-cool-dawn-123456-pooler.us-east-2.aws.neon.tech/dbname

# Dev branch -- different endpoint ID
postgresql://user:pass@ep-quiet-hill-789012-pooler.us-east-2.aws.neon.tech/dbname
```

---

### Pattern 8: Neon API for Programmatic Branch Management

The Neon REST API (`https://console.neon.tech/api/v2`) enables programmatic branch management. Authenticate with `Authorization: Bearer <NEON_API_KEY>`. Key operations: create branches with TTL expiration, delete branches, list branches for cleanup scripts.

```typescript
const NEON_API_BASE = "https://console.neon.tech/api/v2";
// POST /projects/{projectId}/branches -- create with { branch: { name, expires_at }, endpoints: [{ type: "read_write" }] }
// DELETE /projects/{projectId}/branches/{branchId} -- delete a branch
```

See [examples/branching.md](examples/branching.md) -- Pattern 3 for a full typed TypeScript branch manager with create, delete, and list operations.
See [reference.md](reference.md) for the complete API endpoint table.

</patterns>

---

<decision_framework>

## Decision Framework

### HTTP (`neon()`) vs WebSocket (`Pool`/`Client`)

```
What kind of database operation?
+-- Single query (SELECT, INSERT, UPDATE, DELETE)
|   +-- YES --> Use neon() HTTP function (fastest, ~3 round trips)
+-- Multiple queries that must be atomic?
|   +-- Can all queries be determined upfront (non-interactive)?
|   |   +-- YES --> Use sql.transaction() over HTTP
|   |   +-- NO --> Use Pool/Client over WebSocket
+-- Need node-postgres (pg) API compatibility?
|   +-- YES --> Use Pool/Client over WebSocket
+-- Running in edge runtime (no TCP)?
    +-- YES --> Use @neondatabase/serverless (HTTP or WebSocket)
    +-- NO --> Standard pg driver with TCP may be simpler
```

### Pooled vs Direct Connection

```
What is the workload?
+-- Serverless function / edge function --> Pooled (-pooler)
+-- Web application (many concurrent requests) --> Pooled (-pooler)
+-- Schema migration --> Direct (needs session state)
+-- pg_dump / pg_restore --> Direct (uses SET statements)
+-- LISTEN / NOTIFY --> Direct (session-level feature)
+-- Long-running analytics query --> Direct (avoid pool contention)
+-- Default / unsure --> Pooled (-pooler)
```

### Branch Strategy

```
What do you need the branch for?
+-- Developer working on a feature --> Dev branch (long-lived, manually managed)
+-- PR preview environment --> Preview branch (TTL expiration, auto-cleanup on merge)
+-- CI test run --> Ephemeral branch (short TTL, schema-only if data-sensitive)
+-- Database recovery --> Restore from branch history (up to 30 days on Scale plan)
+-- Load testing --> Branch from production (copy-on-write, no storage cost until diverge)
```

</decision_framework>

---

<red_flags>

## RED FLAGS

**High Priority Issues:**

- **Global `Pool` in serverless** -- Creating a Pool outside the request handler in edge/serverless functions leaks WebSocket connections. Pool/Client must be created, used, and closed within a single request.
- **Using direct connection string in serverless** -- Direct connections bypass PgBouncer and are limited to compute-size max connections (100-4,000). Serverless functions should always use pooled (`-pooler`) connections.
- **Passing user input to `sql.unsafe()`** -- `sql.unsafe()` embeds raw SQL without parameterization. It exists only for trusted identifiers (table/column names). User input in `sql.unsafe()` is a SQL injection vulnerability.

**Medium Priority Issues:**

- **Double pooling** -- Combining Neon's server-side PgBouncer with a client-side connection pool in your driver creates unnecessary overhead. Let Neon handle pooling.
- **Ignoring `pool.end()` in serverless** -- Forgetting to call `pool.end()` after using WebSocket connections exhausts available connections across invocations.
- **Using `SET` statements through pooled connections** -- PgBouncer transaction mode resets session state after each transaction. Use `ALTER ROLE ... SET` for role-level defaults or use direct connections.
- **Not handling cold start latency** -- First request after idle period adds 200-500ms. Without appropriate timeouts (10+ seconds) and retry logic, applications fail intermittently.

**Common Mistakes:**

- **Wrong package name** -- The package is `@neondatabase/serverless`, not `neon-serverless` or `pg-neon`.
- **Missing `ws` package on Node.js <= v21** -- Node.js versions before v22 lack built-in WebSocket support. Set `neonConfig.webSocketConstructor = ws` when using Pool/Client.
- **Calling `neon()` result as a function instead of tagged template** -- `sql("SELECT ...")` is a type error since v1.0. Use `` sql`SELECT ...` `` (tagged template).
- **Expecting Pool to survive across serverless invocations** -- Each cold start creates a new execution context. Do not rely on global state for connection management.
- **64MB request/response limit** -- HTTP mode has a 64MB payload limit. Large result sets or bulk inserts must be chunked.

**Gotchas & Edge Cases:**

- **Transaction options apply to the transaction, not individual queries** -- Setting `arrayMode: true` on individual queries inside `sql.transaction()` is ignored. Set it on the transaction itself.
- **PgBouncer's 120-second query wait timeout** -- If all pooled connections are busy, new queries queue for up to 120 seconds before timing out.
- **Branch endpoints are different from parent** -- Each branch gets a unique endpoint ID. You cannot use the parent's connection string to connect to a child branch.
- **Scale-to-zero only for computes <= 16 CU** -- Computes larger than 16 CU remain always-on regardless of configuration.
- **Logical replication prevents suspension** -- Active replication subscribers keep the compute running, bypassing scale-to-zero.
- **Schema-only branches** -- Use `neonctl branches create --schema-only` or the REST API with `"init_source": "schema-only"`. Schema-only branches require exactly one read-write compute endpoint.
- **Branch history has a retention window** -- Free plan: 6 hours. Launch: 7 days. Scale: 30 days. You cannot restore beyond this window.
- **Node.js v19+ required** -- The GA version of `@neondatabase/serverless` (v1.0+) requires Node.js 19 or higher.

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST use the `neon()` HTTP function for single queries in edge/serverless runtimes -- it is 2-3x faster than WebSocket for one-shot operations)**

**(You MUST close `Pool`/`Client` connections within the same request handler in serverless environments -- WebSocket connections cannot outlive a single request)**

**(You MUST use pooled connection strings (`-pooler` suffix) for serverless workloads -- direct connections exhaust the limited connection slots)**

**(You MUST handle scale-to-zero wake-up latency (200-500ms) with appropriate connection timeouts and retry logic)**

**(You MUST use `sql.unsafe()` only for trusted, known-safe strings like table/column names -- never for user input)**

**Failure to follow these rules will cause connection exhaustion, SQL injection vulnerabilities, or intermittent cold-start failures.**

</critical_reminders>
