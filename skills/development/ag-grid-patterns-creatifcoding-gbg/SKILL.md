---
name: ag-grid-patterns
description: AG-Grid v34 integration patterns for TMNL. Invoke when implementing data grids, custom cell renderers, themes, or grid-based UI. Provides canonical file locations and pattern precedents.
model_invoked: true
triggers:
  - "AG-Grid"
  - "ag-grid"
  - "data grid"
  - "DataGrid"
  - "TmnlDataGrid"
  - "cell renderer"
  - "column definition"
  - "rowData"
  - "GridVariant"
  - "flash"
  - "cell flash"
---

# AG-Grid Patterns for TMNL

## Critical: AG-Grid v34 Module Registration

**Without this, grid renders blank. No exceptions.**

```typescript
import { ModuleRegistry, AllCommunityModule } from 'ag-grid-community'
ModuleRegistry.registerModules([AllCommunityModule])
```

No CSS imports needed when using the `theme` prop.

---

## Canonical Sources

### Core Library (v2)
- **Compound component**: `src/lib/data-grid/components/UnifiedDataGrid.tsx`
- **Context system**: `src/lib/data-grid/components/DataGridContext.tsx`
- **Theme composer**: `src/lib/data-grid/composer/theme-composer.ts`
- **Flash system**: `src/lib/data-grid/flash/index.ts`
- **Cell renderers**: `src/lib/data-grid/renderers/`
- **Variants**: `src/lib/data-grid/variants/`
- **Barrel export**: `src/lib/data-grid/index.ts`

### tldraw Integration
- **V2 shape (modern)**: `src/components/tldraw/shapes/data-grid-shape-v2.tsx`
- **V1 shape (legacy)**: `src/components/tldraw/shapes/data-grid-shape.tsx`
- **Hybrid drag**: `src/components/tldraw/shapes/data-grid-shape.tsx:366-594`

### Architecture Documentation
- **Deep dive**: `assets/documents/AG_GRID_THEMING_ARCHITECTURE.md`

---

## Pattern 1: Tmnl.DataGrid — COMPOUND COMPONENT API

**When:** Building any data grid in TMNL.

The modern API uses compound components for declarative composition.

```tsx
import { Tmnl } from '@/lib/data-grid'
import { tmnlDenseDark } from '@/lib/data-grid/variants/tmnl-dense-dark'

<Tmnl.DataGrid
  id="emitters"
  variant={tmnlDenseDark}
  rowData={data}
  columnDefs={columnDefs}
>
  <Tmnl.DataGrid.Header>
    <Tmnl.DataGrid.Title title="EMITTERS" badge={data.length} />
    <Tmnl.DataGrid.SettingsButton onClick={openSettings} />
  </Tmnl.DataGrid.Header>

  <Tmnl.DataGrid.Body />

  <Tmnl.DataGrid.StatusBar>
    <span className="text-cyan-500">V2</span>
    <span>{data.length} rows</span>
  </Tmnl.DataGrid.StatusBar>

  <Tmnl.DataGrid.CornerDecorations />
</Tmnl.DataGrid>
```

### Child Components

| Component | Purpose | Props |
|-----------|---------|-------|
| `Header` | Container for title/controls | children |
| `Title` | Grid title with optional badge | title, badge? |
| `SettingsButton` | Settings action button | onClick |
| `Body` | The actual AG-Grid | (none - uses context) |
| `StatusBar` | Footer status area | children |
| `CornerDecorations` | Visual corner accents | variant? |

### Per-Grid Runtime Isolation

Each `<Tmnl.DataGrid>` creates its own Effect runtime with isolated services:

```typescript
// Inside Tmnl.DataGrid provider
const runtime = useMemo(() => createDataGridRuntime(), [gridId])

// Child components access via context
const ctx = useDataGridContext()
const variant = ctx.variant      // Reactive variant
const gridApi = ctx.gridApi      // Reactive grid API
```

**Canonical source**: `src/lib/data-grid/components/UnifiedDataGrid.tsx`

---

## Pattern 2: GridVariant System — VARIANT-DRIVEN THEMING

**When:** Customizing grid appearance, density, or behavior.

