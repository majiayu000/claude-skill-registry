---
name: "Next.js App Router Development"
description: "Build Next.js applications with App Router, Server and Client Components, data fetching, routing, and TypeScript. Use when implementing Next.js pages, layouts, API routes, or React Server Components."
tools: Read, Grep, Glob, Write, Edit, Bash
model: inherit
---

# Skill: Next.js App Router Development

Complete guide for building Next.js applications using the App Router architecture with Server and Client Components, data fetching, routing, and navigation.

## When to Use

- Creating new pages or layouts in Next.js App Router
- Implementing Server and Client Component patterns
- Setting up data fetching with Server Components
- Building API route handlers
- Implementing navigation and routing
- Debugging Next.js-specific issues
- Working with dynamic routes and params

## Domain Knowledge

### Critical Patterns

#### Server vs Client Components (CRITICAL)

In Next.js App Router, components are **Server Components by default**.

**Server Components:**
- Default behavior (no directive needed)
- Render on server only
- Can be async for data fetching
- Cannot use React hooks (useState, useEffect, etc.)
- Cannot use browser APIs
- Better performance (smaller bundle size)

**Client Components:**
- Require `"use client"` directive at top of file
- Render on both server and client
- Can use React hooks (useState, useEffect, etc.)
- Can use browser APIs
- Required for interactivity

```typescript
// Server Component (default)
async function ServerPage() {
  const data = await fetchData(); // Can be async
  return <div>{data}</div>;
}

// Client Component
"use client";
import { useState } from "react";

function ClientComponent() {
  const [count, setCount] = useState(0); // Can use hooks
  return <button onClick={() => setCount(count + 1)}>{count}</button>;
}
```

**Rule**: Use Server Components by default, only use Client Components when you need:
- React hooks (useState, useEffect, etc.)
- Event handlers (onClick, onChange, etc.)
- Browser APIs (window, localStorage, etc.)
- Third-party libraries that use hooks

#### Async Server Components for Data Fetching

Server Components can be async, enabling direct data fetching:

```typescript
// ✅ Correct - async Server Component
async function UserProfile({ userId }: { userId: string }) {
  const user = await fetchUser(userId);
  return <div>{user.name}</div>;
}

// ❌ Wrong - using useEffect in Server Component
function UserProfile({ userId }: { userId: string }) {
  const [user, setUser] = useState(null);

  useEffect(() => {
    fetchUser(userId).then(setUser); // This will error
  }, [userId]);

  return <div>{user?.name}</div>;
}
```

**Why**: Server Components don't support hooks. Use async/await directly instead.

#### Server to Client Data Flow

Pass data from Server Components to Client Components via props:

```typescript
// Server Component (page.tsx)
async function Page() {
  const data = await fetchData(); // Fetch on server

  return <ClientComponent data={data} />; // Pass via props
}

// Client Component
"use client";
function ClientComponent({ data }: { data: Data }) {
  const [selected, setSelected] = useState(null);

  return (
    <div onClick={() => setSelected(data.id)}>
      {data.name}
    </div>
  );
}
```

**Rule**: Server Components fetch data, Client Components handle interactivity.

#### Navigation Hooks (Client Only)

Navigation hooks can ONLY be used in Client Components:

```typescript
"use client";
import { useRouter, usePathname, useSearchParams } from "next/navigation";

function Navigation() {
  const router = useRouter();
  const pathname = usePathname();
  const searchParams = useSearchParams();

  return (
    <button onClick={() => router.push("/dashboard")}>
      Go to Dashboard
    </button>
  );
}
```

**Common imports:**
- Import from `"next/navigation"` (NOT `"next/router"`)
- `useRouter` - programmatic navigation
- `usePathname` - current path
- `useSearchParams` - URL query params

#### Awaiting Params in Next.js 15+ (CRITICAL)

In Next.js 15+, dynamic route params and searchParams MUST be awaited:

