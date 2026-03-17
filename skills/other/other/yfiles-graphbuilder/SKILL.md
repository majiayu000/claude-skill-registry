---
name: yfiles-graphbuilder
description: Builds graphs from business data using GraphBuilder, TreeBuilder, or AdjacencyGraphBuilder. Handles node/edge ID mapping, hierarchical structures, and data binding. Use when importing data, loading JSON, creating graphs from arrays, or when user mentions "data to graph", "import data", "business data", "load from JSON", or "GraphBuilder".
---

# Build Graphs from Data

Converts business data into graph visualizations using GraphBuilder API.

## Quick Start

```typescript
import { GraphBuilder } from '@yfiles/yfiles'

const builder = new GraphBuilder(graph)
builder.createNodesSource({ data: nodesData, id: 'id' })
builder.createEdgesSource({
  data: edgesData,
  id: 'id',
  sourceId: 'source',
  targetId: 'target'
})
builder.buildGraph()
```

## Before Building

**Always query yFiles MCP for current API:**

```
yfiles:yfiles_get_symbol_details(name="GraphBuilder")
yfiles:yfiles_search_documentation(query="GraphBuilder tutorial")
```

## Common Patterns

See [patterns.md](patterns.md) for:
- Basic node/edge creation
- Custom styles from data
- Labels from data
- Node positioning
- Updating existing graphs

## Advanced Features

See [advanced.md](advanced.md) for:
- Group nodes (hierarchical graphs)
- Ports and bends
- TreeBuilder (for tree data)
- AdjacencyGraphBuilder (for adjacency lists)

## Complete Examples

See [examples.md](examples.md) for full working code.

## Key Concepts

- **Data stays in tags**: Original data stored in element `.tag` property
- **ID mapping**: Use field names or functions for IDs
- **Build order**: Groups before nodes, nodes before edges
- **Provider functions**: For computed values (styles, labels, layouts)
- **updateGraph()**: Updates existing graph instead of rebuilding

**Important**: Never directly assign to readonly properties like `node.layout`, `edge.sourceNode`, or `edge.targetNode`. Use IGraph methods instead (e.g., `graph.setNodeLayout()`, `graph.setEdgePorts()`). The `@yfiles/eslint-plugin` rule `@yfiles/suggest-setter-methods` warns about these mistakes.

## After Building

Graph likely needs layout:
```
/yfiles-layout
```

## MCP Tools

- `yfiles:yfiles_get_symbol_details(name="GraphBuilder")` - Full API
- `yfiles:yfiles_search_documentation(query="GraphBuilder")` - Tutorials
- `yfiles:yfiles_get_symbol_details(name="TreeBuilder")` - For tree data
- `yfiles:yfiles_get_symbol_details(name="AdjacencyGraphBuilder")` - For adjacency data
