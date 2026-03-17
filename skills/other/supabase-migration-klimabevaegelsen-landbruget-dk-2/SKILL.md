---
name: supabase-migration
description: |
  Activates when working with database migrations, RLS policies, or Supabase schema changes.
  Use this skill for: creating migrations, writing RLS policies, handling PostGIS geometry,
  creating indexes, managing materialized views, and generating TypeScript types.
  Keywords: migration, supabase, RLS, policy, PostGIS, geometry, schema, table, index
---

# Supabase Migration Skill

This skill provides guidance for database migrations and schema management in Landbruget.dk.

## Activation Context

This skill activates when:
- Creating database migrations
- Writing RLS (Row Level Security) policies
- Working with PostGIS/geometry columns
- Creating indexes for performance
- Managing materialized views
- Generating TypeScript types from schema

## Environment Setup

```bash
# Check Supabase connection
supabase status

# Link to remote project (if not linked)
supabase link --project-ref <project-ref>

# Pull latest schema
supabase db pull
```

## Creating Migrations

### Standard Migration

```bash
# Create new migration
supabase migration new <migration_name>

# Example
supabase migration new add_farm_statistics_table
```

This creates: `supabase/migrations/[timestamp]_add_farm_statistics_table.sql`

### Migration Template

```sql
-- supabase/migrations/[timestamp]_[name].sql

-- ===========================================
-- Migration: [Description]
-- Created: [Date]
-- ===========================================

-- 1. Create Tables
CREATE TABLE IF NOT EXISTS [table_name] (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),

  -- Business columns
  cvr_number VARCHAR(8) NOT NULL,
  name TEXT NOT NULL,

  -- Constraints
  CONSTRAINT valid_cvr CHECK (cvr_number ~ '^\d{8}$')
);

-- 2. Enable RLS
ALTER TABLE [table_name] ENABLE ROW LEVEL SECURITY;

-- 3. Create RLS Policies
CREATE POLICY "Allow public read access"
  ON [table_name]
  FOR SELECT
  USING (true);

-- 4. Create Indexes
CREATE INDEX idx_[table]_cvr ON [table_name] (cvr_number);
CREATE INDEX idx_[table]_created ON [table_name] (created_at);

-- 5. Create Triggers (if needed)
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER [table]_updated_at
  BEFORE UPDATE ON [table_name]
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at();

-- 6. Comments
COMMENT ON TABLE [table_name] IS '[Description of table purpose]';
COMMENT ON COLUMN [table_name].[column] IS '[Description]';
```

## RLS Policies

### Common Policy Patterns

**Public Read Access (most common for Landbruget.dk):**
```sql
CREATE POLICY "Allow public read access"
  ON [table_name]
  FOR SELECT
  USING (true);
```

**Authenticated Users Only:**
```sql
CREATE POLICY "Allow authenticated read"
  ON [table_name]
  FOR SELECT
  TO authenticated
  USING (true);
```

**Owner-Only Access:**
```sql
CREATE POLICY "Users can only see own data"
  ON [table_name]
  FOR SELECT
  USING (auth.uid() = user_id);
```

**Role-Based Access:**
```sql
CREATE POLICY "Admins can do everything"
  ON [table_name]
  FOR ALL
  USING (
    EXISTS (
      SELECT 1 FROM user_roles
      WHERE user_id = auth.uid()
      AND role = 'admin'
    )
  );
```

## PostGIS / Geometry

### Creating Geometry Columns

```sql
-- Enable PostGIS (usually already enabled)
CREATE EXTENSION IF NOT EXISTS postgis;

-- Add geometry column
ALTER TABLE [table_name]
ADD COLUMN geom GEOMETRY(Point, 4326);

-- Or for polygons
ALTER TABLE [table_name]
ADD COLUMN boundary GEOMETRY(Polygon, 4326);

-- Create spatial index
CREATE INDEX idx_[table]_geom ON [table_name] USING GIST (geom);
```

### Coordinate Systems

