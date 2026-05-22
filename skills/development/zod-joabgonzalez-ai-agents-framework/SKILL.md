---
name: zod
description: TypeScript-first schema validation with static type inference. Type-safe validation, parsing, refinements, transformations. Trigger: When creating validation schemas, parsing user input, or ensuring type-safe data validation with Zod.
skills:
  - conventions
  - typescript
dependencies:
  zod: ">=3.0.0 <4.0.0"
allowed-tools:
  - documentation-reader
  - web-search
---

# Zod Skill

## Overview

TypeScript-first schema validation library with automatic type inference and excellent developer experience.

## Objective

Enable developers to define runtime-safe schemas with full TypeScript integration and type inference.

---

## When to Use

Use this skill when:

- Validating user input or API responses at runtime
- Parsing external data with type safety
- Creating form validation schemas
- Transforming and refining data during validation
- Ensuring data conforms to TypeScript types

Don't use this skill for:

- Compile-time-only typing (use typescript skill)
- Yup-specific patterns (use yup skill)
- Form management (use formik skill for forms)

---

## Critical Patterns

### ✅ REQUIRED: Use z.infer for Type Extraction

```typescript
// ✅ CORRECT: Automatic type inference
const userSchema = z.object({
  name: z.string(),
  age: z.number(),
});

type User = z.infer<typeof userSchema>; // { name: string; age: number }

// ❌ WRONG: Manual type definition (can drift from schema)
interface User {
  name: string;
  age: number;
}
const userSchema = z.object({
  /* ... */
});
```

### ✅ REQUIRED: Use safeParse for Error Handling

```typescript
// ✅ CORRECT: Safe parsing with error handling
const result = schema.safeParse(data);
if (result.success) {
  const validated = result.data;
} else {
  console.error(result.error.format());
}

// ❌ WRONG: parse() throws, requires try/catch
const validated = schema.parse(data); // Throws on error
```

### ✅ REQUIRED: Chain Validations

```typescript
// ✅ CORRECT: Chained validations
const emailSchema = z
  .string()
  .email("Invalid email")
  .min(5, "Too short")
  .max(100, "Too long");

// ❌ WRONG: Single validation (insufficient)
const emailSchema = z.string();
```

---

## Conventions

Refer to conventions for:

- Error handling

Refer to typescript for:

- Type patterns

### Zod Specific

- Define schemas with z.object, z.string, etc.
- Use z.infer for automatic type extraction
- Implement custom refinements
- Use transforms for data manipulation
- Handle validation errors with proper types

---

## Decision Tree

**String validation?** → Use `.string()` with chains: `.email()`, `.url()`, `.min()`, `.max()`, `.regex()`.

**Number validation?** → Use `.number()` with `.int()`, `.positive()`, `.min()`, `.max()`.

**Optional field?** → Use `.optional()` or `.nullable()`. Use `.default()` for default values.

**Union types?** → Use `z.union([schema1, schema2])` or `z.enum(['a', 'b'])`for literals.

**Custom validation?** → Use `.refine((val) => condition, { message: 'Error' })`.

**Transform data?** → Use `.transform((val) => transformed)` after validation.

**Array validation?** → Use `z.array(itemSchema)` with `.min()`, `.max()`, `.nonempty()`.

**Async validation?** → Use `.parseAsync()` or `.safeParseAsync()` with async refinements.

---

## Example

```typescript
import { z } from "zod";

const userSchema = z.object({
  name: z.string().min(1, "Name is required"),
  email: z.string().email("Invalid email"),
  age: z.number().int().positive().min(18, "Must be 18 or older"),
});

type User = z.infer<typeof userSchema>;

const result = userSchema.safeParse({
  name: "John",
  email: "john@example.com",
  age: 25,
});

if (result.success) {
  const user: User = result.data;
} else {
  console.error(result.error.format());
}
```

---

## Edge Cases

**Circular references:** Use `z.lazy()` for recursive schemas that reference themselves.

**Discriminated unions:** Use `.discriminatedUnion('type', [...])` for better type narrowing and performance.

**Error formatting:** Use `.format()` for nested errors object, `.flatten()` for flat structure, `.issues` for array.

**Coercion:** Use `z.coerce.number()` to parse strings as numbers, useful for form inputs.

**Unknown keys:** By default, Zod strips unknown keys. Use `.passthrough()` to keep them or `.strict()` to error.

---

## References

- https://zod.dev/
