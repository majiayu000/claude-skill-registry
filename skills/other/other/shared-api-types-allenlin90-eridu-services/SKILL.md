---
name: shared-api-types
description: Provides guidelines for using keys, schemas, and types from the shared @eridu/api-types package. This skill should be used when defining API contracts, ensuring type safety between frontend and backend, or implementing Zod schemas.
---

# Shared API Types & Schemas

This skill outlines the standards for using the `@eridu/api-types` package. This package is the **Single Source of Truth** for API contracts between Backend, Frontend, and external services.

## When to Use

| Use Case                   | Location               | Reason                                       |
| :------------------------- | :--------------------- | :------------------------------------------- |
| **API Responses**          | `packages/api-types`   | Ensures FE and BE agree on response shape    |
| **API Requests**           | `packages/api-types`   | Ensures inputs are validated consistently    |
| **Shared Enums**           | `packages/api-types`   | Consistency (e.g., `ShowStatus`, `UserRole`) |
| **Internal Service Logic** | `apps/erify_api/...`   | Keep implementation details private          |
| **DB Models**              | `prisma/schema.prisma` | DB layer should be separate from API layer   |

## Directory Structure

Organize by **Domain Resource**:

```
packages/api-types/src/
├── shows/        # Domain: Shows
├── users/        # Domain: Users
├── task-management/ # Domain: Task Management
│   ├── index.ts      # Exports
│   ├── task-template.schema.ts
│   └── template-definition.schema.ts
└── pagination/       # Shared utilities
```

## Import Strategy (Subpath Exports)

Always use subpath imports to keep domains separated.

```typescript
// ✅ Correct
import { TaskTemplate } from '@eridu/api-types/task-management';
import { User } from '@eridu/api-types/users';

// ❌ Avoid (if root export exists)
import { TaskTemplate } from '@eridu/api-types'; 
```

> [!NOTE]
> While it's possible to split `schemas.ts` and `types.ts`, current practice in this monorepo is to consolidate them into `schemas.ts` for simplicity and easier maintenance.

## Implementation Pattern

### 1. Define Zod Schemas (`schemas.ts`)

Define schemas that represent the **wire format** (usually `snake_case`).

```typescript
import { z } from 'zod';

export const userApiResponseSchema = z.object({
  id: z.string(),
  email: z.email(),
  created_at: z.string(),
});

export const createUserDtoSchema = z.object({
  email: z.string().email(),
  name: z.string().min(2),
});
```

### 2. Infer TypeScript Types (`types.ts`)

ALWAYS infer types from the Zod schemas. Never manually duplicate interfaces.

```typescript
import type { z } from 'zod';
import { userApiResponseSchema, createUserDtoSchema } from './schemas.js';

export type UserApiResponse = z.infer<typeof userApiResponseSchema>;
export type CreateUserDto = z.infer<typeof createUserDtoSchema>;
```

### 3. Usage in Backend (`erify_api`)

Import schemas for validation decortors and types for strongly-typed services.

```typescript
// Controller
import { createUserDtoSchema, CreateUserDto } from '@eridu/api-types/users';

@Post()
// Validate input body with shared schema
@UsePipes(new ZodValidationPipe(createUserDtoSchema))
create(@Body() body: CreateUserDto) { ... }
```

### 4. Usage in Frontend (`erify_creators`)

Import types for API clients and schemas for form validation.

```typescript
import { type CreateUserDto, createUserDtoSchema } from '@eridu/api-types/users';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';

// Use shared schema for form validation
const form = useForm<CreateUserDto>({
  resolver: zodResolver(createUserDtoSchema)
});
```

## Checklist

- [ ] New API contract? Add to `@eridu/api-types` first.
- [ ] Group by domain folder (`src/my-domain/`).
- [ ] Export `schemas` (runtime) and `types` (static).
- [ ] Use `snake_case` for wire formats.
- [ ] Infer types using `z.infer`.
