---
name: database-design-patterns
description: Schema design, normalization decisions, indexing strategies, and migration safety for relational databases. Use when designing tables, choosing between normalize vs denormalize, selecting index
  types, planning zero-downtime migrations, or setting up connection pooling. Activate on "schema design", "normalization", "denormalization", "foreign key", "index strategy", "migration", "connection pooling",
  "composite key", "surrogate key", "soft delete", "polymorphic association". NOT for PostgreSQL-specific query tuning or EXPLAIN analysis (use postgresql-optimization), NoSQL or document database design,
  or cloud database provisioning.
allowed-tools: Read,Write,Edit,Grep,Glob
metadata:
  category: Design & Creative
  tags:
  - database
  - design
  - patterns
  - schema-design
  - normalization
  pairs-with:
  - skill: drizzle-migrations
    reason: Schema design decisions are implemented through ORM migration workflows
  - skill: postgresql-optimization
    reason: Index strategies and query patterns depend on underlying schema design choices
  - skill: supabase-admin
    reason: Supabase RLS policies and schema architecture implement database design patterns
---

# Database Design Patterns

Relational database schema design expert. Covers normalization decisions, index selection, migration safety, and connection pooling — the structural foundations that determine whether a database performs well at scale or becomes a maintenance burden.

## When to Use

Use for:
- Designing new schemas or refactoring existing ones
- Deciding whether to normalize or denormalize for a specific query pattern
- Choosing index types (B-tree, GIN, GiST, hash, partial, covering)
- Planning migrations that must not break running production systems
- Implementing soft deletes, polymorphic associations, or composite keys
- Configuring PgBouncer or Prisma connection pools

NOT for:
- Running EXPLAIN ANALYZE or reading query plans → use **postgresql-optimization**
- Document model design (MongoDB, DynamoDB) → use a NoSQL skill
- Database provisioning, replicas, or infrastructure → use a cloud/infra skill
- ORM-specific code generation → use the relevant ORM skill

---

## Normalize vs. Denormalize Decision Tree

```mermaid
flowchart TD
    A[New data or query performance problem?] --> B{New data design?}
    B -->|Yes| C[Start normalized: 3NF]
    B -->|No — query too slow| D{Measured with EXPLAIN?}
    D -->|No| E[Measure first. Never guess.]
    D -->|Yes — proven join bottleneck| F{Read-heavy or write-heavy?}
    F -->|Read-heavy, joins are the bottleneck| G[Controlled denormalization:\nmaterialized view or cached column]
    F -->|Write-heavy or balanced| H[Keep normalized.\nOptimize query or add index first.]
    C --> I{Any repeated groups in a row?}
    I -->|Yes| J[1NF: Move to child table]
    I -->|No| K{Non-key cols depend on part of PK?}
    K -->|Yes| L[2NF: Extract to separate table]
    K -->|No| M{Transitive dependencies?}
    M -->|Yes| N[3NF: Extract lookup table]
    M -->|No| O[Schema is 3NF — ship it]
```

**The rule**: Start at 3NF. Denormalize only after measuring, and only the specific join that is provably too slow. Never denormalize speculatively.

---

## Index Selection Decision Tree

```mermaid
flowchart TD
    A[Which index type?] --> B{Data type and query pattern}
    B -->|Equality or range on scalar| C[B-tree — default choice]
    B -->|Full-text search, arrays, JSONB| D[GIN — inverted index]
    B -->|Geometric / PostGIS types| E[GiST — generalized search]
    B -->|Exact equality only, very high cardinality| F[Hash — rare, limited utility]
    C --> G{Subset of rows frequently queried?}
    G -->|Yes, e.g. status = 'active'| H[Partial index:\nWHERE status = 'active']
    G -->|No| I{Query selects only indexed columns?}
    I -->|Yes| J[Covering index:\nINCLUDE additional columns]
    I -->|No| K[Standard B-tree index]
```

**Always index**:
- Every foreign key column (prevents full table scans on joins)
- Columns that appear in WHERE, ORDER BY, or JOIN ON clauses in frequent queries
- Composite indexes: put the most selective column first

**Consult** `references/indexing-strategies.md` when choosing between partial vs. covering indexes or tuning multi-column index column order.

---

