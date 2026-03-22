---
name: integrate-road-network
description: Integrate real-world street networks into VRP problems using OpenStreetMap data. Use when loading real map data, creating instances from actual locations, computing network-based distances, or building tutorials with real-world scenarios. Guides through installation, loading areas, extracting nodes, computing distance matrices, and creating PDPTW instances from map data.
---

# Road Network Integration

Integrate real-world street networks from OpenStreetMap into your VRP toolkit using map data.

## Integration Workflow

### Step 1: Install Dependencies

Install OSMnx and geo-processing libraries.

**Using conda (recommended):**
```bash
conda install -c conda-forge osmnx
```

**Using pip:**
```bash
pip install osmnx geopandas shapely fiona pyproj
```

**Verify installation:**
```python
import osmnx as ox
print(f"OSMnx version: {ox.__version__}")
```

**Troubleshooting:** See [troubleshooting.md](references/troubleshooting.md) for installation issues.

### Step 2: Load Street Network

Choose loading method based on your needs:

#### Option A: Load by Place Name

For well-known locations (recommended for campuses, cities).

```python
import osmnx as ox

# Load area by name
place_name = "Purdue University, West Lafayette, IN, USA"
G = ox.graph_from_place(
    place_name,
    network_type='drive',  # 'drive', 'walk', 'bike', or 'all'
    simplify=True
)

# Save for reuse (much faster than re-downloading)
ox.save_graphml(G, "data/campus_network.graphml")

print(f"Loaded {len(G.nodes)} nodes and {len(G.edges)} edges")
```

#### Option B: Load by Bounding Box

For specific coordinate ranges.

```python
# Define bounding box (north, south, east, west)
north, south, east, west = 40.4300, 40.4200, -86.9100, -86.9250

G = ox.graph_from_bbox(north, south, east, west, network_type='drive')
```

**Data structure details:** See [maintain-data-structures](../maintain-data-structures/) skill → data_layer.md → OSMnx Graph

**More examples:** See [osmnx_examples.md](references/osmnx_examples.md) → Examples 1-2

### Step 3: Define VRP Locations

Map your problem locations (depot, customers, pickups, deliveries) to network nodes.

#### 3a. Extract from Points of Interest (POIs)

```python
# Find buildings/amenities as potential locations
tags = {
    'building': ['university', 'dormitory'],
    'amenity': ['cafe', 'restaurant', 'library']
}

pois = ox.geometries_from_place(place_name, tags=tags)

# Extract coordinates
locations = []
for idx, poi in pois.iterrows():
    if poi.geometry.geom_type == 'Point':
        lat, lon = poi.geometry.y, poi.geometry.x
    else:  # Polygon
        lat, lon = poi.geometry.centroid.y, poi.geometry.centroid.x

    locations.append((lat, lon))

print(f"Found {len(locations)} potential customer locations")
```

#### 3b. Use Manually Defined Locations

```python
# Define locations manually (lat, lon)
depot_loc = (40.4237, -86.9212)

pickup_locs = [
    (40.4280, -86.9145),
    (40.4200, -86.9180)
]

delivery_locs = [
    (40.4250, -86.9100),
    (40.4210, -86.9220)
]
```

**More examples:** See [osmnx_examples.md](references/osmnx_examples.md) → Example 3

### Step 4: Map to Network Nodes

Find nearest nodes in the street network for each location.

```python
# Find nearest network nodes
depot_node = ox.distance.nearest_nodes(
    G,
    depot_loc[1],  # X = longitude
    depot_loc[0]   # Y = latitude
)

pickup_nodes = [
    ox.distance.nearest_nodes(G, lon, lat)
    for lat, lon in pickup_locs
]

delivery_nodes = [
    ox.distance.nearest_nodes(G, lon, lat)
    for lat, lon in delivery_locs
]

# All nodes for VRP instance
all_osm_nodes = [depot_node] + pickup_nodes + delivery_nodes

print(f"Mapped to {len(all_osm_nodes)} network nodes")
```

**IMPORTANT:** `nearest_nodes` takes `(X, Y)` which is `(longitude, latitude)`, NOT `(lat, lon)`!

**Troubleshooting:** See [troubleshooting.md](references/troubleshooting.md) → Coordinate Issues

**More examples:** See [osmnx_examples.md](references/osmnx_examples.md) → Example 4

### Step 5: Compute Distance Matrix

Calculate network-based distances between all nodes.

