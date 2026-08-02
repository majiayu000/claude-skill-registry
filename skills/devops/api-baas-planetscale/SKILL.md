---
name: api-baas-planetscale
description: Serverless MySQL platform with branching, deploy requests, and edge-compatible driver
---

# PlanetScale Serverless MySQL Patterns

> **Quick Guide:** Use `@planetscale/database` for edge/serverless MySQL access via HTTP (Fetch API). Use `Client` to create per-request connections, `conn.execute()` for parameterized queries, and `conn.transaction()` for atomic operations. Never run DDL directly on production -- use deploy requests with safe migrations enabled. PlanetScale runs on Vitess: foreign keys are supported but opt-in, stored procedures are not supported, and all schema changes go through online DDL. The built-in `cast` handles regular integers and floats automatically, but provide a custom `cast` for BigInt, Date, and boolean columns. Branch your database like git branches for dev/preview environments.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST use `conn.execute(sql, params)` with parameterized queries -- never interpolate user input into SQL strings)**

**(You MUST use deploy requests for ALL schema changes on production branches with safe migrations enabled -- direct DDL is rejected)**

**(You MUST create a fresh `Client.connection()` per request in serverless environments -- do not reuse connections across invocations)**

**(You MUST handle the Vitess/MySQL compatibility differences: no stored procedures, no `RENAME COLUMN` via direct DDL, no `:=` operator, no `LOAD DATA INFILE`)**

**(You MUST provide a custom `cast` function for BigInt (INT64/UINT64), Date (DATETIME/TIMESTAMP), and boolean (TINYINT(1)) columns -- the default cast handles regular integers and floats but leaves these as strings)**

</critical_requirements>

---

**Auto-detection:** PlanetScale, @planetscale/database, planetscale serverless driver, pscale, deploy request, safe migrations, Vitess, database branching, planetscale branch, planetscale boost, mysql serverless, pscale CLI, planetscale connection

**When to use:**

- Querying MySQL from edge/serverless functions via the PlanetScale serverless driver
- Managing schema changes through deploy requests and safe migrations
- Creating database branches for dev, preview, or CI environments
- Setting up connections with `@planetscale/database` (host/username/password or URL)
- Running transactions in serverless contexts
- Handling Vitess-specific SQL compatibility constraints
- Programmatic branch management via `pscale` CLI

**Key patterns covered:**

- `connect()` / `Client` connection setup with host, username, password
- `conn.execute()` with positional (`?`) and named (`:param`) parameters
- `conn.transaction()` for atomic multi-statement operations
- Custom `cast` functions for type-safe value conversion (BigInt, Date, boolean)
- Deploy request workflow (branch, change schema, create DR, review, deploy)
- Safe migrations and the no-direct-DDL enforcement model
- Database branching for dev/preview/CI environments
- Vitess SQL compatibility constraints and workarounds
- `pscale` CLI for branch and deploy request management

**When NOT to use:**

