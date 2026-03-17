---
name: postgis
description: MANDATORY when working with geographic data, spatial queries, geometry operations, or location-based features - enforces PostGIS 3.6.1 best practices including ST_CoverageClean, SFCGAL 3D functions, and bigint topology
---

# PostGIS 3.6.1 Spatial Database

## Overview

PostGIS 3.6.1 (with GEOS 3.14) brings significant improvements: ST_CoverageClean for topology repair, enhanced SFCGAL 3D operations, bigint topology support for massive datasets, and improved PostgreSQL 18 integration. This skill ensures you leverage these capabilities correctly.

**Core principle:** Spatial is special. Generic database patterns often fail with geographic data.

**Announce at start:** "I'm applying postgis to ensure PostGIS 3.6.1 spatial best practices."

## When This Skill Applies

This skill is MANDATORY when ANY of these patterns are touched:

| Pattern | Examples |
|---------|----------|
| `**/*geo*` | models/geography.ts, geo_utils.py |
| `**/*spatial*` | lib/spatial.ts |
| `**/*location*` | services/locationService.ts |
| `**/*coordinate*` | types/coordinates.ts |
| `**/*polygon*` | db/polygons.sql |
| `**/*geometry*` | migrations/add_geometry.sql |
| `**/*postgis*` | setup/postgis.sql |
| `**/*gis*` | utils/gis.ts |

Or when files contain:

```sql
-- These patterns trigger this skill
ST_*
geography
geometry
SRID
```

## PostGIS 3.6.1 Features

### 1. ST_CoverageClean (New in 3.6.1)

Coverage cleaning repairs topological errors in polygon collections. Requires GEOS 3.14:

```sql
-- Clean a set of polygons that should form a seamless coverage
-- Fixes: overlaps, gaps, edge inconsistencies
SELECT ST_CoverageClean(
  ARRAY[polygon1, polygon2, polygon3]::geometry[]
) AS cleaned_polygons;

-- Use case: Administrative boundaries, parcels, zones
-- Before: Manual repair with ST_MakeValid, ST_SnapToGrid
-- After: Single function handles entire coverage

-- Example: Clean municipal boundaries
WITH boundaries AS (
  SELECT geom FROM municipalities
)
SELECT ST_CoverageClean(array_agg(geom))
FROM boundaries;
```

**When to use:**
- Importing GIS data with topological errors
- Merging datasets from different sources
- Ensuring seamless coverage (no gaps/overlaps)
- Cadastral/parcel data management

### 2. SFCGAL 3D Functions

PostGIS 3.6.1 includes enhanced SFCGAL support for 3D operations:

```sql
-- Enable SFCGAL (if not already enabled)
CREATE EXTENSION IF NOT EXISTS postgis_sfcgal;

-- 3D intersection (true 3D, not projection)
SELECT ST_3DIntersection(
  ST_GeomFromText('POLYHEDRALSURFACE Z (...)'),
  ST_GeomFromText('POLYHEDRALSURFACE Z (...)')
);

-- 3D union
SELECT ST_3DUnion(geom1, geom2);

-- 3D area (actual surface area in 3D)
SELECT ST_3DArea(polyhedral_surface);

-- Minkowski sum (for buffer-like operations in 3D)
SELECT ST_MinkowskiSum(geometry1, geometry2);

-- Straight skeleton (for building roofs, etc.)
SELECT ST_StraightSkeleton(polygon);

-- Extrude 2D to 3D
SELECT ST_Extrude(polygon, 0, 0, height);
```

**Use cases:**
- Building/structure modeling
- Underground infrastructure
- Airspace management
- 3D terrain analysis

### 3. Bigint Topology Support

PostGIS 3.6.1 supports bigint topology IDs for massive datasets:

```sql
-- Create topology with bigint IDs (new in 3.6.1)
SELECT CreateTopology('massive_parcels', 4326, 0.0000001, true);
-- Last parameter: use_bigint = true

-- Supports > 2 billion features per topology
-- Previous limit: ~2 billion (int4 max)

-- Add layer
SELECT AddTopoGeometryColumn('massive_parcels', 'public', 'parcels', 'topogeom', 'POLYGON');

-- TopoGeometry operations work the same
SELECT ST_CreateTopoGeo('massive_parcels', geom);
```

**When to use:**
- National/continental scale datasets
- High-resolution parcel data
- OpenStreetMap imports
- Any topology > 2 billion edges

### 4. PostgreSQL 18 Interrupt Handling

PostGIS 3.6.1 properly handles PostgreSQL 18's improved query cancellation:

```sql
-- Long-running spatial operations can now be cancelled cleanly
-- No more orphaned locks or corrupted state

-- Example: Cancellable heavy operation
SELECT ST_Union(geom)
FROM very_large_table
GROUP BY region;
-- ^C now works properly

-- COPY operations with PostGIS also respect cancellation
COPY (SELECT id, ST_AsGeoJSON(geom) FROM features) TO '/tmp/export.json';
```

## Data Types

### Geometry vs Geography

```sql
-- GEOMETRY: Planar coordinates, any SRID
-- Faster computations, less accurate over large distances
CREATE TABLE places_geometry (
  id uuid PRIMARY KEY DEFAULT uuidv7(),
  location geometry(Point, 4326)  -- WGS84
);

-- GEOGRAPHY: Spherical coordinates, always WGS84
-- Accurate distances/areas, slower computations
CREATE TABLE places_geography (
  id uuid PRIMARY KEY DEFAULT uuidv7(),
  location geography(Point, 4326)  -- Always WGS84
);

-- When to use GEOMETRY:
-- - Local/city-scale applications
-- - Need complex operations (union, intersection)
-- - Performance critical
-- - Non-earth data (game maps, floor plans)

-- When to use GEOGRAPHY:
-- - Global applications
-- - Distance/area accuracy matters
-- - Simple operations (distance, contains)
-- - User-facing distance calculations
```

### Choosing SRID

```sql
-- Common SRIDs:
-- 4326: WGS84 (GPS coordinates, web maps)
-- 3857: Web Mercator (tile-based web maps, display only)
-- Local projections for accurate measurements

-- ALWAYS store in 4326 (WGS84) as source of truth
-- Transform for calculations when needed

CREATE TABLE locations (
  id uuid PRIMARY KEY DEFAULT uuidv7(),
  name text NOT NULL,
  location geography(Point, 4326),  -- Storage
  location_local geometry(Point)     -- NULL, computed as needed
);

-- Transform for local calculations
SELECT ST_Transform(
  location::geometry,
  32610  -- UTM Zone 10N (California)
) FROM locations WHERE name = 'San Francisco';
```

## Index Strategy

### Spatial Indexes

```sql
-- GiST index: Default for most spatial queries
CREATE INDEX idx_locations_geom ON locations USING gist(location);

-- BRIN index: For very large, naturally ordered datasets
-- (e.g., GPS tracks ordered by time)
CREATE INDEX idx_tracks_geom ON gps_tracks USING brin(location);

-- SP-GiST: For non-overlapping data (points, IP ranges)
CREATE INDEX idx_points_spgist ON points USING spgist(location);
```

### Index Best Practices

```sql
-- Always include spatial index
CREATE TABLE features (
  id uuid PRIMARY KEY DEFAULT uuidv7(),
  geom geometry(Polygon, 4326),
  created_at timestamptz DEFAULT now()
);
CREATE INDEX idx_features_geom ON features USING gist(geom);

-- Partial spatial index for active records
CREATE INDEX idx_features_geom_active ON features USING gist(geom)
  WHERE deleted_at IS NULL;

-- Composite index for common query patterns
CREATE INDEX idx_features_type_geom ON features USING gist(geom)
  WHERE feature_type = 'building';
```

### Index Clustering

```sql
-- Cluster table by spatial index for range query performance
CLUSTER features USING idx_features_geom;

-- For large tables, recluster periodically
-- Schedule during maintenance window
```

## Query Patterns

### Distance Queries

```sql
-- Find points within distance (geography, in meters)
SELECT * FROM locations
WHERE ST_DWithin(
  location,
  ST_MakePoint(-122.4194, 37.7749)::geography,
  1000  -- 1km radius
);

-- Find points within distance (geometry, in SRID units)
SELECT * FROM locations
WHERE ST_DWithin(
  location,
  ST_SetSRID(ST_MakePoint(-122.4194, 37.7749), 4326),
  0.01  -- ~1km at this latitude (degrees)
);

-- K-nearest neighbors (KNN)
SELECT *, location <-> ST_MakePoint(-122.4194, 37.7749)::geography AS distance
FROM locations
ORDER BY location <-> ST_MakePoint(-122.4194, 37.7749)::geography
LIMIT 10;
-- Uses index for efficient KNN
```

### Containment Queries

```sql
-- Points within polygon
SELECT * FROM points
WHERE ST_Within(location, (
  SELECT boundary FROM regions WHERE name = 'California'
));

-- Polygon contains point
SELECT * FROM regions
WHERE ST_Contains(boundary, ST_MakePoint(-122.4194, 37.7749));

-- Intersects (overlaps in any way)
SELECT * FROM features
WHERE ST_Intersects(geom, query_polygon);
```

