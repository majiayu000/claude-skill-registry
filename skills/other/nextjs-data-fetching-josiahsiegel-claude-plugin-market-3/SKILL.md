---
name: nextjs-data-fetching
description: Complete Next.js data fetching system (Next.js 15.5/16). PROACTIVELY activate for: (1) Server Component data fetching, (2) Parallel and sequential fetching, (3) Streaming with Suspense, (4) Route Handlers (API routes), (5) Client-side fetching with SWR/TanStack Query, (6) generateStaticParams for static generation, (7) Revalidation strategies, (8) Error handling for data, (9) Async params/searchParams (Next.js 16), (10) Cache Components with 'use cache'. Provides: Fetch patterns, caching options, streaming UI, API route handlers, client fetching setup, async params pattern. Ensures optimal data loading with proper caching and error handling.
---

## Quick Reference

| Pattern | Code | Purpose |
|---------|------|---------|
| Server fetch | `await fetch(url)` | Cached by default |
| No cache | `{ cache: 'no-store' }` | Always fresh |
| Revalidate | `{ next: { revalidate: 60 } }` | Time-based refresh |
| Tags | `{ next: { tags: ['posts'] } }` | Tag-based invalidation |

| Config | Value | Effect |
|--------|-------|--------|
| `dynamic` | `'force-dynamic'` | Always SSR |
| `revalidate` | `60` | ISR every 60s |
| `fetchCache` | `'force-no-store'` | No caching |

| Client Library | Hook | Use Case |
|----------------|------|----------|
| SWR | `useSWR(key, fetcher)` | Simple client fetching |
| TanStack Query | `useQuery({ queryKey, queryFn })` | Complex state/mutations |

## When to Use This Skill

Use for **data loading patterns**:
- Fetching data in Server Components
- Setting up parallel data fetching with Promise.all
- Implementing streaming with Suspense boundaries
- Creating API routes with Route Handlers
- Client-side data fetching and mutations

**Related skills:**
- For caching strategies: see `nextjs-caching`
- For Server Actions (mutations): see `nextjs-server-actions`
- For App Router basics: see `nextjs-app-router`

---

# Next.js Data Fetching

## Server Components Data Fetching

### Basic Data Fetching

```tsx
// app/posts/page.tsx
async function getPosts() {
  const res = await fetch('https://api.example.com/posts');
  if (!res.ok) throw new Error('Failed to fetch posts');
  return res.json();
}

export default async function PostsPage() {
  const posts = await getPosts();

  return (
    <ul>
      {posts.map((post: Post) => (
        <li key={post.id}>{post.title}</li>
      ))}
    </ul>
  );
}
```

### Direct Database Access

```tsx
// app/users/page.tsx
import { db } from '@/lib/db';

export default async function UsersPage() {
  // Direct database query - no API needed
  const users = await db.users.findMany({
    orderBy: { createdAt: 'desc' },
    take: 10,
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

```tsx
// app/dashboard/page.tsx
async function getUser() {
  const res = await fetch('https://api.example.com/user');
  return res.json();
}

async function getPosts() {
  const res = await fetch('https://api.example.com/posts');
  return res.json();
}

async function getAnalytics() {
  const res = await fetch('https://api.example.com/analytics');
  return res.json();
}

export default async function DashboardPage() {
  // Fetch all data in parallel
  const [user, posts, analytics] = await Promise.all([
    getUser(),
    getPosts(),
    getAnalytics(),
  ]);

  return (
    <div>
      <UserCard user={user} />
      <PostsList posts={posts} />
      <AnalyticsChart data={analytics} />
    </div>
  );
}
```

### Sequential Data Fetching

```tsx
// When data depends on previous request
async function getUser(userId: string) {
  const res = await fetch(`https://api.example.com/users/${userId}`);
  return res.json();
}

async function getUserPosts(userId: string) {
  const res = await fetch(`https://api.example.com/users/${userId}/posts`);
  return res.json();
}

