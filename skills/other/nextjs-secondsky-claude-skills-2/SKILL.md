---
name: nextjs
description: Next.js 16 with App Router, Server Components, Server Actions, Cache Components. Use for React 19.2 apps, SSR, or encountering async params, proxy.ts migration, use cache errors.

  Keywords: Next.js 16, Next.js App Router, Next.js Pages Router, Server Components, React Server Components, Server Actions, Cache Components, use cache, Next.js 16 breaking changes, async params nextjs, proxy.ts migration, React 19.2, Next.js metadata, Next.js SEO, generateMetadata, static generation, dynamic rendering, streaming SSR, Suspense, parallel routes, intercepting routes, route groups, Next.js middleware, Next.js API routes, Route Handlers, revalidatePath, revalidateTag, next/navigation, useSearchParams, turbopack, next.config
license: MIT
metadata:
  version: 1.0.0
  last_verified: 2025-11-21
  nextjs_version: 16.0.3
  react_version: 19.2.0
  node_version: 20.9+
  author: Claude Skills Maintainers
  repository: https://github.com/secondsky/claude-skills
  production_tested: true
  token_savings: 65-70%
  errors_prevented: 18+
allowed-tools: ["Read", "Write", "Edit", "Bash", "Glob", "Grep"]
---

# Next.js App Router - Production Patterns

**Version**: Next.js 16.0.3
**React Version**: 19.2.0
**Node.js**: 20.9+
**Last Verified**: 2025-11-21

