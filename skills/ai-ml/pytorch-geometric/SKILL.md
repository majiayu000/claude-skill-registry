---
name: pytorch-geometric
description: Library for Graph Neural Networks (GNNs). Covers MessagePassing layers, modular aggregation schemes, and handling large graphs via mini-batching with disjoint graph representation. (pyg, messagepassing, gnn, gcn, gat, edge_index, knn_graph, global_mean_pool)
---

## Overview

PyTorch Geometric (PyG) is built on top of PyTorch to simplify the implementation of Graph Neural Networks. It treats graphs as `Data` objects containing node features and edge indices, and provides a powerful `MessagePassing` base class for custom layer development.

## When to Use

Use PyG for data that is naturally represented as a graph, such as social networks, molecular structures, or point clouds. Use it when you need to perform node classification, edge prediction, or graph-level regression.

## Decision Tree

1. Do you have a list of small graphs?
   - USE: `torch_geometric.loader.DataLoader` to create a single giant disjoint graph.
2. Do you need to pool node features into a graph-level feature?
   - USE: `global_mean_pool` or `global_max_pool` using the `batch` vector.
3. Are you building a custom convolution?
   - INHERIT: From `torch_geometric.nn.MessagePassing`.

## Workflows

1. **Defining a Custom GNN Layer**
   1. Inherit from `torch_geometric.nn.MessagePassing`.
   2. Set the aggregation scheme (`aggr='add'`, `'mean'`, or `'max'`) in `__init__`.
   3. Implement the forward pass using `self.propagate()`.
   4. Define the `message()` function to compute the transformation for each edge.
   5. Optionally define the `update()` function to transform aggregated results.

2. **Mini-batching Large Graphs**
   1. Use `torch_geometric.loader.DataLoader` instead of the standard PyTorch version.
   2. PyG automatically creates a single giant disjoint graph from a list of small graphs.
   3. The `batch` vector in the resulting `Data` object tracks which original graph each node belongs to.
   4. Use global pooling (e.g., `global_mean_pool`) to aggregate node features into graph-level representations.

3. **Constructing Graphs from Point Clouds**
   1. Represent point clouds as node features in a tensor `[N, F]`.
   2. Apply `knn_graph()` to dynamically compute an `edge_index` based on spatial proximity.
   3. Pass the results into an `EdgeConv` or `DynamicEdgeConv` layer for feature extraction.

## Non-Obvious Insights

- **Auto-Indexing**: The `_i` and `_j` notation in `MessagePassing` methods automatically handles indexing into source and destination nodes during propagation without manual slice logic.
- **Disjoint Representation**: PyG batches multiple graphs by stacking them into a single block-diagonal adjacency matrix. This allows standard sparse matrix operations to process multiple graphs in parallel without zero-padding.
- **Modular Aggregation**: Aggregation is a first-class principle in PyG; users can swap simple sum/mean with advanced learnable schemes like `SoftmaxAggregation` by simply changing the `aggr` parameter.

## Evidence

- "PyG provides the MessagePassing base class, which helps in creating such kinds of message passing graph neural networks by automatically taking care of message propagation." (https://pytorch-geometric.readthedocs.io/en/latest/tutorial/create_gnn.html)
- "Tensors passed to propagate() can be mapped to the respective nodes i and j by appending _i or _j to the variable name." (https://pytorch-geometric.readthedocs.io/en/latest/tutorial/create_gnn.html)

## Scripts

- `scripts/pytorch-geometric_tool.py`: Template for a custom GNN layer and graph data loader.
- `scripts/pytorch-geometric_tool.js`: Node.js script to run PyG training experiments.

## Dependencies

- torch
- torch-geometric
- torch-scatter / torch-sparse (optional but recommended)

## References

- [PyTorch Geometric Reference](references/README.md)