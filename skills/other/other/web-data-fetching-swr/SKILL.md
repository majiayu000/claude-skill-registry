---
name: web-data-fetching-swr
description: SWR data fetching patterns - useSWR, useSWRMutation, caching, revalidation, infinite scroll
---

# SWR Data Fetching Patterns

> **Quick Guide:** Use SWR for lightweight data fetching with stale-while-revalidate caching. Ideal for read-heavy applications with minimal mutations. Choose over React Query when you need a smaller bundle size and simpler API.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

**(You MUST use a stable key - keys should NOT change on every render or you'll trigger infinite requests)**

**(You MUST handle isLoading vs isValidating correctly - isLoading is true only on initial fetch with no data)**

**(You MUST wrap mutations in `useSWRMutation` for write operations - NOT useSWR)**

**(You MUST use named constants for ALL timeout, retry, and interval values - NO magic numbers)**

**(You MUST use named exports only - NO default exports)**

</critical_requirements>

---

**Auto-detection:** SWR useSWR, useSWRMutation, useSWRInfinite, SWRConfig, mutate, revalidate, fetcher, stale-while-revalidate

**When to use:**

- Read-heavy applications with infrequent mutations
- Need lightweight bundle (5.3KB vs 16KB for React Query)
- Simple caching with automatic revalidation
- Next.js applications (built by Vercel, seamless integration)
- Applications where stale-while-revalidate pattern is desired

**When NOT to use:**

- Complex mutation workflows with many side effects (use React Query)
- Need request cancellation out of the box (use React Query)
- Complex dependent queries with fine-grained control

> **Note (SWR 2.0+):** SWR DevTools browser extension is now available with zero setup for v2+. See [SWR DevTools](https://swr-devtools.vercel.app/) for installation.

**Key patterns covered:**

- useSWR hook for data fetching with caching
- Fetcher function patterns (fetch, axios)
- isLoading vs isValidating distinction
- Revalidation strategies (focus, reconnect, interval)
- useSWRMutation for write operations
- Optimistic updates with rollback
- useSWRInfinite for pagination
- Conditional fetching (null key pattern)
- SWRConfig for global configuration
- Suspense integration

**Detailed Resources:**

- For code examples, see [examples/](examples/)
- For decision frameworks and anti-patterns, see [reference.md](reference.md)

---

<philosophy>

## Philosophy

SWR (stale-while-revalidate) is a data fetching strategy that returns cached (stale) data first, then sends the fetch request (revalidate), and finally comes with the up-to-date data. This creates a fast, responsive UI while ensuring data freshness.

**Core principles:**

- **Stale-While-Revalidate**: Show cached data immediately, update in background
- **Deduplication**: Multiple components using same key share one request
- **Focus Revalidation**: Refetch when user returns to tab
- **Optimistic UI**: Update UI immediately, rollback on error
- **Minimal API**: Simple hooks, less configuration than alternatives

**Trade-offs:**

- Simpler API means less control over complex scenarios
- Request cancellation requires manual AbortController setup
- Less opinionated about mutations than React Query

**SWR 2.0+ Features:**

- SWR DevTools browser extension (zero setup for v2+)
- useSWRMutation for remote mutations with trigger function
- preload API for prefetching resources
- isLoading state (distinct from isValidating)
- keepPreviousData option for smooth data transitions
- throwOnError option for error boundary integration

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Basic useSWR Setup

Use useSWR for fetching data with automatic caching and revalidation.

#### Constants

```typescript
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "/api";
```

#### Fetcher Function

```typescript
// lib/fetcher.ts
const fetcher = async <T>(url: string): Promise<T> => {
  const response = await fetch(url);

  if (!response.ok) {
    const error = new Error("An error occurred while fetching the data.");
    // Attach extra info to the error object
    (error as any).info = await response.json();
    (error as any).status = response.status;
    throw error;
  }

  return response.json();
};

export { fetcher };
```

#### Implementation

```typescript
// components/user-profile.tsx
import useSWR from "swr";
import { fetcher } from "@/lib/fetcher";

interface User {
  id: string;
  name: string;
  email: string;
}

function UserProfile({ userId }: { userId: string }) {
  const { data, error, isLoading, isValidating, mutate } = useSWR<User>(
    `/api/users/${userId}`,
    fetcher
  );

  // isLoading: First load, no data yet
  if (isLoading) return <UserProfileSkeleton />;

  // error: Request failed
  if (error) return <ErrorCard message={error.message} onRetry={() => mutate()} />;

  // No data after loading
  if (!data) return <NotFound message="User not found" />;

  return (
    <article>
      {/* isValidating: Background refresh in progress */}
      {isValidating && <RefreshIndicator />}
      <h1>{data.name}</h1>
      <p>{data.email}</p>
    </article>
  );
}

export { UserProfile };
```

**Why good:** Clear distinction between isLoading (initial) and isValidating (background), typed fetcher provides type safety, bound mutate enables manual revalidation

---

### Pattern 2: Return Values and States

Understand all useSWR return values for proper state handling.

#### State Machine

```typescript
// Understanding useSWR states
interface SWRState<T> {
  data: T | undefined; // The fetched data
  error: Error | undefined; // Error object if request failed
  isLoading: boolean; // True when fetching AND no data exists
  isValidating: boolean; // True when any request is in-flight
  mutate: () => Promise<T>; // Manually revalidate
}

// State combinations:
// Initial load:     { data: undefined, isLoading: true,  isValidating: true }
// Success:          { data: {...},     isLoading: false, isValidating: false }
// Revalidating:     { data: {...},     isLoading: false, isValidating: true }
// Error (no data):  { error: {...},    isLoading: false, isValidating: false }
// Error (has data): { data: {...}, error: {...}, isLoading: false, isValidating: false }
```

#### Implementation

```typescript
// components/data-display.tsx
import useSWR from "swr";

function DataDisplay({ endpoint }: { endpoint: string }) {
  const { data, error, isLoading, isValidating, mutate } = useSWR(endpoint, fetcher);

  // Pattern: Show loading only on initial fetch
  if (isLoading) {
    return <Skeleton />;
  }

  // Pattern: Show error with retry
  if (error && !data) {
    return (
      <div className="error">
        <p>Failed to load: {error.message}</p>
        <button onClick={() => mutate()}>Retry</button>
      </div>
    );
  }

  // Pattern: Show stale data with error banner
  if (error && data) {
    return (
      <div>
        <Banner type="warning">Data may be outdated. {error.message}</Banner>
        <DataView data={data} />
      </div>
    );
  }

  // Pattern: Show data with refresh indicator
  return (
    <div>
      {isValidating && <span className="refresh-indicator">Updating...</span>}
      <DataView data={data} />
    </div>
  );
}

export { DataDisplay };
```

**Why good:** Handles all state combinations gracefully, shows stale data with error banner rather than hiding it, refresh indicator informs users without blocking content

---

### Pattern 3: Global Configuration with SWRConfig

Configure SWR defaults at the application level.

#### Constants

```typescript
const REVALIDATE_INTERVAL_MS = 30 * 1000;
const ERROR_RETRY_COUNT = 3;
const ERROR_RETRY_INTERVAL_MS = 5000;
const DEDUPING_INTERVAL_MS = 2000;
```

#### Implementation

```typescript
// providers/swr-provider.tsx
"use client";

import { SWRConfig } from "swr";
import type { ReactNode } from "react";
import { fetcher } from "@/lib/fetcher";

const REVALIDATE_INTERVAL_MS = 30 * 1000;
const ERROR_RETRY_COUNT = 3;
const ERROR_RETRY_INTERVAL_MS = 5000;
const DEDUPING_INTERVAL_MS = 2000;

interface SWRProviderProps {
  children: ReactNode;
  fallback?: Record<string, unknown>;
}

function SWRProvider({ children, fallback = {} }: SWRProviderProps) {
  return (
    <SWRConfig
      value={{
        // Default fetcher for all useSWR calls
        fetcher,

        // Revalidation settings
        revalidateOnFocus: true,
        revalidateOnReconnect: true,
        revalidateIfStale: true,

        // Polling (disabled by default)
        refreshInterval: 0,

        // Error handling
        errorRetryCount: ERROR_RETRY_COUNT,
        errorRetryInterval: ERROR_RETRY_INTERVAL_MS,
        shouldRetryOnError: true,

        // Deduplication
        dedupingInterval: DEDUPING_INTERVAL_MS,

        // Performance
        keepPreviousData: true,

        // Pre-fetched data (from SSR/SSG)
        fallback,

        // Global error handler
        onError: (error, key) => {
          if (error.status !== 403 && error.status !== 404) {
            // Report to error tracking service
            console.error(`SWR Error [${key}]:`, error);
          }
        },
      }}
    >
      {children}
    </SWRConfig>
  );
}

export { SWRProvider };
```

**Why good:** Centralized configuration reduces repetition, fallback enables SSR/SSG data hydration, named constants make intervals self-documenting, global error handler enables centralized logging

---

### Pattern 4: Fetcher Patterns (fetch, axios)

Create typed fetchers for different HTTP clients.

#### Fetch Fetcher

```typescript
// lib/fetchers/fetch-fetcher.ts
interface FetchError extends Error {
  info: unknown;
  status: number;
}

async function fetchFetcher<T>(url: string): Promise<T> {
  const response = await fetch(url, {
    credentials: "include",
    headers: {
      "Content-Type": "application/json",
    },
  });

  if (!response.ok) {
    const error = new Error("Fetch failed") as FetchError;
    error.info = await response.json().catch(() => null);
    error.status = response.status;
    throw error;
  }

  return response.json();
}

export { fetchFetcher };
export type { FetchError };
```

#### Axios Fetcher

```typescript
// lib/fetchers/axios-fetcher.ts
import axios from "axios";
import type { AxiosError } from "axios";

const API_TIMEOUT_MS = 10000;

const apiClient = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
  timeout: API_TIMEOUT_MS,
  withCredentials: true,
});

async function axiosFetcher<T>(url: string): Promise<T> {
  const response = await apiClient.get<T>(url);
  return response.data;
}

// Fetcher with POST (for complex queries)
async function axiosPostFetcher<T>([url, body]: [string, unknown]): Promise<T> {
  const response = await apiClient.post<T>(url, body);
  return response.data;
}

export { axiosFetcher, axiosPostFetcher, apiClient };
```

#### GraphQL Fetcher

```typescript
// lib/fetchers/graphql-fetcher.ts
interface GraphQLVariables {
  [key: string]: unknown;
}

interface GraphQLResponse<T> {
  data: T;
  errors?: Array<{ message: string }>;
}

const GRAPHQL_ENDPOINT = process.env.NEXT_PUBLIC_GRAPHQL_URL || "/graphql";

async function graphqlFetcher<T>([query, variables]: [
  string,
  GraphQLVariables?,
]): Promise<T> {
  const response = await fetch(GRAPHQL_ENDPOINT, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ query, variables }),
  });

  const json: GraphQLResponse<T> = await response.json();

  if (json.errors) {
    throw new Error(json.errors.map((e) => e.message).join(", "));
  }

  return json.data;
}

export { graphqlFetcher };
```

**Why good:** Typed fetchers provide full TypeScript support, error objects include status for conditional handling, axios instance enables interceptors and defaults, array keys enable multi-parameter fetchers

---

### Pattern 5: Revalidation Strategies

Control when and how data is revalidated.

#### Constants

```typescript
const POLL_INTERVAL_MS = 10 * 1000;
const FOCUS_THROTTLE_MS = 5000;
```

#### Implementation

```typescript
// components/live-data.tsx
import useSWR from "swr";

const POLL_INTERVAL_MS = 10 * 1000;
const FOCUS_THROTTLE_MS = 5000;

// Pattern 1: Polling for real-time data
function LiveStockPrice({ symbol }: { symbol: string }) {
  const { data } = useSWR(
    `/api/stocks/${symbol}`,
    fetcher,
    {
      // Poll every 10 seconds
      refreshInterval: POLL_INTERVAL_MS,
      // Don't poll when window is hidden
      refreshWhenHidden: false,
      // Don't poll when offline
      refreshWhenOffline: false,
    }
  );

  return <span>{data?.price}</span>;
}

// Pattern 2: Revalidate on focus (default behavior)
function UserDashboard() {
  const { data } = useSWR("/api/dashboard", fetcher, {
    revalidateOnFocus: true,
    // Throttle focus revalidation
    focusThrottleInterval: FOCUS_THROTTLE_MS,
  });

  return <Dashboard data={data} />;
}

// Pattern 3: Revalidate on reconnect
function OfflineAwareData() {
  const { data } = useSWR("/api/data", fetcher, {
    revalidateOnReconnect: true,
  });

  return <DataView data={data} />;
}

// Pattern 4: Disable automatic revalidation (static data)
function StaticContent() {
  const { data } = useSWR("/api/config", fetcher, {
    revalidateOnFocus: false,
    revalidateOnReconnect: false,
    revalidateIfStale: false,
  });

  return <Config data={data} />;
}

// Pattern 5: Manual revalidation only
function ManualRefresh() {
  const { data, mutate } = useSWR("/api/data", fetcher, {
    revalidateOnFocus: false,
    revalidateOnReconnect: false,
    revalidateIfStale: false,
    refreshInterval: 0,
  });

  return (
    <div>
      <DataView data={data} />
      <button onClick={() => mutate()}>Refresh</button>
    </div>
  );
}

export { LiveStockPrice, UserDashboard, OfflineAwareData, StaticContent, ManualRefresh };
```

**Why good:** Different strategies for different data freshness needs, named constants make intervals clear, disabled options for static data prevent unnecessary requests

---

### Pattern 6: useSWRMutation for Write Operations

Use useSWRMutation for POST/PUT/DELETE operations.

#### Implementation

```typescript
// components/create-post-form.tsx
import useSWRMutation from "swr/mutation";
import { useState } from "react";
import type { FormEvent } from "react";

interface CreatePostInput {
  title: string;
  content: string;
}

interface Post {
  id: string;
  title: string;
  content: string;
  createdAt: string;
}

// Mutation fetcher - receives key and { arg }
async function createPost(url: string, { arg }: { arg: CreatePostInput }): Promise<Post> {
  const response = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(arg),
  });

  if (!response.ok) {
    throw new Error("Failed to create post");
  }

  return response.json();
}

function CreatePostForm({ onSuccess }: { onSuccess?: (post: Post) => void }) {
  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");

  const { trigger, isMutating, error, reset } = useSWRMutation(
    "/api/posts",
    createPost,
    {
      onSuccess: (data) => {
        setTitle("");
        setContent("");
        onSuccess?.(data);
      },
      onError: (err) => {
        console.error("Create post failed:", err);
      },
    }
  );

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    if (!title.trim() || !content.trim()) return;

    await trigger({ title, content });
  };

  return (
    <form onSubmit={handleSubmit}>
      {error && (
        <div className="error">
          <p>{error.message}</p>
          <button type="button" onClick={reset}>Dismiss</button>
        </div>
      )}
      <input
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        placeholder="Title"
        disabled={isMutating}
      />
      <textarea
        value={content}
        onChange={(e) => setContent(e.target.value)}
        placeholder="Content"
        disabled={isMutating}
      />
      <button type="submit" disabled={isMutating || !title.trim() || !content.trim()}>
        {isMutating ? "Creating..." : "Create Post"}
      </button>
    </form>
  );
}

export { CreatePostForm };
```

**Why good:** trigger function gives control over when mutation fires, isMutating provides loading state, reset clears error state, separate from useSWR keeps read/write concerns separated

---

### Pattern 7: Optimistic Updates

Update UI immediately while mutation is in progress.

#### Implementation

```typescript
// components/todo-item.tsx
import useSWR, { useSWRConfig } from "swr";
import useSWRMutation from "swr/mutation";

interface Todo {
  id: string;
  title: string;
  completed: boolean;
}

async function toggleTodo(url: string, { arg }: { arg: { completed: boolean } }) {
  const response = await fetch(url, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(arg),
  });
  return response.json();
}

function TodoItem({ todo }: { todo: Todo }) {
  const { mutate } = useSWRConfig();

  const { trigger } = useSWRMutation(
    `/api/todos/${todo.id}`,
    toggleTodo,
    {
      // Optimistic update
      optimisticData: (currentData: Todo) => ({
        ...currentData,
        completed: !currentData.completed,
      }),

      // Rollback on error
      rollbackOnError: true,

      // Revalidate after mutation
      revalidate: true,

      // Also update the list cache
      onSuccess: () => {
        mutate("/api/todos");
      },
    }
  );

  return (
    <label>
      <input
        type="checkbox"
        checked={todo.completed}
        onChange={() => trigger({ completed: !todo.completed })}
      />
      <span style={{ textDecoration: todo.completed ? "line-through" : "none" }}>
        {todo.title}
      </span>
    </label>
  );
}

export { TodoItem };
```

#### Advanced Optimistic Pattern with List Updates

```typescript
// components/todo-list.tsx
import useSWR, { useSWRConfig } from "swr";
import useSWRMutation from "swr/mutation";

interface Todo {
  id: string;
  title: string;
  completed: boolean;
}

async function deleteTodo(url: string) {
  const response = await fetch(url, { method: "DELETE" });
  if (!response.ok) throw new Error("Delete failed");
  return response.json();
}

function TodoList() {
  const { data: todos, mutate } = useSWR<Todo[]>("/api/todos", fetcher);

  const handleDelete = async (todoId: string) => {
    // Optimistically remove from list
    const optimisticTodos = todos?.filter((t) => t.id !== todoId);

    // Update cache optimistically, then revalidate
    await mutate(
      async () => {
        await fetch(`/api/todos/${todoId}`, { method: "DELETE" });
        return optimisticTodos;
      },
      {
        optimisticData: optimisticTodos,
        rollbackOnError: true,
        revalidate: true,
      }
    );
  };

  return (
    <ul>
      {todos?.map((todo) => (
        <li key={todo.id}>
          {todo.title}
          <button onClick={() => handleDelete(todo.id)}>Delete</button>
        </li>
      ))}
    </ul>
  );
}

export { TodoList };
```

**Why good:** optimisticData shows immediate feedback, rollbackOnError ensures data consistency on failure, mutate with function enables complex update logic, list cache updated after item mutation

---

### Pattern 8: useSWRInfinite for Pagination

Implement infinite scroll with useSWRInfinite.

#### Constants

```typescript
const PAGE_SIZE = 20;
const INTERSECTION_THRESHOLD = 0.5;
```

#### Implementation

```typescript
// components/infinite-post-list.tsx
import useSWRInfinite from "swr/infinite";
import { useCallback, useRef, useEffect } from "react";

interface Post {
  id: string;
  title: string;
  excerpt: string;
}

interface PostsResponse {
  posts: Post[];
  nextCursor: string | null;
  hasMore: boolean;
}

const PAGE_SIZE = 20;
const INTERSECTION_THRESHOLD = 0.5;

// Key function - receives page index and previous page data
const getKey = (pageIndex: number, previousPageData: PostsResponse | null) => {
  // Reached the end
  if (previousPageData && !previousPageData.hasMore) return null;

  // First page
  if (pageIndex === 0) return `/api/posts?limit=${PAGE_SIZE}`;

  // Subsequent pages with cursor
  return `/api/posts?limit=${PAGE_SIZE}&cursor=${previousPageData?.nextCursor}`;
};

function InfinitePostList() {
  const loadMoreRef = useRef<HTMLDivElement>(null);

  const {
    data,
    error,
    size,
    setSize,
    isLoading,
    isValidating,
  } = useSWRInfinite<PostsResponse>(getKey, fetcher, {
    revalidateFirstPage: false,
    revalidateOnFocus: false,
  });

  // Flatten pages into single array
  const posts = data?.flatMap((page) => page.posts) ?? [];
  const isEmpty = data?.[0]?.posts.length === 0;
  const isReachingEnd = data?.[data.length - 1]?.hasMore === false;
  const isLoadingMore = isLoading || (size > 0 && data && typeof data[size - 1] === "undefined");

  // Intersection Observer for infinite scroll
  const loadMore = useCallback(() => {
    if (!isReachingEnd && !isLoadingMore) {
      setSize(size + 1);
    }
  }, [isReachingEnd, isLoadingMore, setSize, size]);

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        if (entries[0].isIntersecting) {
          loadMore();
        }
      },
      { threshold: INTERSECTION_THRESHOLD }
    );

    const currentRef = loadMoreRef.current;
    if (currentRef) observer.observe(currentRef);

    return () => {
      if (currentRef) observer.unobserve(currentRef);
    };
  }, [loadMore]);

  if (isLoading) return <PostListSkeleton count={PAGE_SIZE} />;
  if (error) return <ErrorCard message={error.message} />;
  if (isEmpty) return <EmptyState message="No posts found" />;

  return (
    <div className="post-list">
      <ul>
        {posts.map((post) => (
          <li key={post.id}>
            <article>
              <h3>{post.title}</h3>
              <p>{post.excerpt}</p>
            </article>
          </li>
        ))}
      </ul>

      <div ref={loadMoreRef} className="load-more-sentinel">
        {isLoadingMore && <Spinner />}
        {isReachingEnd && posts.length > 0 && <p>No more posts</p>}
      </div>
    </div>
  );
}

export { InfinitePostList };
```

**Why good:** getKey function handles pagination logic, null return stops fetching, flatMap combines pages, IntersectionObserver enables smooth infinite scroll, proper loading states prevent UI flicker

---

### Pattern 9: Conditional Fetching

Control when requests are made using null key or conditional logic.

#### Null Key Pattern

```typescript
// components/conditional-data.tsx
import useSWR from "swr";

// Pattern 1: Null key prevents request
function UserProfile({ userId }: { userId: string | null }) {
  // Won't fetch if userId is null
  const { data, isLoading } = useSWR(
    userId ? `/api/users/${userId}` : null,
    fetcher
  );

  if (!userId) return <p>Please select a user</p>;
  if (isLoading) return <Skeleton />;

  return <Profile user={data} />;
}

// Pattern 2: Dependent queries
function UserPosts({ userId }: { userId: string }) {
  // First query
  const { data: user } = useSWR(`/api/users/${userId}`, fetcher);

  // Dependent query - only runs when user data exists
  const { data: posts } = useSWR(
    user ? `/api/users/${user.id}/posts` : null,
    fetcher
  );

  return (
    <div>
      <h1>{user?.name}</h1>
      <PostList posts={posts} />
    </div>
  );
}

// Pattern 3: Conditional based on state
function SearchResults() {
  const [searchTerm, setSearchTerm] = useState("");
  const MIN_SEARCH_LENGTH = 3;

  // Only search when term is long enough
  const { data, isLoading } = useSWR(
    searchTerm.length >= MIN_SEARCH_LENGTH
      ? `/api/search?q=${encodeURIComponent(searchTerm)}`
      : null,
    fetcher,
    {
      // Don't keep stale search results
      keepPreviousData: false,
    }
  );

  return (
    <div>
      <input
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
        placeholder="Search..."
      />
      {isLoading && <Spinner />}
      {data && <Results items={data} />}
    </div>
  );
}

export { UserProfile, UserPosts, SearchResults };
```

**Why good:** Null key is the idiomatic SWR pattern for conditional fetching, dependent queries enable data cascades, keepPreviousData: false prevents showing stale search results

---

### Pattern 10: TypeScript Patterns

Proper typing for SWR hooks.

#### Implementation

```typescript
// types/api.ts
interface User {
  id: string;
  name: string;
  email: string;
}

interface Post {
  id: string;
  title: string;
  content: string;
  authorId: string;
}

interface ApiError {
  message: string;
  status: number;
}

// Typed hook wrapper
import useSWR from "swr";
import type { SWRConfiguration, Key, Fetcher } from "swr";

function useTypedSWR<T>(
  key: Key,
  options?: SWRConfiguration<T, ApiError>
) {
  return useSWR<T, ApiError>(key, fetcher, options);
}

// Usage in component
function UserCard({ userId }: { userId: string }) {
  const { data, error } = useTypedSWR<User>(`/api/users/${userId}`);

  if (error) {
    // error is typed as ApiError
    if (error.status === 404) return <NotFound />;
    return <Error message={error.message} />;
  }

  // data is typed as User | undefined
  return <Card name={data?.name} email={data?.email} />;
}

// Generic fetcher with type inference
async function typedFetcher<T>(url: string): Promise<T> {
  const response = await fetch(url);
  if (!response.ok) {
    const error: ApiError = {
      message: "Fetch failed",
      status: response.status,
    };
    throw error;
  }
  return response.json() as Promise<T>;
}

export { useTypedSWR, typedFetcher };
export type { User, Post, ApiError };
```

**Why good:** Generic types flow through to components, error typing enables type-safe error handling, wrapper hooks reduce boilerplate, type inference works with conditional data

</patterns>

---

<integration>

## Integration Guide

**Works with:**

- **Next.js**: Built by Vercel, seamless integration with App Router and Pages Router, supports SSR/SSG fallback
- **React**: Client-side data fetching with hooks
- **axios**: Can use axios as fetcher for interceptors and defaults
- **TypeScript**: Full type inference for data and errors

**Replaces / Conflicts with:**

- **React Query**: Both are data fetching libraries - choose one. SWR is simpler, React Query has more features
- **Apollo Client (for REST)**: SWR is for REST/custom APIs, Apollo is for GraphQL
- **Custom fetch hooks**: SWR provides caching and deduplication that custom hooks typically lack

</integration>

---

<critical_reminders>

## CRITICAL REMINDERS

**(You MUST use a stable key - keys should NOT change on every render or you'll trigger infinite requests)**

**(You MUST handle isLoading vs isValidating correctly - isLoading is true only on initial fetch with no data)**

**(You MUST wrap mutations in `useSWRMutation` for write operations - NOT useSWR)**

**(You MUST use named constants for ALL timeout, retry, and interval values - NO magic numbers)**

**(You MUST use named exports only - NO default exports)**

**Failure to follow these rules will cause infinite request loops, incorrect loading states, and unmaintainable code.**

</critical_reminders>
