---
name: typescript-type-safe-api-contracts
description: |
  TypeScript patterns for type-safe API contracts, strict typing, Zod integration. Use when designing
  APIs, creating types, validating data. Keywords: "api design", "schema", "type safety", "interface",
  "zod", "validation", "type", "strict mode".
---

# TypeScript Type-Safe API Contracts

## Core Principle: Explicit Return Types (Mandatory)

```tsx
// ❌ BAD: Implicit return type
export function getUser(id: string) {
  return db.user.findUnique({ where: { id } });
}

// ✅ GOOD: Explicit return type
export async function getUser(id: string): Promise<User | null> {
  return db.user.findUnique({ where: { id } });
}
```

## Interface vs Type

**Use `interface` for object shapes**:

```tsx
interface User {
  id: string;
  name: string;
  email: string;
}

interface ApiResponse<T> {
  success: boolean;
  data: T;
}
```

**Use `type` for unions, intersections, utilities**:

```tsx
type Status = 'pending' | 'active' | 'archived';

type ApiResult<T> =
  | { success: true; data: T }
  | { success: false; error: string };
```

## Generic API Response Wrapper

```tsx
// types/api/common.ts
export type ApiResponse<T> =
  | ApiSuccessResponse<T>
  | ApiErrorResponse;

export interface ApiSuccessResponse<T> {
  success: true;
  data: T;
}

export interface ApiErrorResponse {
  success: false;
  error: {
    code: string;
    message: string;
    details?: Record<string, string[]>;
  };
}

// Usage
export async function createUser(data: CreateUserInput): Promise<ApiResponse<User>> {
  // ...
}
```

## Zod Integration (Runtime Validation)

```tsx
import { z } from 'zod';

// 1. Define Zod schema
const userSchema = z.object({
  name: z.string().min(1, 'Name required').max(100),
  email: z.string().email('Invalid email'),
  age: z.number().int().positive().optional(),
});

// 2. Infer TypeScript type from schema
export type User = z.infer<typeof userSchema>;

// 3. Validate at runtime
export async function createUser(input: unknown): Promise<ApiResponse<User>> {
  try {
    const validated = userSchema.parse(input); // Throws if invalid
    // ...
  } catch (error) {
    if (error instanceof z.ZodError) {
      return {
        success: false,
        error: {
          code: 'VALIDATION_ERROR',
          message: 'Invalid input',
          details: error.flatten().fieldErrors,
        },
      };
    }
  }
}
```

## Utility Types for Transformations

```tsx
interface User {
  id: string;
  name: string;
  email: string;
  password: string;
}

// Pick specific fields
type PublicUser = Pick<User, 'id' | 'name'>; // { id: string; name: string }

// Omit fields
type UserWithoutPassword = Omit<User, 'password'>; // { id: string; name: string; email: string }

// Make all fields optional
type PartialUser = Partial<User>; // { id?: string; name?: string; ... }

// Make all fields required
type RequiredUser = Required<Partial<User>>;

// Create record type
type UserMap = Record<string, User>; // { [key: string]: User }
```

## Anti-Patterns

❌ **Using `any`** (FORBIDDEN):

```tsx
// ❌ BAD
function processData(data: any) { }

// ✅ GOOD
function processData(data: unknown) {
  if (typeof data === 'string') {
    // Type narrowing
  }
}
```

❌ **Non-null assertion without guards**:

```tsx
// ❌ BAD
const user = getUser()!; // Assumes non-null, can crash

// ✅ GOOD
const user = getUser();
if (!user) return;
// Now TypeScript knows user is non-null
```

For backend synchronization and Python/Pydantic mapping, see `/api-contract` command.
