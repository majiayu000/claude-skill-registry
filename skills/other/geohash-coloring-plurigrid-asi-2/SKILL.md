---
name: geohash-coloring
description: 'Geohash Coloring Skill'
version: 1.0.0
---

# Geohash Coloring Skill

GF(3) colored geohashes for hierarchical spatial indexing with deterministic color derivation.

## Trigger
- Geohash encoding/decoding
- Hierarchical spatial clustering
- Location-based coloring schemes
- Privacy-preserving location representation

## GF(3) Trit: +1 (Generator)
Generates colored spatial identifiers from coordinates.

## Geohash Basics

Geohash encodes lat/lon into a string where:
- Longer = more precise
- Prefix = parent cell
- Adjacent cells share prefixes

```
Precision | Cell Width | Cell Height
    1     |  5,009 km  |  4,992 km
    2     |  1,252 km  |    624 km
    3     |    156 km  |    156 km
    4     |     39 km  |     19 km
    5     |      5 km  |      5 km
    6     |    1.2 km  |    0.6 km
    7     |    153 m   |    153 m
    8     |     38 m   |     19 m
    9     |      5 m   |      5 m
```

## Core Implementation

```python
import hashlib

# Geohash alphabet (base32)
GEOHASH_CHARS = '0123456789bcdefghjkmnpqrstuvwxyz'

def encode_geohash(lat: float, lon: float, precision: int = 9) -> str:
    """Encode lat/lon to geohash string."""
    lat_range = (-90.0, 90.0)
    lon_range = (-180.0, 180.0)
    
    geohash = []
    bits = 0
    bit_count = 0
    is_lon = True
    
    while len(geohash) < precision:
        if is_lon:
            mid = (lon_range[0] + lon_range[1]) / 2
            if lon >= mid:
                bits = (bits << 1) | 1
                lon_range = (mid, lon_range[1])
            else:
                bits = bits << 1
                lon_range = (lon_range[0], mid)
        else:
            mid = (lat_range[0] + lat_range[1]) / 2
            if lat >= mid:
                bits = (bits << 1) | 1
                lat_range = (mid, lat_range[1])
            else:
                bits = bits << 1
                lat_range = (lat_range[0], mid)
        
        is_lon = not is_lon
        bit_count += 1
        
        if bit_count == 5:
            geohash.append(GEOHASH_CHARS[bits])
            bits = 0
            bit_count = 0
    
    return ''.join(geohash)

def decode_geohash(geohash: str) -> tuple[float, float, float, float]:
    """Decode geohash to bounding box (lat_min, lat_max, lon_min, lon_max)."""
    lat_range = [-90.0, 90.0]
    lon_range = [-180.0, 180.0]
    is_lon = True
    
    for char in geohash:
        idx = GEOHASH_CHARS.index(char.lower())
        for i in range(4, -1, -1):
            bit = (idx >> i) & 1
            if is_lon:
                mid = (lon_range[0] + lon_range[1]) / 2
                if bit:
                    lon_range[0] = mid
                else:
                    lon_range[1] = mid
            else:
                mid = (lat_range[0] + lat_range[1]) / 2
                if bit:
                    lat_range[0] = mid
                else:
                    lat_range[1] = mid
            is_lon = not is_lon
    
    return lat_range[0], lat_range[1], lon_range[0], lon_range[1]

def geohash_center(geohash: str) -> tuple[float, float]:
    """Get center point of geohash cell."""
    lat_min, lat_max, lon_min, lon_max = decode_geohash(geohash)
    return (lat_min + lat_max) / 2, (lon_min + lon_max) / 2
```

## GF(3) Coloring

```python
# SplitMix64 constants
GOLDEN = 0x9E3779B97F4A7C15
MIX1 = 0xBF58476D1CE4E5B9
MIX2 = 0x94D049BB133111EB
MASK64 = 0xFFFFFFFFFFFFFFFF

def splitmix64(seed: int) -> tuple[int, int]:
    state = (seed + GOLDEN) & MASK64
    z = state
    z = ((z ^ (z >> 30)) * MIX1) & MASK64
    z = ((z ^ (z >> 27)) * MIX2) & MASK64
    z = z ^ (z >> 31)
    return state, z

def color_geohash(geohash: str) -> dict:
    """Assign GF(3) color to geohash."""
    # Seed from geohash string
    seed = int(hashlib.sha256(geohash.encode()).hexdigest()[:16], 16)
    seed = seed & 0x7FFFFFFFFFFFFFFF
    
    _, z = splitmix64(seed)
    hue = z % 360
    
    # Trit from hue region
    if hue < 60 or hue >= 300:
        trit = 1   # Red → Generator
    elif hue < 180:
        trit = 0   # Green → Ergodic
    else:
        trit = -1  # Blue → Validator
    
    # HSL to hex
    h = hue / 360.0
    s, l = 0.7, 0.55
    c = (1 - abs(2 * l - 1)) * s
    x = c * (1 - abs((h * 6) % 2 - 1))
    m = l - c / 2
    h6 = int(h * 6)
    
    if h6 == 0: r, g, b = c, x, 0
    elif h6 == 1: r, g, b = x, c, 0
    elif h6 == 2: r, g, b = 0, c, x
    elif h6 == 3: r, g, b = 0, x, c
    elif h6 == 4: r, g, b = x, 0, c
    else: r, g, b = c, 0, x
    
    hex_color = '#{:02X}{:02X}{:02X}'.format(
        int((r + m) * 255), int((g + m) * 255), int((b + m) * 255))
    
    lat, lon = geohash_center(geohash)
    
    return {
        'geohash': geohash,
        'lat': lat,
        'lon': lon,
        'precision': len(geohash),
        'seed': seed,
        'hue': hue,
        'hex': hex_color,
        'trit': trit
    }

def colored_geohash(lat: float, lon: float, precision: int = 9) -> dict:
    """Encode and color in one step."""
    gh = encode_geohash(lat, lon, precision)
    return color_geohash(gh)
```

