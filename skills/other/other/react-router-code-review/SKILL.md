---
name: react-router-code-review
description: Reviews React Router code for proper data loading, mutations, error handling, and navigation patterns. Use when reviewing React Router v6.4+ code, loaders, actions, or navigation logic.
---

# React Router Code Review

## Quick Reference

| Issue Type | Reference |
|------------|-----------|
| useEffect for data, missing loaders, params | [references/data-loading.md](references/data-loading.md) |
| Form vs useFetcher, action patterns | [references/mutations.md](references/mutations.md) |
| Missing error boundaries, errorElement | [references/error-handling.md](references/error-handling.md) |
| navigate() vs Link, pending states | [references/navigation.md](references/navigation.md) |

## Review Checklist

- [ ] Data loaded via `loader` not `useEffect`
- [ ] Route params accessed type-safely with validation
- [ ] Using `defer()` for parallel data fetching when appropriate
- [ ] Mutations use `<Form>` or `useFetcher` not manual fetch
- [ ] Actions handle both success and error cases
- [ ] Error boundaries with `errorElement` on routes
- [ ] Using `isRouteErrorResponse()` to check error types
- [ ] Navigation uses `<Link>` over `navigate()` where possible
- [ ] Pending states shown via `useNavigation()` or `fetcher.state`
- [ ] No navigation in render (only in effects or handlers)

## Valid Patterns (Do NOT Flag)

These patterns are correct React Router usage - do not report as issues:

- **useEffect for client-only data** - Loaders run server-side; localStorage, window dimensions, and browser APIs must use useEffect
- **navigate() in event handlers** - Link is for declarative navigation; navigate() is correct for imperative navigation in callbacks/handlers
- **Type annotation on loader data** - `useLoaderData<typeof loader>()` is a type annotation, not a type assertion
- **Empty errorElement at route level** - Route may intentionally rely on parent error boundary
- **Form without action prop** - Posts to current URL by convention; explicit action is optional
- **loader returning null** - Valid when data may not exist; null is a legitimate loader return value
- **Using fetcher.data without checking fetcher.state** - May be intentional when stale data is acceptable during revalidation

## Context-Sensitive Rules

Only flag these issues when the specific context applies:

| Issue | Flag ONLY IF |
|-------|--------------|
| Missing loader | Data is available server-side (not client-only) |
| useEffect for data fetching | Data is NOT client-only (localStorage, browser APIs, window size) |
| Missing errorElement | No parent route in the hierarchy has an error boundary |
| navigate() instead of Link | Navigation is NOT triggered by an event handler or conditional logic |

## When to Load References

- Reviewing data fetching code → data-loading.md
- Reviewing forms or mutations → mutations.md
- Reviewing error handling → error-handling.md
- Reviewing navigation logic → navigation.md

## Review Questions

1. Is data loaded in loaders instead of effects?
2. Are mutations using Form/action patterns?
3. Are there error boundaries at appropriate route levels?
4. Is navigation declarative with Link components?
5. Are pending states properly handled?

## Before Submitting Findings

Load and follow [review-verification-protocol](../review-verification-protocol/SKILL.md) before reporting any issue.
