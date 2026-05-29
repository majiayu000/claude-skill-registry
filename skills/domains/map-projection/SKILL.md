---
name: map-projection
description: Map Projection Skill
version: 1.0.0
---

# Map Projection Skill

Category theory of map projections: functors between manifolds with distortion analysis.

## Trigger
- Map projection selection and analysis
- Distortion metrics (Tissot's indicatrix)
- Coordinate system transformations
- Cartographic design decisions

## GF(3) Trit: +1 (Generator)
Generates projections from sphere to plane, creating new coordinate representations.

## Category Theory of Projections

A map projection is a functor:
```
P: Sphere → Plane
   S² → ℝ²
```

Different projections preserve different properties:
- **Conformal** (angle-preserving): Mercator, Stereographic
- **Equal-area**: Albers, Lambert, Mollweide
- **Equidistant**: Azimuthal equidistant
- **Compromise**: Robinson, Winkel Tripel

## Projection Functors

```python
import math

class Projection:
    """Base projection functor."""
    
    def forward(self, lat, lon):
        """S² → ℝ²"""
        raise NotImplementedError
    
    def inverse(self, x, y):
        """ℝ² → S²"""
        raise NotImplementedError
    
    @property
    def distortion_type(self):
        raise NotImplementedError

class Mercator(Projection):
    """Conformal cylindrical projection."""
    
    def forward(self, lat, lon):
        x = math.radians(lon)
        y = math.log(math.tan(math.pi/4 + math.radians(lat)/2))
        return x, y
    
    def inverse(self, x, y):
        lon = math.degrees(x)
        lat = math.degrees(2 * math.atan(math.exp(y)) - math.pi/2)
        return lat, lon
    
    @property
    def distortion_type(self):
        return "conformal"  # Preserves angles

class LambertAzimuthal(Projection):
    """Equal-area azimuthal projection."""
    
    def __init__(self, lat0=0, lon0=0):
        self.lat0 = math.radians(lat0)
        self.lon0 = math.radians(lon0)
    
    def forward(self, lat, lon):
        phi = math.radians(lat)
        lam = math.radians(lon)
        
        k = math.sqrt(2 / (1 + math.sin(self.lat0)*math.sin(phi) + 
                          math.cos(self.lat0)*math.cos(phi)*math.cos(lam - self.lon0)))
        
        x = k * math.cos(phi) * math.sin(lam - self.lon0)
        y = k * (math.cos(self.lat0)*math.sin(phi) - 
                 math.sin(self.lat0)*math.cos(phi)*math.cos(lam - self.lon0))
        return x, y
    
    @property
    def distortion_type(self):
        return "equal-area"  # Preserves area

class Stereographic(Projection):
    """Conformal azimuthal projection."""
    
    def __init__(self, lat0=90, lon0=0):
        self.lat0 = math.radians(lat0)
        self.lon0 = math.radians(lon0)
    
    def forward(self, lat, lon):
        phi = math.radians(lat)
        lam = math.radians(lon)
        
        k = 2 / (1 + math.sin(self.lat0)*math.sin(phi) + 
                 math.cos(self.lat0)*math.cos(phi)*math.cos(lam - self.lon0))
        
        x = k * math.cos(phi) * math.sin(lam - self.lon0)
        y = k * (math.cos(self.lat0)*math.sin(phi) - 
                 math.sin(self.lat0)*math.cos(phi)*math.cos(lam - self.lon0))
        return x, y
    
    @property
    def distortion_type(self):
        return "conformal"
```

## Tissot's Indicatrix (Distortion Analysis)

```python
def tissot_indicatrix(projection, lat, lon, delta=0.01):
    """
    Compute Tissot's indicatrix at a point.
    Returns semi-major axis a, semi-minor axis b, and rotation theta.
    """
    # Jacobian via finite differences
    x0, y0 = projection.forward(lat, lon)
    x1, y1 = projection.forward(lat + delta, lon)
    x2, y2 = projection.forward(lat, lon + delta)
    
    # Partial derivatives
    dx_dlat = (x1 - x0) / delta
    dy_dlat = (y1 - y0) / delta
    dx_dlon = (x2 - x0) / delta
    dy_dlon = (y2 - y0) / delta
    
    # Scale factors
    h = math.sqrt(dx_dlat**2 + dy_dlat**2)  # meridian scale
    k = math.sqrt(dx_dlon**2 + dy_dlon**2) / math.cos(math.radians(lat))  # parallel scale
    
    # Angular distortion
    sin_theta = (dx_dlat * dy_dlon - dy_dlat * dx_dlon) / (h * k * math.cos(math.radians(lat)))
    
    # Area distortion
    area_factor = h * k * sin_theta
    
    return {
        'h': h,  # meridian scale
        'k': k,  # parallel scale
        'area_factor': area_factor,
        'angular_distortion': math.degrees(math.asin(1 - abs(sin_theta)))
    }
```

## Projection with GF(3) Coloring

```python
def project_with_color(projection, lat, lon, seed):
    """Project point and assign GF(3) color."""
    x, y = projection.forward(lat, lon)
    
    # Derive color from seed + projected coords
    point_seed = int((seed + hash((x, y))) & 0x7FFFFFFFFFFFFFFF)
    hue = point_seed % 360
    
    if hue < 60 or hue >= 300:
        trit = 1   # Red → Generator
    elif hue < 180:
        trit = 0   # Green → Ergodic
    else:
        trit = -1  # Blue → Validator
    
    return {
        'lat': lat,
        'lon': lon,
        'x': x,
        'y': y,
        'projection': projection.__class__.__name__,
        'distortion_type': projection.distortion_type,
        'seed': point_seed,
        'trit': trit
    }
```

## Natural Transformations Between Projections

```python
def projection_morphism(P1, P2, lat, lon):
    """
    Natural transformation between projections.
    P1 → P2 via S² (the universal object).
    """
    # Forward through P1
    x1, y1 = P1.forward(lat, lon)
    
    # Inverse to sphere
    lat_s, lon_s = P1.inverse(x1, y1)
    
    # Forward through P2
    x2, y2 = P2.forward(lat_s, lon_s)
    
    return {
        'source': (x1, y1),
        'target': (x2, y2),
        'sphere_point': (lat_s, lon_s),
        'transformation': f"{P1.__class__.__name__} → {P2.__class__.__name__}"
    }

# All projections form a category with S² as terminal object
# The "best" projection is context-dependent (no universal winner)
```

## DuckDB Integration

```sql
-- Create projection lookup table
CREATE TABLE projections (
    projection_id VARCHAR PRIMARY KEY,
    name VARCHAR,
    type VARCHAR,  -- conformal, equal-area, equidistant, compromise
    suitable_for VARCHAR[],
    gf3_trit INTEGER DEFAULT 1  -- Generator
);

INSERT INTO projections VALUES
    ('mercator', 'Mercator', 'conformal', ['navigation', 'web_maps'], 1),
    ('albers', 'Albers Equal-Area', 'equal-area', ['thematic_maps', 'usa'], 1),
    ('robinson', 'Robinson', 'compromise', ['world_maps', 'education'], 1),
    ('utm', 'UTM', 'conformal', ['surveying', 'military'], 1);

-- Select projection based on use case
SELECT * FROM projections 
WHERE 'navigation' = ANY(suitable_for);
```

## Triads

```
map-projection (+1) ⊗ duckdb-spatial (0) ⊗ osm-topology (-1) = 0 ✓
map-projection (+1) ⊗ geodesic-manifold (0) ⊗ geohash-coloring (-1) = 0 ✓
```

## References
- Snyder, "Map Projections: A Working Manual"
- PROJ library documentation
- Tissot's Indicatrix theory



## Scientific Skill Interleaving

This skill connects to the K-Dense-AI/claude-scientific-skills ecosystem:

### Geospatial
- **geopandas** [○] via bicomodule

### Bibliography References

- `general`: 734 citations in bib.duckdb



## SDF Interleaving

This skill connects to **Software Design for Flexibility** (Hanson & Sussman, 2021):

### Primary Chapter: 10. Adventure Game Example

**Concepts**: autonomous agent, game, synthesis

### GF(3) Balanced Triad

```
map-projection (−) + SDF.Ch10 (+) + [balancer] (○) = 0
```

**Skill Trit**: -1 (MINUS - verification)


### Connection Pattern

Adventure games synthesize techniques. This skill integrates multiple patterns.
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