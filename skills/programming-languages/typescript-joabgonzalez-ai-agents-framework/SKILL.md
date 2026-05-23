---
name: typescript
description: "TypeScript best practices with strict typing for type-safe development. Avoid any, use unknown, leverage generics and utility types. Trigger: When implementing or refactoring TypeScript in .ts/.tsx files, adding types/interfaces, or enforcing type safety."
skills:
  - conventions
  - javascript
dependencies:
  typescript: ">=5.0.0 <6.0.0"
allowed-tools:
  - documentation-reader
  - web-search
---

# TypeScript Skill

## Overview

Comprehensive TypeScript guidance with focus on strict typing, type safety, and modern TypeScript features.

## Objective

Enable developers to write type-safe code with proper TypeScript patterns, avoiding `any`, and leveraging advanced type features.

---

## When to Use

Use this skill when:

- Writing or refactoring TypeScript code in .ts or .tsx files
- Adding type definitions, interfaces, or type aliases
- Enforcing type safety and strict typing
- Working with generics, utility types, or advanced type features
- Configuring tsconfig.json
- Resolving type errors or improving type inference

Don't use this skill for:

- Runtime validation (use zod or yup skills)
- JavaScript-only patterns (use javascript skill)
- Framework-specific typing (delegate to react, mui, etc.)

---

## 📚 Extended Mandatory Read Protocol

**This skill has a `references/` directory with detailed guides for utility types, generics, and advanced TypeScript features.**

### Reading Rules

**Read references/ when:**

- **MUST read [utility-types.md](references/utility-types.md)** when:
  - Transforming types (Partial, Pick, Omit, etc.)
  - Need overview of 30+ built-in utilities
  - Avoiding manual type definitions

- **MUST read [generics-advanced.md](references/generics-advanced.md)** when:
  - Creating reusable generic functions/components
  - Working with conditional types or infer keyword
  - Building mapped types

- **MUST read [type-guards.md](references/type-guards.md)** when:
  - Runtime type checking
  - Narrowing union types
  - Creating user-defined type guards

- **MUST read [config-patterns.md](references/config-patterns.md)** when:
  - Setting up new TypeScript project
  - Configuring tsconfig.json
  - Enabling strict mode

- **CHECK [error-handling.md](references/error-handling.md)** when:
  - Implementing type-safe error handling
  - Using Result/Either patterns

**Quick reference only:** Use this SKILL.md for basic patterns and quick decisions. Decision Tree below directs you to specific references.

### Reading Priority

| Situation                    | Read This                           | Why                            |
| ---------------------------- | ----------------------------------- | ------------------------------ |
| Type transformation          | **utility-types.md** (REQUIRED)     | 30+ utilities documented       |
| Generic functions/components | **generics-advanced.md** (REQUIRED) | Constraints, conditional types |
| Runtime validation           | **type-guards.md** (REQUIRED)       | Type narrowing patterns        |
| Project setup                | **config-patterns.md** (REQUIRED)   | Strict mode, module resolution |
| Error handling               | **error-handling.md** (CHECK)       | Result patterns                |

**See [references/README.md](references/README.md)** for complete navigation guide.

---

## Critical Patterns

### ❌ NEVER: Use `any` Type

```typescript
// ❌ WRONG: Disables type checking
function process(data: any) {
  return data.value; // No type safety
}

// ✅ CORRECT: Use unknown with type guards
function process(data: unknown) {
  if (typeof data === "object" && data !== null && "value" in data) {
    return (data as { value: string }).value;
  }
  throw new Error("Invalid data");
}
```

### ✅ REQUIRED: Enable Strict Mode

```json
// tsconfig.json
{
  "compilerOptions": {
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "strictFunctionTypes": true
  }
}
```

### ✅ REQUIRED: Use Proper Type for Object Shapes

```typescript
// ✅ CORRECT: Interface for extensible objects
interface User {
  id: number;
  name: string;
}

// ✅ CORRECT: Type alias for unions/intersections
type Status = "pending" | "approved" | "rejected";
type UserWithStatus = User & { status: Status };

// ❌ WRONG: Empty object type (too permissive)
const user: {} = { anything: "allowed" };
```

### ✅ REQUIRED: Generic Constraints

```typescript
// ✅ CORRECT: Constrained generic
function getProperty<T extends object, K extends keyof T>(
  obj: T,
  key: K,
): T[K] {
  return obj[key];
}

// ❌ WRONG: Unconstrained generic (too permissive)
function getProperty<T>(obj: T, key: string): any {
  return obj[key]; // No type safety
}
```

### ✅ REQUIRED: Use import type for Type-Only Imports

