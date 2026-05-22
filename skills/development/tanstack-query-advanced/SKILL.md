---
name: tanstack-query-advanced
description: Advanced TanStack Query v5 patterns for infinite queries, optimistic updates, prefetching, gcTime, and queryOptions. Use when building data fetching, caching, or optimistic updates.
tags: [tanstack-query, react-query, caching, infinite-scroll, optimistic-updates, prefetching, suspense]
context: fork
agent: frontend-ui-developer
version: 1.0.0
allowed-tools: [Read, Write, Grep, Glob]
author: SkillForge
user-invocable: false
---

# TanStack Query Advanced

Production patterns for TanStack Query v5 - server state management done right.

## Overview

- Infinite scroll / pagination
- Optimistic UI updates
- Prefetching for instant navigation
- Complex cache invalidation
- Dependent/parallel queries
- Mutations with rollback

## Core Patterns

### 1. Infinite Queries (Cursor-Based)

```typescript
import { useInfiniteQuery } from '@tanstack/react-query';

interface Page {
  items: Item[];
  nextCursor: string | null;
}

function useInfiniteItems() {
  return useInfiniteQuery({
    queryKey: ['items'],
    queryFn: async ({ pageParam }): Promise<Page> => {
      const res = await fetch(`/api/items?cursor=${pageParam ?? ''}`);
      return res.json();
    },
    initialPageParam: null as string | null,
    getNextPageParam: (lastPage) => lastPage.nextCursor,
    getPreviousPageParam: (firstPage) => firstPage.prevCursor,
  });
}

// Component
function ItemList() {
  const { data, fetchNextPage, hasNextPage, isFetchingNextPage } = useInfiniteItems();

  return (
    <>
      {data?.pages.flatMap((page) => page.items.map((item) => (
        <ItemCard key={item.id} item={item} />
      )))}
      <button
        onClick={() => fetchNextPage()}
        disabled={!hasNextPage || isFetchingNextPage}
      >
        {isFetchingNextPage ? 'Loading...' : hasNextPage ? 'Load More' : 'No more'}
      </button>
    </>
  );
}
```

### 2. Optimistic Updates

```typescript
import { useMutation, useQueryClient } from '@tanstack/react-query';

function useUpdateTodo() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: updateTodo,
    onMutate: async (newTodo) => {
      // Cancel outgoing refetches
      await queryClient.cancelQueries({ queryKey: ['todos', newTodo.id] });

      // Snapshot previous value
      const previousTodo = queryClient.getQueryData(['todos', newTodo.id]);

      // Optimistically update
      queryClient.setQueryData(['todos', newTodo.id], newTodo);

      // Return context for rollback
      return { previousTodo };
    },
    onError: (err, newTodo, context) => {
      // Rollback on error
      queryClient.setQueryData(['todos', newTodo.id], context?.previousTodo);
    },
    onSettled: (data, error, variables) => {
      // Always refetch after error or success
      queryClient.invalidateQueries({ queryKey: ['todos', variables.id] });
    },
  });
}
```

### 3. Prefetching Patterns

```typescript
// Prefetch on hover
function UserLink({ userId }: { userId: string }) {
  const queryClient = useQueryClient();

  const prefetchUser = () => {
    queryClient.prefetchQuery({
      queryKey: ['user', userId],
      queryFn: () => fetchUser(userId),
      staleTime: 5 * 60 * 1000, // 5 minutes
    });
  };

  return (
    <Link to={`/users/${userId}`} onMouseEnter={prefetchUser}>
      View User
    </Link>
  );
}

// Prefetch in loader (React Router)
export const loader = (queryClient: QueryClient) => async ({ params }) => {
  await queryClient.ensureQueryData({
    queryKey: ['user', params.id],
    queryFn: () => fetchUser(params.id),
  });
  return null;
};
```

### 4. Smart Cache Invalidation

```typescript
const queryClient = useQueryClient();

// Invalidate exact query
queryClient.invalidateQueries({ queryKey: ['todos', 1] });

// Invalidate all todos queries
queryClient.invalidateQueries({ queryKey: ['todos'] });

// Invalidate with predicate
queryClient.invalidateQueries({
  predicate: (query) =>
    query.queryKey[0] === 'todos' &&
    (query.queryKey[1] as Todo)?.status === 'done',
});

// Invalidate and refetch immediately
queryClient.refetchQueries({ queryKey: ['todos'], type: 'active' });

// Remove from cache entirely
queryClient.removeQueries({ queryKey: ['todos', 1] });
```

### 5. Dependent Queries

