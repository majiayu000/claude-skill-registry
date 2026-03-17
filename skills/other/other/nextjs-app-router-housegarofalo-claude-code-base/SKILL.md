---
name: nextjs-app-router
description: Build production Next.js 14+ applications with App Router. Covers server/client components, routing, data fetching, caching, streaming, metadata, and middleware. Use for full-stack React apps, SSR, ISR, and edge deployments.
---

# Next.js App Router

Modern Next.js development with the App Router paradigm for production applications.

## Core Concepts

### Server vs Client Components

```tsx
// app/components/ServerComponent.tsx
// Server Components are the default - no "use client" directive
async function ServerComponent() {
  // Can directly access databases, file system, secrets
  const data = await db.query('SELECT * FROM users');

  return (
    <ul>
      {data.map(user => (
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
  );
}

// app/components/ClientComponent.tsx
'use client';

import { useState } from 'react';

export function ClientComponent() {
  // Client components for interactivity
  const [count, setCount] = useState(0);

  return (
    <button onClick={() => setCount(c => c + 1)}>
      Count: {count}
    </button>
  );
}
```

### Component Composition Pattern

```tsx
// app/dashboard/page.tsx
import { Suspense } from 'react';
import { ServerData } from './ServerData';
import { ClientInteraction } from './ClientInteraction';
import { Loading } from '@/components/Loading';

export default function DashboardPage() {
  return (
    <div className="dashboard">
      {/* Server component with streaming */}
      <Suspense fallback={<Loading />}>
        <ServerData />
      </Suspense>

      {/* Client component for interaction */}
      <ClientInteraction />
    </div>
  );
}
```

## File-Based Routing

### Route Structure

```
app/
├── layout.tsx          # Root layout (required)
├── page.tsx            # Home page (/)
├── loading.tsx         # Loading UI
├── error.tsx           # Error boundary
├── not-found.tsx       # 404 page
├── dashboard/
│   ├── layout.tsx      # Nested layout
│   ├── page.tsx        # /dashboard
│   ├── loading.tsx     # Dashboard loading
│   └── [id]/
│       └── page.tsx    # /dashboard/[id]
├── api/
│   └── users/
│       └── route.ts    # API route handler
└── (marketing)/        # Route group (no URL segment)
    ├── about/
    │   └── page.tsx    # /about
    └── contact/
        └── page.tsx    # /contact
```

### Dynamic Routes

```tsx
// app/blog/[slug]/page.tsx
interface PageProps {
  params: { slug: string };
  searchParams: { [key: string]: string | string[] | undefined };
}

export default async function BlogPost({ params, searchParams }: PageProps) {
  const post = await getPost(params.slug);

  return (
    <article>
      <h1>{post.title}</h1>
      <div dangerouslySetInnerHTML={{ __html: post.content }} />
    </article>
  );
}

// Generate static params for SSG
export async function generateStaticParams() {
  const posts = await getAllPosts();

  return posts.map((post) => ({
    slug: post.slug,
  }));
}
```

## Data Fetching

### Server Component Data Fetching

```tsx
// app/users/page.tsx
async function getUsers() {
  const res = await fetch('https://api.example.com/users', {
    // Cache options
    cache: 'force-cache',     // Default - cache indefinitely
    // cache: 'no-store',     // No caching
    next: {
      revalidate: 3600,       // Revalidate every hour
      tags: ['users'],        // Tag for on-demand revalidation
    },
  });

  if (!res.ok) throw new Error('Failed to fetch');
  return res.json();
}

export default async function UsersPage() {
  const users = await getUsers();

  return (
    <ul>
      {users.map(user => (
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
  );
}
```

### Parallel Data Fetching

```tsx
// app/dashboard/page.tsx
async function DashboardPage() {
  // Fetch in parallel - don't await each one sequentially
  const [users, posts, stats] = await Promise.all([
    getUsers(),
    getPosts(),
    getStats(),
  ]);

  return (
    <div>
      <UserList users={users} />
      <PostList posts={posts} />
      <StatsPanel stats={stats} />
    </div>
  );
}
```

### Streaming with Suspense

```tsx
// app/dashboard/page.tsx
import { Suspense } from 'react';

export default function Dashboard() {
  return (
    <div className="grid grid-cols-2 gap-4">
      {/* Each suspense boundary streams independently */}
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
```

## Server Actions

### Form Actions

```tsx
// app/actions.ts
'use server';

import { revalidatePath, revalidateTag } from 'next/cache';
import { redirect } from 'next/navigation';

export async function createUser(formData: FormData) {
  const name = formData.get('name') as string;
  const email = formData.get('email') as string;

  // Validate
  if (!name || !email) {
    return { error: 'Name and email required' };
  }

  // Create in database
  const user = await db.user.create({
    data: { name, email },
  });

  // Revalidate cache
  revalidatePath('/users');
  revalidateTag('users');

  // Redirect
  redirect(`/users/${user.id}`);
}

// app/users/new/page.tsx
import { createUser } from '@/app/actions';

export default function NewUserPage() {
  return (
    <form action={createUser}>
      <input name="name" placeholder="Name" required />
      <input name="email" type="email" placeholder="Email" required />
      <button type="submit">Create User</button>
    </form>
  );
}
```

## API Routes

### Route Handlers

```tsx
// app/api/users/route.ts
import { NextRequest, NextResponse } from 'next/server';

export async function GET(request: NextRequest) {
  const searchParams = request.nextUrl.searchParams;
  const limit = searchParams.get('limit') || '10';

  const users = await db.user.findMany({
    take: parseInt(limit),
  });

  return NextResponse.json(users);
}

export async function POST(request: NextRequest) {
  const body = await request.json();

  const user = await db.user.create({
    data: body,
  });

  return NextResponse.json(user, { status: 201 });
}
```

## Middleware

```tsx
// middleware.ts
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  // Check authentication
  const token = request.cookies.get('token')?.value;

  if (!token && request.nextUrl.pathname.startsWith('/dashboard')) {
    return NextResponse.redirect(new URL('/login', request.url));
  }

  // Add custom headers
  const response = NextResponse.next();
  response.headers.set('x-custom-header', 'value');

  return response;
}

export const config = {
  matcher: [
    // Match all paths except static files
    '/((?!_next/static|_next/image|favicon.ico).*)',
  ],
};
```

## Metadata & SEO

### Dynamic Metadata

```tsx
// app/blog/[slug]/page.tsx
import type { Metadata } from 'next';

interface Props {
  params: { slug: string };
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const post = await getPost(params.slug);

  return {
    title: post.title,
    description: post.excerpt,
    openGraph: {
      title: post.title,
      description: post.excerpt,
      images: [post.image],
      type: 'article',
      publishedTime: post.publishedAt,
    },
  };
}

export default async function BlogPost({ params }: Props) {
  const post = await getPost(params.slug);
  return <article>{/* Post content */}</article>;
}
```

## Best Practices

1. **Default to Server Components** - Only use 'use client' when needed
2. **Colocate Data Fetching** - Fetch data where it's used
3. **Use Streaming** - Wrap slow components in Suspense
4. **Parallel Fetching** - Use Promise.all for independent data
5. **Revalidate Strategically** - Use tags and paths for cache invalidation
6. **Handle Errors Gracefully** - Use error.tsx boundaries
7. **Optimize Images** - Always use next/image
8. **Type Everything** - Use TypeScript throughout

## When to Use

- Full-stack React applications
- SEO-critical websites
- E-commerce platforms
- Marketing sites with CMS
- Dashboards needing SSR
- Applications requiring edge deployment
