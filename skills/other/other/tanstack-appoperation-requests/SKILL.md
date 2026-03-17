---
name: tanstack-appoperation-requests
description: Standardize how API requests are defined and consumed via AppOperation together with TanStack Query. Use in React Native/Expo projects when the user mentions appOperation, QUERY_KEYS, api.ts from this kit, or wants to add new API calls, hooks, or screens that talk to the backend.
---

# TanStack Query + AppOperation Requests (Kit)

This skill is the portable version of the pattern:

- Central `AppOperation` class (`src/AppOperation.ts`).
- `QUERY_KEYS` object (`as const`) + `Requests` map + `requests` object (`src/api.ts`).
- `appOperation.getRequest` as the only HTTP entry point.
- TanStack Query hooks using `appOperation` in `queryFn` / `mutationFn`.
- A single `showToast(type, message)` handler passed to `AppOperation` (and optionally overridden via `setToastHandler`) so all success/error toasts are handled in one place; individual calls can pass `suppressToast: true` when they must be silent.

Use this whenever editing projects that consume `tanstack-appoperation-kit`.

For full instructions and examples, see the main [README](../../README.md).

