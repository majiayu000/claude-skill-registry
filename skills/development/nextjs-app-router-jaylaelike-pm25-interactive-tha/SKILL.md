---
name: nextjs-app-router
description: Use when next.js App Router with layouts, loading states, and streaming. Use when building modern Next.js 13+ applications.
allowed-tools:
  - Bash
  - Read
---

# Next.js App Router

Master the Next.js App Router for building modern, performant web
applications with server components and advanced routing.

## App Directory Structure

The app directory uses file-system based routing with special files:

```typescript
app/
  layout.tsx       # Root layout (required)
  page.tsx         # Home page
  loading.tsx      # Loading UI
  error.tsx        # Error UI
  not-found.tsx    # 404 UI
  template.tsx     # Re-rendered layout
  about/
    page.tsx       # /about
  blog/
    layout.tsx     # Blog-specific layout
    page.tsx       # /blog
    loading.tsx    # Blog loading state
    [slug]/
      page.tsx     # /blog/[slug]
  dashboard/
    (auth)/        # Route group (doesn't affect URL)
      layout.tsx   # Layout for auth routes
      settings/
        page.tsx   # /dashboard/settings
      profile/
        page.tsx   # /dashboard/profile

// app/layout.tsx - Root layout (required)
export default function RootLayout({
  children
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>
        <header>
          <Navigation />
        </header>
        <main>{children}</main>
        <footer>
          <Footer />
        </footer>
      </body>
    </html>
  );
}
```

## Layouts: Root, Nested, and Templates

```typescript
// app/layout.tsx - Root Layout (wraps entire app)
import { Inter } from 'next/font/google';
import './globals.css';

const inter = Inter({ subsets: ['latin'] });

export const metadata = {
  title: 'My App',
  description: 'Built with Next.js App Router'
};

export default function RootLayout({
  children
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <Providers>
          <Navigation />
          {children}
        </Providers>
      </body>
    </html>
  );
}

// app/dashboard/layout.tsx - Nested Layout
export default function DashboardLayout({
  children
}: {
  children: React.ReactNode
}) {
  return (
    <div className="dashboard">
      <aside>
        <DashboardNav />
      </aside>
      <section>{children}</section>
    </div>
  );
}

// app/dashboard/template.tsx - Template (re-renders on navigation)
// Use when you need fresh state on each navigation
export default function DashboardTemplate({
  children
}: {
  children: React.ReactNode
}) {
  // This re-renders and resets state on navigation
  return <div className="animate-fade-in">{children}</div>;
}
```

## Dynamic Routes and generateStaticParams

```typescript
// app/blog/[slug]/page.tsx
interface PageProps {
  params: { slug: string };
  searchParams: { [key: string]: string | string[] | undefined };
}

export default async function BlogPost({ params }: PageProps) {
  const post = await getPost(params.slug);

  return (
    <article>
      <h1>{post.title}</h1>
      <p>{post.content}</p>
    </article>
  );
}

// Generate static paths at build time (SSG)
export async function generateStaticParams() {
  const posts = await getPosts();

  return posts.map((post) => ({
    slug: post.slug
  }));
}

// Generate metadata dynamically
export async function generateMetadata({ params }: PageProps) {
  const post = await getPost(params.slug);

  return {
    title: post.title,
    description: post.excerpt,
    openGraph: {
      title: post.title,
      description: post.excerpt,
      images: [{ url: post.image }]
    }
  };
}

// Multiple dynamic segments: app/shop/[category]/[product]/page.tsx
export default async function Product({
  params
}: {
  params: { category: string; product: string }
}) {
  const product = await getProduct(params.category, params.product);
  return <div>{product.name}</div>;
}

export async function generateStaticParams() {
  const products = await getProducts();

  return products.map((product) => ({
    category: product.category,
    product: product.slug
  }));
}

// Catch-all routes: app/docs/[...slug]/page.tsx
export default function Docs({ params }: { params: { slug: string[] } }) {
  // /docs/a/b/c -> params.slug = ['a', 'b', 'c']
  const path = params.slug.join('/');
  return <div>Documentation: {path}</div>;
}

// Optional catch-all: app/blog/[[...slug]]/page.tsx
// Matches both /blog and /blog/a/b/c
```

