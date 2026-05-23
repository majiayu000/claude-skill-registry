---
name: react
description: Auto-activates when user mentions React, hooks, components, JSX, or React patterns. Expert in React 18/19 best practices including Server Components, hooks, and performance optimization.
category: frontend
---

# React Best Practices

**Official React 18/19 guidelines - Hooks, Server Components, Performance, Patterns**

## Core Principles

1. **ALWAYS Use Hooks** - Functional components with hooks over class components
2. **Server Components by Default** - Client components only when needed ("use client")
3. **Proper Dependencies** - Always specify correct dependency arrays
4. **Cleanup Effects** - Return cleanup functions from useEffect
5. **Avoid Premature Optimization** - Use React.memo, useMemo, useCallback wisely

## React Hooks - Complete Guide

### useState - State Management

#### ✅ Good: Basic useState Patterns
```typescript
import { useState } from 'react'

// Simple state
function Counter() {
  const [count, setCount] = useState(0)

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => setCount(count + 1)}>Increment</button>
    </div>
  )
}

// Functional updates for derived state
function Counter() {
  const [count, setCount] = useState(0)

  const increment = () => {
    // ✅ Use functional update when new state depends on previous state
    setCount(prev => prev + 1)
  }

  const incrementByFive = () => {
    // ✅ Functional updates batch correctly
    setCount(prev => prev + 1)
    setCount(prev => prev + 1)
    setCount(prev => prev + 1)
    setCount(prev => prev + 1)
    setCount(prev => prev + 1)
  }

  return <button onClick={increment}>Count: {count}</button>
}

// Multiple state variables for independent values
function UserProfile() {
  const [name, setName] = useState('')
  const [age, setAge] = useState(0)
  const [email, setEmail] = useState('')

  return (
    <form>
      <input value={name} onChange={e => setName(e.target.value)} />
      <input value={age} onChange={e => setAge(Number(e.target.value))} />
      <input value={email} onChange={e => setEmail(e.target.value)} />
    </form>
  )
}

// Object state for related values
function UserProfile() {
  const [user, setUser] = useState({
    name: '',
    age: 0,
    email: ''
  })

  const updateName = (name: string) => {
    // ✅ Always spread previous state for object updates
    setUser(prev => ({ ...prev, name }))
  }

  return (
    <input 
      value={user.name} 
      onChange={e => updateName(e.target.value)} 
    />
  )
}

// Lazy initialization for expensive initial state
function ExpensiveComponent() {
  // ✅ Pass function to useState for lazy initialization
  const [data, setData] = useState(() => {
    const expensive = computeExpensiveValue()
    return expensive
  })

  return <div>{data}</div>
}
```

#### ❌ Bad: useState Anti-patterns
```typescript
// ❌ WRONG - Mutating state directly
function Counter() {
  const [count, setCount] = useState(0)

  const increment = () => {
    count++  // ❌ Direct mutation doesn't trigger re-render
    setCount(count)
  }
}

// ❌ WRONG - Not using functional updates
function Counter() {
  const [count, setCount] = useState(0)

  const incrementByFive = () => {
    setCount(count + 1)  // ❌ All updates use same count value
    setCount(count + 1)  // Only increments by 1, not 5
    setCount(count + 1)
  }
}

// ❌ WRONG - Mutating object state
function UserProfile() {
  const [user, setUser] = useState({ name: '', age: 0 })

  const updateName = (name: string) => {
    user.name = name  // ❌ Direct mutation
    setUser(user)     // ❌ Same object reference, no re-render
  }
}

// ❌ WRONG - Expensive computation on every render
function ExpensiveComponent() {
  const [data, setData] = useState(computeExpensiveValue())  // ❌ Runs on every render
}
```

### useEffect - Side Effects & External System Synchronization

#### ✅ Good: useEffect Patterns
```typescript
import { useEffect, useState } from 'react'

// Basic effect with cleanup
function ChatRoom({ roomId }: { roomId: string }) {
  useEffect(() => {
    const connection = createConnection(roomId)
    connection.connect()

    // ✅ Always return cleanup function
    return () => {
      connection.disconnect()
    }
  }, [roomId])  // ✅ Specify all dependencies

  return <div>Chat Room: {roomId}</div>
}

// Data fetching with race condition prevention
function UserProfile({ userId }: { userId: string }) {
  const [user, setUser] = useState<User | null>(null)

  useEffect(() => {
    let ignore = false  // ✅ Prevent race conditions

    async function fetchUser() {
      const data = await fetch(`/api/users/${userId}`).then(r => r.json())
      if (!ignore) {
        setUser(data)
      }
    }

    fetchUser()

    return () => {
      ignore = true  // ✅ Cleanup to ignore stale requests
    }
  }, [userId])

  return <div>{user?.name}</div>
}

// Event listener with cleanup
function WindowSize() {
  const [size, setSize] = useState({ width: 0, height: 0 })

  useEffect(() => {
    function handleResize() {
      setSize({ width: window.innerWidth, height: window.innerHeight })
    }

    window.addEventListener('resize', handleResize)
    handleResize()  // Set initial size

    // ✅ Remove event listener on cleanup
    return () => {
      window.removeEventListener('resize', handleResize)
    }
  }, [])  // ✅ Empty array - run once on mount

  return <div>{size.width} x {size.height}</div>
}

// Timer with cleanup
function Timer() {
  const [count, setCount] = useState(0)

  useEffect(() => {
    const interval = setInterval(() => {
      setCount(prev => prev + 1)
    }, 1000)

    // ✅ Clear interval on cleanup
    return () => clearInterval(interval)
  }, [])

  return <div>Seconds: {count}</div>
}

// Effect with multiple dependencies
function ProductPage({ productId, category }: Props) {
  const [product, setProduct] = useState<Product | null>(null)

  useEffect(() => {
    fetchProduct(productId, category).then(setProduct)
  }, [productId, category])  // ✅ All reactive values included

  return <div>{product?.name}</div>
}

// Conditional effect logic
function Component({ shouldSubscribe, channel }: Props) {
  useEffect(() => {
    if (!shouldSubscribe) {
      return  // ✅ Early return is OK
    }

    const subscription = subscribe(channel)
    return () => subscription.unsubscribe()
  }, [shouldSubscribe, channel])
}
```

