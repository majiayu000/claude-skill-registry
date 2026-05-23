---
name: drawer-floating-system
description: Drawer and floating panel system for TMNL. Invoke when implementing drawer stacks, floating panels, drag/resize behaviors, or parallax animations. Provides Rolodex stack, stx-powered state, and container query patterns.
model_invoked: true
triggers:
  - "drawer"
  - "floating panel"
  - "FloatingPanel"
  - "Rolodex"
  - "drawer stack"
  - "parallax"
  - "withDraggable"
  - "resize handles"
  - "panel persistence"
  - "stx state"
  - "GlobalSlot"
  - "PanelSlot"
---

# Drawer & Floating Panel System for TMNL

## Overview

A comprehensive panel management system with:
- **Drawer Stack** — Rolodex-style stacking with parallax lift animations
- **Floating Panels** — stx-powered state machines with 8-direction resize
- **Global/Panel Slots** — Composable content injection system
- **Motion Blur** — Velocity-based blur effects during drag
- **Persistence** — localStorage-backed panel geometry

## Canonical Sources

### TMNL Implementations

| File | Purpose | Pattern |
|------|---------|---------|
| `src/lib/drawer/Drawer.tsx` | Main drawer component | Compound component |
| `src/lib/drawer/DrawerStackContext.tsx` | Stack state management | React Context |
| `src/lib/drawer/GlobalSlot.tsx` | Global content injection | Slot pattern |
| `src/lib/drawer/PanelSlot.tsx` | Per-drawer content slots | Slot pattern |
| `src/lib/drawer/animations/rolodex.ts` | Rolodex stack animation | GSAP driver |
| `src/lib/drawer/animations/parallax-lift.ts` | Parallax scroll effect | Transform math |
| `src/lib/floating/FloatingPanel.tsx` | Floating panel component | stx + resize |
| `src/lib/floating/floating-stx.ts` | Legend-State + XState hybrid | stx pattern |
| `src/lib/floating/withDraggable.tsx` | Drag behavior HOC | Pointer events |
| `src/lib/floating/ResizeHandles.tsx` | 8-direction resize | Edge detection |

### Testbeds

- **DrawerTestbed**: `/testbed/drawer` — Rolodex stack, slot injection
- **FloatingPanelTestbed**: `/testbed/floating` — Drag, resize, persistence

---

## Pattern 1: Drawer Stack Management — ROLODEX PATTERN

**When:** Managing multiple stacked drawers with animated transitions.

The drawer stack uses a LIFO (Last-In-First-Out) model with visual stacking:

```typescript
import { createContext, useContext, useReducer } from 'react'

interface DrawerState {
  drawers: DrawerInstance[]
  activeId: string | null
}

type DrawerAction =
  | { type: 'PUSH'; drawer: DrawerInstance }
  | { type: 'POP' }
  | { type: 'POP_TO'; id: string }
  | { type: 'REPLACE'; drawer: DrawerInstance }

const drawerReducer = (state: DrawerState, action: DrawerAction): DrawerState => {
  switch (action.type) {
    case 'PUSH':
      return {
        drawers: [...state.drawers, action.drawer],
        activeId: action.drawer.id,
      }
    case 'POP':
      const popped = state.drawers.slice(0, -1)
      return {
        drawers: popped,
        activeId: popped[popped.length - 1]?.id ?? null,
      }
    case 'POP_TO': {
      const idx = state.drawers.findIndex(d => d.id === action.id)
      if (idx === -1) return state
      const remaining = state.drawers.slice(0, idx + 1)
      return {
        drawers: remaining,
        activeId: action.id,
      }
    }
    case 'REPLACE': {
      const replaced = [...state.drawers.slice(0, -1), action.drawer]
      return {
        drawers: replaced,
        activeId: action.drawer.id,
      }
    }
  }
}

const DrawerStackContext = createContext<{
  state: DrawerState
  dispatch: React.Dispatch<DrawerAction>
} | null>(null)
```

**TMNL Location**: `src/lib/drawer/DrawerStackContext.tsx`

---

## Pattern 2: Parallax Stack Animation — DEPTH EFFECTS

**When:** Creating visual depth with offset and scale transformations.