## Loading UI and Streaming

```typescript
// app/blog/loading.tsx - Automatic loading UI
export default function Loading() {
  return (
    <div className="loading">
      <Skeleton />
      <Skeleton />
      <Skeleton />
    </div>
  );
}

// app/blog/page.tsx - Server component with streaming
import { Suspense } from 'react';

export default function BlogPage() {
  return (
    <div>
      <h1>Blog</h1>

      {/* Stream this component independently */}
      <Suspense fallback={<PostsSkeleton />}>
        <BlogPosts />
      </Suspense>

      {/* Stream this separately */}
      <Suspense fallback={<CommentsSkeleton />}>
        <RecentComments />
      </Suspense>
    </div>
  );
}

// Components can stream as they load
async function BlogPosts() {
  const posts = await getPosts(); // Server-side data fetch

  return (
    <div>
      {posts.map(post => (
        <PostCard key={post.id} post={post} />
      ))}
    </div>
  );
}

async function RecentComments() {
  const comments = await getComments();

  return (
    <div>
      {comments.map(comment => (
        <CommentCard key={comment.id} comment={comment} />
      ))}
    </div>
  );
}
```

## Error Boundaries and Error Handling

```typescript
// app/blog/error.tsx - Error boundary
'use client'; // Error components must be Client Components

import { useEffect } from 'react';

export default function Error({
  error,
  reset
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    // Log error to error reporting service
    console.error('Blog error:', error);
  }, [error]);

  return (
    <div className="error-container">
      <h2>Something went wrong!</h2>
      <p>{error.message}</p>
      <button onClick={() => reset()}>Try again</button>
    </div>
  );
}

// app/global-error.tsx - Global error boundary
'use client';

export default function GlobalError({
  error,
  reset
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  return (
    <html>
      <body>
        <h2>Application Error</h2>
        <button onClick={() => reset()}>Try again</button>
      </body>
    </html>
  );
}

// app/blog/not-found.tsx - Custom 404 page
import Link from 'next/link';

export default function NotFound() {
  return (
    <div>
      <h2>Post Not Found</h2>
      <p>Could not find the requested blog post.</p>
      <Link href="/blog">View all posts</Link>
    </div>
  );
}

// Programmatically trigger 404
import { notFound } from 'next/navigation';

export default async function Post({ params }: { params: { id: string } }) {
  const post = await getPost(params.id);

  if (!post) {
    notFound(); // Renders closest not-found.tsx
  }

  return <article>{post.content}</article>;
}
```

## Route Groups for Organization

```typescript
// Route groups don't affect URL structure
app/
  (marketing)/        # Group routes without affecting URLs
    layout.tsx        # Marketing layout
    page.tsx          # / (homepage)
    about/
      page.tsx        # /about
    contact/
      page.tsx        # /contact
  (shop)/
    layout.tsx        # Shop layout
    products/
      page.tsx        # /products
    cart/
      page.tsx        # /cart
  (auth)/
    layout.tsx        # Auth layout
    login/
      page.tsx        # /login
    register/
      page.tsx        # /register

// app/(marketing)/layout.tsx
export default function MarketingLayout({
  children
}: {
  children: React.ReactNode
}) {
  return (
    <>
      <MarketingHeader />
      {children}
      <MarketingFooter />
    </>
  );
}

// app/(shop)/layout.tsx
export default function ShopLayout({
  children
}: {
  children: React.ReactNode
}) {
  return (
    <>
      <ShopHeader />
      <ShopNav />
      {children}
    </>
  );
}
```

## Parallel Routes

```typescript
// Use parallel routes to render multiple pages in the same layout
app/
  dashboard/
    @analytics/
      page.tsx
    @team/
      page.tsx
    @user/
      page.tsx
    layout.tsx
    page.tsx

// app/dashboard/layout.tsx
export default function DashboardLayout({
  children,
  analytics,
  team,
  user
}: {
  children: React.ReactNode;
  analytics: React.ReactNode;
  team: React.ReactNode;
  user: React.ReactNode;
}) {
  return (
    <div className="dashboard-grid">
      <div className="main">{children}</div>
      <div className="analytics">{analytics}</div>
      <div className="team">{team}</div>
      <div className="user">{user}</div>
    </div>
  );
}

// Conditional rendering with parallel routes
export default function Layout({ user, admin }: {
  user: React.ReactNode;
  admin: React.ReactNode;
}) {
  const session = await getSession();

  return session.isAdmin ? admin : user;
}
```

