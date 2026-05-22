---
name: TanStack Query Core
description: This skill should be used when the user asks about "TanStack Query", "React Query", "useQuery", "query keys", "staleTime", "query client setup", "query factories", "queryOptions", or needs guidance on core TanStack Query concepts, mental models, and setup patterns.
version: 1.0.0
---

# TanStack Query Core Patterns

This skill provides guidance for working with TanStack Query (formerly React Query), covering mental models, setup, and core patterns based on best practices from TKDodo (the library maintainer).

## Core Mental Model

TanStack Query is an **async state manager**, not a data fetching library. Understanding this distinction is fundamental:

- It manages any asynchronous state through Promises
- The actual data fetching happens in `queryFn` using any tool (axios, fetch, etc.)
- It synchronizes data across the application using unique `QueryKey` identifiers

### Server State vs Client State

Server state differs fundamentally from client state:
- It's a snapshot in time that can become outdated
- Multiple users may modify it simultaneously
- It requires automatic synchronization to stay current

**Critical rule**: Use TanStack Query exclusively for async/server state. Manage client state (filters, UI toggles) separately using local state, context, or other state managers.

## The Query Options API (v5+)

The recommended pattern for defining queries uses `queryOptions()` for type safety and reusability:

```typescript
import { queryOptions, useQuery } from '@tanstack/react-query'

// Define query options - reusable across useQuery, prefetch, etc.
const todoQueryOptions = (id: string) => queryOptions({
  queryKey: ['todos', id],
  queryFn: () => fetchTodo(id),
  staleTime: 5 * 60 * 1000, // 5 minutes
})

// Usage in component
const { data } = useQuery(todoQueryOptions(id))

// Usage in prefetch
await queryClient.prefetchQuery(todoQueryOptions(id))
```

### Query Factories Pattern

Organize related queries using factory functions:

```typescript
export const todoQueries = {
  all: () => queryOptions({
    queryKey: ['todos'],
    queryFn: fetchAllTodos,
  }),

  lists: () => queryOptions({
    queryKey: ['todos', 'list'],
    queryFn: fetchTodoLists,
  }),

  detail: (id: string) => queryOptions({
    queryKey: ['todos', 'detail', id],
    queryFn: () => fetchTodo(id),
    staleTime: 5 * 60 * 1000,
  }),
}

// Usage
const { data } = useQuery(todoQueries.detail(id))
queryClient.invalidateQueries({ queryKey: ['todos'] }) // invalidates all
```

## Understanding staleTime

`staleTime` is the most important configuration option. The default of 0ms means data is immediately considered stale.

### How staleTime Works

- **Fresh data** (within staleTime): Served from cache only, no refetch
- **Stale data** (beyond staleTime): Served from cache, refetch in background

### Configuring staleTime

```typescript
// For rarely changing data
queryOptions({
  queryKey: ['config'],
  queryFn: fetchConfig,
  staleTime: Infinity, // Never refetch automatically
})

// For frequently updated data
queryOptions({
  queryKey: ['notifications'],
  queryFn: fetchNotifications,
  staleTime: 30 * 1000, // 30 seconds
})

// Default for most cases
queryOptions({
  queryKey: ['todos'],
  queryFn: fetchTodos,
  staleTime: 5 * 60 * 1000, // 5 minutes - reasonable default
})
```

### Global Defaults

Set sensible defaults at the QueryClient level:

```typescript
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 60 * 1000, // 1 minute default
      gcTime: 5 * 60 * 1000, // 5 minutes garbage collection
    },
  },
})
```

## Query Keys as Dependencies

Always include query parameters in the queryKey. This ensures:
- Separate cache entries per input
- Automatic refetches when parameters change
- No stale closure bugs
- No race conditions

```typescript
// CORRECT: Parameters in queryKey
const todoQuery = (id: string) => queryOptions({
  queryKey: ['todos', id],
  queryFn: () => fetchTodo(id),
})

// INCORRECT: Parameter only in queryFn
const todoQuery = (id: string) => queryOptions({
  queryKey: ['todos'], // Missing id!
  queryFn: () => fetchTodo(id),
})
```

## Smart Refetch Triggers

Configure automatic refetching at strategic moments:

```typescript
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnMount: true,        // When component mounts
      refetchOnWindowFocus: true,  // When tab gains focus (great for production)
      refetchOnReconnect: true,    // When network reconnects
    },
  },
})
```

**Important**: Don't disable these mechanisms. Instead, adjust `staleTime` to control when refetches actually happen.

## Common Anti-Patterns to Avoid

### 1. Passing Parameters to refetch()

```typescript
// WRONG: Trying to pass parameters
const { refetch } = useQuery(todoQuery(id))
refetch({ id: newId }) // This doesn't work!

// CORRECT: Use state to change the query
const [todoId, setTodoId] = useState(id)
const { data } = useQuery(todoQuery(todoId))
setTodoId(newId) // This triggers a new query
```

### 2. Using for Client State

TanStack Query is not for synchronous UI state (toggles, preferences). Use Zustand, Jotai, or React state for client-only state.

### 3. Creating QueryClient Inside Component

```typescript
// WRONG: New client on every render = cache reset
function App() {
  const queryClient = new QueryClient() // Bad!
  return <QueryClientProvider client={queryClient}>...</QueryClientProvider>
}

// CORRECT: Create outside component or use useState
const queryClient = new QueryClient()
function App() {
  return <QueryClientProvider client={queryClient}>...</QueryClientProvider>
}
```

## Selectors with `select`

Use `select` for fine-grained subscriptions:

```typescript
const productQuery = (id: string) => queryOptions({
  queryKey: ['products', id],
  queryFn: () => fetchProduct(id),
})

// Select specific fields - component only re-renders when title changes
const { data: title } = useQuery({
  ...productQuery(id),
  select: (data) => data.title,
})
```

For expensive transformations, stabilize with `useCallback`:

```typescript
const { data } = useQuery({
  ...productQuery(id),
  select: useCallback(
    (data: Product) => filterByRating(data, minRating),
    [minRating]
  ),
})
```

## Suspense Integration (v5+)

`useSuspenseQuery` provides type-safe guaranteed data:

```typescript
// Data is guaranteed to exist (no undefined check needed)
const { data } = useSuspenseQuery(todoQuery(id))
// data is Todo, not Todo | undefined
```

Wrap with Suspense boundary:

```typescript
<Suspense fallback={<Loading />}>
  <TodoDetail id={id} />
</Suspense>
```

## Quick Reference Table

| Concept | Recommendation |
|---------|----------------|
| Query definition | Use `queryOptions()` helper |
| Query organization | Use query factories |
| staleTime | Start with 60s, adjust per resource |
| Parameters | Always include in queryKey |
| Client state | Don't use RQ, use separate state |
| Refetch control | Adjust staleTime, don't disable refetch |
| Type safety | Let queryFn return type flow through |

## Additional Resources

### Reference Files

For detailed patterns and advanced techniques, consult:
- **`references/gotchas.md`** - Common mistakes and FAQs from TKDodo
- **`references/context-integration.md`** - Using React Query with React Context

### Related Skills

- **tanstack-mutations** - Mutation patterns, invalidation, optimistic updates
- **tanstack-types** - Type safety with queryOptions and Zod
- **tanstack-errors** - Error handling strategies
- **tanstack-forms** - Forms integration patterns
