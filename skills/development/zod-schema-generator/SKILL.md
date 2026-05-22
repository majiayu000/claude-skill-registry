---
name: zod-schema-generator
description: Generate Zod validation schemas from Prisma models, TypeScript interfaces, or JSON examples. Use when asked to generate Zod schemas, create validation, bridge Prisma to Zod, validate API input/output, or generate runtime type checks.
---

# Zod Schema Generator

Before generating any output, read `config/defaults.md` and adapt all patterns, imports, and code examples to the user's configured stack.

## Process

1. Identify the source: Prisma model, TypeScript interface/type, or raw JSON example.
2. Determine schema purpose: input validation (create/update), output validation (API response), or full round-trip.
3. Generate Zod schema with correct types, optional fields, and refinements.
4. Add `.transform()` and `.refine()` where appropriate.
5. Output the schema file with proper imports and exports.

## Source: Prisma Model

Parse the Prisma model and generate both input and output schemas.

### Input Schema (for create/update)

Omit auto-generated fields (`id`, `createdAt`, `updatedAt`) and fields with `@default`.

```prisma
model User {
  id        String   @id @default(cuid())
  email     String   @unique
  name      String?
  role      Role     @default(USER)
  posts     Post[]
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
}
```

```typescript
// Generated: user.schema.ts
import { z } from "zod";

export const createUserSchema = z.object({
  email: z.string().email().trim().toLowerCase(),
  name: z.string().min(1).trim().optional(),
  role: z.enum(["USER", "ADMIN"]).optional(), // has @default
});

export const updateUserSchema = createUserSchema.partial();

export type CreateUserInput = z.infer<typeof createUserSchema>;
export type UpdateUserInput = z.infer<typeof updateUserSchema>;
```

### Output Schema (for API responses)

Include all fields. Use `z.coerce.date()` for DateTime fields.

```typescript
export const userSchema = z.object({
  id: z.string().cuid(),
  email: z.string().email(),
  name: z.string().nullable(),
  role: z.enum(["USER", "ADMIN"]),
  createdAt: z.coerce.date(),
  updatedAt: z.coerce.date(),
});

export type User = z.infer<typeof userSchema>;
```

### Relations

For input schemas, generate nested create/connect patterns:

```typescript
// One-to-many: creating a post with author
export const createPostSchema = z.object({
  title: z.string().min(1).max(255),
  content: z.string(),
  author: z.union([
    z.object({ connect: z.object({ id: z.string() }) }),
    z.object({ create: createUserSchema }),
  ]),
});
```

For output schemas, include the related object shape:

```typescript
export const postWithAuthorSchema = postSchema.extend({
  author: userSchema,
});
```

## Source: TypeScript Interface

Map TypeScript types directly to Zod equivalents.

```typescript
// Input
interface OrderItem {
  productId: string;
  quantity: number;
  price: number;
  notes?: string;
  metadata: Record<string, unknown>;
}
```

```typescript
// Generated
export const orderItemSchema = z.object({
  productId: z.string().uuid(),
  quantity: z.number().int().positive(),
  price: z.number().nonnegative(),
  notes: z.string().optional(),
  metadata: z.record(z.string(), z.unknown()),
});
```

### Discriminated Unions

```typescript
// Input
type PaymentMethod =
  | { type: "card"; cardNumber: string; expiry: string }
  | { type: "bank"; accountNumber: string; routingNumber: string }
  | { type: "crypto"; walletAddress: string };
```

```typescript
// Generated
export const paymentMethodSchema = z.discriminatedUnion("type", [
  z.object({
    type: z.literal("card"),
    cardNumber: z.string().regex(/^\d{16}$/),
    expiry: z.string().regex(/^\d{2}\/\d{2}$/),
  }),
  z.object({
    type: z.literal("bank"),
    accountNumber: z.string(),
    routingNumber: z.string().regex(/^\d{9}$/),
  }),
  z.object({
    type: z.literal("crypto"),
    walletAddress: z.string().min(26).max(62),
  }),
]);
```

## Source: JSON Example

Infer schema from a JSON payload by analyzing value types and structure.

```json
{
  "name": "Acme Corp",
  "employees": 150,
  "active": true,
  "tags": ["tech", "startup"],
  "address": {
    "street": "123 Main St",
    "city": "Springfield",
    "zip": "62701"
  }
}
```

```typescript
// Generated (with refinement suggestions in comments)
export const companySchema = z.object({
  name: z.string().min(1),
  employees: z.number().int().nonnegative(),
  active: z.boolean(),
  tags: z.array(z.string()),
  address: z.object({
    street: z.string(),
    city: z.string(),
    zip: z.string().regex(/^\d{5}(-\d{4})?$/), // inferred US zip
  }),
});
```

## Common Refinements

Apply these automatically when field names or patterns suggest them:

| Field pattern | Refinement |
|---|---|
| `email` | `.email().trim().toLowerCase()` |
| `url`, `website` | `.url()` |
| `id`, `*Id` (cuid) | `.cuid()` or `.cuid2()` |
| `uuid`, `*Uuid` | `.uuid()` |
| `phone` | `.regex(/^\+?[\d\s-()]+$/)` |
| `password` | `.min(8)` |
| `*At` (timestamps) | `z.coerce.date()` |
| `slug` | `.regex(/^[a-z0-9]+(?:-[a-z0-9]+)*$/)` |
| `price`, `amount` | `.nonnegative()` |
| `quantity`, `count` | `.int().nonnegative()` |

## File Placement

- **Colocated**: Place schema next to the model/route it validates (e.g., `app/api/users/schema.ts`).
- **Centralized**: Place in `lib/validations/` or `src/schemas/` when schemas are shared across multiple routes.

Match the project's existing pattern. Default to colocated if no convention exists.

## Output Format

```
## Generated Zod Schema

**Source**: [Prisma model | TypeScript interface | JSON example]
**File**: `path/to/schema.ts`

[Generated code block]

### Refinements Applied
- `email`: Added `.email().trim().toLowerCase()`
- `createdAt`: Used `z.coerce.date()` for DateTime

### Usage Example
[Short example showing schema.parse() or schema.safeParse()]
```

## Reference

See [references/prisma-zod-mapping.md](references/prisma-zod-mapping.md) for the complete Prisma-to-Zod type mapping table and refinement catalog.
