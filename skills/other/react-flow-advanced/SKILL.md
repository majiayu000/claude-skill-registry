---
name: react-flow-advanced
description: Advanced React Flow patterns for complex use cases. Use when implementing sub-flows, custom connection lines, programmatic layouts, drag-and-drop, undo/redo, or complex state synchronization.
---

# Advanced React Flow Patterns

## Sub-Flows (Nested Nodes)

```tsx
const nodes = [
  // Parent (group) node
  {
    id: 'group-1',
    type: 'group',
    position: { x: 0, y: 0 },
    style: { width: 400, height: 300, padding: 10 },
    data: { label: 'Group' },
  },
  // Child nodes
  {
    id: 'child-1',
    parentId: 'group-1',        // Reference parent
    extent: 'parent',           // Constrain to parent bounds
    expandParent: true,         // Auto-expand parent if dragged to edge
    position: { x: 20, y: 50 }, // Relative to parent
    data: { label: 'Child 1' },
  },
  {
    id: 'child-2',
    parentId: 'group-1',
    extent: 'parent',
    position: { x: 200, y: 50 },
    data: { label: 'Child 2' },
  },
];
```

### Group Node Component

```tsx
function GroupNode({ data, id }: NodeProps) {
  return (
    <div className="group-node">
      <div className="group-header">{data.label}</div>
      {/* Children are rendered automatically by React Flow */}
    </div>
  );
}
```

## Custom Connection Line

```tsx
import { ConnectionLineComponentProps, getSmoothStepPath } from '@xyflow/react';

function CustomConnectionLine({
  fromX, fromY, fromPosition,
  toX, toY, toPosition,
  connectionStatus,
}: ConnectionLineComponentProps) {
  const [path] = getSmoothStepPath({
    sourceX: fromX,
    sourceY: fromY,
    sourcePosition: fromPosition,
    targetX: toX,
    targetY: toY,
    targetPosition: toPosition,
  });

  return (
    <g>
      <path
        d={path}
        fill="none"
        stroke={connectionStatus === 'valid' ? '#22c55e' : '#ef4444'}
        strokeWidth={2}
        strokeDasharray="5 5"
      />
    </g>
  );
}

<ReactFlow connectionLineComponent={CustomConnectionLine} />
```

## Drag and Drop from External Source

```tsx
import { useReactFlow, useCallback, useRef } from 'react';

function DnDFlow() {
  const reactFlowWrapper = useRef(null);
  const { screenToFlowPosition, addNodes } = useReactFlow();
  const [reactFlowInstance, setReactFlowInstance] = useState(null);

  const onDragOver = useCallback((event: DragEvent) => {
    event.preventDefault();
    event.dataTransfer.dropEffect = 'move';
  }, []);

  const onDrop = useCallback((event: DragEvent) => {
    event.preventDefault();

    const type = event.dataTransfer.getData('application/reactflow');
    if (!type) return;

    // Convert screen position to flow position
    const position = screenToFlowPosition({
      x: event.clientX,
      y: event.clientY,
    });

    const newNode = {
      id: `${Date.now()}`,
      type,
      position,
      data: { label: `${type} node` },
    };

    addNodes(newNode);
  }, [screenToFlowPosition, addNodes]);

  return (
    <div ref={reactFlowWrapper} style={{ height: '100%' }}>
      <ReactFlow
        onDragOver={onDragOver}
        onDrop={onDrop}
        onInit={setReactFlowInstance}
      />
    </div>
  );
}

// Sidebar component
function Sidebar() {
  const onDragStart = (event: DragEvent, nodeType: string) => {
    event.dataTransfer.setData('application/reactflow', nodeType);
    event.dataTransfer.effectAllowed = 'move';
  };

  return (
    <aside>
      <div draggable onDragStart={(e) => onDragStart(e, 'input')}>
        Input Node
      </div>
      <div draggable onDragStart={(e) => onDragStart(e, 'default')}>
        Default Node
      </div>
    </aside>
  );
}
```

