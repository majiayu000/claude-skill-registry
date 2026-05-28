---
name: remix-v2-routing
description: Remix v2 routing patterns. Use when implementing flat-routes v2 conventions, route file naming, nested layouts, resource routes, or root.tsx scaffolding. Triggers on _<name>.tsx (pathless layout), _index.tsx, $param, app/routes/, @remix-run/dev, defineRoutes, <Outlet /> in route modules.
---

# Remix v2 Routing

## Quick Reference

**Flat-routes v2 filename rules** (all files live in `app/routes/`):

```text
_index.tsx                 → /
concerts.tsx               → /concerts                (acts as layout when dotted children exist; otherwise leaf for /concerts)
concerts._index.tsx        → /concerts                (renders under layout)
concerts.$city.tsx         → /concerts/:city          params.city
concerts.trending.tsx      → /concerts/trending
_auth.tsx + _auth.login.tsx → /login (pathless layout, no URL segment)
files.$.tsx                → /files/*                 params["*"]
($lang)._index.tsx         → / and /en (or /fr etc.) — optional segment
sitemap[.]xml.tsx          → /sitemap.xml             (escape literal)
concerts_.mine.tsx         → /concerts/mine           (opts out of layout)
dashboard/route.tsx        → /dashboard               (folder + route.tsx)
reports.$id[.pdf].tsx      → /reports/:id.pdf         (no default export = resource)
```

**Imports — always use `@remix-run/react`, never `react-router-dom`**:

```tsx
import { Outlet, Link, useLoaderData, useParams } from "@remix-run/react";
import type { LoaderFunctionArgs } from "@remix-run/node"; // or /cloudflare, /deno
```

## File Naming Conventions

Dots in filenames create URL slashes and parent/child nesting. Underscore prefix marks pathless segments (`_auth.tsx`) and index routes (`_index.tsx`). Trailing underscore (`concerts_.mine.tsx`) opts out of layout nesting while keeping the URL nested. Brackets escape literal characters: `sitemap[.]xml.tsx`. Splat is the single dollar sign: `$.tsx` exposes the rest of the path under `params["*"]`. Optional segments are wrapped in parens: `($lang)`.

See [references/conventions.md](references/conventions.md) for the full table and edge cases.

## Nested Layouts

A parent module (`concerts.tsx`) renders `<Outlet />`; child routes (`concerts.$city.tsx`, `concerts._index.tsx`) mount inside it automatically based on the dot-delimited filename.

```tsx
// app/routes/concerts.tsx
import { Outlet } from "@remix-run/react";

export default function ConcertsLayout() {
  return (
    <section>
      <nav>{/* concerts subnav */}</nav>
      <Outlet />
    </section>
  );
}
```

```tsx
// app/routes/concerts._index.tsx  (renders at exactly /concerts)
export default function ConcertsIndex() {
  return <h1>Browse concerts</h1>;
}
```

For a layout with **no** URL contribution, prefix with a single underscore:

```tsx
// app/routes/_auth.tsx          → wraps /login, /signup; no URL segment
// app/routes/_auth.login.tsx    → /login   (inherits _auth layout)
// app/routes/_auth.signup.tsx   → /signup
```

## Dynamic Segments and Splats

`$name` captures a single segment; `$.tsx` captures the rest of the path. Loader receives values via `params`:

```tsx
// app/routes/concerts.$city.tsx
import type { LoaderFunctionArgs } from "@remix-run/node";
import { json } from "@remix-run/node";
import { useLoaderData } from "@remix-run/react";

export async function loader({ params }: LoaderFunctionArgs) {
  if (!params.city) throw new Response("Not found", { status: 404 });
  return json({ city: params.city });
}

export default function City() {
  const { city } = useLoaderData<typeof loader>();
  return <h1>{city}</h1>;
}
```

Splat values live under `"*"` — there is no `params.splat`:

```tsx
// app/routes/files.$.tsx
export async function loader({ params }: LoaderFunctionArgs) {
  const rest = params["*"]; // bracket access only
  return new Response(await readBlob(rest), { headers: { "Content-Type": "application/octet-stream" } });
}
```

## Root Module

