---
name: tanstack-query
description: >-
  You are an expert in TanStack Query (formerly React Query), the
  data-fetching and server state management library. You help developers build
  React applications with automatic caching, background refetching, optimistic
  updates, pagination, infinite scroll, and offline support — replacing manual
  `useEffect` + `useState` patterns with declarative, type-safe data fetching
  hooks.
license: Apache-2.0
compatibility: ''
metadata:
  author: terminal-skills
  version: 1.0.0
  category: Frontend Development
  tags:
    - react
    - data-fetching
    - cache
    - state-management
    - async
    - typescript
---

# TanStack Query — Async State Management for React

You are an expert in TanStack Query (formerly React Query), the data-fetching and server state management library. You help developers build React applications with automatic caching, background refetching, optimistic updates, pagination, infinite scroll, and offline support — replacing manual `useEffect` + `useState` patterns with declarative, type-safe data fetching hooks.

## Core Capabilities

### Basic Queries

```tsx
import { useQuery, useMutation, useQueryClient, QueryClient, QueryClientProvider } from "@tanstack/react-query";

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000,          // 5 min before refetch
      gcTime: 10 * 60 * 1000,            // 10 min cache lifetime
      retry: 2,
      refetchOnWindowFocus: true,
    },
  },
});

// Wrap app
function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Dashboard />
    </QueryClientProvider>
  );
}

function UserList() {
  const { data, isLoading, error } = useQuery({
    queryKey: ["users"],
    queryFn: () => fetch("/api/users").then(r => r.json()),
  });

  if (isLoading) return <Skeleton />;
  if (error) return <Error message={error.message} />;
  return <ul>{data.map(u => <li key={u.id}>{u.name}</li>)}</ul>;
}
```

### Mutations with Optimistic Updates

```tsx
function useCreateTodo() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (newTodo: { title: string }) =>
      fetch("/api/todos", { method: "POST", body: JSON.stringify(newTodo) }).then(r => r.json()),

    onMutate: async (newTodo) => {
      await queryClient.cancelQueries({ queryKey: ["todos"] });
      const previous = queryClient.getQueryData(["todos"]);
      queryClient.setQueryData(["todos"], (old: Todo[]) => [
        ...old, { id: "temp", ...newTodo, completed: false },
      ]);
      return { previous };
    },
    onError: (_err, _todo, context) => {
      queryClient.setQueryData(["todos"], context?.previous);
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ["todos"] });
    },
  });
}
```

### Infinite Scroll

```tsx
function InfiniteFeed() {
  const { data, fetchNextPage, hasNextPage, isFetchingNextPage } = useInfiniteQuery({
    queryKey: ["feed"],
    queryFn: ({ pageParam }) => fetch(`/api/feed?cursor=${pageParam}`).then(r => r.json()),
    initialPageParam: "",
    getNextPageParam: (lastPage) => lastPage.nextCursor ?? undefined,
  });

  return (
    <div>
      {data?.pages.map(page => page.items.map(item => <FeedItem key={item.id} item={item} />))}
      <button onClick={() => fetchNextPage()} disabled={!hasNextPage || isFetchingNextPage}>
        {isFetchingNextPage ? "Loading..." : hasNextPage ? "Load more" : "No more"}
      </button>
    </div>
  );
}
```

## Installation

```bash
npm install @tanstack/react-query
npm install @tanstack/react-query-devtools  # Optional dev tools
```

## Best Practices

1. **Query keys** — Use arrays: `["users", userId, { status }]`; TanStack auto-invalidates related queries
2. **staleTime** — Set based on data freshness needs; 0 = always refetch, 5min for semi-static data
3. **Optimistic updates** — Update cache immediately on mutation; rollback on error for instant UX
4. **Prefetching** — Use `queryClient.prefetchQuery` on hover/focus for perceived instant navigation
5. **Infinite queries** — Use `useInfiniteQuery` for paginated lists; `getNextPageParam` handles cursor logic
6. **Dependent queries** — Use `enabled` option: `enabled: !!userId` to chain queries that depend on each other
7. **DevTools** — Add `<ReactQueryDevtools />` in development; shows all queries, cache state, and timings
8. **Select for transforms** — Use `select` option to transform server data in the query; derived data is memoized
