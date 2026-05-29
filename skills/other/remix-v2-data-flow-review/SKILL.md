---
name: remix-v2-data-flow-review
description: Reviews Remix v2 loaders and actions for mutations-in-loader, missing validation, leaked server fields, wrong return helpers, v1 useTransition holdovers, and revalidation traps. Use when reviewing loader/action code in a Remix v2 codebase.
---

# Remix v2 Data Flow Code Review

Targets TypeScript route modules importing from `@remix-run/*`. See [beagle-react:remix-v2-data-flow](../remix-v2-data-flow/SKILL.md) for canonical patterns.

## Scope

- **In scope**: route modules under `app/routes/` exporting `loader`, `action`, `shouldRevalidate`, or `headers`; components that consume `useLoaderData`, `useActionData`, `useNavigation`, `useFetcher`, `useRevalidator`, `<Await>`.
- **Out of scope**: form ergonomics (`<Form>` markup, accessibility, `useFetcher` UI patterns) → covered by `remix-v2-forms-review`. Route module conventions, file naming, nested routing, error boundary placement → covered by `remix-v2-routing-review`.
- **Imports expected**: `@remix-run/node` (or `@remix-run/cloudflare` / `@remix-run/deno`) for server utilities; `@remix-run/react` for hooks and components.

## Quick Reference

| Issue Type | Reference |
|------------|-----------|
| Mutations in loader, missing validation, leaked server fields, throwing primitives, missing param checks | [references/loaders.md](references/loaders.md) |
| Unvalidated FormData, `json` instead of `redirect` on success, missing error case, leaked actionData | [references/actions.md](references/actions.md) |
| `useTransition` v1 holdover, missing pending state, blanket `shouldRevalidate: false`, misused `useRevalidator` | [references/revalidation.md](references/revalidation.md) |
| `defer` for already-fast data, missing `<Suspense>`, no `errorElement` on `<Await>`, awaiting what should stream | [references/defer-await.md](references/defer-await.md) |

## Review Checklist

- [ ] Data needed for first render is in `loader`, not `useEffect`
- [ ] Loaders only read; writes live in `action`
- [ ] `request.formData()` results are validated (zod/valibot/invariant) before use
- [ ] Loader/action return values are projected DTOs — no password hashes, tokens, or `internal_*` fields
- [ ] `useLoaderData<typeof loader>()` uses the type annotation form (not `as Foo`)
- [ ] 404 / auth short-circuits `throw` a `Response` (or `json`/`redirect`), never a plain `Error` or string
- [ ] Successful action returns `redirect(...)` (PRG); validation failures return `json({ errors }, { status: 400 })`
- [ ] Action handles both success and error branches; no silent `return null`
- [ ] `params.foo` is checked with `invariant` / zod before use
- [ ] Pending UI reads `useNavigation()` / `fetcher.state` — no `useTransition`
- [ ] `formMethod` comparisons use UPPERCASE (`"POST"`, not `"post"`)
- [ ] `shouldRevalidate` returns `defaultShouldRevalidate` by default; opt-outs are narrow and justified
- [ ] `defer()` is used only when at least one promise streams (no `await` before passing it)
- [ ] Every `<Await>` is wrapped in `<Suspense>` and has an `errorElement`
- [ ] `useRevalidator().revalidate()` is reserved for focus/polling/SSE — not called immediately after a `<Form>` post or `fetcher.submit` (Remix already revalidates).

## Valid Patterns (Do NOT Flag)

These are correct Remix v2 usage and must not be reported as issues:

- **`useEffect` for client-only data** — Loaders run server-side; `localStorage`, `window` dimensions, `IntersectionObserver`, and browser-only APIs belong in `useEffect`.
- **`loader` returning `null`** — A loader may legitimately return `null` (e.g. optional resource not present); flag only if it should be a 404 `throw`.
- **`useLoaderData<typeof loader>()` as type annotation** — The `<typeof loader>` is a generic parameter feeding `SerializeFrom<T>`, not a `as`-style type assertion. Do not flag it as "unsafe cast."
- **Bare `new Response(body, init)` returns** — v2 routes may return any `Response`; `json()` is an ergonomic wrapper, not a requirement. Non-JSON bodies (binary, text, streams) correctly skip `json()`.
- **`return redirect(...)` from an action** — Both `return redirect(...)` and `throw redirect(...)` are legal in actions; throwing is required only from non-action helpers when you want to exit the calling function.
- **`loader` declared without the `request` arg** — Loaders may destructure only what they need (`{ params }`, `{ context }`, or `()` with no args); the unused arg is not a bug.
- **Parent `loader` revalidated after an unrelated action** — This is default Remix behavior, not a smell. Flag only if `shouldRevalidate` exists and is wrong.
- **Action returning `json({ errors }, { status: 400 })`** — This is the canonical validation-error pattern (keeps the form route rendered with field errors). Not the same as the "no redirect on success" anti-pattern.
- **`useRevalidator` for focus / polling / cross-tab sync** — These are the documented use cases; only flag manual `revalidate()` calls that immediately follow a `<Form>` post or `fetcher.submit` Remix would already revalidate.
- **`SerializeFrom`-induced type changes** — `Date` typed as `string`, `Map` typed as `{}` after deserialization is correct wire-format behavior, not a typing bug.

