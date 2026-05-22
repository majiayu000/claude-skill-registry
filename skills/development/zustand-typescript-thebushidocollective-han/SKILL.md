---
name: zustand-typescript
description: Use when working with Zustand in TypeScript projects. Covers type-safe store creation, typed selectors, and advanced TypeScript patterns with Zustand.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
---

# Zustand - TypeScript Integration

Zustand has excellent TypeScript support out of the box. This skill covers type-safe patterns and best practices for using Zustand with TypeScript.

## Key Concepts

### Basic Type-Safe Store

Define your store interface and use it with `create`:

```typescript
import { create } from 'zustand'

interface BearStore {
  bears: number
  increasePopulation: () => void
  removeAllBears: () => void
  updateBears: (newBears: number) => void
}

const useBearStore = create<BearStore>()((set) => ({
  bears: 0,
  increasePopulation: () => set((state) => ({ bears: state.bears + 1 })),
  removeAllBears: () => set({ bears: 0 }),
  updateBears: (newBears) => set({ bears: newBears }),
}))
```

### Type Inference

Zustand can infer types automatically:

```typescript
const useStore = create((set) => ({
  count: 0,
  text: '',
  increment: () => set((state) => ({ count: state.count + 1 })),
  setText: (text: string) => set({ text }),
}))

// Types are inferred automatically
type Store = ReturnType<typeof useStore.getState>
// {
//   count: number
//   text: string
//   increment: () => void
//   setText: (text: string) => void
// }
```

## Best Practices

### 1. Define Store Interfaces

Always define explicit interfaces for better type safety and IDE support:

```typescript
interface User {
  id: string
  name: string
  email: string
}

interface UserStore {
  // State
  users: User[]
  selectedUserId: string | null
  isLoading: boolean
  error: string | null

  // Computed
  selectedUser: User | null

  // Actions
  fetchUsers: () => Promise<void>
  selectUser: (id: string) => void
  clearSelection: () => void
}

const useUserStore = create<UserStore>()((set, get) => ({
  users: [],
  selectedUserId: null,
  isLoading: false,
  error: null,

  get selectedUser() {
    const { users, selectedUserId } = get()
    return users.find((u) => u.id === selectedUserId) ?? null
  },

  fetchUsers: async () => {
    set({ isLoading: true, error: null })
    try {
      const users = await api.fetchUsers()
      set({ users, isLoading: false })
    } catch (error) {
      set({ error: error.message, isLoading: false })
    }
  },

  selectUser: (id) => set({ selectedUserId: id }),
  clearSelection: () => set({ selectedUserId: null }),
}))
```

### 2. Type-Safe Selectors

Create typed selector functions for reusable logic:

```typescript
interface TodoStore {
  todos: Todo[]
  filter: 'all' | 'active' | 'completed'
  addTodo: (text: string) => void
  toggleTodo: (id: string) => void
  setFilter: (filter: TodoStore['filter']) => void
}

const useTodoStore = create<TodoStore>()(/* ... */)

// Typed selector functions
const selectFilteredTodos = (state: TodoStore) => {
  if (state.filter === 'all') return state.todos
  if (state.filter === 'active') return state.todos.filter((t) => !t.completed)
  return state.todos.filter((t) => t.completed)
}

const selectActiveTodoCount = (state: TodoStore) =>
  state.todos.filter((t) => !t.completed).length

// Usage
function TodoList() {
  const filteredTodos = useTodoStore(selectFilteredTodos)
  const activeCount = useTodoStore(selectActiveTodoCount)

  return (
    <div>
      <p>{activeCount} active todos</p>
      {filteredTodos.map((todo) => (
        <TodoItem key={todo.id} todo={todo} />
      ))}
    </div>
  )
}
```

### 3. Slice Pattern with Types

Type-safe store slices for large applications:

```typescript
import { StateCreator } from 'zustand'

interface BearSlice {
  bears: number
  addBear: () => void
  eatFish: () => void
}

interface FishSlice {
  fishes: number
  addFish: () => void
}

interface SharedSlice {
  addBoth: () => void
  getBoth: () => number
}

const createBearSlice: StateCreator<
  BearSlice & FishSlice,
  [],
  [],
  BearSlice
> = (set) => ({
  bears: 0,
  addBear: () => set((state) => ({ bears: state.bears + 1 })),
  eatFish: () => set((state) => ({ fishes: state.fishes - 1 })),
})

const createFishSlice: StateCreator<
  BearSlice & FishSlice,
  [],
  [],
  FishSlice
> = (set) => ({
  fishes: 0,
  addFish: () => set((state) => ({ fishes: state.fishes + 1 })),
})

const createSharedSlice: StateCreator<
  BearSlice & FishSlice,
  [],
  [],
  SharedSlice
> = (set, get) => ({
  addBoth: () => {
    get().addBear()
    get().addFish()
  },
  getBoth: () => get().bears + get().fishes,
})

const useBoundStore = create<BearSlice & FishSlice & SharedSlice>()(
  (...a) => ({
    ...createBearSlice(...a),
    ...createFishSlice(...a),
    ...createSharedSlice(...a),
  })
)
```

