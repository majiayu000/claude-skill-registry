---
id: sql-leading-wildcard-like
title: LIKE with leading wildcard — cannot use a B-tree index
severity: warning
impact: HIGH
impactDescription: Hot-path or correctness risk at realistic n
language: sql
tags: sql, warning
---

# LIKE with leading wildcard — cannot use a B-tree index

A B-tree index sorts by prefix. `LIKE '%foo'` cannot use it — the query scans the table. Use a trigram index (Postgres `pg_trgm`), reverse the column for suffix search, or a full-text search index.

## Fix

Use a trigram index (pg_trgm), full-text search, or a reversed-column index.

## Incorrect

```sql
SELECT * FROM products WHERE name LIKE '%phone';
```

## Correct

```sql
-- Postgres: GIN index on trigrams
CREATE INDEX products_name_trgm ON products USING gin (name gin_trgm_ops);
SELECT * FROM products WHERE name ILIKE '%phone%';

-- Or full-text:
SELECT * FROM products WHERE to_tsvector(name) @@ to_tsquery('phone');
```
