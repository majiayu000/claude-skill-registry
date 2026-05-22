---
name: nextjs-app-router-expert
version: 1.0.0
category: frontend
tags: [nextjs, react, app-router, rsc, server-components, full-stack]
---

# Next.js App Router Expert

## Overview

Expert in Next.js 14/15 App Router architecture, React Server Components (RSC), Server Actions, and modern full-stack React development. Specializes in routing patterns, data fetching strategies, caching, streaming, and deployment optimization.

## When to Use

- Starting a new Next.js project with App Router
- Migrating from Pages Router to App Router
- Implementing complex routing patterns (parallel, intercepting routes)
- Optimizing data fetching with RSC and caching
- Setting up Server Actions for mutations
- Configuring middleware for auth/redirects
- Debugging hydration errors or RSC issues
- Deploying to Vercel, Cloudflare, or self-hosted

## Capabilities

### Routing Architecture
- File-based routing with `app/` directory
- Dynamic routes (`[slug]`, `[...catchAll]`, `[[...optional]]`)
- Route groups `(group)` for organization
- Parallel routes `@modal`, `@sidebar`
- Intercepting routes `(.)`, `(..)`, `(..)(..)`
- Loading and error boundaries per route segment

### React Server Components
- Server vs Client component boundaries
- `'use client'` directive placement
- Composition patterns (server wrapping client)
- Streaming with Suspense boundaries
- Progressive rendering strategies

### Data Fetching
- `fetch()` with automatic deduplication
- Caching strategies (`force-cache`, `no-store`, `revalidate`)
- `generateStaticParams()` for static generation
- Incremental Static Regeneration (ISR)
- On-demand revalidation with `revalidatePath()` / `revalidateTag()`

### Server Actions
- Form mutations with `'use server'`
- Optimistic updates with `useOptimistic`
- Progressive enhancement (works without JS)
- Error handling and validation
- Redirect after mutation

### Middleware & Edge
- `middleware.ts` for auth, redirects, rewrites
- Edge Runtime vs Node.js Runtime
- Geolocation and conditional routing
- A/B testing and feature flags

### Performance Optimization
- Image optimization with `next/image`
- Font optimization with `next/font`
- Script loading strategies
- Bundle analysis and code splitting
- Partial prerendering (PPR)

## Dependencies

Works well with:
- `react-performance-optimizer` - React-specific performance patterns
- `vercel-deployment` - Vercel deployment configuration
- `cloudflare-worker-dev` - Edge deployment patterns
- `postgresql-optimization` - Database queries for RSC

## Examples

### Basic Route Structure
```
app/
├── layout.tsx          # Root layout (required)
├── page.tsx            # Home page (/)
├── loading.tsx         # Loading UI
├── error.tsx           # Error boundary
├── not-found.tsx       # 404 page
├── blog/
│   ├── page.tsx        # /blog
│   └── [slug]/
│       ├── page.tsx    # /blog/:slug
│       └── loading.tsx # Per-route loading
└── (auth)/             # Route group (no URL impact)
    ├── login/
    │   └── page.tsx    # /login
    └── register/
        └── page.tsx    # /register
```

### Server Component with Data Fetching
```typescript
// app/posts/page.tsx
import { Suspense } from 'react';

async function getPosts() {
  const res = await fetch('https://api.example.com/posts', {
    next: { revalidate: 3600 }, // ISR: revalidate every hour
  });
  return res.json();
}

export default async function PostsPage() {
  const posts = await getPosts();

  return (
    <main>
      <h1>Blog Posts</h1>
      <Suspense fallback={<PostsSkeleton />}>
        <PostList posts={posts} />
      </Suspense>
    </main>
  );
}
```

### Server Action Form
```typescript
// app/contact/page.tsx
import { redirect } from 'next/navigation';
import { revalidatePath } from 'next/cache';

async function submitContact(formData: FormData) {
  'use server';

  const email = formData.get('email') as string;
  const message = formData.get('message') as string;

  // Validate
  if (!email || !message) {
    throw new Error('Email and message required');
  }

  // Save to database
  await db.contacts.create({ email, message });

  // Revalidate and redirect
  revalidatePath('/contact');
  redirect('/contact/success');
}

export default function ContactPage() {
  return (
    <form action={submitContact}>
      <input name="email" type="email" required />
      <textarea name="message" required />
      <button type="submit">Send</button>
    </form>
  );
}
```

