---
name: solidstart-hydration-guard
description: "SolidStart hydration guard: keep SSR/CSR output identical, gate browser-only APIs, use stable IDs, align Suspense/resource fallbacks, and use clientOnly/onMount for client-only UI."
metadata:
  globs:
    - "src/app.tsx"
    - "src/routes/**/*"
    - "src/entry-*.tsx"
---

# SolidStart Hydration Guard

## SSR/CSR Symmetry
- No browser-only globals during SSR: guard `window`, `document`, `localStorage`, `matchMedia`, `ResizeObserver` with `if (!isServer)` or `typeof window !== "undefined"`.
- Keep server HTML stable: avoid `Math.random()`, `Date.now()` in render; use `createUniqueId()` or values passed from server data.
- Ensure Suspense fallbacks are the same server/client; don’t branch on browser checks for fallback.
- Avoid rendering different markup based on `isServer` unless the client version is wrapped in `clientOnly` or `<NoHydration>`.

## Stable IDs & Data
- For IDs, use `createUniqueId()` inside components, or pass stable IDs from server data/props.
- Call `createUniqueId()` the same number of times on server and client; don’t gate it behind `isServer` or `<NoHydration>`.
- Only pass JSON-serializable data from server fetchers; avoid class instances/functions.

## Resources & Suspense
- For `createResource`/router `createAsync`, keep `initialValue` consistent between server and client.
- Prefer `ssrLoadFrom: "server"` when you need the server-rendered HTML to match hydration; `"initial"` will re-fetch on the client.
- Use `onHydrated` to inspect resource values during hydration when debugging.
- Resources inside non-hydrating sections are not serialized; wrap client-needed data in `<Hydration>` or pass it through props.
- Use `deferStream` only when you can set headers/status before flush; otherwise keep data in initial render to avoid mismatch.

## Client-Only UI
- Wrap client-only components with `clientOnly` and provide a SSR-safe fallback.
- For browser-only effects (e.g., viewport size), run inside `onMount` or `createEffect` gated by `!isServer`.
- Effects do not run during the initial client hydration, so they cannot fix initial mismatches.
- `<Portal>` is client-only with hydration disabled; use it for overlays that should not hydrate.
- `<NoHydration>` skips hydration for its subtree; use `<Hydration>` to resume for interactive islands when needed.

## Streaming & Headers
- When streaming (`renderToStream`), set `HttpHeader`/`HttpStatusCode` before first flush; hydrate assumes status/headers are fixed.

## Router Integration
- Wrap `<FileRoutes />` with `<Suspense>` in the Router root to avoid hydration errors.
- Keep route `preload` functions pure; SSR runs them and resumes on the client during hydration.

## Document & Script Setup
- Include `<HydrationScript />` once (SolidStart injects it via the document `assets` slot).

## Debug Checklist
- Verify Router root uses `<Suspense>` and that fallbacks match server/client.
- Check for non-deterministic render output (`Math.random()`, `Date.now()`).
- Confirm `createUniqueId()` call counts are identical on server/client.
- Validate query args and server data are JSON-serializable.
- If you must render different client UI, isolate it with `clientOnly`, `<NoHydration>`, or `<Portal>`.

## Quick Checks
- Are all browser APIs guarded? 
- Are IDs and fallbacks stable between server and client? 
- Are Suspense boundaries identical on both sides?
