---
name: remix-v2-forms
description: Remix v2 form submissions and mutations. Use when implementing forms, optimistic UI, file uploads, or multi-action routes. Triggers on <Form>, useFetcher, useSubmit, useNavigation for pending state, unstable_parseMultipartFormData, fetcher.formData, intent-based actions, encType multipart.
---

# Remix v2 Forms & Mutations

Canonical mutation primitives for the `@remix-run/react@^2` route-module
framework. A correct Remix v2 mutation is: a `<Form method="post">` (or
`<fetcher.Form>`), an `action` that parses `request.formData()` and returns
either `redirect(...)` or `json(...)`, and UI that reads `useActionData()`
(or `fetcher.data`) for errors plus `useNavigation()` (or `fetcher.state`)
for pending state. Anything that bypasses this loop — `fetch()`, raw
`<form>`, `e.preventDefault()` + client state — silently sacrifices
revalidation, progressive enhancement, and race-safe transitions.

## Quick Reference

**`<Form>` + action**:

```tsx
import { json, redirect, type ActionFunctionArgs } from "@remix-run/node";
import { Form, useActionData, useNavigation } from "@remix-run/react";

export async function action({ request }: ActionFunctionArgs) {
  const form = await request.formData();
  const email = String(form.get("email") ?? "");
  if (!email.includes("@")) return json({ errors: { email: "Invalid" } }, { status: 400 });
  await createUser({ email });
  return redirect("/dashboard");
}

export default function Signup() {
  const actionData = useActionData<typeof action>();
  const nav = useNavigation();
  const busy = nav.state !== "idle" && nav.formAction === "/signup";
  return (
    <Form method="post" replace>
      <input name="email" type="email" />
      {actionData?.errors?.email ? <em>{actionData.errors.email}</em> : null}
      <button disabled={busy}>{busy ? "Signing up..." : "Sign Up"}</button>
    </Form>
  );
}
```

## Primitives

| Name | Purpose |
|---|---|
| `<Form>` from `@remix-run/react` | Navigating, progressively-enhanced form that posts to a route `action` and triggers full-page revalidation |
| `<Form navigate={false}>` | Shorthand for "post via fetcher; do not navigate." Equivalent to `<fetcher.Form>` without holding a fetcher ref — useful when you only need pending state, not a programmatic handle |
| `useFetcher()` | Non-navigating submission channel for inline mutations, list rows, popovers — same revalidation, no URL change |
| `useFetchers()` | **Read-only** array of all in-flight fetcher states across the app. Use for global pending indicators (top-bar loader) without prop drilling. No `Form`/`submit`/`load` methods on the returned items — just `formData`, `state`, etc. |
| `useNavigation()` | Observes page-level navigation; the source of truth for `<Form>` pending state |
| `useSubmit()` | Programmatic submission (onChange autosave, keyboard shortcuts). Accepts `HTMLFormElement`, `FormData`, plain object (form-encoded), or plain object encoded as JSON via `{ encType: "application/json" }` |
| `useActionData<typeof action>()` | Read the most recent action result for the current route |

State transitions:

- `useNavigation().state`: `idle → submitting → loading → idle` for non-GET
  form submissions; `idle → loading → idle` for GET navigation.
- `useFetcher().state`: `idle → submitting → loading → idle`.

**Asymmetry:** `useNavigation` skips `submitting` for GET navigations; `useFetcher` does NOT — only `fetcher.load()` skips it. `<fetcher.Form method='get'>` and `fetcher.submit(..., {method:'get'})` both transition through `submitting`.

## Key Patterns

### `<Form>` for navigation, `useFetcher` for in-place

`<Form>` changes the URL, adds history, and revalidates all loaders.
`useFetcher` does the same revalidation but stays on the current URL.
Each `useFetcher()` call returns an independent submission channel, so
two rows submitting at once do not share pending state.

### Intent pattern for multiple actions on one route

One `action`, switch on `formData.get("intent")`, distinct
`<button name="intent" value="...">` per operation. Only the clicked
submit button's `name=value` lands in the body. See
[references/intent-actions.md](references/intent-actions.md).

### Optimistic UI from `formData`

`fetcher.formData` and `navigation.formData` are populated synchronously
on submit and cleared at `idle`. Read directly each render; never mirror
into local React state. See
[references/optimistic-ui.md](references/optimistic-ui.md).

### File uploads need `encType="multipart/form-data"`

