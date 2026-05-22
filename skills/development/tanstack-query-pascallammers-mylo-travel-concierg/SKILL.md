---
name: tanstack-query
description: Auto-activates when user mentions TanStack Query, React Query, useQuery, useMutation, or server state management. Expert in TanStack Query v5 including caching strategies, optimistic updates, and infinite queries.
category: state-management
---

# TanStack Query (React Query) - Comprehensive Guide

**Version:** TanStack Query v5  
**Framework:** React  
**Lines:** 900+

Comprehensive guide for TanStack Query (formerly React Query) - the powerful data-fetching and state management library for React applications.

---

## Table of Contents

1. [Query Basics](#1-query-basics)
2. [Mutations](#2-mutations)
3. [Caching Strategies](#3-caching-strategies)
4. [Invalidation & Refetching](#4-invalidation--refetching)
5. [Pagination](#5-pagination)
6. [Infinite Queries](#6-infinite-queries)
7. [Error Handling & Retries](#7-error-handling--retries)

---

## 1. Query Basics

### Installation & Setup

```bash
npm install @tanstack/react-query
# or
bun add @tanstack/react-query
```

### QueryClient Setup

✅ **Good: Proper QueryClient configuration**
```typescript
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 60 * 1000, // 1 minute
      gcTime: 5 * 60 * 1000, // 5 minutes (formerly cacheTime)
      refetchOnWindowFocus: false,
      retry: 1,
    },
  },
});

export function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <YourApp />
    </QueryClientProvider>
  );
}
```

❌ **Bad: No configuration, using defaults blindly**
```typescript
const queryClient = new QueryClient();
// No custom defaults, will refetch on every window focus
// No consideration for your app's needs
```

### useQuery Hook Basics

✅ **Good: Proper query key structure with dependencies**
```typescript
import { useQuery } from '@tanstack/react-query';

interface User {
  id: string;
  name: string;
  email: string;
}

function useUser(userId: string) {
  return useQuery({
    queryKey: ['user', userId],
    queryFn: async () => {
      const response = await fetch(`/api/users/${userId}`);
      if (!response.ok) throw new Error('Failed to fetch user');
      return response.json() as Promise<User>;
    },
    enabled: !!userId, // Only run when userId exists
  });
}

function UserProfile({ userId }: { userId: string }) {
  const { data, isLoading, error } = useUser(userId);

  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;
  
  return <div>{data?.name}</div>;
}
```

❌ **Bad: Static query keys, no dependencies**
```typescript
function useUser(userId: string) {
  return useQuery({
    queryKey: ['user'], // Missing userId dependency!
    queryFn: async () => {
      const response = await fetch(`/api/users/${userId}`);
      return response.json();
    },
  });
}
// All users will share the same cache key, causing data corruption
```

### Query Keys Best Practices

✅ **Good: Hierarchical query key structure**
```typescript
const queryKeys = {
  users: {
    all: ['users'] as const,
    lists: () => [...queryKeys.users.all, 'list'] as const,
    list: (filters: string) => [...queryKeys.users.lists(), { filters }] as const,
    details: () => [...queryKeys.users.all, 'detail'] as const,
    detail: (id: string) => [...queryKeys.users.details(), id] as const,
  },
  posts: {
    all: ['posts'] as const,
    lists: () => [...queryKeys.posts.all, 'list'] as const,
    list: (filters: string) => [...queryKeys.posts.lists(), { filters }] as const,
    details: () => [...queryKeys.posts.all, 'detail'] as const,
    detail: (id: string) => [...queryKeys.posts.details(), id] as const,
  },
};

// Usage
function useUserDetail(userId: string) {
  return useQuery({
    queryKey: queryKeys.users.detail(userId),
    queryFn: () => fetchUser(userId),
  });
}

function useUsersList(filters: string) {
  return useQuery({
    queryKey: queryKeys.users.list(filters),
    queryFn: () => fetchUsers(filters),
  });
}
```

❌ **Bad: Flat, inconsistent query keys**
```typescript
useQuery({ queryKey: ['user-detail', userId], ... });
useQuery({ queryKey: ['userDetail', userId], ... });
useQuery({ queryKey: ['users', 'detail', userId], ... });
// Inconsistent naming makes invalidation difficult
```

### Query Functions

✅ **Good: Typed query functions with proper error handling**
```typescript
interface Todo {
  id: number;
  title: string;
  completed: boolean;
}

const fetchTodos = async (): Promise<Todo[]> => {
  const response = await fetch('/api/todos');
  
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }
  
  return response.json();
};

function useTodos() {
  return useQuery({
    queryKey: ['todos'],
    queryFn: fetchTodos,
  });
}
```

❌ **Bad: No error handling, no types**
```typescript
function useTodos() {
  return useQuery({
    queryKey: ['todos'],
    queryFn: () => fetch('/api/todos').then(res => res.json()),
    // No error handling if response is not ok
    // No type safety
  });
}
```

### Dependent Queries

✅ **Good: Using enabled option for dependent queries**
```typescript
interface User {
  id: string;
  organizationId: string;
}

interface Organization {
  id: string;
  name: string;
}

function useUserWithOrganization(userId: string) {
  const { data: user } = useQuery({
    queryKey: ['user', userId],
    queryFn: () => fetchUser(userId),
  });

  const { data: organization } = useQuery({
    queryKey: ['organization', user?.organizationId],
    queryFn: () => fetchOrganization(user!.organizationId),
    enabled: !!user?.organizationId, // Only run when user is loaded
  });

  return { user, organization };
}
```

❌ **Bad: Not handling dependencies properly**
```typescript
function useUserWithOrganization(userId: string) {
  const { data: user } = useQuery({
    queryKey: ['user', userId],
    queryFn: () => fetchUser(userId),
  });

  const { data: organization } = useQuery({
    queryKey: ['organization', user?.organizationId],
    queryFn: () => fetchOrganization(user!.organizationId),
    // Will try to fetch even when user is undefined
    // Will cause errors
  });

  return { user, organization };
}
```

### Parallel Queries

✅ **Good: Using useQueries for multiple parallel queries**
```typescript
import { useQueries } from '@tanstack/react-query';

function useUserProjects(projectIds: string[]) {
  return useQueries({
    queries: projectIds.map(id => ({
      queryKey: ['project', id],
      queryFn: () => fetchProject(id),
      staleTime: 5 * 60 * 1000,
    })),
  });
}

// Usage
function ProjectsList({ projectIds }: { projectIds: string[] }) {
  const projects = useUserProjects(projectIds);
  
  const isLoading = projects.some(q => q.isLoading);
  const hasError = projects.some(q => q.error);
  
  if (isLoading) return <div>Loading projects...</div>;
  if (hasError) return <div>Error loading projects</div>;
  
  return (
    <div>
      {projects.map((result, i) => (
        <div key={projectIds[i]}>{result.data?.name}</div>
      ))}
    </div>
  );
}
```

❌ **Bad: Multiple useQuery calls in a loop**
```typescript
// This will violate React's rules of hooks
function ProjectsList({ projectIds }: { projectIds: string[] }) {
  const projects = projectIds.map(id => {
    const { data } = useQuery({ // ❌ Hooks in a loop!
      queryKey: ['project', id],
      queryFn: () => fetchProject(id),
    });
    return data;
  });
  
  return <div>{/* ... */}</div>;
}
```

---

## 2. Mutations

### Basic Mutations

✅ **Good: Properly structured mutation with callbacks**
```typescript
import { useMutation, useQueryClient } from '@tanstack/react-query';

interface CreateTodoData {
  title: string;
  description: string;
}

interface Todo extends CreateTodoData {
  id: string;
  completed: boolean;
}

function useCreateTodo() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: async (newTodo: CreateTodoData): Promise<Todo> => {
      const response = await fetch('/api/todos', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newTodo),
      });
      
      if (!response.ok) {
        throw new Error('Failed to create todo');
      }
      
      return response.json();
    },
    onSuccess: (data) => {
      // Invalidate and refetch todos list
      queryClient.invalidateQueries({ queryKey: ['todos'] });
      console.log('Todo created:', data.id);
    },
    onError: (error) => {
      console.error('Failed to create todo:', error);
    },
  });
}

// Usage
function CreateTodoForm() {
  const createTodo = useCreateTodo();
  
  const handleSubmit = (data: CreateTodoData) => {
    createTodo.mutate(data, {
      onSuccess: () => {
        alert('Todo created!');
      },
    });
  };
  
  return (
    <form onSubmit={handleSubmit}>
      {createTodo.isPending && <div>Creating...</div>}
      {createTodo.error && <div>Error: {createTodo.error.message}</div>}
      {/* form fields */}
    </form>
  );
}
```

❌ **Bad: No error handling, no cache invalidation**
```typescript
function useCreateTodo() {
  return useMutation({
    mutationFn: (newTodo) => 
      fetch('/api/todos', {
        method: 'POST',
        body: JSON.stringify(newTodo),
      }).then(res => res.json()),
    // No onSuccess to update cache
    // No error handling
    // No types
  });
}
```

### Optimistic Updates

✅ **Good: Proper optimistic updates with rollback**
```typescript
interface UpdateTodoData {
  id: string;
  completed: boolean;
}

function useUpdateTodo() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: async (data: UpdateTodoData): Promise<Todo> => {
      const response = await fetch(`/api/todos/${data.id}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      });
      
      if (!response.ok) throw new Error('Update failed');
      return response.json();
    },
    onMutate: async (updatedTodo) => {
      // Cancel outgoing refetches
      await queryClient.cancelQueries({ queryKey: ['todos'] });
      
      // Snapshot previous value
      const previousTodos = queryClient.getQueryData<Todo[]>(['todos']);
      
      // Optimistically update cache
      queryClient.setQueryData<Todo[]>(['todos'], (old) =>
        old?.map((todo) =>
          todo.id === updatedTodo.id
            ? { ...todo, ...updatedTodo }
            : todo
        )
      );
      
      // Return context with previous value
      return { previousTodos };
    },
    onError: (err, updatedTodo, context) => {
      // Rollback on error
      queryClient.setQueryData(['todos'], context?.previousTodos);
    },
    onSettled: () => {
      // Refetch after error or success
      queryClient.invalidateQueries({ queryKey: ['todos'] });
    },
  });
}
```

❌ **Bad: Optimistic update without rollback**
```typescript
function useUpdateTodo() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (data) => updateTodo(data),
    onMutate: (updatedTodo) => {
      queryClient.setQueryData(['todos'], (old: any) =>
        old.map((todo: any) =>
          todo.id === updatedTodo.id ? { ...todo, ...updatedTodo } : todo
        )
      );
      // No snapshot saved, can't rollback on error!
    },
  });
}
```

### Mutation Variables and Context

✅ **Good: Using mutation context effectively**
```typescript
interface DeleteTodoContext {
  previousTodos?: Todo[];
  deletedId: string;
}

