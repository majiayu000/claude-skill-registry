---
name: nextjs-16
description: Auto-activates when user mentions Next.js, App Router, server components, or Next.js routing. Expert in Next.js 16 best practices including App Router, React Server Components, and caching strategies.
category: framework
---

# Next.js 16 Best Practices

**Official Next.js 16 Guidelines - App Router, React 19, Server Components**

## Core Principles

1. **ALWAYS Use App Router** - Pages Router is legacy, use `/app` directory
2. **ALWAYS Use Server Components** - Client components only when needed
3. **Async Everything** - params, searchParams, cookies, headers are now async
4. **Server Actions for Mutations** - Replace API routes with Server Actions
5. **React 19 Features** - Use `use()` hook, async components, new hooks

## Next.js 16 Async Request APIs (BREAKING CHANGE)

### ✅ Good: Await All Request APIs
```typescript
// app/product/[id]/page.tsx
export default async function Page({
  params,
  searchParams,
}: {
  params: Promise<{ id: string }>
  searchParams: Promise<{ filter?: string }>
}) {
  // MUST await params and searchParams in Next.js 16
  const { id } = await params
  const { filter } = await searchParams

  return <div>Product {id}, Filter: {filter}</div>
}

// app/api/route.ts
import { cookies, headers } from 'next/headers'

export async function GET() {
  // MUST await cookies() and headers() in Next.js 16
  const cookieStore = await cookies()
  const headersList = await headers()

  const token = cookieStore.get('auth')
  const userAgent = headersList.get('user-agent')

  return Response.json({ token, userAgent })
}
```

### ❌ Bad: Old Next.js 15 Synchronous APIs
```typescript
// ❌ WRONG - This worked in Next.js 15, breaks in 16
export default function Page({ params, searchParams }) {
  const id = params.id  // Error: params is a Promise
  const filter = searchParams.filter  // Error: searchParams is a Promise
}

// ❌ WRONG - This worked in Next.js 15, breaks in 16
import { cookies, headers } from 'next/headers'

export async function GET() {
  const cookieStore = cookies()  // Error: must await
  const headersList = headers()  // Error: must await
}
```

## Upgrading from Next.js 15 to 16

### Use Codemod for Automatic Migration
```bash
# Automatically migrates async request APIs
npx @next/codemod@latest upgrade latest

# Or specifically for async APIs
npx @next/codemod@canary next-async-request-api .
```

### Manual Migration Checklist
```typescript
// 1. Add await to params
- const { id } = params
+ const { id } = await params

// 2. Add await to searchParams
- const { filter } = searchParams
+ const { filter } = await searchParams

// 3. Add await to cookies()
- const cookieStore = cookies()
+ const cookieStore = await cookies()

// 4. Add await to headers()
- const headersList = headers()
+ const headersList = await headers()

// 5. Make all page components async
- export default function Page({ params }) {
+ export default async function Page({ params }) {
```

## Server Components (Default)

### ✅ Good: Server Component Patterns
```typescript
// app/posts/page.tsx - Server Component (default)
import { Suspense } from 'react'

async function getPosts() {
  const res = await fetch('https://api.example.com/posts', {
    cache: 'no-store' // or next: { revalidate: 3600 }
  })
  return res.json()
}

export default async function PostsPage() {
  // Direct data fetching in Server Component
  const posts = await getPosts()

  return (
    <main>
      <h1>Posts</h1>
      <Suspense fallback={<div>Loading...</div>}>
        <PostList posts={posts} />
      </Suspense>
    </main>
  )
}

// Nested Server Component
async function PostList({ posts }: { posts: Post[] }) {
  return (
    <ul>
      {posts.map(post => (
        <li key={post.id}>{post.title}</li>
      ))}
    </ul>
  )
}
```

