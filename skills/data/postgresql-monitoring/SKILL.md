---
name: postgresql-monitoring
description: PostgreSQL monitoring - metrics, alerting, observability
version: "3.0.0"
sasmp_version: "1.3.0"
bonded_agent: 03-postgresql-performance
bond_type: SECONDARY_BOND
category: database
difficulty: intermediate
estimated_time: 3h
---

# PostgreSQL Monitoring Skill

> Atomic skill for performance monitoring

## Overview

Production-ready patterns for metrics collection, alerting, and observability.

## Prerequisites

- PostgreSQL 16+
- pg_stat_statements extension
- Optional: Prometheus, Grafana

## Parameters

```yaml
parameters:
  operation:
    type: string
    required: true
    enum: [collect_metrics, setup_alerting, diagnose]
  metric_type:
    type: string
    enum: [connections, queries, replication, storage]
```

## Quick Reference

### Key Queries

```sql
-- Connection stats
SELECT count(*), state FROM pg_stat_activity GROUP BY state;

-- Slow queries
SELECT query, mean_exec_time FROM pg_stat_statements
ORDER BY mean_exec_time DESC LIMIT 10;

-- Cache hit ratio
SELECT round(100.0 * sum(heap_blks_hit) /
    nullif(sum(heap_blks_hit + heap_blks_read), 0), 2) as ratio
FROM pg_statio_user_tables;

-- Table sizes
SELECT tablename, pg_size_pretty(pg_total_relation_size(tablename::regclass))
FROM pg_tables WHERE schemaname = 'public' ORDER BY pg_total_relation_size(tablename::regclass) DESC;

-- Replication lag
SELECT client_addr, pg_size_pretty(pg_wal_lsn_diff(sent_lsn, replay_lsn)) as lag
FROM pg_stat_replication;
```

### Critical Thresholds

| Metric | Warning | Critical |
|--------|---------|----------|
| Connections | 80% max | 95% max |
| Cache hit | < 99% | < 95% |
| Replication lag | > 1MB | > 100MB |
| Dead tuples | > 10K | > 100K |

### Prometheus Exporter
```yaml
postgres-exporter:
  image: prometheuscommunity/postgres-exporter
  environment:
    DATA_SOURCE_NAME: "postgresql://monitor:pass@postgres:5432/postgres"
```

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| No stats | Extension missing | CREATE EXTENSION pg_stat_statements |
| Old metrics | Stats not reset | pg_stat_statements_reset() |
| High connections | Leak or surge | Check application |

## Usage

```
Skill("postgresql-monitoring")
```