## Hierarchical Coloring

```python
def geohash_hierarchy(lat: float, lon: float, max_precision: int = 9) -> list[dict]:
    """
    Get colored geohash at all precision levels.
    Enables hierarchical spatial visualization.
    """
    full_hash = encode_geohash(lat, lon, max_precision)
    
    hierarchy = []
    for p in range(1, max_precision + 1):
        prefix = full_hash[:p]
        colored = color_geohash(prefix)
        hierarchy.append(colored)
    
    return hierarchy

def gf3_balance_at_level(geohashes: list[str]) -> dict:
    """Check GF(3) balance for a set of geohashes."""
    trit_sum = 0
    by_trit = {-1: [], 0: [], 1: []}
    
    for gh in geohashes:
        colored = color_geohash(gh)
        trit_sum += colored['trit']
        by_trit[colored['trit']].append(gh)
    
    return {
        'count': len(geohashes),
        'trit_sum': trit_sum,
        'mod3': trit_sum % 3,
        'balanced': trit_sum % 3 == 0,
        'by_trit': {
            'plus': len(by_trit[1]),
            'ergodic': len(by_trit[0]),
            'minus': len(by_trit[-1])
        }
    }
```

## Neighbors with Color

```python
GEOHASH_NEIGHBORS = {
    'n': {'even': 'p0r21436x8zb9dcf5h7kjnmqesgutwvy', 'odd': 'bc01fg45238967deuvhjyznpkmstqrwx'},
    's': {'even': '14365h7k9dcfesgujnmqp0r2twvyx8zb', 'odd': '238967debc01telegramuhjyznpkmstqrwx'},
    'e': {'even': 'bc01fg45238967deuvhjyznpkmstqrwx', 'odd': 'p0r21436x8zb9dcf5h7kjnmqesgutwvy'},
    'w': {'even': '238967debc01fg45uvhjyznpkmstqrwx', 'odd': '14365h7k9dcfesgujnmqp0r2twvyx8zb'}
}

def geohash_neighbors(geohash: str) -> dict:
    """Get 8 neighbors with colors."""
    directions = ['n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw']
    neighbors = {}
    
    # Simplified: compute from center with offset
    lat, lon = geohash_center(geohash)
    precision = len(geohash)
    
    # Approximate cell size
    lat_delta = 180 / (2 ** (precision * 2.5))
    lon_delta = 360 / (2 ** (precision * 2.5))
    
    offsets = {
        'n': (lat_delta, 0),
        'ne': (lat_delta, lon_delta),
        'e': (0, lon_delta),
        'se': (-lat_delta, lon_delta),
        's': (-lat_delta, 0),
        'sw': (-lat_delta, -lon_delta),
        'w': (0, -lon_delta),
        'nw': (lat_delta, -lon_delta)
    }
    
    for direction, (dlat, dlon) in offsets.items():
        neighbor_lat = lat + dlat
        neighbor_lon = lon + dlon
        neighbor_gh = encode_geohash(neighbor_lat, neighbor_lon, precision)
        neighbors[direction] = color_geohash(neighbor_gh)
    
    return neighbors

def neighbor_gf3_analysis(geohash: str) -> dict:
    """Analyze GF(3) distribution of cell and neighbors."""
    center = color_geohash(geohash)
    neighbors = geohash_neighbors(geohash)
    
    all_trits = [center['trit']] + [n['trit'] for n in neighbors.values()]
    
    return {
        'center': center,
        'neighbors': neighbors,
        'total_cells': 9,
        'trit_sum': sum(all_trits),
        'mod3': sum(all_trits) % 3,
        'distribution': {
            'plus': all_trits.count(1),
            'ergodic': all_trits.count(0),
            'minus': all_trits.count(-1)
        }
    }
```

## DuckDB Integration

```sql
-- Create colored geohash table
CREATE TABLE location_hashes (
    location_id VARCHAR,
    geohash VARCHAR,
    precision INTEGER,
    lat DOUBLE,
    lon DOUBLE,
    seed BIGINT,
    gay_color VARCHAR,
    gf3_trit INTEGER
);

-- Aggregate by geohash prefix (clustering)
SELECT 
    LEFT(geohash, 4) as cluster,
    COUNT(*) as count,
    SUM(gf3_trit) as trit_sum,
    SUM(gf3_trit) % 3 as gf3_balance
FROM location_hashes
GROUP BY LEFT(geohash, 4)
HAVING COUNT(*) > 10
ORDER BY count DESC;

-- Find balanced clusters
SELECT cluster, count, trit_sum
FROM (
    SELECT 
        LEFT(geohash, 5) as cluster,
        COUNT(*) as count,
        SUM(gf3_trit) as trit_sum
    FROM location_hashes
    GROUP BY LEFT(geohash, 5)
)
WHERE trit_sum % 3 = 0;
```

## Triads

```
geohash-coloring (+1) ⊗ duckdb-spatial (0) ⊗ osm-topology (-1) = 0 ✓
geohash-coloring (+1) ⊗ geodesic-manifold (0) ⊗ map-projection (-1) = 0 ✓
geohash-coloring (+1) ⊗ acsets (0) ⊗ three-match (-1) = 0 ✓
```

## References
- Geohash.org specification
- H3 hexagonal alternative (Uber)
- S2 geometry (Google)