### ✅ Good: Environment Variables in Server Components
```typescript
// Server Component - safe to access env vars
export default async function Page() {
  // ✅ OK - Server Components can access env vars
  const apiKey = process.env.API_KEY
  const data = await fetch(`https://api.example.com/data`, {
    headers: { 'Authorization': `Bearer ${apiKey}` }
  })

  return <div>{/* render */}</div>
}
```

### ❌ Bad: Server Component Anti-patterns
```typescript
// ❌ WRONG - useState in Server Component
import { useState } from 'react'

export default async function Page() {
  const [count, setCount] = useState(0)  // Error!
  return <div>{count}</div>
}

// ❌ WRONG - useEffect in Server Component
import { useEffect } from 'react'

export default async function Page() {
  useEffect(() => {}, [])  // Error!
  return <div></div>
}

// ❌ WRONG - Event handlers in Server Component
export default async function Page() {
  return <button onClick={() => alert('Hi')}>Click</button>  // Error!
}
```

## Client Components

### ✅ Good: Client Component with 'use client'
```typescript
// app/components/Counter.tsx
'use client'

import { useState } from 'react'

export default function Counter() {
  const [count, setCount] = useState(0)

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => setCount(count + 1)}>
        Increment
      </button>
    </div>
  )
}
```

### ✅ Good: Composing Server and Client Components
```typescript
// app/page.tsx - Server Component
import Counter from './components/Counter'  // Client Component

async function getData() {
  const res = await fetch('https://api.example.com/data')
  return res.json()
}

export default async function Page() {
  const data = await getData()

  return (
    <main>
      <h1>Server Component</h1>
      <p>Data: {JSON.stringify(data)}</p>

      {/* Client Component for interactivity */}
      <Counter />
    </main>
  )
}
```

### ✅ Good: Passing Server Data to Client Components
```typescript
// app/page.tsx - Server Component
import ClientComponent from './ClientComponent'

async function getData() {
  const res = await fetch('https://api.example.com/user')
  return res.json()
}

export default async function Page() {
  const user = await getData()

  // ✅ OK - Pass serializable props to Client Component
  return <ClientComponent user={user} />
}

// ClientComponent.tsx
'use client'

export default function ClientComponent({ user }) {
  return <div>Welcome {user.name}</div>
}
```

### ❌ Bad: Client Component Anti-patterns
```typescript
// ❌ WRONG - Don't wrap Server Component in Client Component
'use client'

import ServerComponent from './ServerComponent'  // Error!

export default function ClientWrapper() {
  return <ServerComponent />  // Won't work
}

// ❌ WRONG - Passing functions as props from Server to Client
// app/page.tsx
export default async function Page() {
  async function serverAction() {
    'use server'
    // ...
  }

  return <ClientComponent onClick={serverAction} />  // Use Server Actions instead!
}

// ❌ WRONG - Accessing env vars in Client Component
'use client'

export default function Page() {
  const apiKey = process.env.API_KEY  // undefined! Not exposed to client
  return <div>{apiKey}</div>
}
```

## Server Actions and Mutations

### ✅ Good: Server Actions with 'use server'
```typescript
// app/actions.ts
'use server'

import { revalidatePath } from 'next/cache'
import { redirect } from 'next/navigation'

export async function createPost(formData: FormData) {
  const title = formData.get('title') as string
  const content = formData.get('content') as string

  // Validate
  if (!title || !content) {
    throw new Error('Title and content are required')
  }

  // Database operation
  await db.post.create({
    data: { title, content }
  })

  // Revalidate cache
  revalidatePath('/posts')

  // Redirect
  redirect('/posts')
}
```

### ✅ Good: Form with Server Action
```typescript
// app/posts/new/page.tsx
import { createPost } from '@/app/actions'

export default function NewPost() {
  return (
    <form action={createPost}>
      <input type="text" name="title" required />
      <textarea name="content" required />
      <button type="submit">Create Post</button>
    </form>
  )
}
```

### ✅ Good: Server Action with useFormState (React 19)
```typescript
// app/actions.ts
'use server'

