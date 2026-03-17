---
name: zustand-state
description: Zustand state management for React and vanilla JavaScript. Use when creating stores, using selectors, persisting state to localStorage, integrating devtools, or managing global state without Redux complexity. Triggers on zustand, create(), createStore, useStore, persist, devtools, immer middleware.
---

# Zustand State Management

Minimal state management - no providers, minimal boilerplate.

## Quick Reference

```typescript
import { create } from 'zustand'

interface BearState {
  bears: number
  increase: (by: number) => void
}

const useBearStore = create<BearState>()((set) => ({
  bears: 0,
  increase: (by) => set((state) => ({ bears: state.bears + by })),
}))

// In component - select only what you need
const bears = useBearStore((state) => state.bears)
const increase = useBearStore((state) => state.increase)
```

## State Updates

```typescript
// Flat updates (auto-merged at one level)
set({ bears: 5 })
set((state) => ({ bears: state.bears + 1 }))

// Nested objects (manual spread required)
set((state) => ({
  nested: { ...state.nested, count: state.nested.count + 1 }
}))

// Replace entire state (no merge)
set({ bears: 0 }, true)
```

## Selectors & Performance

```typescript
// Good - subscribes only to bears
const bears = useBearStore((state) => state.bears)

// Bad - rerenders on any change
const state = useBearStore()

// Multiple values with useShallow (prevents rerenders with shallow comparison)
import { useShallow } from 'zustand/react/shallow'

const { bears, fish } = useBearStore(
  useShallow((state) => ({ bears: state.bears, fish: state.fish }))
)

// Array destructuring also works
const [bears, fish] = useBearStore(
  useShallow((state) => [state.bears, state.fish])
)
```

## Access Outside Components

```typescript
// Get current state (non-reactive)
const state = useBearStore.getState()

// Update state
useBearStore.setState({ bears: 5 })

// Subscribe to changes
const unsub = useBearStore.subscribe((state) => console.log(state))
unsub() // unsubscribe
```

## Vanilla Store (No React)

```typescript
import { createStore } from 'zustand/vanilla'

const store = createStore((set) => ({
  bears: 0,
  increase: (by) => set((state) => ({ bears: state.bears + by })),
}))

store.getState().bears
store.setState({ bears: 10 })
store.subscribe((state) => console.log(state))
```

## Additional Documentation

- **Middleware**: See [references/middleware.md](references/middleware.md) for persist, devtools, immer
- **Patterns**: See [references/patterns.md](references/patterns.md) for slices, testing, best practices
- **TypeScript**: See [references/typescript.md](references/typescript.md) for advanced typing patterns

## Key Patterns

| Pattern | When to Use |
|---------|-------------|
| Single selector | One piece of state needed |
| `useShallow` | Multiple values, avoid rerenders |
| `getState()` | Outside React, event handlers |
| `subscribe()` | External systems, logging |
| Vanilla store | Non-React environments |