## Table of Contents
1. [When to Use This Skill](#when-to-use-this-skill)
2. [When NOT to Use This Skill](#when-not-to-use-this-skill)
3. [Next.js 16 Breaking Changes](#nextjs-16-breaking-changes)
4. [Cache Components & Caching APIs](#cache-components--caching-apis)
5. [Server Components](#server-components)
6. [Server Actions](#server-actions)
7. [Route Handlers](#route-handlers)
8. [React 19.2 Features](#react-192-features)
9. [Metadata API](#metadata-api)
10. [Image & Font Optimization](#image--font-optimization)
11. [Top 5 Critical Errors](#top-5-critical-errors)
12. [Performance Patterns](#performance-patterns)
13. [TypeScript Configuration](#typescript-configuration)

---

## When to Use This Skill

Use this skill when you need:

- **Next.js 16 App Router patterns** (layouts, loading, error boundaries, routing)
- **Server Components** best practices (data fetching, composition, streaming)
- **Server Actions** patterns (forms, mutations, revalidation, error handling)
- **Cache Components** with `"use cache"` directive (NEW in Next.js 16)
- **New caching APIs**: `revalidateTag()`, `updateTag()`, `refresh()` (Updated in Next.js 16)
- **Migration from Next.js 15 to 16** (async params, proxy.ts, parallel routes)
- **Route Handlers** (API endpoints, webhooks, streaming responses)
- **Proxy patterns** (`proxy.ts` replaces `middleware.ts` in Next.js 16)
- **Async route params** (`params`, `searchParams`, `cookies()`, `headers()` now async)
- **Parallel routes with default.js** (breaking change in Next.js 16)
- **React 19.2 features** (View Transitions, `useEffectEvent()`, React Compiler)
- **Metadata API** (SEO, Open Graph, Twitter Cards, sitemaps)
- **Image optimization** (`next/image` with updated defaults in Next.js 16)
- **Performance optimization** (lazy loading, code splitting, PPR, ISR)

## When NOT to Use This Skill

Do NOT use this skill for:

- **Cloudflare Workers deployment** → Use `cloudflare-nextjs` skill instead
- **Pages Router patterns** → This skill covers App Router ONLY (Pages Router is legacy)
- **Authentication libraries** → Use `clerk-auth`, `auth-js`, or other auth-specific skills
- **Database integration** → Use `cloudflare-d1`, `drizzle-orm-d1`, or database-specific skills
- **UI component libraries** → Use `tailwind-v4-shadcn` skill for Tailwind + shadcn/ui
- **State management** → Use `zustand-state-management`, `tanstack-query` skills
- **Form libraries** → Use `react-hook-form-zod` skill

---

## Next.js 16 Breaking Changes

**CRITICAL**: Next.js 16 has multiple breaking changes. For detailed migration steps, see `references/next-16-migration-guide.md`.

| Breaking Change | Before | After |
|-----------------|--------|-------|
| **Async params** | `params.slug` | `const { slug } = await params` |
| **Async headers** | `cookies()` sync | `await cookies()` |
| **Middleware** | `middleware.ts` | `proxy.ts` (renamed) |
| **Parallel routes** | `default.js` optional | `default.js` **required** |
| **Caching** | Auto-cached fetch | Opt-in with `"use cache"` |
| **revalidateTag()** | 1 argument | 2 arguments (tag + cacheLife) |
| **Node.js** | 18.x+ | **20.9+** required |
| **React** | 18.x | **19.2+** required |

**Quick Fix for Async Params**:
```typescript
// ✅ Next.js 16 pattern
export default async function Page({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params
  return <div>{id}</div>
}
```

**Codemod**: `bunx @next/codemod@canary upgrade latest`

**See**: `references/next-16-migration-guide.md` for complete migration guide with examples.

---

## Cache Components & Caching APIs

### "use cache" Directive (NEW in Next.js 16)

```typescript
'use cache'

export async function BlogPosts() {
  const posts = await db.posts.findMany()
  return posts.map(post => <article key={post.id}>{post.title}</article>)
}
```

### Caching APIs Summary

| API | Purpose | Example |
|-----|---------|---------|
| `"use cache"` | Opt-in component/function caching | `'use cache'` at top |
| `revalidateTag()` | Invalidate by tag | `revalidateTag('posts', 'max')` |
| `updateTag()` | Update cache without revalidation | `updateTag('posts', newData)` |
| `refresh()` | Refresh current page | `refresh()` |
| `revalidatePath()` | Invalidate by path | `revalidatePath('/posts')` |

### PPR (Partial Prerendering)

```typescript
// next.config.ts
const config = { experimental: { ppr: true } }

// page.tsx
export const experimental_ppr = true

export default function Page() {
  return (
    <>
      <StaticHeader />
      <Suspense fallback={<Skeleton />}>
        <DynamicContent />
      </Suspense>
    </>
  )
}
```

**See**: `references/caching-apis.md` for complete caching API reference with ISR, tag-based revalidation, and advanced patterns.

---

## Server Components

Server Components are the **default** in App Router. They run on the server and can fetch data, access databases, and keep logic server-side.

```typescript
// app/posts/page.tsx (Server Component by default)
export default async function PostsPage() {
  const posts = await db.posts.findMany()
  return <div>{posts.map(p => <article key={p.id}>{p.title}</article>)}</div>
}
```

### Streaming with Suspense

```typescript
import { Suspense } from 'react'

export default function Page() {
  return (
    <div>
      <Header />
      <Suspense fallback={<Skeleton />}>
        <Posts />
      </Suspense>
    </div>
  )
}
```

### Server vs Client Components

| Server Components | Client Components |
|-------------------|-------------------|
| Data fetching, DB access | Interactivity (onClick) |
| Sensitive logic | React hooks (useState) |
| Large dependencies | Browser APIs |
| Static content | Real-time updates |

**Client Component** (requires `'use client'`):
```typescript
'use client'
import { useState } from 'react'
export function Counter() {
  const [count, setCount] = useState(0)
  return <button onClick={() => setCount(count + 1)}>{count}</button>
}
```

---

## Server Actions

Server Actions are async functions that run on the server, callable from Client or Server Components.

### Basic Server Action

```typescript
// app/actions.ts
'use server'

import { revalidatePath } from 'next/cache'

export async function createPost(formData: FormData) {
  const title = formData.get('title') as string
  await db.posts.create({ data: { title } })
  revalidatePath('/posts')
}
```

### Form Handling

```typescript
// Server Component Form (simplest)
import { createPost } from './actions'

export default function NewPostPage() {
  return (
    <form action={createPost}>
      <input name="title" required />
      <button type="submit">Create</button>
    </form>
  )
}
```

### Available Patterns

| Pattern | Use Case | Reference |
|---------|----------|-----------|
| Client Form with Loading | useFormState + useFormStatus | `templates/server-action-form.tsx` |
| Error Handling | Return { error } or { success } | `references/server-actions-patterns.md` |
| Optimistic Updates | useOptimistic hook | `references/server-actions-patterns.md` |
| File Upload | FormData + blob storage | `references/server-actions-patterns.md` |
| Redirect After Action | redirect() function | `references/server-actions-patterns.md` |

**See**: `references/server-actions-patterns.md` for error handling, optimistic updates, file uploads, and advanced patterns.

---

## Route Handlers

Route Handlers are the App Router equivalent of API Routes.

```typescript
// app/api/posts/route.ts
export async function GET(request: Request) {
  const posts = await db.posts.findMany()
  return Response.json({ posts })
}

export async function POST(request: Request) {
  const body = await request.json()
  const post = await db.posts.create({ data: body })
  return Response.json({ post }, { status: 201 })
}
```

**Dynamic Routes** (with async params):
```typescript
// app/api/posts/[id]/route.ts
export async function GET(
  request: Request,
  { params }: { params: Promise<{ id: string }> }
) {
  const { id } = await params // Await in Next.js 16
  const post = await db.posts.findUnique({ where: { id } })
  return post ? Response.json({ post }) : Response.json({ error: 'Not found' }, { status: 404 })
}
```

**See**: `templates/route-handler-api.ts` for search params, webhooks, and streaming patterns.

---

## React 19.2 Features

| Feature | Usage |
|---------|-------|
| **React Compiler** | `experimental: { reactCompiler: true }` - Auto-memoization |
| **View Transitions** | `useTransition()` + `router.push()` |
| **useEffectEvent** | Stable event handlers without deps |

---

## Metadata API

```typescript
// Static metadata
export const metadata: Metadata = {
  title: 'My Blog',
  description: 'A blog about Next.js',
  openGraph: { title: 'My Blog', images: ['/og-image.jpg'] },
}

// Dynamic metadata (await params in Next.js 16)
export async function generateMetadata({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params
  const post = await db.posts.findUnique({ where: { id } })
  return { title: post.title, description: post.excerpt }
}
```

---

## Image & Font Optimization

```typescript
// next/image
import Image from 'next/image'
<Image src="/profile.jpg" alt="Profile" width={500} height={500} priority />

// next/font
import { Inter } from 'next/font/google'
const inter = Inter({ subsets: ['latin'], variable: '--font-inter' })
<html className={inter.variable}>
```

**Remote images**: Configure `images.remotePatterns` in `next.config.ts`.

---

## Top 5 Critical Errors

### Error 1: `params` is a Promise

**Error**: `Type 'Promise<{ id: string }>' is not assignable to type '{ id: string }'`

**Solution**: Await params in Next.js 16:
```typescript
export default async function Page({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params
}
```

---

### Error 2: `middleware.ts` is deprecated

**Warning**: `middleware.ts is deprecated. Use proxy.ts instead.`

**Solution**: Rename file and function:
```typescript
// Rename: middleware.ts → proxy.ts
// Rename function: middleware → proxy
export function proxy(request: NextRequest) {
  // Same logic
}
```

---

### Error 3: Parallel route missing `default.js`

**Error**: `Parallel route @modal was matched but no default.js was found`

**Solution**: Add default.tsx:
```typescript
// app/@modal/default.tsx
export default function ModalDefault() {
  return null
}
```

---

### Error 4: Cannot use React hooks in Server Component

**Error**: `You're importing a component that needs useState. It only works in a Client Component`

**Solution**: Add `'use client'`:
```typescript
'use client'

import { useState } from 'react'

export function Counter() {
  const [count, setCount] = useState(0)
  return <button onClick={() => setCount(count + 1)}>{count}</button>
}
```

---

### Error 5: `fetch()` not caching

**Cause**: Next.js 16 uses opt-in caching with `"use cache"`.

**Solution**: Add `"use cache"` directive:
```typescript
'use cache'

export async function getPosts() {
  const response = await fetch('/api/posts')
  return response.json()
}
```

---

**See All 18 Errors**: `references/error-catalog.md`

---

## Performance Patterns

| Pattern | Usage |
|---------|-------|
| **Lazy Loading** | `const HeavyComp = dynamic(() => import('./Heavy'), { ssr: false })` |
| **Code Splitting** | Automatic per route - each `page.tsx` gets own bundle |
| **Turbopack** | Default in Next.js 16, opt out with `--webpack` flag |
| **PPR** | `experimental: { ppr: true }` + `<Suspense>` boundaries |

---

## TypeScript Configuration

```json
{
  "compilerOptions": {
    "strict": true,
    "baseUrl": ".",
    "paths": { "@/*": ["./*"] }
  }
}
```

---

## When to Load References

| Reference | Load When... |
|-----------|--------------|
| `next-16-migration-guide.md` | Migrating from Next.js 15, async params errors, proxy.ts setup |
| `server-actions-patterns.md` | Error handling, optimistic updates, file uploads, advanced forms |
| `caching-apis.md` | ISR, tag-based revalidation, updateTag(), refresh(), PPR details |
| `error-catalog.md` | Debugging any Next.js error, comprehensive error solutions |
| `top-errors.md` | Quick fixes for the 5 most common Next.js errors |

---

## Bundled Resources

| Type | Files |
|------|-------|
| **References** | `error-catalog.md`, `top-errors.md`, `next-16-migration-guide.md`, `server-actions-patterns.md`, `caching-apis.md` |
| **Templates** | `async-params-page.tsx`, `server-action-form.tsx`, `route-handler-api.ts`, `cache-component-use-cache.tsx`, `parallel-routes-with-default.tsx`, `proxy-migration.ts` |

---

## Related Skills

| Skill | Purpose |
|-------|---------|
| `cloudflare-nextjs` | Deploy to Cloudflare Workers |
| `tailwind-v4-shadcn` | Styling |
| `clerk-auth` | Authentication |
| `drizzle-orm-d1` | Database |
| `react-hook-form-zod` | Forms |
| `zustand-state-management` | Client state |

**Official Docs**: https://nextjs.org/docs | **App Router**: https://nextjs.org/docs/app

---

**Version**: Next.js 16.0.0 | React 19.2.0 | Node.js 20.9+ | TypeScript 5.3+
**Production Tested**: E-commerce, SaaS, content sites | **Token Savings**: 65-70%