## Context-Sensitive Rules

Only flag these issues when the specific context applies:

| Issue | Flag ONLY IF |
|-------|--------------|
| Missing loader (using `useEffect` instead) | Data is available server-side and is NOT a browser-only API read |
| `loader` returns a raw ORM object | The object contains fields a reviewer would not paste into a screenshot (passwords, tokens, internal flags) |
| Action returns `json` on success | The action is invoked via `<Form>` causing a URL change — NOT via `useFetcher` |
| Missing pending UI | No `nav.state` / `fetcher.state` reference exists elsewhere in the file driving the same surface |
| `shouldRevalidate` returns `false` | The body has no condition or never references `formAction` / `currentParams` / `nextParams` |
| Manual `useRevalidator().revalidate()` | The call follows a Remix-managed mutation (`<Form>` post, `fetcher.submit`) — not focus / polling / websocket |
| `defer()` used | Every promise in the `defer({...})` payload was already `await`ed before the call |

## Hard gates (before writing findings)

Run these in order. **Do not draft user-facing findings until every gate passes** for the batch you are about to report.

1. **Location evidence** — **Pass:** Each issue lists the repo path to the route module and either a line range or a short verbatim quote from the file you read (not from memory or diff-only guesswork). Loader/action issues without a path to the `export async function loader|action` are not reportable.

2. **Exemption check** — **Pass:** For each issue, you can state in one line why it is *not* covered by [Valid Patterns (Do NOT Flag)](#valid-patterns-do-not-flag). In particular: confirm `useEffect` is not loading client-only data; confirm a bare `Response` return is not intentionally non-JSON; confirm a `loader` returning `null` is not a legitimate optional read.

3. **Type-annotation vs type-assertion check** — **Pass:** Before flagging an "unsafe cast" on loader/action consumption, confirm the code uses `as` (assertion) — not `useLoaderData<typeof loader>()` (annotation) and not `useActionData<typeof action>()` (annotation). The generic form is the documented safe path and must not be flagged.

4. **v1 holdover check** — **Pass:** Before flagging "missing pending state," grep the file for `useTransition`, `transition.submission`, `fetcher.type`, `formMethod === "post"` or `formMethod==='post'` (lowercase, any whitespace/quote variation), and `LoaderArgs` / `ActionArgs`. If present, the finding is a v1-holdover migration issue, not a missing-feature issue — label it accordingly.

5. **Protocol** — **Pass:** You completed the Pre-Report Verification Checklist in [beagle-core:review-verification-protocol](../../../beagle-core/skills/review-verification-protocol/SKILL.md) for this review.

## When to Load References

- Reviewing a `loader` body, return shape, params, throws, or sensitive-field leaks → [references/loaders.md](references/loaders.md)
- Reviewing an `action` body, FormData validation, success/error branches, or PRG redirect → [references/actions.md](references/actions.md)
- Reviewing `useNavigation` / `useTransition` migrations, `shouldRevalidate`, or `useRevalidator` use → [references/revalidation.md](references/revalidation.md)
- Reviewing `defer()`, `<Await>`, `<Suspense>`, or streaming decisions → [references/defer-await.md](references/defer-await.md)

## Review Questions

1. Is data needed for first render fetched in a `loader`, or is it stuck in a `useEffect` that defeats SSR and revalidation?
2. Does every loader return a projected DTO, or do raw ORM records (with `password`, `token`, `internal_*` fields) leak to the browser?
3. Does every action validate `request.formData()` with a schema before touching the database?
4. Does the success branch of each action `redirect(...)` so refresh / back behaves correctly (PRG)?
5. Is the consumer code using `useLoaderData<typeof loader>()` (annotation) — not `useLoaderData() as Foo` (assertion)?
6. Do any v1 holdovers remain (`useTransition`, `transition.submission`, `fetcher.type`, lowercase `formMethod`, `LoaderArgs` / `ActionArgs`)?
7. Does `shouldRevalidate` return a literal `false`, or does it reach for `defaultShouldRevalidate` and opt out narrowly?
8. Is `defer()` used only when at least one promise is passed unresolved, and is every `<Await>` wrapped in `<Suspense>` with an `errorElement`?

## Additional Documentation

- Canonical Remix v2 data-flow patterns and v1 → v2 diff → [beagle-react:remix-v2-data-flow](../remix-v2-data-flow/SKILL.md)
- Pre-report verification checklist → [beagle-core:review-verification-protocol](../../../beagle-core/skills/review-verification-protocol/SKILL.md)

## Before Submitting Findings

Complete [Hard gates](#hard-gates-before-writing-findings) (especially gate 5), then report only issues that still pass the [beagle-core:review-verification-protocol](../../../beagle-core/skills/review-verification-protocol/SKILL.md) pre-report checks.
