---
name: ssr-migration
description: >-
  Migrate client-side rendered (CSR) React/Vue applications to server-side
  rendering (SSR) or static site generation (SSG) using Next.js, Nuxt, or
  Astro. Use when you need to improve SEO, reduce time-to-first-byte, fix
  blank page issues for crawlers, or improve Core Web Vitals. Covers
  incremental adoption, data fetching patterns, hydration debugging, and
  deployment configuration. Trigger words: SSR, SSG, server-side rendering,
  static generation, Next.js migration, SEO, hydration, TTFB, Core Web Vitals.
license: Apache-2.0
compatibility: "Node.js 18+. React 18+ for Next.js, Vue 3+ for Nuxt 3."
metadata:
  author: terminal-skills
  version: "1.0.0"
  category: development
  tags: ["ssr", "ssg", "nextjs", "performance", "seo"]
---

# SSR Migration

## Overview
This skill guides the migration of client-side rendered single-page applications to server-side rendering or static site generation. It covers the incremental migration strategy (not a rewrite), identifying which pages benefit from SSR vs SSG vs CSR, fixing hydration mismatches, adapting data fetching patterns, and configuring deployment for SSR workloads.

## Instructions

### 1. Audit the current CSR application
Identify what needs to change before migrating:

```bash
# Check for SSR-incompatible patterns:
# 1. Direct window/document access at module level
grep -rn "window\." src/ --include="*.tsx" --include="*.ts" | grep -v "typeof window"

# 2. Browser-only libraries imported at top level
grep -rn "import.*from.*('|\")(chart.js|swiper|mapbox)" src/

# 3. localStorage/sessionStorage usage outside useEffect
grep -rn "localStorage\|sessionStorage" src/ --include="*.tsx"

# 4. Dynamic imports that should stay client-only
grep -rn "React.lazy\|dynamic(" src/ --include="*.tsx"
```

Classify each page by rendering strategy:
- **SSG** — content changes rarely, same for all users (marketing pages, blog posts, docs)
- **SSR** — content changes frequently or is user-specific (dashboards, search results)
- **CSR** — highly interactive, no SEO need (admin panels, internal tools)

### 2. Set up Next.js App Router alongside existing code
Migrate incrementally using Next.js App Router:

```typescript
// app/products/page.tsx — SSG with revalidation
export const revalidate = 3600; // Regenerate every hour

async function getProducts() {
  const res = await fetch("https://api.example.com/products", {
    next: { revalidate: 3600 },
  });
  return res.json();
}

export default async function ProductsPage() {
  const products = await getProducts();
  return (
    <main>
      <h1>Products</h1>
      <ProductGrid products={products} />
    </main>
  );
}

// app/products/[id]/page.tsx — SSG with dynamic params
export async function generateStaticParams() {
  const products = await fetch("https://api.example.com/products").then(r => r.json());
  return products.map((p: { id: string }) => ({ id: p.id }));
}

export default async function ProductPage({ params }: { params: { id: string } }) {
  const product = await fetch(`https://api.example.com/products/${params.id}`).then(r => r.json());
  return <ProductDetail product={product} />;
}
```

### 3. Handle hydration mismatches
The most common migration bugs are hydration errors:

```typescript
// BAD — different output on server vs client
function Greeting() {
  return <p>Current time: {new Date().toLocaleTimeString()}</p>;
}

// GOOD — defer client-only content
"use client";
import { useState, useEffect } from "react";

function Greeting() {
  const [time, setTime] = useState<string | null>(null);
  useEffect(() => {
    setTime(new Date().toLocaleTimeString());
  }, []);
  return <p>Current time: {time ?? "Loading..."}</p>;
}
```

### 4. Migrate data fetching patterns

```typescript
// BEFORE (CSR): useEffect + useState
function Dashboard() {
  const [data, setData] = useState(null);
  useEffect(() => {
    fetch("/api/dashboard").then(r => r.json()).then(setData);
  }, []);
  if (!data) return <Spinner />;
  return <DashboardView data={data} />;
}

// AFTER (SSR): Server Component with async/await
async function Dashboard() {
  const data = await fetch("http://internal-api/dashboard", {
    headers: { cookie: cookies().toString() },
  }).then(r => r.json());
  return <DashboardView data={data} />;
}
```

### 5. Configure deployment for SSR

```dockerfile
# Dockerfile for Next.js SSR
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:20-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static
COPY --from=builder /app/public ./public
EXPOSE 3000
CMD ["node", "server.js"]
```

## Examples

### Example 1: Marketing site migration
**Prompt:** "Migrate our React SPA marketing site to Next.js with SSG. We have 12 pages: homepage, 5 product pages, pricing, about, blog listing, blog posts (40 articles), contact, and FAQ."

**Agent output:**
- Creates Next.js App Router structure with static pages for homepage, pricing, about, contact, FAQ
- Blog listing and posts use `generateStaticParams` + ISR (revalidate every 30 minutes)
- Product pages use SSG with on-demand revalidation via webhook
- Identifies 3 components using `window` directly — wraps them in dynamic imports with `ssr: false`
- Adds `next-sitemap` configuration for automatic XML sitemap generation

### Example 2: Dashboard with mixed rendering
**Prompt:** "Our React dashboard app needs SSR for the main feed (SEO matters) but the settings and admin pages can stay client-rendered. How do I set this up incrementally?"

**Agent output:**
- Creates `app/(public)/feed/page.tsx` as a Server Component with SSR
- Creates `app/(private)/settings/page.tsx` with `"use client"` directive, keeping existing CSR logic
- Adds middleware for authentication that redirects unauthenticated users before SSR runs
- Migrates the feed's `useEffect` data fetching to server-side `fetch` with cookie forwarding
- Keeps the real-time notification widget as a Client Component embedded within the SSR layout

## Guidelines

- **Migrate incrementally** — move one route at a time, not the entire app at once.
- **Start with SSG pages** — they're the easiest win and don't require a Node.js server.
- **Use `"use client"` sparingly** — only for components that genuinely need browser APIs or interactivity.
- **Test hydration in development** — React 18's strict mode double-renders to catch mismatches early.
- **Forward cookies for authenticated SSR** — server-side fetch won't include user cookies automatically.
- **Monitor TTFB after migration** — SSR adds server computation time. If TTFB increases, consider caching or ISR.
- **Keep bundle size in check** — SSR doesn't eliminate the need for code splitting. Use dynamic imports for heavy client components.