export default async function UserPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;

  // Sequential: user first, then posts
  const user = await getUser(id);
  const posts = await getUserPosts(user.id);

  return (
    <div>
      <h1>{user.name}</h1>
      <PostsList posts={posts} />
    </div>
  );
}
```

## Caching and Revalidation

### Caching Behavior

```tsx
// Cached by default (equivalent to cache: 'force-cache')
const data = await fetch('https://api.example.com/data');

// Opt out of caching
const data = await fetch('https://api.example.com/data', {
  cache: 'no-store',
});

// Time-based revalidation
const data = await fetch('https://api.example.com/data', {
  next: { revalidate: 3600 }, // Revalidate every hour
});

// Tag-based revalidation
const data = await fetch('https://api.example.com/posts', {
  next: { tags: ['posts'] },
});
```

### Route Segment Config

```tsx
// app/posts/page.tsx
export const dynamic = 'force-dynamic'; // Always dynamic
// or
export const revalidate = 60; // Revalidate every 60 seconds
// or
export const fetchCache = 'force-no-store'; // Don't cache any fetches
```

### Revalidating Data

```tsx
// app/actions.ts
'use server';

import { revalidatePath, revalidateTag } from 'next/cache';

export async function createPost(formData: FormData) {
  await db.posts.create({
    data: { title: formData.get('title') as string },
  });

  // Revalidate specific path
  revalidatePath('/posts');

  // Or revalidate by tag
  revalidateTag('posts');
}
```

## Streaming with Suspense

### Component-Level Streaming

```tsx
// app/dashboard/page.tsx
import { Suspense } from 'react';

async function SlowComponent() {
  const data = await fetch('https://api.example.com/slow-data');
  return <div>{/* render data */}</div>;
}

async function FastComponent() {
  const data = await fetch('https://api.example.com/fast-data');
  return <div>{/* render data */}</div>;
}

export default function DashboardPage() {
  return (
    <div>
      {/* Fast component renders immediately */}
      <Suspense fallback={<FastSkeleton />}>
        <FastComponent />
      </Suspense>

      {/* Slow component streams in when ready */}
      <Suspense fallback={<SlowSkeleton />}>
        <SlowComponent />
      </Suspense>
    </div>
  );
}
```

### Nested Suspense Boundaries

```tsx
// app/page.tsx
import { Suspense } from 'react';

export default function Page() {
  return (
    <Suspense fallback={<PageSkeleton />}>
      <Header />
      <Suspense fallback={<SidebarSkeleton />}>
        <Sidebar />
      </Suspense>
      <Suspense fallback={<ContentSkeleton />}>
        <MainContent />
        <Suspense fallback={<CommentsSkeleton />}>
          <Comments />
        </Suspense>
      </Suspense>
    </Suspense>
  );
}
```

## Client-Side Data Fetching

### SWR

```tsx
'use client';

import useSWR from 'swr';

const fetcher = (url: string) => fetch(url).then((res) => res.json());

export function UserProfile({ userId }: { userId: string }) {
  const { data, error, isLoading, mutate } = useSWR(
    `/api/users/${userId}`,
    fetcher
  );

  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error loading user</div>;

  return (
    <div>
      <h1>{data.name}</h1>
      <button onClick={() => mutate()}>Refresh</button>
    </div>
  );
}
```

### TanStack Query

```tsx
// providers/query-provider.tsx
'use client';

import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { useState } from 'react';

export function QueryProvider({ children }: { children: React.ReactNode }) {
  const [queryClient] = useState(
    () =>
      new QueryClient({
        defaultOptions: {
          queries: {
            staleTime: 60 * 1000,
          },
        },
      })
  );

  return (
    <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
  );
}
```

```tsx
// components/Posts.tsx
'use client';

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';

async function fetchPosts() {
  const res = await fetch('/api/posts');
  return res.json();
}

async function createPost(data: { title: string }) {
  const res = await fetch('/api/posts', {
    method: 'POST',
    body: JSON.stringify(data),
  });
  return res.json();
}