Variants are **not just themes**. They encode:
- **Density** — Row height, font size, padding
- **Colors** — Background, text, signals, flash
- **Behavior** — Selection, sorting, drag, resize
- **Typography** — Font family, letter spacing, weight

### Variant Structure

```typescript
export const tmnlDenseDark: GridVariant = {
  id: 'tmnl-dense-dark',
  densityTier: 'dense',
  density: DENSITY_PRESETS.dense,
  colorScheme: 'dark',

  colors: {
    background: { base: '#000000', alternateRow: '#0a0a0a', header: '#0d0d0d' },
    text: { primary: '#ffffff', secondary: '#a3a3a3', muted: '#525252' },
    signal: { positive: '#22c55e', negative: '#ef4444', accent: '#00ffcc' },
    border: { primary: '#262626', muted: '#1a1a1a' },
    flash: {
      up: 'rgba(34, 197, 94, 0.4)',
      down: 'rgba(239, 68, 68, 0.4)',
      durationMs: 1500,
    },
  },

  behavior: BEHAVIOR_PRESETS.interactive,

  typography: {
    fontFamily: "'JetBrains Mono', monospace",
    headerLetterSpacing: '0.05em',
  },

  intentOverrides: {
    // Per-column styling rules
  },
}
```

### Density Presets

| Preset | Row Height | Font Size | Padding |
|--------|------------|-----------|---------|
| `dense` | 20px | 10px | 4px |
| `compact` | 24px | 11px | 6px |
| `normal` | 32px | 13px | 8px |
| `comfortable` | 40px | 14px | 12px |

### Behavior Presets

| Preset | Selection | Sorting | Drag | Resize |
|--------|-----------|---------|------|--------|
| `readonly` | none | true | false | false |
| `interactive` | single | true | true | true |
| `editable` | multiple | true | true | true |
| `minimal` | none | false | false | false |

### Variant → Theme Conversion

```typescript
import { composeAgGridTheme } from '@/lib/data-grid/composer/theme-composer'

const agTheme = composeAgGridTheme(tmnlDenseDark)
// Returns AG-Grid themeQuartz.withParams({...})
```

**Canonical source**: `src/lib/data-grid/variants/tmnl-dense-dark.ts`

---

## Pattern 3: Flash System — CELL CHANGE HIGHLIGHTING

**When:** Showing real-time data updates with visual feedback.

### Severity Mapping

| Delta | Severity | Visual Effect |
|-------|----------|---------------|
| 0 | none | No flash |
| 1-5 | low | Subtle background |
| 6-10 | medium | Visible pulse |
| 11-15 | high | Strong glow |
| 16+ | critical | Full glow + pulse |

### Flash State Structure

```typescript
interface FlashState {
  severity: 'none' | 'low' | 'medium' | 'high' | 'critical'
  intensity: number      // 0-1, logarithmic scale
  direction: 'up' | 'down' | 'neutral'
  delta: number
  timestamp: number
  isActive: boolean
}
```

### useFlashTracker Hook

```typescript
import { useFlashTracker } from '@/lib/data-grid/flash'

const { getFlashState, hasFlash, processUpdates, injectKeyframes } = useFlashTracker({
  maxDelta: 20,
  flashExpirationMs: 1500,
})

// Initialize (once)
useEffect(() => injectKeyframes(), [])

// Process row updates
useEffect(() => {
  processUpdates(newData, oldData, 'value')
}, [newData])

// In cell renderer
const flash = getFlashState(rowId, field)
const styles = generateFlashStyles(flash, { colors: variant.colors.flash })
```

### Flash in Cell Renderer

```tsx
function ValueCellRenderer(params: ICellRendererParams) {
  const ctx = useDataGridContext()
  const { getFlashState } = ctx.flash

  const flash = getFlashState(params.node.id, params.colDef.field)

  return (
    <div
      className={flash.isActive ? `flash-${flash.severity}` : ''}
      style={{
        backgroundColor: flash.isActive
          ? flash.direction === 'up'
            ? ctx.variant.colors.flash.up
            : ctx.variant.colors.flash.down
          : undefined,
      }}
    >
      {params.value}
    </div>
  )
}
```

**Canonical source**: `src/lib/data-grid/flash/index.ts`

