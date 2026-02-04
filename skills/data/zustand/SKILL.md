---
name: zustand
description: Manages application state with Zustand including stores, selectors, actions, and middleware. Use when managing client-side state, creating global stores, persisting state, or replacing Redux/Context.
---

# Zustand

Small, fast, and scalable state management using simplified flux principles.

## Quick Start

**Install:**
```bash
npm install zustand
```

**Create a store:**
```typescript
import { create } from 'zustand';

interface BearStore {
  bears: number;
  increase: () => void;
  decrease: () => void;
  reset: () => void;
}

const useBearStore = create<BearStore>((set) => ({
  bears: 0,
  increase: () => set((state) => ({ bears: state.bears + 1 })),
  decrease: () => set((state) => ({ bears: state.bears - 1 })),
  reset: () => set({ bears: 0 }),
}));
```

**Use in component:**
```tsx
function BearCounter() {
  const bears = useBearStore((state) => state.bears);
  const increase = useBearStore((state) => state.increase);

  return (
    <div>
      <h1>{bears} bears</h1>
      <button onClick={increase}>Add bear</button>
    </div>
  );
}
```

## Core Concepts

### Creating Stores

```typescript
import { create } from 'zustand';

// Simple store
const useCountStore = create<{ count: number; inc: () => void }>((set) => ({
  count: 0,
  inc: () => set((state) => ({ count: state.count + 1 })),
}));

// With get for accessing current state
const useStore = create<Store>((set, get) => ({
  count: 0,
  doubleCount: () => get().count * 2,
  increment: () => set((state) => ({ count: state.count + 1 })),
}));
```

### Selectors

```typescript
// Select single value - re-renders only when bears changes
const bears = useBearStore((state) => state.bears);

// Select action - stable reference, no re-renders
const increase = useBearStore((state) => state.increase);

// Select multiple values with shallow compare
import { shallow } from 'zustand/shallow';

const { bears, fish } = useBearStore(
  (state) => ({ bears: state.bears, fish: state.fish }),
  shallow
);

// Or use useShallow hook
import { useShallow } from 'zustand/react/shallow';

const { bears, fish } = useBearStore(
  useShallow((state) => ({ bears: state.bears, fish: state.fish }))
);

// Select array of values
const [bears, fish] = useBearStore(
  useShallow((state) => [state.bears, state.fish])
);
```

### Actions

```typescript
interface TodoStore {
  todos: Todo[];
  addTodo: (text: string) => void;
  removeTodo: (id: string) => void;
  toggleTodo: (id: string) => void;
  clearCompleted: () => void;
}

const useTodoStore = create<TodoStore>((set) => ({
  todos: [],

  addTodo: (text) =>
    set((state) => ({
      todos: [
        ...state.todos,
        { id: crypto.randomUUID(), text, completed: false },
      ],
    })),

  removeTodo: (id) =>
    set((state) => ({
      todos: state.todos.filter((todo) => todo.id !== id),
    })),

  toggleTodo: (id) =>
    set((state) => ({
      todos: state.todos.map((todo) =>
        todo.id === id ? { ...todo, completed: !todo.completed } : todo
      ),
    })),

  clearCompleted: () =>
    set((state) => ({
      todos: state.todos.filter((todo) => !todo.completed),
    })),
}));
```

### Async Actions

```typescript
interface UserStore {
  users: User[];
  loading: boolean;
  error: string | null;
  fetchUsers: () => Promise<void>;
}

const useUserStore = create<UserStore>((set) => ({
  users: [],
  loading: false,
  error: null,

  fetchUsers: async () => {
    set({ loading: true, error: null });

    try {
      const response = await fetch('/api/users');
      const users = await response.json();
      set({ users, loading: false });
    } catch (error) {
      set({ error: 'Failed to fetch users', loading: false });
    }
  },
}));
```

## Middleware

### Persist

```typescript
import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';

interface SettingsStore {
  theme: 'light' | 'dark';
  language: string;
  setTheme: (theme: 'light' | 'dark') => void;
  setLanguage: (language: string) => void;
}

const useSettingsStore = create<SettingsStore>()(
  persist(
    (set) => ({
      theme: 'light',
      language: 'en',
      setTheme: (theme) => set({ theme }),
      setLanguage: (language) => set({ language }),
    }),
    {
      name: 'settings-storage',
      storage: createJSONStorage(() => localStorage),
      partialize: (state) => ({
        theme: state.theme,
        language: state.language,
      }),
    }
  )
);
```

### Persist with Async Storage

```typescript
import { persist, createJSONStorage } from 'zustand/middleware';
import AsyncStorage from '@react-native-async-storage/async-storage';

const useStore = create(
  persist(
    (set) => ({
      // ...state
    }),
    {
      name: 'app-storage',
      storage: createJSONStorage(() => AsyncStorage),
    }
  )
);
```

### DevTools

```typescript
import { create } from 'zustand';
import { devtools } from 'zustand/middleware';

const useStore = create<Store>()(
  devtools(
    (set) => ({
      count: 0,
      increment: () =>
        set(
          (state) => ({ count: state.count + 1 }),
          false,
          'increment' // Action name for DevTools
        ),
    }),
    { name: 'CountStore' }
  )
);
```

### Immer

```typescript
import { create } from 'zustand';
import { immer } from 'zustand/middleware/immer';

interface Store {
  users: User[];
  addUser: (user: User) => void;
  updateUser: (id: string, updates: Partial<User>) => void;
}

const useStore = create<Store>()(
  immer((set) => ({
    users: [],

    addUser: (user) =>
      set((state) => {
        state.users.push(user);
      }),

    updateUser: (id, updates) =>
      set((state) => {
        const user = state.users.find((u) => u.id === id);
        if (user) {
          Object.assign(user, updates);
        }
      }),
  }))
);
```

