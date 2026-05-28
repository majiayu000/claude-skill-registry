---
name: postgresql-extensions
description: Essential PostgreSQL extensions - pg_stat_statements, pg_trgm, PostGIS
version: "3.0.0"
sasmp_version: "1.3.0"
bonded_agent: 05-postgresql-advanced
bond_type: SECONDARY_BOND
category: database
difficulty: intermediate
estimated_time: 2h
---

# PostgreSQL Extensions Skill

> Atomic skill for essential extensions

## Overview

Production-ready patterns for installing and using key PostgreSQL extensions.

## Prerequisites

- PostgreSQL 16+
- Superuser or extension privileges
- Extension packages installed

## Parameters

```yaml
parameters:
  operation:
    type: string
    required: true
    enum: [install, configure, use]
  extension:
    type: string
    enum: [pg_stat_statements, pg_trgm, uuid_ossp, hstore, postgis]
```

## Quick Reference

### Install Extensions
```sql
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;
CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE EXTENSION IF NOT EXISTS uuid_ossp;
CREATE EXTENSION IF NOT EXISTS hstore;

-- Check installed
SELECT extname, extversion FROM pg_extension;
```

### pg_stat_statements
```sql
-- Top queries
SELECT query, calls, mean_exec_time
FROM pg_stat_statements
ORDER BY total_exec_time DESC LIMIT 10;

-- Reset stats
SELECT pg_stat_statements_reset();
```

### pg_trgm (Fuzzy Search)
```sql
-- Similarity search
SELECT name, similarity(name, 'postgresql') as sim
FROM products WHERE name % 'postgresql';

-- Create trigram index
CREATE INDEX idx_trgm ON products USING GIN (name gin_trgm_ops);
```

### uuid-ossp
```sql
SELECT uuid_generate_v4();
```

### hstore
```sql
SELECT 'key=>value'::hstore;
SELECT data->'key' FROM table_with_hstore;
```

## Essential Extensions

| Extension | Use Case |
|-----------|----------|
| pg_stat_statements | Query analysis |
| pg_trgm | Fuzzy text search |
| uuid-ossp | UUID generation |
| hstore | Key-value pairs |
| postgis | Geospatial data |
| pgcrypto | Encryption |

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| Extension not found | Not installed | apt install postgresql-16-* |
| Permission denied | Not superuser | GRANT CREATE ON DATABASE |
| Version mismatch | Old extension | ALTER EXTENSION ... UPDATE |

## Usage

```
Skill("postgresql-extensions")
```
