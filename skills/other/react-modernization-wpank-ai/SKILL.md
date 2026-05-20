---
name: react-modernization
model: reasoning
---

# React Modernization

Upgrade React applications from class components to hooks, adopt concurrent features, and migrate between major versions.

## WHAT

Systematic patterns for modernizing React codebases:
- Class-to-hooks migration with lifecycle method mappings
- React 18/19 concurrent features adoption
- TypeScript migration for React components
- Automated codemods for bulk refactoring
- Performance optimization with modern APIs

## WHEN

- Migrating class components to functional components with hooks
- Upgrading React 16/17 apps to React 18/19
- Adopting concurrent features (Suspense, transitions, use)
- Converting HOCs and render props to custom hooks
- Adding TypeScript to React projects

## KEYWORDS

react upgrade, class to hooks, useEffect, useState, react 18, react 19, concurrent, suspense, transition, codemod, migrate, modernize, functional component


## Installation

### OpenClaw / Moltbot / Clawbot

```bash
npx clawhub@latest install react-modernization
```


---

## Version Upgrade Paths

### React 17 → 18 Breaking Changes

| Change | Impact | Migration |
|--------|--------|-----------|
| New root API | Required | `ReactDOM.render` → `createRoot` |
| Automatic batching | Behavior | State updates batch in async code now |
| Strict Mode | Dev only | Effects fire twice (mount/unmount/mount) |
| Suspense on server | Optional | Enable SSR streaming |

### React 18 → 19 Breaking Changes

| Change | Impact | Migration |
|--------|--------|-----------|
| `use()` hook | New API | Read promises/context in render |
| `ref` as prop | Simplified | No more `forwardRef` needed |
| Context as provider | Simplified | `<Context>` not `<Context.Provider>` |
| Async actions | New pattern | `useActionState`, `useOptimistic` |

---

## Class to Hooks Migration

### Lifecycle Method Mappings

```tsx
// componentDidMount → useEffect with empty deps
useEffect(() => {
  fetchData()
}, [])

// componentDidUpdate → useEffect with deps
useEffect(() => {
  updateWhenIdChanges()
}, [id])

// componentWillUnmount → useEffect cleanup
useEffect(() => {
  const subscription = subscribe()
  return () => subscription.unsubscribe()
}, [])

// shouldComponentUpdate → React.memo
const Component = React.memo(({ data }) => <div>{data}</div>)

// getDerivedStateFromProps → useMemo
const derivedValue = useMemo(() => computeFrom(props), [props])
```

### State Migration Pattern

```tsx
// BEFORE: Class with multiple state properties
class UserProfile extends React.Component {
  state = { user: null, loading: true, error: null }
  
  componentDidMount() {
    fetchUser(this.props.id)
      .then(user => this.setState({ user, loading: false }))
      .catch(error => this.setState({ error, loading: false }))
  }
  
  componentDidUpdate(prevProps) {
    if (prevProps.id !== this.props.id) {
      this.setState({ loading: true })
      fetchUser(this.props.id)
        .then(user => this.setState({ user, loading: false }))
    }
  }
  
  render() {
    const { user, loading, error } = this.state
    if (loading) return <Spinner />
    if (error) return <Error message={error.message} />
    return <Profile user={user} />
  }
}

// AFTER: Custom hook + functional component
function useUser(id: string) {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<Error | null>(null)

  useEffect(() => {
    let cancelled = false
    setLoading(true)
    
    fetchUser(id)
      .then(data => {
        if (!cancelled) {
          setUser(data)
          setLoading(false)
        }
      })
      .catch(err => {
        if (!cancelled) {
          setError(err)
          setLoading(false)
        }
      })

    return () => { cancelled = true }
  }, [id])

  return { user, loading, error }
}

function UserProfile({ id }: { id: string }) {
  const { user, loading, error } = useUser(id)
  
  if (loading) return <Spinner />
  if (error) return <Error message={error.message} />
  return <Profile user={user} />
}
```

### HOC to Hook Migration

```tsx
// BEFORE: Higher-Order Component
function withUser(Component) {
  return function WithUser(props) {
    const [user, setUser] = useState(null)
    useEffect(() => { fetchUser().then(setUser) }, [])
    return <Component {...props} user={user} />
  }
}

const ProfileWithUser = withUser(Profile)

// AFTER: Custom hook (simpler, composable)
function useCurrentUser() {
  const [user, setUser] = useState(null)
  useEffect(() => { fetchUser().then(setUser) }, [])
  return user
}

function Profile() {
  const user = useCurrentUser()
  return user ? <div>{user.name}</div> : null
}
```

---

## React 18+ Concurrent Features

### New Root API (Required)

