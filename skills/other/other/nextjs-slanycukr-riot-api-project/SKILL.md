---
name: Next.js 15
description: Modern React framework for building full-stack web applications with App Router, Server Components, and optimized performance
when_to_use: Building React applications with server-side rendering, static site generation, API routes, or full-stack applications
---

# Next.js 15

Next.js is a React framework that provides server-side rendering, static site generation, API routes, and many other features for building modern web applications.

## Quick Start (App Router)

```bash
npx create-next-app@latest my-app
cd my-app
npm run dev
```

## Core Concepts

### Server vs Client Components

**Server Components** (default):

- Run on the server
- Can access server-side resources (database, files)
- No JavaScript sent to client
- Can use async/await directly

```tsx
// app/page.tsx
async function getPosts() {
  const res = await fetch("https://api.example.com/posts");
  return res.json();
}

export default async function Page() {
  const posts = await getPosts();
  return <PostList posts={posts} />;
}
```

**Client Components** (with 'use client'):

- Run on client and server
- Can use state, effects, browser APIs
- JavaScript sent to client

```tsx
// components/Counter.tsx
"use client";

import { useState } from "react";

export default function Counter() {
  const [count, setCount] = useState(0);
  return <button onClick={() => setCount(count + 1)}>Count: {count}</button>;
}
```

### Data Fetching Patterns

**Static Data (Default)**:

```tsx
// Cached until manually invalidated
export default async function Page() {
  const data = await fetch("https://api.example.com/posts");
  return <PostsList posts={await data.json()} />;
}
```

**Dynamic Data (No Cache)**:

```tsx
// Refetched on every request
export default async function Page() {
  const data = await fetch("https://api.example.com/posts", {
    cache: "no-store",
  });
  return <PostsList posts={await data.json()} />;
}
```

**Revalidated Data**:

```tsx
// Revalidated every 60 seconds
export default async function Page() {
  const data = await fetch("https://api.example.com/posts", {
    next: { revalidate: 60 },
  });
  return <PostsList posts={await data.json()} />;
}
```

### Route Handlers (API Routes)

Create API endpoints in the `app` directory:

```tsx
// app/api/posts/route.ts
import { NextResponse } from "next/server";

export async function GET() {
  const res = await fetch("https://api.example.com/posts");
  const posts = await res.json();
  return NextResponse.json(posts);
}

export async function POST(request: Request) {
  const body = await request.json();
  // Create post logic
  return NextResponse.json({ success: true });
}
```

### Layouts and Routing

**Root Layout**:

```tsx
// app/layout.tsx
export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        <Header />
        <main>{children}</main>
        <Footer />
      </body>
    </html>
  );
}
```

**Dynamic Routes**:

```tsx
// app/blog/[slug]/page.tsx
export default async function BlogPost({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  const post = await getPost(slug);
  return <article>{post.content}</article>;
}
```

### Navigation

```tsx
import Link from "next/link";
import { useRouter } from "next/navigation";

function Navigation() {
  const router = useRouter();

  return (
    <nav>
      <Link href="/about">About</Link>
      <Link href="/blog/[slug]" as="/blog/hello-world">
        Blog Post
      </Link>
      <button onClick={() => router.push("/dashboard")}>Dashboard</button>
    </nav>
  );
}
```

### Loading and Error States

**Loading UI**:

```tsx
// app/dashboard/loading.tsx
export default function Loading() {
  return <div>Loading dashboard...</div>;
}
```

**Error Handling**:

```tsx
// app/dashboard/error.tsx
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
      <button onClick={() => reset()}>Try again</button>
    </div>
  );
}
```

### Server Actions

```tsx
// app/actions.ts
"use server";

export async function createPost(formData: FormData) {
  const title = formData.get("title") as string;
  // Database operation
  revalidatePath("/blog"); // Update cache
}

// Usage in component
export default function CreatePostForm() {
  return (
    <form action={createPost}>
      <input name="title" />
      <button type="submit">Create Post</button>
    </form>
  );
}
```

## Practical Examples

### E-commerce Product Page

```tsx
// app/products/[id]/page.tsx
import Image from "next/image";
import AddToCart from "./add-to-cart";

async function getProduct(id: string) {
  const res = await fetch(`https://api.example.com/products/${id}`);
  return res.json();
}

export default async function ProductPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  const product = await getProduct(id);

  return (
    <div>
      <Image src={product.image} alt={product.name} width={300} height={300} />
      <h1>{product.name}</h1>
      <p>{product.description}</p>
      <p>${product.price}</p>
      <AddToCart productId={product.id} />
    </div>
  );
}
```

### Blog with Search

```tsx
// app/blog/page.tsx
import BlogList from "./blog-list";
import SearchForm from "./search-form";

export default async function BlogPage({
  searchParams,
}: {
  searchParams: Promise<{ query?: string }>;
}) {
  const { query } = await searchParams;
  const posts = await getPosts(query);

  return (
    <div>
      <SearchForm initialQuery={query} />
      <BlogList posts={posts} />
    </div>
  );
}
```

### Dashboard with Real-time Data

```tsx
// app/dashboard/page.tsx
import { Suspense } from "react";
import StatsCard from "./stats-card";
import RecentActivity from "./recent-activity";

export default function Dashboard() {
  return (
    <div>
      <h1>Dashboard</h1>
      <Suspense fallback={<div>Loading stats...</div>}>
        <StatsCard />
      </Suspense>
      <Suspense fallback={<div>Loading activity...</div>}>
        <RecentActivity />
      </Suspense>
    </div>
  );
}
```

## Requirements

- Node.js 18.17+ or 20+
- React 18+
- TypeScript (recommended)
- Modern web browser

## Key Features

- **App Router**: New routing model with Server Components
- **Server Components**: Reduced client-side JavaScript
- **Streaming**: Progressive rendering with Suspense
- **Route Handlers**: Built-in API routes
- **Server Actions**: Form handling and mutations
- **Optimized Builds**: Fast builds with Turbopack
- **Image Optimization**: Automatic image optimization
- **Font Optimization**: Automatic web font optimization

## Common Patterns

1. **Fetch data in Server Components, pass to Client Components**
2. **Use Server Actions for form submissions**
3. **Implement Loading states with Suspense**
4. **Use dynamic routes for parameterized pages**
5. **Leverage route groups for layout organization**
6. **Use middleware for authentication and redirects**

## Best Practices

- Keep Server Components server-only (no state/effects)
- Minimize 'use client' usage
- Use TypeScript for better DX
- Implement proper error boundaries
- Use appropriate caching strategies
- Optimize images and fonts
- Structure routes logically
