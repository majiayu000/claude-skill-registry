---
name: web-framework-remix
description: File-based routing, loaders, actions, defer streaming, useFetcher, error boundaries, progressive enhancement
---

# Remix Framework Patterns

> **Quick Guide:** Remix is a full-stack React framework where each route exports a loader for reads and an action for writes. Data fetching happens on the server, forms work without JavaScript, and nested routes enable parallel data loading.

---

<migration_notice>

## IMPORTANT: React Router v7 Migration

**Remix has merged into React Router v7.** What was planned as Remix v3 is now React Router v7 "framework mode". Key changes:

**Deprecated utilities (will be removed in React Router v7):**

- `json()` - Return raw objects instead, or use `data()` for custom headers/status
- `defer()` - Return Promises directly in objects with Single Fetch

**New patterns in React Router v7:**

- `data()` utility for setting headers/status: `return data(item, { status: 201 })`
- Single Fetch enables returning raw objects and streaming Promises directly
- Automatic type generation: Use `Route.LoaderArgs`, `Route.ActionArgs`, `Route.ComponentProps` from `./+types/route-name`
- `clientAction` for browser-only mutations (complements server-only `action`)
- Imports change from `@remix-run/*` to `react-router` and `@react-router/*`
- Entry files: `RemixServer` → `ServerRouter`, `RemixBrowser` → `HydratedRouter`
- Scripts: `remix vite:dev` → `react-router dev`, `remix vite:build` → `react-router build`

**Migration resources:**

