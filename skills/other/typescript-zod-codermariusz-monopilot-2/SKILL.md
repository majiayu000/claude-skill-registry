---
name: typescript-zod
description: Apply when validating external data (API inputs, form data, environment variables) with TypeScript type inference.
---

## When to Use

Apply when validating external data (API inputs, form data, environment variables) with TypeScript type inference.

## Patterns

### Pattern 1: Basic Schema
```typescript
// Source: https://zod.dev/
import { z } from 'zod';

const UserSchema = z.object({
  id: z.string().uuid(),
  name: z.string().min(2).max(100),
  email: z.string().email(),
  age: z.number().int().positive().optional(),
});

type User = z.infer<typeof UserSchema>; // Auto-infer TS type
```

### Pattern 2: Parse vs SafeParse
```typescript
// Source: https://zod.dev/
// Throws on error
const user = UserSchema.parse(data);

// Returns result object (safer)
const result = UserSchema.safeParse(data);
if (result.success) {
  console.log(result.data); // User type
} else {
  console.log(result.error.issues); // Validation errors
}
```

### Pattern 3: API Request Validation
```typescript
// Source: https://zod.dev/
const CreateUserSchema = z.object({
  name: z.string().min(1, 'Name is required'),
  email: z.string().email('Invalid email format'),
  password: z.string().min(8, 'Password must be at least 8 characters'),
});

// In API handler
export async function POST(req: Request) {
  const body = await req.json();
  const result = CreateUserSchema.safeParse(body);

  if (!result.success) {
    return Response.json({ errors: result.error.flatten() }, { status: 400 });
  }

  // result.data is typed as { name: string; email: string; password: string }
  const user = await createUser(result.data);
  return Response.json(user, { status: 201 });
}
```

### Pattern 4: Environment Variables
```typescript
// Source: https://zod.dev/
const EnvSchema = z.object({
  DATABASE_URL: z.string().url(),
  API_KEY: z.string().min(1),
  PORT: z.coerce.number().default(3000),
  NODE_ENV: z.enum(['development', 'production', 'test']),
});

export const env = EnvSchema.parse(process.env);
```

### Pattern 5: Transform & Refinements
```typescript
// Source: https://zod.dev/
const DateSchema = z.string().transform(s => new Date(s));

const PasswordSchema = z.string()
  .min(8)
  .refine(p => /[A-Z]/.test(p), 'Must contain uppercase')
  .refine(p => /[0-9]/.test(p), 'Must contain number');
```

## Anti-Patterns

- **No validation on boundaries** - Always validate external data
- **Using `parse` in user flows** - Use `safeParse` to handle errors gracefully
- **Duplicating types** - Use `z.infer<>` instead of manual types
- **Ignoring error messages** - Provide user-friendly messages

## Verification Checklist

- [ ] All API inputs validated with Zod
- [ ] Types inferred with `z.infer<>`
- [ ] `safeParse` used for user-facing validation
- [ ] Custom error messages for UX
- [ ] Environment variables validated at startup

## MonoPilot: Domain Schemas

MonoPilot validation pattern (from `lib/validation/`):

```typescript
// 1. Define enums first
export const UserRoleEnum = z.enum([
  'owner', 'admin', 'production_manager', 'quality_manager',
  'warehouse_manager', 'production_operator', 'quality_inspector',
  'warehouse_operator', 'planner', 'viewer',
])
export type UserRole = z.infer<typeof UserRoleEnum>

// 2. Schema using enum + custom messages + .trim()
export const CreateUserSchema = z.object({
  email: z.string().min(1, 'Email is required').email('Invalid email').max(255),
  first_name: z.string().min(1, 'Required').max(100).trim(),
  role: UserRoleEnum.optional(),
  role_id: z.string().uuid('Invalid role ID').optional(),
}).refine(
  (data) => data.role !== undefined || data.role_id !== undefined,
  { message: 'Role is required', path: ['role'] }
)

// 3. Helper function
export function validateCreateUser(data: unknown) {
  return CreateUserSchema.parse(data)
}

// 4. Display label map
export const roleLabels: Record<UserRole, string> = {
  owner: 'Owner', admin: 'Administrator', /* ... */
}
```