```typescript
import { gsap } from 'gsap'

interface ParallaxConfig {
  offsetY: number      // Vertical offset per layer (px)
  scaleDecay: number   // Scale reduction per layer (0-1)
  opacityDecay: number // Opacity reduction per layer (0-1)
}

const DEFAULT_CONFIG: ParallaxConfig = {
  offsetY: 20,
  scaleDecay: 0.02,
  opacityDecay: 0.15,
}

function applyParallaxStack(
  drawers: HTMLElement[],
  config: ParallaxConfig = DEFAULT_CONFIG
) {
  const active = drawers.length - 1

  drawers.forEach((el, idx) => {
    const depth = active - idx  // 0 = active, 1+ = behind

    gsap.to(el, {
      y: -depth * config.offsetY,
      scale: 1 - depth * config.scaleDecay,
      opacity: 1 - depth * config.opacityDecay,
      duration: 0.3,
      ease: 'power2.out',
    })
  })
}
```

**Key Formula**: `transform: translateY(${-depth * offsetY}px) scale(${1 - depth * scaleDecay})`

**TMNL Location**: `src/lib/drawer/animations/parallax-lift.ts`

---

## Pattern 3: TableService Integration — DATA-AWARE DRAWERS

**When:** Connecting drawers to data sources via table-service.

```typescript
import { TableService } from '@/lib/table-service'

interface DataDrawerProps<T> {
  tableService: TableService<T>
  rowId: string
  children: (data: T) => React.ReactNode
}

function DataDrawer<T>({ tableService, rowId, children }: DataDrawerProps<T>) {
  const row = useTableRow(tableService, rowId)

  if (!row) return null

  return (
    <Drawer id={`data-${rowId}`} title={`Row ${rowId}`}>
      {children(row)}
    </Drawer>
  )
}

// Usage
<DataDrawer tableService={assetService} rowId="asset-123">
  {(asset) => (
    <div>
      <h2>{asset.name}</h2>
      <AssetDetails asset={asset} />
    </div>
  )}
</DataDrawer>
```

**TMNL Location**: Integration pattern documented in `src/lib/table-service/`

---

## Pattern 4: stx-Powered Floating Panels — HYBRID STATE

**When:** Managing complex panel state with Legend-State reactivity + XState machines.

The "stx" pattern combines:
- **Legend-State** — Fine-grained reactive state (position, size)
- **XState** — Lifecycle state machine (idle, dragging, resizing)

```typescript
import { observable } from '@legendapp/state'
import { setup, createActor } from 'xstate'

// Legend-State for reactive data
const panelState = observable({
  panels: new Map<string, PanelState>(),
  zOrder: [] as string[],
})

// XState for lifecycle
const panelMachine = setup({
  types: {
    context: {} as { panelId: string; initialPos: Position },
    events: {} as
      | { type: 'DRAG_START'; x: number; y: number }
      | { type: 'DRAG_MOVE'; x: number; y: number }
      | { type: 'DRAG_END' }
      | { type: 'RESIZE_START'; edge: ResizeEdge }
      | { type: 'RESIZE_MOVE'; x: number; y: number }
      | { type: 'RESIZE_END' },
  },
}).createMachine({
  id: 'panel',
  initial: 'idle',
  states: {
    idle: {
      on: {
        DRAG_START: 'dragging',
        RESIZE_START: 'resizing',
      },
    },
    dragging: {
      on: {
        DRAG_MOVE: { actions: 'updatePosition' },
        DRAG_END: 'idle',
      },
    },
    resizing: {
      on: {
        RESIZE_MOVE: { actions: 'updateSize' },
        RESIZE_END: 'idle',
      },
    },
  },
})

// Combine into stx
const getFloatingStx = () => ({
  data: panelState,
  machine: panelMachine,
  computed: {
    topPanel: () => panelState.zOrder.get()[panelState.zOrder.get().length - 1],
    motionBlurStyle: (velocity: number) => ({
      filter: `blur(${Math.min(velocity * 0.1, 4)}px)`,
    }),
  },
  effects: {
    persist: () => {
      localStorage.setItem('panels', JSON.stringify(panelState.get()))
    },
    restore: () => {
      const saved = localStorage.getItem('panels')
      if (saved) panelState.set(JSON.parse(saved))
    },
  },
})
```

