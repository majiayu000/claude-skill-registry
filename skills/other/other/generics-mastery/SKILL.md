---
name: generics-mastery
description: >
  Master TypeScript generics for reusable, type-safe abstractions.
  Use when the user works with generic constraints, conditional types, mapped
  types, the infer keyword, utility types, recursive types, or needs help
  building type-safe libraries, APIs, or data structures.
---

# TypeScript Generics Mastery

Build powerful, reusable type abstractions with generics. Generics let you write
code that works across types while preserving full type safety.

## When to Use
- Creating reusable functions, classes, or data structures
- Building type-safe wrappers or middleware
- Transforming object shapes (pick, omit, remap keys)
- Extracting types from complex structures with infer
- Designing library-grade APIs with flexible type parameters

## Core Patterns

### Pattern 1: Generic Constraints

Constrain type parameters to ensure they have required properties.

```typescript
// Basic constraint
function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key];
}

const user = { name: "Alice", age: 30 };
const name = getProperty(user, "name"); // string
// getProperty(user, "email"); // Compile error

// Constraint with interface
interface HasId {
  id: string;
}

function findById<T extends HasId>(items: readonly T[], id: string): T | undefined {
  return items.find((item) => item.id === id);
}

// Multiple constraints
function merge<T extends object, U extends object>(a: T, b: U): T & U {
  return { ...a, ...b };
}
```

### Pattern 2: Conditional Types

Types that choose a branch based on a condition, like a type-level ternary.

```typescript
// Basic conditional
type IsString<T> = T extends string ? true : false;
type A = IsString<"hello">; // true
type B = IsString<42>;      // false

// Distributive conditional types (distributes over unions)
type NonNullable<T> = T extends null | undefined ? never : T;
type C = NonNullable<string | null | undefined>; // string

// Extract and Exclude
type Extract<T, U> = T extends U ? T : never;
type Exclude<T, U> = T extends U ? never : T;

type Numbers = Extract<string | number | boolean, number>; // number
type WithoutBool = Exclude<string | number | boolean, boolean>; // string | number

// Conditional return types
function process<T extends string | number>(
  value: T
): T extends string ? string[] : number {
  if (typeof value === "string") {
    return value.split("") as T extends string ? string[] : number;
  }
  return (value * 2) as T extends string ? string[] : number;
}
```

### Pattern 3: Mapped Types

Transform every property of an existing type.

```typescript
// Make all properties optional
type Partial<T> = { [K in keyof T]?: T[K] };

// Make all properties required
type Required<T> = { [K in keyof T]-?: T[K] };

// Make all properties readonly
type Readonly<T> = { readonly [K in keyof T]: T[K] };

// Remap keys with `as`
type Getters<T> = {
  [K in keyof T as `get${Capitalize<string & K>}`]: () => T[K];
};

interface Person { name: string; age: number }
type PersonGetters = Getters<Person>;
// { getName: () => string; getAge: () => number }

// Filter properties by value type
type PickByType<T, V> = {
  [K in keyof T as T[K] extends V ? K : never]: T[K];
};

type StringProps = PickByType<Person, string>;
// { name: string }
```

### Pattern 4: The infer Keyword

Extract types from inside other types within conditional type clauses.

```typescript
// Extract return type
type ReturnType<T> = T extends (...args: any[]) => infer R ? R : never;
type R = ReturnType<() => string>; // string

// Extract promise value
type Awaited<T> = T extends Promise<infer U> ? Awaited<U> : T;
type V = Awaited<Promise<Promise<number>>>; // number

// Extract array element
type ElementOf<T> = T extends readonly (infer E)[] ? E : never;
type E = ElementOf<string[]>; // string

// Extract function parameters
type FirstParam<T> = T extends (first: infer F, ...rest: any[]) => any ? F : never;
type P = FirstParam<(name: string, age: number) => void>; // string

// Infer from template literals
type ParseRoute<T extends string> =
  T extends `${infer _Start}:${infer Param}/${infer Rest}`
    ? Param | ParseRoute<Rest>
    : T extends `${infer _Start}:${infer Param}`
      ? Param
      : never;

type Params = ParseRoute<"/users/:userId/posts/:postId">;
// "userId" | "postId"
```

### Pattern 5: Utility Types in Practice

Combine built-in and custom utility types for real-world scenarios.

```typescript
// Updatable entity: id is required and readonly, rest is partial
type Updatable<T extends { id: string }> = Readonly<Pick<T, "id">> &
  Partial<Omit<T, "id">>;

interface User {
  id: string;
  name: string;
  email: string;
  role: "admin" | "user";
}

type UserUpdate = Updatable<User>;
// { readonly id: string; name?: string; email?: string; role?: "admin" | "user" }

// Deep partial
type DeepPartial<T> = T extends object
  ? { [K in keyof T]?: DeepPartial<T[K]> }
  : T;

// StrictOmit that validates the key exists
type StrictOmit<T, K extends keyof T> = Omit<T, K>;

// Record with specific keys
type ApiEndpoints = Record<"getUser" | "listUsers" | "createUser", string>;
```

### Pattern 6: Recursive Types

Types that reference themselves for tree structures and deep transformations.

```typescript
// JSON type
type Json =
  | string
  | number
  | boolean
  | null
  | Json[]
  | { [key: string]: Json };

// Tree structure
interface TreeNode<T> {
  value: T;
  children: ReadonlyArray<TreeNode<T>>;
}

// Deep readonly
type DeepReadonly<T> = T extends (infer E)[]
  ? ReadonlyArray<DeepReadonly<E>>
  : T extends object
    ? { readonly [K in keyof T]: DeepReadonly<T[K]> }
    : T;

// Path type for nested access
type Path<T, K extends keyof T = keyof T> = K extends string
  ? T[K] extends object
    ? K | `${K}.${Path<T[K]>}`
    : K
  : never;

interface Config {
  db: { host: string; port: number };
  cache: { ttl: number };
}
type ConfigPath = Path<Config>; // "db" | "cache" | "db.host" | "db.port" | "cache.ttl"
```

## Anti-Patterns

- **Over-generic code** -- Do not add type parameters when a concrete type suffices. Generics
  add cognitive load; use them only when you need reuse across multiple types.
  ```typescript
  // BAD: unnecessary generic
  function greet<T extends string>(name: T): string { return `Hi ${name}`; }
  // GOOD: concrete type
  function greet(name: string): string { return `Hi ${name}`; }
  ```

- **Using `any` as a constraint** -- Prefer `unknown` or a specific interface. `extends any`
  provides no safety.

- **Deeply nested conditional types** -- If a conditional type needs more than 3 levels of
  nesting, consider breaking it into named helper types for readability.

- **Ignoring distributive behavior** -- Conditional types distribute over unions by default.
  Wrap in `[T]` to prevent distribution when you need to treat the union as a whole:
  ```typescript
  type IsUnion<T> = [T] extends [infer U] ? ([U] extends [T] ? false : true) : never;
  ```

## Quick Reference

| Concept | Syntax | Purpose |
|---------|--------|---------|
| Constraint | `T extends U` | Limit what T can be |
| Conditional | `T extends U ? A : B` | Branch on type |
| Mapped | `{ [K in keyof T]: ... }` | Transform all props |
| Key remapping | `as` in mapped types | Rename/filter keys |
| infer | `T extends F<infer U>` | Extract inner type |
| Recursive | Self-referencing type | Trees, deep transforms |
| Distributive | Default on naked T | Applies to each union member |
