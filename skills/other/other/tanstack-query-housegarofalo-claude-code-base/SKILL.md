---
name: tanstack-query
description: Manage server state with TanStack Query (React Query). Covers data fetching, caching, mutations, optimistic updates, infinite queries, and prefetching. Use for API integration, server state management, and data synchronization in React applications.
---

# TanStack Query (React Query)

Powerful asynchronous state management for React - fetch, cache, synchronize and update server state.

## Instructions

1. **Separate server state** - Use React Query for server data, not local UI state
2. **Configure stale time** - Set appropriate stale times based on data freshness needs
3. **Use query keys** - Structure keys hierarchically for cache management
4. **Handle loading/error** - Every query needs these states handled
5. **Invalidate strategically** - Invalidate related queries after mutations

## Setup

```bash
npm install @tanstack/react-query
```

```tsx
// main.tsx
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5, // 5 minutes
      retry: 3,
      refetchOnWindowFocus: false,
    },
  },
});

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <YourApp />
      <ReactQueryDevtools initialIsOpen={false} />
    </QueryClientProvider>
  );
}
```

## Basic Queries

### Simple Query

```tsx
import { useQuery } from '@tanstack/react-query';

interface User {
  id: string;
  name: string;
  email: string;
}

async function fetchUser(userId: string): Promise<User> {
  const response = await fetch(`/api/users/${userId}`);
  if (!response.ok) throw new Error('Failed to fetch user');
  return response.json();
}

function UserProfile({ userId }: { userId: string }) {
  const {
    data: user,
    isLoading,
    isError,
    error,
    refetch,
  } = useQuery({
    queryKey: ['user', userId],
    queryFn: () => fetchUser(userId),
  });

  if (isLoading) return <Skeleton />;
  if (isError) return <Error message={error.message} onRetry={refetch} />;

  return (
    <div>
      <h1>{user.name}</h1>
      <p>{user.email}</p>
    </div>
  );
}
```

### Query with Options

```tsx
const { data } = useQuery({
  queryKey: ['todos', { status: 'active' }],
  queryFn: fetchActiveTodos,
  staleTime: 1000 * 60 * 10,     // Data fresh for 10 minutes
  gcTime: 1000 * 60 * 30,        // Cache for 30 minutes (formerly cacheTime)
  refetchInterval: 1000 * 30,    // Refetch every 30 seconds
  refetchOnMount: true,
  refetchOnWindowFocus: true,
  enabled: !!userId,             // Only run if userId exists
  placeholderData: [],           // Show while loading
  select: (data) => data.filter(todo => !todo.completed), // Transform data
});
```

## Mutations

### Basic Mutation

```tsx
import { useMutation, useQueryClient } from '@tanstack/react-query';

interface CreateTodoInput {
  title: string;
  completed: boolean;
}

function TodoForm() {
  const queryClient = useQueryClient();

  const mutation = useMutation({
    mutationFn: (newTodo: CreateTodoInput) =>
      fetch('/api/todos', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newTodo),
      }).then(res => res.json()),

    onSuccess: () => {
      // Invalidate and refetch
      queryClient.invalidateQueries({ queryKey: ['todos'] });
    },

    onError: (error) => {
      toast.error(`Failed to create: ${error.message}`);
    },
  });

  return (
    <form onSubmit={(e) => {
      e.preventDefault();
      const formData = new FormData(e.currentTarget);
      mutation.mutate({
        title: formData.get('title') as string,
        completed: false,
      });
    }}>
      <input name="title" required />
      <button type="submit" disabled={mutation.isPending}>
        {mutation.isPending ? 'Adding...' : 'Add Todo'}
      </button>
    </form>
  );
}
```

### Optimistic Updates

```tsx
const mutation = useMutation({
  mutationFn: updateTodo,

  onMutate: async (newTodo) => {
    // Cancel outgoing refetches
    await queryClient.cancelQueries({ queryKey: ['todos'] });

    // Snapshot previous value
    const previousTodos = queryClient.getQueryData(['todos']);

    // Optimistically update
    queryClient.setQueryData(['todos'], (old: Todo[]) =>
      old.map(todo =>
        todo.id === newTodo.id ? { ...todo, ...newTodo } : todo
      )
    );

    // Return snapshot for rollback
    return { previousTodos };
  },

  onError: (err, newTodo, context) => {
    // Rollback on error
    queryClient.setQueryData(['todos'], context?.previousTodos);
  },

  onSettled: () => {
    // Refetch after error or success
    queryClient.invalidateQueries({ queryKey: ['todos'] });
  },
});
```

## Infinite Queries

