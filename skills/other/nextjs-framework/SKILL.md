---
name: nextjs-framework
description: "Build production-ready full-stack React applications with Next.js 15+ using App Router, Server Components, Server Actions, and advanced rendering strategies. Master file-based routing, data fetching patterns, caching, streaming, middleware, and deployment optimization. Use for: creating SEO-optimized web applications, implementing hybrid SSR/SSG/ISR rendering, building API routes and serverless functions, optimizing performance with automatic code splitting, integrating authentication and authorization, deploying to Vercel or custom infrastructure, and leveraging React Server Components for zero-bundle-size server rendering."
---

# Next.js Framework

Build scalable, production-ready full-stack React applications with Next.js 15+ App Router architecture.

## Overview

Next.js is a React framework for building full-stack web applications with built-in routing, rendering strategies (SSR, SSG, ISR), Server Components, Server Actions, and deployment optimization. The App Router (Next.js 13+) represents a fundamental shift toward server-first architecture with React Server Components as the default.

## App Router Architecture

### File-System Based Routing

| File | Purpose | Example |
|------|---------|--------|
| `page.tsx` | Route UI, publicly accessible | `app/dashboard/page.tsx` → `/dashboard` |
| `layout.tsx` | Shared UI wrapper, persists across routes | `app/dashboard/layout.tsx` |
| `loading.tsx` | Loading UI with Suspense | `app/dashboard/loading.tsx` |
| `error.tsx` | Error boundary UI | `app/dashboard/error.tsx` |
| `not-found.tsx` | 404 UI | `app/not-found.tsx` |
| `route.ts` | API endpoint (GET, POST, etc.) | `app/api/users/route.ts` |
| `template.tsx` | Re-renders on navigation (unlike layout) | `app/template.tsx` |
| `default.tsx` | Parallel route fallback | `app/@modal/default.tsx` |

### Dynamic Routes

```typescript
// app/blog/[slug]/page.tsx
interface PageProps {
  params: { slug: string };
  searchParams: { [key: string]: string | string[] | undefined };
}

export default async function BlogPost({ params, searchParams }: PageProps) {
  const post = await getPost(params.slug);
  return <article>{post.content}</article>;
}

// Generate static params for SSG
export async function generateStaticParams() {
  const posts = await getPosts();
  return posts.map(post => ({ slug: post.slug }));
}
```

### Route Groups and Organization

```
app/
  (marketing)/          # Route group (not in URL)
    page.tsx            # /
    about/page.tsx      # /about
  (shop)/
    products/page.tsx   # /products
  (auth)/
    login/page.tsx      # /login
```

## Server vs Client Components

### Server Components (Default)

**Benefits**: Zero client JS, direct backend access, automatic code splitting

```typescript
// app/users/page.tsx - Server Component by default
import { db } from '@/lib/database';

export default async function UsersPage() {
  const users = await db.user.findMany(); // Direct DB access
  
  return (
    <div>
      {users.map(user => (
        <UserCard key={user.id} user={user} />
      ))}
    </div>
  );
}
```

### Client Components

**Use when**: Interactivity, hooks, browser APIs needed

```typescript
// components/Counter.tsx
"use client";

import { useState } from 'react';

export function Counter() {
  const [count, setCount] = useState(0);
  return <button onClick={() => setCount(count + 1)}>{count}</button>;
}
```

### Composition Pattern

```typescript
// Server Component
export default async function Page() {
  const data = await fetchData();
  
  return (
    <ClientWrapper>
      {/* Server Component passed as children */}
      <ServerDataDisplay data={data} />
    </ClientWrapper>
  );
}
```

## Data Fetching Patterns

### Server Component Data Fetching

```typescript
// Parallel fetching
async function getData() {
  const [users, posts] = await Promise.all([
    fetch('https://api.example.com/users'),
    fetch('https://api.example.com/posts'),
  ]);
  return { users, posts };
}

// Sequential fetching (when dependent)
async function getUser(id: string) {
  const user = await fetch(`/api/users/${id}`);
  const posts = await fetch(`/api/users/${id}/posts`); // Waits for user
  return { user, posts };
}
```

### Fetch Caching Options

```typescript
// Cached by default (force-cache)
fetch('https://api.example.com/data');

// Opt out of caching
fetch('https://api.example.com/data', { cache: 'no-store' });

// Revalidate every 60 seconds (ISR)
fetch('https://api.example.com/data', { next: { revalidate: 60 } });

// Tag-based revalidation
fetch('https://api.example.com/data', { next: { tags: ['products'] } });
```

### Route Segment Config

```typescript
// app/dashboard/page.tsx
export const dynamic = 'force-dynamic'; // SSR (no caching)
export const revalidate = 3600; // ISR (revalidate hourly)
export const runtime = 'edge'; // Edge runtime

export default async function Dashboard() {
  const data = await fetchData();
  return <div>{data}</div>;
}
```

## Server Actions

Server Actions enable calling server code from Client Components without API routes.

### Defining Server Actions

```typescript
// app/actions.ts
"use server";

import { db } from '@/lib/database';
import { revalidatePath } from 'next/cache';

export async function createPost(formData: FormData) {
  const title = formData.get('title') as string;
  const content = formData.get('content') as string;
  
  await db.post.create({ data: { title, content } });
  
  revalidatePath('/posts');
  return { success: true };
}
```

### Using in Forms

```typescript
// components/PostForm.tsx
"use client";

import { createPost } from '@/app/actions';
import { useFormStatus } from 'react-dom';

function SubmitButton() {
  const { pending } = useFormStatus();
  return <button disabled={pending}>{pending ? 'Creating...' : 'Create'}</button>;
}

export function PostForm() {
  return (
    <form action={createPost}>
      <input name="title" required />
      <textarea name="content" required />
      <SubmitButton />
    </form>
  );
}
```

