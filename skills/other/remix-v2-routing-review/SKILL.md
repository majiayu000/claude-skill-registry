---
name: remix-v2-routing-review
description: Reviews Remix v2 route files for naming convention violations, missing layouts, resource-route shape, and v1 holdovers. Use when reviewing files under app/routes/ in a Remix v2 codebase.
user-invocable: false
---

# Remix v2 Routing Code Review

Loaded by `review-remix-v2` (umbrella) to flag routing anti-patterns in `app/routes/` modules. See [beagle-react:remix-v2-routing](../remix-v2-routing/SKILL.md) for canonical patterns.

## Quick Reference

| Issue Type | Reference |
|------------|-----------|
| Filename smells (`index.tsx`, `__auth`, wrong escape, non-route files) | [references/route-files.md](references/route-files.md) |
| Missing `<Outlet />`, orphan dotted segments, duplicated layout logic | [references/layouts-outlets.md](references/layouts-outlets.md) |
| Default export on a resource, `<Link>` without `reloadDocument`, splat params | [references/resource-routes.md](references/resource-routes.md) |
| `react-router-dom` imports, `__double` folders, v1-adapter fallback | [references/v1-holdovers.md](references/v1-holdovers.md) |
| Missing `<Meta />`/`<Links />`/`<Scripts />`/`<ScrollRestoration />`, Vite-vs-Classic `<LiveReload />`, root `ErrorBoundary` without document shell | [references/root-shell.md](references/root-shell.md) |

## Scope

This skill flags issues in:

- Files under `app/routes/` (filenames, exports, imports, JSX shape)
- `app/root.tsx` (document shell, root `<Outlet />`)
- `remix.config.js` (entries that change route discovery: `routes()`, `ignoredRouteFiles`, `@remix-run/v1-route-convention`)
- Any module that links to a resource route (`<Link>` usage)

Out of scope: loader/action data contracts (covered by `remix-v2-data-flow-review`), form behavior (`remix-v2-forms-review`), meta/headers (`remix-v2-meta-sessions-review`).

## Review Checklist

