---
name: nextjs-routing-advanced
description: Complete Next.js advanced routing system. PROACTIVELY activate for: (1) Dynamic routes with [slug], (2) Catch-all routes [...slug], (3) Route groups for organization, (4) Parallel routes with @slot, (5) Intercepting routes for modals, (6) Private folders with _prefix, (7) Route Handlers (API), (8) Search params handling, (9) Programmatic navigation. Provides: Dynamic routing patterns, parallel route slots, modal interception, API handlers. Ensures flexible routing with proper URL structure.
---

## Quick Reference

| Route Type | Folder Pattern | URL Example |
|------------|----------------|-------------|
| Dynamic | `[slug]` | `/blog/hello` → `{ slug: 'hello' }` |
| Catch-all | `[...slug]` | `/docs/a/b` → `{ slug: ['a', 'b'] }` |
| Optional catch-all | `[[...slug]]` | `/shop` or `/shop/a/b` |
| Route group | `(name)` | No URL impact, layout grouping |
| Parallel route | `@slot` | Independent loading/error |
| Intercept same level | `(.)path` | Modal pattern |
| Private folder | `_folder` | Not a route |

| Navigation | Code | Use Case |
|------------|------|----------|
| Link | `<Link href="/path">` | Declarative nav |
| router.push | `router.push('/path')` | Programmatic nav |
| router.replace | `router.replace('/path')` | No history entry |
| redirect | `redirect('/path')` | Server redirect |

| Route Handler | Method | Pattern |
|---------------|--------|---------|
| `GET` | Read | `export async function GET() {}` |
| `POST` | Create | `export async function POST() {}` |
| `PUT` | Update | `export async function PUT() {}` |
| `DELETE` | Delete | `export async function DELETE() {}` |

## When to Use This Skill

Use for **advanced routing patterns**:
- Dynamic blog/product pages with slugs
- Documentation with catch-all routes
- Dashboard layouts with parallel routes
- Photo gallery modals with intercepting routes
- API endpoints with Route Handlers

**Related skills:**
- For App Router basics: see `nextjs-app-router`
- For middleware routing: see `nextjs-middleware`
- For data in routes: see `nextjs-data-fetching`

---

# Next.js Advanced Routing

## Dynamic Routes

### Single Dynamic Segment

```tsx
// app/blog/[slug]/page.tsx
interface PageProps {
  params: Promise<{ slug: string }>;
}

export default async function BlogPost({ params }: PageProps) {
  const { slug } = await params;
  const post = await getPost(slug);

  return <article>{post.content}</article>;
}

// /blog/hello-world → { slug: 'hello-world' }
```

### Multiple Dynamic Segments

```tsx
// app/shop/[category]/[product]/page.tsx
interface PageProps {
  params: Promise<{ category: string; product: string }>;
}

export default async function ProductPage({ params }: PageProps) {
  const { category, product } = await params;
  const productData = await getProduct(category, product);

  return <div>{productData.name}</div>;
}

// /shop/electronics/laptop → { category: 'electronics', product: 'laptop' }
```

### Catch-All Segments

```tsx
// app/docs/[...slug]/page.tsx
interface PageProps {
  params: Promise<{ slug: string[] }>;
}

export default async function DocsPage({ params }: PageProps) {
  const { slug } = await params;
  // slug is an array of path segments
  const doc = await getDoc(slug.join('/'));

  return <div>{doc.content}</div>;
}

// /docs/getting-started → { slug: ['getting-started'] }
// /docs/api/auth/login → { slug: ['api', 'auth', 'login'] }
```

### Optional Catch-All Segments

```tsx
// app/shop/[[...slug]]/page.tsx
interface PageProps {
  params: Promise<{ slug?: string[] }>;
}

export default async function ShopPage({ params }: PageProps) {
  const { slug } = await params;

  if (!slug) {
    // /shop - show all products
    return <AllProducts />;
  }

  if (slug.length === 1) {
    // /shop/category - show category
    return <CategoryProducts category={slug[0]} />;
  }

  // /shop/category/product - show product
  return <ProductDetail category={slug[0]} product={slug[1]} />;
}

// /shop → { slug: undefined }
// /shop/electronics → { slug: ['electronics'] }
// /shop/electronics/laptop → { slug: ['electronics', 'laptop'] }
```

## Route Groups

### Organizing Without URL Impact