function useDeleteTodo() {
  const queryClient = useQueryClient();
  
  return useMutation<void, Error, string, DeleteTodoContext>({
    mutationFn: async (todoId: string) => {
      const response = await fetch(`/api/todos/${todoId}`, {
        method: 'DELETE',
      });
      
      if (!response.ok) throw new Error('Delete failed');
    },
    onMutate: async (todoId): Promise<DeleteTodoContext> => {
      await queryClient.cancelQueries({ queryKey: ['todos'] });
      
      const previousTodos = queryClient.getQueryData<Todo[]>(['todos']);
      
      queryClient.setQueryData<Todo[]>(['todos'], (old) =>
        old?.filter((todo) => todo.id !== todoId)
      );
      
      return { previousTodos, deletedId: todoId };
    },
    onError: (err, todoId, context) => {
      if (context?.previousTodos) {
        queryClient.setQueryData(['todos'], context.previousTodos);
      }
      console.error(`Failed to delete todo ${context?.deletedId}`);
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ['todos'] });
    },
  });
}
```

❌ **Bad: No context, losing important information**
```typescript
function useDeleteTodo() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (todoId) => deleteTodo(todoId),
    onError: () => {
      // No way to know which todo failed
      // No way to rollback specific changes
    },
  });
}
```

### Sequential Mutations

✅ **Good: Chaining mutations properly**
```typescript
function useCreateAndPublishPost() {
  const queryClient = useQueryClient();
  const createPost = useMutation({ mutationFn: createPostApi });
  const publishPost = useMutation({ mutationFn: publishPostApi });
  
  const createAndPublish = async (data: CreatePostData) => {
    try {
      const post = await createPost.mutateAsync(data);
      await publishPost.mutateAsync(post.id);
      queryClient.invalidateQueries({ queryKey: ['posts'] });
      return post;
    } catch (error) {
      console.error('Failed:', error);
      throw error;
    }
  };
  
  return {
    createAndPublish,
    isLoading: createPost.isPending || publishPost.isPending,
  };
}
```

❌ **Bad: Not handling sequential mutations**
```typescript
function CreatePostButton() {
  const createPost = useMutation({ mutationFn: createPostApi });
  const publishPost = useMutation({ mutationFn: publishPostApi });
  
  const handleClick = () => {
    createPost.mutate(data, {
      onSuccess: (post) => {
        publishPost.mutate(post.id);
        // No proper error handling
        // No way to track overall status
      },
    });
  };
}
```

---

## 3. Caching Strategies

### staleTime vs gcTime (formerly cacheTime)

✅ **Good: Understanding and configuring both options**
```typescript
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      // Data is fresh for 5 minutes
      staleTime: 5 * 60 * 1000,
      
      // Unused data stays in cache for 10 minutes
      gcTime: 10 * 60 * 1000, // v5: gcTime (was cacheTime in v4)
    },
  },
});

