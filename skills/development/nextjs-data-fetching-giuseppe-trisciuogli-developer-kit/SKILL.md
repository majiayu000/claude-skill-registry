---
name: nextjs-data-fetching
description: Provides Next.js App Router data fetching patterns including SWR and React Query integration, parallel data fetching, Incremental Static Regeneration (ISR), revalidation strategies, and error boundaries. Use when implementing data fetching in Next.js applications, choosing between server and client fetching, setting up caching strategies, or handling loading and error states.
allowed-tools: Read, Write, Edit, Bash
---

# Next.js Data Fetching

## Overview

Provides patterns for data fetching in Next.js App Router: server-side fetching, SWR/React Query integration, ISR, revalidation, error boundaries, and loading states.

## When to Use

- Implementing data fetching in Next.js App Router
- Choosing between Server Components and Client Components
- Setting up SWR or React Query for client-side caching
- Configuring ISR, time-based, or on-demand revalidation
- Handling loading and error states
- Building forms with Server Actions

## Instructions

### Server Component Fetching

Fetch directly in async Server Components:

```tsx
async function getPosts() {
  const res = await fetch('https://api.example.com/posts');
  if (!res.ok) throw new Error('Failed to fetch posts');
  return res.json();
}

export default async function PostsPage() {
  const posts = await getPosts();
  return (
    <ul>
      {posts.map((post) => (
        <li key={post.id}>{post.title}</li>
      ))}
    </ul>
  );
}
```

### Parallel Data Fetching

Use `Promise.all()` for independent requests:

```tsx
async function getDashboardData() {
  const [user, posts, analytics] = await Promise.all([
    fetch('/api/user').then(r => r.json()),
    fetch('/api/posts').then(r => r.json()),
    fetch('/api/analytics').then(r => r.json()),
  ]);
  return { user, posts, analytics };
}

export default async function DashboardPage() {
  const { user, posts, analytics } = await getDashboardData();
  // Render dashboard
}
```

### Sequential Data Fetching (When Dependencies Exist)

```tsx
async function getUserPosts(userId: string) {
  const user = await fetch(`/api/users/${userId}`).then(r => r.json());
  const posts = await fetch(`/api/users/${userId}/posts`).then(r => r.json());
  return { user, posts };
}
```

### Time-based Revalidation (ISR)

```tsx
async function getPosts() {
  const res = await fetch('https://api.example.com/posts', {
    next: { revalidate: 60 } // Revalidate every 60 seconds
  });
  return res.json();
}
```

### On-Demand Revalidation

```tsx
// app/api/revalidate/route.ts
import { revalidateTag } from 'next/cache';
import { NextRequest } from 'next/server';

export async function POST(request: NextRequest) {
  const tag = request.nextUrl.searchParams.get('tag');
  if (tag) {
    revalidateTag(tag);
    return Response.json({ revalidated: true });
  }
  return Response.json({ revalidated: false }, { status: 400 });
}
```

Tag data for selective revalidation:

```tsx
async function getPosts() {
  const res = await fetch('https://api.example.com/posts', {
    next: { tags: ['posts'], revalidate: 3600 }
  });
  return res.json();
}
```

### Opt-out of Caching

```tsx
async function getRealTimeData() {
  const res = await fetch('https://api.example.com/data', {
    cache: 'no-store'
  });
  return res.json();
}

// Or:
export const dynamic = 'force-dynamic';
```

## Client-Side Data Fetching

### SWR Integration

Install: `npm install swr`

```tsx
'use client';

import useSWR from 'swr';

const fetcher = (url: string) => fetch(url).then(r => r.json());

export function Posts() {
  const { data, error, isLoading } = useSWR('/api/posts', fetcher, {
    refreshInterval: 5000,
    revalidateOnFocus: true,
  });

  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Failed to load posts</div>;

  return (
    <ul>
      {data.map((post: any) => (
        <li key={post.id}>{post.title}</li>
      ))}
    </ul>
  );
}
```

### React Query Integration

Install: `npm install @tanstack/react-query`

```tsx
// app/providers.tsx
'use client';

import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { useState } from 'react';

export function Providers({ children }: { children: React.ReactNode }) {
  const [queryClient] = useState(() => new QueryClient({
    defaultOptions: {
      queries: {
        staleTime: 60 * 1000,
        refetchOnWindowFocus: false,
      },
    },
  }));

  return (
    <QueryClientProvider client={queryClient}>
      {children}
    </QueryClientProvider>
  );
}
```

