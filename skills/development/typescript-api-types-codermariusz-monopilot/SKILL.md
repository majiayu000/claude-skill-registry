---
name: typescript-api-types
description: Apply when defining API request/response types, DTOs, and shared types between frontend and backend.
version: 1.1.0
tokens: ~650
confidence: high
sources:
  - https://www.typescriptlang.org/docs/handbook/utility-types.html
  - https://zod.dev/
last_validated: 2025-12-10
next_review: 2025-12-24
tags: [typescript, api, types, validation]
---

## When to Use

Apply when defining API request/response types, DTOs, and shared types between frontend and backend.

## Patterns

### Pattern 1: Request/Response Types
```typescript
// Source: https://www.typescriptlang.org/docs/handbook/utility-types.html
// Base entity
interface User {
  id: string;
  email: string;
  name: string;
  createdAt: Date;
  updatedAt: Date;
}

// Create DTO (omit auto-generated fields)
type CreateUserDto = Omit<User, 'id' | 'createdAt' | 'updatedAt'>;

// Update DTO (all fields optional except id)
type UpdateUserDto = Partial<Omit<User, 'id'>> & Pick<User, 'id'>;

// Response (dates as strings from JSON)
type UserResponse = Omit<User, 'createdAt' | 'updatedAt'> & {
  createdAt: string;
  updatedAt: string;
};
```

### Pattern 2: API Response Wrapper
```typescript
// Source: Best practice pattern
interface ApiResponse<T> {
  data: T;
  meta?: {
    page?: number;
    limit?: number;
    total?: number;
  };
}

interface ApiError {
  error: {
    code: string;
    message: string;
    details?: Record<string, string[]>;
  };
}

type ApiResult<T> = ApiResponse<T> | ApiError;

// Type guard
function isApiError(result: ApiResult<unknown>): result is ApiError {
  return 'error' in result;
}
```

### Pattern 3: Zod Schema as Single Source
```typescript
// Source: https://zod.dev/
import { z } from 'zod';

// Schema is source of truth
const UserSchema = z.object({
  id: z.string().uuid(),
  email: z.string().email(),
  name: z.string().min(1),
  role: z.enum(['user', 'admin']),
});

// Infer types from schema
type User = z.infer<typeof UserSchema>;

const CreateUserSchema = UserSchema.omit({ id: true });
type CreateUserDto = z.infer<typeof CreateUserSchema>;

const UpdateUserSchema = UserSchema.partial().required({ id: true });
type UpdateUserDto = z.infer<typeof UpdateUserSchema>;
```

### Pattern 4: Shared Types Package
```typescript
// packages/shared-types/src/user.ts
export interface User { /* ... */ }
export type CreateUserDto = Omit<User, 'id'>;

// Frontend: import { User } from '@myapp/shared-types';
// Backend:  import { User } from '@myapp/shared-types';
```

### Pattern 5: API Endpoint Type Map
```typescript
// Source: Best practice pattern
interface ApiEndpoints {
  'GET /users': { response: User[] };
  'GET /users/:id': { params: { id: string }; response: User };
  'POST /users': { body: CreateUserDto; response: User };
  'PUT /users/:id': { params: { id: string }; body: UpdateUserDto; response: User };
  'DELETE /users/:id': { params: { id: string }; response: void };
}

// Type-safe API client
async function api<K extends keyof ApiEndpoints>(
  endpoint: K,
  options?: Omit<ApiEndpoints[K], 'response'>
): Promise<ApiEndpoints[K]['response']> {
  // Implementation
}
```

### Pattern 6: NoInfer for Strict Type Matching (TypeScript 5.4+)
```typescript
// Source: https://www.typescriptlang.org/docs/handbook/utility-types.html
// Ensure parameter matches exact union, don't expand it
function validateStatus<S extends string>(
  validStatuses: S[],
  currentStatus: NoInfer<S>
): boolean {
  return validStatuses.includes(currentStatus);
}

// S inferred as 'pending' | 'active' | 'done'
validateStatus(['pending', 'active', 'done'], 'active');  // OK
validateStatus(['pending', 'active', 'done'], 'invalid'); // Error
```

## Anti-Patterns

- **Duplicate types** - Single source of truth (Zod or interface)
- **Manual JSON date parsing** - Use consistent date handling
- **`any` for API responses** - Type everything
- **Frontend/backend type drift** - Use shared types package

## Verification Checklist

- [ ] DTOs derived from base type (Omit, Pick, Partial)
- [ ] Zod schemas validate at runtime
- [ ] Types inferred from Zod (no duplication)
- [ ] API error type defined and handled
- [ ] Date serialization consistent
