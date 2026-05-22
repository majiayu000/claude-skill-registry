---
name: react-zustand-patterns
description: Zustand state management patterns for React. Use when working with Zustand stores, debugging state timing issues, or implementing async actions. Works for both React web and React Native.
---

# Zustand Patterns for React

## Problem Statement

Zustand's simplicity hides important timing details. `set()` is synchronous, but React re-renders are batched. `getState()` escapes stale closures. Async actions in stores need careful handling. Understanding these internals prevents subtle bugs.

---

## Pattern: set() is Synchronous, Renders are Batched

**Problem:** Assuming state is "ready" for React immediately after `set()`.

```typescript
const useStore = create((set, get) => ({
  count: 0,

  increment: () => {
    set({ count: get().count + 1 });
    // State IS updated here (set is sync)
    console.log(get().count); // ✅ Shows new value

    // But React hasn't re-rendered yet
    // Component will see old value until next render cycle
  },
}));
```

**Key insight:**
- `set()` updates the store synchronously
- `getState()` immediately reflects the new value
- React components re-render asynchronously (batched)

**When this matters:**
- Chaining multiple state updates
- Validating state after update
- Debugging "stale" component values

---

## Pattern: getState() Escapes Stale Closures

**Problem:** Callbacks and async functions capture state at creation time. Using `get()` or `getState()` always gets current state.

```typescript
const useStore = create((set, get) => ({
  data: {},

  // WRONG - closure captures stale state
  saveDataBad: (id: string, value: number) => {
    setTimeout(() => {
      // If someone passed `data` as a parameter, it would be stale
    }, 1000);
  },

  // CORRECT - always use get() for current state
  saveData: async (id: string, value: number) => {
    await someAsyncOperation();
    // After await, use get() to ensure current state
    const currentData = get().data;
    set({ data: { ...currentData, [id]: value } });
  },
}));

// In components - same principle
function Component() {
  const data = useStore((s) => s.data);

  const handleSave = async () => {
    await delay(1000);
    // data here is stale! Captured at render time

    // Use getState() for current value
    const current = useStore.getState().data;
  };
}
```

**Rule:** After any `await`, use `get()` or `getState()` - never rely on closure-captured values.

---

## Pattern: Async Actions in Stores

**Problem:** Async actions need explicit `async/await` and careful state reads after awaits.

```typescript
const useStore = create((set, get) => ({
  loading: false,
  data: null,
  error: null,

  // WRONG - no async keyword, race condition prone
  fetchDataBad: (id: string) => {
    set({ loading: true });
    api.fetch(id).then((data) => {
      set({ data, loading: false });
    });
    // Returns immediately, caller can't await
  },

  // CORRECT - proper async action
  fetchData: async (id: string) => {
    set({ loading: true, error: null });

    try {
      const data = await api.fetch(id);
      // Re-read state after await if needed
      if (get().loading) { // Check we're still in loading state
        set({ data, loading: false });
      }
    } catch (error) {
      set({ error: error.message, loading: false });
    }
  },
}));

// Caller can properly await
await useStore.getState().fetchData('123');
```

---

## Pattern: Selector Stability

**Problem:** Selectors that create new objects cause unnecessary re-renders.

```typescript
// WRONG - creates new object every render
const data = useStore((state) => ({
  name: state.name,
  count: state.count,
}));

// CORRECT - use multiple selectors
const name = useStore((state) => state.name);
const count = useStore((state) => state.count);

// OR - use shallow comparison (Zustand 4.x)
import { shallow } from 'zustand/shallow';

const { name, count } = useStore(
  (state) => ({ name: state.name, count: state.count }),
  shallow
);

// Zustand 5.x - use useShallow hook
import { useShallow } from 'zustand/react/shallow';

const { name, count } = useStore(
  useShallow((state) => ({ name: state.name, count: state.count }))
);
```

---

## Pattern: Derived State

**Problem:** Computing derived values in selectors vs storing them.