- [Upgrading from Remix](https://reactrouter.com/upgrading/remix)
- [Single Fetch Guide](https://v2.remix.run/docs/guides/single-fetch)
- [React Router v7 Actions](https://reactrouter.com/start/framework/actions)

**This skill documents Remix v2 patterns** which remain valid for existing projects. For new projects, consider using React Router v7 directly.

</migration_notice>

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST export loaders and actions as named exports from route modules only)**

**(You MUST use `useLoaderData<typeof loader>()` for type-safe data access in components)**

**(You MUST throw Response objects for expected errors - use ErrorBoundary for handling)**

**(You MUST wrap state mutations after await in `runInAction()` if combining with MobX)**

**(You MUST use `defer()` for non-critical data that can stream - keep critical data in direct returns)** _(deprecated in React Router v7 - use raw Promises instead)_

</critical_requirements>

---

**Auto-detection:** Remix routes, React Router v7, loader function, action function, clientAction, useLoaderData, useActionData, useFetcher, defer, ErrorBoundary, Form component, meta function, links function, Single Fetch, ServerRouter, HydratedRouter

**When to use:**

- Building full-stack React applications with server-side rendering
- Implementing data loading with loaders and mutations with actions
- Creating progressively enhanced forms that work without JavaScript
- Streaming non-critical data with defer and Suspense
- Handling errors gracefully with route-level ErrorBoundary

**Key patterns covered:**

- File-based routing (routes/, \_index, $params, \_layout)
- Loaders for data fetching
- Actions for mutations
- defer() for streaming
- useFetcher for non-navigation mutations
- Error boundaries (ErrorBoundary)
- Form component and progressive enhancement
- Meta and Links functions for SEO
- Resource routes
- Nested routing patterns

**When NOT to use:**

- Static sites without server-side logic (consider Astro)
- Simple SPAs without server rendering needs (consider Vite + React)
- Projects already committed to Next.js patterns

**Detailed Resources:**

- For code examples, see [examples.md](examples.md)
- For decision frameworks and anti-patterns, see [reference.md](reference.md)

---

<philosophy>

## Philosophy

Remix simplifies full-stack development to a single mental model: **each route exports a loader for reads and an action for writes**. Both functions execute exclusively on the server, enabling direct database access without exposing secrets to the client.

**Core Principles:**

1. **Server-first data loading**: Loaders run on the server before rendering, eliminating client-side data fetching waterfalls
2. **Progressive enhancement**: Forms work with plain POST requests - JavaScript enhances but isn't required
3. **HTTP semantics**: Caching uses standard HTTP headers (Cache-Control), not framework-specific solutions
4. **Nested routes**: URL segments map to component hierarchy, enabling parallel data loading
5. **Web standards**: Uses Fetch API Request/Response objects throughout

**Data Flow:**

```
URL Change → Loader(s) Execute → Component Renders → User Interacts
                                                          ↓
                                        Action Executes → Loaders Revalidate
```

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: File-Based Routing

Remix uses file-system conventions to define routes. Files in `app/routes/` become URL paths.

#### Routing Conventions

| File Name         | URL           | Description                   |
| ----------------- | ------------- | ----------------------------- |
| `_index.tsx`      | `/`           | Index route (root)            |
| `about.tsx`       | `/about`      | Static route                  |
| `blog.$slug.tsx`  | `/blog/:slug` | Dynamic parameter             |
| `blog_.tsx`       | `/blog`       | Pathless layout escape        |
| `_auth.tsx`       | (none)        | Layout route (no URL segment) |
| `_auth.login.tsx` | `/login`      | Route nested in layout        |
| `$.tsx`           | `/*`          | Splat/catch-all route         |

```typescript
// app/routes/blog.$slug.tsx
// URL: /blog/my-post-title
import type { LoaderFunctionArgs } from "@remix-run/node";
import { useLoaderData } from "@remix-run/react";

export async function loader({ params }: LoaderFunctionArgs) {
  const { slug } = params;
  // slug is typed as string | undefined
  return { slug };
}

export default function BlogPost() {
  const { slug } = useLoaderData<typeof loader>();
  return <h1>Post: {slug}</h1>;
}
```

**Why good:** File names map directly to URLs making routing predictable, dynamic segments use `$` prefix which is clear and TypeScript-friendly, loader params are typed

---

### Pattern 2: Loaders for Data Fetching

Loaders are server-only functions that provide data to routes. They run on initial server render and on client navigation via fetch.

#### Basic Loader

```typescript
// app/routes/users.tsx
import type { LoaderFunctionArgs } from "@remix-run/node";
import { json } from "@remix-run/node";
import { useLoaderData } from "@remix-run/react";

const DEFAULT_PAGE = 1;
const PAGE_SIZE = 20;

export async function loader({ request }: LoaderFunctionArgs) {
  const url = new URL(request.url);
  const page = Number(url.searchParams.get("page")) || DEFAULT_PAGE;

  const users = await db.user.findMany({
    skip: (page - 1) * PAGE_SIZE,
    take: PAGE_SIZE,
  });

  return json({ users, page });
}

export default function Users() {
  const { users, page } = useLoaderData<typeof loader>();

  return (
    <ul>
      {users.map((user) => (
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
  );
}
```

**Why good:** Type-safe data access with `typeof loader`, server-only code stays on server, named constants for pagination values, URL search params for pagination state

#### Throwing Responses for Expected Errors

```typescript
// app/routes/users.$userId.tsx
import type { LoaderFunctionArgs } from "@remix-run/node";
import { json } from "@remix-run/node";

const HTTP_NOT_FOUND = 404;
const HTTP_FORBIDDEN = 403;

export async function loader({ params, request }: LoaderFunctionArgs) {
  const user = await db.user.findUnique({ where: { id: params.userId } });

  if (!user) {
    throw json({ message: "User not found" }, { status: HTTP_NOT_FOUND });
  }

  const session = await getSession(request);
  if (!session.userId) {
    throw json(
      { message: "Authentication required" },
      { status: HTTP_FORBIDDEN },
    );
  }

  return json({ user });
}
```

**Why good:** Thrown responses trigger ErrorBoundary, HTTP status codes use named constants, early returns for invalid states, authentication checked in loader

---

### Pattern 3: Actions for Mutations

Actions handle non-GET requests (POST, PUT, DELETE, PATCH). They run before loaders and enable form handling.

#### Basic Action with Form

```typescript
// app/routes/contacts.new.tsx
import type { ActionFunctionArgs } from "@remix-run/node";
import { json, redirect } from "@remix-run/node";
import { Form, useActionData } from "@remix-run/react";

const HTTP_BAD_REQUEST = 400;

export async function action({ request }: ActionFunctionArgs) {
  const formData = await request.formData();
  const name = formData.get("name");
  const email = formData.get("email");

  const errors: Record<string, string> = {};

  if (!name || typeof name !== "string") {
    errors.name = "Name is required";
  }
  if (!email || typeof email !== "string" || !email.includes("@")) {
    errors.email = "Valid email is required";
  }

  if (Object.keys(errors).length > 0) {
    return json({ errors }, { status: HTTP_BAD_REQUEST });
  }

  await db.contact.create({ data: { name, email } });

  return redirect("/contacts");
}

export default function NewContact() {
  const actionData = useActionData<typeof action>();

  return (
    <Form method="post">
      <div>
        <label htmlFor="name">Name</label>
        <input id="name" name="name" type="text" />
        {actionData?.errors?.name && (
          <span role="alert">{actionData.errors.name}</span>
        )}
      </div>
      <div>
        <label htmlFor="email">Email</label>
        <input id="email" name="email" type="email" />
        {actionData?.errors?.email && (
          <span role="alert">{actionData.errors.email}</span>
        )}
      </div>
      <button type="submit">Create Contact</button>
    </Form>
  );
}
```

**Why good:** Form works without JavaScript (progressive enhancement), validation errors returned with proper HTTP status, redirect after successful mutation prevents double-submission, accessible error messages with role="alert"

#### Multiple Actions with Intent

```typescript
// app/routes/tasks.$taskId.tsx
import type { ActionFunctionArgs } from "@remix-run/node";
import { json, redirect } from "@remix-run/node";
import { Form } from "@remix-run/react";

type Intent = "update" | "delete" | "toggle";

export async function action({ params, request }: ActionFunctionArgs) {
  const formData = await request.formData();
  const intent = formData.get("intent") as Intent;

  switch (intent) {
    case "update": {
      const title = formData.get("title") as string;
      await db.task.update({
        where: { id: params.taskId },
        data: { title },
      });
      return json({ success: true });
    }
    case "delete": {
      await db.task.delete({ where: { id: params.taskId } });
      return redirect("/tasks");
    }
    case "toggle": {
      const task = await db.task.findUnique({ where: { id: params.taskId } });
      await db.task.update({
        where: { id: params.taskId },
        data: { completed: !task?.completed },
      });
      return json({ success: true });
    }
    default:
      throw new Error(`Unknown intent: ${intent}`);
  }
}

export default function Task() {
  return (
    <div>
      <Form method="post">
        <input type="hidden" name="intent" value="toggle" />
        <button type="submit">Toggle Complete</button>
      </Form>

      <Form method="post">
        <input type="hidden" name="intent" value="delete" />
        <button type="submit">Delete</button>
      </Form>
    </div>
  );
}
```

**Why good:** Single action handles multiple intents via hidden field, switch statement for clear intent handling, redirect after delete prevents stale data display

---

### Pattern 4: Defer for Streaming

Use `defer()` to stream non-critical data that can load after initial render.

```typescript
// app/routes/dashboard.tsx
import type { LoaderFunctionArgs } from "@remix-run/node";
import { defer } from "@remix-run/node";
import { Await, useLoaderData } from "@remix-run/react";
import { Suspense } from "react";

export async function loader({ request }: LoaderFunctionArgs) {
  // Critical data - wait for this
  const user = await getUser(request);

  // Non-critical data - stream this
  const analyticsPromise = getAnalytics(user.id);
  const recentActivityPromise = getRecentActivity(user.id);

  return defer({
    user,
    analytics: analyticsPromise,
    recentActivity: recentActivityPromise,
  });
}

export default function Dashboard() {
  const { user, analytics, recentActivity } = useLoaderData<typeof loader>();

  return (
    <div>
      <h1>Welcome, {user.name}</h1>

      <Suspense fallback={<div>Loading analytics...</div>}>
        <Await resolve={analytics}>
          {(data) => <AnalyticsChart data={data} />}
        </Await>
      </Suspense>

      <Suspense fallback={<div>Loading activity...</div>}>
        <Await resolve={recentActivity}>
          {(activity) => <ActivityList items={activity} />}
        </Await>
      </Suspense>
    </div>
  );
}
```

**Why good:** Critical user data loads immediately, non-critical data streams in parallel, Suspense provides loading states, page is interactive before all data loads

**When to use defer:**

- Analytics and reporting data
- Recommendation systems
- Comments and social features
- Any data not needed for initial render

**When NOT to defer:**

- Authentication data (user must be known)
- SEO-critical content
- Data needed for page structure

---

### Pattern 5: useFetcher for Non-Navigation Data

`useFetcher` enables data loading and mutations without causing page navigation.

#### Inline Mutations

```typescript
// app/routes/posts.$postId.tsx
import { useFetcher } from "@remix-run/react";

function LikeButton({ postId, isLiked }: { postId: string; isLiked: boolean }) {
  const fetcher = useFetcher();

  // Optimistic UI - show expected state immediately
  const optimisticIsLiked = fetcher.formData
    ? fetcher.formData.get("liked") === "true"
    : isLiked;

  return (
    <fetcher.Form method="post" action={`/api/posts/${postId}/like`}>
      <input type="hidden" name="liked" value={String(!optimisticIsLiked)} />
      <button type="submit" disabled={fetcher.state !== "idle"}>
        {optimisticIsLiked ? "Unlike" : "Like"}
      </button>
    </fetcher.Form>
  );
}
```

**Why good:** No page navigation on like/unlike, optimistic UI shows expected state immediately, disabled state prevents double-clicks

#### Data Loading Without Navigation

```typescript
// Autocomplete search component
import { useFetcher } from "@remix-run/react";
import { useEffect } from "react";

const DEBOUNCE_DELAY_MS = 300;

function SearchAutocomplete() {
  const fetcher = useFetcher<{ results: string[] }>();

  const handleSearch = (query: string) => {
    fetcher.load(`/api/search?q=${encodeURIComponent(query)}`);
  };

  return (
    <div>
      <input
        type="search"
        onChange={(e) => handleSearch(e.target.value)}
        placeholder="Search..."
      />
      {fetcher.state === "loading" && <span>Searching...</span>}
      {fetcher.data?.results && (
        <ul>
          {fetcher.data.results.map((result, i) => (
            <li key={i}>{result}</li>
          ))}
        </ul>
      )}
    </div>
  );
}
```

**Why good:** Search doesn't navigate away from current page, loading state indicates active request, type-safe response data

---

### Pattern 6: Error Boundaries

Export `ErrorBoundary` from route modules to handle errors gracefully.

```typescript
// app/routes/users.$userId.tsx
import { isRouteErrorResponse, useRouteError } from "@remix-run/react";

const HTTP_NOT_FOUND = 404;
const HTTP_UNAUTHORIZED = 401;
const HTTP_FORBIDDEN = 403;

export function ErrorBoundary() {
  const error = useRouteError();

  if (isRouteErrorResponse(error)) {
    switch (error.status) {
      case HTTP_NOT_FOUND:
        return (
          <div role="alert">
            <h1>User Not Found</h1>
            <p>The user you're looking for doesn't exist.</p>
          </div>
        );
      case HTTP_UNAUTHORIZED:
        return (
          <div role="alert">
            <h1>Unauthorized</h1>
            <p>Please log in to view this page.</p>
          </div>
        );
      case HTTP_FORBIDDEN:
        return (
          <div role="alert">
            <h1>Access Denied</h1>
            <p>You don't have permission to view this page.</p>
          </div>
        );
      default:
        return (
          <div role="alert">
            <h1>{error.status} {error.statusText}</h1>
            <p>{error.data?.message || "An error occurred"}</p>
          </div>
        );
    }
  }

  // Unexpected errors
  if (error instanceof Error) {
    return (
      <div role="alert">
        <h1>Unexpected Error</h1>
        <p>{error.message}</p>
      </div>
    );
  }

  return (
    <div role="alert">
      <h1>Unknown Error</h1>
    </div>
  );
}
```

**Why good:** Route-level error isolation keeps rest of page functional, different UI for different error types, accessible error messages with role="alert", named constants for HTTP status codes

---

### Pattern 7: Meta Function for SEO

Export `meta` function to set page metadata dynamically.

```typescript
// app/routes/blog.$slug.tsx
import type { MetaFunction, LoaderFunctionArgs } from "@remix-run/node";
import { json } from "@remix-run/node";

const SITE_NAME = "My Blog";
const DEFAULT_DESCRIPTION = "A blog about web development";

export const meta: MetaFunction<typeof loader> = ({ data }) => {
  if (!data) {
    return [
      { title: "Post Not Found" },
      { name: "description", content: "The requested post could not be found" },
    ];
  }

  return [
    { title: `${data.post.title} | ${SITE_NAME}` },
    { name: "description", content: data.post.excerpt || DEFAULT_DESCRIPTION },
    { property: "og:title", content: data.post.title },
    { property: "og:description", content: data.post.excerpt },
    { property: "og:type", content: "article" },
    {
      tagName: "link",
      rel: "canonical",
      href: `https://example.com/blog/${data.post.slug}`,
    },
  ];
};

