---
name: api-database-surrealdb
description: SurrealDB multi-model database - SurrealQL queries, record links, graph relations, live queries, schema definitions, authentication, TypeScript SDK
---

# SurrealDB Patterns

> **Quick Guide:** Use the `surrealdb` SDK (v2+) with `new Surreal()` and `connect()`. Model relationships with record links for simple pointers and `RELATE` for graph edges with metadata. Use `SCHEMAFULL` tables in production with `DEFINE FIELD` constraints. Always use parameterized queries (`$variable`) to prevent injection. Record IDs are `table:id` -- they are immutable and first-class values in SurrealQL. Live queries push changes without polling.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST use parameterized queries with `$variables` for ALL user input -- string interpolation in SurrealQL enables injection attacks)**

**(You MUST use `new RecordId("table", "id")` in SDK v2 -- plain `"table:id"` strings are NOT automatically parsed as record IDs)**

**(You MUST call `db.use({ namespace, database })` or pass namespace/database in `connect()` options BEFORE any queries -- queries without a selected namespace/database silently fail or error)**

**(You MUST NOT rely on `SCHEMALESS` tables in production -- use `SCHEMAFULL` with `DEFINE FIELD` to enforce data integrity at the database layer)**

**(You MUST NOT use `UPDATE`/`DELETE` with `WHERE` on large tables without indexes -- SurrealDB currently does not use indexes for UPDATE/DELETE WHERE clauses (use subquery workaround))**

</critical_requirements>

---

**Auto-detection:** SurrealDB, Surreal, surrealdb, SurrealQL, RELATE, RecordId, record link, LIVE SELECT, SCHEMAFULL, SCHEMALESS, DEFINE TABLE, DEFINE FIELD, DEFINE ACCESS, surql, graph traversal, ->relation->, <-relation<-

**When to use:**

- Connecting to SurrealDB and executing queries via the JavaScript SDK
- Modeling data with record links and graph edges (`RELATE`)
- Defining schemas with `SCHEMAFULL` tables and field constraints
- Building real-time features with live queries
- Implementing authentication with `DEFINE ACCESS` and record-level permissions
- Multi-tenant architectures using namespaces and databases

**Key patterns covered:**

- SDK connection setup (v2 API with `Surreal`, `connect`, `RecordId`, `Table`)
- CRUD operations with type-safe queries
- Record links vs graph edges (when to use each)
- Schema definitions (`DEFINE TABLE`, `DEFINE FIELD`, permissions)
- Live queries for real-time subscriptions

**When NOT to use:**

- Heavy analytical/OLAP workloads (use a columnar database)
- Simple key-value caching (use a dedicated cache)
- Mature relational schemas that require decades of SQL ecosystem tooling

**Detailed Resources:**

- For decision frameworks and anti-patterns, see [reference.md](reference.md)

**Core Patterns:**

- [examples/core.md](examples/core.md) - SDK setup, connection, CRUD, TypeScript typing, RecordId

**Graph & Relations:**

- [examples/graph-relations.md](examples/graph-relations.md) - Record links, RELATE, graph traversal, edge metadata

**Schema & Auth:**

- [examples/schema-auth.md](examples/schema-auth.md) - DEFINE TABLE/FIELD, SCHEMAFULL, permissions, DEFINE ACCESS, authentication

**Live Queries & Transactions:**

- [examples/live-queries.md](examples/live-queries.md) - LIVE SELECT, subscriptions, transactions, events

---

<philosophy>

## Philosophy

SurrealDB is a multi-model database combining document, graph, and relational paradigms with a SQL-inspired query language (SurrealQL). The core principle: **model your data the way you think about it -- records link to records, relationships carry metadata, and schemas enforce integrity without separate migration tools.**

**Core principles:**

1. **Record IDs are first-class** -- Every record has a `table:id` identity that doubles as a direct pointer. SurrealDB fetches linked records from disk without table scans.
2. **Graph when you need metadata, link when you don't** -- Record links (`friends = [person:tobie]`) are lightweight pointers. Graph edges (`RELATE person:a->follows->person:b`) store relationship context (timestamps, weights, roles).
3. **Schema-full for production** -- `SCHEMAFULL` tables with `DEFINE FIELD` constraints enforce types, validation, and defaults at the database layer. Use `SCHEMALESS` only for rapid prototyping.
4. **Permissions at every level** -- Namespace, database, table, and field-level permissions. `DEFINE ACCESS` with `SIGNUP`/`SIGNIN` enables end-user authentication without a separate auth service.
5. **Real-time by default** -- `LIVE SELECT` pushes changes to subscribers as they commit. No polling, no message broker.
6. **Parameterize everything** -- SurrealQL variables (`$email`, `$limit`) prevent injection and improve query plan caching.

**When to use SurrealDB:**

- Applications needing both document flexibility and graph traversal
- Multi-tenant SaaS (namespace/database isolation)
- Real-time collaborative features (live queries)
- Social graphs, recommendation engines, knowledge graphs
- Projects wanting database-level auth without a separate auth service

**When NOT to use:**

