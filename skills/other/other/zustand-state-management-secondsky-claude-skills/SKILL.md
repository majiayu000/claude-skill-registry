---
name: zustand-state-management
description: Zustand state management for React with TypeScript. Use for global state, Redux/Context API migration, localStorage persistence, slices pattern, devtools, Next.js SSR, or encountering hydration errors, TypeScript inference issues, persist middleware problems, infinite render loops.

  Keywords: zustand, state management, React state, TypeScript state, persist middleware,
  devtools, slices pattern, global state, React hooks, create store, useBoundStore,
  StateCreator, hydration error, text content mismatch, infinite render, localStorage,
  sessionStorage, immer middleware, shallow equality, selector pattern, zustand v5
license: MIT
---

# Zustand State Management

**Status**: Production Ready ✅
**Last Updated**: 2025-11-21
**Latest Version**: zustand@5.0.8
**Dependencies**: React 18+, TypeScript 5+

---

## Quick Start (3 Minutes)

### 1. Install Zustand

```bash
bun add zustand  # preferred
# or: npm install zustand
# or: yarn add zustand
```

**Why Zustand?**
- Minimal API: Only 1 function to learn (`create`)
- No boilerplate: No providers, reducers, or actions
- TypeScript-first: Excellent type inference
- Fast: Fine-grained subscriptions prevent unnecessary re-renders
- Flexible: Middleware for persistence, devtools, and more

### 2. Create Your First Store (TypeScript)

```typescript
import { create } from 'zustand'

interface BearStore {
  bears: number
  increase: (by: number) => void
  reset: () => void
}

const useBearStore = create<BearStore>()((set) => ({
  bears: 0,
  increase: (by) => set((state) => ({ bears: state.bears + by })),
  reset: () => set({ bears: 0 }),
}))
```

**CRITICAL**: Notice the **double parentheses** `create<T>()()` - this is required for TypeScript with middleware.

### 3. Use Store in Components

```tsx
import { useBearStore } from './store'

function BearCounter() {
  const bears = useBearStore((state) => state.bears)
  return <h1>{bears} around here...</h1>
}

function Controls() {
  const increase = useBearStore((state) => state.increase)
  return <button onClick={() => increase(1)}>Add bear</button>
}
```

**Why this works:**
- Components only re-render when their selected state changes
- No Context providers needed
- Selector function extracts specific state slice

---

## The 3-Pattern Setup Process

### Pattern 1: Basic Store (JavaScript)

For simple use cases without TypeScript:

```javascript
import { create } from 'zustand'

const useStore = create((set) => ({
  count: 0,
  increment: () => set((state) => ({ count: state.count + 1 })),
  decrement: () => set((state) => ({ count: state.count - 1 })),
}))
```

**When to use:**
- Prototyping
- Small apps
- No TypeScript in project

### Pattern 2: TypeScript Store (Recommended)

For production apps with type safety:

```typescript
import { create } from 'zustand'

// Define store interface
interface CounterStore {
  count: number
  increment: () => void
  decrement: () => void
}

// Create typed store
const useCounterStore = create<CounterStore>()((set) => ({
  count: 0,
  increment: () => set((state) => ({ count: state.count + 1 })),
  decrement: () => set((state) => ({ count: state.count - 1 })),
}))
```

**Key Points:**
- Separate interface for state + actions
- Use `create<T>()()` syntax (currying for middleware)
- Full IDE autocomplete and type checking

### Pattern 3: Persistent Store

For state that survives page reloads:

```typescript
import { create } from 'zustand'
import { persist, createJSONStorage } from 'zustand/middleware'

interface UserPreferences {
  theme: 'light' | 'dark' | 'system'
  language: string
  setTheme: (theme: UserPreferences['theme']) => void
  setLanguage: (language: string) => void
}

const usePreferencesStore = create<UserPreferences>()(
  persist(
    (set) => ({
      theme: 'system',
      language: 'en',
      setTheme: (theme) => set({ theme }),
      setLanguage: (language) => set({ language }),
    }),
    {
      name: 'user-preferences', // unique name in localStorage
      storage: createJSONStorage(() => localStorage), // optional: defaults to localStorage
    },
  ),
)
```

**Why this matters:**
- State automatically saved to localStorage
- Restored on page reload
- Works with sessionStorage too
- Handles serialization automatically

---

## Critical Rules

### Always Do

✅ Use `create<T>()()` (double parentheses) in TypeScript for middleware compatibility
✅ Define separate interfaces for state and actions
✅ Use selector functions to extract specific state slices
✅ Use `set` with updater functions for derived state: `set((state) => ({ count: state.count + 1 }))`
✅ Use unique names for persist middleware storage keys
✅ Handle Next.js hydration with `hasHydrated` flag pattern
✅ Use `shallow` for selecting multiple values
✅ Keep actions pure (no side effects except state updates)

### Never Do

