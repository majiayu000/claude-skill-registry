---
name: nextjs-knowledge-skill
description: >
  Skill providing structured Next.js knowledge: App Router patterns, RSC
  usage, rendering/data strategies, and modern Next.js best practices.
---

# Next.js Knowledge Skill – Architecture & Patterns

This skill equips agents with high-level Next.js knowledge without bloating
individual agent prompts.

It is intended for:
- `nextjs-grand-architect`
- `nextjs-architect`
- Next.js specialists (TS/perf/a11y/SEO) when they need architectural context.

## Core Next.js Concepts (v13+)

### App Router

- **File-system routing** with `app/` directory
- **Layouts** for shared UI across routes
- **Route groups** `(folder)` for organization without affecting URL
- **Parallel routes** `@folder` for simultaneous rendering
- **Intercepting routes** `(..)folder` for modals and overlays

### React Server Components (RSC)

- **Server Components** (default): Render on server, reduce client bundle
  - Good for: Data fetching, accessing backend resources, static content
  - Cannot: Use hooks, handle events, use browser APIs

- **Client Components** (`"use client"`): Run in browser
  - Good for: Interactivity, hooks, event handlers, browser APIs
  - Pattern: Keep client boundaries as low in the tree as possible

### Rendering Strategies

1. **Static Site Generation (SSG)**
   - Pre-render at build time
   - Use: `output: 'export'` for full static export
   - Use: `generateStaticParams()` for dynamic routes

2. **Server-Side Rendering (SSR)**
   - Render on each request
   - Use: `cache: 'no-store'` in fetch

3. **Incremental Static Regeneration (ISR)**
   - Re-generate pages after deployment
   - Use: `revalidate` option in fetch or route segment config

4. **Streaming**
   - Send UI progressively as it renders
   - Use: `loading.tsx` for instant loading states
   - Use: Suspense boundaries for granular streaming

### Data Fetching Patterns

- **Server Components**: Fetch directly in component
  ```tsx
  async function getData() {
    const res = await fetch('https://...', { cache: 'force-cache' })
    return res.json()
  }

  export default async function Page() {
    const data = await getData()
    return <div>{data.title}</div>
  }
  ```

- **Parallel Fetching**: Multiple fetches resolve concurrently
- **Sequential Fetching**: Await one fetch before starting another
- **Automatic Deduplication**: Same fetch called multiple times → single request

### Static Exports

For fully static sites (`output: 'export'`):
- All routes pre-rendered at build time
- No server-side features (Server Actions, dynamic routes without `generateStaticParams`)
- Data fetching runs during `next build`
- Good for: Hosting on CDN, static site hosts, or edge networks

### CSS & Styling

Next.js supports multiple approaches:
- **CSS Modules**: Scoped CSS with `.module.css` files
- **Global CSS**: Import in `app/layout.tsx`
- **CSS-in-JS**: styled-components, emotion, etc.
- **Utility-first**: Tailwind CSS integration
- **Sass**: Built-in support for `.scss` and `.sass`

## Usage Pattern

1. When planning a Next.js task:
   - Determine rendering strategy (static, SSR, ISR)
   - Decide RSC vs client component boundaries
   - Choose data fetching approach
   - Consider caching strategy

2. When writing implementation plans:
   - Reflect these decisions in architecture path
   - Document component boundaries (server vs client)
   - Note any dynamic routes needing `generateStaticParams`

3. Best practices:
   - **Prefer Server Components** for non-interactive content
   - **Use Client Components** only where needed (interactivity, hooks)
   - **Leverage caching** with appropriate fetch options
   - **Optimize images** with `next/image`
   - **Use route groups** for clean organization

This skill provides the architectural foundation for building performant,
well-structured Next.js applications without requiring agents to memorize
all patterns upfront.