Without it, `request.formData()` strips file data and you get the
filename string instead of a `File`. Parse with
`unstable_parseMultipartFormData` and a bounded upload handler. The
`unstable_` prefix is permanent in v2. See
[references/uploads.md](references/uploads.md).

## Gates (decision sequencing)

Answer **in order**. **Pass** means the condition is true; pick the API
on the same line and **stop**.

### `<Form>` vs `useFetcher`

1. **Does the URL need to change after the mutation** (creating a record
   and routing to `/records/:id`, deleting and going back to a list,
   multi-step flow)?
   - **Pass →** `<Form method="post">` + `redirect(...)` from the action. **Stop.**
   - **Fail →** Step 2.
2. **Is this a mutation against a row, cell, toggle, or sub-section while
   the user stays on the same page** (favorite, like, increment quantity,
   inline edit)?
   - **Pass →** `useFetcher()` with `<fetcher.Form>`. **Stop.**
   - **Fail →** Step 3.
3. **Is this loading data outside of normal navigation** (popover content,
   combobox results, prefetch)?
   - **Pass →** `fetcher.load(href)`. **Stop.**
   - **Fail →** Default to `<Form>`. Navigation is the conservative
     choice — revalidation and history work out of the box.

Hard rule: never reach for `fetch()` or `axios` for in-app mutations
against your own Remix routes. That bypasses the action lifecycle and
skips loader revalidation.

### `useNavigation` vs `useFetcher.state` for pending state

1. **Is the pending indicator global** (page spinner in root, top-bar
   loading bar)?
   - **Pass →** `useNavigation()` in `root.tsx`
     (`navigation.state !== "idle"`). **Stop.**
   - **Fail →** Step 2.
2. **Was the mutation made with `useFetcher`?**
   - **Pass →** Use that fetcher's `fetcher.state`. `useNavigation()`
     will NOT reflect fetcher activity. **Stop.**
   - **Fail →** Step 3.
3. **Is the indicator scoped to one row/button inside a list where each
   row has its own fetcher?**
   - **Pass →** Use the per-row `fetcher.state` (or look up by key via
     `useFetchers()`) so other rows do not flicker. **Stop.**
   - **Fail →** Step 4.
4. **Is the indicator scoped to the form just submitted via `<Form>`?**
   - **Pass →** `useNavigation()` AND check
     `navigation.formAction === "/expected-path"` so unrelated navigations
     don't trigger your local spinner. **Stop.**
   - **Fail →** Step 5.
5. **Need to render an optimistic value?**
   - **Pass →** Read `navigation.formData?.get("field")` (page form) or
     `fetcher.formData?.get("field")` (fetcher) — both are populated
     while `state !== "idle"`. **Stop.**

## Additional Documentation

- **`<Form>` component**: See [references/form.md](references/form.md) for
  `<Form>` vs native `<form>` vs `fetch()`, progressive enhancement,
  redirect-after-success, and validation error display via `useActionData`.
- **`useFetcher`**: See [references/fetcher.md](references/fetcher.md) for
  inline mutations, list operations, popovers, `fetcher.state`,
  `fetcher.data`, `fetcher.Form`, `fetcher.submit`, `fetcher.load`.
- **Optimistic UI**: See
  [references/optimistic-ui.md](references/optimistic-ui.md) for
  `fetcher.formData` and `useNavigation.formData`, when to apply, and
  reverting on failure.
- **File uploads**: See [references/uploads.md](references/uploads.md)
  for `unstable_parseMultipartFormData`,
  `unstable_createMemoryUploadHandler`,
  `unstable_createFileUploadHandler`, and bounded handlers.
- **Intent-based actions**: See
  [references/intent-actions.md](references/intent-actions.md) for
  multiple actions on one route via the FormData `intent` field.

## Comparison

| Concern | `<Form>` | `useFetcher` | Native `<form>` | `fetch()` |
|---|---|---|---|---|
| URL change / history entry | Yes | No | Yes (hard nav) | No |
| Works without JS | Yes | Yes | Yes | No |
| Revalidates loaders | Yes | Yes | Yes (hard reload) | No |
| Pending state hook | `useNavigation()` | `fetcher.state` | None | Manual |
| Optimistic input source | `navigation.formData` | `fetcher.formData` | None | Manual |
| In-app mutation use case | Create / delete / multi-step | Inline / row / toggle | External targets only | Never for own routes |
