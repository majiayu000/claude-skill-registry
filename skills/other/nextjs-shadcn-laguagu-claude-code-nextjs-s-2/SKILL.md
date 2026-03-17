---
name: nextjs-shadcn
description: Creates Next.js 16 frontends with shadcn/ui. Use when building React UIs, components, pages, or applications with shadcn, Tailwind, or modern frontend patterns.
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
bunx --bun shadcn@latest create --preset "https://ui.shadcn.com/init?base=radix&style=nova&baseColor=neutral&iconLibrary=lucide&font=geist-sans" --template next
```

## Component Rules

### Page Structure

```tsx
// page.tsx - content only, no layout chrome
export default function Page() {
  return (
    <>
      <HeroSection />
      <Features />
      <Testimonials />
    </>
  );
}

// layout.tsx - shared UI (header, footer, sidebar)
export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <>
      <Header />
      <main>{children}</main>
      <Footer />
    </>
  );
}
```

### Client Boundaries

- `"use client"` only at leaf components (smallest boundary)
- Props must be serializable (data or Server Actions, no functions/classes)
- Pass server content via `children`

### Import Aliases

Always use `@/` alias (e.g., `@/lib/utils`) instead of relative paths (`../../lib/utils`).

### Style Merging

```tsx
import { cn } from "@/lib/utils";

function Button({ className, ...props }) {
  return <button className={cn("px-4 py-2 rounded", className)} {...props} />;
}
```

## File Organization

```
app/
├── (protected)/         # Auth required routes
│   ├── dashboard/
│   ├── settings/
│   ├── components/      # Route-specific components
│   └── lib/             # Route-specific utils/types
├── (public)/            # Public routes
│   ├── login/
│   └── register/
├── actions/             # Server Actions (global)
├── api/                 # API routes
├── layout.tsx           # Root layout
└── globals.css          # Theme tokens
components/              # Shared components
├── ui/                  # shadcn primitives
└── shared/              # Business components
hooks/                   # Custom React hooks
lib/                     # Shared utils
data/                    # Database queries
ai/                      # AI logic (tools, agents, prompts)
```

## Next.js 16 Features

### Async Params

```tsx
export default async function Page({
  params,
  searchParams,
}: {
  params: Promise<{ id: string }>;
  searchParams: Promise<{ q?: string }>;
}) {
  const { id } = await params;
  const { q } = await searchParams;
}
```

### Data Fetching vs Server Actions

**CRITICAL RULE:**
- **Server Actions** = ONLY for mutations (create, update, delete)
- **Data fetching** = In Server Components or `'use cache'` functions

```tsx
// ❌ WRONG: Server Action for data fetching
"use server"
export async function getUsers() {
  return await db.users.findMany()
}

// ✅ CORRECT: Data function with caching
// data/users.ts
export async function getUsers() {
  "use cache"
  cacheTag("users")
  cacheLife("hours")
  return await db.users.findMany()
}

// ✅ CORRECT: Read cookies in Server Component directly
export default async function Page() {
  const theme = (await cookies()).get("theme")?.value ?? "light"
  return <App theme={theme} />
}
```

### Caching

```tsx
"use cache";

import { cacheTag, cacheLife } from "next/cache";

export async function getProducts() {
  cacheTag("products");
  cacheLife("hours");
  return await db.products.findMany();
}
```

### Server Actions (Mutations Only)

```tsx
"use server";

import { updateTag, revalidateTag } from "next/cache";
import { z } from "zod";

const schema = z.object({
  title: z.string().min(1),
  content: z.string(),
});

export async function createPost(formData: FormData) {
  // Always validate input
  const parsed = schema.parse({
    title: formData.get("title"),
    content: formData.get("content"),
  });

  await db.insert(posts).values(parsed);
  updateTag("posts"); // Read-your-writes
}
```

### Proxy API

Use `proxy.ts` for request interception (replaces middleware). Place at project root:

```tsx
// proxy.ts (project root, same level as app/)
import { NextResponse } from "next/server"
import type { NextRequest } from "next/server"

export function proxy(request: NextRequest) {
  // Auth checks, redirects, etc.
}

export const config = {
  matcher: ['/dashboard/:path*'],
}
```

## References

- **Architecture**: [references/architecture.md](references/architecture.md) - Components, routing, Suspense, data patterns, AI directory structure
- **Styling**: [references/styling.md](references/styling.md) - Themes, fonts, radius, animations, CSS variables
- **Sidebar**: [references/sidebar.md](references/sidebar.md) - shadcn sidebar with nested layouts
- **Project Setup**: [references/project-setup.md](references/project-setup.md) - bun commands, presets
- **shadcn/ui**: [llms.txt](https://ui.shadcn.com/llms.txt) - Official AI-optimized reference

## Package Manager

**Always use bun**, never npm or npx:

- `bun install` (not npm install)
- `bun add` (not npm install package)
- `bunx --bun` (not npx)
