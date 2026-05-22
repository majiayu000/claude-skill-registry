---
name: nextjs-project-manager
description: Expert guide for Next.js 14+ App Router projects. Use when building features, routing, server/client components, forms, layouts, or debugging Next.js-specific issues.
---

# Next.js Project Manager Skill

## Overview

This skill helps you build production-ready Next.js 14+ applications using the App Router. Use this when working on routing, components, server actions, data fetching, or any Next.js-specific patterns.

## Core Principles

### 1. App Router First
- All routes in `src/app/` directory
- Use `page.tsx` for routes, `layout.tsx` for shared layouts
- Server Components by default, Client Components when needed
- Route groups with `(group)` for organization

### 2. Server vs Client Components

**Server Components (Default):**
- No "use client" directive needed
- Can use async/await directly
- Access database/backend directly
- Better performance (less JS sent to client)
- Cannot use hooks or browser APIs

**Client Components ("use client"):**
- Use when you need:
  - State (useState, useReducer)
  - Effects (useEffect)
  - Event handlers (onClick, onChange)
  - Browser APIs (localStorage, window)
  - Third-party libraries that use hooks

### 3. Data Fetching Patterns

**Server Components:**
```typescript
// Direct async fetch in component
export default async function Page() {
  const data = await fetch('https://api.example.com/data')
  const json = await data.json()
  return <div>{json.title}</div>
}
```

**Client Components:**
```typescript
'use client'
import { useEffect, useState } from 'react'

export default function Page() {
  const [data, setData] = useState(null)

  useEffect(() => {
    fetch('/api/data')
      .then(res => res.json())
      .then(setData)
  }, [])

  return <div>{data?.title}</div>
}
```

### 4. Server Actions

Use Server Actions for form submissions and mutations:

```typescript
// app/actions.ts
'use server'

export async function createItem(formData: FormData) {
  const title = formData.get('title')
  // Database operation
  await db.insert({ title })
  revalidatePath('/items')
  redirect('/items')
}

// app/form.tsx
'use client'
import { createItem } from './actions'

export function Form() {
  return (
    <form action={createItem}>
      <input name="title" />
      <button type="submit">Create</button>
    </form>
  )
}
```

## Common Patterns

### Route Structure

```
src/app/
├── (auth)/
│   ├── login/
│   │   └── page.tsx
│   └── signup/
│       └── page.tsx
├── (dashboard)/
│   ├── layout.tsx          # Shared dashboard layout
│   ├── page.tsx            # Dashboard home
│   └── settings/
│       └── page.tsx
├── api/
│   └── endpoint/
│       └── route.ts        # API routes
├── layout.tsx              # Root layout
└── page.tsx                # Home page
```

### Layouts

```typescript
// app/(dashboard)/layout.tsx
import { Sidebar } from '@/components/sidebar'

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

### Loading States

```typescript
// app/dashboard/loading.tsx
export default function Loading() {
  return <div>Loading...</div>
}
```

### Error Handling

```typescript
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

### Metadata

```typescript
// app/page.tsx
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Page Title',
  description: 'Page description',
}

export default function Page() {
  return <div>Content</div>
}
```

## API Routes

```typescript
// app/api/items/route.ts
import { NextRequest, NextResponse } from 'next/server'

export async function GET(request: NextRequest) {
  const items = await db.getItems()
  return NextResponse.json({ items })
}

export async function POST(request: NextRequest) {
  const body = await request.json()
  const item = await db.createItem(body)
  return NextResponse.json({ item }, { status: 201 })
}
```

## Dynamic Routes

```typescript
// app/posts/[id]/page.tsx
export default function Post({ params }: { params: { id: string } }) {
  return <div>Post {params.id}</div>
}

// Generate static params
export async function generateStaticParams() {
  const posts = await getPosts()
  return posts.map((post) => ({ id: post.id }))
}
```

## Middleware

```typescript
// middleware.ts
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export function middleware(request: NextRequest) {
  // Check auth, redirect, rewrite, etc.
  return NextResponse.next()
}

export const config = {
  matcher: '/dashboard/:path*',
}
```

## Environment Variables

```typescript
// Access in Server Components or Server Actions
const apiKey = process.env.API_KEY

// Access in Client Components (must be prefixed with NEXT_PUBLIC_)
const publicKey = process.env.NEXT_PUBLIC_API_KEY
```

## Best Practices Checklist

- [ ] Use Server Components by default
- [ ] Add "use client" only when necessary
- [ ] Use Server Actions for mutations
- [ ] Implement loading.tsx for loading states
- [ ] Implement error.tsx for error boundaries
- [ ] Use route groups for organization
- [ ] Add metadata to all pages
- [ ] Use TypeScript for type safety
- [ ] Implement proper error handling
- [ ] Use middleware for auth checks
- [ ] Optimize images with next/image
- [ ] Use dynamic imports for large components

## Debugging Tips

1. **Hydration Errors**: Check for server/client mismatches
2. **"use client" Errors**: Missing directive on component using hooks
3. **Cannot Access Browser APIs**: Move to client component
4. **Data Not Updating**: Use revalidatePath() or revalidateTag()
5. **Build Errors**: Check for async components without proper typing

## Performance Optimization

- Use React Suspense for loading states
- Implement streaming with loading.tsx
- Use dynamic imports for code splitting
- Optimize images with next/image
- Use Font optimization with next/font
- Implement ISR (Incremental Static Regeneration)
- Use caching with fetch options

## When to Use This Skill

Invoke this skill when:
- Creating new routes or pages
- Setting up layouts
- Implementing forms with Server Actions
- Debugging Next.js-specific errors
- Optimizing performance
- Setting up middleware
- Creating API routes
- Working with metadata
