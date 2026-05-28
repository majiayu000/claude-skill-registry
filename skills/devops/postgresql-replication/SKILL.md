---
name: postgresql-replication
description: PostgreSQL streaming replication - setup, monitoring, failover
version: "3.0.0"
sasmp_version: "1.3.0"
bonded_agent: 08-postgresql-devops
bond_type: SECONDARY_BOND
category: database
difficulty: advanced
estimated_time: 4h
---

# PostgreSQL Replication Skill

> Atomic skill for streaming replication

## Overview

Production-ready patterns for streaming replication, monitoring, and failover with Patroni.

## Prerequisites

- PostgreSQL 16+
- Multiple server nodes
- Network connectivity

## Parameters

```yaml
parameters:
  operation:
    type: string
    required: true
    enum: [setup_primary, setup_replica, monitor, failover]
  replication_mode:
    type: string
    enum: [async, sync]
    default: async
```

## Quick Reference

### Primary Setup
```sql
-- postgresql.conf
wal_level = replica
max_wal_senders = 10
max_replication_slots = 10

-- Create replication user
CREATE ROLE replicator WITH REPLICATION LOGIN PASSWORD 'secret';

-- Create slot
SELECT pg_create_physical_replication_slot('replica1');
```

### Replica Setup
```bash
pg_basebackup -h primary -D /data -U replicator -v -P -R
```

### Monitor Lag
```sql
-- On primary
SELECT client_addr, state,
    pg_size_pretty(pg_wal_lsn_diff(sent_lsn, replay_lsn)) as lag
FROM pg_stat_replication;

-- On replica
SELECT pg_is_in_recovery(), pg_last_wal_replay_lsn();
```

### Patroni HA
```yaml
scope: cluster
bootstrap:
  dcs:
    ttl: 30
    maximum_lag_on_failover: 1048576
```

## Replication Modes

| Mode | Data Safety | Latency |
|------|------------|---------|
| async | Possible loss | Low |
| sync | No loss | Higher |

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| Lag increasing | Slow replica | Check I/O |
| Slot inactive | Replica down | Drop old slot |
| Failover failed | etcd issue | Check cluster |

## Usage

```
Skill("postgresql-replication")
```