export async function createPost(prevState: any, formData: FormData) {
  const title = formData.get('title') as string

  if (!title) {
    return { error: 'Title is required' }
  }

  await db.post.create({ data: { title } })
  return { success: true }
}

// app/components/CreatePostForm.tsx
'use client'

import { useFormState } from 'react-dom'
import { createPost } from '@/app/actions'

export default function CreatePostForm() {
  const [state, formAction] = useFormState(createPost, null)

  return (
    <form action={formAction}>
      <input type="text" name="title" />
      {state?.error && <p>{state.error}</p>}
      {state?.success && <p>Post created!</p>}
      <button type="submit">Create</button>
    </form>
  )
}
```

### ✅ Good: Server Action with useFormStatus (React 19)
```typescript
'use client'

import { useFormStatus } from 'react-dom'

export default function SubmitButton() {
  const { pending } = useFormStatus()

  return (
    <button type="submit" disabled={pending}>
      {pending ? 'Creating...' : 'Create Post'}
    </button>
  )
}
```

### ✅ Good: Server Action with Zod Validation
```typescript
'use server'

import { z } from 'zod'

const schema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
})

export async function signup(formData: FormData) {
  const result = schema.safeParse({
    email: formData.get('email'),
    password: formData.get('password'),
  })

  if (!result.success) {
    return { errors: result.error.flatten().fieldErrors }
  }

  const { email, password } = result.data

  // Create user
  await db.user.create({ data: { email, password } })

  return { success: true }
}
```

### ❌ Bad: Server Action Anti-patterns
```typescript
// ❌ WRONG - No validation
'use server'

export async function createPost(formData: FormData) {
  const title = formData.get('title')
  await db.post.create({ data: { title } })  // No validation!
}

// ❌ WRONG - No error handling
'use server'

export async function createPost(formData: FormData) {
  await db.post.create({ data: {} })  // Can throw, not handled!
}

// ❌ WRONG - Not calling revalidatePath after mutation
'use server'

export async function createPost(formData: FormData) {
  await db.post.create({ data: { title: 'Post' } })
  // Missing: revalidatePath('/posts')
}
```

## Data Fetching and Caching

### ✅ Good: Fetch with Caching Strategies
```typescript
// Static data - cached indefinitely
async function getStaticData() {
  const res = await fetch('https://api.example.com/static', {
    cache: 'force-cache'  // default
  })
  return res.json()
}

// Dynamic data - no cache
async function getDynamicData() {
  const res = await fetch('https://api.example.com/dynamic', {
    cache: 'no-store'
  })
  return res.json()
}

// Revalidate every hour
async function getRevalidatedData() {
  const res = await fetch('https://api.example.com/data', {
    next: { revalidate: 3600 }  // seconds
  })
  return res.json()
}

// Tag-based revalidation
async function getTaggedData() {
  const res = await fetch('https://api.example.com/posts', {
    next: { tags: ['posts'] }
  })
  return res.json()
}
```

### ✅ Good: Revalidating Cached Data
```typescript
'use server'

import { revalidatePath, revalidateTag } from 'next/cache'

// Revalidate specific path
export async function revalidatePostsPath() {
  revalidatePath('/posts')
}

// Revalidate specific tag
export async function revalidatePostsTag() {
  revalidateTag('posts')
}

// Revalidate layout
export async function revalidateLayout() {
  revalidatePath('/dashboard', 'layout')
}
```

### ✅ Good: Parallel Data Fetching
```typescript
export default async function Page() {
  // Parallel fetching - both requests start at once
  const [posts, users] = await Promise.all([
    fetch('https://api.example.com/posts').then(r => r.json()),
    fetch('https://api.example.com/users').then(r => r.json())
  ])

  return <div>{/* render */}</div>
}
```

### ✅ Good: Sequential Data Fetching (when dependent)
```typescript
export default async function Page() {
  // Sequential fetching - second depends on first
  const user = await fetch('https://api.example.com/user/1').then(r => r.json())

  // Use user.id for second request
  const posts = await fetch(`https://api.example.com/users/${user.id}/posts`)
    .then(r => r.json())

  return <div>{/* render */}</div>
}
```

### ❌ Bad: Data Fetching Anti-patterns
```typescript
// ❌ WRONG - Fetching in useEffect (use Server Component instead)
'use client'

