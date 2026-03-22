---
name: web-state-jotai
description: Atomic state management with auto-dependency tracking
---

# Jotai Atomic State Management

> **Quick Guide:** Jotai provides atomic, bottom-up state management with automatic dependency tracking. Define atoms at module level (never inside components). Use primitive atoms for values, derived atoms for computed state, write-only atoms for actions, and async atoms with Suspense for loading. Components only re-render when their specific atoms change. The `atomFamily` utility is deprecated -- use the `jotai-family` package for new code.

---

<critical_requirements>

## CRITICAL: Before Using Jotai

**(You MUST define atoms OUTSIDE components -- creating atoms inside render causes broken state)**

**(You MUST wrap async atom consumers in Suspense boundaries -- async atoms trigger Suspense by default)**

**(You MUST use write atoms (action atoms) to encapsulate multi-atom updates and post-async state changes)**

**(You MUST use `jotai-family` package instead of deprecated `atomFamily` from `jotai/utils` for new code)**

</critical_requirements>

---

**Auto-detection:** Jotai, jotai, atom, useAtom, useAtomValue, useSetAtom, atomWithStorage, atomFamily, splitAtom, selectAtom, derived atom, loadable, unwrap, createStore, Provider store

**When to use:**

- Fine-grained reactivity without manual memoization
- Bottom-up state composition with automatic dependency tracking
- Async state with React Suspense integration
- Computed/derived state that auto-updates when dependencies change
- Avoiding prop drilling for shared UI state

**Key patterns covered:**

- Primitive, derived, write-only, and read-write atoms
- Async atoms with Suspense and loadable/unwrap utilities
- atomWithStorage for persistence
- splitAtom for array item isolation
- Store and Provider patterns for isolation and testing

**When NOT to use:**

- Server/API data (use your data fetching solution)
- Simple local component state (use useState)
- State that should be in URL (use searchParams)

---

<philosophy>

## Philosophy

Jotai takes an **atomic, bottom-up approach** to state management. The core principle: **"Anything that can be derived from the application state should be derived automatically."**

Consider atoms like cells in a spreadsheet:

- Each atom is an independent cell holding a value
- Derived atoms are formulas that reference other cells
- When a cell changes, only formulas depending on it recalculate
- This provides the minimum necessary work automatically

**Key characteristics:**

- **Bottom-up state design**: Build state from small, composable atoms
- **Automatic dependency tracking**: Atoms automatically update when dependencies change
- **Fine-grained reactivity**: Components only re-render when their specific atoms change
- **First-class async support**: Async operations integrate seamlessly with React Suspense

**Mental Model:**
Instead of one large store, you have many small atoms that can be combined. This creates natural code splitting and enables precise re-render optimization without manual memoization.

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Primitive Atoms

The simplest atom type -- holds a single value with automatic type inference. Always define at module level.

```typescript
import { atom } from "jotai";

const INITIAL_COUNT = 0;
const countAtom = atom(INITIAL_COUNT);
const userAtom = atom<User | null>(null);

export { countAtom, userAtom };
```

**Why good:** Module-level definition persists state, type inference works automatically, explicit typing only for unions/nullable

See [examples/core.md](examples/core.md) Pattern 1 for complete examples with type patterns.

---

### Pattern 2: Derived (Read-Only) Atoms

Compute values from other atoms -- dependencies tracked automatically, cached until dependencies change.

```typescript
const subtotalAtom = atom((get) => get(priceAtom) * get(quantityAtom));
const taxAtom = atom((get) => get(subtotalAtom) * get(taxRateAtom));
const totalAtom = atom((get) => get(subtotalAtom) + get(taxAtom));
```

**Why good:** Automatic dependency tracking, cached computation, chain of derivations is composable

See [examples/core.md](examples/core.md) Pattern 2 for derived atom chains and conditional derivations.

---

### Pattern 3: Write-Only Atoms (Action Atoms)

Encapsulate side effects and multi-atom updates. First argument is `null` (no read value).

```typescript
const resetAllAtom = atom(null, (get, set) => {
  set(countAtom, 0);
  set(itemsAtom, []);
  set(selectedAtom, null);
});
```

**Why good:** Actions are reusable, enables code splitting, multiple atoms updated atomically

See [examples/core.md](examples/core.md) Pattern 3 for action atoms with arguments.

---

### Pattern 4: Read-Write Atoms

Atoms that can both read derived state and accept writes. Useful for lens-like property access on larger objects.

```typescript
const nameAtom = atom(
  (get) => get(userAtom).name,
  (get, set, newName: string) => {
    set(userAtom, { ...get(userAtom), name: newName });
  },
);
```

**Why good:** Granular read/write access to object properties, keeps parent intact

See [examples/core.md](examples/core.md) Pattern 4 for lens patterns and transformations.

---

### Pattern 5: Async Atoms with Suspense

Async atoms trigger Suspense by default. Use `loadable()` for manual loading states or `unwrap()` for fallback values.

