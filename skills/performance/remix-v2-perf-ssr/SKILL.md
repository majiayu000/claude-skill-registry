---
name: remix-v2-perf-ssr
description: Remix v2 performance, streaming, caching, and server/client boundaries. Use when configuring HTTP caching, server-only modules, hydration safety, or prefetch. Triggers on headers export, Cache-Control, PrefetchPageLinks, Link prefetch, .server.ts, .client.ts, useHydrated, ClientOnly, window.ENV, links preload, useId.
---

# Remix v2 Performance, Streaming, Caching, Server/Client Split

Remix v2 has no built-in image optimizer and no opaque framework cache — it pushes everything to the standard HTTP layer. The performance surface is four pillars: streaming (`defer`/`<Await>`), HTTP caching (`headers` export), prefetching (`<Link prefetch>` and `<PrefetchPageLinks>`), and a hard server/client split (`.server.*` / `.client.*` file conventions).

## Quick Reference

**`headers` export with SWR (forward loader headers to the document)**:
```tsx
import type { HeadersFunction, LoaderFunctionArgs } from "@remix-run/node";
import { json } from "@remix-run/node";

export async function loader({ params }: LoaderFunctionArgs) {
  const post = await cms.getPost(params.slug);
  return json(post, {
    headers: {
      "Cache-Control":
        "public, max-age=60, s-maxage=3600, stale-while-revalidate=86400",
    },
  });
}

export const headers: HeadersFunction = ({ loaderHeaders }) => ({
  "Cache-Control": loaderHeaders.get("Cache-Control") ?? "no-store",
});
```

**`.server.ts` for server-only modules** — build fails loud if the file leaks into the client graph:
```tsx
// app/lib/db.server.ts — never bundled into the client
import { PrismaClient } from "@prisma/client";
export const db = new PrismaClient();
```

**`defer()` for slow secondary data**:
```tsx
import { defer } from "@remix-run/node";
import { Await, useLoaderData } from "@remix-run/react";
import { Suspense } from "react";

export async function loader({ params }: LoaderFunctionArgs) {
  const product = await db.getProduct(params.id);   // critical, awaited
  const reviews = db.getReviews(params.id);          // slow, not awaited
  return defer({ product, reviews });
}

export default function Product() {
  const { product, reviews } = useLoaderData<typeof loader>();
  return (
    <>
      <ProductHeader product={product} />
      <Suspense fallback={<ReviewsSkeleton />}>
        <Await resolve={reviews} errorElement={<ReviewsError />}>
          {(r) => <ReviewList reviews={r} />}
        </Await>
      </Suspense>
    </>
  );
}
```

## Streaming with `defer` and `<Await>`

Every promise passed to `defer` must be created **before** any `await` in the loader, otherwise the loader still blocks on the slow call and streaming gains nothing. Always pair `<Await>` with `errorElement` — without it, a rejected deferred promise bubbles to the route's `ErrorBoundary` and tears down the whole route, defeating the streaming benefit.

See [references/streaming.md](references/streaming.md) for full coverage.

## HTTP Caching via `headers`

