---
name: geodesic-manifold
description: 'Geodesic Manifold Skill'
version: 1.0.0
---

# Geodesic Manifold Skill

Spherical geometry, great circles, and Riemannian manifolds with Gay.jl coloring.

## Trigger
- Geodesic calculations, great circle routes
- Spherical trigonometry, haversine distance
- Riemannian geometry on Earth's surface
- Flight paths, navigation, ship routing

## GF(3) Trit Assignment
- **+1 (Generator)**: Creates geodesic paths, generates waypoints
- **0 (Ergodic)**: Distance calculations, coordinate transforms
- **-1 (Validator)**: Verifies shortest path optimality

## Core Concepts

### Great Circle Distance (Haversine)
```python
import math

def haversine(lat1, lon1, lat2, lon2):
    """Distance in km between two points on Earth."""
    R = 6371  # Earth radius km
    
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    
    a = math.sin(dphi/2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    
    return R * c
```

### Geodesic Waypoints with Color
```python
def geodesic_waypoints(lat1, lon1, lat2, lon2, n_points, seed):
    """Generate colored waypoints along great circle."""
    from math import radians, degrees, sin, cos, atan2, sqrt
    
    # Convert to radians
    phi1, lambda1 = radians(lat1), radians(lon1)
    phi2, lambda2 = radians(lat2), radians(lon2)
    
    waypoints = []
    for i in range(n_points + 1):
        f = i / n_points  # Fraction along path
        
        # Spherical interpolation (slerp)
        d = haversine(lat1, lon1, lat2, lon2) / 6371
        a = sin((1 - f) * d) / sin(d)
        b = sin(f * d) / sin(d)
        
        x = a * cos(phi1) * cos(lambda1) + b * cos(phi2) * cos(lambda2)
        y = a * cos(phi1) * sin(lambda1) + b * cos(phi2) * sin(lambda2)
        z = a * sin(phi1) + b * sin(phi2)
        
        lat = degrees(atan2(z, sqrt(x**2 + y**2)))
        lon = degrees(atan2(y, x))
        
        # Color from seed + index
        wp_seed = (seed + i * 0x9E3779B97F4A7C15) & 0x7FFFFFFFFFFFFFFF
        color = color_from_seed(wp_seed)
        
        waypoints.append({
            'index': i,
            'lat': lat,
            'lon': lon,
            'fraction': f,
            'color': color['hex'],
            'trit': color['trit']
        })
    
    return waypoints
```

### Riemannian Metric on Sphere
```python
def spherical_metric(lat, lon):
    """
    Riemannian metric tensor at point (lat, lon).
    
    ds² = R²(dφ² + cos²φ dλ²)
    
    Returns 2x2 metric tensor g_ij.
    """
    R = 6371  # km
    phi = math.radians(lat)
    
    g = [
        [R**2, 0],
        [0, R**2 * math.cos(phi)**2]
    ]
    return g

def christoffel_symbols(lat):
    """
    Christoffel symbols for sphere.
    Non-zero: Γ^φ_λλ = sin(φ)cos(φ), Γ^λ_φλ = -tan(φ)
    """
    phi = math.radians(lat)
    return {
        'phi_lambda_lambda': math.sin(phi) * math.cos(phi),
        'lambda_phi_lambda': -math.tan(phi)
    }
```

## DuckDB Spatial Integration

```sql
-- Install spatial extension
INSTALL spatial;
LOAD spatial;

-- Create geodesic table with colors
CREATE TABLE geodesic_routes (
    route_id VARCHAR,
    origin GEOMETRY,
    destination GEOMETRY,
    distance_km DOUBLE,
    seed BIGINT,
    gay_color VARCHAR,
    gf3_trit INTEGER
);

-- Calculate great circle distance
SELECT ST_Distance_Spheroid(
    ST_Point(-122.4194, 37.7749),  -- San Francisco
    ST_Point(-0.1276, 51.5074)     -- London
) / 1000 as distance_km;
```

## Manifold Category Theory

The sphere S² is a 2-dimensional Riemannian manifold:

```
Geodesic: Hom(I, S²) where I = [0,1]
Parallel Transport: Functor from Path groupoid to GL(T_p S²)
Holonomy: π₁(S²) → Aut(fiber)
```

### Fiber Bundle Structure
```
Tangent Bundle: TS² → S²
Frame Bundle: F(S²) → S² with fiber GL(2,ℝ)
Spinor Bundle: Spin(S²) → S² (for quantum geography)
```

## Example: Flight Route Coloring

```python
def color_flight_route(origin, destination, seed=42):
    """Color a flight route with GF(3) balanced waypoints."""
    waypoints = geodesic_waypoints(
        origin['lat'], origin['lon'],
        destination['lat'], destination['lon'],
        n_points=10,
        seed=seed
    )
    
    # Verify GF(3) balance
    trit_sum = sum(wp['trit'] for wp in waypoints)
    
    return {
        'origin': origin,
        'destination': destination,
        'waypoints': waypoints,
        'total_distance_km': haversine(
            origin['lat'], origin['lon'],
            destination['lat'], destination['lon']
        ),
        'gf3_sum': trit_sum,
        'gf3_mod3': trit_sum % 3
    }

# San Francisco to Tokyo
route = color_flight_route(
    {'lat': 37.7749, 'lon': -122.4194, 'name': 'SFO'},
    {'lat': 35.6762, 'lon': 139.6503, 'name': 'NRT'},
    seed=69
)
```

## References
- Riemannian Geometry (do Carmo)
- Differential Geometry of Curves and Surfaces
- Geodesy and Map Projections
