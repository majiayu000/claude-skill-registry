---
name: territory-mapper
description: Use when asked to visualize sales territories, coverage areas, service regions, or geographic boundaries on interactive maps.
---

# Territory Mapper

Visualize sales territories, coverage areas, and service regions on interactive maps with customizable boundaries and styling.

## Purpose

Territory visualization for:
- Sales territory assignment and planning
- Service area coverage mapping
- Market analysis and expansion
- Delivery zone visualization
- Regional performance tracking

## Features

- **Territory Polygons**: Draw custom boundaries
- **Color Coding**: Color by performance, team, status
- **Interactive Maps**: Zoom, pan, tooltips
- **Data Overlay**: Add markers, heatmaps, routes
- **Statistical Layers**: Population, demographics
- **Export**: HTML, PNG, GeoJSON

## Quick Start

```python
from territory_mapper import TerritoryMapper

# Create territory map
mapper = TerritoryMapper()
mapper.add_territory(
    name='West Coast',
    coordinates=[(37.7, -122.4), (34.0, -118.2), ...],
    color='blue',
    data={'sales': 1000000, 'rep': 'Alice'}
)
mapper.save_html('territories.html')
```

## CLI Usage

```bash
# Create map from GeoJSON
python territory_mapper.py --geojson territories.geojson --output map.html

# Color by column
python territory_mapper.py --geojson territories.geojson --color-by sales --output map.html
```
