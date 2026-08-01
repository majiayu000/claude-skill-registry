---
name: xyflow-patterns
description: XYFlow integration patterns for ChainGraph visual flow editor. Use when
  working on node rendering, edge rendering, drag-and-drop, selection handling, anchors,
  handles, or any XYFlow-related UI code. C
---

---
name: xyflow-patterns
description: XYFlow integration patterns for ChainGraph visual flow editor. Use when working on node rendering, edge rendering, drag-and-drop, selection handling, anchors, handles, or any XYFlow-related UI code. Covers custom nodes/edges, performance optimization, handle positioning. Triggers: xyflow, reactflow, node rendering, edge rendering, handle, anchor, drag drop, selection, viewport, canvas, flow editor UI.
---

# XYFlow Patterns for ChainGraph

This skill covers XYFlow (React Flow) integration patterns used in the ChainGraph visual flow editor.

## XYFlow Overview

**Library**: `@xyflow/react` (React Flow v12+)
**Purpose**: Canvas-based flow editor with nodes, edges, zoom, pan
**ChainGraph Integration**: `apps/chaingraph-frontend/src/components/flow/Flow.tsx`

## Architecture

```
┌────────────────────────────────────────────────────────────┐
│                    Flow.tsx (Main Component)                │
│  ├─ ReactFlow                                               │
│  │   ├─ nodes (from useXYFlowNodes())                       │
│  │   ├─ edges (from useXYFlowEdges())                       │
│  │   ├─ nodeTypes (chaingraphNode, groupNode, anchorNode)   │
│  │   ├─ edgeTypes (flow, animated, default)                 │
│  │   └─ callbacks (onNodesChange, onEdgesChange, ...)       │
│  ├─ Background                                              │
│  ├─ StyledControls                                          │
│  └─ Custom UI Overlays (ContextMenu, ControlPanel)          │
└────────────────────────────────────────────────────────────┘
```

---

## Node Types

ChainGraph defines 3 custom node types:

**File**: `apps/chaingraph-frontend/src/components/flow/Flow.tsx:134-138`

```typescript
const nodeTypes = useMemo(() => ({
  chaingraphNode: ChaingraphNodeOptimized,  // Main computational node
  groupNode: memo(GroupNode),               // Container for grouping
  anchorNode: memo(AnchorNode),             // Edge anchor waypoints
}), [])
```

### ChaingraphNodeOptimized

**File**: `apps/chaingraph-frontend/src/components/flow/nodes/ChaingraphNode/ChaingraphNodeOptimized.tsx`

The main node component with heavy optimization via memoization:

```typescript
const ChaingraphNodeOptimized = memo(
  (props: NodeProps<ChaingraphNode>) => <ChaingraphNodeComponent {...props} />,
  (prevProps, nextProps) => {
    // Custom comparison for performance
    // Returns false (re-render) when id, selected, version, width, or height change
    return true // (no re-render) when everything matches
  },
)
```

### ChaingraphNode Component

**File**: `apps/chaingraph-frontend/src/components/flow/nodes/ChaingraphNode/ChaingraphNode.tsx`

Uses single consolidated render data subscription:

```typescript
function ChaingraphNodeComponent({ data, selected, id }: NodeProps<ChaingraphNode>) {
  // ✅ Single subscription for ALL render data (replaces 10 hooks)
  const renderData = useXYFlowNodeRenderData(id)

  // ✅ Flow metadata (keep separate - rarely changes, used for handlers)
  const activeFlow = useUnit($activeFlowMetadata)

  // ✅ Flow loaded (keep separate - simple guard)
  const isFlowLoaded = useUnit($isFlowLoaded)

  // ... component rendering
}
```

**Performance Result**: 97% fewer re-renders during drag operations (from 13 subscriptions to 4).

---

## Performance Optimization

### Consolidated Render Data Store

**Store**: `$xyflowNodeRenderMap` (NOT `$xyflowNodeRenderData`)
**File**: `apps/chaingraph-frontend/src/store/xyflow/stores/node-render-data.ts`
**Hook**: `useXYFlowNodeRenderData(nodeId)`

```typescript
// Hook usage (apps/chaingraph-frontend/src/store/xyflow/hooks/useXYFlowNodeRenderData.ts)
const renderData = useXYFlowNodeRenderData(nodeId)
```

### XYFlowNodeRenderData Interface

**File**: `apps/chaingraph-frontend/src/store/xyflow/types.ts:48-114`

