---
name: react-concurrency-and-memoization
version: "1.0"
description: >
  React 18+ concurrency features and strategic memoization techniques.
  PROACTIVELY activate for: (1) Using useTransition for non-urgent updates, (2) useDeferredValue for deferred rendering,
  (3) Strategic useMemo and useCallback, (4) React.memo for expensive components, (5) Profiling re-renders.
  Triggers: "react performance", "useTransition", "useDeferredValue", "useMemo", "useCallback", "React.memo", "re-render", "bottleneck", "profiler"
core-integration:
  techniques:
    primary: ["systematic_analysis"]
    secondary: ["structured_evaluation"]
  contracts:
    input: "none"
    output: "none"
  patterns: "none"
  rubrics: "none"
---

# React Concurrency and Memoization

This skill teaches the modern React performance paradigm, focusing on leveraging concurrent features to maintain UI responsiveness and applying memoization techniques strategically to prevent unnecessary computational work and re-renders.

## Concurrent Rendering Model

React 18 introduced a fundamental shift from blocking, synchronous rendering to interruptible, concurrent rendering. This enables React to prepare multiple versions of the UI simultaneously and prioritize urgent updates over less important ones.

### Key Concepts

**Urgent updates**: User interactions that should feel immediate (typing, clicking, hovering)
**Transition updates**: Non-urgent UI updates that can be deferred (search results, navigation)

React can now interrupt rendering of a transition to handle urgent updates, keeping the UI responsive.

## Strategic Concurrency with useTransition

The `useTransition` hook marks state updates as non-urgent transitions, allowing React to keep the UI responsive by de-prioritizing heavy rendering work.

### Basic Pattern

```tsx
import { useState, useTransition } from 'react'

function SearchPage() {
  const [query, setQuery] = useState('')
  const [results, setResults] = useState([])
  const [isPending, startTransition] = useTransition()

  function handleChange(e: React.ChangeEvent<HTMLInputElement>) {
    const value = e.target.value

    // Urgent: Update input immediately
    setQuery(value)

    // Non-urgent: Defer expensive search computation
    startTransition(() => {
      const searchResults = performExpensiveSearch(value)
      setResults(searchResults)
    })
  }

  return (
    <div>
      <input value={query} onChange={handleChange} />
      {isPending && <Spinner />}
      <SearchResults results={results} />
    </div>
  )
}
```

The input field stays responsive while search results are computed in the background.

### Tab Switching Pattern

```tsx
function TabContainer() {
  const [activeTab, setActiveTab] = useState('about')
  const [isPending, startTransition] = useTransition()

  function selectTab(tab: string) {
    startTransition(() => {
      setActiveTab(tab)
    })
  }

  return (
    <>
      <TabButtons active={activeTab} onSelect={selectTab} />
      {isPending && <Spinner />}
      <TabContent tab={activeTab} />
    </>
  )
}
```

### Conditional Rendering Optimization

```tsx
function FilteredList({ items }: { items: Item[] }) {
  const [filter, setFilter] = useState('')
  const [filteredItems, setFilteredItems] = useState(items)
  const [isPending, startTransition] = useTransition()

  function handleFilterChange(value: string) {
    setFilter(value) // Urgent: Update input

    startTransition(() => {
      // Non-urgent: Filter large list
      const filtered = items.filter(item =>
        item.name.toLowerCase().includes(value.toLowerCase())
      )
      setFilteredItems(filtered)
    })
  }

  return (
    <>
      <input
        value={filter}
        onChange={(e) => handleFilterChange(e.target.value)}
        placeholder="Filter items..."
      />
      <div className={isPending ? 'loading' : ''}>
        {filteredItems.map(item => <ListItem key={item.id} item={item} />)}
      </div>
    </>
  )
}
```

## Deferring Values with useDeferredValue

The `useDeferredValue` hook creates a deferred version of a value, allowing React to prioritize rendering other parts of the UI first.

### Basic Pattern