import { useEffect, useState } from 'react'

export default function Page() {
  const [data, setData] = useState(null)

  useEffect(() => {
    fetch('/api/data')
      .then(r => r.json())
      .then(setData)
  }, [])

  return <div>{data?.title}</div>
}

// ❌ WRONG - Waterfall fetching (fetch then render then fetch)
export default async function Page() {
  const posts = await fetch('https://api.example.com/posts').then(r => r.json())

  return (
    <div>
      {posts.map(post => (
        <PostWithComments key={post.id} postId={post.id} />
      ))}
    </div>
  )
}

async function PostWithComments({ postId }) {
  // Each post fetches comments sequentially - slow!
  const comments = await fetch(`/api/posts/${postId}/comments`).then(r => r.json())
  return <div>{/* render */}</div>
}
```

## Loading and Streaming

### ✅ Good: loading.tsx for Instant Loading UI
```typescript
// app/posts/loading.tsx
export default function Loading() {
  return <div>Loading posts...</div>
}

// app/posts/page.tsx
export default async function PostsPage() {
  const posts = await getPosts()  // Shows loading.tsx while fetching
  return <div>{/* render */}</div>
}
```

### ✅ Good: Suspense for Granular Streaming
```typescript
import { Suspense } from 'react'

export default function Page() {
  return (
    <div>
      <h1>Dashboard</h1>

      {/* Stream Posts independently */}
      <Suspense fallback={<div>Loading posts...</div>}>
        <Posts />
      </Suspense>

      {/* Stream Comments independently */}
      <Suspense fallback={<div>Loading comments...</div>}>
        <Comments />
      </Suspense>
    </div>
  )
}

async function Posts() {
  const posts = await fetch('https://api.example.com/posts').then(r => r.json())
  return <div>{/* render */}</div>
}

async function Comments() {
  const comments = await fetch('https://api.example.com/comments').then(r => r.json())
  return <div>{/* render */}</div>
}
```

## Route Handlers (API Routes)

### ✅ Good: GET Route Handler
```typescript
// app/api/posts/route.ts
import { NextRequest, NextResponse } from 'next/server'

export async function GET(request: NextRequest) {
  const searchParams = request.nextUrl.searchParams
  const query = searchParams.get('query')

  const posts = await db.post.findMany({
    where: query ? { title: { contains: query } } : {}
  })

  return NextResponse.json({ posts })
}
```

### ✅ Good: POST Route Handler with Validation
```typescript
// app/api/posts/route.ts
import { NextRequest, NextResponse } from 'next/server'
import { z } from 'zod'

const schema = z.object({
  title: z.string().min(1),
  content: z.string().min(1),
})

export async function POST(request: NextRequest) {
  const body = await request.json()

  const result = schema.safeParse(body)
  if (!result.success) {
    return NextResponse.json(
      { errors: result.error.flatten() },
      { status: 400 }
    )
  }

  const post = await db.post.create({ data: result.data })

  return NextResponse.json({ post }, { status: 201 })
}
```

### ✅ Good: Dynamic Route Handler
```typescript
// app/api/posts/[id]/route.ts
export async function GET(
  request: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  const { id } = await params  // Must await in Next.js 16

  const post = await db.post.findUnique({
    where: { id }
  })

  if (!post) {
    return NextResponse.json(
      { error: 'Post not found' },
      { status: 404 }
    )
  }

  return NextResponse.json({ post })
}
```

### ✅ Good: CORS Headers in Route Handler
```typescript
export async function GET(request: NextRequest) {
  const data = { message: 'Hello from API' }

  return NextResponse.json(data, {
    headers: {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    },
  })
}
```

## Middleware

### ✅ Good: Middleware for Authentication
```typescript
// middleware.ts
import { NextRequest, NextResponse } from 'next/server'