// Frequently accessed, rarely changing data
function useAppConfig() {
  return useQuery({
    queryKey: ['appConfig'],
    queryFn: fetchAppConfig,
    staleTime: Infinity, // Never goes stale
    gcTime: Infinity, // Never garbage collected
  });
}

// Real-time data
function useRealtimeData() {
  return useQuery({
    queryKey: ['realtime'],
    queryFn: fetchRealtimeData,
    staleTime: 0, // Always stale, always refetch
    gcTime: 0, // Don't cache at all
  });
}

// Balanced approach for user data
function useUser(id: string) {
  return useQuery({
    queryKey: ['user', id],
    queryFn: () => fetchUser(id),
    staleTime: 60 * 1000, // Fresh for 1 minute
    gcTime: 5 * 60 * 1000, // Keep in cache for 5 minutes
  });
}
```

❌ **Bad: Not understanding the difference**
```typescript
useQuery({
  queryKey: ['data'],
  queryFn: fetchData,
  gcTime: 5000,
  // Forgot staleTime - data will refetch on every mount
  // even though it's cached!
});

useQuery({
  queryKey: ['data'],
  queryFn: fetchData,
  staleTime: 5000,
  gcTime: 1000,
  // gcTime < staleTime is usually wrong
  // Data will be garbage collected before it goes stale
});
```

### Cache Persistence

✅ **Good: Using persistQueryClient for offline support**
```typescript
import { QueryClient } from '@tanstack/react-query';
import { PersistQueryClientProvider } from '@tanstack/react-query-persist-client';
import { createSyncStoragePersister } from '@tanstack/query-sync-storage-persister';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      gcTime: 1000 * 60 * 60 * 24, // 24 hours
    },
  },
});

