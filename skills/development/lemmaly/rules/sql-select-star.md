---
id: sql-select-star
title: SELECT * — fetches unused columns; blocks index-only scans
severity: warning
impact: HIGH
impactDescription: Hot-path or correctness risk at realistic n
language: sql
tags: sql, warning
---

# SELECT * — fetches unused columns; blocks index-only scans

`SELECT *` fetches every column, defeating index-only scans, inflating wire traffic, and breaking downstream code when a column is added/renamed. Project only what you need.

## Fix

Name the columns. Smaller payload and more covering-index opportunities.

## Incorrect

```sql
SELECT * FROM users WHERE id = $1;
```

## Correct

```sql
SELECT id, email, created_at FROM users WHERE id = $1;
```
