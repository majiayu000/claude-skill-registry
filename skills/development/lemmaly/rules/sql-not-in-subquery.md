---
id: sql-not-in-subquery
title: NOT IN (subquery) — null-unsafe; usually slower than NOT EXISTS
severity: warning
impact: HIGH
impactDescription: Hot-path or correctness risk at realistic n
language: sql
tags: sql, warning, invariant-guard
---

# NOT IN (subquery) — null-unsafe; usually slower than NOT EXISTS

`NOT IN (subquery)` is null-unsafe: if any row in the subquery is NULL, the whole predicate is NULL (not TRUE), and the outer row is dropped. `NOT EXISTS` is null-safe and usually has a better plan.

## Fix

Rewrite as `WHERE NOT EXISTS (SELECT 1 FROM ... WHERE ...)`.

## Incorrect

```sql
SELECT * FROM orders
WHERE user_id NOT IN (SELECT id FROM banned_users);
-- One NULL in banned_users.id → returns zero rows
```

## Correct

```sql
SELECT o.* FROM orders o
WHERE NOT EXISTS (
  SELECT 1 FROM banned_users b WHERE b.id = o.user_id
);
```

## Escalate to

If this pattern is widespread in the codebase, load **invariant-guard** for the corrective workflow.
