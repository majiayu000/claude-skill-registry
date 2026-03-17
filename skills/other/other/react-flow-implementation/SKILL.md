---
name: react-flow-implementation
description: Implements React Flow node-based UIs correctly using @xyflow/react. Use when building flow charts, diagrams, visual editors, or node-based applications with React. Covers nodes, edges, handles, custom components, state management, and viewport control.
---

# React Flow Implementation

## Quick Start

```tsx
import { ReactFlow, useNodesState, useEdgesState, addEdge } from '@xyflow/react';
import '@xyflow/react/dist/style.css';

const initialNodes = [
  { id: '1', position: { x: 0, y: 0 }, data: { label: 'Node 1' } },
  { id: '2', position: { x: 200, y: 100 }, data: { label: 'Node 2' } },
];

const initialEdges = [{ id: 'e1-2', source: '1', target: '2' }];

export default function Flow() {
  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);

  const onConnect = useCallback(
    (connection) => setEdges((eds) => addEdge(connection, eds)),
    [setEdges]
  );

  return (
    <div style={{ width: '100%', height: '100vh' }}>
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onConnect={onConnect}
        fitView
      />
    </div>
  );
}
```

## Core Patterns

### TypeScript Types

```typescript
import type { Node, Edge, NodeProps, BuiltInNode } from '@xyflow/react';

// Define custom node type with data shape
type CustomNode = Node<{ value: number; label: string }, 'custom'>;

// Combine with built-in nodes
type MyNode = CustomNode | BuiltInNode;
type MyEdge = Edge<{ weight?: number }>;

// Use throughout app
const [nodes, setNodes] = useNodesState<MyNode>(initialNodes);
```

### Custom Nodes

```tsx
import { memo } from 'react';
import { Handle, Position, type NodeProps } from '@xyflow/react';

// Define node type
type CounterNode = Node<{ count: number }, 'counter'>;

// Always wrap in memo for performance
const CounterNode = memo(function CounterNode({ data, isConnectable }: NodeProps<CounterNode>) {
  return (
    <>
      <Handle type="target" position={Position.Top} isConnectable={isConnectable} />
      <div className="counter-node">
        Count: {data.count}
        {/* nodrag prevents dragging when interacting with button */}
        <button className="nodrag" onClick={() => console.log('clicked')}>
          Increment
        </button>
      </div>
      <Handle type="source" position={Position.Bottom} isConnectable={isConnectable} />
    </>
  );
});

// Register in nodeTypes (define OUTSIDE component to avoid re-renders)
const nodeTypes = { counter: CounterNode };

// Use in ReactFlow
<ReactFlow nodeTypes={nodeTypes} ... />
```

### Multiple Handles

```tsx
// Use handle IDs when a node has multiple handles of same type
<Handle type="source" position={Position.Right} id="a" />
<Handle type="source" position={Position.Right} id="b" style={{ top: 20 }} />

// Connect with specific handles
const edge = {
  id: 'e1-2',
  source: '1',
  sourceHandle: 'a',
  target: '2',
  targetHandle: null
};
```

### Custom Edges

```tsx
import { BaseEdge, EdgeProps, getSmoothStepPath } from '@xyflow/react';

function CustomEdge({ id, sourceX, sourceY, targetX, targetY, sourcePosition, targetPosition, data }: EdgeProps) {
  const [edgePath, labelX, labelY] = getSmoothStepPath({
    sourceX, sourceY, sourcePosition,
    targetX, targetY, targetPosition,
  });

  return (
    <>
      <BaseEdge id={id} path={edgePath} />
      <text x={labelX} y={labelY} className="edge-label">{data?.label}</text>
    </>
  );
}

const edgeTypes = { custom: CustomEdge };
```

## State Management

### Controlled (Recommended for Production)