```tsx
import { useInfiniteQuery } from '@tanstack/react-query';

interface PostsPage {
  posts: Post[];
  nextCursor: string | null;
}

function PostsList() {
  const {
    data,
    fetchNextPage,
    hasNextPage,
    isFetchingNextPage,
  } = useInfiniteQuery({
    queryKey: ['posts'],
    queryFn: async ({ pageParam }): Promise<PostsPage> => {
      const res = await fetch(`/api/posts?cursor=${pageParam}`);
      return res.json();
    },
    initialPageParam: '',
    getNextPageParam: (lastPage) => lastPage.nextCursor,
  });

  const allPosts = data?.pages.flatMap(page => page.posts) ?? [];

  return (
    <div>
      {allPosts.map(post => (
        <PostCard key={post.id} post={post} />
      ))}

      {hasNextPage && (
        <button
          onClick={() => fetchNextPage()}
          disabled={isFetchingNextPage}
        >
          {isFetchingNextPage ? 'Loading more...' : 'Load More'}
        </button>
      )}
    </div>
  );
}
```

## Prefetching

```tsx
import { useQueryClient } from '@tanstack/react-query';

function PostsList() {
  const queryClient = useQueryClient();

  const prefetchPost = (postId: string) => {
    queryClient.prefetchQuery({
      queryKey: ['post', postId],
      queryFn: () => fetchPost(postId),
      staleTime: 1000 * 60 * 5,
    });
  };

  return (
    <ul>
      {posts.map(post => (
        <li
          key={post.id}
          onMouseEnter={() => prefetchPost(post.id)}
        >
          <Link to={`/posts/${post.id}`}>{post.title}</Link>
        </li>
      ))}
    </ul>
  );
}
```

## Query Keys

### Hierarchical Keys

```tsx
// Structure keys for easy invalidation
const queryKeys = {
  all: ['todos'] as const,
  lists: () => [...queryKeys.all, 'list'] as const,
  list: (filters: Filters) => [...queryKeys.lists(), filters] as const,
  details: () => [...queryKeys.all, 'detail'] as const,
  detail: (id: string) => [...queryKeys.details(), id] as const,
};

// Usage
useQuery({
  queryKey: queryKeys.detail(todoId),
  queryFn: () => fetchTodo(todoId),
});

// Invalidate all todos
queryClient.invalidateQueries({ queryKey: queryKeys.all });

// Invalidate only lists
queryClient.invalidateQueries({ queryKey: queryKeys.lists() });
```

## Parallel & Dependent Queries

### Parallel Queries

```tsx
function Dashboard() {
  const usersQuery = useQuery({
    queryKey: ['users'],
    queryFn: fetchUsers,
  });

  const projectsQuery = useQuery({
    queryKey: ['projects'],
    queryFn: fetchProjects,
  });

  if (usersQuery.isLoading || projectsQuery.isLoading) {
    return <Loading />;
  }

  return (
    <>
      <UsersList users={usersQuery.data} />
      <ProjectsList projects={projectsQuery.data} />
    </>
  );
}
```

### Dependent Queries

```tsx
function UserPosts({ userId }: { userId: string }) {
  // First query
  const { data: user } = useQuery({
    queryKey: ['user', userId],
    queryFn: () => fetchUser(userId),
  });

  // Dependent query - only runs when user exists
  const { data: posts } = useQuery({
    queryKey: ['posts', user?.id],
    queryFn: () => fetchUserPosts(user!.id),
    enabled: !!user?.id, // Only run when user.id exists
  });

  return <PostsList posts={posts} />;
}
```

## Error Handling

```tsx
function ErrorBoundaryWithRetry({
  error,
  resetErrorBoundary,
}: {
  error: Error;
  resetErrorBoundary: () => void;
}) {
  return (
    <div className="error-container">
      <h2>Something went wrong</h2>
      <pre>{error.message}</pre>
      <button onClick={resetErrorBoundary}>Try again</button>
    </div>
  );
}

// Global error handling
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      throwOnError: true, // Propagate to error boundary
    },
    mutations: {
      onError: (error) => {
        toast.error(`Error: ${error.message}`);
      },
    },
  },
});
```

## Best Practices

| Practice | Recommendation |
|----------|----------------|
| **Query Keys** | Use arrays, structure hierarchically |
| **Stale Time** | Set based on data update frequency |
| **Mutations** | Invalidate related queries on success |
| **Loading** | Always handle isLoading state |
| **Errors** | Always handle isError with retry option |
| **Devtools** | Use in development for debugging |

## When to Use

- Fetching data from REST/GraphQL APIs
- Server state management
- Real-time data synchronization
- Pagination and infinite scroll
- Optimistic updates
- Data prefetching

## Notes

- TanStack Query v5 renamed cacheTime to gcTime
- Works with any fetching library (fetch, axios, etc.)
- Excellent TypeScript support
- Supports React, Vue, Solid, Svelte
- 25kb gzipped bundle size
