---
name: software-database-design
description: "Designs database schemas, migrations, and data models for PostgreSQL, MySQL, MongoDB, and Redis. Use when planning tables, relationships, indexes, or ORM-backed schema changes."
compatibility: Portable core. Works on Claude Code and Codex.
version: "1.2"
last_validated: 2026-07-11
---

# Database Design

Schema design, data modeling, migration safety, and ORM patterns. This skill covers structural decisions — what tables exist, how they relate, how schemas evolve. For tuning queries on an existing schema, use `data-sql-optimization`.

## Quick Reference

| Task | Default Picks | Notes |
|------|---------------|-------|
| Relational database | PostgreSQL 18 | Transactions, complex queries, JSON support, native `uuidv7()`, async I/O |
| Relational (MySQL family) | MySQL 8.4 LTS | 8.0 reached EOL (Apr 2026); 8.4 is the LTS migration target, 9.x is the quarterly innovation train |
| Embedded / edge relational | SQLite 3.5x | Current release train moves fast (monthly point releases); pin a version, don't chase latest blindly |
| Flexible schema | MongoDB 8.x | Rapid iteration, embedded relationships |
| Caching / sessions | Redis | Ephemeral data, counters, pub/sub |
| Graph traversals | Neo4j | Relationship-heavy queries (social, fraud) |
| Time-series | TimescaleDB, InfluxDB | Metrics, IoT, event streams |
| Managed app backend | [../software-baas-platforms/SKILL.md](../software-baas-platforms/SKILL.md) | Use when auth, realtime, storage, and functions are part of the platform choice |
| Schema migrations | expand-contract pattern | Zero-downtime changes |
| ORM | Prisma, Drizzle, SQLAlchemy, EF Core | Match stack; review generated SQL |
| Vector similarity | pgvector (co-located with PostgreSQL) | HNSW is the default index for new work; see `ai-vector-brain` for implementation depth |

## When to Use This Skill

- Design table/collection schemas and normalization strategies
- Model relationships (1:N, M:N, polymorphic associations)
- Plan zero-downtime migrations (expand-contract)
- Define indexing strategies based on access patterns
- Configure ORMs and avoid common anti-patterns
- Choose between relational, document, key-value, and graph databases

## When NOT to Use This Skill

| Problem | Go here |
|---------|---------|
| Query optimization on existing schemas | [data-sql-optimization](../data-sql-optimization/SKILL.md) |
| Backend service implementation | [software-backend](../software-backend/SKILL.md) |
| Managed app backend platform (Supabase, Convex, Firebase, Appwrite, PocketBase) | [software-baas-platforms](../software-baas-platforms/SKILL.md) |
| SwiftData/Core Data schemas mirrored to CloudKit | [software-ios-native](../software-ios-native/SKILL.md) |
| On-device iOS semantic/vector retrieval | [software-ios-ai-engine](../software-ios-ai-engine/SKILL.md) |
| Data lake or warehouse architecture | [data-lake-platform](../data-lake-platform/SKILL.md) |
| Streaming or real-time pipelines | [data-streaming](../data-streaming/SKILL.md) |
| System-level data architecture decisions | [software-architecture-design](../software-architecture-design/SKILL.md) |

## ASCII Flow

```text
Database design request
  -> Define entities, access patterns, integrity, and migration constraints
  -> Route tuning, backend, or lakehouse work when schema design is not central
  -> Choose model, normalization stance, indexes, and migration path
  -> Verify engine-specific behavior from references
  -> Return schema guidance with validation and rollout risks
```

## Workflow

1. Define the entities, access patterns, integrity constraints, and migration constraints first.
2. Route query tuning, backend implementation, or lakehouse design to the adjacent skill when schema design is not the real problem.
3. Choose the data model and normalization stance from the decision tree.
4. Apply the migration, indexing, and ORM guidance needed for the target stack.
5. Validate current engine-specific behavior with the navigation references before final recommendations.

## Decision Tree

```text
1) Identify entities and their relationships
2) Choose data model:
   - Relational (PostgreSQL, MySQL) for structured data with complex joins
   - Document (MongoDB) for flexible schemas with embedded relationships
   - Key-value (Redis) for caching, sessions, counters
   - Graph (Neo4j) for relationship-heavy traversals (depth > 3 hops)
3) Normalize to 3NF by default; denormalize with justification
4) Define primary keys, foreign keys, and constraints
5) Plan indexing strategy based on access patterns
6) Design migration path (can it be applied with zero downtime?)
```

