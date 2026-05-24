---
id: sql-or-in-where
title: OR in WHERE — can prevent index use
severity: info
impact: MEDIUM
impactDescription: Suboptimal; flag when n is large or on a hot path
language: sql
tags: sql, info
---

# OR in WHERE — can prevent index use

A query planner can use an index on one side of an `OR` but often not both, falling back to a sequential scan. `UNION ALL` or `IN (...)` (when both sides are equality on the same column) usually wins.

## Fix

Equality on same column → `WHERE col IN (...)`. Otherwise consider UNION ALL.

## Incorrect

```sql
SELECT * FROM events
WHERE user_id = $1 OR account_id = $1;
```

## Correct

```sql
SELECT * FROM events WHERE user_id = $1
UNION ALL
SELECT * FROM events WHERE account_id = $1;

-- Or, when both sides are the same column:
SELECT * FROM events WHERE user_id IN ($1, $2, $3);
```
