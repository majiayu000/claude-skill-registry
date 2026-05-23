---
name: web-state-zustand
description: Zustand stores, client state patterns. Use when deciding between Zustand vs useState, managing global state, or avoiding Context misuse.
---

# Client State Management Patterns

> **Quick Guide:** Local UI state? useState. Shared UI (2+ components)? Zustand. Server data? Use your data fetching solution. URL-appropriate filters? searchParams. NEVER use Context for state management. Zustand v5: use `useShallow` from `zustand/react/shallow` (not the old equality-fn second arg), selectors must return stable references, and `persist` no longer stores initial state during creation.

**Detailed Resources:**

- [examples/core.md](examples/core.md) - Store setup, selectors, useShallow, Context anti-patterns, URL state

---

<critical_requirements>

## CRITICAL: Before Managing Client State

**(You MUST use a data fetching solution for ALL server/API data - NEVER useState, Zustand, or Context)**

**(You MUST use Zustand for ALL shared UI state (2+ components) - NOT Context or prop drilling)**

**(You MUST use useState ONLY for truly component-local state - NOT for anything shared)**

**(You MUST use atomic selectors or `useShallow` from `zustand/react/shallow` - NEVER destructure the entire store)**

**(You MUST ensure selectors return stable references - inline object/function creation causes infinite loops in v5)**

</critical_requirements>

---

**Auto-detection:** Zustand, zustand, create from zustand, useShallow, zustand/middleware, zustand store, client state, shared UI state, Context misuse, prop drilling, global state

**When to use:**

- Deciding between Zustand or useState for a use case
- Setting up Zustand for shared UI state (modals, sidebars, preferences)
- Understanding when NOT to use Context for state management
- Structuring stores: slices, actions, selectors

**Key patterns covered:**

- Client state = useState (local) or Zustand (shared, 2+ components)
- Context for dependency injection only (NEVER for state management)
- Store setup with devtools and persist middleware
- Selector patterns: atomic selectors vs useShallow
- URL params for shareable/bookmarkable state (filters, search)

**When NOT to use:**

- Server/API data (use a dedicated data fetching solution)
- State that should be shareable via URL (use searchParams)
- Any Context-based state management approach

---

<philosophy>

## Philosophy

Zustand is a minimal, hook-based state manager. The key principle: **use the right tool for the right job**. Server data belongs in a dedicated data fetching layer with caching and synchronization. Local UI state stays in useState. Shared UI state lives in Zustand for performance. URL state makes filters shareable. Context is ONLY for dependency injection, never state management.

**Store design principles** (from TkDodo and official docs):

- **Keep stores small** - multiple focused stores beat one monolithic store
- **Business logic in the store** - components call actions, stores decide what happens
- **Only export custom hooks** - never expose the raw store creator
- **Atomic selectors preferred** - return single values, not objects, for best performance

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: State Placement Decision

The most critical decision: where does this state belong?

```
Is it server data (from API)?
├─ YES → Data fetching solution (not this skill's scope)
└─ NO → Is it URL-appropriate (filters, search)?
    ├─ YES → URL params (searchParams)
    └─ NO → Is it needed in 2+ components?
        ├─ YES → Zustand
        └─ NO → Is it truly component-local?
            ├─ YES → useState
            └─ NO → Is it a singleton/dependency?
                └─ YES → Context (ONLY for DI, not state)
```

