---
name: zustand-store-patterns
description: Use when creating and managing Zustand stores for React state management. Covers store creation, selectors, actions, and basic usage patterns.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
---

# Zustand - Store Patterns

Zustand is a small, fast, and scalable state management solution for React. It uses a simplified flux principles with a hooks-based API.

## Key Concepts

### Store Creation

A Zustand store is created using the `create` function:

```typescript
import { create } from 'zustand'

interface BearStore {
  bears: number
  increasePopulation: () => void
  removeAllBears: () => void
}

const useBearStore = create<BearStore>((set) => ({
  bears: 0,
  increasePopulation: () => set((state) => ({ bears: state.bears + 1 })),
  removeAllBears: () => set({ bears: 0 }),
}))
```

### Using the Store in Components

```typescript
function BearCounter() {
  const bears = useBearStore((state) => state.bears)
  return <h1>{bears} around here...</h1>
}

function Controls() {
  const increasePopulation = useBearStore((state) => state.increasePopulation)
  return <button onClick={increasePopulation}>Add bear</button>
}
```

### State Updates

Zustand provides two ways to update state:

```typescript
// Replace state
set({ bears: 5 })

// Merge state (shallow merge)
set((state) => ({ bears: state.bears + 1 }))
```

## Best Practices

### 1. Use Selectors for Performance

Select only the state you need to prevent unnecessary re-renders:

```typescript
// ❌ Bad: Component re-renders on any state change
function BadComponent() {
  const store = useBearStore()
  return <div>{store.bears}</div>
}

// ✅ Good: Component only re-renders when bears changes
function GoodComponent() {
  const bears = useBearStore((state) => state.bears)
  return <div>{bears}</div>
}
```

### 2. Separate Actions from State

Keep your store organized by separating data from actions:

```typescript
interface TodoStore {
  // State
  todos: Todo[]
  filter: 'all' | 'active' | 'completed'

  // Actions
  addTodo: (text: string) => void
  toggleTodo: (id: string) => void
  removeTodo: (id: string) => void
  setFilter: (filter: TodoStore['filter']) => void
}

const useTodoStore = create<TodoStore>((set) => ({
  todos: [],
  filter: 'all',

  addTodo: (text) =>
    set((state) => ({
      todos: [...state.todos, { id: Date.now().toString(), text, completed: false }],
    })),

  toggleTodo: (id) =>
    set((state) => ({
      todos: state.todos.map((todo) =>
        todo.id === id ? { ...todo, completed: !todo.completed } : todo
      ),
    })),

  removeTodo: (id) =>
    set((state) => ({
      todos: state.todos.filter((todo) => todo.id !== id),
    })),

  setFilter: (filter) => set({ filter }),
}))
```

### 3. Use Shallow Equality for Multiple Selectors

When selecting multiple values, use `shallow` from `zustand/shallow`:

```typescript
import { create } from 'zustand'
import { shallow } from 'zustand/shallow'

const useStore = create<Store>((set) => ({
  nuts: 0,
  honey: 0,
  increaseNuts: () => set((state) => ({ nuts: state.nuts + 1 })),
  increaseHoney: () => set((state) => ({ honey: state.honey + 1 })),
}))

// ✅ Using shallow comparison
function Component() {
  const { nuts, honey } = useStore(
    (state) => ({ nuts: state.nuts, honey: state.honey }),
    shallow
  )
  return <div>{nuts} nuts, {honey} honey</div>
}
```

### 4. Organize Large Stores with Slices

For complex applications, split stores into logical slices:

```typescript
interface UserSlice {
  user: User | null
  login: (credentials: Credentials) => Promise<void>
  logout: () => void
}

interface CartSlice {
  items: CartItem[]
  addItem: (item: Product) => void
  removeItem: (id: string) => void
  clearCart: () => void
}

const createUserSlice = (set: StateCreator<UserSlice>) => ({
  user: null,
  login: async (credentials) => {
    const user = await api.login(credentials)
    set({ user })
  },
  logout: () => set({ user: null }),
})

const createCartSlice = (set: StateCreator<CartSlice>) => ({
  items: [],
  addItem: (product) =>
    set((state) => ({
      items: [...state.items, { ...product, quantity: 1 }],
    })),
  removeItem: (id) =>
    set((state) => ({
      items: state.items.filter((item) => item.id !== id),
    })),
  clearCart: () => set({ items: [] }),
})

const useStore = create<UserSlice & CartSlice>()((...a) => ({
  ...createUserSlice(...a),
  ...createCartSlice(...a),
}))
```

### 5. Access Store Outside Components

Use `getState` and `setState` for non-reactive access:

```typescript
const useBearStore = create<BearStore>((set, get) => ({
  bears: 0,
  increasePopulation: () => set((state) => ({ bears: state.bears + 1 })),
  doSomething: () => {
    const currentBears = get().bears
    console.log(`Current bears: ${currentBears}`)
  },
}))

// Outside components
const currentState = useBearStore.getState()
useBearStore.setState({ bears: 10 })
```

## Examples

### Simple Counter Store

```typescript
import { create } from 'zustand'

interface CounterStore {
  count: number
  increment: () => void
  decrement: () => void
  reset: () => void
}

export const useCounterStore = create<CounterStore>((set) => ({
  count: 0,
  increment: () => set((state) => ({ count: state.count + 1 })),
  decrement: () => set((state) => ({ count: state.count - 1 })),
  reset: () => set({ count: 0 }),
}))

// Usage
function Counter() {
  const { count, increment, decrement, reset } = useCounterStore()

  return (
    <div>
      <h1>Count: {count}</h1>
      <button onClick={increment}>+</button>
      <button onClick={decrement}>-</button>
      <button onClick={reset}>Reset</button>
    </div>
  )
}
```