### Combine Middleware

```typescript
import { create } from 'zustand';
import { devtools, persist } from 'zustand/middleware';
import { immer } from 'zustand/middleware/immer';

const useStore = create<Store>()(
  devtools(
    persist(
      immer((set) => ({
        // ...state and actions
      })),
      { name: 'store' }
    ),
    { name: 'Store' }
  )
);
```

## Patterns

### Slices Pattern

```typescript
// stores/userSlice.ts
export interface UserSlice {
  user: User | null;
  setUser: (user: User) => void;
  clearUser: () => void;
}

export const createUserSlice: StateCreator<
  UserSlice & CartSlice,
  [],
  [],
  UserSlice
> = (set) => ({
  user: null,
  setUser: (user) => set({ user }),
  clearUser: () => set({ user: null }),
});

// stores/cartSlice.ts
export interface CartSlice {
  items: CartItem[];
  addItem: (item: CartItem) => void;
  removeItem: (id: string) => void;
}

export const createCartSlice: StateCreator<
  UserSlice & CartSlice,
  [],
  [],
  CartSlice
> = (set) => ({
  items: [],
  addItem: (item) =>
    set((state) => ({ items: [...state.items, item] })),
  removeItem: (id) =>
    set((state) => ({ items: state.items.filter((i) => i.id !== id) })),
});

// stores/index.ts
import { create } from 'zustand';
import { createUserSlice, UserSlice } from './userSlice';
import { createCartSlice, CartSlice } from './cartSlice';

export const useStore = create<UserSlice & CartSlice>()((...a) => ({
  ...createUserSlice(...a),
  ...createCartSlice(...a),
}));
```

### Computed Values

```typescript
interface Store {
  items: CartItem[];
  getTotal: () => number;
  getItemCount: () => number;
}

const useCartStore = create<Store>((set, get) => ({
  items: [],

  getTotal: () => {
    return get().items.reduce(
      (total, item) => total + item.price * item.quantity,
      0
    );
  },

  getItemCount: () => {
    return get().items.reduce((count, item) => count + item.quantity, 0);
  },
}));

// Usage
function CartSummary() {
  const items = useCartStore((state) => state.items);
  const getTotal = useCartStore((state) => state.getTotal);

  return (
    <div>
      <p>Total: ${getTotal()}</p>
    </div>
  );
}
```

### Subscribe to Changes

```typescript
// Subscribe outside React
const unsub = useStore.subscribe(
  (state) => console.log('State changed:', state)
);

// Subscribe with selector
const unsub = useStore.subscribe(
  (state) => state.count,
  (count, prevCount) => {
    console.log('Count changed from', prevCount, 'to', count);
  }
);

// Cleanup
unsub();
```

### Access State Outside React

```typescript
// Get current state
const state = useStore.getState();
console.log(state.count);

// Update state
useStore.setState({ count: 10 });

// Call actions
useStore.getState().increment();
```

### Reset Store

```typescript
interface Store {
  count: number;
  name: string;
  increment: () => void;
  reset: () => void;
}

const initialState = {
  count: 0,
  name: '',
};

const useStore = create<Store>((set) => ({
  ...initialState,
  increment: () => set((state) => ({ count: state.count + 1 })),
  reset: () => set(initialState),
}));
```

## React Patterns

### Context for SSR

```tsx
// For Next.js App Router with SSR
import { createContext, useContext, useRef } from 'react';
import { createStore, StoreApi } from 'zustand';

const StoreContext = createContext<StoreApi<Store> | null>(null);

export function StoreProvider({
  children,
  initialState,
}: {
  children: React.ReactNode;
  initialState?: Partial<Store>;
}) {
  const storeRef = useRef<StoreApi<Store>>();

  if (!storeRef.current) {
    storeRef.current = createStore<Store>((set) => ({
      ...defaultState,
      ...initialState,
    }));
  }

  return (
    <StoreContext.Provider value={storeRef.current}>
      {children}
    </StoreContext.Provider>
  );
}

export function useAppStore<T>(selector: (state: Store) => T): T {
  const store = useContext(StoreContext);
  if (!store) throw new Error('Missing StoreProvider');
  return useStore(store, selector);
}
```

### Hydration

```typescript
import { create } from 'zustand';
import { persist } from 'zustand/middleware';

const useStore = create(
  persist(
    (set) => ({
      // state
    }),
    { name: 'store' }
  )
);

// Check hydration status
function Component() {
  const [hydrated, setHydrated] = useState(false);

  useEffect(() => {
    setHydrated(true);
  }, []);

  if (!hydrated) {
    return <Skeleton />;
  }

  return <ActualContent />;
}

// Or use onRehydrateStorage
persist(
  (set) => ({
    // state
  }),
  {
    name: 'store',
    onRehydrateStorage: () => (state, error) => {
      if (error) {
        console.error('Hydration error:', error);
      }
    },
  }
);
```

## Best Practices

1. **Use selectors** - Only subscribe to needed state
2. **Shallow compare for objects** - Prevent unnecessary re-renders
3. **Actions in store** - Keep logic centralized
4. **Persist selectively** - Use partialize for sensitive data
5. **DevTools in dev** - Enable for debugging

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Selecting entire state | Use specific selectors |
| Missing shallow compare | Add shallow for objects |
| Mutating state directly | Use immer or spread |
| Actions outside store | Define actions in create() |
| No TypeScript types | Define interface for store |

## Reference Files

- [references/patterns.md](references/patterns.md) - Advanced patterns
- [references/middleware.md](references/middleware.md) - Middleware guide
- [references/testing.md](references/testing.md) - Testing stores
