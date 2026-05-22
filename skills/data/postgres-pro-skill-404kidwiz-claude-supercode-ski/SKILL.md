---
name: postgres-pro
description: Use when user needs PostgreSQL database administration, performance optimization, high availability setup, backup/recovery, or advanced PostgreSQL feature implementation.
---

# PostgreSQL Professional

## Purpose

Provides comprehensive PostgreSQL expertise specializing in database administration, performance optimization, and advanced feature implementation. Excels at achieving maximum reliability, performance, and scalability for PostgreSQL deployments with high availability and advanced extensions.

## When to Use

- PostgreSQL-specific features needed (JSONB, full-text search, PostGIS, pgvector)
- Setting up streaming or logical replication
- Implementing PostgreSQL extensions
- Troubleshooting PostgreSQL-specific issues
- Optimizing PostgreSQL configuration
- Implementing partitioning and high availability

## Quick Start

**Invoke this skill when:**
- PostgreSQL-specific features needed (JSONB indexing, full-text search, PostGIS, pgvector)
- Setting up streaming replication or logical replication for PostgreSQL
- Implementing PostgreSQL extensions (pg_trgm, PostGIS, timescaledb, pg_partman)
- Troubleshooting PostgreSQL-specific issues (autovacuum, bloat, WAL archiving)
- Optimizing PostgreSQL configuration (shared_buffers, work_mem, vacuum settings)
- Implementing PostgreSQL partitioning (declarative partitioning, constraint exclusion)
- Setting up PostgreSQL high availability (Patroni, repmgr, pgpool-II)
- Designing JSONB schema and query optimization with GIN indexes

**Do NOT invoke when:**
- General SQL query writing (use sql-pro for ANSI SQL queries)
- Cross-platform database optimization (use database-optimizer for general tuning)
- MySQL or SQL Server specific features (use platform-specific skills)
- Database administration basics (users, permissions - use database-administrator)
- Simple query optimization without PostgreSQL-specific features
- ORM query patterns (use backend-developer with ORM expertise)

## Core Capabilities

### PostgreSQL Architecture
- Process architecture and memory configuration
- WAL mechanics and MVCC implementation
- Storage layout and buffer management
- Lock management and background workers

### Advanced Features
- JSONB optimization with GIN indexes
- Full-text search with tsvector and GIN indexes
- PostGIS spatial queries and indexing
- Time-series data handling and partitioning
- Foreign data wrappers and cross-database queries
- Parallel queries and JIT compilation

### Performance Tuning
- Configuration optimization (memory, connections, checkpoints)
- Query optimization and execution plan analysis
- Index strategies and index usage monitoring
- Vacuum tuning and autovacuum configuration
- Connection pooling and parallel execution

### Replication Strategies
- Streaming replication and logical replication
- Synchronous setup and cascading replicas
- Delayed replicas and failover automation
- Load balancing and conflict resolution

### Backup and Recovery
- pg_dump strategies and physical backups
- WAL archiving and PITR setup
- Backup validation and recovery testing
- Automation scripts and retention policies

## Decision Framework

### JSONB Index Strategy

```
JSONB Query Pattern Analysis
│
├─ Containment queries (@> operator)?
│   └─ Use GIN with jsonb_path_ops
│       CREATE INDEX idx ON table USING GIN (column jsonb_path_ops);
│       • 2-3x smaller than default GIN
│       • Faster for @> containment checks
│       • Does NOT support key existence (?)
│
├─ Key existence queries (? or ?| or ?& operators)?
│   └─ Use default GIN operator class
│       CREATE INDEX idx ON table USING GIN (column);
│       • Supports all JSONB operators
│       • Larger index size
│
├─ Specific path frequently queried?
│   └─ Use expression index
│       CREATE INDEX idx ON table ((column->>'key'));
│       • Most efficient for specific path
│       • B-tree allows range queries
│
└─ Full document search needed?
    └─ Combine GIN + expression indexes
        • GIN for flexible queries
        • Expression for hot paths
```

### Replication Strategy Selection

| Requirement | Strategy | Configuration |
|------------|----------|---------------|
| Read scaling | Streaming (async) | Multiple read replicas |
| Zero data loss | Streaming (sync) | synchronous_commit = on |
| Table-level replication | Logical | CREATE PUBLICATION/SUBSCRIPTION |
| Cross-version upgrade | Logical | Replicate to new version |
| Disaster recovery | Streaming + WAL archive | PITR capability |
| Delayed recovery | Delayed replica | recovery_min_apply_delay |

## Quality Checklist

**Performance:**
- [ ] Query performance targets met (OLTP <50ms, Analytics <2s)
- [ ] EXPLAIN ANALYZE reviewed for all critical queries
- [ ] GIN/GiST indexes used for JSONB, array, full-text queries
- [ ] Partitioning implemented for tables >10GB with time-series data
- [ ] Cache hit ratio >95% (shared_buffers + OS cache)
- [ ] Connection pooling implemented (PgBouncer or application pool)

**Configuration:**
- [ ] shared_buffers = 25% of RAM
- [ ] effective_cache_size = 75% of RAM
- [ ] work_mem tuned for workload (no temp file spills in EXPLAIN)
- [ ] Autovacuum configured (scale_factor ≤0.05 for large tables)
- [ ] max_connections appropriate (or using PgBouncer)
- [ ] WAL archiving enabled for PITR

**Replication (if applicable):**
- [ ] Replication slots created (prevents WAL deletion)
- [ ] Replication lag <500ms (P95)
- [ ] pg_stat_replication monitored (sync_state, replay_lag)
- [ ] Failover tested (promote replica to primary)
- [ ] pg_hba.conf configured for replication access

**Extensions:**
- [ ] Required extensions installed (pg_trgm, PostGIS, pgvector, etc.)
- [ ] Extension versions compatible with PostgreSQL version
- [ ] GIN indexes created for JSONB, tsvector, trigrams
- [ ] Full-text search configured with proper language dictionaries

**JSONB (if used):**
- [ ] GIN indexes created (jsonb_path_ops for containment queries)
- [ ] Expression indexes for frequently queried paths
- [ ] JSONB validation in application (jsonschema or custom)
- [ ] No deeply nested JSONB (>3 levels → consider normalization)

**Monitoring:**
- [ ] Slow query log configured (log_min_duration_statement = 200ms)
- [ ] pg_stat_statements installed and monitored
- [ ] Autovacuum progress monitored (pg_stat_progress_vacuum)
- [ ] Table bloat monitored (<15% dead tuples)
- [ ] Replication lag alerts configured (<1s threshold)

## Additional Resources

- **Detailed Technical Reference**: See [REFERENCE.md](REFERENCE.md)
- **Code Examples & Patterns**: See [EXAMPLES.md](EXAMPLES.md)
