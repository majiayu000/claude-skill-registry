---
name: react-flow-code-review
description: Reviews React Flow code for anti-patterns, performance issues, and best practices. Use when reviewing code that uses @xyflow/react, checking for common mistakes, or optimizing node-based UI implementations.
---

# React Flow Code Review

## Critical Anti-Patterns

### 1. Defining nodeTypes/edgeTypes Inside Components

**Problem**: Causes all nodes to re-mount on every render.

```tsx
// BAD - recreates object every render
function Flow() {
  const nodeTypes = { custom: CustomNode };  // WRONG
  return <ReactFlow nodeTypes={nodeTypes} />;
}

// GOOD - defined outside component
const nodeTypes = { custom: CustomNode };
function Flow() {
  return <ReactFlow nodeTypes={nodeTypes} />;
}

// GOOD - useMemo if dynamic
function Flow() {
  const nodeTypes = useMemo(() => ({ custom: CustomNode }), []);
  return <ReactFlow nodeTypes={nodeTypes} />;
}
```

### 2. Missing memo() on Custom Nodes/Edges

**Problem**: Custom components re-render on every parent update.

```tsx
// BAD - no memoization
function CustomNode({ data }: NodeProps) {
  return <div>{data.label}</div>;
}

// GOOD - wrapped in memo
import { memo } from 'react';
const CustomNode = memo(function CustomNode({ data }: NodeProps) {
  return <div>{data.label}</div>;
});
```

### 3. Inline Callbacks Without useCallback

**Problem**: Creates new function references, breaking memoization.

```tsx
// BAD - inline callback
<ReactFlow
  onNodesChange={(changes) => setNodes(applyNodeChanges(changes, nodes))}
/>

// GOOD - memoized callback
const onNodesChange = useCallback(
  (changes) => setNodes((nds) => applyNodeChanges(changes, nds)),
  []
);
<ReactFlow onNodesChange={onNodesChange} />
```

### 4. Using useReactFlow Outside Provider

```tsx
// BAD - will throw error
function App() {
  const { getNodes } = useReactFlow();  // ERROR: No provider
  return <ReactFlow ... />;
}

// GOOD - wrap in provider
function FlowContent() {
  const { getNodes } = useReactFlow();  // Works
  return <ReactFlow ... />;
}

function App() {
  return (
    <ReactFlowProvider>
      <FlowContent />
    </ReactFlowProvider>
  );
}
```

### 5. Storing Complex Objects in Node Data

**Problem**: Reference equality checks fail, causing unnecessary updates.

```tsx
// BAD - new object reference every time
setNodes(nodes.map(n => ({
  ...n,
  data: { ...n.data, config: { nested: 'value' } }  // New object each time
})));

// GOOD - use updateNodeData for targeted updates
const { updateNodeData } = useReactFlow();
updateNodeData(nodeId, { config: { nested: 'value' } });
```

## Performance Checklist

### Node Rendering

- [ ] Custom nodes wrapped in `memo()`
- [ ] nodeTypes defined outside component or memoized
- [ ] Heavy computations inside nodes use `useMemo`
- [ ] Event handlers use `useCallback`

### Edge Rendering

- [ ] Custom edges wrapped in `memo()`
- [ ] edgeTypes defined outside component or memoized
- [ ] Edge path calculations are not duplicated

### State Updates

- [ ] Using functional form of setState: `setNodes((nds) => ...)`
- [ ] Not spreading entire state for single property updates
- [ ] Using `updateNodeData` for data-only changes
- [ ] Batch updates when adding multiple nodes/edges

### Viewport

- [ ] Not calling `fitView()` on every render
- [ ] Using `fitViewOptions` for initial fit only
- [ ] Animation durations are reasonable (< 500ms)

## Common Mistakes

### Missing Container Height

```tsx
// BAD - no height, flow won't render
<ReactFlow nodes={nodes} edges={edges} />

// GOOD - explicit dimensions
<div style={{ width: '100%', height: '100vh' }}>
  <ReactFlow nodes={nodes} edges={edges} />
</div>
```

### Missing CSS Import

```tsx
// Required for default styles
import '@xyflow/react/dist/style.css';
```

### Forgetting nodrag on Interactive Elements

```tsx
// BAD - clicking button drags node
<button onClick={handleClick}>Click</button>

// GOOD - prevents drag
<button className="nodrag" onClick={handleClick}>Click</button>
```

### Not Using Position Constants

```tsx
// BAD - string literals
<Handle type="source" position="right" />

// GOOD - type-safe constants
import { Position } from '@xyflow/react';
<Handle type="source" position={Position.Right} />
```

### Mutating Nodes/Edges Directly

```tsx
// BAD - direct mutation
nodes[0].position = { x: 100, y: 100 };
setNodes(nodes);

// GOOD - immutable update
setNodes(nodes.map(n =>
  n.id === '1' ? { ...n, position: { x: 100, y: 100 } } : n
));
```

## TypeScript Issues

### Missing Generic Types

```tsx
// BAD - loses type safety
const [nodes, setNodes] = useNodesState(initialNodes);

// GOOD - explicit types
type MyNode = Node<{ value: number }, 'custom'>;
const [nodes, setNodes] = useNodesState<MyNode>(initialNodes);
```

### Wrong Props Type

```tsx
// BAD - using wrong type
function CustomNode(props: any) { ... }

// GOOD - correct props type
function CustomNode(props: NodeProps<MyNode>) { ... }
```

## Review Questions

1. Are all custom components memoized?
2. Are nodeTypes/edgeTypes defined outside render?
3. Are callbacks wrapped in useCallback?
4. Is the container sized properly?
5. Are styles imported?
6. Is useReactFlow used inside a provider?
7. Are interactive elements marked with nodrag?
8. Are types used consistently throughout?
