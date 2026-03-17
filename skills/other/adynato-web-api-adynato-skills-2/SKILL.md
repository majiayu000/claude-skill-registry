---
name: adynato-web-api
description: Web API development conventions for Adynato projects. Covers API routes, middleware, authentication, error handling, validation, and response formats for Next.js and Node.js backends. Use when building or modifying API endpoints, server actions, or backend logic.
---

# Web API Skill

Use this skill when building APIs for Adynato web projects.

## Stack

- **Framework**: Next.js API Routes or App Router Route Handlers
- **Validation**: Zod
- **Auth**: NextAuth.js / Auth.js
- **Database**: Prisma + PostgreSQL
- **Rate Limiting**: Upstash

## Route Handlers (App Router)

### Basic Structure

```
app/
└── api/
    ├── auth/
    │   └── [...nextauth]/
    │       └── route.ts
    ├── users/
    │   ├── route.ts          # GET /api/users, POST /api/users
    │   └── [id]/
    │       └── route.ts      # GET/PATCH/DELETE /api/users/:id
    └── health/
        └── route.ts
```

### Route Handler Pattern

```typescript
// app/api/users/route.ts
import { NextRequest, NextResponse } from 'next/server'
import { z } from 'zod'
import { prisma } from '@/lib/prisma'
import { auth } from '@/lib/auth'

const createUserSchema = z.object({
  email: z.string().email(),
  name: z.string().min(1).max(100),
})

export async function GET(request: NextRequest) {
  try {
    const session = await auth()
    if (!session) {
      return NextResponse.json(
        { error: 'Unauthorized' },
        { status: 401 }
      )
    }

    const users = await prisma.user.findMany({
      select: { id: true, email: true, name: true },
    })

    return NextResponse.json({ data: users })
  } catch (error) {
    console.error('GET /api/users error:', error)
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    )
  }
}

export async function POST(request: NextRequest) {
  try {
    const session = await auth()
    if (!session) {
      return NextResponse.json(
        { error: 'Unauthorized' },
        { status: 401 }
      )
    }

    const body = await request.json()
    const result = createUserSchema.safeParse(body)

    if (!result.success) {
      return NextResponse.json(
        { error: 'Validation failed', details: result.error.flatten() },
        { status: 400 }
      )
    }

    const user = await prisma.user.create({
      data: result.data,
    })

    return NextResponse.json({ data: user }, { status: 201 })
  } catch (error) {
    console.error('POST /api/users error:', error)
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    )
  }
}
```

### Dynamic Route Handler

```typescript
// app/api/users/[id]/route.ts
import { NextRequest, NextResponse } from 'next/server'
import { prisma } from '@/lib/prisma'

interface RouteParams {
  params: { id: string }
}

export async function GET(request: NextRequest, { params }: RouteParams) {
  const { id } = params

  const user = await prisma.user.findUnique({
    where: { id },
  })

  if (!user) {
    return NextResponse.json(
      { error: 'User not found' },
      { status: 404 }
    )
  }

  return NextResponse.json({ data: user })
}

export async function DELETE(request: NextRequest, { params }: RouteParams) {
  const { id } = params

  await prisma.user.delete({ where: { id } })

  return new NextResponse(null, { status: 204 })
}
```

## Response Format

### Success Responses

```typescript
// Single resource
{ "data": { "id": "123", "name": "John" } }

// Collection
{ "data": [...], "meta": { "total": 100, "page": 1, "limit": 20 } }

// Created
{ "data": { ... } } // 201 status

// No content
// Empty body, 204 status
```

### Error Responses

```typescript
// Client error
{
  "error": "Validation failed",
  "details": { ... }  // Optional
}

// Not found
{ "error": "Resource not found" }

// Unauthorized
{ "error": "Unauthorized" }

// Server error
{ "error": "Internal server error" }
```

## Validation with Zod

### Schema Definition

