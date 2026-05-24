---
id: sql-select-no-limit
title: SELECT without LIMIT — unbounded result set
severity: info
impact: MEDIUM
impactDescription: Suboptimal; flag when n is large or on a hot path
language: sql
tags: sql, info
---

# SELECT without LIMIT — unbounded result set

A query with no `LIMIT` returns however many rows match. On a small table this is fine; on a growing one it eventually OOMs the client or the page. Add a bound, or paginate.

## Fix

Add LIMIT, or paginate by id range. Unbounded reads OOM under growth.

## Incorrect

```sql
SELECT id, email FROM users ORDER BY created_at DESC;
```

## Correct

```sql
SELECT id, email FROM users
ORDER BY created_at DESC
LIMIT 100;

-- Keyset pagination for next page:
SELECT id, email FROM users
WHERE created_at < $1
ORDER BY created_at DESC
LIMIT 100;
```
