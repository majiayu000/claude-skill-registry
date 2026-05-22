---
name: geospatial-data-pipeline
description: Process, analyze, and visualize geospatial data at scale. Handles drone imagery, GPS tracks, GeoJSON optimization, coordinate transformations, and tile generation. Use for mapping apps, drone data processing, location-based services. Activate on "geospatial", "GIS", "PostGIS", "GeoJSON", "map tiles", "coordinate systems". NOT for simple address validation, basic distance calculations, or static map embeds.
allowed-tools: Read,Write,Edit,Bash(npm:*,gdal*,postgres*)
---

# Geospatial Data Pipeline

Expert in processing, optimizing, and visualizing geospatial data at scale.

## When to Use

✅ **Use for**:
- Drone imagery processing and annotation
- GPS track analysis and visualization
- Location-based search (find nearby X)
- Map tile generation for web/mobile
- Coordinate system transformations
- Geofencing and spatial queries
- GeoJSON optimization for web

❌ **NOT for**:
- Simple address validation (use address APIs)
- Basic distance calculations (use Haversine formula)
- Static map embeds (use Mapbox Static API)
- Geocoding (use Nominatim or Google Geocoding API)

---

## Technology Selection

### Database: PostGIS vs MongoDB Geospatial

| Feature | PostGIS | MongoDB |
|---------|---------|---------|
| Spatial indexes | GiST, SP-GiST | 2dsphere |
| Query language | SQL + spatial functions | Aggregation pipeline |
| Geometry types | 20+ (full OGC support) | Basic (Point, Line, Polygon) |
| Coordinate systems | 6000+ via EPSG | WGS84 only |
| Performance (10M points) | &lt;100ms | &lt;200ms |
| Best for | Complex spatial analysis | Document-centric apps |

**Timeline**:
- 2005: PostGIS 1.0 released
- 2012: MongoDB adds geospatial indexes
- 2020: PostGIS 3.0 with improved performance
- 2024: PostGIS remains gold standard for GIS workloads

---

## Common Anti-Patterns

### Anti-Pattern 1: Storing Coordinates as Strings

**Novice thinking**: "I'll just store lat/lon as text, it's simple"

**Problem**: Can't use spatial indexes, queries are slow, no validation.

**Wrong approach**:
```typescript
// ❌ String storage, no spatial features
interface Location {
  id: string;
  name: string;
  latitude: string;   // "37.7749"
  longitude: string;  // "-122.4194"
}

// Linear scan for "nearby" queries
async function findNearby(lat: string, lon: string): Promise<Location[]> {
  const all = await db.locations.findAll();

  return all.filter(loc => {
    const distance = calculateDistance(
      parseFloat(lat),
      parseFloat(lon),
      parseFloat(loc.latitude),
      parseFloat(loc.longitude)
    );
    return distance < 5000; // 5km
  });
}
```

**Why wrong**: O(N) linear scan, no spatial index, string parsing overhead.

**Correct approach**:
```typescript
// ✅ PostGIS GEOGRAPHY type with spatial index
CREATE TABLE locations (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255),
  location GEOGRAPHY(POINT, 4326)  -- WGS84 coordinates
);

-- Spatial index (GiST)
CREATE INDEX idx_locations_geography ON locations USING GIST(location);

-- TypeScript query
async function findNearby(lat: number, lon: number, radiusMeters: number): Promise<Location[]> {
  const query = `
    SELECT id, name, ST_AsGeoJSON(location) as geojson
    FROM locations
    WHERE ST_DWithin(
      location,
      ST_SetSRID(ST_MakePoint($1, $2), 4326)::geography,
      $3
    )
    ORDER BY location <-> ST_SetSRID(ST_MakePoint($1, $2), 4326)::geography
    LIMIT 100
  `;

  return db.query(query, [lon, lat, radiusMeters]);  // &lt;10ms with index
}
```

**Timeline context**:
- 2000s: Stored lat/lon as FLOAT columns, did math in app code
- 2010s: PostGIS adoption, spatial indexes
- 2024: `GEOGRAPHY` type handles Earth curvature automatically

---

### Anti-Pattern 2: Not Using Spatial Indexes

**Problem**: Proximity queries do full table scans.

