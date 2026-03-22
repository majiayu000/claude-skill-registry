---
name: tanstack-start
description: TanStack Start, Router, Query, and Server Functions patterns and best practices for this project.
user-invocable: true
---

# TanStack Start Patterns

## Server Functions
- Define with `createServerFn` from `@tanstack/react-start`
- Use `.validator()` for input validation (e.g. with zod)
- Use `.handler()` for the implementation
- Server functions run on the server only — safe for DB access and secrets

## Router
- File-based routing in `src/routes/`
- Use `createFileRoute` for route definitions
- Use `loader` for server-side data fetching (runs on server)
- Use `beforeLoad` for auth guards and redirects
- Route context flows from `__root.tsx` to child routes

## Query
- Use `queryOptions` to define reusable query configs
- Use `useSuspenseQuery` in components for data fetching
- Invalidate queries after mutations with `queryClient.invalidateQueries()`
- TanStack Query handles caching, deduplication, and background refetching

## Key Conventions
- Path alias: `@/` → `apps/web/src/`
- Route files: `src/routes/<path>.tsx`
- Layouts: `src/routes/_<layout>.tsx` (pathless layout routes)
- API routes: `src/routes/api/<name>.ts`