```
app/
├── (marketing)/
│   ├── layout.tsx      # Marketing layout
│   ├── about/
│   │   └── page.tsx    # /about
│   └── contact/
│       └── page.tsx    # /contact
│
├── (shop)/
│   ├── layout.tsx      # Shop layout
│   ├── products/
│   │   └── page.tsx    # /products
│   └── cart/
│       └── page.tsx    # /cart
│
└── (auth)/
    ├── layout.tsx      # Auth layout (centered, minimal)
    ├── login/
    │   └── page.tsx    # /login
    └── register/
        └── page.tsx    # /register
```

### Multiple Root Layouts

```tsx
// app/(marketing)/layout.tsx
export default function MarketingLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html>
      <body>
        <MarketingHeader />
        {children}
        <MarketingFooter />
      </body>
    </html>
  );
}

// app/(app)/layout.tsx
export default function AppLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html>
      <body>
        <AppSidebar />
        <main>{children}</main>
      </body>
    </html>
  );
}
```

## Parallel Routes

### Basic Parallel Routes

```
app/
├── layout.tsx
├── page.tsx
├── @analytics/
│   ├── page.tsx
│   └── loading.tsx
├── @team/
│   ├── page.tsx
│   └── loading.tsx
└── @notifications/
    └── page.tsx
```

```tsx
// app/layout.tsx
export default function Layout({
  children,
  analytics,
  team,
  notifications,
}: {
  children: React.ReactNode;
  analytics: React.ReactNode;
  team: React.ReactNode;
  notifications: React.ReactNode;
}) {
  return (
    <div className="dashboard">
      <main>{children}</main>
      <aside>
        {analytics}
        {team}
        {notifications}
      </aside>
    </div>
  );
}
```

### Conditional Rendering with Parallel Routes

```tsx
// app/layout.tsx
import { auth } from '@/lib/auth';

export default async function Layout({
  children,
  admin,
  user,
}: {
  children: React.ReactNode;
  admin: React.ReactNode;
  user: React.ReactNode;
}) {
  const session = await auth();

  return (
    <div>
      {children}
      {session?.role === 'admin' ? admin : user}
    </div>
  );
}
```

### Default Slots

```tsx
// app/@analytics/default.tsx
// Shown when the slot doesn't match current route
export default function AnalyticsDefault() {
  return null; // or a default UI
}
```

## Intercepting Routes

### Modal Pattern

```
app/
├── feed/
│   └── page.tsx              # /feed - main feed
├── photo/
│   └── [id]/
│       └── page.tsx          # /photo/123 - full page photo
└── @modal/
    └── (.)photo/
        └── [id]/
            └── page.tsx      # Intercepted: shows modal
```

### Intercepting Conventions

```
(.)  - Match same level
(..) - Match one level above
(..)(..) - Match two levels above
(...) - Match from root
```

### Photo Gallery Modal Example

```tsx
// app/feed/page.tsx
import Link from 'next/link';

export default function FeedPage() {
  const photos = await getPhotos();

  return (
    <div className="grid">
      {photos.map((photo) => (
        <Link key={photo.id} href={`/photo/${photo.id}`}>
          <img src={photo.thumbnail} alt={photo.title} />
        </Link>
      ))}
    </div>
  );
}
```

```tsx
// app/@modal/(.)photo/[id]/page.tsx
import { Modal } from '@/components/modal';

export default async function PhotoModal({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  const photo = await getPhoto(id);

  return (
    <Modal>
      <img src={photo.url} alt={photo.title} />
      <p>{photo.description}</p>
    </Modal>
  );
}
```

```tsx
// app/photo/[id]/page.tsx - Full page view (direct navigation)
export default async function PhotoPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  const photo = await getPhoto(id);

  return (
    <div className="photo-page">
      <img src={photo.url} alt={photo.title} />
      <h1>{photo.title}</h1>
      <p>{photo.description}</p>
    </div>
  );
}
```

```tsx
// app/layout.tsx
export default function RootLayout({
  children,
  modal,
}: {
  children: React.ReactNode;
  modal: React.ReactNode;
}) {
  return (
    <html>
      <body>
        {children}
        {modal}
      </body>
    </html>
  );
}
```

```tsx
// components/modal.tsx
'use client';

import { useRouter } from 'next/navigation';

export function Modal({ children }: { children: React.ReactNode }) {
  const router = useRouter();

  return (
    <div className="modal-overlay" onClick={() => router.back()}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <button onClick={() => router.back()}>Close</button>
        {children}
      </div>
    </div>
  );
}
```

