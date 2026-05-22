---
name: nextjs-app-router-mastery
description: Next.js 14+ App Router patterns, server components, and data fetching
license: MIT
compatibility: nextjs 14+, react 18+
allowed-tools: read_file write_file apply_patch search_with_context run_command
---

# Next.js App Router Mastery

## Core Concepts

1. **Server Components by Default** - Components are server-rendered unless marked `'use client'`
2. **Streaming & Suspense** - Progressive rendering with loading states
3. **Parallel Routes** - Simultaneous route rendering
4. **Intercepting Routes** - Modal patterns without navigation

## File Conventions

```
app/
  layout.tsx          # Root layout (required)
  page.tsx            # Route UI
  loading.tsx         # Loading UI (Suspense boundary)
  error.tsx           # Error boundary
  not-found.tsx       # 404 UI
  route.ts            # API route handler
  template.tsx        # Re-renders on navigation
  default.tsx         # Parallel route fallback
```

## Data Fetching Patterns

### Server Component Fetching
```typescript
// app/posts/page.tsx - Server Component
async function PostsPage() {
  const posts = await fetchPosts(); // Direct fetch, no useEffect
  return <PostList posts={posts} />;
}
```

### Parallel Data Fetching
```typescript
async function Dashboard() {
  // Parallel fetches - don't await sequentially
  const [user, posts, analytics] = await Promise.all([
    fetchUser(),
    fetchPosts(),
    fetchAnalytics(),
  ]);
  return <DashboardView user={user} posts={posts} analytics={analytics} />;
}
```

### Streaming with Suspense
```typescript
export default function Page() {
  return (
    <div>
      <h1>Dashboard</h1>
      <Suspense fallback={<StatsSkeleton />}>
        <Stats /> {/* Async component */}
      </Suspense>
      <Suspense fallback={<ChartSkeleton />}>
        <Chart /> {/* Streams in when ready */}
      </Suspense>
    </div>
  );
}
```

## Server Actions

```typescript
// app/actions.ts
'use server';

import { revalidatePath } from 'next/cache';

export async function createPost(formData: FormData) {
  const title = formData.get('title') as string;
  await db.posts.create({ data: { title } });
  revalidatePath('/posts');
}
```

## Route Handlers

```typescript
// app/api/posts/route.ts
import { NextResponse } from 'next/server';

export async function GET(request: Request) {
  const posts = await fetchPosts();
  return NextResponse.json(posts);
}

export async function POST(request: Request) {
  const body = await request.json();
  const post = await createPost(body);
  return NextResponse.json(post, { status: 201 });
}
```

## Caching Strategies

```typescript
// Force dynamic rendering
export const dynamic = 'force-dynamic';

// Revalidate every 60 seconds
export const revalidate = 60;

// Static generation
export const dynamic = 'force-static';

// Per-fetch revalidation
fetch(url, { next: { revalidate: 3600 } });

// On-demand revalidation
revalidatePath('/posts');
revalidateTag('posts');
```

## Metadata

```typescript
// Static metadata
export const metadata: Metadata = {
  title: 'My App',
  description: 'App description',
};

// Dynamic metadata
export async function generateMetadata({ params }): Promise<Metadata> {
  const post = await fetchPost(params.id);
  return { title: post.title };
}
```

## Best Practices

1. Keep client components at the leaves of the tree
2. Pass serializable props from server to client components
3. Use `loading.tsx` for route-level loading states
4. Colocate data fetching with the component that uses it
5. Use route groups `(group)` for organization without affecting URL
