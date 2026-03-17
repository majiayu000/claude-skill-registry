---
name: postgres-migrations
description: Comprehensive guide to PostgreSQL migrations - common errors, generated columns, full-text search, indexes, idempotent migrations, and best practices for database schema changes
---

# PostgreSQL Migrations Skill

## Common PostgreSQL Migration Errors and Solutions

### 1. "Subquery uses ungrouped column from outer query"

**Cause**: Subquery in SELECT/CASE references columns from outer query that aren't in GROUP BY.

**Solution**: Use CTE (Common Table Expression) to separate aggregation from subqueries:

```sql
-- ❌ Bad - subquery references ungrouped p.id
SELECT
  SPLIT_PART(p.id, '/', 1) as author,
  COUNT(*) as count,
  CASE WHEN EXISTS (
    SELECT 1 FROM users WHERE username = SPLIT_PART(p.id, '/', 1)
  ) THEN TRUE ELSE FALSE END as claimed
FROM packages p
GROUP BY SPLIT_PART(p.id, '/', 1);

-- ✅ Good - use CTE to compute aggregates first
WITH author_stats AS (
  SELECT
    SPLIT_PART(p.id, '/', 1) as author,
    COUNT(*) as count
  FROM packages p
  GROUP BY SPLIT_PART(p.id, '/', 1)
)
SELECT
  author,
  count,
  EXISTS (SELECT 1 FROM users WHERE username = author_stats.author) as claimed
FROM author_stats;
```

### 2. "Functions in index expression must be marked IMMUTABLE"

**Cause**: PostgreSQL requires functions in indexes/generated columns to be IMMUTABLE.

**Problem Functions**:
- `array_to_string()` - marked STABLE, not IMMUTABLE
- `to_char()` - depends on timezone/locale settings
- `now()` - changes over time

**Solution**: Create IMMUTABLE wrapper functions:

```sql
-- Create IMMUTABLE wrapper for array_to_string
CREATE OR REPLACE FUNCTION immutable_array_to_string(text[], text)
RETURNS text AS $$
  SELECT array_to_string($1, $2)
$$ LANGUAGE SQL IMMUTABLE PARALLEL SAFE;

-- Use in generated column
ALTER TABLE packages
ADD COLUMN search_vector tsvector
GENERATED ALWAYS AS (
  setweight(to_tsvector('english', coalesce(name, '')), 'A') ||
  setweight(to_tsvector('english', immutable_array_to_string(tags, ' ')), 'B')
) STORED;

-- Now you can index it
CREATE INDEX idx_search ON packages USING gin(search_vector);
```

### 3. "Relation does not exist" (Extensions)

**Cause**: Extension not installed (e.g., `pg_stat_statements`, `pg_trgm`, `uuid-ossp`).

**Solution**: Make extension usage optional with error handling:

```sql
-- Try to create extension, ignore if unavailable
DO $$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_extension WHERE extname = 'pg_trgm') THEN
    BEGIN
      CREATE EXTENSION pg_trgm;
    EXCEPTION
      WHEN insufficient_privilege OR feature_not_supported THEN
        RAISE NOTICE 'pg_trgm extension not available - skipping trigram indexes';
    END;
  END IF;
END $$;

-- Only create trigram indexes if extension exists
DO $$
BEGIN
  IF EXISTS (SELECT 1 FROM pg_extension WHERE extname = 'pg_trgm') THEN
    CREATE INDEX idx_name_trgm ON packages USING gin(name gin_trgm_ops);
  END IF;
END $$;
```

### 4. Idempotent Migrations

**Always use IF (NOT) EXISTS** to make migrations re-runnable:

```sql
-- Tables
CREATE TABLE IF NOT EXISTS users (...);

-- Columns
ALTER TABLE users ADD COLUMN IF NOT EXISTS email VARCHAR(255);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);

-- Drop operations
DROP TABLE IF EXISTS old_table CASCADE;
DROP INDEX IF EXISTS old_index;
DROP VIEW IF EXISTS old_view CASCADE;
DROP FUNCTION IF EXISTS old_function(args);

-- Extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
```

### 5. Handling Circular Dependencies

**Issue**: Table A references table B, table B references table A.

**Solution**: Create tables first without foreign keys, then add constraints:

```sql
-- Step 1: Create tables without foreign keys
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  name VARCHAR(255)
);

CREATE TABLE posts (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  author_id UUID  -- No FK constraint yet
);

-- Step 2: Add foreign key constraints
ALTER TABLE posts
ADD CONSTRAINT fk_posts_author
FOREIGN KEY (author_id) REFERENCES users(id);
```

