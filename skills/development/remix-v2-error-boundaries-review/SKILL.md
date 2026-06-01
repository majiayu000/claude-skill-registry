---
name: remix-v2-error-boundaries-review
description: Reviews Remix v2 error-handling code for the unified ErrorBoundary, isRouteErrorResponse narrowing, throw-vs-return, root boundary scaffolding, and v1 holdovers (CatchBoundary, useCatch). Use when reviewing routes that throw or define ErrorBoundary in a Remix v2 codebase.
---

# Remix v2 Error Boundaries Code Review

Targets TypeScript route modules importing from `@remix-run/*`. No sibling
knowledge skill exists for this topic; the canonical mental model is
summarized inline below and expanded in `references/`.

## v2 Boundary Model (read first)

Remix v2 unified v1's `CatchBoundary` + `ErrorBoundary` into a **single**
`ErrorBoundary` route-module export. The framework calls it for **both**
thrown `Response`s (e.g. `throw new Response(...)`, `throw json(...)`)
**and** thrown runtime errors (loader/action/render exceptions). Inside
the boundary you read the value with the `useRouteError()` hook, then
narrow in this order:

1. `isRouteErrorResponse(error)` → it was a thrown `Response`; read
   `error.status`, `error.statusText`, `error.data`.
2. `error instanceof Error` → real runtime error; read `error.message`.
3. else → unknown thrown value; render a generic fallback.

The boundary takes **no props**. `CatchBoundary`, `useCatch`, and the
`future.v2_errorBoundary` flag are all gone — finding any of them is a
v1 holdover. Errors render the *nearest* `ErrorBoundary` and bubble to
the root if none exists; the root boundary remounts the whole document,
so it must render `<Meta />`, `<Links />`, and `<Scripts />`. Only
**thrown** loader/action results reach the boundary — a `return json(...)`
with a 4xx status is a successful loader, not an error. Server-side
runtime errors also flow through an optional `entry.server.tsx`
`handleError` export (thrown `Response`s do *not*).

## Quick Reference

| Issue Type | Reference |
|------------|-----------|
| Missing route `ErrorBoundary`, props-on-boundary, narrowing-only `instanceof Error`, narrowing-only `isRouteErrorResponse` | [references/boundary-shape.md](references/boundary-shape.md) |
| Return-instead-of-throw 4xx/5xx, swallowing `error.data`, throwing strings, missing `handleError` | [references/throw-response.md](references/throw-response.md) |
| Missing root boundary, root boundary without `<Meta />`/`<Links />`/`<Scripts />`, `useLoaderData()` in root boundary | [references/root-boundary.md](references/root-boundary.md) |
| `CatchBoundary` export, `useCatch` import, `v2_errorBoundary` future flag | [references/v1-holdovers.md](references/v1-holdovers.md) |

## Review Checklist

