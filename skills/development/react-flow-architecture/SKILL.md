---
name: react-flow-architecture
description: Architectural guidance for building node-based UIs with React Flow. Use when designing flow-based applications, making decisions about state management, integration patterns, or evaluating whether React Flow fits a use case.
---

# React Flow Architecture

## When to Use React Flow

### Good Fit

- Visual programming interfaces
- Workflow builders and automation tools
- Diagram editors (flowcharts, org charts)
- Data pipeline visualization
- Mind mapping tools
- Node-based audio/video editors
- Decision tree builders
- State machine designers

### Consider Alternatives

- Simple static diagrams (use SVG or canvas directly)
- Heavy real-time collaboration (may need custom sync layer)
- 3D visualizations (use Three.js, react-three-fiber)
- Graph analysis with 10k+ nodes (use WebGL-based solutions like Sigma.js)

## Architecture Patterns

### Package Structure (xyflow)

```
@xyflow/system (vanilla TypeScript)
├── Core algorithms (edge paths, bounds, viewport)
├── xypanzoom (d3-based pan/zoom)
├── xydrag, xyhandle, xyminimap, xyresizer
└── Shared types

@xyflow/react (depends on @xyflow/system)
├── React components and hooks
├── Zustand store for state management
└── Framework-specific integrations

@xyflow/svelte (depends on @xyflow/system)
└── Svelte components and stores
```

**Implication**: Core logic is framework-agnostic. When contributing or debugging, check if issue is in @xyflow/system or framework-specific package.

### State Management Approaches

#### 1. Local State (Simple Apps)

```tsx
// useNodesState/useEdgesState for prototyping
const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);
```

**Pros**: Simple, minimal boilerplate
**Cons**: State isolated to component tree

#### 2. External Store (Production)

```tsx
// Zustand store example
import { create } from 'zustand';

interface FlowStore {
  nodes: Node[];
  edges: Edge[];
  setNodes: (nodes: Node[]) => void;
  onNodesChange: OnNodesChange;
}

const useFlowStore = create<FlowStore>((set, get) => ({
  nodes: initialNodes,
  edges: initialEdges,
  setNodes: (nodes) => set({ nodes }),
  onNodesChange: (changes) => {
    set({ nodes: applyNodeChanges(changes, get().nodes) });
  },
}));

// In component
function Flow() {
  const { nodes, edges, onNodesChange } = useFlowStore();
  return <ReactFlow nodes={nodes} onNodesChange={onNodesChange} />;
}
```

**Pros**: State accessible anywhere, easier persistence/sync
**Cons**: More setup, need careful selector optimization

#### 3. Redux/Other State Libraries

```tsx
// Connect via selectors
const nodes = useSelector(selectNodes);
const dispatch = useDispatch();

const onNodesChange = useCallback((changes: NodeChange[]) => {
  dispatch(nodesChanged(changes));
}, [dispatch]);
```

### Data Flow Architecture

```
User Input → Change Event → Reducer/Handler → State Update → Re-render
     ↓
[Drag node] → onNodesChange → applyNodeChanges → setNodes → ReactFlow
     ↓
[Connect]   → onConnect → addEdge → setEdges → ReactFlow
     ↓
[Delete]    → onNodesDelete → deleteElements → setNodes/setEdges → ReactFlow
```

### Sub-Flow Pattern (Nested Nodes)

```tsx
// Parent node containing child nodes
const nodes = [
  {
    id: 'group-1',
    type: 'group',
    position: { x: 0, y: 0 },
    style: { width: 300, height: 200 },
  },
  {
    id: 'child-1',
    parentId: 'group-1',  // Key: parent reference
    extent: 'parent',      // Key: constrain to parent
    position: { x: 10, y: 30 },  // Relative to parent
    data: { label: 'Child' },
  },
];
```

**Considerations**:
- Use `extent: 'parent'` to constrain dragging
- Use `expandParent: true` to auto-expand parent
- Parent z-index affects child rendering order

### Viewport Persistence

```tsx
// Save viewport state
const { toObject, setViewport } = useReactFlow();

const handleSave = () => {
  const flow = toObject();
  // flow.nodes, flow.edges, flow.viewport
  localStorage.setItem('flow', JSON.stringify(flow));
};

const handleRestore = () => {
  const flow = JSON.parse(localStorage.getItem('flow'));
  setNodes(flow.nodes);
  setEdges(flow.edges);
  setViewport(flow.viewport);
};
```

## Integration Patterns

### With Backend/API

```tsx
// Load from API
useEffect(() => {
  fetch('/api/flow')
    .then(r => r.json())
    .then(({ nodes, edges }) => {
      setNodes(nodes);
      setEdges(edges);
    });
}, []);

// Debounced auto-save
const debouncedSave = useMemo(
  () => debounce((nodes, edges) => {
    fetch('/api/flow', {
      method: 'POST',
      body: JSON.stringify({ nodes, edges }),
    });
  }, 1000),
  []
);

useEffect(() => {
  debouncedSave(nodes, edges);
}, [nodes, edges]);
```

### With Layout Algorithms

```tsx
import dagre from 'dagre';

function getLayoutedElements(nodes: Node[], edges: Edge[]) {
  const g = new dagre.graphlib.Graph();
  g.setGraph({ rankdir: 'TB' });
  g.setDefaultEdgeLabel(() => ({}));

  nodes.forEach((node) => {
    g.setNode(node.id, { width: 150, height: 50 });
  });

  edges.forEach((edge) => {
    g.setEdge(edge.source, edge.target);
  });

  dagre.layout(g);

  return {
    nodes: nodes.map((node) => {
      const pos = g.node(node.id);
      return { ...node, position: { x: pos.x, y: pos.y } };
    }),
    edges,
  };
}
```

## Performance Scaling

### Node Count Guidelines

| Nodes | Strategy |
|-------|----------|
| < 100 | Default settings |
| 100-500 | Enable `onlyRenderVisibleElements` |
| 500-1000 | Simplify custom nodes, reduce DOM elements |
| > 1000 | Consider virtualization, WebGL alternatives |

### Optimization Techniques

```tsx
<ReactFlow
  // Only render nodes/edges in viewport
  onlyRenderVisibleElements={true}

  // Reduce node border radius (improves intersect calculations)
  nodeExtent={[[-1000, -1000], [1000, 1000]]}

  // Disable features not needed
  elementsSelectable={false}
  panOnDrag={false}
  zoomOnScroll={false}
/>
```

## Trade-offs

### Controlled vs Uncontrolled

| Controlled | Uncontrolled |
|------------|--------------|
| More boilerplate | Less code |
| Full state control | Internal state |
| Easy persistence | Need `toObject()` |
| Better for complex apps | Good for prototypes |

### Connection Modes

| Strict (default) | Loose |
|------------------|-------|
| Source → Target only | Any handle → any handle |
| Predictable behavior | More flexible |
| Use for data flows | Use for diagrams |

```tsx
<ReactFlow connectionMode={ConnectionMode.Loose} />
```

### Edge Rendering

| Default edges | Custom edges |
|---------------|--------------|
| Fast rendering | More control |
| Limited styling | Any SVG/HTML |
| Simple use cases | Complex labels |