```typescript
function useUserPosts(userId: string) {
  // First query
  const userQuery = useQuery({
    queryKey: ['user', userId],
    queryFn: () => fetchUser(userId),
  });

  // Dependent query - only runs when user is loaded
  const postsQuery = useQuery({
    queryKey: ['posts', userId],
    queryFn: () => fetchUserPosts(userId),
    enabled: !!userQuery.data, // Only fetch when user exists
  });

  return { user: userQuery.data, posts: postsQuery.data };
}
```

### 6. Parallel Queries

```typescript
import { useQueries } from '@tanstack/react-query';

function useMultipleUsers(userIds: string[]) {
  return useQueries({
    queries: userIds.map((id) => ({
      queryKey: ['user', id],
      queryFn: () => fetchUser(id),
      staleTime: 5 * 60 * 1000,
    })),
    combine: (results) => ({
      users: results.map((r) => r.data).filter(Boolean),
      pending: results.some((r) => r.isPending),
      error: results.find((r) => r.error)?.error,
    }),
  });
}
```

### 7. Query Deduplication & Batching

```typescript
// Configure in QueryClient
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60, // 1 minute
      gcTime: 1000 * 60 * 5, // 5 minutes (formerly cacheTime)
      refetchOnWindowFocus: false,
      retry: 3,
      retryDelay: (attemptIndex) => Math.min(1000 * 2 ** attemptIndex, 30000),
    },
  },
});
```

### 8. Suspense Integration

```typescript
import { useSuspenseQuery } from '@tanstack/react-query';

function UserProfile({ userId }: { userId: string }) {
  // This will suspend until data is ready
  const { data: user } = useSuspenseQuery({
    queryKey: ['user', userId],
    queryFn: () => fetchUser(userId),
  });

  return <div>{user.name}</div>;
}

// Wrap with Suspense
<Suspense fallback={<Skeleton />}>
  <UserProfile userId="123" />
</Suspense>
```

### 9. Mutation State Tracking

```typescript
import { useMutationState } from '@tanstack/react-query';

function PendingTodos() {
  // Track all pending todo mutations
  const pendingMutations = useMutationState({
    filters: { mutationKey: ['addTodo'], status: 'pending' },
    select: (mutation) => mutation.state.variables as Todo,
  });

  return (
    <>
      {pendingMutations.map((todo) => (
        <TodoItem key={todo.id} todo={todo} isPending />
      ))}
    </>
  );
}
```

## Configuration Best Practices

```typescript
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60,       // Data fresh for 1 min
      gcTime: 1000 * 60 * 5,      // Cache for 5 min
      refetchOnWindowFocus: true, // Refetch on tab focus
      refetchOnReconnect: true,   // Refetch on network reconnect
      retry: 3,                   // Retry failed requests
    },
    mutations: {
      retry: 1,
      onError: (error) => toast.error(error.message),
    },
  },
});
```

## Quick Reference

```typescript
// ✅ Create typed query with queryOptions helper (v5)
const userQueryOptions = (id: string) => queryOptions({
  queryKey: ['user', id] as const,
  queryFn: () => fetchUser(id),
  staleTime: 5 * 60 * 1000,
});

// ✅ Use the query options for consistency
const { data } = useQuery(userQueryOptions(userId));
await queryClient.prefetchQuery(userQueryOptions(userId));
await queryClient.ensureQueryData(userQueryOptions(userId));

// ✅ v5: isPending instead of isLoading (initial load only)
if (isPending) return <Skeleton />;

// ✅ v5: gcTime instead of cacheTime
gcTime: 5 * 60 * 1000,

// ✅ useSuspenseQuery for Suspense integration
const { data } = useSuspenseQuery(userQueryOptions(userId));

// ✅ Selective invalidation
queryClient.invalidateQueries({ queryKey: ['todos'], exact: true });

// ❌ NEVER destructure useQuery result at call site
const { data, isLoading } = useQuery({ queryKey: ['users'] }); // BAD - recreates object

// ❌ NEVER use string keys
useQuery({ queryKey: 'users' }); // BAD - use arrays

// ❌ NEVER store server state in Zustand
const useStore = create((set) => ({ users: [] })); // BAD - use React Query
```

## Key Decisions

