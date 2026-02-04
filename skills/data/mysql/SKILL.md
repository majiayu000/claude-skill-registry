---
name: mysql
description: MySQL DBA skill for schema design review, indexing, query performance tuning (EXPLAIN), transaction/isolation issues, replication/high availability, backup/restore, and operational checklists. Use for tasks like diagnosing slow queries, designing keys/indexes, partitioning strategy, and safe online schema changes.
---

# mysql

Use this skill for MySQL 数据库设计、性能与运维（DBA）相关任务。

## Defaults / assumptions to confirm

- MySQL version (5.7 / 8.0)
- Storage engine (InnoDB)
- Character set/collation (`utf8mb4`)
- Replication topology (single-primary, multi-source, etc.)

## Workflow

1) Understand workload and constraints
- Read/write ratio, QPS, data size growth.
- Latency SLO, peak patterns, critical tables/queries.

2) Schema review
- Primary key strategy (avoid random PK for hot inserts unless needed; be explicit).
- Data types: avoid oversized VARCHAR/TEXT; use proper INT/BIGINT/DECIMAL.
- Nullability and defaults aligned with business meaning.
- Avoid over-normalization that forces heavy joins on critical paths.

3) Index design
- Add indexes for query patterns (WHERE, JOIN, ORDER BY, GROUP BY).
- Prefer composite indexes that match left-prefix usage.
- Avoid redundant indexes; keep write amplification in mind.
- Unique constraints where required; ensure consistent naming.

4) Query tuning
- Use `EXPLAIN` / `EXPLAIN ANALYZE` (8.0) to verify index usage.
- Watch for full table scans, filesort, temporary tables.
- Fix N+1 queries at application layer when possible.

5) Transactions & locking
- Confirm isolation level; analyze deadlocks and lock waits.
- Keep transactions short; avoid large gap locks where possible.

6) Partitioning / sharding (when needed)
- Partition only with clear pruning benefits and operational plan.
- Prefer application-level sharding with stable keys when scaling beyond single instance.

7) Operations
- Backups: logical + physical, restore drills, retention.
- Replication monitoring: lag, GTID, failover procedures.
- Online schema changes: `gh-ost`/`pt-online-schema-change` where appropriate.

## Outputs

- Index plan: which queries, which indexes, expected benefit, trade-offs.
- Migration plan: DDL, rollout steps, backout plan, verification queries.
- Performance report: top queries, proposed fixes, metrics to watch.

