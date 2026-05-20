---
name: wiring-framework
description: Use for API/SWR wiring in PierceDesk. Covers Supabase auth patterns, client-to-API wiring, data fetching for large datasets or high-frequency updates, and references to docs/system wiring guidance.
---

# Wiring Framework Skill

## Core wiring rules

- **Supabase auth is the only auth system**; always use the established Supabase auth flow.
- **Client → API → Supabase**: Client uses SWR/axios to call Next.js API routes; API routes use Supabase server client.
- **Never call Supabase directly from UI components** unless the existing pattern explicitly does so.
- **Always scope by auth.uid() in API routes** and rely on RLS enforcement.
- **Reuse SWR hooks** in `src/services/swr/api-hooks/` instead of creating ad-hoc fetches.

## Efficiency rules

### Large datasets

- Prefer server-side filtering, pagination, and select lists (avoid `select('*')`).
- Use query params for filters in API routes (e.g., `?contact_id=...&type=...`).
- Return grouped/aggregated data from API endpoints when UI expects grouped data.

### High-frequency updates

- Use SWR `dedupingInterval`, `refreshInterval`, and `revalidateOnFocus` thoughtfully.
- Use `mutate` with optimistic updates for drag/drop or fast UI state changes.
- Avoid redundant API calls by caching or batching where possible.

## Supabase auth patterns

- Server-side auth via `@supabase/ssr` in API routes.
- Root layout validates session; middleware can redirect authenticated users.
- Follow the documented auth/RLS decisions in docs/system.

## Required references (read before wiring work)

- `references/system-docs-map.md`
- `references/auth-patterns-map.md`

## Process checklist

1. Identify existing SWR hooks for the feature; reuse or extend.
2. Confirm API route patterns from docs/system design.
3. Ensure API routes use Supabase server client + auth validation.
4. Apply filtering/pagination strategy for large datasets.
5. Add optimistic updates for high-frequency UI actions when needed.
6. Verify responses match existing mock data shapes.
