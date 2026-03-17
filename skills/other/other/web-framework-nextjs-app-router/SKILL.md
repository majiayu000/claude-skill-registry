---
name: web-framework-nextjs-app-router
description: Next.js 15 App Router patterns - file-based routing, Server/Client Components, streaming, Suspense, metadata API, parallel routes, Turbopack, async params
---

# Next.js App Router Patterns

> **Quick Guide:** Use Server Components by default, add `"use client"` only for interactivity. Use `loading.tsx` for route-level loading states, `<Suspense>` for granular streaming. Keep Client Components small and leaf-level.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST use Server Components by default - add `"use client"` ONLY when you need state, effects, or event handlers)**

**(You MUST keep `"use client"` components small and push them to the leaves of your component tree)**

**(You MUST use `loading.tsx` for route-level loading states and `<Suspense>` for granular streaming)**

**(You MUST use the Metadata API (`metadata` object or `generateMetadata`) for SEO - never manual `<head>` tags)**

**(You MUST use `server-only` package for code with secrets to prevent accidental client exposure)**

</critical_requirements>

---

**Auto-detection:** Next.js App Router, page.tsx, layout.tsx, loading.tsx, error.tsx, Server Components, Client Components, "use client", streaming, Suspense, parallel routes, intercepting routes, generateMetadata, generateStaticParams, Turbopack, next/form, use cache, PPR, experimental_ppr, instrumentation.ts, after(), typedRoutes

**When to use:**

- Building Next.js applications with the App Router (`app/` directory)
- Implementing file-based routing with layouts, loading states, and error boundaries
- Deciding when to use Server Components vs Client Components
- Implementing streaming and progressive rendering with Suspense
- Setting up SEO with the Metadata API
- Building advanced routing patterns (parallel routes, intercepting routes, modals)

**Key patterns covered:**

- File conventions (page.tsx, layout.tsx, loading.tsx, error.tsx, not-found.tsx)
- Server Components vs Client Components boundary decisions
- Streaming with Suspense and loading.tsx
- Parallel Routes and Intercepting Routes for modals
- Route Groups and Dynamic Routes
- Metadata API for SEO optimization
- generateStaticParams for static generation
- Next.js 15.5+ features (PPR, Turbopack builds, typed routes, after() API)
- Next.js 16 migration preparation

**When NOT to use:**

- Pages Router (`pages/` directory) - different patterns apply
- Pure React without Next.js framework
- Non-App Router Next.js projects

**Detailed Resources:**

- For code examples, see [examples/](examples/) folder
- For Next.js 15.5+ features (PPR, after(), typed routes), see [examples/nextjs-15-features.md](examples/nextjs-15-features.md)
- For decision frameworks and anti-patterns, see [reference.md](reference.md)

---

<philosophy>

## Philosophy

The App Router represents a paradigm shift from traditional React: **Server Components are the default**, and client-side JavaScript is opt-in. This reduces bundle size, improves initial load performance, and allows data fetching directly in components without client-server waterfalls.

**Core principles:**

1. **Server-first rendering** - Components run on the server by default, shipping zero JavaScript to the client
2. **Streaming and progressive rendering** - HTML streams to the browser as it becomes available
3. **Colocation** - Data fetching, styling, and metadata live alongside the components that need them
4. **Nested layouts** - Layouts persist across navigations, preserving state and avoiding re-renders
5. **File-based conventions** - Special files define behavior (page.tsx, layout.tsx, loading.tsx, error.tsx)

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: File-Based Routing Conventions

The App Router uses a file-system based router where folders define routes and special files define UI and behavior.

#### File Conventions