- [ ] `ErrorBoundary` declared `export function ErrorBoundary()` with **no** props
- [ ] Error read via `useRouteError()`, not `useCatch()` and not a prop
- [ ] Narrowing checks `isRouteErrorResponse(error)` **first**, then `error instanceof Error`, then fallback
- [ ] `error.data` rendered defensively (typed/narrowed before going into JSX)
- [ ] 4xx / 5xx in loaders/actions use `throw` (not `return`) for `Response` / `json`
- [ ] Routes that can throw export their own `ErrorBoundary` (don't tear down parents for a widget failure)
- [ ] Root `app/root.tsx` exports an `ErrorBoundary` that renders `<Meta />`, `<Links />`, and `<Scripts />`
- [ ] Root boundary uses `useRouteLoaderData("root")` (not `useLoaderData()`) when reading root data
- [ ] No `CatchBoundary` export anywhere; no `useCatch` import; no `future.v2_errorBoundary` in `remix.config.js`
- [ ] `entry.server.tsx` exports `handleError` and pipes runtime errors to an error reporter
- [ ] `handleError` does **not** assume thrown `Response`s flow through it (they don't)
- [ ] Thrown values are `Response`/`json`/`Error` instances — never plain strings or POJOs

## Valid Patterns (Do NOT Flag)

These are correct Remix v2 usage and must not be reported as issues:

- **Route without `ErrorBoundary` that intentionally inherits from a parent** — Boundaries cascade up. A child route may omit `ErrorBoundary` so the parent (or root) renders the fallback. Only flag if the route handles user-distinct error UX *and* a parent boundary cannot.
- **`throw new Response(...)` or `throw json(...)` from a loader/action** — The canonical way to signal 404/401/403/etc. This is *not* "using exceptions for control flow"; it is documented v2 contract.
- **Narrowing only with `isRouteErrorResponse(error)`** — Acceptable when the route demonstrably only throws `Response`s and has no render-time crash risk. Severity is **ADVISORY at most**; suggest adding an `instanceof Error` branch for defense-in-depth, do not flag as a bug.
- **`ErrorBoundary` that does not call `useRouteError()`** — Valid when the boundary renders a static "Something went wrong" fallback intentionally (e.g. marketing pages that don't want to surface error detail).
- **Root `ErrorBoundary` calling `useRouteLoaderData("root")` and getting `undefined`** — Documented defensive pattern (root loader may have thrown). Do not flag the `undefined` handling as "dead code."
- **`handleError` returning early on `request.signal.aborted`** — Documented noise filter, not a swallowed error.
- **`handleError` not handling thrown `Response`s** — By framework contract `handleError` only fires for runtime errors. The absence of `Response` handling is correct, not a gap.
- **Nested `ErrorBoundary` returning a bare fragment (no `<html>` / `<body>`)** — Only the root boundary owns the document. Nested boundaries render *inside* parent layouts and must not include document tags.

## Severity guidance

Use these defaults unless the codebase has documented a different scale:

| Pattern | Default severity |
|---|---|
| `CatchBoundary` export or `useCatch` import in v2 codebase | BLOCKER (build-breaking or dead code) |
| Root `ErrorBoundary` missing `<Scripts />` | BLOCKER (dead-end error page) |
| `ErrorBoundary` with `({ error })` v1 prop signature | WARN (silent runtime undefined) |
| `return json(...)` for 4xx instead of `throw` | WARN (boundary never fires) |
| Missing `instanceof Error` branch on a route with render-crash risk | WARN |
| Missing `instanceof Error` branch on a Response-only route | ADVISORY |
| `useLoaderData()` (vs `useRouteLoaderData`) in root boundary | WARN (latent loop) |
| Missing `handleError` in `entry.server.tsx` | ADVISORY (observability gap, not a bug) |

## Hard gates (before writing findings)

Run in order. **Do not draft user-facing findings until every gate
passes** for the batch you are about to report.

1. **Location evidence** — **Pass:** Each issue lists the repo path to
   the route module (or `app/root.tsx`, or `app/entry.server.tsx`) and
   either a line range or a short verbatim quote from the file you read
   (not from memory or diff-only guesswork). "The root boundary is
   wrong" without a path to `app/root.tsx` is not reportable.

2. **Exemption check** — **Pass:** For each issue, you can state in one
   line why it is *not* covered by [Valid Patterns (Do NOT Flag)](#valid-patterns-do-not-flag).
   In particular: confirm a missing `ErrorBoundary` is not a deliberate
   cascade to a parent boundary; confirm an `isRouteErrorResponse`-only
   narrowing is not on a route that demonstrably only throws Responses
   (downgrade to ADVISORY in that case).

3. **v1-vs-v2 marker check** — **Pass:** Before writing the finding,
   grep the route module (and the repo at large for cross-cutting
   issues) for: `CatchBoundary`, `useCatch`, `v2_errorBoundary`,
   `ErrorBoundary({ error`, `ErrorBoundary({error`. If any of these
   appear, the finding is a **v1 holdover** (load [references/v1-holdovers.md](references/v1-holdovers.md))
   and must be labeled as such — *not* as a generic "missing error
   handling" issue. If none appear, the code is v2-shape and the
   finding is about v2 correctness.

4. **Protocol** — **Pass:** You completed the Pre-Report Verification
   Checklist in [review-verification-protocol](../../../beagle-core/skills/review-verification-protocol/SKILL.md)
   for this review.

## Review Questions

1. Does every route that can throw (loader, action, or render) have an
   `ErrorBoundary` at the right level — local where the recovery UI
   matters, parent/root where cascade is intentional?
2. Does each `ErrorBoundary` call `useRouteError()` (not `useCatch()`,
   not props) and narrow `isRouteErrorResponse` first?
3. Are 4xx / 5xx control flows using `throw` (not `return`) so the
   boundary actually fires?
4. Does `app/root.tsx` export an `ErrorBoundary` with `<Meta />`,
   `<Links />`, and `<Scripts />`, and use `useRouteLoaderData("root")`
   defensively?
5. Are there any v1 markers left (`CatchBoundary`, `useCatch`,
   `v2_errorBoundary`, `({ error })` prop signature)?
6. Is `handleError` present in `entry.server.tsx` for runtime-error
   observability, with the correct contract (no Response handling)?

## Additional Documentation

- Reviewing the `ErrorBoundary` export shape, hook usage, or narrowing → [references/boundary-shape.md](references/boundary-shape.md)
- Reviewing thrown `Response` / `json` patterns, `handleError`, or return-vs-throw → [references/throw-response.md](references/throw-response.md)
- Reviewing `app/root.tsx` boundary scaffolding → [references/root-boundary.md](references/root-boundary.md)
- Detecting v1 holdovers (`CatchBoundary`, `useCatch`, `v2_errorBoundary`) → [references/v1-holdovers.md](references/v1-holdovers.md)
- Remix v2 ErrorBoundary docs: https://remix.run/docs/en/main/route/error-boundary
- Remix v2 error handling guide: https://remix.run/docs/en/main/guides/errors
- Remix v2 `entry.server` / `handleError` docs: https://remix.run/docs/en/main/file-conventions/entry.server
