---
name: zustand-advanced-patterns
description: Use when implementing advanced Zustand patterns including transient updates, subscriptions with selectors, store composition, and performance optimization techniques.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
---

# Zustand - Advanced Patterns

Advanced techniques and patterns for building complex applications with Zustand, including transient updates, optimistic updates, and sophisticated state management strategies.

## Key Concepts

### Transient Updates

Update state without triggering re-renders:

```typescript
const useStore = create((set) => ({
  count: 0,
  increment: () =>
    set((state) => ({ count: state.count + 1 }), false, 'increment'),
}))

// Usage: Update without re-rendering
useStore.setState({ count: 10 }, true) // replace: true, skip re-render
```

### Subscriptions with Selectors

Subscribe to specific slices of state:

```typescript
const useStore = create<Store>()((set) => ({ /* ... */ }))

// Subscribe only to count changes
const unsubscribe = useStore.subscribe(
  (state) => state.count,
  (count, prevCount) => {
    console.log(`Count changed from ${prevCount} to ${count}`)
  },
  {
    equalityFn: (a, b) => a === b,
    fireImmediately: false,
  }
)
```

## Best Practices

### 1. Optimistic Updates

Update UI immediately, then sync with server:

```typescript
interface TodoStore {
  todos: Todo[]
  addTodo: (text: string) => Promise<void>
  updateTodo: (id: string, text: string) => Promise<void>
  deleteTodo: (id: string) => Promise<void>
}

const useTodoStore = create<TodoStore>()((set, get) => ({
  todos: [],

  addTodo: async (text) => {
    const optimisticTodo = {
      id: `temp-${Date.now()}`,
      text,
      completed: false,
    }

    // Optimistic update
    set((state) => ({
      todos: [...state.todos, optimisticTodo],
    }))

    try {
      const savedTodo = await api.createTodo({ text })

      // Replace optimistic todo with real one
      set((state) => ({
        todos: state.todos.map((todo) =>
          todo.id === optimisticTodo.id ? savedTodo : todo
        ),
      }))
    } catch (error) {
      // Rollback on error
      set((state) => ({
        todos: state.todos.filter((todo) => todo.id !== optimisticTodo.id),
      }))
      throw error
    }
  },

  updateTodo: async (id, text) => {
    const previousTodos = get().todos

    // Optimistic update
    set((state) => ({
      todos: state.todos.map((todo) =>
        todo.id === id ? { ...todo, text } : todo
      ),
    }))

    try {
      await api.updateTodo(id, { text })
    } catch (error) {
      // Rollback on error
      set({ todos: previousTodos })
      throw error
    }
  },

  deleteTodo: async (id) => {
    const previousTodos = get().todos

    // Optimistic update
    set((state) => ({
      todos: state.todos.filter((todo) => todo.id !== id),
    }))

    try {
      await api.deleteTodo(id)
    } catch (error) {
      // Rollback on error
      set({ todos: previousTodos })
      throw error
    }
  },
}))
```

### 2. Undo/Redo Pattern

Implement time-travel functionality:

```typescript
interface HistoryState<T> {
  past: T[]
  present: T
  future: T[]
}

interface HistoryStore<T> {
  history: HistoryState<T>
  canUndo: boolean
  canRedo: boolean
  set: (newPresent: T) => void
  undo: () => void
  redo: () => void
  reset: (initialState: T) => void
}

function createHistoryStore<T>(initialState: T) {
  return create<HistoryStore<T>>()((set, get) => ({
    history: {
      past: [],
      present: initialState,
      future: [],
    },

    get canUndo() {
      return get().history.past.length > 0
    },

    get canRedo() {
      return get().history.future.length > 0
    },

    set: (newPresent) =>
      set((state) => ({
        history: {
          past: [...state.history.past, state.history.present],
          present: newPresent,
          future: [],
        },
      })),

    undo: () =>
      set((state) => {
        if (state.history.past.length === 0) return state

        const previous = state.history.past[state.history.past.length - 1]
        const newPast = state.history.past.slice(0, -1)

        return {
          history: {
            past: newPast,
            present: previous,
            future: [state.history.present, ...state.history.future],
          },
        }
      }),

    redo: () =>
      set((state) => {
        if (state.history.future.length === 0) return state

        const next = state.history.future[0]
        const newFuture = state.history.future.slice(1)

        return {
          history: {
            past: [...state.history.past, state.history.present],
            present: next,
            future: newFuture,
          },
        }
      }),

    reset: (initialState) =>
      set({
        history: {
          past: [],
          present: initialState,
          future: [],
        },
      }),
  }))
}

// Usage
interface CanvasState {
  shapes: Shape[]
  selectedId: string | null
}

const useCanvasStore = createHistoryStore<CanvasState>({
  shapes: [],
  selectedId: null,
})

function Canvas() {
  const { present } = useCanvasStore((state) => state.history)
  const { canUndo, canRedo, undo, redo } = useCanvasStore()

  return (
    <div>
      <button onClick={undo} disabled={!canUndo}>
        Undo
      </button>
      <button onClick={redo} disabled={!canRedo}>
        Redo
      </button>
      {/* Render canvas */}
    </div>
  )
}
```

### 3. Store Composition

Compose multiple stores together:

```typescript
import { create, StoreApi } from 'zustand'

// Create bound stores that can access each other
function createBoundStore() {
  const useAuthStore = create<AuthStore>()((set, get) => ({
    user: null,
    login: async (credentials) => {
      const user = await api.login(credentials)
      set({ user })

      // Access cart store after login
      const cartStore = stores.cart.getState()
      await cartStore.syncCart()
    },
    logout: () => {
      set({ user: null })
      // Clear cart on logout
      stores.cart.getState().clearCart()
    },
  }))

  const useCartStore = create<CartStore>()((set, get) => ({
    items: [],
    addItem: (item) =>
      set((state) => ({ items: [...state.items, item] })),
    clearCart: () => set({ items: [] }),
    syncCart: async () => {
      const user = stores.auth.getState().user
      if (!user) return

      const items = await api.fetchCart(user.id)
      set({ items })
    },
  }))

  return {
    auth: useAuthStore,
    cart: useCartStore,
  }
}

const stores = createBoundStore()

export const useAuthStore = stores.auth
export const useCartStore = stores.cart
```

### 4. React Context Integration

Use Zustand with React Context for scoped stores:

```typescript
import { createContext, useContext, useRef } from 'react'
import { createStore, useStore } from 'zustand'

interface TodoStore {
  todos: Todo[]
  addTodo: (text: string) => void
  toggleTodo: (id: string) => void
}

type TodoStoreApi = ReturnType<typeof createTodoStore>

const createTodoStore = (initialTodos: Todo[] = []) => {
  return createStore<TodoStore>()((set) => ({
    todos: initialTodos,
    addTodo: (text) =>
      set((state) => ({
        todos: [
          ...state.todos,
          { id: Date.now().toString(), text, completed: false },
        ],
      })),
    toggleTodo: (id) =>
      set((state) => ({
        todos: state.todos.map((todo) =>
          todo.id === id ? { ...todo, completed: !todo.completed } : todo
        ),
      })),
  }))
}

const TodoStoreContext = createContext<TodoStoreApi | null>(null)

export function TodoStoreProvider({
  children,
  initialTodos,
}: {
  children: React.ReactNode
  initialTodos?: Todo[]
}) {
  const storeRef = useRef<TodoStoreApi>()

  if (!storeRef.current) {
    storeRef.current = createTodoStore(initialTodos)
  }

  return (
    <TodoStoreContext.Provider value={storeRef.current}>
      {children}
    </TodoStoreContext.Provider>
  )
}

export function useTodoStore<T>(selector: (state: TodoStore) => T): T {
  const store = useContext(TodoStoreContext)

  if (!store) {
    throw new Error('useTodoStore must be used within TodoStoreProvider')
  }

  return useStore(store, selector)
}

// Usage
function App() {
  return (
    <TodoStoreProvider initialTodos={[]}>
      <TodoList />
    </TodoStoreProvider>
  )
}

function TodoList() {
  const todos = useTodoStore((state) => state.todos)
  const addTodo = useTodoStore((state) => state.addTodo)

  return (
    <div>
      {todos.map((todo) => (
        <div key={todo.id}>{todo.text}</div>
      ))}
      <button onClick={() => addTodo('New todo')}>Add</button>
    </div>
  )
}
```