#### ❌ Bad: useEffect Anti-patterns
```typescript
// ❌ WRONG - Missing dependencies
function ChatRoom({ roomId }: { roomId: string }) {
  useEffect(() => {
    const connection = createConnection(roomId)
    connection.connect()
    return () => connection.disconnect()
  }, [])  // ❌ Missing roomId dependency
}

// ❌ WRONG - No cleanup function
function ChatRoom({ roomId }: { roomId: string }) {
  useEffect(() => {
    const connection = createConnection(roomId)
    connection.connect()
    // ❌ Missing cleanup - connection leak
  }, [roomId])
}

// ❌ WRONG - Infinite loop
function BadComponent() {
  const [count, setCount] = useState(0)

  useEffect(() => {
    setCount(count + 1)  // ❌ Updates count, triggers re-render, runs effect again
  })  // ❌ No dependency array - runs after every render
}

// ❌ WRONG - Object/function dependencies causing unnecessary re-runs
function BadComponent() {
  const options = { filter: 'active' }  // ❌ New object every render

  useEffect(() => {
    fetchData(options)
  }, [options])  // ❌ Effect runs every render
}

// ❌ WRONG - Not handling race conditions
function UserProfile({ userId }: { userId: string }) {
  const [user, setUser] = useState<User | null>(null)

  useEffect(() => {
    fetch(`/api/users/${userId}`)
      .then(r => r.json())
      .then(setUser)  // ❌ No race condition handling
    // If userId changes quickly, older responses may overwrite newer ones
  }, [userId])
}

// ❌ WRONG - Using effect for derived state
function BadComponent({ items }: { items: Item[] }) {
  const [filteredItems, setFilteredItems] = useState<Item[]>([])

  useEffect(() => {
    setFilteredItems(items.filter(i => i.active))  // ❌ Don't use effect for this
  }, [items])

  // ✅ Better: Compute during render
  // const filteredItems = items.filter(i => i.active)
}
```

### useCallback - Memoizing Functions

#### ✅ Good: useCallback Patterns
```typescript
import { useCallback, memo } from 'react'

// Stable callback for child component
interface TodoItemProps {
  id: string
  onDelete: (id: string) => void
}

const TodoItem = memo(({ id, onDelete }: TodoItemProps) => {
  return <button onClick={() => onDelete(id)}>Delete</button>
})

function TodoList({ todos }: { todos: Todo[] }) {
  // ✅ useCallback prevents new function on every render
  const handleDelete = useCallback((id: string) => {
    deleteTodo(id)
  }, [])  // ✅ No dependencies - function never changes

  return (
    <div>
      {todos.map(todo => (
        <TodoItem key={todo.id} id={todo.id} onDelete={handleDelete} />
      ))}
    </div>
  )
}

// Callback with dependencies
function SearchBox({ category }: { category: string }) {
  const [query, setQuery] = useState('')

  const handleSearch = useCallback((value: string) => {
    // ✅ category is a dependency
    searchAPI(value, category)
  }, [category])  // ✅ Recreate when category changes

  return <input onChange={e => handleSearch(e.target.value)} />
}

// useCallback with useEffect
function DataFetcher({ userId }: { userId: string }) {
  const fetchData = useCallback(async () => {
    const data = await fetch(`/api/users/${userId}`).then(r => r.json())
    return data
  }, [userId])

  useEffect(() => {
    fetchData()
  }, [fetchData])  // ✅ fetchData is stable unless userId changes

  return <div>User Data</div>
}
```

#### ❌ Bad: useCallback Anti-patterns
```typescript
// ❌ WRONG - Premature optimization
function SimpleComponent() {
  // ❌ No need for useCallback if not passing to memoized child
  const handleClick = useCallback(() => {
    console.log('clicked')
  }, [])

  return <button onClick={handleClick}>Click</button>
}

// ❌ WRONG - Missing dependencies
function BadComponent({ userId, category }: Props) {
  const fetchData = useCallback(() => {
    fetch(`/api/data/${userId}/${category}`)  // Uses userId and category
  }, [])  // ❌ Missing dependencies

  useEffect(() => {
    fetchData()
  }, [fetchData])
}

// ❌ WRONG - Over-wrapping everything
function BadComponent() {
  const add = useCallback((a: number, b: number) => a + b, [])  // ❌ Unnecessary
  const subtract = useCallback((a: number, b: number) => a - b, [])  // ❌ Unnecessary
  const multiply = useCallback((a: number, b: number) => a * b, [])  // ❌ Unnecessary
}
```

### useMemo - Memoizing Computed Values

#### ✅ Good: useMemo Patterns
```typescript
import { useMemo, useState } from 'react'

// Expensive calculation
function ProductList({ products, filter }: Props) {
  // ✅ Memoize expensive filtering/sorting
  const filteredProducts = useMemo(() => {
    return products
      .filter(p => p.category === filter)
      .sort((a, b) => b.price - a.price)
  }, [products, filter])  // ✅ Recalculate when dependencies change

  return (
    <ul>
      {filteredProducts.map(p => (
        <li key={p.id}>{p.name}</li>
      ))}
    </ul>
  )
}

// Stable object reference
function TodoList({ todos }: { todos: Todo[] }) {
  // ✅ Prevent new object on every render
  const options = useMemo(() => ({
    filter: 'active',
    sort: 'date'
  }), [])

  useEffect(() => {
    fetchData(options)
  }, [options])  // ✅ options reference is stable

  return <div>Todos</div>
}

// Derived state from props
function Statistics({ data }: { data: number[] }) {
  // ✅ Memoize heavy calculations
  const stats = useMemo(() => {
    const sum = data.reduce((a, b) => a + b, 0)
    const mean = sum / data.length
    const variance = data.reduce((v, n) => v + Math.pow(n - mean, 2), 0) / data.length
    const stdDev = Math.sqrt(variance)
    
    return { sum, mean, variance, stdDev }
  }, [data])

  return <div>Mean: {stats.mean}, StdDev: {stats.stdDev}</div>
}

// Memoizing component instances
function ParentComponent({ data }: Props) {
  // ✅ Prevent creating new child element on every render
  const childElement = useMemo(() => {
    return <ExpensiveChild data={data} />
  }, [data])

  return <div>{childElement}</div>
}
```

#### ❌ Bad: useMemo Anti-patterns
```typescript
// ❌ WRONG - Memoizing simple operations
function BadComponent({ a, b }: { a: number, b: number }) {
  const sum = useMemo(() => a + b, [a, b])  // ❌ Simple addition doesn't need memoization
  const doubled = useMemo(() => a * 2, [a])  // ❌ Overhead > benefit
}

// ❌ WRONG - Missing dependencies
function BadComponent({ items, filter }: Props) {
  const filtered = useMemo(() => {
    return items.filter(i => i.category === filter)
  }, [items])  // ❌ Missing filter dependency
}

// ❌ WRONG - Over-optimization
function BadComponent() {
  const name = useMemo(() => 'John', [])  // ❌ Pointless
  const age = useMemo(() => 30, [])  // ❌ Overhead for no benefit
}

// ❌ WRONG - Memoizing everything
function BadComponent({ data }: Props) {
  const value1 = useMemo(() => data.field1, [data])  // ❌ Simple property access
  const value2 = useMemo(() => data.field2, [data])  // ❌ No calculation needed
  const value3 = useMemo(() => data.field3, [data])  // ❌ Over-optimization
}
```

