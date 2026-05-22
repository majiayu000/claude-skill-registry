---
name: solid-router-queries
description: "Solid Router queries: query() for data fetching with caching/deduplication, createAsync() for reactive signals, createAsyncStore() for fine-grained reactivity, query keys for revalidation."
metadata:
  globs:
    - "**/*router*"
    - "**/routes/**/*"
---

# Solid Router Queries

## Defining Queries

Queries provide caching, deduplication, and revalidation:

```tsx
import { query } from "@solidjs/router";

const getUserQuery = query(async (userId: string) => {
  const response = await fetch(`/api/users/${userId}`);
  if (!response.ok) {
    throw new Error("Failed to fetch user");
  }
  return response.json();
}, "user");
```

**Query features:**
- Automatic request deduplication
- Caching for preloading and navigation
- Server-side deduplication in SSR
- Automatic revalidation after actions
- Browser history navigation reuse

## Using Queries with createAsync

```tsx
import { Show, Suspense, ErrorBoundary } from "solid-js";
import { createAsync, query } from "@solidjs/router";

const getUserQuery = query(async (id: string) => {
  // Fetch user
}, "user");

function UserProfile(props: { userId: string }) {
  const user = createAsync(() => getUserQuery(props.userId));
  
  return (
    <ErrorBoundary fallback={<div>Error loading user</div>}>
      <Suspense fallback={<div>Loading...</div>}>
        <Show when={user()}>
          <div>{user()!.name}</div>
        </Show>
      </Suspense>
    </ErrorBoundary>
  );
}
```

### createAsync Options

```tsx
const data = createAsync(() => getDataQuery(), {
  name: "myData",        // Debug name
  initialValue: [],      // Initial value before fetch
  deferStream: true      // Wait for data before streaming (SSR)
});
```

**deferStream**: Set to `true` when data is critical for SEO or initial render.

## createAsyncStore

For large datasets that need fine-grained reactivity:

```tsx
import { createAsyncStore } from "@solidjs/router";

const getNotificationsQuery = query(async (unreadOnly: boolean) => {
  // Fetch notifications
}, "notifications");

function Notifications() {
  const notifications = createAsyncStore(() =>
    getNotificationsQuery(false),
    { initialValue: [] }
  );
  
  // Access as store (direct property access)
  return (
    <For each={notifications()}>
      {(notification) => (
        <div>{notification.message}</div>
      )}
    </For>
  );
}
```

**Use `createAsyncStore` when:**
- Working with large, complex data structures
- Need fine-grained reactivity on nested properties
- Want reconciliation when data updates

## cache (Deprecated)

**Note:** `cache` is deprecated since v0.15.0. Use `query` instead.

```tsx
// ❌ Deprecated
import { cache } from "@solidjs/router";
const getUser = cache(async (id) => fetchUser(id), "user");

// ✅ Use query instead
import { query } from "@solidjs/router";
const getUser = query(async (id) => fetchUser(id), "user");
```

## Query Keys

Query keys are generated from name and arguments. Access for revalidation:

```tsx
const getProductQuery = query(async (id: string) => {
  // ...
}, "product");

// Base key - revalidates all instances
getProductQuery.key

// Specific key - revalidates one instance
getProductQuery.keyFor("123")
```

## Best Practices

1. Wrap async data with `<Suspense>` and `<ErrorBoundary>`
2. Use `deferStream: true` for SEO-critical data
3. Use query names for debugging and devtools
4. Use `createAsyncStore` for complex nested data
5. Access query keys for manual revalidation when needed
