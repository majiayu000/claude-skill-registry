---
name: solid-router-advanced
description: "Solid Router advanced: preloading routes, streaming with Suspense, revalidation (automatic/manual), layouts, response helpers (json/redirect/reload), protected routes."
metadata:
  globs:
    - "**/*router*"
    - "**/routes/**/*"
---

# Solid Router Advanced Patterns

## Routing Setup

### Component-Based Routing (JSX)

Define routes using JSX components:

```tsx
import { Router, Route } from "@solidjs/router";

<Router>
  <Route path="/" component={Home} />
  <Route path="/about" component={About} />
</Router>
```

### Config-Based Routing

Define routes using config objects (useful for lazy loading):

```tsx
import { lazy } from "solid-js";
import { Router } from "@solidjs/router";

const routes = [
  {
    path: "/",
    component: lazy(() => import("./routes/index")),
  },
  {
    path: "/about",
    component: lazy(() => import("./routes/about")),
  }
];

<Router>{routes}</Router>
```

**Best practice:** Use `lazy()` with config-based routing for code splitting.

## Preloading

### Route Preloading

Preload data before navigation:

```tsx
import { Route, query, createAsync } from "@solidjs/router";

const getProductQuery = query(async (id: string) => {
  // Fetch product
}, "product");

function ProductPage(props) {
  const product = createAsync(() => getProductQuery(props.params.id));
  return <div>{product()?.title}</div>;
}

function preloadProduct({ params }: { params: { id: string } }) {
  getProductQuery(params.id);
}

function Routes() {
  return (
    <Route 
      path="/products/:id" 
      component={ProductPage} 
      preload={preloadProduct}
    />
  );
}
```

**Preloading triggers:**
- On hover over links (user intent)
- During route rendering (ensure data ready)

**Benefits:**
- Data ready when component renders
- No loading spinners on navigation
- Better perceived performance

### Preload with Intent

```tsx
function preloadData({ params, intent }) {
  if (intent === "preload") {
    // Only prefetch, don't wait
    getProductQuery(params.id);
  } else {
    // During navigation, ensure data is ready
    return getProductQuery(params.id);
  }
}
```

## Streaming

### Suspense Boundaries

Create independent streaming boundaries:

```tsx
import { Suspense, For } from "solid-js";
import { query, createAsync } from "@solidjs/router";

const getAccountStatsQuery = query(async () => {
  // Slow query
}, "accountStats");

const getRecentTransactionsQuery = query(async () => {
  // Fast query
}, "recentTransactions");

function Dashboard() {
  const stats = createAsync(() => getAccountStatsQuery());
  const transactions = createAsync(() => getRecentTransactionsQuery());
  
  return (
    <div>
      <h1>Dashboard</h1>
      
      <Suspense fallback={<p>Loading stats...</p>}>
        <For each={stats()}>
          {(stat) => <div>{stat.label}: {stat.value}</div>}
        </For>
      </Suspense>
      
      <Suspense fallback={<p>Loading transactions...</p>}>
        <For each={transactions()}>
          {(transaction) => <div>{transaction.description}</div>}
        </For>
      </Suspense>
    </div>
  );
}
```

Each `<Suspense>` creates independent boundary - fast queries render while slow ones stream.

### Disabling Streaming

Use `deferStream: true` for SEO-critical data:

```tsx
const article = createAsync(() => getArticleQuery(), {
  deferStream: true // Wait for data before initial HTML
});

return <h1>{article()?.title}</h1>; // Always in initial HTML
```

## Revalidation

### Automatic Revalidation

After actions complete successfully, all active queries revalidate automatically.

### Manual Revalidation

```tsx
import { revalidate } from "@solidjs/router";

const refreshUser = async () => {
  await updateUserData();
  // Revalidate specific query
  revalidate(getUserQuery.keyFor(userId));
  
  // Revalidate all instances of query
  revalidate(getUserQuery.key);
  
  // Revalidate multiple queries
  revalidate([getUserQuery.key, getPostsQuery.key]);
};
```

### Selective Revalidation

Use `json` helper to control revalidation:

```tsx
import { json } from "@solidjs/router";

const createPostAction = action(async (formData: FormData) => {
  const newPost = await db.createPost(formData);
  
  // Only revalidate posts query, not user query
  return json(newPost, { 
    revalidate: "posts" 
  });
}, "createPost");

// Disable automatic revalidation
return json(newPost, { revalidate: [] });
```

