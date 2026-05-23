---
name: render-optimization
description: React render performance patterns including React Compiler integration, memoization strategies, TanStack Virtual, and DevTools profiling. Use when debugging slow renders, optimizing large lists, or reducing unnecessary re-renders.
context: fork
agent: frontend-ui-developer
version: 1.0.0
tags: [react, performance, optimization, react-compiler, virtualization, memo, profiler]
user-invocable: false
---

# React Render Optimization

Modern render performance patterns for React 19+.

## When to Use

- Debugging slow or janky UI
- Rendering large lists (100+ items)
- Reducing unnecessary re-renders
- Migrating to React Compiler

## Decision Tree: React Compiler First (2026)

```
Is React Compiler enabled?
├─ YES → Let compiler handle memoization automatically
│        Only use useMemo/useCallback as escape hatches
│        DevTools shows "Memo ✨" badge
│
└─ NO → Profile first, then optimize
         1. React DevTools Profiler
         2. Identify actual bottlenecks
         3. Apply targeted optimizations
```

## React Compiler (Primary Approach)

React 19's compiler automatically memoizes:
- Component re-renders
- Intermediate values (like useMemo)
- Callback references (like useCallback)
- JSX elements

```tsx
// next.config.js (Next.js 16+)
const nextConfig = {
  reactCompiler: true,
}

// Expo SDK 54+ enables by default
```

**Verification**: Open React DevTools → Look for "Memo ✨" badge

## When Manual Memoization Still Needed

Use `useMemo`/`useCallback` as escape hatches when:

```tsx
// 1. Effect dependencies that shouldn't trigger re-runs
const stableConfig = useMemo(() => ({
  apiUrl: process.env.API_URL
}), [])

useEffect(() => {
  initializeSDK(stableConfig)
}, [stableConfig])

// 2. Third-party libraries without compiler support
const memoizedValue = useMemo(() =>
  expensiveThirdPartyComputation(data), [data])

// 3. Precise control over memoization boundaries
const handleClick = useCallback(() => {
  // Critical callback that must be stable
}, [dependency])
```

## Virtualization Thresholds

| Item Count | Recommendation |
|------------|----------------|
| < 100 | Regular rendering usually fine |
| 100-500 | Consider virtualization |
| 500+ | Virtualization required |

```tsx
import { useVirtualizer } from '@tanstack/react-virtual'

const virtualizer = useVirtualizer({
  count: items.length,
  getScrollElement: () => parentRef.current,
  estimateSize: () => 50,
  overscan: 5,
})
```

## State Colocation

Move state as close to where it's used as possible:

```tsx
// ❌ State too high - causes unnecessary re-renders
function App() {
  const [filter, setFilter] = useState('')
  return (
    <Header />  {/* Re-renders on filter change! */}
    <FilterInput value={filter} onChange={setFilter} />
    <List filter={filter} />
  )
}

// ✅ State colocated - minimal re-renders
function App() {
  return (
    <Header />
    <FilterableList />  {/* State inside */}
  )
}
```

## Profiling Workflow

1. **React DevTools Profiler**: Record, interact, analyze
2. **Identify**: Components with high render counts or duration
3. **Verify**: Is the re-render actually causing perf issues?
4. **Fix**: Apply targeted optimization
5. **Measure**: Confirm improvement

## Quick Wins

1. **Key prop**: Stable, unique keys for lists
2. **Lazy loading**: `React.lazy()` for code splitting
3. **Debounce**: Input handlers with `useDeferredValue`
4. **Suspense**: Streaming with proper boundaries

## Key Decisions

| Decision | Recommendation |
|----------|----------------|
| Memoization | Let React Compiler handle it (2026 default) |
| Lists 100+ items | Use TanStack Virtual |
| State placement | Colocate as close to usage as possible |
| Profiling | Always measure before optimizing |

## Related Skills

- `react-server-components-framework` - Server-first rendering
- `vite-advanced` - Build optimization
- `e2e-testing` - Performance testing with Playwright

## References

- [React Compiler Migration](references/react-compiler-migration.md) - Compiler adoption
- [Memoization Escape Hatches](references/memoization-escape-hatches.md) - When useMemo needed
- [TanStack Virtual](references/tanstack-virtual-patterns.md) - Virtualization
- [State Colocation](references/state-colocation.md) - State placement
- [DevTools Profiler](references/devtools-profiler-workflow.md) - Finding bottlenecks