```typescript
const useStore = create((set, get) => ({
  items: [],

  // WRONG - storing derived state that can become stale
  totalItems: 0,
  updateTotalItems: () => {
    set({ totalItems: get().items.length });
  },
}));

// CORRECT - compute in selector (always fresh)
const totalItems = useStore((state) => state.items.length);

// For expensive computations, memoize outside the store
import { useMemo } from 'react';

function Component() {
  const items = useStore((state) => state.items);
  const expensiveResult = useMemo(() => {
    return computeExpensiveAnalysis(items);
  }, [items]);
}
```

---

## Pattern: Store Subscriptions for Side Effects

**Problem:** Need to react to state changes outside React components.

```typescript
// Subscribe to specific state changes
const unsubscribe = useStore.subscribe(
  (state) => state.data,
  (data, prevData) => {
    console.log('Data changed:', { prev: prevData, current: data });
    // Persist to storage, send analytics, etc.
  },
  { equalityFn: shallow }
);

// In Zustand 4.x with subscribeWithSelector middleware
import { subscribeWithSelector } from 'zustand/middleware';

const useStore = create(
  subscribeWithSelector((set, get) => ({
    data: {},
    // ...
  }))
);
```

---

## Pattern: Testing Zustand Stores

**Problem:** Tests need to reset store state and verify async flows.

```typescript
// Store with reset capability
const initialState = {
  data: {},
  loading: false,
};

const useStore = create((set, get) => ({
  ...initialState,

  // Actions...

  // Reset for testing
  _reset: () => set(initialState),
}));

// Test
describe('Data Store', () => {
  beforeEach(() => {
    useStore.getState()._reset();
  });

  it('fetches data correctly', async () => {
    const store = useStore.getState();

    await store.fetchData('123');

    expect(useStore.getState().data).toBeDefined();
    expect(useStore.getState().loading).toBe(false);
  });
});
```

---

## Pattern: Debugging State Changes

**Problem:** Tracking down when/where state changed unexpectedly.

```typescript
// Add logging middleware
import { devtools } from 'zustand/middleware';

const useStore = create(
  devtools(
    (set, get) => ({
      // ... your store
    }),
    { name: 'MyStore' }
  )
);

// Manual logging for specific debugging
const useStore = create((set, get) => ({
  data: {},

  saveData: (id: string, value: number) => {
    console.log('[saveData] Before:', {
      id,
      value,
      currentData: get().data,
    });

    set((state) => ({
      data: { ...state.data, [id]: value },
    }));

    console.log('[saveData] After:', {
      data: get().data,
    });
  },
}));
```

---

## Pattern: Persist Middleware

**Problem:** Persisting state across sessions.

```typescript
import { persist } from 'zustand/middleware';

// Web - localStorage
const useStore = create(
  persist(
    (set, get) => ({
      preferences: {},
      setPreference: (key, value) =>
        set((state) => ({
          preferences: { ...state.preferences, [key]: value }
        })),
    }),
    {
      name: 'app-preferences',
      // Optional: choose what to persist
      partialize: (state) => ({ preferences: state.preferences }),
    }
  )
);
```

---

## Common Pitfalls

| Pitfall | Solution |
|---------|----------|
| Stale closure after await | Use `get()` after every await |
| Selector returns new object | Use `shallow` or multiple selectors |
| Action not awaitable | Add `async` keyword, return promise |
| State seems stale in component | Component hasn't re-rendered yet - use `getState()` for immediate reads |
| Can't find when state changed | Add devtools middleware or manual logging |

---

## Zustand 5.x Migration Notes

If upgrading from 4.x:

```typescript
// 4.x - shallow from main package
import { shallow } from 'zustand/shallow';

// 5.x - useShallow hook for React
import { useShallow } from 'zustand/react/shallow';

// 4.x - type parameter often needed
const useStore = create<StoreType>()((set, get) => ({...}));

// 5.x - improved type inference
const useStore = create((set, get) => ({...}));
```