```python
import networkx as nx
import numpy as np

n = len(all_osm_nodes)
distance_matrix = np.zeros((n, n))

for i, origin in enumerate(all_osm_nodes):
    # Compute shortest paths from origin to all destinations
    lengths = nx.single_source_dijkstra_path_length(
        G, origin, weight='length'  # Use 'length' for distance in meters
    )

    for j, dest in enumerate(all_osm_nodes):
        if i != j and dest in lengths:
            distance_matrix[i, j] = lengths[dest]

print("Distance matrix computed (in meters)")
print(distance_matrix)
```

**Optional: Convert to time matrix**
```python
average_speed_kmh = 30  # km/h
average_speed_ms = average_speed_kmh * 1000 / 3600  # m/s

time_matrix_seconds = distance_matrix / average_speed_ms
time_matrix_minutes = time_matrix_seconds / 60
```

**Data structure details:** See [maintain-data-structures](../maintain-data-structures/) skill → runtime_formats.md → Distance Matrix

**Troubleshooting:** See [troubleshooting.md](references/troubleshooting.md) → Routing Issues

**More examples:** See [osmnx_examples.md](references/osmnx_examples.md) → Examples 5-6

### Step 6: Create Node Objects

Create VRP toolkit Node objects from OSMnx nodes.

```python
from vrp_toolkit.problems import Node

nodes = []

# Depot
depot_data = G.nodes[depot_node]
nodes.append(Node(
    node_id=0,
    x=depot_data['x'],  # longitude
    y=depot_data['y'],  # latitude
    node_type='depot'
))

# Pickups and deliveries (paired)
for idx, (p_node, d_node) in enumerate(zip(pickup_nodes, delivery_nodes), 1):
    pickup_id = idx * 2 - 1
    delivery_id = idx * 2

    # Pickup node
    p_data = G.nodes[p_node]
    nodes.append(Node(
        node_id=pickup_id,
        x=p_data['x'],
        y=p_data['y'],
        demand=10.0,  # Adjust as needed
        time_window=(8.0, 17.0),  # 8am - 5pm
        service_time=0.25,  # 15 minutes
        node_type='pickup',
        pair_node_id=delivery_id
    ))

    # Delivery node
    d_data = G.nodes[d_node]
    nodes.append(Node(
        node_id=delivery_id,
        x=d_data['x'],
        y=d_data['y'],
        demand=-10.0,  # Negative for delivery
        time_window=(8.0, 17.0),
        service_time=0.25,
        node_type='delivery',
        pair_node_id=pickup_id
    ))

print(f"Created {len(nodes)} Node objects")
```

**Data structure details:** See [maintain-data-structures](../maintain-data-structures/) skill → problem_layer.md → Node

### Step 7: Create PDPTW Instance

Combine everything into a problem instance.

```python
from vrp_toolkit.problems import PDPTWInstance

instance = PDPTWInstance(
    nodes=nodes,
    battery_capacity=100.0,
    max_route_time=480.0,  # 8 hours in minutes
    vehicle_capacity=50.0
)

# Attach distance matrix
instance.distance_matrix = distance_matrix

# Optionally attach time matrix
instance.time_matrix = time_matrix_minutes

# Save instance for later use
import pickle
with open('data/campus_pdptw_instance.pkl', 'wb') as f:
    pickle.dump(instance, f)

print("PDPTW instance created successfully!")
```

**Complete example:** See [osmnx_examples.md](references/osmnx_examples.md) → Example 7

**Data structure details:** See [maintain-data-structures](../maintain-data-structures/) skill → problem_layer.md → PDPTWInstance

### Step 8: Validate and Solve

Test the instance and solve.

```python
from vrp_toolkit.algorithms.alns import ALNSSolver, ALNSConfig

# Validate instance
print(f"Number of nodes: {len(instance.nodes)}")
print(f"Number of pickup-delivery pairs: {len(instance.pickup_delivery_pairs)}")
print(f"Distance matrix shape: {instance.distance_matrix.shape}")

# Solve
config = ALNSConfig(max_iterations=1000)
solver = ALNSSolver(config)
solution = solver.solve(instance)

# Check solution
if solution.is_feasible():
    print(f"Feasible solution found!")
    print(f"Objective value: {solution.objective_value()}")
    solution.plot()
else:
    print("Solution is infeasible")
```

## Advanced Features

### Visualize Routes on Street Network

Plot solution routes on the actual map.

