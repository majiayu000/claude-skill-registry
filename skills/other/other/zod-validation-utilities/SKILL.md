---
name: zod-validation-utilities
description: Creates reusable Zod v4 schemas, validates API payloads, forms, and configuration input, transforms and coerces data safely, and handles validation errors with strong type inference for TypeScript applications. Use when designing validation layers, parsing `z.string()`, `z.object()`, or `z.email()` schemas, or implementing runtime type-safe data validation.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# Zod Validation Utilities

## Overview

Production-ready Zod v4 patterns for reusable, type-safe validation with minimal boilerplate. Focuses on modern APIs, predictable error handling, and form integration.

## When to Use

- Defining request/response validation schemas in TypeScript services
- Parsing untrusted input from APIs, forms, env vars, or external systems
- Standardizing coercion, transforms, and cross-field validation
- Building reusable schema utilities across teams
- Integrating React Hook Form with Zod using `zodResolver`

## Instructions

1. Start with strict object schemas and explicit field constraints
2. Prefer modern Zod v4 APIs and the `error` option for error messages
3. Use coercion at boundaries (`z.coerce.*`) when input types are uncertain
4. Keep business invariants in `refine`/`superRefine` close to schema definitions
5. Export both schema and inferred types (`z.input`/`z.output`) for consistency
6. Reuse utility schemas (email, id, dates, pagination) to reduce duplication

## Validation Workflow

When integrating validation into an API handler or service:

1. **Define** the schema at the boundary (handler, queue, config loader)
2. **Parse** with `safeParse` to handle errors gracefully
3. **Check** `result.success` to branch on failure/success
4. **Use** `result.data` with full type inference in success path
5. **Return** formatted errors or proceed with validated data

See example 7 (`safeParse` workflow) for the complete pattern.

## Examples

### 1) Modern Zod 4 primitives and object errors

```ts
import { z } from "zod";

export const UserIdSchema = z.uuid({ error: "Invalid user id" });
export const EmailSchema = z.email({ error: "Invalid email" });
export const WebsiteSchema = z.url({ error: "Invalid URL" });

export const UserProfileSchema = z.object(
  {
    id: UserIdSchema,
    email: EmailSchema,
    website: WebsiteSchema.optional(),
  },
  { error: "Invalid user profile payload" }
);
```

### 2) Coercion, preprocess, and transform

```ts
import { z } from "zod";

export const PaginationQuerySchema = z.object({
  page: z.coerce.number().int().min(1).default(1),
  pageSize: z.coerce.number().int().min(1).max(100).default(20),
  includeArchived: z.coerce.boolean().default(false),
});

export const DateFromUnknownSchema = z.preprocess(
  (value) => (typeof value === "string" || value instanceof Date ? value : undefined),
  z.coerce.date({ error: "Invalid date" })
);

export const NormalizedEmailSchema = z
  .string()
  .trim()
  .toLowerCase()
  .email({ error: "Invalid email" })
  .transform((value) => value as Lowercase<string>);
```

### 3) Complex schema structures

```ts
import { z } from "zod";

const TagSchema = z.string().trim().min(1).max(40);

export const ProductSchema = z.object({
  sku: z.string().min(3).max(24),
  tags: z.array(TagSchema).max(15),
  attributes: z.record(z.string(), z.union([z.string(), z.number(), z.boolean()])),
  dimensions: z.tuple([z.number().positive(), z.number().positive(), z.number().positive()]),
});

export const PaymentMethodSchema = z.discriminatedUnion("type", [
  z.object({ type: z.literal("card"), last4: z.string().regex(/^\d{4}$/) }),
  z.object({ type: z.literal("paypal"), email: z.email() }),
  z.object({ type: z.literal("wire"), iban: z.string().min(10) }),
]);
```

### 4) `refine` and `superRefine`

```ts
import { z } from "zod";

export const PasswordSchema = z
  .string()
  .min(12)
  .refine((v) => /[A-Z]/.test(v), { error: "Must include an uppercase letter" })
  .refine((v) => /\d/.test(v), { error: "Must include a number" });

export const RegisterSchema = z
  .object({
    email: z.email(),
    password: PasswordSchema,
    confirmPassword: z.string(),
  })
  .superRefine((data, ctx) => {
    if (data.password !== data.confirmPassword) {
      ctx.addIssue({
        code: "custom",
        path: ["confirmPassword"],
        message: "Passwords do not match",
      });
    }
  });
```

### 5) Optional, nullable, nullish, and default

```ts
import { z } from "zod";

export const UserPreferencesSchema = z.object({
  nickname: z.string().min(2).optional(),      // undefined allowed
  bio: z.string().max(280).nullable(),         // null allowed
  avatarUrl: z.url().nullish(),                // null or undefined allowed
  locale: z.string().default("en"),           // fallback when missing
});
```

### 6) React Hook Form integration (`zodResolver`)

```tsx
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";

const ProfileFormSchema = z.object({
  name: z.string().min(2, { error: "Name too short" }),
  email: z.email({ error: "Invalid email" }),
  age: z.coerce.number().int().min(18),
});

type ProfileFormInput = z.input<typeof ProfileFormSchema>;
type ProfileFormOutput = z.output<typeof ProfileFormSchema>;

const form = useForm<ProfileFormInput, unknown, ProfileFormOutput>({
  resolver: zodResolver(ProfileFormSchema),
  criteriaMode: "all",
});
```

### 7) Error handling workflow with `safeParse`

```ts
import { z } from "zod";
import type { ZodError } from "zod";

const ResultSchema = z.object({ id: z.string(), name: z.string() });

function parseAndHandle(input: unknown) {
  const result = ResultSchema.safeParse(input);

  if (!result.success) {
    const error = result.error as ZodError;
    console.error("Validation failed:", error.errors);
    return { success: false as const, error: error.format() };
  }

  return { success: true as const, data: result.data };
}
```

> **Tip**: For advanced discriminated union patterns and complex React Hook Form workflows, see `references/advanced-patterns.md`.

## Best Practices

- Keep schemas near boundaries (HTTP handlers, queues, config loaders)
- Prefer `safeParse` for recoverable flows; `parse` for fail-fast execution
- Share small schema utilities (`id`, `email`, `slug`) to enforce consistency
- Use `z.input` and `z.output` when transforms/coercions change runtime shape
- Avoid overusing `preprocess`; prefer explicit `z.coerce.*` where possible
- Treat external payloads as untrusted and always validate before use

## Constraints and Warnings

- Ensure examples match your installed `zod` major version (v4 APIs shown)
- `error` is the preferred option for custom errors in Zod v4 patterns
- Discriminated unions require a stable discriminator key across variants
- Coercion can hide bad upstream data; add bounds and refinements defensively