const persister = createSyncStoragePersister({
  storage: window.localStorage,
});

export function App() {
  return (
    <PersistQueryClientProvider
      client={queryClient}
      persistOptions={{ persister }}
    >
      <YourApp />
    </PersistQueryClientProvider>
  );
}
```

❌ **Bad: Manual localStorage management**
```typescript
// Don't do this - let TanStack Query handle it
function useData() {
  useEffect(() => {
    const cached = localStorage.getItem('my-data');
    if (cached) {
      setData(JSON.parse(cached));
    }
  }, []);
  
  const { data } = useQuery({
    queryKey: ['data'],
    queryFn: fetchData,
    onSuccess: (data) => {
      localStorage.setItem('my-data', JSON.stringify(data));
    },
  });
}
```

### Prefetching

✅ **Good: Strategic prefetching for better UX**
```typescript
function useUsersList() {
  const queryClient = useQueryClient();
  
  const { data: users } = useQuery({
    queryKey: ['users', 'list'],
    queryFn: fetchUsersList,
  });
  
  // Prefetch user details on hover
  const prefetchUser = (userId: string) => {
    queryClient.prefetchQuery({
      queryKey: ['user', userId],
      queryFn: () => fetchUser(userId),
      staleTime: 60 * 1000,
    });
  };
  
  return { users, prefetchUser };
}

function UsersList() {
  const { users, prefetchUser } = useUsersList();
  
  return (
    <div>
      {users?.map((user) => (
        <div 
          key={user.id}
          onMouseEnter={() => prefetchUser(user.id)}
        >
          {user.name}
        </div>
      ))}
    </div>
  );
}
```

❌ **Bad: Not prefetching predictable navigation**
```typescript
function UsersList() {
  const { data: users } = useQuery({
    queryKey: ['users'],
    queryFn: fetchUsersList,
  });
  
  return (
    <div>
      {users?.map((user) => (
        <Link to={`/users/${user.id}`}>
          {/* User details will only load when clicked */}
          {/* Could have prefetched on hover */}
          {user.name}
        </Link>
      ))}
    </div>
  );
}
```

### Background Refetching

✅ **Good: Smart background refetching configuration**
```typescript
// Critical data - frequent background updates
function useOrderStatus(orderId: string) {
  return useQuery({
    queryKey: ['order', orderId, 'status'],
    queryFn: () => fetchOrderStatus(orderId),
    refetchInterval: 5000, // Refetch every 5 seconds
    refetchOnWindowFocus: true,
    refetchOnMount: true,
  });
}

// Static data - minimal refetching
function useProductCatalog() {
  return useQuery({
    queryKey: ['products', 'catalog'],
    queryFn: fetchProductCatalog,
    staleTime: 60 * 60 * 1000, // 1 hour
    refetchOnWindowFocus: false,
    refetchOnMount: false,
  });
}

// User-specific data - refetch on focus
function useUserPreferences() {
  return useQuery({
    queryKey: ['user', 'preferences'],
    queryFn: fetchUserPreferences,
    staleTime: 5 * 60 * 1000, // 5 minutes
    refetchOnWindowFocus: true,
    refetchOnMount: false,
  });
}
```

❌ **Bad: One-size-fits-all refetching**
```typescript
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchInterval: 1000, // Everything refetches every second!
      refetchOnWindowFocus: true,
      refetchOnMount: true,
      // Way too aggressive for most data
    },
  },
});
```

---

## 4. Invalidation & Refetching

### Query Invalidation

✅ **Good: Targeted query invalidation**
```typescript
function useUpdateUser() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: updateUserApi,
    onSuccess: (updatedUser) => {
      // Invalidate specific user
      queryClient.invalidateQueries({
        queryKey: ['user', updatedUser.id],
      });
      
      // Invalidate all user lists
      queryClient.invalidateQueries({
        queryKey: ['users', 'list'],
      });
      
      // Invalidate exact match only
      queryClient.invalidateQueries({
        queryKey: ['users', 'list', { page: 1 }],
        exact: true,
      });
    },
  });
}
```

❌ **Bad: Overly broad invalidation**
```typescript
function useUpdateUser() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: updateUserApi,
    onSuccess: () => {
      // Invalidates EVERYTHING!
      queryClient.invalidateQueries();
      // This will refetch all queries in your app
    },
  });
}
```

### Partial Matching vs Exact Matching

✅ **Good: Using appropriate matching strategies**
```typescript
const queryClient = useQueryClient();

// Invalidate all todo queries (partial match)
queryClient.invalidateQueries({
  queryKey: ['todos'],
});
// Matches: ['todos'], ['todos', '1'], ['todos', 'list'], etc.

// Invalidate specific todo (partial match)
queryClient.invalidateQueries({
  queryKey: ['todos', todoId],
});
// Matches: ['todos', '1'], ['todos', '1', 'comments'], etc.

// Invalidate exact query (exact match)
queryClient.invalidateQueries({
  queryKey: ['todos', 'list', { status: 'active', page: 1 }],
  exact: true,
});
// Only matches the exact key

