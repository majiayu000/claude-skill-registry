---
name: route-handlers
description: This skill should be used when the user asks to "create an API route", "add an endpoint", "build a REST API", "handle POST requests", "create route handlers", "stream responses", or needs guidance on Next.js API development in the App Router.
version: 1.0.0
---

# Next.js Route Handlers

## Overview

Route Handlers allow you to create API endpoints using the Web Request and Response APIs. They're defined in `route.ts` files within the `app` directory.

## Basic Structure

### File Convention

Route handlers use `route.ts` (or `route.js`):

```
app/
├── api/
│   ├── users/
│   │   └── route.ts      # /api/users
│   └── posts/
│       ├── route.ts      # /api/posts
│       └── [id]/
│           └── route.ts  # /api/posts/:id
```

### HTTP Methods

Export functions named after HTTP methods:

```tsx
// app/api/users/route.ts
import { NextResponse } from 'next/server'

export async function GET() {
  const users = await db.user.findMany()
  return NextResponse.json(users)
}

export async function POST(request: Request) {
  const body = await request.json()
  const user = await db.user.create({ data: body })
  return NextResponse.json(user, { status: 201 })
}
```

Supported methods: `GET`, `POST`, `PUT`, `PATCH`, `DELETE`, `HEAD`, `OPTIONS`

## Request Handling

### Reading Request Body

```tsx
export async function POST(request: Request) {
  // JSON body
  const json = await request.json()

  // Form data
  const formData = await request.formData()
  const name = formData.get('name')

  // Text body
  const text = await request.text()

  return NextResponse.json({ received: true })
}
```

### URL Parameters

Dynamic route parameters:

```tsx
// app/api/posts/[id]/route.ts
interface RouteContext {
  params: Promise<{ id: string }>
}

export async function GET(
  request: Request,
  context: RouteContext
) {
  const { id } = await context.params
  const post = await db.post.findUnique({ where: { id } })

  if (!post) {
    return NextResponse.json(
      { error: 'Not found' },
      { status: 404 }
    )
  }

  return NextResponse.json(post)
}
```

### Query Parameters

```tsx
export async function GET(request: Request) {
  const { searchParams } = new URL(request.url)
  const page = searchParams.get('page') ?? '1'
  const limit = searchParams.get('limit') ?? '10'

  const posts = await db.post.findMany({
    skip: (parseInt(page) - 1) * parseInt(limit),
    take: parseInt(limit),
  })

  return NextResponse.json(posts)
}
```

### Request Headers

```tsx
export async function GET(request: Request) {
  const authHeader = request.headers.get('authorization')

  if (!authHeader?.startsWith('Bearer ')) {
    return NextResponse.json(
      { error: 'Unauthorized' },
      { status: 401 }
    )
  }

  const token = authHeader.split(' ')[1]
  // Validate token...

  return NextResponse.json({ authenticated: true })
}
```

## Response Handling

### JSON Response

```tsx
import { NextResponse } from 'next/server'

export async function GET() {
  return NextResponse.json(
    { message: 'Hello' },
    { status: 200 }
  )
}
```

### Setting Headers

```tsx
export async function GET() {
  return NextResponse.json(
    { data: 'value' },
    {
      headers: {
        'Cache-Control': 'max-age=3600',
        'X-Custom-Header': 'custom-value',
      },
    }
  )
}
```

### Setting Cookies

```tsx
import { cookies } from 'next/headers'

export async function POST(request: Request) {
  const cookieStore = await cookies()

  // Set cookie
  cookieStore.set('session', 'abc123', {
    httpOnly: true,
    secure: process.env.NODE_ENV === 'production',
    sameSite: 'lax',
    maxAge: 60 * 60 * 24 * 7, // 1 week
  })

  return NextResponse.json({ success: true })
}
```

### Redirects

```tsx
import { redirect } from 'next/navigation'
import { NextResponse } from 'next/server'

export async function GET() {
  // Option 1: redirect function (throws)
  redirect('/login')

  // Option 2: NextResponse.redirect
  return NextResponse.redirect(new URL('/login', request.url))
}
```

## Streaming Responses

### Text Streaming

```tsx
export async function GET() {
  const encoder = new TextEncoder()
  const stream = new ReadableStream({
    async start(controller) {
      for (let i = 0; i < 10; i++) {
        controller.enqueue(encoder.encode(`data: ${i}\n\n`))
        await new Promise(resolve => setTimeout(resolve, 100))
      }
      controller.close()
    },
  })

  return new Response(stream, {
    headers: {
      'Content-Type': 'text/event-stream',
      'Cache-Control': 'no-cache',
      'Connection': 'keep-alive',
    },
  })
}
```

### AI/LLM Streaming

```tsx
export async function POST(request: Request) {
  const { prompt } = await request.json()

  const response = await openai.chat.completions.create({
    model: 'gpt-4',
    messages: [{ role: 'user', content: prompt }],
    stream: true,
  })

  const stream = new ReadableStream({
    async start(controller) {
      for await (const chunk of response) {
        const text = chunk.choices[0]?.delta?.content || ''
        controller.enqueue(new TextEncoder().encode(text))
      }
      controller.close()
    },
  })

  return new Response(stream, {
    headers: { 'Content-Type': 'text/plain' },
  })
}
```

## CORS Configuration

```tsx
export async function OPTIONS() {
  return new Response(null, {
    status: 204,
    headers: {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE',
      'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    },
  })
}

export async function GET() {
  return NextResponse.json(
    { data: 'value' },
    {
      headers: {
        'Access-Control-Allow-Origin': '*',
      },
    }
  )
}
```

## Caching

### Static (Default for GET)

```tsx
// Cached by default
export async function GET() {
  const data = await fetch('https://api.example.com/data')
  return NextResponse.json(await data.json())
}
```

### Opt-out of Caching

```tsx
export const dynamic = 'force-dynamic'

export async function GET() {
  // Always fresh
}

// Or use cookies/headers (auto opts out)
import { cookies } from 'next/headers'

export async function GET() {
  const cookieStore = await cookies()
  // Now dynamic
}
```

## Error Handling

```tsx
export async function GET(request: Request) {
  try {
    const data = await riskyOperation()
    return NextResponse.json(data)
  } catch (error) {
    console.error('API Error:', error)

    if (error instanceof ValidationError) {
      return NextResponse.json(
        { error: error.message },
        { status: 400 }
      )
    }

    return NextResponse.json(
      { error: 'Internal Server Error' },
      { status: 500 }
    )
  }
}
```

## Resources

For detailed patterns, see:
- `references/http-methods.md` - Complete HTTP method guide
- `references/streaming-responses.md` - Advanced streaming patterns
- `examples/crud-api.md` - Full CRUD API example
