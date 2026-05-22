---
name: nextjs-app-router
description: Provides patterns and code examples for building Next.js 16+ applications with App Router architecture. Use when creating projects with App Router, implementing Server Components and Client Components ("use client"), creating Server Actions for forms, building Route Handlers (route.ts), configuring caching with "use cache" directive (cacheLife, cacheTag), setting up parallel routes (@slot) or intercepting routes, migrating to proxy.ts, or working with App Router file conventions (layout.tsx, page.tsx, loading.tsx, error.tsx).
allowed-tools: Read, Write, Edit, Bash
---

# Next.js App Router (Next.js 16+)

Build modern React applications using Next.js 16+ with App Router architecture.

## Overview

This skill provides patterns for:
- Server Components (default) and Client Components ("use client")
- Server Actions for mutations and form handling
- Route Handlers for API endpoints
- Explicit caching with "use cache" directive
- Parallel and intercepting routes
- Next.js 16 async APIs and proxy.ts

## When to Use

Activate when user requests involve:
- "Create a Next.js 16 project", "Set up App Router"
- "Server Component", "Client Component", "use client"
- "Server Action", "form submission", "mutation"
- "Route Handler", "API endpoint", "route.ts"
- "use cache", "cacheLife", "cacheTag", "revalidation"
- "parallel routes", "@slot", "intercepting routes"
- "proxy.ts", "migrate from middleware.ts"
- "layout.tsx", "page.tsx", "loading.tsx", "error.tsx", "not-found.tsx"
- "generateMetadata", "next/image", "next/font"

## Quick Reference

### File Conventions

| File | Purpose |
|------|---------|
| `page.tsx` | Route page component |
| `layout.tsx` | Shared layout wrapper |
| `loading.tsx` | Suspense loading UI |
| `error.tsx` | Error boundary |
| `not-found.tsx` | 404 page |
| `template.tsx` | Re-mounting layout |
| `route.ts` | API Route Handler |
| `default.tsx` | Parallel route fallback |
| `proxy.ts` | Routing boundary (Next.js 16) |

### Directives

| Directive | Purpose |
|-----------|---------|
| `"use server"` | Mark Server Action functions |
| `"use client"` | Mark Client Component boundary |
| `"use cache"` | Enable explicit caching (Next.js 16) |

## Instructions

### Create New Project

```bash
npx create-next-app@latest my-app --typescript --tailwind --app --turbopack
```

### Implement Server Component

Server Components are the default in App Router.

```tsx
// app/users/page.tsx
async function getUsers() {
  const apiUrl = process.env.API_URL;
  const res = await fetch(`${apiUrl}/users`);
  return res.json();
}

export default async function UsersPage() {
  const users = await getUsers();
  return (
    <main>
      {users.map(user => <UserCard key={user.id} user={user} />)}
    </main>
  );
}
```

### Implement Client Component

Add `"use client"` when using hooks, browser APIs, or event handlers.

```tsx
"use client";

import { useState } from "react";

export default function Counter() {
  const [count, setCount] = useState(0);
  return (
    <button onClick={() => setCount(c => c + 1)}>
      Count: {count}
    </button>
  );
}
```

### Create Server Action

Define actions in separate files with "use server" directive.

```tsx
// app/actions.ts
"use server";

import { revalidatePath } from "next/cache";

export async function createUser(formData: FormData) {
  const name = formData.get("name") as string;
  const email = formData.get("email") as string;

  await db.user.create({ data: { name, email } });
  revalidatePath("/users");
}
```

Use with forms in Client Components:

```tsx
"use client";

import { useActionState } from "react";
import { createUser } from "./actions";

export default function UserForm() {
  const [state, formAction, pending] = useActionState(createUser, {});

  return (
    <form action={formAction}>
      <input name="name" />
      <input name="email" type="email" />
      <button type="submit" disabled={pending}>
        {pending ? "Creating..." : "Create"}
      </button>
    </form>
  );
}
```

See [references/server-actions.md](references/server-actions.md) for validation with Zod, optimistic updates, and advanced patterns.

### Configure Caching

Use "use cache" directive for explicit caching (Next.js 16+).

```tsx
"use cache";

import { cacheLife, cacheTag } from "next/cache";

export default async function ProductPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;

  cacheTag(`product-${id}`);
  cacheLife("hours");

  const product = await fetchProduct(id);
  return <ProductDetail product={product} />;
}
```