## Response Helpers

### json

Return JSON with revalidation control:

```tsx
import { json } from "@solidjs/router";

const getData = query(async () => {
  return json(
    { data: "value" },
    {
      revalidate: ["posts", "users"],
      headers: { "Cache-Control": "max-age=60" },
      status: 200
    }
  );
}, "data");
```

### redirect

```tsx
import { redirect } from "@solidjs/router";

const loginAction = action(async (formData: FormData) => {
  await authenticate(formData);
  throw redirect("/dashboard"); // Or return redirect(...)
}, "login");
```

### reload

```tsx
import { reload } from "@solidjs/router";

const refreshAction = action(async () => {
  await invalidateCache();
  throw reload(); // Reload current route data
}, "refresh");
```

## Layouts

### Root Layout

```tsx
import { Router } from "@solidjs/router";

const Layout = (props) => (
  <>
    <header>Header</header>
    {props.children}
    <footer>Footer</footer>
  </>
);

<Router root={Layout}>
  <Route path="/" component={Home} />
</Router>
```

### Nested Layouts

```tsx
function PageWrapper(props) {
  return (
    <div>
      <h1>Users</h1>
      {props.children}
      <A href="/">Back Home</A>
    </div>
  );
}

<Router>
  <Route path="/users" component={PageWrapper}>
    <Route path="/" component={Users} />
    <Route path="/:id" component={User} />
  </Route>
</Router>
```

## Route Configuration

```tsx
import type { RouteDefinition } from "@solidjs/router";

export const route = {
  preload({ params, location, intent }) {
    // Preload logic
    if (intent === "preload") {
      getProductQuery(params.id);
    } else {
      return getProductQuery(params.id);
    }
  }
} satisfies RouteDefinition;

export default function Page() {
  return <div>Content</div>;
}
```

## Protected Routes

```tsx
const getProtectedData = query(async () => {
  if (!isAuthenticated()) {
    throw redirect("/login");
  }
  return await fetchProtectedData();
}, "protectedData");

function ProtectedPage() {
  const data = createAsync(() => getProtectedData(), { deferStream: true });
  return <div>{data()}</div>;
}
```

**Important:** Use `deferStream: true` - server-side redirects can't occur after streaming starts.

## Error Handling

```tsx
import { ErrorBoundary } from "solid-js";

function DataComponent() {
  const data = createAsync(() => fetchData());
  
  return (
    <ErrorBoundary fallback={(err) => <div>Error: {err.message}</div>}>
      <Suspense fallback={<div>Loading...</div>}>
        <div>{data()}</div>
      </Suspense>
    </ErrorBoundary>
  );
}
```

## Rendering Modes

### SPA (Single Page Application)

Client-side routing without SSR. Configure redirects for CDN/hosting:

**Netlify** (`public/_redirects`):
```
/*   /index.html   200
```

**Vercel** (`vercel.json`):
```json
{
  "rewrites": [
    {
      "source": "/(.*)",
      "destination": "/index.html"
    }
  ]
}
```

### SSR (Server-Side Rendering)

Enable SSR by passing URL to Router:

```tsx
import { isServer } from "solid-js/web";
import { Router } from "@solidjs/router";

<Router url={isServer ? req.url : ""}>
  {/* routes */}
</Router>
```

**Benefits:**
- SEO optimization
- Faster initial page load
- Server-side data preloading

## Best Practices

1. Preload important routes - Better navigation performance
2. Use streaming for non-critical data - Faster perceived performance
3. Use `deferStream` for SEO-critical data - Include in initial HTML
4. Revalidate selectively - Only revalidate what changed
5. Define layouts for consistent UI organization
6. Use `redirect` for server-side navigation (authentication, etc.)
7. Wrap async data with `<Suspense>` and `<ErrorBoundary>`
8. Configure redirects for SPA deployment

1. Preload important routes - Better navigation performance
2. Use streaming for non-critical data - Faster perceived performance
3. Use `deferStream` for SEO-critical data - Include in initial HTML
4. Revalidate selectively - Only revalidate what changed
5. Define layouts for consistent UI organization
6. Use `redirect` for server-side navigation (authentication, etc.)
7. Wrap async data with `<Suspense>` and `<ErrorBoundary>`

