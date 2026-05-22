---
name: zustand-patterns
description: Zustand 5.x state management with slices, middleware, Immer, useShallow, and persistence patterns for React applications. Use when building state management with Zustand.
tags: [zustand, state-management, react, immer, middleware, persistence, slices]
context: fork
agent: frontend-ui-developer
version: 1.0.0
allowed-tools: [Read, Write, Grep, Glob]
author: SkillForge
user-invocable: false
---

# Zustand Patterns

Modern state management with Zustand 5.x - lightweight, TypeScript-first, no boilerplate.

## Overview

- Global state without Redux complexity
- Shared state across components without prop drilling
- Persisted state with localStorage/sessionStorage
- Computed/derived state with selectors
- State that needs middleware (logging, devtools, persistence)

## Core Patterns

### 1. Basic Store with TypeScript

```typescript
import { create } from 'zustand';

interface BearState {
  bears: number;
  increase: (by: number) => void;
  reset: () => void;
}

const useBearStore = create<BearState>()((set) => ({
  bears: 0,
  increase: (by) => set((state) => ({ bears: state.bears + by })),
  reset: () => set({ bears: 0 }),
}));
```

### 2. Slices Pattern (Modular Stores)

```typescript
import { create, StateCreator } from 'zustand';

// Auth slice
interface AuthSlice {
  user: User | null;
  login: (user: User) => void;
  logout: () => void;
}

const createAuthSlice: StateCreator<AuthSlice & CartSlice, [], [], AuthSlice> = (set) => ({
  user: null,
  login: (user) => set({ user }),
  logout: () => set({ user: null }),
});

// Cart slice
interface CartSlice {
  items: CartItem[];
  addItem: (item: CartItem) => void;
  clearCart: () => void;
}

const createCartSlice: StateCreator<AuthSlice & CartSlice, [], [], CartSlice> = (set) => ({
  items: [],
  addItem: (item) => set((state) => ({ items: [...state.items, item] })),
  clearCart: () => set({ items: [] }),
});

// Combined store
const useStore = create<AuthSlice & CartSlice>()((...a) => ({
  ...createAuthSlice(...a),
  ...createCartSlice(...a),
}));
```

### 3. Immer Middleware (Immutable Updates)

```typescript
import { create } from 'zustand';
import { immer } from 'zustand/middleware/immer';

interface TodoState {
  todos: Todo[];
  addTodo: (text: string) => void;
  toggleTodo: (id: string) => void;
  updateNested: (id: string, subtaskId: string, done: boolean) => void;
}

const useTodoStore = create<TodoState>()(
  immer((set) => ({
    todos: [],
    addTodo: (text) =>
      set((state) => {
        state.todos.push({ id: crypto.randomUUID(), text, done: false });
      }),
    toggleTodo: (id) =>
      set((state) => {
        const todo = state.todos.find((t) => t.id === id);
        if (todo) todo.done = !todo.done;
      }),
    updateNested: (id, subtaskId, done) =>
      set((state) => {
        const todo = state.todos.find((t) => t.id === id);
        const subtask = todo?.subtasks?.find((s) => s.id === subtaskId);
        if (subtask) subtask.done = done;
      }),
  }))
);
```

### 4. Persist Middleware

```typescript
import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';

interface SettingsState {
  theme: 'light' | 'dark';
  language: string;
  setTheme: (theme: 'light' | 'dark') => void;
}

const useSettingsStore = create<SettingsState>()(
  persist(
    (set) => ({
      theme: 'light',
      language: 'en',
      setTheme: (theme) => set({ theme }),
    }),
    {
      name: 'settings-storage',
      storage: createJSONStorage(() => localStorage),
      partialize: (state) => ({ theme: state.theme }), // Only persist theme
      version: 1,
      migrate: (persisted, version) => {
        if (version === 0) {
          // Migration logic
        }
        return persisted as SettingsState;
      },
    }
  )
);
```

### 5. Selectors (Prevent Re-renders)

```typescript
// ❌ BAD: Re-renders on ANY state change
const { bears, fish } = useBearStore();

// ✅ GOOD: Only re-renders when bears changes
const bears = useBearStore((state) => state.bears);

// ✅ GOOD: Shallow comparison for objects (Zustand 5.x)
import { useShallow } from 'zustand/react/shallow';

const { bears, fish } = useBearStore(
  useShallow((state) => ({ bears: state.bears, fish: state.fish }))
);

// ✅ GOOD: Computed/derived state via selector
const totalAnimals = useBearStore((state) => state.bears + state.fish);

// ❌ BAD: Storing computed state
const useStore = create((set) => ({
  items: [],
  total: 0, // Don't store derived values!
  addItem: (item) => set((s) => ({
    items: [...s.items, item],
    total: s.total + item.price, // Sync issues!
  })),
}));

// ✅ GOOD: Compute in selector
const total = useStore((s) => s.items.reduce((sum, i) => sum + i.price, 0));
```

