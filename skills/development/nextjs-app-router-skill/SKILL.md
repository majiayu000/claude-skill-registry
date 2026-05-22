---
name: "Next.js App Router & Server Components"
description: "Build Next.js 15 applications using App Router, Server Components, Client Components, Server Actions, and streaming. Apply when creating pages, handling data fetching, implementing routes, or optimizing performance."
allowed-tools: Read, Write, Edit, Bash
version: 1.0.0
---

# Next.js App Router & Server Components

Systematic Next.js 15 development with App Router, Server Components, and performance optimization.

## Overview

This Skill enforces:
- Server Components by default (use client only when needed)
- Proper data fetching patterns
- File-based routing with App Router
- Server Actions for mutations
- Streaming and Suspense boundaries
- Performance optimization
- Route handlers and middleware

Apply when building Next.js pages, implementing routes, or optimizing performance.

## Server vs Client Components

**Default: Server Components** (no directive needed)
**When needed: Client Components** (add `'use client'`)

### Decision Tree

```
Does component need browser APIs?
├─ YES → Client Component ('use client')
└─ NO → Server Component (default)

Does component need event handlers?
├─ YES → Client Component
└─ NO → Server Component

Does component need state or effects?
├─ YES → Client Component
└─ NO → Server Component

Does component fetch data?
├─ YES → Server Component (preferred)
└─ NO → Check other criteria
```

## Server Components (Default)

### Benefits

- Runs on server only
- Zero JavaScript sent to browser
- Direct database access
- Access to secrets
- Better SEO
- Faster initial load

### Example

```tsx
// app/users/page.tsx
// No 'use client' = Server Component
import { db } from '@/lib/db';

export default async function UsersPage() {
  // Direct database query (server-only)
  const users = await db.user.findMany();

  return (
    <div>
      <h1>Users</h1>
      <ul>
        {users.map(user => (
          <li key={user.id}>{user.name}</li>
        ))}
      </ul>
    </div>
  );
}
```

### Data Fetching in Server Components

```tsx
// ✅ GOOD: Async component with await
export default async function Page() {
  const data = await fetch('https://api.example.com/data', {
    next: { revalidate: 3600 }  // Cache for 1 hour
  });
  const result = await data.json();

  return <div>{result.title}</div>;
}

// ✅ GOOD: Parallel data fetching
export default async function Page() {
  const [users, posts] = await Promise.all([
    fetch('https://api.example.com/users').then(r => r.json()),
    fetch('https://api.example.com/posts').then(r => r.json())
  ]);

  return (
    <div>
      <Users data={users} />
      <Posts data={posts} />
    </div>
  );
}

// ❌ BAD: useEffect in Server Component
export default function Page() {
  useEffect(() => {
    // This doesn't work in Server Components!
    fetchData();
  }, []);
}
```

## Client Components

### When to Use

Add `'use client'` when you need:
- Event handlers (onClick, onChange, etc.)
- State (useState, useReducer)
- Effects (useEffect, useLayoutEffect)
- Browser APIs (localStorage, window, navigator)
- Custom hooks that use above
- Interactive UI (modals, dropdowns, forms with validation)

### Example

```tsx
// app/components/Counter.tsx
'use client';

import { useState } from 'react';

export function Counter() {
  const [count, setCount] = useState(0);

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => setCount(count + 1)}>
        Increment
      </button>
    </div>
  );
}
```

### Composing Server and Client

```tsx
// app/page.tsx (Server Component)
import { Counter } from './components/Counter';  // Client Component

export default async function Page() {
  const data = await fetch('https://api.example.com/stats');
  const stats = await data.json();

  return (
    <div>
      <h1>Dashboard</h1>
      <p>Server-rendered stats: {stats.total}</p>
      
      {/* Client Component embedded in Server Component */}
      <Counter />
    </div>
  );
}
```

## File-Based Routing

### App Router Structure

