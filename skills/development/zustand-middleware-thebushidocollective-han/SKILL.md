---
name: zustand-middleware
description: Use when implementing Zustand middleware for persistence, dev tools, immutability, and other enhanced store functionality. Covers persist, devtools, immer, and custom middleware.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
---

# Zustand - Middleware

Zustand provides powerful middleware to enhance store functionality including persistence, Redux DevTools integration, immutable updates with Immer, and more.

## Key Concepts

### Middleware Composition

Middleware wraps the store creator function:

```typescript
import { create } from 'zustand'
import { persist, devtools } from 'zustand/middleware'

const useStore = create(
  devtools(
    persist(
      (set) => ({
        count: 0,
        increment: () => set((state) => ({ count: state.count + 1 })),
      }),
      { name: 'counter-storage' }
    )
  )
)
```

### Order Matters

Apply middleware from inside out:

```typescript
// ✅ Correct order
create(devtools(persist(immer(...))))

// devtools wraps persist wraps immer wraps your store
```

## Best Practices

### 1. Persist Middleware

Save and restore store state to localStorage or other storage:

```typescript
import { create } from 'zustand'
import { persist, createJSONStorage } from 'zustand/middleware'

interface CartStore {
  items: CartItem[]
  addItem: (item: CartItem) => void
  removeItem: (id: string) => void
  clearCart: () => void
}

const useCartStore = create<CartStore>()(
  persist(
    (set) => ({
      items: [],
      addItem: (item) =>
        set((state) => ({ items: [...state.items, item] })),
      removeItem: (id) =>
        set((state) => ({
          items: state.items.filter((item) => item.id !== id),
        })),
      clearCart: () => set({ items: [] }),
    }),
    {
      name: 'shopping-cart',
      storage: createJSONStorage(() => localStorage),
    }
  )
)
```

#### Persist Options

```typescript
persist(
  (set) => ({ /* store */ }),
  {
    name: 'my-store', // unique name for storage key
    storage: createJSONStorage(() => localStorage), // or sessionStorage
    partialize: (state) => ({ count: state.count }), // only persist specific fields
    onRehydrateStorage: (state) => {
      console.log('hydration starts')
      return (state, error) => {
        if (error) {
          console.log('error during hydration', error)
        } else {
          console.log('hydration finished')
        }
      }
    },
    version: 1,
    migrate: (persistedState, version) => {
      // Handle version migrations
      if (version === 0) {
        // migrate old state to new format
      }
      return persistedState
    },
  }
)
```

### 2. DevTools Middleware

Integrate with Redux DevTools for debugging:

```typescript
import { create } from 'zustand'
import { devtools } from 'zustand/middleware'

interface Store {
  count: number
  increment: () => void
  decrement: () => void
}

const useStore = create<Store>()(
  devtools(
    (set) => ({
      count: 0,
      increment: () =>
        set((state) => ({ count: state.count + 1 }), false, 'increment'),
      decrement: () =>
        set((state) => ({ count: state.count - 1 }), false, 'decrement'),
    }),
    { name: 'CounterStore' }
  )
)
```

#### DevTools Options

```typescript
devtools(
  (set) => ({ /* store */ }),
  {
    name: 'MyStore', // name in devtools
    enabled: process.env.NODE_ENV === 'development', // enable conditionally
    anonymousActionType: 'action', // default action name
    trace: true, // include stack traces
  }
)
```

### 3. Immer Middleware

Write immutable updates with mutable syntax:

```typescript
import { create } from 'zustand'
import { immer } from 'zustand/middleware/immer'

interface TodoStore {
  todos: Todo[]
  addTodo: (text: string) => void
  toggleTodo: (id: string) => void
  updateTodo: (id: string, text: string) => void
}

const useTodoStore = create<TodoStore>()(
  immer((set) => ({
    todos: [],

    addTodo: (text) =>
      set((state) => {
        state.todos.push({
          id: Date.now().toString(),
          text,
          completed: false,
        })
      }),

    toggleTodo: (id) =>
      set((state) => {
        const todo = state.todos.find((t) => t.id === id)
        if (todo) {
          todo.completed = !todo.completed
        }
      }),

    updateTodo: (id, text) =>
      set((state) => {
        const todo = state.todos.find((t) => t.id === id)
        if (todo) {
          todo.text = text
        }
      }),
  }))
)
```

### 4. Subscriptions

Listen to state changes outside React:

```typescript
const useStore = create<Store>()((set) => ({ /* ... */ }))

// Subscribe to all changes
const unsubscribe = useStore.subscribe((state, prevState) => {
  console.log('State changed:', state)
})

// Subscribe to specific values
const unsubscribe = useStore.subscribe(
  (state) => state.count,
  (count, prevCount) => {
    console.log('Count changed from', prevCount, 'to', count)
  }
)

// Clean up
unsubscribe()
```

### 5. Combining Multiple Middleware

```typescript
import { create } from 'zustand'
import { devtools, persist } from 'zustand/middleware'
import { immer } from 'zustand/middleware/immer'

interface Store {
  count: number
  todos: Todo[]
  increment: () => void
  addTodo: (text: string) => void
}

const useStore = create<Store>()(
  devtools(
    persist(
      immer((set) => ({
        count: 0,
        todos: [],

        increment: () =>
          set((state) => {
            state.count++
          }),

        addTodo: (text) =>
          set((state) => {
            state.todos.push({
              id: Date.now().toString(),
              text,
              completed: false,
            })
          }),
      })),
      {
        name: 'app-storage',
        partialize: (state) => ({
          count: state.count,
          todos: state.todos,
        }),
      }
    ),
    { name: 'AppStore' }
  )
)
```

## Examples

### Custom Logging Middleware

```typescript
import { StateCreator, StoreMutatorIdentifier } from 'zustand'

type Logger = <
  T,
  Mps extends [StoreMutatorIdentifier, unknown][] = [],
  Mcs extends [StoreMutatorIdentifier, unknown][] = []
>(
  f: StateCreator<T, Mps, Mcs>,
  name?: string
) => StateCreator<T, Mps, Mcs>

type LoggerImpl = <T>(
  f: StateCreator<T, [], []>,
  name?: string
) => StateCreator<T, [], []>

const loggerImpl: LoggerImpl = (f, name) => (set, get, store) => {
  const loggedSet: typeof set = (...a) => {
    set(...a)
    console.log(...(name ? [`${name}:`] : []), get())
  }

  store.setState = loggedSet

  return f(loggedSet, get, store)
}

export const logger = loggerImpl as unknown as Logger

// Usage
const useStore = create<Store>()(
  logger(
    (set) => ({
      count: 0,
      increment: () => set((state) => ({ count: state.count + 1 })),
    }),
    'CounterStore'
  )
)
```

### Custom Reset Middleware

```typescript
import { StateCreator, StoreMutatorIdentifier } from 'zustand'

type Resettable = <
  T,
  Mps extends [StoreMutatorIdentifier, unknown][] = [],
  Mcs extends [StoreMutatorIdentifier, unknown][] = []
>(
  f: StateCreator<T, Mps, Mcs>
) => StateCreator<T, Mps, Mcs>

type ResettableImpl = <T>(
  f: StateCreator<T, [], []>
) => StateCreator<T, [], []>

const resettableImpl: ResettableImpl = (f) => (set, get, store) => {
  const initialState = f(set, get, store)

  store.reset = () => set(initialState)

  return initialState
}

export const resettable = resettableImpl as unknown as Resettable

// Extend store type
declare module 'zustand' {
  interface StoreApi<T> {
    reset?: () => void
  }
}

// Usage
const useStore = create<Store>()(
  resettable((set) => ({
    count: 0,
    name: '',
    increment: () => set((state) => ({ count: state.count + 1 })),
    setName: (name) => set({ name }),
  }))
)

// Reset to initial state
useStore.reset()
```

### IndexedDB Persistence

```typescript
import { StateStorage } from 'zustand/middleware'
import { get, set, del } from 'idb-keyval'

const indexedDBStorage: StateStorage = {
  getItem: async (name: string): Promise<string | null> => {
    return (await get(name)) || null
  },
  setItem: async (name: string, value: string): Promise<void> => {
    await set(name, value)
  },
  removeItem: async (name: string): Promise<void> => {
    await del(name)
  },
}

const useStore = create<Store>()(
  persist(
    (set) => ({
      largeData: [],
      addData: (data) =>
        set((state) => ({ largeData: [...state.largeData, data] })),
    }),
    {
      name: 'large-data-storage',
      storage: createJSONStorage(() => indexedDBStorage),
    }
  )
)
```

### Async Storage for React Native

