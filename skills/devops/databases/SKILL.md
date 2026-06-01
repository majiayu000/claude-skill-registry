---
name: databases
description: >
  · Configure/tune/migrate PostgreSQL, MongoDB, MySQL/MariaDB, MSSQL. Triggers: 'database', 'postgres', 'mysql', 'mongodb', 'schema', 'migration', 'pgbouncer', 'EXPLAIN'. Not for HTTP APIs (use backend-api).
license: MIT
compatibility: "Requires one or more of: psql, mongosh, mysql, or sqlcmd"
metadata:
  source: iuliandita/skills
  date_added: "2026-03-24"
  effort: high
  argument_hint: "[engine-or-task-or-query]"
---

# Databases: Production Configuration & Operations

Configure, tune, design schemas, migrate, back up, and review database engines - from single-node dev setups to PCI-compliant production clusters. The goal is correct, performant, durable databases that survive failures, pass audits, and don't wake you up at 3am.

**Target versions** (May 2026):
- PostgreSQL **18.4** (EOL 2030-11; May 2026 security release), previous: 17.10, 16.14
- MongoDB **8.0.20** (GA, EOL 2029-10); rapid lane (8.3 latest) is Atlas-only with a short window - verify live before pinning
- MariaDB **11.8.7** (LTS, EOL 2028-06); 12.x rolling GA is quarterly and EOLs at each successor (12.2 reached EOL 2026-05), with 12.3 the next yearly LTS - verify live
- MySQL **8.4.8** (LTS); innovation lane (9.x) has a short support window - verify live
- SQL Server **2025 RTM + CU3** (GA 2025-11-18)
- PgBouncer **1.25.1**, Pgpool-II **4.7.1**, ProxySQL **3.0.6**

This skill covers six domains depending on context:
- **Configuration** - engine settings, authentication, TLS, tuning parameters
- **Schema design** - indexing strategy, partitioning, normalization, type selection
- **Migration** - cross-engine migration, zero-downtime DDL, ORM migration tooling
- **Operations** - backup/restore, replication, connection pooling, monitoring
- **Performance** - query plan analysis, index optimization, vacuum/maintenance
- **Compliance** - PCI-DSS 4.0 encryption, audit logging, key management, data masking

## When to use

- Configuring database engines (postgresql.conf, mongod.conf, my.cnf, MSSQL settings)
- Designing or reviewing database schemas (indexes, partitioning, types, constraints)
- Planning or executing cross-engine migrations (MySQL -> PostgreSQL, etc.)
- Setting up backup/restore strategies and PITR
- Configuring replication (streaming, logical, replica sets, GTID)
- Tuning connection pooling (PgBouncer, ProxySQL, application-side pools)
- Analyzing query performance (EXPLAIN, slow query logs, index usage)
- Database-level PCI-DSS 4.0 compliance (encryption, audit logging, access control)
- Evaluating managed vs self-hosted database decisions
- Setting up database monitoring and alerting

## When NOT to use

- Deploying databases on Kubernetes (StatefulSets, PVCs, operators) - use **kubernetes**
- Provisioning managed databases (RDS, Cloud SQL, Atlas) via IaC - use **terraform**
- Docker Compose for database containers - use **docker**
- Database-related Ansible playbooks and roles - use **ansible**
- Application-level database bugs (N+1, transaction misuse, ORM pitfalls) - use **code-review**
- SQL injection detection, connection string secrets in code - use **security-audit**
- CI/CD pipelines that run migrations - use **ci-cd**
- Redis/Valkey (cache/KV stores) and other non-relational engines (Cassandra, DynamoDB, ClickHouse, etc.) - outside this skill's four primary engines; use the relevant platform skill or general guidance

---

## AI Self-Check

AI tools consistently produce the same database mistakes. **Before returning any generated SQL, schema, migration, or config, verify against this list:**

### Migrations

