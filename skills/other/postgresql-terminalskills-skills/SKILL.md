---
name: postgresql
description: >-
  Assists with designing schemas, writing performant queries, managing indexes, and operating
  PostgreSQL databases. Use when working with JSONB, full-text search, window functions,
  CTEs, row-level security, replication, or performance tuning. Trigger words: postgresql,
  postgres, sql, database, jsonb, rls, window functions, cte.
license: Apache-2.0
compatibility: "No special requirements"
metadata:
  author: terminal-skills
  version: "1.0.0"
  category: data-ai
  tags: ["postgresql", "database", "sql", "relational", "jsonb"]
---

# PostgreSQL

## Overview

PostgreSQL is an advanced relational database with features that often eliminate the need for separate tools: JSONB for semi-structured data, built-in full-text search, window functions for analytics, recursive CTEs for hierarchical queries, row-level security for multi-tenant isolation, and streaming replication for high availability. It supports partitioning, multiple index types (B-tree, GIN, GiST, BRIN), and connection pooling via PgBouncer.

## Instructions

- When designing schemas, use `UUID` primary keys with `gen_random_uuid()`, `TIMESTAMP WITH TIME ZONE` for all timestamps, appropriate constraints (CHECK, UNIQUE, foreign keys with ON DELETE), and partitioning for time-series data.
- When working with JSON, use `JSONB` for truly dynamic data with GIN indexes for containment queries, but prefer proper columns for known fields since they provide better validation and performance.
- When optimizing queries, add indexes based on `EXPLAIN ANALYZE` output rather than guesswork, use partial indexes for filtered queries, expression indexes for computed values, and covering indexes with `INCLUDE` for index-only scans.
- When building full-text search, create `tsvector` generated columns with GIN indexes, use `ts_rank()` for relevance scoring, and choose the appropriate language configuration for stemming.
- When implementing multi-tenancy, use row-level security (RLS) policies for database-level isolation rather than application-level checks, setting the user context via `current_setting()`.
- When managing production databases, use PgBouncer for connection pooling, monitor with `pg_stat_statements`, run `VACUUM ANALYZE` after bulk operations, and set up streaming replication with Patroni for high availability.

## Examples

### Example 1: Design a multi-tenant SaaS database with RLS

**User request:** "Set up a PostgreSQL database with row-level security for multi-tenant isolation"

**Actions:**
1. Create tables with a `tenant_id` column and `UUID` primary keys
2. Enable RLS with `ALTER TABLE ... ENABLE ROW LEVEL SECURITY`
3. Create policies using `current_setting('app.tenant_id')` for per-request isolation
4. Set up connection pooling with PgBouncer and configure `app.tenant_id` per connection

**Output:** A multi-tenant database where tenant data is isolated at the database level, preventing cross-tenant data leaks.

### Example 2: Add full-text search to a content platform

**User request:** "Implement search across articles with relevance ranking and highlighting"

**Actions:**
1. Add a `search_vector` generated column using `to_tsvector('english', title || ' ' || body)`
2. Create a GIN index on the search vector column
3. Build a search query using `@@` with `plainto_tsquery()` and rank results with `ts_rank()`
4. Add `ts_headline()` for highlighting matched terms in results

**Output:** A fast full-text search with relevance ranking, highlighting, and GIN index-backed performance.

## Guidelines

- Use `UUID` primary keys to avoid sequential ID enumeration and merge conflicts.
- Use `TIMESTAMP WITH TIME ZONE` for all timestamps; never use `TIMESTAMP` which loses timezone context.
- Add indexes based on `EXPLAIN ANALYZE` output, not guesswork; measure before optimizing.
- Use connection pooling (PgBouncer) for applications with more than 20 connections since PostgreSQL forks a process per connection.
- Use RLS for multi-tenant applications since database-level isolation is more reliable than application-level checks.
- Use `JSONB` for truly dynamic data, not as a replacement for proper columns.
- Run `VACUUM ANALYZE` after bulk operations since stale statistics lead to bad query plans.