### useRef - References & Mutable Values

#### ✅ Good: useRef Patterns
```typescript
import { useRef, useEffect } from 'react'

// DOM reference
function TextInput() {
  const inputRef = useRef<HTMLInputElement>(null)

  const focusInput = () => {
    // ✅ Access DOM node directly
    inputRef.current?.focus()
  }

  return (
    <div>
      <input ref={inputRef} />
      <button onClick={focusInput}>Focus Input</button>
    </div>
  )
}

// Store previous value
function Component({ value }: { value: number }) {
  const prevValueRef = useRef<number>()

  useEffect(() => {
    // ✅ useRef to track previous value without causing re-render
    prevValueRef.current = value
  }, [value])

  const prevValue = prevValueRef.current

  return <div>Current: {value}, Previous: {prevValue}</div>
}

// Mutable value that doesn't trigger re-renders
function Timer() {
  const [count, setCount] = useState(0)
  const intervalRef = useRef<number | null>(null)

  const startTimer = () => {
    if (intervalRef.current !== null) return

    // ✅ Store interval ID in ref
    intervalRef.current = setInterval(() => {
      setCount(c => c + 1)
    }, 1000)
  }

  const stopTimer = () => {
    if (intervalRef.current !== null) {
      clearInterval(intervalRef.current)
      intervalRef.current = null
    }
  }

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={startTimer}>Start</button>
      <button onClick={stopTimer}>Stop</button>
    </div>
  )
}

// Callback ref for dynamic measurements
function MeasureComponent() {
  const [height, setHeight] = useState(0)

  // ✅ Callback ref called whenever ref changes
  const measuredRef = useCallback((node: HTMLDivElement | null) => {
    if (node !== null) {
      setHeight(node.getBoundingClientRect().height)
    }
  }, [])

  return (
    <div ref={measuredRef}>
      <p>Height: {height}px</p>
    </div>
  )
}

// Storing latest callback without effect dependencies
function ChatRoom({ onMessage }: { onMessage: (msg: string) => void }) {
  const onMessageRef = useRef(onMessage)

  useEffect(() => {
    // ✅ Always use latest callback
    onMessageRef.current = onMessage
  }, [onMessage])

  useEffect(() => {
    const socket = connectToChat()
    socket.on('message', (msg) => {
      onMessageRef.current(msg)  // ✅ Always calls latest onMessage
    })
    return () => socket.disconnect()
  }, [])  // ✅ No need to include onMessage in deps
}
```

#### ❌ Bad: useRef Anti-patterns
```typescript
// ❌ WRONG - Using ref for state that should trigger renders
function BadCounter() {
  const countRef = useRef(0)

  const increment = () => {
    countRef.current++  // ❌ Increments but doesn't re-render
  }

  return <div>Count: {countRef.current}</div>  // ❌ UI won't update
}

// ❌ WRONG - Modifying ref during render
function BadComponent() {
  const renderCountRef = useRef(0)
  
  renderCountRef.current++  // ❌ Don't mutate refs during render

  // ✅ Better: Use useEffect
  useEffect(() => {
    renderCountRef.current++
  })
}

// ❌ WRONG - Not checking for null
function BadComponent() {
  const inputRef = useRef<HTMLInputElement>(null)

  const focusInput = () => {
    inputRef.current.focus()  // ❌ May be null
  }

  // ✅ Better: inputRef.current?.focus()
}
```

### useContext - Context API

#### ✅ Good: useContext Patterns
```typescript
import { createContext, useContext, useState } from 'react'

// Theme context
interface ThemeContextValue {
  theme: 'light' | 'dark'
  toggleTheme: () => void
}

const ThemeContext = createContext<ThemeContextValue | null>(null)

function ThemeProvider({ children }: { children: React.ReactNode }) {
  const [theme, setTheme] = useState<'light' | 'dark'>('light')

  const toggleTheme = () => {
    setTheme(prev => prev === 'light' ? 'dark' : 'light')
  }

  return (
    <ThemeContext.Provider value={{ theme, toggleTheme }}>
      {children}
    </ThemeContext.Provider>
  )
}

// ✅ Custom hook for context with error handling
function useTheme() {
  const context = useContext(ThemeContext)
  if (!context) {
    throw new Error('useTheme must be used within ThemeProvider')
  }
  return context
}

function Button() {
  const { theme, toggleTheme } = useTheme()
  
  return (
    <button 
      style={{ background: theme === 'light' ? '#fff' : '#000' }}
      onClick={toggleTheme}
    >
      Toggle Theme
    </button>
  )
}

// Auth context
interface User {
  id: string
  name: string
  email: string
}

interface AuthContextValue {
  user: User | null
  login: (email: string, password: string) => Promise<void>
  logout: () => void
}

const AuthContext = createContext<AuthContextValue | null>(null)

function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null)

  const login = async (email: string, password: string) => {
    const user = await loginAPI(email, password)
    setUser(user)
  }

  const logout = () => {
    setUser(null)
  }

  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

function useAuth() {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider')
  }
  return context
}

// Split context to prevent unnecessary re-renders
const UserContext = createContext<User | null>(null)
const UserDispatchContext = createContext<{
  login: (u: User) => void
  logout: () => void
} | null>(null)

function UserProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null)

  const login = (user: User) => setUser(user)
  const logout = () => setUser(null)

  return (
    <UserContext.Provider value={user}>
      <UserDispatchContext.Provider value={{ login, logout }}>
        {children}
      </UserDispatchContext.Provider>
    </UserContext.Provider>
  )
}

// ✅ Components can subscribe to only what they need
function UserName() {
  const user = useContext(UserContext)  // ✅ Only re-renders when user changes
  return <div>{user?.name}</div>
}

function LoginButton() {
  const { login, logout } = useContext(UserDispatchContext)!  // ✅ Never re-renders
  return <button onClick={logout}>Logout</button>
}
```

#### ❌ Bad: useContext Anti-patterns
```typescript
// ❌ WRONG - Context for frequently changing values
const AppContext = createContext<{
  count: number
  mousePosition: { x: number, y: number }
  items: Item[]
  // ... many other values
} | null>(null)

// ❌ All consumers re-render when any value changes

// ❌ WRONG - Not checking for null
function BadComponent() {
  const theme = useContext(ThemeContext)
  return <div>{theme.value}</div>  // ❌ May be null
}

// ❌ WRONG - Using context for all state
const GlobalContext = createContext<{
  user: User
  posts: Post[]
  comments: Comment[]
  notifications: Notification[]
  // ❌ Too much global state
} | null>(null)

// ✅ Better: Split into multiple contexts or use proper state management
```

