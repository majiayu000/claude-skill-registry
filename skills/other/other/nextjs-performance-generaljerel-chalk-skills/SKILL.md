---
name: nextjs-performance
description: Audit and optimize Next.js application performance when the user asks about Next.js performance, caching, or rendering strategies
author: chalk
version: "1.0.0"
metadata-version: "3"
allowed-tools: Read, Glob, Grep
argument-hint: "[page path, route, or performance concern]"
read-only: true
destructive: false
idempotent: true
open-world: false
user-invocable: true
tags: nextjs, performance, optimization
---

# Next.js Performance

## Overview

Audit and optimize Next.js applications for performance. Covers the SSR/SSG/ISR decision tree, image and font optimization, route segment caching, and bundle analysis. Stack-specific Tier 3 reference skill.

## Workflow

1. **Read project setup** — Check `.chalk/docs/engineering/` for architecture docs. Determine the Next.js version (App Router vs. Pages Router changes the entire optimization approach), deployment target (Vercel, self-hosted, edge), and data fetching patterns in use.

2. **Identify the scope** — Parse `$ARGUMENTS` for specific pages or routes. If none specified, scan `app/` or `pages/` for routes and identify the highest-traffic or most complex ones.

3. **Audit rendering strategy** — For each route, apply the decision tree:
   - **Static (SSG)**: Content does not change between deploys? Use `generateStaticParams` / `getStaticProps`. Best performance.
   - **Incremental Static (ISR)**: Content changes periodically but not per-request? Use `revalidate` with an appropriate interval. Good balance.
   - **Server (SSR)**: Content is personalized or changes every request? Use dynamic rendering. Ensure streaming with `loading.tsx` or Suspense.
   - **Client**: Content depends on client-only APIs (localStorage, geolocation)? Use `"use client"` components, but keep the boundary as low in the tree as possible.

4. **Audit caching configuration** — Check for:
   - Route segment config (`export const dynamic`, `export const revalidate`) set appropriately per route
   - `fetch` calls with correct cache and revalidation options
   - Missing `cache()` or `unstable_cache()` for expensive server-side computations
   - Over-fetching in layouts that could be cached independently of pages

5. **Audit image optimization** — Check for:
   - Images not using `next/image` (missing automatic optimization, lazy loading, and responsive sizing)
   - Missing `width`/`height` or `sizes` prop causing layout shift
   - Large images served without format conversion (WebP/AVIF)
   - Images above the fold missing the `priority` prop

6. **Audit font optimization** — Check for:
   - Fonts not using `next/font` (causes Flash of Unstyled Text)
   - Multiple font files loaded when a variable font would suffice
   - Font files loaded from external CDNs instead of self-hosted via `next/font`

7. **Audit bundle size** — Check for:
   - Large client-side bundles (use `@next/bundle-analyzer`)
   - Server-only code leaking into client bundles (missing `"server-only"` imports)
   - Barrel file imports pulling in unused code
   - Third-party scripts not loaded with `next/script` and appropriate `strategy`

8. **Report findings** — Present audit results with file references, current state, recommended fix, and expected impact.

## Output

- **Format**: Audit report delivered in the conversation
- **Key sections**: Rendering Strategy Assessment (route-by-route), Caching Configuration Review, Image/Font Optimization Findings, Bundle Analysis, Prioritized Recommendations

## Anti-patterns

- **Making everything dynamic** — Defaulting to SSR when SSG or ISR would work wastes server resources and increases TTFB. Start static, add dynamism only where needed.
- **Ignoring streaming** — Long SSR pages without Suspense boundaries block the entire page. Use `loading.tsx` and Suspense to stream content progressively.
- **Client components at the top** — Placing `"use client"` at the layout level opts the entire subtree out of server rendering. Push client boundaries as low as possible in the component tree.
- **Disabling cache without understanding why** — Adding `export const dynamic = "force-dynamic"` because caching caused a bug means the bug is not fixed, just hidden. Understand the caching behavior and fix the root cause.
- **Skipping next/image for "simplicity"** — Using raw `<img>` tags loses automatic optimization, lazy loading, and responsive sizing. The small learning curve of `next/image` pays for itself immediately.