---

## Pattern 4: DataGridContext — PER-GRID SERVICES

**When:** Child components need access to grid state, variant, or API.

### Context Shape

```typescript
interface DataGridContextValue<TData = unknown> {
  gridId: string
  runtime: DataGridRuntime           // Per-grid Effect services
  variant: GridVariantType           // Reactive variant
  rowData: TData[]
  columnDefs: ColDef<TData>[]
  getRowId?: GetRowIdFunc<TData>
  gridApi: GridApi | null            // AG-Grid API reference
  setGridApi: (api: GridApi | null) => void
  flash: FlashTrackerAPI
}
```

### Usage in Components

```typescript
// Required context (throws if missing)
const ctx = useDataGridContext()

// Optional context (returns null if outside grid)
const ctx = useDataGridContextMaybe()
```

### Color Extraction from Context

```typescript
function StatusCellRenderer(params: ICellRendererParams) {
  const ctx = useDataGridContextMaybe()

  // Variant colors with fallback
  const colors = ctx?.variant.colors ?? {
    signal: { positive: '#22c55e', negative: '#ef4444' }
  }

  return (
    <span style={{ color: colors.signal.positive }}>
      {params.value}
    </span>
  )
}
```

**Canonical source**: `src/lib/data-grid/components/DataGridContext.tsx`

---

## Pattern 5: Context-Aware Cell Renderers

**When:** Renderers need variant colors or grid services.

### Pattern: Fallback for Standalone Usage

```typescript
import { useDataGridContextMaybe } from '@/lib/data-grid'
import { COLORS } from '@/lib/tokens'

export function ValueCellRenderer(params: ValueCellRendererParams) {
  const ctx = useDataGridContextMaybe()

  // Colors from variant OR token fallback
  const textColor = ctx?.variant.colors.text.primary ?? COLORS.textPrimary
  const accentColor = ctx?.variant.colors.signal.accent ?? COLORS.accentCyan

  return (
    <div style={{ color: textColor }}>
      <span>{params.value}</span>
      <div
        style={{
          backgroundColor: accentColor,
          width: `${params.data.percentage}%`,
        }}
      />
    </div>
  )
}
```

### Pattern: Flash-Aware Renderer

```typescript
export function FlashValueRenderer(params: ICellRendererParams) {
  const ctx = useDataGridContext()
  const flash = ctx.flash.getFlashState(params.node.id, params.colDef.field!)

  return (
    <div
      className={cn(
        'transition-all duration-300',
        flash.isActive && `flash-${flash.severity}`,
        flash.direction === 'up' && 'text-green-400',
        flash.direction === 'down' && 'text-red-400',
      )}
    >
      {params.value}
    </div>
  )
}
```

**Canonical source**: `src/lib/data-grid/renderers/ValueCellRenderer.tsx`

---

## Pattern 6: Hybrid Drag System — GRID-TO-CANVAS

**When:** Dragging rows from AG-Grid onto a tldraw canvas.

### Drag Phase Transitions

```
┌─────────────────────────────────┐
│   AG-Grid Internal Drag         │
│   (rowDragManaged=true)         │
└──────────────┬──────────────────┘
               │ onRowDragMove
               ▼
        Check: outside grid bounds?
               │
        ┌──────┴──────┐
       NO            YES
        │             │
     Continue    Create ghost
     in grid     shape on canvas
        │             │
        │      onPointerMove
        │      updateGhost()
        │             │
        └─────┬───────┘
              │ onPointerUp
        spawnDataCard()
        Remove ghost
```

### Drag State Schema

```typescript
interface DragState {
  isDragging: boolean
  isOutsideGrid: boolean    // Key flag for phase transition
  rowData: DataGridRow | null
  ghostId: string | null    // tldraw shape ID
}
```

### Phase Handlers

