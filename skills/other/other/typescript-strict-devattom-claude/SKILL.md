---
name: typescript-strict
description: TypeScript strict typing patterns and best practices. ALWAYS use when the user mentions "any type", "type error", "ts-ignore", "type guard", "unknown type", "zod schema", "type safety", "erreur de type", "typage strict". Provides patterns for avoiding `any`, proper use of `unknown`, type guards, and Zod validation.
---

# TypeScript Strict Typing

## Forbidden Patterns

**NEVER use these** - they defeat TypeScript's purpose:

| Type | Why it's bad | What to do instead |
|------|--------------|---------------------|
| `any` | Disables all type checking | Use proper types or `unknown` with type guards |
| `as any` | Type assertion escape hatch | Fix the underlying type issue |
| `@ts-ignore` | Silences compiler errors | Fix the type error properly |
| `@ts-expect-error` | Only acceptable with explanation | Prefer fixing the actual issue |

## Proper Use of `unknown`

Use `unknown` ONLY when:
- Receiving data from external sources (API responses, user input)
- Parsing JSON
- Working with third-party libraries without types
- **Always** narrow with type guards before using

```typescript
// WRONG - using any
function process(data: any) { return data.value; }

// CORRECT - using unknown with type guard
function process(data: unknown) {
  if (isValidData(data)) {
    return data.value;
  }
  throw new Error('Invalid data');
}

// Type guard function
function isValidData(data: unknown): data is { value: string } {
  return typeof data === 'object' && data !== null && 'value' in data;
}
```

## Proper Use of `never`

Use `never` ONLY for:
- Exhaustive switch/if checks
- Functions that always throw
- Impossible states in discriminated unions

```typescript
function handleStatus(status: 'pending' | 'done' | 'error'): string {
  switch (status) {
    case 'pending': return 'Waiting...';
    case 'done': return 'Complete!';
    case 'error': return 'Failed';
    default:
      const _exhaustive: never = status;
      throw new Error(`Unhandled status: ${_exhaustive}`);
  }
}
```

## Type Inference Best Practices

- **Let TypeScript infer** when the type is obvious
- **Explicitly type** function parameters and return types
- **Explicitly type** exported functions and public APIs
- **Use const assertions** for literal types: `as const`

```typescript
// Let inference work - no need to annotate
const count = 0;                    // inferred as number
const items = ['a', 'b'];           // inferred as string[]

// Explicitly type function signatures
function calculateTotal(items: CartItem[]): number {
  return items.reduce((sum, item) => sum + item.price, 0);
}

// Use const for literal types
const CONFIG = {
  apiUrl: 'https://api.example.com',
  timeout: 5000,
} as const;
```

## Runtime Validation with Zod

For external data, use Zod for runtime validation:

```typescript
import { z } from 'zod';

const UserSchema = z.object({
  id: z.string().uuid(),
  email: z.string().email(),
  name: z.string().min(1),
});

type User = z.infer<typeof UserSchema>;

// Safe parsing with runtime validation
function parseUser(data: unknown): User {
  return UserSchema.parse(data);
}
```

## Strict tsconfig Settings

Ensure these are enabled:

```json
{
  "compilerOptions": {
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "strictFunctionTypes": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noImplicitReturns": true,
    "exactOptionalPropertyTypes": true
  }
}
```
