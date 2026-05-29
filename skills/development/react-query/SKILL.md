---
name: react-query
description: Guidelines for using React Query for data fetching, caching, and server state synchronization in React applications
---

# React Query Best Practices

You are an expert in React Query, TypeScript, and React development. React Query (now TanStack Query) simplifies data fetching logic with built-in caching, background updates, and stale data management.

## Core Principles

- Use React Query for all data fetching and caching
- Leverage React Query's built-in state management instead of `useState` for server data
- Use React Context and `useReducer` for managing client-side global state
- Avoid excessive API calls through proper caching strategies
- Always handle loading states and errors properly

## Project Structure

```
src/
  components/
    [Feature]/
      index.tsx
      queries.ts           # Feature-specific query hooks
      mutations.ts         # Feature-specific mutation hooks
  hooks/
    useAuth.ts
    useApi.ts
  services/
    api/
      client.ts            # Axios/fetch configuration
      users.ts             # User API functions
      posts.ts             # Post API functions
  providers/
    ReactQueryProvider.tsx
  types/
    index.ts
```

## Setup

### Provider Configuration

```typescript
// providers/ReactQueryProvider.tsx
import { QueryClient, QueryClientProvider } from 'react-query';
import { ReactQueryDevtools } from 'react-query/devtools';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000,    // 5 minutes
      cacheTime: 30 * 60 * 1000,   // 30 minutes
      retry: 2,
      refetchOnWindowFocus: true,
    },
  },
});

export function ReactQueryProvider({ children }: { children: React.ReactNode }) {
  return (
    <QueryClientProvider client={queryClient}>
      {children}
      <ReactQueryDevtools />
    </QueryClientProvider>
  );
}
```

## Query Patterns

### Basic Query Hook

```typescript
import { useQuery } from 'react-query';
import { fetchUser, User } from '@/services/api/users';

export function useUser(userId: string) {
  return useQuery<User, Error>(
    ['user', userId],
    () => fetchUser(userId),
    {
      enabled: !!userId,
      staleTime: 1000 * 60 * 10, // 10 minutes
    }
  );
}
```

### Query with Error Handling

Services should throw user-friendly errors that React Query can catch and display:

```typescript
// services/api/users.ts
export async function fetchUser(userId: string): Promise<User> {
  const response = await fetch(`/api/users/${userId}`);

  if (!response.ok) {
    // Throw user-friendly error message
    throw new Error('Unable to load user profile. Please try again.');
  }

  return response.json();
}

// Component usage
function UserProfile({ userId }: { userId: string }) {
  const { data: user, isLoading, error } = useUser(userId);

  if (isLoading) return <LoadingSpinner />;
  if (error) return <ErrorMessage message={error.message} />;

  return <ProfileCard user={user} />;
}
```

### Dependent Queries

```typescript
function useUserWithPosts(userId: string) {
  const userQuery = useUser(userId);

  const postsQuery = useQuery(
    ['posts', userId],
    () => fetchUserPosts(userId),
    {
      enabled: !!userQuery.data,
    }
  );

  return { userQuery, postsQuery };
}
```

### Paginated Queries

```typescript
function usePaginatedUsers(page: number, limit: number = 10) {
  return useQuery(
    ['users', 'list', { page, limit }],
    () => fetchUsers({ page, limit }),
    {
      keepPreviousData: true,
    }
  );
}
```

### Infinite Scroll

```typescript
import { useInfiniteQuery } from 'react-query';

function useInfiniteUsers() {
  return useInfiniteQuery(
    ['users', 'infinite'],
    ({ pageParam = 1 }) => fetchUsers({ page: pageParam }),
    {
      getNextPageParam: (lastPage) => lastPage.nextPage ?? undefined,
    }
  );
}
```

## Mutation Patterns

### Basic Mutation

```typescript
import { useMutation, useQueryClient } from 'react-query';

function useCreateUser() {
  const queryClient = useQueryClient();

  return useMutation(createUser, {
    onSuccess: () => {
      queryClient.invalidateQueries(['users']);
    },
    onError: (error: Error) => {
      toast.error(error.message);
    },
  });
}
```

### Optimistic Updates