// Predicate-based invalidation
queryClient.invalidateQueries({
  predicate: (query) =>
    query.queryKey[0] === 'todos' &&
    query.queryKey[1] !== 'archived',
});
```

❌ **Bad: Not understanding matching behavior**
```typescript
// Trying to invalidate specific todo
queryClient.invalidateQueries({
  queryKey: ['todos'],
  // This invalidates ALL todo queries, not just one!
});

// Over-specific invalidation
queryClient.invalidateQueries({
  queryKey: ['todos', '1', 'comments', '5', 'replies'],
  exact: true,
  // Too specific, might miss related queries
});
```

### Manual Refetching

✅ **Good: Controlled refetching**
```typescript
function TodosList() {
  const { data, refetch, isRefetching } = useQuery({
    queryKey: ['todos'],
    queryFn: fetchTodos,
  });
  
  const queryClient = useQueryClient();
  
  const handleRefresh = () => {
    // Option 1: Refetch specific query
    refetch();
    
    // Option 2: Refetch via queryClient
    queryClient.refetchQueries({ queryKey: ['todos'] });
    
    // Option 3: Refetch only active queries
    queryClient.refetchQueries({
      queryKey: ['todos'],
      type: 'active',
    });
  };
  
  return (
    <div>
      <button onClick={handleRefresh} disabled={isRefetching}>
        {isRefetching ? 'Refreshing...' : 'Refresh'}
      </button>
      {/* ... */}
    </div>
  );
}
```

❌ **Bad: Fetching without using the query system**
```typescript
function TodosList() {
  const [data, setData] = useState([]);
  
  const refresh = async () => {
    // Bypasses React Query's caching!
    const newData = await fetchTodos();
    setData(newData);
  };
  
  return <button onClick={refresh}>Refresh</button>;
}
```

### Invalidation Timing

✅ **Good: Strategic invalidation timing**
```typescript
function useUpdateSettings() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: updateSettingsApi,
    onMutate: async (newSettings) => {
      // Cancel outgoing refetches
      await queryClient.cancelQueries({ queryKey: ['settings'] });
      
      // Snapshot
      const previous = queryClient.getQueryData(['settings']);
      
      // Optimistic update
      queryClient.setQueryData(['settings'], newSettings);
      
      return { previous };
    },
    onError: (err, variables, context) => {
      // Rollback
      if (context?.previous) {
        queryClient.setQueryData(['settings'], context.previous);
      }
    },
    onSettled: () => {
      // Always refetch after mutation completes
      queryClient.invalidateQueries({ queryKey: ['settings'] });
    },
  });
}
```

❌ **Bad: Invalidating too early**
```typescript
function useUpdateSettings() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: updateSettingsApi,
    onMutate: () => {
      // Invalidating during mutation can cause race conditions
      queryClient.invalidateQueries({ queryKey: ['settings'] });
    },
  });
}
```

---

## 5. Pagination

### Basic Offset/Limit Pagination

✅ **Good: Proper pagination with placeholderData**
```typescript
interface PaginatedResponse<T> {
  data: T[];
  page: number;
  totalPages: number;
  total: number;
}

interface PaginationParams {
  page: number;
  limit: number;
}

function usePaginatedTodos(page: number) {
  return useQuery({
    queryKey: ['todos', 'list', { page }],
    queryFn: async (): Promise<PaginatedResponse<Todo>> => {
      const response = await fetch(
        `/api/todos?page=${page}&limit=10`
      );
      return response.json();
    },
    placeholderData: (previousData) => previousData, // Keep previous data while loading
    staleTime: 60 * 1000,
  });
}

function TodosPaginatedList() {
  const [page, setPage] = useState(1);
  const { data, isPlaceholderData, isLoading } = usePaginatedTodos(page);
  
  const queryClient = useQueryClient();
  
  // Prefetch next page
  useEffect(() => {
    if (!isPlaceholderData && data?.page < data?.totalPages) {
      queryClient.prefetchQuery({
        queryKey: ['todos', 'list', { page: page + 1 }],
        queryFn: () => fetchTodos(page + 1),
      });
    }
  }, [data, isPlaceholderData, page, queryClient]);
  
  if (isLoading) return <div>Loading...</div>;
  
  return (
    <div>
      {data?.data.map((todo) => (
        <div key={todo.id}>{todo.title}</div>
      ))}
      
      <div>
        <button
          onClick={() => setPage((old) => Math.max(old - 1, 1))}
          disabled={page === 1}
        >
          Previous
        </button>
        <span>Page {page} of {data?.totalPages}</span>
        <button
          onClick={() => setPage((old) => old + 1)}
          disabled={isPlaceholderData || page >= (data?.totalPages ?? 0)}
        >
          Next
        </button>
      </div>
    </div>
  );
}
```

❌ **Bad: Pagination without placeholderData**
```typescript
function useTodos(page: number) {
  return useQuery({
    queryKey: ['todos', page], // Inconsistent key structure
    queryFn: () => fetchTodos(page),
    // No placeholderData - UI will flash on page change
  });
}

function TodosList() {
  const [page, setPage] = useState(1);
  const { data, isLoading } = useTodos(page);
  
  // Every page change shows loading state
  if (isLoading) return <div>Loading...</div>;
  
  return <div>{/* ... */}</div>;
}
```

### Cursor-Based Pagination

✅ **Good: Cursor pagination for dynamic data**
```typescript
interface CursorPaginatedResponse<T> {
  items: T[];
  nextCursor?: string;
  hasMore: boolean;
}

