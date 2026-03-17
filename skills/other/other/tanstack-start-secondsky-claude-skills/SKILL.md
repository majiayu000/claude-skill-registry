---
name: tanstack-start
description: TanStack Start (RC) full-stack React with server functions, SSR, Cloudflare Workers. Use for Next.js migration, edge rendering, or encountering hydration, auth, data pattern errors.
license: MIT
allowed-tools: [Bash, Read, Write, Edit]
metadata:
  version: 1.0.0-rc.1
  author: Claude Skills Maintainers
  last-verified: 2025-12-09
  production-tested: false
  status: rc
  keywords:
    - tanstack start
    - tanstack react start
    - full-stack react
    - selective ssr
    - spa mode
    - static prerender
    - server functions
    - server routes
  - cloudflare workers
  - edge rendering
  - hydration errors
  - next.js migration
---

# TanStack Start (React) — RC-Ready Playbook

Full-stack React on TanStack Router with per-route SSR/CSR, file-based routing, server functions, and first-class Cloudflare Workers support.

## Use this skill when
- Building a greenfield React app that needs route-level SSR/CSR/SSG switches.
- Migrating from Next.js/React Router while keeping file-based routing + API routes.
- Shipping to edge runtimes (Workers) with typed server functions and bindings.
- You want predictable routing with type-safe params/search + built-in preloading.

## What’s inside
- **References**: quickstart/layout, rendering modes, server functions, Cloudflare hosting, execution/auth, plus new routing/data/navigation/devtools guides.
- **Script**: `scripts/bootstrap-cloudflare-start.sh <app>` scaffolds Start + Workers + binding types.
- **Troubleshooting**: hydration, API routing, bindings, navigation/preloading failures.

---

## Quick Start (React)
```bash
npm create @tanstack/start@latest my-app
cd my-app
npm run dev
```
Manual installs (all bundle targets are supported): add `@tanstack/react-router` + `@tanstack/react-start` with your bundler plugin (`vite`, `webpack`, or `esbuild`) per the official install guides.

### Core layout reminder
- `app/routes/**` file-based routes → router tree, automatic code-splitting + data preloading.
- `app/entry.client.tsx` hydrates `<StartClient />`; `app/entry.server.tsx` wraps `createServerEntry`.
- `app/config.ts` or `app/start.ts` sets `defaultSsr`, `spaMode`, middleware, and context.

---

## Routing + Data Best Practices

- **Type-safe params & search**: `createFileRoute()` infers path params; add `validateSearch` (zod) to parse and coerce search params.
- **Route matching order is deterministic** (index → static → dynamic → splat); rely on this when adding catch-alls.
- **Loaders run once per location change**; return plain data, throw `redirect()`/`notFound()` for control flow.
- **Data mutations**: colocate `action`/server functions; keep loaders read-only and invalidate via `router.invalidate()` after mutation.
- **TanStack Query bridge**: create a `QueryClient` in router context and `ensureQueryData` inside loaders to dedupe fetches.
- **Deferred/external data**: stream partial data or read from external loaders; prefer suspense-friendly responses.
- **Head management**: set `head` per route for `<title>`/meta; derive from loader data to keep SEO consistent.
- **Not-found/auth**: throw `notFound()` or `redirect()` in loaders/middleware; use error boundaries for UX.

Example route (typed search + data-only SSR):
```ts
// app/routes/posts.$postId.tsx
import { createFileRoute, redirect } from '@tanstack/react-router'
import { z } from 'zod'

export const Route = createFileRoute('/posts/$postId')({
  validateSearch: z.object({ preview: z.boolean().optional() }),
  ssr: 'data-only',
  loader: async ({ params, search, context }) => {
    const post = await context.queryClient.ensureQueryData(['post', params.postId], () =>
      fetch(`/api/posts/${params.postId}?preview=${!!search.preview}`).then(r => r.json())
    )
    if (!post.published && !search.preview) throw redirect({ to: '/drafts' })
    return { post }
  },
})
```

---

## Navigation, Preloading, and UX

- **Link prefetch defaults**: `<Link preload="intent">` (hover/focus) preloads route data/code; use `preload="render"` for above-the-fold routes.
- **Programmatic preloading**: `router.preloadRoute({ to, search })` to warm caches before navigation (e.g., on visibility).
- **Route masking**: keep canonical URLs while showing user-friendly masks (e.g., `/products?slug=abc` masked as `/p/abc`).
- **Navigation blocking**: protect unsaved forms with `router.navigate({ to, replace, from })` blockers or `useBlocker`.
- **Scroll restoration**: enable `scrollRestoration` to restore positions on back/forward; customize per route when using long lists.
- **Search param serialization**: customize parse/stringify to keep numbers/dates stable and avoid stringified booleans.

---

## Rendering & Performance

- **Per-route SSR**: set `ssr: true | false | 'data-only'` on routes; `defaultSsr` config sets the baseline.
- **Code-splitting**: file-based routes auto-split; add `lazy`/`load` for manual chunks on code-based routes.
- **Preloading strategy**: pair `preload="intent"` links with `defaultPreloadStaleTime` to avoid over-fetching.
- **Render optimizations**: keep loaders pure, memoize heavy components, and use `pendingComponent` for CSR routes to avoid layout shift.

---

## Devtools, Linting, and LLM Support

- Add `<RouterDevtools />` during development to inspect matches, loader states, and preloading.
- Enable the ESLint plugin `@tanstack/eslint-plugin-router` with the recommended config to enforce inference-sensitive property order (e.g., `beforeLoad` before `loader`).
- LLM-aware routing: the Router exposes structured route metadata to LLM agents; keep descriptions concise in `Route` meta for better AI navigation.

---

## Deployment Notes (Cloudflare-friendly)

- Keep `cloudflare({ viteEnvironment: { name: 'ssr' } })` first in Vite plugins so bindings reach server entry.
- Regenerate bindings after changes: `npm run cf-typegen`.
- For static-heavy sites, enable prerender to ship HTML to Workers Assets/Pages; exclude param routes or add explicit `pages`.

---

## Ship Checklist
- [ ] Routes load without hydration warnings (prefer `ssr: 'data-only'` for non-deterministic UI).
- [ ] Search params validated with `validateSearch` and custom serializer where needed.
- [ ] Link preloading configured for high-traffic routes; blockers added for unsaved forms.
- [ ] ESLint plugin enabled (`create-route-property-order` rule) and `npm run check` passes.
- [ ] Devtools verified locally; `router.matches` state looks correct.
- [ ] Cloudflare bindings typed (`cf-typegen`) and streaming tested via `curl -N`.
