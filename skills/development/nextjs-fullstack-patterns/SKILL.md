---
name: nextjs-fullstack-patterns
description: Build production Next.js applications with App Router patterns, server components, data fetching strategies, authentication, and deployment. Covers the full stack from database to UI. Triggers on Next.js development, React server components, App Router, or full-stack TypeScript requests.
license: MIT
---

# Next.js Full-Stack Patterns

Production patterns for modern Next.js applications.

## App Router Fundamentals

### File-Based Routing

```
app/
├── layout.tsx          # Root layout (required)
├── page.tsx            # Home page (/)
├── loading.tsx         # Loading UI
├── error.tsx           # Error boundary
├── not-found.tsx       # 404 page
├── globals.css         # Global styles
│
├── (marketing)/        # Route group (no URL impact)
│   ├── about/
│   │   └── page.tsx    # /about
│   └── blog/
│       └── page.tsx    # /blog
│
├── dashboard/
│   ├── layout.tsx      # Dashboard layout
│   ├── page.tsx        # /dashboard
│   └── settings/
│       └── page.tsx    # /dashboard/settings
│
├── api/
│   └── route.ts        # API route (/api)
│
└── [slug]/
    └── page.tsx        # Dynamic route
```

### Route Conventions

| File | Purpose |
|------|---------|
| `page.tsx` | Unique UI for route |
| `layout.tsx` | Shared UI, preserves state |
| `template.tsx` | Like layout but re-mounts |
| `loading.tsx` | Loading UI (Suspense) |
| `error.tsx` | Error boundary |
| `not-found.tsx` | 404 UI |
| `route.ts` | API endpoint |

---

## Server vs Client Components

### Default: Server Components

```tsx
// app/posts/page.tsx (Server Component by default)
async function PostsPage() {
  const posts = await db.posts.findMany(); // Direct DB access
  
  return (
    <ul>
      {posts.map(post => (
        <li key={post.id}>{post.title}</li>
      ))}
    </ul>
  );
}

export default PostsPage;
```

### Client Components

```tsx
'use client'; // Required directive

import { useState } from 'react';

export function Counter() {
  const [count, setCount] = useState(0);
  
  return (
    <button onClick={() => setCount(c => c + 1)}>
      Count: {count}
    </button>
  );
}
```

### When to Use Each

| Server Components | Client Components |
|-------------------|-------------------|
| Data fetching | Event handlers (onClick, etc.) |
| Access backend resources | useState, useEffect |
| Sensitive data (tokens, keys) | Browser APIs |
| Large dependencies | Interactivity |
| SEO-critical content | Real-time updates |

### Composition Pattern

```tsx
// Server Component with Client island
import { Counter } from './counter'; // Client component

async function Page() {
  const data = await fetchData(); // Server-side
  
  return (
    <div>
      <h1>{data.title}</h1>
      <Counter /> {/* Client island */}
    </div>
  );
}
```

---

## Data Fetching

### Server Component Fetching

```tsx
// Direct async/await in component
async function Page() {
  const data = await fetch('https://api.example.com/data', {
    cache: 'force-cache',     // Default: cache
    // cache: 'no-store',     // No cache (dynamic)
    // next: { revalidate: 60 } // ISR: revalidate every 60s
  });
  
  return <div>{data.title}</div>;
}
```

### Parallel Data Fetching

```tsx
async function Page() {
  // Parallel fetching (don't await sequentially)
  const [posts, comments] = await Promise.all([
    getPosts(),
    getComments(),
  ]);
  
  return (
    <>
      <Posts data={posts} />
      <Comments data={comments} />
    </>
  );
}
```

### Streaming with Suspense

```tsx
import { Suspense } from 'react';

async function Page() {
  return (
    <div>
      <h1>Dashboard</h1>
      
      {/* Streams in when ready */}
      <Suspense fallback={<Loading />}>
        <SlowComponent />
      </Suspense>
    </div>
  );
}
```

---

## Server Actions

### Form Actions

```tsx
// app/actions.ts
'use server';

import { revalidatePath } from 'next/cache';
import { redirect } from 'next/navigation';

export async function createPost(formData: FormData) {
  const title = formData.get('title') as string;
  
  await db.posts.create({ data: { title } });
  
  revalidatePath('/posts');
  redirect('/posts');
}
```

```tsx
// app/posts/new/page.tsx
import { createPost } from '../actions';

export default function NewPost() {
  return (
    <form action={createPost}>
      <input name="title" required />
      <button type="submit">Create</button>
    </form>
  );
}
```

### With useFormStatus

```tsx
'use client';

import { useFormStatus } from 'react-dom';

function SubmitButton() {
  const { pending } = useFormStatus();
  
  return (
    <button type="submit" disabled={pending}>
      {pending ? 'Saving...' : 'Save'}
    </button>
  );
}
```

