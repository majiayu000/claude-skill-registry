---
name: remix-v2-meta-sessions-review
description: Reviews Remix v2 code for v1-shape meta exports (BREAKING in v2), cookie security gaps (httpOnly, secure, secrets rotation), auth gates in wrong layer, and missing CSRF. Use when reviewing meta/SEO, session, auth, or form-mutation code in a Remix v2 codebase.
user-invocable: false
---

# Remix v2 Meta, Sessions, Auth, and CSRF Code Review

Reviews Remix v2 meta/SEO, session, auth-gate, and CSRF code paths. Loaded
by the umbrella `review-remix-v2` reviewer when a diff touches any of:
`meta`/`links` exports, `root.tsx`, `*.server.ts` session/cookie modules,
loaders/actions reading or writing `session`, or `<Form>`/`useFetcher`
mutations.

See [beagle-remix-v2:remix-v2-meta-sessions](../remix-v2-meta-sessions/SKILL.md) for canonical patterns.

## Quick Reference

| Issue Type | Reference |
|------------|-----------|
| **`meta` returning v1 object shape (BREAKING)**, OG shorthand, `document.title` in effect, missing `<Meta />`/`<Links />`, parent merge | [references/meta-v2-shape.md](references/meta-v2-shape.md) |
| Missing `httpOnly`/`secure`, hardcoded secrets, single-string `secrets`, replace-not-prepend rotation | [references/cookie-security.md](references/cookie-security.md) |
| Auth check in component, logout in loader, missing `commitSession`, `flash` without commit | [references/auth-gates.md](references/auth-gates.md) |
| Manual `fetch` POST bypassing CSRF, token in session cookie, no CSRF protection, shared secrets | [references/csrf.md](references/csrf.md) |

**Highest-stakes detection — call out first:** v1 `meta` object shape (`return { title, description }`) in a v2 codebase. It typechecks, but the runtime ignores it and the page renders with **no title and no meta tags**. Grep every `export const meta` and confirm the return value starts with `[`, not `{`.

## Review Checklist

- [ ] `meta` returns `MetaDescriptor[]` (array starts with `[`), NOT the v1 object shape
- [ ] OG / Twitter tags use `{ property, content }`, NOT v1 shorthand `{ "og:title": "..." }`
- [ ] No `document.title = "..."` or `useEffect(() => { document.title = ... })` — meta is set via the `meta` export
- [ ] `root.tsx` includes `<Meta />` and `<Links />` inside `<head>`
- [ ] Child `meta` that wants parent values uses `matches.flatMap((m) => m.meta ?? [])`
- [ ] `meta` null-guards `data` (loader may not have run / returned `undefined` on 404)
- [ ] Cookie config sets `httpOnly: true` and `secure: process.env.NODE_ENV === "production"`
- [ ] `secrets` is read from `process.env` (no hardcoded strings, no committed `.env.example` values)
- [ ] `secrets` is an array supporting rotation (prepend new, keep old) — not a single value
- [ ] Every `session.set`/`session.unset`/`session.flash` is followed by a response with `"Set-Cookie": await commitSession(session)`
- [ ] Auth gate is in `loader` (or `action`) via `requireUserId(request)` — NOT a component-level redirect
- [ ] Logout is an `action` (POST), not a `loader` (GET)
- [ ] Mutating actions call `csrf.validate(request)` when CSRF protection is in use
- [ ] CSRF token uses a dedicated `createCookie("csrf", ...)`, NOT the session cookie
- [ ] Mutations use `<Form>` / `useFetcher` so `AuthenticityTokenInput` attaches the token (no manual `fetch` POST)

## Valid Patterns (Do NOT Flag)

These are correct usage — do not report as issues:

- **`sameSite: "lax"`** — acceptable default. Not every app needs `"strict"`; flag only when threat model warrants stricter (e.g. CSRF protection is otherwise absent).
- **`meta` returning `[]`** — legitimate when the route intentionally emits no meta (inherits root tags or relies on a sibling).
- **`links` returning `[]`** — legitimate when the route has no route-specific stylesheets or preloads.
- **`session.flash(...)` followed on the next line by `commitSession(session)`** — the standard 2-line flash pattern. The separation is correct; do not flag it as "missing commit".
- **Auth check in `action` (not `loader`)** — correct for POST-only routes (e.g. logout, delete). Loaders gate GETs; actions gate mutations.
- **`charset` and `viewport` as plain JSX `<meta>`** in `root.tsx`'s `<head>` — preferred over the `meta` export to avoid duplicate-tag warnings under v2's no-merge behavior.
- **`secrets: [process.env.X!, process.env.X_OLD!]`** — `!` non-null assertion is acceptable when a fail-fast guard above (`if (!process.env.X) throw`) is present.
- **`throw redirect(...)`** inside a loader/action — canonical Remix pattern; the thrown response is intentional.
- **`commitSession` called in a loader (not just an action)** — required when a loader reads a flash message and must clear it.