export async function loader({ params }: LoaderFunctionArgs) {
  const post = await db.post.findUnique({ where: { slug: params.slug } });
  if (!post) throw new Response("Not Found", { status: 404 });
  return json({ post });
}
```

**Why good:** Meta data derived from loader data, fallback for missing data, canonical URL prevents duplicate content issues, Open Graph tags for social sharing

---

### Pattern 8: Links Function for Assets

Export `links` function to add stylesheets and preload assets.

```typescript
// app/routes/dashboard.tsx
import type { LinksFunction } from "@remix-run/node";

import dashboardStyles from "~/styles/dashboard.css?url";
import chartStyles from "~/styles/charts.css?url";

export const links: LinksFunction = () => [
  { rel: "stylesheet", href: dashboardStyles },
  { rel: "stylesheet", href: chartStyles },
  {
    rel: "preload",
    href: "/fonts/inter.woff2",
    as: "font",
    type: "font/woff2",
    crossOrigin: "anonymous",
  },
];
```

**Why good:** Route-specific styles only load when needed, preload critical assets, crossOrigin required for font preloading

**Note:** For dynamic links based on loader data (like canonical URLs), use `meta` function with `tagName: "link"` instead.

---

### Pattern 9: Resource Routes

Routes without a default export become resource routes - useful for APIs and file downloads.

```typescript
// app/routes/api.users.ts (no default export = resource route)
import type { LoaderFunctionArgs } from "@remix-run/node";
import { json } from "@remix-run/node";