## Migration Safety Decision Tree

```mermaid
flowchart TD
    A[Schema change needed] --> B{Breaking change?}
    B -->|No: add nullable column, add index| C[Single migration, safe to run]
    B -->|Yes: rename column, change type, drop column| D[Expand-Contract pattern]
    D --> E[Phase 1 — Expand:\nAdd new column/table, keep old]
    E --> F[Deploy app: write to both old and new]
    F --> G[Backfill existing rows to new column]
    G --> H[Phase 2 — Contract:\nRemove old column once all reads use new]
    H --> I[Deploy app: read only from new]
    I --> J[Drop old column in final migration]
    C --> K{Large table?}
    K -->|Yes| L[CREATE INDEX CONCURRENTLY\nALTER TABLE with minimal lock]
    K -->|No| M[Standard migration]
```

**Consult** `references/migration-patterns.md` for expand-contract templates, lock timeout settings, and rollback strategies.

---

## Normalization Reference

### 1NF — No Repeating Groups
Each column holds one value. No comma-separated lists in a column.

```sql
-- Bad: tags stored as CSV
CREATE TABLE articles (
  id SERIAL PRIMARY KEY,
  tags TEXT  -- "sql,indexing,performance"
);

-- Good: normalized to child table
CREATE TABLE article_tags (
  article_id INT REFERENCES articles(id),
  tag TEXT NOT NULL,
  PRIMARY KEY (article_id, tag)
);
```

### 2NF — No Partial Dependencies (composite PKs only)
Every non-key column depends on the whole primary key, not just part of it.

```sql
-- Bad: product_name depends only on product_id, not on (order_id, product_id)
CREATE TABLE order_items (
  order_id INT,
  product_id INT,
  product_name TEXT,  -- should be in products table
  quantity INT,
  PRIMARY KEY (order_id, product_id)
);
```

### 3NF — No Transitive Dependencies
Non-key columns depend only on the primary key, not on each other.

```sql
-- Bad: zip_code determines city/state (transitive)
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  zip_code TEXT,
  city TEXT,    -- derivable from zip_code
  state TEXT    -- derivable from zip_code
);

-- Good: extract lookup table
CREATE TABLE zip_codes (
  zip TEXT PRIMARY KEY,
  city TEXT,
  state TEXT
);
```

---

## Key Design Decisions

### Surrogate vs. Composite Keys

Use surrogate keys (serial/UUID) when:
- The natural key is multi-column and would be repeated in child tables as FK
- The natural key can change (email addresses, usernames)
- The table will be referenced by many other tables

Use composite primary keys when:
- The table is a pure join/association table with no additional attributes
- The combination is truly stable and globally unique

```sql
-- Pure join table: composite PK is correct
CREATE TABLE user_roles (
  user_id INT REFERENCES users(id),
  role_id INT REFERENCES roles(id),
  PRIMARY KEY (user_id, role_id)
);

-- Association with attributes: add surrogate key
CREATE TABLE user_project_memberships (
  id SERIAL PRIMARY KEY,
  user_id INT REFERENCES users(id),
  project_id INT REFERENCES projects(id),
  joined_at TIMESTAMPTZ DEFAULT NOW(),
  role TEXT
);
```

### Soft Deletes

```sql
-- Pattern: deleted_at nullable timestamp
ALTER TABLE orders ADD COLUMN deleted_at TIMESTAMPTZ;

-- Partial index makes "active" queries fast
CREATE INDEX idx_orders_active ON orders (user_id, created_at)
WHERE deleted_at IS NULL;

-- View hides soft-deleted rows for application code
CREATE VIEW active_orders AS
  SELECT * FROM orders WHERE deleted_at IS NULL;
```

**Warning**: Soft deletes complicate unique constraints. A unique email column allows only one deleted user with that email. Use partial unique indexes:

```sql
CREATE UNIQUE INDEX idx_users_email_active ON users (email)
WHERE deleted_at IS NULL;
```

### Polymorphic Associations

Two approaches — avoid the naive pattern:

```sql
-- Bad: nullable FK columns for each possible parent type
CREATE TABLE comments (
  id SERIAL PRIMARY KEY,
  post_id INT REFERENCES posts(id),      -- nullable
  article_id INT REFERENCES articles(id), -- nullable
  video_id INT REFERENCES videos(id),     -- nullable
  body TEXT
);

-- Good: separate association tables (referential integrity preserved)
CREATE TABLE post_comments (
  comment_id INT REFERENCES comments(id),
  post_id INT REFERENCES posts(id),
  PRIMARY KEY (comment_id, post_id)
);

-- Or: single-table inheritance with a type column + CHECK constraint
CREATE TABLE comments (
  id SERIAL PRIMARY KEY,
  parent_type TEXT NOT NULL CHECK (parent_type IN ('post', 'article', 'video')),
  parent_id INT NOT NULL,
  body TEXT
);
CREATE INDEX idx_comments_parent ON comments (parent_type, parent_id);
```

### Connection Pooling

PgBouncer configuration for typical web applications:

```ini
[pgbouncer]
pool_mode = transaction        ; Best for short-lived web requests
max_client_conn = 1000         ; Total client connections pooler accepts
default_pool_size = 20         ; DB connections per database/user pair
server_idle_timeout = 600      ; Close idle server connections after 10 min
```

Prisma with PgBouncer — set `pgbouncer=true` in the connection URL:
```
DATABASE_URL="postgresql://user:pass@host:6432/db?pgbouncer=true&connection_limit=1"
```

**Note**: PgBouncer transaction mode does not support prepared statements, `SET`, or `LISTEN/NOTIFY`. Use session mode if your ORM requires prepared statements and pool size is manageable.

---

## Anti-Patterns

### Anti-Pattern: Premature Denormalization

**Novice**: "Joins are slow, so I'll copy data into the main table to avoid them."

**Expert**: Joins are fast when indexes exist. Copying data creates update anomalies — the same fact stored in two places that can diverge. The correct sequence is: normalize first, measure query time under real load, identify the specific join bottleneck with EXPLAIN ANALYZE, then consider a materialized view or a single cached denormalized column as a last resort.

**Detection**: Look for columns like `user_name` on an `orders` table alongside a `user_id` FK to a `users` table. If `users.name` can change, `orders.user_name` will drift.

**LLM mistake**: Training data contains many tutorials that denormalize early as a "performance optimization." These predate widespread index-aware ORMs and assume manual query writing.

---

### Anti-Pattern: Missing Indexes on Foreign Keys

**Novice**: "The database will figure out how to join — I just need the FK constraint."

**Expert**: A foreign key constraint enforces referential integrity but creates no index. A `JOIN orders ON orders.user_id = users.id` with no index on `orders.user_id` causes a full sequential scan of the `orders` table for every user. On a table with millions of rows this is catastrophic.

**Detection**:
```sql
-- Find FK columns with no index (PostgreSQL)
SELECT
  tc.table_name,
  kcu.column_name
FROM information_schema.table_constraints tc
JOIN information_schema.key_column_usage kcu
  ON tc.constraint_name = kcu.constraint_name
LEFT JOIN pg_indexes pi
  ON pi.tablename = tc.table_name
  AND pi.indexdef LIKE '%' || kcu.column_name || '%'
WHERE tc.constraint_type = 'FOREIGN KEY'
  AND pi.indexname IS NULL;
```

**Fix**: Add an index on every FK column, always with `CONCURRENTLY` on a live table.

---

### Anti-Pattern: SELECT * in Production Queries

**Novice**: "SELECT * is fine — the database only fetches what I need."

**Expert**: `SELECT *` fetches all columns including large TEXT, JSONB, and BYTEA columns you don't use. It prevents index-only scans (the query must hit the heap even if an index covers the query). It breaks when columns are added or reordered in ORMs that rely on positional column binding. Always name columns explicitly.

**Detection**: Search application code for `SELECT *` in any query that runs in a hot path. In ORMs, check if `.findAll()` or equivalent selects all columns by default and add explicit field selection.

---

## References

- `references/indexing-strategies.md` — Consult when choosing between B-tree, GIN, GiST, hash, partial, and covering indexes; includes index-only scan prerequisites and multi-column index ordering rules.
- `references/migration-patterns.md` — Consult when planning zero-downtime migrations; covers expand-contract pattern, lock timeout settings, backfill chunking, and rollback strategies.
