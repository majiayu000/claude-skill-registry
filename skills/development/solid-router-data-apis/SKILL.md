---
name: solid-router-data-apis
description: "Solid Router data APIs: query for caching/deduplication, createAsync for reactive promises, createAsyncStore for store-based async, revalidate for cache invalidation."
metadata:
  globs:
    - "**/*query*"
    - "**/*createAsync*"
    - "**/*revalidate*"
---

# Solid Router Data APIs

Complete guide to data fetching and caching in Solid Router. Use these APIs for efficient data fetching, caching, and cache invalidation.

## query - Request Deduplication

`query` wraps an async function and provides automatic caching and deduplication. Prevents redundant API calls and enables efficient data fetching.

### Basic Usage

```tsx
import { query } from "@solidjs/router";

const getUserProfileQuery = query(async (userId: string) => {
  const response = await fetch(
    `https://api.example.com/users/${encodeURIComponent(userId)}`
  );
  const json = await response.json();

  if (!response.ok) {
    throw new Error(json?.message ?? "Failed to load user profile.");
  }

  return json;
}, "userProfile");
```

**Key characteristics:**
- Automatic deduplication
- Server-side request deduplication
- Preload cache (5 seconds)
- Browser back/forward cache (5 minutes)
- Active subscription reuse

### When Cache is Used

The cached result is reused in these scenarios:

1. **Preloading**: Within 5 seconds after preload
2. **Active subscriptions**: While component uses the query
3. **Browser navigation**: Back/forward button navigation
4. **Server-side**: Within single SSR request
5. **Client hydration**: Uses SSR data immediately

### Query Keys

```tsx
const getUserQuery = query(async (id: string) => {
  // ...
}, "users");

getUserQuery.key;              // "users"
getUserQuery.keyFor("123");    // "users[123]"
```

Keys are generated from:
- Query name (second parameter)
- Serialized arguments (deterministic)

## createAsync - Reactive Promises

`createAsync` transforms promises into reactive signals. Recommended for most async data fetching.

### Basic Usage

```tsx
import { createAsync, query } from "@solidjs/router";
import { Suspense, ErrorBoundary } from "solid-js";

const getUserQuery = query(async (id: string) => {
  const response = await fetch(`/api/users/${id}`);
  return response.json();
}, "user");

function UserProfile() {
  const user = createAsync(() => getUserQuery("123"));

  return (
    <ErrorBoundary fallback={<p>Could not fetch user data.</p>}>
      <Suspense fallback={<p>Loading user...</p>}>
        <p>{user()!.name}</p>
      </Suspense>
    </ErrorBoundary>
  );
}
```

### Options

```tsx
const data = createAsync(
  () => fetchData(),
  {
    name: "myData",           // Debug name
    initialValue: null,       // Initial value before fetch
    deferStream: false,       // Defer streaming until resolved
  }
);
```

**Options:**
- `name`: Debug identifier
- `initialValue`: Value before first fetch completes
- `deferStream`: Defer streaming SSR until resolved

### Reactive Dependencies

```tsx
function UserProfile() {
  const [userId, setUserId] = createSignal("123");
  
  // Re-fetches when userId changes
  const user = createAsync(() => getUserQuery(userId()));

  return (
    <div>
      <button onClick={() => setUserId("456")}>Switch User</button>
      <Suspense fallback={<p>Loading...</p>}>
        <p>{user()?.name}</p>
      </Suspense>
    </div>
  );
}
```

## createAsyncStore - Store-Based Async

`createAsyncStore` creates deeply reactive stores from async data. Uses reconciliation to merge updates intelligently.

### Basic Usage

```tsx
import { createAsyncStore, query } from "@solidjs/router";
import { For } from "solid-js";

const getNotificationsQuery = query(async (unreadOnly: boolean) => {
  const response = await fetch(
    `/api/notifications?unreadOnly=${unreadOnly}`
  );
  return response.json();
}, "notifications");

function Notifications() {
  const [unreadOnly, setUnreadOnly] = createSignal(false);
  const notifications = createAsyncStore(() =>
    getNotificationsQuery(unreadOnly())
  );

  return (
    <div>
      <button onClick={() => setUnreadOnly(!unreadOnly())}>
        Toggle unread
      </button>
      <ul>
        <For each={notifications()}>
          {(notification) => (
            <li>
              <div>{notification.message}</div>
              <div>{notification.user.name}</div>
            </li>
          )}
        </For>
      </ul>
    </div>
  );
}
```

### Reconciliation Options

```tsx
const data = createAsyncStore(
  () => fetchData(),
  {
    reconcile: {
      key: "id",        // Match items by id
      merge: false,      // Replace non-matching items
    },
  }
);
```

**Benefits:**
- Fine-grained updates (only changed fields)
- Preserves unchanged state
- Efficient for large datasets
- Intelligent merging

### When to Use

**createAsync:**
- Simple data structures
- No need for fine-grained updates
- Standard async data fetching

**createAsyncStore:**
- Complex nested data
- Large datasets
- Need fine-grained reactivity
- Model data with relationships

## revalidate - Cache Invalidation

`revalidate` manually refreshes cached queries. Use for polling, manual refetch, or after mutations.

### Basic Usage

```tsx
import { query, createAsync, revalidate } from "@solidjs/router";
import { For } from "solid-js";

const getPosts = query(async () => {
  return await fetch("https://api.com/posts").then((r) => r.json());
}, "posts");

