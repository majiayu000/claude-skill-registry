---
name: react-hook-composition
description: Custom hook patterns for TMNL. Covers hook composition, useDebugValue, atom subscriptions, and registry patterns. Use for building reusable hook APIs like useSlider, useDataManager.
model_invoked: true
triggers:
  - "custom hook"
  - "useSlider"
  - "useDataManager"
  - "hook composition"
  - "useAtomValue"
  - "useDebugValue"
---

# React Hook Composition for TMNL

## Overview

Custom hooks encapsulate stateful logic, effects, and event handlers into reusable functions. In TMNL, hooks bridge Effect services (via effect-atom) with React components, providing ergonomic interfaces for complex systems.

**Key Insight**: Hooks compose behavior, not UI. They return data and operations, letting components decide presentation.

## Canonical Sources

### TMNL Implementations

- **useSlider** — `/src/lib/slider/v1/hooks/useSlider.ts` (comprehensive hook interface)
  - Local atom state via `Atom.make()`
  - Event dispatch with reducer pattern
  - Derived values via `useMemo`
  - Handler composition with `useCallback`

- **useDataManager** — `/src/lib/data-manager/v1/hooks/useDataManager.ts` (Effect service integration)
  - Atom subscriptions via `useAtomValue`
  - Operation setters via `useAtomSet`
  - Derived atoms for computed state
  - Promise-based operations

- **useVariable** — `/src/lib/variables/hooks/useVariable.ts` (registry pattern)
  - Service-scoped state management
  - Type-safe variable access
  - Reactive updates via atoms

- **useDrawer** — `/src/lib/drawer/hooks/useDrawer.ts` (UI state hook)
  - Atom-based drawer state
  - Imperative open/close API
  - Content registration

### Reference Documentation

