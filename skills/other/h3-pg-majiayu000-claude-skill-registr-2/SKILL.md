---
name: h3-pg
description: PostgreSQL bindings for H3 hexagonal grid system. Use when working with H3 cells in Postgres, including spatial indexing, geometry/geography integration, and raster analysis.
---

# h3-pg PostgreSQL Extension

## Extension Architecture

**Two extensions:**
- `CREATE EXTENSION h3` — Core H3 bindings (indexing, traversal, hierarchy, inspection, `<->` operator). No PostGIS dependency.
- `CREATE EXTENSION h3_postgis` — PostGIS integration (geometry/geography casts, `@` operator, polygon fill, raster helpers). Requires `postgis` and optionally `postgis_raster`.

## Postgres-Specific H3 Features

These exist only in h3-pg, not other H3 language bindings.

**Direct casts** (`h3_postgis`):
- `h3index::geometry` → cell centroid as POINT, SRID 4326
- `h3index::geography` → cell centroid as POINT, SRID 4326

**Operators:**
- `a <-> b` — grid distance in cells between two h3index values (`h3`)
- `geom @ resolution` — index geometry/geography at resolution (`h3_postgis`)

**Operator classes** for `h3index`: BTREE, HASH, BRIN, SP-GIST (`h3`)

**Boundary helpers** (`h3_postgis`):
- `h3_cell_to_boundary_geometry(h3index)` → polygon with SRID 4326, splits at antimeridian
- `h3_cell_to_boundary_geography(h3index)` → geography polygon, splits at antimeridian

**Polygon fill** (`h3_postgis`):
- `h3_polygon_to_cells(geometry, resolution)` → SETOF h3index
- `h3_polygon_to_cells(geography, resolution)` → SETOF h3index

**Raster integration** (`h3_postgis`, requires `postgis_raster`):
- `h3_raster_summary(raster, resolution, [band])` — per-cell stats (count, sum, mean, stddev, min, max)
- `h3_raster_summary_clip(...)` — clips raster by cell boundaries
- `h3_raster_summary_centroids(...)` — uses cell centroids, avoids pentagon edge cases
- `h3_raster_summary_subpixel(...)` — for cells smaller than pixels
- `h3_raster_class_summary*(...)` — discrete class counts per cell

**Tile helper** (`h3_postgis`):
- `h3_get_resolution_from_tile_zoom(z, [max_h3_resolution=15], [min_h3_resolution], [hex_edge_pixels=44], [tile_size=512])` — returns optimal H3 resolution for XYZ tile zoom level `z`, targeting hexagons approximately `hex_edge_pixels` wide on screen

## Common Pattern Fixes

| Pattern | DO NOT | DO |
|---------|--------|----|
| Get centroid | `ST_Centroid(h3_cell_to_boundary_geometry(h3))` | `h3::geometry` |
| Get boundary with SRID | `h3_cell_to_boundary(h3)::geometry` | `h3_cell_to_boundary_geometry(h3)` |
| Distance check (meters) | `ST_Distance(a.h3::geography, b.h3::geography) <= N` | `ST_DWithin(a.h3::geography, b.h3::geography, N)` |
| Grid distance (cells) | `h3_distance(a, b)` | `a <-> b` |

**Antimeridian gotcha:** Cells crossing 180° are split into valid polygons. `ST_Centroid` of a split polygon may fall outside the cell — use `h3::geometry` for centroids instead.

## Critical v3 → v4 Renames

| v3 Name (DO NOT USE) | v4 Replacement |
|---------------------|----------------|
| `h3_geo_to_h3` | `h3_latlng_to_cell` |
| `h3_to_geo` | `h3_cell_to_latlng` |
| `h3_to_geo_boundary` | `h3_cell_to_boundary` |
| `h3_k_ring` | `h3_grid_disk` |
| `h3_k_ring_distances` | `h3_grid_disk_distances` |
| `h3_hex_ring` | `h3_grid_ring_unsafe` |
| `h3_line` | `h3_grid_path_cells` |
| `h3_distance` | `h3_grid_distance` |
| `h3_to_parent` | `h3_cell_to_parent` |
| `h3_to_children` | `h3_cell_to_children` |
| `h3_compact` | `h3_compact_cells` |
| `h3_uncompact` | `h3_uncompact_cells` |
| `h3_polyfill` | `h3_polygon_to_cells` |
| `h3_indexes_are_neighbors` | `h3_are_neighbor_cells` |
| `h3_hex_area` | `h3_get_hexagon_area_avg` |
| `h3_hex_area_km2` / `h3_hex_area_m2` | `h3_get_hexagon_area_avg(res, unit)` |
| `h3_edge_length_km` / `h3_edge_length_m` | `h3_get_hexagon_edge_length_avg(res, unit)` |

**Unit parameters (v4):** Area and length functions now take a `unit` text parameter:
- `h3_get_hexagon_area_avg(resolution, [unit = 'km^2'])` — use `'km^2'` or `'m^2'`
- `h3_get_hexagon_edge_length_avg(resolution, [unit = 'km'])` — use `'km'` or `'m'`
- `h3_cell_area(cell, [unit = 'km^2'])` — exact area for specific cell
- `h3_edge_length(edge, [unit = 'km'])` — exact length for specific edge

**Spelling change (v4.2.3+):** Prefer `h3_latlng_to_cell` over `h3_lat_lng_to_cell` (underscore version deprecated). Same for `h3_cell_to_latlng`, `h3_vertex_to_latlng`.

## Documentation

- API reference: https://github.com/zachasme/h3-pg/blob/main/docs/api.md
- v3→v4 migration: https://h3geo.org/docs/library/migration-3.x/functions