### Programmatic Invocation

```typescript
"use client";

import { useTransition } from 'react';
import { deletePost } from '@/app/actions';

export function DeleteButton({ postId }: { postId: string }) {
  const [isPending, startTransition] = useTransition();
  
  return (
    <button
      onClick={() => startTransition(() => deletePost(postId))}
      disabled={isPending}
    >
      {isPending ? 'Deleting...' : 'Delete'}
    </button>
  );
}
```

## Streaming and Suspense

### Streaming with loading.tsx

```typescript
// app/dashboard/loading.tsx
export default function Loading() {
  return <DashboardSkeleton />;
}

// app/dashboard/page.tsx
export default async function Dashboard() {
  const data = await fetchData(); // Streams while loading
  return <DashboardContent data={data} />;
}
```

### Granular Suspense Boundaries

```typescript
import { Suspense } from 'react';

export default function Page() {
  return (
    <div>
      <h1>Dashboard</h1>
      <Suspense fallback={<Skeleton />}>
        <SlowComponent />
      </Suspense>
      <Suspense fallback={<Skeleton />}>
        <AnotherSlowComponent />
      </Suspense>
    </div>
  );
}
```

## Caching and Revalidation

### Cache Layers

1. **Request Memoization**: Automatic deduplication of fetch requests
2. **Data Cache**: Persistent cache across requests and deployments
3. **Full Route Cache**: Pre-rendered HTML and RSC payload
4. **Router Cache**: Client-side cache of visited routes

### Revalidation Strategies

```typescript
// Time-based revalidation
export const revalidate = 3600; // 1 hour

// On-demand revalidation
import { revalidatePath, revalidateTag } from 'next/cache';

await revalidatePath('/posts');
await revalidateTag('products');
```

## Middleware

Run code before request completion for authentication, redirects, rewrites.

```typescript
// middleware.ts
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  const token = request.cookies.get('token');
  
  if (!token && request.nextUrl.pathname.startsWith('/dashboard')) {
    return NextResponse.redirect(new URL('/login', request.url));
  }
  
  return NextResponse.next();
}

export const config = {
  matcher: ['/dashboard/:path*', '/api/:path*'],
};
```

## Route Handlers (API Routes)

```typescript
// app/api/users/route.ts
import { NextRequest, NextResponse } from 'next/server';

export async function GET(request: NextRequest) {
  const users = await db.user.findMany();
  return NextResponse.json(users);
}

export async function POST(request: NextRequest) {
  const body = await request.json();
  const user = await db.user.create({ data: body });
  return NextResponse.json(user, { status: 201 });
}

// Dynamic routes
// app/api/users/[id]/route.ts
export async function GET(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  const user = await db.user.findUnique({ where: { id: params.id } });
  return NextResponse.json(user);
}
```

## Image Optimization

```typescript
import Image from 'next/image';

<Image
  src="/photo.jpg"
  alt="Photo"
  width={500}
  height={300}
  priority // Load immediately (above fold)
  placeholder="blur" // Show blur while loading
  blurDataURL="data:image/..." // Custom blur
/>

// Remote images (configure in next.config.js)
<Image
  src="https://i.ytimg.com/vi/sd8ggbUytkk/maxresdefault.jpg"
  alt="Photo"
  width={500}
  height={300}
  loader={({ src, width }) => `${src}?w=${width}`}
/>
```

## Metadata and SEO

### Static Metadata

```typescript
import { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'My App',
  description: 'App description',
  openGraph: {
    title: 'My App',
    description: 'App description',
    images: ['/og-image.jpg'],
  },
};
```

### Dynamic Metadata

```typescript
export async function generateMetadata({ params }): Promise<Metadata> {
  const post = await getPost(params.id);
  
  return {
    title: post.title,
    description: post.excerpt,
    openGraph: {
      images: [post.coverImage],
    },
  };
}
```

## Performance Optimization

### Code Splitting

```typescript
import dynamic from 'next/dynamic';

const DynamicComponent = dynamic(() => import('@/components/Heavy'), {
  loading: () => <Skeleton />,
  ssr: false, // Disable SSR for this component
});
```

### Font Optimization

```typescript
import { Inter, Roboto_Mono } from 'next/font/google';

const inter = Inter({ subsets: ['latin'] });
const robotoMono = Roboto_Mono({ subsets: ['latin'] });

export default function Layout({ children }) {
  return (
    <html className={inter.className}>
      <body>{children}</body>
    </html>
  );
}
```

## Deployment

### Vercel (Recommended)

```bash
npm install -g vercel
vercel
```

### Docker

```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["npm", "start"]
```

### Environment Variables

```bash
# .env.local
DATABASE_URL=postgresql://...
NEXT_PUBLIC_API_URL=https://api.example.com
```

## Using the Reference Files

### When to Read Each Reference

**`/references/app-router-patterns.md`** — Read when implementing complex routing scenarios, parallel routes, intercepting routes, or route groups.

**`/references/data-fetching-caching.md`** — Read when optimizing data fetching strategies, implementing ISR, or debugging cache behavior.

**`/references/server-actions-forms.md`** — Read when building forms with Server Actions, implementing mutations, or handling file uploads.

**`/references/deployment-optimization.md`** — Read when preparing for production deployment, optimizing bundle size, or configuring custom infrastructure.

**`/references/authentication-patterns.md`** — Read when implementing authentication with NextAuth.js, middleware-based auth, or session management.