### useReducer - Complex State Logic

#### ✅ Good: useReducer Patterns
```typescript
import { useReducer } from 'react'

// Form state with reducer
interface FormState {
  name: string
  email: string
  password: string
  errors: Record<string, string>
}

type FormAction =
  | { type: 'SET_FIELD'; field: string; value: string }
  | { type: 'SET_ERROR'; field: string; error: string }
  | { type: 'CLEAR_ERRORS' }
  | { type: 'RESET' }

const initialState: FormState = {
  name: '',
  email: '',
  password: '',
  errors: {}
}

function formReducer(state: FormState, action: FormAction): FormState {
  switch (action.type) {
    case 'SET_FIELD':
      return {
        ...state,
        [action.field]: action.value
      }
    case 'SET_ERROR':
      return {
        ...state,
        errors: { ...state.errors, [action.field]: action.error }
      }
    case 'CLEAR_ERRORS':
      return { ...state, errors: {} }
    case 'RESET':
      return initialState
    default:
      return state
  }
}

function RegistrationForm() {
  const [state, dispatch] = useReducer(formReducer, initialState)

  const handleChange = (field: string, value: string) => {
    dispatch({ type: 'SET_FIELD', field, value })
  }

  const handleSubmit = () => {
    // Validation logic
    if (!state.email.includes('@')) {
      dispatch({ type: 'SET_ERROR', field: 'email', error: 'Invalid email' })
    }
  }

  return (
    <form>
      <input 
        value={state.name} 
        onChange={e => handleChange('name', e.target.value)} 
      />
      <input 
        value={state.email} 
        onChange={e => handleChange('email', e.target.value)} 
      />
      {state.errors.email && <span>{state.errors.email}</span>}
    </form>
  )
}

// Shopping cart with reducer
interface CartItem {
  id: string
  name: string
  price: number
  quantity: number
}

interface CartState {
  items: CartItem[]
  total: number
}

type CartAction =
  | { type: 'ADD_ITEM'; item: Omit<CartItem, 'quantity'> }
  | { type: 'REMOVE_ITEM'; id: string }
  | { type: 'UPDATE_QUANTITY'; id: string; quantity: number }
  | { type: 'CLEAR_CART' }

function cartReducer(state: CartState, action: CartAction): CartState {
  switch (action.type) {
    case 'ADD_ITEM': {
      const existing = state.items.find(i => i.id === action.item.id)
      
      const items = existing
        ? state.items.map(i =>
            i.id === action.item.id
              ? { ...i, quantity: i.quantity + 1 }
              : i
          )
        : [...state.items, { ...action.item, quantity: 1 }]

      const total = items.reduce((sum, item) => sum + item.price * item.quantity, 0)

      return { items, total }
    }
    case 'REMOVE_ITEM': {
      const items = state.items.filter(i => i.id !== action.id)
      const total = items.reduce((sum, item) => sum + item.price * item.quantity, 0)
      return { items, total }
    }
    case 'UPDATE_QUANTITY': {
      const items = state.items.map(i =>
        i.id === action.id ? { ...i, quantity: action.quantity } : i
      )
      const total = items.reduce((sum, item) => sum + item.price * item.quantity, 0)
      return { items, total }
    }
    case 'CLEAR_CART':
      return { items: [], total: 0 }
    default:
      return state
  }
}

function ShoppingCart() {
  const [state, dispatch] = useReducer(cartReducer, { items: [], total: 0 })

  return (
    <div>
      <p>Total: ${state.total.toFixed(2)}</p>
      <button onClick={() => dispatch({ type: 'CLEAR_CART' })}>
        Clear Cart
      </button>
    </div>
  )
}
```

#### ❌ Bad: useReducer Anti-patterns
```typescript
// ❌ WRONG - Using useReducer for simple state
function BadCounter() {
  const [count, dispatch] = useReducer(
    (state: number, action: { type: 'INC' | 'DEC' }) => {
      return action.type === 'INC' ? state + 1 : state - 1
    },
    0
  )
  // ✅ Better: const [count, setCount] = useState(0)
}

// ❌ WRONG - Mutating state directly
function badReducer(state: State, action: Action): State {
  state.count++  // ❌ Mutation
  return state   // ❌ Same reference
}
```

### Custom Hooks - Reusable Logic

#### ✅ Good: Custom Hook Patterns
```typescript
// useFetch - Data fetching hook
function useFetch<T>(url: string) {
  const [data, setData] = useState<T | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<Error | null>(null)

  useEffect(() => {
    let ignore = false

    async function fetchData() {
      try {
        setLoading(true)
        const response = await fetch(url)
        const json = await response.json()
        
        if (!ignore) {
          setData(json)
          setError(null)
        }
      } catch (err) {
        if (!ignore) {
          setError(err as Error)
        }
      } finally {
        if (!ignore) {
          setLoading(false)
        }
      }
    }

    fetchData()

    return () => {
      ignore = true
    }
  }, [url])

  return { data, loading, error }
}

// Usage
function UserProfile({ userId }: { userId: string }) {
  const { data, loading, error } = useFetch<User>(`/api/users/${userId}`)

  if (loading) return <div>Loading...</div>
  if (error) return <div>Error: {error.message}</div>
  
  return <div>{data?.name}</div>
}

// useLocalStorage - Persist state in localStorage
function useLocalStorage<T>(key: string, initialValue: T) {
  const [storedValue, setStoredValue] = useState<T>(() => {
    try {
      const item = window.localStorage.getItem(key)
      return item ? JSON.parse(item) : initialValue
    } catch (error) {
      console.error(error)
      return initialValue
    }
  })

  const setValue = (value: T | ((val: T) => T)) => {
    try {
      const valueToStore = value instanceof Function ? value(storedValue) : value
      setStoredValue(valueToStore)
      window.localStorage.setItem(key, JSON.stringify(valueToStore))
    } catch (error) {
      console.error(error)
    }
  }

  return [storedValue, setValue] as const
}

// Usage
function Settings() {
  const [theme, setTheme] = useLocalStorage('theme', 'light')
  
  return (
    <button onClick={() => setTheme(theme === 'light' ? 'dark' : 'light')}>
      Theme: {theme}
    </button>
  )
}

// useDebounce - Debounce value changes
function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState(value)

  useEffect(() => {
    const timer = setTimeout(() => {
      setDebouncedValue(value)
    }, delay)

    return () => clearTimeout(timer)
  }, [value, delay])

  return debouncedValue
}

// Usage
function SearchBox() {
  const [query, setQuery] = useState('')
  const debouncedQuery = useDebounce(query, 500)

  useEffect(() => {
    if (debouncedQuery) {
      searchAPI(debouncedQuery)
    }
  }, [debouncedQuery])

  return <input value={query} onChange={e => setQuery(e.target.value)} />
}

// useOnClickOutside - Detect clicks outside element
function useOnClickOutside<T extends HTMLElement>(
  ref: React.RefObject<T>,
  handler: (event: MouseEvent | TouchEvent) => void
) {
  useEffect(() => {
    const listener = (event: MouseEvent | TouchEvent) => {
      if (!ref.current || ref.current.contains(event.target as Node)) {
        return
      }
      handler(event)
    }

    document.addEventListener('mousedown', listener)
    document.addEventListener('touchstart', listener)

    return () => {
      document.removeEventListener('mousedown', listener)
      document.removeEventListener('touchstart', listener)
    }
  }, [ref, handler])
}

// Usage
function Modal({ onClose }: { onClose: () => void }) {
  const modalRef = useRef<HTMLDivElement>(null)
  useOnClickOutside(modalRef, onClose)

  return (
    <div ref={modalRef}>
      <p>Modal Content</p>
    </div>
  )
}

// useMediaQuery - Responsive design hook
function useMediaQuery(query: string): boolean {
  const [matches, setMatches] = useState(false)

  useEffect(() => {
    const media = window.matchMedia(query)
    
    if (media.matches !== matches) {
      setMatches(media.matches)
    }

    const listener = () => setMatches(media.matches)
    media.addEventListener('change', listener)

    return () => media.removeEventListener('change', listener)
  }, [matches, query])

  return matches
}

// Usage
function ResponsiveComponent() {
  const isMobile = useMediaQuery('(max-width: 768px)')
  
  return <div>{isMobile ? 'Mobile View' : 'Desktop View'}</div>
}

// useInterval - Declarative interval
function useInterval(callback: () => void, delay: number | null) {
  const savedCallback = useRef(callback)

  useEffect(() => {
    savedCallback.current = callback
  }, [callback])

  useEffect(() => {
    if (delay === null) return

    const tick = () => savedCallback.current()
    const id = setInterval(tick, delay)

    return () => clearInterval(id)
  }, [delay])
}

// Usage
function Clock() {
  const [time, setTime] = useState(new Date())
  
  useInterval(() => {
    setTime(new Date())
  }, 1000)

  return <div>{time.toLocaleTimeString()}</div>
}
```