❌ Use `create<T>(...)` (single parentheses) in TypeScript - breaks middleware types
❌ Mutate state directly: `set((state) => { state.count++; return state })` - use immutable updates
❌ Create new objects in selectors: `useStore((state) => ({ a: state.a }))` - causes infinite renders
❌ Use same storage name for multiple stores - causes data collisions
❌ Access localStorage during SSR without hydration check
❌ Use Zustand for server state - use TanStack Query instead
❌ Export store instance directly - always export the hook

---

## Known Issues Prevention (5 Issues)

| Issue | Error | Quick Fix |
|-------|-------|-----------|
| **#1 Hydration mismatch** | "Text content does not match" | Use `_hasHydrated` flag + `onRehydrateStorage` |
| **#2 TypeScript inference** | Types break with middleware | Use `create<T>()()` double parentheses |
| **#3 Import error** | "createJSONStorage not exported" | Upgrade to zustand@5.0.8+ |
| **#4 Infinite loop** | Browser freezes | Use `shallow` or separate selectors |
| **#5 Slices types** | StateCreator types fail | Explicit `StateCreator<Combined, [], [], Slice>` |

**Most Critical** - TypeScript double parentheses:
```typescript
// ❌ WRONG: create<T>((set) => ...)
// ✅ CORRECT: create<T>()((set) => ...)
```

**See**: `references/known-issues.md` for complete solutions with code examples.

---

## Middleware Configuration

```typescript
import { create } from 'zustand'
import { devtools, persist } from 'zustand/middleware'

const useStore = create<MyStore>()(
  devtools(
    persist(
      (set) => ({ /* store definition */ }),
      { name: 'my-storage' },
    ),
    { name: 'MyStore' },
  ),
)
```

| Middleware | Purpose | Import |
|------------|---------|--------|
| `persist` | localStorage/sessionStorage | `zustand/middleware` |
| `devtools` | Redux DevTools integration | `zustand/middleware` |
| `immer` | Mutable update syntax | `zustand/middleware/immer` |

**Order matters**: `devtools(persist(...))` shows persist actions in DevTools.

**See**: `references/middleware-guide.md` for complete middleware documentation.

---

## Common Patterns

| Pattern | Use Case | Key Technique |
|---------|----------|---------------|
| **Computed values** | Derived data | Compute in selector: `state.items.length` |
| **Async actions** | API calls | `set({ isLoading: true })` + try/catch |
| **Reset store** | Logout, form clear | `set(initialState)` |
| **Selector with params** | Dynamic access | `state.todos.find(t => t.id === id)` |
| **Multiple stores** | Separation of concerns | Create separate `create()` calls |

**See**: `references/common-patterns.md` for complete implementations.

---

## Advanced Topics

| Topic | Use Case | Key API |
|-------|----------|---------|
| **Vanilla store** | Non-React, testing | `createStore()` from `zustand/vanilla` |
| **Custom middleware** | Logging, timestamps | Wrap `StateCreator` |
| **Immer** | Mutable update syntax | `immer()` middleware |
| **Subscriptions** | Side effects | `store.subscribe()` |

**See**: `references/advanced-topics.md` for complete implementations.

---

## Bundled Resources

| Type | Files |
|------|-------|
| **Templates** | `basic-store.ts`, `typescript-store.ts`, `persist-store.ts`, `slices-pattern.ts`, `devtools-store.ts`, `nextjs-store.ts`, `computed-store.ts`, `async-actions-store.ts` |
| **References** | `middleware-guide.md`, `typescript-patterns.md`, `nextjs-hydration.md`, `migration-guide.md`, `known-issues.md`, `common-patterns.md`, `advanced-topics.md` |

---

## When to Load References

| Reference | Load When... |
|-----------|--------------|
| `known-issues.md` | Debugging hydration, TypeScript, infinite loop, or slices errors |
| `common-patterns.md` | Implementing computed values, async actions, reset patterns |
| `advanced-topics.md` | Vanilla stores, custom middleware, Immer, subscriptions |
| `middleware-guide.md` | Configuring persist, devtools, or combining middlewares |
| `typescript-patterns.md` | Complex type inference issues, StateCreator problems |
| `nextjs-hydration.md` | Next.js SSR/hydration problems |
| `migration-guide.md` | Migrating from Redux, Context API, or Zustand v4 |

---

## Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| Store updates don't trigger re-renders | Use selector: `useStore(state => state.value)` not destructuring |
| TypeScript errors with middleware | Use `create<T>()()` double parentheses |
| Hydration error with persist | Implement `_hasHydrated` flag pattern |
| Actions not showing in DevTools | Pass action name: `set(newState, undefined, 'actionName')` |
| Store resets unexpectedly | HMR causes reset in development |

---

## Dependencies

```json
{ "dependencies": { "zustand": "^5.0.8", "react": "^18.0.0+" } }
```

**Compatibility**: React 18+, React 19, TypeScript 5+, Next.js 14+, Vite 5+

---

**Official Docs**: https://zustand.docs.pmnd.rs/ | **GitHub**: https://github.com/pmndrs/zustand