```typescript
const onRowDragMove = useCallback((event: RowDragMoveEvent) => {
  const { clientX, clientY } = event.event
  const gridRect = gridRef.current?.getBoundingClientRect()

  const isOutside = !gridRect ||
    clientX < gridRect.left || clientX > gridRect.right ||
    clientY < gridRect.top || clientY > gridRect.bottom

  if (isOutside && !dragState.isOutsideGrid) {
    // Transition: GridInternal → CanvasTracking
    const ghostId = createGhostShape(dragState.rowData, { x: clientX, y: clientY })
    setDragState(prev => ({ ...prev, isOutsideGrid: true, ghostId }))
  } else if (!isOutside && dragState.isOutsideGrid) {
    // Transition: CanvasTracking → GridInternal
    removeGhostShape(dragState.ghostId)
    setDragState(prev => ({ ...prev, isOutsideGrid: false, ghostId: null }))
  }
}, [dragState, createGhostShape, removeGhostShape])
```

### Effect Service for Drag

```typescript
export interface GridDragServiceApi {
  readonly getState: Effect.Effect<DragState>
  readonly dispatch: (event: GridDragEvent) => Effect.Effect<void>
  readonly subscribe: (handler: (state: DragState) => void) => Effect.Effect<() => void>
  readonly isDragging: Effect.Effect<boolean>
  readonly getPhase: Effect.Effect<DragPhase>
}
```

**Canonical source**: `src/lib/data-grid/services/GridDragService.ts`

---

## Pattern 7: Theme Composition via composeAgGridTheme

**When:** Converting a GridVariant to an AG-Grid theme.

```typescript
import { themeQuartz } from 'ag-grid-community'

export function composeAgGridTheme(variant: GridVariant) {
  const { colors, density, typography } = variant

  return themeQuartz.withParams({
    // Core colors
    backgroundColor: colors.background.base,
    foregroundColor: colors.text.primary,
    accentColor: colors.signal.accent,

    // Header
    headerBackgroundColor: colors.background.header,
    headerTextColor: colors.text.secondary,

    // Rows
    oddRowBackgroundColor: colors.background.alternateRow,
    rowHoverColor: `${colors.background.base}cc`,
    selectedRowBackgroundColor: `${colors.signal.accent}15`,

    // Typography
    fontFamily: typography.fontFamily,
    fontSize: density.fontSize,
    headerFontSize: density.fontSizeXs,

    // Density-driven spacing
    rowHeight: density.rowHeight,
    headerHeight: density.headerHeight,
    cellHorizontalPaddingScale: density.paddingX / 8,

    // Borders
    borderColor: colors.border.primary,
    wrapperBorderRadius: 0,
  })
}
```

**Canonical source**: `src/lib/data-grid/composer/theme-composer.ts`

---

## Pattern 8: Color Extraction Helpers

**When:** Extracting semantic colors from variant for custom UI.

```typescript
export function extractStatusColors(variant: GridVariant) {
  return {
    active: variant.colors.signal.positive,
    pending: variant.colors.signal.warning ?? variant.colors.signal.accent,
    inactive: variant.colors.signal.neutral ?? variant.colors.text.muted,
    error: variant.colors.signal.negative,
    default: variant.colors.text.muted,
  } as const
}

export function extractFlashConfig(variant: GridVariant) {
  const flash = variant.colors.flash
  return {
    enabled: variant.behavior.microInteractions?.enableCellFlash ?? true,
    upColor: flash.up,
    downColor: flash.down,
    durationMs: flash.durationMs,
  }
}
```

---

## Pattern 9: Legacy Basic Patterns

### Theme Creation via themeQuartz (Direct)

```typescript
import { themeQuartz } from 'ag-grid-community'
import { TMNL_TOKENS } from './data-grid-theme'

export const tmnlDataGridTheme = themeQuartz.withParams({
  backgroundColor: TMNL_TOKENS.colors.background,
  foregroundColor: TMNL_TOKENS.colors.text.primary,
  borderColor: TMNL_TOKENS.colors.border,
  headerBackgroundColor: TMNL_TOKENS.colors.surface,
  // ... etc
})
```

### Basic Cell Renderer (Non-Context)

```typescript
const IdCellRenderer = (params: ICellRendererParams) => (
  <span
    style={{
      color: TMNL_TOKENS.colors.text.muted,
      fontSize: TMNL_TOKENS.typography.sizes.xs,
      fontFamily: TMNL_TOKENS.typography.fontFamily,
      letterSpacing: '0.05em',
    }}
  >
    {params.value}
  </span>
)
```

