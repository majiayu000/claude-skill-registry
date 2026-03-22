---
name: nextjs
description: |
  Next.js 14+ framework guardrails, patterns, and best practices for AI-assisted development.
  Use when working with Next.js projects, or when the user mentions Next.js/Next.
  Provides App Router patterns, server components, data fetching, and deployment guidelines.
license: MIT
metadata:
  author: samuel
  version: "1.0"
  category: framework
  language: typescript
  extensions: ".jsx,.tsx"
---

# Next.js Framework Guide

> **Framework**: Next.js 14+ (App Router)
> **Language**: TypeScript/JavaScript
> **Use Cases**: Full-Stack Web Apps, SSR/SSG, E-commerce, Blogs, Dashboards

## Overview

Next.js is a React framework providing server-side rendering, static site generation, API routes, and full-stack development in a single codebase. Version 14+ uses the App Router as the default, built on React Server Components.

## Project Setup

```bash
# Create new Next.js app
npx create-next-app@latest my-app --typescript --tailwind --eslint --app

cd my-app
npm run dev
```

### Recommended Project Structure

```
my-app/
├── app/
│   ├── (auth)/                 # Route group (no URL segment)
│   │   ├── login/page.tsx
│   │   └── register/page.tsx
│   ├── dashboard/
│   │   ├── page.tsx            # /dashboard
│   │   ├── loading.tsx         # Loading UI
│   │   ├── error.tsx           # Error boundary
│   │   └── layout.tsx          # Dashboard layout
│   ├── api/
│   │   └── users/route.ts     # API route handler
│   ├── globals.css
│   ├── layout.tsx              # Root layout (required)
│   └── page.tsx                # Home page (/)
├── components/
│   ├── ui/                     # Reusable UI components
│   └── features/               # Feature-specific components
├── lib/
│   ├── db.ts                   # Database client
│   └── utils.ts                # Utility functions
├── hooks/                      # Custom React hooks
├── types/                      # TypeScript type definitions
├── public/                     # Static assets
├── middleware.ts               # Edge middleware
├── next.config.js
├── tailwind.config.ts
└── package.json
```

## Routing (App Router)

### File-Based Routing Conventions

| File            | Purpose                                      |
|-----------------|----------------------------------------------|
| `page.tsx`      | Route UI (makes segment publicly accessible) |
| `layout.tsx`    | Shared layout (wraps children, persists)     |
| `loading.tsx`   | Loading UI (Suspense boundary)               |
| `error.tsx`     | Error boundary (must be `'use client'`)      |
| `not-found.tsx` | 404 UI for this segment                      |
| `route.ts`      | API route handler (GET, POST, etc.)          |
| `template.tsx`  | Like layout but re-mounts on navigation      |
| `default.tsx`   | Fallback for parallel routes                 |

### Route Patterns

```
app/
├── page.tsx                    # /
├── about/page.tsx              # /about
├── blog/
│   ├── page.tsx                # /blog
│   └── [slug]/page.tsx         # /blog/:slug (dynamic)
├── shop/
│   └── [...categories]/page.tsx  # /shop/a/b/c (catch-all)
├── (marketing)/                # Route group (no URL impact)
│   ├── pricing/page.tsx        # /pricing
│   └── features/page.tsx       # /features
└── @modal/                     # Parallel route (named slot)
    └── login/page.tsx
```

### Page Component with Params

```tsx
// app/blog/[slug]/page.tsx
interface PageProps {
  params: { slug: string };
  searchParams: { [key: string]: string | string[] | undefined };
}

export default function BlogPost({ params, searchParams }: PageProps) {
  return <article><h1>Post: {params.slug}</h1></article>;
}

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const post = await getPost(params.slug);
  return { title: post.title, description: post.excerpt };
}
```

### Layouts

```tsx
// app/layout.tsx -- Root Layout (required, wraps entire app)
import { Inter } from 'next/font/google';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: { default: 'My App', template: '%s | My App' },
  description: 'My application',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className={inter.className}>{children}</body>
    </html>
  );
}
```

