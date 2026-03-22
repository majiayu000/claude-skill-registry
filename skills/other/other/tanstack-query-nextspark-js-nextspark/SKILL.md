---
name: tanstack-query
description: |
  TanStack Query (React Query) patterns for data fetching in this Next.js application.
  Covers useQuery, useMutation, optimistic updates, cache invalidation, and anti-patterns.
  Use this skill when implementing data fetching or state management with server data.
allowed-tools: Read, Glob, Grep
version: 1.0.0
---

# TanStack Query Skill

Data fetching patterns and best practices with TanStack Query (React Query).

## Architecture Overview

```
core/providers/
└── query-provider.tsx           # QueryClient configuration

core/hooks/
├── useEntityQuery.ts            # Generic entity query hook
├── useEntityMutations.ts        # CRUD mutations with optimistic updates
└── useUserProfile.ts            # Example simple mutation
```

## When to Use This Skill

- Fetching data from API endpoints
- Implementing CRUD operations
- Managing server state and caching
- Implementing optimistic updates
- Avoiding useEffect anti-patterns

## Query Client Setup

```typescript
// core/providers/query-provider.tsx
export function QueryProvider({ children }: { children: React.ReactNode }) {
  const [queryClient] = useState(
    () =>
      new QueryClient({
        defaultOptions: {
          queries: {
            staleTime: 60 * 1000,           // 1 minute default
            refetchOnWindowFocus: false,    // Disabled
          },
        },
      })
  )

  return (
    <QueryClientProvider client={queryClient}>
      {children}
      {process.env.NEXT_PUBLIC_RQ_DEVTOOLS === 'true' && (
        <ReactQueryDevtools initialIsOpen={false} />
      )}
    </QueryClientProvider>
  )
}
```

**Key Configuration:**

| Setting | Value | Reason |
|---------|-------|--------|
| `staleTime` | 60 seconds | Prevents excessive refetching |
| `refetchOnWindowFocus` | false | Manual control over refetching |
| `gcTime` | 5 minutes (default) | Cache cleanup |

## Query Key Conventions

Query keys should be hierarchical arrays for proper cache management:

```typescript
// Pattern: ['domain', 'resource', filters, id]

// Entity list with filters
['entity', 'tasks', { page: 1, search: 'test', status: 'active' }]

// Single entity
['entity', 'tasks', 'task-123']

// Single entity with options
['entity', 'tasks', 'task-123', { includeChildren: true }]

// User-specific data
['user-profile']
['user-settings', 'notifications']

// Admin data
['superadmin-users', search, roleFilter, statusFilter, page]
```

## useQuery Patterns

### Basic Query

```typescript
import { useQuery } from '@tanstack/react-query'

function useTaskList(filters: TaskFilters) {
  return useQuery({
    queryKey: ['entity', 'tasks', filters],
    queryFn: async () => {
      const params = new URLSearchParams({
        page: String(filters.page),
        limit: String(filters.limit),
        ...(filters.status && { status: filters.status }),
        ...(filters.search && { search: filters.search }),
      })

      const response = await fetch(`/api/v1/tasks?${params}`)
      if (!response.ok) {
        throw new Error('Failed to fetch tasks')
      }
      return response.json()
    },
  })
}
```

### Query with Conditional Enabling

```typescript
function useTask(id: string | null) {
  return useQuery({
    queryKey: ['entity', 'tasks', id],
    queryFn: async () => {
      const response = await fetch(`/api/v1/tasks/${id}`)
      if (!response.ok) throw new Error('Failed to fetch task')
      return response.json()
    },
    enabled: !!id,  // Only fetch when id exists
  })
}
```

### Query with Authentication Guard