| File            | Purpose                                                        | Required |
| --------------- | -------------------------------------------------------------- | -------- |
| `page.tsx`      | Unique UI for a route, makes the route publicly accessible     | Yes      |
| `layout.tsx`    | Shared UI for a segment and its children, preserves state      | No       |
| `loading.tsx`   | Loading UI for a segment, automatically wraps page in Suspense | No       |
| `error.tsx`     | Error UI for a segment, catches runtime errors                 | No       |
| `not-found.tsx` | Not found UI, triggered by `notFound()` function               | No       |
| `template.tsx`  | Re-rendered layout (doesn't preserve state)                    | No       |
| `default.tsx`   | Fallback UI for parallel routes when no match                  | No       |

#### Route Segment Structure

```
app/
├── layout.tsx           # Root layout (required)
├── page.tsx             # Home page (/)
├── loading.tsx          # Loading state for /
├── error.tsx            # Error boundary for /
├── not-found.tsx        # 404 page
├── dashboard/
│   ├── layout.tsx       # Dashboard layout (nested)
│   ├── page.tsx         # /dashboard
│   ├── loading.tsx      # Loading state for /dashboard
│   ├── settings/
│   │   └── page.tsx     # /dashboard/settings
│   └── [id]/
│       └── page.tsx     # /dashboard/:id (dynamic)
└── (marketing)/         # Route group (no URL impact)
    ├── about/
    │   └── page.tsx     # /about
    └── blog/
        └── page.tsx     # /blog
```

**Why this works:** File conventions eliminate boilerplate routing configuration, layouts automatically nest, and special files provide consistent behavior patterns across the app.

---

### Pattern 2: Server Components vs Client Components

Server Components are the default in the App Router. Use `"use client"` directive only when necessary.

#### When to Use Server Components (Default)

- Fetching data from databases or APIs
- Accessing backend resources (file system, environment variables)
- Keeping sensitive information on the server (API keys, tokens)
- Reducing client-side JavaScript bundle
- Rendering static content

#### When to Use Client Components (`"use client"`)

- Adding interactivity with event handlers (`onClick`, `onChange`)
- Using React state (`useState`, `useReducer`)
- Using lifecycle effects (`useEffect`, `useLayoutEffect`)
- Using browser-only APIs (`localStorage`, `window`, `navigator`)
- Using custom hooks that depend on state or effects

#### Composition Pattern: Server Wrapping Client

```tsx
// app/dashboard/page.tsx (Server Component - default)
import { getUser } from "@/lib/data";
import { UserProfile } from "./user-profile";

export default async function DashboardPage() {
  const user = await getUser(); // Server-side data fetch

  return (
    <div>
      <h1>Dashboard</h1>
      {/* Pass data as props to Client Component */}
      <UserProfile user={user} />
    </div>
  );
}
```

```tsx
// app/dashboard/user-profile.tsx (Client Component)
"use client";

import { useState } from "react";
import type { User } from "@/lib/types";

interface UserProfileProps {
  user: User;
}

export function UserProfile({ user }: UserProfileProps) {
  const [isEditing, setIsEditing] = useState(false);

  return (
    <div>
      <p>{user.name}</p>
      <button onClick={() => setIsEditing(!isEditing)}>
        {isEditing ? "Cancel" : "Edit"}
      </button>
    </div>
  );
}
```

**Why good:** Server Component fetches data without client-side JavaScript, Client Component handles only the interactive parts, minimal JavaScript shipped to browser

---

### Pattern 3: Streaming with Suspense and loading.tsx

Streaming allows progressive rendering by sending HTML chunks as they become available.

#### Route-Level Loading with loading.tsx

```tsx
// app/dashboard/loading.tsx
export default function DashboardLoading() {
  return (
    <div className="animate-pulse">
      <div className="h-8 w-48 bg-gray-200 rounded mb-4" />
      <div className="h-64 bg-gray-200 rounded" />
    </div>
  );
}
```

**Why good:** Automatically wraps page in Suspense boundary, shows loading state immediately while data fetches, no manual Suspense setup needed

#### Granular Streaming with Suspense

```tsx
// app/dashboard/page.tsx
import { Suspense } from "react";
import { RevenueChart, RevenueChartSkeleton } from "./revenue-chart";
import { LatestInvoices, InvoicesSkeleton } from "./latest-invoices";

export default function DashboardPage() {
  return (
    <div>
      <h1>Dashboard</h1>

      {/* Each section streams independently */}
      <Suspense fallback={<RevenueChartSkeleton />}>
        <RevenueChart />
      </Suspense>

      <Suspense fallback={<InvoicesSkeleton />}>
        <LatestInvoices />
      </Suspense>
    </div>
  );
}
```

**Why good:** Slow data fetches don't block fast ones, users see content progressively, each section loads independently improving perceived performance

---

### Pattern 4: Layouts and Nested Layouts

Layouts wrap page content and persist across navigations within their segment.

#### Root Layout (Required)

```tsx
// app/layout.tsx
import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: {
    template: "%s | Acme",
    default: "Acme",
  },
  description: "The React Framework for the Web",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
```

#### Nested Layout with Navigation

```tsx
// app/dashboard/layout.tsx
import { DashboardNav } from "./dashboard-nav";

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="flex">
      <DashboardNav />
      <main className="flex-1 p-6">{children}</main>
    </div>
  );
}
```

**Why good:** Navigation state persists when switching between dashboard pages, layout doesn't re-render on navigation, shared UI defined once

---

### Pattern 5: Error Handling with error.tsx

Error boundaries catch runtime errors and display fallback UI.

#### Error Boundary Component

```tsx
// app/dashboard/error.tsx
"use client"; // Error components must be Client Components

import { useEffect } from "react";

interface ErrorProps {
  error: Error & { digest?: string };
  reset: () => void;
}

export default function DashboardError({ error, reset }: ErrorProps) {
  useEffect(() => {
    // Log error to reporting service
    console.error("Dashboard error:", error);
  }, [error]);

  return (
    <div role="alert" className="p-6 text-center">
      <h2>Something went wrong!</h2>
      <p className="text-red-600">{error.message}</p>
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

**Why good:** Errors are contained to the segment (rest of app remains functional), reset function allows retry without full page reload, digest provides server-side error reference

#### Global Error Handler

```tsx
// app/global-error.tsx
"use client";

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
        <button onClick={reset}>Try again</button>
      </body>
    </html>
  );
}
```

**Note:** global-error.tsx must define its own `<html>` and `<body>` tags as it replaces the root layout when triggered.

---

### Pattern 6: Metadata API for SEO

Use static `metadata` object or dynamic `generateMetadata` function for SEO.

#### Static Metadata

```tsx
// app/about/page.tsx
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "About Us",
  description: "Learn more about our company",
  openGraph: {
    title: "About Us | Acme",
    description: "Learn more about our company",
    images: ["/og-about.png"],
  },
};

