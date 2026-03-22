---
name: strict-typescript
description: >
  Enforce strict TypeScript compiler settings and type narrowing patterns.
  Use when the user creates a new TypeScript project, configures tsconfig.json,
  encounters null/undefined errors, deals with indexed access issues, or asks
  about strict mode, type safety, or narrowing techniques.
---

# Strict TypeScript Configuration

Enforce the strictest TypeScript compiler settings and apply proper type narrowing
to eliminate runtime type errors at compile time.

## When to Use
- Setting up or reviewing tsconfig.json
- Encountering "possibly undefined" or "possibly null" errors
- Accessing objects by dynamic keys or array indices
- Configuring a new TypeScript project from scratch
- Debugging type-related runtime errors

## Core Patterns

### Pattern 1: Essential Strict Settings

Always enable the full strict family plus additional safety flags.

```jsonc
// tsconfig.json
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true,
    "noFallthroughCasesInSwitch": true,
    "noImplicitReturns": true,
    "noPropertyAccessFromIndexSignature": true,
    "forceConsistentCasingInFileNames": true,
    "verbatimModuleSyntax": true
  }
}
```

`strict: true` enables: `strictNullChecks`, `strictFunctionTypes`, `strictBindCallApply`,
`strictPropertyInitialization`, `noImplicitAny`, `noImplicitThis`,
`useUnknownInCatchVariables`, `alwaysStrict`.

### Pattern 2: Safe Indexed Access with noUncheckedIndexedAccess

With `noUncheckedIndexedAccess`, every index signature access returns `T | undefined`.

```typescript
const scores: Record<string, number> = { alice: 95, bob: 87 };

// Without noUncheckedIndexedAccess: score is number (WRONG at runtime)
// With noUncheckedIndexedAccess: score is number | undefined (CORRECT)
const score = scores["charlie"];

// You must narrow before using
if (score !== undefined) {
  console.log(score.toFixed(2)); // safe
}

// Same applies to arrays
const items = ["a", "b", "c"];
const item = items[5]; // string | undefined -- forces you to check
```

### Pattern 3: Type Narrowing Techniques

Use narrowing to convert broad types into specific ones without unsafe casts.

```typescript
// typeof narrowing
function process(value: string | number): string {
  if (typeof value === "string") {
    return value.toUpperCase(); // narrowed to string
  }
  return value.toFixed(2); // narrowed to number
}

// in narrowing
interface Dog { bark(): void }
interface Cat { meow(): void }

function speak(animal: Dog | Cat): void {
  if ("bark" in animal) {
    animal.bark(); // narrowed to Dog
  } else {
    animal.meow(); // narrowed to Cat
  }
}

// instanceof narrowing
function formatError(err: unknown): string {
  if (err instanceof Error) {
    return err.message; // narrowed to Error
  }
  return String(err);
}
```

### Pattern 4: exactOptionalPropertyTypes

Distinguishes between "missing" and "explicitly undefined" properties.

```typescript
interface Config {
  debug?: boolean;
  // With exactOptionalPropertyTypes:
  // debug can be omitted OR set to true/false
  // but NOT set to undefined explicitly
}

// Valid
const a: Config = {};
const b: Config = { debug: true };

// Invalid with exactOptionalPropertyTypes
// const c: Config = { debug: undefined }; // Error!

// Use union with undefined if you need explicit undefined
interface FlexibleConfig {
  debug?: boolean | undefined; // now explicit undefined is allowed
}
```

### Pattern 5: Assertion Functions and Type Predicates

Create reusable narrowing with custom type guards.

```typescript
// Type predicate
function isNonNull<T>(value: T | null | undefined): value is T {
  return value != null;
}

const values = [1, null, 2, undefined, 3];
const clean: number[] = values.filter(isNonNull); // number[]

// Assertion function
function assertDefined<T>(
  value: T | null | undefined,
  name: string
): asserts value is T {
  if (value == null) {
    throw new Error(`Expected ${name} to be defined`);
  }
}

function processUser(id: string | undefined): void {
  assertDefined(id, "id");
  // id is now string -- no need for further checks
  console.log(id.toUpperCase());
}
```

## Anti-Patterns

- **Using `as` to silence errors** -- Type assertions bypass the compiler. Use narrowing instead.
  ```typescript
  // BAD: hiding the problem
  const name = (data as any).user.name;
  // GOOD: validate the shape
  if (data && typeof data === "object" && "user" in data) { ... }
  ```

- **Using the non-null assertion `!`** -- Tells the compiler to trust you, but you might be wrong.
  ```typescript
  // BAD
  const el = document.getElementById("app")!;
  // GOOD
  const el = document.getElementById("app");
  if (!el) throw new Error("Missing #app element");
  ```

- **Disabling strict flags per file with `// @ts-ignore`** -- Fix the types instead of ignoring them.

- **Using `any` instead of `unknown`** -- Prefer `unknown` and narrow. `any` disables type checking entirely.

## Quick Reference

| Flag | What It Catches |
|------|----------------|
| `strictNullChecks` | null/undefined on non-nullable types |
| `noUncheckedIndexedAccess` | Unsafe array/record access |
| `exactOptionalPropertyTypes` | Explicit undefined on optional props |
| `noImplicitAny` | Missing type annotations |
| `useUnknownInCatchVariables` | Untyped catch variables |
| `noPropertyAccessFromIndexSignature` | Forces bracket notation for dynamic keys |

Narrowing priority: `typeof` > `in` > `instanceof` > type predicates > assertion functions.
