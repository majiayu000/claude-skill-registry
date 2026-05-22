---
name: TanStack Mutations
description: This skill should be used when the user asks about "useMutation", "mutations", "query invalidation", "optimistic updates", "cache updates", "setQueryData", "invalidateQueries", "onMutate", "onSettled", or needs guidance on mutation patterns, cache synchronization, and optimistic UI in TanStack Query.
version: 1.0.0
---

# TanStack Query Mutation Patterns

This skill provides guidance for working with mutations in TanStack Query, covering invalidation strategies, optimistic updates, and cache synchronization based on TKDodo's best practices.

## Understanding Mutations

Mutations are functions with side effects that modify server state. Unlike queries (declarative, automatic), mutations are imperative—invoke them when needed.

### Key Differences from Queries

| Aspect | useQuery | useMutation |
|--------|----------|-------------|
| Execution | Automatic, declarative | Manual, imperative |
| State Sharing | Cached and shared | Not shared between instances |
| Lifecycle | Controlled by component mount | Controlled by mutate() calls |

## Basic Mutation Setup

```typescript
import { useMutation, useQueryClient } from '@tanstack/react-query'

function TodoItem({ todo }: { todo: Todo }) {
  const queryClient = useQueryClient()

  const updateMutation = useMutation({
    mutationFn: (updates: Partial<Todo>) =>
      api.patch(`/todos/${todo.id}`, updates),

    onSuccess: () => {
      // Invalidate related queries after successful mutation
      queryClient.invalidateQueries({ queryKey: ['todos'] })
    },
  })

  return (
    <button
      onClick={() => updateMutation.mutate({ completed: true })}
      disabled={updateMutation.isPending}
    >
      Complete
    </button>
  )
}
```

## Two Primary Cache Synchronization Strategies

### Strategy 1: Query Invalidation

Invalidate queries to trigger refetch. Best for most cases:

```typescript
const deleteMutation = useMutation({
  mutationFn: (id: string) => api.delete(`/todos/${id}`),

  onSuccess: () => {
    // Fuzzy matching - invalidates all queries starting with ['todos']
    queryClient.invalidateQueries({ queryKey: ['todos'] })
  },
})
```

**Key behaviors:**
- Fuzzy matching: `['todos']` invalidates `['todos', 'list']`, `['todos', 'detail', id]`, etc.
- Only active queries refetch immediately
- Inactive queries marked stale until reused

### Strategy 2: Direct Cache Updates

Update cache directly when mutation returns complete data:

```typescript
const updateMutation = useMutation({
  mutationFn: (updates: Partial<Todo>) =>
    api.patch(`/todos/${todo.id}`, updates),

  onSuccess: (updatedTodo) => {
    // Update specific query cache directly
    queryClient.setQueryData(
      ['todos', 'detail', todo.id],
      updatedTodo
    )

    // Also update list caches if needed
    queryClient.setQueryData(['todos', 'list'], (old: Todo[] | undefined) =>
      old?.map(t => t.id === todo.id ? updatedTodo : t)
    )
  },
})
```

**When to use direct updates:**
- Mutation returns complete updated entity
- Need immediate UI update without network roundtrip
- Simple transformations (no complex list filtering)

## Callback Best Practices

### Separate Concerns: useMutation vs mutate Callbacks

```typescript
// useMutation callbacks: Logic-based, runs always
const mutation = useMutation({
  mutationFn: createTodo,

  onSuccess: () => {
    // Always runs: cache invalidation, logging
    queryClient.invalidateQueries({ queryKey: ['todos'] })
    analytics.track('todo_created')
  },

  onError: (error) => {
    // Always runs: error logging
    logger.error('Failed to create todo', error)
  },
})

// mutate callbacks: UI-specific, component-scoped
mutation.mutate(newTodo, {
  onSuccess: () => {
    // Only runs if component still mounted
    toast.success('Todo created!')
    navigate('/todos')
  },
})
```

**Why this matters:** useMutation callbacks run even if component unmounts. mutate callbacks don't run if component unmounted—perfect for UI effects.

### Return invalidateQueries for Loading State

Keep mutation in loading state while queries refetch:

```typescript
const mutation = useMutation({
  mutationFn: updateTodo,

  onSuccess: () => {
    // Return the promise to keep mutation pending
    return queryClient.invalidateQueries({ queryKey: ['todos'] })
  },
})

// mutation.isPending stays true until queries finish refetching
```

## mutate vs mutateAsync

Prefer `mutate` over `mutateAsync` unless managing concurrent mutations:

```typescript
// PREFERRED: mutate handles errors internally
mutation.mutate(data, {
  onError: (error) => {
    toast.error(error.message)
  },
})

// ONLY when needed: mutateAsync requires manual error handling
try {
  await mutation.mutateAsync(data)
  // Do something after
} catch (error) {
  // MUST handle error - not automatic
  toast.error(error.message)
}
```