`max-age` controls browser cache; `s-maxage` controls shared/CDN cache and overrides `max-age` at the CDN; `stale-while-revalidate` lets the CDN serve stale content while it refreshes in the background. Two cache scopes exist per route: the **document** response (controlled by the `headers` export) and the **data** request (the `?_data=` JSON request fired on client-side navigation — controlled by the loader's response headers). They can — and often should — carry different policies.

**Parent/child merge is "deepest route wins"**: only the deepest matched route's `headers` runs by default. If a child route has no `headers` export, Remix walks up to the nearest parent that does. The safest rule: define `headers` only on leaf routes, never on layouts that wrap personalized children. Otherwise an aggressive parent policy silently caches per-user HTML at the CDN.

When merging in a child, pick the **smaller** `max-age` — never widen a parent's caching policy from a child:
```tsx
export const headers: HeadersFunction = ({ loaderHeaders, parentHeaders }) => {
  const loader = parseCacheControl(loaderHeaders.get("Cache-Control"));
  const parent = parseCacheControl(parentHeaders.get("Cache-Control"));
  const maxAge = Math.min(loader["max-age"] ?? 0, parent["max-age"] ?? 0);
  return { "Cache-Control": `private, max-age=${maxAge}` };
};
```

See [references/headers-caching.md](references/headers-caching.md).

## Server/Client Split

The compiler strips `loader`, `action`, and `headers` exports from client bundles along with the dependencies used **inside them** — but only if those dependencies have no module side effects. A top-level `new PrismaClient()`, a `console.log`, an `initializeApp` call all defeat tree-shaking. Rule: any module that imports `node:fs`, `prisma`, `bcrypt`, `jsonwebtoken`, or reads `process.env` should be named `*.server.ts` (or live under `app/.server/` — directory form requires the Remix Vite plugin; Classic Compiler supports only the filename suffix). Build fails loud if it reaches the client graph — silent leaks are eliminated.

Public env vars reach the browser via a root-loader `window.ENV` pattern. Never return raw `process.env` from a loader. See [references/server-client-split.md](references/server-client-split.md).

## `clientLoader` and `clientAction`

v2 added optional `clientLoader` / `clientAction` exports that run in the browser alongside (or instead of) the server `loader`/`action`. By default `clientLoader` does **NOT** run on initial hydration — the server `loader` SSRs the page, and `clientLoader` only fires on subsequent client navigations. Opt in to first-render execution with `clientLoader.hydrate = true` and export a `HydrateFallback` component to render while it executes:

```tsx
import type { ClientLoaderFunctionArgs } from "@remix-run/react";

export async function loader() {
  return json({ /* SSR data */ });
}

export async function clientLoader({ serverLoader }: ClientLoaderFunctionArgs) {
  const cached = clientCache.get();
  if (cached) return cached;
  const fresh = await serverLoader<typeof loader>(); // round-trip to server loader
  clientCache.set(fresh);
  return fresh;
}
clientLoader.hydrate = true; // opt in to running on initial hydration

export function HydrateFallback() {
  return <Skeleton />;
}
```

Use `clientLoader` for: client-side caching of server payloads, reading from IndexedDB / `localStorage` after hydration, fully client-only routes (skip `loader` entirely). **Do NOT** re-fetch the same server payload SSR'd by the route's `loader` — that's a wasted round-trip; either call `serverLoader()` and cache, or only run on transitions (leave `hydrate` `false`).

## Hydration Safety

`useHydrated()` returns `false` during SSR and on the very first client render, then flips to `true` on the next render — that two-pass behavior is what keeps HTML matched. For components that should never SSR (maps, charts that read `window`), wrap in `<ClientOnly fallback={...}>`. For SSR-safe IDs use React's `useId()`, never `Math.random()` or `crypto.randomUUID()` in render.

The hydration-mismatch grep list: `new Date(`, `Math.random(`, `crypto.randomUUID(`, `Date.now(`, `window.`, `document.`, `localStorage`, `sessionStorage`, `navigator.`, `Intl.DateTimeFormat()` without an explicit locale, `Intl.NumberFormat`, `.toLocaleDateString`, `.toLocaleTimeString`, `.toLocaleString`, `process.env.` in component bodies, `typeof window` ternaries that produce different JSX, third-party scripts that mutate the DOM, browser extensions injecting nodes into `<body>`. See [references/hydration.md](references/hydration.md).

## Prefetching

Four `<Link prefetch>` modes: `"none"` (default), `"intent"` (hover/focus), `"render"` (immediate, on render), `"viewport"` (scrolled into view). Prefetch fires `<link rel="prefetch">` tags as siblings of the anchor — use `:last-of-type` in CSS, not `:last-child`, because the prefetch tags briefly become last child.

A subtle gotcha: hover-prefetch with no `Cache-Control` on the loader doubles the request count because the browser doesn't cache the prefetch response. Detect the `Purpose: prefetch` header in the loader and return `Cache-Control: private, max-age=10`. See [references/prefetch.md](references/prefetch.md).

## Asset Preloading via `links`

The `links` export injects `<link>` tags into the document head — preload critical fonts and CSS, prefetch likely-next-page assets. Remix has no built-in image optimizer; size images at build time (`sharp`, `unpic`, `remix-image`) and always set `width`/`height`. See [references/links-preload.md](references/links-preload.md).

## Gates (decision sequencing)

Answer **in order**. **Pass** means the condition is true; pick the API on the same line and **stop**.

### `defer()` vs awaiting in the loader

1. **Is this data required for the initial paint, meta tags, or SEO** (e.g. product title, page title)?
   - **Pass →** `await` it in the loader, return via `json()`. **Stop.**
   - **Fail →** Step 2.
2. **Is the call genuinely slow** (>~50ms, cross-region DB, external API — not in-memory cache)?
   - **Pass →** Pass the unresolved promise through `defer()`, wrap in `<Suspense>` + `<Await errorElement={...}>`. **Stop.**
   - **Fail →** `await` it. Deferring fast data adds streaming overhead and flashes a skeleton for no gain.

### `.server.ts` vs runtime `typeof window` check

1. **Does the module import `node:*`, `prisma`, `bcrypt`, `jsonwebtoken`, `fs`, `path`, or read `process.env` at the top level**?
   - **Pass →** Name the file `*.server.ts` (or place under `app/.server/` — directory form requires the Remix Vite plugin; Classic Compiler supports only the filename suffix). Build fails loud if leaked to client. **Stop.**
   - **Fail →** Step 2.
2. **Is the module called only inside `loader`/`action`/`headers`** with no top-level side effects?
   - **Pass →** `.server.ts` is still preferred for clarity; tree-shaking may work but is unreliable. **Stop.**
   - **Fail →** Step 3.
3. **Is the code legitimately isomorphic but needs to branch on environment** (logger, feature flag)?
   - **Pass →** `typeof window === "undefined"` is acceptable inside a function body — never at module top level (the dead branch can pull server deps into the client graph).

### `<Link prefetch>` mode selection

1. **Is the link sensitive, expensive, or has loader side effects** (logout, analytics-instrumented page view, mutation-triggering loader)?
   - **Pass →** `prefetch="none"`. **Stop.**
   - **Fail →** Step 2.
2. **Is this an above-the-fold critical nav link** likely to be the next click?
   - **Pass →** `prefetch="render"`. Loader/JS/CSS prefetched immediately. **Stop.**
   - **Fail →** Step 3.
3. **Is the link in a long list** (table row, search results, feed)?
   - **Pass →** `prefetch="viewport"` (fires when scrolled in) or `"intent"` (fires on hover). Never `"render"` on long lists. **Stop.**
   - **Fail →** Step 4.
4. **Default**: `prefetch="intent"` for standard nav (header, sidebar, footer).

## Additional Documentation

- **Headers and caching**: see [references/headers-caching.md](references/headers-caching.md) for `HeadersFunction` signature, `loaderHeaders`/`parentHeaders`/`actionHeaders`/`errorHeaders`, SWR patterns, and parent/child merge semantics.
- **Streaming**: see [references/streaming.md](references/streaming.md) for `defer()`, `<Await>`, `<Suspense>`, `abortDelay`, error handling, CSP interactions.
- **Server/client split**: see [references/server-client-split.md](references/server-client-split.md) for `.server.*` / `.client.*` (directory form requires the Remix Vite plugin; Classic Compiler supports only the filename suffix), env var handling, the `window.ENV` pattern.
- **Hydration**: see [references/hydration.md](references/hydration.md) for `useHydrated`, `<ClientOnly>`, `useId`, mismatch grep list.
- **Prefetch**: see [references/prefetch.md](references/prefetch.md) for `<Link prefetch>` modes, `<PrefetchPageLinks>`, the `Purpose: prefetch` header trick.
- **Preload links**: see [references/links-preload.md](references/links-preload.md) for `links` export, font/CSS preload, image guidance.

## Comparison: When to use which API

| Need | API | Module |
|---|---|---|
| Stream slow secondary data | `defer()` + `<Await>` | `@remix-run/node` + `@remix-run/react` |
| CDN-cache document response | `headers` export | route module |
| CDN-cache data response | `Cache-Control` on `json()`/`Response` | loader return |
| Server-only module | `*.server.ts` filename | file convention |
| Browser-only module | `*.client.ts` filename | file convention |
| Public env vars in client | `window.ENV` via root loader | pattern |
| SSR-safe IDs | `useId()` | `react` |
| Suppress SSR for one component | `<ClientOnly>` | `remix-utils/client-only` |
| Branch after hydration | `useHydrated()` | `remix-utils/use-hydrated` |
| Prefetch on hover | `<Link prefetch="intent">` | `@remix-run/react` |
| Prefetch on render (above-fold) | `<Link prefetch="render">` | `@remix-run/react` |
| Programmatic prefetch | `<PrefetchPageLinks page="/absolute/path">` | `@remix-run/react` |
| Preload font/CSS | `links` export | route module |