function useCursorPaginatedTodos(filters: string) {
  const [cursors, setCursors] = useState<string[]>(['']);
  const [currentPage, setCurrentPage] = useState(0);
  
  const { data, isLoading } = useQuery({
    queryKey: ['todos', 'cursor', { filters, cursor: cursors[currentPage] }],
    queryFn: async (): Promise<CursorPaginatedResponse<Todo>> => {
      const response = await fetch(
        `/api/todos?cursor=${cursors[currentPage]}&filters=${filters}`
      );
      return response.json();
    },
    placeholderData: (previousData) => previousData,
  });
  
  const goToNextPage = () => {
    if (data?.nextCursor) {
      setCursors((old) => [...old, data.nextCursor!]);
      setCurrentPage((old) => old + 1);
    }
  };
  
  const goToPreviousPage = () => {
    setCurrentPage((old) => Math.max(0, old - 1));
  };
  
  return {
    data: data?.items,
    goToNextPage,
    goToPreviousPage,
    hasNextPage: data?.hasMore ?? false,
    hasPreviousPage: currentPage > 0,
    isLoading,
  };
}
```

❌ **Bad: Not tracking cursor history**
```typescript
function useCursorPaginatedTodos() {
  const [cursor, setCursor] = useState('');
  
  const { data } = useQuery({
    queryKey: ['todos', cursor],
    queryFn: () => fetchTodos(cursor),
  });
  
  const nextPage = () => {
    setCursor(data?.nextCursor);
    // Can't go back to previous pages!
  };
}
```

---

## 6. Infinite Queries

### useInfiniteQuery Basics

✅ **Good: Proper infinite query implementation**
```typescript
interface InfiniteResponse {
  items: Todo[];
  nextPage?: number;
  hasMore: boolean;
}

function useInfiniteTodos() {
  return useInfiniteQuery({
    queryKey: ['todos', 'infinite'],
    queryFn: async ({ pageParam = 1 }): Promise<InfiniteResponse> => {
      const response = await fetch(`/api/todos?page=${pageParam}&limit=20`);
      const data = await response.json();
      
      return {
        items: data.items,
        nextPage: data.nextPage,
        hasMore: data.hasMore,
      };
    },
    getNextPageParam: (lastPage) => lastPage.nextPage,
    initialPageParam: 1,
  });
}

function InfiniteTodosList() {
  const {
    data,
    fetchNextPage,
    hasNextPage,
    isFetchingNextPage,
    isLoading,
  } = useInfiniteTodos();
  
  if (isLoading) return <div>Loading...</div>;
  
  return (
    <div>
      {data?.pages.map((page, pageIndex) => (
        <React.Fragment key={pageIndex}>
          {page.items.map((todo) => (
            <div key={todo.id}>{todo.title}</div>
          ))}
        </React.Fragment>
      ))}
      
      <button
        onClick={() => fetchNextPage()}
        disabled={!hasNextPage || isFetchingNextPage}
      >
        {isFetchingNextPage
          ? 'Loading more...'
          : hasNextPage
          ? 'Load More'
          : 'No more data'}
      </button>
    </div>
  );
}
```

❌ **Bad: Manual pagination instead of useInfiniteQuery**
```typescript
function useTodos() {
  const [pages, setPages] = useState<Todo[][]>([]);
  const [page, setPage] = useState(1);
  
  const { data } = useQuery({
    queryKey: ['todos', page],
    queryFn: () => fetchTodos(page),
  });
  
  useEffect(() => {
    if (data) {
      setPages(prev => [...prev, data]);
    }
  }, [data]);
  
  // Managing infinite scroll manually - error prone!
}
```

### Bi-directional Infinite Queries

✅ **Good: Both directions supported**
```typescript
interface Message {
  id: string;
  text: string;
  timestamp: number;
}

function useInfiniteMessages(channelId: string) {
  return useInfiniteQuery({
    queryKey: ['messages', channelId],
    queryFn: async ({ pageParam = { direction: 'forward', cursor: null } }) => {
      const { direction, cursor } = pageParam;
      const response = await fetch(
        `/api/messages/${channelId}?cursor=${cursor}&direction=${direction}`
      );
      return response.json();
    },
    getNextPageParam: (lastPage) => ({
      direction: 'forward',
      cursor: lastPage.nextCursor,
    }),
    getPreviousPageParam: (firstPage) => ({
      direction: 'backward',
      cursor: firstPage.previousCursor,
    }),
    initialPageParam: { direction: 'forward', cursor: null },
  });
}