```
app/
├── layout.tsx          # Root layout (wraps all pages)
├── page.tsx            # Home page (/)
├── about/
│   └── page.tsx        # About page (/about)
├── blog/
│   ├── page.tsx        # Blog list (/blog)
│   └── [slug]/
│       └── page.tsx    # Blog post (/blog/post-1)
├── dashboard/
│   ├── layout.tsx      # Nested layout
│   ├── page.tsx        # Dashboard (/dashboard)
│   └── settings/
│       └── page.tsx    # Settings (/dashboard/settings)
└── api/
    └── users/
        └── route.ts    # API route (/api/users)
```

### Layouts

**Root Layout** (required):

```tsx
// app/layout.tsx
export default function RootLayout({
  children
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        <nav>Navigation</nav>
        {children}
        <footer>Footer</footer>
      </body>
    </html>
  );
}
```

**Nested Layout**:

```tsx
// app/dashboard/layout.tsx
export default function DashboardLayout({
  children
}: {
  children: React.ReactNode;
}) {
  return (
    <div>
      <aside>Sidebar</aside>
      <main>{children}</main>
    </div>
  );
}
```

### Dynamic Routes

```tsx
// app/blog/[slug]/page.tsx
export default async function BlogPost({
  params
}: {
  params: { slug: string };
}) {
  const post = await getPost(params.slug);

  return (
    <article>
      <h1>{post.title}</h1>
      <p>{post.content}</p>
    </article>
  );
}

// Generate static params at build time
export async function generateStaticParams() {
  const posts = await getAllPosts();

  return posts.map(post => ({
    slug: post.slug
  }));
}
```

### Catch-All Routes

```tsx
// app/docs/[...slug]/page.tsx
export default function DocsPage({
  params
}: {
  params: { slug: string[] };
}) {
  // /docs/a/b/c → params.slug = ['a', 'b', 'c']
  return <div>Docs: {params.slug.join('/')}</div>;
}
```

## Server Actions

### Form Mutations

```tsx
// app/actions.ts
'use server';

import { revalidatePath } from 'next/cache';

export async function createUser(formData: FormData) {
  const name = formData.get('name') as string;
  const email = formData.get('email') as string;

  // Validate
  if (!name || !email) {
    return { error: 'Name and email required' };
  }

  // Create user
  await db.user.create({
    data: { name, email }
  });

  // Revalidate cache
  revalidatePath('/users');

  return { success: true };
}
```

### Using Server Actions

```tsx
// app/users/page.tsx
import { createUser } from './actions';

export default function UsersPage() {
  return (
    <form action={createUser}>
      <input name="name" placeholder="Name" />
      <input name="email" type="email" placeholder="Email" />
      <button type="submit">Create User</button>
    </form>
  );
}
```

### With Client Component

```tsx
// app/components/UserForm.tsx
'use client';

import { createUser } from '../actions';
import { useFormState } from 'react-dom';

export function UserForm() {
  const [state, formAction] = useFormState(createUser, null);

  return (
    <form action={formAction}>
      <input name="name" placeholder="Name" />
      <input name="email" type="email" placeholder="Email" />
      
      {state?.error && <p className="error">{state.error}</p>}
      {state?.success && <p className="success">User created!</p>}
      
      <button type="submit">Create User</button>
    </form>
  );
}
```

## Streaming and Suspense

### Streaming with Suspense

```tsx
// app/dashboard/page.tsx
import { Suspense } from 'react';

async function SlowComponent() {
  await new Promise(resolve => setTimeout(resolve, 3000));
  return <div>Loaded after 3 seconds</div>;
}

export default function DashboardPage() {
  return (
    <div>
      <h1>Dashboard</h1>
      
      {/* Instant render */}
      <p>This loads immediately</p>
      
      {/* Streamed when ready */}
      <Suspense fallback={<div>Loading...</div>}>
        <SlowComponent />
      </Suspense>
    </div>
  );
}
```

### Loading States