## Intercepting Routes

```typescript
// Intercept routes to show modals or overlays
app/
  feed/
    page.tsx
    @modal/
      (.)photo/
        [id]/
          page.tsx
  photo/
    [id]/
      page.tsx

// app/feed/@modal/(.)photo/[id]/page.tsx
// Intercepts /photo/[id] when navigating from /feed
export default function PhotoModal({ params }: { params: { id: string } }) {
  return (
    <Modal>
      <Photo id={params.id} />
    </Modal>
  );
}

// app/photo/[id]/page.tsx
// Direct navigation to /photo/[id] shows full page
export default function PhotoPage({ params }: { params: { id: string } }) {
  return (
    <div className="photo-page">
      <Photo id={params.id} />
    </div>
  );
}

// Intercepting patterns:
// (.) matches same level
// (..) matches one level up
// (..)(..) matches two levels up
// (...) matches from root
```

## Metadata API for SEO

```typescript
// app/layout.tsx - Static metadata
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: {
    default: 'My App',
    template: '%s | My App' // Used by child pages
  },
  description: 'My awesome Next.js app',
  keywords: ['nextjs', 'react', 'typescript'],
  authors: [{ name: 'John Doe' }],
  openGraph: {
    title: 'My App',
    description: 'My awesome Next.js app',
    url: 'https://myapp.com',
    siteName: 'My App',
    images: [
      {
        url: 'https://myapp.com/og.png',
        width: 1200,
        height: 630
      }
    ],
    locale: 'en_US',
    type: 'website'
  },
  twitter: {
    card: 'summary_large_image',
    title: 'My App',
    description: 'My awesome Next.js app',
    images: ['https://myapp.com/twitter.png']
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      'max-video-preview': -1,
      'max-image-preview': 'large',
      'max-snippet': -1
    }
  }
};

// app/blog/[slug]/page.tsx - Dynamic metadata
export async function generateMetadata({
  params
}: {
  params: { slug: string }
}): Promise<Metadata> {
  const post = await getPost(params.slug);

  return {
    title: post.title,
    description: post.excerpt,
    authors: [{ name: post.author }],
    openGraph: {
      title: post.title,
      description: post.excerpt,
      images: [post.image],
      publishedTime: post.publishedAt,
      authors: [post.author]
    }
  };
}

// JSON-LD structured data
export default function Article({ params }: { params: { slug: string } }) {
  const post = getPost(params.slug);

  const jsonLd = {
    '@context': 'https://schema.org',
    '@type': 'Article',
    headline: post.title,
    datePublished: post.publishedAt,
    author: {
      '@type': 'Person',
      name: post.author
    }
  };

  return (
    <>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
      />
      <article>{post.content}</article>
    </>
  );
}
```

## Route Handlers (API Routes)

```typescript
// app/api/users/route.ts
import { NextRequest, NextResponse } from 'next/server';

// GET /api/users
export async function GET(request: NextRequest) {
  const searchParams = request.nextUrl.searchParams;
  const query = searchParams.get('query');

  const users = await getUsers(query);

  return NextResponse.json(users);
}

// POST /api/users
export async function POST(request: NextRequest) {
  const body = await request.json();

  const user = await createUser(body);

  return NextResponse.json(user, { status: 201 });
}

// app/api/users/[id]/route.ts
// GET /api/users/:id
export async function GET(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  const user = await getUser(params.id);

  if (!user) {
    return NextResponse.json({ error: 'User not found' }, { status: 404 });
  }

  return NextResponse.json(user);
}

// DELETE /api/users/:id
export async function DELETE(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  await deleteUser(params.id);

  return new NextResponse(null, { status: 204 });
}

// With middleware
export async function GET(request: NextRequest) {
  const session = await getSession(request);

  if (!session) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  const data = await getData(session.userId);

  return NextResponse.json(data);
}
```

