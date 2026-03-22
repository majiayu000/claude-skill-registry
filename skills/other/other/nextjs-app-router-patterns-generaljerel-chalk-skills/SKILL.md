---
name: nextjs-app-router-patterns
description: Next.js App Router patterns — server vs client components, data fetching, caching, streaming, parallel routes, and error boundaries
author: chalk
version: "1.0.0"
metadata-version: "3"
allowed-tools: Read, Glob, Grep, Bash
argument-hint: "[file path or pattern question]"
read-only: false
destructive: false
idempotent: false
open-world: true
user-invocable: true
tags: nextjs, routing, patterns
---

# Next.js App Router Patterns

## Overview

Reference guide for idiomatic Next.js 14+ App Router patterns. Apply these when building pages, layouts, and data flows to fully leverage server components, streaming, and the caching system.

## Server vs Client Component Decision Tree

```
Does the component need...
├── Browser APIs (window, localStorage, navigator)?
│   └── YES → "use client"
├── Event listeners (onClick, onChange, onSubmit)?
│   └── YES → "use client"
├── useState, useEffect, useRef, or custom hooks?
│   └── YES → "use client"
├── Only data fetching and rendering?
│   └── YES → Server Component (default) ✓
├── Third-party library that uses hooks or browser APIs?
│   └── YES → "use client" wrapper component
└── Static content (no interactivity)?
    └── YES → Server Component (default) ✓
```

### Key Principle: Push "use client" Down

Keep the boundary as low as possible. Only the interactive leaf should be a client component.

```
app/
  dashboard/
    page.tsx          ← Server Component (fetches data)
    DashboardGrid.tsx ← Server Component (layout)
    MetricCard.tsx    ← Server Component (displays data)
    ChartWidget.tsx   ← "use client" (uses chart library with hooks)
    FilterBar.tsx     ← "use client" (has onChange handlers)
```

```tsx
// app/dashboard/page.tsx — Server Component
import { getMetrics } from "@/lib/data";
import { DashboardGrid } from "./DashboardGrid";
import { FilterBar } from "./FilterBar";

export default async function DashboardPage() {
  const metrics = await getMetrics(); // Direct DB/API call, no useEffect

  return (
    <div>
      <FilterBar /> {/* Client island for interactivity */}
      <DashboardGrid metrics={metrics} /> {/* Server component */}
    </div>
  );
}
```

## Data Fetching Patterns

### Server Components: Direct Async

```tsx
// app/users/page.tsx
import { db } from "@/lib/db";

export default async function UsersPage() {
  const users = await db.user.findMany({
    orderBy: { createdAt: "desc" },
  });

  return (
    <ul>
      {users.map((user) => (
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
  );
}
```

### Parallel Data Fetching

Fetch multiple resources in parallel with `Promise.all` to avoid waterfalls.

```tsx
export default async function ProfilePage({ params }: { params: { id: string } }) {
  // Parallel — both start immediately
  const [user, posts] = await Promise.all([
    getUser(params.id),
    getUserPosts(params.id),
  ]);

  return (
    <>
      <UserHeader user={user} />
      <PostList posts={posts} />
    </>
  );
}
```

### Data Fetching with Preloading

For components deeper in the tree, use the preload pattern.

```tsx
// lib/data.ts
import { cache } from "react";

export const getUser = cache(async (id: string) => {
  return db.user.findUnique({ where: { id } });
});

// Preload function — call early, consume later
export const preloadUser = (id: string) => {
  void getUser(id);
};

// app/user/[id]/page.tsx
import { getUser, preloadUser } from "@/lib/data";

export default async function UserPage({ params }: { params: { id: string } }) {
  preloadUser(params.id); // Start fetch early
  // ... other work ...
  const user = await getUser(params.id); // Deduplicated, may already be resolved
  return <Profile user={user} />;
}
```

## Caching Strategies

### Fetch Cache (Request Deduplication)

```tsx
// These two calls in the same render are automatically deduplicated
async function UserName({ id }: { id: string }) {
  const user = await fetch(`/api/users/${id}`); // cached
  return <span>{user.name}</span>;
}

async function UserAvatar({ id }: { id: string }) {
  const user = await fetch(`/api/users/${id}`); // same URL = deduplicated
  return <img src={user.avatar} />;
}
```

### Revalidation

