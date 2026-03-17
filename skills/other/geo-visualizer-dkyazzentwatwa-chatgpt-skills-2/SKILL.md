---
name: geo-visualizer
description: Create interactive maps with markers, heatmaps, routes, and choropleth layers. Use when visualizing geographic data, plotting locations, or creating map-based reports.
---

# Geo Visualizer

Create interactive HTML maps from geographic data using Folium.

## Features

- **Markers**: Plot points with custom icons, popups, and tooltips
- **Heatmaps**: Visualize density/intensity data
- **Choropleth**: Color regions by data values
- **Routes/Lines**: Draw paths between points
- **Circles/Areas**: Show radius-based coverage
- **Layer Control**: Toggle multiple layers
- **Clustering**: Auto-cluster dense markers

## Quick Start

```python
from geo_visualizer import GeoVisualizer

# Simple marker map
viz = GeoVisualizer()
viz.add_markers([
    {"lat": 40.7128, "lon": -74.0060, "name": "New York"},
    {"lat": 34.0522, "lon": -118.2437, "name": "Los Angeles"}
])
viz.save("cities.html")

# From CSV
viz = GeoVisualizer()
viz.from_csv("locations.csv", lat_col="latitude", lon_col="longitude")
viz.save("map.html")
```

## CLI Usage

```bash
# Plot markers from CSV
python geo_visualizer.py --input locations.csv --lat latitude --lon longitude --output map.html

# Add heatmap
python geo_visualizer.py --input data.csv --lat lat --lon lng --heatmap --output heat.html

# With clustering
python geo_visualizer.py --input stores.csv --lat lat --lon lon --cluster --output stores.html

# Choropleth map
python geo_visualizer.py --geojson states.geojson --data stats.csv --key state --value population --output choropleth.html
```

## API Reference

### GeoVisualizer Class

```python
class GeoVisualizer:
    def __init__(self, center=None, zoom=10, tiles="OpenStreetMap")

    # Data loading
    def from_csv(self, filepath, lat_col, lon_col, **kwargs) -> 'GeoVisualizer'
    def from_dataframe(self, df, lat_col, lon_col, **kwargs) -> 'GeoVisualizer'
    def from_geojson(self, filepath) -> 'GeoVisualizer'

    # Markers
    def add_marker(self, lat, lon, popup=None, tooltip=None, icon=None, color="blue")
    def add_markers(self, locations: list, name_col=None, popup_cols=None)
    def cluster_markers(self, enabled=True) -> 'GeoVisualizer'

    # Layers
    def add_heatmap(self, points=None, weight_col=None, radius=15) -> 'GeoVisualizer'
    def add_choropleth(self, geojson, data, key_on, value_col, **kwargs) -> 'GeoVisualizer'
    def add_route(self, points, color="blue", weight=3) -> 'GeoVisualizer'
    def add_circle(self, lat, lon, radius_m, color="blue", fill=True)

    # Output
    def save(self, filepath) -> str
    def get_html(self) -> str
    def fit_bounds(self) -> 'GeoVisualizer'
```

## Marker Options

```python
# Custom icons
viz.add_marker(lat, lon, icon="fa-coffee", color="red")

# With popup content
viz.add_marker(lat, lon, popup="<b>Store #123</b><br>Open 9-5")

# From CSV with popup columns
viz.from_csv("stores.csv", lat_col="lat", lon_col="lon")
viz.add_markers(viz.data, popup_cols=["name", "address", "phone"])
```

## Heatmap Options

```python
# Basic heatmap
viz.add_heatmap()

# Weighted heatmap (e.g., by sales volume)
viz.add_heatmap(weight_col="sales", radius=20, blur=15, max_zoom=12)
```

## Choropleth Maps

```python
# Color regions by data
viz.add_choropleth(
    geojson="us-states.geojson",
    data=state_data,
    key_on="feature.properties.name",  # GeoJSON property
    value_col="population",
    fill_color="YlOrRd",  # Color scale
    legend_name="Population"
)
```

## Tile Layers

Available base maps:
- `OpenStreetMap` (default)
- `CartoDB positron` (light, minimal)
- `CartoDB dark_matter` (dark theme)
- `Stamen Terrain` (terrain features)
- `Stamen Toner` (high contrast B&W)

```python
viz = GeoVisualizer(tiles="CartoDB positron")
```

## Example Workflows

### Store Locator Map
```python
viz = GeoVisualizer()
viz.from_csv("stores.csv", lat_col="lat", lon_col="lon")
viz.add_markers(viz.data, popup_cols=["name", "address", "hours"])
viz.cluster_markers(True)
viz.fit_bounds()
viz.save("store_locator.html")
```

### Sales Heatmap
```python
viz = GeoVisualizer(tiles="CartoDB dark_matter")
viz.from_csv("sales.csv", lat_col="lat", lon_col="lon")
viz.add_heatmap(weight_col="revenue", radius=25)
viz.save("sales_heat.html")
```

### Delivery Route
```python
viz = GeoVisualizer()
stops = [(40.7, -74.0), (40.8, -73.9), (40.75, -73.95)]
viz.add_route(stops, color="blue", weight=4)
for i, (lat, lon) in enumerate(stops):
    viz.add_marker(lat, lon, popup=f"Stop {i+1}")
viz.save("route.html")
```

## Output

- **HTML**: Interactive map viewable in any browser
- **Auto-fit**: Automatically zooms to show all data
- **Responsive**: Works on mobile devices

## Dependencies

- folium>=0.14.0
- pandas>=2.0.0
- branca>=0.6.0
