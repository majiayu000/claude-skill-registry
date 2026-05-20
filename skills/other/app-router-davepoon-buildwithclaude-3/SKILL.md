---
name: app-router
description: This skill should be used when the user asks to "create a Next.js route", "add a page", "set up layouts", "implement loading states", "add error boundaries", "organize routes", "create dynamic routes", or needs guidance on Next.js App Router file conventions and routing patterns.
version: 1.0.0
---

# Next.js App Router Patterns

## Overview

The App Router is Next.js's file-system based router built on React Server Components. It uses a `app/` directory structure where folders define routes and special files control UI behavior.

## Core File Conventions

### Route Files

Each route segment is defined by a folder. Special files within folders control behavior:

| File | Purpose |
|------|---------|
| `page.tsx` | Unique UI for a route, makes route publicly accessible |
| `layout.tsx` | Shared UI wrapper, preserves state across navigations |
| `loading.tsx` | Loading UI using React Suspense |
| `error.tsx` | Error boundary for route segment |
| `not-found.tsx` | UI for 404 responses |
| `template.tsx` | Like layout but re-renders on navigation |
| `default.tsx` | Fallback for parallel routes |

### Folder Conventions

| Pattern | Purpose | Example |
|---------|---------|---------|
| `folder/` | Route segment | `app/blog/` → `/blog` |
| `[folder]/` | Dynamic segment | `app/blog/[slug]/` → `/blog/:slug` |
| `[...folder]/` | Catch-all segment | `app/docs/[...slug]/` → `/docs/*` |
| `[[...folder]]/` | Optional catch-all | `app/shop/[[...slug]]/` → `/shop` or `/shop/*` |
| `(folder)/` | Route group (no URL) | `app/(marketing)/about/` → `/about` |
| `@folder/` | Named slot (parallel routes) | `app/@modal/login/` |
| `_folder/` | Private folder (excluded) | `app/_components/` |

## Creating Routes

### Basic Route Structure

To create a new route, add a folder with `page.tsx`:

```
app/
├── page.tsx              # / (home)
├── about/
│   └── page.tsx          # /about
└── blog/
    ├── page.tsx          # /blog
    └── [slug]/
        └── page.tsx      # /blog/:slug
```

### Page Component

A page is a Server Component by default:

```tsx
// app/about/page.tsx
export default function AboutPage() {
  return (
    <main>
      <h1>About Us</h1>
      <p>Welcome to our company.</p>
    </main>
  )
}
```

### Dynamic Routes

Access route parameters via the `params` prop:

```tsx
// app/blog/[slug]/page.tsx
interface PageProps {
  params: Promise<{ slug: string }>
}

export default async function BlogPost({ params }: PageProps) {
  const { slug } = await params
  const post = await getPost(slug)

  return <article>{post.content}</article>
}
```

## Layouts

### Root Layout (Required)

Every app needs a root layout with `<html>` and `<body>`:

```tsx
// app/layout.tsx
export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
```

### Nested Layouts

Layouts wrap their children and preserve state:

```tsx
// app/dashboard/layout.tsx
export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <div className="flex">
      <Sidebar />
      <main className="flex-1">{children}</main>
    </div>
  )
}
```

## Loading and Error States

### Loading UI

Create instant loading states with Suspense:

```tsx
// app/dashboard/loading.tsx
export default function Loading() {
  return <div className="animate-pulse">Loading...</div>
}
```

### Error Boundaries

Handle errors gracefully:

```tsx
// app/dashboard/error.tsx
'use client'

export default function Error({
  error,
  reset,
}: {
  error: Error
  reset: () => void
}) {
  return (
    <div>
      <h2>Something went wrong!</h2>
      <button onClick={reset}>Try again</button>
    </div>
  )
}
```

## Route Groups

Organize routes without affecting URL structure:

```
app/
├── (marketing)/
│   ├── layout.tsx        # Marketing layout
│   ├── about/page.tsx    # /about
│   └── contact/page.tsx  # /contact
└── (shop)/
    ├── layout.tsx        # Shop layout
    └── products/page.tsx # /products
```

## Metadata

### Static Metadata

```tsx
// app/about/page.tsx
import { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'About Us',
  description: 'Learn more about our company',
}
```

### Dynamic Metadata

```tsx
// app/blog/[slug]/page.tsx
export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { slug } = await params
  const post = await getPost(slug)
  return { title: post.title }
}
```

## Key Patterns

1. **Colocation**: Keep components, tests, and styles near routes
2. **Private folders**: Use `_folder` for non-route files
3. **Route groups**: Use `(folder)` to organize without URL impact
4. **Parallel routes**: Use `@slot` for complex layouts
5. **Intercepting routes**: Use `(.)` patterns for modals

## Resources

For detailed patterns, see:
- `references/routing-conventions.md` - Complete file conventions
- `references/layouts-templates.md` - Layout composition patterns
- `references/loading-error-states.md` - Suspense and error handling
- `examples/dynamic-routes.md` - Dynamic routing examples
- `examples/parallel-routes.md` - Parallel and intercepting routes
