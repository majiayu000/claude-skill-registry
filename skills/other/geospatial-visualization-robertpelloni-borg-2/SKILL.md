---
name: geospatial-visualization
description: Master geographic and mapping visualizations with GeoViews. Use this skill when creating interactive maps, visualizing point/polygon/line geographic data, building choropleth maps, performing spatial analysis (joins, buffers, proximity), working with coordinate reference systems, or integrating tile providers and basemaps.
version: 2025-01-07
compatibility: Requires geoviews >= 1.11.0, geopandas >= 0.10.0, shapely >= 1.8.0, pyproj >= 3.0.0, cartopy >= 0.20.0 (optional)
---

# Geospatial Visualization Skill

## Overview

Master geographic and mapping visualizations with GeoViews and spatial data handling. This skill covers creating interactive maps, analyzing geographic data, and visualizing spatial relationships.

## Dependencies

- geoviews >= 1.11.0
- geopandas >= 0.10.0
- shapely >= 1.8.0
- cartopy >= 0.20.0 (optional)
- pyproj >= 3.0.0

## Core Capabilities

### 1. Basic Geographic Visualization

GeoViews extends HoloViews with geographic support:

```python
import geoviews as gv
import geopandas as gpd
from geoviews import tile_providers as gvts

# Load geographic data
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# Basic map visualization
world_map = gv.Polygons(world, vdims=['name', 'pop_est']).opts(
    title='World Population',
    height=600,
    width=800,
    tools=['hover']
)

# Add tile layer background
tiled = gvts.ESRI.apply.opts(
    alpha=0.4,
    xaxis=None,
    yaxis=None
) * world_map
```

### 2. Point Data on Maps

```python
# Create point features
cities_data = {
    'city': ['New York', 'Los Angeles', 'Chicago'],
    'latitude': [40.7128, 34.0522, 41.8781],
    'longitude': [-74.0060, -118.2437, -87.6298],
    'population': [8337000, 3990456, 2693976]
}

cities_gdf = gpd.GeoDataFrame(
    cities_data,
    geometry=gpd.points_from_xy(cities_data['longitude'], cities_data['latitude']),
    crs='EPSG:4326'
)

# Visualize points
points = gv.Points(cities_gdf, kdims=['longitude', 'latitude'], vdims=['city', 'population'])
points = points.opts(
    size=gv.dim('population').norm(min=5, max=50),
    color='red',
    tools=['hover', 'box_select']
)

# With tile background
map_with_points = gvts.CartoDEM.apply.opts(alpha=0.5) * points
```

### 3. Choropleth Maps

```python
# Color regions by data value
choropleth = gv.Polygons(world, vdims=['name', 'pop_est']).opts(
    cmap='viridis',
    color=gv.dim('pop_est').norm(),
    colorbar=True,
    height=600,
    width=900,
    tools=['hover']
)

# Add interactivity
choropleth = choropleth.opts(
    hover_fill_color='red',
    hover_fill_alpha=0.5
)
```

### 4. Interactive Feature Selection

```python
from holoviews import streams

# Create selectable map
selectable_map = gv.Polygons(world).opts(
    tools=['box_select', 'tap'],
    selection_fill_color='red',
    nonselection_fill_alpha=0.2
)

# Stream for selection
selection_stream = streams.Selection1D()

def get_selected_data(index):
    if index:
        return world.iloc[index[0]]
    return None

# Get info about selected region
selected_info = hv.DynamicMap(
    lambda index: hv.Text(0, 0, str(get_selected_data(index))),
    streams=[selection_stream]
)
```

### 5. Vector and Raster Layers

```python
# Multiple layers
terrain = gvts.Stamen.Terrain.apply.opts(alpha=0.3)
points = gv.Points(cities_gdf, kdims=['longitude', 'latitude'])
lines = gv.Lines(routes_gdf, kdims=['longitude', 'latitude'])

# Compose layers
map_composition = terrain * lines * points

# Faceted geographic display
faceted_maps = gv.Polygons(world, vdims=['name', 'continent']).facet('continent')
```

### 6. Hexbin and Rasterized Aggregation

```python
# Hexbin aggregation for point data
hexbin = gv.HexTiles(cities_gdf).opts(
    cmap='viridis',
    colorbar=True,
    height=600,
    width=800
)

# With tile background
map_hexbin = gvts.CartoDEM.apply.opts(alpha=0.4) * hexbin
```

## Spatial Analysis Workflows

### 1. Spatial Joins

```python
# Combine different geographic layers
points_gdf = gpd.GeoDataFrame(
    cities_data,
    geometry=gpd.points_from_xy(cities_data['longitude'], cities_data['latitude']),
    crs='EPSG:4326'
)

regions_gdf = gpd.read_file('regions.geojson')

# Spatial join: which cities are in which regions
joined = gpd.sjoin(points_gdf, regions_gdf, how='left', predicate='within')

# Visualize result
joined_map = gv.Points(joined, kdims=['longitude', 'latitude']) * \
             gv.Polygons(regions_gdf)
```

### 2. Buffer and Proximity Analysis

```python
from shapely.geometry import Point

# Create buffer zones
buffered = cities_gdf.copy()
buffered['geometry'] = buffered.geometry.buffer(1.0)  # 1 degree

# Visualize buffered regions
buffers = gv.Polygons(buffered).opts(fill_alpha=0.3)
points = gv.Points(cities_gdf)

proximity_map = gvts.CartoDEM.apply.opts(alpha=0.3) * buffers * points
```

