---
name: nextjs
displayName: Next.js
description: Next.js 15+ App Router development patterns
version: 1.0.0
---

# Next.js Development Guidelines

Development patterns for Next.js 15+ using the App Router, Server Components, and modern data fetching.

## Core Principles

1. **Server-First Architecture**: Default to Server Components, use Client Components only when needed
2. **File-Based Routing**: Use App Router conventions for pages, layouts, and route handlers
3. **Data Fetching**: Fetch data where it's needed using async/await in Server Components
4. **Type Safety**: Leverage TypeScript for route params, search params, and data types
5. **Performance**: Optimize with streaming, parallel data fetching, and static generation

## App Router Structure

### File Conventions

```
app/
├── layout.tsx              # Root layout (required)
├── page.tsx               # Home page
├── loading.tsx            # Loading UI
├── error.tsx              # Error boundary
├── not-found.tsx          # 404 page
├── posts/
│   ├── layout.tsx         # Posts layout
│   ├── page.tsx          # /posts
│   ├── [id]/
│   │   └── page.tsx      # /posts/123
│   └── new/
│       └── page.tsx      # /posts/new
└── api/
    └── posts/
        └── route.ts      # API route handler
```

### Page Component

```typescript
// app/posts/page.tsx
import { getPosts } from '@/lib/api';

export const metadata = {
  title: 'Posts',
  description: 'Browse all blog posts'
};

export default async function PostsPage() {
  const posts = await getPosts();

  return (
    <div>
      <h1>Posts</h1>
      <ul>
        {posts.map(post => (
          <li key={post.id}>
            <a href={`/posts/${post.id}`}>{post.title}</a>
          </li>
        ))}
      </ul>
    </div>
  );
}
```

### Dynamic Routes

```typescript
// app/posts/[id]/page.tsx
import { getPost } from '@/lib/api';
import { notFound } from 'next/navigation';

interface PageProps {
  params: Promise<{ id: string }>;
  searchParams: Promise<{ [key: string]: string | string[] | undefined }>;
}

export async function generateMetadata({ params }: PageProps) {
  const { id } = await params;
  const post = await getPost(id);
  return {
    title: post.title,
    description: post.excerpt
  };
}

export default async function PostPage({ params }: PageProps) {
  const { id } = await params;
  const post = await getPost(id);

  if (!post) {
    notFound();
  }

  return (
    <article>
      <h1>{post.title}</h1>
      <div dangerouslySetInnerHTML={{ __html: post.content }} />
    </article>
  );
}
```

## Server vs Client Components

### Server Components (Default)

Use for:
- Data fetching
- Accessing backend resources
- Keeping sensitive info on server
- Reducing client-side JavaScript

```typescript
// app/posts/page.tsx (Server Component by default)
import { db } from '@/lib/db';

export default async function PostsPage() {
  // Direct database access
  const posts = await db.post.findMany();

  return <PostList posts={posts} />;
}
```

### Client Components

Use for:
- Event listeners (onClick, onChange, etc.)
- State and lifecycle (useState, useEffect)
- Browser-only APIs
- Custom hooks

```typescript
// components/SearchBar.tsx
'use client'; // Required directive

import { useState } from 'react';
import { useRouter } from 'next/navigation';

export function SearchBar() {
  const [query, setQuery] = useState('');
  const router = useRouter();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    router.push(`/search?q=${query}`);
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        value={query}
        onChange={e => setQuery(e.target.value)}
        placeholder="Search posts..."
      />
      <button type="submit">Search</button>
    </form>
  );
}
```

### Composition Pattern

```typescript
// app/posts/page.tsx (Server Component)
import { getPosts } from '@/lib/api';
import { SearchBar } from '@/components/SearchBar'; // Client Component

export default async function PostsPage() {
  const posts = await getPosts();

  return (
    <div>
      <SearchBar /> {/* Client Component for interactivity */}
      <PostList posts={posts} /> {/* Can be Server Component */}
    </div>
  );
}
```

## Data Fetching

### Basic Pattern

```typescript
// Server Component with async/await
export default async function PostsPage() {
  const posts = await fetch('https://api.example.com/posts', {
    next: { revalidate: 3600 } // Cache for 1 hour
  }).then(res => res.json());

  return <PostList posts={posts} />;
}
```

### Parallel Data Fetching

```typescript
export default async function DashboardPage() {
  // Fetch in parallel
  const [user, posts, stats] = await Promise.all([
    getUser(),
    getPosts(),
    getStats()
  ]);

  return (
    <div>
      <UserProfile user={user} />
      <PostList posts={posts} />
      <Stats data={stats} />
    </div>
  );
}
```

### Streaming with Suspense

