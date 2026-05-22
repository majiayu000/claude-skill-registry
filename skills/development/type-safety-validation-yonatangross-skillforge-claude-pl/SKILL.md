---
name: type-safety-validation
description: End-to-end type safety with Zod, tRPC, Prisma, and TypeScript 5.7+ patterns. Use when creating Zod schemas, setting up tRPC, validating input, implementing exhaustive switch statements, branded types, or type checking with ty.
context: fork
agent: frontend-ui-developer
version: 1.1.0
author: AI Agent Hub
tags: [typescript, zod, trpc, prisma, type-safety, validation, exhaustive-types, branded-types, 2025]
user-invocable: false
---

# Type Safety & Validation

## Overview

**When to use this skill:**
- Building type-safe APIs (REST, RPC, GraphQL)
- Validating user input and external data
- Ensuring database queries are type-safe
- Creating end-to-end typed full-stack applications
- Implementing strict validation rules

## Core Stack Quick Reference

| Tool | Purpose | Key Pattern |
|------|---------|-------------|
| **Zod** | Runtime validation | `z.object({}).safeParse(data)` |
| **tRPC** | Type-safe APIs | `t.procedure.input(schema).query()` |
| **Prisma** | Type-safe ORM | Auto-generated types from schema |
| **TypeScript 5.7+** | Compile-time safety | `satisfies`, const params, decorators |

## Zod Essentials

```typescript
import { z } from 'zod'

// Define schema
const UserSchema = z.object({
  id: z.string().uuid(),
  email: z.string().email(),
  age: z.number().int().positive().max(120),
  role: z.enum(['admin', 'user', 'guest']),
  createdAt: z.date().default(() => new Date())
})

// Infer TypeScript type
type User = z.infer<typeof UserSchema>

// Validate with error handling
const result = UserSchema.safeParse(data)
if (result.success) {
  const user: User = result.data
} else {
  console.error(result.error.issues)
}
```

**See:** `references/zod-patterns.md` for transforms, refinements, discriminated unions, and recursive types.

## tRPC Essentials

```typescript
import { initTRPC } from '@trpc/server'
import { z } from 'zod'

const t = initTRPC.create()

export const appRouter = t.router({
  getUser: t.procedure
    .input(z.object({ id: z.string() }))
    .query(async ({ input }) => {
      return await db.user.findUnique({ where: { id: input.id } })
    }),

  createUser: t.procedure
    .input(z.object({ email: z.string().email(), name: z.string() }))
    .mutation(async ({ input }) => {
      return await db.user.create({ data: input })
    })
})

export type AppRouter = typeof appRouter
```

**See:** `references/trpc-setup.md` for middleware, authentication, React integration, and error handling.

## Exhaustive Type Checking

```typescript
// ALWAYS use assertNever for compile-time exhaustiveness
function assertNever(x: never): never {
  throw new Error("Unexpected value: " + x)
}

type Status = 'pending' | 'running' | 'completed' | 'failed'

function getStatusColor(status: Status): string {
  switch (status) {
    case 'pending': return 'gray'
    case 'running': return 'blue'
    case 'completed': return 'green'
    case 'failed': return 'red'
    default: return assertNever(status) // Compile-time check!
  }
}

// Exhaustive record mapping
const statusColors = {
  pending: 'gray',
  running: 'blue',
  completed: 'green',
  failed: 'red',
} as const satisfies Record<Status, string>
```

**See:** `references/typescript-advanced.md` for handler objects, type guards, and anti-patterns.

## Branded Types

**TypeScript (with Zod):**
```typescript
const UserId = z.string().uuid().brand<'UserId'>()
const AnalysisId = z.string().uuid().brand<'AnalysisId'>()

type UserId = z.infer<typeof UserId>
type AnalysisId = z.infer<typeof AnalysisId>

function deleteAnalysis(id: AnalysisId): void { ... }
deleteAnalysis(userId) // Error: UserId not assignable to AnalysisId
```

**Python (with NewType):**
```python
from typing import NewType
from uuid import UUID

AnalysisID = NewType("AnalysisID", UUID)
ArtifactID = NewType("ArtifactID", UUID)

def delete_analysis(id: AnalysisID) -> None: ...
delete_analysis(artifact_id)  # Error with mypy/ty
```

**See:** `references/typescript-advanced.md` for factory patterns and pure TypeScript branding.

