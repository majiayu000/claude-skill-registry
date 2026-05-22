---
name: postgres-best-practices
description: PostgreSQL and Supabase optimization guide.
category: development
version: 4.1.0-fractal
layer: master-skill
---

# PostgreSQL Best Practices

> **Goal**: Design scalable, secure, and performant database schemas and queries, specifically optimized for Supabase/PostgreSQL environments.

## 1. Schema Design

- **Normalization**: Aim for 3NF (Third Normal Form) to reduce redundancy.
- **Primary Keys**: Use `UUID` (v7 or v4) or `BIGINT` (Identity) for primary keys. Avoid simplistic auto-increment `INT` if scaling horizontally.
- **Naming**: Use `snake_case` for table and column names. Plural for tables (`users`, `orders`).
- **Foreign Keys**: Always define foreign key constraints to ensure data integrity. Index all FK columns.

## 2. Performance & Indexing

- **Indexes**:
    - **B-Tree**: Default for equality and range queries.
    - **GIN**: For JSONB and Full-Text Search (`tsvector`).
    - **GiST**: For Geo-spatial data (`PostGIS`).
- **Composite Indexes**: Create composite indexes for columns frequently queried together (order matters: equality first, then range).
- **Explain Analyze**: Always check `EXPLAIN ANALYZE` on complex queries to verify index usage.

## 3. Security (Row Level Security - RLS)

- **Enable RLS**: `ALTER TABLE "table_name" ENABLE ROW LEVEL SECURITY;`
- **Policies**: Define strict policies for `SELECT`, `INSERT`, `UPDATE`, `DELETE`.
    - *Example*: `auth.uid() = user_id` for user-private data.
- **Service Role**: Use service role keys only for backend admin tasks; never expose to client.

## 4. JSONB vs Relational

- **When to use JSONB**:
    - Dynamic payload (e.g., webhook responses, configuration settings).
    - Data structure varies significantly per row.
- **When NOT to use JSONB**:
    - Data that needs frequent joining or aggregating.
    - Data that requires foreign key constraints.

## 5. Application Usage (Prisma/Supabase JS)

- **Connection Pooling**: Use Supabase Transaction Pooler (port 6543) for serverless functions to avoid connection exhaustion.
- **N+1 Problem**: Be wary of N+1 queries in ORMs (Prisma). Use `.include()` or explicit joins carefully.

---

**Supabase Specific**:
- **Realtime**: Only enable Realtime for tables that specifically need it (to save resources).
- **Storage**: Use RLS policies for Storage Buckets file access as well.
