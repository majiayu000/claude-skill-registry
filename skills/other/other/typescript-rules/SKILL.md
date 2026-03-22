---
name: typescript-rules
description: TypeScript coding conventions
user-invocable: false
---

# TypeScript Rules

## Types
- Never use `any` — use `unknown` with type guards or explicit types
- Prefer `interface` for object shapes, `type` for unions/intersections
- Export types alongside their functions, not from barrel files
- Use `satisfies` for type-safe object literals: `const x = { ... } satisfies Config`

## Imports
- Use `@/` path alias for imports from `apps/web/src/`
- Group imports: external libs → `@/lib/` → relative slice imports
- Use `type` imports for type-only: `import type { Foo } from './types'`

## Architecture Boundaries

### Vertical slice structure (`src/features/<slice>/`)
- Each slice owns its own server functions, queries, components, and types
- No cross-slice imports — shared code goes in `src/lib/`
- `src/lib/` modules must NOT import from `src/features/`

### File naming
- Server function files: `*.server.ts`
- Query/hooks files: `*.queries.ts`
- Component files: PascalCase (e.g., `SessionCard.tsx`)
- Test files: `*.test.ts(x)` co-located with source

## Error Handling
- Throw typed errors, not strings: `throw new Error('message')`
- Use discriminated unions for result types: `{ ok: true; data: T } | { ok: false; error: string }`
- Catch `unknown`, narrow with `instanceof`

## Functions
- Prefer named function declarations over arrow functions for top-level exports
- Use explicit return types on exported functions
- Keep functions small — max ~50 lines

## Zod
- Validate all external input (API responses, form data, URL params) with Zod
- Co-locate schemas with server functions, not in separate schema files
- Use `z.infer<typeof schema>` for derived types