export function middleware(request: NextRequest) {
  const token = request.cookies.get('token')?.value

  // Redirect to login if not authenticated
  if (!token && request.nextUrl.pathname.startsWith('/dashboard')) {
    return NextResponse.redirect(new URL('/login', request.url))
  }

  return NextResponse.next()
}

export const config = {
  matcher: ['/dashboard/:path*']
}
```

### ✅ Good: Middleware for Rewrites
```typescript
// middleware.ts
import { NextRequest, NextResponse } from 'next/server'

export function middleware(request: NextRequest) {
  // Rewrite /blog/* to /posts/*
  if (request.nextUrl.pathname.startsWith('/blog')) {
    const newPath = request.nextUrl.pathname.replace('/blog', '/posts')
    return NextResponse.rewrite(new URL(newPath, request.url))
  }

  return NextResponse.next()
}
```

### ✅ Good: Middleware for Headers
```typescript
// middleware.ts
import { NextRequest, NextResponse } from 'next/server'

export function middleware(request: NextRequest) {
  const response = NextResponse.next()

  // Add custom headers
  response.headers.set('x-custom-header', 'my-value')
  response.headers.set('x-request-id', crypto.randomUUID())

  return response
}
```

## Metadata and SEO

### ✅ Good: Static Metadata
```typescript
// app/page.tsx
import { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'My App',
  description: 'Welcome to my app',
  openGraph: {
    title: 'My App',
    description: 'Welcome to my app',
    images: ['/og-image.jpg'],
  },
}

export default function Page() {
  return <div>Home</div>
}
```

### ✅ Good: Dynamic Metadata with generateMetadata
```typescript
// app/posts/[id]/page.tsx
import { Metadata } from 'next'

export async function generateMetadata({
  params,
}: {
  params: Promise<{ id: string }>
}): Promise<Metadata> {
  const { id } = await params

  const post = await fetch(`https://api.example.com/posts/${id}`)
    .then(r => r.json())

  return {
    title: post.title,
    description: post.excerpt,
    openGraph: {
      title: post.title,
      description: post.excerpt,
      images: [post.coverImage],
    },
  }
}

export default async function Page({
  params,
}: {
  params: Promise<{ id: string }>
}) {
  const { id } = await params
  const post = await fetch(`https://api.example.com/posts/${id}`)
    .then(r => r.json())

  return <article>{post.title}</article>
}
```

## Image Optimization

### ✅ Good: Next.js Image Component
```typescript
import Image from 'next/image'

export default function Page() {
  return (
    <div>
      {/* Local image - auto width/height */}
      <Image
        src="/hero.jpg"
        alt="Hero"
        width={1920}
        height={1080}
        priority  // LCP image
      />

      {/* Remote image - must specify width/height */}
      <Image
        src="https://example.com/photo.jpg"
        alt="Photo"
        width={800}
        height={600}
        quality={90}
      />

      {/* Fill container */}
      <div style={{ position: 'relative', height: '400px' }}>
        <Image
          src="/background.jpg"
          alt="Background"
          fill
          style={{ objectFit: 'cover' }}
        />
      </div>
    </div>
  )
}
```

### ✅ Good: Image Loader for External CDN
```typescript
// next.config.js
module.exports = {
  images: {
    loader: 'custom',
    loaderFile: './imageLoader.ts',
  },
}

// imageLoader.ts
export default function cloudinaryLoader({ src, width, quality }) {
  const params = ['f_auto', 'c_limit', `w_${width}`, `q_${quality || 'auto'}`]
  return `https://res.cloudinary.com/demo/image/upload/${params.join(',')}${src}`
}
```

## Static Generation

### ✅ Good: generateStaticParams for Dynamic Routes
```typescript
// app/posts/[id]/page.tsx
export async function generateStaticParams() {
  const posts = await fetch('https://api.example.com/posts')
    .then(r => r.json())

  return posts.map((post: any) => ({
    id: post.id.toString(),
  }))
}

