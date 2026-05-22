---
name: postgresql-performance
description: Optimize PostgreSQL performance - EXPLAIN ANALYZE, indexing, query tuning
version: "3.0.0"
sasmp_version: "1.3.0"
bonded_agent: 03-postgresql-performance
bond_type: PRIMARY_BOND
category: database
difficulty: advanced
estimated_time: 4h
---

# PostgreSQL Performance Skill

> Atomic skill for query optimization

## Overview

Production-ready patterns for EXPLAIN analysis, index design, and configuration tuning.

## Prerequisites

- PostgreSQL 16+
- pg_stat_statements extension

## Parameters

```yaml
parameters:
  operation:
    type: string
    required: true
    enum: [analyze_query, create_index, tune_config, diagnose]
  target_time_ms:
    type: integer
    default: 100
```

## Quick Reference

### EXPLAIN Commands
```sql
EXPLAIN (ANALYZE, BUFFERS) SELECT * FROM users WHERE email = 'test@example.com';
```

### Index Types
| Use Case | Type | Example |
|----------|------|---------|
| Equality | B-tree | `CREATE INDEX idx ON t(col)` |
| JSONB | GIN | `USING GIN(data jsonb_path_ops)` |
| Time-series | BRIN | `USING BRIN(created_at)` |

### Key Metrics
| Metric | Healthy | Warning |
|--------|---------|---------|
| Seq Scan rows | < 10K | > 100K |
| Buffer hit | > 99% | < 95% |
| Planning time | < 10ms | > 100ms |

## Diagnostic Queries

```sql
-- Slow queries
SELECT query, mean_exec_time FROM pg_stat_statements ORDER BY mean_exec_time DESC LIMIT 10;

-- Unused indexes
SELECT indexrelname, idx_scan FROM pg_stat_user_indexes WHERE idx_scan = 0;

-- Table bloat
SELECT tablename, n_dead_tup FROM pg_stat_user_tables WHERE n_dead_tup > 10000;
```

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| Seq Scan | Missing index | Create index |
| High buffer reads | Cold cache | Increase shared_buffers |
| Wrong estimates | Stale stats | Run ANALYZE |

## Usage

```
Skill("postgresql-performance")
```