**TMNL Location**: `src/lib/floating/floating-stx.ts`

---

## Pattern 5: FloatingPanel Component — 8-DIRECTION RESIZE

**When:** Creating resizable, draggable floating panels.

```tsx
import { useFloatingPanel } from './hooks/useFloatingPanel'
import { ResizeHandles } from './ResizeHandles'

interface FloatingPanelProps {
  id: string
  title: string
  initialPosition?: Position
  initialSize?: Size
  minSize?: Size
  maxSize?: Size
  children: React.ReactNode
}

function FloatingPanel({
  id,
  title,
  initialPosition = { x: 100, y: 100 },
  initialSize = { width: 320, height: 240 },
  minSize = { width: 200, height: 150 },
  maxSize,
  children,
}: FloatingPanelProps) {
  const {
    position,
    size,
    zIndex,
    isDragging,
    isResizing,
    handleDragStart,
    handleResizeStart,
    bringToFront,
  } = useFloatingPanel(id, { initialPosition, initialSize })

  return (
    <div
      className="floating-panel"
      style={{
        position: 'fixed',
        left: position.x,
        top: position.y,
        width: size.width,
        height: size.height,
        zIndex,
      }}
      onPointerDown={bringToFront}
    >
      {/* Title bar (drag handle) */}
      <div
        className="panel-titlebar"
        onPointerDown={handleDragStart}
      >
        {title}
      </div>

      {/* Content */}
      <div className="panel-content">
        {children}
      </div>

      {/* Resize handles */}
      <ResizeHandles
        onResizeStart={handleResizeStart}
        minSize={minSize}
        maxSize={maxSize}
      />
    </div>
  )
}
```

**TMNL Location**: `src/lib/floating/FloatingPanel.tsx`

---

## Pattern 6: withDraggable HOC — POINTER EVENT MANAGEMENT

**When:** Adding drag behavior to any component.

```tsx
import { useCallback, useRef, useState } from 'react'

interface DraggableOptions {
  onDragStart?: (pos: Position) => void
  onDrag?: (pos: Position, delta: Position) => void
  onDragEnd?: (pos: Position) => void
  constraint?: 'none' | 'horizontal' | 'vertical' | DOMRect
}

function withDraggable<P extends object>(
  Component: React.ComponentType<P>,
  options: DraggableOptions = {}
) {
  return function DraggableComponent(props: P) {
    const [isDragging, setIsDragging] = useState(false)
    const startPos = useRef<Position>({ x: 0, y: 0 })
    const currentPos = useRef<Position>({ x: 0, y: 0 })

    const handlePointerDown = useCallback((e: React.PointerEvent) => {
      e.preventDefault()
      e.currentTarget.setPointerCapture(e.pointerId)

      startPos.current = { x: e.clientX, y: e.clientY }
      currentPos.current = { x: e.clientX, y: e.clientY }
      setIsDragging(true)

      options.onDragStart?.(startPos.current)
    }, [])

    const handlePointerMove = useCallback((e: React.PointerEvent) => {
      if (!isDragging) return

      const delta = {
        x: e.clientX - currentPos.current.x,
        y: e.clientY - currentPos.current.y,
      }
      currentPos.current = { x: e.clientX, y: e.clientY }

      options.onDrag?.(currentPos.current, delta)
    }, [isDragging])

    const handlePointerUp = useCallback((e: React.PointerEvent) => {
      e.currentTarget.releasePointerCapture(e.pointerId)
      setIsDragging(false)

      options.onDragEnd?.(currentPos.current)
    }, [])

    return (
      <Component
        {...props}
        onPointerDown={handlePointerDown}
        onPointerMove={handlePointerMove}
        onPointerUp={handlePointerUp}
        data-dragging={isDragging}
      />
    )
  }
}
```

**TMNL Location**: `src/lib/floating/withDraggable.tsx`

---

## Pattern 7: Container Queries — RESPONSIVE PANELS

**When:** Adapting panel content to available space.