- [ ] `IF NOT EXISTS` / `IF EXISTS` guards on `ADD COLUMN` / `DROP COLUMN` (bare DDL crashes on re-run)
- [ ] Adding `NOT NULL` column includes a `DEFAULT` value (or two-step: add nullable, backfill, alter NOT NULL)
- [ ] Index creation uses `CONCURRENTLY` on PostgreSQL (prevents full table lock)
- [ ] Large table changes run in batches, not a single transaction (lock escalation, OOM risk)
- [ ] Migration is backward-compatible (old app version can still run against new schema)
- [ ] No `DROP TABLE` or `DROP DATABASE` without explicit user confirmation
- [ ] Migration is idempotent - can be run twice without error
- [ ] Rollback/down migration exists and is tested
- [ ] PG enum changes use `ALTER TYPE ... ADD VALUE` outside a transaction (PG 12+ allows it inside a transaction, but the new value cannot be used until that transaction commits - run it standalone to use the value immediately)

### Schema

- [ ] New timestamp columns use `timestamptz` (PG), `DATETIME2` (MSSQL), `DATETIME` (MySQL - `TIMESTAMP` has the 2038 problem)
- [ ] Character set is `utf8mb4` for MySQL (not `utf8` which is 3-byte only), `UTF8` for PG
- [ ] Identity columns use `GENERATED ALWAYS AS IDENTITY` over `SERIAL` in PG 10+ (non-bypassable)
- [ ] Foreign keys have explicit `ON DELETE` behavior (don't rely on engine defaults)
- [ ] Indexes exist on all foreign key columns (PG does NOT auto-create these, unlike MySQL InnoDB)
- [ ] Composite index column order follows: equality columns first, range column last, selectivity-ordered

### Configuration

- [ ] No `trust` or `md5` authentication in `pg_hba.conf` (use `scram-sha-256`)
- [ ] MySQL `sql_mode` includes `STRICT_TRANS_TABLES` (prevents silent data truncation)
- [ ] TLS enforced for all connections (not just "available")
- [ ] `max_connections` is sized for the actual workload, not left at default
- [ ] Password authentication uses modern hashing (SCRAM-SHA-256 for PG, `caching_sha2_password` for MySQL)
- [ ] No default/example passwords in config files

### Bulk Operations

- [ ] Bulk inserts are chunked - never pass an unbounded array into a single `INSERT ... VALUES` statement
- [ ] Chunk size computed as `floor(max_host_parameters / columns_per_row)`, where host-parameter limits are: PostgreSQL 65,535, MySQL 65,535, SQLite 32,766 (default `SQLITE_MAX_VARIABLE_NUMBER`), MSSQL 2,100
- [ ] When the app targets multiple backends, chunk size uses the lowest limit across all supported engines
- [ ] Chunked writes stay inside one transaction when replace-all semantics are required (DELETE + INSERT pattern)
- [ ] Tests assert that multiple insert calls fire when row count crosses the safe chunk threshold

### General

- [ ] All SQL uses parameterized queries / prepared statements (never string concatenation)
- [ ] Connection pool settings don't exceed `max_connections` across all app instances
- [ ] Backup strategy tested by actually restoring (backup without restore test = hope, not a strategy)
- [ ] Secrets (passwords, connection strings) injected via env vars or secret managers, not config files
- [ ] **Current source checked**: dated versions, CLI flags, API names, and support windows are verified against primary docs before repeating them
- [ ] **Hidden state identified**: local config, credentials, caches, contexts, branches, cluster targets, or previous runs are made explicit before acting
- [ ] **Verification is real**: final checks exercise the actual runtime, parser, service, or integration point instead of only linting prose or happy paths
- [ ] **Routing overlap checked**: overlapping skills, trigger terms, and "When NOT to use" boundaries are checked before returning guidance
- [ ] **Spec claims verified**: claims about tool behavior, output contracts, or repo conventions are checked against current docs, scripts, or skill files
- [ ] **Engine/version checked**: SQL syntax, index options, and replication advice match the named engine and major version
- [ ] **Data-loss path gated**: migrations, deletes, reindexes, and failovers include backup, dry-run, rollback, or maintenance-window guidance

---

## Performance

- Use `EXPLAIN`/`EXPLAIN ANALYZE` with realistic parameters before adding indexes.
- Tune connection pools to database capacity; more app connections can reduce throughput.
- Batch writes and migrations in bounded chunks to avoid lock escalation, replication lag, and runaway transactions.


---

## Best Practices

- Take restorable backups before schema changes and verify restore procedures periodically.
- Separate online, background, and analytical workloads where query shape or latency differs.
- Prefer additive migrations with backfills and compatibility windows for zero-downtime services.


## Workflow

### Step 1: Determine the domain

Based on the request:
- **"Configure PostgreSQL / tune settings"** -> Configuration
- **"Design a schema / review indexes"** -> Schema design
- **"Migrate from X to Y / add a column"** -> Migration
- **"Set up backups / replication / pooling"** -> Operations
- **"This query is slow / optimize"** -> Performance
- **"PCI audit / encrypt database"** -> Compliance
- **"Review this schema/config"** -> Apply production checklist + AI self-check

### Step 2: Gather requirements

Before writing SQL or config, determine these. If the user doesn't specify, use the sensible defaults shown:
- **Engine and version** - behavior differs significantly across versions. Default: latest stable (see target versions above).
- **Deployment model** - self-hosted (bare metal, VM, container, K8s) vs managed (RDS, Cloud SQL, Atlas). Default: assume self-hosted unless context says otherwise.
- **Workload type** - OLTP (many small transactions) vs OLAP (few large queries) vs mixed. Default: OLTP.
- **Data volume** - row counts, table sizes, growth rate. Default: medium (1-100GB). If unknown, optimize for growth.
- **Compliance** - PCI-DSS CDE? HIPAA? What data classification? Default: no compliance scope (but still apply security baseline).
- **HA requirements** - RTO/RPO targets, multi-AZ, read replicas. Default: single-node with PITR.
- **Existing infrastructure** - what's already running, what ORMs/drivers are in use. Inspect the codebase if accessible.

### Step 3: Build

Follow the domain-specific section below. Always apply the production checklist and AI self-check before finishing.

**Common operations - quick-start patterns:**

**Query optimization** (the most frequent request):
1. Get the plan: `EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT) SELECT ...;` (PG), `EXPLAIN FORMAT=TREE ...;` (MySQL 8.0+), `db.collection.explain('executionStats').find(...)` (MongoDB).
2. Look for: `Seq Scan` on large tables (PG) / `Full Table Scan` (MySQL) / `COLLSCAN` (MongoDB), `Nested Loop` with high row estimates, `Sort` spilling to disk (`Sort Method: external merge`), and `Rows Removed by Filter` >> `Rows` returned.
2a. Before assuming an index problem, verify semantic correctness: check JOIN conditions for column mismatches, confirm WHERE clause predicates don't unintentionally filter nulls, and verify LEFT JOIN semantics aren't silently converted to INNER JOIN by outer-table filters.
3. Check index usage: `SELECT schemaname, relname, idx_scan, seq_scan FROM pg_stat_user_tables WHERE seq_scan > 100 ORDER BY seq_scan DESC;` (PG; adjust `schemaname = 'public'` filter for non-public schemas) or `SELECT * FROM sys.schema_unused_indexes;` (MySQL performance_schema).
4. If a missing index is the fix, create it with `CONCURRENTLY` (PG): `CREATE INDEX CONCURRENTLY idx_orders_customer ON orders (customer_id);` or `ALGORITHM=INPLACE, LOCK=NONE` (MySQL).
5. Re-run `EXPLAIN ANALYZE` to confirm the planner uses the new index and that estimated vs actual rows are close.

**Lock contention / deadlock diagnosis** (second most common "it's stuck" scenario):
1. PG: `SELECT pid, age(backend_xact_start), query, wait_event_type, wait_event FROM pg_stat_activity WHERE state != 'idle' AND wait_event IS NOT NULL ORDER BY age(backend_xact_start) DESC;`
2. PG blocked queries: `SELECT blocked.pid AS blocked_pid, blocked.query AS blocked_query, blocking.pid AS blocking_pid, blocking.query AS blocking_query FROM pg_stat_activity blocked JOIN pg_locks bl ON bl.pid = blocked.pid JOIN pg_locks kl ON kl.locktype = bl.locktype AND kl.database IS NOT DISTINCT FROM bl.database AND kl.relation IS NOT DISTINCT FROM bl.relation AND kl.page IS NOT DISTINCT FROM bl.page AND kl.tuple IS NOT DISTINCT FROM bl.tuple AND kl.transactionid IS NOT DISTINCT FROM bl.transactionid AND kl.pid != bl.pid JOIN pg_stat_activity blocking ON blocking.pid = kl.pid WHERE NOT bl.granted AND kl.granted;`
3. MySQL: `SHOW ENGINE INNODB STATUS\G` - look for `LATEST DETECTED DEADLOCK` section. Also: `SELECT * FROM performance_schema.data_lock_waits;` (MySQL 8.0+).
4. MongoDB: `db.currentOp({"waitingForLock": true})` and check `mongod` log for `LockTimeout` entries.
5. Fix: kill the blocking query if it's stuck (`SELECT pg_terminate_backend(PID);` / `KILL CONNECTION thread_id;`), then investigate why the lock was held (long transactions, missing indexes on UPDATE/DELETE WHERE clauses, lock ordering bugs in application code).

**Connection pooler sizing** (second most common):
1. Determine backend budget: `max_connections` minus superuser_reserved minus replication slots = available.
2. PgBouncer `default_pool_size` per user/db pair: start at `available / number_of_app_instances`, round down.
3. Set `max_client_conn` to the total connections your app fleet will open (all instances combined).
4. Use `transaction` pool mode for stateless web apps. Switch to `session` mode (which supports all PostgreSQL features) when the app needs session-level state: temp tables, advisory locks, `SET`, or prepared statements on PgBouncer older than 1.21 (1.21+ supports prepared statements in transaction mode via `max_prepared_statements`).
5. Validate: `psql -h pgbouncer-host -p 6432 pgbouncer -c "SHOW POOLS;"` - watch `sv_active` vs `sv_idle` under load.

**Migration safety check** (before running any DDL in production):
1. Verify the migration is idempotent: `IF NOT EXISTS` / `IF EXISTS` guards on all DDL.
2. Check table size: `SELECT pg_size_pretty(pg_total_relation_size('tablename'));` - anything over 1GB needs batched operations or `CONCURRENTLY` indexes.
3. Verify backward compatibility: can the current app version still function after this DDL runs?
4. Test the rollback/down migration against a copy of production data, not just an empty schema.
5. Run during low-traffic window if the operation takes locks (even brief ones).

### Step 4: Validate

```bash
# PostgreSQL
psql -c "SHOW config_file;"                    # verify config location
pg_isready -h localhost                         # connection check
psql -c "SELECT * FROM pg_hba_file_rules;"     # verify pg_hba.conf
psql -c "EXPLAIN (ANALYZE, BUFFERS) <query>;"  # query plan analysis

# MongoDB
mongosh --eval "db.adminCommand({getCmdLineOpts: 1})"  # verify config
mongosh --eval "rs.status()"                            # replica set health
mongosh --eval "db.collection.explain('executionStats').find({})"

# MySQL / MariaDB
mysql -e "SELECT @@sql_mode;"                  # verify strict mode
mysql -e "SHOW VARIABLES LIKE 'innodb%';"      # InnoDB settings
mysql -e "EXPLAIN FORMAT=TREE <query>;"        # query plan (MySQL 8.0+)

# MSSQL
sqlcmd -Q "SELECT @@VERSION;"
sqlcmd -Q "DBCC CHECKDB ('dbname') WITH NO_INFOMSGS;"  # integrity check
```

---

## Engine Routing

- **PostgreSQL**: SCRAM, poolers, WAL or logical replication, `pg_stat_statements`, and careful vacuum strategy
- **MongoDB**: replica-set health, schema validation, oplog sizing, and avoiding fan-out document patterns
- **MySQL/MariaDB**: strict mode, `utf8mb4`, GTID or Galera choices, and understanding the MySQL/MariaDB divergence
- **MSSQL**: memory limits, TempDB layout, Query Store, and backup or restore discipline

Read `references/config-templates.md` for copy-pasteable engine configs and `references/backup-patterns.md`
for recovery specifics.

---

## Schema, Migration, and Performance

- Favor expand-contract for zero-downtime schema changes.
- Composite index order still follows equality, sort, then range.
- Choose tenant isolation deliberately; PCI-sensitive shared-schema designs need extra scrutiny.
- Treat query-plan review and monitoring as normal operations, not emergency-only work.
- Watch for `WHERE` clauses that nullify `LEFT JOIN` semantics (filtering the outer table converts it to `INNER JOIN` - move the filter into the `ON` clause or use a subquery).

### Major version upgrades

Three approaches, pick by downtime tolerance:

| Method | Downtime | Best for |
|--------|----------|----------|
| `pg_upgrade --link` | Minutes (metadata copy) | Small-to-medium DBs where brief downtime is acceptable |
| Logical replication | Seconds (cutover only) | Large DBs, zero-downtime requirement, PG 10+ to any higher |
| `pg_dump` / `pg_restore` | Hours (full copy) | Cross-engine, major schema changes, or when logical replication is impractical |

**Zero-downtime with logical replication** (PG -> PG):
1. Stand up new version replica alongside the primary
2. Create publication on source: `CREATE PUBLICATION upgrade_pub FOR ALL TABLES;`
3. Create subscription on target: `CREATE SUBSCRIPTION upgrade_sub CONNECTION '...' PUBLICATION upgrade_pub;`
4. Wait for initial sync + catchup (monitor `pg_stat_subscription`, replication lag)
5. Migrate sequences: logical replication does not replicate sequence values - copy them manually
6. Test application against the new version (read traffic, connection pooler split). **Monitor during split-test**: query latency p50/p95/p99 (compare old vs new - regression means planner stats or config drift), error rates by query type (new version may have stricter behavior), connection pool saturation (`SHOW POOLS` in PgBouncer - watch `cl_waiting`), replication lag trend (should stay flat or decrease, never grow during read-only test), and memory/CPU on the new instance. Run for at least one full traffic cycle (24h if your workload is diurnal). Abort and route back to old primary if error rate exceeds baseline or p99 latency degrades >20%.
7. Cutover: stop writes to old primary, verify lag = 0, point connection pooler to new primary
8. Drop subscription and decommission old primary

**Rollback procedure** (if replication stalls or validation fails):
- **Lag not reaching zero**: Check `pg_stat_subscription` for `last_msg_send_time` vs `last_msg_receipt_time` delta. Common causes: long-running transactions on source blocking WAL send, tables missing primary keys (forces full-row comparison), or network throughput limits. If lag is stuck, check `pg_replication_slots` on the source for `active = false` - an inactive slot means the subscription dropped. Recreate the subscription; do not proceed with cutover.
- **Application validation fails on new version**: Route all traffic back to the old primary (update pooler config). The old primary never stopped accepting writes, so no data is lost. Drop the subscription on the new instance: `DROP SUBSCRIPTION upgrade_sub;` - this also drops the replication slot on the source. Investigate, fix, and restart from step 3.
- **Post-cutover rollback** (writes already went to new primary): This is the hard case. Options: (a) set up reverse logical replication from new -> old before decommissioning the old primary (plan this before cutover if RTO requires it), or (b) restore old primary from backup + WAL and accept data loss for the cutover window. Option (a) requires the old primary to still be running. **Decision point**: if you need rollback after cutover, set up reverse replication in step 6 before routing write traffic.

**Key pitfalls** (check all of these before starting):
- Tables need primary keys or `REPLICA IDENTITY FULL` - check first: `SELECT c.relname FROM pg_class c JOIN pg_namespace n ON c.relnamespace = n.oid WHERE n.nspname = 'public' AND c.relkind = 'r' AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conrelid = c.oid AND contype = 'p');`
- DDL is not replicated - schema changes during migration need manual sync on both sides
- Large objects (`lo`) are not replicated
- Sequence values drift - copy them manually after cutover, not before

Read `references/migration-patterns.md` for cross-engine type mapping, ORM migration tooling, and detailed migration patterns.

---

## Pooling, Backup, and Platform Choice

- PostgreSQL pooling is usually non-negotiable; use PgBouncer unless a concrete reason says otherwise.
- Backup discipline means restore testing, encryption, retention limits, and monitoring backup freshness.
- Managed databases reduce toil but do not remove shared-responsibility or compliance review.
- Self-hosted databases buy control at the cost of HA, patching, and operational burden.

---

## Production Checklist

### All Engines

- [ ] Authentication uses modern hashing (SCRAM-SHA-256, caching_sha2_password, certificate auth)
- [ ] TLS enforced for all connections (not just "available")
- [ ] No default passwords, no `trust` auth, no passwordless access
- [ ] Connection pool in front of the database (PgBouncer, ProxySQL, or application-side)
- [ ] `max_connections` sized for actual workload, not default
- [ ] Backup strategy implemented, tested, and monitored
- [ ] Restore procedure documented and tested (at least monthly)
- [ ] Monitoring in place (connections, query performance, replication lag, disk usage)
- [ ] Slow query logging enabled with appropriate threshold
- [ ] Dead/unused indexes identified and removed
- [ ] Character encoding correct (`utf8mb4` for MySQL, `UTF8` for PG)

### PostgreSQL-Specific

- [ ] `pg_hba.conf`: `hostssl` only, `scram-sha-256` only, CIDR-restricted
- [ ] `shared_buffers` = 25% RAM, `effective_cache_size` = 75% RAM
- [ ] `work_mem` sized for concurrency (PG default is 4MB; allocated per sort/hash operation, not per connection - multiply by concurrent queries x operations to estimate peak memory)
- [ ] `random_page_cost = 1.1` for SSD storage
- [ ] `statement_timeout` set per-role (not globally - migrations need longer)
- [ ] `idle_in_transaction_session_timeout` set (60s default)
- [ ] `pg_stat_statements` enabled
- [ ] Autovacuum tuned for large tables (`autovacuum_vacuum_scale_factor`)
- [ ] WAL archiving enabled for PITR (`archive_mode = on` + pgBackRest/Barman, or managed backup)
- [ ] Foreign key columns have indexes
- [ ] pgAudit installed and configured (if PCI scope)
- [ ] Patched against CVE-2026-2005 (pgcrypto heap buffer overflow, RCE) - 18.2+ / 17.8+ / 16.12+
- [ ] On the May 2026 PostgreSQL update (CVE-2026-6473/6475/6477/6637, up to CVSS 8.8: integer-overflow allocations, libpq client stack overwrite, refint stack overflow, MD5 timing leak) - 18.4+ / 17.10+ / 16.14+ / 15.18+ / 14.23+

### MySQL/MariaDB-Specific

- [ ] `sql_mode` includes `STRICT_TRANS_TABLES` (prevents silent data truncation)
- [ ] `innodb_buffer_pool_size` = 70% RAM
- [ ] `innodb_flush_log_at_trx_commit = 1` for durability
- [ ] `require_secure_transport = ON`
- [ ] `character-set-server = utf8mb4`
- [ ] Binary log enabled for PITR (`log_bin = ON`)
- [ ] `innodb_file_per_table = ON`
- [ ] MariaDB patched against CVE-2026-32710 (JSON_SCHEMA_VALID crash/RCE) - 11.8.6+ / 11.4.10+

### MongoDB-Specific

- [ ] `security.authorization: enabled` (never run without auth)
- [ ] Replica set with 3+ members (not standalone in production)
- [ ] Write concern `w: "majority"` (default in 8.0+)
- [ ] Schema validation (`$jsonSchema`) on critical collections
- [ ] Patched against MongoBleed (CVE-2025-14847) - 8.0.17+
- [ ] Patched against CVE-2026-25611 (pre-auth DoS via compression) - 8.0.18+ / 8.2.4+
- [ ] TLS enabled (`net.tls.mode: requireTLS`)

### MSSQL-Specific

- [ ] `Max Server Memory` set explicitly (not unlimited)
- [ ] `MAXDOP` set to core count per NUMA node
- [ ] `Cost Threshold for Parallelism` raised from default 5
- [ ] TempDB files = min(CPU cores, 8), equal size
- [ ] Query Store enabled
- [ ] Recovery model = FULL for production databases
- [ ] TDE enabled for CDE databases
- [ ] Patched against CVE-2026-21262 (privilege escalation) - March 2026 CU+

### Compliance (PCI-DSS 4.0)

- [ ] Encryption at rest: TDE or column-level (disk-level alone insufficient per Req 3.5.1.2)
- [ ] Encryption in transit: TLS 1.2+ enforced on all connections (Req 4)
- [ ] Audit logging: pgAudit/audit plugin, shipped to immutable SIEM (Req 10)
- [ ] Key management: keys in HSM/KMS, not alongside data (Req 3.6)
- [ ] Key rotation: DEKs every 90 days, master keys annually (Req 3.7)
- [ ] Access control: separate roles, no shared accounts, MFA for CDE access (Req 7, 8)
- [ ] Data masking: PAN display limited to last 4 digits (Req 3.3)
- [ ] No cardholder data in non-prod environments (Req 6.5.4)
- [ ] Quarterly access review documented (Req 7.2.5)
- [ ] Vulnerability scanning includes database engine, not just containers (Req 11.3)

---

## Reference Files

- `references/config-templates.md` - engine configuration templates
- `references/backup-patterns.md` - backup, restore, and PITR patterns
- `references/migration-patterns.md` - cross-engine migration patterns and type-mapping guidance

---

## Rules

These are non-negotiable. Violating any of these is a bug.

1. **Backups without restore tests are not backups.** Test restores monthly. Document the procedure.
2. **No `trust` auth in `pg_hba.conf`.** Not in dev, not in Docker, not anywhere. Use `scram-sha-256`.
3. **MySQL strict mode ON.** `STRICT_TRANS_TABLES` prevents silent data truncation. Without it, MySQL silently corrupts your data.
4. **TLS enforced, not just available.** `require_secure_transport`, `hostssl`, `requireTLS`. Connections without TLS are a finding.
5. **Connection pooler for PostgreSQL.** PG's process-per-connection model doesn't scale without one. Use PgBouncer.
6. **Indexes on foreign keys in PostgreSQL.** PG doesn't auto-create them. Missing FK indexes cause sequential scans on JOINs and cascading DELETEs.
7. **`utf8mb4` for MySQL, always.** `utf8` is a lie - it's 3-byte only, can't store emoji or many CJK characters.
8. **`timestamptz` for PostgreSQL, always.** Bare `timestamp` stores no timezone, breaks when server timezone changes.
9. **Parameterized queries everywhere.** String concatenation for SQL is a bug, not a shortcut. Doubly true for AI-generated code.
10. **Disk-level encryption is insufficient for PCI-DSS 4.0.** Req 3.5.1.2 requires TDE, column-level, or application-layer encryption.
11. **Patch MongoBleed (CVE-2025-14847).** Self-hosted MongoDB < 8.0.17 / 7.0.28 / 6.0.27 is actively exploitable with no authentication required.
12. **Patch MongoDB compression DoS (CVE-2026-25611).** Pre-auth DoS via crafted OP_COMPRESSED messages. Default config affected (compression enabled since 3.6). Fixed in 8.0.18+ / 8.2.4+ / 7.0.29+.
13. **Patch PgBouncer (CVE-2025-12819).** PgBouncer < 1.25.1 can allow unauthenticated SQL execution when `track_extra_parameters` includes `search_path` AND `auth_user` is set (both non-default). Upgrade regardless - the fix is low-risk.
14. **Chunk bulk inserts.** Never build a single `INSERT ... VALUES` with an unbounded row list. Compute batch size from the lowest host-parameter ceiling across supported backends (`floor(limit / columns_per_row)`). Wrap chunks in one transaction when atomicity matters.
15. **Run the AI self-check.** Every generated migration, schema, or config gets verified against the checklist above before returning.

---

## Output Contract

See `skills/_shared/output-contract.md` for the full contract.

- **Skill name:** DATABASES
- **Deliverable bucket:** `audits`
- **Mode:** conditional. When invoked to **analyze, review, audit, or improve** existing repo content, emit the full contract - boxed inline header, body summary inline plus per-finding detail in the deliverable file, boxed conclusion, conclusion table - and write the deliverable to `docs/local/audits/databases/<YYYY-MM-DD>-<slug>.md`. When invoked to **answer a question, teach a concept, build a new artifact, or generate content**, respond freely without the contract.
- **Severity scale:** `P0 | P1 | P2 | P3 | info` (see shared contract; only used in audit/review mode).

## Related Skills

- **code-review** - has a `databases.md` reference for application-level database **bug patterns** (transaction misuse, NULL handling, ORM N+1, type coercion). This skill covers engine configuration and operations; code-review covers how the application uses the database.
- **security-audit** - for SQL injection detection and credential scanning in application code
- **kubernetes** - for deploying databases on K8s (StatefulSets, operators, PVCs)
- **terraform** - for provisioning managed databases (RDS, Cloud SQL, Atlas)
- **docker** - for database containers in Docker Compose
- **ansible** - for database server configuration management
- **ci-cd** - for CI/CD pipelines that run migrations (schema execution in CI, migration gating, rollback automation)
