---
name: typescript
description: Write TypeScript code following best practices. Use when developing TypeScript/JavaScript applications. Covers type safety, patterns, and tooling.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# TypeScript Development

## Project Setup

```bash
# Initialize with pnpm
pnpm init
pnpm add -D typescript @types/node

# TypeScript config
npx tsc --init
```

### tsconfig.json
```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitReturns": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "outDir": "./dist"
  },
  "include": ["src/**/*"]
}
```

## Type Patterns

### Discriminated Unions
```typescript
type Result<T> =
  | { success: true; data: T }
  | { success: false; error: Error };

function handleResult(result: Result<User>) {
  if (result.success) {
    console.log(result.data); // User
  } else {
    console.error(result.error); // Error
  }
}
```

### Branded Types
```typescript
type UserId = string & { readonly brand: unique symbol };
type OrderId = string & { readonly brand: unique symbol };

function createUserId(id: string): UserId {
  return id as UserId;
}
```

### Utility Types
```typescript
// Make all properties optional
Partial<User>

// Make all properties required
Required<User>

// Pick specific properties
Pick<User, 'id' | 'email'>

// Omit specific properties
Omit<User, 'password'>

// Make properties readonly
Readonly<User>
```

## Error Handling

```typescript
// Result type pattern
type Result<T, E = Error> =
  | { ok: true; value: T }
  | { ok: false; error: E };

async function fetchUser(id: string): Promise<Result<User>> {
  try {
    const user = await db.users.findById(id);
    if (!user) {
      return { ok: false, error: new Error('User not found') };
    }
    return { ok: true, value: user };
  } catch (error) {
    return { ok: false, error: error as Error };
  }
}
```

## Testing with Vitest

```typescript
import { describe, test, expect, vi } from 'vitest';

describe('UserService', () => {
  test('creates user with valid email', async () => {
    const service = new UserService(mockRepo);
    const user = await service.create('test@example.com');
    expect(user.email).toBe('test@example.com');
  });

  test('throws on invalid email', async () => {
    const service = new UserService(mockRepo);
    await expect(service.create('invalid')).rejects.toThrow();
  });
});
```

## Tooling

```bash
# Biome (linting + formatting)
pnpm add -D @biomejs/biome
pnpm biome check --apply .

# Vitest (testing)
pnpm add -D vitest
pnpm vitest
```
