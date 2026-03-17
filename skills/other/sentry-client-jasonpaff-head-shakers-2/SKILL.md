---
name: sentry-client
description: Enforces project client-side Sentry monitoring conventions when implementing error boundaries, route-level error pages, user interaction tracking, and client component error handling. This skill ensures consistent patterns for global error handling, breadcrumbs, and front-end error capture.
---

# Sentry Client Monitoring Skill

## Purpose

This skill enforces the project **client-side/front-end** Sentry monitoring conventions automatically during error tracking implementation. It ensures consistent patterns for error boundaries, route-level error pages, user interaction tracking, and client component error handling.

**Note:** For server-side Sentry patterns (server actions, facades, middleware), use the `sentry-server` skill instead.

## Activation

This skill activates when working on **client-side/front-end code**:

- Creating or modifying client components with error handling
- Implementing error boundaries (`src/components/ui/error-boundary/`)
- Creating route-level error pages (`error.tsx` files)
- Working on the global error handler (`global-error.tsx`)
- Adding user interaction tracking/breadcrumbs in client components
- Working with client instrumentation (`src/instrumentation-client.ts`)
- Components with `'use client'` directive that need error tracking

## Workflow

1. Detect client-side Sentry work (imports from `@sentry/nextjs` in client files)
2. Load `references/Sentry-Client-Conventions.md`
3. Generate/modify code following all conventions
4. Scan for violations of Sentry patterns
5. Auto-fix all violations (no permission needed)
6. Report fixes applied

## Key Patterns

### Error Boundaries

- Use class-based `ErrorBoundary` component for component-level errors
- Capture exceptions in `componentDidCatch` with full context
- Log user actions (retry, continue) with `captureMessage`

### Route-Level Error Pages

- ALL `error.tsx` files MUST have Sentry integration
- Use `captureException` in `useEffect` with proper context and tags
- Include digest, route name, and feature area in context

### Global Error Handler

- `global-error.tsx` captures fatal errors with `level: 'fatal'`
- Include error digest and route context

### Client Components

- Add breadcrumbs before significant user interactions
- Track form submissions, dialog opens, and key actions
- Capture exceptions for failed client-side operations

## Constants (Always Use)

| Constant                       | Import Path              | Purpose                        |
| ------------------------------ | ------------------------ | ------------------------------ |
| `SENTRY_CONTEXTS`              | `@/lib/constants/sentry` | Context names for `setContext` |
| `SENTRY_BREADCRUMB_CATEGORIES` | `@/lib/constants/sentry` | Breadcrumb category values     |
| `SENTRY_LEVELS`                | `@/lib/constants/sentry` | Breadcrumb level values        |
| `SENTRY_TAGS`                  | `@/lib/constants/sentry` | Tag names for tags             |

## Usage Pattern Reference

| Use Case              | Primary Method            | Level   |
| --------------------- | ------------------------- | ------- |
| Route error page      | `Sentry.captureException` | `error` |
| Global error          | `Sentry.captureException` | `fatal` |
| Error boundary catch  | `Sentry.captureException` | `error` |
| Error boundary reset  | `Sentry.captureMessage`   | `info`  |
| User interaction      | `Sentry.addBreadcrumb`    | `info`  |
| Form submission start | `Sentry.addBreadcrumb`    | `info`  |
| Client action failure | `Sentry.captureException` | `error` |

## File Patterns

This skill applies to:

- `src/app/**/error.tsx`
- `src/app/global-error.tsx`
- `src/components/ui/error-boundary/**/*.tsx`
- `src/instrumentation-client.ts`
- Client components (`'use client'`) with Sentry imports
- `src/app/**/components/*-client.tsx`
- `src/components/feature/**/*.tsx` with error handling

## References

- `references/Sentry-Client-Conventions.md` - Complete client-side Sentry monitoring conventions
