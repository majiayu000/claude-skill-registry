---
name: arcanea-next-best-practices
description: Next.js 16 App Router best practices for Arcanea. Use when writing or reviewing Next.js page files, layouts, route handlers, middleware, metadata, image/font optimization, RSC boundaries, async params/cookies, or any App Router pattern. Triggers on: layout.tsx, page.tsx, route.ts, loading.tsx, error.tsx, generateMetadata, Server Actions, 'use client', 'use server', next/image, next/font. Sourced from Vercel's official next-skills repository.
license: MIT (source: vercel-labs/next-skills)
metadata:
  author: Arcanea (adapted from Vercel Labs)
  version: "1.0.0"
  stack: Next.js 16 App Router, React 19, TypeScript strict
---

# Arcanea Next.js 16 Best Practices

> *"Aiyami guards the Crown Gate at 741 Hz — Enlightenment. Correct App Router patterns are enlightenment. Wrong patterns are Malachar's confusion."*

## File Conventions

### Route Structure
```
apps/web/app/
├── layout.tsx           # Root layout (html + body)
├── page.tsx             # Home page
├── (marketing)/         # Route group (no URL segment)
│   ├── about/page.tsx
│   └── pricing/page.tsx
├── lore/
│   ├── layout.tsx       # Nested layout
│   ├── page.tsx         # /lore
│   ├── [element]/
│   │   └── page.tsx     # /lore/fire, /lore/water...
│   └── [...slug]/
│       └── page.tsx     # Catch-all: /lore/fire/draconia/...
├── academy/
│   └── gates/
│       └── [gate]/
│           └── page.tsx # /academy/gates/foundation
└── api/
    └── guardians/
        └── route.ts     # GET/POST /api/guardians
```

### Special Files (all must be .tsx for JSX)
| File | Purpose |
|------|---------|
| `layout.tsx` | Shared UI, persists across navigation |
| `page.tsx` | Unique route UI |
| `loading.tsx` | Suspense boundary automatically |
| `error.tsx` | Error boundary (must be `'use client'`) |
| `not-found.tsx` | 404 handling |
| `global-error.tsx` | Root error boundary |
| `route.ts` | API endpoint (no JSX) |
| `middleware.ts` | App root only (not in app/) |

---

## RSC Boundaries

### Server Component (default — no directive needed)
```typescript
// app/lore/[element]/page.tsx — Server Component by default
import { supabase } from '@/lib/supabase-server'

export default async function ElementPage({ params }: { params: Promise<{ element: string }> }) {
  const { element } = await params // NEXT.JS 16: params is now a Promise
  const { data } = await supabase.from('elements').select().eq('slug', element).single()
  return <ElementProfile data={data} />
}
```

### Client Component — only when needed
```typescript
// 'use client' required for: useState, useEffect, event handlers, browser APIs
'use client'
import { useState } from 'react'

export function GateQuiz() {
  const [selectedGate, setSelectedGate] = useState<string | null>(null)
  return <div onClick={() => setSelectedGate('foundation')}>...</div>
}
```

### Invalid Patterns — RSC Errors
```typescript
// ERROR: async Client Component (not allowed in React 19)
'use client'
export default async function Invalid() { // async + 'use client' = ERROR
  const data = await fetch(...)
}

// ERROR: non-serializable props from Server to Client
// Server Component:
<ClientComp fn={() => console.log('hi')} /> // Functions can't cross RSC boundary

// VALID: Serialize data before passing
<ClientComp data={JSON.parse(JSON.stringify(complexObject))} />
```

---

## Async APIs (Next.js 16 BREAKING CHANGES)

Next.js 16 made these APIs async. Always await them:

```typescript
// app/academy/page.tsx
import { cookies, headers } from 'next/headers'

export default async function AcademyPage({
  params,
  searchParams,
}: {
  params: Promise<{ slug: string }> // NOW A PROMISE
  searchParams: Promise<{ gate?: string }> // NOW A PROMISE
}) {
  const { slug } = await params
  const { gate } = await searchParams
  const cookieStore = await cookies() // NOW ASYNC
  const headersList = await headers() // NOW ASYNC
  
  const token = cookieStore.get('arcanea-session')
  // ...
}
```

### Server Actions — async params too
```typescript
'use server'
import { cookies } from 'next/headers'

export async function unlockGate(gate: string) {
  const cookieStore = await cookies() // async in Next.js 16
  cookieStore.set('gate-unlocked', gate)
}
```

---

## Error Handling

### error.tsx — Must be Client Component
```typescript
// app/lore/error.tsx
'use client'
import { useEffect } from 'react'

export default function LoreError({
  error,
  reset,
}: {
  error: Error & { digest?: string }
  reset: () => void
}) {
  useEffect(() => {
    console.error('[Lore Error]', error)
  }, [error])

  return (
    <div className="glass-card text-center">
      <h2 className="text-gradient-aurora">The Lore is Veiled</h2>
      <p className="text-white/70">{error.message}</p>
      <button onClick={reset} className="btn-cosmic">Try Again</button>
    </div>
  )
}
```

