---
name: trpc-patterns
description: tRPC API patterns using Vertical Slice Architecture. Use when building tRPC procedures, routers, and handling API concerns.
---

# tRPC Patterns

Best practices for building tRPC APIs with Vertical Slice Architecture.

## When This Applies

- When `@trpc/server` is in dependencies
- Building API procedures
- Organizing backend features

## Quick Reference

| Section | Impact | Prefix |
|---------|--------|--------|
| Architecture | CRITICAL | `arch-` |
| Procedures | HIGH | `proc-` |
| Schemas | HIGH | `schema-` |
| Error Handling | MEDIUM-HIGH | `error-` |
| Data Access | MEDIUM | `data-` |
| Cross-Slice | MEDIUM | `cross-` |

## File Structure

```
packages/api/src/
  features/
    invitations/
      create/
        create.procedure.ts
        create.schema.ts
        create.repository.ts
        create.test.ts
      list/
        ...
      router.ts
  shared/
    procedures.ts
    context.ts
    errors.ts
  router.ts
```

## Rules

See `rules/` directory for individual rules organized by section prefix.