```python
import matplotlib.pyplot as plt

# Plot base network
fig, ax = ox.plot_graph(
    G,
    bgcolor='white',
    node_size=0,
    edge_color='gray',
    edge_linewidth=0.5,
    show=False,
    close=False
)

# Plot solution routes (assuming routes contain OSM node IDs)
colors = ['blue', 'red', 'green', 'orange']

for route_idx, route in enumerate(solution.routes):
    # Map VRP node IDs back to OSM node IDs
    osm_route = [all_osm_nodes[node_id] for node_id in route]

    # Get coordinates
    xs = [G.nodes[node]['x'] for node in osm_route]
    ys = [G.nodes[node]['y'] for node in osm_route]

    # Plot
    ax.plot(xs, ys,
            color=colors[route_idx % len(colors)],
            linewidth=3,
            alpha=0.7,
            label=f'Route {route_idx + 1}')

ax.legend()
plt.title("VRP Solution on Real Street Network")
plt.show()
```

**More examples:** See [osmnx_examples.md](references/osmnx_examples.md) → Example 8

### Cache for Performance

Save processed graphs to avoid re-downloading.

```python
import os

cache_file = "data/campus_network.graphml"

if os.path.exists(cache_file):
    # Load from cache (instant!)
    G = ox.load_graphml(cache_file)
    print("Loaded from cache")
else:
    # Download and save
    G = ox.graph_from_place(place_name)
    ox.save_graphml(G, cache_file)
    print("Downloaded and cached")
```

**More examples:** See [osmnx_examples.md](references/osmnx_examples.md) → Example 9

### Handle Graph Connectivity

Ensure all nodes can reach each other.

```python
import networkx as nx

# Check connectivity
if not nx.is_weakly_connected(G):
    print("Graph has multiple disconnected components")

    # Keep only largest connected component
    largest_component = max(
        nx.weakly_connected_components(G),
        key=len
    )
    G = G.subgraph(largest_component).copy()
    print(f"Using largest component with {len(G.nodes)} nodes")
```

**Troubleshooting:** See [troubleshooting.md](references/troubleshooting.md) → Routing Issues

## Creating Tutorials with OSMnx

When creating a tutorial that uses OSMnx:

1. **Choose recognizable location**
   - Use well-known places (e.g., university campus, downtown area)
   - Easier for readers to relate to

2. **Cache the graph**
   - Include downloaded graph in tutorial repository
   - Avoids download delays for users

3. **Use small areas**
   - Keep examples fast (<30 seconds to run)
   - Small bounding boxes or specific places

4. **Provide visualization**
   - Plot the network with routes overlaid
   - Makes results more tangible

5. **Handle edge cases**
   - Show what to do if node unreachable
   - Demonstrate connectivity checks

## Common Patterns

### Pattern 1: Campus Routing

```python
# 1. Load campus
G = ox.graph_from_place("University Name, City, State, USA")

# 2. Find buildings as customer locations
pois = ox.geometries_from_place(place_name, tags={'building': True})

# 3. Create distance matrix
# 4. Build PDPTW instance
# 5. Solve and visualize on map
```

### Pattern 2: City-Wide Delivery

```python
# 1. Load city with bounding box
G = ox.graph_from_bbox(north, south, east, west)

# 2. Use address geocoding for customer locations
# 3. Compute network distances
# 4. Create VRP instance
# 5. Solve at scale
```

### Pattern 3: Benchmark Comparison

```python
# Create two instances:
# - Euclidean distance (traditional)
# - Network distance (OSMnx)
# Compare solution quality and computation time
```

## Integration with Other Skills

**Works with:**
- **maintain-data-structures**: Reference OSMnx data structures (Graph, GeoDataFrame, distance matrices)
- **migrate-module**: When migrating `real_map.py` from old codebase
- **tutorial-creator**: When creating real-world VRP tutorials (when that skill exists)

**Example:**
```
You: "Create a real-world PDPTW instance for Purdue campus"
→ osmnx-integration skill triggers
→ References maintain-data-structures for OSMnx Graph structure
→ Creates instance following workflow
```

## Reference Materials

- **Examples:** [osmnx_examples.md](references/osmnx_examples.md) - 10 complete examples
- **Troubleshooting:** [troubleshooting.md](references/troubleshooting.md) - Common issues and solutions
- **Data Structures:** See [maintain-data-structures](../maintain-data-structures/) skill for OSMnx structure details

## Key Reminders

1. ⚠️ **Coordinate order:** `nearest_nodes(G, lon, lat)` not `(lat, lon)`!
2. 💾 **Cache graphs:** Save downloaded graphs to avoid re-downloading
3. 🔗 **Check connectivity:** Ensure all nodes can reach each other
4. 📏 **Distance units:** OSMnx uses meters, convert as needed
5. 🗺️ **Simplify graphs:** Use `simplify=True` for faster processing unless you need exact geometry