## Undo/Redo

```tsx
import { useCallback, useState } from 'react';

function useUndoRedo<T>(initialState: T) {
  const [history, setHistory] = useState<T[]>([initialState]);
  const [index, setIndex] = useState(0);

  const state = history[index];

  const setState = useCallback((newState: T | ((prev: T) => T)) => {
    setHistory((prev) => {
      const resolved = typeof newState === 'function'
        ? (newState as (prev: T) => T)(prev[index])
        : newState;

      // Remove future states and add new state
      const newHistory = prev.slice(0, index + 1);
      return [...newHistory, resolved];
    });
    setIndex((i) => i + 1);
  }, [index]);

  const undo = useCallback(() => {
    setIndex((i) => Math.max(0, i - 1));
  }, []);

  const redo = useCallback(() => {
    setIndex((i) => Math.min(history.length - 1, i + 1));
  }, [history.length]);

  const canUndo = index > 0;
  const canRedo = index < history.length - 1;

  return { state, setState, undo, redo, canUndo, canRedo };
}

// Usage
function Flow() {
  const {
    state: { nodes, edges },
    setState,
    undo, redo, canUndo, canRedo
  } = useUndoRedo({ nodes: initialNodes, edges: initialEdges });

  // Capture state on significant changes
  const onNodesChange = useCallback((changes) => {
    const hasPositionChange = changes.some(c => c.type === 'position' && !c.dragging);
    if (hasPositionChange) {
      setState(prev => ({
        nodes: applyNodeChanges(changes, prev.nodes),
        edges: prev.edges,
      }));
    }
  }, [setState]);
}
```

## Programmatic Layout with dagre

```tsx
import dagre from 'dagre';

interface LayoutOptions {
  direction: 'TB' | 'BT' | 'LR' | 'RL';
  nodeWidth: number;
  nodeHeight: number;
}

function getLayoutedElements(
  nodes: Node[],
  edges: Edge[],
  options: LayoutOptions = { direction: 'TB', nodeWidth: 172, nodeHeight: 36 }
) {
  const g = new dagre.graphlib.Graph();
  g.setGraph({ rankdir: options.direction });
  g.setDefaultEdgeLabel(() => ({}));

  nodes.forEach((node) => {
    g.setNode(node.id, {
      width: node.measured?.width ?? options.nodeWidth,
      height: node.measured?.height ?? options.nodeHeight,
    });
  });

  edges.forEach((edge) => {
    g.setEdge(edge.source, edge.target);
  });

  dagre.layout(g);

  const layoutedNodes = nodes.map((node) => {
    const nodeWithPosition = g.node(node.id);
    return {
      ...node,
      position: {
        x: nodeWithPosition.x - (node.measured?.width ?? options.nodeWidth) / 2,
        y: nodeWithPosition.y - (node.measured?.height ?? options.nodeHeight) / 2,
      },
    };
  });

  return { nodes: layoutedNodes, edges };
}

// Usage after nodes are measured
function Flow() {
  const { fitView } = useReactFlow();

  const onLayout = useCallback((direction: 'TB' | 'LR') => {
    const { nodes: layoutedNodes, edges: layoutedEdges } = getLayoutedElements(
      nodes,
      edges,
      { direction, nodeWidth: 150, nodeHeight: 50 }
    );

    setNodes([...layoutedNodes]);
    setEdges([...layoutedEdges]);

    window.requestAnimationFrame(() => {
      fitView({ duration: 500 });
    });
  }, [nodes, edges, setNodes, setEdges, fitView]);
}
```

## Connection with Edge on Drop