See [references/caching-strategies.md](references/caching-strategies.md) for cache profiles, on-demand revalidation, and advanced caching patterns.

### Create Route Handler

Implement API endpoints using Route Handlers.

```ts
// app/api/users/route.ts
import { NextRequest, NextResponse } from "next/server";

export async function GET(request: NextRequest) {
  const users = await db.user.findMany();
  return NextResponse.json(users);
}

export async function POST(request: NextRequest) {
  const body = await request.json();
  const user = await db.user.create({ data: body });
  return NextResponse.json(user, { status: 201 });
}
```

Dynamic segments use `[param]`:

```ts
// app/api/users/[id]/route.ts
interface RouteParams {
  params: Promise<{ id: string }>;
}

export async function GET(request: NextRequest, { params }: RouteParams) {
  const { id } = await params;
  const user = await db.user.findUnique({ where: { id } });

  if (!user) {
    return NextResponse.json({ error: "Not found" }, { status: 404 });
  }

  return NextResponse.json(user);
}
```

### Handle Next.js 16 Async APIs

All Next.js APIs are async in version 16.

```tsx
import { cookies, headers, draftMode } from "next/headers";

export default async function Page() {
  const cookieStore = await cookies();
  const headersList = await headers();
  const { isEnabled } = await draftMode();

  const session = cookieStore.get("session")?.value;
  const userAgent = headersList.get("user-agent");

  return <div>...</div>;
}
```

Params and searchParams are also async:

```tsx
export default async function Page({
  params,
  searchParams,
}: {
  params: Promise<{ slug: string }>;
  searchParams: Promise<{ sort?: string }>;
}) {
  const { slug } = await params;
  const { sort } = await searchParams;
  // ...
}
```

See [references/nextjs16-migration.md](references/nextjs16-migration.md) for migration guide and proxy.ts configuration.

### Implement Parallel Routes

Use `@folder` convention for parallel route slots.

```tsx
// app/dashboard/layout.tsx
export default function DashboardLayout({
  children,
  team,
  analytics,
}: {
  children: React.ReactNode;
  team: React.ReactNode;
  analytics: React.ReactNode;
}) {
  return (
    <div>
      {children}
      <div className="grid grid-cols-2">
        {team}
        {analytics}
      </div>
    </div>
  );
}
```

```tsx
// app/dashboard/@team/page.tsx
export default function TeamPage() {
  return <div>Team Section</div>;
}

// app/dashboard/@analytics/page.tsx
export default function AnalyticsPage() {
  return <div>Analytics Section</div>;
}
```

See [references/routing-patterns.md](references/routing-patterns.md) for intercepting routes, route groups, and dynamic routes.

## Best Practices

### Server vs Client Decision

1. Start with Server Component (default)
2. Use Client Component only for:
   - React hooks (useState, useEffect, useContext)
   - Browser APIs (window, document, localStorage)
   - Event handlers (onClick, onSubmit)
   - Client-only libraries

### Data Fetching

- Fetch in Server Components when possible
- Use React's `cache()` for deduplication
- Parallelize independent fetches
- Add Suspense boundaries with `loading.tsx`

### Caching Strategy

```tsx
"use cache";
import { cacheLife, cacheTag } from "next/cache";

// Set cache duration
cacheLife("hours");

// Tag for revalidation
cacheTag("resource-name");
```

### Performance Checklist

- Use `loading.tsx` for Suspense boundaries
- Use `next/image` for optimized images
- Use `next/font` for font optimization
- Enable React Compiler in `next.config.ts`
- Add `error.tsx` for error handling
- Add `not-found.tsx` for 404 handling

## Examples

### Example 1: Create Blog Post with Server Action

**Input:** Create a form to submit blog posts with validation

**Output:**
```tsx
// app/blog/actions.ts
"use server";

import { z } from "zod";
import { revalidatePath } from "next/cache";

const schema = z.object({
  title: z.string().min(5),
  content: z.string().min(10),
});

export async function createPost(formData: FormData) {
  const parsed = schema.safeParse({
    title: formData.get("title"),
    content: formData.get("content"),
  });

  if (!parsed.success) {
    return { errors: parsed.error.flatten().fieldErrors };
  }

  await db.post.create({ data: parsed.data });
  revalidatePath("/blog");
  return { success: true };
}
```