### 5. Derived State with Selectors

Create memoized derived state:

```typescript
import { create } from 'zustand'
import { shallow } from 'zustand/shallow'

interface Store {
  items: Item[]
  filter: 'all' | 'active' | 'completed'
  sortBy: 'name' | 'date'
}

const useStore = create<Store>()((set) => ({ /* ... */ }))

// Memoized selector
const selectFilteredAndSortedItems = (state: Store) => {
  let items = state.items

  // Filter
  if (state.filter === 'active') {
    items = items.filter((item) => !item.completed)
  } else if (state.filter === 'completed') {
    items = items.filter((item) => item.completed)
  }

  // Sort
  if (state.sortBy === 'name') {
    items = [...items].sort((a, b) => a.name.localeCompare(b.name))
  } else {
    items = [...items].sort((a, b) => b.date.getTime() - a.date.getTime())
  }

  return items
}

// Usage
function ItemList() {
  const items = useStore(selectFilteredAndSortedItems)
  return <div>{items.map((item) => <Item key={item.id} item={item} />)}</div>
}
```

## Examples

### WebSocket Integration

```typescript
interface ChatStore {
  messages: Message[]
  isConnected: boolean
  connect: () => void
  disconnect: () => void
  sendMessage: (text: string) => void
}

const useChatStore = create<ChatStore>()((set, get) => {
  let ws: WebSocket | null = null

  return {
    messages: [],
    isConnected: false,

    connect: () => {
      ws = new WebSocket('wss://chat.example.com')

      ws.onopen = () => {
        set({ isConnected: true })
      }

      ws.onmessage = (event) => {
        const message = JSON.parse(event.data)
        set((state) => ({
          messages: [...state.messages, message],
        }))
      }

      ws.onclose = () => {
        set({ isConnected: false })
      }

      ws.onerror = (error) => {
        console.error('WebSocket error:', error)
        set({ isConnected: false })
      }
    },

    disconnect: () => {
      ws?.close()
      ws = null
      set({ isConnected: false })
    },

    sendMessage: (text) => {
      if (!ws || ws.readyState !== WebSocket.OPEN) return

      const message = {
        id: Date.now().toString(),
        text,
        timestamp: new Date(),
        userId: 'current-user',
      }

      ws.send(JSON.stringify(message))

      // Optimistically add to messages
      set((state) => ({
        messages: [...state.messages, message],
      }))
    },
  }
})
```

### Pagination Pattern

```typescript
interface PaginatedStore<T> {
  items: T[]
  page: number
  pageSize: number
  total: number
  isLoading: boolean
  hasMore: boolean

  fetchPage: (page: number) => Promise<void>
  nextPage: () => Promise<void>
  prevPage: () => Promise<void>
  reset: () => void
}

function createPaginatedStore<T>(
  fetcher: (page: number, pageSize: number) => Promise<{ items: T[]; total: number }>,
  pageSize: number = 20
) {
  return create<PaginatedStore<T>>()((set, get) => ({
    items: [],
    page: 1,
    pageSize,
    total: 0,
    isLoading: false,

    get hasMore() {
      const { page, pageSize, total } = get()
      return page * pageSize < total
    },

    fetchPage: async (page) => {
      set({ isLoading: true })

      try {
        const { items, total } = await fetcher(page, get().pageSize)
        set({ items, page, total, isLoading: false })
      } catch (error) {
        set({ isLoading: false })
        throw error
      }
    },

    nextPage: async () => {
      const { page, hasMore } = get()
      if (!hasMore) return

      await get().fetchPage(page + 1)
    },

    prevPage: async () => {
      const { page } = get()
      if (page <= 1) return

      await get().fetchPage(page - 1)
    },

    reset: () =>
      set({
        items: [],
        page: 1,
        total: 0,
        isLoading: false,
      }),
  }))
}

// Usage
const useProductStore = createPaginatedStore<Product>(
  async (page, pageSize) => {
    const response = await fetch(
      `/api/products?page=${page}&pageSize=${pageSize}`
    )
    return response.json()
  }
)
```