| EPSG | Name | Use Case |
|------|------|----------|
| 4326 | WGS84 | Storage standard |
| 25832 | UTM 32N | Danish data input |
| 3857 | Web Mercator | Display/maps |

**Conversion:**
```sql
-- Convert from Danish UTM to WGS84
SELECT ST_Transform(geom, 4326) FROM ...

-- Set SRID
SELECT ST_SetSRID(geom, 4326) FROM ...
```

### Common Spatial Queries

```sql
-- Find points within polygon
SELECT * FROM farms
WHERE ST_Within(geom, (SELECT boundary FROM regions WHERE name = 'Jutland'));

-- Distance query (in meters)
SELECT *, ST_Distance(geom::geography, point::geography) as distance
FROM farms
WHERE ST_DWithin(geom::geography, point::geography, 10000)
ORDER BY distance;

-- Centroid of polygon
SELECT ST_Centroid(boundary) FROM fields;
```

## Indexes

### When to Create Indexes

- Columns used in WHERE clauses frequently
- Columns used in JOIN conditions
- Columns used in ORDER BY
- Foreign key columns

### Index Types

```sql
-- B-tree (default, good for equality and range)
CREATE INDEX idx_name ON table (column);

-- GiST (for geometry)
CREATE INDEX idx_geom ON table USING GIST (geom);

-- GIN (for arrays, JSONB, full-text search)
CREATE INDEX idx_data ON table USING GIN (data_jsonb);

-- Partial index (filtered)
CREATE INDEX idx_active ON table (column) WHERE is_active = true;
```

### Required Indexes for Landbruget.dk

```sql
-- Always index these columns
CREATE INDEX idx_[table]_cvr ON [table] (cvr_number);
CREATE INDEX idx_[table]_chr ON [table] (chr_number);
CREATE INDEX idx_[table]_bfe ON [table] (bfe_number);
CREATE INDEX idx_[table]_geom ON [table] USING GIST (geom);
```

## Materialized Views

For complex aggregations that don't need real-time updates:

```sql
-- Create materialized view
CREATE MATERIALIZED VIEW farm_statistics AS
SELECT
  cvr_number,
  COUNT(*) as field_count,
  SUM(area_ha) as total_area,
  array_agg(DISTINCT crop_type) as crop_types
FROM fields
GROUP BY cvr_number;

-- Create index on materialized view
CREATE UNIQUE INDEX idx_farm_stats_cvr ON farm_statistics (cvr_number);

-- Refresh (run periodically)
REFRESH MATERIALIZED VIEW CONCURRENTLY farm_statistics;
```

## Applying Migrations

```bash
# Apply to local database
supabase db push

# Reset local database (caution: loses data)
supabase db reset

# Check migration status
supabase migration list
```

## Generate TypeScript Types

```bash
# Generate types from database schema
supabase gen types typescript --local > frontend/src/types/supabase.ts

# Or from remote
supabase gen types typescript --project-id <project-id> > frontend/src/types/supabase.ts
```

## Rollback Strategies

**For simple changes, create a new migration:**
```sql
-- Migration to rollback previous change
DROP TABLE IF EXISTS [table_name];
```

**For complex rollbacks, keep down migrations:**
```sql
-- up migration: 001_create_table.sql
CREATE TABLE ...

-- down migration: 001_drop_table.sql (keep separately)
DROP TABLE ...
```

## Migration Checklist

Before marking migration work complete:
- [ ] Table created with proper columns
- [ ] RLS enabled on table
- [ ] RLS policies created (at minimum, public read)
- [ ] Indexes created for CVR/CHR/BFE columns
- [ ] Spatial index created for geometry columns
- [ ] TypeScript types regenerated
- [ ] Migration applies without errors: `supabase db push`
- [ ] Data validation queries work as expected

## Troubleshooting

### Migration Syntax Error
```bash
# Check SQL syntax
supabase db lint
```

### RLS Blocking Access
```sql
-- Temporarily check without RLS (for debugging)
SET LOCAL ROLE postgres;
SELECT * FROM [table];
```

### Missing PostGIS
```sql
CREATE EXTENSION IF NOT EXISTS postgis;
```
