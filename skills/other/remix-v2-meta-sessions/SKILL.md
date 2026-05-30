---
name: remix-v2-meta-sessions
description: Remix v2 meta/SEO, sessions, auth, and CSRF. Use when working with document head, cookie sessions, auth gates, or CSRF protection. Triggers on meta export (v2 array shape), links export, createCookieSessionStorage, commitSession, destroySession, requireUserId, remix-utils/csrf, remix-auth.
---

# Remix v2 Meta, Sessions, Auth, and CSRF

## Quick Reference

**v2 `meta` returns an array of descriptor objects** — NOT the v1 object shape.
A v1-style object literal still typechecks in stale codebases but renders no
tags at runtime.

```tsx
// app/routes/posts.$slug.tsx
import type { MetaFunction } from "@remix-run/node";

export const meta: MetaFunction<typeof loader> = ({ data }) => {
  if (!data?.post) return [{ title: "Not Found" }];
  return [
    { title: `${data.post.title} | My Blog` },
    { name: "description", content: data.post.excerpt },
    { property: "og:title", content: data.post.title },
    { tagName: "link", rel: "canonical", href: data.post.url },
  ];
};
```

**Cookie session storage with secure defaults and secret rotation**:

```ts
// app/session.server.ts
import { createCookieSessionStorage } from "@remix-run/node";

type SessionData = { userId: string };
type SessionFlashData = { error: string };

const SESSION_SECRET = process.env.SESSION_SECRET;
if (!SESSION_SECRET) throw new Error("SESSION_SECRET is required");

export const { getSession, commitSession, destroySession } =
  createCookieSessionStorage<SessionData, SessionFlashData>({
    cookie: {
      name: "__session",
      httpOnly: true,
      secure: process.env.NODE_ENV === "production",
      sameSite: "lax",
      path: "/",
      maxAge: 60 * 60 * 24 * 30,
      secrets: [
        SESSION_SECRET,
        ...(process.env.SESSION_SECRET_OLD ? [process.env.SESSION_SECRET_OLD] : []),
      ],
    },
  });
```

## Document Head: `meta` and `links`

`<Meta />` and `<Links />` must live inside `<head>` in `root.tsx`;
`<ScrollRestoration />`, `<Scripts />`, and `<LiveReload />` go at the end of
`<body>`. Missing either of these aggregators produces "css doesn't load" or
"meta tags missing" with no compile error.

```tsx
// app/root.tsx
import { Links, LiveReload, Meta, Outlet, Scripts, ScrollRestoration } from "@remix-run/react";

export default function App() {
  return (
    <html lang="en">
      <head>
        <meta charSet="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <Meta />
        <Links />
      </head>
      <body>
        <Outlet />
        <ScrollRestoration />
        <Scripts />
        <LiveReload />
      </body>
    </html>
  );
}
```

**`<Meta />` and `<Links />` aggregate differently.** `<Links />` walks the
entire route match chain and renders **every** matched route's `links` export
— a stylesheet declared in a leaf route is rendered automatically and
unloaded on navigation away. `<Meta />` does **NOT** aggregate; Remix picks
the last matching route's `meta` array only. To inherit from parents in
`meta`, flatMap `matches` explicitly:

```tsx
import type { MetaFunction } from "@remix-run/node";
import type { loader as projectLoader } from "./project.$pid";

export const meta: MetaFunction<
  typeof loader,
  { "routes/project.$pid": typeof projectLoader }
> = ({ data, matches }) => {
  const parentMeta = matches.flatMap((m) => m.meta ?? []);
  const project = matches.find((m) => m.id === "routes/project.$pid")?.data;
  return [
    ...parentMeta,
    { title: `${data?.task.name} | ${project?.name}` },
  ];
};
```

The second generic on `MetaFunction` (keyed by route id) types
`matches.find(...).data` for parent routes. See
[references/meta-v2.md](references/meta-v2.md).

## Sessions

`commitSession` must be attached as a `Set-Cookie` header on every mutating
response. Remix does NOT auto-commit; calling `session.set(...)` and returning
plain `json(data)` silently drops the change.

```ts
return redirect("/dashboard", {
  headers: { "Set-Cookie": await commitSession(session) },
});
```

`session.flash(key, value)` is read-once; the consuming loader must still call
`commitSession` after reading to clear the flash. See
[references/sessions.md](references/sessions.md).

## Auth: throw `redirect` from loaders

The canonical pattern is a `requireUserId(request)` helper that **throws**
`redirect()` for unauthenticated requests. The thrown response short-circuits
the loader; no top-level `return` is needed.