```tsx
// External state with change handlers
const [nodes, setNodes] = useState<Node[]>(initialNodes);
const [edges, setEdges] = useState<Edge[]>(initialEdges);

const onNodesChange = useCallback(
  (changes) => setNodes((nds) => applyNodeChanges(changes, nds)),
  []
);

const onEdgesChange = useCallback(
  (changes) => setEdges((eds) => applyEdgeChanges(changes, eds)),
  []
);

<ReactFlow
  nodes={nodes}
  edges={edges}
  onNodesChange={onNodesChange}
  onEdgesChange={onEdgesChange}
/>
```

### Using useReactFlow

```tsx
import { useReactFlow, ReactFlowProvider } from '@xyflow/react';

function FlowControls() {
  const {
    getNodes, setNodes, addNodes, updateNodeData,
    getEdges, setEdges, addEdges,
    fitView, zoomIn, zoomOut, setViewport,
    deleteElements, toObject,
  } = useReactFlow();

  const addNode = () => {
    addNodes({ id: `${Date.now()}`, position: { x: 100, y: 100 }, data: { label: 'New' } });
  };

  return <button onClick={addNode}>Add Node</button>;
}

// Must wrap in provider when using useReactFlow
function App() {
  return (
    <ReactFlowProvider>
      <Flow />
      <FlowControls />
    </ReactFlowProvider>
  );
}
```

### Updating Node Data

```tsx
const { updateNodeData } = useReactFlow();

// Merge with existing data
updateNodeData(nodeId, { label: 'Updated' });

// Replace data entirely
updateNodeData(nodeId, { newField: 'value' }, { replace: true });
```

## Viewport & Fit View

```tsx
// Fit on initial render
<ReactFlow fitView fitViewOptions={{ padding: 0.2, maxZoom: 1 }} />

// Programmatic control
const { fitView, setViewport, getViewport, zoomTo } = useReactFlow();

// Fit to specific nodes
fitView({ nodes: [{ id: '1' }, { id: '2' }], duration: 500 });

// Set exact viewport
setViewport({ x: 100, y: 100, zoom: 1.5 }, { duration: 300 });
```

## Connection Validation

```tsx
const isValidConnection = useCallback((connection: Connection) => {
  // Prevent self-connections
  if (connection.source === connection.target) return false;

  // Custom validation logic
  const sourceNode = getNode(connection.source);
  const targetNode = getNode(connection.target);

  return sourceNode?.type !== targetNode?.type;
}, []);

<ReactFlow isValidConnection={isValidConnection} />
```

## Common Props Reference

```tsx
<ReactFlow
  // Core data
  nodes={nodes}
  edges={edges}
  onNodesChange={onNodesChange}
  onEdgesChange={onEdgesChange}

  // Custom types (define OUTSIDE component)
  nodeTypes={nodeTypes}
  edgeTypes={edgeTypes}

  // Connections
  onConnect={onConnect}
  connectionMode={ConnectionMode.Loose}  // Allow target-to-target
  isValidConnection={isValidConnection}

  // Viewport
  fitView
  minZoom={0.1}
  maxZoom={4}
  defaultViewport={{ x: 0, y: 0, zoom: 1 }}

  // Interaction
  nodesDraggable={true}
  nodesConnectable={true}
  elementsSelectable={true}
  panOnDrag={true}
  zoomOnScroll={true}

  // Additional components
  <MiniMap />
  <Controls />
  <Background variant={BackgroundVariant.Dots} />
</ReactFlow>
```

## CSS Classes for Interaction

| Class | Effect |
|-------|--------|
| `nodrag` | Prevent dragging when clicking element |
| `nowheel` | Prevent zoom on wheel events |
| `nopan` | Prevent panning from element |
| `nokey` | Prevent keyboard events (use on inputs) |

## Additional Components

See [ADDITIONAL_COMPONENTS.md](ADDITIONAL_COMPONENTS.md) for MiniMap, Controls, Background, NodeToolbar, NodeResizer.
