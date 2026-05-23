---
name: react-performance-patterns
description: React performance optimization patterns for TMNL. Covers useMemo, useCallback, React.memo, virtualization, and when optimization matters vs premature optimization. Use for performance-critical components.
model_invoked: true
triggers:
  - "useMemo"
  - "useCallback"
  - "React.memo"
  - "performance"
  - "optimization"
  - "virtualization"
  - "memoization"
---

# React Performance Patterns for TMNL

## Overview

React performance optimization is about **preventing unnecessary work**. In TMNL, we optimize selectively: virtualize large lists, memoize expensive computations, and stabilize function references—but only when profiling shows a problem.

**Key Insight**: Premature optimization is waste. Profile first, optimize second.

## Canonical Sources

### TMNL Implementations

- **useSlider** — `/src/lib/slider/v1/hooks/useSlider.ts` (strategic memoization)
  - `useMemo` for stable atom reference (once per component)
  - `useCallback` for event handlers passed as props
  - Derived values memoized with `useMemo`

- **useDataManager** — `/src/lib/data-manager/v1/hooks/useDataManager.ts` (atom subscriptions)
  - `useCallback` for wrapped operations
  - Atom subscriptions auto-memoize (no manual memo needed)

- **DataGrid** — `/src/components/data-grid/DataGrid.tsx` (AG-Grid integration)
  - AG-Grid handles virtualization internally
  - No React.memo needed (AG-Grid's own rendering)

### Reference Documentation

- [React Performance Optimization](https://react.dev/learn/render-and-commit#optimizing-performance)
- [When to useMemo and useCallback](https://kentcdodds.com/blog/usememo-and-usecallback)
- [AG-Grid Performance](https://www.ag-grid.com/react-data-grid/performance/)

## Pattern Variants

### Pattern 1: useMemo for Expensive Computations

Use when:
- Computation is expensive (>5ms)
- Result is used in render
- Dependencies change infrequently

```tsx
import { useMemo } from 'react'

function DataProcessor({ data }: { data: DataPoint[] }) {
  // ✅ GOOD - Expensive computation
  const processedData = useMemo(() => {
    return data
      .filter((d) => d.value > 0)
      .map((d) => ({ ...d, normalized: d.value / maxValue }))
      .sort((a, b) => b.normalized - a.normalized)
  }, [data, maxValue])

  return <Chart data={processedData} />
}
```

**When to skip**:
```tsx
// ❌ NOT NEEDED - Simple computation
const doubled = useMemo(() => value * 2, [value])

// ✅ BETTER - Just compute directly
const doubled = value * 2
```

**Canonical source**: `src/lib/slider/v1/hooks/useSlider.ts:155-170`

### Pattern 2: useCallback for Stable Function References

Use when:
- Function is passed as prop to memoized child
- Function is a dependency in useEffect/useMemo/useCallback
- Function is used in external library hooks

```tsx
import { useCallback } from 'react'

function SearchBox({ onSearch }: { onSearch: (query: string) => void }) {
  // ✅ GOOD - Stable reference for prop
  const handleKeyDown = useCallback((e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      onSearch(e.currentTarget.value)
    }
  }, [onSearch])

  return <input onKeyDown={handleKeyDown} />
}
```

**When to skip**:
```tsx
// ❌ NOT NEEDED - Function not passed as prop
const Component = () => {
  const handleClick = useCallback(() => {
    console.log('clicked')
  }, [])

  // Only used internally, no memo needed
  return <button onClick={handleClick}>Click</button>
}

// ✅ BETTER - Just define inline
const Component = () => {
  return <button onClick={() => console.log('clicked')}>Click</button>
}
```

**Canonical source**: `src/lib/slider/v1/hooks/useSlider.ts:185-240`

### Pattern 3: React.memo for Component Memoization

Use when:
- Component renders frequently with same props
- Props are primitives or stable references
- Render is expensive (>16ms)

```tsx
import { memo } from 'react'

interface ResultItemProps {
  id: string
  title: string
  score: number
}

// ✅ GOOD - Expensive component, stable props
const ResultItem = memo(({ id, title, score }: ResultItemProps) => {
  return (
    <div className="result-item">
      <h3>{title}</h3>
      <span>{score.toFixed(2)}</span>
    </div>
  )
})

ResultItem.displayName = 'ResultItem'
```

**With custom comparison**:
```tsx
// ✅ GOOD - Custom comparison for complex props
const ExpensiveChart = memo(
  ({ data, config }: { data: DataPoint[]; config: ChartConfig }) => {
    // Expensive render
    return <Canvas data={data} config={config} />
  },
  (prev, next) => {
    // Only re-render if data length changed
    return prev.data.length === next.data.length
  }
)
```

**When to skip**:
```tsx
// ❌ NOT NEEDED - Simple component, changes frequently
const Counter = memo(({ count }: { count: number }) => {
  return <span>{count}</span>
})

// ✅ BETTER - No memo for trivial components
const Counter = ({ count }: { count: number }) => {
  return <span>{count}</span>
}
```

### Pattern 4: Atom-Based Fine-Grained Subscriptions

Use when:
- State updates frequently
- Only part of state affects component
- Multiple components subscribe to same state

```tsx
import { Atom } from '@effect-atom/atom-react'
import { useAtomValue } from '@effect-atom/atom-react'

// State atoms
const resultsAtom = Atom.make<SearchResult[]>([])
const statusAtom = Atom.make<'idle' | 'loading' | 'complete'>('idle')

// Derived atom (auto-memoized)
const resultCountAtom = Atom.make((get) => get(resultsAtom).length)

// ✅ GOOD - Fine-grained subscription
function ResultCount() {
  const count = useAtomValue(resultCountAtom)
  // Only re-renders when count changes, not when results array changes
  return <span>{count} results</span>
}

function ResultsList() {
  const results = useAtomValue(resultsAtom)
  // Only re-renders when results array changes
  return results.map((r) => <ResultItem key={r.id} result={r} />)
}
```

**Canonical source**: `src/lib/data-manager/v1/atoms/index.ts:82-104`

### Pattern 5: Virtualization for Large Lists

Use when:
- Rendering 100+ items
- Each item is a DOM node (not canvas/webgl)
- Scrollable container

```tsx
import { AgGridReact } from 'ag-grid-react'

// ✅ GOOD - AG-Grid handles virtualization
function DataGrid({ rowData }: { rowData: SearchResult[] }) {
  return (
    <AgGridReact
      rowData={rowData}
      rowHeight={40}
      // AG-Grid only renders visible rows
    />
  )
}
```

**Alternative with react-window**:
```tsx
import { FixedSizeList } from 'react-window'

// ✅ GOOD - react-window for custom lists
function VirtualList({ items }: { items: string[] }) {
  return (
    <FixedSizeList
      height={600}
      itemCount={items.length}
      itemSize={40}
      width="100%"
    >
      {({ index, style }) => (
        <div style={style}>{items[index]}</div>
      )}
    </FixedSizeList>
  )
}
```

**Canonical source**: `src/components/data-grid/DataGrid.tsx`

### Pattern 6: Stable References with useMemo

Use when:
- Creating objects/arrays passed as props to memoized children
- Object/array used as dependency in useEffect/useMemo/useCallback

```tsx
import { useMemo } from 'react'

function FilteredResults({ results, filter }: { results: Result[]; filter: Filter }) {
  // ✅ GOOD - Stable array reference
  const filteredResults = useMemo(() => {
    return results.filter((r) => r.category === filter.category)
  }, [results, filter.category])

  // ✅ GOOD - Stable config object
  const gridConfig = useMemo(() => ({
    rowHeight: 40,
    columnDefs: columnDefsFromFilter(filter),
  }), [filter])

  return <DataGrid data={filteredResults} config={gridConfig} />
}
```

**Canonical source**: `src/lib/slider/v1/hooks/useSlider.ts:100-120`

## Decision Tree

```
Performance issue?
│
├─ Profile first with React DevTools Profiler
│  │
│  ├─ Component re-renders unnecessarily?
│  │  │
│  │  ├─ Props are stable but component re-renders?
│  │  │  └─ Use: React.memo
│  │  │
│  │  └─ Props change but render is cheap?
│  │     └─ Skip optimization
│  │
│  ├─ Expensive computation on every render?
│  │  └─ Use: useMemo
│  │
│  ├─ Function reference instability causing issues?
│  │  └─ Use: useCallback
│  │
│  ├─ Rendering 100+ list items?
│  │  └─ Use: Virtualization (AG-Grid or react-window)
│  │
│  └─ State updates trigger too many re-renders?
│     └─ Use: Fine-grained atom subscriptions
│
└─ No profile? No optimization.
```

## Examples

### Example 1: useSlider Memoization Strategy

Strategic memoization for complex hook.

```tsx
export function useSlider(options: UseSliderOptions = {}): UseSliderReturn {
  const { value, onChange, behavior = LinearBehavior.shape } = options

  // ✅ Stable atom reference (once per component)
  const stateAtom = useMemo(
    () => Atom.make<SliderState>(initialState),
    [] // Empty deps - create once
  )

  const state = Atom.get(stateAtom)

  // ✅ Memoize derived values
  const normalizedValue = useMemo(
    () => behavior.toNormalized(state.value),
    [state.value, behavior]
  )

  const displayValue = useMemo(
    () => behavior.format(state.value, config),
    [state.value, behavior, config]
  )

  // ✅ Stable handlers with useCallback
  const handlePointerDown = useCallback((e: React.PointerEvent) => {
    dispatch({ type: 'POINTER_DOWN', event: e })
  }, [dispatch])

  return {
    state,
    normalizedValue,
    displayValue,
    handlePointerDown,
  }
}
```

**Canonical source**: `src/lib/slider/v1/hooks/useSlider.ts:98-300`

### Example 2: DataManager Atom Subscriptions

Fine-grained subscriptions prevent unnecessary re-renders.

```tsx
// Atoms (auto-memoized)
export const resultsAtom = Atom.make<SearchResult[]>([])
export const statusAtom = Atom.make<StreamStatus>('idle')
export const resultCountAtom = Atom.make((get) => get(resultsAtom).length)

// Hook with stable operations
export function useDataManager<T>() {
  // Subscriptions (no memo needed - atoms handle it)
  const results = useAtomValue(resultsAtom) as readonly SearchResult<T>[]
  const status = useAtomValue(statusAtom)
  const resultCount = useAtomValue(resultCountAtom)

  // ✅ Stable operation references
  const search = useCallback(
    async (query: SearchQuery): Promise<readonly SearchResult<T>[]> => {
      return await doSearch(query)
    },
    [doSearch]
  )

  return { results, status, resultCount, search }
}
```

**Canonical source**: `src/lib/data-manager/v1/hooks/useDataManager.ts:98-174`

### Example 3: DataGrid with Virtualization

AG-Grid handles virtualization internally.

```tsx
function SearchResultsGrid() {
  const { results } = useDataManager<MovieItem>()

  // ✅ AG-Grid virtualizes automatically
  return (
    <AgGridReact
      rowData={results}
      rowHeight={40}
      // Only visible rows rendered
      // No manual virtualization needed
    />
  )
}
```

**Canonical source**: `src/components/testbed/DataManagerTestbed.tsx:680-750`

## Anti-Patterns (BANNED)

### Premature Optimization

```tsx
// ❌ BANNED - No profiling, just cargo-cult memoization
const Component = () => {
  const data = useMemo(() => props.data, [props.data])
  const handleClick = useCallback(() => {}, [])
  const result = useMemo(() => value * 2, [value])

  return <div onClick={handleClick}>{result}</div>
}

// ✅ CORRECT - Profile first, optimize if needed
const Component = () => {
  const result = props.data.value * 2
  return <div onClick={() => {}}>{result}</div>
}
```

### useMemo for Simple Values

```tsx
// ❌ BANNED - Memoization overhead > computation cost
const doubled = useMemo(() => value * 2, [value])
const greeting = useMemo(() => `Hello, ${name}`, [name])

// ✅ CORRECT - Just compute directly
const doubled = value * 2
const greeting = `Hello, ${name}`
```

### useCallback for Internal Functions

```tsx
// ❌ BANNED - Function only used internally
const Component = () => {
  const handleClick = useCallback(() => {
    console.log('clicked')
  }, [])

  return <button onClick={handleClick}>Click</button>
}

// ✅ CORRECT - No callback needed
const Component = () => {
  return <button onClick={() => console.log('clicked')}>Click</button>
}
```

### React.memo Everywhere

```tsx
// ❌ BANNED - Memoizing everything
const Button = memo(({ onClick, label }) => (
  <button onClick={onClick}>{label}</button>
))

const Icon = memo(({ name }) => <span>{name}</span>)

const Text = memo(({ children }) => <span>{children}</span>)

// ✅ CORRECT - Only memoize expensive components
const ExpensiveChart = memo(({ data }) => {
  // Complex rendering logic
  return <Canvas data={data} />
})

const Button = ({ onClick, label }) => (
  <button onClick={onClick}>{label}</button>
)
```

### Unstable Dependencies in useMemo/useCallback

```tsx
// ❌ BANNED - Recreates on every render
const memoized = useMemo(() => {
  return data.filter((d) => d.value > threshold)
}, [data, { threshold }]) // ← Object recreated each render!

// ✅ CORRECT - Stable dependencies
const memoized = useMemo(() => {
  return data.filter((d) => d.value > threshold)
}, [data, threshold]) // ← Primitive value
```

## When to Optimize

### Profile BEFORE Optimizing

Use React DevTools Profiler:

1. **Record a session** — Interact with component
2. **Check flamegraph** — Identify slow renders
3. **Measure render time** — Is it >16ms (60fps)?
4. **Count renders** — Does component render unnecessarily?
5. **Optimize** — Apply patterns from this skill
6. **Re-profile** — Verify improvement

### Optimization Thresholds

| Metric | Threshold | Action |
|--------|-----------|--------|
| Render time | >16ms | Consider memoization |
| Render time | >50ms | Definitely optimize |
| Re-render count | >10/sec | Check atom subscriptions |
| List length | >100 items | Use virtualization |
| Computation time | >5ms | Use useMemo |

## Implementation Checklist

When optimizing performance:

- [ ] **Profile first** — Use React DevTools Profiler
- [ ] **Identify bottleneck** — Slow renders or unnecessary re-renders?
- [ ] **Choose pattern** — useMemo, useCallback, React.memo, virtualization?
- [ ] **Apply optimization** — Minimal change to fix bottleneck
- [ ] **Re-profile** — Verify improvement
- [ ] **Document** — Add comment explaining why optimization was needed
- [ ] **Avoid premature** — Don't optimize without profiling

## Optimization Priority

1. **Virtualize long lists** — Biggest impact for least effort
2. **Fine-grained atom subscriptions** — Prevent cascading re-renders
3. **Memoize expensive computations** — Only if >5ms
4. **Stabilize function references** — Only if causing issues
5. **React.memo components** — Last resort, high maintenance

## Related Patterns

- **react-state-migration** — Atoms enable fine-grained subscriptions
- **react-hook-composition** — Hooks use useMemo/useCallback strategically
- **effect-patterns** — Atom-as-State prevents Effect.Ref overhead

## Filing New Patterns

When you discover a new performance pattern:

1. Profile before/after with React DevTools
2. Document performance gains (render time, re-render count)
3. Update this skill with canonical source references
4. Add to testbed with performance metrics
