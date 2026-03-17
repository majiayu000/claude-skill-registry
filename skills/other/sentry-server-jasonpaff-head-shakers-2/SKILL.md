---
name: sentry-server
description: Enforces project server-side Sentry monitoring conventions when implementing error tracking, performance monitoring, and breadcrumb logging in server actions, facades, middleware, and API routes. This skill ensures consistent patterns for context setting, breadcrumb categories, error capture, and performance spans.
---

# Sentry Server Monitoring Skill

## Purpose

This skill enforces the project **server-side** Sentry monitoring conventions automatically during error tracking implementation. It ensures consistent patterns for context setting, breadcrumb categories, error capture, performance spans, and middleware integration.

**Note:** For client-side/front-end Sentry patterns, use the `sentry-client` skill instead.

## Activation

This skill activates when working on **server-side code**:

- Creating or modifying server actions in `src/lib/actions/`
- Implementing error handling in facades (`src/lib/facades/`)
- Setting up performance monitoring spans in server code
- Adding breadcrumbs in server-side operations
- Working with middleware (`src/middleware.ts`, `src/lib/middleware/`)
- API routes (`src/app/api/`)
- Instrumentation files (`src/instrumentation.ts`)

## Workflow

1. Detect server-side Sentry work (imports from `@sentry/nextjs` in server files)
2. Load `references/Sentry-Server-Conventions.md`
3. Generate/modify code following all conventions
4. Scan for violations of Sentry patterns
5. Auto-fix all violations (no permission needed)
6. Report fixes applied

## Key Patterns

### Server Actions

- Set context at the start with `Sentry.setContext(SENTRY_CONTEXTS.*, {...})`
- Add breadcrumbs for successful operations
- Log non-critical failures (e.g., cache invalidation) with `level: 'warning'`

### Facades

- Add breadcrumbs for non-blocking operations (Cloudinary cleanup)
- Capture non-critical exceptions without failing the operation

### Middleware

- Use `Sentry.withScope` and `Sentry.startSpan` for performance tracking
- Set tags and context within the scope

### Instrumentation

- Export `onRequestError = Sentry.captureRequestError` for RSC error capture

## Constants (Always Use)

| Constant                       | Import Path              | Purpose                        |
| ------------------------------ | ------------------------ | ------------------------------ |
| `SENTRY_CONTEXTS`              | `@/lib/constants/sentry` | Context names for `setContext` |
| `SENTRY_BREADCRUMB_CATEGORIES` | `@/lib/constants/sentry` | Breadcrumb category values     |
| `SENTRY_LEVELS`                | `@/lib/constants/sentry` | Breadcrumb level values        |
| `SENTRY_TAGS`                  | `@/lib/constants/sentry` | Tag names for `setTag`         |
| `SENTRY_OPERATIONS`            | `@/lib/constants/sentry` | Operation names for spans      |

## Helper Utilities (Recommended)

Import from `@/lib/utils/sentry-server/breadcrumbs.server`:

### For Server Actions

| Function                    | Purpose                                                    |
| --------------------------- | ---------------------------------------------------------- |
| `withActionErrorHandling()` | Wrap action with automatic breadcrumbs + error handling    |
| `withActionBreadcrumbs()`   | Wrap action with breadcrumbs only (no error handling)      |
| `trackActionEntry()`        | Track action operation start                               |
| `trackActionSuccess()`      | Track action success with optional result data             |
| `trackActionWarning()`      | Track action warning for partial failures                  |
| `trackCacheInvalidation()`  | Track cache invalidation with automatic warning on failure |
| `setActionContext()`        | Set Sentry context with type-safe keys                     |

### For Facades

| Function                  | Purpose                                                    |
| ------------------------- | ---------------------------------------------------------- |
| `withFacadeBreadcrumbs()` | Wrap facade method with automatic breadcrumbs              |
| `trackFacadeEntry()`      | Track facade operation start                               |
| `trackFacadeSuccess()`    | Track facade success with optional result data             |
| `trackFacadeWarning()`    | Track facade warning for partial failures                  |
| `trackFacadeError()`      | Track facade error                                         |
| `facadeBreadcrumb()`      | Add a simple breadcrumb for facade operations              |
| `captureFacadeWarning()`  | Capture non-critical exception with warning level and tags |

See `references/Sentry-Server-Conventions.md` for complete documentation with examples.

## Usage Pattern Reference

| Use Case             | Primary Method            | Level     |
| -------------------- | ------------------------- | --------- |
| Action start         | `Sentry.setContext`       | N/A       |
| Successful operation | `Sentry.addBreadcrumb`    | `INFO`    |
| Non-critical failure | `Sentry.captureException` | `warning` |
| Critical failure     | Let error propagate       | `error`   |
| Performance tracking | `Sentry.startSpan`        | N/A       |

## File Patterns

This skill applies to:

- `src/lib/actions/**/*.ts`
- `src/lib/facades/**/*.ts`
- `src/lib/middleware/**/*.ts`
- `src/middleware.ts`
- `src/app/api/**/*.ts`
- `src/instrumentation.ts`
- `sentry.server.config.ts`
- `sentry.edge.config.ts`

## References

- `references/Sentry-Server-Conventions.md` - Complete server-side Sentry monitoring conventions