For the full relational vs. graph vs. vector decision matrix, see [references/storage-paradigm-selection.md](references/storage-paradigm-selection.md).

## Normalization Decision Table

| Situation | Approach | Rationale |
|-----------|----------|-----------|
| Transactional data (orders, users) | Normalize to 3NF | Data integrity, reduce anomalies |
| Read-heavy dashboards | Denormalize or materialized views | Query performance |
| Audit logs | Append-only, denormalized | Immutability, query speed |
| User preferences/settings | JSON column or document | Flexible schema, rarely joined |
| Hierarchical data (categories, org charts) | Adjacency list or materialized path | Query pattern determines choice |
| Many-to-many with attributes | Junction table with columns | Clean modeling |

**When to stop normalizing.** 3NF is a starting default, not a finish line to chase past the point of diminishing returns. Stop and denormalize (or never split further) when: a join is on the hot path of a request that needs single-digit-millisecond latency and the joined table rarely changes independently; the "normalized" shape only exists to satisfy theory and every real query re-joins the same two tables anyway (that's a sign they should be one table, or the second table should hold a cached copy of the field with an explicit invalidation path); or the entity has no independent lifecycle, cardinality, or access pattern of its own (e.g., splitting `users` and `user_profile` 1:1 for no reason but "it felt cleaner" — that's schema for its own sake, not for a query it serves). Denormalization is a performance or availability decision, not a modeling default — it needs a name (materialized view, cache column, read replica) and an owner who knows it can drift.

