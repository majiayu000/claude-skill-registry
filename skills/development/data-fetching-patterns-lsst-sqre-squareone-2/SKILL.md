---
name: data-fetching-patterns
description: SWR-based data fetching and caching patterns used throughout the monorepo. Use this skill when implementing API interactions, creating custom data hooks, handling loading/error states, or working with mock data. Covers SWR configuration, custom hook patterns (useUserInfo, useTimesSquarePage), error handling, and mock data setup.
---

# Data Fetching Patterns

The monorepo uses SWR (stale-while-revalidate) for data fetching and caching.

## SWR Basics

### Simple Usage

```typescript
import useSWR from 'swr';

function MyComponent() {
  const { data, error, isLoading } = useSWR('/api/data', fetcher);

  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;

  return <div>{data.value}</div>;
}
```

### Fetcher Function

```typescript
const fetcher = (url: string) => fetch(url).then(res => res.json());

// Or with error handling
const fetcher = async (url: string) => {
  const res = await fetch(url);

  if (!res.ok) {
    const error = new Error('An error occurred while fetching the data.');
    error.info = await res.json();
    error.status = res.status;
    throw error;
  }

  return res.json();
};
```

## Custom Hook Pattern

### Basic Pattern

```typescript
import useSWR from 'swr';

type UserData = {
  username: string;
  email: string;
  groups: string[];
};

export function useUserInfo() {
  const { data, error, isLoading } = useSWR<UserData>(
    '/auth/api/v1/user-info',
    fetcher
  );

  return {
    user: data,
    isLoading,
    error,
  };
}
```

### With Conditional Fetching

```typescript
export function useTimesSquarePage(pageSlug: string | null) {
  const { data, error, isLoading } = useSWR(
    pageSlug ? `/times-square/api/v1/pages/${pageSlug}` : null,
    fetcher
  );

  return {
    page: data,
    isLoading,
    error,
  };
}
```

### With Parameters

```typescript
export function usePageData(id: string, options?: { refreshInterval?: number }) {
  const { data, error, isLoading, mutate } = useSWR(
    `/api/pages/${id}`,
    fetcher,
    {
      refreshInterval: options?.refreshInterval,
    }
  );

  return {
    data,
    isLoading,
    error,
    refresh: mutate, // Manual revalidation
  };
}
```

## Error Handling

### In Components

```typescript
function MyComponent() {
  const { data, error, isLoading } = useUserInfo();

  if (isLoading) {
    return <LoadingSpinner />;
  }

  if (error) {
    return (
      <ErrorMessage
        title="Failed to load user data"
        message={error.message}
        retry={() => window.location.reload()}
      />
    );
  }

  if (!data) {
    return <EmptyState message="No data available" />;
  }

  return <UserProfile user={data} />;
}
```

### Global Error Handler

```typescript
// _app.tsx
import { SWRConfig } from 'swr';

function MyApp({ Component, pageProps }) {
  return (
    <SWRConfig
      value={{
        fetcher,
        onError: (error, key) => {
          console.error('SWR Error:', key, error);
          // Send to error tracking
        },
      }}
    >
      <Component {...pageProps} />
    </SWRConfig>
  );
}
```

## Mutations

### Optimistic Updates

```typescript
function useUpdateUser() {
  const { data, mutate } = useSWR('/api/user', fetcher);

  const updateUser = async (updates: Partial<UserData>) => {
    // Optimistic update
    mutate(
      { ...data, ...updates },
      false // Don't revalidate yet
    );

    try {
      // Make API call
      const updated = await fetch('/api/user', {
        method: 'PATCH',
        body: JSON.stringify(updates),
      }).then(res => res.json());

      // Revalidate with real data
      mutate(updated);
    } catch (error) {
      // Rollback on error
      mutate();
      throw error;
    }
  };

  return { data, updateUser };
}
```

### Revalidation

```typescript
function MyComponent() {
  const { data, mutate } = useSWR('/api/data', fetcher);

  const handleRefresh = () => {
    mutate(); // Revalidate
  };

  const handleUpdate = async () => {
    await updateData();
    mutate(); // Revalidate after update
  };

  return (
    <div>
      <button onClick={handleRefresh}>Refresh</button>
      {data && <DataDisplay data={data} />}
    </div>
  );
}
```

## Caching and Revalidation

### SWR Configuration

```typescript
<SWRConfig
  value={{
    refreshInterval: 30000, // Revalidate every 30s
    revalidateOnFocus: true, // Revalidate when window regains focus
    revalidateOnReconnect: true, // Revalidate on network recovery
    dedupingInterval: 2000, // Dedupe requests within 2s
  }}
>
  <App />
</SWRConfig>
```