```typescript
// ❌ Wrong - synchronous params (Next.js 14 pattern)
export default function Page({ params }: { params: { id: string } }) {
  return <div>Post {params.id}</div>;
}

// ✅ Correct - async params (Next.js 15+)
export default async function Page({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  return <div>Post {id}</div>;
}
```

**searchParams also need awaiting:**
```typescript
export default async function Page({
  searchParams,
}: {
  searchParams: Promise<{ query?: string }>;
}) {
  const { query } = await searchParams;
  return <div>Search: {query}</div>;
}
```

**Why**: Next.js 15 made params async for better streaming and performance.

### Key Files

- **app/layout.tsx** - Root layout (wraps all pages)
- **app/page.tsx** - Home page
- **app/[dynamic]/page.tsx** - Dynamic route page
- **app/api/[route]/route.ts** - API route handler
- **middleware.ts** - Middleware for auth, redirects, etc.
- **next.config.ts** - Next.js configuration

### File-Based Routing

```
app/
├── page.tsx                 → /
├── about/page.tsx          → /about
├── blog/
│   ├── page.tsx            → /blog
│   └── [slug]/page.tsx     → /blog/[slug]
├── dashboard/
│   ├── layout.tsx          → Layout for /dashboard/*
│   └── page.tsx            → /dashboard
└── api/
    └── users/route.ts      → /api/users
```

**Special Files:**
- `page.tsx` - Route page
- `layout.tsx` - Shared layout
- `loading.tsx` - Loading UI
- `error.tsx` - Error UI
- `not-found.tsx` - 404 UI
- `route.ts` - API endpoint

## Workflows

### Workflow 1: Create New Page with Data Fetching

**Step 1: Create Page File**

```typescript
// app/posts/page.tsx
import { api } from "@/convex/_generated/api";
import { fetchQuery } from "convex/nextjs";

export default async function PostsPage() {
  // Fetch data on server
  const posts = await fetchQuery(api.posts.list);

  return (
    <div>
      <h1>Posts</h1>
      <PostList posts={posts} />
    </div>
  );
}
```

**Step 2: Create Client Component for Interactivity**

```typescript
// app/posts/PostList.tsx
"use client";
import { useState } from "react";

export function PostList({ posts }: { posts: Post[] }) {
  const [filter, setFilter] = useState("");

  const filtered = posts.filter(p =>
    p.title.toLowerCase().includes(filter.toLowerCase())
  );

  return (
    <div>
      <input
        type="text"
        value={filter}
        onChange={(e) => setFilter(e.target.value)}
        placeholder="Filter posts..."
      />
      {filtered.map(post => (
        <PostCard key={post._id} post={post} />
      ))}
    </div>
  );
}
```

**Step 3: Add Loading State**

```typescript
// app/posts/loading.tsx
export default function Loading() {
  return <div>Loading posts...</div>;
}
```

**Step 4: Add Error Handling**

```typescript
// app/posts/error.tsx
"use client";

export default function Error({
  error,
  reset,
}: {
  error: Error;
  reset: () => void;
}) {
  return (
    <div>
      <h2>Something went wrong!</h2>
      <p>{error.message}</p>
      <button onClick={reset}>Try again</button>
    </div>
  );
}
```

### Workflow 2: Create Dynamic Route

**Step 1: Create Dynamic Route File**

```typescript
// app/posts/[id]/page.tsx
import { api } from "@/convex/_generated/api";
import { fetchQuery } from "convex/nextjs";
import { Id } from "@/convex/_generated/dataModel";

export default async function PostPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  // CRITICAL: Await params in Next.js 15+
  const { id } = await params;

  // Fetch post data
  const post = await fetchQuery(api.posts.get, {
    id: id as Id<"posts">
  });

  if (!post) {
    return <div>Post not found</div>;
  }

  return (
    <article>
      <h1>{post.title}</h1>
      <p>{post.content}</p>
    </article>
  );
}
```

**Step 2: Generate Static Params (Optional)**

For static site generation, provide all possible params:

```typescript
// app/posts/[id]/page.tsx
export async function generateStaticParams() {
  const posts = await fetchQuery(api.posts.list);

  return posts.map((post) => ({
    id: post._id,
  }));
}
```