### With useActionState

```tsx
'use client';

import { useActionState } from 'react';
import { createPost } from './actions';

export function PostForm() {
  const [state, action, pending] = useActionState(createPost, null);
  
  return (
    <form action={action}>
      <input name="title" />
      {state?.error && <p>{state.error}</p>}
      <button disabled={pending}>Create</button>
    </form>
  );
}
```

---

## API Routes

### Route Handlers

```typescript
// app/api/posts/route.ts
import { NextRequest, NextResponse } from 'next/server';

export async function GET(request: NextRequest) {
  const posts = await db.posts.findMany();
  return NextResponse.json(posts);
}

export async function POST(request: NextRequest) {
  const body = await request.json();
  const post = await db.posts.create({ data: body });
  return NextResponse.json(post, { status: 201 });
}
```

### Dynamic Route Handlers

```typescript
// app/api/posts/[id]/route.ts
import { NextRequest, NextResponse } from 'next/server';

export async function GET(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  const post = await db.posts.findUnique({ 
    where: { id: params.id } 
  });
  
  if (!post) {
    return NextResponse.json(
      { error: 'Not found' }, 
      { status: 404 }
    );
  }
  
  return NextResponse.json(post);
}
```

---

## Authentication Pattern

### Middleware Auth

```typescript
// middleware.ts
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  const token = request.cookies.get('token'); <!-- allow-secret -->
  
  if (!token && request.nextUrl.pathname.startsWith('/dashboard')) {
    return NextResponse.redirect(new URL('/login', request.url));
  }
  
  return NextResponse.next();
}

export const config = {
  matcher: ['/dashboard/:path*'],
};
```

### Auth Context Pattern

```tsx
// lib/auth.ts
import { cookies } from 'next/headers';
import { cache } from 'react';

export const getUser = cache(async () => {
  const token = cookies().get('token')?.value; <!-- allow-secret -->
  if (!token) return null;
  
  // Validate token, fetch user
  return await validateAndFetchUser(token);
});
```

```tsx
// app/dashboard/page.tsx
import { getUser } from '@/lib/auth';
import { redirect } from 'next/navigation';

export default async function Dashboard() {
  const user = await getUser();
  
  if (!user) {
    redirect('/login');
  }
  
  return <div>Welcome, {user.name}</div>;
}
```

---

## Database Patterns

### Prisma Setup

```typescript
// lib/db.ts
import { PrismaClient } from '@prisma/client';

const globalForPrisma = globalThis as unknown as {
  prisma: PrismaClient | undefined;
};

export const db = globalForPrisma.prisma ?? new PrismaClient();

if (process.env.NODE_ENV !== 'production') {
  globalForPrisma.prisma = db;
}
```

### Data Access Layer

```typescript
// lib/data/posts.ts
import { db } from '@/lib/db';
import { cache } from 'react';

export const getPosts = cache(async () => {
  return db.post.findMany({
    orderBy: { createdAt: 'desc' },
    include: { author: true },
  });
});

export const getPost = cache(async (id: string) => {
  return db.post.findUnique({
    where: { id },
    include: { author: true },
  });
});
```

---

## Error Handling

### Error Boundary

```tsx
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
      <h2>Something went wrong!</h2>
      <button onClick={() => reset()}>Try again</button>
    </div>
  );
}
```

### Not Found

```tsx
// app/posts/[id]/page.tsx
import { notFound } from 'next/navigation';

export default async function Post({ params }: { params: { id: string } }) {
  const post = await getPost(params.id);
  
  if (!post) {
    notFound();
  }
  
  return <article>{post.content}</article>;
}
```

---

## Metadata & SEO

### Static Metadata

```tsx
// app/about/page.tsx
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'About Us',
  description: 'Learn about our company',
};
```

### Dynamic Metadata

```tsx
// app/posts/[id]/page.tsx
import type { Metadata } from 'next';

export async function generateMetadata({ 
  params 
}: { 
  params: { id: string } 
}): Promise<Metadata> {
  const post = await getPost(params.id);
  
  return {
    title: post?.title,
    description: post?.excerpt,
  };
}
```

---

## Project Structure

```
├── app/                  # App Router
├── components/
│   ├── ui/              # Reusable UI components
│   └── features/        # Feature-specific components
├── lib/
│   ├── db.ts            # Database client
│   ├── auth.ts          # Auth utilities
│   └── utils.ts         # General utilities
├── actions/             # Server Actions
├── types/               # TypeScript types
├── hooks/               # Custom React hooks
└── public/              # Static assets
```

---

## References

- `references/deployment-checklist.md` - Production deployment
- `references/performance-patterns.md` - Optimization techniques
- `references/testing-patterns.md` - Testing Next.js apps