```typescript
export interface XYFlowNodeRenderData {
  // Core identity
  nodeId: string
  version: number

  // Port ID arrays (pre-computed - no iteration in components!)
  inputPortIds: string[]
  outputPortIds: string[]
  passthroughPortIds: string[]

  // Specific system ports (pre-computed)
  flowInputPortId: string | null
  flowOutputPortId: string | null
  errorPortId: string | null
  errorMessagePortId: string | null

  // Metadata
  title: string
  status: 'idle' | 'running' | 'completed' | 'failed' | 'skipped'

  // Position & dimensions
  position: Position
  dimensions: { width: number, height: number }

  // Visual properties
  nodeType: 'chaingraphNode' | 'groupNode'
  categoryMetadata: CategoryMetadata
  zIndex: number

  // State flags
  isSelected: boolean
  isHidden: boolean
  isDraggable: boolean
  parentNodeId: string | undefined

  // Execution state
  executionStyle: string | undefined
  executionStatus: NodeExecutionStatus
  executionNode: ExecutionNodeData | null

  // Interaction state
  isHighlighted: boolean
  hasAnyHighlights: boolean
  pulseState: PulseState
  dropFeedback: DropFeedback | null

  // Debug state
  hasBreakpoint: boolean
  debugMode: boolean
}
```

### 8-Wire Delta Update System

The store uses 8 wires for surgical delta updates instead of full recalculation:

1. **Position updates** - High frequency (60fps during drag)
2. **Node data changes** - Version, dimensions, selection
3. **Execution state** - Execution events
4. **Highlight changes** - User highlights
5. **Pulse state** - Animation (200ms intervals)
6. **Drop feedback** - Drag operations
7. **Layer depth** - Parent structure changes
8. **Category metadata** - Theme changes

---

## Edge Types

**File**: `apps/chaingraph-frontend/src/components/flow/edges/index.ts`

```typescript
export const edgeTypes = {
  animated: AnimatedEdge,
  flow: FlowEdge,
  default: AnimatedEdge, // Fallback for edges without explicit type
} satisfies EdgeTypes
```

**Note**: Edge type keys are `flow`, `animated`, `default` - NOT `flowEdge`, `animatedEdge`.

### FlowEdge Component

**File**: `apps/chaingraph-frontend/src/components/flow/edges/FlowEdge.tsx`

Features:
- Catmull-Rom splines via `catmullRomToBezierPath()`
- Ghost anchors for adding new waypoints
- Selection highlighting
- Hover state feedback
- Animated particle effects (when `data.animated = true`)

```typescript
export const FlowEdge = memo(({
  id, sourceX, sourceY, targetX, targetY,
  sourcePosition, targetPosition, style, data,
}: EdgeProps) => {
  // Anchor support
  const selectedEdgeId = useUnit($selectedEdgeId)
  const isSelected = selectedEdgeId === id

  // Get anchor positions from anchor nodes store
  // PROTOTYPE: Anchors are now XYFlow nodes, positions come from their node positions
  const anchorPositions = useAnchorNodePositions(edgeId)

  // Path calculation with Catmull-Rom splines
  const pathData = useMemo(() => {
    return catmullRomToBezierPath(source, target, anchorPositions, sourcePosition, targetPosition)
  }, [source, target, anchorPositions, sourcePosition, targetPosition])

  // Ghost anchors (only when selected)
  const ghostAnchors = useMemo(() => {
    if (!isSelected) return []
    return calculateGhostAnchors(source, target, anchorPositions, sourcePosition, targetPosition)
  }, [isSelected, source, target, anchorPositions, sourcePosition, targetPosition])

  // ...
})
```

---

## Anchor System

**Key Insight**: Anchors are now XYFlow nodes (`anchorNode` type), NOT SVG circles rendered inside edges.

### Architecture

```
User clicks ghost anchor
    ↓
addAnchorNode event fires
    ↓
$anchorNodes store updates
    ↓
$anchorXYFlowNodes derived store creates XYFlow Node
    ↓
XYFlow handles drag/selection natively
    ↓
FlowEdge queries anchor positions for path calculation
    ↓
Changes sync to backend in EdgeMetadata.anchors[] format
```

### AnchorNodeState

**File**: `apps/chaingraph-frontend/src/store/edges/anchor-nodes.ts:46-56`

```typescript
export interface AnchorNodeState {
  id: string
  edgeId: string
  x: number // Flow position (top-left of node, not center)
  y: number
  index: number
  color?: string
  parentNodeId?: string // For XYFlow native parenting
  selected?: boolean
  version: number // Increments on any change to force XYFlow re-render
}
```

### EdgeAnchor Interface (Backend)

**File**: `packages/chaingraph-types/src/edge/types.ts:27-40`