**Step 3: Add Metadata**

```typescript
export async function generateMetadata({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  const post = await fetchQuery(api.posts.get, { id: id as Id<"posts"> });

  return {
    title: post.title,
    description: post.excerpt,
  };
}
```

### Workflow 3: Create API Route Handler

**Step 1: Create Route File**

```typescript
// app/api/users/route.ts
import { NextRequest, NextResponse } from "next/server";

export async function GET(request: NextRequest) {
  try {
    // Get query params
    const searchParams = request.nextUrl.searchParams;
    const query = searchParams.get("query");

    // Fetch data
    const users = await fetchUsers(query);

    return NextResponse.json({ users });
  } catch (error) {
    return NextResponse.json(
      { error: "Failed to fetch users" },
      { status: 500 }
    );
  }
}

export async function POST(request: NextRequest) {
  try {
    // Parse body
    const body = await request.json();

    // Validate
    if (!body.name || !body.email) {
      return NextResponse.json(
        { error: "Name and email required" },
        { status: 400 }
      );
    }

    // Create user
    const user = await createUser(body);

    return NextResponse.json({ user }, { status: 201 });
  } catch (error) {
    return NextResponse.json(
      { error: "Failed to create user" },
      { status: 500 }
    );
  }
}
```

**Step 2: Use Route from Frontend**

```typescript
// In Client Component
const response = await fetch("/api/users", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ name, email }),
});

const { user } = await response.json();
```

### Workflow 4: Implement Protected Route

**Step 1: Create Middleware**

```typescript
// middleware.ts
import { clerkMiddleware, createRouteMatcher } from "@clerk/nextjs/server";

const isProtectedRoute = createRouteMatcher([
  "/dashboard(.*)",
  "/api/protected(.*)",
]);

export default clerkMiddleware((auth, req) => {
  if (isProtectedRoute(req)) auth().protect();
});

export const config = {
  matcher: ["/((?!.*\\..*|_next).*)", "/", "/(api|trpc)(.*)"],
};
```

**Step 2: Access User in Server Component**

```typescript
// app/dashboard/page.tsx
import { auth } from "@clerk/nextjs/server";

export default async function Dashboard() {
  const { userId } = await auth();

  if (!userId) {
    redirect("/sign-in");
  }

  const userData = await fetchUserData(userId);

  return (
    <div>
      <h1>Dashboard</h1>
      <p>Welcome, {userData.name}</p>
    </div>
  );
}
```

**Step 3: Access User in Client Component**

```typescript
// app/dashboard/UserProfile.tsx
"use client";
import { useUser } from "@clerk/nextjs";

export function UserProfile() {
  const { user } = useUser();

  if (!user) return null;

  return (
    <div>
      <img src={user.imageUrl} alt={user.fullName} />
      <p>{user.emailAddresses[0].emailAddress}</p>
    </div>
  );
}
```

### Workflow 5: Implement Navigation

**Step 1: Use Link Component for Navigation**

```typescript
import Link from "next/link";

export function Navigation() {
  return (
    <nav>
      <Link href="/">Home</Link>
      <Link href="/about">About</Link>
      <Link href="/blog">Blog</Link>
    </nav>
  );
}
```

**Step 2: Programmatic Navigation in Client Component**

```typescript
"use client";
import { useRouter } from "next/navigation";

export function LoginForm() {
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    await login();
    router.push("/dashboard"); // Navigate after login
  };

  return <form onSubmit={handleSubmit}>...</form>;
}
```

**Step 3: Access Current Route Information**

```typescript
"use client";
import { usePathname, useSearchParams } from "next/navigation";

export function ActiveLink({ href, children }) {
  const pathname = usePathname();
  const isActive = pathname === href;

  return (
    <Link
      href={href}
      className={isActive ? "active" : ""}
    >
      {children}
    </Link>
  );
}
```

## Troubleshooting

### Issue: Cannot Use useState/useEffect in Component

**Symptoms:**
- Error: "You're importing a component that needs useState/useEffect"
- Hooks not working in component