```tsx
import { useState, useDeferredValue, memo } from 'react'

function App() {
  const [query, setQuery] = useState('')
  const deferredQuery = useDeferredValue(query)

  return (
    <>
      <input
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />
      {/* This component re-renders with the deferred value */}
      <SlowList query={deferredQuery} />
    </>
  )
}

// Must be memoized to benefit from deferredValue
const SlowList = memo(function SlowList({ query }: { query: string }) {
  const items = useMemo(() => {
    // Expensive computation
    return filterItems(query)
  }, [query])

  return <List items={items} />
})
```

### Live Chart Pattern

```tsx
function Dashboard() {
  const [value, setValue] = useState(0)
  const deferredValue = useDeferredValue(value)

  return (
    <>
      <input
        type="range"
        value={value}
        onChange={(e) => setValue(Number(e.target.value))}
      />

      {/* Slider stays responsive while chart updates in background */}
      <ExpensiveChart value={deferredValue} />
    </>
  )
}
```

### Stale Content Indicator

```tsx
function SearchResults({ query }: { query: string }) {
  const deferredQuery = useDeferredValue(query)
  const isStale = query !== deferredQuery

  return (
    <div style={{ opacity: isStale ? 0.5 : 1 }}>
      <Results query={deferredQuery} />
    </div>
  )
}
```

## Purposeful Memoization

Memoization is an optimization technique that should be applied **only after profiling** has identified a clear performance bottleneck.

### When to Use useMemo

Use `useMemo` to cache expensive calculations between re-renders:

```tsx
function TodoList({ todos, filter }: { todos: Todo[], filter: string }) {
  // GOOD: Expensive filtering operation
  const filteredTodos = useMemo(() => {
    return todos.filter(todo => {
      // Complex matching logic
      return performExpensiveMatch(todo, filter)
    })
  }, [todos, filter])

  return <List items={filteredTodos} />
}
```

### When NOT to Use useMemo

```tsx
// BAD: Cheap calculation, useMemo adds overhead
const sum = useMemo(() => a + b, [a, b])

// GOOD: Just calculate directly
const sum = a + b

// BAD: Creating objects/arrays for immediate use
const styles = useMemo(() => ({ color: 'red' }), [])

// GOOD: Create inline
const styles = { color: 'red' }
```

### When to Use useCallback

Use `useCallback` when a function is passed as a prop to a memoized component:

```tsx
function TodoApp() {
  const [todos, setTodos] = useState<Todo[]>([])

  // GOOD: Prevents TodoList re-renders when function reference changes
  const handleToggle = useCallback((id: string) => {
    setTodos(todos => todos.map(todo =>
      todo.id === id ? { ...todo, done: !todo.done } : todo
    ))
  }, [])

  return <MemoizedTodoList todos={todos} onToggle={handleToggle} />
}

const MemoizedTodoList = memo(TodoList)
```

### When NOT to Use useCallback

```tsx
// BAD: Function not passed to memoized component
const handleClick = useCallback(() => {
  console.log('clicked')
}, [])

// GOOD: Just define inline
const handleClick = () => {
  console.log('clicked')
}
```

### When to Use React.memo

Use `React.memo` to prevent re-renders when props haven't changed:

```tsx
// GOOD: Expensive component with stable props
const ExpensiveComponent = memo(function ExpensiveComponent({
  data,
  onAction
}: {
  data: Data,
  onAction: () => void
}) {
  // Complex rendering logic
  return <ComplexVisualization data={data} onAction={onAction} />
})

// BAD: Simple component with cheap rendering
const SimpleComponent = memo(function SimpleComponent({ text }: { text: string }) {
  return <p>{text}</p>
})
// The memo overhead exceeds the rendering cost
```

### Custom Comparison Function

```tsx
const Chart = memo(
  function Chart({ data }: { data: ChartData[] }) {
    return <ExpensiveChart data={data} />
  },
  (prevProps, nextProps) => {
    // Custom comparison: only re-render if data length or first item changed
    return (
      prevProps.data.length === nextProps.data.length &&
      prevProps.data[0]?.value === nextProps.data[0]?.value
    )
  }
)
```

## Memoization Decision Guide