#### ❌ Bad: Custom Hook Anti-patterns
```typescript
// ❌ WRONG - Not starting with 'use' prefix
function fetchData() {  // ❌ Should be useFetchData
  const [data, setData] = useState(null)
  // ... violates Rules of Hooks
}

// ❌ WRONG - Over-abstracting simple logic
function useAddition(a: number, b: number) {  // ❌ Unnecessary hook
  return a + b
}

// ❌ WRONG - Not following hook rules
function useBadHook(condition: boolean) {
  if (condition) {
    const [state, setState] = useState(0)  // ❌ Conditional hook call
  }
}
```

## Component Patterns

### Composition Patterns

#### ✅ Good: Component Composition
```typescript
// Children prop pattern
function Card({ children }: { children: React.ReactNode }) {
  return (
    <div className="card">
      {children}
    </div>
  )
}

// Usage
function App() {
  return (
    <Card>
      <h2>Title</h2>
      <p>Content</p>
    </Card>
  )
}

// Slots pattern with multiple children
interface LayoutProps {
  header: React.ReactNode
  sidebar: React.ReactNode
  content: React.ReactNode
}

function Layout({ header, sidebar, content }: LayoutProps) {
  return (
    <div>
      <header>{header}</header>
      <aside>{sidebar}</aside>
      <main>{content}</main>
    </div>
  )
}

// Usage
function App() {
  return (
    <Layout
      header={<Header />}
      sidebar={<Sidebar />}
      content={<MainContent />}
    />
  )
}

// Render props pattern
interface MouseTrackerProps {
  render: (position: { x: number; y: number }) => React.ReactNode
}

function MouseTracker({ render }: MouseTrackerProps) {
  const [position, setPosition] = useState({ x: 0, y: 0 })

  useEffect(() => {
    const handleMove = (e: MouseEvent) => {
      setPosition({ x: e.clientX, y: e.clientY })
    }

    window.addEventListener('mousemove', handleMove)
    return () => window.removeEventListener('mousemove', handleMove)
  }, [])

  return <>{render(position)}</>
}

// Usage
function App() {
  return (
    <MouseTracker
      render={({ x, y }) => (
        <div>Mouse position: {x}, {y}</div>
      )}
    />
  )
}

// Compound components pattern
interface TabsContextValue {
  activeTab: string
  setActiveTab: (id: string) => void
}

const TabsContext = createContext<TabsContextValue | null>(null)

function Tabs({ children, defaultTab }: { 
  children: React.ReactNode
  defaultTab: string 
}) {
  const [activeTab, setActiveTab] = useState(defaultTab)

  return (
    <TabsContext.Provider value={{ activeTab, setActiveTab }}>
      <div className="tabs">{children}</div>
    </TabsContext.Provider>
  )
}

function TabList({ children }: { children: React.ReactNode }) {
  return <div className="tab-list">{children}</div>
}

function Tab({ id, children }: { id: string; children: React.ReactNode }) {
  const context = useContext(TabsContext)!
  const isActive = context.activeTab === id

  return (
    <button
      className={isActive ? 'active' : ''}
      onClick={() => context.setActiveTab(id)}
    >
      {children}
    </button>
  )
}

function TabPanel({ id, children }: { id: string; children: React.ReactNode }) {
  const context = useContext(TabsContext)!
  
  if (context.activeTab !== id) return null

  return <div className="tab-panel">{children}</div>
}

// Attach sub-components
Tabs.List = TabList
Tabs.Tab = Tab
Tabs.Panel = TabPanel

// Usage
function App() {
  return (
    <Tabs defaultTab="1">
      <Tabs.List>
        <Tabs.Tab id="1">Tab 1</Tabs.Tab>
        <Tabs.Tab id="2">Tab 2</Tabs.Tab>
      </Tabs.List>
      <Tabs.Panel id="1">Content 1</Tabs.Panel>
      <Tabs.Panel id="2">Content 2</Tabs.Panel>
    </Tabs>
  )
}
```

#### ❌ Bad: Composition Anti-patterns
```typescript
// ❌ WRONG - Prop drilling
function App() {
  const user = { name: 'John' }
  return <GrandParent user={user} />
}

function GrandParent({ user }: { user: User }) {
  return <Parent user={user} />
}

function Parent({ user }: { user: User }) {
  return <Child user={user} />
}

function Child({ user }: { user: User }) {
  return <div>{user.name}</div>
}

// ✅ Better: Use Context or composition
```

### Higher-Order Components (HOCs)

