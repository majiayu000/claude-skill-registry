---
name: remix-v2-forms-review
description: Reviews Remix v2 form code for manual fetch() mutations, native <form> misuse, wrong useNavigation/useFetcher choice, missing pending state, unbounded uploads, and intent-pattern violations. Use when reviewing form/mutation code in a Remix v2 codebase.
---

# Remix v2 Forms Code Review

See [beagle-react:remix-v2-forms](../remix-v2-forms/SKILL.md) for canonical
patterns. This skill flags violations; the sibling skill teaches the patterns.

## Quick Reference

| Issue Type | Reference |
|------------|-----------|
| Manual `fetch()`, native `<form>`, wrong `<Form>` vs `useFetcher` choice | [references/form-vs-fetcher.md](references/form-vs-fetcher.md) |
| `useState` loading flags, `useNavigation` for per-row, missing pending state | [references/pending-state.md](references/pending-state.md) |
| Unbounded memory uploads, missing `encType`, unvalidated FormData, mirrored optimistic state | [references/uploads-validation.md](references/uploads-validation.md) |
| Route sprawl instead of intent pattern, PUT/DELETE without PE fallback | [references/multi-action-routes.md](references/multi-action-routes.md) |

## Review Checklist

- [ ] In-app mutations use `<Form>` or `<fetcher.Form>`, never `fetch()` / `axios`
- [ ] `<Form>` is imported from `@remix-run/react` (not native `<form>`) for POST mutations
- [ ] `useFetcher` used when URL should NOT change (row toggle, inline edit)
- [ ] `<Form>` + `redirect(...)` used when URL SHOULD change (create, delete-then-list)
- [ ] Pending state derived from `useNavigation()` or `fetcher.state`, never `useState`
- [ ] Per-row pending uses per-row `fetcher.state` (not page-global `useNavigation`)
- [ ] `useNavigation()` calls check `navigation.formAction` to scope to expected path
- [ ] Optimistic UI reads `fetcher.formData` / `navigation.formData` directly (not mirrored)
- [ ] Actions returning success `redirect(...)`, returning `json()` only for errors / same-page
- [ ] `<Form encType="multipart/form-data">` on every file-upload form
- [ ] `unstable_createMemoryUploadHandler` always has `maxPartSize`; large files use disk/stream handler
- [ ] `FormData` values are validated/coerced before reaching the DB (no `form.get(x) as string`)
- [ ] Multiple mutations on one route use intent pattern, not separate routes
- [ ] `method="put|patch|delete"` is documented as JS-only, or rewritten as POST + intent
- [ ] `nav.formMethod` / `fetcher.formMethod` compared against UPPERCASE strings (`"POST"`, `"GET"`); v2's `v2_normalizeFormMethod` default returns UPPERCASE — `=== "post"` silently never matches.

## Valid Patterns (Do NOT Flag)

These are correct Remix v2 usage and should not be reported:

- **`<Form>` without `action` prop** — posts to the current URL by convention; explicit `action` is optional.
- **GET `<Form>`** — legitimate for search/filter UIs; hits the loader with form fields as URL search params and does NOT call an action. Most "hygiene" rules (intent, `redirect`, `encType`) apply only to POST forms.
- **Multiple `useFetcher()` instances on one page** — each call returns an independent submission channel; intentional for parallel mutations to different rows.
- **`useSubmit()` in an event handler** — correct programmatic submission for autosave, keyboard shortcuts, or `onChange` triggers.
- **Reading `fetcher.formData` during a submission** — intended; this is the canonical optimistic source.
- **`useActionData` data persisting after submission** — known behavior; it returns the last action result until the next navigation or action.
- **`navigate={false}` on `<Form>`** — turns it into a fetcher form; equivalent to `<fetcher.Form>` without holding a fetcher ref.
- **`unstable_` prefix on `parseMultipartFormData` / upload handlers** — permanent in v2; do not flag as "unstable API".

## Context-Sensitive Rules

Only flag these when the listed condition holds:

| Issue | Flag ONLY IF |
|-------|--------------|
| Native `<form>` instead of `<Form>` | Method is POST and the route has an `action` — GET forms and external-URL forms are fine |
| Missing pending state | The form is POST and there is no `useNavigation()` / `fetcher.state` read anywhere in the component |
| Action returns `json({ ok: true })` after a create | The route is a "/new" or creation surface — same-page edit forms legitimately return JSON |
| `method="put"` / `"patch"` / `"delete"` | Progressive enhancement is in scope for the surface (public app) — admin/JS-only tools may opt out if documented |
| Unbounded `unstable_createMemoryUploadHandler` | The upload accepts user-controlled files (not a fixed-size internal artifact) |
| Separate routes per mutation | The mutations operate on the same resource with compatible auth — sibling resources with different rules are fine |
| `useNavigation()` without `formAction` filter | The component contains other navigation surfaces (sidebar `<Link>`, sibling forms) that would trigger false positives |
| Mirroring `fetcher.formData` into state | The shadowed value drives a user-visible element (button label, count, toggle) — a local "is-editing" flag is unrelated |

## Hard gates (before writing findings)

Run these in order. **Do not draft user-facing findings until every gate passes** for the batch you are about to report.

1. **Location evidence** — **Pass:** Each issue lists a repo path and either a line range or a short verbatim quote from the file you read (not from memory or diff-only guesswork). Name the route module, the component, and the `action` if one exists.

2. **Exemption check** — **Pass:** For each issue, you can state in one line why it is *not* covered by [Valid Patterns (Do NOT Flag)](#valid-patterns-do-not-flag) and any matching row in [Context-Sensitive Rules](#context-sensitive-rules).

3. **Form-method check** — **Pass:** Before flagging missing intent, missing `encType`, missing `redirect`, or missing pending state, you have confirmed the form is `method="post"` (or `put|patch|delete`). GET forms are legitimate for search/filter and trigger loaders, not actions — applying POST-form rules to them is a false positive.

4. **Protocol** — **Pass:** You completed the Pre-Report Verification Checklist in [review-verification-protocol](../../../beagle-core/skills/review-verification-protocol/SKILL.md) for this review.

## Additional Documentation

- **Form vs fetcher misuse** — manual `fetch()`, native `<form>`, wrong primitive: [references/form-vs-fetcher.md](references/form-vs-fetcher.md)
- **Pending state anti-patterns** — `useState` flags, page-global vs per-row, missing entirely: [references/pending-state.md](references/pending-state.md)
- **Uploads & FormData validation** — unbounded handlers, missing `encType`, unvalidated keys, mirrored optimistic state: [references/uploads-validation.md](references/uploads-validation.md)
- **Multi-action routes** — intent-pattern violations, PUT/DELETE without PE fallback, missing submit button: [references/multi-action-routes.md](references/multi-action-routes.md)
- **Canonical patterns** — see sibling [beagle-react:remix-v2-forms](../remix-v2-forms/SKILL.md)

## When to Load References

- Reviewing forms that call `fetch()` / `axios` / native `<form>`, or choose between `<Form>` and `useFetcher` → [form-vs-fetcher.md](references/form-vs-fetcher.md)
- Reviewing loading flags, spinners, disabled-button logic, per-row pending → [pending-state.md](references/pending-state.md)
- Reviewing file uploads, `unstable_*` handlers, FormData parsing, optimistic UI → [uploads-validation.md](references/uploads-validation.md)
- Reviewing routes with multiple mutations, intent fields, PUT/DELETE methods → [multi-action-routes.md](references/multi-action-routes.md)

## Review Questions

1. Does every in-app mutation flow through a route `action` (no manual `fetch()`)?
2. Is the `<Form>` vs `useFetcher` choice driven by whether the URL should change?
3. Is pending state derived from `useNavigation()` / `fetcher.state` (never `useState`)?
4. Are per-row spinners wired to per-row `fetcher.state` (not page-global `useNavigation`)?
5. Do file-upload forms set `encType="multipart/form-data"` and use bounded handlers?
6. Are FormData values validated before reaching the DB?
7. Do multiple mutations on one resource use the intent pattern, not separate routes?
8. Do POST forms have at least one real submit button for progressive enhancement?

## False-Positive Notes

- A `<Form>` rendering inside a non-route component is still tied to the
  nearest route's `action` — read the route file before flagging
  "missing action".
- `useActionData()` returning data after a successful submission is
  expected behavior; the data persists until the next navigation. Only
  flag if a success banner is rendered unconditionally without a
  dismiss path.
- Code that imports `Form` aliased (e.g. `import { Form as RemixForm }`)
  is still the Remix component — match on import source, not local name.

## Before Submitting Findings

Complete [Hard gates](#hard-gates-before-writing-findings) (especially gate 4), then report only issues that still pass the [review-verification-protocol](../../../beagle-core/skills/review-verification-protocol/SKILL.md) pre-report checks.
