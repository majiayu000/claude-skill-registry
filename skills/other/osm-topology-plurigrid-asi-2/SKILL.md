---
name: osm-topology
description: 'OSM Topology Skill'
version: 1.0.0
---

# OSM Topology Skill

OpenStreetMap graph analysis: road networks, routing, and topological structure with GF(3) coloring.

## Trigger
- OpenStreetMap data processing
- Road network analysis, routing
- Graph-based geographic queries
- Street network topology

## GF(3) Trit: -1 (Validator)
Validates topological consistency of geographic networks.

## OSM Data Model

OSM uses three primitives:
- **Nodes**: Points with lat/lon
- **Ways**: Ordered lists of nodes (roads, boundaries)
- **Relations**: Groups of nodes/ways (routes, multipolygons)

## DuckDB OSM Integration

```sql
-- Read OSM PBF files (requires osm extension)
-- Install from: https://github.com/duckdb/duckdb_osm

-- Alternative: Use pre-processed Parquet
CREATE TABLE osm_nodes AS 
SELECT * FROM read_parquet('osm_nodes.parquet');

CREATE TABLE osm_ways AS
SELECT * FROM read_parquet('osm_ways.parquet');

-- Schema for colored OSM data
CREATE TABLE osm_network (
    way_id BIGINT,
    name VARCHAR,
    highway_type VARCHAR,
    geometry GEOMETRY,
    node_ids BIGINT[],
    -- Topology
    start_node BIGINT,
    end_node BIGINT,
    length_m DOUBLE,
    -- GF(3) coloring
    seed BIGINT,
    gay_color VARCHAR,
    gf3_trit INTEGER
);
```

## Graph Extraction

```python
import duckdb
import networkx as nx

def extract_road_graph(osm_parquet_path):
    """Extract road network as colored graph."""
    conn = duckdb.connect()
    conn.execute("INSTALL spatial; LOAD spatial;")
    
    # Load ways with road tags
    conn.execute(f"""
        CREATE TABLE roads AS
        SELECT 
            way_id,
            tags->>'name' as name,
            tags->>'highway' as highway,
            nodes,
            ST_Length_Spheroid(ST_MakeLine(
                LIST_TRANSFORM(nodes, n -> ST_Point(n.lon, n.lat))
            )) as length_m
        FROM read_parquet('{osm_parquet_path}')
        WHERE tags->>'highway' IS NOT NULL
    """)
    
    # Build graph
    G = nx.DiGraph()
    
    roads = conn.execute("""
        SELECT way_id, nodes, length_m, highway FROM roads
    """).fetchall()
    
    for way_id, nodes, length, highway in roads:
        for i in range(len(nodes) - 1):
            n1, n2 = nodes[i], nodes[i+1]
            
            # Color edge from way_id
            seed = way_id & 0x7FFFFFFFFFFFFFFF
            hue = seed % 360
            trit = 1 if (hue < 60 or hue >= 300) else (0 if hue < 180 else -1)
            
            G.add_edge(n1['id'], n2['id'], 
                      way_id=way_id,
                      length=length / (len(nodes) - 1),
                      highway=highway,
                      trit=trit)
            
            # Add reverse for bidirectional roads
            if highway not in ('motorway', 'motorway_link'):
                G.add_edge(n2['id'], n1['id'],
                          way_id=way_id,
                          length=length / (len(nodes) - 1),
                          highway=highway,
                          trit=trit)
    
    return G
```

## Topological Validation