```typescript
import { Suspense } from 'react';

export default function PostsPage() {
  return (
    <div>
      <h1>Posts</h1>
      <Suspense fallback={<PostsSkeleton />}>
        <Posts />
      </Suspense>
    </div>
  );
}

async function Posts() {
  const posts = await getPosts(); // Slow data fetch
  return <PostList posts={posts} />;
}
```

## Layouts

### Root Layout (Required)

```typescript
// app/layout.tsx
import './globals.css';

export const metadata = {
  title: {
    default: 'My Blog',
    template: '%s | My Blog'
  }
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        <header>
          <nav>{/* Navigation */}</nav>
        </header>
        <main>{children}</main>
        <footer>{/* Footer */}</footer>
      </body>
    </html>
  );
}
```

### Nested Layout

```typescript
// app/posts/layout.tsx
export default function PostsLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div>
      <aside>
        <PostsSidebar />
      </aside>
      <div>{children}</div>
    </div>
  );
}
```

## Route Handlers (API Routes)

### Basic Handler

```typescript
// app/api/posts/route.ts
import { NextRequest, NextResponse } from 'next/server';

export async function GET(request: NextRequest) {
  const posts = await getPosts();
  return NextResponse.json({ posts });
}

export async function POST(request: NextRequest) {
  const body = await request.json();
  const post = await createPost(body);
  return NextResponse.json({ post }, { status: 201 });
}
```

### Dynamic Route Handler

```typescript
// app/api/posts/[id]/route.ts
export async function GET(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  const post = await getPost(params.id);

  if (!post) {
    return NextResponse.json(
      { error: 'Post not found' },
      { status: 404 }
    );
  }

  return NextResponse.json({ post });
}
```

## Server Actions

### Basic Server Action

```typescript
// app/actions/posts.ts
'use server';

import { revalidatePath } from 'next/cache';
import { redirect } from 'next/navigation';

export async function createPost(formData: FormData) {
  const title = formData.get('title') as string;
  const content = formData.get('content') as string;

  const post = await db.post.create({
    data: { title, content }
  });

  revalidatePath('/posts');
  redirect(`/posts/${post.id}`);
}
```

### Using in Forms

```typescript
import { createPost } from '@/app/actions/posts';

export default function NewPostPage() {
  return (
    <form action={createPost}>
      <input name="title" required />
      <textarea name="content" required />
      <button type="submit">Create Post</button>
    </form>
  );
}
```

## Navigation

### Link Component

```typescript
import Link from 'next/link';

export function PostCard({ post }: { post: Post }) {
  return (
    <Link href={`/posts/${post.id}`} prefetch={true}>
      <h2>{post.title}</h2>
      <p>{post.excerpt}</p>
    </Link>
  );
}
```

### Programmatic Navigation

```typescript
'use client';

import { useRouter } from 'next/navigation';

export function PostActions({ postId }: { postId: string }) {
  const router = useRouter();

  const handleDelete = async () => {
    await deletePost(postId);
    router.push('/posts');
    router.refresh(); // Refresh server components
  };

  return <button onClick={handleDelete}>Delete</button>;
}
```

### Router Hooks

```typescript
'use client';

import { usePathname, useSearchParams } from 'next/navigation';

const pathname = usePathname(); // /posts/123
const searchParams = useSearchParams(); // ?q=hello
const query = searchParams.get('q');
```

## Metadata

```typescript
// Static metadata
export const metadata = {
  title: 'All Posts',
  description: 'Browse our collection of blog posts'
};

// Dynamic metadata
export async function generateMetadata({ params }: PageProps) {
  const { id } = await params;
  const post = await getPost(id);
  return {
    title: post.title,
    description: post.excerpt
  };
}
```

## Error Handling

```typescript
// app/posts/error.tsx
'use client';

export default function Error({ error, reset }: { error: Error; reset: () => void }) {
  return (
    <div>
      <h2>Something went wrong!</h2>
      <button onClick={() => reset()}>Try again</button>
    </div>
  );
}

// app/posts/[id]/not-found.tsx
export default function NotFound() {
  return <div>Post Not Found</div>;
}
```

## Static Generation & ISR

```typescript
// Generate static pages at build time
export async function generateStaticParams() {
  const posts = await getPosts();
  return posts.map((post) => ({ id: post.id }));
}

// Revalidate every hour (ISR)
export const revalidate = 3600;

export default async function PostPage({
  params
}: {
  params: Promise<{ id: string }>
}) {
  const { id } = await params;
  const post = await getPost(id);
  return <Post data={post} />;
}
```

## Additional Resources

For detailed information, see:
- [Server Actions Guide](resources/server-actions.md)
- [Data Fetching Patterns](resources/data-fetching.md)
- [Routing and Navigation](resources/routing.md)
- [Performance Optimization](resources/performance.md)
