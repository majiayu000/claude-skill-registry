---
name: cross-env-postgresql-extensions
description: Activate when creating database migrations that enable or disable PostgreSQL extensions. Provides the DO block pattern for cross-environment compatibility between Nhost Cloud, CNPG (CloudNativePG), and other PostgreSQL environments.
updated: 2025-01-13
---

# Cross-Environment PostgreSQL Extensions

This skill provides the **DO block pattern** for PostgreSQL extensions that works across different hosting environments.

## When This Skill Activates

Claude automatically uses this skill when you:

- Enable PostgreSQL extensions in migrations
- Disable PostgreSQL extensions in rollback migrations
- Create migrations that need `CREATE EXTENSION`
- Work with multiple PostgreSQL environments (cloud, self-hosted, CNPG)

## The Problem: Permission Errors Across Environments

Different PostgreSQL environments have different permission models:

| Environment | Extension Behavior | Required Pattern |
|-------------|-------------------|------------------|
| **Nhost Cloud** | Extensions require `SET ROLE postgres` | Must elevate privileges |
| **CNPG / CloudNativePG** | Extensions pre-installed, `SET ROLE` fails | Must handle privilege error |
| **Standard PostgreSQL** | Varies by configuration | Needs flexible pattern |

**❌ STANDARD PATTERN FAILS:**

```sql
-- Fails in Nhost Cloud: "permission denied"
CREATE EXTENSION IF NOT EXISTS vector;

-- Fails in CNPG: "SET ROLE postgres" permission error
SET ROLE postgres;
CREATE EXTENSION IF NOT EXISTS vector;
```

## The Solution: DO Block Pattern

The DO block pattern with exception handling works in **all environments**:

```sql
-- ✅ WORKS EVERYWHERE
DO $$
BEGIN
  SET ROLE postgres;
EXCEPTION
  WHEN OTHERS THEN NULL;
END $$;
CREATE EXTENSION IF NOT EXISTS {extension_name};
```

### How It Works

1. **Nhost Cloud**: `SET ROLE postgres` succeeds → Extension created
2. **CNPG**: `SET ROLE postgres` fails → Exception caught → Extension already exists
3. **Other**: Handles both cases gracefully

## Enable Extension (up.sql)

```sql
-- ✅ CORRECT - Cross-environment compatible pattern
-- Nhost Cloud: SET ROLE postgres succeeds, then creates extension
-- CNPG: SET ROLE postgres fails (caught by exception), extension already exists
-- Standard PostgreSQL: Works with or without superuser privileges
DO $$
BEGIN
  SET ROLE postgres;
EXCEPTION
  WHEN OTHERS THEN NULL;
END $$;
CREATE EXTENSION IF NOT EXISTS {extension_name};
```

**Examples:**

```sql
-- Enable pgvector for semantic search
DO $$
BEGIN
  SET ROLE postgres;
EXCEPTION
  WHEN OTHERS THEN NULL;
END $$;
CREATE EXTENSION IF NOT EXISTS vector;

-- Enable PostGIS for geospatial queries
DO $$
BEGIN
  SET ROLE postgres;
EXCEPTION
  WHEN OTHERS THEN NULL;
END $$;
CREATE EXTENSION IF NOT EXISTS postgis;

-- Enable trigram matching for fuzzy search
DO $$
BEGIN
  SET ROLE postgres;
EXCEPTION
  WHEN OTHERS THEN NULL;
END $$;
CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- Enable unaccent for accent-insensitive search
DO $$
BEGIN
  SET ROLE postgres;
EXCEPTION
  WHEN OTHERS THEN NULL;
END $$;
CREATE EXTENSION IF NOT EXISTS unaccent;
```

## Disable Extension (down.sql)

```sql
-- ✅ CORRECT - Cross-environment compatible pattern
DO $$
BEGIN
  SET ROLE postgres;
EXCEPTION
  WHEN OTHERS THEN NULL;
END $$;
DROP EXTENSION IF EXISTS {extension_name} CASCADE;
```

**Examples:**

```sql
-- Drop pgvector
DO $$
BEGIN
  SET ROLE postgres;
EXCEPTION
  WHEN OTHERS THEN NULL;
END $$;
DROP EXTENSION IF EXISTS vector CASCADE;

-- Drop PostGIS
DO $$
BEGIN
  SET ROLE postgres;
EXCEPTION
  WHEN OTHERS THEN NULL;
END $$;
DROP EXTENSION IF EXISTS postgis CASCADE;
```

## Common PostgreSQL Extensions

| Extension | Purpose | Use Cases |
|-----------|---------|-----------|
| **vector** | pgvector for vector embeddings | AI search, recommendations, RAG |
| **postgis** | Geographic data types | Location search, distance calculations |
| **pg_trgm** | Trigram matching | Fuzzy text search, autocomplete |
| **unaccent** | Accent-insensitive text | International search (café = cafe) |
| **fuzzystrmatch** | Phonetic string matching | Soundex, Levenshtein distance |
| **btree_gin** | B-tree/GIN index types | Advanced indexing strategies |
| **btree_gist** | B-tree/GiST index types | Exclusion constraints |
| **uuid-ossp** | UUID generation | Primary keys, unique identifiers |
| **citext** | Case-insensitive text | Email, username comparisons |
| **hstore** | Key-value pairs | EAV patterns, flexible attributes |

