---
name: component-refactoring
description: Refactor high-complexity React components. Use when complexity is high, when the user asks for code splitting, hook extraction, or complexity reduction.
---

# Component Refactoring

Refactor high-complexity React components with structured patterns.

> **Complexity Threshold**: Components with complexity > 50 or lineCount > 300 should be refactored before testing.

## Complexity Score Interpretation

| Score | Level | Action |
|-------|-------|--------|
| 0-25 | 🟢 Simple | Ready for testing |
| 26-50 | 🟡 Medium | Consider minor refactoring |
| 51-75 | 🟠 Complex | **Refactor before testing** |
| 76-100 | 🔴 Very Complex | **Must refactor** |

## Core Refactoring Patterns

### Pattern 1: Extract Custom Hooks

**When**: Component has complex state management, multiple useEffects, or business logic mixed with UI.

```typescript
// ❌ Before: Logic mixed in component
const Component = () => {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  
  useEffect(() => {
    setLoading(true)
    fetchData().then(setData).catch(setError).finally(() => setLoading(false))
  }, [])
  
  return <div>{/* ... */}</div>
}

// ✅ After: Logic extracted to hook
const useDataFetching = () => {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  
  useEffect(() => {
    setLoading(true)
    fetchData().then(setData).catch(setError).finally(() => setLoading(false))
  }, [])
  
  return { data, loading, error }
}

const Component = () => {
  const { data, loading, error } = useDataFetching()
  return <div>{/* ... */}</div>
}
```

### Pattern 2: Split Large Components

**When**: Component has multiple distinct sections or responsibilities.

```typescript
// ❌ Before: One large component
const Dashboard = () => {
  return (
    <div>
      {/* 100 lines of header */}
      {/* 150 lines of sidebar */}
      {/* 200 lines of content */}
    </div>
  )
}

// ✅ After: Split into focused components
const Dashboard = () => {
  return (
    <div>
      <DashboardHeader />
      <DashboardSidebar />
      <DashboardContent />
    </div>
  )
}
```

### Pattern 3: Extract Render Functions

**When**: Complex conditional rendering or list rendering.

```typescript
// ❌ Before: Inline complex rendering
const List = ({ items }) => {
  return (
    <ul>
      {items.map(item => (
        <li key={item.id}>
          {item.type === 'a' ? (
            <div>{/* 50 lines */}</div>
          ) : item.type === 'b' ? (
            <div>{/* 40 lines */}</div>
          ) : (
            <div>{/* 30 lines */}</div>
          )}
        </li>
      ))}
    </ul>
  )
}

// ✅ After: Extract to separate components
const ListItemA = ({ item }) => <div>{/* ... */}</div>
const ListItemB = ({ item }) => <div>{/* ... */}</div>
const ListItemDefault = ({ item }) => <div>{/* ... */}</div>

const ListItem = ({ item }) => {
  const components = { a: ListItemA, b: ListItemB }
  const Component = components[item.type] || ListItemDefault
  return <Component item={item} />
}
```

### Pattern 4: Consolidate State

**When**: Multiple related useState calls.

```typescript
// ❌ Before: Related state scattered
const [name, setName] = useState('')
const [email, setEmail] = useState('')
const [phone, setPhone] = useState('')

// ✅ After: Consolidated state
const [formValues, setFormValues] = useState({
  name: '',
  email: '',
  phone: ''
})

// Or use useReducer for complex state
const [state, dispatch] = useReducer(formReducer, initialState)
```

## Refactoring Workflow

1. **Measure Current Complexity**
   - Count lines of code
   - Count useState/useEffect calls
   - Identify nested conditionals

2. **Identify Extraction Candidates**
   - Related state that move together
   - Reusable UI sections
   - Business logic that can be isolated

3. **Apply Patterns (one at a time)**
   - Extract hooks for state/logic
   - Split components for UI sections
   - Consolidate related state

4. **Verify After Each Change**
   - Tests still pass
   - Behavior unchanged
   - Complexity reduced

## Common Mistakes to Avoid

### ❌ Over-Engineering

```typescript
// ❌ Too many tiny hooks
const useButtonText = () => useState('Click')
const useButtonDisabled = () => useState(false)

// ✅ Cohesive hook with related state
const useButtonState = () => {
  const [text, setText] = useState('Click')
  const [disabled, setDisabled] = useState(false)
  return { text, setText, disabled, setDisabled }
}
```

### ❌ Breaking Existing Patterns

- Follow existing directory structures
- Maintain naming conventions
- Preserve export patterns

### ❌ Premature Abstraction

- Only extract when there's clear benefit
- Don't create abstractions for single-use code
- Keep refactored code in the same domain area

## Success Criteria

After refactoring:
- [ ] Complexity score < 50
- [ ] Line count < 300
- [ ] Max function complexity < 30
- [ ] All tests pass
- [ ] No behavior changes
