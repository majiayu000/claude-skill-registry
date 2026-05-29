---
name: postgresql-scaling
description: Scale PostgreSQL - partitioning, connection pooling, high availability
version: "3.0.0"
sasmp_version: "1.3.0"
bonded_agent: 07-postgresql-scaling
bond_type: PRIMARY_BOND
category: database
difficulty: advanced
estimated_time: 5h
---

# PostgreSQL Scaling Skill

> Atomic skill for horizontal and vertical scaling

## Overview

Production-ready patterns for partitioning, connection pooling, and high availability.

## Prerequisites

- PostgreSQL 16+
- Understanding of replication
- PgBouncer or Patroni experience

## Parameters

```yaml
parameters:
  operation:
    type: string
    required: true
    enum: [partition, pool, replicate, shard]
  partition_type:
    type: string
    enum: [range, list, hash]
```

## Quick Reference

### Range Partitioning
```sql
CREATE TABLE events (id BIGINT, data JSONB, created_at TIMESTAMPTZ)
PARTITION BY RANGE (created_at);

CREATE TABLE events_2024_q1 PARTITION OF events
    FOR VALUES FROM ('2024-01-01') TO ('2024-04-01');
```

### PgBouncer Config
```ini
[pgbouncer]
pool_mode = transaction
default_pool_size = 20
max_client_conn = 1000
```

### Replication Setup
```sql
CREATE ROLE replicator WITH REPLICATION LOGIN PASSWORD 'secret';
SELECT pg_create_physical_replication_slot('replica1');
```

### Monitor Lag
```sql
SELECT client_addr, pg_size_pretty(pg_wal_lsn_diff(sent_lsn, replay_lsn)) as lag
FROM pg_stat_replication;
```

## Pool Mode Selection

| Mode | Use Case |
|------|----------|
| session | Long connections |
| transaction | Web apps (recommended) |
| statement | Simple queries |

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| Partition not used | Pruning disabled | SET enable_partition_pruning = on |
| Too many connections | No pooler | Use PgBouncer |
| Replication lag | Slow replica | Check I/O, network |

## Usage

```
Skill("postgresql-scaling")
```