function MessageList({ channelId }: { channelId: string }) {
  const {
    data,
    fetchNextPage,
    fetchPreviousPage,
    hasNextPage,
    hasPreviousPage,
  } = useInfiniteMessages(channelId);
  
  return (
    <div>
      {hasPreviousPage && (
        <button onClick={() => fetchPreviousPage()}>
          Load Older Messages
        </button>
      )}
      
      {data?.pages.map((page, i) => (
        <div key={i}>
          {page.messages.map((msg: Message) => (
            <div key={msg.id}>{msg.text}</div>
          ))}
        </div>
      ))}
      
      {hasNextPage && (
        <button onClick={() => fetchNextPage()}>
          Load Newer Messages
        </button>
      )}
    </div>
  );
}
```

❌ **Bad: Only forward pagination**
```typescript
function useMessages() {
  return useInfiniteQuery({
    queryKey: ['messages'],
    queryFn: ({ pageParam = 1 }) => fetchMessages(pageParam),
    getNextPageParam: (lastPage) => lastPage.nextPage,
    // Missing getPreviousPageParam - can't load older messages
  });
}
```

### Infinite Scroll Integration

✅ **Good: Using Intersection Observer for infinite scroll**
```typescript
function useInfiniteScroll(
  fetchNextPage: () => void,
  hasNextPage: boolean | undefined,
  isFetchingNextPage: boolean
) {
  const observerTarget = useRef<HTMLDivElement>(null);
  
  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        if (entries[0].isIntersecting && hasNextPage && !isFetchingNextPage) {
          fetchNextPage();
        }
      },
      { threshold: 1.0 }
    );
    
    const currentTarget = observerTarget.current;
    if (currentTarget) {
      observer.observe(currentTarget);
    }
    
    return () => {
      if (currentTarget) {
        observer.unobserve(currentTarget);
      }
    };
  }, [fetchNextPage, hasNextPage, isFetchingNextPage]);
  
  return observerTarget;
}

