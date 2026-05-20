---
name: nextjs-app-router
description: Complete Next.js App Router fundamentals system (Next.js 15.5/16). PROACTIVELY activate for: (1) App directory structure and conventions, (2) Layouts and templates, (3) Loading and error boundaries, (4) Route groups and organization, (5) Parallel routes setup, (6) Metadata and SEO, (7) Server vs Client Components, (8) Navigation and View Transitions, (9) Async params pattern (Next.js 16 breaking change). Provides: File conventions, layout nesting, streaming UI, error handling, metadata templates, View Transitions API. Ensures correct App Router architecture with proper component boundaries.
---

## Quick Reference

| Convention | File | Purpose |
|------------|------|---------|
| Page | `page.tsx` | Route UI (required for route) |
| Layout | `layout.tsx` | Shared UI (persists across navigations) |
| Loading | `loading.tsx` | Loading UI with Suspense |
| Error | `error.tsx` | Error boundary (must be 'use client') |
| Not Found | `not-found.tsx` | 404 UI |
| Template | `template.tsx` | Re-renders on navigation |

| Pattern | Syntax | Example |
|---------|--------|---------|
| Dynamic Route | `[slug]` | `/blog/[slug]/page.tsx` |
| Catch-all | `[...slug]` | `/docs/[...slug]/page.tsx` |
| Optional Catch-all | `[[...slug]]` | `/shop/[[...slug]]/page.tsx` |
| Route Group | `(name)` | `/(marketing)/about/page.tsx` |
| Parallel Route | `@slot` | `/@analytics/page.tsx` |

## When to Use This Skill

Use for **App Router fundamentals**:
- Setting up new Next.js 15 projects with App Router
- Understanding file-based routing conventions
- Creating layouts that persist across navigation
- Implementing loading states and error boundaries
- Organizing routes with groups

**Related skills:**
- For data fetching: see `nextjs-data-fetching`
- For advanced routing: see `nextjs-routing-advanced`
- For caching strategies: see `nextjs-caching`

---

# Next.js App Router Fundamentals

## Project Structure

### App Directory

```
app/
├── layout.tsx              # Root layout (required)
├── page.tsx                # Home page (/)
├── loading.tsx             # Loading UI
├── error.tsx               # Error boundary
├── not-found.tsx           # 404 page
├── global-error.tsx        # Global error boundary
├── template.tsx            # Re-renders on navigation
│
├── (marketing)/            # Route group (no URL impact)
│   ├── about/
│   │   └── page.tsx        # /about
│   └── contact/
│       └── page.tsx        # /contact
│
├── dashboard/
│   ├── layout.tsx          # Dashboard layout
│   ├── page.tsx            # /dashboard
│   ├── loading.tsx         # Dashboard loading
│   ├── @analytics/         # Parallel route
│   │   └── page.tsx
│   ├── @team/              # Parallel route
│   │   └── page.tsx
│   └── settings/
│       └── page.tsx        # /dashboard/settings
│
├── blog/
│   ├── page.tsx            # /blog
│   └── [slug]/             # Dynamic route
│       ├── page.tsx        # /blog/:slug
│       └── opengraph-image.tsx
│
├── products/
│   └── [...slug]/          # Catch-all route
│       └── page.tsx        # /products/*
│
├── shop/
│   └── [[...slug]]/        # Optional catch-all
│       └── page.tsx        # /shop or /shop/*
│
└── api/
    └── users/
        └── route.ts        # API route handler
```

## Layouts

### Root Layout (Required)

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
  description: 'My application description',
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

### Nested Layout

```tsx
// app/dashboard/layout.tsx
import { Sidebar } from '@/components/sidebar';

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="dashboard">
      <Sidebar />
      <div className="dashboard-content">{children}</div>
    </div>
  );
}
```

### Layout with Parallel Routes

```tsx
// app/dashboard/layout.tsx
export default function DashboardLayout({
  children,
  analytics,
  team,
}: {
  children: React.ReactNode;
  analytics: React.ReactNode;
  team: React.ReactNode;
}) {
  return (
    <div className="dashboard">
      <div className="main">{children}</div>
      <div className="sidebar">
        {analytics}
        {team}
      </div>
    </div>
  );
}
```