```tsx
// Use container queries for panel-intrinsic sizing
function ResponsivePanelContent({ children }: { children: React.ReactNode }) {
  return (
    <div className="@container panel-content">
      <div className="@[200px]:grid-cols-1 @[400px]:grid-cols-2 @[600px]:grid-cols-3 grid gap-4">
        {children}
      </div>
    </div>
  )
}

// CSS (Tailwind container queries)
// @container panel-content (min-width: 400px) { ... }
```

**Alternative: FloatingDimensionContext**

```tsx
import { createContext, useContext } from 'react'

const FloatingDimensionContext = createContext<Size>({ width: 320, height: 240 })

function FloatingPanel({ size, children }) {
  return (
    <FloatingDimensionContext.Provider value={size}>
      {children}
    </FloatingDimensionContext.Provider>
  )
}

function PanelContent() {
  const { width, height } = useContext(FloatingDimensionContext)

  // Adapt to available dimensions
  const columns = width < 300 ? 1 : width < 500 ? 2 : 3
  return <Grid columns={columns}>...</Grid>
}
```

**TMNL Location**: `src/lib/floating/FloatingDimensionContext.tsx`

---

## Pattern 8: Motion Blur — VELOCITY-BASED EFFECTS

**When:** Adding motion blur during fast drag operations.

```typescript
const calculateMotionBlur = (velocity: number): string => {
  // velocity = pixels/frame
  const blurAmount = Math.min(velocity * 0.15, 8)  // Cap at 8px
  const direction = velocity > 0 ? 'horizontal' : 'vertical'

  if (blurAmount < 0.5) return 'none'

  return `blur(${blurAmount}px)`
}

// In drag handler
const handleDrag = (e: PointerEvent) => {
  const velocity = Math.sqrt(
    Math.pow(e.movementX, 2) + Math.pow(e.movementY, 2)
  )

  panelRef.current.style.filter = calculateMotionBlur(velocity)
}

const handleDragEnd = () => {
  // Animate blur removal
  gsap.to(panelRef.current, {
    filter: 'blur(0px)',
    duration: 0.2,
  })
}
```

**TMNL Location**: `src/lib/floating/floating-stx.ts` (computed)

---

## Pattern 9: Panel Persistence — LOCALSTORAGE GEOMETRY

**When:** Remembering panel positions/sizes across sessions.

```typescript
import { useEffect } from 'react'

const STORAGE_KEY = 'tmnl:panel-geometry'

interface PersistedPanel {
  id: string
  position: Position
  size: Size
  zIndex: number
}

const usePanelPersistence = (panelId: string) => {
  const loadGeometry = (): PersistedPanel | null => {
    const stored = localStorage.getItem(STORAGE_KEY)
    if (!stored) return null

    const panels: Record<string, PersistedPanel> = JSON.parse(stored)
    return panels[panelId] ?? null
  }

  const saveGeometry = (geometry: Omit<PersistedPanel, 'id'>) => {
    const stored = localStorage.getItem(STORAGE_KEY)
    const panels: Record<string, PersistedPanel> = stored ? JSON.parse(stored) : {}

    panels[panelId] = { id: panelId, ...geometry }
    localStorage.setItem(STORAGE_KEY, JSON.stringify(panels))
  }

  // Debounced save during drag/resize
  const debouncedSave = useMemo(
    () => debounce(saveGeometry, 200),
    [panelId]
  )

  return { loadGeometry, saveGeometry: debouncedSave }
}
```

**TMNL Location**: `src/lib/floating/hooks/usePanelPersistence.ts`

---

## Pattern 10: Global vs Panel Slots — CONTENT INJECTION

**When:** Injecting content at different levels of the drawer hierarchy.