See [react-query.md](references/react-query.md) for mutations, optimistic updates, infinite queries, and advanced patterns.

## Error Boundaries

Wrap client-side data fetching in Error Boundaries to handle failures gracefully:

See [error-boundaries.md](references/error-boundaries.md) for full `ErrorBoundary` implementations (basic, with reset callback) and usage examples with data fetching.

## Server Actions

Use Server Actions for mutations with cache revalidation:

See [server-actions.md](references/server-actions.md) for complete examples including form validation with `useActionState`, error handling, and cache invalidation.

## Loading States

### loading.tsx Pattern

```tsx
// app/posts/loading.tsx
export default function PostsLoading() {
  return (
    <div className="space-y-4">
      {[...Array(5)].map((_, i) => (
        <div key={i} className="h-16 bg-gray-200 animate-pulse rounded" />
      ))}
    </div>
  );
}
```

### Suspense Boundaries

```tsx
// app/posts/page.tsx
import { Suspense } from 'react';
import { PostsList } from './PostsList';
import { PostsSkeleton } from './PostsSkeleton';

export default function PostsPage() {
  return (
    <div>
      <h1>Posts</h1>
      <Suspense fallback={<PostsSkeleton />}>
        <PostsList />
      </Suspense>
    </div>
  );
}
```

## Best Practices

1. **Default to Server Components** — Fetch in Server Components for better performance
2. **Use parallel fetching** — `Promise.all()` for independent requests to reduce latency
3. **Choose appropriate caching**:
   - Static data: long revalidation intervals
   - Dynamic data: short revalidation or `cache: 'no-store'`
   - User-specific data: use dynamic rendering
4. **Handle errors gracefully** — Wrap client data fetching in error boundaries
5. **Implement loading states** — Use `loading.tsx` or Suspense boundaries
6. **Prefer SWR/React Query for**: real-time data, user interactions, background updates
7. **Use Server Actions for**: form submissions, mutations requiring cache revalidation

## Constraints and Warnings

### Critical Constraints

- Server Components cannot use hooks (`useState`, `useEffect`) or client data fetching libraries
- Client Components must include the `'use client'` directive
- The `fetch` API in Next.js extends standard Web fetch with Next.js-specific caching options
- Server Actions require `'use server'` and can only be called from Client Components or form actions

### Common Pitfalls

1. **Fetching in loops** — Avoid sequential fetches in Server Components; use parallel fetching
2. **Cache poisoning** — Do not use `force-cache` for user-specific or personalized data
3. **Memory leaks** — Clean up subscriptions in Client Components when using real-time data
4. **Hydration mismatches** — Ensure server and client render the same initial state with React Query hydration

## Examples

### Example 1: Blog with ISR

**Input:** Create a blog page that fetches posts and updates every hour.

```tsx
// app/blog/page.tsx
async function getPosts() {
  const res = await fetch('https://api.example.com/posts', {
    next: { revalidate: 3600 }
  });
  return res.json();
}

export default async function BlogPage() {
  const posts = await getPosts();
  return (
    <main>
      <h1>Blog Posts</h1>
      {posts.map(post => (
        <article key={post.id}>
          <h2>{post.title}</h2>
          <p>{post.excerpt}</p>
        </article>
      ))}
    </main>
  );
}
```

**Output:** Page statically generated at build time, revalidated every hour.

### Example 2: Dashboard with Parallel Fetching

**Input:** Build a dashboard showing user profile, stats, and recent activity in parallel.

```tsx
// app/dashboard/page.tsx
async function getDashboardData() {
  const [user, stats, activity] = await Promise.all([
    fetch('/api/user').then(r => r.json()),
    fetch('/api/stats').then(r => r.json()),
    fetch('/api/activity').then(r => r.json()),
  ]);
  return { user, stats, activity };
}

export default async function DashboardPage() {
  const { user, stats, activity } = await getDashboardData();
  return (
    <div className="dashboard">
      <UserProfile user={user} />
      <StatsCards stats={stats} />
      <ActivityFeed activity={activity} />
    </div>
  );
}
```

**Output:** All three requests execute concurrently, minimizing total load time.