function Posts() {
  const posts = createAsync(() => getPosts());

  function refetchPosts() {
    revalidate(getPosts.key);
  }

  return (
    <div>
      <button onClick={refetchPosts}>Refetch posts</button>
      <ul>
        <For each={posts()}>
          {(post) => <li>{post.title}</li>}
        </For>
      </ul>
    </div>
  );
}
```

### Revalidate Specific Query

```tsx
// Revalidate all queries with base key
revalidate(getPosts.key);

// Revalidate specific query
revalidate(getPosts.keyFor("123"));

// Revalidate multiple keys
revalidate([getPosts.key, getUsers.key]);

// Revalidate everything
revalidate(undefined);
```

### Force Revalidation

```tsx
// Delete cache and refetch
revalidate(getPosts.key, { force: true });

// Default behavior (force: true)
revalidate(getPosts.key);
```

**Parameters:**
- `key`: Query key or array of keys
- `force`: Delete cache before refetch (default: `true`)

## Common Patterns

### Query with Parameters

```tsx
const getUserQuery = query(
  async (id: string, options = {}) => {
    const params = new URLSearchParams({
      summary: String(options.summary || false),
    });
    const response = await fetch(`/api/users/${id}?${params}`);
    return response.json();
  },
  "usersById"
);

// Different arguments = different cache keys
getUserQuery("123");                    // Cache key: usersById[123,{}]
getUserQuery("123", { summary: true });  // Cache key: usersById[123,{"summary":true}]
```

### Preloading with Query

```tsx
import { lazy, Route } from "@solidjs/router";
import { getUserQuery } from "./queries";

const User = lazy(() => import("./pages/users/[id].js"));

// Preload function
function preloadUser({ params, location }) {
  void getUserQuery(params.id);
}

// Pass in route definition
<Route path="/users/:id" component={User} preload={preloadUser} />;
```

### Error Handling

```tsx
import { ErrorBoundary, Suspense } from "solid-js";
import { createAsync, query } from "@solidjs/router";

const getUserQuery = query(async (id: string) => {
  const response = await fetch(`/api/users/${id}`);
  if (!response.ok) {
    throw new Error("Failed to fetch user");
  }
  return response.json();
}, "user");

function UserProfile() {
  const user = createAsync(() => getUserQuery("123"));

  return (
    <ErrorBoundary
      fallback={(err) => (
        <div>
          <p>Error: {err.message}</p>
          <button onClick={() => revalidate(getUserQuery.keyFor("123"))}>
            Retry
          </button>
        </div>
      )}
    >
      <Suspense fallback={<p>Loading...</p>}>
        <div>{user()!.name}</div>
      </Suspense>
    </ErrorBoundary>
  );
}
```

### Polling

```tsx
import { onMount, onCleanup } from "solid-js";
import { createAsync, query, revalidate } from "@solidjs/router";

const getStatusQuery = query(async () => {
  return fetch("/api/status").then((r) => r.json());
}, "status");

function Status() {
  const status = createAsync(() => getStatusQuery());

  onMount(() => {
    const interval = setInterval(() => {
      revalidate(getStatusQuery.key);
    }, 5000); // Poll every 5 seconds

    onCleanup(() => clearInterval(interval));
  });

  return <div>Status: {status()?.value}</div>;
}
```

### After Mutations

```tsx
import { action, revalidate } from "@solidjs/router";
import { getUserQuery } from "./queries";

const updateUserAction = action(async (userId: string, data: FormData) => {
  await fetch(`/api/users/${userId}`, {
    method: "PUT",
    body: data,
  });
  
  // Revalidate after mutation
  revalidate(getUserQuery.keyFor(userId));
}, "updateUser");
```

### Multiple Data Sources

```tsx
const getUserQuery = query(async (id: string) => {
  return fetch(`/api/users/${id}`).then((r) => r.json());
}, "user");

const getUserPostsQuery = query(async (id: string) => {
  return fetch(`/api/users/${id}/posts`).then((r) => r.json());
}, "userPosts");

function UserProfile() {
  const [userId] = useParams();
  
  const user = createAsync(() => getUserQuery(userId));
  const posts = createAsync(() => getUserPostsQuery(userId));

  return (
    <Suspense fallback={<p>Loading...</p>}>
      <div>
        <h1>{user()!.name}</h1>
        <For each={posts()}>
          {(post) => <article>{post.title}</article>}
        </For>
      </div>
    </Suspense>
  );
}
```

## query vs cache

**Note:** `cache` is deprecated. Use `query` instead.

**query advantages:**
- Better performance
- Better invalidation
- More features
- Active development

## Best Practices

1. **Always use query for API calls:**
   - Automatic deduplication
   - Efficient caching
   - Preload support

2. **Use createAsync for reactive data:**
   - Works with Suspense
   - Automatic error handling
   - Reactive dependencies

3. **Use createAsyncStore for complex data:**
   - Fine-grained updates
   - Large datasets
   - Nested structures

4. **Revalidate after mutations:**
   - Keep data fresh
   - Update UI after changes
   - Invalidate related queries

5. **Handle errors and loading:**
   - Use ErrorBoundary
   - Use Suspense
   - Provide fallbacks

6. **Use meaningful query names:**
   - Unique per query function
   - Descriptive identifiers
   - Helps with debugging

## Summary

- **query**: Cache and deduplicate API calls
- **createAsync**: Reactive promises with Suspense
- **createAsyncStore**: Store-based async with reconciliation
- **revalidate**: Manual cache invalidation
- **query > cache**: Use query instead of deprecated cache

