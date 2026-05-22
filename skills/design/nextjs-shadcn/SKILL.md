---
name: nextjs-shadcn
description: Creates Next.js 16 frontends with shadcn/ui. Use when building React UIs, components, pages, or applications with shadcn, Tailwind, or modern frontend patterns.
user-invocable: true
---

# Next.js 16 + shadcn/ui

Build distinctive, production-grade interfaces that avoid generic "AI slop" aesthetics.

## Core Principles

1. **Minimize noise** - Icons communicate; excessive labels don't
2. **No generic AI-UI** - Avoid purple gradients, excessive shadows, predictable layouts
3. **Context over decoration** - Every element serves a purpose
4. **Theme consistency** - Use CSS variables from `globals.css`, never hardcode colors

## Quick Start

```bash
bunx --bun shadcn@latest create --preset "https://ui.shadcn.com/init?style=vega&iconLibrary=lucide" --template next
```

## Component Rules

### Page Structure
```tsx
// page.tsx - flat composition, no logic
export default function Page() {
  return (
    <>
      <Header />
      <HeroSection />
      <Features />
      <Footer />
    </>
  )
}
```

### Client Boundaries
- `"use client"` only at leaf components (smallest boundary)
- Props must be serializable (data or Server Actions, no functions/classes)
- Pass server content via `children`

### Style Merging
```tsx
import { cn } from "@/lib/utils"

function Button({ className, ...props }) {
  return (
    <button className={cn("px-4 py-2 rounded", className)} {...props} />
  )
}
```

## File Organization

```
app/
├── (marketing)/         # Route group - no URL segment
│   ├── about/
│   └── pricing/
├── (dashboard)/         # Another route group
│   ├── dashboard/
│   ├── settings/
│   ├── components/      # Route-specific components
│   └── lib/             # Route-specific utils/types
├── (auth)/
│   ├── login/
│   └── register/
├── layout.tsx           # Root layout
└── globals.css          # Theme tokens
components/              # Shared components
lib/                     # Shared utils
```

## Next.js 16 Features

### Async Params
```tsx
export default async function Page({
  params,
  searchParams,
}: {
  params: Promise<{ id: string }>
  searchParams: Promise<{ q?: string }>
}) {
  const { id } = await params
  const { q } = await searchParams
}
```

### Caching
```tsx
"use cache"

export async function getData() {
  // Cached at function level
}
```

### Server Actions
```tsx
"use server"

import { updateTag, revalidateTag } from "next/cache"

export async function createPost(data: FormData) {
  // Validate with Zod
  await db.insert(posts).values(parsed)
  updateTag("posts")  // Read-your-writes
}
```

### Proxy API
Use `proxy.ts` for request interception (replaces middleware):
```tsx
// app/api/[...proxy]/proxy.ts
export function proxy(request: Request) {
  // Auth checks, redirects, etc.
}
```

## References

- **Architecture**: [references/architecture.md](references/architecture.md) - Components, routing, Suspense, data patterns
- **Styling**: [references/styling.md](references/styling.md) - Themes, animations, CSS variables
- **Project Setup**: [references/project-setup.md](references/project-setup.md) - bun commands, presets

## Package Manager

**Always use bun**, never npm or npx:
- `bun install` (not npm install)
- `bun add` (not npm install package)
- `bunx --bun` (not npx)
