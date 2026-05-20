---
name: dag-visual-editor-design
version: 1.0.0
description: Design modern, intuitive DAG/workflow visual editors that feel like LEGO, not LabView
category: Design
tags:
  - dag
  - workflow
  - visual-programming
  - node-editor
  - react-flow
  - ux-design
trigger_phrases:
  - "design dag editor"
  - "workflow builder ui"
  - "node graph ux"
  - "visual programming interface"
  - "make dag editor intuitive"
allowed_tools:
  - Read
  - Write
  - Edit
  - WebSearch
  - WebFetch
---

# DAG Visual Editor Design

Design modern, intuitive DAG and workflow visual editors. This skill captures best practices from industry leaders like **n8n**, **ComfyUI**, **Retool Workflows**, and **React Flow** — prioritizing clarity over complexity.

## Philosophy: LEGO, Not LabView

Traditional node editors (LabView, Max/MSP, older VFX tools) suffer from:
- Dense, cluttered interfaces
- Overwhelming port/connection complexity
- Steep learning curves
- "Spaghetti" wire syndrome

Modern DAG editors take a different approach:
- **LEGO-like composability** — snap blocks together
- **Progressive disclosure** — show complexity only when needed
- **Clear data flow** — left-to-right or top-to-bottom
- **Minimal chrome** — the content IS the interface

## Core Design Principles

### 1. Nodes as First-Class Components

Nodes should feel like self-contained units, not wiring terminals.

```
┌─────────────────────────────┐
│ 🔄 Transform Data           │  ← Clear title with icon
├─────────────────────────────┤
│ Input: users.json           │  ← Inline config, not ports
│ Output: filtered_users      │
├─────────────────────────────┤
│ ▶ Run  │ ⚙ Config │ 📋 Docs │  ← Actions in footer
└─────────────────────────────┘
```

**Bad (LabView style):**
```
    ●─┬─●     ●─●
      │       │
  ┌───┴───┐ ┌─┴─┐
  │ Node  │─│ N │
  └───┬───┘ └─┬─┘
      │       │
    ●─┴─●   ●─┴─●
```

**Good (Modern style):**
```
┌──────────┐      ┌──────────┐
│  Input   │ ───▶ │ Process  │ ───▶ [Output]
└──────────┘      └──────────┘
```

### 2. Connection Semantics

| Pattern | When to Use | Visual |
|---------|------------|--------|
| **Implicit** | Sequential flows | Vertical stack, no lines |
| **Explicit minimal** | Branching logic | Single clear edge |
| **Bundled** | Multiple data channels | Grouped/labeled edges |
| **Animated** | Execution/data flow | Particles along edges |

**Key insight from ComfyUI:** Show data flowing through edges during execution. Users understand what's happening.

### 3. Handle Design

**Avoid:** Multiple tiny ports crammed on node sides

**Prefer:**
- Single input handle (top or left)
- Single output handle (bottom or right)
- Type indicators via color/shape only when needed
- Handle reveals on hover for clean default state

### 4. Layout Algorithms

Auto-layout is critical. Users shouldn't manually arrange nodes.

```typescript
// Dagre layout (hierarchical, left-to-right)
const layout = dagre.graphlib.Graph()
  .setGraph({ rankdir: 'LR', ranksep: 80, nodesep: 40 })
  .setDefaultEdgeLabel(() => ({}));

// ELK (more sophisticated, handles complex graphs)
const elk = new ELK();
await elk.layout(graph, {
  algorithm: 'layered',
  'elk.direction': 'RIGHT',
  'elk.layered.spacing.nodeNodeBetweenLayers': 100,
});
```

### 5. Minimap & Navigation

Essential for complex workflows:
- Minimap in corner (toggleable)
- Fit-to-view on double-click background
- Breadcrumbs for nested/grouped nodes
- Search to jump to nodes

## Technology Stack

### React Flow (Recommended)
```tsx
import ReactFlow, {
  Background,
  Controls,
  MiniMap,
  useNodesState,
  useEdgesState,
} from 'reactflow';

function WorkflowEditor() {
  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);

  return (
    <ReactFlow
      nodes={nodes}
      edges={edges}
      onNodesChange={onNodesChange}
      onEdgesChange={onEdgesChange}
      fitView
    >
      <Background variant="dots" gap={16} />
      <MiniMap />
      <Controls />
    </ReactFlow>
  );
}
```

