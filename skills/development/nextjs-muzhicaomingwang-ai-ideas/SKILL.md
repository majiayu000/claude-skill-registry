---
name: nextjs
description: Build, review, and refactor Next.js (App Router) frontend projects with TypeScript. Use for tasks like creating pages/layouts, routing, server components vs client components, data fetching patterns, UI component structure, forms/validation, auth integration points, env vars, linting/testing, and production deployment readiness.
---

# nextjs

Use this skill to implement or review a Next.js frontend in a consistent, production-friendly way.

## Defaults (unless repo dictates otherwise)

- Next.js App Router (`app/`)
- TypeScript
- Server Components by default; add `"use client"` only when needed
- CSS: Tailwind if already present; otherwise follow existing styling approach

## Workflow

1) Identify project mode
- New app: decide App Router vs Pages Router (prefer App Router unless constrained).
- Existing app: follow current structure, conventions, and tooling.

2) Establish app structure (App Router)
- `app/layout.tsx`: global shell (providers, fonts, nav).
- `app/page.tsx`: landing page.
- Route groups for domains: `app/(dashboard)/...`, `app/(marketing)/...`.
- Shared UI: `components/` (reusable), `app/**/_components/` (route-scoped).
- Types/utilities: `lib/` (fetchers, helpers), `types/`.

3) Server vs client boundaries
- Prefer Server Components for data loading and initial render.
- Use Client Components for: event handlers, stateful UI, browser APIs, client-only libraries.
- Keep props serializable across the boundary; avoid passing functions/classes.

4) Data fetching patterns
- Prefer colocated server fetchers in `lib/` and call them from Server Components.
- Use `fetch()` with Next caching semantics when appropriate.
- Handle loading and errors with `loading.tsx` / `error.tsx` per route segment.

5) Forms and validation
- Use server actions when appropriate; otherwise route handlers (`app/api/...`) + client submit.
- Validate on server; optionally mirror on client.

6) Env vars & config
- Document required env vars; use `process.env.X`.
- Only expose public vars with `NEXT_PUBLIC_` prefix.

7) Quality gates
- Run `lint` and `typecheck` (and tests if present).
- Ensure accessibility basics: labels, focus states, keyboard navigation.
- Avoid breaking route segments/URLs; add redirects when changing paths.

## Output expectations when making changes

- Keep diffs small and localized.
- Prefer composition over complex shared state.
- Add a short usage note (routes added, env vars, how to run) when you introduce new capabilities.