| Decision | Option A | Option B | Recommendation |
|----------|----------|----------|----------------|
| Query key structure | String | Array | **Array** - supports hierarchy and serialization |
| Cache timing | staleTime | gcTime | **Both** - staleTime for freshness, gcTime for memory |
| Loading state | isLoading | isPending | **isPending** (v5) - isLoading includes background refetches |
| Query definition | Inline | queryOptions | **queryOptions** - reusable for prefetch/loader/useQuery |
| Suspense | useQuery + loading | useSuspenseQuery | **useSuspenseQuery** for React 18+ Suspense |
| Optimistic updates | setQueryData only | setQueryData + invalidate | **Both** - optimistic then reconcile |
| Parallel queries | Multiple useQuery | useQueries | **useQueries** - combined loading/error state |
| Infinite queries | Manual pagination | useInfiniteQuery | **useInfiniteQuery** - built-in cursor handling |

## Anti-Patterns (FORBIDDEN)

```typescript
// ❌ FORBIDDEN: Storing server state in Zustand/Redux
const useStore = create((set) => ({
  users: [],  // Server state belongs in React Query!
  fetchUsers: async () => {
    const users = await api.getUsers();
    set({ users }); // Stale data, no background refetch
  },
}));

// ❌ FORBIDDEN: String query keys
useQuery({
  queryKey: 'todos',  // Must be an array!
  queryFn: fetchTodos,
});

// ❌ FORBIDDEN: Using deprecated cacheTime (v5)
useQuery({
  queryKey: ['todos'],
  cacheTime: 5 * 60 * 1000,  // WRONG - use gcTime in v5
});

// ❌ FORBIDDEN: Using isLoading for initial state (v5)
// isLoading = isPending && isFetching (includes background refetch)
if (isLoading) return <Skeleton />;  // WRONG - use isPending

// ❌ FORBIDDEN: Over-invalidating after mutations
useMutation({
  mutationFn: updateTodo,
  onSuccess: () => {
    queryClient.invalidateQueries(); // Invalidates EVERYTHING!
  },
});

// ❌ FORBIDDEN: Forgetting to cancel queries in optimistic updates
useMutation({
  onMutate: async (newTodo) => {
    // Missing: await queryClient.cancelQueries(...)
    const previous = queryClient.getQueryData(['todos']);
    queryClient.setQueryData(['todos'], (old) => [...old, newTodo]);
    return { previous };
  },
});

// ❌ FORBIDDEN: Not returning context from onMutate
useMutation({
  onMutate: async (newTodo) => {
    const previous = queryClient.getQueryData(['todos']);
    queryClient.setQueryData(['todos'], (old) => [...old, newTodo]);
    // Missing: return { previous }; // Required for rollback!
  },
  onError: (err, newTodo, context) => {
    queryClient.setQueryData(['todos'], context?.previous); // context is undefined!
  },
});

// ❌ FORBIDDEN: Mutating cache data directly
queryClient.setQueryData(['todos'], (old) => {
  old.push(newTodo);  // WRONG - mutates existing array
  return old;
});
// ✅ CORRECT: Return new array
queryClient.setQueryData(['todos'], (old) => [...old, newTodo]);

// ❌ FORBIDDEN: Fetching inside useEffect
useEffect(() => {
  fetch('/api/users').then(setUsers);  // Use React Query instead!
}, []);
```

## Related Skills

- `zustand-patterns` - Client state management (use alongside React Query for server state)
- `form-state-patterns` - Form state with React Hook Form (integrate mutation status)
- `msw-mocking` - Mock Service Worker for testing queries without network
- `react-server-components-framework` - RSC hydration with React Query

## Capability Details

### infinite-queries
**Keywords**: infinite, pagination, cursor, load more, scroll, pages
**Solves**: Implementing cursor-based pagination with automatic page management

### optimistic-updates
**Keywords**: optimistic, instant, rollback, onMutate, setQueryData, cancel
**Solves**: Showing immediate UI feedback before server confirmation with rollback

### prefetching
**Keywords**: prefetch, hover, preload, ensureQueryData, loader, navigation
**Solves**: Loading data before it's needed for instant navigation

### cache-invalidation
**Keywords**: invalidate, refetch, stale, fresh, gcTime, staleTime, exact
**Solves**: Keeping cache in sync with server after mutations

### suspense-integration
**Keywords**: suspense, useSuspenseQuery, streaming, fallback, boundary
**Solves**: Integrating with React Suspense for declarative loading states

### parallel-queries
**Keywords**: useQueries, parallel, concurrent, combine, batch
**Solves**: Fetching multiple independent queries with combined state

## References

- `references/cache-strategies.md` - Cache invalidation patterns
- `templates/query-hooks-template.ts` - Production query hook template
- `checklists/tanstack-checklist.md` - Implementation checklist
- `examples/tanstack-examples.md` - Real-world usage examples