### 6. Async Actions

```typescript
interface UserState {
  user: User | null;
  loading: boolean;
  error: string | null;
  fetchUser: (id: string) => Promise<void>;
}

const useUserStore = create<UserState>()((set) => ({
  user: null,
  loading: false,
  error: null,
  fetchUser: async (id) => {
    set({ loading: true, error: null });
    try {
      const user = await api.getUser(id);
      set({ user, loading: false });
    } catch (error) {
      set({ error: error.message, loading: false });
    }
  },
}));
```

### 7. DevTools Integration

```typescript
import { create } from 'zustand';
import { devtools } from 'zustand/middleware';

const useStore = create<State>()(
  devtools(
    (set) => ({
      // ... state and actions
    }),
    { name: 'MyStore', enabled: process.env.NODE_ENV === 'development' }
  )
);
```

## Quick Reference

```typescript
// ✅ Create typed store with double-call pattern
const useStore = create<State>()((set, get) => ({ ... }));

// ✅ Use selectors for all state access
const count = useStore((s) => s.count);

// ✅ Use useShallow for multiple values (Zustand 5.x)
const { a, b } = useStore(useShallow((s) => ({ a: s.a, b: s.b })));

// ✅ Middleware order: immer → subscribeWithSelector → devtools → persist
create(persist(devtools(immer((set) => ({ ... })))))

// ❌ Never destructure entire store
const store = useStore(); // Re-renders on ANY change

// ❌ Never store server state (use TanStack Query instead)
const useStore = create((set) => ({ users: [], fetchUsers: async () => ... }));
```

## Key Decisions

| Decision | Option A | Option B | Recommendation |
|----------|----------|----------|----------------|
| State structure | Single store | Multiple stores | **Slices in single store** - easier cross-slice access |
| Nested updates | Spread operator | Immer middleware | **Immer** for deeply nested state (3+ levels) |
| Persistence | Manual localStorage | persist middleware | **persist middleware** with partialize |
| Multiple values | Multiple selectors | useShallow | **useShallow** for 2-5 related values |
| Server state | Zustand | TanStack Query | **TanStack Query** - Zustand for client-only state |
| DevTools | Always on | Conditional | **Conditional** - `enabled: process.env.NODE_ENV === 'development'` |

## Anti-Patterns (FORBIDDEN)

```typescript
// ❌ FORBIDDEN: Destructuring entire store
const { count, increment } = useStore(); // Re-renders on ANY state change

// ❌ FORBIDDEN: Storing derived/computed state
const useStore = create((set) => ({
  items: [],
  total: 0, // Will get out of sync!
}));

// ❌ FORBIDDEN: Storing server state
const useStore = create((set) => ({
  users: [], // Use TanStack Query instead
  fetchUsers: async () => { ... },
}));

// ❌ FORBIDDEN: Mutating state without Immer
set((state) => {
  state.items.push(item); // Breaks reactivity!
  return state;
});

// ❌ FORBIDDEN: Using deprecated shallow import
import { shallow } from 'zustand/shallow'; // Use useShallow from zustand/react/shallow
```

## Integration with React Query

```typescript
// ✅ Zustand for CLIENT state (UI, preferences, local-only)
const useUIStore = create<UIState>()((set) => ({
  sidebarOpen: false,
  theme: 'light',
  toggleSidebar: () => set((s) => ({ sidebarOpen: !s.sidebarOpen })),
}));

// ✅ TanStack Query for SERVER state (API data)
function Dashboard() {
  const sidebarOpen = useUIStore((s) => s.sidebarOpen);
  const { data: users } = useQuery({ queryKey: ['users'], queryFn: fetchUsers });
  // Zustand: UI state | TanStack Query: server data
}
```

## Related Skills

- `tanstack-query-advanced` - Server state management (use with Zustand for client state)
- `form-state-patterns` - Form state (React Hook Form vs Zustand for forms)
- `react-server-components-framework` - RSC hydration considerations with Zustand

## Capability Details

### store-creation
**Keywords**: zustand, create, store, typescript, state
**Solves**: Setting up type-safe Zustand stores with proper TypeScript inference

### slices-pattern
**Keywords**: slices, modular, split, combine, StateCreator
**Solves**: Organizing large stores into maintainable, domain-specific slices

### middleware-stack
**Keywords**: immer, persist, devtools, middleware, compose
**Solves**: Combining middleware in correct order for immutability, persistence, and debugging

### selector-optimization
**Keywords**: selector, useShallow, re-render, performance, memoization
**Solves**: Preventing unnecessary re-renders with proper selector patterns

### persistence-migration
**Keywords**: persist, localStorage, sessionStorage, migrate, version
**Solves**: Persisting state with schema migrations between versions

## References

- `references/middleware-composition.md` - Combining multiple middleware
- `templates/store-template.ts` - Production-ready store template
- `checklists/zustand-checklist.md` - Implementation checklist
