---
name: server-actions
description: Enforces project server actions coding conventions when creating or modifying server actions using next-safe-action, and ensures consistent client-side consumption patterns using the project's useServerAction hook. This skill covers both server-side action implementation and frontend integration patterns.
---

# Server Actions Skill

## Purpose

This skill enforces the project server actions coding conventions automatically during server action development. It ensures consistent patterns for authentication, validation, error handling, Sentry integration, cache invalidation, and client-side consumption via the `useServerAction` hook.

## Activation

This skill activates when:

- Creating new server actions in `src/lib/actions/`
- Modifying existing server action files (`.actions.ts`)
- Implementing form submissions that call server actions
- Working with the next-safe-action library
- Creating components that consume server actions via `useServerAction`
- Implementing dialogs, forms, or features that require mutations

## Workflow

1. Detect server action work (file path contains `actions/` or imports from `next-safe-action` or `use-server-action`)
2. Load `references/Server-Actions-Conventions.md`
3. Generate/modify code following all conventions
4. Scan for violations of server action patterns (both server-side and client-side)
5. Auto-fix all violations (no permission needed)
6. Report fixes applied

## Server-Side Key Patterns

- Use `authActionClient`, `adminActionClient`, or `publicActionClient` based on auth requirements
- Always use `ctx.sanitizedInput` parsed through Zod schema (never use `parsedInput` directly)
- Include proper metadata with `actionName` and `isTransactionRequired`
- **Use `withActionErrorHandling()` wrapper** for automatic Sentry context, breadcrumbs, and error handling (recommended)
- Alternatively, use `withActionBreadcrumbs()` for breadcrumbs without error handling
- Use `trackCacheInvalidation()` to log cache failures as warnings without throwing
- Use facades for business logic (actions should be thin orchestrators)
- Handle errors with `handleActionError` utility (automatic with `withActionErrorHandling`)
- Invalidate cache after mutations using `CacheRevalidationService`
- Return consistent response shape: `{ success, message, data }`

## Client-Side Key Patterns

- Always use `useServerAction` hook from `@/hooks/use-server-action` (never `useAction` directly)
- Use `executeAsync` with `toastMessages` for user-initiated mutations
- Use `execute` with `isDisableToast: true` for silent background operations
- Use `breadcrumbContext` for Sentry tracking on user-initiated actions (provides `action` and `component` names)
- Access results via `data.data` in callbacks or `result?.data?.data` from result object
- Use `isExecuting` for loading states and button disabled states
- Integrate with `useAppForm` for form submissions with focus management
- Use `withFocusManagement` HOC and `useFocusContext` for form error focusing

## Usage Pattern Reference

| Use Case               | Hook Setup                    | Execution                               |
| ---------------------- | ----------------------------- | --------------------------------------- |
| Form submission        | `toastMessages` + `onSuccess` | `await executeAsync(value)`             |
| Delete with navigation | `toastMessages`               | `await executeAsync(id).then(redirect)` |
| Search/autocomplete    | `isDisableToast: true`        | `execute(query)` in useEffect           |
| Silent background ops  | `isDisableToast: true`        | `execute(data)` in callback             |
| Availability check     | `isDisableToast: true`        | `execute(value)` in useEffect           |

## References

- `references/Server-Actions-Conventions.md` - Complete server actions conventions (server & client)