`app/root.tsx` is the only required route. It owns the document shell and must render `<Meta />`, `<Links />`, `<Outlet />`, `<ScrollRestoration />`, `<Scripts />`, and (during dev) `<LiveReload />`. See [references/root.md](references/root.md).

## Resource Routes

A route module without a `default` export is a **resource route** — it returns raw `Response` objects (PDF, JSON, RSS, webhooks). Parent loaders do **not** run, and `<Link>` must use `reloadDocument` (or be replaced with `<a>`) to trigger a real document request. See [references/resource-routes.md](references/resource-routes.md).

## Gates (decision sequencing)

Answer **in order**. **Pass** means the condition is true; pick the answer on the same line and **stop**.

### Layout vs flat URL

0. **Is there shared chrome at all (nav, breadcrumbs, sidebar) at this level**?
   - **Fail →** Use plain dotted segments (`about.tsx`, `pricing.tsx`); no layout module needed. **Stop.**
   - **Pass →** Step 1.
1. **Should this URL share UI (nav, breadcrumbs, sidebar) with a parent path**?
   - **Pass →** Use dot-delimited nesting (`concerts.$city.tsx` under `concerts.tsx`). **Stop.**
   - **Fail →** Step 2.
2. **Does the URL just *happen* to be nested but should render standalone**?
   - **Pass →** Trailing underscore (`concerts_.mine.tsx`). **Stop.**
   - **Fail →** Step 3.
3. **Need a wrapper layout but no parent URL segment**?
   - **Pass →** Single-underscore pathless parent (`_auth.tsx` + `_auth.login.tsx`). **Stop.**

### UI route vs resource route

1. **Does this URL ever render HTML to a user**?
   - **Pass →** Export a `default` component. UI route. **Stop.**
   - **Fail →** Step 2.
2. **Returns JSON, PDF, RSS, sitemap, webhook, or other raw `Response`**?
   - **Pass →** Omit `default` export — module becomes a resource route. Use `reloadDocument` on any `<Link>` pointing to it. **Stop.**

### `_index.tsx` vs `index.tsx`

1. **On Remix v2 with flat-routes**?
   - **Pass →** `_index.tsx` (leading underscore). **Stop.**
   - **Fail →** Step 2 — you're on v1 (or using the v1 fallback adapter).
2. **Need to keep a v1 nested-folder tree alive**?
   - **Pass →** Install `@remix-run/v1-route-convention` and wire it in `remix.config.js`. See [references/v1-migration.md](references/v1-migration.md). **Stop.**

## Additional Documentation

- **Conventions**: See [references/conventions.md](references/conventions.md) for the full filename grammar (`_index`, `_layout`, `$param`, splat, optional, escape, folder + `route.tsx`, trailing underscore).
- **Root module**: See [references/root.md](references/root.md) for the `root.tsx` scaffold and the required document elements.
- **Resource routes**: See [references/resource-routes.md](references/resource-routes.md) for non-HTML responses, the no-`default`-export rule, parent-loader skipping, and `reloadDocument`.
- **v1 → v2 migration**: See [references/v1-migration.md](references/v1-migration.md) for differences from v1 (`__double` underscore folders, `index.tsx`, `@remix-run/v1-route-convention`, `ignoredRouteFiles`).

## v1 vs v2 Convention Comparison

| Concern              | v1 (nested folders)              | v2 (flat routes)              |
|----------------------|----------------------------------|-------------------------------|
| Index route          | `index.tsx`                      | `_index.tsx`                  |
| Pathless layout      | `__auth/` (double underscore)    | `_auth.tsx` (single)          |
| Nested URL           | folder hierarchy                 | dot delimiter in filename     |
| Dynamic segment      | `$param.tsx`                     | `$param.tsx` (unchanged)      |
| Splat                | `$.tsx`                          | `$.tsx` (unchanged)           |
| Escape literal       | n/a                              | `[.]`, `[]` brackets          |
| Opt-out of layout    | move out of folder               | trailing `_` (`foo_.bar.tsx`) |
| Co-location          | adjacent files in folder         | `feature/route.tsx` + siblings|
| Fallback adapter     | n/a                              | `@remix-run/v1-route-convention` |