- [React Hooks API Reference](https://react.dev/reference/react)
- [effect-atom Hooks](https://github.com/tim-smart/effect-atom#react-bindings)

## Pattern Variants

### Pattern 1: Atom Subscription Hook

Use when consuming reactive state from effect-atom atoms.

```tsx
import { useAtomValue, useAtomSet } from '@effect-atom/atom-react'
import { useCallback } from 'react'
import { resultsAtom, searchOps } from '../atoms'
import type { SearchQuery, SearchResult } from '../types'

// ─────────────────────────────────────────────────────────────────────────
// Hook Interface
// ─────────────────────────────────────────────────────────────────────────

export interface UseDataManagerResult<T = unknown> {
  // State (from atoms)
  readonly results: readonly SearchResult<T>[]
  readonly isSearching: boolean
  readonly hasResults: boolean

  // Operations
  readonly search: (query: SearchQuery) => Promise<readonly SearchResult<T>[]>
}

// ─────────────────────────────────────────────────────────────────────────
// Hook Implementation
// ─────────────────────────────────────────────────────────────────────────

export function useDataManager<T = unknown>(): UseDataManagerResult<T> {
  // Atom subscriptions (plain atoms return values directly)
  const results = useAtomValue(resultsAtom) as readonly SearchResult<T>[]
  const isSearching = useAtomValue(isSearchingAtom)
  const hasResults = useAtomValue(hasResultsAtom)

  // Operation setters (fn atoms return promises)
  const doSearch = useAtomSet(searchOps.search, { mode: 'promise' })

  // Wrapped operations
  const search = useCallback(
    async (query: SearchQuery): Promise<readonly SearchResult<T>[]> => {
      const result = await doSearch(query)
      return result as readonly SearchResult<T>[]
    },
    [doSearch]
  )

  return {
    results,
    isSearching,
    hasResults,
    search,
  }
}
```

**Canonical source**: `src/lib/data-manager/v1/hooks/useDataManager.ts:98-174`

**Key patterns**:
- `useAtomValue` for reactive state subscriptions
- `useAtomSet` for mutation operations
- `useCallback` to stabilize function references
- Type generics for consumer-provided types

### Pattern 2: Local State Hook with Reducer

Use when managing complex local state with dispatched events.

```tsx
import { useCallback, useMemo, useRef } from 'react'
import { Atom } from '@effect-atom/atom-react'
import type { SliderState, SliderEvent, SliderBehaviorShape } from '../types'
import { sliderReducer } from '../atoms'
import { LinearBehavior } from '../services/SliderBehavior'

// ─────────────────────────────────────────────────────────────────────────
// Hook Interface
// ─────────────────────────────────────────────────────────────────────────

export interface UseSliderOptions {
  value?: number
  onChange?: (value: number) => void
  behavior?: SliderBehaviorShape
  debug?: boolean
}

export interface UseSliderReturn {
  // State
  state: SliderState
  value: number
  normalizedValue: number

  // Event handlers
  dispatch: (event: SliderEvent) => void
  handlePointerDown: (e: React.PointerEvent) => void
  handleKeyDown: (e: React.KeyboardEvent) => void

  // Ref for container
  containerRef: React.RefObject<HTMLDivElement>
}

// ─────────────────────────────────────────────────────────────────────────
// Hook Implementation
// ─────────────────────────────────────────────────────────────────────────

export function useSlider(options: UseSliderOptions = {}): UseSliderReturn {
  const {
    value: initialValue = 0,
    onChange,
    behavior = LinearBehavior.shape,
    debug = false,
  } = options

  // Local atom for state
  const stateAtom = useMemo(
    () => Atom.make<SliderState>({
      value: initialValue,
      isDragging: false,
      isFocused: false,
      isEditing: false,
      activeSensitivity: 1.0,
      activeModifiers: [],
    }),
    []
  )

  const state = Atom.get(stateAtom)

  // Dispatch function
  const dispatch = useCallback((event: SliderEvent) => {
    const newState = sliderReducer(Atom.get(stateAtom), event, behavior)
    Atom.set(stateAtom, newState)

    // Fire onChange if value changed
    if (newState.value !== Atom.get(stateAtom).value && onChange) {
      onChange(newState.value)
    }
  }, [stateAtom, onChange, behavior])

  // Derived values
  const normalizedValue = useMemo(
    () => behavior.toNormalized(state.value),
    [state.value, behavior]
  )

  // Event handlers
  const containerRef = useRef<HTMLDivElement>(null)

  const handlePointerDown = useCallback((e: React.PointerEvent) => {
    dispatch({ type: 'POINTER_DOWN', event: e })
  }, [dispatch])

  const handleKeyDown = useCallback((e: React.KeyboardEvent) => {
    dispatch({ type: 'KEY_DOWN', event: e })
  }, [dispatch])

  return {
    state,
    value: state.value,
    normalizedValue,
    dispatch,
    handlePointerDown,
    handleKeyDown,
    containerRef,
  }
}
```

**Canonical source**: `src/lib/slider/v1/hooks/useSlider.ts:98-300`

**Key patterns**:
- `useMemo` to create stable atom reference (once per component)
- `Atom.make()` for local reactive state
- `useCallback` for stable event handlers
- `useRef` for DOM node access

### Pattern 3: Derived State Hook

Use when exposing computed values from atoms.

```tsx
import { useAtomValue } from '@effect-atom/atom-react'
import { useMemo } from 'react'
import { resultsAtom, statusAtom } from '../atoms'

export function useSearchMetrics() {
  const results = useAtomValue(resultsAtom)
  const status = useAtomValue(statusAtom)

  // Derived values
  const resultCount = useMemo(() => results.length, [results])
  const hasResults = useMemo(() => resultCount > 0, [resultCount])
  const isSearching = useMemo(() => status === 'streaming', [status])

  return {
    resultCount,
    hasResults,
    isSearching,
  }
}
```

**Key patterns**:
- `useMemo` for derived computations
- Multiple atom subscriptions
- Pure computation, no side effects

### Pattern 4: Hook with useDebugValue

Use when debugging complex hook state.

```tsx
import { useAtomValue } from '@effect-atom/atom-react'
import { useDebugValue } from 'react'
import { stateAtom } from '../atoms'

export function useSliderDebug() {
  const state = useAtomValue(stateAtom)

  // Show in React DevTools
  useDebugValue(
    state,
    (s) => `value: ${s.value}, dragging: ${s.isDragging}`
  )

  return state
}
```

**Key patterns**:
- `useDebugValue` for DevTools visibility
- Optional formatter function for readable labels

### Pattern 5: Registry Pattern Hook

Use when accessing service-scoped registries.

```tsx
import { useAtomValue, useAtomSet } from '@effect-atom/atom-react'
import { useCallback } from 'react'
import { variablesAtom, registerOps } from '../atoms'
import type { Variable } from '../types'

export function useVariableRegistry() {
  const variables = useAtomValue(variablesAtom)
  const doRegister = useAtomSet(registerOps.register)

  const register = useCallback(
    (variable: Variable) => {
      doRegister(variable)
    },
    [doRegister]
  )

  const get = useCallback(
    (id: string) => variables.find((v) => v.id === id),
    [variables]
  )

  return {
    variables,
    register,
    get,
  }
}
```

**Canonical source**: `src/lib/variables/hooks/useVariable.ts`

**Key patterns**:
- Registry lookup via `find()`
- Imperative register API
- Service-scoped state

## Decision Tree

```
Need reusable stateful logic?
│
├─ Consuming Effect service atoms?
│  └─ Use: Atom Subscription Hook
│     (e.g., useDataManager with useAtomValue)
│
├─ Complex local state with events?
│  └─ Use: Local State Hook with Reducer
│     (e.g., useSlider with Atom.make + dispatch)
│
├─ Computed values from multiple atoms?
│  └─ Use: Derived State Hook
│     (e.g., useSearchMetrics with useMemo)
│
└─ Accessing a registry or collection?
   └─ Use: Registry Pattern Hook
      (e.g., useVariableRegistry)
```

## Examples

### Example 1: useSlider Full Interface

Comprehensive hook with state, events, derived values, and handlers.

```tsx
function SliderComponent({ value, onChange }: { value: number; onChange: (v: number) => void }) {
  const {
    state,
    normalizedValue,
    displayValue,
    handlePointerDown,
    handlePointerMove,
    handlePointerUp,
    handleKeyDown,
    handleWheel,
    handleDoubleClick,
    containerRef,
  } = useSlider({
    value,
    onChange,
    behavior: DecibelBehavior.shape,
    debug: true,
  })

  return (
    <div
      ref={containerRef}
      onPointerDown={handlePointerDown}
      onPointerMove={handlePointerMove}
      onPointerUp={handlePointerUp}
      onKeyDown={handleKeyDown}
      onWheel={handleWheel}
      onDoubleClick={handleDoubleClick}
    >
      <div style={{ width: `${normalizedValue * 100}%` }} />
      <span>{displayValue}</span>
    </div>
  )
}
```

**Canonical source**: `src/lib/slider/v1/hooks/useSlider.ts:50-92`

### Example 2: useDataManager with Progressive Results

Hook that subscribes to streaming search results.

```tsx
function SearchUI() {
  const {
    results,
    isSearching,
    hasResults,
    resultCount,
    search,
    indexData,
  } = useDataManager<MovieItem>()

  useEffect(() => {
    indexData(movies, { fields: ['title', 'cast', 'genres'] })
  }, [movies, indexData])

  const handleSearch = async (query: string) => {
    await search({ query, limit: 100 })
  }

  return (
    <div>
      {isSearching && <Spinner />}
      <div>Results: {resultCount}</div>
      {results.map((r) => (
        <Result key={r.item.id} result={r} />
      ))}
    </div>
  )
}
```

**Canonical source**: `src/components/testbed/DataManagerTestbed.tsx:536-638`

## Anti-Patterns (BANNED)

### useState for Cross-Component State

```tsx
// BANNED - Use atoms for shared state
function useSharedData() {
  const [data, setData] = useState([])
  // Other components can't access this!
  return { data, setData }
}

// CORRECT - Use atoms
const dataAtom = Atom.make([])

function useSharedData() {
  const data = useAtomValue(dataAtom)
  const setData = useCallback((newData) => {
    Atom.set(dataAtom, newData)
  }, [])
  return { data, setData }
}
```

### Returning JSX from Hooks

```tsx
// BANNED - Hooks return data, not UI
function useCard() {
  return <Card>Content</Card>
}

// CORRECT - Return data and operations
function useCard() {
  const [isOpen, setIsOpen] = useState(false)
  return { isOpen, setIsOpen }
}
```

### Unstable Function References

```tsx
// BANNED - Creates new function on every render
function useSearch() {
  const search = (query: string) => { /* ... */ }
  return { search }
}

// CORRECT - Stable with useCallback
function useSearch() {
  const search = useCallback((query: string) => { /* ... */ }, [])
  return { search }
}
```

### Conditional Hook Calls

```tsx
// BANNED - Violates Rules of Hooks
function useData(shouldFetch: boolean) {
  if (shouldFetch) {
    const data = useAtomValue(dataAtom) // ← WRONG!
  }
}

// CORRECT - Always call hooks
function useData(shouldFetch: boolean) {
  const data = useAtomValue(dataAtom)
  return shouldFetch ? data : null
}
```

## Implementation Checklist

When creating a custom hook:

- [ ] **Name**: Prefix with `use` (e.g., `useSlider`)
- [ ] **Interface**: Define `UseXOptions` and `UseXReturn` types
- [ ] **Atoms**: Use `useAtomValue` for subscriptions, `useAtomSet` for operations
- [ ] **Callbacks**: Wrap handlers with `useCallback`
- [ ] **Memoization**: Use `useMemo` for derived values
- [ ] **Refs**: Use `useRef` for DOM nodes or mutable values
- [ ] **Debug**: Add `useDebugValue` for complex hooks
- [ ] **TypeScript**: Export hook interface types
- [ ] **Documentation**: Add JSDoc with usage example

## Composition Patterns

### Composing Multiple Hooks

```tsx
function useSearchWithMetrics() {
  const { search, results } = useDataManager()
  const { resultCount, hasResults } = useSearchMetrics()
  const { logEvent } = useAnalytics()

  const searchWithLogging = useCallback(async (query: string) => {
    logEvent('search_started', { query })
    const results = await search({ query, limit: 100 })
    logEvent('search_completed', { resultCount: results.length })
    return results
  }, [search, logEvent])

  return {
    search: searchWithLogging,
    results,
    resultCount,
    hasResults,
  }
}
```

### Hook Factories

```tsx
function createUseSlider(defaultBehavior: SliderBehaviorShape) {
  return function useSliderWithDefaults(options: UseSliderOptions = {}) {
    return useSlider({
      ...options,
      behavior: options.behavior ?? defaultBehavior,
    })
  }
}

const useDecibelSlider = createUseSlider(DecibelBehavior.shape)
const useLinearSlider = createUseSlider(LinearBehavior.shape)
```

## Related Patterns

- **effect-patterns** — Hooks consume Effect services via atoms
- **react-state-migration** — Migrate useState to atoms consumed by hooks
- **react-compound-components** — Hooks often power compound component context

## Filing New Patterns

When you discover a new hook pattern:

1. Implement in `src/lib/<domain>/hooks/` with full TypeScript types
2. Add usage example in testbed
3. Update this skill with canonical source references
4. Document atom subscriptions and service integrations