For full examples, see [examples/core.md](examples/core.md#pattern-1-state-placement).

---

### Pattern 2: Local State with useState

Use ONLY when state is truly component-local and never shared.

- State used ONLY in one component (isExpanded, isOpen)
- Temporary UI state that never needs to be shared
- As soon as a second component needs it, move to Zustand

For good/bad comparisons, see [examples/core.md](examples/core.md#pattern-2-local-state-with-usestate).

---

### Pattern 3: Zustand Store Setup

Use as soon as state is needed in 2+ components across the tree.

```typescript
// stores/ui-store.ts
import { create } from "zustand";
import { devtools, persist } from "zustand/middleware";

const UI_STORAGE_KEY = "ui-storage";

interface UIState {
  sidebarOpen: boolean;
  theme: "light" | "dark";
  toggleSidebar: () => void;
  setTheme: (theme: "light" | "dark") => void;
}

export const useUIStore = create<UIState>()(
  devtools(
    persist(
      (set) => ({
        sidebarOpen: true,
        theme: "light",
        toggleSidebar: () => set((s) => ({ sidebarOpen: !s.sidebarOpen })),
        setTheme: (theme) => set({ theme }),
      }),
      { name: UI_STORAGE_KEY, partialize: (s) => ({ theme: s.theme }) },
    ),
  ),
);
```

**Key points:** devtools for debugging, persist only what survives sessions (preferences, not transient UI), `partialize` to exclude ephemeral state.

For selectors, useShallow, and v5 stability patterns, see [examples/core.md](examples/core.md#pattern-3-zustand-store-setup).

---

### Pattern 4: Context API - Dependency Injection ONLY

Context is NOT a state management solution. It's for dependency injection and singletons ONLY.

**ONLY use Context for:**

- Framework providers (router, query client)
- Dependency injection (services, API clients, DB connections)
- Values set once at app initialization that never change

**NEVER use Context for:**

- ANY state management (use Zustand instead)
- ANY frequently updating values (every consumer re-renders on any change)

For why Context fails for state and acceptable DI usage, see [examples/core.md](examples/core.md#pattern-4-context-api---dependency-injection-only).

---

### Pattern 5: URL State for Shareable Filters

Use URL params (searchParams) for state that should be shareable, bookmarkable, or navigable.

- Filter selections, search queries, pagination, sort order
- Browser back/forward works correctly
- URLs can be shared with specific filter state

For implementation examples, see [examples/core.md](examples/core.md#pattern-5-url-state-for-shareable-filters).

</patterns>

---

<decision_framework>

## Decision Framework

### Quick Reference Table

| Use Case                        | Solution               | Why                                          |
| ------------------------------- | ---------------------- | -------------------------------------------- |
| Server/API data                 | Data fetching solution | Caching, synchronization, loading states     |
| Shareable filters               | URL params             | Bookmarkable, browser navigation             |
| Shared UI state (2+ components) | Zustand                | Fast, selective re-renders, no prop drilling |
| Local UI state (1 component)    | useState               | Simple, component-local                      |
| Framework providers / DI        | Context                | Singletons that never change                 |
| **ANY state management**        | **NEVER Context**      | **Causes full re-renders on any change**     |

</decision_framework>

---

<red_flags>

## RED FLAGS

**High Priority Issues:**

- **Storing server/API data in client state (useState, Context, Zustand)** - causes stale data, no caching, manual sync complexity
- **Using Context with useState/useReducer for state management** - every consumer re-renders on any change, performance nightmare
- **Destructuring the entire store** `const { x, y } = useStore()` - subscribes to all changes, defeats selective re-rendering
- **Using useState for state needed in 2+ components** - causes prop drilling, tight coupling, refactoring difficulty

**Medium Priority Issues:**

- Prop drilling 3+ levels instead of using Zustand
- Filter state in useState instead of URL params (not shareable/bookmarkable)
- Creating unnecessary object references in Zustand selectors (causes re-renders)
- One monolithic store instead of multiple focused stores

**Gotchas & Edge Cases:**

- Context re-renders ALL consumers when ANY value changes - no way to select specific values
- Zustand selectors that return new objects cause re-renders even if values are identical - use `useShallow` from `zustand/react/shallow` or atomic selectors
- URL params are always strings - need parsing for numbers/booleans
- Persisting modal/sidebar state across sessions confuses users - only persist preferences
- **Zustand v5:** Selectors must return stable references - returning new functions/objects inline causes infinite loops
- **Zustand v5:** The old `shallow` second argument to `create()` is removed - use `useShallow` hook wrapper or `createWithEqualityFn` from `zustand/traditional`
- **Zustand v5:** The persist middleware no longer stores initial state during creation - set computed/random initial values explicitly with `useStore.setState()`
- **Zustand v5:** Requires React 18+ and TypeScript 4.5+
- **Zustand v5:** `use-sync-external-store` is a peer dependency only when using `zustand/traditional`

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

**(You MUST use a data fetching solution for ALL server/API data - NEVER useState, Zustand, or Context)**

**(You MUST use Zustand for ALL shared UI state (2+ components) - NOT Context or prop drilling)**

**(You MUST use useState ONLY for truly component-local state - NOT for anything shared)**

**(You MUST use atomic selectors or `useShallow` from `zustand/react/shallow` - NEVER destructure the entire store)**

**(You MUST ensure selectors return stable references - inline object/function creation causes infinite loops in v5)**

**Failure to follow these rules will cause stale data issues, performance problems, and infinite render loops.**

</critical_reminders>
