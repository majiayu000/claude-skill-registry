---
name: Network Analysis
description: Analyze network structures, identify communities, measure centrality, and visualize relationships for social networks and organizational structures
---

# Network Analysis

## Overview

This skill enables analysis of network structures to identify communities, measure centrality, detect influential nodes, and visualize complex relationships in social networks, organizational structures, and interconnected systems.

## When to Use

- Analyzing social networks to identify influential users and community structures
- Mapping organizational hierarchies and identifying key connectors or bottlenecks
- Studying citation networks to find impactful research papers and collaboration patterns
- Building recommendation systems based on network relationships and similarities
- Analyzing supply chain networks to optimize logistics and identify vulnerabilities
- Detecting fraud patterns through network analysis of financial transactions

## Network Concepts

- **Nodes**: Individual entities
- **Edges**: Connections/relationships
- **Degree**: Number of connections
- **Centrality**: Node importance measures
- **Community**: Densely connected groups
- **Clustering Coefficient**: Local density

## Key Metrics

- **Degree Centrality**: Number of connections
- **Betweenness Centrality**: Control over paths
- **Closeness Centrality**: Average distance to others
- **Eigenvector Centrality**: Connections to important nodes
- **Modularity**: Community structure strength

## Implementation with Python

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from collections import defaultdict, Counter
import seaborn as sns

# Create sample network (social network)
G = nx.Graph()

# Add nodes with attributes
nodes = [
    ('Alice', {'role': 'Manager', 'dept': 'Sales'}),
    ('Bob', {'role': 'Engineer', 'dept': 'Tech'}),
    ('Carol', {'role': 'Designer', 'dept': 'Design'}),
    ('David', {'role': 'Engineer', 'dept': 'Tech'}),
    ('Eve', {'role': 'Analyst', 'dept': 'Sales'}),
    ('Frank', {'role': 'Manager', 'dept': 'HR'}),
    ('Grace', {'role': 'Designer', 'dept': 'Design'}),
    ('Henry', {'role': 'Engineer', 'dept': 'Tech'}),
    ('Iris', {'role': 'Analyst', 'dept': 'Sales'}),
    ('Jack', {'role': 'Manager', 'dept': 'Finance'}),
]

for node, attrs in nodes:
    G.add_node(node, **attrs)

# Add edges (relationships)
edges = [
    ('Alice', 'Bob'), ('Alice', 'Carol'), ('Alice', 'Eve'),
    ('Bob', 'David'), ('Bob', 'Henry'), ('Carol', 'Grace'),
    ('David', 'Henry'), ('Eve', 'Iris'), ('Frank', 'Jack'),
    ('Grace', 'Carol'), ('Alice', 'Frank'), ('Bob', 'Carol'),
    ('Eve', 'Alice'), ('Iris', 'Eve'), ('Jack', 'Frank'),
    ('Henry', 'David'), ('Carol', 'David'),
]

G.add_edges_from(edges)

print("Network Summary:")
print(f"Nodes: {G.number_of_nodes()}")
print(f"Edges: {G.number_of_edges()}")
print(f"Density: {nx.density(G):.2%}")

# 1. Degree Centrality
degree_centrality = nx.degree_centrality(G)
print("\n1. Degree Centrality (Top 5):")
for node, score in sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)[:5]:
    print(f"  {node}: {score:.3f}")

# 2. Betweenness Centrality (control over network)
betweenness_centrality = nx.betweenness_centrality(G)
print("\n2. Betweenness Centrality (Top 5):")
for node, score in sorted(betweenness_centrality.items(), key=lambda x: x[1], reverse=True)[:5]:
    print(f"  {node}: {score:.3f}")

# 3. Closeness Centrality (average distance to others)
closeness_centrality = nx.closeness_centrality(G)
print("\n3. Closeness Centrality (Top 5):")
for node, score in sorted(closeness_centrality.items(), key=lambda x: x[1], reverse=True)[:5]:
    print(f"  {node}: {score:.3f}")

# 4. Eigenvector Centrality
try:
    eigenvector_centrality = nx.eigenvector_centrality(G, max_iter=100)
    print("\n4. Eigenvector Centrality (Top 5):")
    for node, score in sorted(eigenvector_centrality.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"  {node}: {score:.3f}")
except:
    print("\n4. Eigenvector Centrality: Not converged")

# 5. Community Detection (using modularity)
from networkx.algorithms import community

communities = list(community.greedy_modularity_communities(G))
print(f"\n5. Community Detection:")
print(f"Number of communities: {len(communities)}")
for i, comm in enumerate(communities):
    print(f"  Community {i+1}: {list(comm)}")

# 6. Network Statistics
degrees = [G.degree(n) for n in G.nodes()]
print(f"\n6. Network Statistics:")
print(f"Average Degree: {np.mean(degrees):.2f}")
print(f"Max Degree: {max(degrees)}")
print(f"Min Degree: {min(degrees)}")
print(f"Clustering Coefficient: {nx.average_clustering(G):.3f}")
print(f"Number of Triangles: {sum(nx.triangles(G).values()) // 3}")

