---
name: nextjs-data-fetching
description: Provides Next.js App Router data fetching patterns including SWR and React Query integration, parallel data fetching, Incremental Static Regeneration (ISR), revalidation strategies, and error boundaries. Use when implementing data fetching in Next.js applications, choosing between server and client fetching, setting up caching strategies, or handling loading and error states.
allowed-tools: Read, Write, Edit, Bash
---

# Next.js Data Fetching

## Overview

This skill provides comprehensive patterns for data fetching in Next.js App Router applications. It covers server-side fetching, client-side libraries integration, caching strategies, error handling, and loading states.

## When to Use

Use this skill for:
- Implementing data fetching in Next.js App Router
- Choosing between Server Components and Client Components for data fetching
- Setting up SWR or React Query integration
- Implementing parallel data fetching patterns
- Configuring ISR and revalidation strategies
- Creating error boundaries for data fetching

## Instructions

### Server Component Fetching (Default)

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

Fetch multiple resources in parallel:

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

## Caching and Revalidation

### Time-based Revalidation (ISR)

```tsx
async function getPosts() {
  const res = await fetch('https://api.example.com/posts', {
    next: {
      revalidate: 60 // Revalidate every 60 seconds
    }
  });
  return res.json();
}
```

### On-Demand Revalidation

Use route handlers with `revalidateTag` or `revalidatePath`:

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

Tag cached data for selective revalidation:

```tsx
async function getPosts() {
  const res = await fetch('https://api.example.com/posts', {
    next: {
      tags: ['posts'],
      revalidate: 3600
    }
  });
  return res.json();
}
```

### Opt-out of Caching

```tsx
// Dynamic rendering (no caching)
async function getRealTimeData() {
  const res = await fetch('https://api.example.com/data', {
    cache: 'no-store'
  });
  return res.json();
}

// Or use dynamic export
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

Setup provider:

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

Use in components:

```tsx
'use client';

import { useQuery } from '@tanstack/react-query';

export function Posts() {
  const { data, error, isLoading } = useQuery({
    queryKey: ['posts'],
    queryFn: async () => {
      const res = await fetch('/api/posts');
      if (!res.ok) throw new Error('Failed to fetch');
      return res.json();
    },
  });

  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;

  return (
    <ul>
      {data.map((post: any) => (
        <li key={post.id}>{post.title}</li>
      ))}
    </ul>
  );
}
```

See [REACT-QUERY.md](references/REACT-QUERY.md) for advanced patterns.

## Error Boundaries

### Creating Error Boundaries

```tsx
// app/components/ErrorBoundary.tsx
'use client';

import { Component, ReactNode } from 'react';

interface Props {
  children: ReactNode;
  fallback: ReactNode;
}

interface State {
  hasError: boolean;
}

export class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(): State {
    return { hasError: true };
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    console.error('Error caught by boundary:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback;
    }

    return this.props.children;
  }
}
```

### Using Error Boundaries with Data Fetching

```tsx
// app/posts/page.tsx
import { ErrorBoundary } from '../components/ErrorBoundary';
import { Posts } from './Posts';
import { PostsError } from './PostsError';

export default function PostsPage() {
  return (
    <ErrorBoundary fallback={<PostsError />}>
      <Posts />
    </ErrorBoundary>
  );
}
```

### Error Boundary with Reset

```tsx
'use client';

import { Component, ReactNode } from 'react';

interface Props {
  children: ReactNode;
  fallback: (props: { reset: () => void }) => ReactNode;
}

interface State {
  hasError: boolean;
}

export class ErrorBoundary extends Component<Props, State> {
  state = { hasError: false };

  static getDerivedStateFromError(): State {
    return { hasError: true };
  }

  reset = () => {
    this.setState({ hasError: false });
  };

  render() {
    if (this.state.hasError) {
      return this.props.fallback({ reset: this.reset });
    }

    return this.props.children;
  }
}
```

## Server Actions for Mutations

```tsx
// app/actions/posts.ts
'use server';

import { revalidateTag } from 'next/cache';

export async function createPost(formData: FormData) {
  const title = formData.get('title') as string;
  const content = formData.get('content') as string;

  const response = await fetch('https://api.example.com/posts', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ title, content }),
  });

  if (!response.ok) {
    throw new Error('Failed to create post');
  }

  revalidateTag('posts');
  return response.json();
}
```

```tsx
// app/posts/CreatePostForm.tsx
'use client';

import { createPost } from '../actions/posts';

