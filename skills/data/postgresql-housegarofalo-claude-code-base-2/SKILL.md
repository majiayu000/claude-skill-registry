---
name: postgresql
description: Design, optimize, and manage PostgreSQL databases. Covers indexing, pgvector for AI embeddings, JSON operations, full-text search, and query optimization. Use when working with PostgreSQL, database design, or building data-intensive applications.
---

# PostgreSQL Skill

Expert guidance for PostgreSQL database design, optimization, and advanced features including pgvector for AI embeddings.

## Triggers

Use this skill when:
- Designing PostgreSQL database schemas or normalization
- Creating indexes (B-tree, GIN, GiST, BRIN)
- Working with pgvector for AI embeddings and similarity search
- Implementing JSON/JSONB operations
- Building full-text search functionality
- Writing window functions, CTEs, or recursive queries
- Tuning PostgreSQL performance
- Implementing table partitioning
- Setting up backup and restore procedures
- Keywords: postgresql, postgres, pgvector, jsonb, full-text search, database indexing, sql optimization, partitioning, cte

## Table of Contents

- [Database Design & Normalization](#database-design--normalization)
- [Index Types & Strategies](#index-types--strategies)
- [pgvector for AI Embeddings](#pgvector-for-ai-embeddings)
- [JSON/JSONB Operations](#jsonjsonb-operations)
- [Full-Text Search](#full-text-search)
- [Window Functions](#window-functions)
- [CTEs & Recursive Queries](#ctes--recursive-queries)
- [Performance Tuning](#performance-tuning)
- [Table Partitioning](#table-partitioning)
- [Backup & Restore](#backup--restore)

---

## Database Design & Normalization

### Normalization Levels

```sql
-- 1NF: Atomic values, no repeating groups
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 2NF: No partial dependencies (all non-key columns depend on entire PK)
CREATE TABLE order_items (
    order_id INTEGER REFERENCES orders(id),
    product_id INTEGER REFERENCES products(id),
    quantity INTEGER NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,  -- Price at time of order
    PRIMARY KEY (order_id, product_id)
);

-- 3NF: No transitive dependencies
CREATE TABLE addresses (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    street VARCHAR(255),
    city VARCHAR(100),
    state VARCHAR(50),
    postal_code VARCHAR(20),
    country VARCHAR(100)
);
```

### Strategic Denormalization

```sql
-- Denormalized for read-heavy analytics
CREATE TABLE order_analytics (
    id SERIAL PRIMARY KEY,
    order_id INTEGER,
    user_id INTEGER,
    user_email VARCHAR(255),      -- Denormalized
    user_name VARCHAR(200),       -- Denormalized
    product_count INTEGER,        -- Pre-computed
    total_amount DECIMAL(12,2),   -- Pre-computed
    order_date DATE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Materialized view for complex aggregations
CREATE MATERIALIZED VIEW monthly_sales AS
SELECT
    DATE_TRUNC('month', order_date) AS month,
    COUNT(*) AS order_count,
    SUM(total_amount) AS revenue,
    AVG(total_amount) AS avg_order_value
FROM orders
GROUP BY DATE_TRUNC('month', order_date)
WITH DATA;

-- Refresh strategy
REFRESH MATERIALIZED VIEW CONCURRENTLY monthly_sales;
```

### Essential Constraints

```sql
-- Comprehensive table with constraints
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    sku VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    price DECIMAL(10,2) NOT NULL CHECK (price >= 0),
    stock_quantity INTEGER DEFAULT 0 CHECK (stock_quantity >= 0),
    category_id INTEGER REFERENCES categories(id) ON DELETE SET NULL,
    status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active', 'inactive', 'discontinued')),
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Trigger for updated_at
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER products_updated_at
    BEFORE UPDATE ON products
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at();
```

---

## Index Types & Strategies

### B-tree Indexes (Default)

```sql
-- Standard B-tree for equality and range queries
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_orders_created ON orders(created_at DESC);

-- Composite index (column order matters!)
CREATE INDEX idx_orders_user_date ON orders(user_id, created_at DESC);

-- Partial index for filtered queries
CREATE INDEX idx_active_orders ON orders(created_at)
WHERE status = 'active';

-- Expression index
CREATE INDEX idx_users_email_lower ON users(LOWER(email));

-- Unique index
CREATE UNIQUE INDEX idx_users_email_unique ON users(email);
```

### GIN Indexes (Generalized Inverted)

```sql
-- For JSONB containment queries
CREATE INDEX idx_products_metadata ON products USING GIN(metadata);

-- Query using GIN index
SELECT * FROM products WHERE metadata @> '{"featured": true}';
SELECT * FROM products WHERE metadata ? 'discount';

-- For array columns
CREATE TABLE articles (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255),
    tags TEXT[]
);
CREATE INDEX idx_articles_tags ON articles USING GIN(tags);

-- Query arrays
SELECT * FROM articles WHERE tags @> ARRAY['postgresql', 'database'];
SELECT * FROM articles WHERE 'sql' = ANY(tags);

-- For full-text search
CREATE INDEX idx_articles_fts ON articles USING GIN(to_tsvector('english', title));
```

### GiST Indexes (Generalized Search Tree)

```sql
-- For geometric/spatial data
CREATE EXTENSION IF NOT EXISTS postgis;

CREATE TABLE locations (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    coordinates GEOMETRY(Point, 4326)
);

CREATE INDEX idx_locations_geo ON locations USING GIST(coordinates);

-- Range types
CREATE TABLE reservations (
    id SERIAL PRIMARY KEY,
    room_id INTEGER,
    during TSTZRANGE NOT NULL,
    EXCLUDE USING GIST (room_id WITH =, during WITH &&)
);

-- Query spatial data
SELECT * FROM locations
WHERE ST_DWithin(
    coordinates,
    ST_SetSRID(ST_MakePoint(-122.4194, 37.7749), 4326),
    1000  -- meters
);
```

### BRIN Indexes (Block Range)

```sql
-- Excellent for naturally ordered data (time-series)
CREATE TABLE sensor_readings (
    id BIGSERIAL PRIMARY KEY,
    sensor_id INTEGER,
    reading_value DECIMAL(10,4),
    recorded_at TIMESTAMPTZ DEFAULT NOW()
);

-- BRIN is much smaller than B-tree for ordered data
CREATE INDEX idx_readings_time ON sensor_readings USING BRIN(recorded_at);

-- Best for append-only tables with natural ordering
```

### Index Maintenance

```sql
-- Check index usage
SELECT
    indexrelname AS index_name,
    idx_scan AS times_used,
    idx_tup_read AS tuples_read,
    idx_tup_fetch AS tuples_fetched,
    pg_size_pretty(pg_relation_size(indexrelid)) AS size
FROM pg_stat_user_indexes
ORDER BY idx_scan DESC;

-- Find unused indexes
SELECT indexrelname, idx_scan
FROM pg_stat_user_indexes
WHERE idx_scan = 0 AND indexrelname NOT LIKE '%_pkey';

-- Rebuild bloated indexes
REINDEX INDEX CONCURRENTLY idx_users_email;
```

---

## pgvector for AI Embeddings

### Setup

```sql
-- Install extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Create table with vector column
CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    content TEXT,
    embedding vector(1536),  -- OpenAI ada-002 dimensions
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

### Vector Indexes

```sql
-- IVFFlat index (faster build, good for < 1M vectors)
CREATE INDEX idx_documents_embedding_ivf ON documents
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

-- HNSW index (slower build, better recall, good for > 1M vectors)
CREATE INDEX idx_documents_embedding_hnsw ON documents
USING hnsw (embedding vector_cosine_ops)
WITH (m = 16, ef_construction = 64);

-- Distance operators:
-- vector_cosine_ops  - Cosine distance (<=>)
-- vector_l2_ops      - Euclidean distance (<->)
-- vector_ip_ops      - Inner product (<#>)
```

### Similarity Search

```sql
-- Find similar documents using cosine similarity
SELECT
    id,
    title,
    1 - (embedding <=> $1) AS similarity
FROM documents
ORDER BY embedding <=> $1  -- $1 is query embedding
LIMIT 10;

-- With metadata filter
SELECT id, title, 1 - (embedding <=> $1) AS similarity
FROM documents
WHERE metadata->>'category' = 'technical'
ORDER BY embedding <=> $1
LIMIT 10;

-- Hybrid search: vector + keyword
SELECT
    d.id,
    d.title,
    1 - (d.embedding <=> $1) AS vector_score,
    ts_rank(to_tsvector('english', d.content), plainto_tsquery($2)) AS text_score
FROM documents d
WHERE to_tsvector('english', d.content) @@ plainto_tsquery($2)
ORDER BY (1 - (d.embedding <=> $1)) * 0.7 +
         ts_rank(to_tsvector('english', d.content), plainto_tsquery($2)) * 0.3 DESC
LIMIT 10;
```

### RAG Pattern

```sql
-- Function for semantic search
CREATE OR REPLACE FUNCTION search_documents(
    query_embedding vector(1536),
    match_count INTEGER DEFAULT 5,
    similarity_threshold FLOAT DEFAULT 0.7
)
RETURNS TABLE (
    id INTEGER,
    title VARCHAR,
    content TEXT,
    similarity FLOAT
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        d.id,
        d.title,
        d.content,
        1 - (d.embedding <=> query_embedding) AS similarity
    FROM documents d
    WHERE 1 - (d.embedding <=> query_embedding) > similarity_threshold
    ORDER BY d.embedding <=> query_embedding
    LIMIT match_count;
END;
$$ LANGUAGE plpgsql;
```

---

## JSON/JSONB Operations

### Basic Operations

```sql
-- Insert JSONB data
INSERT INTO products (name, metadata) VALUES
('Laptop', '{"brand": "Dell", "specs": {"ram": 16, "storage": 512}}');

-- Access nested values
SELECT
    name,
    metadata->>'brand' AS brand,                    -- Text
    metadata->'specs'->>'ram' AS ram,               -- Nested text
    (metadata->'specs'->'ram')::INTEGER AS ram_int  -- Cast to integer
FROM products;

-- Path extraction
SELECT metadata #>> '{specs, storage}' AS storage FROM products;
```

### JSONB Operators

```sql
-- Containment (@>)
SELECT * FROM products WHERE metadata @> '{"brand": "Dell"}';

-- Key existence (?)
SELECT * FROM products WHERE metadata ? 'discount';
SELECT * FROM products WHERE metadata ?| ARRAY['discount', 'sale'];  -- Any key
SELECT * FROM products WHERE metadata ?& ARRAY['brand', 'specs'];    -- All keys

-- Update JSONB
UPDATE products
SET metadata = metadata || '{"featured": true}'
WHERE id = 1;

-- Set nested value
UPDATE products
SET metadata = jsonb_set(metadata, '{specs,ram}', '32')
WHERE id = 1;

-- Remove key
UPDATE products
SET metadata = metadata - 'discount';
```

### JSONB Aggregation

```sql
-- Build JSON from rows
SELECT jsonb_agg(
    jsonb_build_object(
        'id', id,
        'name', name,
        'price', price
    )
) AS products
FROM products
WHERE category_id = 1;

-- Object aggregation
SELECT jsonb_object_agg(sku, price) AS price_map
FROM products;

-- Expand JSONB to rows
SELECT
    p.id,
    elem->>'key' AS setting_key,
    elem->>'value' AS setting_value
FROM products p,
LATERAL jsonb_array_elements(p.metadata->'settings') AS elem;
```

---

## Full-Text Search

### Setup

```sql
-- Add tsvector column
ALTER TABLE articles ADD COLUMN search_vector tsvector;

-- Populate search vector
UPDATE articles SET search_vector =
    setweight(to_tsvector('english', COALESCE(title, '')), 'A') ||
    setweight(to_tsvector('english', COALESCE(content, '')), 'B');

-- Create GIN index
CREATE INDEX idx_articles_search ON articles USING GIN(search_vector);

-- Auto-update trigger
CREATE OR REPLACE FUNCTION articles_search_trigger()
RETURNS TRIGGER AS $$
BEGIN
    NEW.search_vector :=
        setweight(to_tsvector('english', COALESCE(NEW.title, '')), 'A') ||
        setweight(to_tsvector('english', COALESCE(NEW.content, '')), 'B');
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER articles_search_update
    BEFORE INSERT OR UPDATE ON articles
    FOR EACH ROW
    EXECUTE FUNCTION articles_search_trigger();
```

### Search Queries

```sql
-- Basic search
SELECT * FROM articles
WHERE search_vector @@ plainto_tsquery('english', 'postgresql database');

-- Phrase search
SELECT * FROM articles
WHERE search_vector @@ phraseto_tsquery('english', 'full text search');

-- Advanced query syntax
SELECT * FROM articles
WHERE search_vector @@ to_tsquery('english', 'postgres & (performance | optimization)');

-- Ranked results with highlights
SELECT
    id,
    title,
    ts_rank(search_vector, query) AS rank,
    ts_headline('english', content, query,
        'StartSel=<mark>, StopSel=</mark>, MaxWords=50') AS snippet
FROM articles, plainto_tsquery('english', 'postgresql optimization') query
WHERE search_vector @@ query
ORDER BY rank DESC
LIMIT 10;
```

---

## Window Functions

### Ranking Functions

```sql
-- ROW_NUMBER, RANK, DENSE_RANK
SELECT
    name,
    category,
    price,
    ROW_NUMBER() OVER (ORDER BY price DESC) AS row_num,
    RANK() OVER (ORDER BY price DESC) AS rank,
    DENSE_RANK() OVER (ORDER BY price DESC) AS dense_rank
FROM products;

-- Partition by category
SELECT
    name,
    category,
    price,
    ROW_NUMBER() OVER (PARTITION BY category ORDER BY price DESC) AS category_rank
FROM products;

-- NTILE for percentiles
SELECT
    name,
    price,
    NTILE(4) OVER (ORDER BY price) AS price_quartile
FROM products;
```

### Aggregate Windows

```sql
-- Running totals
SELECT
    order_date,
    amount,
    SUM(amount) OVER (ORDER BY order_date) AS running_total,
    AVG(amount) OVER (ORDER BY order_date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS moving_avg_7d
FROM orders;

-- Comparison with previous/next
SELECT
    order_date,
    amount,
    LAG(amount, 1) OVER (ORDER BY order_date) AS prev_amount,
    LEAD(amount, 1) OVER (ORDER BY order_date) AS next_amount,
    amount - LAG(amount, 1) OVER (ORDER BY order_date) AS change
FROM orders;

-- First/Last in partition
SELECT DISTINCT
    category,
    FIRST_VALUE(name) OVER (PARTITION BY category ORDER BY price DESC) AS most_expensive,
    LAST_VALUE(name) OVER (
        PARTITION BY category
        ORDER BY price DESC
        RANGE BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    ) AS cheapest
FROM products;
```

---

## CTEs & Recursive Queries

### Standard CTEs

```sql
-- Multiple CTEs for complex queries
WITH
active_users AS (
    SELECT id, email, created_at
    FROM users
    WHERE status = 'active'
),
user_orders AS (
    SELECT
        user_id,
        COUNT(*) AS order_count,
        SUM(total) AS total_spent
    FROM orders
    WHERE created_at > NOW() - INTERVAL '1 year'
    GROUP BY user_id
)
SELECT
    au.email,
    COALESCE(uo.order_count, 0) AS orders,
    COALESCE(uo.total_spent, 0) AS spent
FROM active_users au
LEFT JOIN user_orders uo ON uo.user_id = au.id
ORDER BY spent DESC;
```

### Recursive CTEs

```sql
-- Hierarchical data (org chart, categories)
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    parent_id INTEGER REFERENCES categories(id)
);

-- Get all descendants
WITH RECURSIVE category_tree AS (
    -- Base case
    SELECT id, name, parent_id, 0 AS depth, ARRAY[id] AS path
    FROM categories
    WHERE parent_id IS NULL

    UNION ALL

    -- Recursive case
    SELECT c.id, c.name, c.parent_id, ct.depth + 1, ct.path || c.id
    FROM categories c
    INNER JOIN category_tree ct ON c.parent_id = ct.id
)
SELECT
    id,
    REPEAT('  ', depth) || name AS name,
    depth,
    path
FROM category_tree
ORDER BY path;

-- Get all ancestors
WITH RECURSIVE ancestors AS (
    SELECT id, name, parent_id
    FROM categories
    WHERE id = 42  -- Starting category

    UNION ALL

    SELECT c.id, c.name, c.parent_id
    FROM categories c
    INNER JOIN ancestors a ON c.id = a.parent_id
)
SELECT * FROM ancestors;
```

---

## Performance Tuning

### Query Analysis

```sql
-- Detailed execution plan
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT u.email, COUNT(o.id) AS order_count
FROM users u
LEFT JOIN orders o ON o.user_id = u.id
WHERE u.created_at > '2024-01-01'
GROUP BY u.id
HAVING COUNT(o.id) > 5
ORDER BY order_count DESC
LIMIT 10;

-- Key metrics to watch:
-- - Seq Scan vs Index Scan
-- - Rows estimated vs actual
-- - Buffers hit vs read
-- - Sort method (quicksort vs external merge)
```

### Configuration Tuning

```sql
-- Memory settings (adjust based on available RAM)
ALTER SYSTEM SET shared_buffers = '4GB';           -- 25% of RAM
ALTER SYSTEM SET effective_cache_size = '12GB';    -- 75% of RAM
ALTER SYSTEM SET work_mem = '256MB';               -- Per-operation memory
ALTER SYSTEM SET maintenance_work_mem = '1GB';     -- For VACUUM, INDEX

-- Query planner
ALTER SYSTEM SET random_page_cost = 1.1;           -- For SSDs (default 4.0)
ALTER SYSTEM SET effective_io_concurrency = 200;   -- For SSDs

-- Parallel queries
ALTER SYSTEM SET max_parallel_workers_per_gather = 4;
ALTER SYSTEM SET max_parallel_workers = 8;

-- Apply changes
SELECT pg_reload_conf();
```

### Common Optimizations

```sql
-- SLOW: Function on indexed column
SELECT * FROM users WHERE LOWER(email) = 'user@example.com';

-- FAST: Expression index or store lowercase
CREATE INDEX idx_users_email_lower ON users(LOWER(email));

-- SLOW: OR conditions
SELECT * FROM orders WHERE status = 'pending' OR status = 'processing';

-- FAST: Use IN or UNION ALL
SELECT * FROM orders WHERE status IN ('pending', 'processing');

-- SLOW: SELECT *
SELECT * FROM orders WHERE user_id = 1;

-- FAST: Select only needed columns
SELECT id, status, total FROM orders WHERE user_id = 1;

-- SLOW: OFFSET for pagination
SELECT * FROM products ORDER BY id LIMIT 10 OFFSET 10000;

-- FAST: Keyset pagination
SELECT * FROM products WHERE id > 10000 ORDER BY id LIMIT 10;
```

### Monitoring Queries

```sql
-- Slow query log
ALTER SYSTEM SET log_min_duration_statement = 1000; -- Log queries > 1s

-- Active queries
SELECT
    pid,
    NOW() - query_start AS duration,
    state,
    LEFT(query, 100) AS query_preview
FROM pg_stat_activity
WHERE state != 'idle'
ORDER BY duration DESC;

-- Table statistics
SELECT
    relname AS table,
    n_live_tup AS live_rows,
    n_dead_tup AS dead_rows,
    last_vacuum,
    last_autovacuum,
    last_analyze
FROM pg_stat_user_tables
ORDER BY n_dead_tup DESC;
```

---

## Table Partitioning

### Range Partitioning (Time-based)

```sql
-- Parent table
CREATE TABLE events (
    id BIGSERIAL,
    event_type VARCHAR(50),
    payload JSONB,
    created_at TIMESTAMPTZ NOT NULL,
    PRIMARY KEY (id, created_at)
) PARTITION BY RANGE (created_at);

-- Create partitions
CREATE TABLE events_2024_q1 PARTITION OF events
    FOR VALUES FROM ('2024-01-01') TO ('2024-04-01');

CREATE TABLE events_2024_q2 PARTITION OF events
    FOR VALUES FROM ('2024-04-01') TO ('2024-07-01');

-- Default partition for unmatched values
CREATE TABLE events_default PARTITION OF events DEFAULT;

-- Auto-create partitions (function)
CREATE OR REPLACE FUNCTION create_monthly_partition(table_name TEXT, partition_date DATE)
RETURNS VOID AS $$
DECLARE
    partition_name TEXT;
    start_date DATE;
    end_date DATE;
BEGIN
    partition_name := table_name || '_' || TO_CHAR(partition_date, 'YYYY_MM');
    start_date := DATE_TRUNC('month', partition_date);
    end_date := start_date + INTERVAL '1 month';

    EXECUTE FORMAT(
        'CREATE TABLE IF NOT EXISTS %I PARTITION OF %I FOR VALUES FROM (%L) TO (%L)',
        partition_name, table_name, start_date, end_date
    );
END;
$$ LANGUAGE plpgsql;
```

### List Partitioning

```sql
-- Partition by region
CREATE TABLE sales (
    id SERIAL,
    region VARCHAR(20) NOT NULL,
    amount DECIMAL(12,2),
    sale_date DATE,
    PRIMARY KEY (id, region)
) PARTITION BY LIST (region);

CREATE TABLE sales_americas PARTITION OF sales
    FOR VALUES IN ('US', 'CA', 'MX', 'BR');

CREATE TABLE sales_europe PARTITION OF sales
    FOR VALUES IN ('UK', 'DE', 'FR', 'IT');

CREATE TABLE sales_apac PARTITION OF sales
    FOR VALUES IN ('JP', 'CN', 'AU', 'IN');
```

### Hash Partitioning

```sql
-- Distribute by user_id
CREATE TABLE user_activity (
    id BIGSERIAL,
    user_id INTEGER NOT NULL,
    action VARCHAR(50),
    created_at TIMESTAMPTZ,
    PRIMARY KEY (id, user_id)
) PARTITION BY HASH (user_id);

CREATE TABLE user_activity_0 PARTITION OF user_activity
    FOR VALUES WITH (MODULUS 4, REMAINDER 0);
CREATE TABLE user_activity_1 PARTITION OF user_activity
    FOR VALUES WITH (MODULUS 4, REMAINDER 1);
CREATE TABLE user_activity_2 PARTITION OF user_activity
    FOR VALUES WITH (MODULUS 4, REMAINDER 2);
CREATE TABLE user_activity_3 PARTITION OF user_activity
    FOR VALUES WITH (MODULUS 4, REMAINDER 3);
```

---

## Backup & Restore

### pg_dump

```bash
# Full database backup
pg_dump -h localhost -U postgres -d mydb -F c -f backup.dump

# Schema only
pg_dump -h localhost -U postgres -d mydb --schema-only -f schema.sql

# Data only
pg_dump -h localhost -U postgres -d mydb --data-only -f data.sql

# Specific tables
pg_dump -h localhost -U postgres -d mydb -t users -t orders -F c -f tables.dump

# Exclude tables
pg_dump -h localhost -U postgres -d mydb --exclude-table='logs_*' -F c -f backup.dump

# Parallel dump (faster for large databases)
pg_dump -h localhost -U postgres -d mydb -F d -j 4 -f backup_dir/
```

### pg_restore

```bash
# Restore full database
pg_restore -h localhost -U postgres -d mydb -c backup.dump

# Restore specific tables
pg_restore -h localhost -U postgres -d mydb -t users backup.dump

# Parallel restore
pg_restore -h localhost -U postgres -d mydb -j 4 backup_dir/

# List contents of dump
pg_restore -l backup.dump
```

### Automated Backup Script

```bash
#!/bin/bash
# backup.sh - Automated PostgreSQL backup

DB_NAME="mydb"
BACKUP_DIR="/backups"
RETENTION_DAYS=30
DATE=$(date +%Y%m%d_%H%M%S)

# Create backup
pg_dump -h localhost -U postgres -d $DB_NAME -F c \
    -f "$BACKUP_DIR/${DB_NAME}_${DATE}.dump"

# Verify backup
if pg_restore -l "$BACKUP_DIR/${DB_NAME}_${DATE}.dump" > /dev/null 2>&1; then
    echo "Backup successful: ${DB_NAME}_${DATE}.dump"
else
    echo "Backup verification failed!"
    exit 1
fi

# Cleanup old backups
find $BACKUP_DIR -name "*.dump" -mtime +$RETENTION_DAYS -delete
```

---

## Quick Reference

### Common Data Types

| Type | Description | Example |
|------|-------------|---------|
| `SERIAL` | Auto-increment integer | `id SERIAL PRIMARY KEY` |
| `UUID` | Universal unique identifier | `id UUID DEFAULT gen_random_uuid()` |
| `VARCHAR(n)` | Variable-length string | `name VARCHAR(255)` |
| `TEXT` | Unlimited text | `content TEXT` |
| `INTEGER` | 4-byte integer | `quantity INTEGER` |
| `BIGINT` | 8-byte integer | `views BIGINT` |
| `DECIMAL(p,s)` | Exact numeric | `price DECIMAL(10,2)` |
| `TIMESTAMPTZ` | Timestamp with timezone | `created_at TIMESTAMPTZ` |
| `JSONB` | Binary JSON | `metadata JSONB` |
| `vector(n)` | pgvector embedding | `embedding vector(1536)` |

### Essential Extensions

```sql
-- UUID generation
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
-- or use gen_random_uuid() (built-in in PG13+)

-- Cryptographic functions
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- Vector similarity search
CREATE EXTENSION IF NOT EXISTS vector;

-- Full-text search dictionaries
CREATE EXTENSION IF NOT EXISTS unaccent;

-- Statistical functions
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;

-- Spatial data
CREATE EXTENSION IF NOT EXISTS postgis;
```

### Performance Checklist

- [ ] Index foreign keys
- [ ] Use partial indexes for filtered queries
- [ ] Configure shared_buffers (25% RAM)
- [ ] Set random_page_cost = 1.1 for SSDs
- [ ] Enable pg_stat_statements
- [ ] Regular VACUUM ANALYZE
- [ ] Use EXPLAIN ANALYZE for slow queries
- [ ] Consider partitioning for tables > 100M rows
- [ ] Use connection pooling (PgBouncer)
- [ ] Monitor with pg_stat_activity
