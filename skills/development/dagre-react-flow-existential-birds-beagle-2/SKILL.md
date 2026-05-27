---
name: dagre-react-flow
description: Automatic graph layout using dagre with React Flow (@xyflow/react). Use when implementing auto-layout, hierarchical layouts, tree structures, or arranging nodes programmatically. Triggers on dagre, auto-layout, automatic layout, getLayoutedElements, rankdir, hierarchical graph.
---

# Dagre with React Flow

Dagre is a JavaScript library for laying out directed graphs. It computes optimal node positions for hierarchical/tree layouts. React Flow handles rendering; dagre handles positioning.

## Quick Start

```bash
pnpm add @dagrejs/dagre
```

```typescript
import dagre from '@dagrejs/dagre';
import { Node, Edge } from '@xyflow/react';

const getLayoutedElements = (
  nodes: Node[],
  edges: Edge[],
  direction: 'TB' | 'LR' = 'TB'
) => {
  const g = new dagre.graphlib.Graph();
  g.setGraph({ rankdir: direction });
  g.setDefaultEdgeLabel(() => ({}));

  nodes.forEach((node) => {
    g.setNode(node.id, { width: 172, height: 36 });
  });

  edges.forEach((edge) => {
    g.setEdge(edge.source, edge.target);
  });

  dagre.layout(g);

  const layoutedNodes = nodes.map((node) => {
    const pos = g.node(node.id);
    return {
      ...node,
      position: { x: pos.x - 86, y: pos.y - 18 }, // Center to top-left
    };
  });

  return { nodes: layoutedNodes, edges };
};
```

## Core Concepts

### Coordinate System Difference

**Critical:** Dagre returns center coordinates; React Flow uses top-left.

```typescript
// Dagre output: center of node
const dagrePos = g.node(nodeId); // { x: 100, y: 50 } = center

// React Flow expects: top-left corner
const rfPosition = {
  x: dagrePos.x - nodeWidth / 2,
  y: dagrePos.y - nodeHeight / 2,
};
```

### Node Dimensions

Dagre requires explicit dimensions. Three approaches:

**1. Fixed dimensions (simplest):**
```typescript
g.setNode(node.id, { width: 172, height: 36 });
```

**2. Per-node dimensions from data:**
```typescript
g.setNode(node.id, {
  width: node.data.width ?? 172,
  height: node.data.height ?? 36,
});
```

**3. Measured dimensions (most accurate):**
```typescript
// After React Flow measures nodes
g.setNode(node.id, {
  width: node.measured?.width ?? 172,
  height: node.measured?.height ?? 36,
});
```

### Layout Directions

| Value | Direction | Use Case |
|-------|-----------|----------|
| `TB` | Top to Bottom | Org charts, decision trees |
| `BT` | Bottom to Top | Dependency graphs (deps at bottom) |
| `LR` | Left to Right | Timelines, horizontal flows |
| `RL` | Right to Left | RTL layouts |

```typescript
g.setGraph({ rankdir: 'LR' }); // Horizontal layout
```

## Complete Implementation

### Basic Layout Function

```typescript
import dagre from '@dagrejs/dagre';
import type { Node, Edge } from '@xyflow/react';

interface LayoutOptions {
  direction?: 'TB' | 'BT' | 'LR' | 'RL';
  nodeWidth?: number;
  nodeHeight?: number;
  nodesep?: number;  // Horizontal spacing
  ranksep?: number;  // Vertical spacing (between ranks)
}

export function getLayoutedElements(
  nodes: Node[],
  edges: Edge[],
  options: LayoutOptions = {}
): { nodes: Node[]; edges: Edge[] } {
  const {
    direction = 'TB',
    nodeWidth = 172,
    nodeHeight = 36,
    nodesep = 50,
    ranksep = 50,
  } = options;

  const g = new dagre.graphlib.Graph();
  g.setGraph({ rankdir: direction, nodesep, ranksep });
  g.setDefaultEdgeLabel(() => ({}));

  nodes.forEach((node) => {
    const width = node.measured?.width ?? nodeWidth;
    const height = node.measured?.height ?? nodeHeight;
    g.setNode(node.id, { width, height });
  });

  edges.forEach((edge) => {
    g.setEdge(edge.source, edge.target);
  });

  dagre.layout(g);

  const layoutedNodes = nodes.map((node) => {
    const pos = g.node(node.id);
    const width = node.measured?.width ?? nodeWidth;
    const height = node.measured?.height ?? nodeHeight;

    return {
      ...node,
      position: {
        x: pos.x - width / 2,
        y: pos.y - height / 2,
      },
    };
  });

  return { nodes: layoutedNodes, edges };
}
```