- Long-running server processes with persistent TCP MySQL connections (use `mysql2` driver)
- Complex ORM-specific patterns (use your ORM's own skill)
- General MySQL query syntax (use a SQL/MySQL skill)
- PostgreSQL workloads (use Neon or another Postgres provider)

**Detailed Resources:**

- For decision frameworks, CLI reference, and quick lookup tables, see [reference.md](reference.md)

**Driver & Queries:**

- [examples/core.md](examples/core.md) -- Connection setup, parameterized queries, transactions, type casting

**Branching & Schema Changes:**

- [examples/branching.md](examples/branching.md) -- Dev branches, deploy requests, safe migrations, pscale CLI, CI/CD workflows

---

<philosophy>

## Philosophy

PlanetScale is a serverless MySQL platform built on Vitess, the same technology that powers YouTube's database infrastructure. The `@planetscale/database` driver uses HTTP (Fetch API) instead of TCP, making MySQL accessible from edge runtimes that lack TCP support.

**Core principles:**

1. **HTTP-based, stateless connections** -- Every query is an HTTP request. There are no persistent connections to manage, no connection pools to configure. Create a connection, execute queries, done. PlanetScale handles connection pooling at the infrastructure level (Vitess VTTablet + Global Routing).
2. **Schema changes via deploy requests, never direct DDL** -- Production branches with safe migrations reject direct `CREATE`, `ALTER`, `DROP` statements. All schema changes go through deploy requests: branch, modify schema on the branch, create a deploy request, review the diff, deploy with zero downtime via online DDL.
3. **Branches are cheap** -- Database branches are isolated copies of your schema (and optionally data). Create them for feature development, PR previews, CI runs. Delete when done.
4. **Vitess under the hood** -- PlanetScale runs Vitess, which adds horizontal scaling but introduces SQL compatibility differences. No stored procedures, no `RENAME COLUMN` in DDL, no `:=` operator. Foreign keys are supported but opt-in and come with performance trade-offs.
5. **Default cast handles common types, customize for the rest** -- The driver's built-in `cast` function automatically converts INT8-32 and FLOAT32/64 to JavaScript numbers, and parses JSON. However, INT64/UINT64 (BigInt), DATETIME/TIMESTAMP (Date), DECIMAL, and TINYINT(1) (boolean) remain as strings -- provide a custom `cast` function for these.

**When to use PlanetScale serverless driver:**

- Edge/serverless functions that cannot open TCP connections
- Applications using PlanetScale's branching and deploy request workflow
- High-concurrency serverless apps benefiting from PlanetScale's infrastructure-level pooling
- Teams wanting git-like database workflows (branch, review, merge)

**When NOT to use:**

- Long-running server processes (use `mysql2` with TCP for persistent connections)
- Workloads requiring stored procedures, triggers, or events (Vitess does not support them)
- Applications requiring `LOAD DATA INFILE` (not supported)

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Connection Setup

The driver provides two connection methods: `connect()` for a single connection and `Client` for a connection factory. Use `Client` in serverless (fresh connection per request), `connect()` for single long-lived connection objects.

```typescript
import { connect } from "@planetscale/database";

const conn = connect({
  host: process.env.DATABASE_HOST!,
  username: process.env.DATABASE_USERNAME!,
  password: process.env.DATABASE_PASSWORD!,
});
const { rows } = await conn.execute(
  "SELECT id, name FROM users WHERE active = ?",
  [true],
);
```

See [examples/core.md](examples/core.md) for full connection patterns including `Client` factory, URL-based config, and custom fetch for HTTP/2.

---

### Pattern 2: Parameterized Queries

The driver supports positional (`?`) and named (`:param`) parameter styles. Both are auto-escaped preventing SQL injection. Never mix styles in a single `execute()` call.

```typescript
// Positional: array of values
await conn.execute("SELECT id, name FROM users WHERE id = ? AND active = ?", [
  userId,
  true,
]);

// Named: object of values
await conn.execute("SELECT id, name FROM users WHERE role = :role", {
  role: "admin",
});
```

See [examples/core.md](examples/core.md) for complex named parameter queries and bad examples to avoid.

---

### Pattern 3: Transactions

`conn.transaction()` executes multiple queries atomically with automatic rollback on error. Each `tx.execute()` is an HTTP round trip, but conditional logic runs client-side within the callback.

```typescript
const result = await conn.transaction(async (tx) => {
  const debit = await tx.execute(
    "UPDATE accounts SET balance = balance - ? WHERE id = ? AND balance >= ?",
    [amount, fromId, amount],
  );
  if (debit.rowsAffected === 0) throw new Error("Insufficient funds"); // triggers rollback
  await tx.execute("UPDATE accounts SET balance = balance + ? WHERE id = ?", [
    amount,
    toId,
  ]);
  return debit;
});
```

See [examples/core.md](examples/core.md) for full transaction examples with inventory checks and `FOR UPDATE` locking.

---

### Pattern 4: Custom Type Casting

The built-in `cast` handles INT8-32 and FLOAT32/64 automatically. Provide a custom `cast` for INT64/UINT64 (BigInt), DATETIME/TIMESTAMP (Date), and TINYINT(1) (boolean) -- these remain as strings by default.

```typescript
import { connect, cast } from "@planetscale/database";
import type { Field } from "@planetscale/database";

function customCast(field: Field, value: any): any {
  if (value == null) return null;
  if (field.type === "INT64" || field.type === "UINT64") return BigInt(value);
  if (field.type === "DATETIME" || field.type === "TIMESTAMP")
    return new Date(value + "Z");
  if (field.type === "INT8" && field.columnLength === 1) return value === "1";
  return cast(field, value);
}

const conn = connect({ url: process.env.DATABASE_URL, cast: customCast });
```

See [examples/core.md](examples/core.md) for per-query cast overrides and type-specific cast variants.

---

### Pattern 5: Deploy Request Workflow

Schema changes on production branches with safe migrations must go through deploy requests. Direct DDL is rejected. The workflow is: branch, modify schema, create deploy request, review diff, deploy.

```bash
pscale branch create my-database add-user-roles          # 1. Create dev branch
pscale shell my-database add-user-roles                  # 2. Make schema changes (DDL)
pscale deploy-request create my-database add-user-roles --into main  # 3. Create DR
pscale deploy-request diff my-database 1                 # 4. Review schema diff
pscale deploy-request deploy my-database 1               # 5. Deploy (online DDL)
pscale deploy-request revert my-database 1               # 6. Revert within 30 min if needed
```

See [examples/branching.md](examples/branching.md) for gated deployments, instant deployments, and CI/CD workflows.

---

### Pattern 6: Database Branching

Branches are isolated copies of your database schema. Development branches allow direct DDL. Production branches require deploy requests when safe migrations is enabled.

```bash
pscale branch create my-database dev-alice               # Create dev branch
pscale shell my-database dev-alice                       # Interactive MySQL shell
pscale password create my-database dev-alice my-password # Generate app credentials
pscale branch delete my-database dev-alice               # Clean up when done
```

See [examples/branching.md](examples/branching.md) for PR preview branches, safe column renames, FK setup, and branch cleanup scripts.

---

### Pattern 7: Vitess SQL Compatibility

PlanetScale runs on Vitess, which introduces SQL differences from standard MySQL. Key constraints: no stored procedures/triggers/events, no `RENAME COLUMN` (use three-step add/migrate/drop pattern), no `:=` operator, no `LOAD DATA INFILE`, no `CREATE DATABASE`.

See [reference.md](reference.md) for the full supported/unsupported SQL compatibility table.

</patterns>

---

<decision_framework>

## Decision Framework

### Connection Method

```
What is the runtime environment?
+-- Edge/serverless (Cloudflare Workers, Vercel Edge, etc.)
|   +-- Use @planetscale/database (HTTP-based, no TCP needed)
+-- Traditional Node.js server (always-on)
|   +-- Need PlanetScale branching/deploy workflow?
|   |   +-- YES --> @planetscale/database works fine (HTTP)
|   |   +-- NO --> mysql2 driver with TCP may be simpler
+-- ORM integration?
    +-- Check your ORM's docs for its PlanetScale/serverless adapter
```

### connect() vs Client

```
How many connections per process?
+-- Single connection (scripts, simple handlers) --> connect()
+-- Multiple connections (serverless, per-request) --> Client + client.connection()
```

### Schema Change Strategy

```
Is the target branch a production branch with safe migrations?
+-- YES --> Deploy requests ONLY (direct DDL is rejected)
|   +-- Simple change (add column, add index) --> Standard deploy request
|   +-- Needs controlled cutover timing --> Gated deployment (--disable-auto-apply)
|   +-- Instant-eligible change --> Deploy with --instant flag
+-- NO (development branch) --> Direct DDL is allowed
    +-- Experimenting --> pscale shell <db> <branch>
    +-- Scripted migration --> Connect to branch, run DDL
```

### Foreign Keys

```
Do you need foreign key constraints?
+-- YES --> Enable in database settings (opt-in)
|   +-- Aware of limitations?
|   |   +-- Deploy requests don't validate existing referential integrity
|   |   +-- Reverts can create orphaned rows
|   |   +-- Performance impact in high-concurrency workloads
|   +-- Sharded database? --> FK only supported on unsharded databases
+-- NO --> Use application-level referential integrity
    +-- ORM-level relationship definitions
    +-- Application validation before INSERT/DELETE
```

</decision_framework>

---

<red_flags>

## RED FLAGS

**High Priority Issues:**

- **String interpolation in SQL** -- `conn.execute(\`SELECT \* FROM users WHERE id = '${id}'\`)`bypasses parameterization. Always use`?`or`:param` placeholders with the params argument.
- **Direct DDL on production with safe migrations** -- `ALTER TABLE` statements are silently rejected on production branches with safe migrations enabled. All schema changes must go through deploy requests.
- **No custom cast for BigInt/Date columns** -- The default cast handles regular integers and floats, but INT64/UINT64 remain as strings and DATETIME/TIMESTAMP are not converted to Date objects. Provide a custom `cast` for these types.

**Medium Priority Issues:**

- **Reusing connections across serverless invocations** -- Each serverless invocation gets a fresh execution context. Do not store connection state in global variables expecting it to persist.
- **Using `RENAME COLUMN` in deploy requests** -- Column renames can be destructive through Vitess online DDL. Use the three-step pattern: add new column, migrate data, drop old column.
- **Missing revert window awareness** -- Deploy requests can be reverted within 30 minutes. After that window closes, you must create a new deploy request to undo changes. Plan accordingly.
- **Foreign keys enabled without understanding implications** -- FK constraints on PlanetScale don't validate existing referential integrity during `ALTER TABLE ADD FOREIGN KEY`. Orphaned rows will silently remain.

**Common Mistakes:**

- **Wrong package name** -- The package is `@planetscale/database`, not `planetscale`, `mysql-planetscale`, or `@planetscale/serverless`.
- **Expecting connection pooling in the driver** -- `@planetscale/database` does not do client-side connection pooling. PlanetScale handles pooling at the infrastructure level (Vitess VTTablet + Global Routing). Do not wrap it in a pool library.
- **Using positional and named params together** -- A single `execute()` call uses either `?` with an array OR `:param` with an object. Never mix them.
- **Expecting Node.js `mysql2` compatibility** -- `@planetscale/database` has a different API from `mysql2`. There is no `pool.query()`, no `connection.query()`. The API is `conn.execute(sql, params)`.
- **Running `CREATE DATABASE` or `DROP DATABASE`** -- Database creation/deletion is managed via the PlanetScale dashboard, API, or `pscale` CLI, not SQL.

**Gotchas & Edge Cases:**

- **INT64/UINT64 and dates remain as strings with the default cast** -- `SELECT count(*) as total` returns `{ total: 42 }` (INT64 is an exception -- it stays as `"42"` string). DATETIME returns `"2024-01-15 10:30:00"`. Regular INT32 and FLOAT types are auto-converted.
- **`rowsAffected` is 0 for SELECT** -- Only DML statements (INSERT, UPDATE, DELETE) populate `rowsAffected`. For SELECT, check `rows.length` or `size`.
- **`insertId` is a string** -- Even though MySQL auto-increment IDs are integers, `insertId` in the result is always a string. Cast if needed: `BigInt(result.insertId)`.
- **Transactions over HTTP are not interactive** -- Unlike traditional MySQL transactions, PlanetScale's HTTP transactions send all statements in a single request. You CAN use conditional logic within the `transaction()` callback (it runs client-side), but each `tx.execute()` is an HTTP round trip.
- **`DATETIME` values lack timezone** -- MySQL `DATETIME` is stored without timezone info. The driver returns it as a string like `"2024-01-15 10:30:00"`. Append `"Z"` when parsing as UTC, or handle timezone explicitly.
- **64KB query limit per execute** -- Individual SQL statements have a size limit. For bulk inserts, batch into multiple `execute()` calls.
- **SQL mode is session-only** -- `SET sql_mode = '...'` only lasts for the current connection. On PlanetScale's HTTP driver, that means a single request. Global SQL mode changes are not allowed.
- **PlanetScale Boost requires explicit opt-in** -- Boost query caching is available on Scaler Pro plans and above. Enable per-query via `@@boost_cached_queries = true` in a session `SET` before the boosted query. Not all queries are eligible.
- **Empty schemas are invalid** -- Production branches require at least one table. You cannot have an empty database on a production branch.
- **Instant deployments cannot be reverted** -- Using `--instant` on a deploy request uses MySQL's `ALGORITHM=INSTANT` and skips the revert window entirely.

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST use `conn.execute(sql, params)` with parameterized queries -- never interpolate user input into SQL strings)**

**(You MUST use deploy requests for ALL schema changes on production branches with safe migrations enabled -- direct DDL is rejected)**

**(You MUST create a fresh `Client.connection()` per request in serverless environments -- do not reuse connections across invocations)**

**(You MUST handle the Vitess/MySQL compatibility differences: no stored procedures, no `RENAME COLUMN` via direct DDL, no `:=` operator, no `LOAD DATA INFILE`)**

**(You MUST provide a custom `cast` function for BigInt (INT64/UINT64), Date (DATETIME/TIMESTAMP), and boolean (TINYINT(1)) columns -- the default cast handles regular integers and floats but leaves these as strings)**

**Failure to follow these rules will cause SQL injection vulnerabilities, failed deploy requests, or silent type coercion bugs.**

</critical_reminders>
