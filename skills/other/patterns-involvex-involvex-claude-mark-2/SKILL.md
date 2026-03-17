---
name: react-patterns
description: React 19 specific patterns including React Compiler optimization, Server Actions, Forms, and new hooks. Use when implementing React 19 features, optimizing components, or choosing between Actions vs TanStack Query for mutations.
---

# React 19 Patterns and Best Practices

Modern React 19 patterns leveraging the React Compiler, Server Actions, and new hooks.

## Compiler-Friendly Code

The React Compiler automatically optimizes components for performance. Write code that works well with it:

**Best Practices:**
- Keep components pure and props serializable
- Derive values during render (don't stash in refs unnecessarily)
- Keep event handlers inline unless they close over large mutable objects
- Verify compiler is working (DevTools ✨ badge)
- Opt-out problematic components with `"use no memo"` while refactoring

**Example - Pure Component:**
```typescript
// ✅ Compiler-friendly - pure function
function UserCard({ user }: { user: User }) {
  const displayName = `${user.firstName} ${user.lastName}`
  const isVIP = user.points > 1000

  return (
    <div>
      <h2>{displayName}</h2>
      {isVIP && <Badge>VIP</Badge>}
    </div>
  )
}

// ❌ Avoid - unnecessary effects
function UserCard({ user }: { user: User }) {
  const [displayName, setDisplayName] = useState('')

  useEffect(() => {
    setDisplayName(`${user.firstName} ${user.lastName}`)
  }, [user])

  return <div><h2>{displayName}</h2></div>
}
```

**Verification:**
- Open React DevTools
- Look for "Memo ✨" badge on components
- If missing, component wasn't optimized (check for violations)

**Opt-Out When Needed:**
```typescript
'use no memo'

// Component code that can't be optimized yet
function ProblematicComponent() {
  // ... code with compiler issues
}
```

## Actions & Forms

For SPA mutations, choose **one approach per feature**:
- **React 19 Actions:** `<form action={fn}>`, `useActionState`, `useOptimistic`
- **TanStack Query:** `useMutation`

Don't duplicate logic between both approaches.

### React 19 Actions (Form-Centric)

**Best for:**
- Form submissions
- Simple CRUD operations
- When you want form validation built-in

**Basic Action:**
```typescript
'use server' // Only if using SSR/RSC, omit for SPA

async function createTodoAction(formData: FormData) {
  const text = formData.get('text') as string

  // Validation
  if (!text || text.length < 3) {
    return { error: 'Text must be at least 3 characters' }
  }

  // API call
  await api.post('/todos', { text })

  // Revalidation happens automatically
  return { success: true }
}

// Component
function TodoForm() {
  return (
    <form action={createTodoAction}>
      <input name="text" required />
      <button type="submit">Add Todo</button>
    </form>
  )
}
```

**With State (useActionState):**
```typescript
import { useActionState } from 'react'

function TodoForm() {
  const [state, formAction, isPending] = useActionState(
    createTodoAction,
    { error: null, success: false }
  )

  return (
    <form action={formAction}>
      {state.error && <ErrorMessage>{state.error}</ErrorMessage>}
      <input name="text" required />
      <button type="submit" disabled={isPending}>
        {isPending ? 'Adding...' : 'Add Todo'}
      </button>
    </form>
  )
}
```

**With Optimistic Updates (useOptimistic):**
```typescript
import { useOptimistic } from 'react'

function TodoList({ initialTodos }: { initialTodos: Todo[] }) {
  const [optimisticTodos, addOptimisticTodo] = useOptimistic(
    initialTodos,
    (state, newTodo: string) => [
      ...state,
      { id: `temp-${Date.now()}`, text: newTodo, completed: false }
    ]
  )

  async function handleSubmit(formData: FormData) {
    const text = formData.get('text') as string
    addOptimisticTodo(text)

    await createTodoAction(formData)
  }

  return (
    <>
      <ul>
        {optimisticTodos.map(todo => (
          <li key={todo.id} style={{ opacity: todo.id.startsWith('temp-') ? 0.5 : 1 }}>
            {todo.text}
          </li>
        ))}
      </ul>
      <form action={handleSubmit}>
        <input name="text" required />
        <button type="submit">Add</button>
      </form>
    </>
  )
}
```

### TanStack Query Mutations (Preferred for SPAs)

**Best for:**
- Non-form mutations (e.g., button clicks)
- Complex optimistic updates with rollback
- Integration with existing Query cache
- More control over caching and invalidation

See **tanstack-query** skill for comprehensive mutation patterns.

**Quick Example:**
```typescript
import { useMutation, useQueryClient } from '@tanstack/react-query'

function useCre

ateTodo() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (text: string) => api.post('/todos', { text }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['todos'] })
    },
  })
}

// Usage
function TodoForm() {
  const createTodo = useCreateTodo()

  return (
    <form onSubmit={(e) => {
      e.preventDefault()
      const formData = new FormData(e.currentTarget)
      createTodo.mutate(formData.get('text') as string)
    }}>
      <input name="text" required />
      <button type="submit" disabled={createTodo.isPending}>
        {createTodo.isPending ? 'Adding...' : 'Add Todo'}
      </button>
    </form>
  )
}
```

## The `use` Hook

The `use` hook unwraps Promises and Context, enabling new patterns.

**With Promises:**
```typescript
import { use, Suspense } from 'react'

function UserProfile({ userPromise }: { userPromise: Promise<User> }) {
  const user = use(userPromise)

  return <div>{user.name}</div>
}

// Usage
function App() {
  const userPromise = fetchUser(1)

  return (
    <Suspense fallback={<Spinner />}>
      <UserProfile userPromise={userPromise} />
    </Suspense>
  )
}
```

**With Context:**
```typescript
import { use, createContext } from 'react'

const ThemeContext = createContext<string>('light')

function Button() {
  const theme = use(ThemeContext)
  return <button className={theme}>Click me</button>
}
```

**When to Use:**
- Primarily useful with Suspense/data primitives and RSC (React Server Components)
- **For SPA-only apps**, prefer **TanStack Query + Router loaders** for data fetching
- `use` shines when you already have a Promise from a parent component

## Component Composition Patterns

**Compound Components:**
```typescript
// ✅ Good - composable, flexible
<Card>
  <Card.Header>
    <Card.Title>Dashboard</Card.Title>
  </Card.Header>
  <Card.Content>
    {/* content */}
  </Card.Content>
</Card>

// Implementation
function Card({ children }: { children: React.ReactNode }) {
  return <div className="card">{children}</div>
}

Card.Header = function CardHeader({ children }: { children: React.ReactNode }) {
  return <header className="card-header">{children}</header>
}

Card.Title = function CardTitle({ children }: { children: React.ReactNode }) {
  return <h2 className="card-title">{children}</h2>
}

Card.Content = function CardContent({ children }: { children: React.ReactNode }) {
  return <div className="card-content">{children}</div>
}
```

**Render Props (when needed):**
```typescript
function DataLoader<T>({
  fetch,
  render
}: {
  fetch: () => Promise<T>
  render: (data: T) => React.ReactNode
}) {
  const { data } = useQuery({ queryKey: ['data'], queryFn: fetch })

  if (!data) return <Spinner />

  return <>{render(data)}</>
}

// Usage
<DataLoader
  fetch={() => fetchUser(1)}
  render={(user) => <UserCard user={user} />}
/>
```

## Error Boundaries

React 19 still requires class components for error boundaries (or use a library):

```typescript
import { Component, ReactNode } from 'react'

class ErrorBoundary extends Component<
  { children: ReactNode; fallback: ReactNode },
  { hasError: boolean }
> {
  state = { hasError: false }

  static getDerivedStateFromError() {
    return { hasError: true }
  }

  componentDidCatch(error: Error, info: { componentStack: string }) {
    console.error('Error caught:', error, info)
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback
    }

    return this.props.children
  }
}

// Usage
<ErrorBoundary fallback={<ErrorFallback />}>
  <App />
</ErrorBoundary>
```

**Or use react-error-boundary library:**
```typescript
import { ErrorBoundary } from 'react-error-boundary'

<ErrorBoundary
  fallback={<div>Something went wrong</div>}
  onError={(error, info) => console.error(error, info)}
>
  <App />
</ErrorBoundary>
```

## Decision Guide: Actions vs Query Mutations

| Scenario | Recommendation |
|----------|---------------|
| Form submission with validation | React Actions |
| Button click mutation | TanStack Query |
| Needs optimistic updates + rollback | TanStack Query |
| Integrates with existing cache | TanStack Query |
| SSR/RSC application | React Actions |
| SPA with complex data flow | TanStack Query |
| Simple CRUD with forms | React Actions |

**Rule of Thumb:** For SPAs with TanStack Query already in use, prefer Query mutations for consistency. Only use Actions for form-heavy features where the form-centric API is beneficial.

## Related Skills

- **tanstack-query** - Server state with mutations and optimistic updates
- **core-principles** - Overall project structure
- **tooling-setup** - React Compiler configuration