### Shopping Cart Store

```typescript
import { create } from 'zustand'

interface CartItem {
  id: string
  name: string
  price: number
  quantity: number
}

interface CartStore {
  items: CartItem[]
  addItem: (product: Omit<CartItem, 'quantity'>) => void
  removeItem: (id: string) => void
  updateQuantity: (id: string, quantity: number) => void
  clearCart: () => void
  total: number
}

export const useCartStore = create<CartStore>((set, get) => ({
  items: [],

  addItem: (product) =>
    set((state) => {
      const existingItem = state.items.find((item) => item.id === product.id)

      if (existingItem) {
        return {
          items: state.items.map((item) =>
            item.id === product.id
              ? { ...item, quantity: item.quantity + 1 }
              : item
          ),
        }
      }

      return {
        items: [...state.items, { ...product, quantity: 1 }],
      }
    }),

  removeItem: (id) =>
    set((state) => ({
      items: state.items.filter((item) => item.id !== id),
    })),

  updateQuantity: (id, quantity) =>
    set((state) => ({
      items: state.items.map((item) =>
        item.id === id ? { ...item, quantity } : item
      ),
    })),

  clearCart: () => set({ items: [] }),

  get total() {
    return get().items.reduce(
      (sum, item) => sum + item.price * item.quantity,
      0
    )
  },
}))
```

### Authentication Store

```typescript
import { create } from 'zustand'

interface User {
  id: string
  email: string
  name: string
}

interface AuthStore {
  user: User | null
  token: string | null
  isLoading: boolean
  error: string | null

  login: (email: string, password: string) => Promise<void>
  logout: () => void
  checkAuth: () => Promise<void>
}

export const useAuthStore = create<AuthStore>((set) => ({
  user: null,
  token: null,
  isLoading: false,
  error: null,

  login: async (email, password) => {
    set({ isLoading: true, error: null })

    try {
      const response = await fetch('/api/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
      })

      if (!response.ok) {
        throw new Error('Login failed')
      }

      const { user, token } = await response.json()
      set({ user, token, isLoading: false })
      localStorage.setItem('token', token)
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : 'Login failed',
        isLoading: false,
      })
    }
  },

  logout: () => {
    localStorage.removeItem('token')
    set({ user: null, token: null })
  },

  checkAuth: async () => {
    const token = localStorage.getItem('token')
    if (!token) return

    set({ isLoading: true })

    try {
      const response = await fetch('/api/me', {
        headers: { Authorization: `Bearer ${token}` },
      })

      if (!response.ok) {
        throw new Error('Auth check failed')
      }

      const user = await response.json()
      set({ user, token, isLoading: false })
    } catch (error) {
      localStorage.removeItem('token')
      set({ user: null, token: null, isLoading: false })
    }
  },
}))
```

## Common Patterns

### Computed Values

Use getters for derived state:

```typescript
const useStore = create<Store>((set, get) => ({
  items: [],

  get itemCount() {
    return get().items.length
  },

  get hasItems() {
    return get().items.length > 0
  },
}))
```

### Async Actions

Handle async operations within actions:

```typescript
const useStore = create<Store>((set) => ({
  data: null,
  isLoading: false,
  error: null,

  fetchData: async () => {
    set({ isLoading: true, error: null })

    try {
      const data = await api.fetchData()
      set({ data, isLoading: false })
    } catch (error) {
      set({ error: error.message, isLoading: false })
    }
  },
}))
```

### Reset Store

Implement a reset action:

```typescript
const initialState = {
  count: 0,
  name: '',
}

const useStore = create<Store>((set) => ({
  ...initialState,

  increment: () => set((state) => ({ count: state.count + 1 })),
  setName: (name: string) => set({ name }),
  reset: () => set(initialState),
}))
```

## Anti-Patterns

### ❌ Don't Mutate State Directly

```typescript
// Bad
const useStore = create((set) => ({
  items: [],
  addItem: (item) => {
    // DON'T mutate state directly
    items.push(item)
  },
}))

// Good
const useStore = create((set) => ({
  items: [],
  addItem: (item) =>
    set((state) => ({
      items: [...state.items, item],
    })),
}))
```

### ❌ Don't Select the Entire Store

```typescript
// Bad: Causes re-render on any state change
const store = useStore()

// Good: Select only what you need
const count = useStore((state) => state.count)
```

### ❌ Don't Use External State in Selectors

```typescript
// Bad: Selector depends on external value
const [userId, setUserId] = useState('123')
const user = useStore((state) => state.users[userId])

// Good: Pass external values as arguments
const getUser = (userId: string) => useStore.getState().users[userId]
```

### ❌ Don't Create Multiple Stores for Related Data

```typescript
// Bad: Splitting related state across stores
const useUserStore = create(...)
const useUserSettingsStore = create(...)
const useUserPreferencesStore = create(...)

// Good: Keep related state together
const useUserStore = create((set) => ({
  profile: null,
  settings: {},
  preferences: {},
}))
```

## Related Skills

- **zustand-typescript**: TypeScript integration and type safety patterns
- **zustand-middleware**: Using persist, devtools, and immer middleware
- **zustand-advanced-patterns**: Subscriptions, transient updates, and advanced techniques
