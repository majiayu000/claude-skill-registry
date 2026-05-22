---
name: TanStack Forms
description: This skill should be used when the user asks about "React Query with forms", "form submission with useMutation", "form state vs server state", "defaultValue from query", "form reset after mutation", "double submit prevention", or needs guidance on integrating TanStack Query with forms.
version: 1.0.0
---

# TanStack Query Forms Integration Patterns

This skill provides guidance for integrating TanStack Query with forms, covering the challenge of mixing server state with form (client) state, based on TKDodo's recommendations.

## The Core Challenge

Form data exists in a hybrid zone:
- **Initially**: Server State (fetched data)
- **During editing**: Client State (user changes)
- **After submit**: Server State again

Understanding this lifecycle is key to choosing the right pattern.

## Two Main Approaches

### Approach 1: Simple - Copy to Form State

Use server state as initial data only. The form manages its own state:

```typescript
function EditTodo({ id }: { id: string }) {
  const { data: todo, isLoading } = useQuery(todoQueries.detail(id))

  if (isLoading) return <Skeleton />

  return <TodoForm initialData={todo} />
}

function TodoForm({ initialData }: { initialData: Todo }) {
  // Form state is independent copy of server state
  const [title, setTitle] = useState(initialData.title)
  const [description, setDescription] = useState(initialData.description)

  const mutation = useMutation({
    mutationFn: (data: Partial<Todo>) =>
      api.patch(`/todos/${initialData.id}`, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['todos'] })
    },
  })

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    mutation.mutate({ title, description })
  }

  return (
    <form onSubmit={handleSubmit}>
      <input
        value={title}
        onChange={(e) => setTitle(e.target.value)}
      />
      <textarea
        value={description}
        onChange={(e) => setDescription(e.target.value)}
      />
      <button type="submit" disabled={mutation.isPending}>
        Save
      </button>
    </form>
  )
}
```

**Pros:**
- Simple to understand
- Form is in full control
- Works with any form library

**Cons:**
- Background updates won't reflect in form
- Can lead to stale data submission in collaborative apps

**Best for:** Single-user apps, short-lived forms, simple editing flows

### Approach 2: Derived State Pattern

Keep server state and form state separate, display whichever is relevant:

```typescript
function EditTodo({ id }: { id: string }) {
  const { data: serverTodo } = useQuery(todoQueries.detail(id))

  // Track which fields user has changed
  const [formChanges, setFormChanges] = useState<Partial<Todo>>({})

  // Derived state: show user changes, fall back to server data
  const displayedTodo = {
    ...serverTodo,
    ...formChanges, // User changes override server data
  }

  const mutation = useMutation({
    mutationFn: (data: Partial<Todo>) => api.patch(`/todos/${id}`, data),
    onSuccess: () => {
      // Clear form changes after successful save
      setFormChanges({})
      queryClient.invalidateQueries({ queryKey: ['todos', id] })
    },
  })

  const handleFieldChange = (field: keyof Todo, value: string) => {
    setFormChanges((prev) => ({ ...prev, [field]: value }))
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    mutation.mutate(formChanges)
  }

  return (
    <form onSubmit={handleSubmit}>
      <input
        value={displayedTodo?.title ?? ''}
        onChange={(e) => handleFieldChange('title', e.target.value)}
      />
      {/* Fields user hasn't touched will update from server */}
    </form>
  )
}
```

**Pros:**
- Background updates visible for untouched fields
- Better for collaborative editing
- Server is always source of truth

**Cons:**
- More complex state management
- Requires controlled components
- Must track changed fields

**Best for:** Collaborative apps, long-lived forms, real-time environments

## Essential Patterns

### Double Submit Prevention

Always disable submit during mutation:

```typescript
const mutation = useMutation({
  mutationFn: createTodo,
})

<button
  type="submit"
  disabled={mutation.isPending}
>
  {mutation.isPending ? 'Saving...' : 'Save'}
</button>
```

### Form Reset After Mutation

Reset form state to allow server state to show through:

```typescript
const [formData, setFormData] = useState<Partial<Todo>>({})

const mutation = useMutation({
  mutationFn: (data: Partial<Todo>) => api.patch(`/todos/${id}`, data),
  onSuccess: () => {
    // 1. Invalidate to get fresh server data
    queryClient.invalidateQueries({ queryKey: ['todos', id] })
    // 2. Clear form state so server state shows
    setFormData({})
  },
})
```

### Component Splitting for Initialization

