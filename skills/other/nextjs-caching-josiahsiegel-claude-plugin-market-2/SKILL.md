---
name: nextjs-caching
description: Complete Next.js caching system with 'use cache' directive (Next.js 16). PROACTIVELY activate for: (1) Understanding 4 caching layers (Request Memoization, Data Cache, Full Route Cache, Router Cache), (2) Cache Components with 'use cache' directive, (3) fetch() caching options, (4) cacheLife() and cacheTag() functions, (5) Time-based revalidation, (6) On-demand revalidation with revalidatePath/revalidateTag, (7) Static generation with generateStaticParams, (8) Cache debugging. Provides: 'use cache' patterns, Cache Components, caching strategies, revalidation patterns, ISR setup, cache headers. Ensures optimal performance with correct cache invalidation.
---

## Quick Reference

| Cache Layer | Location | Duration | Purpose |
|-------------|----------|----------|---------|
| Request Memoization | Server | Per-request | Dedupe same fetches |
| Data Cache | Server | Persistent | Store fetch results |
| Full Route Cache | Server | Persistent | Pre-rendered HTML/RSC |
| Router Cache | Client | Session | Client-side navigation |

### Next.js 16: 'use cache' Directive

| Directive | Scope | Use Case |
|-----------|-------|----------|
| `'use cache'` | Default cache | General caching |
| `'use cache: remote'` | CDN/Edge cache | Static shared content |
| `'use cache: private'` | Per-user cache | User-specific data |

| Cache Function | Code | Purpose |
|----------------|------|---------|
| `cacheLife('hours')` | Duration | Set cache lifetime |
| `cacheTag('posts')` | Tagging | Enable targeted revalidation |

### Fetch Options

| Fetch Option | Code | Effect |
|--------------|------|--------|
| Default | `fetch(url)` | Cached indefinitely |
| No cache | `{ cache: 'no-store' }` | Always fresh |
| Revalidate | `{ next: { revalidate: 60 } }` | Stale after 60s |
| Tags | `{ next: { tags: ['posts'] } }` | Tag for invalidation |

| Revalidation | Code | Use Case |
|--------------|------|----------|
| `revalidatePath('/posts')` | Path | After mutation |
| `revalidateTag('posts')` | Tag | Invalidate tagged data |
| `router.refresh()` | Client | Refresh current route |

## When to Use This Skill

Use for **caching and revalidation**:
- Understanding Next.js caching behavior
- Configuring fetch caching strategies
- Setting up Incremental Static Regeneration (ISR)
- Implementing on-demand revalidation
- Debugging cache issues

**Related skills:**
- For data fetching: see `nextjs-data-fetching`
- For Server Actions: see `nextjs-server-actions`
- For static generation: see `nextjs-deployment`

---

# Next.js Caching

## Caching Overview

Next.js has four caching mechanisms:

| Mechanism | What | Where | Purpose | Duration |
|-----------|------|-------|---------|----------|
| Request Memoization | Return values of functions | Server | Avoid duplicate requests in component tree | Per-request |
| Data Cache | Data | Server | Store data across requests and deployments | Persistent |
| Full Route Cache | HTML and RSC payload | Server | Reduce rendering cost | Persistent |
| Router Cache | RSC payload | Client | Reduce server requests on navigation | Session |

## Request Memoization

### Automatic Deduplication

```tsx
// This is automatically memoized - only one fetch happens
async function getUser(id: string) {
  const res = await fetch(`https://api.example.com/users/${id}`);
  return res.json();
}

// Layout uses getUser
export default async function Layout({ children }: { children: React.ReactNode }) {
  const user = await getUser('1'); // First call - fetches
  return <div>{children}</div>;
}

// Page also uses getUser
export default async function Page() {
  const user = await getUser('1'); // Second call - uses cached result
  return <div>{user.name}</div>;
}
```

### Manual Memoization with cache()

```tsx
import { cache } from 'react';