```tsx
import { createContext, useContext } from 'react'

// Global slot: content appears in all drawers
const GlobalSlotContext = createContext<React.ReactNode>(null)

function GlobalSlot({ children }: { children: React.ReactNode }) {
  return (
    <GlobalSlotContext.Provider value={children}>
      {children}
    </GlobalSlotContext.Provider>
  )
}

// Panel slot: content scoped to specific drawer
const PanelSlotContext = createContext<Map<string, React.ReactNode>>(new Map())

function PanelSlot({
  name,
  children,
}: {
  name: string
  children: React.ReactNode
}) {
  const slots = useContext(PanelSlotContext)
  slots.set(name, children)
  return null
}

// Usage in drawer
function Drawer({ id, children }) {
  const globalContent = useContext(GlobalSlotContext)
  const [slots] = useState(() => new Map())

  return (
    <PanelSlotContext.Provider value={slots}>
      <div className="drawer">
        {/* Global slot renders in header */}
        <div className="drawer-header">{globalContent}</div>

        {/* Main content */}
        <div className="drawer-content">{children}</div>

        {/* Named slots render in footer */}
        <div className="drawer-footer">{slots.get('footer')}</div>
      </div>
    </PanelSlotContext.Provider>
  )
}

// Consumer
<GlobalSlot>
  <Breadcrumbs />
</GlobalSlot>

<Drawer id="details">
  <AssetDetails />
  <PanelSlot name="footer">
    <ActionButtons />
  </PanelSlot>
</Drawer>
```

**TMNL Location**: `src/lib/drawer/GlobalSlot.tsx`, `src/lib/drawer/PanelSlot.tsx`

---

## Decision Tree: Component Selection

```
What are you building?
│
├─ Stacked content panels?
│  ├─ Sequential navigation? → Drawer Stack (Pattern 1)
│  └─ Depth effect? → Parallax Stack (Pattern 2)
│
├─ Floating window?
│  ├─ Resizable + draggable? → FloatingPanel (Pattern 5)
│  └─ Just draggable? → withDraggable HOC (Pattern 6)
│
├─ Complex state with animations?
│  └─ stx-Powered Panels (Pattern 4)
│
├─ Remember panel positions?
│  └─ Panel Persistence (Pattern 9)
│
└─ Content injection?
   ├─ All drawers? → GlobalSlot
   └─ Specific drawer? → PanelSlot
```

---

## Anti-Patterns

### Don't: Use transform-origin incorrectly for stacking

```tsx
// BANNED - Scale from wrong origin causes visual jump
style={{ transform: `scale(${1 - depth * 0.02})` }}

// CORRECT - Scale from top center for card-like effect
style={{
  transformOrigin: 'top center',
  transform: `scale(${1 - depth * 0.02})`,
}}
```

### Don't: Store panel position in useState during drag

```tsx
// BANNED - Too many re-renders during drag
const [position, setPosition] = useState({ x: 0, y: 0 })
onDrag={(pos) => setPosition(pos)}  // 60+ re-renders/sec

// CORRECT - Use refs for drag, sync state on end
const posRef = useRef({ x: 0, y: 0 })
onDrag={(pos) => { posRef.current = pos }}
onDragEnd={() => setPosition(posRef.current)}
```

### Don't: Forget pointer capture

```tsx
// BANNED - Drag breaks if pointer leaves element
onPointerDown={() => setDragging(true)}

// CORRECT - Capture pointer for reliable tracking
onPointerDown={(e) => {
  e.currentTarget.setPointerCapture(e.pointerId)
  setDragging(true)
}}
```

---

## Integration Points

**Depends on:**
- `xstate-integration` — Panel lifecycle machines
- `tmnl-animation-tokens` — Animation timings
- `react-hoc-patterns` — withDraggable HOC

**Used by:**
- `ag-grid-patterns` — Detail panels for grid rows
- `tmnl-registry-patterns` — Overlay system

---

## Quick Reference

| Task | Pattern | File |
|------|---------|------|
| Stack drawers with animation | Drawer Stack | drawer/DrawerStackContext.tsx |
| Create parallax depth | Parallax Stack | drawer/animations/parallax-lift.ts |
| Build floating panel | FloatingPanel | floating/FloatingPanel.tsx |
| Add drag behavior | withDraggable | floating/withDraggable.tsx |
| Manage stx state | floating-stx | floating/floating-stx.ts |
| Add resize handles | ResizeHandles | floating/ResizeHandles.tsx |
| Persist panel geometry | usePanelPersistence | floating/hooks/usePanelPersistence.ts |
| Inject global content | GlobalSlot | drawer/GlobalSlot.tsx |