## Private Folders

```
app/
├── _components/         # Private - not a route
│   ├── Button.tsx
│   └── Card.tsx
├── _lib/               # Private - not a route
│   └── utils.ts
├── dashboard/
│   ├── _components/    # Private - scoped to dashboard
│   │   └── Chart.tsx
│   └── page.tsx
└── page.tsx
```

## Route Handlers

### HTTP Methods

```tsx
// app/api/posts/route.ts
import { NextResponse } from 'next/server';

export async function GET(request: Request) {
  const posts = await getPosts();
  return NextResponse.json(posts);
}

export async function POST(request: Request) {
  const body = await request.json();
  const post = await createPost(body);
  return NextResponse.json(post, { status: 201 });
}

export async function PUT(request: Request) {
  const body = await request.json();
  const post = await updatePost(body);
  return NextResponse.json(post);
}

export async function DELETE(request: Request) {
  await deletePost();
  return new NextResponse(null, { status: 204 });
}
```

### Dynamic Route Handlers

```tsx
// app/api/posts/[id]/route.ts
interface RouteContext {
  params: Promise<{ id: string }>;
}

export async function GET(request: Request, context: RouteContext) {
  const { id } = await context.params;
  const post = await getPost(id);

  if (!post) {
    return NextResponse.json({ error: 'Not found' }, { status: 404 });
  }

  return NextResponse.json(post);
}
```

### Route Handler Options

```tsx
// Force dynamic
export const dynamic = 'force-dynamic';

// Set runtime
export const runtime = 'edge';

// Set revalidation
export const revalidate = 60;
```

## URL Query Parameters

### Accessing Search Params

```tsx
// app/search/page.tsx
interface SearchPageProps {
  searchParams: Promise<{ q?: string; page?: string; sort?: string }>;
}

export default async function SearchPage({ searchParams }: SearchPageProps) {
  const { q, page = '1', sort = 'relevance' } = await searchParams;

  const results = await search({
    query: q,
    page: parseInt(page),
    sort,
  });

  return (
    <div>
      <h1>Results for: {q}</h1>
      <SearchResults results={results} />
    </div>
  );
}
```

### Client-Side URL Updates

```tsx
'use client';

import { useRouter, useSearchParams, usePathname } from 'next/navigation';

export function SearchFilter() {
  const router = useRouter();
  const pathname = usePathname();
  const searchParams = useSearchParams();

  const updateSearch = (key: string, value: string) => {
    const params = new URLSearchParams(searchParams.toString());
    params.set(key, value);
    router.push(`${pathname}?${params.toString()}`);
  };

  return (
    <select onChange={(e) => updateSearch('sort', e.target.value)}>
      <option value="relevance">Relevance</option>
      <option value="date">Date</option>
      <option value="price">Price</option>
    </select>
  );
}
```

## Programmatic Navigation

### useRouter Hook

```tsx
'use client';

import { useRouter } from 'next/navigation';

export function NavigationExample() {
  const router = useRouter();

  return (
    <div>
      <button onClick={() => router.push('/dashboard')}>
        Go to Dashboard
      </button>
      <button onClick={() => router.replace('/login')}>
        Replace with Login
      </button>
      <button onClick={() => router.back()}>
        Go Back
      </button>
      <button onClick={() => router.forward()}>
        Go Forward
      </button>
      <button onClick={() => router.refresh()}>
        Refresh
      </button>
      <button onClick={() => router.prefetch('/about')}>
        Prefetch About
      </button>
    </div>
  );
}
```

### redirect() Function

```tsx
// In Server Component or Server Action
import { redirect } from 'next/navigation';

export default async function ProtectedPage() {
  const session = await getSession();

  if (!session) {
    redirect('/login');
  }

  return <div>Protected content</div>;
}
```

### permanentRedirect() Function

```tsx
import { permanentRedirect } from 'next/navigation';

export default async function OldPage() {
  permanentRedirect('/new-page'); // 308 status
}
```

## Best Practices

| Practice | Description |
|----------|-------------|
| Use route groups for organization | Group by feature or layout |
| Implement loading states | Add loading.tsx for each segment |
| Use parallel routes for dashboards | Independent loading/error states |
| Intercept for modals | Better UX for overlays |
| Keep private folders organized | Use _ prefix for non-routes |
| Type your params | Use Promise<> for params and searchParams |