## Complete Migration Example

**Migration: enable_search_extensions**

```sql
-- up.sql
-- Enable vector extension for semantic embeddings
DO $$
BEGIN
  SET ROLE postgres;
EXCEPTION
  WHEN OTHERS THEN NULL;
END $$;
CREATE EXTENSION IF NOT EXISTS vector;

-- Enable PostGIS for geographic distance calculations
DO $$
BEGIN
  SET ROLE postgres;
EXCEPTION
  WHEN OTHERS THEN NULL;
END $$;
CREATE EXTENSION IF NOT EXISTS postgis;

-- Enable trigram matching for fuzzy text search
DO $$
BEGIN
  SET ROLE postgres;
EXCEPTION
  WHEN OTHERS THEN NULL;
END $$;
CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- Enable unaccent for accent-insensitive search
DO $$
BEGIN
  SET ROLE postgres;
EXCEPTION
  WHEN OTHERS THEN NULL;
END $$;
CREATE EXTENSION IF NOT EXISTS unaccent;
```

```sql
-- down.sql (rollback in reverse order with CASCADE)
-- Drop extensions in reverse order
DO $$
BEGIN
  SET ROLE postgres;
EXCEPTION
  WHEN OTHERS THEN NULL;
END $$;
DROP EXTENSION IF EXISTS unaccent CASCADE;

DO $$
BEGIN
  SET ROLE postgres;
EXCEPTION
  WHEN OTHERS THEN NULL;
END $$;
DROP EXTENSION IF EXISTS pg_trgm CASCADE;

DO $$
BEGIN
  SET ROLE postgres;
EXCEPTION
  WHEN OTHERS THEN NULL;
END $$;
DROP EXTENSION IF EXISTS postgis CASCADE;

DO $$
BEGIN
  SET ROLE postgres;
EXCEPTION
  WHEN OTHERS THEN NULL;
END $$;
DROP EXTENSION IF EXISTS vector CASCADE;
```

## Important Notes

- **Always use the DO block pattern** for cross-environment compatibility
- Always use `IF NOT EXISTS` to make migrations idempotent
- Always use `CASCADE` when dropping to clean up dependent objects
- Drop extensions in **reverse order** of creation in down.sql
- Extensions are **cluster-level**, they persist across databases
- Test migrations in both development and production-like environments
- The DO block pattern ensures migrations work whether extensions are pre-installed or need to be created

## Extension-Specific Patterns

### Vector Extension (pgvector)

```sql
-- up.sql
DO $$
BEGIN
  SET ROLE postgres;
EXCEPTION
  WHEN OTHERS THEN NULL;
END $$;
CREATE EXTENSION IF NOT EXISTS vector;

-- Create vector column
ALTER TABLE items
ADD COLUMN embedding vector(1536);

-- Create vector index for similarity search
CREATE INDEX items_embedding_idx ON items
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);
```

### PostGIS Extension

```sql
-- up.sql
DO $$
BEGIN
  SET ROLE postgres;
EXCEPTION
  WHEN OTHERS THEN NULL;
END $$;
CREATE EXTENSION IF NOT EXISTS postgis;

-- Add geometry column
ALTER TABLE locations
ADD COLUMN geom geometry(Point, 4326);

-- Create spatial index
CREATE INDEX locations_geom_idx ON locations
USING GIST (geom);
```

### pg_trgm Extension

```sql
-- up.sql
DO $$
BEGIN
  SET ROLE postgres;
EXCEPTION
  WHEN OTHERS THEN NULL;
END $$;
CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- Create GIN index for trigram search
CREATE INDEX items_name_trgm_idx ON items
USING GIN (name gin_trgm_ops);
```

## Quick Reference

| Task | Pattern |
|------|---------|
| Enable extension | `DO $$ BEGIN SET ROLE postgres; EXCEPTION WHEN OTHERS THEN NULL; END $$; CREATE EXTENSION IF NOT EXISTS {name};` |
| Disable extension | `DO $$ BEGIN SET ROLE postgres; EXCEPTION WHEN OTHERS THEN NULL; END $$; DROP EXTENSION IF EXISTS {name} CASCADE;` |
| Check if enabled | `SELECT * FROM pg_extension WHERE extname = '{name}';` |
| List all extensions | `SELECT * FROM pg_extension ORDER BY extname;` |

## References

- [Nhost Database Extensions](https://docs.nhost.io/products/database/extensions)
- [PostgreSQL Extensions](https://www.postgresql.org/docs/current/sql-createextension.html)
- [pgvector Documentation](https://github.com/pgvector/pgvector)
- [PostGIS Documentation](https://postgis.net/documentation/)

---

**Remember**: Always use the DO block pattern when creating or dropping PostgreSQL extensions in migrations. This ensures your migrations work across Nhost Cloud, CNPG, and standard PostgreSQL environments.