```tsx
// BEFORE: React 17
import ReactDOM from 'react-dom'
ReactDOM.render(<App />, document.getElementById('root'))

// AFTER: React 18+
import { createRoot } from 'react-dom/client'
const root = createRoot(document.getElementById('root')!)
root.render(<App />)
```

### useTransition for Non-Urgent Updates

```tsx
function SearchResults() {
  const [query, setQuery] = useState('')
  const [results, setResults] = useState([])
  const [isPending, startTransition] = useTransition()

  function handleChange(e: React.ChangeEvent<HTMLInputElement>) {
    // Urgent: update input immediately
    setQuery(e.target.value)
    
    // Non-urgent: can be interrupted
    startTransition(() => {
      setResults(searchDatabase(e.target.value))
    })
  }

  return (
    <>
      <input value={query} onChange={handleChange} />
      {isPending ? <Spinner /> : <ResultsList data={results} />}
    </>
  )
}
```

### Suspense for Data Fetching

```tsx
// With React 19's use() hook
function ProfilePage({ userId }: { userId: string }) {
  return (
    <Suspense fallback={<ProfileSkeleton />}>
      <ProfileDetails userId={userId} />
    </Suspense>
  )
}

function ProfileDetails({ userId }: { userId: string }) {
  // use() suspends until promise resolves
  const user = use(fetchUser(userId))
  return <h1>{user.name}</h1>
}
```

### React 19: use() Hook

```tsx
// Read promises directly in render
function Comments({ commentsPromise }) {
  const comments = use(commentsPromise)
  return comments.map(c => <Comment key={c.id} {...c} />)
}

// Read context (simpler than useContext)
function ThemeButton() {
  const theme = use(ThemeContext)
  return <button className={theme}>Click</button>
}
```

### React 19: Actions

```tsx
// useActionState for form submissions
function UpdateName() {
  const [error, submitAction, isPending] = useActionState(
    async (previousState, formData) => {
      const error = await updateName(formData.get('name'))
      if (error) return error
      redirect('/profile')
    },
    null
  )

  return (
    <form action={submitAction}>
      <input name="name" />
      <button disabled={isPending}>Update</button>
      {error && <p>{error}</p>}
    </form>
  )
}
```

---

## Automated Codemods

### Run Official React Codemods

```bash
# Update to new JSX transform (no React import needed)
npx codemod@latest react/19/replace-reactdom-render

# Update deprecated APIs
npx codemod@latest react/19/replace-string-ref

# Class to function components
npx codemod@latest react/19/replace-use-form-state
```

### Manual Search Patterns

```bash
# Find class components
rg "class \w+ extends (React\.)?Component" --type tsx

# Find deprecated lifecycle methods
rg "componentWillMount|componentWillReceiveProps|componentWillUpdate" --type tsx

# Find ReactDOM.render (needs migration to createRoot)
rg "ReactDOM\.render" --type tsx
```

---

## TypeScript Migration

```tsx
// Add types to functional components
interface ButtonProps {
  onClick: () => void
  children: React.ReactNode
  variant?: 'primary' | 'secondary'
}

function Button({ onClick, children, variant = 'primary' }: ButtonProps) {
  return (
    <button onClick={onClick} className={variant}>
      {children}
    </button>
  )
}

// Type event handlers
function Form() {
  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
  }
  
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    console.log(e.target.value)
  }

  return (
    <form onSubmit={handleSubmit}>
      <input onChange={handleChange} />
    </form>
  )
}

// Generic components
interface ListProps<T> {
  items: T[]
  renderItem: (item: T) => React.ReactNode
}

function List<T>({ items, renderItem }: ListProps<T>) {
  return <>{items.map(renderItem)}</>
}
```

---

## Migration Checklist

### Pre-Migration
- [ ] Upgrade dependencies incrementally
- [ ] Review breaking changes in release notes
- [ ] Set up comprehensive test coverage
- [ ] Create feature branch

### Class → Hooks
- [ ] Start with leaf components (no children)
- [ ] Convert state to `useState`
- [ ] Convert lifecycle to `useEffect`
- [ ] Extract shared logic to custom hooks
- [ ] Convert HOCs to hooks where possible

### React 18+ Upgrade
- [ ] Update to `createRoot` API
- [ ] Test with StrictMode double-invocation
- [ ] Address hydration mismatches
- [ ] Adopt Suspense boundaries where beneficial
- [ ] Use transitions for expensive updates

### Post-Migration
- [ ] Run full test suite
- [ ] Check for console warnings
- [ ] Profile performance before/after
- [ ] Document changes for team

---

## NEVER

- Skip testing after migration
- Migrate multiple components in one commit
- Ignore StrictMode warnings (they reveal bugs)
- Use `// eslint-disable-next-line react-hooks/exhaustive-deps` without understanding why
- Mix class and hooks in same component