### Computed Properties with Getters

```typescript
interface Store {
  items: Item[]
  filter: string
  sortBy: string

  // Computed
  filteredItems: Item[]
  sortedItems: Item[]
  stats: {
    total: number
    completed: number
    active: number
  }
}

const useStore = create<Store>()((set, get) => ({
  items: [],
  filter: 'all',
  sortBy: 'date',

  get filteredItems() {
    const { items, filter } = get()
    if (filter === 'all') return items
    if (filter === 'completed') return items.filter((i) => i.completed)
    return items.filter((i) => !i.completed)
  },

  get sortedItems() {
    const { filteredItems, sortBy } = get()
    const items = [...filteredItems]

    if (sortBy === 'name') {
      return items.sort((a, b) => a.name.localeCompare(b.name))
    }

    return items.sort((a, b) => b.date.getTime() - a.date.getTime())
  },

  get stats() {
    const { items } = get()
    return {
      total: items.length,
      completed: items.filter((i) => i.completed).length,
      active: items.filter((i) => !i.completed).length,
    }
  },
}))
```

## Common Patterns

### Batched Updates

Update multiple stores atomically:

```typescript
function batchUpdates(updates: Array<() => void>) {
  updates.forEach((update) => update())
}

// Usage
batchUpdates([
  () => useAuthStore.setState({ user: newUser }),
  () => useCartStore.setState({ items: [] }),
  () => useNotificationStore.setState({ unread: 0 }),
])
```

### Error Boundary Integration

```typescript
interface ErrorStore {
  errors: Error[]
  addError: (error: Error) => void
  clearErrors: () => void
}

const useErrorStore = create<ErrorStore>()((set) => ({
  errors: [],
  addError: (error) =>
    set((state) => ({ errors: [...state.errors, error] })),
  clearErrors: () => set({ errors: [] }),
}))

// Error boundary
function ErrorBoundary({ children }: { children: React.ReactNode }) {
  const errors = useErrorStore((state) => state.errors)

  if (errors.length > 0) {
    return <div>Error: {errors[0].message}</div>
  }

  return <>{children}</>
}
```

## Anti-Patterns

### ❌ Don't Store Derived State

```typescript
// Bad: Storing derived state
const useStore = create((set) => ({
  items: [],
  itemCount: 0, // ❌ Redundant
  addItem: (item) =>
    set((state) => ({
      items: [...state.items, item],
      itemCount: state.items.length + 1, // ❌ Manual sync
    })),
}))

// Good: Use getters for derived state
const useStore = create((set, get) => ({
  items: [],
  get itemCount() {
    return get().items.length
  },
  addItem: (item) =>
    set((state) => ({ items: [...state.items, item] })),
}))
```

### ❌ Don't Create Circular Dependencies

```typescript
// Bad: Circular dependencies
const useStoreA = create((set) => ({
  value: 0,
  update: () => {
    useStoreB.getState().sync() // ❌ Circular
  },
}))

const useStoreB = create((set) => ({
  value: 0,
  sync: () => {
    useStoreA.getState().update() // ❌ Circular
  },
}))
```

### ❌ Don't Overuse Subscriptions

```typescript
// Bad: Subscribing in every component
function Component() {
  useEffect(() => {
    const unsubscribe = useStore.subscribe((state) => {
      console.log(state) // ❌ Memory leak if not cleaned up
    })
    // Missing return unsubscribe
  }, [])
}

// Good: Use selectors instead
function Component() {
  const value = useStore((state) => state.value)
  return <div>{value}</div>
}
```

## Related Skills

- **zustand-store-patterns**: Basic store creation and usage
- **zustand-typescript**: TypeScript integration
- **zustand-middleware**: Using middleware for enhanced functionality