- [ ] Index routes named `_index.tsx`, not `index.tsx`
- [ ] Pathless layouts use single underscore (`_auth.tsx`), not double (`__auth/`)
- [ ] Dotted child routes (`users.profile.tsx`) have a parent module *or* use trailing underscore (`users_.profile.tsx`)
- [ ] Parent route modules render `<Outlet />`
- [ ] Splat segments read `params["*"]`, never `params.splat` / `params.rest`
- [ ] Literal dots/special chars escaped with brackets (`sitemap[.]xml.tsx`)
- [ ] Resource routes have **no** `default` export
- [ ] `<Link>` to a resource route uses `reloadDocument` (or is a plain `<a>`)
- [ ] Imports come from `@remix-run/react`, not `react-router-dom`
- [ ] Non-route files (CSS, helpers, tests) live in a folder with `route.tsx`, or are listed in `ignoredRouteFiles`
- [ ] Trailing-underscore opt-outs only used when a parent layout actually exists to escape
- [ ] Optional segments `($lang)` narrow `params.lang` in the loader (see [references/route-files.md](references/route-files.md#optional-segments-lang-without-narrowing-in-the-loader))

## Valid Patterns (Do NOT Flag)

- **Resource route with no default export** — this *is* the convention that makes it a resource route. Never flag.
- **Any `_`-prefixed pathless layout file without `<Outlet />`** when the module is intentionally a wrapper that renders fixed UI only. Confirm by checking children — if no `*.{segment}.tsx` siblings exist, the wrapper-only shape is intentional.
- **Files prefixed with `_` that don't appear in any URL** — pathless layouts and `_index` are supposed to be hidden from the URL.
- **`@remix-run/v1-route-convention`** wired up in `remix.config.js` — legitimate migration adapter, not a smell on its own. Only flag if v1-style files appear *without* the adapter installed.
- **`useLoaderData<typeof loader>()`** — type annotation, not assertion.
- **Splat route accessing `params["*"]`** with bracket syntax — that is the only correct access pattern.
- **Folder `app/routes/dashboard/` with `route.tsx` plus sibling `.server.ts`, `.css`, component files** — co-location is the documented pattern.
- **Trailing underscore (`concerts_.mine.tsx`)** when a sibling `concerts.tsx` layout exists and this URL intentionally skips it.

## Context-Sensitive Rules

Only flag these issues when the specific context applies:

| Issue | Flag ONLY IF |
|-------|--------------|
| `index.tsx` under `app/routes/` | Project is v2 and `@remix-run/v1-route-convention` is NOT wired in `remix.config.js` |
| Parent module without `<Outlet />` | Sibling dotted children (`parent.*.tsx`) exist in `app/routes/` |
| `__double` underscore folder | No v1-convention adapter is installed |
| Trailing-underscore segment | No corresponding parent layout exists (nothing to opt out of) |
| Default export on a module returning non-HTML | The loader/action actually returns a raw `Response` (PDF, JSON, RSS) |
| `<Link>` to resource route | Target route has no `default` export AND `<Link>` lacks `reloadDocument` |

## Hard gates (before writing findings)

Run these in order. **Do not draft user-facing findings until every gate passes** for the batch you are about to report.

1. **Location evidence** — **Pass:** Each issue lists a repo path (file under `app/routes/` or `remix.config.js`) and either a line range or a short verbatim quote from the file you read. Filename-only smells must quote the literal filename.

2. **Exemption check** — **Pass:** For each issue, state in one line why it is *not* covered by [Valid Patterns (Do NOT Flag)](#valid-patterns-do-not-flag). Resource-route flags require explicit evidence of a `default` export or a `<Link>` without `reloadDocument`.

3. **Version check** — **Pass:** Confirm the project is Remix v2 (check `package.json` for `@remix-run/react` ^2, *or* presence of v2 flat-routes filenames elsewhere in `app/routes/`). If `@remix-run/v1-route-convention` is wired in `remix.config.js`, v1 filenames (`__auth/`, `index.tsx`) are intentional — do not flag them as smells.

4. **Protocol** — **Pass:** Complete the Pre-Report Verification Checklist in [review-verification-protocol](../../../beagle-core/skills/review-verification-protocol/SKILL.md) for this review.

## When to Load References

- Reviewing filenames under `app/routes/` → [references/route-files.md](references/route-files.md)
- Reviewing parent modules and shared chrome → [references/layouts-outlets.md](references/layouts-outlets.md)
- Reviewing a module that returns non-HTML, or any `<Link>` to such a module → [references/resource-routes.md](references/resource-routes.md)
- Reviewing imports or filenames that look like v1 → [references/v1-holdovers.md](references/v1-holdovers.md)
- Reviewing `app/root.tsx` (document shell, `<Meta />`/`<Links />`/`<Scripts />`/`<ScrollRestoration />`, `<LiveReload />` on Vite vs Classic Compiler, root `ErrorBoundary`) → [references/root-shell.md](references/root-shell.md)

## Review Questions

1. Does every parent route render `<Outlet />`, or is it a deliberate wrapper-only?
2. Do filenames match the v2 grammar (single `_` for pathless, `_index` for index, `[...]` for escapes)?
3. Are resource routes free of `default` exports, and do all `<Link>`s to them use `reloadDocument`?
4. Are all router imports from `@remix-run/react` (and server helpers from `@remix-run/node`)?
5. If v1 filenames exist, is `@remix-run/v1-route-convention` wired up — or are they accidental?

## Additional Documentation

- **Route file naming smells**: [references/route-files.md](references/route-files.md) — `index.tsx`, `__double` folders, wrong escape syntax, dot/underscore confusion, non-route files under `app/routes/`.
- **Layouts and outlets**: [references/layouts-outlets.md](references/layouts-outlets.md) — pathless layout misuse, missing `<Outlet />`, orphan dotted children, duplicated layout logic.
- **Resource routes**: [references/resource-routes.md](references/resource-routes.md) — accidental default export, `<Link>` without `reloadDocument`, splat `params["*"]` access.
- **v1 holdovers**: [references/v1-holdovers.md](references/v1-holdovers.md) — `react-router-dom` imports, `__auth` folders, `@remix-run/v1-route-convention` as a deliberate-vs-accidental tell.
