---
name: strict-typescript-mode
description: Enforces TypeScript best practices when writing code. Automatically enables strict typing for TypeScript projects, prevents `any` usage, and recommends generic constraints. Activate on TS/TSX files, new features, code reviews.
---

# Strict TypeScript Mode

This skill enforces TypeScript best practices based on the State-of-the-Art Guide 2025.

## When to Activate

- When working with `.ts` or `.tsx` files
- On new feature implementations
- During code reviews
- When refactoring JavaScript to TypeScript

## Strict Rules

### 1. NEVER use `any` without documentation

```typescript
// FORBIDDEN
function process(data: any) { ... }

// ALLOWED (with justification)
// eslint-disable-next-line @typescript-eslint/no-explicit-any
// Reason: External API returns untyped data, validated at runtime
function processExternal(data: any) { ... }

// BETTER: Use unknown with Type Guard
function process(data: unknown): ProcessedData {
  if (!isValidData(data)) throw new Error('Invalid data');
  return data as ProcessedData;
}
```

### 2. Explicit Types for Public APIs

```typescript
// FORBIDDEN: Implicit return types on exports
export const calculate = (x, y) => x + y;

// REQUIRED: Explicit types
export const calculate = (x: number, y: number): number => x + y;

// For React Components
interface ButtonProps {
  label: string;
  onClick: () => void;
  variant?: 'primary' | 'secondary';
}

export const Button = ({ label, onClick, variant = 'primary' }: ButtonProps) => { ... };
```

### 3. Use Generic Constraints

```typescript
// FORBIDDEN: Unbounded generic
function getValue<T>(obj: T, key: string) {
  return obj[key]; // Error
}

// REQUIRED: Constrained generic
function getValue<T extends object, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key];
}
```

### 4. Leverage Utility Types

```typescript
// Instead of duplication:
interface UserBase { name: string; email: string; }
interface UserCreate { name: string; email: string; }
interface UserUpdate { name?: string; email?: string; }

// Use Utility Types:
interface User { id: string; name: string; email: string; createdAt: Date; }
type UserCreate = Omit<User, 'id' | 'createdAt'>;
type UserUpdate = Partial<Pick<User, 'name' | 'email'>>;
```

### 5. Readonly for Immutability

```typescript
interface Config {
  readonly apiUrl: string;
  readonly timeout: number;
}

// For arrays
const items: readonly string[] = ['a', 'b'];
// or
const items: ReadonlyArray<string> = ['a', 'b'];
```

### 6. Const Assertions for Literals

```typescript
// Without const assertion
const STATUS = { ACTIVE: 'active', INACTIVE: 'inactive' };
// Type: { ACTIVE: string; INACTIVE: string }

// With const assertion
const STATUS = { ACTIVE: 'active', INACTIVE: 'inactive' } as const;
// Type: { readonly ACTIVE: "active"; readonly INACTIVE: "inactive" }
```

### 7. Discriminated Unions for State

```typescript
// Instead of optional properties:
interface Response {
  data?: Data;
  error?: Error;
  loading?: boolean;
}

// Use Discriminated Unions:
type Response =
  | { status: 'loading' }
  | { status: 'success'; data: Data }
  | { status: 'error'; error: Error };
```

## Recommended tsconfig.json

```json
{
  "compilerOptions": {
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "strictFunctionTypes": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitOverride": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,
    "forceConsistentCasingInFileNames": true
  }
}
```

## Pre-Edit Checklist

- [ ] No `any` without documented reason
- [ ] Explicit types on exports
- [ ] Generic constraints where applicable
- [ ] Utility types instead of duplication
- [ ] Readonly where immutability is desired
- [ ] Discriminated unions for states

## On Violation

1. Issue a warning with a specific improvement suggestion
2. Show a code example for the correct approach
3. Link to TypeScript Handbook for complex cases

## Exceptions (require documentation)

- Legacy code migration (temporary)
- Third-party library interop
- Performance-critical hot paths (with benchmark evidence)