export async function loader({ request }: LoaderFunctionArgs) {
  const users = await db.user.findMany();
  return json({ users });
}

// app/routes/api.posts.$postId.like.ts
import type { ActionFunctionArgs } from "@remix-run/node";
import { json } from "@remix-run/node";

export async function action({ params, request }: ActionFunctionArgs) {
  const formData = await request.formData();
  const liked = formData.get("liked") === "true";

  await db.like.upsert({
    where: {
      postId_userId: {
        postId: params.postId!,
        userId: getCurrentUserId(request),
      },
    },
    create: {
      postId: params.postId!,
      userId: getCurrentUserId(request),
      liked,
    },
    update: { liked },
  });

  return json({ success: true });
}
```

**Why good:** Clean API endpoints without UI, can be called from useFetcher, follows REST conventions

---

### Pattern 10: Nested Routes and Layouts

Nested routes share parent layouts and load data in parallel.

```typescript
// app/routes/dashboard.tsx (parent layout)
import { Outlet, useLoaderData } from "@remix-run/react";
import type { LoaderFunctionArgs } from "@remix-run/node";
import { json } from "@remix-run/node";

export async function loader({ request }: LoaderFunctionArgs) {
  const user = await getUser(request);
  return json({ user });
}

export default function DashboardLayout() {
  const { user } = useLoaderData<typeof loader>();

  return (
    <div>
      <nav>
        <span>Welcome, {user.name}</span>
        {/* Navigation links */}
      </nav>
      <main>
        <Outlet /> {/* Child routes render here */}
      </main>
    </div>
  );
}

