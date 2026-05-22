---
name: nextjs-app-router-file-conventions
version: "1.0"
description: >
  Special file conventions in Next.js 14+ App Router for pages, layouts, and API routes.
  PROACTIVELY activate for: (1) creating pages and layouts, (2) implementing loading and error states, (3) building API route handlers.
  Triggers: "new page", "layout", "api route"
group: foundation
core-integration:
  techniques:
    primary: ["structured_decomposition"]
    secondary: []
  contracts:
    input: "none"
    output: "none"
  patterns: "none"
  rubrics: "none"
---

# Next.js App Router File Conventions

## Special Files

| File | Purpose | Required | Component Type |
|------|---------|----------|----------------|
| `layout.tsx` | Shared UI for route segment | Yes (root only) | Server |
| `page.tsx` | Unique UI for route | Yes | Server (default) |
| `loading.tsx` | Loading UI (Suspense fallback) | No | Server |
| `error.tsx` | Error UI (Error Boundary) | No | **Client** |
| `not-found.tsx` | 404 UI | No | Server |
| `route.ts` | API endpoint | No | N/A (API) |

## File Structure Example

```
app/
├── layout.tsx              # Root layout (wraps all pages)
├── page.tsx                # Home page (/)
├── loading.tsx             # Global loading
├── error.tsx               # Global error boundary
├── not-found.tsx           # Global 404
├── blog/
│   ├── layout.tsx          # Blog layout
│   ├── page.tsx            # Blog index (/blog)
│   └── [slug]/
│       ├── page.tsx        # Blog post (/blog/my-post)
│       ├── loading.tsx     # Post loading state
│       └── error.tsx       # Post error handling
└── api/
    └── posts/
        └── route.ts        # API endpoint (/api/posts)
```

## layout.tsx (Persistent Wrapper)

```tsx
// app/layout.tsx (ROOT LAYOUT - REQUIRED)
export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <Header />
        {children}
        <Footer />
      </body>
    </html>
  );
}

// app/dashboard/layout.tsx (Nested layout)
export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex">
      <Sidebar />
      <main>{children}</main>
    </div>
  );
}
```

## page.tsx (Route Content)

```tsx
// app/blog/[slug]/page.tsx
interface Props {
  params: Promise<{ slug: string }>;
  searchParams: Promise<{ [key: string]: string | undefined }>;
}

export default async function BlogPost({ params }: Props) {
  const { slug } = await params;
  const post = await fetchPost(slug);
  return <article>{post.content}</article>;
}
```

## loading.tsx (Streaming UI)

```tsx
// app/blog/[slug]/loading.tsx
export default function Loading() {
  return <div className="animate-pulse">Loading post...</div>;
}
```

## error.tsx (Error Boundary)

```tsx
// app/blog/[slug]/error.tsx
'use client' // MUST be Client Component

export default function Error({
  error,
  reset,
}: {
  error: Error;
  reset: () => void;
}) {
  return (
    <div>
      <h2>Error: {error.message}</h2>
      <button onClick={reset}>Try again</button>
    </div>
  );
}
```

## route.ts (API Endpoint)

```tsx
// app/api/posts/route.ts
import { NextResponse } from 'next/server';

export async function GET(request: Request) {
  const posts = await fetchPosts();
  return NextResponse.json({ posts });
}

export async function POST(request: Request) {
  const body = await request.json();
  const post = await createPost(body);
  return NextResponse.json({ post }, { status: 201 });
}
```

## Dynamic Routes

- `[id]` - Dynamic segment (e.g., `/blog/[slug]` matches `/blog/hello`)
- `[...slug]` - Catch-all (e.g., `/docs/[...slug]` matches `/docs/a/b/c`)
- `[[...slug]]` - Optional catch-all

For route groups, parallel routes, and intercepting routes, see `resources/advanced-routing.md`.