```typescript
function useEntityQuery(entityConfig: EntityConfig, filters: Filters) {
  const { user } = useAuth()

  return useQuery({
    queryKey: ['entity', entityConfig.slug, filters],
    queryFn: async () => {
      const response = await fetch(`/api/v1/${entityConfig.slug}?${params}`)
      if (!response.ok) throw new Error('Failed to fetch')
      return response.json()
    },
    enabled: !!user,  // Only fetch when authenticated
    staleTime: 1000 * 60 * 5,   // 5 minutes for entity lists
    gcTime: 1000 * 60 * 60,     // 1 hour garbage collection
  })
}
```

### Query Options Summary

| Option | Type | Description |
|--------|------|-------------|
| `queryKey` | `unknown[]` | Cache key (required) |
| `queryFn` | `() => Promise<T>` | Fetch function (required) |
| `enabled` | `boolean` | Conditional fetching |
| `staleTime` | `number` | Time before data is stale (ms) |
| `gcTime` | `number` | Cache retention time (ms) |
| `retry` | `number \| boolean` | Retry attempts |
| `refetchOnWindowFocus` | `boolean` | Refetch on tab focus |
| `refetchInterval` | `number` | Polling interval (ms) |

## useMutation Patterns

### Simple Mutation

```typescript
import { useMutation, useQueryClient } from '@tanstack/react-query'

function useCreateTask() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: async (data: CreateTaskData) => {
      const response = await fetch('/api/v1/tasks', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      })
      if (!response.ok) throw new Error('Failed to create task')
      return response.json()
    },
    onSuccess: () => {
      // Invalidate all task queries to refetch
      queryClient.invalidateQueries({ queryKey: ['entity', 'tasks'] })
    },
  })
}

// Usage
function CreateTaskForm() {
  const createTask = useCreateTask()

  const handleSubmit = async (data: CreateTaskData) => {
    try {
      await createTask.mutateAsync(data)
      toast.success('Task created!')
    } catch (error) {
      toast.error('Failed to create task')
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      {/* form fields */}
      <Button disabled={createTask.isPending}>
        {createTask.isPending ? 'Creating...' : 'Create'}
      </Button>
    </form>
  )
}
```

### Mutation with Optimistic Updates