# Visualization
fig, axes = plt.subplots(2, 2, figsize=(15, 12))

# Network layout
pos = nx.spring_layout(G, k=0.5, iterations=50, seed=42)

# 1. Network Graph (colored by degree)
ax = axes[0, 0]
node_colors = [degree_centrality[node] for node in G.nodes()]
nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=1000, cmap='YlOrRd', ax=ax)
nx.draw_networkx_edges(G, pos, alpha=0.5, ax=ax)
nx.draw_networkx_labels(G, pos, font_size=8, ax=ax)
ax.set_title('Network Graph (Colored by Degree Centrality)')
ax.axis('off')

# 2. Network Graph (colored by communities)
ax = axes[0, 1]
color_map = []
colors = plt.cm.Set3(np.linspace(0, 1, len(communities)))
node_to_color = {}
for i, comm in enumerate(communities):
    for node in comm:
        node_to_color[node] = colors[i]
color_map = [node_to_color[node] for node in G.nodes()]

nx.draw_networkx_nodes(G, pos, node_color=color_map, node_size=1000, ax=ax)
nx.draw_networkx_edges(G, pos, alpha=0.5, ax=ax)
nx.draw_networkx_labels(G, pos, font_size=8, ax=ax)
ax.set_title('Network Graph (Colored by Community)')
ax.axis('off')

# 3. Centrality Comparison
ax = axes[1, 0]
centrality_df = pd.DataFrame({
    'Degree': degree_centrality,
    'Betweenness': betweenness_centrality,
    'Closeness': closeness_centrality,
}).head(8)

centrality_df.plot(kind='barh', ax=ax, width=0.8)
ax.set_xlabel('Centrality Score')
ax.set_title('Top 8 Nodes - Centrality Comparison')
ax.legend(loc='lower right')
ax.grid(True, alpha=0.3, axis='x')

# 4. Degree Distribution
ax = axes[1, 1]
degree_sequence = sorted([d for n, d in G.degree()], reverse=True)
degree_count = Counter(degree_sequence)
degrees_unique = sorted(degree_count.keys())
counts = [degree_count[d] for d in degrees_unique]

ax.bar(degrees_unique, counts, color='steelblue', edgecolor='black', alpha=0.7)
ax.set_xlabel('Degree')
ax.set_ylabel('Count')
ax.set_title('Degree Distribution')
ax.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.show()

# 7. Path Analysis
print(f"\n7. Path Analysis:")
try:
    shortest_path = nx.shortest_path_length(G, 'Alice', 'Jack')
    print(f"Shortest path from Alice to Jack: {shortest_path}")
except nx.NetworkXNoPath:
    print("No path exists between nodes")

# 8. Connectivity Analysis
print(f"\n8. Connectivity Analysis:")
print(f"Is connected: {nx.is_connected(G)}")
num_components = nx.number_connected_components(G)
print(f"Number of connected components: {num_components}")

# 9. Similarity Measures
def jaccard_similarity(node1, node2):
    neighbors1 = set(G.neighbors(node1)) | {node1}
    neighbors2 = set(G.neighbors(node2)) | {node2}
    intersection = len(neighbors1 & neighbors2)
    union = len(neighbors1 | neighbors2)
    return intersection / union if union > 0 else 0

print(f"\n9. Node Similarity (Jaccard):")
print(f"Alice & Bob: {jaccard_similarity('Alice', 'Bob'):.3f}")
print(f"Alice & Jack: {jaccard_similarity('Alice', 'Jack'):.3f}")

# 10. Influence Score (Combination of metrics)
influence_score = {}
for node in G.nodes():
    score = (degree_centrality[node] * 0.4 +
             betweenness_centrality[node] * 0.3 +
             closeness_centrality[node] * 0.3)
    influence_score[node] = score

print(f"\n10. Influence Score (Top 5):")
for node, score in sorted(influence_score.items(), key=lambda x: x[1], reverse=True)[:5]:
    print(f"  {node}: {score:.3f}")

# Summary
print("\n" + "="*50)
print("NETWORK ANALYSIS SUMMARY")
print("="*50)
print(f"Most influential: {max(influence_score, key=influence_score.get)}")
print(f"Most connected: {max(degree_centrality, key=degree_centrality.get)}")
print(f"Network bottleneck: {max(betweenness_centrality, key=betweenness_centrality.get)}")
print(f"Closest to all: {max(closeness_centrality, key=closeness_centrality.get)}")
print("="*50)
```

## Centrality Measures

- **Degree**: Direct connections only
- **Betweenness**: Bridges between groups
- **Closeness**: Access to network
- **Eigenvector**: Connected to important nodes
- **PageRank**: Random walk probability

## Community Detection

- **Modularity Optimization**: Find dense groups
- **Louvain Algorithm**: Hierarchical communities
- **K-clique**: Overlapping communities
- **Spectral**: Eigenvalue-based

## Applications

- Social network analysis
- Organizational structures
- Citation networks
- Recommendation networks
- Supply chain analysis

## Deliverables

- Network visualization
- Centrality analysis
- Community detection results
- Connectivity metrics
- Influence rankings
- Key node identification
- Network statistics summary