```ts
// app/auth.server.ts
import { redirect } from "@remix-run/node";
import { getSession } from "./session.server";

export async function requireUserId(request: Request): Promise<string> {
  const session = await getSession(request.headers.get("Cookie"));
  const userId = session.get("userId");
  if (!userId) {
    const url = new URL(request.url);
    const redirectTo = `${url.pathname}${url.search}`;
    throw redirect(`/login?redirectTo=${encodeURIComponent(redirectTo)}`);
  }
  return userId;
}
```

Never gate routes inside React components — the protected component still SSRs
and ships HTML/loader data to unauthenticated users. See
[references/auth-csrf.md](references/auth-csrf.md).

## CSRF

**Remix has no built-in CSRF protection.** Same-origin `<Form>` posts rely
entirely on whatever `SameSite` value you set on the session cookie.
`SameSite=Lax` blocks cookies on cross-site POST navigations in all current
browsers. (Chrome briefly had a 2-minute "Lax+POST" window in 2020 — removed
in 2021.) The real `Lax`-vs-`Strict` tradeoff is subdomain takeover: with
`Lax`, a compromised subdomain can initiate top-level GET nav with
credentials; with `Strict`, deep-link navigations from external sites lose
session. Apps that use `SameSite=None` for legitimate cross-site needs
(OAuth popups, iframe embeds) have no cookie-level CSRF protection at all.
Recommend `remix-utils/csrf` with a **dedicated** signed cookie — never
reuse the session cookie. Manual `fetch("/api/x", { method: "POST" })`
bypasses `AuthenticityTokenInput`, so any action that does not call
`csrf.validate(request)` is an attacker entry point.

## Gates (decision sequencing)

Answer **in order**. **Pass** means the condition is true; pick the API on the
same line and **stop**.

### Where does this `meta` tag live?

1. **Is it site-wide (charset, viewport, default OG image)?**
   - **Pass →** Plain JSX inside `<head>` in `root.tsx`. Avoids the v2
     no-merge surprise and prevents duplicate tags. **Stop.**
   - **Fail →** Step 2.
2. **Is it route-specific (title, description, canonical, JSON-LD)?**
   - **Pass →** `export const meta` in the leaf route file; if you need
     parent values, `matches.flatMap((m) => m.meta ?? [])`. **Stop.**

### Auth check: `loader`, `action`, or helper?

1. **Is this a GET (page render) that must be protected?**
   - **Pass →** Call `await requireUserId(request)` at the top of the
     `loader`. **Stop.**
2. **Is this a POST/PUT/DELETE mutation that must be protected?**
   - **Pass →** Call `await requireUserId(request)` at the top of the
     `action`, AND call `await csrf.validate(request)`. **Stop.**
3. **Logout?**
   - **Pass →** `action` only, never `loader`. A `<Link to="/logout">`
     pointing at a loader is CSRF-able via `<img src="/logout">`. Use
     `<Form method="post" action="/logout">`. **Stop.**

### Where does the CSRF token live?

1. **Are you using `remix-utils/csrf`?**
   - **Pass →** A dedicated `createCookie("csrf", { ... })` cookie, separate
     from the session cookie. The CSRF value is a signed string; the
     session value is a serialized object — reusing one cookie throws on
     validate. **Stop.**
   - **Fail →** Step 2.
2. **No CSRF library?**
   - **Pass →** Document the threat model; require `sameSite: "strict"` on
     the session cookie and verify the `Origin` header in every action.
     Prefer adding `remix-utils/csrf` instead.

## Additional Documentation

- **Meta v2**: See [references/meta-v2.md](references/meta-v2.md) for
  descriptor types, parent merging via `matches`, JSON-LD, and v1→v2 migration
  pitfalls.
- **Links**: See [references/links.md](references/links.md) for stylesheet,
  preload, dns-prefetch, and the parent-aggregation behavior of `<Links />`.
- **Sessions**: See [references/sessions.md](references/sessions.md) for
  `createCookieSessionStorage` config, `commitSession`/`destroySession`
  patterns, flash messages, and database-backed sessions.
- **Auth and CSRF**: See [references/auth-csrf.md](references/auth-csrf.md)
  for `requireUserId` helpers, login/logout actions, `remix-auth`, and
  `remix-utils/csrf` wiring.

## v1 vs v2 Quick Comparison

| Concern | v1 | v2 |
|---|---|---|
| `meta` return shape | Object `{ title, description }` | Array `[{ title }, { name, content }]` |
| Parent meta merge | Auto-merged (last-write-wins per key) | No merge; last matching route only |
| `meta` argument for parent data | `parentsData` | `matches` (flatMap manually) |
| OG tags | `{ "og:title": "..." }` shorthand | `{ property: "og:title", content: "..." }` |
| Migration flag | `v2_meta: true` future flag | N/A (v2 default) |