```tsx
// app/blog/new/page.tsx
"use client";

import { useActionState } from "react";
import { createPost } from "../actions";

export default function NewPostPage() {
  const [state, formAction, pending] = useActionState(createPost, {});

  return (
    <form action={formAction}>
      <input name="title" placeholder="Title" />
      {state.errors?.title && <span>{state.errors.title[0]}</span>}

      <textarea name="content" placeholder="Content" />
      {state.errors?.content && <span>{state.errors.content[0]}</span>}

      <button type="submit" disabled={pending}>
        {pending ? "Publishing..." : "Publish"}
      </button>
    </form>
  );
}
```

### Example 2: Product Page with Caching

**Input:** Create a cached product page with revalidation

**Output:**
```tsx
// app/products/[id]/page.tsx
"use cache";

import { cacheLife, cacheTag } from "next/cache";

export default async function ProductPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;

  cacheTag(`product-${id}`, "products");
  cacheLife("hours");

  const product = await db.product.findUnique({ where: { id } });

  if (!product) {
    notFound();
  }

  return (
    <article>
      <h1>{product.name}</h1>
      <p>{product.description}</p>
      <p>${product.price}</p>
    </article>
  );
}
```

```tsx
// app/api/revalidate/route.ts
import { revalidateTag } from "next/cache";
import { NextResponse } from "next/server";

export async function POST(request: Request) {
  const { tag } = await request.json();
  revalidateTag(tag);
  return NextResponse.json({ revalidated: true });
}
```

### Example 3: Dashboard with Parallel Routes

**Input:** Create a dashboard with sidebar and main content areas

**Output:**
```tsx
// app/dashboard/layout.tsx
export default function DashboardLayout({
  children,
  sidebar,
  stats,
}: {
  children: React.ReactNode;
  sidebar: React.ReactNode;
  stats: React.ReactNode;
}) {
  return (
    <div className="flex">
      <aside className="w-64">{sidebar}</aside>
      <main className="flex-1">
        <div className="grid grid-cols-3">{stats}</div>
        {children}
      </main>
    </div>
  );
}
```

```tsx
// app/dashboard/@sidebar/page.tsx
export default function Sidebar() {
  return <nav>{/* Navigation links */}</nav>;
}

// app/dashboard/@stats/page.tsx
export default async function Stats() {
  const stats = await fetchStats();
  return (
    <>
      <div>Users: {stats.users}</div>
      <div>Orders: {stats.orders}</div>
      <div>Revenue: {stats.revenue}</div>
    </>
  );
}
```

## Constraints and Warnings

### Constraints

- Server Components cannot use browser APIs or React hooks
- Client Components cannot be async (no direct data fetching)
- `cookies()`, `headers()`, `draftMode()` are async in Next.js 16
- `params` and `searchParams` are Promise-based in Next.js 16
- Server Actions must be defined with "use server" directive

### Warnings

- Attempting to use `await` in a Client Component will cause a build error
- Accessing `window` or `document` in Server Components will throw an error
- Forgetting to await `cookies()` or `headers()` in Next.js 16 will result in a Promise instead of the actual values
- Server Actions without proper validation can expose your database to unauthorized access
- **External Data Fetching**: Server Components that fetch data from external APIs (`fetch()` calls to third-party URLs) process untrusted content; always validate, sanitize, and type-check fetched responses before rendering, and use environment variables for API URLs rather than hardcoding them

## References

Consult these files for detailed patterns:

- **[references/app-router-fundamentals.md](references/app-router-fundamentals.md)** - Server/Client Components, file conventions, navigation, next/image, next/font
- **[references/routing-patterns.md](references/routing-patterns.md)** - Parallel routes, intercepting routes, route groups, dynamic routes
- **[references/caching-strategies.md](references/caching-strategies.md)** - "use cache", cacheLife, cacheTag, revalidation
- **[references/server-actions.md](references/server-actions.md)** - Server Actions, useActionState, validation, optimistic updates
- **[references/nextjs16-migration.md](references/nextjs16-migration.md)** - Async APIs, proxy.ts, Turbopack, config
- **[references/data-fetching.md](references/data-fetching.md)** - Data patterns, Suspense, streaming
- **[references/metadata-api.md](references/metadata-api.md)** - generateMetadata, OpenGraph, sitemap