```typescript
function useUpdateUser() {
  const queryClient = useQueryClient();

  return useMutation(updateUser, {
    onMutate: async (updatedUser) => {
      await queryClient.cancelQueries(['user', updatedUser.id]);

      const previousUser = queryClient.getQueryData(['user', updatedUser.id]);

      queryClient.setQueryData(['user', updatedUser.id], updatedUser);

      return { previousUser };
    },
    onError: (err, updatedUser, context) => {
      if (context?.previousUser) {
        queryClient.setQueryData(['user', updatedUser.id], context.previousUser);
      }
    },
    onSettled: (data, error, updatedUser) => {
      queryClient.invalidateQueries(['user', updatedUser.id]);
    },
  });
}
```

## State Management Integration

### Combining with Context/Reducer

Use React Query for server state and Context/Reducer for client state:

```typescript
// Client state with Context
const AppStateContext = createContext<AppState | undefined>(undefined);
const AppDispatchContext = createContext<Dispatch<Action> | undefined>(undefined);

function AppProvider({ children }: { children: React.ReactNode }) {
  const [state, dispatch] = useReducer(appReducer, initialState);

  return (
    <AppStateContext.Provider value={state}>
      <AppDispatchContext.Provider value={dispatch}>
        {children}
      </AppDispatchContext.Provider>
    </AppStateContext.Provider>
  );
}

// Server state with React Query
function UserDashboard() {
  const { theme } = useAppState();         // Client state
  const { data: user } = useUser(userId);  // Server state

  return <Dashboard theme={theme} user={user} />;
}
```

### Combining with Zustand (Alternative)

```typescript
import { create } from 'zustand';

// Client state store
const useStore = create((set) => ({
  theme: 'light',
  setTheme: (theme) => set({ theme }),
}));

// Component using both
function App() {
  const theme = useStore((state) => state.theme);
  const { data: user } = useUser(userId);

  return <Layout theme={theme} user={user} />;
}
```

## Performance Optimization

### Query Key Best Practices

```typescript
// Structured query keys
const queryKeys = {
  users: {
    all: ['users'] as const,
    lists: () => [...queryKeys.users.all, 'list'] as const,
    list: (filters: Filters) => [...queryKeys.users.lists(), filters] as const,
    details: () => [...queryKeys.users.all, 'detail'] as const,
    detail: (id: string) => [...queryKeys.users.details(), id] as const,
  },
};
```

### Selective Subscriptions

```typescript
// Only subscribe to user name changes
function useUserName(userId: string) {
  return useUser(userId, {
    select: (user) => user.name,
  });
}
```

### Prefetching

```typescript
function UserListItem({ userId }: { userId: string }) {
  const queryClient = useQueryClient();

  const handleMouseEnter = () => {
    queryClient.prefetchQuery(
      ['user', userId],
      () => fetchUser(userId),
      { staleTime: 60000 }
    );
  };

  return (
    <li onMouseEnter={handleMouseEnter}>
      <Link to={`/users/${userId}`}>View Profile</Link>
    </li>
  );
}
```

## Error Handling Patterns

### Global Error Handler

```typescript
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      onError: (error: Error) => {
        console.error('Query error:', error);
      },
    },
    mutations: {
      onError: (error: Error) => {
        toast.error(error.message);
      },
    },
  },
});
```

### Error Boundaries

```typescript
import { QueryErrorResetBoundary } from 'react-query';
import { ErrorBoundary } from 'react-error-boundary';

function App() {
  return (
    <QueryErrorResetBoundary>
      {({ reset }) => (
        <ErrorBoundary
          onReset={reset}
          fallbackRender={({ error, resetErrorBoundary }) => (
            <div>
              <p>Something went wrong: {error.message}</p>
              <button onClick={resetErrorBoundary}>Try again</button>
            </div>
          )}
        >
          <UserProfile />
        </ErrorBoundary>
      )}
    </QueryErrorResetBoundary>
  );
}
```

## Key Conventions

1. Use React Query DevTools to inspect cache and track query status
2. Group react-query hooks within feature-specific directories (feature-based organization)
3. Always handle errors properly with user-friendly messages and retry options
4. Fetch only required data - use API parameters to reduce data transfer
5. Avoid deeply nesting queries - flatten when possible for better performance
6. Use local state for component-specific data, global state for shared data
7. Leverage React Query's built-in caching and state management capabilities

## Anti-Patterns to Avoid

- Do not use `useEffect` for data fetching
- Do not store server data in `useState`
- Do not forget loading and error state handling
- Do not create queries without proper cache invalidation strategies
- Do not skip the `enabled` option for conditional queries
- Do not ignore TypeScript types for query responses