### Aggregation

```sql
-- Union all geometries
SELECT ST_Union(geom) FROM parcels WHERE owner = 'City';

-- Collect without merging (faster, preserves individual geometries)
SELECT ST_Collect(geom) FROM parcels WHERE owner = 'City';

-- Extent (bounding box)
SELECT ST_Extent(geom) FROM features;

-- Centroid of all points
SELECT ST_Centroid(ST_Collect(location)) FROM locations;
```

## GeoJSON Integration

### Import/Export

```sql
-- Geometry to GeoJSON
SELECT ST_AsGeoJSON(location) FROM locations WHERE id = $1;

-- Geometry with properties to Feature
SELECT jsonb_build_object(
  'type', 'Feature',
  'geometry', ST_AsGeoJSON(location)::jsonb,
  'properties', jsonb_build_object(
    'id', id,
    'name', name
  )
) FROM locations WHERE id = $1;

-- FeatureCollection
SELECT jsonb_build_object(
  'type', 'FeatureCollection',
  'features', jsonb_agg(
    jsonb_build_object(
      'type', 'Feature',
      'geometry', ST_AsGeoJSON(location)::jsonb,
      'properties', jsonb_build_object('id', id, 'name', name)
    )
  )
) FROM locations;

-- GeoJSON to Geometry
INSERT INTO locations (name, location)
VALUES ('New Place', ST_GeomFromGeoJSON($1));

-- With SRID enforcement
INSERT INTO locations (name, location)
VALUES ('New Place', ST_SetSRID(ST_GeomFromGeoJSON($1), 4326));
```

### API Response Pattern

```sql
-- Function for API endpoints
CREATE OR REPLACE FUNCTION get_locations_geojson(
  bounds geometry DEFAULT NULL
)
RETURNS jsonb AS $$
SELECT jsonb_build_object(
  'type', 'FeatureCollection',
  'features', COALESCE(jsonb_agg(
    jsonb_build_object(
      'type', 'Feature',
      'id', id,
      'geometry', ST_AsGeoJSON(location, 6)::jsonb,  -- 6 decimal places
      'properties', jsonb_build_object(
        'name', name,
        'created_at', created_at
      )
    )
  ), '[]'::jsonb)
)
FROM locations
WHERE bounds IS NULL OR ST_Intersects(location::geometry, bounds);
$$ LANGUAGE sql STABLE;
```

## Validation and Repair

### Validate Geometries

```sql
-- Check validity
SELECT id, ST_IsValid(geom), ST_IsValidReason(geom)
FROM features
WHERE NOT ST_IsValid(geom);

-- Common issues:
-- "Self-intersection"
-- "Ring Self-intersection"
-- "Too few points in geometry component"
-- "Hole lies outside shell"
```

### Repair Geometries

```sql
-- Simple repair (handles most issues)
UPDATE features
SET geom = ST_MakeValid(geom)
WHERE NOT ST_IsValid(geom);

-- Repair with specific strategy
UPDATE features
SET geom = ST_MakeValid(geom, 'method=structure')
WHERE NOT ST_IsValid(geom);

-- Coverage clean for polygon sets (3.6.1)
WITH cleaned AS (
  SELECT unnest(ST_CoverageClean(array_agg(geom ORDER BY id))) AS geom
  FROM parcels
)
UPDATE parcels p
SET geom = c.geom
FROM cleaned c
WHERE ST_Intersects(p.geom, c.geom);

-- Snap to grid for precision issues
UPDATE features
SET geom = ST_SnapToGrid(geom, 0.000001)
WHERE ST_NPoints(geom) > 1000;  -- High-detail features
```

## Performance Optimization

### Query Optimization

```sql
-- Use && for bounding box pre-filter
SELECT * FROM features
WHERE geom && ST_MakeEnvelope(-122.5, 37.7, -122.4, 37.8, 4326)
  AND ST_Intersects(geom, query_polygon);

-- Simplify for display (reduces transfer size)
SELECT id, ST_Simplify(geom, 0.0001) AS geom_display
FROM features;

-- Viewport-aware simplification
SELECT id,
  CASE
    WHEN zoom < 10 THEN ST_Simplify(geom, 0.01)
    WHEN zoom < 14 THEN ST_Simplify(geom, 0.001)
    ELSE geom
  END AS geom
FROM features
WHERE geom && viewport_bounds;
```

### Table Design for Spatial