### 4. Generic Store Factory

Create reusable store factories with generics:

```typescript
import { create, StoreApi } from 'zustand'

interface AsyncState<T> {
  data: T | null
  isLoading: boolean
  error: string | null
}

interface AsyncActions<T> {
  fetch: () => Promise<void>
  reset: () => void
}

type AsyncStore<T> = AsyncState<T> & AsyncActions<T>

function createAsyncStore<T>(
  fetcher: () => Promise<T>
): StoreApi<AsyncStore<T>> {
  return create<AsyncStore<T>>()((set) => ({
    data: null,
    isLoading: false,
    error: null,

    fetch: async () => {
      set({ isLoading: true, error: null })
      try {
        const data = await fetcher()
        set({ data, isLoading: false })
      } catch (error) {
        set({
          error: error instanceof Error ? error.message : 'Unknown error',
          isLoading: false,
        })
      }
    },

    reset: () => set({ data: null, isLoading: false, error: null }),
  }))
}

// Usage
interface User {
  id: string
  name: string
}

const useUserStore = createAsyncStore<User[]>(() =>
  fetch('/api/users').then((r) => r.json())
)
```

### 5. Type-Safe Middleware

Type middleware correctly for full type safety:

```typescript
import { create } from 'zustand'
import { persist, devtools } from 'zustand/middleware'
import type { PersistOptions } from 'zustand/middleware'

interface MyStore {
  count: number
  increment: () => void
}

type MyPersist = (
  config: StateCreator<MyStore>,
  options: PersistOptions<MyStore>
) => StateCreator<MyStore>

const useStore = create<MyStore>()(
  devtools(
    persist(
      (set) => ({
        count: 0,
        increment: () => set((state) => ({ count: state.count + 1 })),
      }),
      {
        name: 'my-store',
      }
    )
  )
)
```

## Examples

### Type-Safe CRUD Store

```typescript
interface Entity {
  id: string
  name: string
  createdAt: Date
}

interface CrudStore<T extends Entity> {
  items: T[]
  selectedId: string | null
  isLoading: boolean
  error: string | null

  // Computed
  selectedItem: T | null

  // Actions
  fetchAll: () => Promise<void>
  fetchOne: (id: string) => Promise<void>
  create: (data: Omit<T, 'id' | 'createdAt'>) => Promise<void>
  update: (id: string, data: Partial<T>) => Promise<void>
  delete: (id: string) => Promise<void>
  select: (id: string | null) => void
}

function createCrudStore<T extends Entity>(
  apiEndpoint: string
): StoreApi<CrudStore<T>> {
  return create<CrudStore<T>>()((set, get) => ({
    items: [],
    selectedId: null,
    isLoading: false,
    error: null,

    get selectedItem() {
      const { items, selectedId } = get()
      return items.find((item) => item.id === selectedId) ?? null
    },

    fetchAll: async () => {
      set({ isLoading: true, error: null })
      try {
        const response = await fetch(apiEndpoint)
        const items = await response.json()
        set({ items, isLoading: false })
      } catch (error) {
        set({ error: error.message, isLoading: false })
      }
    },

    fetchOne: async (id) => {
      set({ isLoading: true, error: null })
      try {
        const response = await fetch(`${apiEndpoint}/${id}`)
        const item = await response.json()
        set((state) => ({
          items: state.items.some((i) => i.id === id)
            ? state.items.map((i) => (i.id === id ? item : i))
            : [...state.items, item],
          isLoading: false,
        }))
      } catch (error) {
        set({ error: error.message, isLoading: false })
      }
    },

    create: async (data) => {
      set({ isLoading: true, error: null })
      try {
        const response = await fetch(apiEndpoint, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(data),
        })
        const newItem = await response.json()
        set((state) => ({
          items: [...state.items, newItem],
          isLoading: false,
        }))
      } catch (error) {
        set({ error: error.message, isLoading: false })
      }
    },

    update: async (id, data) => {
      set({ isLoading: true, error: null })
      try {
        const response = await fetch(`${apiEndpoint}/${id}`, {
          method: 'PATCH',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(data),
        })
        const updatedItem = await response.json()
        set((state) => ({
          items: state.items.map((item) =>
            item.id === id ? updatedItem : item
          ),
          isLoading: false,
        }))
      } catch (error) {
        set({ error: error.message, isLoading: false })
      }
    },

    delete: async (id) => {
      set({ isLoading: true, error: null })
      try {
        await fetch(`${apiEndpoint}/${id}`, { method: 'DELETE' })
        set((state) => ({
          items: state.items.filter((item) => item.id !== id),
          selectedId: state.selectedId === id ? null : state.selectedId,
          isLoading: false,
        }))
      } catch (error) {
        set({ error: error.message, isLoading: false })
      }
    },

    select: (id) => set({ selectedId: id }),
  }))
}

// Usage
interface Product extends Entity {
  price: number
  description: string
}

const useProductStore = createCrudStore<Product>('/api/products')
```

### Strongly Typed Actions