### Redirect and notFound in Server Components
```typescript
import { redirect, notFound } from 'next/navigation'

export default async function GuardianPage({ params }: { params: Promise<{ gate: string }> }) {
  const { gate } = await params
  const guardian = await getGuardian(gate)
  
  if (!guardian) notFound() // renders not-found.tsx
  if (guardian.deprecated) redirect(`/lore/guardians/${guardian.newSlug}`)
  
  return <GuardianProfile guardian={guardian} />
}
```

---

## Metadata & SEO

### Static Metadata
```typescript
// app/lore/layout.tsx
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Lore | Arcanea',
  description: 'The mythology of the Ten Gates and Five Elements',
  openGraph: {
    title: 'Arcanea Lore',
    description: 'Enter the mythology.',
    images: ['/og/lore.png'],
  },
}
```

### Dynamic Metadata
```typescript
// app/lore/[element]/page.tsx
export async function generateMetadata({
  params,
}: {
  params: Promise<{ element: string }>
}): Promise<Metadata> {
  const { element } = await params
  const data = await getElement(element)
  
  return {
    title: `${data.name} | Arcanea Lore`,
    description: data.description,
    openGraph: {
      images: [data.ogImage],
    },
  }
}
```

### OG Image Generation
```typescript
// app/lore/[element]/opengraph-image.tsx
import { ImageResponse } from 'next/og'

export const runtime = 'edge'
export const size = { width: 1200, height: 630 }

export default async function OGImage({ params }: { params: Promise<{ element: string }> }) {
  const { element } = await params
  return new ImageResponse(
    <div style={{ background: 'linear-gradient(135deg, #1a0a2e, #0d1b40)', width: '100%', height: '100%' }}>
      <h1 style={{ color: '#7fffd4', fontSize: 72 }}>{element}</h1>
    </div>
  )
}
```

---

## Image Optimization

### Always next/image — Never raw <img>
```typescript
import Image from 'next/image'

// Local image — width/height required
<Image src="/godbeast/draconis.png" alt="Draconis" width={800} height={600} />

// Remote image — configure in next.config.ts
<Image
  src="https://cdn.arcanea.ai/guardians/draconia.jpg"
  alt="Draconia"
  fill // fills container — parent needs position: relative
  sizes="(max-width: 768px) 100vw, 50vw"
  priority // add for LCP images (above-the-fold)
/>
```

### Remote images config
```typescript
// next.config.ts
const config: NextConfig = {
  images: {
    remotePatterns: [
      { protocol: 'https', hostname: 'cdn.arcanea.ai' },
      { protocol: 'https', hostname: '*.supabase.co' },
    ],
  },
}
```

---

## Font Optimization

### next/font — Always, never link tags
```typescript
// app/layout.tsx — Arcanea font setup
// MEMORY.md override: Inter everywhere, no Cinzel in new code
import { Inter, JetBrains_Mono } from 'next/font/google'

const inter = Inter({
  subsets: ['latin'],
  variable: '--font-inter',
  display: 'swap',
})

const jetbrains = JetBrains_Mono({
  subsets: ['latin'],
  variable: '--font-code',
  display: 'swap',
})

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className={`${inter.variable} ${jetbrains.variable}`}>
      <body>{children}</body>
    </html>
  )
}
```

---

## Route Handlers

```typescript
// app/api/guardians/route.ts
import { NextRequest, NextResponse } from 'next/server'
import { createServerClient } from '@/lib/supabase-server'

// IMPORTANT: GET handler conflicts with page.tsx in same directory
// Use separate directories: app/api/guardians/route.ts (no page.tsx here)

export async function GET(request: NextRequest) {
  const supabase = createServerClient()
  const { searchParams } = new URL(request.url)
  const gate = searchParams.get('gate')
  
  const query = supabase.from('guardians').select()
  if (gate) query.eq('gate', gate)
  
  const { data, error } = await query
  if (error) return NextResponse.json({ error: error.message }, { status: 500 })
  return NextResponse.json(data)
}

export async function POST(request: NextRequest) {
  const supabase = createServerClient()
  const { data: { user } } = await supabase.auth.getUser()
  if (!user) return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
  
  const body = await request.json()
  const { data, error } = await supabase.from('user_progress').insert(body).select().single()
  if (error) return NextResponse.json({ error: error.message }, { status: 500 })
  return NextResponse.json(data, { status: 201 })
}
```

---

## Bundling Gotchas

```typescript
// Server-incompatible packages — use dynamic import with ssr: false
// fs, path, canvas, sharp — Server only (ok in RSC)
// window, document, navigator — Client only (use dynamic or 'use client')

// CSS — import in JS files, never link tags
import '@/styles/globals.css' // correct
// <link rel="stylesheet"> in layout is WRONG for App Router

// next.config.ts — transpile if needed
const config: NextConfig = {
  transpilePackages: ['@arcanea/ui'],
}
```

---

## Quick Checklist

Before any Next.js 16 page/route in Arcanea:

- [ ] `params` and `searchParams` awaited (they're Promises in Next.js 16)
- [ ] `cookies()` and `headers()` awaited
- [ ] `'use client'` only where browser APIs or interactivity needed
- [ ] No async Client Components
- [ ] `generateMetadata` returns proper OG data
- [ ] Images use `next/image` with sizes and priority where above fold
- [ ] Fonts use `next/font` — Inter + JetBrains Mono only
- [ ] Route handlers in `/api/` separate from page routes
- [ ] error.tsx has `'use client'` directive