### 6. Working with Generated Columns

**Rules**:
- Must use IMMUTABLE functions only
- Cannot reference other generated columns
- Use STORED (not VIRTUAL in PostgreSQL)
- Cannot be updated directly

```sql
-- ✅ Good - IMMUTABLE functions
ALTER TABLE packages
ADD COLUMN full_name TEXT
GENERATED ALWAYS AS (namespace || '/' || name) STORED;

-- ✅ Good - with COALESCE for nulls
ALTER TABLE packages
ADD COLUMN search_text TEXT
GENERATED ALWAYS AS (
  coalesce(name, '') || ' ' || coalesce(description, '')
) STORED;

-- ❌ Bad - NOW() is not immutable
ALTER TABLE logs
ADD COLUMN year INTEGER
GENERATED ALWAYS AS (EXTRACT(YEAR FROM NOW())) STORED;  -- ERROR

-- ✅ Good - use created_at column instead
ALTER TABLE logs
ADD COLUMN year INTEGER
GENERATED ALWAYS AS (EXTRACT(YEAR FROM created_at)) STORED;
```

### 7. Materialized Views

**Best Practices**:

```sql
-- Create with data
CREATE MATERIALIZED VIEW IF NOT EXISTS package_rankings AS
SELECT
  id,
  name,
  total_downloads,
  ROW_NUMBER() OVER (ORDER BY total_downloads DESC) as rank
FROM packages
WHERE visibility = 'public';

-- Create indexes on materialized views
CREATE INDEX IF NOT EXISTS idx_rankings_downloads
ON package_rankings(total_downloads DESC);

-- Refresh function
CREATE OR REPLACE FUNCTION refresh_rankings()
RETURNS void AS $$
BEGIN
  REFRESH MATERIALIZED VIEW CONCURRENTLY package_rankings;
END;
$$ LANGUAGE plpgsql;

-- Schedule refresh (requires pg_cron extension)
-- SELECT cron.schedule('refresh-rankings', '0 * * * *', 'SELECT refresh_rankings()');
```

### 8. Full-Text Search Optimization

**Pattern**: Use generated column + GIN index for best performance:

```sql
-- 1. Create immutable helper
CREATE OR REPLACE FUNCTION immutable_array_to_string(text[], text)
RETURNS text AS $$
  SELECT array_to_string($1, $2)
$$ LANGUAGE SQL IMMUTABLE PARALLEL SAFE;

-- 2. Add generated column
ALTER TABLE packages
ADD COLUMN search_vector tsvector
GENERATED ALWAYS AS (
  setweight(to_tsvector('english', coalesce(name, '')), 'A') ||
  setweight(to_tsvector('english', coalesce(description, '')), 'B') ||
  setweight(to_tsvector('english', immutable_array_to_string(tags, ' ')), 'C')
) STORED;

-- 3. Create GIN index
CREATE INDEX idx_packages_search ON packages USING gin(search_vector);

-- 4. Query using the index
SELECT *
FROM packages
WHERE search_vector @@ websearch_to_tsquery('english', 'react hooks');
```

### 9. Composite Indexes for Common Queries

**Principles**:
- Equality filters first, then ranges, then sorts
- Most selective columns first
- Include WHERE clause conditions

```sql
-- Query: WHERE type = 'agent' AND category = 'development' ORDER BY downloads DESC
CREATE INDEX idx_packages_type_category_downloads
ON packages(type, category, total_downloads DESC)
WHERE visibility = 'public';

-- Query: WHERE author = 'foo' AND deprecated = FALSE ORDER BY created_at DESC
CREATE INDEX idx_packages_author_active
ON packages(author_id, created_at DESC)
WHERE deprecated = FALSE AND visibility = 'public';

-- Partial index for common filter
CREATE INDEX idx_packages_verified
ON packages(verified, total_downloads DESC)
WHERE verified = TRUE AND visibility = 'public';
```

### 10. Migration File Structure

**Best Practice Template**:

```sql
-- Migration XXX: Description
-- Brief explanation of what this migration does

-- ============================================
-- EXTENSIONS
-- ============================================

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- ============================================
-- TABLES
-- ============================================

CREATE TABLE IF NOT EXISTS table_name (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  name VARCHAR(255) NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ============================================
-- INDEXES
-- ============================================

CREATE INDEX IF NOT EXISTS idx_table_name ON table_name(name);

-- ============================================
-- VIEWS
-- ============================================

CREATE OR REPLACE VIEW view_name AS
SELECT * FROM table_name WHERE active = true;

-- ============================================
-- FUNCTIONS
-- ============================================

CREATE OR REPLACE FUNCTION function_name()
RETURNS void AS $$
BEGIN
  -- Function body
END;
$$ LANGUAGE plpgsql;

-- ============================================
-- TRIGGERS
-- ============================================

CREATE OR REPLACE FUNCTION update_timestamp()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_timestamp
  BEFORE UPDATE ON table_name
  FOR EACH ROW
  EXECUTE FUNCTION update_timestamp();

-- ============================================
-- COMMENTS
-- ============================================

COMMENT ON TABLE table_name IS 'Description of table purpose';
COMMENT ON COLUMN table_name.name IS 'Description of column';
```

## Common Patterns

### Pattern: Auto-updating Timestamps

```sql
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply to all tables that need it
CREATE TRIGGER trigger_users_updated_at
  BEFORE UPDATE ON users
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at();
```

### Pattern: Soft Delete

```sql
ALTER TABLE packages ADD COLUMN IF NOT EXISTS deleted_at TIMESTAMP WITH TIME ZONE;

CREATE INDEX IF NOT EXISTS idx_packages_not_deleted
ON packages(id) WHERE deleted_at IS NULL;

-- View for active records
CREATE OR REPLACE VIEW active_packages AS
SELECT * FROM packages WHERE deleted_at IS NULL;
```

### Pattern: Enumerated Types

```sql
-- Option 1: CHECK constraint (more flexible)
ALTER TABLE packages
ADD COLUMN status VARCHAR(50) DEFAULT 'active'
CHECK (status IN ('active', 'deprecated', 'archived'));

-- Option 2: ENUM type (more strict)
CREATE TYPE package_status AS ENUM ('active', 'deprecated', 'archived');
ALTER TABLE packages ADD COLUMN status package_status DEFAULT 'active';
```

### Pattern: JSON/JSONB Columns

```sql
ALTER TABLE packages ADD COLUMN IF NOT EXISTS metadata JSONB DEFAULT '{}';

-- Index on JSONB keys
CREATE INDEX IF NOT EXISTS idx_packages_metadata_tags
ON packages USING gin((metadata->'tags'));

-- Index on specific JSON path
CREATE INDEX IF NOT EXISTS idx_packages_metadata_version
ON packages((metadata->>'version'));
```

## Performance Tips

### 1. ANALYZE After Migrations

```sql
-- Update statistics after adding indexes or bulk data
ANALYZE packages;
ANALYZE VERBOSE packages;  -- Show details
```

### 2. EXPLAIN Your Queries

```sql
-- Check if indexes are being used
EXPLAIN ANALYZE
SELECT * FROM packages WHERE type = 'agent' ORDER BY downloads DESC LIMIT 10;

-- Look for:
-- - "Index Scan" (good) vs "Seq Scan" (bad for large tables)
-- - High "cost" values
-- - Long "execution time"
```

### 3. Vacuum After Bulk Changes

```sql
-- Clean up dead rows
VACUUM ANALYZE packages;

-- Full vacuum (locks table)
VACUUM FULL packages;
```

## Migration Checklist

- [ ] All CREATE statements use IF (NOT) EXISTS
- [ ] All DROP statements use IF EXISTS
- [ ] All functions in indexes/generated columns are IMMUTABLE
- [ ] Foreign keys reference existing tables
- [ ] Indexes have meaningful names (idx_table_column pattern)
- [ ] Extensions are optional with error handling
- [ ] Comments added for complex logic
- [ ] Test migration in local/dev before production
- [ ] Migration is idempotent (can run multiple times safely)
- [ ] Large migrations include progress logging

## Testing Migrations Locally

```bash
# Run migration
npm run migrate

# Check for errors
docker-compose logs postgres

# Rollback if needed (manual)
# Connect to DB and DROP objects created by migration

# Verify
docker-compose exec postgres psql -U prpm -d prpm_registry -c "\d packages"
docker-compose exec postgres psql -U prpm -d prpm_registry -c "\di"  # List indexes
```

## Resources

- [PostgreSQL CREATE INDEX](https://www.postgresql.org/docs/current/sql-createindex.html)
- [Generated Columns](https://www.postgresql.org/docs/current/ddl-generated-columns.html)
- [Full-Text Search](https://www.postgresql.org/docs/current/textsearch.html)
- [IMMUTABLE Functions](https://www.postgresql.org/docs/current/xfunc-volatility.html)