export default function AboutPage() {
  return <h1>About Us</h1>;
}
```

#### Dynamic Metadata with generateMetadata

```tsx
// app/blog/[slug]/page.tsx
import type { Metadata } from "next";
import { getPost } from "@/lib/data";

interface PageProps {
  params: Promise<{ slug: string }>;
}

export async function generateMetadata({
  params,
}: PageProps): Promise<Metadata> {
  const { slug } = await params;
  const post = await getPost(slug);

  if (!post) {
    return { title: "Post Not Found" };
  }

  return {
    title: post.title,
    description: post.excerpt,
    openGraph: {
      title: post.title,
      description: post.excerpt,
      images: [post.coverImage],
      type: "article",
      publishedTime: post.publishedAt,
    },
  };
}

export default async function BlogPostPage({ params }: PageProps) {
  const { slug } = await params;
  const post = await getPost(slug);
  // ...
}
```

**Why good:** Type-safe metadata, automatic deduplication, fetch requests memoized across generateMetadata and page component

---

### Pattern 7: Static Generation with generateStaticParams

Pre-render dynamic routes at build time for performance.

```tsx
// app/blog/[slug]/page.tsx
import { getAllPosts, getPost } from "@/lib/data";

// Generate static params at build time
export async function generateStaticParams() {
  const posts = await getAllPosts();

  return posts.map((post) => ({
    slug: post.slug,
  }));
}

interface PageProps {
  params: Promise<{ slug: string }>;
}

export default async function BlogPostPage({ params }: PageProps) {
  const { slug } = await params;
  const post = await getPost(slug);

  return (
    <article>
      <h1>{post.title}</h1>
      <div dangerouslySetInnerHTML={{ __html: post.content }} />
    </article>
  );
}
```

**Why good:** Pages pre-rendered at build time for instant loading, combined with generateMetadata for complete static optimization, new posts added via ISR

---

### Pattern 8: Dynamic Routes

Use folder naming conventions for dynamic segments.

#### Single Dynamic Segment

```tsx
// app/users/[id]/page.tsx
interface PageProps {
  params: Promise<{ id: string }>;
}

export default async function UserPage({ params }: PageProps) {
  const { id } = await params;
  return <h1>User: {id}</h1>;
}
```

#### Catch-All Segments

```tsx
// app/docs/[...slug]/page.tsx
// Matches /docs/a, /docs/a/b, /docs/a/b/c, etc.

interface PageProps {
  params: Promise<{ slug: string[] }>;
}

export default async function DocsPage({ params }: PageProps) {
  const { slug } = await params;
  // slug is an array: ["a", "b", "c"]
  return <h1>Docs: {slug.join("/")}</h1>;
}
```

#### Optional Catch-All Segments

```tsx
// app/shop/[[...slug]]/page.tsx
// Matches /shop, /shop/a, /shop/a/b, etc.