Use discriminated unions for type-safe action patterns:

```typescript
type Action =
  | { type: 'increment' }
  | { type: 'decrement' }
  | { type: 'set'; value: number }
  | { type: 'reset' }

interface CounterStore {
  count: number
  dispatch: (action: Action) => void
}

const useCounterStore = create<CounterStore>()((set) => ({
  count: 0,

  dispatch: (action) => {
    switch (action.type) {
      case 'increment':
        set((state) => ({ count: state.count + 1 }))
        break
      case 'decrement':
        set((state) => ({ count: state.count - 1 }))
        break
      case 'set':
        set({ count: action.value })
        break
      case 'reset':
        set({ count: 0 })
        break
    }
  },
}))

// Usage with full type safety
const dispatch = useCounterStore((state) => state.dispatch)
dispatch({ type: 'set', value: 10 }) // ✅ Type-safe
dispatch({ type: 'set', value: 'abc' }) // ❌ TypeScript error
```

## Common Patterns

### Namespace Pattern for Large Stores

Organize related state and actions:

```typescript
interface Store {
  auth: {
    user: User | null
    token: string | null
    login: (credentials: Credentials) => Promise<void>
    logout: () => void
  }
  cart: {
    items: CartItem[]
    addItem: (item: Product) => void
    removeItem: (id: string) => void
    clear: () => void
  }
}

const useStore = create<Store>()((set) => ({
  auth: {
    user: null,
    token: null,
    login: async (credentials) => {
      const { user, token } = await api.login(credentials)
      set((state) => ({
        auth: { ...state.auth, user, token },
      }))
    },
    logout: () =>
      set((state) => ({
        auth: { ...state.auth, user: null, token: null },
      })),
  },
  cart: {
    items: [],
    addItem: (product) =>
      set((state) => ({
        cart: {
          ...state.cart,
          items: [...state.cart.items, { ...product, quantity: 1 }],
        },
      })),
    removeItem: (id) =>
      set((state) => ({
        cart: {
          ...state.cart,
          items: state.cart.items.filter((item) => item.id !== id),
        },
      })),
    clear: () =>
      set((state) => ({
        cart: { ...state.cart, items: [] },
      })),
  },
}))

// Usage
const login = useStore((state) => state.auth.login)
const cartItems = useStore((state) => state.cart.items)
```

### Type-Safe Event Emitter

Create a typed event system:

```typescript
type Events = {
  'user:login': { userId: string; timestamp: Date }
  'user:logout': { userId: string }
  'cart:add': { productId: string; quantity: number }
  'cart:remove': { productId: string }
}

type EventListener<T extends keyof Events> = (data: Events[T]) => void

interface EventStore {
  listeners: {
    [K in keyof Events]?: EventListener<K>[]
  }
  on: <T extends keyof Events>(event: T, listener: EventListener<T>) => void
  off: <T extends keyof Events>(event: T, listener: EventListener<T>) => void
  emit: <T extends keyof Events>(event: T, data: Events[T]) => void
}

const useEventStore = create<EventStore>()((set, get) => ({
  listeners: {},

  on: (event, listener) => {
    set((state) => ({
      listeners: {
        ...state.listeners,
        [event]: [...(state.listeners[event] || []), listener],
      },
    }))
  },

  off: (event, listener) => {
    set((state) => ({
      listeners: {
        ...state.listeners,
        [event]: (state.listeners[event] || []).filter((l) => l !== listener),
      },
    }))
  },

  emit: (event, data) => {
    const listeners = get().listeners[event] || []
    listeners.forEach((listener) => listener(data))
  },
}))
```

## Anti-Patterns

### ❌ Don't Use `any` Types

```typescript
// Bad
const useStore = create<any>()((set) => ({
  data: null,
  setData: (data: any) => set({ data }),
}))

// Good
interface Store {
  data: User | null
  setData: (data: User | null) => void
}

const useStore = create<Store>()((set) => ({
  data: null,
  setData: (data) => set({ data }),
}))
```

### ❌ Don't Ignore Return Types

```typescript
// Bad: Ignoring return type
const useStore = create((set) => ({
  fetch: async () => {
    const data = await api.fetch()
    set({ data })
    // Missing return type
  },
}))

// Good: Explicit return types
interface Store {
  fetch: () => Promise<void>
}

const useStore = create<Store>()((set) => ({
  fetch: async (): Promise<void> => {
    const data = await api.fetch()
    set({ data })
  },
}))
```

### ❌ Don't Mix State and Actions in Types

```typescript
// Bad: Confusing structure
interface Store {
  count: number
  increment: () => void
  name: string
  setName: (name: string) => void
}

// Good: Separate concerns
interface StoreState {
  count: number
  name: string
}

interface StoreActions {
  increment: () => void
  setName: (name: string) => void
}

type Store = StoreState & StoreActions
```

## Related Skills

- **zustand-store-patterns**: Basic store creation and usage
- **zustand-middleware**: Using middleware with TypeScript
- **zustand-advanced-patterns**: Advanced TypeScript patterns and techniques