**Wrong approach**:
```sql
-- ❌ No index, sequential scan
CREATE TABLE drone_images (
  id SERIAL PRIMARY KEY,
  image_url VARCHAR(255),
  location GEOGRAPHY(POINT, 4326)
);

-- This query scans ALL rows
SELECT * FROM drone_images
WHERE ST_DWithin(
  location,
  ST_SetSRID(ST_MakePoint(-122.4194, 37.7749), 4326)::geography,
  1000  -- 1km
);
```

**EXPLAIN output**: `Seq Scan on drone_images (cost=0.00..1234.56 rows=1 width=123)`

**Correct approach**:
```sql
-- ✅ GiST index for spatial queries
CREATE INDEX idx_drone_images_location ON drone_images USING GIST(location);

-- Same query, now uses index
SELECT * FROM drone_images
WHERE ST_DWithin(
  location,
  ST_SetSRID(ST_MakePoint(-122.4194, 37.7749), 4326)::geography,
  1000
);
```

**EXPLAIN output**: `Bitmap Index Scan on idx_drone_images_location (cost=4.30..78.30 rows=50 width=123)`

**Performance impact**: 10M points, 5km radius query
- Without index: 3.2 seconds (full scan)
- With GiST index: 12ms (99.6% faster)

---

### Anti-Pattern 3: Mixing Coordinate Systems

**Novice thinking**: "Coordinates are just numbers, I can mix them"

**Problem**: Incorrect distances, misaligned map features.

**Wrong approach**:
```typescript
// ❌ Mixing EPSG:4326 (WGS84) and EPSG:3857 (Web Mercator)
const userLocation = {
  lat: 37.7749,   // WGS84
  lon: -122.4194
};

const droneImage = {
  x: -13634876,  // Web Mercator (EPSG:3857)
  y: 4545684
};

// Comparing apples to oranges!
const distance = Math.sqrt(
  Math.pow(userLocation.lon - droneImage.x, 2) +
  Math.pow(userLocation.lat - droneImage.y, 2)
);
```

**Result**: Wildly incorrect distance (millions of "units").

**Correct approach**:
```sql
-- ✅ Transform to common coordinate system
SELECT ST_Distance(
  ST_Transform(
    ST_SetSRID(ST_MakePoint(-122.4194, 37.7749), 4326),  -- WGS84
    3857  -- Transform to Web Mercator
  ),
  ST_SetSRID(ST_MakePoint(-13634876, 4545684), 3857)  -- Already Web Mercator
) AS distance_meters;
```

**Or better**: Always store in one system (WGS84), transform on display only.

**Timeline**:
- 2005: Web Mercator (EPSG:3857) introduced by Google Maps
- 2010: Confusion peaks as apps mix WGS84 data with Web Mercator tiles
- 2024: Best practice: Store WGS84, transform to 3857 only for tile rendering

---

### Anti-Pattern 4: Loading Huge GeoJSON Files

**Problem**: 50MB GeoJSON file crashes browser.

**Wrong approach**:
```typescript
// ❌ Load entire file into memory
const geoJson = await fetch('/drone-survey-data.geojson').then(r => r.json());

// 50MB of GeoJSON = browser freeze
map.addSource('drone-data', {
  type: 'geojson',
  data: geoJson  // All 10,000 polygons loaded at once
});
```

**Correct approach 1**: Vector tiles (pre-chunked)
```typescript
// ✅ Serve as vector tiles (MBTiles or PMTiles)
map.addSource('drone-data', {
  type: 'vector',
  tiles: ['https://api.example.com/tiles/{z}/{x}/{y}.pbf'],
  minzoom: 10,
  maxzoom: 18
});

// Browser only loads visible tiles
```

**Correct approach 2**: GeoJSON simplification + chunking
```bash
# Simplify geometry (reduce points)
npm install -g @mapbox/geojson-precision
geojson-precision -p 5 input.geojson output.geojson

# Split into tiles
npm install -g geojson-vt
# Generate tiles programmatically (see scripts/tile_generator.ts)
```

**Correct approach 3**: Server-side filtering
```typescript
// ✅ Only fetch visible bounds
async function fetchVisibleFeatures(bounds: Bounds): Promise<GeoJSON> {
  const response = await fetch(
    `/api/features?bbox=${bounds.west},${bounds.south},${bounds.east},${bounds.north}`
  );
  return response.json();
}

map.on('moveend', async () => {
  const bounds = map.getBounds();
  const geojson = await fetchVisibleFeatures(bounds);
  map.getSource('dynamic-data').setData(geojson);
});
```

