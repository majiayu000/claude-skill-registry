---
name: TanStack Errors
description: This skill should be used when the user asks about "React Query error handling", "error boundaries with useQuery", "throwOnError", "global error callbacks", "onError callback", "query error state", "mutation error handling", or needs guidance on error handling strategies and patterns in TanStack Query.
version: 1.0.0
---

# TanStack Query Error Handling Patterns

This skill provides guidance for error handling in TanStack Query, covering local vs global strategies, Error Boundaries, and best practices based on TKDodo's recommendations.

## Three Approaches to Error Handling

### 1. Local Error State

Check the `error` property directly in components:

```typescript
function TodoList() {
  const { data, error, isError } = useQuery(todoQueries.all())

  if (isError) {
    return <ErrorMessage error={error} />
  }

  return <ul>{data?.map(todo => <TodoItem key={todo.id} todo={todo} />)}</ul>
}
```

**Pros:** Simple, explicit, component controls its error UI
**Cons:** Repetitive across many components

### 2. Error Boundaries

Propagate errors to Error Boundaries using `throwOnError`:

```typescript
// Component throws errors to boundary
function TodoList() {
  const { data } = useQuery({
    ...todoQueries.all(),
    throwOnError: true, // Throws on error
  })

  return <ul>{data.map(todo => <TodoItem key={todo.id} todo={todo} />)}</ul>
}

// Parent catches with Error Boundary
<ErrorBoundary fallback={<ErrorPage />}>
  <TodoList />
</ErrorBoundary>
```

### 3. Global Error Callbacks

Handle errors at the QueryCache level:

```typescript
const queryClient = new QueryClient({
  queryCache: new QueryCache({
    onError: (error, query) => {
      // Global error handling
      if (query.state.data !== undefined) {
        // Only show toast if we already have data (background refetch failed)
        toast.error(`Background update failed: ${error.message}`)
      }
    },
  }),
})
```

## Choosing the Right Approach

| Scenario | Recommended Approach |
|----------|---------------------|
| Critical page data | Error Boundary |
| Background refetch failures | Global callbacks with toast |
| Form validation errors | Local error state |
| 404 errors | Local error state or boundary |
| 5xx server errors | Error Boundary |
| Network errors | Global callbacks |

## Error Boundaries with throwOnError

### Basic Usage

```typescript
const { data } = useQuery({
  queryKey: ['todos'],
  queryFn: fetchTodos,
  throwOnError: true,
})
```

### Conditional Throwing

Only throw for specific error types:

```typescript
const { data } = useQuery({
  queryKey: ['todos'],
  queryFn: fetchTodos,
  throwOnError: (error) => {
    // Only throw for server errors (5xx)
    return error.response?.status >= 500
  },
})
```

This pattern allows:
- 5xx errors → Error Boundary (page-level error)
- 4xx errors → Local handling (validation, not found)

### Creating an Error Boundary

```typescript
import { QueryErrorResetBoundary } from '@tanstack/react-query'
import { ErrorBoundary } from 'react-error-boundary'

function App() {
  return (
    <QueryErrorResetBoundary>
      {({ reset }) => (
        <ErrorBoundary
          onReset={reset}
          fallbackRender={({ error, resetErrorBoundary }) => (
            <div>
              <h2>Something went wrong</h2>
              <p>{error.message}</p>
              <button onClick={resetErrorBoundary}>Try again</button>
            </div>
          )}
        >
          <Routes />
        </ErrorBoundary>
      )}
    </QueryErrorResetBoundary>
  )
}
```

`QueryErrorResetBoundary` ensures queries retry when the boundary resets.

## Global Error Callbacks

### The Problem with Per-Query onError

```typescript
// BAD: onError fires per observer (per component using this query)
const { data } = useQuery({
  queryKey: ['todos'],
  queryFn: fetchTodos,
  onError: (error) => {
    toast.error(error.message) // Shows multiple toasts!
  },
})
```

If three components use this query, you get three toast notifications.

### The Solution: QueryCache Callbacks

```typescript
const queryClient = new QueryClient({
  queryCache: new QueryCache({
    onError: (error, query) => {
      // Fires once per request, not per observer
      toast.error(`Error: ${error.message}`)
    },
  }),
})
```

### Smarter Global Handling

Only show errors when they matter:

```typescript
const queryClient = new QueryClient({
  queryCache: new QueryCache({
    onError: (error, query) => {
      // Only toast on background refetch failures
      // (user already sees data, update silently failed)
      if (query.state.data !== undefined) {
        toast.error(`Failed to refresh: ${error.message}`)
      }
      // Initial load failures handled by component/boundary
    },
  }),
  mutationCache: new MutationCache({
    onError: (error) => {
      // Always toast mutation errors
      toast.error(`Operation failed: ${error.message}`)
    },
  }),
})
```

## Prerequisites: Making Errors Happen

### Fetch API Doesn't Throw on HTTP Errors

```typescript
// BAD: No error on 404 or 500
const fetchTodo = async (id: string) => {
  const response = await fetch(`/api/todos/${id}`)
  return response.json() // Silently returns error body as "data"
}

// GOOD: Check response.ok
const fetchTodo = async (id: string) => {
  const response = await fetch(`/api/todos/${id}`)

  if (!response.ok) {
    throw new Error(`HTTP ${response.status}: ${response.statusText}`)
  }

  return response.json()
}
```

### Axios Throws by Default

```typescript
// Axios throws on non-2xx responses automatically
const fetchTodo = async (id: string) => {
  const { data } = await axios.get(`/api/todos/${id}`)
  return data
}
```

### Don't Swallow Errors

```typescript
// BAD: Error caught and swallowed
const fetchTodo = async (id: string) => {
  try {
    const response = await api.get(`/todos/${id}`)
    return response.data
  } catch (error) {
    console.error(error) // Logged but not re-thrown!
    // Returns undefined - query thinks it succeeded
  }
}

// GOOD: Re-throw after logging
const fetchTodo = async (id: string) => {
  try {
    const response = await api.get(`/todos/${id}`)
    return response.data
  } catch (error) {
    console.error(error)
    throw error // Let React Query handle it
  }
}
```

## Mutation Error Handling

### Local Handling with mutate Callbacks

```typescript
const mutation = useMutation({
  mutationFn: createTodo,
})

mutation.mutate(newTodo, {
  onError: (error) => {
    // Show error in UI
    setFormError(error.message)
  },
})
```

### Global Mutation Errors

```typescript
const queryClient = new QueryClient({
  mutationCache: new MutationCache({
    onError: (error, variables, context, mutation) => {
      // Log all mutation errors
      logger.error('Mutation failed', { error, variables })

      // Show generic toast for unexpected errors
      if (!mutation.meta?.skipToast) {
        toast.error('Operation failed. Please try again.')
      }
    },
  }),
})

// Skip toast for specific mutations
useMutation({
  mutationFn: saveForm,
  meta: { skipToast: true }, // Handle errors locally instead
})
```

## Pattern: Combining Approaches

Use multiple strategies together:

```typescript
// 1. Global: Log and toast background failures
const queryClient = new QueryClient({
  queryCache: new QueryCache({
    onError: (error, query) => {
      logger.error('Query failed', { error, queryKey: query.queryKey })

      if (query.state.data !== undefined) {
        toast.error('Failed to refresh data')
      }
    },
  }),
})

// 2. Boundary: Catch critical page errors
function TodoPage() {
  return (
    <ErrorBoundary fallback={<TodoPageError />}>
      <TodoList />
    </ErrorBoundary>
  )
}

// 3. Local: Handle specific errors
function TodoList() {
  const { data, error, isError } = useQuery({
    ...todoQueries.all(),
    throwOnError: (error) => error.status >= 500, // Only throw 5xx
  })

  if (isError && error.status === 404) {
    return <EmptyState message="No todos found" />
  }

  return <ul>{data?.map(...)}</ul>
}
```

## Quick Reference

| Error Type | Strategy |
|------------|----------|
| Network failure | Global toast + retry |
| 5xx server error | Error Boundary |
| 404 Not Found | Local state |
| 400 Validation | Local state (show form errors) |
| 401 Unauthorized | Global redirect to login |
| Background refetch fail | Global toast only |
| Mutation fail | Local state or global toast |

## Additional Resources

### Reference Files

For detailed patterns and advanced techniques, consult:
- **`references/retry-patterns.md`** - Retry strategies and configuration

### Related Skills

- **tanstack-query** - Core concepts, staleTime
- **tanstack-mutations** - Mutation-specific error handling
- **tanstack-types** - Typed error handling
