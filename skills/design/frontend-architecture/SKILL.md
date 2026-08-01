---
name: frontend-architecture
description: Frontend package architecture for ChainGraph visual flow editor. Use
  when working on apps/chaingraph-frontend, React components, Effector stores, XYFlow
  integration, UI components, providers, or hooks
---

---
name: frontend-architecture
description: Frontend package architecture for ChainGraph visual flow editor. Use when working on apps/chaingraph-frontend, React components, Effector stores, XYFlow integration, UI components, providers, or hooks. Covers directory structure, domain organization, provider hierarchy, component patterns. Triggers: frontend, react, component, provider, hook, ui, sidebar, flow editor, chaingraph-frontend, vite, tailwind.
---

# ChainGraph Frontend Architecture

This skill provides architectural guidance for the `@badaitech/chaingraph-frontend` package - a React-based visual programming interface for designing computational graphs.

## Package Overview

**Location**: `apps/chaingraph-frontend/`
**Purpose**: Visual flow editor for ChainGraph using XYFlow
**Stack**: React 19 + Vite + TypeScript + Effector + XYFlow + Tailwind + Radix UI

## Directory Structure

```
apps/chaingraph-frontend/src/
├── main.tsx                 # Entry point, store initialization
├── App.tsx                  # Router setup
├── FlowLayout.tsx           # Layout: Sidebar + Flow
├── config.ts                # Environment configuration
│
├── components/
│   ├── flow/                # Main flow editor (see below)
│   ├── ui/                  # Radix UI components (31 files)
│   ├── sidebar/             # Navigation & flow list
│   ├── dnd/                 # Drag-and-drop (dnd-kit)
│   ├── debug/               # Debug tools
│   └── theme/               # Theme switching
│
├── store/                   # Effector state (15 domains)
│   ├── domains.ts           # Domain definitions
│   ├── initialization.ts    # App init orchestration
│   ├── nodes/               # Node CRUD, positions
│   ├── edges/               # Edge connections, anchors
│   ├── flow/                # Active flow, metadata
│   ├── ports-v2/            # Port values, configs, UI
│   ├── execution/           # Execution state
│   ├── trpc/                # tRPC clients (2 servers)
│   └── ...                  # 20+ more domains
│
├── hooks/                   # Global custom hooks
└── providers/               # Provider hierarchy
```

## Flow Component Structure

```
components/flow/
├── Flow.tsx                 # Main XYFlow container (13.6KB)
├── nodes/
│   ├── ChaingraphNode/      # Main node component (17 files)
│   │   ├── ChaingraphNodeOptimized.tsx  # Perf-optimized
│   │   └── ports/           # ArrayPort, ObjectPort
│   ├── AnchorNode/          # Edge anchor visualization
│   └── GroupNode/           # Group nodes
├── edges/
│   ├── components/          # Edge UI
│   └── utils/               # Edge calculations
└── hooks/                   # 18 flow-specific hooks
    ├── useNodeDragHandling.ts
    ├── useNodeSelection.ts
    ├── useFlowCopyPaste.ts
    ├── useKeyboardShortcuts.ts
    └── ...
```

## Key Architectural Patterns

### 1. Two tRPC Clients

The app manages TWO separate WebSocket connections:

```typescript
// Main Server (flows, nodes, edges)
$trpcClient → ws://localhost:3001

// Executor Server (execution events)
$trpcClientExecutor → ws://localhost:4021
```

### 2. Effector Domain-Based Stores

15 domains organized by feature:

| Domain | Purpose |
|--------|---------|
| `nodes` | Node CRUD, positions, dimensions |
| `edges` | Connections, anchors, selection |
| `flow` | Active flow, metadata |
| `ports-v2` | Port values, configs, UI state |
| `execution` | Execution state & events |
| `trpc` | tRPC client instances |
| `xyflow` | XYFlow render optimization |

### 3. Optimistic Updates + Debouncing

```typescript
// Pattern: Local update → Debounce → Server sync
updateNodePositionLocal(event)  // Immediate UI update
// After NODE_POSITION_DEBOUNCE_MS (300ms)...
updateNodePositionFx(event)     // Send to server
```

### 4. Provider Hierarchy

```
ChainGraphProvider
  └─ RootProvider
      ├─ ThemeProvider
      ├─ ReactFlowProvider
      │   ├─ ZoomProvider
      │   ├─ DndContextProvider
      │   └─ MenuPositionProvider
      └─ [children]
```

## Store Patterns

### Creating a Store

```typescript
import { nodesDomain } from '../domains'

// Events (commands)
export const addNode = nodesDomain.createEvent<INode>()
export const removeNode = nodesDomain.createEvent<string>()

// Effects (async operations)
export const addNodeFx = nodesDomain.createEffect(async (params) => {
  const client = $trpcClient.getState()
  return client.flow.addNode.mutate(params)
})

// Stores
export const $nodes = nodesDomain.createStore<Record<string, INode>>({})
  .on(addNode, (nodes, node) => ({ ...nodes, [node.id]: node }))
  .on(removeNode, (nodes, id) => {
    const { [id]: _, ...rest } = nodes
    return rest
  })

// Derived stores
export const $selectedNodeIds = combine($nodes, (nodes) =>
  Object.keys(nodes).filter(id => nodes[id].isSelected)
)
```

### Global Reset Pattern

All stores support global reset:

```typescript
import { globalReset } from '../global'

$myStore.reset(globalReset)
```

## Component Patterns

### Using Effector in Components

```typescript
import { useUnit } from 'effector-react'
import { $nodes, addNode } from '@/store/nodes'

function MyComponent() {
  const [nodes, handleAddNode] = useUnit([$nodes, addNode])
  // ...
}
```

### Lazy Loading

```typescript
const LazyComponent = lazy(() => import('./HeavyComponent'))

// In render
<Suspense fallback={<Loading />}>
  <LazyComponent />
</Suspense>
```

## Performance Considerations

1. **Node Position Interpolation** - Smooth animations via `position-interpolation-advanced.ts`
2. **XYFlow Store** - Combined render data per node to reduce re-renders
3. **Effector Sampling** - Accumulate rapid updates, sample at intervals
4. **Debounce Constants**:
   - `NODE_POSITION_DEBOUNCE_MS = 300`
   - `NODE_DIMENSIONS_DEBOUNCE_MS = 500`
   - `NODE_UI_DEBOUNCE_MS = 1000`

## Key Files Reference

| File | Purpose |
|------|---------|
| `src/main.tsx` | App bootstrap |
| `src/store/initialization.ts` | Init orchestration |
| `src/store/domains.ts` | 13 Effector domains |
| `src/components/flow/Flow.tsx` | Main flow component |
| `src/providers/ChainGraphProvider.tsx` | Top-level provider |

## Best Practices

1. **Use domain-based stores** - Create stores within appropriate domains
2. **Optimistic updates first** - Update local store immediately, sync to server with debounce
3. **Avoid direct tRPC calls in components** - Use Effector effects
4. **Use `useUnit`** - Not `useStore` or `useEvent` separately
5. **Reset on `globalReset`** - All stores should support global reset
6. **Lazy load heavy components** - Especially documentation/tooltips
7. **Use ports-v2** - Legacy `ports/` is being phased out

## Related Skills

- `effector-patterns` - Effector state management anti-patterns
- `xyflow-patterns` - XYFlow integration patterns
- `subscription-sync` - Real-time data synchronization
- `optimistic-updates` - Optimistic UI patterns
- `chaingraph-concepts` - Core domain concepts
- `trpc-patterns` - tRPC framework patterns
- `trpc-flow-editing` - Flow editing tRPC procedures