- Heavy OLAP/analytics (use a columnar warehouse)
- Legacy systems requiring strict SQL standard compliance
- Simple key-value workloads (use a dedicated KV store)
- Workloads requiring battle-tested ORMs with decades of ecosystem

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: SDK Connection

Establish connection with namespace and database selection. SDK v2 uses `new Surreal()` with engine configuration.

```typescript
import Surreal from "surrealdb";
import { RecordId, Table } from "surrealdb";

const db = new Surreal();

await db.connect("http://127.0.0.1:8000", {
  namespace: "myapp",
  database: "production",
});

// Authenticate as root (development only)
await db.signin({
  username: "root",
  password: "root",
});

export { db };
```

**Why good:** Uses `127.0.0.1` (not `localhost`), namespace/database set at connection, explicit root signin separated from connection

```typescript
// BAD: Missing namespace/database, string interpolation for credentials
const db = new Surreal();
await db.connect("http://localhost:8000");
await db.query(`SIGNIN AS user:${username} PASSWORD '${password}'`);
```

**Why bad:** No namespace/database selection causes silent failures, `localhost` can fail with IPv6, string interpolation enables injection, credentials should use `signin()` method

---

### Pattern 2: CRUD with RecordId

SDK v2 requires `RecordId` objects for record identification -- plain strings are not automatically parsed.

```typescript
import Surreal, { RecordId, Table } from "surrealdb";

interface User {
  id: RecordId;
  name: string;
  email: string;
  role: "admin" | "user";
}

// Create with auto-generated ID
const created = await db.create<User>(new Table("user"), {
  name: "Alice",
  email: "alice@example.com",
  role: "user",
});

// Create with specific ID
const specific = await db.create<User>(new RecordId("user", "alice"), {
  name: "Alice",
  email: "alice@example.com",
  role: "admin",
});

// Select by ID
const user = await db.select<User>(new RecordId("user", "alice"));

// Partial update (merge)
await db.merge(new RecordId("user", "alice"), {
  role: "admin",
});
// Or chainable: await db.update(new RecordId("user", "alice")).merge({ role: "admin" });

// Delete
await db.delete(new RecordId("user", "alice"));
```

**Why good:** `RecordId` objects for type-safe record access, TypeScript generics for return type, `merge()` for partial update (or chainable `update().merge()`), `Table` for table-scoped operations

```typescript
// BAD: Using plain strings as record IDs
const user = await db.select("user:alice"); // v2 does not auto-parse
await db.query(`DELETE user:${userId}`); // Injection risk
```

**Why bad:** SDK v2 requires `RecordId` objects (plain strings not auto-parsed), string interpolation in queries enables injection

---

### Pattern 3: Parameterized Queries

Always bind user input as parameters. SurrealQL parameters use `$name` syntax.

```typescript
const PAGE_SIZE = 20;
const MIN_AGE = 18;

// Parameterized query -- safe from injection
const users = await db.query<[User[]]>(
  `SELECT * FROM user WHERE age >= $min_age AND role = $role ORDER BY name LIMIT $limit`,
  { min_age: MIN_AGE, role: "admin", limit: PAGE_SIZE },
);

// Multiple statements return tuple of results
const [users2, count] = await db.query<[User[], [{ count: number }]]>(
  `SELECT * FROM user WHERE active = true LIMIT $limit;
   SELECT count() AS count FROM user WHERE active = true GROUP ALL;`,
  { limit: PAGE_SIZE },
);

// Parameterized record ID lookup
const record = await db.query<[User[]]>(`SELECT * FROM $record_id`, {
  record_id: new RecordId("user", "alice"),
});
```

**Why good:** Named constants for all numeric values, parameters prevent injection, tuple typing for multi-statement queries, `RecordId` used even in parameterized queries

```typescript
// BAD: String interpolation with user input
const users = await db.query(`SELECT * FROM user WHERE email = '${userInput}'`);
```

**Why bad:** Direct string interpolation enables SurrealQL injection -- attacker can escape string and execute arbitrary queries

---

### Pattern 4: Record Links (Lightweight Pointers)

Record links are direct field-level pointers to other records. SurrealDB fetches linked records via dot notation without explicit JOINs.

```typescript
// Create records with record link fields
await db.query(`
  CREATE person:alice SET
    name = "Alice",
    best_friend = person:bob,
    friends = [person:bob, person:carol];
`);

// Dot notation traverses links automatically
const result = await db.query<[{ name: string; friend_name: string }[]]>(
  `SELECT name, best_friend.name AS friend_name FROM person:alice`,
);

// Multi-level traversal
const deep = await db.query<[{ fof: string[] }[]]>(
  `SELECT friends.friends.name AS fof FROM person:alice`,
);
```

**Why good:** Record links are direct disk lookups (no table scan), dot notation traverses links transparently, multi-level traversal in a single query

**When to use:** Simple, unidirectional references without relationship metadata (author of a post, parent category, user preferences).

**When not to use:** When you need relationship metadata (timestamps, weights), bidirectional traversal, or relationship-level permissions. Use graph edges instead.

---

### Pattern 5: Graph Edges with RELATE

