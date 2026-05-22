---
name: nextjs-patterns
description: Next.js 15 App Router patterns - use for frontend pages, API routes, server components, client components, and middleware
---

# Next.js 15 App Router Patterns

## File Structure

```
app/
├── layout.tsx              # Root layout (required)
├── page.tsx                # Home page (/)
├── loading.tsx             # Loading UI
├── error.tsx               # Error boundary
├── not-found.tsx           # 404 page
├── globals.css             # Global styles
├── environments/
│   ├── page.tsx            # /environments
│   ├── [id]/
│   │   ├── page.tsx        # /environments/[id]
│   │   └── loading.tsx     # Loading for this route
│   └── new/
│       └── page.tsx        # /environments/new
├── api/
│   └── environments/
│       ├── route.ts        # GET/POST /api/environments
│       └── [id]/
│           └── route.ts    # GET/PUT/DELETE /api/environments/[id]
└── (auth)/                 # Route group (no URL impact)
    ├── login/
    │   └── page.tsx
    └── layout.tsx          # Shared auth layout
```

## Server Components (Default)

```tsx
// app/environments/page.tsx
// Server Component - can use async/await directly
import { getEnvironments } from '@/lib/api'

export default async function EnvironmentsPage() {
  const environments = await getEnvironments()

  return (
    <main className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Environments</h1>
      <EnvironmentList environments={environments} />
    </main>
  )
}

// With search params
export default async function EnvironmentsPage({
  searchParams,
}: {
  searchParams: Promise<{ status?: string; page?: string }>
}) {
  const params = await searchParams
  const environments = await getEnvironments({
    status: params.status,
    page: parseInt(params.page || '1'),
  })

  return <EnvironmentList environments={environments} />
}
```

## Client Components

```tsx
// components/EnvironmentActions.tsx
'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'

export function EnvironmentActions({ id }: { id: string }) {
  const [isLoading, setIsLoading] = useState(false)
  const router = useRouter()

  async function handleDelete() {
    setIsLoading(true)
    try {
      await fetch(`/api/environments/${id}`, { method: 'DELETE' })
      router.refresh() // Refresh server components
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <button
      onClick={handleDelete}
      disabled={isLoading}
      className="btn btn-danger"
    >
      {isLoading ? 'Deleting...' : 'Delete'}
    </button>
  )
}
```

## API Route Handlers

```tsx
// app/api/environments/route.ts
import { NextRequest, NextResponse } from 'next/server'
import { z } from 'zod'

const CreateEnvironmentSchema = z.object({
  name: z.string().min(1).max(100),
  description: z.string().optional(),
})

// GET /api/environments
export async function GET(request: NextRequest) {
  const searchParams = request.nextUrl.searchParams
  const status = searchParams.get('status')

  const environments = await prisma.environment.findMany({
    where: status ? { status } : undefined,
    orderBy: { createdAt: 'desc' },
  })

  return NextResponse.json(environments)
}

// POST /api/environments
export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    const data = CreateEnvironmentSchema.parse(body)

    const environment = await prisma.environment.create({
      data: {
        name: data.name,
        description: data.description,
        status: 'PENDING',
      },
    })

    return NextResponse.json(environment, { status: 201 })
  } catch (error) {
    if (error instanceof z.ZodError) {
      return NextResponse.json(
        { error: 'Validation failed', details: error.errors },
        { status: 400 }
      )
    }
    throw error
  }
}

// app/api/environments/[id]/route.ts
export async function GET(
  request: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  const { id } = await params

  const environment = await prisma.environment.findUnique({
    where: { id },
  })

  if (!environment) {
    return NextResponse.json(
      { error: 'Environment not found' },
      { status: 404 }
    )
  }

  return NextResponse.json(environment)
}
```

## Middleware