export default async function Page({
  params,
}: {
  params: Promise<{ id: string }>
}) {
  const { id } = await params
  const post = await fetch(`https://api.example.com/posts/${id}`)
    .then(r => r.json())

  return <article>{post.title}</article>
}
```

## Performance Optimization

### ✅ Good: Lazy Loading Components
```typescript
import dynamic from 'next/dynamic'

// Lazy load component
const HeavyComponent = dynamic(() => import('./HeavyComponent'), {
  loading: () => <div>Loading...</div>
})

export default function Page() {
  return (
    <div>
      <h1>Page</h1>
      <HeavyComponent />
    </div>
  )
}
```

### ✅ Good: Font Optimization
```typescript
// app/layout.tsx
import { Inter, Roboto_Mono } from 'next/font/google'

const inter = Inter({
  subsets: ['latin'],
  display: 'swap',
})

const robotoMono = Roboto_Mono({
  subsets: ['latin'],
  display: 'swap',
})

export default function RootLayout({ children }) {
  return (
    <html lang="en" className={inter.className}>
      <body>{children}</body>
    </html>
  )
}
```

### ✅ Good: Script Optimization
```typescript
import Script from 'next/script'

export default function Page() {
  return (
    <div>
      {/* Load after page is interactive */}
      <Script
        src="https://example.com/script.js"
        strategy="lazyOnload"
      />

      {/* Critical script - load before hydration */}
      <Script
        src="https://example.com/critical.js"
        strategy="beforeInteractive"
      />
    </div>
  )
}
```

## Error Handling

### ✅ Good: error.tsx for Error Boundaries
```typescript
// app/posts/error.tsx
'use client'

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string }
  reset: () => void
}) {
  return (
    <div>
      <h2>Something went wrong!</h2>
      <p>{error.message}</p>
      <button onClick={() => reset()}>Try again</button>
    </div>
  )
}
```

### ✅ Good: not-found.tsx for 404 Errors
```typescript
// app/posts/[id]/not-found.tsx
export default function NotFound() {
  return (
    <div>
      <h2>Post Not Found</h2>
      <p>Could not find the requested post.</p>
    </div>
  )
}

// app/posts/[id]/page.tsx
import { notFound } from 'next/navigation'

export default async function Page({
  params,
}: {
  params: Promise<{ id: string }>
}) {
  const { id } = await params
  const post = await fetch(`https://api.example.com/posts/${id}`)
    .then(r => r.ok ? r.json() : null)

  if (!post) {
    notFound()  // Shows not-found.tsx
  }

  return <article>{post.title}</article>
}
```

## Environment Variables

### ✅ Good: Environment Variables
```bash
# .env.local

# Server-only (not exposed to browser)
DATABASE_URL=postgresql://...
API_SECRET=secret123

# Exposed to browser (must start with NEXT_PUBLIC_)
NEXT_PUBLIC_API_URL=https://api.example.com
NEXT_PUBLIC_SITE_URL=https://example.com
```

```typescript
// Server Component or Server Action - can access all env vars
export default async function Page() {
  const dbUrl = process.env.DATABASE_URL  // ✅ OK
  const apiUrl = process.env.NEXT_PUBLIC_API_URL  // ✅ OK
}

// Client Component - can only access NEXT_PUBLIC_*
'use client'

export default function ClientComponent() {
  const apiUrl = process.env.NEXT_PUBLIC_API_URL  // ✅ OK
  const dbUrl = process.env.DATABASE_URL  // ❌ undefined
}
```

**CRITICAL: ALWAYS await params/searchParams/cookies/headers in Next.js 16, use Server Components by default, Server Actions for mutations, and async components for data fetching.**
