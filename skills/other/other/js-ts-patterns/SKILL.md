---
name: js-ts-patterns
description: Use when creating JS/TS projects, choosing frameworks, or building advanced type patterns. Covers tooling opinions, type decisions, and non-obvious gotchas.
---

# JS/TS Patterns

Tooling opinions, type-level decisions, and non-obvious patterns. Opus knows the basics -- this covers what to choose and when.

## Style Guide

Source: Google JS + TS Style Guides. Only rules linters/formatters cannot enforce.

### Naming
- Treat abbreviations as whole words: `loadHttpUrl` not `loadHTTPURL`
- Single-letter names only within ≤10-line scope
- Never abbreviate by deleting letters: `customerId` not `cstmrId`
- Descriptive over terse: `errorCount` not `errCnt`
- Boolean names: `isVisible`, `hasPermission`, `canEdit`
- Event handlers: `onEventName` pattern (`onClick`, `onSubmit`)
- Test methods: `testX_whenY_doesZ` for structured names
- `CONSTANT_CASE` only for deeply immutable module-level values, not local `const`

### Practices
- Named exports only — no default exports
- Prefer `interface` over `type` for object shapes
- Avoid type assertions (`as`); use runtime checks
- Catch errors as `unknown`, assert `Error` type
- `== null` is the one acceptable `==` (catches null + undefined)
- Function declarations at module level, arrow functions for callbacks
- No getters/setters unless framework-required
- Modules for namespacing, not static-only container classes

## Tooling Defaults

| Concern | Use | Why |
|---------|-----|-----|
| Package manager | `pnpm` | Faster, disk-efficient, strict by default |
| Bundler | `Vite` (apps), `tsup` (libs) | Fast, sensible defaults |
| Test runner | `Vitest` | Vite-native, Jest-compatible API |
| Linter | `ESLint` + `@typescript-eslint` | Catches real bugs |
| Formatter | Biome or Prettier | Opinionated, zero config |
| Runtime (scripts) | `tsx` | TS execution without build step |

## Project Types

| Type | When | Init |
|------|------|------|
| **Next.js** | Full-stack React, SSR/SSG | `pnpm create next-app@latest` |
| **React + Vite** | SPA, component libs | `pnpm create vite . --template react-ts` |
| **Node.js API** | Express/Fastify backends | Manual setup with tsx |
| **Library** | NPM packages | tsup for bundling |
| **CLI** | Command-line tools | `commander` or `yargs` |

## TypeScript Config Opinions

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "paths": { "@/*": ["./src/*"] }
  }
}
```

- **Always `strict: true`** -- no exceptions
- **`moduleResolution: "bundler"`** for apps (Vite/Next), `"node16"` for libraries
- **`skipLibCheck: true`** -- speeds up compilation, rarely hides real bugs
- **`"type": "module"`** in package.json for all new projects

## Advanced Type Patterns

### When to Reach for Advanced Types

| Need | Pattern |
|------|---------|
| Type-safe events | `Record<EventName, Payload>` + generic `on`/`emit` |
| Typed API client | Mapped type over endpoint config |
| State machines | Discriminated unions + exhaustive switch |
| Deep immutability | Recursive `DeepReadonly<T>` |
| Config paths | Template literal recursion: `"server.host"` |

### Discriminated Unions (most underused pattern)

```typescript
type Result<T> =
  | { status: 'success'; data: T }
  | { status: 'error'; error: string }
  | { status: 'loading' };

// Compiler enforces all cases
function handle<T>(r: Result<T>) {
  switch (r.status) {
    case 'success': return r.data;
    case 'error': throw new Error(r.error);
    case 'loading': return null;
  }
}
```

### Key Remapping

```typescript
type Getters<T> = {
  [K in keyof T as `get${Capitalize<string & K>}`]: () => T[K]
};

type PickByType<T, U> = {
  [K in keyof T as T[K] extends U ? K : never]: T[K]
};
```

### `infer` Patterns

```typescript
type ElementOf<T> = T extends (infer U)[] ? U : never;
type Awaited<T> = T extends Promise<infer U> ? Awaited<U> : T;
type ReturnOf<T> = T extends (...args: any[]) => infer R ? R : never;
```

### Branded Types (nominal typing)

```typescript
type UserId = string & { __brand: 'UserId' };
type OrderId = string & { __brand: 'OrderId' };

function getUser(id: UserId) { /* ... */ }
// getUser("abc")          -- compile error
// getUser("abc" as UserId) -- ok
```

### Type Testing

```typescript
type AssertEqual<T, U> = [T] extends [U] ? [U] extends [T] ? true : false : false;
type _test1 = AssertEqual<string, string>;  // true
type _test2 = AssertEqual<string, number>;  // false
```

## Runtime Patterns

### Library package.json

```json
{
  "type": "module",
  "main": "./dist/index.js",
  "types": "./dist/index.d.ts",
  "exports": {
    ".": { "import": "./dist/index.js", "types": "./dist/index.d.ts" }
  },
  "files": ["dist"],
  "scripts": {
    "build": "tsup src/index.ts --format esm --dts",
    "prepublishOnly": "pnpm build"
  }
}
```

### Type Guards (prefer over assertions)

```typescript
function isString(v: unknown): v is string { return typeof v === 'string'; }

// Assertion function (narrows in-place)
function assertDefined<T>(v: T | undefined): asserts v is T {
  if (v === undefined) throw new Error('undefined');
}
```

## Framework Decisions

### Express vs Fastify

| | Express | Fastify |
|-|---------|---------|
| **Speed** | Baseline | ~2x faster |
| **TypeScript** | Bolted-on types | First-class |
| **Schema validation** | Manual/middleware | Built-in (Ajv) |
| **Ecosystem** | Massive | Growing |
| **Choose when** | Team knows it | New projects |

### Zod vs Joi vs class-validator

| | Zod | Joi | class-validator |
|-|-----|-----|-----------------|
| **TS inference** | Native | None | None |
| **Style** | Functional | Chaining | Decorators |
| **Choose when** | Default choice | Legacy JS | NestJS |

### `type` vs `interface`

| Use `interface` | Use `type` |
|-----------------|------------|
| Object shapes | Unions, intersections |
| Extendable contracts | Mapped/conditional types |
| Better error messages | Complex type algebra |

Rule: start with `interface`, switch to `type` when you need union/conditional.

## Gotchas

- **`any` defeats the type system** -- use `unknown` and narrow
- **Avoid `enum`** -- use `as const` objects or union types (better tree-shaking)
- **`satisfies`** preserves literal types while checking: `const x = { a: 1 } satisfies Record<string, number>`
- **`interface` extends > `type &`** -- intersections can produce `never` silently
- **Deeply nested conditional types** slow tsc -- flatten when possible
- **Circular type references** crash tsc -- break cycles with intermediate types
- **`as const`** to preserve literal types in arrays/objects
