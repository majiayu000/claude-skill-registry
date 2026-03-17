---
name: nextjs-16
description: Expert Next.js 16 with Turbopack, App Router, Cache Components, proxy.ts, React 19. Use when building Next.js apps, routing, caching, server components, or migrating from v15.
versions:
  nextjs: 16
  react: 19
user-invocable: true
references: references/installation.md, references/upgrade.md, references/project-structure.md, references/typescript.md, references/styling.md, references/app-router.md, references/routing-advanced.md, references/navigation.md, references/route-segment-config.md, references/pages-router.md, references/server-components.md, references/directives.md, references/react-19.md, references/rendering.md, references/streaming.md, references/runtime.md, references/data-fetching.md, references/forms.md, references/static-generation.md, references/cookies-headers.md, references/caching.md, references/cache-components.md, references/turbopack.md, references/react-compiler.md, references/dynamic-imports.md, references/loading-patterns.md, references/error-handling.md, references/proxy.md, references/middleware-migration.md, references/api-routes.md, references/security.md, references/metadata.md, references/metadata-files.md, references/images.md, references/fonts.md, references/scripts.md, references/third-party.md, references/analytics.md, references/instrumentation.md, references/devtools-mcp.md, references/environment.md, references/deployment.md, references/testing.md, references/config-advanced.md
related-skills: nextjs-i18n, better-auth, tailwindcss, solid-nextjs
---

# Next.js 16 Expert

Production-ready React framework with Server Components, streaming, and Turbopack.

## Agent Workflow (MANDATORY)

Before ANY implementation, use `TeamCreate` to spawn 3 agents:

1. **fuse-ai-pilot:explore-codebase** - Analyze existing routes, components, and patterns
2. **fuse-ai-pilot:research-expert** - Verify latest Next.js 16 docs via Context7/Exa
3. **mcp__context7__query-docs** - Check breaking changes v15→v16

After implementation, run **fuse-ai-pilot:sniper** for validation.

---

## Overview

### When to Use

- Building new React applications with server-first architecture
- Need Server Components for optimal performance and SEO
- Implementing streaming and progressive rendering
- Migrating from Next.js 14/15 to version 16
- Using proxy.ts for route protection (replaces middleware)
- Leveraging Turbopack for faster development builds

### Why Next.js 16

| Feature | Benefit |
|---------|---------|
| Turbopack default | 2-5x faster builds, 10x faster HMR, Webpack deprecated |
| Cache Components | Explicit caching with `use cache` directive |
| proxy.ts | Full Node.js runtime, replaces Edge middleware |
| React Compiler | Automatic memoization, no manual useMemo/useCallback |
| React 19 | View Transitions, useEffectEvent, Activity component |
| App Router | Nested layouts, parallel routes, intercepting routes |

---

## Breaking Changes from v15

### Critical Migration Points

1. **proxy.ts replaces middleware.ts** - Full Node.js runtime, not Edge
2. **Turbopack ONLY** - Webpack completely deprecated and removed
3. **`use cache` directive** - Replaces Partial Prerendering (PPR)
4. **React 19 required** - New hooks and View Transitions API
5. **Async params/searchParams** - Must await dynamic route params

---

## SOLID Architecture

### Module-Based Structure

Pages are thin entry points importing from feature modules:

- `app/page.tsx` → imports from `modules/public/home/`
- `app/dashboard/page.tsx` → imports from `modules/auth/dashboard/`
- `modules/cores/` → Shared services, utilities, configurations

### File Conventions

- **page.tsx** - Route UI component
- **layout.tsx** - Shared UI wrapper
- **loading.tsx** - Suspense loading state
- **error.tsx** - Error boundary
- **not-found.tsx** - 404 handling

---

## Core Concepts

### Server Components (Default)

All components are Server Components by default. Use `'use client'` directive only when needed for interactivity, hooks, or browser APIs.

### Caching Strategy

- **`use cache`** - Mark async functions for caching
- **`cacheTag()`** - Tag cached data for targeted revalidation
- **`cacheLife()`** - Control cache duration (stale, revalidate, expire)
- **`revalidateTag()`** - Invalidate cached data on-demand

### Data Fetching

Server Components fetch data directly. Use `fetch()` with native caching or database queries. No need for `getServerSideProps` or `getStaticProps`.

---

## Reference Guide

| Need | Reference |
|------|-----------|
| Initial setup | [installation.md](references/installation.md), [project-structure.md](references/project-structure.md) |
| Migration v15→v16 | [upgrade.md](references/upgrade.md), [middleware-migration.md](references/middleware-migration.md) |
| Routing | [app-router.md](references/app-router.md), [routing-advanced.md](references/routing-advanced.md) |
| Caching | [caching.md](references/caching.md), [cache-components.md](references/cache-components.md) |
| Server Components | [server-components.md](references/server-components.md), [directives.md](references/directives.md) |
| React 19 features | [react-19.md](references/react-19.md), [react-compiler.md](references/react-compiler.md) |
| Route protection | [proxy.md](references/proxy.md), [security.md](references/security.md) |
| SEO/Metadata | [metadata.md](references/metadata.md), [metadata-files.md](references/metadata-files.md) |
| Forms/Actions | [forms.md](references/forms.md), [data-fetching.md](references/data-fetching.md) |
| Deployment | [deployment.md](references/deployment.md), [environment.md](references/environment.md) |

---

## Best Practices

1. **Server Components first** - Only add `'use client'` when necessary
2. **Colocate data fetching** - Fetch data where it's used
3. **Streaming with Suspense** - Wrap slow components in Suspense
4. **proxy.ts over middleware** - Full Node.js runtime for auth
5. **Cache explicitly** - Use `use cache` for expensive operations
6. **Parallel routes** - Load independent UI sections simultaneously

---

## Performance

### Build Optimization

- **Turbopack** - Incremental compilation, instant HMR
- **React Compiler** - Automatic memoization
- **Tree shaking** - Unused code elimination
- **Code splitting** - Automatic route-based splitting

### Runtime Optimization

- **Streaming** - Progressive HTML rendering
- **Partial hydration** - Only hydrate interactive components
- **Image optimization** - Automatic WebP/AVIF conversion
- **Font optimization** - Zero layout shift with next/font
