---
name: tanstack-query-basics
description: TanStack Query fundamentals including useQuery, useMutation, query keys, and cache management. Use when working with data fetching, caching, or basic query patterns.
---

# TanStack Query Basics

## useQuery

```typescript
const { data, isLoading, isError, error } = useQuery({
  queryKey: ['users', 'list'],
  queryFn: async () => {
    const response = await fetch('/api/users')
    return response.json()
  },
})
```

## useQuery with Params

```typescript
const userId = ref('123')

const { data } = useQuery({
  queryKey: ['users', 'detail', userId],
  queryFn: async () => {
    const response = await fetch(`/api/users/${userId.value}`)
    return response.json()
  },
})
```

## useMutation

```typescript
const { mutate, isPending, isError, error } = useMutation({
  mutationFn: async (userData: CreateUser) => {
    const response = await fetch('/api/users', {
      method: 'POST',
      body: JSON.stringify(userData),
    })
    return response.json()
  },
  onSuccess: () => {
    showToast({ variant: 'success' })
  },
  onError: (error) => {
    showToast({ variant: 'error', title: error.message })
  },
})

// Trigger mutation
mutate({ name: 'John', email: 'john@example.com' })
```

## Query Keys

Hierarchical structure for cache control:

```typescript
const userKeys = {
  all: ['users'] as const,
  lists: () => [...userKeys.all, 'list'] as const,
  list: (filters: Filters) => [...userKeys.lists(), filters] as const,
  details: () => [...userKeys.all, 'detail'] as const,
  detail: (id: string) => [...userKeys.details(), id] as const,
}
```

## Cache Invalidation

```typescript
const queryClient = useQueryClient()

// Invalidate all user queries
queryClient.invalidateQueries({ queryKey: userKeys.all })

// Invalidate specific detail
queryClient.invalidateQueries({ queryKey: userKeys.detail('123') })

// Invalidate all lists
queryClient.invalidateQueries({ queryKey: userKeys.lists() })
```

## Enabled Queries

```typescript
const { data } = useQuery({
  queryKey: ['user', userId],
  queryFn: () => fetchUser(userId.value),
  enabled: computed(() => !!userId.value), // Only run when userId exists
})
```

## keepPreviousData

```typescript
const { data } = useQuery({
  queryKey: ['users', page],
  queryFn: () => fetchUsers(page.value),
  placeholderData: keepPreviousData, // Keep old data while fetching new
})
```

## Dependent Queries

```typescript
const { data: user } = useQuery({
  queryKey: ['user', userId],
  queryFn: () => fetchUser(userId.value),
})

const { data: posts } = useQuery({
  queryKey: ['posts', userId],
  queryFn: () => fetchUserPosts(userId.value),
  enabled: computed(() => !!user.value), // Wait for user
})
```

## Stale Time

```typescript
const { data } = useQuery({
  queryKey: ['users'],
  queryFn: fetchUsers,
  staleTime: 1000 * 60 * 5, // Consider data fresh for 5 minutes
})
```

## Refetch Intervals

```typescript
const { data } = useQuery({
  queryKey: ['live-data'],
  queryFn: fetchLiveData,
  refetchInterval: 5000, // Refetch every 5 seconds
})
```

## Select (Transform Data)

```typescript
const { data } = useQuery({
  queryKey: ['users'],
  queryFn: fetchUsers,
  select: (data) =>
    data.map((user) => ({
      ...user,
      fullName: `${user.firstName} ${user.lastName}`,
    })),
})
```

## Error Handling

```typescript
const { data, isError, error } = useQuery({
  queryKey: ['users'],
  queryFn: fetchUsers,
})

watchEffect(() => {
  if (isError.value) {
    showToast({ variant: 'error', title: error.value.message })
  }
})
```

## Mutation with Invalidation

```typescript
const queryClient = useQueryClient()

const { mutate } = useMutation({
  mutationFn: createUser,
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: userKeys.lists() })
  },
})
```

## Query Status

```typescript
const { data, status, fetchStatus } = useQuery({
  queryKey: ['users'],
  queryFn: fetchUsers,
})

// status: 'pending' | 'error' | 'success'
// fetchStatus: 'fetching' | 'paused' | 'idle'
```

## Reactive Wrapper

```typescript
const query = reactive(useQuery({
  queryKey: ['users'],
  queryFn: fetchUsers,
}))

// Enables v-model binding
<nord-input v-model="query.data.name" />
```