Nested layouts compose automatically. Dashboard layout wraps all `/dashboard/*` routes:

```tsx
// app/dashboard/layout.tsx
export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex">
      <Sidebar />
      <div className="flex-1">{children}</div>
    </div>
  );
}
```

## Server Components vs Client Components

### Decision Rule

| Need                                      | Component Type |
|-------------------------------------------|---------------|
| Fetch data, access backend resources      | Server (default) |
| Static rendering, SEO content             | Server        |
| Use hooks (useState, useEffect, etc.)     | Client        |
| Browser APIs (window, localStorage)       | Client        |
| Event handlers (onClick, onChange)         | Client        |
| Third-party client-only libraries         | Client        |

### Server Component (Default)

All components in the `app/` directory are Server Components by default. They run on the server only and can directly access databases, file systems, and secrets.

```tsx
// app/users/page.tsx -- Server Component (no directive needed)
import { db } from '@/lib/db';

export default async function UsersPage() {
  const users = await db.user.findMany();
  return (
    <ul>
      {users.map((user) => <li key={user.id}>{user.name}</li>)}
    </ul>
  );
}
```

### Client Component

Add `'use client'` at the top of the file. Push this directive as low in the tree as possible.

```tsx
// components/Counter.tsx
'use client';

import { useState } from 'react';

export function Counter() {
  const [count, setCount] = useState(0);
  return <button onClick={() => setCount(count + 1)}>Count: {count}</button>;
}
```

### Composition Pattern

Fetch data in Server Components, pass to Client Components as props:

```tsx
// app/dashboard/page.tsx (Server Component)
import { ClientSidebar } from '@/components/ClientSidebar';
import { db } from '@/lib/db';

export default async function Dashboard() {
  const stats = await db.stats.get();
  return (
    <div>
      <ClientSidebar initialStats={stats} />
      <DashboardContent stats={stats} />
    </div>
  );
}
```

## Data Fetching

### Server Component Fetch with Caching

```tsx
async function getProducts() {
  const res = await fetch('https://api.example.com/products', {
    next: { revalidate: 3600 }, // ISR: revalidate every hour
  });
  if (!res.ok) throw new Error('Failed to fetch products');
  return res.json();
}
```

### Fetch Caching Options

| Option                          | Behavior                          |
|---------------------------------|-----------------------------------|
| `{ cache: 'force-cache' }`     | Static (default for GET)          |
| `{ cache: 'no-store' }`        | Dynamic (no caching)              |
| `{ next: { revalidate: N } }`  | ISR (revalidate every N seconds)  |
| `{ next: { tags: ['posts'] } }`| Tag-based revalidation            |

### Parallel Fetching

Always fetch independent data in parallel with `Promise.all`:

```tsx
export default async function Dashboard({ params }: { params: { id: string } }) {
  const [user, orders] = await Promise.all([
    getUser(params.id),
    getOrders(params.id),
  ]);
  return <div><UserProfile user={user} /><OrderList orders={orders} /></div>;
}
```

### Streaming with Suspense

```tsx
import { Suspense } from 'react';

export default function Dashboard() {
  return (
    <div>
      <WelcomeMessage />
      <Suspense fallback={<StatsSkeleton />}>
        <Stats />
      </Suspense>
      <Suspense fallback={<OrdersSkeleton />}>
        <RecentOrders />
      </Suspense>
    </div>
  );
}
```

## Server Actions

Define mutations with `'use server'`. They run on the server and can be called from forms or client code.

```tsx
// app/actions.ts
'use server';

import { revalidatePath } from 'next/cache';
import { redirect } from 'next/navigation';
import { z } from 'zod';

const createPostSchema = z.object({
  title: z.string().min(1),
  content: z.string().min(10),
});

export async function createPost(formData: FormData) {
  const validated = createPostSchema.parse({
    title: formData.get('title'),
    content: formData.get('content'),
  });
  await db.post.create({ data: validated });
  revalidatePath('/posts');
  redirect(`/posts`);
}
```

Use in a form (no client JavaScript required for basic submissions):

