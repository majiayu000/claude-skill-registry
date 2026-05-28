---
name: duckdb-spatial
description: DuckDB Spatial Skill
version: 1.0.0
---

# DuckDB Spatial Skill

H3 hexagonal indexing, PostGIS-compatible spatial queries, and geographic analysis with GF(3) coloring.

## Trigger
- Spatial SQL queries, geographic data analysis
- H3 hexagonal grid operations
- Point-in-polygon, distance queries
- Geospatial joins, spatial indexing

## GF(3) Trit: 0 (Ergodic/Coordinator)
Coordinates spatial data flow and transforms between coordinate systems.

## Installation

```sql
INSTALL spatial;
LOAD spatial;

-- Also useful
INSTALL h3 FROM community;
LOAD h3;
```

## Core Spatial Types

```sql
-- Point, LineString, Polygon, MultiPoint, etc.
SELECT ST_Point(-122.4194, 37.7749) as san_francisco;
SELECT ST_GeomFromText('POLYGON((0 0, 1 0, 1 1, 0 1, 0 0))') as square;

-- GeoJSON parsing
SELECT ST_GeomFromGeoJSON('{"type":"Point","coordinates":[-122.4,37.7]}');
```

## Colored Spatial Table Schema

```sql
CREATE TABLE geo_features (
    feature_id VARCHAR PRIMARY KEY,
    name VARCHAR,
    geometry GEOMETRY,
    feature_type VARCHAR,
    -- GF(3) coloring
    seed BIGINT,
    gay_color VARCHAR,
    gf3_trit INTEGER,
    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert with color derivation
INSERT INTO geo_features VALUES (
    'sf-001',
    'San Francisco',
    ST_Point(-122.4194, 37.7749),
    'city',
    4815162342,  -- seed
    '#DC6B3B',   -- gay_color
    1,           -- trit (+1)
    CURRENT_TIMESTAMP
);
```

## H3 Hexagonal Indexing

```sql
-- Convert lat/lon to H3 index at resolution 9
SELECT h3_latlng_to_cell(37.7749, -122.4194, 9) as h3_index;

-- Get cell boundary as polygon
SELECT h3_cell_to_boundary_wkt(h3_latlng_to_cell(37.7749, -122.4194, 9));

-- Get neighbors (k-ring)
SELECT h3_grid_disk(h3_latlng_to_cell(37.7749, -122.4194, 9), 1) as neighbors;

-- Color H3 cells
CREATE TABLE h3_colored AS
SELECT 
    h3_latlng_to_cell(lat, lon, 9) as h3_index,
    COUNT(*) as point_count,
    -- Color from H3 index
    h3_latlng_to_cell(lat, lon, 9) % 3 - 1 as gf3_trit
FROM points
GROUP BY 1;
```

## Spatial Queries with Color

```sql
-- Find all features within 10km of a point
SELECT 
    f.name,
    f.gay_color,
    f.gf3_trit,
    ST_Distance_Spheroid(f.geometry, ST_Point(-122.4194, 37.7749)) / 1000 as dist_km
FROM geo_features f
WHERE ST_DWithin_Spheroid(
    f.geometry,
    ST_Point(-122.4194, 37.7749),
    10000  -- 10km in meters
)
ORDER BY dist_km;

-- Spatial join with GF(3) balance check
SELECT 
    a.name as region,
    COUNT(*) as point_count,
    SUM(b.gf3_trit) as trit_sum,
    SUM(b.gf3_trit) % 3 as gf3_balance
FROM regions a
JOIN points b ON ST_Contains(a.geometry, b.geometry)
GROUP BY a.name;
```

## Coordinate Reference Systems

```sql
-- Transform between CRS
SELECT ST_Transform(
    ST_Point(-122.4194, 37.7749),
    'EPSG:4326',  -- WGS84
    'EPSG:3857'   -- Web Mercator
) as web_mercator;

-- Area calculation in proper units
SELECT ST_Area(
    ST_Transform(geometry, 'EPSG:4326', 'EPSG:32610')  -- UTM Zone 10N
) / 1e6 as area_km2
FROM regions;
```

## GeoParquet Integration

```sql
-- Read GeoParquet files
SELECT * FROM read_parquet('cities.parquet');

-- Write with geometry
COPY (SELECT * FROM geo_features) TO 'features.parquet' (FORMAT PARQUET);

-- Create spatial index
CREATE INDEX geo_features_spatial_idx ON geo_features USING RTREE (geometry);
```

## Example: Colored City Analysis

```python
import duckdb
import hashlib

def seed_from_string(s: str) -> int:
    return int(hashlib.sha256(s.encode()).hexdigest()[:16], 16) & 0x7FFFFFFFFFFFFFFF

def analyze_cities_with_color(cities_geojson):
    conn = duckdb.connect()
    conn.execute("INSTALL spatial; LOAD spatial;")
    
    conn.execute("""
        CREATE TABLE cities AS
        SELECT 
            name,
            ST_GeomFromGeoJSON(geometry) as geom,
            population
        FROM read_json_auto(?)
    """, [cities_geojson])
    
    # Add colors
    conn.execute("""
        ALTER TABLE cities ADD COLUMN seed BIGINT;
        ALTER TABLE cities ADD COLUMN gay_color VARCHAR;
        ALTER TABLE cities ADD COLUMN gf3_trit INTEGER;
    """)
    
    # Update with deterministic colors
    cities = conn.execute("SELECT name FROM cities").fetchall()
    for (name,) in cities:
        seed = seed_from_string(name)
        hue = seed % 360
        trit = 1 if (hue < 60 or hue >= 300) else (0 if hue < 180 else -1)
        conn.execute("""
            UPDATE cities SET seed = ?, gf3_trit = ? WHERE name = ?
        """, [seed, trit, name])
    
    return conn

# Query with spatial + color
conn.execute("""
    SELECT 
        name,
        gf3_trit,
        ST_X(geom) as lon,
        ST_Y(geom) as lat,
        population
    FROM cities
    WHERE ST_DWithin_Spheroid(geom, ST_Point(-122, 37), 500000)
    ORDER BY population DESC
""")
```

## Triads

```
duckdb-spatial (0) ⊗ geodesic-manifold (-1) ⊗ geohash-coloring (+1) = 0 ✓
duckdb-spatial (0) ⊗ osm-topology (-1) ⊗ map-projection (+1) = 0 ✓
```

## References
- [DuckDB Spatial Extension](https://duckdb.org/docs/extensions/spatial)
- [H3 Hexagonal Grid](https://h3geo.org/)
- PostGIS Documentation



## Scientific Skill Interleaving

This skill connects to the K-Dense-AI/claude-scientific-skills ecosystem:

### Dataframes
- **polars** [○] via bicomodule
  - High-performance dataframes

### Geospatial
- **geopandas** [○] via bicomodule
  - Spatial data processing

### Bibliography References

- `general`: 734 citations in bib.duckdb

## Cat# Integration

This skill maps to **Cat# = Comod(P)** as a bicomodule in the equipment structure:

```
Trit: 0 (ERGODIC)
Home: Prof
Poly Op: ⊗
Kan Role: Adj
Color: #26D826
```

### GF(3) Naturality

The skill participates in triads satisfying:
```
(-1) + (0) + (+1) ≡ 0 (mod 3)
```

This ensures compositional coherence in the Cat# equipment structure.


## Forward Reference

- unified-reafference (spatial session mapping)