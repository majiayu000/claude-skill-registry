---
name: web-data-fetching-swr
description: SWR data fetching patterns - useSWR, useSWRMutation, caching, revalidation, infinite scroll
---

# SWR Data Fetching Patterns

> **Quick Guide:** SWR implements the stale-while-revalidate caching strategy: show cached data instantly, revalidate in the background. Keys must be stable (strings or stable arrays), `isLoading` is for initial fetches only (use `isValidating` for background refreshes), and all write operations go through `useSWRMutation`. The null key pattern is how you do conditional fetching -- never call hooks conditionally.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

**(You MUST use a stable key -- keys should NOT change on every render or you'll trigger infinite requests)**

**(You MUST handle isLoading vs isValidating correctly -- isLoading is true only on initial fetch with no data)**

**(You MUST wrap mutations in `useSWRMutation` for write operations -- NOT useSWR)**

**(You MUST use named constants for ALL timeout, retry, and interval values -- NO magic numbers)**

**(You MUST use named exports only -- NO default exports)**

</critical_requirements>

---

**Auto-detection:** SWR, useSWR, useSWRMutation, useSWRInfinite, useSWRImmutable, SWRConfig, mutate, revalidate, fetcher, stale-while-revalidate, preload

**When to use:**

- Read-heavy applications with infrequent mutations
- Need lightweight bundle (~5KB gzipped)
- Simple caching with automatic revalidation
- Applications where stale-while-revalidate pattern is desired

**When NOT to use:**

- Complex mutation workflows requiring many lifecycle callbacks
- Need built-in request cancellation (SWR requires manual AbortController)
- Complex dependent queries needing fine-grained invalidation control

**Key patterns covered:**

- useSWR hook with typed fetchers and state handling
- isLoading vs isValidating distinction (the most common mistake)
- Revalidation strategies (focus, reconnect, interval, manual)
- useSWRMutation for write operations with optimistic updates
- useSWRInfinite for cursor and offset pagination
- Null key pattern for conditional fetching
- SWRConfig for global defaults and SSR fallback

**Detailed Resources:**

- [examples/core.md](examples/core.md) -- Fetchers, return values, SWRConfig, key patterns
- [examples/mutations.md](examples/mutations.md) -- useSWRMutation, optimistic updates, cache invalidation
- [examples/caching.md](examples/caching.md) -- Revalidation strategies, prefetching, persistence
- [examples/pagination.md](examples/pagination.md) -- useSWRInfinite, infinite scroll, offset pagination
- [examples/conditional.md](examples/conditional.md) -- Dependent queries, auth-gated fetching
- [examples/error-handling.md](examples/error-handling.md) -- Retry config, error boundaries, network detection
- [examples/suspense.md](examples/suspense.md) -- Suspense integration, SSR fallback patterns
- [reference.md](reference.md) -- Decision frameworks, configuration tables

---

<philosophy>

## Philosophy

SWR (stale-while-revalidate) returns cached data first, then revalidates in the background. This creates fast, responsive UIs while ensuring data freshness.

**Core principles:**

- **Stale-While-Revalidate**: Show cached data immediately, update in background
- **Deduplication**: Multiple components using same key share one request
- **Focus Revalidation**: Refetch when user returns to tab
- **Optimistic UI**: Update UI immediately, rollback on error
- **Minimal API**: Simple hooks, less configuration than alternatives

**Trade-offs:**

- Simpler API means less control over complex mutation scenarios
- Request cancellation requires manual AbortController setup
- Less opinionated about mutations (fewer lifecycle callbacks)

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Typed Fetcher

The fetcher must throw on non-OK responses. If it doesn't throw, SWR treats error bodies as valid data.

```typescript
// lib/fetcher.ts
interface FetchError extends Error {
  info: unknown;
  status: number;
}

const fetcher = async <T>(url: string): Promise<T> => {
  const response = await fetch(url);
  if (!response.ok) {
    const error = new Error("Fetch failed") as FetchError;
    error.info = await response.json().catch(() => null);
    error.status = response.status;
    throw error;
  }
  return response.json();
};

export { fetcher };
export type { FetchError };
```

**Why good:** Throws on error (required for SWR error state to work), attaches status for conditional handling, typed error enables downstream type narrowing

See [examples/core.md](examples/core.md) for axios, GraphQL, and multi-argument fetcher variants.

---

### Pattern 2: isLoading vs isValidating

The most common SWR mistake. `isLoading` is true only on initial fetch with no data. `isValidating` is true during any in-flight request.

```typescript
// State combinations:
// Initial load:     { data: undefined, isLoading: true,  isValidating: true }
// Success:          { data: T,         isLoading: false, isValidating: false }
// Revalidating:     { data: T,         isLoading: false, isValidating: true }
// Error (no data):  { error: Error,    isLoading: false, isValidating: false }
// Error (has data): { data: T, error: Error, isLoading: false }
```

```typescript
// BAD: Using isValidating as loading indicator hides cached data
if (isValidating) return <Spinner />;

// GOOD: isLoading for initial, isValidating for refresh indicator
if (isLoading) return <Spinner />;
return (
  <div>
    {isValidating && <RefreshIndicator />}
    {error && data && <Banner>Data may be outdated</Banner>}
    <Content data={data} />
  </div>
);
```

**Why bad:** Showing spinner during background revalidation hides perfectly valid cached data, defeating the purpose of stale-while-revalidate

See [examples/core.md](examples/core.md) for full state handling with error + stale data combinations.

---

### Pattern 3: SWRConfig Global Defaults

Centralize fetcher, retry, and revalidation settings. Nested SWRConfig overrides parent config.

```typescript
const ERROR_RETRY_COUNT = 3;
const ERROR_RETRY_INTERVAL_MS = 5000;
const DEDUP_INTERVAL_MS = 2000;

<SWRConfig value={{
  fetcher,
  errorRetryCount: ERROR_RETRY_COUNT,
  errorRetryInterval: ERROR_RETRY_INTERVAL_MS,
  dedupingInterval: DEDUP_INTERVAL_MS,
  keepPreviousData: true,
  fallback, // Pre-fetched data for SSR hydration
}}>
  {children}
</SWRConfig>
```

**Why good:** Eliminates config duplication across components, `fallback` prop enables SSR data hydration, nested configs allow per-section overrides

See [examples/core.md](examples/core.md) for full provider setup and nested config override patterns.

---

### Pattern 4: useSWRMutation for Writes

Never use `useSWR` for mutations. `useSWR` fires on mount -- `useSWRMutation` fires on demand via `trigger()`.

```typescript
import useSWRMutation from "swr/mutation";

async function createPost(
  url: string,
  { arg }: { arg: CreatePostInput },
): Promise<Post> {
  const response = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(arg),
  });
  if (!response.ok) throw new Error("Failed to create post");
  return response.json();
}

const { trigger, isMutating, error, reset } = useSWRMutation(
  "/api/posts",
  createPost,
);
await trigger({ title, content });
```

**Why good:** `trigger()` gives explicit control over when mutation fires, `isMutating` provides loading state, `reset` clears error state, separate from useSWR keeps read/write concerns apart

See [examples/mutations.md](examples/mutations.md) for optimistic updates, cache invalidation, and `populateCache` patterns.

---

### Pattern 5: Optimistic Updates with Rollback

Update UI immediately while mutation is in-flight. Rollback on error.

```typescript
const { trigger } = useSWRMutation(`/api/todos/${todo.id}`, toggleTodo, {
  optimisticData: (currentData: Todo) => ({
    ...currentData,
    completed: !currentData.completed,
  }),
  rollbackOnError: true,
  revalidate: true,
});
```

**Why good:** `optimisticData` shows instant feedback, `rollbackOnError` ensures consistency on failure, `revalidate: true` syncs with server after success

See [examples/mutations.md](examples/mutations.md) for list-level optimistic updates and `populateCache` for skipping revalidation.

---

### Pattern 6: Null Key for Conditional Fetching

Pass `null` as the key to skip the request. Never call hooks conditionally.

```typescript
// BAD: Conditional hook call (breaks Rules of Hooks)
if (!userId) return <SelectUser />;
const { data } = useSWR(`/api/users/${userId}`, fetcher);

// GOOD: Null key prevents request without conditional hook
const { data } = useSWR(userId ? `/api/users/${userId}` : null, fetcher);

// GOOD: Dependent queries -- second waits for first
const { data: user } = useSWR(`/api/users/${userId}`, fetcher);
const { data: posts } = useSWR(user ? `/api/users/${user.id}/posts` : null, fetcher);
```

**Why good:** Hook always called (no Rules of Hooks violation), null key is idiomatic SWR pattern, enables data cascades for dependent queries

See [examples/conditional.md](examples/conditional.md) for auth-gated, feature-flag, and complex multi-condition patterns.

---

### Pattern 7: useSWRInfinite for Pagination

The `getKey` function receives page index and previous page data. Return `null` to stop.

```typescript
import useSWRInfinite from "swr/infinite";

const PAGE_SIZE = 20;

const getKey = (pageIndex: number, previousPageData: PostsResponse | null) => {
  if (previousPageData && !previousPageData.hasMore) return null; // End
  if (pageIndex === 0) return `/api/posts?limit=${PAGE_SIZE}`;
  return `/api/posts?limit=${PAGE_SIZE}&cursor=${previousPageData?.nextCursor}`;
};

const { data, size, setSize, isLoading } = useSWRInfinite<PostsResponse>(
  getKey,
  fetcher,
  {
    revalidateFirstPage: false,
  },
);

const posts = data?.flatMap((page) => page.posts) ?? [];
const isReachingEnd = data?.[data.length - 1]?.hasMore === false;
```

**Why good:** `getKey` returning null stops fetching, `flatMap` flattens pages, `revalidateFirstPage: false` prevents refetching all pages on focus

See [examples/pagination.md](examples/pagination.md) for IntersectionObserver infinite scroll, offset pagination, and filtered pagination with reset.

---

### Pattern 8: Revalidation Strategies

Choose strategy based on data freshness requirements.

```typescript
const POLL_INTERVAL_MS = 10 * 1000;

// Real-time: polling
useSWR(key, fetcher, {
  refreshInterval: POLL_INTERVAL_MS,
  refreshWhenHidden: false,
});

// Default: revalidate on focus/reconnect (enabled by default)
useSWR(key, fetcher, { revalidateOnFocus: true, revalidateOnReconnect: true });

// Static: disable all revalidation
useSWR(key, fetcher, {
  revalidateOnFocus: false,
  revalidateOnReconnect: false,
  revalidateIfStale: false,
});

// Shorthand for static: useSWRImmutable
import useSWRImmutable from "swr/immutable";
useSWRImmutable(key, fetcher);
```

**Why good:** Different strategies for different freshness needs, `useSWRImmutable` is cleaner than disabling all options manually, `refreshWhenHidden: false` prevents polling when tab is hidden

See [examples/caching.md](examples/caching.md) for prefetching with `preload()`, cache persistence with localStorage, and deduplication.

</patterns>

---

<red_flags>

## RED FLAGS

**High Priority Issues:**

- **Unstable key causing infinite requests** -- Object/array keys create new references each render. Use string keys or stable arrays of primitives.
- **isValidating used as loading state** -- Shows spinner during background refresh, hiding cached data. Use `isLoading` for initial load only.
- **useSWR for mutations** -- `useSWR` fires on mount. Use `useSWRMutation` for POST/PUT/DELETE.
- **Fetcher doesn't throw on error** -- Non-throwing fetcher returns error body as `data`, error state never triggers.
- **Conditional hook call** -- `if (!userId) return; const { data } = useSWR(...)` breaks Rules of Hooks. Use null key pattern.

**Medium Priority Issues:**

- **Missing `rollbackOnError` with `optimisticData`** -- Without rollback, failed mutations leave stale optimistic data in cache.
- **`keepPreviousData: true` for search** -- Shows stale search results for a different query. Set to `false` for search.
- **`revalidateAll: true` with useSWRInfinite** -- Refetches all loaded pages on every focus event. Disable for performance.
- **Missing error retry configuration** -- Default retry may not be appropriate (retries 404s, retries auth errors).
- **Creating fetcher inside component** -- Creates new function reference each render, breaking deduplication.

**Gotchas & Edge Cases:**

- `null` key stops fetching, but `undefined` key still fetches (gets coerced to string `"undefined"`)
- `mutate()` without arguments revalidates the bound key only, but global `mutate()` without a key filter revalidates everything
- `refreshInterval: 0` disables polling (same as omitting the option)
- `revalidateOnFocus` fires on every tab focus even if data is fresh (use `focusThrottleInterval` to limit)
- Multiple `useSWR` with same key share cache and deduplicate requests automatically
- `fallback` in `SWRConfig` must match exact key strings -- `/api/users/1` and `/api/users/1/` are different keys
- `useSWRInfinite` revalidates all pages by default (set `revalidateAll: false`)
- Error objects don't serialize well for cache persistence -- use structured error types
- `useSWRImmutable` in v2.4+ properly overrides global `refreshInterval` settings (fixed from earlier versions)

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

**(You MUST use a stable key -- keys should NOT change on every render or you'll trigger infinite requests)**

**(You MUST handle isLoading vs isValidating correctly -- isLoading is true only on initial fetch with no data)**

**(You MUST wrap mutations in `useSWRMutation` for write operations -- NOT useSWR)**

**(You MUST use named constants for ALL timeout, retry, and interval values -- NO magic numbers)**

**(You MUST use named exports only -- NO default exports)**

**Failure to follow these rules will cause infinite request loops, incorrect loading states, and unmaintainable code.**

</critical_reminders>