#### ✅ Good: HOC Patterns (Legacy)
```typescript
// withAuth HOC
function withAuth<P extends object>(
  Component: React.ComponentType<P>
) {
  return function AuthenticatedComponent(props: P) {
    const { user, loading } = useAuth()

    if (loading) return <div>Loading...</div>
    if (!user) return <Navigate to="/login" />

    return <Component {...props} />
  }
}

// Usage
const ProtectedPage = withAuth(Dashboard)

// withLogging HOC
function withLogging<P extends object>(
  Component: React.ComponentType<P>,
  componentName: string
) {
  return function LoggedComponent(props: P) {
    useEffect(() => {
      console.log(`${componentName} mounted`)
      return () => console.log(`${componentName} unmounted`)
    }, [])

    return <Component {...props} />
  }
}
```

#### ❌ Bad: HOC Anti-patterns
```typescript
// ❌ WRONG - Prefer custom hooks over HOCs in modern React
// HOCs create wrapper hell and naming collisions

// ✅ Better: Custom hook
function useAuth() {
  const { user, loading } = useAuthContext()
  
  if (loading) return { user: null, loading: true }
  if (!user) {
    // Redirect logic
  }

  return { user, loading: false }
}
```

### Controlled vs Uncontrolled Components

#### ✅ Good: Controlled Components
```typescript
// Controlled input
function ControlledForm() {
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    console.log({ name, email })
  }

  return (
    <form onSubmit={handleSubmit}>
      <input 
        value={name} 
        onChange={e => setName(e.target.value)} 
      />
      <input 
        value={email} 
        onChange={e => setEmail(e.target.value)} 
      />
      <button type="submit">Submit</button>
    </form>
  )
}
```

#### ✅ Good: Uncontrolled Components
```typescript
// Uncontrolled input with ref
function UncontrolledForm() {
  const nameRef = useRef<HTMLInputElement>(null)
  const emailRef = useRef<HTMLInputElement>(null)

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    console.log({
      name: nameRef.current?.value,
      email: emailRef.current?.value
    })
  }

  return (
    <form onSubmit={handleSubmit}>
      <input ref={nameRef} defaultValue="John" />
      <input ref={emailRef} />
      <button type="submit">Submit</button>
    </form>
  )
}
```

## Performance Optimization

### React.memo - Prevent Unnecessary Re-renders

#### ✅ Good: React.memo Usage
```typescript
import { memo } from 'react'

// Memoize expensive pure component
interface ProductCardProps {
  product: Product
  onAddToCart: (id: string) => void
}

const ProductCard = memo(({ product, onAddToCart }: ProductCardProps) => {
  console.log('Rendering ProductCard:', product.name)
  
  return (
    <div>
      <h3>{product.name}</h3>
      <p>${product.price}</p>
      <button onClick={() => onAddToCart(product.id)}>Add to Cart</button>
    </div>
  )
})

// Custom comparison function
const ProductCardWithCustomCompare = memo(
  ({ product, onAddToCart }: ProductCardProps) => {
    return (
      <div>
        <h3>{product.name}</h3>
        <p>${product.price}</p>
      </div>
    )
  },
  (prevProps, nextProps) => {
    // Return true if props are equal (skip re-render)
    return prevProps.product.id === nextProps.product.id &&
           prevProps.product.price === nextProps.product.price
  }
)

// Usage
function ProductList({ products }: { products: Product[] }) {
  const handleAddToCart = useCallback((id: string) => {
    // Add to cart logic
  }, [])

  return (
    <div>
      {products.map(product => (
        <ProductCard 
          key={product.id} 
          product={product} 
          onAddToCart={handleAddToCart} 
        />
      ))}
    </div>
  )
}
```

#### ❌ Bad: React.memo Anti-patterns
```typescript
// ❌ WRONG - Memoizing everything
const Text = memo(({ children }: { children: string }) => {
  return <p>{children}</p>  // ❌ Too simple to benefit from memo
})

// ❌ WRONG - Passing new objects/functions as props
function BadList() {
  return (
    <div>
      {items.map(item => (
        <MemoizedItem 
          item={item}
          onClick={() => console.log(item)}  // ❌ New function every render
          style={{ color: 'red' }}  // ❌ New object every render
        />
      ))}
    </div>
  )
}
```

### Code Splitting with React.lazy and Suspense

#### ✅ Good: Code Splitting Patterns
```typescript
import { lazy, Suspense } from 'react'

// Route-based code splitting
const Dashboard = lazy(() => import('./pages/Dashboard'))
const Settings = lazy(() => import('./pages/Settings'))
const Profile = lazy(() => import('./pages/Profile'))

function App() {
  return (
    <BrowserRouter>
      <Suspense fallback={<LoadingSpinner />}>
        <Routes>
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/settings" element={<Settings />} />
          <Route path="/profile" element={<Profile />} />
        </Routes>
      </Suspense>
    </BrowserRouter>
  )
}

// Component-based code splitting
const HeavyChart = lazy(() => import('./components/HeavyChart'))

function Analytics() {
  const [showChart, setShowChart] = useState(false)

  return (
    <div>
      <button onClick={() => setShowChart(true)}>Show Chart</button>
      
      {showChart && (
        <Suspense fallback={<div>Loading chart...</div>}>
          <HeavyChart />
        </Suspense>
      )}
    </div>
  )
}

// Named export code splitting
const Dashboard = lazy(() => 
  import('./pages/Dashboard').then(module => ({ default: module.Dashboard }))
)

// Error boundary with Suspense
class ErrorBoundary extends React.Component<
  { children: React.ReactNode },
  { hasError: boolean }
> {
  state = { hasError: false }

  static getDerivedStateFromError() {
    return { hasError: true }
  }

  render() {
    if (this.state.hasError) {
      return <div>Something went wrong</div>
    }

    return this.props.children
  }
}

function App() {
  return (
    <ErrorBoundary>
      <Suspense fallback={<LoadingSpinner />}>
        <LazyComponent />
      </Suspense>
    </ErrorBoundary>
  )
}
```

#### ❌ Bad: Code Splitting Anti-patterns
```typescript
// ❌ WRONG - Splitting too aggressively
const Button = lazy(() => import('./Button'))  // ❌ Too small
const Text = lazy(() => import('./Text'))  // ❌ Too small

// ❌ WRONG - No Suspense boundary
function BadApp() {
  const Component = lazy(() => import('./Component'))
  return <Component />  // ❌ Error: lazy components must be wrapped in Suspense
}
```

### Virtual Lists for Large Datasets

