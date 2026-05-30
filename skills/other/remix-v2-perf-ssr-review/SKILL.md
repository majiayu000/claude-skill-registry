---
name: remix-v2-perf-ssr-review
description: Reviews Remix v2 code for caching header misuse, missing server/client split, hydration mismatches (Date, Math.random, locale), prefetch hygiene, and asset bottlenecks. Use when reviewing routes that export headers, use .server.ts/.client.ts, or render dates/IDs in a Remix v2 codebase.
---

# Remix v2 Performance / SSR Code Review

Targets TypeScript route modules importing from `@remix-run/*`. See [beagle-react:remix-v2-perf-ssr](../remix-v2-perf-ssr/SKILL.md) for canonical patterns.

## Quick Reference

| Issue Type | Reference |
|------------|-----------|
| Missing `headers` export, unsafe `public` cache, child-drops-parent headers, missing `Vary: Cookie`, `Set-Cookie` + `public` | [references/caching-headers.md](references/caching-headers.md) |
| Server libs imported without `.server.ts`, `process.env.SECRET_*` leaks, `typeof window` substituted for `.server.ts` | [references/server-client-split.md](references/server-client-split.md) |
| `new Date()` in render, `Math.random()` in keys, locale formatting without explicit locale, missing `useId()`, blanket `suppressHydrationWarning` | [references/hydration.md](references/hydration.md) |
| `prefetch="render"` on every link, `defer` for fast data, missing `<Suspense>` around `<Await>`, prefetch to side-effect routes | [references/prefetch-streaming.md](references/prefetch-streaming.md) |
| `dangerouslySetInnerHTML` with untrusted data, missing `loading="lazy"`, missing `links` preload, stylesheet injected in body | [references/assets.md](references/assets.md) |

## Review Checklist