## Pages

### Basic Page

```tsx
// app/page.tsx
export default function HomePage() {
  return (
    <div>
      <h1>Welcome to My App</h1>
      <p>This is the home page.</p>
    </div>
  );
}
```

### Async Server Component Page

```tsx
// app/posts/page.tsx
import { db } from '@/lib/db';

async function getPosts() {
  return db.posts.findMany({
    orderBy: { createdAt: 'desc' },
  });
}

export default async function PostsPage() {
  const posts = await getPosts();

  return (
    <div>
      <h1>Blog Posts</h1>
      <ul>
        {posts.map((post) => (
          <li key={post.id}>
            <a href={`/posts/${post.slug}`}>{post.title}</a>
          </li>
        ))}
      </ul>
    </div>
  );
}
```

### Dynamic Route Page

```tsx
// app/posts/[slug]/page.tsx
import { notFound } from 'next/navigation';
import { db } from '@/lib/db';

interface PageProps {
  params: Promise<{ slug: string }>;
}

export async function generateMetadata({ params }: PageProps) {
  const { slug } = await params;
  const post = await db.posts.findUnique({ where: { slug } });

  if (!post) {
    return { title: 'Post Not Found' };
  }

  return {
    title: post.title,
    description: post.excerpt,
  };
}

export async function generateStaticParams() {
  const posts = await db.posts.findMany({ select: { slug: true } });
  return posts.map((post) => ({ slug: post.slug }));
}

export default async function PostPage({ params }: PageProps) {
  const { slug } = await params;
  const post = await db.posts.findUnique({ where: { slug } });

  if (!post) {
    notFound();
  }

  return (
    <article>
      <h1>{post.title}</h1>
      <div dangerouslySetInnerHTML={{ __html: post.content }} />
    </article>
  );
}
```

## Loading UI

### Loading Component

```tsx
// app/dashboard/loading.tsx
export default function Loading() {
  return (
    <div className="loading-container">
      <div className="spinner" />
      <p>Loading dashboard...</p>
    </div>
  );
}
```

### Skeleton Loading

```tsx
// app/posts/loading.tsx
export default function PostsLoading() {
  return (
    <div className="posts-skeleton">
      {Array.from({ length: 5 }).map((_, i) => (
        <div key={i} className="post-skeleton">
          <div className="skeleton-title" />
          <div className="skeleton-excerpt" />
        </div>
      ))}
    </div>
  );
}
```

### Streaming with Suspense

```tsx
// app/dashboard/page.tsx
import { Suspense } from 'react';
import { Analytics } from './analytics';
import { RecentSales } from './recent-sales';

export default function DashboardPage() {
  return (
    <div>
      <h1>Dashboard</h1>

      <Suspense fallback={<AnalyticsSkeleton />}>
        <Analytics />
      </Suspense>

      <Suspense fallback={<SalesSkeleton />}>
        <RecentSales />
      </Suspense>
    </div>
  );
}
```

## Error Handling

### Error Boundary

```tsx
// app/dashboard/error.tsx
'use client';

import { useEffect } from 'react';

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    console.error(error);
  }, [error]);

  return (
    <div className="error-container">
      <h2>Something went wrong!</h2>
      <p>{error.message}</p>
      <button onClick={() => reset()}>Try again</button>
    </div>
  );
}
```

### Global Error Boundary

```tsx
// app/global-error.tsx
'use client';

export default function GlobalError({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  return (
    <html>
      <body>
        <h2>Something went wrong!</h2>
        <button onClick={() => reset()}>Try again</button>
      </body>
    </html>
  );
}
```

### Not Found Page

```tsx
// app/not-found.tsx
import Link from 'next/link';

export default function NotFound() {
  return (
    <div className="not-found">
      <h2>Page Not Found</h2>
      <p>Could not find the requested resource.</p>
      <Link href="/">Return Home</Link>
    </div>
  );
}
```

### Triggering Not Found