### Column Definitions

```typescript
const columnDefs: ColDef[] = [
  {
    field: 'id',
    headerName: 'ID',
    width: 80,
    cellRenderer: IdCellRenderer,
    sortable: true,
  },
  {
    field: 'value',
    headerName: 'Value',
    width: 120,
    cellRenderer: ValueCellRenderer,
    comparator: (a, b) => a - b,
  },
]
```

---

## Anti-Patterns (BANNED)

### 1. Importing CSS Files

```typescript
// BANNED - No CSS imports with v34
import 'ag-grid-community/styles/ag-grid.css'
import 'ag-grid-community/styles/ag-theme-quartz.css'
// Use theme prop instead
```

### 2. Missing Module Registration

```typescript
// BANNED - Grid will render blank
<AgGridReact rowData={data} columnDefs={cols} />
// Must register modules FIRST
```

### 3. useState for Grid Data

```typescript
// BANNED when data crosses boundaries
const [rowData, setRowData] = useState([])
// Use Atom.make + service methods instead
```

### 4. Direct Theme Customization

```typescript
// BANNED - Bypasses variant system
const theme = themeQuartz.withParams({ backgroundColor: '#123' })
// Use GridVariant + composeAgGridTheme() instead
```

### 5. Cell Renderer Without Context Fallback

```typescript
// BANNED - Breaks outside grid context
function BadRenderer(params) {
  const ctx = useDataGridContext()  // Throws if no context!
  return <span style={{ color: ctx.variant.colors.text.primary }}>...</span>
}

// CORRECT - Graceful fallback
function GoodRenderer(params) {
  const ctx = useDataGridContextMaybe()
  const color = ctx?.variant.colors.text.primary ?? COLORS.textPrimary
  return <span style={{ color }}>...</span>
}
```

### 6. Creating Atoms Inside Components

```typescript
// BANNED - Recreates on every render
function BadGrid() {
  const rowDataAtom = Atom.make([])  // BAD!
  return <AgGridReact ... />
}

// CORRECT - Module-level atoms
const rowDataAtom = Atom.make<RowData[]>([])
function GoodGrid() {
  const rowData = useAtomValue(rowDataAtom)
  return <AgGridReact rowData={rowData} ... />
}
```

---

## Decision Tree: Which API to Use

```
Building a data grid?
│
├─ Simple, one-off grid?
│  └─ Use: Direct AgGridReact with composeAgGridTheme()
│
├─ Grid with header, status bar, controls?
│  └─ Use: Tmnl.DataGrid compound component
│
├─ Grid in tldraw shape?
│  └─ Use: V2 pattern (data-grid-shape-v2.tsx)
│
├─ Need real-time flash updates?
│  └─ Use: useFlashTracker + FlashValueRenderer
│
└─ Need custom variant?
   └─ Clone tmnlDenseDark and modify
```

---

## File Locations Summary

| Component | File | Purpose |
|-----------|------|---------|
| **Tmnl.DataGrid** | `src/lib/data-grid/components/UnifiedDataGrid.tsx` | Compound component |
| **DataGridContext** | `src/lib/data-grid/components/DataGridContext.tsx` | Per-grid context |
| **composeAgGridTheme** | `src/lib/data-grid/composer/theme-composer.ts` | Variant → theme |
| **Flash system** | `src/lib/data-grid/flash/index.ts` | Cell highlighting |
| **ValueCellRenderer** | `src/lib/data-grid/renderers/ValueCellRenderer.tsx` | Context-aware |
| **tmnlDenseDark** | `src/lib/data-grid/variants/tmnl-dense-dark.ts` | Canonical variant |
| **V2 tldraw shape** | `src/components/tldraw/shapes/data-grid-shape-v2.tsx` | Modern integration |
| **Hybrid drag** | `src/components/tldraw/shapes/data-grid-shape.tsx:366-594` | Grid-to-canvas |

---

## Integration Points

- **effect-atom-integration** — Atom-as-State for rowData
- **tmnl-design-tokens** — Token fallbacks in renderers
- **common-conventions** — Barrel exports, naming patterns
- **effect-patterns** — Effect.Service for GridDragService

