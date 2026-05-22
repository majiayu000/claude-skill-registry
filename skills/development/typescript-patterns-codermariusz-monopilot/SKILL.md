---
name: typescript-patterns
description: Apply when writing TypeScript code requiring type safety, utility types, discriminated unions, or generic patterns.
version: 1.0.0
tokens: ~800
confidence: high
sources:
  - https://www.typescriptlang.org/docs/handbook/2/types-from-types.html
  - https://www.typescriptlang.org/docs/handbook/utility-types.html
last_validated: 2025-01-10
next_review: 2025-01-24
tags: [typescript, patterns, types]
---

## When to Use

Apply when writing TypeScript code requiring type safety, utility types, discriminated unions, or generic patterns.

## Patterns

### Pattern 1: Discriminated Unions
```typescript
// Source: https://www.typescriptlang.org/docs/handbook/2/narrowing.html
type Result<T> =
  | { success: true; data: T }
  | { success: false; error: string };

function handle<T>(result: Result<T>) {
  if (result.success) {
    console.log(result.data); // T - narrowed
  } else {
    console.log(result.error); // string - narrowed
  }
}
```

### Pattern 2: Utility Types
```typescript
// Source: https://www.typescriptlang.org/docs/handbook/utility-types.html
interface User {
  id: string;
  name: string;
  email: string;
}

type CreateUser = Omit<User, 'id'>;           // { name, email }
type UpdateUser = Partial<Omit<User, 'id'>>;  // { name?, email? }
type UserKeys = keyof User;                    // 'id' | 'name' | 'email'
type ReadonlyUser = Readonly<User>;           // all props readonly
```

### Pattern 3: Generic Constraints
```typescript
// Source: https://www.typescriptlang.org/docs/handbook/2/generics.html
function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key];
}

const user = { name: 'John', age: 30 };
const name = getProperty(user, 'name'); // string
```

### Pattern 4: Type Guards
```typescript
// Source: https://www.typescriptlang.org/docs/handbook/2/narrowing.html
function isString(value: unknown): value is string {
  return typeof value === 'string';
}

function process(value: unknown) {
  if (isString(value)) {
    console.log(value.toUpperCase()); // value is string
  }
}
```

### Pattern 5: Mapped Types
```typescript
// Source: https://www.typescriptlang.org/docs/handbook/2/mapped-types.html
type Getters<T> = {
  [K in keyof T as `get${Capitalize<string & K>}`]: () => T[K];
};

interface Person { name: string; age: number; }
type PersonGetters = Getters<Person>;
// { getName: () => string; getAge: () => number; }
```

### Pattern 6: const Assertions
```typescript
// Source: https://www.typescriptlang.org/docs/handbook/release-notes/typescript-3-4.html
const routes = ['home', 'about', 'contact'] as const;
type Route = typeof routes[number]; // 'home' | 'about' | 'contact'

const config = { env: 'prod', port: 3000 } as const;
// { readonly env: 'prod'; readonly port: 3000; }
```

## Anti-Patterns

- **`any` type** - Use `unknown` and narrow with type guards
- **Type assertions (`as`)** - Prefer type guards for runtime safety
- **Overly complex generics** - Simplify; readability > cleverness
- **Missing `strict` mode** - Enable in tsconfig.json

## Verification Checklist

- [ ] `strict: true` in tsconfig.json
- [ ] No `any` without justification
- [ ] Type guards for runtime checks
- [ ] Utility types used over manual definitions
- [ ] Generics have constraints where needed