## Python Type Safety with Ty

```python
from typing import cast

# Type-safe extraction from untyped dict
result = {"findings": {...}, "confidence_score": 0.85}

findings_to_save: dict[str, object] | None = (
    cast("dict[str, object]", result.get("findings"))
    if isinstance(result.get("findings"), dict) else None
)
confidence_to_save: float | None = (
    float(result.get("confidence_score"))
    if isinstance(result.get("confidence_score"), (int, float)) else None
)
```

**See:** `references/ty-type-checker-patterns.md` for mixed numeric handling and nested dict extraction.

## References

| Reference | Content |
|-----------|---------|
| `references/zod-patterns.md` | Schemas, transforms, refinements, unions, recursion, error handling |
| `references/trpc-setup.md` | Server setup, middleware, routers, client integration, subscriptions |
| `references/typescript-5-features.md` | TS 5.0-5.7 features, satisfies, decorators, strict config |
| `references/typescript-advanced.md` | Exhaustive patterns, branded types, type guards |
| `references/ty-type-checker-patterns.md` | Python ty compliance, dict extraction, type narrowing |
| `references/prisma-types.md` | Prisma ORM types, queries, relations |

## Best Practices

### Validation
- Validate at boundaries (API inputs, form submissions, external data)
- Use `.safeParse()` to handle errors gracefully
- Use branded types for IDs (`z.string().brand<'UserId'>()`)

### Type Safety
- Enable `strict: true` in `tsconfig.json`
- Use `noUncheckedIndexedAccess` for safer array access
- Prefer `unknown` over `any`
- **Exhaustive switches**: Always use `assertNever` in default case
- **Exhaustive records**: Use `satisfies Record<UnionType, Value>`

### Performance
- Reuse schemas (don't create inline in hot paths)
- Use `.parse()` for known-good data (faster than `.safeParse()`)
- Use tRPC batching for multiple queries

## Resources

- [Zod Documentation](https://zod.dev)
- [tRPC Documentation](https://trpc.io)
- [Prisma Documentation](https://www.prisma.io/docs)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/handbook/intro.html)

## Related Skills

- `input-validation` - Security-focused validation and sanitization patterns
- `api-design-framework` - REST API design with type-safe contracts
- `fastapi-advanced` - Python backend with Pydantic type validation

## Key Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Runtime Validation | Zod | Best DX, excellent TypeScript inference, composable schemas |
| API Layer | tRPC | End-to-end type safety without code generation |
| Exhaustive Checks | assertNever | Compile-time guarantee for union completeness |
| Branded Types | Zod .brand() | Prevents ID type confusion with minimal overhead |

---

**Skill Version**: 1.2.0
**Last Updated**: 2025-12-27
**Maintained by**: AI Agent Hub Team

## Capability Details

### zod-schemas
**Keywords:** zod, schema, validation, parse, safeParse, infer, refine, transform
**Solves:**
- How do I validate input with Zod?
- Create runtime validation schema
- Infer TypeScript types from Zod
- Transform and refine data with Zod

### exhaustive-types
**Keywords:** exhaustive, assertNever, never assertion, switch exhaustive, compile-time exhaustiveness
**Solves:**
- How do I make switch statements exhaustive?
- Compile-time check for missing union cases
- assertNever pattern for TypeScript

### branded-types
**Keywords:** branded type, type branding, nominal type, NewType, brand, distinct types, id types
**Solves:**
- How do I prevent mixing different ID types?
- Branded types with Zod
- Python NewType for type safety

### trpc
**Keywords:** trpc, type-safe api, procedure, router, mutation, query, middleware
**Solves:**
- How do I set up tRPC?
- Type-safe API calls
- tRPC with React Query

### prisma-types
**Keywords:** prisma, orm, generated types, model, client, payload
**Solves:**
- How do I use Prisma types?
- Type-safe database queries

### typescript-5-features
**Keywords:** typescript 5, const parameters, satisfies, decorators, template literals
**Solves:**
- Use TypeScript 5.x features
- Const type parameters
- Satisfies operator

### ty-type-checker
**Keywords:** ty, rust type checker, strict typing, isinstance, cast, type narrowing
**Solves:**
- How do I make ty type checker pass?
- Extract values from untyped dicts safely
- Type narrowing with isinstance checks