```typescript
function useEntityMutations(entityConfig: EntityConfig) {
  const queryClient = useQueryClient()
  const baseQueryKey = ['entity', entityConfig.slug]

  const createMutation = useMutation({
    mutationFn: async (data: Record<string, unknown>) => {
      const response = await fetch(`/api/v1/${entityConfig.slug}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      })
      if (!response.ok) throw new Error('Failed to create')
      return response.json()
    },

    // OPTIMISTIC UPDATE
    onMutate: async (newItem) => {
      // 1. Cancel outgoing refetches to avoid overwriting optimistic update
      await queryClient.cancelQueries({ queryKey: baseQueryKey })

      // 2. Snapshot current data for rollback
      const previousData = queryClient.getQueriesData({ queryKey: baseQueryKey })

      // 3. Optimistically update all matching queries
      queryClient.setQueriesData({ queryKey: baseQueryKey }, (old: any) => {
        if (!old?.items) return old
        return {
          ...old,
          items: [
            { ...newItem, id: `temp-${Date.now()}` },  // Temporary ID
            ...old.items
          ],
          total: old.total + 1,
        }
      })

      // 4. Return context for rollback
      return { previousData }
    },

    // ROLLBACK ON ERROR
    onError: (error, variables, context) => {
      if (context?.previousData) {
        context.previousData.forEach(([queryKey, data]) => {
          queryClient.setQueryData(queryKey, data)
        })
      }
      toast.error('Failed to create item')
    },

    // SYNC WITH SERVER
    onSettled: () => {
      // Always refetch after mutation to sync with server
      queryClient.invalidateQueries({ queryKey: baseQueryKey })
    },
  })

  const updateMutation = useMutation({
    mutationFn: async ({ id, data }: { id: string; data: Record<string, unknown> }) => {
      const response = await fetch(`/api/v1/${entityConfig.slug}/${id}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      })
      if (!response.ok) throw new Error('Failed to update')
      return response.json()
    },

    onMutate: async ({ id, data }) => {
      await queryClient.cancelQueries({ queryKey: baseQueryKey })
      const previousData = queryClient.getQueriesData({ queryKey: baseQueryKey })

      // Update item in all matching queries
      queryClient.setQueriesData({ queryKey: baseQueryKey }, (old: any) => {
        if (!old?.items) return old
        return {
          ...old,
          items: old.items.map((item: any) =>
            item.id === id ? { ...item, ...data } : item
          ),
        }
      })

      return { previousData }
    },

    onError: (error, variables, context) => {
      if (context?.previousData) {
        context.previousData.forEach(([queryKey, data]) => {
          queryClient.setQueryData(queryKey, data)
        })
      }
    },

    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: baseQueryKey })
    },
  })

  const deleteMutation = useMutation({
    mutationFn: async (id: string) => {
      const response = await fetch(`/api/v1/${entityConfig.slug}/${id}`, {
        method: 'DELETE',
      })
      if (!response.ok) throw new Error('Failed to delete')
      return response.json()
    },

    onMutate: async (id) => {
      await queryClient.cancelQueries({ queryKey: baseQueryKey })
      const previousData = queryClient.getQueriesData({ queryKey: baseQueryKey })

      // Remove item from all matching queries
      queryClient.setQueriesData({ queryKey: baseQueryKey }, (old: any) => {
        if (!old?.items) return old
        return {
          ...old,
          items: old.items.filter((item: any) => item.id !== id),
          total: old.total - 1,
        }
      })

      return { previousData }
    },

    onError: (error, variables, context) => {
      if (context?.previousData) {
        context.previousData.forEach(([queryKey, data]) => {
          queryClient.setQueryData(queryKey, data)
        })
      }
    },

    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: baseQueryKey })
    },
  })

  return {
    create: createMutation,
    update: updateMutation,
    delete: deleteMutation,
  }
}
```

## Cache Invalidation Strategies

### Broad Invalidation

Affects all queries with matching prefix:

```typescript
// Invalidate all task queries (any filters)
queryClient.invalidateQueries({ queryKey: ['entity', 'tasks'] })

// Invalidate all entity queries
queryClient.invalidateQueries({ queryKey: ['entity'] })
```

### Specific Invalidation

Target specific queries:

```typescript
// Invalidate single task
queryClient.invalidateQueries({
  queryKey: ['entity', 'tasks', 'task-123']
})

// Invalidate list with specific filters
queryClient.invalidateQueries({
  queryKey: ['entity', 'tasks', { status: 'active' }],
  exact: true  // Only exact match
})
```

### Direct Cache Update

Update without refetch:

```typescript
// Update single item in cache
queryClient.setQueryData(
  ['entity', 'tasks', 'task-123'],
  (old) => ({ ...old, status: 'completed' })
)

// Update all matching queries
queryClient.setQueriesData(
  { queryKey: ['entity', 'tasks'] },
  (old: any) => ({
    ...old,
    items: old.items.map((item: any) =>
      item.id === 'task-123' ? { ...item, status: 'completed' } : item
    ),
  })
)
```

## State Management Hierarchy

```
1. Server State      → TanStack Query (useQuery, useMutation)
2. URL State         → Search params (shareable, bookmarkable)
3. Component State   → useState (local, ephemeral)
4. Context API       → Cross-component (theme, auth, user)
5. External Stores   → useSyncExternalStore (third-party)
```

**Rule:** Use TanStack Query for ALL server data. Don't store server data in useState.

## Loading & Error States

```typescript
function TaskList() {
  const { data, isLoading, isError, error, refetch } = useTaskList(filters)

  if (isLoading) {
    return <Skeleton count={5} />
  }

  if (isError) {
    return (
      <Alert variant="destructive">
        <AlertTitle>Error</AlertTitle>
        <AlertDescription>
          {error.message}
          <Button onClick={() => refetch()}>Retry</Button>
        </AlertDescription>
      </Alert>
    )
  }

  return (
    <ul>
      {data.items.map((task) => (
        <TaskItem key={task.id} task={task} />
      ))}
    </ul>
  )
}
```

### State Properties

| Property | Description |
|----------|-------------|
| `isLoading` | First fetch, no data yet |
| `isFetching` | Any fetch (including background) |
| `isPending` | Mutation in progress |
| `isError` | Query/mutation failed |
| `isSuccess` | Query/mutation succeeded |
| `data` | Query result |
| `error` | Error object |

## Anti-Patterns (CRITICAL)

### FORBIDDEN: useEffect for Data Fetching

```typescript
// ❌ NEVER DO THIS
function TaskList() {
  const [tasks, setTasks] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    setLoading(true)
    fetch('/api/v1/tasks')
      .then(res => res.json())
      .then(data => {
        setTasks(data.items)
        setLoading(false)
      })
  }, [])

  // Problems: No caching, no error handling, no refetch, race conditions
}

// ✅ CORRECT
function TaskList() {
  const { data, isLoading, error } = useQuery({
    queryKey: ['entity', 'tasks'],
    queryFn: () => fetch('/api/v1/tasks').then(res => res.json())
  })

  // Benefits: Caching, error handling, automatic refetch, deduplication
}
```

### FORBIDDEN: useEffect for Derived State

```typescript
// ❌ NEVER DO THIS
function TaskStats({ tasks }) {
  const [completedCount, setCompletedCount] = useState(0)

  useEffect(() => {
    setCompletedCount(tasks.filter(t => t.status === 'completed').length)
  }, [tasks])
}

// ✅ CORRECT - Calculate during render
function TaskStats({ tasks }) {
  const completedCount = useMemo(
    () => tasks.filter(t => t.status === 'completed').length,
    [tasks]
  )
}
```

### FORBIDDEN: Storing Server Data in State

```typescript
// ❌ NEVER DO THIS
function TaskPage() {
  const { data } = useTaskList()
  const [tasks, setTasks] = useState([])

  useEffect(() => {
    if (data) setTasks(data.items)
  }, [data])

  // Now have TWO sources of truth!
}

// ✅ CORRECT - Use query data directly
function TaskPage() {
  const { data } = useTaskList()
  const tasks = data?.items ?? []

  // Single source of truth
}
```

### FORBIDDEN: Missing Query Keys for Filters

```typescript
// ❌ WRONG - Same key regardless of filters
useQuery({
  queryKey: ['tasks'],
  queryFn: () => fetch(`/api/v1/tasks?status=${status}`)
})

// ✅ CORRECT - Include filters in key
useQuery({
  queryKey: ['tasks', { status }],
  queryFn: () => fetch(`/api/v1/tasks?status=${status}`)
})
```

## Key Conventions

| Aspect | Convention |
|--------|-----------|
| **Query Keys** | `['domain', 'resource', filters, id]` |
| **Stale Time** | 60s (global), 5min (entity lists) |
| **GC Time** | 1 hour |
| **Retry** | 2 attempts |
| **Window Refetch** | Disabled |
| **Enabled Guard** | `enabled: !!user && conditions` |
| **Optimistic IDs** | `temp-${Date.now()}` |
| **Error Handling** | Throw in queryFn, toast in onError |

## Checklist

Before finalizing data fetching:

- [ ] Uses TanStack Query (not useEffect + useState)
- [ ] Query key includes all cache-affecting parameters
- [ ] Enabled guard for conditional queries
- [ ] Proper error handling with user feedback
- [ ] Loading states with Skeleton components
- [ ] Mutations invalidate related queries
- [ ] Optimistic updates for better UX (where appropriate)
- [ ] No server data stored in useState
- [ ] No derived state in useEffect

## Related Skills

- `entity-api` - API endpoint patterns
- `shadcn-components` - Loading/error UI components
- `react-patterns` - React best practices