Separate data fetching from form rendering to properly initialize `defaultValue`:

```typescript
// Wrapper handles loading state
function EditTodoPage({ id }: { id: string }) {
  const { data, isLoading, error } = useQuery(todoQueries.detail(id))

  if (isLoading) return <FormSkeleton />
  if (error) return <ErrorDisplay error={error} />
  if (!data) return null

  // Form only renders when data exists
  return <TodoForm todo={data} />
}

// Form receives guaranteed data
function TodoForm({ todo }: { todo: Todo }) {
  // Safe to use as defaultValue - todo is guaranteed
  return (
    <form>
      <input defaultValue={todo.title} name="title" />
      <textarea defaultValue={todo.description} name="description" />
    </form>
  )
}
```

### Using with React Hook Form

```typescript
import { useForm } from 'react-hook-form'

function TodoForm({ todo }: { todo: Todo }) {
  const { register, handleSubmit, reset } = useForm({
    defaultValues: todo,
  })

  const mutation = useMutation({
    mutationFn: (data: Todo) => api.patch(`/todos/${todo.id}`, data),
    onSuccess: (updatedTodo) => {
      queryClient.invalidateQueries({ queryKey: ['todos'] })
      // Reset form to new server values
      reset(updatedTodo)
    },
  })

  return (
    <form onSubmit={handleSubmit((data) => mutation.mutate(data))}>
      <input {...register('title')} />
      <textarea {...register('description')} />
      <button type="submit" disabled={mutation.isPending}>
        Save
      </button>
    </form>
  )
}
```

## Preventing Stale Data Issues

### Option 1: Disable Background Refetch

For the simple approach, prevent confusing UX:

```typescript
const { data } = useQuery({
  ...todoQueries.detail(id),
  staleTime: Infinity, // Don't refetch while editing
  refetchOnWindowFocus: false, // Don't refetch on tab focus
})
```

### Option 2: Warn About Conflicts

For collaborative apps, detect and warn:

```typescript
function EditTodo({ id }: { id: string }) {
  const { data: serverTodo, dataUpdatedAt } = useQuery(todoQueries.detail(id))
  const [formData, setFormData] = useState<Partial<Todo>>({})
  const [formStartedAt] = useState(Date.now())

  // Detect if server data changed while editing
  const hasConflict = dataUpdatedAt > formStartedAt && Object.keys(formData).length > 0

  return (
    <form>
      {hasConflict && (
        <Alert>
          This item was updated. Review changes before saving.
          <button onClick={() => setFormData({})}>
            Discard my changes
          </button>
        </Alert>
      )}
      {/* Form fields */}
    </form>
  )
}
```

## Quick Reference

| Scenario | Pattern |
|----------|---------|
| Simple edit form | Copy to state, staleTime: Infinity |
| Collaborative editing | Derived state pattern |
| Create form | Standard mutation, no query needed |
| With form library | Split loading/form components |
| Long-lived form | Conflict detection |

## Common Mistakes

### 1. Using Query Data Directly as Form State

```typescript
// BAD: Query data changes unexpectedly
const { data } = useQuery(todoQueries.detail(id))

return (
  <input
    value={data?.title} // Changes on refetch!
    onChange={(e) => /* where does this go? */}
  />
)
```

### 2. Not Handling Loading State Before Form

```typescript
// BAD: defaultValue is undefined
function Form({ id }) {
  const { data } = useQuery(todoQueries.detail(id))

  return <input defaultValue={data?.title} /> // undefined on first render!
}

// GOOD: Split components
function FormWrapper({ id }) {
  const { data, isLoading } = useQuery(todoQueries.detail(id))
  if (isLoading || !data) return <Loading />
  return <Form todo={data} />
}
```

### 3. Forgetting to Reset Form on Success

```typescript
// BAD: Old form data persists after save
onSuccess: () => {
  queryClient.invalidateQueries({ queryKey: ['todos'] })
  // Form still shows old local state!
}

// GOOD: Reset form state
onSuccess: (newData) => {
  queryClient.invalidateQueries({ queryKey: ['todos'] })
  setFormState({}) // or reset(newData) with RHF
}
```

## Additional Resources

### Reference Files

For detailed patterns and advanced techniques, consult:
- **`references/form-library-integration.md`** - Patterns with React Hook Form, Formik

### Related Skills

- **tanstack-mutations** - Mutation patterns for form submission
- **tanstack-query** - Query patterns for loading initial data
- **tanstack-errors** - Handling form submission errors