## Single Argument Rule

Mutations only accept a single argument. Pass objects for multiple variables:

```typescript
// WRONG: Multiple arguments
mutate(title, body) // Doesn't work!

// CORRECT: Object argument
mutate({ title, body })

// In mutation definition
const mutation = useMutation({
  mutationFn: ({ title, body }: { title: string; body: string }) =>
    api.post('/todos', { title, body }),
})
```

## Optimistic Updates

### Basic Pattern

```typescript
const updateMutation = useMutation({
  mutationFn: (newTodo: Partial<Todo>) =>
    api.patch(`/todos/${todo.id}`, newTodo),

  onMutate: async (newTodo) => {
    // 1. Cancel outgoing refetches
    await queryClient.cancelQueries({ queryKey: ['todos', todo.id] })

    // 2. Snapshot previous value
    const previousTodo = queryClient.getQueryData(['todos', todo.id])

    // 3. Optimistically update
    queryClient.setQueryData(['todos', todo.id], (old: Todo) => ({
      ...old,
      ...newTodo,
    }))

    // 4. Return context for rollback
    return { previousTodo }
  },

  onError: (err, newTodo, context) => {
    // Rollback on error
    if (context?.previousTodo) {
      queryClient.setQueryData(['todos', todo.id], context.previousTodo)
    }
  },

  onSettled: () => {
    // Always refetch to ensure consistency
    queryClient.invalidateQueries({ queryKey: ['todos', todo.id] })
  },
})
```

### Concurrent Optimistic Updates

Prevent "windows of inconsistency" with concurrent mutations:

```typescript
const toggleMutation = useMutation({
  mutationKey: ['todos', 'toggle'], // Important for isMutating check

  mutationFn: (id: string) => api.patch(`/todos/${id}/toggle`),

  onMutate: async (id) => {
    // Cancel queries to prevent overwriting optimistic update
    await queryClient.cancelQueries({ queryKey: ['todos', id] })

    const previousTodo = queryClient.getQueryData(['todos', id])
    queryClient.setQueryData(['todos', id], (old: Todo) => ({
      ...old,
      completed: !old.completed,
    }))

    return { previousTodo }
  },

  onSettled: (data, error, id) => {
    // Only invalidate if this is the last mutation
    if (queryClient.isMutating({ mutationKey: ['todos', 'toggle'] }) === 1) {
      queryClient.invalidateQueries({ queryKey: ['todos', id] })
    }
  },
})
```

**Why check isMutating:** Concurrent mutations without this pattern create "windows of inconsistency where state toggles back and forth."

## Automatic Invalidation Patterns

### Global Mutation Cache Callbacks

Invalidate everything after every mutation:

```typescript
const queryClient = new QueryClient({
  mutationCache: new MutationCache({
    onSuccess: () => {
      queryClient.invalidateQueries()
    },
  }),
})
```

### MutationKey-Based Filtering

Tie invalidation to mutation categories:

```typescript
const queryClient = new QueryClient({
  mutationCache: new MutationCache({
    onSuccess: (_data, _variables, _context, mutation) => {
      if (mutation.options.mutationKey) {
        // Invalidate queries matching mutation key
        queryClient.invalidateQueries({
          queryKey: mutation.options.mutationKey,
        })
      } else {
        // No key = invalidate everything
        queryClient.invalidateQueries()
      }
    },
  }),
})

// Usage
useMutation({
  mutationKey: ['todos'], // Only invalidates todo queries
  mutationFn: createTodo,
})
```

## Caution: Optimistic Updates Complexity

Use optimistic updates selectively:

> "The code needed to make optimistic updates work is non-trivial"

**Consider whether instant feedback is truly necessary:**
- Simple toggles: Often worth it
- Complex list updates: May require duplicating server logic
- Forms: Usually better to show loading state

## Quick Reference

| Pattern | Use When |
|---------|----------|
| Query invalidation | Most cases, simple and reliable |
| Direct cache update | Mutation returns complete data, need instant UI |
| Optimistic update | User expects instant feedback, can handle rollback |
| mutate callbacks | UI effects (toast, navigation) |
| useMutation callbacks | Logic (invalidation, logging) |

## Additional Resources

### Reference Files

For detailed patterns and advanced techniques, consult:
- **`references/optimistic-patterns.md`** - Advanced optimistic update scenarios
- **`references/invalidation-strategies.md`** - Automatic invalidation patterns

### Related Skills

- **tanstack-query** - Core concepts, query factories, staleTime
- **tanstack-types** - Type safety with mutations
- **tanstack-errors** - Error handling in mutations