// app/routes/dashboard._index.tsx (child - renders at /dashboard)
import { useLoaderData } from "@remix-run/react";
import type { LoaderFunctionArgs } from "@remix-run/node";
import { json } from "@remix-run/node";

export async function loader({ request }: LoaderFunctionArgs) {
  // This loader runs IN PARALLEL with parent loader
  const stats = await getDashboardStats();
  return json({ stats });
}

export default function DashboardIndex() {
  const { stats } = useLoaderData<typeof loader>();
  return <StatsDisplay stats={stats} />;
}
```

**Why good:** Parent layout data (user) available to all children, child loaders run in parallel with parent (no waterfall), Outlet renders child routes maintaining layout structure

#### Opting Out of Layout Nesting

Use trailing underscore to share URL structure without UI nesting:

```typescript
// app/routes/dashboard_.settings.tsx
// URL: /dashboard/settings
// But NOT nested inside dashboard.tsx layout

export default function Settings() {
  return <FullPageSettingsForm />;
}
```

</patterns>

---

<integration>

## Integration Guide

**Works with:**

- **React**: Remix is built on React - use React components and hooks
- **Node.js/Deno adapters**: Server runtime is adapter-agnostic
- **Any database**: Loaders/actions can use any data source

**Styling Integration:**

Components accept `className` prop for styling flexibility. Remix doesn't prescribe a styling solution - use your preferred approach via the `className` prop.

**State Management:**

- Server state: Use loaders and actions (Remix handles caching and revalidation)
- Client state: Use React hooks (useState, useReducer) or external solutions via props

</integration>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md**

**(You MUST export loaders and actions as named exports from route modules only)**

**(You MUST use `useLoaderData<typeof loader>()` for type-safe data access in components)**

**(You MUST throw Response objects for expected errors - use ErrorBoundary for handling)**

**(You MUST wrap state mutations after await in `runInAction()` if combining with MobX)**

**(You MUST use `defer()` for non-critical data that can stream - keep critical data in direct returns)**

**Failure to follow these rules will break data loading, type safety, and error handling.**

</critical_reminders>
