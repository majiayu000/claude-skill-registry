---
name: typecheck
description: TypeScript type-safety rules and guidance.
---

# Typecheck Skill

Use this skill when handling TypeScript type errors or type-safety decisions.

## Core Rule: Never Use `as any`

**CRITICAL**: NEVER add `as any` type assertions to fix TypeScript errors. If you
cannot figure out a proper type-safe solution, tell the user that you can't
figure it out rather than using `as any`.

## Rationale

Using `as any`:
- Disables type checking, removing TypeScript's safety guarantees
- Hides actual type problems that should be addressed properly
- Makes the codebase more error-prone and harder to maintain
- Is a code smell that indicates deeper type design issues

## What to Do Instead

1. **Investigate the root cause**: Understand why TypeScript can't infer the
   correct type
2. **Use proper type narrowing**: Use type guards, conditional types, or better
   type constraints
3. **Fix the type definitions**: Update interfaces, generics, or type utilities
   if needed
4. **Ask for help**: If you truly cannot solve it type-safely, inform the user
   that you cannot figure out a proper solution

## When Encountering Type Errors

- ✅ **DO**: Analyze the error message carefully to understand the type mismatch
- ✅ **DO**: Check if helper types or type utilities can resolve it
- ✅ **DO**: Consider if the API or type definitions need improvement
- ✅ **DO**: Tell the user if you cannot find a type-safe solution

- ❌ **DON'T**: Add `as any` to silence the error
- ❌ **DON'T**: Use `as unknown as T` as a workaround (same problem as `as any`)
- ❌ **DON'T**: Use `@ts-ignore` or `@ts-expect-error` to suppress type errors

## Examples of What NOT to Do

```typescript
// ❌ WRONG - Never do this
const rows = yield* db
  .select()
  .from(pgTable as any)
  .where(eq(pgTable.id, id));
```

```typescript
// ❌ WRONG - This is also bad
const value = someValue as unknown as ExpectedType;
```

## When You Cannot Solve It Type-Safely

If after careful analysis you cannot find a type-safe solution, you should:

1. Explain what the type error is
2. Describe what you tried
3. State clearly that you cannot figure out a proper type-safe solution
4. Suggest potential approaches (better type definitions, helper utilities,
   etc.)

**Example response**:
> "I'm encountering a TypeScript error where `pgTable` from `models[modelName]`
> cannot be properly narrowed for use in Drizzle's `.from()` method. The complex
> generic types from `InferAggregateModels` are preventing proper type
> inference. I've tried [X, Y, Z approaches] but cannot find a type-safe
> solution. This likely requires improving the type definitions for the table
> mapping or using a different pattern for accessing tables. I cannot figure out
> a proper type-safe fix for this."
