---
name: nextjs
description: Next.js App Router architecture, Server Components, and modern patterns. Use when building Next.js apps, choosing rendering strategies, or optimizing data fetching.
---

# Next.js Best Practices Skill

## Overview
Next.js App Router architecture, Server Components, and modern patterns.

## Core Concepts

### 1. App Router Structure
```
app/
├── layout.tsx          # Root layout
├── page.tsx            # Home page
├── loading.tsx         # Loading UI
├── error.tsx           # Error UI
├── not-found.tsx       # 404 page
├── (marketing)/        # Route group
│   ├── about/
│   └── contact/
└── api/
    └── route.ts        # API route
```

### 2. Server vs Client Components

```tsx
// Server Component (default)
async function UserProfile({ userId }: { userId: string }) {
  const user = await getUser(userId); // Direct DB access
  return <div>{user.name}</div>;
}

// Client Component
'use client';
import { useState } from 'react';

function Counter() {
  const [count, setCount] = useState(0);
  return <button onClick={() => setCount(c => c + 1)}>{count}</button>;
}
```

### 3. Data Fetching
```tsx
// Server Component with fetch
async function Posts() {
  const posts = await fetch('https://api.example.com/posts', {
    next: { revalidate: 3600 } // ISR: revalidate every hour
  }).then(res => res.json());
  
  return posts.map(post => <PostCard key={post.id} post={post} />);
}

// Server Actions
'use server';
async function createPost(formData: FormData) {
  const title = formData.get('title');
  await db.posts.create({ title });
  revalidatePath('/posts');
}
```

### 4. Metadata & SEO
```tsx
export const metadata: Metadata = {
  title: 'My App',
  description: 'App description',
  openGraph: {
    title: 'My App',
    images: ['/og-image.png'],
  },
};

// Dynamic metadata
export async function generateMetadata({ params }): Promise<Metadata> {
  const post = await getPost(params.id);
  return { title: post.title };
}
```

### 5. Route Handlers (API)
```tsx
// app/api/users/route.ts
import { NextResponse } from 'next/server';

export async function GET(request: Request) {
  const users = await getUsers();
  return NextResponse.json(users);
}

export async function POST(request: Request) {
  const body = await request.json();
  const user = await createUser(body);
  return NextResponse.json(user, { status: 201 });
}
```

## Performance Tips
- Use `<Image>` for automatic optimization
- Leverage Streaming with `<Suspense>`
- Use `next/dynamic` for conditional imports
- Enable PPR (Partial Prerendering) where applicable