```typescript
export interface EdgeAnchor {
  /** Unique identifier */
  id: string
  /** X coordinate (absolute if no parent, relative if parentNodeId is set) */
  x: number
  /** Y coordinate (absolute if no parent, relative if parentNodeId is set) */
  y: number
  /** Order index in path (0 = closest to source) */
  index: number
  /** Parent group node ID (if anchor is child of a group) */
  parentNodeId?: string
  /** Selection state (set by backend during paste operations) */
  selected?: boolean
}
```

### Anchor Events

```typescript
// Add anchor (from ghost anchor click)
export const addAnchorNode = edgesDomain.createEvent<{
  edgeId: string
  x: number
  y: number
  index: number
  color?: string
}>()

// Remove anchor (double-click or Delete key)
export const removeAnchorNode = edgesDomain.createEvent<{
  anchorNodeId: string
  edgeId?: string
}>()

// Update position (from XYFlow drag)
export const updateAnchorNodePosition = edgesDomain.createEvent<{
  anchorNodeId: string
  x: number
  y: number
}>()
```

### Ghost Anchors

Ghost anchors are SVG visual hints that appear when an edge is selected:

```typescript
// FlowEdge.tsx:268-272
const ghostAnchors = useMemo(() => {
  if (!isSelected) return []
  return calculateGhostAnchors(source, target, anchorPositions, sourcePosition, targetPosition)
}, [isSelected, source, target, anchorPositions, sourcePosition, targetPosition])

// Click handler creates real anchor node
const handleGhostClick = useCallback((insertIndex: number, x: number, y: number) => {
  addAnchorNode({
    edgeId,
    x,
    y,
    index: insertIndex,
    color: stroke,
  })
}, [edgeId, stroke])
```

---

## Handle Positioning

Handle positioning is delegated to XYFlow's automatic layout system.

**File**: `apps/chaingraph-frontend/src/components/flow/nodes/ChaingraphNode/ports/ui/PortHandle.tsx`

```typescript
const position = direction === 'input'
  ? Position.Left
  : Position.Right

<Handle
  type={direction === 'input' ? 'target' : 'source'}
  position={position}
  id={portId}
/>
```

**Note**: ChainGraph does NOT use custom `calculateHandlePosition()` functions. Vertical handle distribution is managed by the component layout, not explicit Y positioning.

---

## Custom Hooks

### Flow Interaction Hooks (18 hooks)

**Location**: `apps/chaingraph-frontend/src/components/flow/hooks/`

| Hook | Purpose |
|------|---------|
| `useBoxSelection` | Blender-style box selection with B key |
| `useCanvasHover` | Canvas hover detection for hotkeys |
| `useConnectionHandling` | Connection creation with cycle detection |
| `useEdgeAnchorKeyboard` | Keyboard shortcuts for anchor management |
| `useEdgeChanges` | Edge removal and selection handling |
| `useEdgeKeyboardShortcuts` | Edge-related keyboard shortcuts |
| `useEdgeReconnection` | Edge reconnection (onReconnectStart/onReconnect/onReconnectEnd) |
| `useFlowCallbacks` | Orchestrates all flow interaction callbacks |
| `useFlowCopyPaste` | Copy/paste and export/import operations |
| `useFlowUtils` | Utility functions (NOT a React hook - exports pure functions) |
| `useGrabMode` | Blender-style grab mode with G key |
| `useKeyboardShortcuts` | Unified shortcuts (Ctrl+C, Ctrl+V, Shift+D, A, F, X) |
| `useNodeChanges` | Node position, selection, and parent updates |
| `useNodeDragHandling` | Node drag with parent/group management |
| `useNodeDrop` | Node drop handling with position calculation |
| `useNodeSchemaDropEvents` | Node schema drop detection via event emitter |
| `useNodeSelection` | Node selection utilities (helper functions) |
| `useSelectionHotkeys` | Selection-related hotkeys |

### XYFlow Data Hooks

**Location**: `apps/chaingraph-frontend/src/store/xyflow/hooks/`

| Hook | Purpose |
|------|---------|
| `useXYFlowNodeRenderData` | Single subscription for all node render data |
| `useXYFlowNodeBodyPorts` | Body port IDs for node body rendering |
| `useXYFlowNodeErrorPorts` | Error port IDs for error section |
| `useXYFlowNodeFlowPorts` | Flow port IDs (input/output) |
| `useXYFlowNodeHeaderData` | Header data (title, category, etc.) |

### Store Data Hooks

**Location**: `apps/chaingraph-frontend/src/store/*/hooks/`

| Hook | Purpose |
|------|---------|
| `useXYFlowNodes` | XYFlow-compatible nodes from Effector stores |
| `useXYFlowEdges` | XYFlow-compatible edges from Effector stores |

---