```typescript
import AsyncStorage from '@react-native-async-storage/async-storage'
import { StateStorage } from 'zustand/middleware'

const asyncStorage: StateStorage = {
  getItem: async (name: string): Promise<string | null> => {
    return await AsyncStorage.getItem(name)
  },
  setItem: async (name: string, value: string): Promise<void> => {
    await AsyncStorage.setItem(name, value)
  },
  removeItem: async (name: string): Promise<void> => {
    await AsyncStorage.removeItem(name)
  },
}

const useStore = create<Store>()(
  persist(
    (set) => ({ /* ... */ }),
    {
      name: 'app-storage',
      storage: createJSONStorage(() => asyncStorage),
    }
  )
)
```

## Common Patterns

### Conditional Persistence

Only persist certain fields:

```typescript
const useStore = create<Store>()(
  persist(
    (set) => ({
      // Persisted
      theme: 'light',
      language: 'en',

      // Not persisted
      isLoading: false,
      error: null,

      setTheme: (theme) => set({ theme }),
      setLanguage: (language) => set({ language }),
    }),
    {
      name: 'settings',
      partialize: (state) => ({
        theme: state.theme,
        language: state.language,
      }),
    }
  )
)
```

### Version Migration

Handle breaking changes in persisted state:

```typescript
const useStore = create<Store>()(
  persist(
    (set) => ({ /* ... */ }),
    {
      name: 'app-store',
      version: 2,
      migrate: (persistedState: any, version: number) => {
        if (version === 0) {
          // Migrate from version 0 to 1
          persistedState.newField = 'default'
        }

        if (version === 1) {
          // Migrate from version 1 to 2
          persistedState.items = persistedState.oldItems.map((item: any) => ({
            id: item.id,
            name: item.title, // renamed field
          }))
          delete persistedState.oldItems
        }

        return persistedState as Store
      },
    }
  )
)
```

### Hydration Detection

Know when persisted state is loaded:

```typescript
const useStore = create<Store>()(
  persist(
    (set) => ({
      count: 0,
      increment: () => set((state) => ({ count: state.count + 1 })),
    }),
    {
      name: 'counter',
      onRehydrateStorage: () => (state) => {
        console.log('State hydrated:', state)
      },
    }
  )
)

// In a component
function App() {
  const [hydrated, setHydrated] = useState(false)

  useEffect(() => {
    useStore.persist.onFinishHydration(() => {
      setHydrated(true)
    })
  }, [])

  if (!hydrated) {
    return <div>Loading...</div>
  }

  return <div>App content</div>
}
```

## Anti-Patterns

### ❌ Don't Persist Sensitive Data

```typescript
// Bad: Persisting tokens in localStorage
const useAuthStore = create(
  persist(
    (set) => ({
      token: null,
      user: null,
      login: async (credentials) => {
        const { token, user } = await api.login(credentials)
        set({ token, user }) // ❌ Token in localStorage
      },
    }),
    { name: 'auth' }
  )
)

// Good: Use secure storage or don't persist tokens
const useAuthStore = create(
  persist(
    (set) => ({
      user: null,
      login: async (credentials) => {
        const { token, user } = await api.login(credentials)
        secureStorage.setToken(token) // ✅ Secure storage
        set({ user })
      },
    }),
    {
      name: 'auth',
      partialize: (state) => ({ user: state.user }), // ✅ Only persist user
    }
  )
)
```

### ❌ Don't Ignore Middleware Order

```typescript
// Bad: DevTools won't see persisted initial state
create(persist(devtools(...)))

// Good: DevTools can see full state lifecycle
create(devtools(persist(...)))
```

### ❌ Don't Mutate State Without Immer

```typescript
// Bad: Mutating without immer
const useStore = create((set) => ({
  items: [],
  addItem: (item) =>
    set((state) => {
      state.items.push(item) // ❌ Direct mutation
      return state
    }),
}))

// Good: Use immer middleware
const useStore = create(
  immer((set) => ({
    items: [],
    addItem: (item) =>
      set((state) => {
        state.items.push(item) // ✅ Safe with immer
      }),
  }))
)
```

### ❌ Don't Forget to Clean Up Subscriptions

```typescript
// Bad: Memory leak
useEffect(() => {
  useStore.subscribe((state) => {
    console.log(state)
  })
}, [])

// Good: Clean up subscription
useEffect(() => {
  const unsubscribe = useStore.subscribe((state) => {
    console.log(state)
  })
  return unsubscribe
}, [])
```

## Related Skills

- **zustand-store-patterns**: Basic store creation and usage
- **zustand-typescript**: TypeScript integration with middleware
- **zustand-advanced-patterns**: Custom middleware and advanced techniques