export function Posts() {
  const queryClient = useQueryClient();

  const { data: posts, isLoading } = useQuery({
    queryKey: ['posts'],
    queryFn: fetchPosts,
  });

  const mutation = useMutation({
    mutationFn: createPost,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['posts'] });
    },
  });

  if (isLoading) return <div>Loading...</div>;

  return (
    <div>
      <ul>
        {posts?.map((post: Post) => (
          <li key={post.id}>{post.title}</li>
        ))}
      </ul>
      <button onClick={() => mutation.mutate({ title: 'New Post' })}>
        Add Post
      </button>
    </div>
  );
}
```

## Route Handlers (API Routes)

### Basic Route Handler

```tsx
// app/api/posts/route.ts
import { NextResponse } from 'next/server';

export async function GET() {
  const posts = await db.posts.findMany();
  return NextResponse.json(posts);
}

export async function POST(request: Request) {
  const body = await request.json();
  const post = await db.posts.create({ data: body });
  return NextResponse.json(post, { status: 201 });
}
```

### Dynamic Route Handler

```tsx
// app/api/posts/[id]/route.ts
import { NextResponse } from 'next/server';

interface RouteParams {
  params: Promise<{ id: string }>;
}

export async function GET(request: Request, { params }: RouteParams) {
  const { id } = await params;
  const post = await db.posts.findUnique({ where: { id } });

  if (!post) {
    return NextResponse.json({ error: 'Not found' }, { status: 404 });
  }

  return NextResponse.json(post);
}

export async function PUT(request: Request, { params }: RouteParams) {
  const { id } = await params;
  const body = await request.json();
  const post = await db.posts.update({
    where: { id },
    data: body,
  });
  return NextResponse.json(post);
}

export async function DELETE(request: Request, { params }: RouteParams) {
  const { id } = await params;
  await db.posts.delete({ where: { id } });
  return new NextResponse(null, { status: 204 });
}
```

### Request Helpers

```tsx
// app/api/search/route.ts
import { NextResponse } from 'next/server';

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const query = searchParams.get('q');
  const page = parseInt(searchParams.get('page') || '1');

  const results = await search(query, page);

  return NextResponse.json(results);
}
```

### Headers and Cookies

```tsx
// app/api/auth/route.ts
import { NextResponse } from 'next/server';
import { cookies, headers } from 'next/headers';

export async function GET() {
  const cookieStore = await cookies();
  const token = cookieStore.get('token');

  const headersList = await headers();
  const authorization = headersList.get('authorization');

  // Set cookie in response
  const response = NextResponse.json({ success: true });
  response.cookies.set('session', 'value', {
    httpOnly: true,
    secure: true,
    sameSite: 'strict',
    maxAge: 60 * 60 * 24, // 1 day
  });

  return response;
}
```

## Static Generation

### generateStaticParams

```tsx
// app/posts/[slug]/page.tsx
export async function generateStaticParams() {
  const posts = await db.posts.findMany({ select: { slug: true } });

  return posts.map((post) => ({
    slug: post.slug,
  }));
}

export default async function PostPage({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  const post = await db.posts.findUnique({ where: { slug } });
  return <article>{post?.content}</article>;
}
```

### Dynamic Params Behavior

```tsx
// Allow dynamic paths beyond generateStaticParams
export const dynamicParams = true; // default

// 404 for paths not in generateStaticParams
export const dynamicParams = false;
```

## Error Handling

### Fetch Error Handling

```tsx
async function getData() {
  const res = await fetch('https://api.example.com/data');

  if (!res.ok) {
    throw new Error('Failed to fetch data');
  }

  return res.json();
}

export default async function Page() {
  try {
    const data = await getData();
    return <div>{/* render data */}</div>;
  } catch (error) {
    return <div>Error loading data</div>;
  }
}
```

### Using error.tsx

```tsx
// app/posts/error.tsx
'use client';

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  return (
    <div>
      <h2>Error loading posts</h2>
      <p>{error.message}</p>
      <button onClick={() => reset()}>Try again</button>
    </div>
  );
}
```

## Best Practices

| Practice | Description |
|----------|-------------|
| Fetch in Server Components | Avoid client-side fetching when possible |
| Use parallel fetching | Promise.all for independent data |
| Implement streaming | Suspense for progressive loading |
| Cache appropriately | Use revalidate or tags for fresh data |
| Handle errors | Use error.tsx boundaries |
| Type your data | Use TypeScript for API responses |