## Middleware

```typescript
// middleware.ts (at root level)
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  // Check authentication
  const token = request.cookies.get('token');

  if (!token && request.nextUrl.pathname.startsWith('/dashboard')) {
    return NextResponse.redirect(new URL('/login', request.url));
  }

  // Add custom header
  const response = NextResponse.next();
  response.headers.set('x-custom-header', 'value');

  return response;
}

// Configure which routes use middleware
export const config = {
  matcher: [
    '/dashboard/:path*',
    '/api/:path*',
    '/((?!_next/static|_next/image|favicon.ico).*)'
  ]
};

// Advanced middleware with rewrites
export function middleware(request: NextRequest) {
  // A/B testing
  const bucket = Math.random() < 0.5 ? 'a' : 'b';
  request.cookies.set('bucket', bucket);

  if (bucket === 'a') {
    return NextResponse.rewrite(new URL('/experiment-a', request.url));
  }

  return NextResponse.next();
}
```

## When to Use This Skill

Use nextjs-app-router when you need to:

- Build modern Next.js 13+ applications
- Implement complex routing with layouts
- Use server and client components effectively
- Create loading and error boundaries
- Optimize performance with streaming
- Build SEO-friendly applications
- Implement dynamic and static routes
- Use parallel and intercepting routes
- Build scalable Next.js applications
- Implement advanced routing patterns
- Create type-safe API routes
- Optimize metadata for social sharing

## Best Practices

1. **Use server components by default** - Only mark components with 'use client'
   when they need interactivity or browser APIs.

2. **Implement proper loading states** - Use loading.tsx files and Suspense
   boundaries for better UX during data fetching.

3. **Create granular error boundaries** - Place error.tsx files at appropriate
   levels to handle errors gracefully.

4. **Leverage static generation** - Use generateStaticParams for dynamic routes
   that can be pre-rendered at build time.

5. **Organize with route groups** - Use route groups to organize code without
   affecting URL structure.

6. **Optimize metadata** - Implement both static and dynamic metadata for better
   SEO and social sharing.

7. **Stream content strategically** - Use Suspense to stream independent UI
   sections as they load.

8. **Keep client-side JavaScript minimal** - Maximize server components to reduce
   bundle size and improve performance.

9. **Use middleware wisely** - Apply middleware for authentication, redirects,
   and request modifications.

10. **Test routing behavior** - Verify navigation, loading states, and error
    handling across different routes.

## Common Pitfalls

1. **Using client components unnecessarily** - Marking components with 'use client'
   when they don't need browser APIs increases bundle size.

2. **Not implementing loading states** - Missing loading.tsx files lead to poor UX
   during navigation and data fetching.

3. **Forgetting error boundaries** - Without error.tsx files, errors crash the
   entire application instead of failing gracefully.

4. **Mixing server and client code incorrectly** - Importing server-only code in
   client components or vice versa causes errors.

5. **Not optimizing for static generation** - Missing generateStaticParams means
   pages render on-demand instead of at build time.

6. **Overusing dynamic routes** - Too many dynamic segments can make routing
   complex and hard to maintain.

7. **Not handling route parameters properly** - Failing to validate or sanitize
   route parameters can cause errors or security issues.

8. **Ignoring SEO considerations** - Missing or incomplete metadata hurts search
   engine rankings and social sharing.

9. **Not testing edge cases** - Skipping tests for 404s, errors, and loading
   states leads to poor user experience.

10. **Misunderstanding file conventions** - Naming files incorrectly (e.g., using
    Loading.tsx instead of loading.tsx) breaks conventions.

## Resources

- [Next.js App Router Documentation](https://nextjs.org/docs/app)
- [Next.js Routing Fundamentals](https://nextjs.org/docs/app/building-your-application/routing)
- [Server and Client Components](https://nextjs.org/docs/app/building-your-application/rendering)
- [Data Fetching Patterns](https://nextjs.org/docs/app/building-your-application/data-fetching)
- [Metadata API Reference](https://nextjs.org/docs/app/api-reference/functions/generate-metadata)
- [Next.js Examples](https://github.com/vercel/next.js/tree/canary/examples)