```
Is the component/calculation expensive?
├─ NO → Don't memoize
└─ YES → Have you profiled?
    ├─ NO → Profile first with React DevTools
    └─ YES → Did profiling show a problem?
        ├─ NO → Don't memoize
        └─ YES → Apply appropriate memoization:
            ├─ Expensive calculation → useMemo
            ├─ Function passed to memo component → useCallback
            └─ Expensive component → React.memo
```

## Referential Equality

Memoization relies on referential equality. Props must have the same reference to prevent re-renders.

### Object Props

```tsx
// BAD: New object every render
function Parent() {
  return <Child config={{ theme: 'dark' }} />
}

// GOOD: Memoized object
function Parent() {
  const config = useMemo(() => ({ theme: 'dark' }), [])
  return <Child config={config} />
}

// BETTER: If static, define outside component
const CONFIG = { theme: 'dark' }

function Parent() {
  return <Child config={CONFIG} />
}
```

### Array Props

```tsx
// BAD: New array every render
function Parent() {
  return <Child items={[1, 2, 3]} />
}

// GOOD: Static array outside component
const ITEMS = [1, 2, 3]

function Parent() {
  return <Child items={ITEMS} />
}
```

## Anti-Patterns

### Premature Memoization

```tsx
// BAD: Memoizing everything by default
const Component = memo(function Component({ value }: { value: number }) {
  const doubled = useMemo(() => value * 2, [value])
  const handleClick = useCallback(() => console.log(value), [value])

  return <button onClick={handleClick}>{doubled}</button>
})
// All this memoization adds overhead with no benefit
```

### Blocking the Main Thread

```tsx
// BAD: Synchronous expensive computation in event handler
function handleSearch(query: string) {
  setQuery(query)
  // This blocks the UI
  const results = performVeryExpensiveSearch(query)
  setResults(results)
}

// GOOD: Defer with useTransition
function handleSearch(query: string) {
  setQuery(query)
  startTransition(() => {
    const results = performVeryExpensiveSearch(query)
    setResults(results)
  })
}
```

### Mutating State

```tsx
// BAD: Mutating array directly
const handleAdd = useCallback(() => {
  todos.push(newTodo) // Breaks React's change detection
  setTodos(todos)
}, [todos])

// GOOD: Creating new array
const handleAdd = useCallback(() => {
  setTodos([...todos, newTodo])
}, [todos])

// BETTER: Using functional update
const handleAdd = useCallback(() => {
  setTodos(todos => [...todos, newTodo])
}, [])
```

### Wrong Dependencies in useMemo/useCallback

```tsx
// BAD: Missing dependencies
const filtered = useMemo(() => {
  return items.filter(item => item.category === category)
}, [items]) // Missing 'category' dependency!

// GOOD: Complete dependencies
const filtered = useMemo(() => {
  return items.filter(item => item.category === category)
}, [items, category])
```

### Using useTransition for Urgent Updates

```tsx
// BAD: Wrapping urgent input update
function handleChange(e) {
  startTransition(() => {
    setValue(e.target.value) // Input will feel sluggish
  })
}

// GOOD: Only wrap non-urgent updates
function handleChange(e) {
  setValue(e.target.value) // Urgent

  startTransition(() => {
    setSearchResults(expensiveSearch(e.target.value)) // Non-urgent
  })
}
```

## Performance Checklist

- [ ] Profile with React DevTools Profiler before memoizing
- [ ] Use useTransition for non-urgent updates (search, filtering, navigation)
- [ ] Use useDeferredValue for deferred rendering of expensive components
- [ ] Apply useMemo only to expensive calculations
- [ ] Apply useCallback only for functions passed to memoized components
- [ ] Apply React.memo only to expensive components with stable props
- [ ] Ensure referential equality for object/array props
- [ ] Use functional state updates to avoid stale closures
- [ ] Never mutate state or props directly
- [ ] Verify memoization effectiveness with profiling

## Profiling Workflow

1. **Record baseline**: Profile component without optimizations
2. **Identify bottleneck**: Look for unnecessary re-renders or expensive operations
3. **Apply optimization**: Add memoization or concurrency feature
4. **Verify improvement**: Profile again and compare
5. **Iterate**: Continue optimizing based on data