// For non-fetch functions like database queries
export const getUser = cache(async (id: string) => {
  return db.users.findUnique({ where: { id } });
});

// Both will use the same cached result
const user1 = await getUser('1');
const user2 = await getUser('1');
```

## Data Cache

### Caching with fetch()

```tsx
// Cached indefinitely (default)
const data = await fetch('https://api.example.com/data');

// Opt out of caching
const data = await fetch('https://api.example.com/data', {
  cache: 'no-store',
});

// Time-based revalidation
const data = await fetch('https://api.example.com/data', {
  next: { revalidate: 3600 }, // Revalidate every hour
});

// Tag-based caching
const data = await fetch('https://api.example.com/posts', {
  next: { tags: ['posts'] },
});
```

### unstable_cache for Non-Fetch

```tsx
import { unstable_cache } from 'next/cache';

const getCachedUser = unstable_cache(
  async (userId: string) => {
    return db.users.findUnique({ where: { id: userId } });
  },
  ['user'], // Cache key parts
  {
    revalidate: 3600, // 1 hour
    tags: ['users'],
  }
);

export default async function UserPage({ params }: { params: { id: string } }) {
  const user = await getCachedUser(params.id);
  return <div>{user?.name}</div>;
}
```

### Route Segment Config

```tsx
// Opt entire route out of caching
export const dynamic = 'force-dynamic';

// Set revalidation for entire route
export const revalidate = 60; // seconds

// Disable cache for all fetches in route
export const fetchCache = 'force-no-store';

// Force static generation
export const dynamic = 'force-static';
```

## Revalidation

### Time-Based Revalidation

```tsx
// Fetch with revalidation
const data = await fetch('https://api.example.com/data', {
  next: { revalidate: 60 }, // Revalidate after 60 seconds
});

// Route-level revalidation
export const revalidate = 60;
```

### On-Demand Revalidation

```tsx
// app/actions.ts
'use server';

import { revalidatePath, revalidateTag } from 'next/cache';

// Revalidate a specific path
export async function updatePost(id: string, data: FormData) {
  await db.posts.update({ where: { id }, data: { /* ... */ } });

  // Revalidate the specific post page
  revalidatePath(`/posts/${id}`);

  // Revalidate the posts list
  revalidatePath('/posts');
}

// Revalidate by tag
export async function createPost(data: FormData) {
  await db.posts.create({ data: { /* ... */ } });

  // All fetches with 'posts' tag will be revalidated
  revalidateTag('posts');
}
```

### Revalidation API Route

```tsx
// app/api/revalidate/route.ts
import { revalidatePath, revalidateTag } from 'next/cache';
import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  const secret = request.headers.get('x-revalidate-secret');

  if (secret !== process.env.REVALIDATION_SECRET) {
    return NextResponse.json({ error: 'Invalid secret' }, { status: 401 });
  }

  const body = await request.json();

  if (body.tag) {
    revalidateTag(body.tag);
  }

  if (body.path) {
    revalidatePath(body.path);
  }

  return NextResponse.json({ revalidated: true, now: Date.now() });
}
```

### Tag-Based Caching

```tsx
// Fetch with tags
async function getPosts() {
  const res = await fetch('https://api.example.com/posts', {
    next: { tags: ['posts', 'content'] },
  });
  return res.json();
}

async function getPost(id: string) {
  const res = await fetch(`https://api.example.com/posts/${id}`, {
    next: { tags: ['posts', `post-${id}`] },
  });
  return res.json();
}

// Revalidate all posts
revalidateTag('posts');

// Revalidate specific post
revalidateTag('post-123');

// Revalidate all content
revalidateTag('content');
```

## Full Route Cache

### Static Routes

```tsx
// Automatically cached at build time
export default async function StaticPage() {
  const data = await getData();
  return <div>{data}</div>;
}

