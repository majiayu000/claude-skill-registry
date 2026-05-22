---
name: postgresql
description: PostgreSQL DBA skill for schema design review, indexing, query tuning (EXPLAIN/ANALYZE), vacuum/autovacuum, concurrency/locking, partitioning, backup/restore, replication/HA, and safe migrations. Use for tasks like diagnosing slow queries, designing indexes and constraints, and operating Postgres in production.
---

# postgresql

Use this skill for PostgreSQL 相关设计、性能与运维（DBA）任务。

## Defaults / assumptions to confirm

- Postgres version
- Deployment: managed vs self-hosted, single instance vs HA
- Connection pooler: pgbouncer?
- Workload: OLTP vs OLAP, write-heavy vs read-heavy

## Workflow

1) Understand workload and query paths
- Core tables, top queries, read/write ratio, growth rate.
- Latency SLO and peak hours.

2) Schema review
- Primary key strategy (string IDs vs bigint; be explicit about external IDs).
- Types: `TIMESTAMPTZ` for time, `NUMERIC` vs `BIGINT` vs `DECIMAL` trade-offs.
- Constraints: `NOT NULL`, `CHECK`, `UNIQUE` where needed.
- JSONB usage: keep structure stable; consider normalization vs JSONB.
- Comments: require `COMMENT ON TABLE/COLUMN` for long-lived schemas.

3) Index design
- Add indexes for WHERE/JOIN/ORDER BY patterns.
- Composite indexes aligned with left-prefix.
- Partial indexes for sparse predicates.
- `GIN` for JSONB/array search; `btree_gin`/`pg_trgm` if used.
- Avoid redundant indexes and over-indexing on write-heavy tables.

4) Query tuning
- Use `EXPLAIN (ANALYZE, BUFFERS)` to validate plans.
- Watch for seq scans, bad estimates, bloated tables, missing stats.
- Consider query rewrites, better predicates, and covering indexes.

5) Concurrency and locking
- Inspect lock contention; avoid long transactions.
- Use appropriate isolation; detect deadlocks and hot rows.

6) Maintenance (vacuum / bloat)
- Ensure autovacuum is effective; tune thresholds per table if needed.
- Monitor bloat and `n_dead_tup`; use `VACUUM (ANALYZE)` and reindex when justified.

7) Partitioning & scaling
- Partition only when there is pruning benefit and operational plan.
- Time-based partitions for append-only logs; ensure indexes per partition.
- Consider sharding only with strong requirements and stable shard key.

8) Operations
- Backups: base backup + WAL archiving; restore drills; retention.
- Replication: streaming replication, lag monitoring, failover runbook.
- Migrations: safe rollout steps, lock-time considerations, backout plan.

## Outputs

- Index/constraint plan (query → index/constraint → impact/tradeoff).
- Migration plan (DDL, rollout sequence, verification, rollback).
- Performance report (evidence, root cause, fixes, metrics to monitor).

