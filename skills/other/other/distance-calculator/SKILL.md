---
name: distance-calculator
description: Calculate distances between geographic coordinates, find nearby points, and compute travel distances. Use for logistics, delivery routing, or location analysis.
---

# Distance Calculator

Calculate geographic distances and find nearby locations using various methods.

## Features

- **Point-to-Point Distance**: Haversine, Vincenty, great circle
- **Matrix Distances**: All pairs distances
- **Nearest Neighbors**: Find closest N points
- **Radius Search**: Find all points within distance
- **Batch Processing**: Process CSV files
- **Multiple Units**: km, miles, meters, nautical miles

## Quick Start

```python
from distance_calc import DistanceCalculator

calc = DistanceCalculator()

# Simple distance
dist = calc.distance(
    (40.7128, -74.0060),  # New York
    (34.0522, -118.2437)  # Los Angeles
)
print(f"Distance: {dist:.2f} km")

# Find nearest points
nearest = calc.find_nearest(
    origin=(40.7128, -74.0060),
    points=store_locations,
    n=5
)
```

## CLI Usage

```bash
# Distance between two points
python distance_calc.py --from "40.7128,-74.0060" --to "34.0522,-118.2437"

# Find nearest from CSV
python distance_calc.py --origin "40.7128,-74.0060" --input stores.csv --nearest 5

# Points within radius
python distance_calc.py --origin "40.7128,-74.0060" --input stores.csv --radius 50

# Distance matrix
python distance_calc.py --input locations.csv --matrix --output distances.csv

# Different units
python distance_calc.py --from "40.7128,-74.0060" --to "34.0522,-118.2437" --unit miles
```

## API Reference

### DistanceCalculator Class

```python
class DistanceCalculator:
    def __init__(self, unit: str = "km", method: str = "haversine")

    # Point-to-point
    def distance(self, point1: tuple, point2: tuple) -> float
    def distance_with_details(self, point1: tuple, point2: tuple) -> dict

    # Batch operations
    def distance_matrix(self, points: list) -> list
    def distances_from_origin(self, origin: tuple, points: list) -> list

    # Search
    def find_nearest(self, origin: tuple, points: list, n: int = 1) -> list
    def find_within_radius(self, origin: tuple, points: list, radius: float) -> list

    # File operations
    def from_csv(self, filepath: str, lat_col: str, lon_col: str) -> list
    def matrix_to_csv(self, matrix: list, labels: list, output: str)
```

## Distance Methods

### Haversine (Default)
- Great circle distance assuming spherical Earth
- Fast and accurate for most purposes
- Error: ~0.5% max

### Vincenty
- More accurate, accounts for Earth's ellipsoid shape
- Slightly slower
- Error: ~0.5mm

```python
calc = DistanceCalculator(method="vincenty")
```

## Units

| Unit | Description |
|------|-------------|
| `km` | Kilometers (default) |
| `miles` | Miles |
| `m` | Meters |
| `nm` | Nautical miles |
| `ft` | Feet |

```python
calc = DistanceCalculator(unit="miles")
# Or convert after
dist_km = calc.distance(p1, p2)
dist_miles = calc.convert(dist_km, "km", "miles")
```

## Example Workflows

### Find Nearest Stores
```python
calc = DistanceCalculator(unit="miles")
stores = calc.from_csv("stores.csv", "lat", "lon")

customer = (40.7128, -74.0060)
nearest = calc.find_nearest(customer, stores, n=3)

for store in nearest:
    print(f"{store['name']}: {store['distance']:.1f} miles")
```

### Delivery Zone Check
```python
calc = DistanceCalculator(unit="km")
warehouse = (40.7128, -74.0060)
delivery_radius = 50  # km

customers = calc.from_csv("customers.csv", "lat", "lon")
in_zone = calc.find_within_radius(warehouse, customers, delivery_radius)

print(f"{len(in_zone)} customers in delivery zone")
```

### Distance Matrix for Routing
```python
calc = DistanceCalculator()
stops = [
    (40.7128, -74.0060),
    (40.7589, -73.9851),
    (40.7484, -73.9857),
    (40.7527, -73.9772)
]

matrix = calc.distance_matrix(stops)
calc.matrix_to_csv(matrix, ["HQ", "Store1", "Store2", "Store3"], "distances.csv")
```

## Output Formats

### Distance Result
```python
{
    "distance": 3935.75,
    "unit": "km",
    "from": {"lat": 40.7128, "lon": -74.0060},
    "to": {"lat": 34.0522, "lon": -118.2437},
    "method": "haversine"
}
```

### Nearest Points Result
```python
[
    {"point": (lat, lon), "distance": 5.2, "data": {...}},
    {"point": (lat, lon), "distance": 8.1, "data": {...}},
]
```

## Dependencies

- geopy>=2.4.0