### Custom Node Template
```tsx
const SkillNode = ({ data, selected }) => (
  <div className={cn(
    "rounded-lg border-2 bg-white shadow-md min-w-[200px]",
    selected ? "border-blue-500" : "border-gray-200"
  )}>
    {/* Header */}
    <div className="flex items-center gap-2 px-3 py-2 bg-gray-50 rounded-t-lg">
      <span className="text-lg">{data.icon}</span>
      <span className="font-medium">{data.label}</span>
    </div>

    {/* Body - preview of config */}
    <div className="px-3 py-2 text-sm text-gray-600">
      {data.preview}
    </div>

    {/* Handles */}
    <Handle type="target" position={Position.Left} />
    <Handle type="source" position={Position.Right} />
  </div>
);
```

## Interaction Patterns

### Edge Drawing
1. Click source handle → drag → release on target handle
2. Show valid drop targets while dragging
3. Snap to nearest compatible handle
4. Allow edge deletion via backspace or context menu

### Node Creation
1. **Context menu** — Right-click on canvas
2. **Quick add** — Type `/` to search nodes (like Notion)
3. **Drag from library** — Sidebar with categorized nodes
4. **Connection drop** — Drop edge on empty space → node picker

### Keyboard Shortcuts
| Key | Action |
|-----|--------|
| `Delete` / `Backspace` | Remove selected |
| `Cmd/Ctrl + D` | Duplicate |
| `Cmd/Ctrl + G` | Group selected |
| `Cmd/Ctrl + Z` | Undo |
| `/` | Quick node search |
| `Space + Drag` | Pan canvas |
| `Scroll` | Zoom |

## Visual Hierarchy

### Node States
```css
/* Default */
.node { border: 2px solid #e5e7eb; }

/* Selected */
.node.selected { border-color: #3b82f6; box-shadow: 0 0 0 2px rgba(59,130,246,0.3); }

/* Running */
.node.running { border-color: #f59e0b; animation: pulse 1s infinite; }

/* Completed */
.node.completed { border-color: #10b981; }

/* Error */
.node.error { border-color: #ef4444; background: #fef2f2; }
```

### Edge Animation During Execution
```css
.edge-animated path {
  stroke-dasharray: 5;
  animation: dash 0.5s linear infinite;
}

@keyframes dash {
  to { stroke-dashoffset: -10; }
}
```

## Anti-Patterns to Avoid

1. **Too many handle types** — Color-code sparingly, not per data type
2. **Wire spaghetti** — Use auto-layout, not manual positioning
3. **Hidden complexity** — Don't collapse essential config into modals
4. **No execution feedback** — Show what's running and what's waiting
5. **Monolithic nodes** — Break complex operations into composable pieces
6. **Ignoring touch** — Support touch/pen for tablet users

## Case Studies

### n8n
- Clean card-based nodes
- Inline parameter editing
- Execution visualization with timing
- Excellent error highlighting

### ComfyUI
- Familiar to VFX/3D artists
- Lazy evaluation (only runs changed nodes)
- Shareable workflow JSON files
- Preview widgets inside nodes

### Retool Workflows
- Conditional branching UI
- Loop visualization
- Strong typing with visual indicators
- Enterprise-grade error handling

## Implementation Checklist

- [ ] React Flow or similar graph library
- [ ] Auto-layout with Dagre/ELK
- [ ] Custom node components with consistent design
- [ ] Edge animation during execution
- [ ] Minimap for navigation
- [ ] Keyboard shortcuts
- [ ] Undo/redo system
- [ ] Node search/quick add
- [ ] Save/load workflow state
- [ ] Export to JSON/image

## Resources

- [React Flow Documentation](https://reactflow.dev)
- [xyflow/awesome-node-based-uis](https://github.com/xyflow/awesome-node-based-uis)
- [n8n Node UI Design](https://docs.n8n.io/integrations/creating-nodes/plan/node-ui-design/)
- [ComfyUI Technical Deep Dive](https://medium.com/@mucahitceylan/comfyui-a-technical-deep-dive-into-the-ultimate-stable-diffusion-workflow-engine-df1a7db3f7f5)
- [ELK.js Layout Algorithms](https://eclipse.dev/elk/)
- [Dagre Layout](https://github.com/dagrejs/dagre)