## Context-Sensitive Rules

Only flag these issues when the specific context applies:

| Issue | Flag ONLY IF |
|-------|--------------|
| Missing CSRF validation in action | App declares `remix-utils/csrf` as its protection mechanism, OR the action is public-facing (not internal/VPN-gated) AND no `Origin` check is present |
| `sameSite: "lax"` | App has no library-based CSRF protection AND no `Origin` check — `"lax"` then becomes the only defense and is insufficient |
| Missing `secure` flag | Cookie config is the production session/CSRF cookie (not a test fixture or commented example) |
| `meta` returning `[]` | The route is documented as needing route-specific tags (e.g. a public landing page) — empty is usually intentional inheritance, do not flag by default |
| Auth check in `action` not `loader` | Route is GET-renderable (has a `loader`) — for POST-only routes, `action` is the correct gate |
| Logout in `action` AND `<Form method="post">` | Never flag — that is the canonical pattern |
| Manual `fetch` POST | The target is an internal Remix action AND no CSRF token is attached via headers |
| `secrets: [singleValue]` | App is in production OR has been deployed for long enough to need rotation — flag as recommendation, not CRITICAL |

## Hard gates (before writing findings)

Run these in order. **Do not draft user-facing findings until every gate passes** for the batch you are about to report.

1. **Location evidence** — **Pass:** Each issue lists a repo path and either a line range or a short verbatim quote from the file you read. Diff-only or memory-based claims do not pass. For meta/links/session issues, the cited file is a `.ts`/`.tsx` route module, `root.tsx`, or `*.server.ts` — not a generic config file.

2. **Exemption check** — **Pass:** For each issue, you can state in one line why it is *not* covered by [Valid Patterns (Do NOT Flag)](#valid-patterns-do-not-flag). In particular: `sameSite: "lax"`, empty `meta`/`links` arrays, and the standard `flash` + `commitSession` two-line pattern must be explicitly cleared.

3. **Meta-shape check** — **Pass:** Before flagging *anything* about `meta`, you read the actual function body and confirmed what it returns. TypeScript may have masked the shape (a v1 object can satisfy a poorly-typed `MetaFunction` alias). The check is: the return expression starts with `[` and every element is a descriptor object. If it starts with `{`, that is the v1 shape — flag as CRITICAL. If it is `[]`, that is valid (do not flag).

4. **Protocol** — **Pass:** You completed the Pre-Report Verification Checklist in [review-verification-protocol](../../../beagle-core/skills/review-verification-protocol/SKILL.md) for this review.

## When to Load References

- Reviewing any `export const meta` or `export const links`, or `root.tsx` → [meta-v2-shape.md](references/meta-v2-shape.md)
- Reviewing `createCookieSessionStorage`, `createCookie`, or any `*.server.ts` that configures cookies → [cookie-security.md](references/cookie-security.md)
- Reviewing loaders/actions that read or write `session`, or any auth helper → [auth-gates.md](references/auth-gates.md)
- Reviewing forms, fetchers, or any mutating route → [csrf.md](references/csrf.md)

## Review Questions

1. Does every `meta` export return an array, and is every OG/Twitter tag `{ property, content }`?
2. Does `root.tsx` include `<Meta />` and `<Links />` inside `<head>`?
3. Are cookies `httpOnly` + `secure: NODE_ENV === 'production'` with `secrets` from env in an array (rotation-ready)?
4. Is every session mutation followed by a `Set-Cookie: await commitSession(session)` header?
5. Is auth gated in the loader/action via a throwing helper, never in a component?
6. Is logout an `action` (POST), and do mutating actions validate CSRF (or document the threat model)?

## Additional Documentation

- [references/meta-v2-shape.md](references/meta-v2-shape.md) — v1 object shape in v2 codebases (BREAKING), OG shorthand, `document.title` antipatterns, root scaffolding, parent merging
- [references/cookie-security.md](references/cookie-security.md) — `httpOnly`/`secure`/`sameSite`, hardcoded secrets, rotation hygiene
- [references/auth-gates.md](references/auth-gates.md) — loader-level gates, logout-must-be-action, commit pairing, flash patterns
- [references/csrf.md](references/csrf.md) — `remix-utils/csrf` wiring, manual-fetch bypass, dedicated cookie, shared-secret hygiene

## Before Submitting Findings

Complete [Hard gates](#hard-gates-before-writing-findings) (especially gate 3 — meta-shape check), then report only issues that still pass the [review-verification-protocol](../../../beagle-core/skills/review-verification-protocol/SKILL.md) pre-report checks.