```python
def validate_network_topology(G):
    """
    Validate OSM network topology.
    Returns list of issues with GF(3) classification.
    """
    issues = []
    
    # Check connectivity
    if not nx.is_weakly_connected(G):
        components = list(nx.weakly_connected_components(G))
        issues.append({
            'type': 'disconnected',
            'count': len(components),
            'trit': -1,  # Validation failure
            'severity': 'high'
        })
    
    # Check for dead ends
    dead_ends = [n for n in G.nodes() if G.degree(n) == 1]
    if dead_ends:
        issues.append({
            'type': 'dead_ends',
            'count': len(dead_ends),
            'nodes': dead_ends[:10],
            'trit': 0,  # Ergodic (may be intentional)
            'severity': 'low'
        })
    
    # Check for self-loops
    self_loops = list(nx.selfloop_edges(G))
    if self_loops:
        issues.append({
            'type': 'self_loops',
            'count': len(self_loops),
            'trit': -1,  # Validation failure
            'severity': 'medium'
        })
    
    # Check for duplicate edges
    multi_edges = [(u, v) for u, v in G.edges() if G.number_of_edges(u, v) > 1]
    if multi_edges:
        issues.append({
            'type': 'multi_edges',
            'count': len(multi_edges),
            'trit': -1,
            'severity': 'medium'
        })
    
    return issues

def gf3_balance_check(G):
    """Check if edge trits are GF(3) balanced per node."""
    imbalanced = []
    
    for node in G.nodes():
        edges = list(G.edges(node, data=True))
        trit_sum = sum(e[2].get('trit', 0) for e in edges)
        
        if trit_sum % 3 != 0:
            imbalanced.append({
                'node': node,
                'trit_sum': trit_sum,
                'edge_count': len(edges)
            })
    
    return {
        'total_nodes': G.number_of_nodes(),
        'imbalanced_count': len(imbalanced),
        'balance_ratio': 1 - len(imbalanced) / G.number_of_nodes(),
        'sample_imbalanced': imbalanced[:5]
    }
```

## Routing with Color

```python
def colored_route(G, start, end, weight='length'):
    """Find shortest path with GF(3) coloring."""
    try:
        path = nx.shortest_path(G, start, end, weight=weight)
        edges = []
        total_length = 0
        trit_sum = 0
        
        for i in range(len(path) - 1):
            edge_data = G.edges[path[i], path[i+1]]
            edges.append({
                'from': path[i],
                'to': path[i+1],
                'length': edge_data['length'],
                'highway': edge_data['highway'],
                'trit': edge_data['trit']
            })
            total_length += edge_data['length']
            trit_sum += edge_data['trit']
        
        return {
            'path': path,
            'edges': edges,
            'total_length_m': total_length,
            'hop_count': len(path) - 1,
            'gf3_sum': trit_sum,
            'gf3_mod3': trit_sum % 3,
            'balanced': trit_sum % 3 == 0
        }
    
    except nx.NetworkXNoPath:
        return {'error': 'No path found', 'trit': -1}
```

## Overpass API Integration

```python
import requests

def query_osm_overpass(bbox, highway_types=['primary', 'secondary', 'tertiary']):
    """Query OSM via Overpass API."""
    
    highway_filter = '|'.join(highway_types)
    query = f"""
    [out:json][timeout:60];
    (
      way["highway"~"{highway_filter}"]({bbox});
    );
    out body;
    >;
    out skel qt;
    """
    
    response = requests.post(
        'https://overpass-api.de/api/interpreter',
        data={'data': query}
    )
    
    return response.json()

def osm_to_colored_graph(osm_json, seed=42):
    """Convert Overpass response to colored graph."""
    import hashlib
    
    G = nx.DiGraph()
    nodes = {e['id']: e for e in osm_json['elements'] if e['type'] == 'node'}
    
    for element in osm_json['elements']:
        if element['type'] == 'way':
            way_id = element['id']
            node_refs = element.get('nodes', [])
            
            # Color from way ID
            seed_val = int(hashlib.sha256(str(way_id).encode()).hexdigest()[:16], 16)
            hue = seed_val % 360
            trit = 1 if (hue < 60 or hue >= 300) else (0 if hue < 180 else -1)
            
            for i in range(len(node_refs) - 1):
                n1, n2 = node_refs[i], node_refs[i+1]
                if n1 in nodes and n2 in nodes:
                    G.add_edge(n1, n2,
                              way_id=way_id,
                              tags=element.get('tags', {}),
                              trit=trit)
    
    # Add node coordinates
    for node_id, node_data in nodes.items():
        if node_id in G:
            G.nodes[node_id]['lat'] = node_data['lat']
            G.nodes[node_id]['lon'] = node_data['lon']
    
    return G
```

## Triads

```
osm-topology (-1) ⊗ duckdb-spatial (0) ⊗ map-projection (+1) = 0 ✓
osm-topology (-1) ⊗ geodesic-manifold (0) ⊗ geohash-coloring (+1) = 0 ✓
osm-topology (-1) ⊗ acsets (0) ⊗ gay-mcp (+1) = 0 ✓
```

## References
- OpenStreetMap Wiki
- OSMnx library (Geoff Boeing)
- NetworkX documentation
