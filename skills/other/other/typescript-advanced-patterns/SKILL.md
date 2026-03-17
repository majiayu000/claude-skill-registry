---
name: typescript-advanced-patterns
description: Advanced TypeScript patterns for type-safe, maintainable code using sophisticated type system features. Use when building type-safe APIs, implementing complex domain models, or leveraging TypeScript's advanced type capabilities.
---

# TypeScript Advanced Patterns

Expert guidance for leveraging TypeScript's advanced type system features to build robust, type-safe applications with sophisticated type inference, compile-time guarantees, and maintainable domain models.

## When to Use This Skill

- Building type-safe APIs with strict contracts and validation
- Implementing complex domain models with compile-time enforcement
- Creating reusable libraries with sophisticated type inference
- Enforcing business rules through the type system
- Building type-safe state machines and builders
- Developing framework integrations requiring advanced types
- Implementing runtime validation with type-level guarantees

## Core Concepts

TypeScript's type system enables compile-time safety through:

1. **Conditional Types**: Type selection based on conditions (type-level if/else)
2. **Mapped Types**: Transform object types systematically (Partial, Readonly, Pick, Omit)
3. **Template Literal Types**: String manipulation at compile time
4. **Type Guards**: Runtime checking with type narrowing (`value is Type`)
5. **Discriminated Unions**: Type-safe state machines with exhaustiveness checking
6. **Branded Types**: Nominal types for preventing primitive mixing
7. **Builder Pattern**: Type-safe fluent APIs with progressive type constraints
8. **Advanced Generics**: Constraints, inference, and higher-kinded type patterns
9. **Utility Types**: Deep transformations and compositions
10. **Type Inference**: Const assertions and contextual typing

## Quick Reference

Load detailed references on-demand:

| Topic | Reference File |
|-------|----------------|
| Conditional Types | `skills/typescript-advanced-patterns/references/conditional-types.md` |
| Mapped Types | `skills/typescript-advanced-patterns/references/mapped-types.md` |
| Template Literal Types | `skills/typescript-advanced-patterns/references/template-literal-types.md` |
| Type Guards | `skills/typescript-advanced-patterns/references/type-guards.md` |
| Discriminated Unions | `skills/typescript-advanced-patterns/references/discriminated-unions.md` |
| Branded Types | `skills/typescript-advanced-patterns/references/branded-types.md` |
| Builder Pattern | `skills/typescript-advanced-patterns/references/builder-pattern.md` |
| Advanced Generics | `skills/typescript-advanced-patterns/references/advanced-generics.md` |
| Utility Types | `skills/typescript-advanced-patterns/references/utility-types.md` |
| Type Inference | `skills/typescript-advanced-patterns/references/type-inference.md` |
| Decorators | `skills/typescript-advanced-patterns/references/decorators.md` |
| Performance Best Practices | `skills/typescript-advanced-patterns/references/performance-best-practices.md` |
| Common Pitfalls | `skills/typescript-advanced-patterns/references/common-pitfalls.md` |
| Testing Types | `skills/typescript-advanced-patterns/references/testing-types.md` |

## Implementation Workflow

### 1. Identify Pattern Need
- Analyze type safety requirements
- Identify runtime vs compile-time constraints
- Choose appropriate pattern from Quick Reference

### 2. Load Reference
- Read specific reference file for pattern
- Review examples and use cases
- Understand trade-offs

### 3. Implement Pattern
- Start simple, add complexity as needed
- Use strict mode (`tsconfig.json` with `"strict": true`)
- Test with type assertions

### 4. Validate
- Ensure type errors caught at compile time
- Verify runtime behavior matches types
- Check performance (avoid excessive type complexity)

### 5. Document
- Add JSDoc comments for public APIs
- Document type constraints and assumptions
- Provide usage examples

## Common Mistakes to Avoid

1. **Using `any` instead of `unknown`**: Loses all type safety
   - Use `unknown` and type guards instead

2. **Type assertions without validation**: Unsafe runtime behavior
   - Prefer type guards (`value is Type`) over `as Type`

3. **Overusing generics**: Unnecessary complexity
   - Only use generics when types truly vary

4. **Deep type nesting**: Slow compilation, hard to debug
   - Keep types composable and shallow

5. **Forgetting `readonly`**: Accidental mutations
   - Mark immutable data structures as `readonly`

6. **Not enabling strict mode**: Missing null checks and type errors
   - Always use `"strict": true` in `tsconfig.json`

7. **Mixing type and interface incorrectly**: Confusing semantics
   - Use `type` for unions/utilities, `interface` for object shapes

## Quick Patterns

### Type-Safe ID
```typescript
type UserId = string & { readonly __brand: 'UserId' };
function createUserId(id: string): UserId { return id as UserId; }
```

### Discriminated Union
```typescript
type State =
  | { status: 'loading' }
  | { status: 'success'; data: string }
  | { status: 'error'; error: Error };
```

### Mapped Type Transformation
```typescript
type Readonly<T> = { readonly [P in keyof T]: T[P] };
type Partial<T> = { [P in keyof T]?: T[P] };
```

### Type Guard
```typescript
function isString(value: unknown): value is string {
  return typeof value === 'string';
}
```

## Resources

- **TypeScript Handbook**: https://www.typescriptlang.org/docs/handbook/
- **Type Challenges**: https://github.com/type-challenges/type-challenges
- **ts-toolbelt**: Advanced type utilities library
- **zod**: Runtime validation with TypeScript inference
- **tsd**: Test TypeScript type definitions
