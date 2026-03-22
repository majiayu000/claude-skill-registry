---
name: hooks-mastery
description: >
  Advanced React hooks patterns including custom hooks, memoization, refs, reducers, and
  external store synchronization. Use when the user is writing custom hooks, optimizing
  React performance with useCallback/useMemo, managing complex state with useReducer,
  or integrating external state stores. Trigger on any mention of React hooks, custom hooks,
  memoization, re-render optimization, or rules of hooks violations.
---

# React Hooks Mastery

Patterns for writing correct, performant, and composable React hooks.

## When to Use
- User is creating custom hooks
- User asks about useCallback, useMemo, or performance optimization
- User has complex state logic that needs useReducer
- User is integrating an external store (Redux, Zustand, vanilla)
- User encounters stale closure bugs or rules of hooks violations

## Core Patterns

### Custom Hooks -- Extracting Reusable Logic

Custom hooks encapsulate stateful logic for reuse across components. Name them with the `use` prefix.

```tsx
import { useState, useEffect, useRef } from 'react'

function useFetch<T>(url: string) {
  const [data, setData] = useState<T | null>(null)
  const [error, setError] = useState<Error | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    const controller = new AbortController()
    setIsLoading(true)
    setError(null)

    fetch(url, { signal: controller.signal })
      .then((res) => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`)
        return res.json()
      })
      .then((json) => setData(json as T))
      .catch((err) => {
        if (err.name !== 'AbortError') setError(err)
      })
      .finally(() => setIsLoading(false))

    return () => controller.abort()
  }, [url])

  return { data, error, isLoading }
}
```

### useCallback and useMemo -- When to Memoize

Memoize only when passing callbacks to memoized children or when computation is expensive. Do not memoize everything by default.

```tsx
import { useCallback, useMemo } from 'react'

function ProductList({ products, onSelect }: Props) {
  // Memoize because this is passed to React.memo children
  const handleSelect = useCallback(
    (id: string) => {
      onSelect(id)
    },
    [onSelect]
  )

  // Memoize because sorting is O(n log n)
  const sorted = useMemo(
    () => [...products].sort((a, b) => a.price - b.price),
    [products]
  )

  return (
    <ul>
      {sorted.map((p) => (
        <ProductItem key={p.id} product={p} onSelect={handleSelect} />
      ))}
    </ul>
  )
}

const ProductItem = React.memo(({ product, onSelect }: ItemProps) => (
  <li onClick={() => onSelect(product.id)}>{product.name}</li>
))
```

### useRef -- Mutable Values Without Re-renders

Use refs for values that should persist across renders without triggering re-renders: timers, previous values, DOM elements.

```tsx
function useInterval(callback: () => void, delay: number | null) {
  const savedCallback = useRef(callback)

  // Update ref on every render so the interval always calls the latest callback
  useEffect(() => {
    savedCallback.current = callback
  }, [callback])

  useEffect(() => {
    if (delay === null) return
    const id = setInterval(() => savedCallback.current(), delay)
    return () => clearInterval(id)
  }, [delay])
}

function usePrevious<T>(value: T): T | undefined {
  const ref = useRef<T | undefined>(undefined)
  useEffect(() => {
    ref.current = value
  })
  return ref.current
}
```

### useReducer -- Complex State Transitions

Prefer useReducer when state transitions depend on previous state or when multiple sub-values change together.

```tsx
import { useReducer } from 'react'

interface FormState {
  values: Record<string, string>
  errors: Record<string, string>
  isSubmitting: boolean
}

type FormAction =
  | { type: 'SET_FIELD'; field: string; value: string }
  | { type: 'SET_ERROR'; field: string; error: string }
  | { type: 'SUBMIT_START' }
  | { type: 'SUBMIT_SUCCESS' }
  | { type: 'SUBMIT_FAILURE'; errors: Record<string, string> }

function formReducer(state: FormState, action: FormAction): FormState {
  switch (action.type) {
    case 'SET_FIELD':
      return {
        ...state,
        values: { ...state.values, [action.field]: action.value },
        errors: { ...state.errors, [action.field]: '' },
      }
    case 'SET_ERROR':
      return { ...state, errors: { ...state.errors, [action.field]: action.error } }
    case 'SUBMIT_START':
      return { ...state, isSubmitting: true }
    case 'SUBMIT_SUCCESS':
      return { ...state, isSubmitting: false, errors: {} }
    case 'SUBMIT_FAILURE':
      return { ...state, isSubmitting: false, errors: action.errors }
  }
}

function useForm(initialValues: Record<string, string>) {
  const [state, dispatch] = useReducer(formReducer, {
    values: initialValues,
    errors: {},
    isSubmitting: false,
  })

  const setField = (field: string, value: string) =>
    dispatch({ type: 'SET_FIELD', field, value })

  const submit = async (handler: (values: Record<string, string>) => Promise<void>) => {
    dispatch({ type: 'SUBMIT_START' })
    try {
      await handler(state.values)
      dispatch({ type: 'SUBMIT_SUCCESS' })
    } catch (err) {
      dispatch({ type: 'SUBMIT_FAILURE', errors: { form: String(err) } })
    }
  }

  return { ...state, setField, submit }
}
```

### useSyncExternalStore -- Subscribing to External State

The correct way to subscribe React to any external mutable store (vanilla stores, browser APIs, third-party state).

```tsx
import { useSyncExternalStore } from 'react'

function createStore<T>(initialState: T) {
  let state = initialState
  const listeners = new Set<() => void>()

  return {
    getState: () => state,
    setState: (next: T | ((prev: T) => T)) => {
      state = typeof next === 'function' ? (next as (prev: T) => T)(state) : next
      listeners.forEach((listener) => listener())
    },
    subscribe: (listener: () => void) => {
      listeners.add(listener)
      return () => listeners.delete(listener)
    },
  }
}

const counterStore = createStore({ count: 0 })

function useCounter() {
  const state = useSyncExternalStore(
    counterStore.subscribe,
    counterStore.getState,
    counterStore.getState // server snapshot
  )
  return {
    count: state.count,
    increment: () => counterStore.setState((s) => ({ count: s.count + 1 })),
  }
}
```

## Anti-Patterns

- **Calling hooks conditionally** -- Hooks must be called in the same order every render. Never put hooks inside if/else, loops, or after early returns.
- **Missing dependencies in useEffect** -- Causes stale closures and subtle bugs. Always include all referenced values in the dependency array. Use the exhaustive-deps ESLint rule.
- **Memoizing everything** -- useCallback and useMemo have overhead. Only memoize when passing to React.memo children or for genuinely expensive computations.
- **Using useRef to avoid dependency arrays** -- This hides bugs. Fix the dependency array instead of working around it with refs (except for the interval/timer pattern).
- **Giant useEffect** -- An effect that does multiple unrelated things. Split into separate useEffect calls, each with its own dependencies.

## Quick Reference

| Hook | Purpose | Re-renders? |
|------|---------|-------------|
| useState | Simple state | Yes |
| useReducer | Complex state transitions | Yes |
| useRef | Mutable value, DOM refs | No |
| useMemo | Cache expensive computation | No (returns cached) |
| useCallback | Cache function reference | No (returns cached) |
| useEffect | Side effects after render | No (runs after) |
| useSyncExternalStore | Subscribe to external store | Yes (on store change) |

Rules of Hooks: (1) Only call at the top level. (2) Only call from React functions or custom hooks.