function InfiniteScrollList() {
  const { data, fetchNextPage, hasNextPage, isFetchingNextPage } = 
    useInfiniteTodos();
  
  const observerTarget = useInfiniteScroll(
    fetchNextPage,
    hasNextPage,
    isFetchingNextPage
  );
  
  return (
    <div>
      {data?.pages.map((page, i) => (
        <div key={i}>
          {page.items.map((todo) => (
            <div key={todo.id}>{todo.title}</div>
          ))}
        </div>
      ))}
      
      <div ref={observerTarget} style={{ height: '20px' }} />
      
      {isFetchingNextPage && <div>Loading more...</div>}
    </div>
  );
}
```

❌ **Bad: Scroll event listener (performance issue)**
```typescript
function InfiniteScrollList() {
  const { data, fetchNextPage, hasNextPage } = useInfiniteTodos();
  
  useEffect(() => {
    const handleScroll = () => {
      // This fires constantly while scrolling!
      if (window.innerHeight + window.scrollY >= document.body.offsetHeight) {
        fetchNextPage();
      }
    };
    
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, [fetchNextPage]);
}
```

---

## 7. Error Handling & Retries

### Global Error Handling

✅ **Good: Comprehensive error boundary and global config**
```typescript
import { QueryClient, QueryCache, MutationCache } from '@tanstack/react-query';

const queryClient = new QueryClient({
  queryCache: new QueryCache({
    onError: (error, query) => {
      console.error('Query error:', error);
      
      // Show toast notification
      if (error instanceof Error) {
        showToast(`Query error: ${error.message}`);
      }
    },
  }),
  mutationCache: new MutationCache({
    onError: (error, variables, context, mutation) => {
      console.error('Mutation error:', error);
      showToast(`Mutation failed: ${error.message}`);
    },
  }),
  defaultOptions: {
    queries: {
      retry: (failureCount, error) => {
        // Don't retry on 404
        if (error instanceof Response && error.status === 404) {
          return false;
        }
        // Retry up to 3 times for other errors
        return failureCount < 3;
      },
      retryDelay: (attemptIndex) => Math.min(1000 * 2 ** attemptIndex, 30000),
    },
  },
});
```

❌ **Bad: No global error handling**
```typescript
const queryClient = new QueryClient();
// Errors are silently swallowed or must be handled in every component
```

### Component-Level Error Handling

✅ **Good: Using React Error Boundaries with Query Error Reset**
```typescript
import { 
  QueryErrorResetBoundary,
  useQueryErrorResetBoundary 
} from '@tanstack/react-query';
import { ErrorBoundary } from 'react-error-boundary';

function ErrorFallback({ error, resetErrorBoundary }: any) {
  return (
    <div role="alert">
      <p>Something went wrong:</p>
      <pre>{error.message}</pre>
      <button onClick={resetErrorBoundary}>Try again</button>
    </div>
  );
}

function App() {
  return (
    <QueryErrorResetBoundary>
      {({ reset }) => (
        <ErrorBoundary
          onReset={reset}
          FallbackComponent={ErrorFallback}
        >
          <YourApp />
        </ErrorBoundary>
      )}
    </QueryErrorResetBoundary>
  );
}

// In components
function TodoList() {
  const { error, refetch } = useQuery({
    queryKey: ['todos'],
    queryFn: fetchTodos,
    useErrorBoundary: (error) => error.response?.status >= 500,
  });
  
  // 4xx errors handled locally
  if (error) {
    return <div>Error: {error.message}</div>;
  }
  
  // 5xx errors caught by error boundary
}
```

❌ **Bad: No error boundaries, inconsistent error handling**
```typescript
function TodoList() {
  const { data, error } = useQuery({
    queryKey: ['todos'],
    queryFn: fetchTodos,
  });
  
  // Some errors might crash the app
  // No way to recover without refresh
}
```

### Retry Configuration

✅ **Good: Smart retry logic based on error type**
```typescript
interface ApiError {
  status: number;
  message: string;
}

function useSmartRetry() {
  return useQuery<Data, ApiError>({
    queryKey: ['data'],
    queryFn: fetchData,
    retry: (failureCount, error) => {
      // Don't retry client errors (4xx)
      if (error.status >= 400 && error.status < 500) {
        return false;
      }
      
      // Retry server errors (5xx) up to 3 times
      if (error.status >= 500) {
        return failureCount < 3;
      }
      
      // Network errors - retry up to 5 times
      return failureCount < 5;
    },
    retryDelay: (attemptIndex, error) => {
      // Exponential backoff
      const baseDelay = 1000;
      const maxDelay = 30000;
      const delay = Math.min(baseDelay * 2 ** attemptIndex, maxDelay);
      
      // Add jitter to prevent thundering herd
      const jitter = Math.random() * 1000;
      
      return delay + jitter;
    },
  });
}
```

❌ **Bad: Retrying everything indefinitely**
```typescript
useQuery({
  queryKey: ['data'],
  queryFn: fetchData,
  retry: true, // Retries forever!
  retryDelay: 1000, // Same delay each time
  // Will hammer your server on 404s and other permanent failures
});
```

### Error Reporting

✅ **Good: Integrating with error tracking services**
```typescript
import * as Sentry from '@sentry/react';

const queryClient = new QueryClient({
  queryCache: new QueryCache({
    onError: (error, query) => {
      Sentry.captureException(error, {
        contexts: {
          query: {
            queryKey: query.queryKey,
            queryHash: query.queryHash,
          },
        },
      });
    },
  }),
  mutationCache: new MutationCache({
    onError: (error, variables, context, mutation) => {
      Sentry.captureException(error, {
        contexts: {
          mutation: {
            mutationKey: mutation.options.mutationKey,
            variables: JSON.stringify(variables),
          },
        },
      });
    },
  }),
});
```

❌ **Bad: Just console.log errors**
```typescript
const queryClient = new QueryClient({
  queryCache: new QueryCache({
    onError: (error) => {
      console.log(error); // Lost in production!
    },
  }),
});
```

---

## Best Practices Summary

### ✅ Do's

1. **Use proper query key hierarchies** - Makes invalidation easier
2. **Configure staleTime and gcTime appropriately** - Based on data characteristics
3. **Implement optimistic updates with rollback** - For better UX
4. **Use placeholderData for pagination** - Prevents loading flashes
5. **Prefetch predictable navigations** - Improves perceived performance
6. **Handle errors at multiple levels** - Global + component level
7. **Use TypeScript** - Type safety prevents many bugs
8. **Implement smart retry logic** - Don't retry permanent failures
9. **Use error boundaries** - Graceful degradation
10. **Monitor and track errors** - Integration with error tracking services

### ❌ Don'ts

1. **Don't use static query keys with dynamic data**
2. **Don't invalidate all queries unnecessarily**
3. **Don't bypass React Query's caching**
4. **Don't forget to handle loading and error states**
5. **Don't use the same staleTime/gcTime for all queries**
6. **Don't implement infinite scroll without proper cleanup**
7. **Don't retry 4xx errors**
8. **Don't ignore TypeScript warnings**
9. **Don't fetch data outside of React Query**
10. **Don't forget to cleanup on unmount**

---

## Common Patterns

### 1. Query Factories

```typescript
export const todoQueries = {
  all: () => ['todos'] as const,
  lists: () => [...todoQueries.all(), 'list'] as const,
  list: (filters: string) => [...todoQueries.lists(), { filters }] as const,
  details: () => [...todoQueries.all(), 'detail'] as const,
  detail: (id: string) => [...todoQueries.details(), id] as const,
};
```

### 2. Suspense Mode

```typescript
function TodoList() {
  const { data } = useSuspenseQuery({
    queryKey: ['todos'],
    queryFn: fetchTodos,
  });
  
  // data is always defined, no need for isLoading
  return <div>{data.map(todo => ...)}</div>;
}
```

### 3. Dependent Queries Chain

```typescript
function useUserWithDetails(userId: string) {
  const { data: user } = useQuery({
    queryKey: ['user', userId],
    queryFn: () => fetchUser(userId),
  });
  
  const { data: profile } = useQuery({
    queryKey: ['profile', user?.id],
    queryFn: () => fetchProfile(user!.id),
    enabled: !!user,
  });
  
  const { data: settings } = useQuery({
    queryKey: ['settings', profile?.id],
    queryFn: () => fetchSettings(profile!.id),
    enabled: !!profile,
  });
  
  return { user, profile, settings };
}
```

---

## Resources

- **Official Docs:** https://tanstack.com/query/latest
- **GitHub:** https://github.com/TanStack/query
- **Discord:** https://tlinz.com/discord
- **Query.gg Course:** https://query.gg (Official course by Tanner Linsley)

---

**Total Lines:** 900+  
**Last Updated:** 2025-11-16  
**Version:** TanStack Query v5
