---
name: mern-std
description: Coding standards for MERN Next.js apps in a pnpm monorepo.
---

## Purpose

Ensure consistent, maintainable code. Complements stack, security, and NFR skills.

## Monorepo structure

```
apps/web/                    # Next.js app
  src/
    app/                     # Next.js app router (pages, layouts, API routes)
      api/**/route.ts        # API route handlers
      page.tsx               # Pages
      layout.tsx             # Layouts
    components/              # React components
    lib/                     # Utilities
    server/                  # Server-only utilities
      db/models/             # Mongoose models
packages/shared/             # Zod schemas, types, utilities
```

**Important:** All app router files MUST be in `apps/web/src/app/`, never in `apps/web/app/`.
Next.js with `--src-dir` expects the app directory inside `src/`.

- `apps/web` depends on `packages/shared` via `workspace:*`
- Feature-specific components live under the feature folder

## Key conventions

### Environment

- Never access `process.env` directly in app code; use the env module

### Schemas and types

- Define request/response schemas in `packages/shared`
- Infer types from zod: `z.infer<typeof Schema>` — don't duplicate interfaces
- Reuse schemas across client and server

### API route handlers

- Validate input with zod at boundary
- Consistent JSON envelope for responses
- Safe error mapping (no stack traces to clients)
- Pagination for list endpoints (cursor or offset)
- Rate limiting on auth/expensive endpoints

### Next.js segment configuration

Segment config exports (`revalidate`, `dynamic`, `runtime`, etc.) must be **literal values**, not imported constants:

```typescript
// CORRECT - literal number
export const revalidate = 3600;

// WRONG - imported constant (fails in Next.js 16+)
import { REVALIDATE_SECONDS } from '@/config';
export const revalidate = REVALIDATE_SECONDS;
```

This is a Next.js static analysis requirement.

### Mongoose

- Explicit schemas with `timestamps: true`
- Indexes defined with comments explaining why
- Sanitize user input (reject `$` and `.` keys) before queries

### Naming

- Folders: `kebab-case`
- React components: `PascalCase.tsx`
- Utilities: `camelCase.ts`
- Named exports for utilities; default exports allowed for React components

## Testing requirements

TDD is mandatory — see `/shared-tdd` for the red-green-refactor workflow and evidence requirements.

**Test command:** `pnpm test`

### What to test

- Unit tests for: validation helpers, sanitization helpers, non-trivial business logic
- Component tests for: user interactions, conditional rendering
- API tests for: request validation, response format, error cases
- Playwright for critical user journeys only

### Test file conventions

| Source | Test |
|--------|------|
| `apps/web/src/components/Feature.tsx` | `apps/web/src/components/__tests__/Feature.test.tsx` |
| `apps/web/src/lib/helper.ts` | `apps/web/src/lib/__tests__/helper.test.ts` |
| `apps/web/src/app/api/foo/route.ts` | `apps/web/src/app/api/foo/__tests__/route.test.ts` |
| `packages/shared/src/schemas/foo.ts` | `packages/shared/src/schemas/foo.test.ts` |

## Output

For significant code changes, briefly note:

- Any deviation from these standards and why

## Reference

For detailed patterns and examples, see `reference/mern-std-reference.md`