```tsx
export default function NewPost() {
  return (
    <form action={createPost}>
      <input name="title" required />
      <textarea name="content" required />
      <button type="submit">Create</button>
    </form>
  );
}
```

## API Route Handlers

```tsx
// app/api/users/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { z } from 'zod';

const userSchema = z.object({
  name: z.string().min(2),
  email: z.string().email(),
});

export async function GET(request: NextRequest) {
  const page = parseInt(request.nextUrl.searchParams.get('page') || '1');
  const users = await db.user.findMany({ skip: (page - 1) * 10, take: 10 });
  return NextResponse.json(users);
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const validated = userSchema.parse(body);
    const user = await db.user.create({ data: validated });
    return NextResponse.json(user, { status: 201 });
  } catch (error) {
    if (error instanceof z.ZodError) {
      return NextResponse.json({ errors: error.errors }, { status: 400 });
    }
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}
```

## Middleware

Runs at the edge before every matched request. Use for auth checks, redirects, headers.

```tsx
// middleware.ts (project root)
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  const token = request.cookies.get('session')?.value;
  const isProtected = request.nextUrl.pathname.startsWith('/dashboard');

  if (isProtected && !token) {
    return NextResponse.redirect(new URL('/login', request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: ['/dashboard/:path*', '/api/:path*'],
};
```

## Error Handling

### Error Boundary (`error.tsx`)

```tsx
// app/dashboard/error.tsx
'use client';

export default function Error({ error, reset }: { error: Error; reset: () => void }) {
  return (
    <div>
      <h2>Something went wrong</h2>
      <button onClick={reset}>Try again</button>
    </div>
  );
}
```

### Not Found

```tsx
// app/not-found.tsx
import Link from 'next/link';

export default function NotFound() {
  return (
    <div>
      <h2>Not Found</h2>
      <Link href="/">Return Home</Link>
    </div>
  );
}
```

Trigger programmatically: `import { notFound } from 'next/navigation'; notFound();`

## Configuration

```js
// next.config.js
/** @type {import('next').NextConfig} */
const nextConfig = {
  images: {
    remotePatterns: [{ protocol: 'https', hostname: '**.example.com' }],
  },
  async redirects() {
    return [{ source: '/old', destination: '/new', permanent: true }];
  },
  async headers() {
    return [{
      source: '/api/:path*',
      headers: [{ key: 'Access-Control-Allow-Origin', value: '*' }],
    }];
  },
};
module.exports = nextConfig;
```

## Guardrails

- Use Server Components by default; add `'use client'` only when needed
- Push `'use client'` as low in the component tree as possible
- Colocate data fetching with the component that needs it
- Use `Promise.all` for independent parallel fetches
- Implement `loading.tsx` and `error.tsx` for every route segment
- Use Server Actions for mutations (not API routes for form submissions)
- Validate all inputs with schema validators (Zod) in Server Actions and API routes
- Use `next/image` for images and `next/font` for fonts (performance)
- Set proper metadata on every page for SEO
- Use Suspense boundaries to stream slow data
- Never import server-only modules in Client Components
- Never expose secrets or database access in Client Components

## Commands Reference

```bash
npm run dev          # Development server (http://localhost:3000)
npm run build        # Production build
npm run start        # Start production server
npm run lint         # ESLint check
npx tsc --noEmit     # TypeScript validation
npm test             # Run tests (Vitest/Jest)
```

## Advanced Topics

For detailed code examples, advanced patterns, testing strategies, performance optimization, caching strategies, and ISR/SSG/SSR details, see:

- [references/patterns.md](references/patterns.md) -- Authentication, advanced Server Actions, testing, performance, caching, rendering strategies, deployment

## External References

- [Next.js Documentation](https://nextjs.org/docs)
- [Next.js App Router](https://nextjs.org/docs/app)
- [NextAuth.js / Auth.js](https://authjs.dev/)
- [Vercel Deployment](https://vercel.com/docs)
- [React Server Components](https://react.dev/reference/rsc/server-components)