```typescript
// ✅ CORRECT: Type-only imports (better tree-shaking)
import type { User, Product } from "./types";
import { fetchUser } from "./api";

// ❌ WRONG: Mixed imports (prevents tree-shaking)
import { User, Product, fetchUser } from "./api";
```

### ✅ REQUIRED: Use satisfies for Type Validation

```typescript
// ✅ CORRECT: satisfies validates without widening type
const config = {
  endpoint: "/api/users",
  timeout: 5000,
} satisfies Config;

// Type is inferred as { endpoint: string, timeout: number }
// But validated against Config interface

// ❌ WRONG: Type annotation widens type
const config: Config = {
  endpoint: "/api/users",
  timeout: 5000,
};
// Type is Config (wider than needed)
```

### ✅ REQUIRED: Use as const for Literal Types

```typescript
// ✅ CORRECT: as const for literal inference
const ROUTES = {
  HOME: "/",
  ABOUT: "/about",
} as const;

type Route = (typeof ROUTES)[keyof typeof ROUTES]; // '/' | '/about'

// ❌ WRONG: Without as const (type is string)
const ROUTES = {
  HOME: "/",
  ABOUT: "/about",
};
type Route = (typeof ROUTES)[keyof typeof ROUTES]; // string (too wide)
```

---

## Conventions

Refer to conventions for:

- Code organization
- Naming patterns

Refer to javascript for:

- Modern JavaScript features
- Async patterns

### TypeScript Specific

- Enable strict mode in tsconfig.json
- Avoid `any` type - use `unknown` when type is uncertain
- Use interfaces for object shapes
- Use type aliases for unions and intersections
- Leverage generics for reusable components
- Use utility types (Partial, Pick, Omit, etc.)
- **Use `import type` for type-only imports** (enables better tree-shaking)
- Prefer `interface` over `type` for object shapes (better error messages, extensibility)
- Use `as const` for literal type inference
- Use `satisfies` operator (TS 4.9+) to validate types without widening

## Decision Tree

**Need runtime validation?** → Use zod or yup for runtime schema validation. TypeScript handles compile-time only.

**Transforming types?** → **MUST read [utility-types.md](references/utility-types.md)** for Partial, Pick, Omit, Record, Required, Readonly, Exclude, Extract, NonNullable, ReturnType, and 20+ more utilities.

**Dealing with unknown data?** → Use `unknown` type, never `any`. **MUST read [type-guards.md](references/type-guards.md)** for narrowing with typeof, instanceof, user-defined guards.

**Third-party types missing?** → Install @types/\* packages or declare custom types in `types/` directory.

**Complex object shape?** → Use interface for extensibility, type alias for unions/intersections/computed types.

**Reusable logic with different types?** → **MUST read [generics-advanced.md](references/generics-advanced.md)** for generic constraints, conditional types, mapped types.

**Need type transformation?** → **MUST read [utility-types.md](references/utility-types.md)** instead of manual definitions.

**External API response?** → Define interface from actual response shape. Use tools like quicktype for generation.

**Setting up new project?** → **MUST read [config-patterns.md](references/config-patterns.md)** for strict mode, module resolution, path mapping.

**Type-safe error handling?** → **CHECK [error-handling.md](references/error-handling.md)** for Result patterns, error unions.

## Example

```typescript
interface User {
  id: number;
  name: string;
  email: string;
}

type UserUpdate = Partial<Pick<User, "name" | "email">>;

function updateUser<T extends User>(user: T, updates: UserUpdate): T {
  return { ...user, ...updates };
}

const result: User = updateUser(
  { id: 1, name: "John", email: "john@example.com" },
  { name: "Jane" },
);
```

---

## Edge Cases

**Type narrowing in unions:** Use discriminated unions with literal types for better type narrowing:

```typescript
type Result =
  | { success: true; data: string }
  | { success: false; error: Error };

function handle(result: Result) {
  if (result.success) {
    console.log(result.data); // TypeScript knows data exists
  }
}
```

**Circular type references:** Break circular dependencies by extracting shared interfaces or using type parameters.

**Index signatures:** Use `Record<string, Type>` for dynamic keys. For known keys with dynamic values, use mapped types.

**Const assertions:** Use `as const` for literal types: `const config = { mode: 'development' } as const;` creates `{ readonly mode: 'development' }` not `{ mode: string }`.

**Type guards:** Create custom type guards with `is` keyword:

```typescript
function isUser(value: unknown): value is User {
  return typeof value === "object" && value !== null && "id" in value;
}
```

---

## References

- https://www.typescriptlang.org/docs/
- https://www.typescriptlang.org/tsconfig