### React Flow Integration

```tsx
import { useCallback } from 'react';
import {
  ReactFlow,
  useNodesState,
  useEdgesState,
  useReactFlow,
  ReactFlowProvider,
} from '@xyflow/react';
import { getLayoutedElements } from './layout';

const initialNodes = [
  { id: '1', data: { label: 'Start' }, position: { x: 0, y: 0 } },
  { id: '2', data: { label: 'Process' }, position: { x: 0, y: 0 } },
  { id: '3', data: { label: 'End' }, position: { x: 0, y: 0 } },
];

const initialEdges = [
  { id: 'e1-2', source: '1', target: '2' },
  { id: 'e2-3', source: '2', target: '3' },
];

// Apply initial layout
const { nodes: layoutedNodes, edges: layoutedEdges } = getLayoutedElements(
  initialNodes,
  initialEdges,
  { direction: 'TB' }
);

function Flow() {
  const [nodes, setNodes, onNodesChange] = useNodesState(layoutedNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(layoutedEdges);
  const { fitView } = useReactFlow();

  const onLayout = useCallback((direction: 'TB' | 'LR') => {
    const { nodes: newNodes, edges: newEdges } = getLayoutedElements(
      nodes,
      edges,
      { direction }
    );

    setNodes([...newNodes]);
    setEdges([...newEdges]);

    // Fit view after layout with animation
    window.requestAnimationFrame(() => {
      fitView({ duration: 300 });
    });
  }, [nodes, edges, setNodes, setEdges, fitView]);

  return (
    <div style={{ width: '100%', height: '100vh' }}>
      <div style={{ position: 'absolute', zIndex: 10, padding: 10 }}>
        <button onClick={() => onLayout('TB')}>Vertical</button>
        <button onClick={() => onLayout('LR')}>Horizontal</button>
      </div>
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        fitView
      />
    </div>
  );
}

export default function App() {
  return (
    <ReactFlowProvider>
      <Flow />
    </ReactFlowProvider>
  );
}
```

## useAutoLayout Hook

Reusable hook for automatic layout:

```typescript
import { useCallback, useEffect, useRef } from 'react';
import {
  useReactFlow,
  useNodesInitialized,
  type Node,
  type Edge,
} from '@xyflow/react';
import dagre from '@dagrejs/dagre';

interface UseAutoLayoutOptions {
  direction?: 'TB' | 'BT' | 'LR' | 'RL';
  nodesep?: number;
  ranksep?: number;
}

export function useAutoLayout(options: UseAutoLayoutOptions = {}) {
  const { direction = 'TB', nodesep = 50, ranksep = 50 } = options;
  const { getNodes, getEdges, setNodes, fitView } = useReactFlow();
  const nodesInitialized = useNodesInitialized();
  const layoutApplied = useRef(false);

  const runLayout = useCallback(() => {
    const nodes = getNodes();
    const edges = getEdges();

    const g = new dagre.graphlib.Graph();
    g.setGraph({ rankdir: direction, nodesep, ranksep });
    g.setDefaultEdgeLabel(() => ({}));

    nodes.forEach((node) => {
      g.setNode(node.id, {
        width: node.measured?.width ?? 172,
        height: node.measured?.height ?? 36,
      });
    });

    edges.forEach((edge) => {
      g.setEdge(edge.source, edge.target);
    });

    dagre.layout(g);

    const layouted = nodes.map((node) => {
      const pos = g.node(node.id);
      const width = node.measured?.width ?? 172;
      const height = node.measured?.height ?? 36;

      return {
        ...node,
        position: { x: pos.x - width / 2, y: pos.y - height / 2 },
      };
    });

    setNodes(layouted);
    window.requestAnimationFrame(() => fitView({ duration: 200 }));
  }, [direction, nodesep, ranksep, getNodes, getEdges, setNodes, fitView]);

  // Auto-layout on initialization
  useEffect(() => {
    if (nodesInitialized && !layoutApplied.current) {
      runLayout();
      layoutApplied.current = true;
    }
  }, [nodesInitialized, runLayout]);

  return { runLayout };
}
```