```tsx
// middleware.ts
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'
import { getToken } from 'next-auth/jwt'

export async function middleware(request: NextRequest) {
  const token = await getToken({ req: request })
  const isAuthPage = request.nextUrl.pathname.startsWith('/login')

  // Redirect authenticated users away from auth pages
  if (isAuthPage && token) {
    return NextResponse.redirect(new URL('/dashboard', request.url))
  }

  // Protect dashboard routes
  if (request.nextUrl.pathname.startsWith('/dashboard') && !token) {
    return NextResponse.redirect(new URL('/login', request.url))
  }

  return NextResponse.next()
}

export const config = {
  matcher: ['/dashboard/:path*', '/login'],
}
```

## NextAuth.js Integration

```tsx
// lib/auth.ts
import NextAuth from 'next-auth'
import GoogleProvider from 'next-auth/providers/google'
import { PrismaAdapter } from '@auth/prisma-adapter'
import { prisma } from '@/lib/prisma'

export const { handlers, auth, signIn, signOut } = NextAuth({
  adapter: PrismaAdapter(prisma),
  providers: [
    GoogleProvider({
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
    }),
  ],
  callbacks: {
    session({ session, user }) {
      session.user.id = user.id
      return session
    },
  },
})

// app/api/auth/[...nextauth]/route.ts
import { handlers } from '@/lib/auth'
export const { GET, POST } = handlers
```

## Server Actions

```tsx
// app/environments/actions.ts
'use server'

import { revalidatePath } from 'next/cache'
import { redirect } from 'next/navigation'
import { z } from 'zod'

const CreateSchema = z.object({
  name: z.string().min(1),
})

export async function createEnvironment(formData: FormData) {
  const data = CreateSchema.parse({
    name: formData.get('name'),
  })

  await prisma.environment.create({
    data: { name: data.name, status: 'PENDING' },
  })

  revalidatePath('/environments')
  redirect('/environments')
}

// Usage in component
import { createEnvironment } from './actions'

export function CreateForm() {
  return (
    <form action={createEnvironment}>
      <input name="name" required />
      <button type="submit">Create</button>
    </form>
  )
}
```

## Loading & Error States

```tsx
// app/environments/loading.tsx
export default function Loading() {
  return (
    <div className="animate-pulse">
      <div className="h-8 bg-gray-200 rounded w-1/4 mb-4" />
      <div className="space-y-3">
        {[...Array(5)].map((_, i) => (
          <div key={i} className="h-16 bg-gray-200 rounded" />
        ))}
      </div>
    </div>
  )
}

// app/environments/error.tsx
'use client'

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string }
  reset: () => void
}) {
  return (
    <div className="text-center p-8">
      <h2 className="text-xl font-bold text-red-600">Something went wrong!</h2>
      <p className="text-gray-600 mt-2">{error.message}</p>
      <button
        onClick={reset}
        className="mt-4 px-4 py-2 bg-blue-500 text-white rounded"
      >
        Try again
      </button>
    </div>
  )
}
```

## Data Fetching Patterns

```tsx
// lib/api.ts
const API_URL = process.env.FACADE_URL || 'http://localhost:1337'

export async function getEnvironments() {
  const res = await fetch(`${API_URL}/api/v1/environments`, {
    next: { revalidate: 60 }, // ISR: revalidate every 60 seconds
  })

  if (!res.ok) {
    throw new Error('Failed to fetch environments')
  }

  return res.json()
}

export async function getEnvironment(id: string) {
  const res = await fetch(`${API_URL}/api/v1/environments/${id}`, {
    cache: 'no-store', // Always fresh
  })

  if (!res.ok) {
    if (res.status === 404) return null
    throw new Error('Failed to fetch environment')
  }

  return res.json()
}
```

## Parallel Data Fetching

```tsx
// app/dashboard/page.tsx
export default async function DashboardPage() {
  // Fetch in parallel
  const [environments, users, metrics] = await Promise.all([
    getEnvironments(),
    getUsers(),
    getMetrics(),
  ])

  return (
    <Dashboard
      environments={environments}
      users={users}
      metrics={metrics}
    />
  )
}
```