### 3. Distance and Route Analysis

```python
# Calculate distances between cities
from shapely.geometry import LineString

routes = []
for i in range(len(cities_gdf) - 1):
    start = cities_gdf.geometry.iloc[i]
    end = cities_gdf.geometry.iloc[i + 1]
    route = LineString([start, end])
    distance = start.distance(end)
    routes.append({'geometry': route, 'distance': distance})

routes_gdf = gpd.GeoDataFrame(routes, crs='EPSG:4326')

# Visualize routes
route_lines = gv.Lines(routes_gdf, vdims=['distance']).opts(
    color=gv.dim('distance').norm(),
    cmap='plasma'
)
```

## Tile Providers and Basemaps

```python
# Available tile providers
from geoviews import tile_providers as gvts

# Different styles
openstreetmap = gvts.OpenStreetMap.Mapnik
satellite = gvts.ESRI.WorldImagery
terrain = gvts.Stamen.Terrain
toner = gvts.Stamen.Toner

# Use with visualization
map_with_osm = gvts.OpenStreetMap.Mapnik * gv.Points(cities_gdf)

# Custom styling
base_map = gvts.CartoDEM.apply.opts(
    alpha=0.5,
    xaxis=None,
    yaxis=None
)
```

## Best Practices

### 1. Coordinate Reference Systems
```python
# Always specify and manage CRS
gdf = gpd.read_file('data.geojson')
print(gdf.crs)

# Reproject if necessary
gdf_projected = gdf.to_crs('EPSG:3857')  # Web Mercator

# When creating GeoDataFrame
gdf = gpd.GeoDataFrame(
    data,
    geometry=gpd.points_from_xy(lon, lat),
    crs='EPSG:4326'  # WGS84
)
```

### 2. Large Dataset Optimization
```python
# Use rasterization for dense point clouds
from holoviews.operation.datashader import rasterize

points = gv.Points(large_gdf, kdims=['x', 'y'])
rasterized = rasterize(points)

# Use tile-based rendering for massive datasets
# Consider breaking into GeoJSON tiles
```

### 3. Interactive Map Design
```python
# Combine multiple interaction tools
map_viz = gv.Polygons(gdf).opts(
    tools=['hover', 'box_select', 'tap'],
    hover_fill_color='yellow',
    hover_fill_alpha=0.2,
    selection_fill_color='red'
)

# Add complementary visualizations
statistics = hv.Text(0, 0, '')  # Update based on selection
map_and_stats = hv.Column(map_viz, statistics)
```

### 4. Color and Scale Management
```python
# Use perceptually uniform colormaps
from colorcet import cm

map_viz = gv.Polygons(gdf, vdims=['value']).opts(
    color=gv.dim('value').norm(),
    cmap=cm['viridis'],
    colorbar=True,
    clim=(vmin, vmax)
)
```

## Common Patterns

### Pattern 1: Multi-Layer Map Dashboard
```python
def create_map_dashboard(layers_dict):
    base_map = gvts.CartoDEM.apply.opts(alpha=0.4)
    layers = [gv.Polygons(layers_dict[name]) for name in layers_dict]
    return base_map * hv.Overlay(layers)
```

### Pattern 2: Dynamic Filtering Map
```python
from holoviews import DynamicMap, streams

filter_stream = streams.Stream.define('filter', year=2020)

def update_map(year):
    filtered_gdf = world[world['year'] == year]
    return gv.Polygons(filtered_gdf, vdims=['name', 'value'])

dmap = DynamicMap(update_map, streams=[filter_stream])
```

### Pattern 3: Clustered Points Map
```python
def create_clustered_map(points_gdf, zoom_levels=[1, 5, 10, 20]):
    # Use hexbin for aggregation at different scales
    aggregated = gv.HexTiles(points_gdf, aggregation='count')
    return aggregated.opts(responsive=True)
```

## Integration with Other HoloViz Tools

- **Panel**: Embed maps in web dashboards
- **hvPlot**: Quick geographic plotting with `.hvplot(geo=True)`
- **HoloViews**: Underlying visualization framework
- **Datashader**: Efficient rendering for massive geographic datasets
- **Param**: Parameter-driven map updates

## Common Use Cases

1. **Real Estate Analysis**: Property locations and market data
2. **Climate Analysis**: Temperature, precipitation spatial patterns
3. **Infrastructure Planning**: Network and facility location analysis
4. **Epidemiology**: Disease spread and hotspot visualization
5. **Transportation Analysis**: Route optimization and traffic patterns
6. **Environmental Monitoring**: Land use, vegetation, water quality

## Troubleshooting

### Issue: Map Not Displaying
- Verify CRS is correctly specified
- Check coordinates are in correct order (longitude, latitude)
- Ensure geometry objects are valid with `gdf.is_valid.all()`

### Issue: Performance Problems with Large Datasets
- Use rasterization for dense points
- Simplify geometries with `gdf.geometry.simplify(tolerance)`
- Use tile-based rendering or data pagination
- Consider reducing zoom levels

### Issue: Inaccurate Spatial Analysis
- Verify CRS consistency across all layers
- Use appropriate CRS for distance calculations
- Check topology validity before operations
- Test on sample data first

## Resources

- [GeoViews Documentation](https://geoviews.org)
- [GeoPandas Documentation](https://geopandas.org)
- [GeoJSON Specification](https://geojson.org)
- [EPSG Coordinate Reference Systems](https://epsg.io)
- [Cartopy for Advanced Cartography](https://scitools.org.uk/cartopy)
