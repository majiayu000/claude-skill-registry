---
name: markdowntown-backend
description: Backend API routes, Prisma schema/migrations, and server-side validation patterns for markdowntown. Use when editing Next.js App Router API handlers, Prisma models/migrations, auth/session gating, rate limits, cache revalidation, or backend validation logic.
---

# markdowntown-backend

## Core workflow
1. Identify whether the change is an API route, a data-model change (Prisma), or validation logic.
2. For API routes, confirm auth/rate-limits + response shape and cache tag invalidation.
3. For Prisma changes, update `prisma/schema.prisma`, run migrations/generate, and update callers.
4. For validation updates, reuse shared validators and keep error messages consistent.
5. Run compile/lint/unit tests; update API tests if response shapes change.

## Quick map
- **API routes:** `src/app/api/**/route.ts`
- **Auth gating:** `src/lib/requireSession.ts`, `src/lib/auth.ts`
- **Rate limiting + abuse logging:** `src/lib/rateLimiter.ts`, `src/lib/reports.ts`
- **Prisma client:** `src/lib/prisma.ts`
- **Prisma schema + migrations:** `prisma/schema.prisma`, `prisma/migrations/*`
- **Cache tags + revalidation:** `src/lib/cacheTags.ts`, `src/lib/revalidate.ts`, `src/lib/cache.ts`
- **Validation:** `src/lib/validation.ts`, `src/lib/skills/skillValidate.ts`, `src/lib/uam/uamValidate.ts`, `src/lib/uam/uamLint.ts`

## Guardrails
- Keep API responses deterministic; use `NextResponse.json` with explicit status codes.
- When mutating data, call `safeRevalidateTag` for list/detail tags and landing.
- Do not bypass `requireSession` for private routes; keep 401 responses consistent.
- Avoid direct Prisma access from UI components; use API routes or server utilities.
- Always look for refactoring or bugs; create new bd tasks when you spot them.

## References
- docs/DEV_ONBOARDING.md
- docs/MIGRATIONS.md
- docs/architecture/architecture.md
- docs/architecture/security-public-rendering.md
- codex/skills/markdowntown-backend/references/api-routes.md
- codex/skills/markdowntown-backend/references/prisma.md
- codex/skills/markdowntown-backend/references/validation.md