interface PageProps {
  params: Promise<{ slug?: string[] }>;
}

export default async function ShopPage({ params }: PageProps) {
  const { slug } = await params;
  // slug is undefined for /shop, or an array for nested paths
  return <h1>Shop: {slug?.join("/") ?? "All Products"}</h1>;
}
```

---

### Pattern 9: Route Groups

Organize routes without affecting URL structure using `(groupName)` folders.

```
app/
├── (marketing)/
│   ├── layout.tsx      # Marketing-specific layout
│   ├── about/
│   │   └── page.tsx    # /about (not /marketing/about)
│   └── blog/
│       └── page.tsx    # /blog
├── (shop)/
│   ├── layout.tsx      # Shop-specific layout
│   └── products/
│       └── page.tsx    # /products
└── layout.tsx          # Root layout
```

**Why good:** Different layouts for different sections without URL nesting, logical grouping of related routes, multiple root layouts possible

---

### Pattern 10: Parallel Routes and Slots

Render multiple pages simultaneously in the same layout using `@slot` folders.

#### Dashboard with Multiple Slots

```
app/
└── dashboard/
    ├── @analytics/
    │   ├── page.tsx       # Analytics slot content
    │   └── default.tsx    # Fallback when no match
    ├── @team/
    │   ├── page.tsx       # Team slot content
    │   └── default.tsx
    ├── layout.tsx         # Receives slots as props
    └── page.tsx           # Main dashboard content
```

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
    <div className="grid grid-cols-2 gap-4">
      <div className="col-span-2">{children}</div>
      <div>{analytics}</div>
      <div>{team}</div>
    </div>
  );
}
```

**Why good:** Independent loading states per slot, parallel data fetching, conditional rendering based on user role

---

### Pattern 11: Intercepting Routes for Modals

Intercept navigation to show content in a modal while preserving the original route.

#### Modal Pattern Structure

```
app/
├── @modal/
│   ├── (.)photo/[id]/
│   │   └── page.tsx      # Intercepted route (modal)
│   └── default.tsx       # Returns null when no modal
├── photo/[id]/
│   └── page.tsx          # Full page (direct navigation)
└── layout.tsx
```

#### Intercepting Convention

| Convention | Description         |
| ---------- | ------------------- |
| `(.)`      | Match same level    |
| `(..)`     | Match one level up  |
| `(..)(..)` | Match two levels up |
| `(...)`    | Match from root     |

```tsx
// app/@modal/(.)photo/[id]/page.tsx
import { Modal } from "@/components/modal";
import { getPhoto } from "@/lib/data";

interface PageProps {
  params: Promise<{ id: string }>;
}

export default async function PhotoModal({ params }: PageProps) {
  const { id } = await params;
  const photo = await getPhoto(id);

  return (
    <Modal>
      <img src={photo.url} alt={photo.title} />
      <p>{photo.title}</p>
    </Modal>
  );
}
```

```tsx
// app/@modal/default.tsx
export default function Default() {
  return null;
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

**Why good:** Modal shows on soft navigation with shareable URL, full page renders on hard refresh or direct link, back button closes modal

</patterns>

---

<integration>

## Integration Guide

**Next.js App Router is the framework foundation.** It handles routing, rendering strategies, and data fetching patterns. Other skills build on top of it.

**Styling integration:**

- Apply styles via `className` prop on components
- Global styles imported in root layout
- CSS Modules work with both Server and Client Components

**Data fetching integration:**

- Server Components fetch data directly (no client-side fetching library needed for server data)
- Client Components use your data fetching solution for client-side state

**State integration:**

- Server state: fetch in Server Components, pass as props
- Client state: use your state management solution in Client Components only

</integration>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md**

**(You MUST use Server Components by default - add `"use client"` ONLY when you need state, effects, or event handlers)**

**(You MUST keep `"use client"` components small and push them to the leaves of your component tree)**

**(You MUST use `loading.tsx` for route-level loading states and `<Suspense>` for granular streaming)**

**(You MUST use the Metadata API (`metadata` object or `generateMetadata`) for SEO - never manual `<head>` tags)**

**(You MUST use `server-only` package for code with secrets to prevent accidental client exposure)**

**Failure to follow these rules will ship unnecessary JavaScript to the client, break SEO, or expose secrets.**

</critical_reminders>