---

### Anti-Pattern 5: Euclidean Distance on Spherical Earth

**Novice thinking**: "Distance is just Pythagorean theorem"

**Problem**: Incorrect at scale, worse near poles.

**Wrong approach**:
```typescript
// ❌ Flat Earth distance (wrong!)
function distanceKm(lat1: number, lon1: number, lat2: number, lon2: number): number {
  const dx = lon2 - lon1;
  const dy = lat2 - lat1;

  return Math.sqrt(dx * dx + dy * dy) * 111.32;  // 111.32 km/degree (WRONG)
}

// Example: San Francisco to New York
const distance = distanceKm(37.7749, -122.4194, 40.7128, -74.0060);
// Returns: ~55 km (WRONG! Actual: ~4,130 km)
```

**Why wrong**: Earth is a sphere, not a flat plane.

**Correct approach 1**: Haversine formula (great circle distance)
```typescript
// ✅ Haversine formula (spherical Earth)
function haversineKm(lat1: number, lon1: number, lat2: number, lon2: number): number {
  const R = 6371; // Earth radius in km

  const dLat = toRadians(lat2 - lat1);
  const dLon = toRadians(lon2 - lon1);

  const a =
    Math.sin(dLat / 2) * Math.sin(dLat / 2) +
    Math.cos(toRadians(lat1)) * Math.cos(toRadians(lat2)) *
    Math.sin(dLon / 2) * Math.sin(dLon / 2);

  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));

  return R * c;
}

// San Francisco to New York
const distance = haversineKm(37.7749, -122.4194, 40.7128, -74.0060);
// Returns: ~4,130 km ✅
```

**Correct approach 2**: PostGIS (handles curvature automatically)
```sql
-- ✅ PostGIS ST_Distance with GEOGRAPHY
SELECT ST_Distance(
  ST_SetSRID(ST_MakePoint(-122.4194, 37.7749), 4326)::geography,
  ST_SetSRID(ST_MakePoint(-74.0060, 40.7128), 4326)::geography
) / 1000 AS distance_km;
-- Returns: 4130.137 km ✅
```

**Accuracy comparison**:
| Method | SF to NYC | Error |
|--------|-----------|-------|
| Euclidean (flat) | 55 km | 98.7% wrong |
| Haversine (sphere) | 4,130 km | ✅ Correct |
| PostGIS (ellipsoid) | 4,135 km | Most accurate |

---

## Production Checklist

```
□ PostGIS extension installed and spatial indexes created
□ All coordinates stored in consistent SRID (recommend: 4326)
□ GeoJSON files optimized (&lt;1MB) or served as vector tiles
□ Coordinate transformations use ST_Transform, not manual math
□ Distance calculations use ST_Distance with GEOGRAPHY type
□ Bounding box queries use ST_MakeEnvelope + ST_Intersects
□ Large geometries chunked (not &gt;100KB per feature)
□ Map tiles pre-generated for common zoom levels
□ CORS configured for tile servers
□ Rate limiting on geocoding/reverse geocoding endpoints
```

---

## When to Use vs Avoid

| Scenario | Appropriate? |
|----------|--------------|
| Drone imagery annotation and search | ✅ Yes - process survey data |
| GPS track visualization | ✅ Yes - optimize paths |
| Find nearest coffee shops | ✅ Yes - spatial queries |
| Jurisdiction boundary lookups | ✅ Yes - point-in-polygon |
| Simple address autocomplete | ❌ No - use Mapbox/Google |
| Embed static map on page | ❌ No - use Static API |
| Geocode single address | ❌ No - use geocoding API |

---

## References

- `/references/coordinate-systems.md` - EPSG codes, transformations, Web Mercator vs WGS84
- `/references/postgis-guide.md` - PostGIS setup, spatial indexes, common queries
- `/references/geojson-optimization.md` - Simplification, chunking, vector tiles

## Scripts

- `scripts/geospatial_processor.ts` - Process drone imagery, GPS tracks, GeoJSON validation
- `scripts/tile_generator.ts` - Generate vector tiles (MBTiles/PMTiles) from GeoJSON

---

**This skill guides**: Geospatial data | PostGIS | GeoJSON | Map tiles | Coordinate systems | Drone data processing | Spatial queries