```sql
-- Separate geometry from attributes for large tables
CREATE TABLE features (
  id uuid PRIMARY KEY DEFAULT uuidv7(),
  name text NOT NULL,
  category text,
  metadata jsonb DEFAULT '{}',
  created_at timestamptz DEFAULT now()
);

CREATE TABLE feature_geometries (
  feature_id uuid PRIMARY KEY REFERENCES features(id) ON DELETE CASCADE,
  geom geometry(Geometry, 4326),
  geom_simplified geometry(Geometry, 4326)  -- Pre-computed simplification
);

CREATE INDEX idx_feature_geom ON feature_geometries USING gist(geom);
CREATE INDEX idx_feature_geom_simple ON feature_geometries USING gist(geom_simplified);
```

### Materialized Views for Complex Queries

```sql
-- Pre-computed spatial joins
CREATE MATERIALIZED VIEW feature_regions AS
SELECT f.id AS feature_id, r.id AS region_id, r.name AS region_name
FROM features f
JOIN regions r ON ST_Within(f.location, r.boundary);

CREATE UNIQUE INDEX idx_feature_regions ON feature_regions(feature_id);

-- Refresh periodically
REFRESH MATERIALIZED VIEW CONCURRENTLY feature_regions;
```

## Migration Patterns

### Adding Spatial Column

```sql
-- Step 1: Add column
ALTER TABLE locations ADD COLUMN geom geometry(Point, 4326);

-- Step 2: Create index
CREATE INDEX CONCURRENTLY idx_locations_geom ON locations USING gist(geom);

-- Step 3: Backfill from lat/lng
UPDATE locations
SET geom = ST_SetSRID(ST_MakePoint(longitude, latitude), 4326)
WHERE geom IS NULL AND latitude IS NOT NULL;

-- Step 4: Add constraint if needed
ALTER TABLE locations ADD CONSTRAINT locations_geom_4326
  CHECK (ST_SRID(geom) = 4326);
```

### Converting Geometry to Geography

```sql
-- Create new column
ALTER TABLE locations ADD COLUMN location_geo geography(Point, 4326);

-- Migrate data
UPDATE locations
SET location_geo = location::geography
WHERE location_geo IS NULL;

-- Create index on new column
CREATE INDEX CONCURRENTLY idx_locations_geo ON locations USING gist(location_geo);

-- Update application, then drop old column
ALTER TABLE locations DROP COLUMN location;
ALTER TABLE locations RENAME COLUMN location_geo TO location;
```

## PostGIS Artifact

When implementing spatial features, post this artifact:

```markdown
<!-- POSTGIS_IMPLEMENTATION:START -->
## PostGIS Implementation Summary

### Spatial Columns

| Table | Column | Type | SRID | Index |
|-------|--------|------|------|-------|
| locations | location | geography(Point) | 4326 | gist |
| parcels | boundary | geometry(Polygon) | 4326 | gist |

### PostGIS 3.6.1 Features Used

- [ ] ST_CoverageClean for topology repair
- [ ] SFCGAL 3D functions
- [ ] Bigint topology
- [ ] PostgreSQL 18 interrupt handling

### Spatial Queries

| Query Pattern | Index Used | Performance |
|---------------|------------|-------------|
| KNN distance | Yes (gist) | <10ms |
| ST_Within region | Yes (gist) | <50ms |
| ST_Intersects | Yes (gist) | <100ms |

### Validation

- [ ] All geometries pass ST_IsValid
- [ ] SRID constraints enforced
- [ ] Spatial indexes created
- [ ] Query patterns tested with EXPLAIN ANALYZE

**PostGIS Version:** 3.6.1
**GEOS Version:** 3.14.x
**Verified At:** [timestamp]
<!-- POSTGIS_IMPLEMENTATION:END -->
```

## Checklist

Before completing PostGIS implementation:

- [ ] Correct data type chosen (geometry vs geography)
- [ ] SRID is consistent (4326 recommended for storage)
- [ ] Spatial indexes created on all geometry columns
- [ ] Input geometries validated (ST_IsValid)
- [ ] GeoJSON import/export tested
- [ ] Query performance verified with EXPLAIN ANALYZE
- [ ] PostGIS 3.6.1 features leveraged where appropriate
- [ ] Artifact posted to issue

## Integration

This skill integrates with:
- `database-architecture` - Spatial columns follow general schema patterns
- `postgres-rls` - RLS policies can use spatial predicates
- `timescaledb` - Time-series with spatial dimensions

## References

- [PostGIS 3.6.1 Release Notes](https://postgis.net/docs/release_notes.html)
- [PostGIS Documentation](https://postgis.net/docs/)
- [GEOS 3.14 Changelog](https://libgeos.org/usage/download/)
- [SFCGAL Documentation](http://oslandia.github.io/SFCGAL/)