```tsx
// app/posts/[slug]/page.tsx
import { notFound } from 'next/navigation';

export default async function PostPage({ params }: PageProps) {
  const { slug } = await params;
  const post = await getPost(slug);

  if (!post) {
    notFound();
  }

  return <article>{/* ... */}</article>;
}
```

## Metadata

### Static Metadata

```tsx
// app/about/page.tsx
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'About Us',
  description: 'Learn more about our company',
  openGraph: {
    title: 'About Us',
    description: 'Learn more about our company',
    images: ['/og-about.jpg'],
  },
};

export default function AboutPage() {
  return <div>About content</div>;
}
```

### Dynamic Metadata

```tsx
// app/products/[id]/page.tsx
import type { Metadata, ResolvingMetadata } from 'next';

interface PageProps {
  params: Promise<{ id: string }>;
}

export async function generateMetadata(
  { params }: PageProps,
  parent: ResolvingMetadata
): Promise<Metadata> {
  const { id } = await params;
  const product = await getProduct(id);

  const previousImages = (await parent).openGraph?.images || [];

  return {
    title: product.name,
    description: product.description,
    openGraph: {
      images: [product.image, ...previousImages],
    },
  };
}
```

### Metadata Template

```tsx
// app/layout.tsx
export const metadata: Metadata = {
  title: {
    template: '%s | My Store',
    default: 'My Store',
  },
  metadataBase: new URL('https://mystore.com'),
};

// app/products/page.tsx
export const metadata: Metadata = {
  title: 'Products', // Results in "Products | My Store"
};
```

## Templates vs Layouts

```tsx
// app/dashboard/template.tsx
// Template re-mounts on navigation (state resets)
export default function DashboardTemplate({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div>
      <nav>Dashboard Navigation</nav>
      {children}
    </div>
  );
}
```

## Route Groups

```tsx
// (marketing)/about/page.tsx → /about
// (marketing)/contact/page.tsx → /contact
// (shop)/products/page.tsx → /products
// (shop)/cart/page.tsx → /cart

// Different layouts for different sections
// app/(marketing)/layout.tsx - Marketing layout
// app/(shop)/layout.tsx - Shop layout
```

## Client Components

```tsx
// components/Counter.tsx
'use client';

import { useState } from 'react';

export function Counter() {
  const [count, setCount] = useState(0);

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => setCount((c) => c + 1)}>Increment</button>
    </div>
  );
}
```

### Composing Server and Client Components

```tsx
// app/page.tsx (Server Component)
import { Counter } from '@/components/Counter';
import { db } from '@/lib/db';

export default async function Page() {
  const initialData = await db.getData();

  return (
    <div>
      <h1>Server rendered title</h1>
      <Counter />
      <ClientDataDisplay data={initialData} />
    </div>
  );
}
```

## Navigation

### Link Component

```tsx
import Link from 'next/link';

export function Navigation() {
  return (
    <nav>
      <Link href="/">Home</Link>
      <Link href="/about">About</Link>
      <Link href="/blog" prefetch={false}>Blog</Link>
      <Link href="/dashboard" replace>Dashboard</Link>
    </nav>
  );
}
```

### useRouter Hook

```tsx
'use client';

import { useRouter } from 'next/navigation';

export function NavigateButton() {
  const router = useRouter();

  return (
    <button onClick={() => router.push('/dashboard')}>
      Go to Dashboard
    </button>
  );
}
```

### usePathname and useSearchParams

```tsx
'use client';

import { usePathname, useSearchParams } from 'next/navigation';

export function CurrentPath() {
  const pathname = usePathname();
  const searchParams = useSearchParams();
  const query = searchParams.get('q');

  return (
    <div>
      <p>Current path: {pathname}</p>
      {query && <p>Search query: {query}</p>}
    </div>
  );
}
```

## Best Practices

| Practice | Description |
|----------|-------------|
| Default to Server Components | Only use 'use client' when needed |
| Colocate related files | Keep page, loading, error together |
| Use route groups | Organize without affecting URL |
| Implement loading states | Use loading.tsx or Suspense |
| Handle errors gracefully | Use error.tsx boundaries |
| Optimize metadata | Use generateMetadata for dynamic pages |