## ReactFlow Configuration

**File**: `apps/chaingraph-frontend/src/components/flow/Flow.tsx:303-356`

```typescript
<ReactFlow
  nodes={nodes}
  nodeTypes={nodeTypes}
  edges={edges}
  edgeTypes={edgeTypes}

  // Callbacks
  onNodesChange={onNodesChange}
  onEdgesChange={onEdgesChange}
  onConnect={onConnect}
  onConnectStart={...}
  onConnectEnd={...}
  onNodeClick={handleNodeClick}
  onEdgeClick={handleEdgeClick}
  onPaneClick={handlePaneClick}
  onReconnect={onReconnect}
  onReconnectStart={onReconnectStart}
  onReconnectEnd={onReconnectEnd}
  onNodeDrag={onNodeDrag}
  onNodeDragStart={onNodeDragStart}
  onNodeDragStop={onNodeDragStop}
  onSelectionEnd={onSelectionEnd}
  onViewportChange={onViewportChange}

  // Selection & Pan
  panOnScroll={true}
  panOnDrag={panOnDrag}           // From useBoxSelection()
  selectionOnDrag={selectionOnDrag} // From useBoxSelection()
  selectionMode={selectionMode}   // From useBoxSelection()

  // Features
  zoomOnDoubleClick={true}
  connectOnClick={true}
  deleteKeyCode={['Delete', 'Backspace']}
  fitView={true}
  preventScrolling

  // Zoom limits
  minZoom={0.05}
  maxZoom={2}

  // Drag settings
  nodeDragThreshold={1}
  nodesDraggable={!isGrabMode}

  // Viewport
  defaultViewport={{ x: 0, y: 0, zoom: 0.2 }}
  defaultEdgeOptions={{ animated: true }}

  className="bg-background"
>
  <Background />
  <NodeInternalsSync />
  <StyledControls position="bottom-right" />
  {activeFlowId && <FlowControlPanel />}
</ReactFlow>
```

---

## Key Files

| File | Purpose |
|------|---------|
| `components/flow/Flow.tsx` | Main XYFlow container |
| `components/flow/nodes/ChaingraphNode/ChaingraphNodeOptimized.tsx` | Optimized node wrapper |
| `components/flow/nodes/ChaingraphNode/ChaingraphNode.tsx` | Main node component |
| `components/flow/nodes/AnchorNode/AnchorNode.tsx` | Anchor node component |
| `components/flow/edges/FlowEdge.tsx` | Custom edge with anchors |
| `components/flow/edges/index.ts` | Edge type registration |
| `store/xyflow/types.ts` | XYFlowNodeRenderData interface |
| `store/xyflow/stores/node-render-data.ts` | $xyflowNodeRenderMap store |
| `store/xyflow/hooks/useXYFlowNodeRenderData.ts` | Render data hook |
| `store/nodes/hooks/useXYFlowNodes.ts` | Node data transformation |
| `store/edges/hooks/useXYFlowEdges.ts` | Edge data transformation |
| `store/edges/anchor-nodes.ts` | Anchor node store and events |
| `components/flow/hooks/` | 18 interaction hooks |

---

## Common Patterns

### Adding a Custom Node Type

```typescript
// 1. Create node component
function MyCustomNode({ id, data }: NodeProps<MyData>) {
  return (
    <div className="my-custom-node">
      <Handle type="target" position={Position.Left} />
      {data.label}
      <Handle type="source" position={Position.Right} />
    </div>
  )
}

// 2. Register in nodeTypes (Flow.tsx)
const nodeTypes = useMemo(() => ({
  chaingraphNode: ChaingraphNodeOptimized,
  groupNode: memo(GroupNode),
  anchorNode: memo(AnchorNode),
  myCustomNode: memo(MyCustomNode),  // Add here
}), [])

// 3. Use in node data
addNode({
  id: 'node-1',
  type: 'myCustomNode',
  position: { x: 100, y: 100 },
  data: { label: 'Custom' },
})
```

### Custom Edge Styling

```typescript
function StyledEdge({ id, ...props }: EdgeProps) {
  const selectedEdgeId = useUnit($selectedEdgeId)
  const isActive = selectedEdgeId === id

  return (
    <path
      {...props}
      style={{
        stroke: isActive ? '#3b82f6' : '#6b7280',
        strokeWidth: isActive ? 3 : 2,
      }}
    />
  )
}
```

---

## Related Skills

- `frontend-architecture` - Overall frontend structure
- `effector-patterns` - Store patterns used
- `subscription-sync` - Real-time node/edge updates
- `optimistic-updates` - Position interpolation
- `chaingraph-concepts` - Node/edge domain concepts