**Cause:** Component is a Server Component (default), which doesn't support React hooks

**Solution:**

Add `"use client"` directive at the top of the file:

```typescript
// ❌ Wrong - Server Component trying to use hooks
import { useState } from "react";

export function Counter() {
  const [count, setCount] = useState(0); // Error!
  return <button onClick={() => setCount(count + 1)}>{count}</button>;
}

// ✅ Correct - Client Component
"use client";
import { useState } from "react";

export function Counter() {
  const [count, setCount] = useState(0);
  return <button onClick={() => setCount(count + 1)}>{count}</button>;
}
```

**Frequency:** High (very common mistake)

### Issue: Navigation Hooks Not Found

**Symptoms:**
- Error: "useRouter not found"
- Import error for navigation hooks

**Cause:** Importing from wrong package or using in Server Component

**Solution:**

1. Import from `"next/navigation"` (NOT `"next/router"`):
```typescript
// ❌ Wrong
import { useRouter } from "next/router";

// ✅ Correct
import { useRouter } from "next/navigation";
```

2. Ensure component is a Client Component:
```typescript
"use client";
import { useRouter } from "next/navigation";
```

**Frequency:** Medium

### Issue: Params is Promise Error

**Symptoms:**
- Error: "Type 'Promise<{...}>' is not assignable to type '{...}'"
- Params accessed before awaiting

**Cause:** In Next.js 15+, params is now a Promise that must be awaited

**Solution:**

```typescript
// ❌ Wrong - synchronous access (Next.js 14)
export default function Page({ params }: { params: { id: string } }) {
  return <div>{params.id}</div>;
}

// ✅ Correct - async/await (Next.js 15+)
export default async function Page({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  return <div>{id}</div>;
}
```

**Frequency:** High (common with Next.js 15 upgrade)

### Issue: Hydration Mismatch

**Symptoms:**
- Error: "Text content does not match server-rendered HTML"
- UI briefly shows incorrect content then corrects itself

**Cause:** Server and client rendering different content

**Common causes:**
1. Using `Date.now()` or random values
2. Accessing browser APIs during render
3. Conditional rendering based on browser state

**Solution:**

```typescript
// ❌ Wrong - causes hydration mismatch
function Component() {
  return <div>{Date.now()}</div>; // Different on server vs client
}

// ✅ Correct - use useEffect for client-only values
"use client";
import { useState, useEffect } from "react";

function Component() {
  const [time, setTime] = useState<number | null>(null);

  useEffect(() => {
    setTime(Date.now());
  }, []);

  return <div>{time ?? "Loading..."}</div>;
}
```

**Frequency:** Medium

## Validation Checklist

Before considering Next.js implementation complete:

- [ ] Server Components are used by default (no unnecessary "use client")
- [ ] Client Components have "use client" directive where needed
- [ ] Data fetching uses async Server Components (not useEffect)
- [ ] Navigation hooks only used in Client Components
- [ ] Params and searchParams are awaited in Next.js 15+
- [ ] Links use next/link for client-side navigation
- [ ] API routes have proper error handling
- [ ] Protected routes use middleware for authentication
- [ ] Loading states implemented with loading.tsx
- [ ] Error handling implemented with error.tsx
- [ ] Metadata configured for SEO

## Best Practices

1. **Default to Server Components** - Only use Client Components when necessary
2. **Colocate Server and Client** - Mix Server and Client Components in the same tree
3. **Fetch on the server** - Use async Server Components instead of useEffect
4. **Use Next.js Link** - Client-side navigation for better UX
5. **Implement loading states** - Create loading.tsx for better perceived performance
6. **Handle errors properly** - Use error.tsx for graceful error handling
7. **Protect routes with middleware** - Don't rely on client-side checks alone
8. **Type everything** - Use TypeScript for better DX and fewer bugs

## References

- **Previous expertise**: `.claude/experts/nextjs-expert/expertise.yaml`
- **Agent integration**: `.claude/agents/agent-nextjs.md`
- **Official docs**: https://nextjs.org/docs
