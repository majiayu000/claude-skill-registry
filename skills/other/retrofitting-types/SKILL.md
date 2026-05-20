---
name: retrofitting-types
description: Add types to untyped code gradually without breaking functionality
category: Code Quality
---

# Skill: retrofitting-types

## What I do

I help you add type safety to existing JavaScript or other untyped codebases. I focus on an incremental approach that enhances code quality without requiring a complete rewrite. I ensure that you can transition your project to TypeScript safely and effectively.

## When to use me

- When you're migrating a JavaScript project to TypeScript.
- When you're adding types to an existing API or library.
- When you're trying to improve code readability and maintainability.
- When you're working with legacy code that has many untyped variables or functions.

## Core principles

1. **Incremental typing**, add types at module boundaries first to get the most immediate benefit.
2. **Strictness as a goal**, start with a permissive configuration and gradually enable stricter rules.
3. **Avoid any**, use `unknown` or more specific types to catch real errors.
4. **Leverage inference**, let the type system infer types when possible to reduce boilerplate.

## Patterns & examples

### Boundary typing
Focus on function signatures and external API calls.
- **Pattern**, Define an interface for the incoming data and the return value of a function.

### TypeScript migration path
Follow a step-by-step approach to add types.
- **Step 1**, Enable `allowJs` and `checkJs` in your `tsconfig.json`.
- **Step 2**, Add `@ts-check` to the top of your JavaScript files.
- **Step 3**, Gradually rename files to `.ts` and add explicit types.

### Using unknown over any
Provide more safety when the type is truly unknown.
```typescript
function processData(input: unknown) {
    if (typeof input === 'string') {
        console.log(input.toUpperCase());
    }
}
```

### Type definitions for 3rd-party JS
Create custom `.d.ts` files for libraries that lack them.
- **Action**, Define the main functions and objects exported by the library.

## Anti-patterns to avoid

- ❌ **Type assertion abuse**, using `as Type` too frequently to silence compiler errors.
- ❌ **Excessive any usage**, using `any` everywhere defeats the purpose of adding types.
- ❌ **The "Rewrite" trap**, attempting to rewrite the whole codebase at once instead of incremental improvement.
- ❌ **Ignoring inference**, manually typing every single variable even when the compiler can infer them.

## KB Reference

`~/vaults/baphled/3. Resources/Knowledge Base/AI Development System/Skills/Code-Quality/Retrofitting Types.md`

## Related skills

- `javascript`, for the core language expertise.
- `clean-code`, for maintaining high quality during the transition.
- `refactor`, for restructuring code to be more type-friendly.
- `static-analysis`, for finding issues during the migration.
