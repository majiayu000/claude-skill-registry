---
name: postgresql-advanced-queries
description: Master advanced PostgreSQL queries - CTEs, window functions, recursive queries
version: "3.0.0"
sasmp_version: "1.3.0"
bonded_agent: 02-postgresql-queries
bond_type: PRIMARY_BOND
category: database
difficulty: intermediate
estimated_time: 3h
---

# PostgreSQL Advanced Queries Skill

> Atomic skill for complex query patterns

## Overview

Production-ready patterns for CTEs, window functions, recursive queries, and advanced joins.

## Prerequisites

- PostgreSQL 16+
- Intermediate SQL knowledge

## Parameters

```yaml
parameters:
  query_type:
    type: string
    required: true
    enum: [cte, window, recursive, lateral, aggregate]
  tables:
    type: array
    items: { type: string }
```

## Quick Reference

### CTE Pattern
```sql
WITH step1 AS (SELECT ...), step2 AS (SELECT ... FROM step1)
SELECT * FROM step2;
```

### Window Functions
```sql
ROW_NUMBER() OVER (PARTITION BY cat ORDER BY date DESC)
SUM(amount) OVER (ORDER BY date)  -- Running total
LAG(value, 1) OVER (ORDER BY date)  -- Previous row
```

### Recursive Query
```sql
WITH RECURSIVE tree AS (
    SELECT id, parent_id, 1 as level FROM items WHERE parent_id IS NULL
    UNION ALL
    SELECT i.id, i.parent_id, t.level + 1 FROM items i JOIN tree t ON i.parent_id = t.id
)
SELECT * FROM tree;
```

### LATERAL Join
```sql
SELECT u.*, r.* FROM users u
CROSS JOIN LATERAL (SELECT * FROM orders WHERE user_id = u.id LIMIT 3) r;
```

## Test Template

```sql
DO $$ DECLARE result NUMERIC; BEGIN
    CREATE TEMP TABLE test_sales (id INT, amount NUMERIC);
    INSERT INTO test_sales VALUES (1, 100), (2, 200);
    SELECT SUM(amount) OVER (ORDER BY id) INTO result FROM test_sales WHERE id = 2;
    ASSERT result = 300, 'Running total should be 300';
    DROP TABLE test_sales;
END $$;
```

## Troubleshooting

| Error | Cause | Solution |
|-------|-------|----------|
| `42803` | GROUP BY error | Add missing columns |
| `54001` | Too complex | Break into CTEs |
| `21000` | Multiple rows | Add LIMIT 1 |

## Usage

```
Skill("postgresql-advanced-queries")
```