// Force static
export const dynamic = 'force-static';
```

### Dynamic Routes with generateStaticParams

```tsx
// app/posts/[slug]/page.tsx
export async function generateStaticParams() {
  const posts = await db.posts.findMany({ select: { slug: true } });
  return posts.map((post) => ({ slug: post.slug }));
}

// Pages are pre-rendered at build time
export default async function PostPage({ params }: { params: { slug: string } }) {
  const post = await getPost(params.slug);
  return <article>{post.content}</article>;
}
```

### Opting Out

```tsx
// Dynamic route - not cached
export const dynamic = 'force-dynamic';

// Or use dynamic functions
import { headers, cookies } from 'next/headers';

export default async function Page() {
  const headersList = await headers(); // Makes route dynamic
  return <div>...</div>;
}
```

## Router Cache (Client-Side)

### Prefetching

```tsx
import Link from 'next/link';

// Prefetch on hover (default)
<Link href="/about">About</Link>

// Disable prefetching
<Link href="/dashboard" prefetch={false}>Dashboard</Link>
```

### Invalidating Router Cache

```tsx
'use client';

import { useRouter } from 'next/navigation';

export function RefreshButton() {
  const router = useRouter();

  const handleRefresh = () => {
    // Refresh current route and invalidate cache
    router.refresh();
  };

  return <button onClick={handleRefresh}>Refresh</button>;
}
```

### revalidatePath and Router Cache

```tsx
// Server Action
'use server';

import { revalidatePath } from 'next/cache';

export async function updateData() {
  // Update data in database
  await db.data.update({ /* ... */ });

  // This also clears the Router Cache for this path
  revalidatePath('/data');
}
```

## Cache Headers

### Route Handler Caching

```tsx
// app/api/data/route.ts
import { NextResponse } from 'next/server';

export async function GET() {
  const data = await fetchData();

  return NextResponse.json(data, {
    headers: {
      'Cache-Control': 'public, s-maxage=3600, stale-while-revalidate=86400',
    },
  });
}
```

### generateStaticParams with Dynamic

```tsx
// Generate some pages statically, allow others dynamically
export async function generateStaticParams() {
  // Only pre-render the top 100 posts
  const posts = await db.posts.findMany({ take: 100 });
  return posts.map((post) => ({ slug: post.slug }));
}

// Allow dynamic rendering for posts not in generateStaticParams
export const dynamicParams = true; // default

// Or 404 for unknown slugs
export const dynamicParams = false;
```

## Caching Strategies

### Stale-While-Revalidate Pattern

```tsx
// Serve cached content while revalidating in background
const data = await fetch('https://api.example.com/data', {
  next: { revalidate: 60 },
});

// First request after 60s: serves stale, triggers revalidation
// Subsequent requests: serve fresh data
```

### Cache-First Strategy

```tsx
// Cache indefinitely, revalidate on-demand
const data = await fetch('https://api.example.com/static-data');
// Use revalidateTag('static-data') when data changes
```

### Network-First Strategy

```tsx
// Always fetch fresh data
const data = await fetch('https://api.example.com/realtime', {
  cache: 'no-store',
});
```

## Debugging Cache

### Cache Status Headers

```tsx
// Enable cache debugging
// next.config.js
module.exports = {
  logging: {
    fetches: {
      fullUrl: true,
    },
  },
};
```

### Check Cache Hit/Miss

```tsx
// In development, check terminal for cache status
// HIT - served from cache
// MISS - fetched from origin
// STALE - served stale, revalidating
```

## Best Practices

| Practice | Description |
|----------|-------------|
| Use tags for related data | Group related fetches with tags |
| Revalidate minimally | Only revalidate what changed |
| Prefer static generation | Use generateStaticParams when possible |
| Cache database queries | Use unstable_cache for non-fetch |
| Set appropriate TTL | Balance freshness vs performance |
| Use ISR for content | Time-based revalidation for content sites |