```tsx
function Flow() {
  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);
  const { screenToFlowPosition } = useReactFlow();

  const onConnectEnd = useCallback(
    (event: MouseEvent | TouchEvent, connectionState: FinalConnectionState) => {
      // Only proceed if dropped on pane (not on a node)
      if (!connectionState.isValid && connectionState.fromHandle) {
        const id = `${Date.now()}`;
        const { clientX, clientY } = 'changedTouches' in event
          ? event.changedTouches[0]
          : event;

        const newNode = {
          id,
          position: screenToFlowPosition({ x: clientX, y: clientY }),
          data: { label: 'New Node' },
        };

        setNodes((nds) => [...nds, newNode]);
        setEdges((eds) => [
          ...eds,
          {
            id: `e-${connectionState.fromNode?.id}-${id}`,
            source: connectionState.fromNode?.id ?? '',
            target: id,
          },
        ]);
      }
    },
    [screenToFlowPosition, setNodes, setEdges]
  );

  return (
    <ReactFlow
      nodes={nodes}
      edges={edges}
      onNodesChange={onNodesChange}
      onEdgesChange={onEdgesChange}
      onConnectEnd={onConnectEnd}
    />
  );
}
```

## Accessing Node Data from Edges

```tsx
import { useNodesData, type EdgeProps } from '@xyflow/react';

function DataEdge({ source, target, ...props }: EdgeProps) {
  // Get data for source and target nodes
  const nodesData = useNodesData([source, target]);
  const sourceData = nodesData[0];
  const targetData = nodesData[1];

  const [path, labelX, labelY] = getSmoothStepPath(props);

  return (
    <>
      <BaseEdge path={path} />
      <EdgeLabelRenderer>
        <div style={{ transform: `translate(-50%, -50%) translate(${labelX}px, ${labelY}px)` }}>
          {sourceData?.data?.label} → {targetData?.data?.label}
        </div>
      </EdgeLabelRenderer>
    </>
  );
}
```

## Middleware for Node Changes

```tsx
// Filter or modify changes before they're applied
const onNodesChangeMiddleware = useCallback((changes: NodeChange[]) => {
  // Example: Prevent deletion of certain nodes
  const filteredChanges = changes.filter((change) => {
    if (change.type === 'remove') {
      const node = nodes.find((n) => n.id === change.id);
      return node?.data?.deletable !== false;
    }
    return true;
  });

  setNodes((nds) => applyNodeChanges(filteredChanges, nds));
}, [nodes, setNodes]);
```

## Keyboard Shortcuts

```tsx
import { useKeyPress } from '@xyflow/react';

function Flow() {
  const { deleteElements, getNodes, getEdges, fitView } = useReactFlow();

  // Ctrl/Cmd + A: Select all
  const selectAllPressed = useKeyPress(['Meta+a', 'Control+a']);

  useEffect(() => {
    if (selectAllPressed) {
      setNodes((nds) => nds.map((n) => ({ ...n, selected: true })));
      setEdges((eds) => eds.map((e) => ({ ...e, selected: true })));
    }
  }, [selectAllPressed]);

  // Custom delete handler
  const deletePressed = useKeyPress(['Backspace', 'Delete']);

  useEffect(() => {
    if (deletePressed) {
      const selectedNodes = getNodes().filter((n) => n.selected);
      const selectedEdges = getEdges().filter((e) => e.selected);
      deleteElements({ nodes: selectedNodes, edges: selectedEdges });
    }
  }, [deletePressed]);
}
```

## Performance: Memoizing Selectors

```tsx
import { useCallback } from 'react';
import { useStore, type ReactFlowState } from '@xyflow/react';
import { shallow } from 'zustand/shallow';

// Create stable selector outside component
const nodesSelector = (state: ReactFlowState) => state.nodes;

// Or use multiple values with shallow compare
const flowStateSelector = (state: ReactFlowState) => ({
  nodes: state.nodes,
  edges: state.edges,
  viewport: state.transform,
});

function FlowInfo() {
  const { nodes, edges, viewport } = useStore(flowStateSelector, shallow);
  return <div>Nodes: {nodes.length}, Edges: {edges.length}</div>;
}
```
