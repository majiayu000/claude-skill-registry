---
name: postgresql-json
description: Work with JSONB data - queries, indexing, transformations
version: "3.0.0"
sasmp_version: "1.3.0"
bonded_agent: 05-postgresql-advanced
bond_type: PRIMARY_BOND
category: database
difficulty: intermediate
estimated_time: 2h
---

# PostgreSQL JSON Skill

> Atomic skill for JSONB operations

## Overview

Production-ready patterns for JSONB queries, indexing, and transformations.

## Prerequisites

- PostgreSQL 16+
- Understanding of JSON structure

## Parameters

```yaml
parameters:
  operation:
    type: string
    required: true
    enum: [query, index, transform, aggregate]
  json_path:
    type: string
```

## Quick Reference

### JSONB Operators
| Operator | Description | Example |
|----------|-------------|---------|
| `->` | Get object | `data->'user'` |
| `->>` | Get as text | `data->>'name'` |
| `@>` | Contains | `data @> '{"active":true}'` |
| `?` | Key exists | `data ? 'email'` |

### Index Patterns
```sql
CREATE INDEX idx_data ON t USING GIN(data);  -- Containment
CREATE INDEX idx_data_path ON t USING GIN(data jsonb_path_ops);  -- Faster @>
CREATE INDEX idx_status ON t ((data->>'status'));  -- Specific key
```

### Common Operations
```sql
-- Nested update
UPDATE docs SET data = jsonb_set(data, '{user,verified}', 'true');

-- Array append
UPDATE docs SET data = jsonb_set(data, '{tags}', (data->'tags') || '"new"');

-- Aggregate
SELECT jsonb_agg(jsonb_build_object('id', id, 'name', name)) FROM users;
```

## Troubleshooting

| Error | Cause | Solution |
|-------|-------|----------|
| `22P02` | Invalid JSON | Validate syntax |
| Slow @> | No GIN index | Create GIN index |
| NULL path | Key missing | Check with ? |

## Usage

```
Skill("postgresql-json")
```