export function CreatePostForm() {
  return (
    <form action={createPost}>
      <input name="title" placeholder="Title" required />
      <textarea name="content" placeholder="Content" required />
      <button type="submit">Create Post</button>
    </form>
  );
}
```

## Loading States

### Loading.tsx Pattern

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
import { PopularPosts } from './PopularPosts';

export default function PostsPage() {
  return (
    <div>
      <h1>Posts</h1>

      <Suspense fallback={<PostsSkeleton />}>
        <PostsList />
      </Suspense>

      <Suspense fallback={<div>Loading popular...</div>}>
        <PopularPosts />
      </Suspense>
    </div>
  );
}
```

## Best Practices

1. **Default to Server Components** - Fetch data in Server Components when possible for better performance

2. **Use parallel fetching** - Use `Promise.all()` for independent data requests

3. **Choose appropriate caching**:
   - Static data: Long revalidation intervals or no revalidation
   - Dynamic data: Short revalidation or `cache: 'no-store'`
   - User-specific: Use dynamic rendering

4. **Handle errors gracefully** - Wrap client data fetching in error boundaries

5. **Use loading states** - Implement `loading.tsx` or Suspense boundaries

6. **Prefer SWR/React Query for**:
   - Real-time data
   - User interactions requiring immediate feedback
   - Data that needs background updates

7. **Use Server Actions for**:
   - Form submissions
   - Mutations that need to revalidate cache
   - Operations requiring server-side logic

## Constraints and Warnings

### Critical Constraints

- Server Components cannot use hooks like `useState`, `useEffect`, or data fetching libraries (SWR, React Query)
- Client Components must include the `'use client'` directive
- The `fetch` API in Next.js extends the standard Web API with Next.js-specific caching options
- Server Actions require the `'use server'` directive and can only be called from Client Components or form actions

### Common Pitfalls

1. **Fetching in loops**: Avoid fetching data inside loops in Server Components; use parallel fetching instead
2. **Cache poisoning**: Be careful with `cache: 'force-cache'` for user-specific data
3. **Memory leaks**: Always clean up subscriptions in Client Components when using real-time data
4. **Hydration mismatches**: Ensure server and client render the same initial state when using React Query hydration

## Decision Matrix

| Scenario | Solution |
|----------|----------|
| Static content, infrequent updates | Server Component + ISR |
| Dynamic content, user-specific | Server Component + `cache: 'no-store'` |
| Real-time updates | Client Component + SWR/React Query |
| User interactions | Client Component + mutation library |
| Mixed requirements | Server for initial, Client for updates |

## Examples

### Example 1: Basic Server Component with ISR

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

### Example 2: Parallel Data Fetching for Dashboard

**Input:** Build a dashboard showing user profile, stats, and recent activity.

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

**Output:** All three requests execute concurrently, reducing total load time.

### Example 3: Real-time Data with SWR

**Input:** Display live cryptocurrency prices that update every 5 seconds.

```tsx
// app/crypto/PriceTicker.tsx
'use client';

import useSWR from 'swr';

const fetcher = (url: string) => fetch(url).then(r => r.json());

export function PriceTicker() {
  const { data, error } = useSWR('/api/crypto/prices', fetcher, {
    refreshInterval: 5000,
    revalidateOnFocus: true,
  });

  if (error) return <div>Failed to load prices</div>;
  if (!data) return <div>Loading...</div>;

  return (
    <div className="ticker">
      <span>BTC: ${data.bitcoin}</span>
      <span>ETH: ${data.ethereum}</span>
    </div>
  );
}
```

**Output:** Component displays live-updating prices with automatic refresh.

### Example 4: Form Submission with Server Action

**Input:** Create a contact form that submits data and refreshes the cache.

```tsx
// app/actions/contact.ts
'use server';

import { revalidateTag } from 'next/cache';

export async function submitContact(formData: FormData) {
  const data = {
    name: formData.get('name'),
    email: formData.get('email'),
    message: formData.get('message'),
  };

  await fetch('https://api.example.com/contact', {
    method: 'POST',
    body: JSON.stringify(data),
  });

  revalidateTag('messages');
}
```

```tsx
// app/contact/page.tsx
import { submitContact } from '../actions/contact';

export default function ContactPage() {
  return (
    <form action={submitContact}>
      <input name="name" placeholder="Name" required />
      <input name="email" type="email" placeholder="Email" required />
      <textarea name="message" placeholder="Message" required />
      <button type="submit">Send</button>
    </form>
  );
}
```

**Output:** Form submits via Server Action, cache is invalidated on success.