```typescript
// lib/validations/user.ts
import { z } from 'zod'

export const createUserSchema = z.object({
  email: z.string().email('Invalid email address'),
  name: z.string().min(1, 'Name is required').max(100),
  role: z.enum(['user', 'admin']).default('user'),
})

export const updateUserSchema = createUserSchema.partial()

export type CreateUserInput = z.infer<typeof createUserSchema>
export type UpdateUserInput = z.infer<typeof updateUserSchema>
```

### Query Parameter Validation

```typescript
const querySchema = z.object({
  page: z.coerce.number().min(1).default(1),
  limit: z.coerce.number().min(1).max(100).default(20),
  search: z.string().optional(),
})

export async function GET(request: NextRequest) {
  const searchParams = Object.fromEntries(request.nextUrl.searchParams)
  const query = querySchema.parse(searchParams)
  // ...
}
```

## Authentication

### Auth Check Helper

```typescript
// lib/auth.ts
import { getServerSession } from 'next-auth'
import { authOptions } from '@/app/api/auth/[...nextauth]/route'

export async function auth() {
  return getServerSession(authOptions)
}

export async function requireAuth() {
  const session = await auth()
  if (!session) {
    throw new Error('Unauthorized')
  }
  return session
}
```

### Protected Route Pattern

```typescript
export async function GET(request: NextRequest) {
  const session = await auth()

  if (!session) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
  }

  // Proceed with authenticated logic
}
```

## Server Actions

For mutations that don't need to be APIs:

```typescript
// app/actions/user.ts
'use server'

import { z } from 'zod'
import { revalidatePath } from 'next/cache'
import { prisma } from '@/lib/prisma'
import { auth } from '@/lib/auth'

const updateProfileSchema = z.object({
  name: z.string().min(1).max(100),
})

export async function updateProfile(formData: FormData) {
  const session = await auth()
  if (!session?.user?.id) {
    throw new Error('Unauthorized')
  }

  const result = updateProfileSchema.safeParse({
    name: formData.get('name'),
  })

  if (!result.success) {
    return { error: result.error.flatten() }
  }

  await prisma.user.update({
    where: { id: session.user.id },
    data: result.data,
  })

  revalidatePath('/profile')
  return { success: true }
}
```

## Rate Limiting

```typescript
// lib/rate-limit.ts
import { Ratelimit } from '@upstash/ratelimit'
import { Redis } from '@upstash/redis'

const ratelimit = new Ratelimit({
  redis: Redis.fromEnv(),
  limiter: Ratelimit.slidingWindow(10, '10 s'),
})

export async function checkRateLimit(identifier: string) {
  const { success, limit, remaining } = await ratelimit.limit(identifier)
  return { success, limit, remaining }
}
```

```typescript
// In route handler
export async function POST(request: NextRequest) {
  const ip = request.ip ?? 'anonymous'
  const { success } = await checkRateLimit(ip)

  if (!success) {
    return NextResponse.json(
      { error: 'Too many requests' },
      { status: 429 }
    )
  }
  // ...
}
```

## Error Handling

### Global Error Handler

```typescript
// lib/api-error.ts
export class ApiError extends Error {
  constructor(
    public statusCode: number,
    message: string,
    public details?: unknown
  ) {
    super(message)
  }
}

export function handleApiError(error: unknown) {
  console.error('API Error:', error)

  if (error instanceof ApiError) {
    return NextResponse.json(
      { error: error.message, details: error.details },
      { status: error.statusCode }
    )
  }

  if (error instanceof z.ZodError) {
    return NextResponse.json(
      { error: 'Validation failed', details: error.flatten() },
      { status: 400 }
    )
  }

  return NextResponse.json(
    { error: 'Internal server error' },
    { status: 500 }
  )
}
```

## Checklist

Before deploying APIs:

- [ ] All inputs validated with Zod
- [ ] Authentication checked on protected routes
- [ ] Rate limiting on public endpoints
- [ ] Proper error responses with correct status codes
- [ ] No sensitive data leaked in responses
- [ ] Logging for errors (not sensitive data)
- [ ] CORS configured if needed
- [ ] Response times acceptable