Usage:

```tsx
function Flow() {
  const { runLayout } = useAutoLayout({ direction: 'LR', ranksep: 100 });

  return (
    <>
      <button onClick={runLayout}>Re-layout</button>
      <ReactFlow ... />
    </>
  );
}
```

## Edge Options

Control edge routing with weight and minlen:

```typescript
edges.forEach((edge) => {
  g.setEdge(edge.source, edge.target, {
    weight: edge.data?.priority ?? 1,  // Higher = more direct path
    minlen: edge.data?.minRanks ?? 1,  // Minimum ranks between nodes
  });
});
```

**weight**: Higher weight edges are prioritized for shorter, more direct paths.

**minlen**: Forces minimum rank separation between connected nodes.

```typescript
// Force 2 ranks between nodes
g.setEdge('a', 'b', { minlen: 2 });
```

## Common Patterns

### Handle Position Based on Direction

Adjust handles for horizontal vs vertical layouts:

```tsx
function CustomNode({ data }: NodeProps) {
  const isHorizontal = data.direction === 'LR' || data.direction === 'RL';

  return (
    <div>
      <Handle
        type="target"
        position={isHorizontal ? Position.Left : Position.Top}
      />
      <div>{data.label}</div>
      <Handle
        type="source"
        position={isHorizontal ? Position.Right : Position.Bottom}
      />
    </div>
  );
}
```

### Animated Layout Transitions

Smooth position changes using CSS transitions:

```css
.react-flow__node {
  transition: transform 300ms ease-out;
}
```

For programmatic animation, see [reference.md](reference.md#animated-layout-transitions).

### Layout with Node Groups

Exclude group nodes from dagre layout:

```typescript
const layoutWithGroups = (nodes: Node[], edges: Edge[]) => {
  // Separate regular nodes from groups
  const regularNodes = nodes.filter((n) => n.type !== 'group');
  const groupNodes = nodes.filter((n) => n.type === 'group');

  // Layout only regular nodes
  const { nodes: layouted } = getLayoutedElements(regularNodes, edges);

  // Combine back
  return { nodes: [...groupNodes, ...layouted], edges };
};
```

## Troubleshooting

### Nodes Overlapping

Increase spacing:

```typescript
g.setGraph({
  rankdir: 'TB',
  nodesep: 100,  // Increase horizontal spacing
  ranksep: 100,  // Increase vertical spacing
});
```

### Layout Not Updating

Ensure new array references:

```typescript
// Wrong - same reference
setNodes(layoutedNodes);

// Correct - new reference
setNodes([...layoutedNodes]);
```

### Nodes at Wrong Position

Check coordinate conversion:

```typescript
// Dagre returns center, React Flow needs top-left
position: {
  x: pos.x - width / 2,   // Not just pos.x
  y: pos.y - height / 2,  // Not just pos.y
}
```

### Performance with Large Graphs

- Layout in a Web Worker
- Debounce layout calls
- Use `useMemo` for layout function
- Only re-layout changed portions

## Configuration Reference

See [reference.md](reference.md) for complete dagre configuration options.