- [ ] Routes serving data export `headers` (even if the answer is `no-store`)
- [ ] Child routes serving personalized data export their own `headers` (otherwise they silently inherit the parent's policy)
- [ ] `Cache-Control: public` is never set on auth'd or cookie-bearing responses
- [ ] `Vary: Cookie` is set when cache decision depends on session
- [ ] Server-only libs (`prisma`, `bcrypt`, `node:fs`, `jsonwebtoken`) live in `*.server.ts` or `app/.server/`
- [ ] Secret env (`process.env.STRIPE_SECRET_KEY`, etc.) is read only inside loaders/actions or `.server` modules
- [ ] Client-exposed env is whitelisted into `window.ENV`, never raw `process.env`
- [ ] `typeof window === "undefined"` is not used as a substitute for `.server.ts` (treeshaking is unreliable)
- [ ] No `new Date()`, `Math.random()`, `Date.now()`, `crypto.randomUUID()` in JSX render path
- [ ] Locale formatting (`toLocaleDateString`, `Intl.DateTimeFormat`) passes an explicit locale
- [ ] Components generating IDs use `useId()`, not `Math.random()` or counters
- [ ] `suppressHydrationWarning` is scoped to a single element with a code comment explaining why
- [ ] `<Link prefetch="render">` is reserved for above-the-fold critical nav, not lists
- [ ] `<PrefetchPageLinks>` does not target routes whose loaders have side effects (analytics, mutations)
- [ ] Every `<Await>` is wrapped in `<Suspense>` and has an `errorElement`
- [ ] `defer()` is used only for genuinely slow data (>~50ms); fast data is awaited
- [ ] Below-the-fold images use `loading="lazy"` and have `width`/`height`
- [ ] Critical fonts/CSS are preloaded via the `links` export, not injected in body

## Valid Patterns (Do NOT Flag)

These are correct Remix v2 usage and must not be reported as issues:

- **Route without `headers` export when caching is intentionally off** — auth'd dashboards, account pages, and routes wrapped in a layout that already returns `no-store` may legitimately omit `headers`. Flag only if the route serves cacheable public content with no `headers`.
- **`new Date()` inside `useEffect`** — runs after hydration on the client only; no SSR mismatch possible. Same for `Date.now()`, `Math.random()`, `crypto.randomUUID()` inside effects.
- **`Math.random()` / `new Date()` inside event handlers** — handlers run after hydration. Only flag when the value is used during render.
- **`suppressHydrationWarning` on a single `<time>` (or similar) element with a clear comment** — accepted narrow escape for known-divergent values like absolute timestamps formatted client-side. Flag only when applied at a parent that wraps a large subtree or with no explanation.
- **`.client.ts` files for client-only libraries** — Stripe.js, map widgets, chart libs that read `window` belong in `*.client.ts` by convention; do not flag the file extension.
- **`useId()` with extra characters appended** — `` `${id}-input` `` is the documented pattern for multi-element components; do not flag as "non-stable id."
- **Raw ISO string rendered in SSR + reformatted in `useEffect`** — the canonical hydration-safe time pattern; flag only if the reformat happens in render.
- **`headers` export returning `{}` or `no-store`** — explicit "do not cache" is a deliberate decision and should not be flagged as misuse.
- **`<Link prefetch="intent">` on standard nav** — the recommended default; flag only when the loader has side effects.
- **`loaderHeaders` forwarded to the document via `headers` export** — co-locating data and document policy is the documented pattern, not duplication.

## Context-Sensitive Rules

Apply these only when the specific context applies:

| Issue | Flag ONLY IF |
|-------|--------------|
| Missing `headers` export | Route serves cacheable public content (not auth'd, not personalized, not intentionally `no-store`) |
| Child route missing `headers` | An ancestor exports `headers` AND its policy is broader than the child's cacheability (e.g., parent caches public + s-maxage, child serves personalized data) |
| `Cache-Control: public` | Loader actually reads session / user state (or response carries `Set-Cookie`) |
| `Vary: Cookie` missing | Loader branches response shape on a cookie (theme, locale, session) AND the cache is `public`/`s-maxage` |
| `new Date()` / `Math.random()` / `Date.now()` | Call site is in render path — NOT in `useEffect`, event handler, `<ClientOnly>`, or post-hydration code |
| Locale formatting without locale | Result is rendered into JSX (not used only inside an effect / handler) |
| `<Link prefetch="render">` | Link is inside a list / `.map()` iterator (not above-the-fold critical nav) |
| `<Link prefetch="intent">` to side-effect loader | Loader has observable side effects (analytics write, counter increment, log emit) AND doesn't branch on the `Purpose: prefetch` header |
| Server lib import without `.server.ts` | Importing file is reachable from the client graph (route module, non-`.server` util reached from a component) |
| `process.env.SECRET_*` reference | Reference is in a component body or in a non-`.server` module reached from the client graph |
| Missing `loading="lazy"` on image | Image is rendered below the fold (not in `<header>`, hero section, or above any `<main>` content) |
| Missing `width`/`height` on image | Project does NOT use a build-time image processor that injects dimensions |

## Hard gates (before writing findings)

Run these in order. **Do not draft user-facing findings until every gate passes** for the batch you are about to report.

1. **Location evidence** — **Pass:** Each issue lists the repo path and either a line range or a short verbatim quote from the file you read (not memory or diff-only guesswork). Cache, hydration, and `.server` claims without a concrete file path are not reportable.

2. **Exemption check** — **Pass:** For each issue, you can state in one line why it is *not* covered by [Valid Patterns (Do NOT Flag)](#valid-patterns-do-not-flag). In particular: confirm a missing `headers` export is not on an intentionally-uncacheable route, confirm `.client.ts` is not a legitimate client-only library, confirm `suppressHydrationWarning` is not scoped + commented.

3. **Hydration-context check** — **Pass:** Before flagging `new Date()`, `Math.random()`, `Date.now()`, `crypto.randomUUID()`, or locale formatting, confirm the call site is in the **render path** of a component. Calls inside `useEffect`, `useLayoutEffect`, event handlers, callbacks passed to `setTimeout`/`requestAnimationFrame`, or inside `<ClientOnly>{() => ...}</ClientOnly>` are post-hydration and must not be flagged.

4. **Parent/child headers chain check** — **Pass:** Before flagging "missing `headers` on a child" as silent cache inheritance, confirm an ancestor route in the matched chain actually exports `headers` (search the route file tree for `export const headers` or `export function headers`) AND that the inherited policy is wider than the child's cacheability profile. If no ancestor exports headers, the issue is just "no caching configured," not "child silently inherits parent's cache."

5. **Server/client boundary check** — **Pass:** Before flagging a server-lib import as a leak, confirm the importing file is reachable from the **client graph** — i.e., it's a route module, a non-`.server` utility transitively imported by a route's default export, or a `.client.ts` file. Imports inside `loader`, `action`, `headers`, or other `.server.ts` modules are not leaks.

6. **Protocol** — **Pass:** You completed the Pre-Report Verification Checklist in [review-verification-protocol](../../../beagle-core/skills/review-verification-protocol/SKILL.md) for this review.

## When to Load References

- Reviewing route `headers` exports, `Cache-Control` strings, CDN policy → [references/caching-headers.md](references/caching-headers.md)
- Reviewing `.server.ts` / `.client.ts` files, imports of `prisma`/`bcrypt`/`fs`, or `process.env` access → [references/server-client-split.md](references/server-client-split.md)
- Reviewing any component that renders dates, IDs, locale-formatted values, or browser globals → [references/hydration.md](references/hydration.md)
- Reviewing `<Link prefetch>`, `<PrefetchPageLinks>`, `defer`, `<Await>`, `<Suspense>`, or `<RemixServer abortDelay>` → [references/prefetch-streaming.md](references/prefetch-streaming.md)
- Reviewing `<img>`, `<link>`, `dangerouslySetInnerHTML`, font/CSS loading, or `links` export → [references/assets.md](references/assets.md)

## Review Questions

1. Does every route that serves cacheable data declare a `Cache-Control` policy, even if "no cache"?
2. Are personalized routes free of `public` caching, with `Vary: Cookie` where session influences the response?
3. Do server libs (`prisma`, `bcrypt`, `fs`, secret env access) live in `*.server.ts` modules that the build will reject if leaked?
4. Are public env vars whitelisted into `window.ENV` rather than spread from `process.env`?
5. Are `new Date()` / `Math.random()` / locale formatting calls limited to effects, handlers, or `<ClientOnly>` — not render?
6. Do components needing IDs use `useId()`?
7. Are `<Link prefetch>` modes matched to context (`render` only above the fold, `intent` for nav, `viewport`/`intent` in lists)?
8. Is `defer()` used only for genuinely slow data, with `<Await>` always paired with `<Suspense>` AND `errorElement`?
9. Are images sized, lazy-loaded below the fold, and critical fonts/CSS preloaded via the `links` export?
10. Is `dangerouslySetInnerHTML` used only with sanitized HTML or safely serialized JS?

## Before Submitting Findings

Complete [Hard gates](#hard-gates-before-writing-findings) (especially gate 3 — hydration-context check, and gate 5 — server/client boundary check), then report only issues that still pass the [review-verification-protocol](../../../beagle-core/skills/review-verification-protocol/SKILL.md) pre-report checks. Finding format: `[FILE:LINE] ISSUE_TITLE` with a verbatim quote of the offending code and a one-line rationale tied to the specific Remix v2 contract being violated.

## Additional Documentation

- Reviewing `headers` exports, CDN cache policy, `Vary`, parent/child merge, `Set-Cookie` interactions → [references/caching-headers.md](references/caching-headers.md)
- Reviewing `.server.ts` / `.client.ts` boundaries, `process.env` access, `window.ENV` pattern → [references/server-client-split.md](references/server-client-split.md)
- Reviewing render-time `Date`/`Math.random`/locale issues, `useId`, `suppressHydrationWarning` scope → [references/hydration.md](references/hydration.md)
- Reviewing `<Link prefetch>` modes, `<PrefetchPageLinks>` targets, `defer`/`<Await>`/`<Suspense>` structure → [references/prefetch-streaming.md](references/prefetch-streaming.md)
- Reviewing `dangerouslySetInnerHTML`, image `loading`/`width`/`height`, font/CSS preload, stylesheet placement → [references/assets.md](references/assets.md)
- Canonical patterns and decision gates → [beagle-react:remix-v2-perf-ssr](../remix-v2-perf-ssr/SKILL.md)