**The "one big table + JSON" failure mode.** Storing most of an entity's real, frequently-queried attributes in a single `jsonb`/JSON column on one giant table is not flexibility, it's giving up on the schema. Watch for: no query planner statistics on inner keys (every filter is a sequential scan unless you add expression indexes per key, at which point you've built a shadow schema anyway); no foreign-key integrity on IDs embedded in the JSON; every read paying JSON parse/serialize cost for fields used in `WHERE`; and migrations becoming "read every row, rewrite the blob" scripts instead of `ALTER TABLE`. The boundary: a JSON column is fine for genuinely variable, rarely-filtered, rarely-joined data (user preferences, webhook payloads, feature-flag overrides). The moment you query, filter, sort, aggregate, or join on more than 2-3 of its inner keys regularly, promote those keys to real columns — you can keep the rest of the variable payload in a smaller JSON column alongside them. This is a spectrum, not a binary; the mistake is never revisiting the decision as access patterns solidify.

## Migration Safety Checklist

- [ ] Migration runs while the application serves traffic
- [ ] No long-held table locks on large tables (`CREATE INDEX CONCURRENTLY` in PostgreSQL; every plain `ALTER TABLE` still takes `ACCESS EXCLUSIVE` briefly, so what matters is lock *duration*, not avoiding the lock entirely)
- [ ] New columns are nullable, or have a constant default (metadata-only since Postgres 11 — no table rewrite), or a volatile/expression default (this one *does* rewrite the table and holds `ACCESS EXCLUSIVE` for the duration — treat as high-risk)
- [ ] Schema change is backward-compatible with current application code
- [ ] Rollback plan exists (reverse migration or expand-contract)
- [ ] Data backfill runs as a separate step, not inside the migration
- [ ] Migration tested against production-sized dataset
- [ ] Foreign key constraints added after data is consistent

## Zero-Downtime Migration Pattern (Expand-Contract)

```text
Phase 1: EXPAND
  - Add new column/table (nullable, no constraints yet)
  - Deploy app code that writes to both old and new
  - Backfill existing data into new structure

Phase 2: MIGRATE
  - Deploy app code that reads from new structure
  - Verify data consistency between old and new
  - Add constraints and indexes on new structure

Phase 3: CONTRACT
  - Deploy app code that only uses new structure
  - Remove old column/table in a follow-up migration
  - Each phase is a separate deployment — never combine
```

## Indexing Strategy

| Access Pattern | Index Type | Example |
|---------------|------------|---------|
| Exact lookup | B-tree (default) | `WHERE email = ?` |
| Range queries | B-tree | `WHERE created_at > ?` |
| Full-text search | GIN + tsvector (PG) / FULLTEXT (MySQL) | `WHERE search @@ to_tsquery(?)` |
| JSON field queries | GIN (PG) | `WHERE metadata @> '{"key": "val"}'` |
| Geospatial | GiST or SP-GiST | `WHERE ST_DWithin(location, ?, 1000)` |
| Composite lookups | Multi-column B-tree | `WHERE tenant_id = ? AND status = ?` |
| Uniqueness enforcement | Unique index | `CREATE UNIQUE INDEX ON users(email)` |
| Partial indexing | Filtered index | `WHERE deleted_at IS NULL` |
| Large append-only / naturally ordered columns | BRIN (PG) | `WHERE created_at BETWEEN ? AND ?` on a table physically clustered by insert order (time-series, event logs) |

### Indexing Rules

- [ ] Index columns that appear in WHERE, JOIN ON, and ORDER BY
- [ ] Put high-cardinality columns first in composite indexes
- [ ] Use partial indexes to exclude soft-deleted rows
- [ ] Avoid indexing columns with fewer than 100 distinct values (unless composite)
- [ ] Monitor unused indexes and drop them (they slow writes)
- [ ] Prefer covering indexes for hot queries (include all SELECT columns)
- [ ] Reach for BRIN only when the column correlates with physical row order (e.g. an append-only `created_at`); BRIN is a lossy, block-range summary — a few bytes per range vs. a full B-tree entry per row — and degrades badly the moment the table is updated out of insertion order (e.g. `UPDATE`-heavy tables, or reordering from `VACUUM FULL`/`CLUSTER`)
- [ ] On PostgreSQL, keep `fillfactor` below 100 on frequently-`UPDATE`d tables (e.g. 90) so updates that don't touch indexed columns can use HOT (Heap-Only Tuple) updates — they skip index maintenance entirely and are the single biggest lever against index bloat on write-heavy tables
- [ ] Don't reach for GIN/GiST on a hunch — profile the actual query first; a well-designed B-tree composite index outperforms both for exact-match and range lookups, and GIN write overhead is real on high-churn `jsonb`/array columns

## ORM Patterns

| Pattern | When | Example |
|---------|------|---------|
| Repository pattern | Isolate data access from business logic | `UserRepository.findByEmail()` |
| Unit of Work | Batch multiple changes into one transaction | EF Core `SaveChanges()`, SQLAlchemy `session.commit()` |
| Lazy loading | Relationships rarely accessed | Default in most ORMs |
| Eager loading | N+1 query prevention | `.Include()` (EF), `.joinedload()` (SA), `.populate()` (Mongoose) |
| Raw SQL escape hatch | Complex queries ORMs model poorly | Window functions, recursive CTEs |

### ORM Anti-Patterns

| Avoid | Problem | Do Instead |
|-------|---------|------------|
| N+1 queries | Loading related entities in a loop | Use eager loading or batch queries |
| Fat models with business logic | Couples domain logic to persistence | Separate domain and data layers |
| Ignoring generated SQL | ORM produces inefficient queries | Log and review SQL in development |
| Using ORM for bulk operations | Row-by-row processing is slow | Use bulk insert/update or raw SQL |
| Mapping every table to an entity | Over-abstraction | Use raw queries for reports and analytics |

## Technology Selection

| Need | Best fit | Avoid |
|------|----------|-------|
| Transactions + complex queries | PostgreSQL | MongoDB (limited multi-collection ACID) |
| Flexible schema, rapid iteration | MongoDB | Relational with heavy ALTER TABLE |
| Caching, sessions, counters | Redis | Relational (too heavy for ephemeral data) |
| Relationship traversals (social, fraud) | Neo4j / graph | Relational with recursive self-joins |
| Time-series metrics | TimescaleDB, InfluxDB | Generic relational |
| Full-text search (primary use case) | Elasticsearch / OpenSearch | Relational LIKE queries |

## Partitioning Decision Gates

Partitioning is an operational tool (faster maintenance, cheap bulk-drop of old data, partition pruning on scans) — it is not a performance feature you reach for because a table "feels big." Gate it on real, measured signals:

| Signal | Partition? | Rationale |
|--------|-----------|-----------|
| Table exceeds a few hundred GB, or `VACUUM`/`REINDEX`/backup on it now takes hours | Yes | Maintenance ops scale per-partition, not per-table |
| Retention policy drops data older than N (days/months) on a schedule | Yes | `DROP PARTITION` is instant; `DELETE FROM ... WHERE created_at < ?` on a monolith is a slow, bloat-generating scan |
| Nearly every query filters on the same column you'd partition by (e.g. `tenant_id`, `created_at`) | Yes | Partition pruning turns a full scan into a scan of 1-2 partitions |
| Table is a few tens of GB and queries don't consistently filter on a single candidate key | No | Partitioning adds DDL complexity (per-partition indexes/constraints, cross-partition unique constraints need the partition key in the key) for no query win — a good composite index solves it cheaper |
| The real problem is a missing index or stale statistics | No | Check `EXPLAIN ANALYZE` before reaching for partitioning; it's a common (and expensive) way to avoid diagnosing the actual query plan |

Default to PostgreSQL declarative range or list partitioning on the field the retention/access pattern demands; hash-partition only to spread write load evenly with no natural range/list key. Re-verify current limits (partition count, unique-constraint requirements) against the target major version's docs before committing to a scheme — these have loosened across recent PostgreSQL releases.

## Connection Pooling & Schema Design

Schema and migration choices interact with the connection pooler, not just the database engine — this is easy to miss because it only bites under load:

- **Transaction-mode pooling (PgBouncer, Supavisor, RDS Proxy) breaks session-scoped state.** `SET search_path`, session-level advisory locks, `LISTEN/NOTIFY`, and temp tables don't reliably survive between statements in the same logical transaction if the pool reassigns the underlying connection. Design multi-tenant schema-per-tenant systems to schema-qualify every reference explicitly rather than relying on `search_path` switching per request under a pooled connection.
- **Prepared statements and transaction pooling used to be mutually exclusive**; PgBouncer 1.21+ supports prepared statements in transaction mode via `max_prepared_statements`, but confirm the pooler version and setting before assuming an ORM's prepared-statement cache is safe under pooling — older poolers or misconfigured settings silently fall back to unprepared (slower) execution or error.
- **Schema-per-tenant multiplies pooled connection overhead.** Every additional schema is additional catalog metadata pooled connections must resolve; at a few thousand schemas, `search_path`-per-request switching plus catalog bloat becomes a measurable tax. This is one more reason shared-schema-with-RLS scales further than schema-per-tenant for most SaaS (see Scenario S1).
- **Migrations that use session-level `SET` (e.g. `SET statement_timeout`, `SET lock_timeout`) need it re-applied per pooled connection**, not assumed to persist — run migrations through a direct (non-pooled) connection, not through the application's pooled path.

## Known Traps

- Adding `NOT NULL`, uniqueness, or foreign-key constraints before a data cleanup and backfill plan exists.
- Treating a nullable "temporary" column or JSON blob as a harmless stopgap — it becomes permanent schema debt.
- Planning partitioning, sharding, or exotic indexes before real access patterns and retention rules are measured — see the Partitioning Decision Gates above.
- Rolling out schema changes in an order that breaks mixed-version application deployments during blue/green or rolling releases.
- Assuming ORM migration generators understand operational rollout safety without a manual expand-contract review.
- Storing vector embeddings in a sidecar collection when the source documents already live in MongoDB — forces `$lookup` on every retrieval and creates a consistency surface that breaks under partial failures.
- Mixing embedding dimensions or models in a single Atlas Vector Search index — breaks `$vectorSearch` silently or returns nonsense neighbours.
- Skipping the tenant filter in `$vectorSearch` for multi-tenant agents — vectors leak across tenants because ANN ignores schema-level isolation.
- **Graph: Cartesian-product Cypher** — `MATCH (a:Foo), (b:Bar)` with no connecting pattern produces N×M traversals; always anchor MATCH clauses with an edge pattern or use `WITH` to chain bounded subqueries.
- **Graph: Relying on Neo4j internal node IDs as external references** — IDs are file offsets, get reused after deletion; use an explicit UUID property as the stable identifier.
- **Vector: stale reads under eventual-consistency search engines** — Weaviate (and similar) can return docs updated seconds ago; test the read-your-writes path explicitly.

## Anti-Patterns

| Avoid | Do Instead |
|-------|------------|
| EAV (Entity-Attribute-Value) tables | JSON columns or document store |
| Storing money as floats | Use DECIMAL / NUMERIC or integer cents |
| Soft deletes everywhere | Use only when audit trail required; otherwise hard delete |
| UUID v4 as clustered primary key | UUID v7 (RFC 9562; time-ordered, `uuidv7()` built in as of Postgres 18) or `BIGINT GENERATED ALWAYS AS IDENTITY` |
| Storing files in the database | Store in object storage; keep metadata/URL in DB |
| No foreign keys "for performance" | FK constraints prevent data corruption; index the FK column |
| One migration per PR with schema + data | Separate schema migration from data backfill |
| Graph: indexing every property on every label | Index only properties used in `WHERE`/`MATCH` lookup positions |
| Graph: generic relationship types (`CONNECTED_TO`, `RELATED`) | Use specific typed edges (`FOLLOWS`, `OWNS`, `REPORTS_TO`) |

**Primary key choice is a real trade-off, not dogma.** A `bigint` is 8 bytes vs. 16 for any UUID, so it halves index-entry size and — because it's monotonic — every insert lands at the right edge of the B-tree instead of a random point, avoiding the page splits and bloat that random UUIDv4 inserts cause. Default to `BIGINT GENERATED ALWAYS AS IDENTITY` when a single database owns ID generation and nothing outside it needs to mint or merge IDs. Move to UUIDv7 the moment you need client-side or multi-service ID generation, cross-shard merges, or IDs created before the row reaches the database — UUIDv7's time-ordered layout gets you most of `bigint`'s insert locality back (unlike UUIDv4) while keeping those properties. One trade-off UUIDv7 doesn't remove: the leading 48 bits are a millisecond Unix timestamp, so anyone holding a UUIDv7 can decode approximately when the row was created (and infer creation rate from a handful of IDs) — treat that as a minor information leak if row-creation time is sensitive, not a blocker.

## Scenarios

### S1 — Multi-tenant schema: shared vs schema-per-tenant

1. Enumerate isolation requirements: compliance, data residency, noisy-neighbor risk, and restore granularity.
2. Use **shared schema with `tenant_id`** for most SaaS products; simpler migrations (one DDL run, not N), lower infra cost, RLS handles access control. This is the right default up to thousands of tenants.
3. Use **schema-per-tenant** only when strict data isolation is a legal requirement (e.g. contractual/regulatory data segregation a customer will audit) or tenants need independent point-in-time restore. Weigh the real cost: migrations must run once per schema (a single DDL bug becomes an N-schema incident), connection poolers pay a per-schema catalog-resolution tax that becomes measurable in the low thousands of schemas (see Connection Pooling & Schema Design above), and most managed Postgres offerings soft-cap comfortable schema counts well below "one per tenant" for a large consumer-scale SaaS. Schema-per-tenant fits dozens-to-low-hundreds of large/regulated tenants, not thousands of small ones.
4. For shared schema: add `tenant_id` to every data table, enable RLS, and add a composite index `(tenant_id, id)` on high-traffic tables.
5. Verify a new tenant row produces correct RLS visibility in a CI integration test.

### S2 — Postgres expand-contract migration with online backfill

1. **Expand**: add the new column as `nullable` with no constraints; deploy app code that writes to both old and new columns.
2. Run the backfill as a separate, rate-limited background job — not inside the migration transaction; verify row counts before and after.
3. **Migrate**: deploy app code that reads from the new column; run `CREATE INDEX CONCURRENTLY` on the new column.
4. Add `NOT NULL` + constraints only after backfill is complete. On Postgres 12+, avoid the full-table-scan validation: first add `CHECK (col IS NOT NULL) NOT VALID` (instant, no scan), then `VALIDATE CONSTRAINT` in a separate statement (`SHARE UPDATE EXCLUSIVE` lock only, concurrent writes proceed), then `SET NOT NULL` (Postgres uses the validated constraint and skips its own scan).
5. **Contract**: deploy app code that drops the old column path; remove the old column in a follow-up migration after one release cycle.

### S3 — Index design for high-cardinality lookup

1. Identify the exact `WHERE`, `JOIN ON`, and `ORDER BY` clauses from the query plan (`EXPLAIN ANALYZE`).
2. Put the highest-cardinality column first in a composite index; add low-cardinality filter columns after.
3. Use a partial index to exclude soft-deleted or inactive rows: `WHERE deleted_at IS NULL`.
4. Use a covering index (`INCLUDE (col)`) to avoid a heap fetch on hot queries.
5. Run `CREATE INDEX CONCURRENTLY` on production; monitor `pg_stat_user_indexes` for unused indexes and drop them.

### S4 — Soft-delete vs row archival

1. Use soft delete (`deleted_at TIMESTAMP`) only when you need a recovery window or audit trail.
2. Add a partial index `WHERE deleted_at IS NULL`; exclude deleted rows from all ORM default scopes.
3. For large tables, archive rows older than N days to an archive table on a schedule.
4. When audit trail is the primary need, prefer an append-only audit log table — hard-delete the operational row, keep the event.
5. Verify that all `COUNT`, aggregate, and join queries explicitly filter `deleted_at IS NULL`; add a lint rule or ORM default scope to enforce it.

### S5 — JSONB column versioning

1. Add a `schema_version INT DEFAULT 1` column alongside the JSONB column.
2. On read, branch on `schema_version` and normalize older shapes in the application layer.
3. Run a one-time backfill migration upgrading all `schema_version = 1` rows; rate-limit to avoid lock contention.
4. After backfill, add a `CHECK (schema_version = 2)` constraint and drop the normalization branch.
5. Add a GIN index on the JSONB column for fields queried with `@>` or `->>`operators.

### S6 — MongoDB Atlas as context layer for AI agents

Full pattern (collection topology, vector index, memory schema, operational checklist): see [references/mongodb-atlas-ai-context.md](references/mongodb-atlas-ai-context.md).

## Navigation

### References

- [schema-design-patterns.md](references/schema-design-patterns.md) — Common schema patterns (polymorphic, multi-tenant, audit trails)
- [migration-strategies.md](references/migration-strategies.md) — Zero-downtime migrations, expand-contract, blue-green data
- [orm-framework-guide.md](references/orm-framework-guide.md) — EF Core, SQLAlchemy, Prisma, Drizzle, Mongoose patterns
- [nosql-modeling.md](references/nosql-modeling.md) — Document, key-value, and graph modeling patterns
- [storage-paradigm-selection.md](references/storage-paradigm-selection.md) — Relational vs. graph vs. vector decision matrix and common polyglot combinations
- [mongodb-atlas-ai-context.md](references/mongodb-atlas-ai-context.md) — MongoDB Atlas as an AI agent context layer (RAG, memory, hybrid search)

### Related Skills

| Skill | Relationship |
|-------|--------------|
| [data-sql-optimization](../data-sql-optimization/SKILL.md) | Query tuning on existing schemas |
| [software-backend](../software-backend/SKILL.md) | Data access patterns in backend services |
| [software-baas-platforms](../software-baas-platforms/SKILL.md) | Managed app-backend platform choice and migration boundaries |
| [software-csharp-backend](../software-csharp-backend/SKILL.md) | EF Core data access and migration patterns |
| [software-architecture-design](../software-architecture-design/SKILL.md) | System-level data architecture decisions |
| [data-lake-platform](../data-lake-platform/SKILL.md) | Analytical storage and lakehouse design |
| [software-ios-native](../software-ios-native/SKILL.md) | SwiftData/Core Data + CloudKit persistence in native iOS apps |
| [software-ios-ai-engine](../software-ios-ai-engine/SKILL.md) | On-device iOS semantic search and local vector retrieval |

---

## Verification Gate

Before delivering output:

- [ ] Every referenced table, collection, index, and migration step is internally consistent with the proposed schema.
- [ ] If the repo already contains migration tooling, name the exact validation command; otherwise mark migration validation as unverified.
- [ ] Expand-contract guidance includes rollout order and rollback notes for breaking schema changes.
- [ ] Every referenced schema file, migration path, or ORM config path exists in the repo or is explicitly marked as proposed.

## Fact-Checking

- Known bugs, regressions, and version-specific workaround guidance must be verified against current primary web sources before being treated as current fact.
- Use web search or fetch to verify current external facts, versions, pricing, or platform behavior before final answers.
- Prefer primary sources and report source links for volatile information.
- If web access is unavailable, state the limitation and mark guidance as unverified.

## Learnings Loop

Before applying this skill on a non-trivial task, read `learnings.consolidated.md` in this directory (and `learnings.md` if present).

After applying it, if you encountered a pattern worth remembering, a mistake worth preventing, or a domain fact that surprised you, append one dated bullet to `learnings.md` via `agents-skills-feedback-loop/scripts/append_learning.py`. Do not modify `SKILL.md` itself.
