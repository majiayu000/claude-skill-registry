---
name: typescript-strict
# prettier-ignore
description: Use when writing TypeScript with strict mode - covers type definitions, generics, and declaration files
---

# TypeScript Strict Mode Best Practices

## Quick Start

```typescript
// Enable strict in tsconfig.json
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true
  }
}
```

## Core Principles

- **Strict null checks**: Handle `undefined` and `null` explicitly
- **No implicit any**: Always declare types, avoid `any`
- **Readonly by default**: Use `readonly` for immutable data
- **Discriminated unions**: Use type guards with tagged unions

## Type Definition Patterns

### AST Node Types

```typescript
// Discriminated union for AST nodes
type Expr =
  | { type: "NumberLiteral"; value: number }
  | { type: "BinaryExpr"; op: string; left: Expr; right: Expr }
  | { type: "Identifier"; name: string };

// Type guard
function isNumberLiteral(expr: Expr): expr is Extract<Expr, { type: "NumberLiteral" }> {
  return expr.type === "NumberLiteral";
}
```

### Generic Types

```typescript
// Constrained generics
function map<T, U>(arr: readonly T[], fn: (item: T, index: number) => U): U[] {
  return arr.map(fn);
}

// Conditional types
type Unwrap<T> = T extends Promise<infer U> ? U : T;
```

### Declaration Files

```typescript
// module.d.ts
declare module "lea-lang" {
  export function run(code: string): unknown;
  export function parse(code: string): Program;
}
```

## Common Patterns

- Use `unknown` over `any` for safer type narrowing
- Prefer `interface` for extendable types, `type` for unions
- Use `as const` for literal types
- Leverage `satisfies` for type checking without widening

## Reference Files

- [references/generics.md](references/generics.md) - Advanced generic patterns
- [references/type-guards.md](references/type-guards.md) - Type narrowing techniques