#### ✅ Good: Virtual List Usage
```typescript
import { FixedSizeList } from 'react-window'

// Virtual list with react-window
function VirtualizedList({ items }: { items: Item[] }) {
  const Row = ({ index, style }: { index: number; style: React.CSSProperties }) => (
    <div style={style}>
      {items[index].name}
    </div>
  )

  return (
    <FixedSizeList
      height={600}
      itemCount={items.length}
      itemSize={50}
      width="100%"
    >
      {Row}
    </FixedSizeList>
  )
}

// When to use: Lists with 100+ items
function ProductList({ products }: { products: Product[] }) {
  // ✅ Use virtualization for large lists
  if (products.length > 100) {
    return <VirtualizedList items={products} />
  }

  // Regular rendering for small lists
  return (
    <div>
      {products.map(p => (
        <ProductCard key={p.id} product={p} />
      ))}
    </div>
  )
}
```

### Profiling and Performance Measurement

#### ✅ Good: Performance Profiling
```typescript
import { Profiler } from 'react'

// React Profiler component
function App() {
  const onRenderCallback = (
    id: string,
    phase: 'mount' | 'update',
    actualDuration: number,
    baseDuration: number,
    startTime: number,
    commitTime: number
  ) => {
    console.log(`${id} (${phase}) took ${actualDuration}ms`)
  }

  return (
    <Profiler id="App" onRender={onRenderCallback}>
      <Dashboard />
    </Profiler>
  )
}

// Performance marks
function ExpensiveComponent() {
  useEffect(() => {
    performance.mark('expensive-start')
    
    // Expensive operation
    doExpensiveWork()
    
    performance.mark('expensive-end')
    performance.measure('expensive-operation', 'expensive-start', 'expensive-end')
    
    const measure = performance.getEntriesByName('expensive-operation')[0]
    console.log(`Operation took ${measure.duration}ms`)
  }, [])
}
```

## Server Components vs Client Components

### When to Use Server Components

#### ✅ Good: Server Component Patterns
```typescript
// app/products/page.tsx - Server Component (default in Next.js App Router)
async function ProductsPage() {
  // ✅ Direct database access in Server Component
  const products = await db.product.findMany()

  // ✅ Server-side data fetching
  const categories = await fetch('https://api.example.com/categories').then(r => r.json())

  // ✅ Access environment variables safely
  const apiKey = process.env.API_KEY

  return (
    <div>
      <h1>Products</h1>
      {products.map(product => (
        <ProductCard key={product.id} product={product} />
      ))}
    </div>
  )
}

// Server Component benefits:
// - No JavaScript sent to client
// - Direct database/API access
// - Secure (API keys, secrets safe)
// - Faster initial load
// - Better SEO
```

### When to Use Client Components

#### ✅ Good: Client Component Patterns
```typescript
// components/SearchBox.tsx - Client Component
'use client'  // ✅ Directive at top of file

import { useState } from 'react'

export function SearchBox() {
  // ✅ Client Component for interactivity
  const [query, setQuery] = useState('')

  return (
    <input 
      value={query} 
      onChange={e => setQuery(e.target.value)}  // ✅ Event handlers
      placeholder="Search..."
    />
  )
}

// Client Component use cases:
// - useState, useEffect, other hooks
// - Event handlers (onClick, onChange, etc.)
// - Browser APIs (localStorage, window, etc.)
// - Interactivity and state
```

### Composing Server and Client Components

#### ✅ Good: Server + Client Composition
```typescript
// app/page.tsx - Server Component
import { SearchBox } from '@/components/SearchBox'  // Client Component
import { ProductList } from '@/components/ProductList'  // Server Component

async function HomePage() {
  const products = await fetchProducts()

  return (
    <div>
      {/* ✅ Client Component for interactivity */}
      <SearchBox />
      
      {/* ✅ Server Component for data fetching */}
      <ProductList products={products} />
    </div>
  )
}

// ✅ Pass Server Components as children to Client Components
// components/ClientWrapper.tsx
'use client'

export function ClientWrapper({ children }: { children: React.ReactNode }) {
  const [isOpen, setIsOpen] = useState(false)

  return (
    <div>
      <button onClick={() => setIsOpen(!isOpen)}>Toggle</button>
      {isOpen && children}  {/* ✅ Server Component as children */}
    </div>
  )
}

// app/page.tsx
function Page() {
  return (
    <ClientWrapper>
      <ServerComponent />  {/* ✅ Works! */}
    </ClientWrapper>
  )
}
```

#### ❌ Bad: Server/Client Component Anti-patterns
```typescript
// ❌ WRONG - Importing Server Component into Client Component
'use client'

import { ServerComponent } from './ServerComponent'  // ❌ Error!

export function ClientComponent() {
  return <ServerComponent />  // ❌ Won't work
}

// ❌ WRONG - Using hooks in Server Component
async function ServerComponent() {
  const [state, setState] = useState(0)  // ❌ Error: hooks not allowed
  
  useEffect(() => {  // ❌ Error: hooks not allowed
    // ...
  }, [])
}

// ❌ WRONG - Event handlers in Server Component
async function ServerComponent() {
  return (
    <button onClick={() => console.log('click')}>  {/* ❌ Error */}
      Click
    </button>
  )
}

// ❌ WRONG - Unnecessary Client Components
'use client'  // ❌ Not needed if no interactivity

export function StaticComponent() {
  return <div>Static content</div>  // ✅ Should be Server Component
}
```

## Error Handling

### Error Boundaries

#### ✅ Good: Error Boundary Patterns
```typescript
import React from 'react'

interface ErrorBoundaryProps {
  children: React.ReactNode
  fallback?: React.ReactNode
}

interface ErrorBoundaryState {
  hasError: boolean
  error: Error | null
}

class ErrorBoundary extends React.Component<ErrorBoundaryProps, ErrorBoundaryState> {
  constructor(props: ErrorBoundaryProps) {
    super(props)
    this.state = { hasError: false, error: null }
  }

  static getDerivedStateFromError(error: Error): ErrorBoundaryState {
    return { hasError: true, error }
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    // ✅ Log error to error reporting service
    console.error('Error caught by boundary:', error, errorInfo)
    // logErrorToService(error, errorInfo)
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback || (
        <div>
          <h2>Something went wrong</h2>
          <details>
            <summary>Error details</summary>
            <pre>{this.state.error?.message}</pre>
          </details>
        </div>
      )
    }

    return this.props.children
  }
}

// Usage
function App() {
  return (
    <ErrorBoundary fallback={<ErrorFallback />}>
      <Dashboard />
    </ErrorBoundary>
  )
}

// Multiple error boundaries for granular error handling
function Page() {
  return (
    <div>
      <ErrorBoundary fallback={<div>Header failed to load</div>}>
        <Header />
      </ErrorBoundary>
      
      <ErrorBoundary fallback={<div>Main content failed to load</div>}>
        <MainContent />
      </ErrorBoundary>
      
      <ErrorBoundary fallback={<div>Sidebar failed to load</div>}>
        <Sidebar />
      </ErrorBoundary>
    </div>
  )
}
```