```tsx
// Time-based revalidation
const data = await fetch(url, { next: { revalidate: 60 } }); // Revalidate every 60s

// On-demand revalidation (in a Server Action or Route Handler)
import { revalidatePath, revalidateTag } from "next/cache";

// By path
revalidatePath("/dashboard");

// By tag
const data = await fetch(url, { next: { tags: ["users"] } });
// Later:
revalidateTag("users");

// Opt out of caching
const data = await fetch(url, { cache: "no-store" });
```

### Route Segment Config

```tsx
// app/dashboard/layout.tsx
export const dynamic = "force-dynamic"; // Never cache this segment
export const revalidate = 60; // Revalidate every 60s
```

## Streaming with Suspense

Wrap slow parts in Suspense to stream the page progressively.

```tsx
// app/dashboard/page.tsx
import { Suspense } from "react";
import { SlowAnalytics } from "./SlowAnalytics";
import { QuickSummary } from "./QuickSummary";

export default function DashboardPage() {
  return (
    <div>
      {/* Renders immediately */}
      <QuickSummary />

      {/* Streams in when ready */}
      <Suspense fallback={<AnalyticsSkeleton />}>
        <SlowAnalytics />
      </Suspense>
    </div>
  );
}
```

### Loading States (file convention)

```
app/
  dashboard/
    page.tsx
    loading.tsx    ← Automatic Suspense boundary for the page
    error.tsx      ← Error boundary for the segment
    not-found.tsx  ← Shown when notFound() is called
```

```tsx
// app/dashboard/loading.tsx
export default function Loading() {
  return <DashboardSkeleton />;
}
```

## Parallel Routes

Render multiple pages in the same layout simultaneously.

```
app/
  @analytics/
    page.tsx       ← Analytics panel
    loading.tsx
  @feed/
    page.tsx       ← Feed panel
    loading.tsx
  layout.tsx       ← Receives both as props
```

```tsx
// app/layout.tsx
export default function Layout({
  children,
  analytics,
  feed,
}: {
  children: React.ReactNode;
  analytics: React.ReactNode;
  feed: React.ReactNode;
}) {
  return (
    <div className="grid grid-cols-3">
      <main className="col-span-2">{children}</main>
      <aside>
        {analytics}
        {feed}
      </aside>
    </div>
  );
}
```

## Intercepting Routes

Show a route in a modal while preserving the background page.

```
app/
  photos/
    [id]/
      page.tsx        ← Full photo page (direct navigation)
  @modal/
    (.)photos/[id]/
      page.tsx        ← Modal overlay (intercepted from feed)
    default.tsx       ← Returns null when no modal active
  layout.tsx
  page.tsx            ← Photo feed
```

```tsx
// app/@modal/(.)photos/[id]/page.tsx
import { Modal } from "@/components/Modal";
import { getPhoto } from "@/lib/data";

export default async function PhotoModal({ params }: { params: { id: string } }) {
  const photo = await getPhoto(params.id);
  return (
    <Modal>
      <img src={photo.url} alt={photo.alt} />
    </Modal>
  );
}
```

## Error Boundaries

```tsx
// app/dashboard/error.tsx
"use client"; // Error boundaries must be client components

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  return (
    <div role="alert">
      <h2>Something went wrong</h2>
      <p>{error.message}</p>
      <button onClick={reset}>Try again</button>
    </div>
  );
}
```

## Anti-patterns

### "use client" on Everything

Adding `"use client"` to every component defeats the purpose of RSC. You lose direct data access, increase bundle size, and add unnecessary hydration.

### Client-side Data Fetching When Server Would Work

```tsx
// BAD: useEffect + fetch in a page component
"use client";
export default function UsersPage() {
  const [users, setUsers] = useState([]);
  useEffect(() => { fetch("/api/users").then(/* ... */) }, []);
}

// GOOD: Server component with direct data access
export default async function UsersPage() {
  const users = await db.user.findMany();
  return <UserList users={users} />;
}
```

### Misunderstanding Caching

- `fetch` in server components is cached by default in production
- `POST` requests are NOT cached
- Route Handlers with `GET` are cached when using `export const dynamic = "auto"`
- Dynamic functions (`cookies()`, `headers()`, `searchParams`) opt the entire route out of static rendering

### Not Leveraging Layouts

Layouts persist across navigations and do not re-render. Put shared UI (nav, sidebar) in layouts, not in every page.