Graph edges are full records in a relation table, created with `RELATE`. They support metadata, bidirectional traversal, and schema constraints.

```typescript
// Create a graph edge with metadata
await db.query(`
  RELATE person:alice->follows->person:bob
    SET followed_at = time::now(), strength = "close";
`);

// Forward traversal: who does Alice follow?
const following = await db.query<[{ following: string[] }[]]>(
  `SELECT ->follows->person.name AS following FROM person:alice`,
);

// Reverse traversal: who follows Bob?
const followers = await db.query<[{ followers: string[] }[]]>(
  `SELECT <-follows<-person.name AS followers FROM person:bob`,
);

// Edge metadata query
const edges = await db.query<
  [{ in: RecordId; out: RecordId; strength: string }[]]
>(`SELECT in, out, strength FROM follows WHERE out = person:bob`);

// Bidirectional (undirected) traversal
const friends = await db.query<[{ friends: string[] }[]]>(
  `SELECT <->knows<->person.name AS friends FROM person:alice`,
);
```

**Why good:** `RELATE` creates typed edges with metadata, forward/reverse/bidirectional traversal syntax, edges are queryable records themselves

**When to use:** Relationships needing metadata (followed_at, role, weight), bidirectional queries, social graphs, access control graphs.

</patterns>

---

<red_flags>

## RED FLAGS

**High Priority Issues:**

- Using string interpolation instead of `$parameters` in SurrealQL queries -- enables injection attacks
- Using `"table:id"` strings instead of `new RecordId("table", "id")` in SDK v2 -- strings are not auto-parsed as record IDs
- Running queries without selecting namespace/database -- queries silently fail or return errors
- Using `SCHEMALESS` tables in production without explicit field definitions -- data integrity not enforced

**Medium Priority Issues:**

- `UPDATE table SET ... WHERE condition` on large tables without indexes -- SurrealDB does not use indexes for UPDATE/DELETE WHERE (use `UPDATE (SELECT id FROM table WHERE condition) SET ...` as workaround)
- Using `UPSERT` without a unique index -- `UPSERT` is much more performant with unique indexes (avoids table scan)
- Embedding unbounded arrays as record links -- arrays can grow without limit; use graph edges for unbounded relationships
- Not setting `DURATION FOR TOKEN` and `DURATION FOR SESSION` on `DEFINE ACCESS` -- tokens/sessions without expiry are a security risk

**Common Mistakes:**

- Creating duplicate record IDs silently fails or errors depending on context -- use `INSERT ... ON DUPLICATE KEY UPDATE` or `UPSERT` for idempotent operations
- Expecting `record:id` strings to sort numerically -- `record:1`, `record:10`, `record:2` sorts lexicographically; use numeric IDs (`record:1`, `record:2`, `record:10`) or ULID/UUID for temporal sorting
- Forgetting that record IDs are immutable -- you cannot change a record's ID after creation; you must create a new record and delete the old one
- Using `rand()`, `ulid()`, or `uuid()` in `DEFINE FUNCTION` bodies -- these generate the same value per function call, causing duplicate key errors on subsequent calls
- Confusing `DEFINE FIELD ... VALUE` (recalculated on create/update) with `DEFINE FIELD ... COMPUTED` (recalculated on access, v3.0+)
- Setting `id` field in `CREATE table:specific_id SET id = "other"` -- the explicit record ID takes precedence and the `id` in SET is silently discarded

**Gotchas & Edge Cases:**

- Fields defined with `VALUE` are recalculated alphabetically -- if field `b` depends on field `a`, naming matters
- `FLEXIBLE TYPE` on a `SCHEMAFULL` table allows schemaless nested objects -- useful for JSON metadata but bypasses type checking on that subtree
- `LIVE SELECT` with complex `WHERE` filters may not fire for all edge cases -- test your filters thoroughly
- `localhost` in connection strings can fail on Node.js 18+ due to IPv6 preference -- use `127.0.0.1`
- Numeric string IDs (`"10"`) display as backtick-escaped (`table:\`10\``) to differentiate from numeric IDs (`table:10`)
- Record References (`DEFINE FIELD ... REFERENCE`) are experimental (require `--allow-experimental record_references`) -- do not use in production

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST use parameterized queries with `$variables` for ALL user input -- string interpolation in SurrealQL enables injection attacks)**

**(You MUST use `new RecordId("table", "id")` in SDK v2 -- plain `"table:id"` strings are NOT automatically parsed as record IDs)**

**(You MUST call `db.use({ namespace, database })` or pass namespace/database in `connect()` options BEFORE any queries -- queries without a selected namespace/database silently fail or error)**

**(You MUST NOT rely on `SCHEMALESS` tables in production -- use `SCHEMAFULL` with `DEFINE FIELD` to enforce data integrity at the database layer)**

**(You MUST NOT use `UPDATE`/`DELETE` with `WHERE` on large tables without indexes -- SurrealDB currently does not use indexes for UPDATE/DELETE WHERE clauses (use subquery workaround))**

**Failure to follow these rules will cause injection vulnerabilities, silent query failures, or data integrity issues.**

</critical_reminders>