### Parallel Routes (Modal Pattern)
```
app/
├── layout.tsx
├── page.tsx
├── @modal/
│   ├── default.tsx     # Empty state when no modal
│   └── (.)photo/[id]/
│       └── page.tsx    # Intercept /photo/[id] as modal
└── photo/[id]/
    └── page.tsx        # Full page when direct navigation
```

```typescript
// app/layout.tsx
export default function Layout({
  children,
  modal,
}: {
  children: React.ReactNode;
  modal: React.ReactNode;
}) {
  return (
    <>
      {children}
      {modal}
    </>
  );
}
```

### Middleware for Auth
```typescript
// middleware.ts
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  const token = request.cookies.get('auth-token');
  const isAuthPage = request.nextUrl.pathname.startsWith('/login');
  const isProtectedPage = request.nextUrl.pathname.startsWith('/dashboard');

  // Redirect authenticated users away from login
  if (isAuthPage && token) {
    return NextResponse.redirect(new URL('/dashboard', request.url));
  }

  // Redirect unauthenticated users to login
  if (isProtectedPage && !token) {
    return NextResponse.redirect(new URL('/login', request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: ['/dashboard/:path*', '/login'],
};
```

### Static Generation with Dynamic Params
```typescript
// app/blog/[slug]/page.tsx
import { notFound } from 'next/navigation';

export async function generateStaticParams() {
  const posts = await fetch('https://api.example.com/posts').then(r => r.json());

  return posts.map((post: { slug: string }) => ({
    slug: post.slug,
  }));
}

export async function generateMetadata({ params }: { params: { slug: string } }) {
  const post = await getPost(params.slug);

  return {
    title: post?.title ?? 'Post Not Found',
    description: post?.excerpt,
  };
}

export default async function PostPage({ params }: { params: { slug: string } }) {
  const post = await getPost(params.slug);

  if (!post) {
    notFound();
  }

  return (
    <article>
      <h1>{post.title}</h1>
      {/* NOTE: Always sanitize HTML content with DOMPurify before rendering */}
      <div>{post.content}</div>
    </article>
  );
}
```

### Streaming with Suspense
```typescript
// app/dashboard/page.tsx
import { Suspense } from 'react';

export default function DashboardPage() {
  return (
    <div className="grid grid-cols-2 gap-4">
      {/* These load in parallel and stream in as ready */}
      <Suspense fallback={<CardSkeleton />}>
        <RevenueCard />
      </Suspense>
      <Suspense fallback={<CardSkeleton />}>
        <UsersCard />
      </Suspense>
      <Suspense fallback={<TableSkeleton />}>
        <RecentOrders />
      </Suspense>
    </div>
  );
}

// Each component fetches its own data
async function RevenueCard() {
  const revenue = await getRevenue(); // Server-side fetch
  return <Card title="Revenue" value={revenue} />;
}
```

## Best Practices

1. **Server Components by default** - Only add `'use client'` when needed for interactivity
2. **Colocate data fetching** - Fetch data in the component that needs it
3. **Use Suspense boundaries** - Wrap async components for streaming
4. **Leverage caching** - Use `revalidate` and tags for efficient caching
5. **Progressive enhancement** - Server Actions work without JavaScript
6. **Route groups for organization** - Use `(folder)` to organize without affecting URLs
7. **Error boundaries per segment** - Add `error.tsx` to critical routes
8. **Metadata API** - Use `generateMetadata` for dynamic SEO
9. **Sanitize user content** - Always use DOMPurify or similar when rendering HTML

## Common Pitfalls

- **Hydration mismatches** - Server/client rendering differences (dates, random values)
- **Over-using 'use client'** - Pushing client boundary too high in the tree
- **Waterfall fetching** - Not parallelizing independent data fetches
- **Missing loading states** - Forgetting `loading.tsx` or Suspense boundaries
- **Stale data** - Not invalidating cache after mutations
- **Large client bundles** - Importing server-only code in client components
- **XSS vulnerabilities** - Rendering unsanitized HTML from user input