```typescript
// Triggers Suspense -- wrap consumer in <Suspense>
const userAtom = atom(async (get) => {
  const id = get(userIdAtom);
  const response = await fetch(`/api/users/${id}`);
  return response.json() as Promise<User>;
});

// Non-Suspense alternative
const loadableUserAtom = loadable(userAtom);
// Returns { state: 'loading' } | { state: 'hasData', data } | { state: 'hasError', error }
```

**Why good:** First-class Suspense integration, loadable provides type-safe discriminated union

See [examples/async.md](examples/async.md) for Suspense setup, loadable/unwrap patterns, and AbortController support.

---

### Pattern 6: atomWithStorage for Persistence

Persist atom values to localStorage, sessionStorage, or custom storage. Use `RESET` symbol to restore defaults.

```typescript
import { atomWithStorage, RESET } from "jotai/utils";

const STORAGE_KEY = "app-theme";
const themeAtom = atomWithStorage<Theme>(STORAGE_KEY, "light");
// setTheme(RESET) restores to "light"
```

**Gotcha:** Default behavior renders initial value first, then stored value (flicker). Set `{ getOnInit: true }` for immediate stored value, but beware SSR hydration issues.

See [examples/persistence.md](examples/persistence.md) Pattern 1 for storage variants and reset patterns.

---

### Pattern 7: splitAtom for Array Optimization

Split an array atom into individual item atoms. Each item gets its own atom -- updating one item only re-renders that item's component.

```typescript
import { splitAtom } from "jotai/utils";

const todosAtom = atom<Todo[]>([]);
const todoAtomsAtom = splitAtom(todosAtom, (todo) => todo.id);
// keyExtractor prevents unnecessary atom recreation on reorder
```

**Why good:** Per-item re-render isolation, dispatch for add/remove/move operations

See [examples/persistence.md](examples/persistence.md) Pattern 3 for list rendering with dispatch.

---

### Pattern 8: Store and Provider Patterns

Custom stores enable state access outside React, test isolation, and multi-store architectures.

```typescript
import { createStore, Provider } from "jotai";

const store = createStore();
store.set(countAtom, 10); // Access outside React
store.sub(countAtom, () => { /* react to changes */ });

// Provider with store for isolation
<Provider store={store}><App /></Provider>
```

**Gotcha:** Each Provider creates isolated state. Atoms in different Providers do not share values unless given the same store instance.

See [examples/testing.md](examples/testing.md) for store, provider, and test isolation patterns.

</patterns>

---

**Detailed Resources:**

- [examples/core.md](examples/core.md) -- Primitive, derived, write-only, and read-write atom patterns
- [examples/async.md](examples/async.md) -- Async atoms, Suspense, loadable, unwrap, atomFamily
- [examples/persistence.md](examples/persistence.md) -- atomWithStorage, selectAtom, splitAtom
- [examples/testing.md](examples/testing.md) -- Store, provider, reset, and test isolation patterns
- [reference.md](reference.md) -- Decision frameworks, red flags, anti-patterns

---

<red_flags>

## RED FLAGS

**High Priority Issues:**

- Creating atoms inside components -- causes new atom every render, state never persists
- Missing Suspense boundary for async atoms -- crashes app with React error
- Using deprecated `atomFamily` from `jotai/utils` -- will be removed in v3, use `jotai-family` package
- Grouping unrelated state in one atom -- defeats the purpose of atomic state, causes unnecessary re-renders

**Medium Priority Issues:**

- Using `selectAtom` as a primary pattern -- official docs call it an "escape hatch", prefer derived atoms
- Not using `keyExtractor` with `splitAtom` for items with IDs -- causes unnecessary atom recreation
- Missing Provider isolation in tests -- state bleeds between tests
- Using `atomFamily` without memory cleanup -- `remove()` or `setShouldRemove()` required to prevent leaks

**Gotchas & Edge Cases:**

- Async atoms suspend by default -- this is intentional, not a bug
- Provider creates isolated state -- atoms in different Providers don't share values
- `loadable()` returns discriminated union -- always check `state` property first
- `RESET` symbol is special -- pass to setter to reset `atomWithStorage` to initial value
- Default store is global -- provider-less mode shares state across entire app
- `atomWithStorage` default renders initial value first, then stored value (flicker)
- `getOnInit: true` avoids flicker but may cause SSR hydration mismatches

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

**(You MUST define atoms OUTSIDE components -- creating atoms inside render causes broken state)**

**(You MUST wrap async atom consumers in Suspense boundaries -- async atoms trigger Suspense by default)**

**(You MUST use write atoms (action atoms) to encapsulate multi-atom updates and post-async state changes)**

**(You MUST use `jotai-family` package instead of deprecated `atomFamily` from `jotai/utils` for new code)**

**Failure to follow these rules will cause state corruption, Suspense errors, and deprecated API usage.**

</critical_reminders>