```tsx
// app/dashboard/loading.tsx
export default function Loading() {
  return (
    <div>
      <p>Loading dashboard...</p>
    </div>
  );
}
```

## Data Fetching Patterns

### Caching Strategies

```tsx
// ✅ GOOD: Cached (default)
const data = await fetch('https://api.example.com/data');

// ✅ GOOD: Revalidate every 1 hour
const data = await fetch('https://api.example.com/data', {
  next: { revalidate: 3600 }
});

// ✅ GOOD: No caching (always fresh)
const data = await fetch('https://api.example.com/data', {
  cache: 'no-store'
});

// ✅ GOOD: Tagged cache (revalidate by tag)
const data = await fetch('https://api.example.com/data', {
  next: { tags: ['users'] }
});

// Revalidate specific tag
import { revalidateTag } from 'next/cache';
revalidateTag('users');
```

## Route Handlers (API Routes)

```tsx
// app/api/users/route.ts
import { NextResponse } from 'next/server';

export async function GET(request: Request) {
  const users = await db.user.findMany();
  return NextResponse.json(users);
}

export async function POST(request: Request) {
  const body = await request.json();
  
  const user = await db.user.create({
    data: body
  });
  
  return NextResponse.json(user, { status: 201 });
}
```

### Dynamic Route Handlers

```tsx
// app/api/users/[id]/route.ts
export async function GET(
  request: Request,
  { params }: { params: { id: string } }
) {
  const user = await db.user.findUnique({
    where: { id: params.id }
  });

  if (!user) {
    return NextResponse.json(
      { error: 'User not found' },
      { status: 404 }
    );
  }

  return NextResponse.json(user);
}
```

## Middleware

```tsx
// middleware.ts
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  // Check authentication
  const token = request.cookies.get('token');

  if (!token && request.nextUrl.pathname.startsWith('/dashboard')) {
    return NextResponse.redirect(new URL('/login', request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: ['/dashboard/:path*', '/admin/:path*']
};
```

## Anti-Patterns

```tsx
// ❌ BAD: Client Component doing data fetching
'use client';
export default function Page() {
  const [data, setData] = useState(null);
  
  useEffect(() => {
    fetch('/api/data').then(r => r.json()).then(setData);
  }, []);
}

// ✅ GOOD: Server Component fetches data
export default async function Page() {
  const data = await fetch('/api/data').then(r => r.json());
  return <div>{data}</div>;
}

// ❌ BAD: Entire page as Client Component
'use client';
export default function Page() {
  return <div>...</div>;
}

// ✅ GOOD: Only interactive parts as Client
export default function Page() {
  return (
    <div>
      <StaticContent />
      <InteractiveButton />  {/* This is 'use client' */}
    </div>
  );
}

// ❌ BAD: Passing Server Component to Client Component
<ClientComponent>
  <ServerComponent />
</ClientComponent>

// ✅ GOOD: Pass as children prop
<ClientComponent>
  {children}  {/* Server Component passed as children */}
</ClientComponent>
```

## Verification Before Deployment

- [ ] Server Components used by default
- [ ] `'use client'` only when necessary
- [ ] Data fetching in Server Components
- [ ] Server Actions for mutations
- [ ] Streaming with Suspense boundaries
- [ ] Caching strategy configured
- [ ] Middleware for auth/redirects
- [ ] Loading and error states
- [ ] Route handlers for APIs
- [ ] No unnecessary client bundles

## Integration with Project Standards

Enforces Next.js best practices:
- Performance optimization (streaming, caching)
- Security (Server Components hide secrets)
- Type safety (TypeScript throughout)
- No unnecessary client JavaScript

## Resources

- Next.js 15 Docs: https://nextjs.org/docs
- App Router: https://nextjs.org/docs/app
- Server Components: https://nextjs.org/docs/app/building-your-application/rendering/server-components
- Data Fetching: https://nextjs.org/docs/app/building-your-application/data-fetching