### Per-Hook Configuration

```typescript
const { data } = useSWR('/api/data', fetcher, {
  refreshInterval: 10000, // Override global setting
  revalidateOnFocus: false,
});
```

## Mock Data

### Development Mocks

```typescript
// src/lib/mocks/userData.ts
export const mockUserData = {
  username: 'testuser',
  email: 'test@example.com',
  groups: ['admin', 'developers'],
  uid: 1000,
};

export const mockUserDataError = {
  error: 'Unauthorized',
  message: 'Invalid credentials',
};
```

### Mock API Routes

```typescript
// pages/api/dev/user-info.ts
import type { NextApiRequest, NextApiResponse } from 'next';
import { mockUserData } from '../../../src/lib/mocks/userData';

export default function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  // Simulate delay
  setTimeout(() => {
    res.status(200).json(mockUserData);
  }, 500);
}
```

### Conditional Mocking

```typescript
const fetcher = async (url: string) => {
  // Use mock in development
  if (process.env.NODE_ENV === 'development' && url.startsWith('/api/dev/')) {
    return fetch(url).then(res => res.json());
  }

  // Use real API in production
  return fetch(url).then(res => res.json());
};
```

## Loading States

### Skeleton Loaders

```typescript
function MyComponent() {
  const { data, isLoading } = useData();

  if (isLoading) {
    return (
      <div>
        <Skeleton width="100%" height={60} />
        <Skeleton width="80%" height={40} />
        <Skeleton width="90%" height={40} />
      </div>
    );
  }

  return <DataDisplay data={data} />;
}
```

### Suspense (Experimental)

```typescript
import { Suspense } from 'react';

function MyComponent() {
  const { data } = useSWR('/api/data', fetcher, {
    suspense: true, // Enable Suspense
  });

  return <DataDisplay data={data} />;
}

// Usage
<Suspense fallback={<LoadingSpinner />}>
  <MyComponent />
</Suspense>
```

## Pagination

```typescript
function usePaginatedData(page: number, pageSize: number) {
  const { data, error, isLoading } = useSWR(
    `/api/data?page=${page}&size=${pageSize}`,
    fetcher
  );

  return {
    data: data?.items || [],
    total: data?.total || 0,
    isLoading,
    error,
  };
}

function PaginatedList() {
  const [page, setPage] = useState(1);
  const { data, total, isLoading } = usePaginatedData(page, 10);

  return (
    <div>
      {isLoading ? <LoadingSpinner /> : <List items={data} />}
      <Pagination
        current={page}
        total={total}
        onChange={setPage}
      />
    </div>
  );
}
```

## Infinite Loading

```typescript
import useSWRInfinite from 'swr/infinite';

function useInfiniteData() {
  const getKey = (pageIndex: number, previousPageData: any) => {
    if (previousPageData && !previousPageData.hasMore) return null;
    return `/api/data?page=${pageIndex}`;
  };

  const { data, size, setSize, isLoading } = useSWRInfinite(
    getKey,
    fetcher
  );

  const items = data ? data.flatMap(page => page.items) : [];
  const hasMore = data ? data[data.length - 1]?.hasMore : false;

  return {
    items,
    isLoading,
    hasMore,
    loadMore: () => setSize(size + 1),
  };
}
```

## Best Practices

1. **Create custom hooks** for each API endpoint
2. **Handle all states** (loading, error, empty)
3. **Use TypeScript types** for data
4. **Mock APIs** for development
5. **Configure revalidation** appropriately
6. **Use optimistic updates** for better UX
7. **Dedupe requests** with SWR's built-in caching
8. **Handle authentication** in fetcher
9. **Log errors** for debugging
10. **Test with mock data**

## Common Patterns

### Dependent Fetching

```typescript
function useUserAndPosts() {
  const { data: user } = useUserInfo();
  const { data: posts } = useSWR(
    user ? `/api/users/${user.id}/posts` : null,
    fetcher
  );

  return { user, posts };
}
```

### Polling

```typescript
const { data } = useSWR('/api/status', fetcher, {
  refreshInterval: 1000, // Poll every second
});
```

### Prefetching

```typescript
import { mutate } from 'swr';

function prefetchData() {
  mutate('/api/data', fetcher('/api/data'));
}

// Prefetch on hover
<Link onMouseEnter={() => prefetchData('/api/page-data')}>
  Page
</Link>
```
