---
name: nextjs-fullstack
description: Next.js App Router patterns for full-stack applications. Use when building Next.js apps with App Router, Server Components, API Routes, authentication, or full-stack React applications.
---

# Next.js App Router Patterns

## Project Structure
```
app/
  (auth)/           # Route group (no URL segment)
    login/page.tsx
    register/page.tsx
  (dashboard)/
    layout.tsx      # Dashboard shell with nav
    page.tsx        # Dashboard home
    users/page.tsx
  api/              # API routes
    auth/[...nextauth]/route.ts
    users/route.ts
  layout.tsx        # Root layout (html, body, providers)
  globals.css
components/
  ui/               # Reusable primitives (Button, Input, Modal)
  features/         # Feature-specific components
lib/
  db.ts             # Prisma client
  auth.ts           # NextAuth config
  validations.ts    # Zod schemas
```

## Server Component (default — no 'use client')
```tsx
// app/users/page.tsx — runs on server, has direct DB access
import { db } from '@/lib/db'

export default async function UsersPage() {
  const users = await db.user.findMany({ orderBy: { createdAt: 'desc' } })
  return (
    <div>
      {users.map(u => <UserCard key={u.id} user={u} />)}
    </div>
  )
}
```

## Client Component (interactive)
```tsx
'use client'
import { useState } from 'react'

export function Counter() {
  const [count, setCount] = useState(0)
  return <button onClick={() => setCount(c => c + 1)}>{count}</button>
}
```

## Server Action (form submit without API route)
```tsx
// app/actions.ts
'use server'
import { revalidatePath } from 'next/cache'
import { db } from '@/lib/db'

export async function createUser(formData: FormData) {
  const name = formData.get('name') as string
  if (!name) throw new Error('Name required')
  await db.user.create({ data: { name } })
  revalidatePath('/users')
}

// Usage in Server Component:
<form action={createUser}>
  <input name="name" />
  <button type="submit">Create</button>
</form>
```

## API Route
```tsx
// app/api/users/route.ts
import { NextRequest, NextResponse } from 'next/server'
import { getServerSession } from 'next-auth'

export async function GET(req: NextRequest) {
  const session = await getServerSession(authOptions)
  if (!session) return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
  const users = await db.user.findMany()
  return NextResponse.json(users)
}

export async function POST(req: NextRequest) {
  const body = await req.json()
  const parsed = UserCreateSchema.safeParse(body)
  if (!parsed.success) return NextResponse.json({ error: parsed.error }, { status: 400 })
  const user = await db.user.create({ data: parsed.data })
  return NextResponse.json(user, { status: 201 })
}
```

## Metadata & SEO
```tsx
export const metadata: Metadata = {
  title: 'My App',
  description: '...',
  openGraph: { title: '...', images: ['/og.png'] }
}
```

## Rules
- Default to Server Components — only use 'use client' when you need interactivity
- Use Server Actions for mutations (simpler than API routes for form submits)
- Validate ALL input with Zod on the server side
- Protect routes in middleware.ts (not just in components)
- Use loading.tsx for Suspense boundaries on slow data fetches
- Use error.tsx for error boundaries
- Never fetch data in Client Components if a Server Component can do it
