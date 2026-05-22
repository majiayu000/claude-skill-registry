---
name: nextjs-data-fetching
description: Apply when fetching data in Next.js App Router: server components, caching strategies, revalidation, and streaming.
version: 1.0.0
tokens: ~700
confidence: high
sources:
  - https://nextjs.org/docs/app/building-your-application/data-fetching
  - https://nextjs.org/docs/app/building-your-application/caching
last_validated: 2025-01-10
next_review: 2025-01-24
tags: [nextjs, data-fetching, caching, ssr]
---

## When to Use

Apply when fetching data in Next.js App Router: server components, caching strategies, revalidation, and streaming.

## Patterns

### Pattern 1: Server Component Fetch
```typescript
// Source: https://nextjs.org/docs/app/building-your-application/data-fetching
// app/posts/page.tsx - Server Component (default)
async function PostsPage() {
  const posts = await fetch('https://api.example.com/posts', {
    next: { revalidate: 3600 }, // Revalidate every hour
  }).then((r) => r.json());

  return <PostList posts={posts} />;
}
```

### Pattern 2: Caching Strategies
```typescript
// Source: https://nextjs.org/docs/app/building-your-application/caching
// Force cache (default) - cached indefinitely
fetch(url); // or { cache: 'force-cache' }

// Revalidate time-based
fetch(url, { next: { revalidate: 60 } }); // 60 seconds

// Revalidate on-demand (via tag)
fetch(url, { next: { tags: ['posts'] } });
// Then: revalidateTag('posts') in server action

// No cache - always fresh
fetch(url, { cache: 'no-store' });
```

### Pattern 3: Parallel Data Fetching
```typescript
// Source: https://nextjs.org/docs/app/building-your-application/data-fetching/patterns
async function Dashboard() {
  // Parallel fetches - don't await sequentially
  const [user, posts, analytics] = await Promise.all([
    getUser(),
    getPosts(),
    getAnalytics(),
  ]);

  return (
    <>
      <UserCard user={user} />
      <PostList posts={posts} />
      <Analytics data={analytics} />
    </>
  );
}
```

### Pattern 4: Streaming with Suspense
```typescript
// Source: https://nextjs.org/docs/app/building-your-application/routing/loading-ui-and-streaming
import { Suspense } from 'react';

async function SlowComponent() {
  const data = await fetchSlowData(); // 3+ seconds
  return <Chart data={data} />;
}

export default function Page() {
  return (
    <>
      <h1>Dashboard</h1>
      <FastComponent /> {/* Renders immediately */}
      <Suspense fallback={<ChartSkeleton />}>
        <SlowComponent /> {/* Streams in when ready */}
      </Suspense>
    </>
  );
}
```

### Pattern 5: Server Actions for Mutations
```typescript
// Source: https://nextjs.org/docs/app/building-your-application/data-fetching/server-actions-and-mutations
'use server';

import { revalidatePath } from 'next/cache';

export async function createPost(formData: FormData) {
  const title = formData.get('title');
  await db.posts.create({ data: { title } });
  revalidatePath('/posts'); // Refresh the posts page cache
}

// In component:
<form action={createPost}>
  <input name="title" />
  <button type="submit">Create</button>
</form>
```

## Anti-Patterns

- **Sequential awaits** - Use Promise.all for independent fetches
- **Client fetch for initial data** - Fetch in server component instead
- **No revalidation strategy** - Always define cache behavior
- **Fetching in layout without need** - Layouts cache across navigations

## Verification Checklist

- [ ] Data fetched in server components (not client)
- [ ] Caching strategy defined (revalidate time or tags)
- [ ] Independent fetches run in parallel
- [ ] Slow data wrapped in Suspense
- [ ] Mutations use server actions with revalidation
