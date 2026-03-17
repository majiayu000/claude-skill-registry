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

### Catch-All Routes

```tsx
// app/docs/[...slug]/page.tsx
interface DocsPageProps {
  params: { slug: string[] };
}

export default function DocsPage({ params }: DocsPageProps) {
  // /docs/a/b/c -> params.slug = ['a', 'b', 'c']
  const path = params.slug.join('/');

  return <DocViewer path={path} />;
}
```

## Layouts

### Root Layout

```tsx
// app/layout.tsx
import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: {
    template: '%s | My App',
    default: 'My App',
  },
  description: 'Application description',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <header>
          <nav>{/* Navigation */}</nav>
        </header>
        <main>{children}</main>
        <footer>{/* Footer */}</footer>
      </body>
    </html>
  );
}
```

### Nested Layouts

```tsx
// app/dashboard/layout.tsx
import { Sidebar } from '@/components/Sidebar';

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="flex">
      <Sidebar />
      <div className="flex-1 p-6">{children}</div>
    </div>
  );
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

### Progressive Enhancement

```tsx
'use client';

import { useFormStatus, useFormState } from 'react-dom';
import { createUser } from '@/app/actions';

function SubmitButton() {
  const { pending } = useFormStatus();

  return (
    <button type="submit" disabled={pending}>
      {pending ? 'Creating...' : 'Create User'}
    </button>
  );
}

export function CreateUserForm() {
  const [state, formAction] = useFormState(createUser, null);

  return (
    <form action={formAction}>
      <input name="name" placeholder="Name" required />
      <input name="email" type="email" placeholder="Email" required />
      {state?.error && (
        <p className="text-red-500">{state.error}</p>
      )}
      <SubmitButton />
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

### Dynamic API Routes

```tsx
// app/api/users/[id]/route.ts
import { NextRequest, NextResponse } from 'next/server';

interface RouteParams {
  params: { id: string };
}

export async function GET(request: NextRequest, { params }: RouteParams) {
  const user = await db.user.findUnique({
    where: { id: params.id },
  });

  if (!user) {
    return NextResponse.json(
      { error: 'User not found' },
      { status: 404 }
    );
  }

  return NextResponse.json(user);
}

export async function DELETE(request: NextRequest, { params }: RouteParams) {
  await db.user.delete({
    where: { id: params.id },
  });

  return new NextResponse(null, { status: 204 });
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

### Static Metadata

```tsx
// app/about/page.tsx
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'About Us',
  description: 'Learn about our company',
  openGraph: {
    title: 'About Us',
    description: 'Learn about our company',
    images: ['/og-about.png'],
  },
};

export default function AboutPage() {
  return <div>About content</div>;
}
```

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

## Error Handling

### Error Boundaries

```tsx
// app/dashboard/error.tsx
'use client';

import { useEffect } from 'react';

interface ErrorProps {
  error: Error & { digest?: string };
  reset: () => void;
}

export default function Error({ error, reset }: ErrorProps) {
  useEffect(() => {
    // Log error to monitoring service
    console.error(error);
  }, [error]);

  return (
    <div className="flex flex-col items-center justify-center p-8">
      <h2 className="text-xl font-bold">Something went wrong!</h2>
      <p className="text-gray-600 mt-2">{error.message}</p>
      <button
        onClick={reset}
        className="mt-4 px-4 py-2 bg-blue-500 text-white rounded"
      >
        Try again
      </button>
    </div>
  );
}
```

### Not Found

```tsx
// app/blog/[slug]/page.tsx
import { notFound } from 'next/navigation';

export default async function BlogPost({ params }: Props) {
  const post = await getPost(params.slug);

  if (!post) {
    notFound();
  }

  return <article>{/* Post content */}</article>;
}

// app/blog/not-found.tsx
export default function NotFound() {
  return (
    <div className="text-center py-20">
      <h2 className="text-2xl font-bold">Post Not Found</h2>
      <p>Could not find the requested blog post.</p>
    </div>
  );
}
```

## Performance Optimization

### Image Optimization

```tsx
import Image from 'next/image';

function ProductImage({ src, alt }: { src: string; alt: string }) {
  return (
    <Image
      src={src}
      alt={alt}
      width={800}
      height={600}
      placeholder="blur"
      blurDataURL="data:image/jpeg;base64,..."
      priority={false}       // Set true for LCP images
      loading="lazy"
      sizes="(max-width: 768px) 100vw, 50vw"
    />
  );
}
```

### Font Optimization

```tsx
// app/layout.tsx
import { Inter, Roboto_Mono } from 'next/font/google';

const inter = Inter({
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-inter',
});

const robotoMono = Roboto_Mono({
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-roboto-mono',
});

export default function RootLayout({ children }) {
  return (
    <html lang="en" className={`${inter.variable} ${robotoMono.variable}`}>
      <body>{children}</body>
    </html>
  );
}
```

### Route Segment Config

```tsx
// app/blog/page.tsx

// Force static generation
export const dynamic = 'force-static';

// Or force dynamic rendering
// export const dynamic = 'force-dynamic';

// Revalidation period
export const revalidate = 3600; // 1 hour

// Runtime
export const runtime = 'edge'; // or 'nodejs'
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