### Suspense for Data Fetching

#### ✅ Good: Suspense Patterns
```typescript
import { Suspense } from 'react'

// Suspense with fallback
function App() {
  return (
    <Suspense fallback={<LoadingSpinner />}>
      <UserProfile />
    </Suspense>
  )
}

// Multiple Suspense boundaries
function Page() {
  return (
    <div>
      <Suspense fallback={<HeaderSkeleton />}>
        <Header />
      </Suspense>
      
      <Suspense fallback={<ContentSkeleton />}>
        <MainContent />
      </Suspense>
    </div>
  )
}

// Suspense + Error Boundary
function App() {
  return (
    <ErrorBoundary fallback={<ErrorPage />}>
      <Suspense fallback={<LoadingPage />}>
        <Dashboard />
      </Suspense>
    </ErrorBoundary>
  )
}
```

## State Management

### When to Use Context vs External Libraries

#### ✅ Good: Context for Simple State
```typescript
// ✅ Context for theme, auth, i18n
const ThemeContext = createContext<Theme>('light')
const AuthContext = createContext<AuthState | null>(null)
const I18nContext = createContext<I18nState>({ locale: 'en' })

// ✅ Context for infrequently changing data
function App() {
  const [theme, setTheme] = useState<Theme>('light')

  return (
    <ThemeContext.Provider value={theme}>
      <Dashboard />
    </ThemeContext.Provider>
  )
}
```

#### ✅ Good: External Libraries for Complex State
```typescript
// Zustand for complex client state
import { create } from 'zustand'

interface CartStore {
  items: CartItem[]
  addItem: (item: CartItem) => void
  removeItem: (id: string) => void
  clearCart: () => void
}

const useCartStore = create<CartStore>((set) => ({
  items: [],
  addItem: (item) => set((state) => ({ items: [...state.items, item] })),
  removeItem: (id) => set((state) => ({ items: state.items.filter(i => i.id !== id) })),
  clearCart: () => set({ items: [] })
}))

// Usage
function ShoppingCart() {
  const { items, removeItem } = useCartStore()

  return (
    <div>
      {items.map(item => (
        <div key={item.id}>
          {item.name}
          <button onClick={() => removeItem(item.id)}>Remove</button>
        </div>
      ))}
    </div>
  )
}
```

### State Management Comparison

```typescript
// Context: Simple, infrequent updates
// ✅ Theme, auth, i18n
// ❌ Frequent updates, complex logic

// Zustand: Simple external state
// ✅ Client-side shopping cart, UI state
// ❌ Server state (use React Query instead)

// Jotai: Atomic state management
// ✅ Fine-grained reactivity
// ❌ Overkill for simple cases

// Redux: Complex enterprise apps
// ✅ Time-travel debugging, complex middleware
// ❌ Boilerplate, learning curve
```

## Best Practices Checklist

### Key Prop Usage
```typescript
// ✅ Use unique, stable keys
{items.map(item => (
  <Item key={item.id} data={item} />  // ✅ Unique ID
))}

// ❌ Avoid index as key
{items.map((item, index) => (
  <Item key={index} data={item} />  // ❌ Index can cause bugs
))}

// ✅ Key for conditional rendering
{showA ? <ComponentA key="a" /> : <ComponentB key="b" />}
```

### Fragment Usage
```typescript
// ✅ Use fragments to avoid extra DOM nodes
function Component() {
  return (
    <>
      <Header />
      <Main />
      <Footer />
    </>
  )
}

// ✅ Fragment with key
{items.map(item => (
  <React.Fragment key={item.id}>
    <dt>{item.term}</dt>
    <dd>{item.description}</dd>
  </React.Fragment>
))}
```

### Event Handler Naming
```typescript
// ✅ Consistent naming: handle* for handlers
function Form() {
  const handleSubmit = (e: React.FormEvent) => { /* ... */ }
  const handleChange = (e: React.ChangeEvent) => { /* ... */ }
  const handleClick = () => { /* ... */ }

  return (
    <form onSubmit={handleSubmit}>
      <input onChange={handleChange} />
      <button onClick={handleClick}>Submit</button>
    </form>
  )
}
```

### File Organization
```
src/
├── components/
│   ├── ui/              # Reusable UI components
│   │   ├── Button.tsx
│   │   ├── Input.tsx
│   │   └── Card.tsx
│   ├── features/        # Feature-specific components
│   │   ├── auth/
│   │   └── products/
├── hooks/               # Custom hooks
│   ├── useFetch.ts
│   ├── useDebounce.ts
│   └── useLocalStorage.ts
├── contexts/            # Context providers
│   ├── ThemeContext.tsx
│   └── AuthContext.tsx
├── utils/               # Utility functions
├── types/               # TypeScript types
└── pages/               # Page components
```

### TypeScript Integration
```typescript
// ✅ Type props interfaces
interface ButtonProps {
  children: React.ReactNode
  onClick: () => void
  variant?: 'primary' | 'secondary'
}

export function Button({ children, onClick, variant = 'primary' }: ButtonProps) {
  return <button onClick={onClick}>{children}</button>
}

// ✅ Type event handlers
const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
  console.log(e.target.value)
}

// ✅ Type refs
const inputRef = useRef<HTMLInputElement>(null)
```

### Testing Approaches
```typescript
// Component testing with React Testing Library
import { render, screen, fireEvent } from '@testing-library/react'

test('Counter increments', () => {
  render(<Counter />)
  
  const button = screen.getByText('Increment')
  fireEvent.click(button)
  
  expect(screen.getByText('Count: 1')).toBeInTheDocument()
})

// Hook testing
import { renderHook, act } from '@testing-library/react'

test('useFetch returns data', async () => {
  const { result } = renderHook(() => useFetch('/api/data'))
  
  await waitFor(() => {
    expect(result.current.data).toBeTruthy()
  })
})
```

## Performance Tips Summary

1. **Use Server Components by default** - Only opt into Client Components when needed
2. **Code split by route** - Lazy load pages and heavy components
3. **Virtualize large lists** - Use react-window for 100+ items
4. **Memoize wisely** - Don't over-optimize simple components
5. **Stable callbacks** - Use useCallback for props passed to memoized children
6. **Debounce expensive operations** - Search, API calls, complex calculations
7. **Batch state updates** - Use functional updates when updating related state
8. **Profile before optimizing** - Use React DevTools Profiler to find real bottlenecks

## Links to Official Documentation

- [React Official Docs](https://react.dev)
- [React Hooks Reference](https://react.dev/reference/react/hooks)
- [React Server Components](https://react.dev/reference/rsc/server-components)
- [React Performance](https://react.dev/learn/render-and-commit)
- [TypeScript with React](https://react.dev/learn/typescript)
