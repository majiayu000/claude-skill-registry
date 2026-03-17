---
name: TypeScript Ecosystem
description: This skill should be used when the user asks to "write typescript", "typescript config", "tsconfig", "type definition", "generics", "utility types", or works with TypeScript language patterns and configuration. Provides comprehensive TypeScript ecosystem patterns and best practices.
---

# TypeScript Ecosystem

## Core Concepts

- **Strict mode**: Enable `strict: true` for maximum type safety
- **Module resolution**: `nodenext` for ESM Node.js, `bundler` for Vite/esbuild/webpack
- **Type narrowing**: Use type guards (`typeof`, `instanceof`, `in`, custom predicates)
- **Utility types**: `Partial`, `Required`, `Pick`, `Omit`, `Record`, `Extract`, `Exclude`, `ReturnType`, `Awaited`

## Recommended tsconfig

Node.js 22 LTS (ES2023):
```json
{
  "compilerOptions": {
    "target": "ES2023",
    "lib": ["ES2023"],
    "module": "nodenext",
    "moduleResolution": "nodenext",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,
    "outDir": "./dist",
    "rootDir": "./src"
  },
  "include": ["src"],
  "exclude": ["node_modules", "dist"]
}
```

## Key Strict Options

- `strictNullChecks` - null/undefined handled explicitly
- `noImplicitAny` - Error on implicit any
- `noUncheckedIndexedAccess` - Add undefined to index signatures
- `noUnusedLocals/Parameters` - Error on unused variables

## Type Patterns

### Conditional Types with infer
```typescript
type UnwrapPromise<T> = T extends Promise<infer U> ? U : T;
type ArrayElement<T> = T extends (infer E)[] ? E : never;
```

### Mapped Types with Key Remapping
```typescript
type Getters<T> = {
  [K in keyof T as `get${Capitalize<string & K>}`]: () => T[K];
};
```

### Custom Type Guards
```typescript
function isCat(pet: Cat | Dog): pet is Cat {
  return (pet as Cat).meow !== undefined;
}
```

### Branded Types
```typescript
type UserId = string & { readonly __brand: unique symbol };
type OrderId = string & { readonly __brand: unique symbol };
```

### satisfies Operator
```typescript
const config = {
  endpoint: "/api",
  timeout: 3000,
} satisfies Record<string, string | number>;
// config.endpoint inferred as "/api" (literal), not string
```

## Anti-Patterns

- **any abuse**: Use `unknown` and narrow with type guards
- **Type assertions**: Use type guards instead of excessive `as` casts
- **Enums**: Use `as const` objects instead
- **Namespaces**: Use ES modules
- **Barrel overuse**: Can hurt tree-shaking

## Tools

- `tsc --noEmit` - Type check only
- `tsx` - Run TypeScript directly with esbuild
- ESLint flat config with `typescript-eslint`
- Vitest or Jest for testing

## Context7 Reference

Library ID: `/microsoft/typescript`
