---
name: yup
description: "Schema validation for JavaScript objects with expressive API. Object schemas, async validation, type inference, custom validators. Trigger: When creating validation schemas with Yup, validating forms, or implementing schema-based validation."
skills:
  - conventions
  - typescript
dependencies:
  yup: ">=1.0.0 <2.0.0"
allowed-tools:
  - documentation-reader
  - web-search
---

# Yup Skill

## Overview

Schema-based validation library for JavaScript and TypeScript with intuitive API.

## Objective

Enable developers to define and validate data schemas with proper TypeScript integration and error handling.

---

## When to Use

Use this skill when:

- Validating form data with Yup schemas
- Creating validation logic for JavaScript/TypeScript objects
- Implementing async validation
- Integrating with Formik or other form libraries
- Defining reusable validation schemas

Don't use this skill for:

- Zod-specific patterns (use zod skill)
- TypeScript compile-time typing only (use typescript skill)
- Runtime parsing without validation (use zod for better TypeScript integration)

---

## Critical Patterns

### ✅ REQUIRED: Use InferType for Type Extraction

```typescript
// ✅ CORRECT: Automatic type inference
import * as yup from "yup";

const schema = yup.object({
  name: yup.string().required(),
});

type User = yup.InferType<typeof schema>; // { name: string }

// ❌ WRONG: Manual type definition (can drift)
interface User {
  name: string;
}
const schema = yup.object({
  /* ... */
});
```

### ✅ REQUIRED: Use validate() with try/catch

```typescript
// ✅ CORRECT: Proper error handling
try {
  const valid = await schema.validate(data);
  console.log(valid);
} catch (error) {
  if (error instanceof yup.ValidationError) {
    console.error(error.message);
  }
}

// ❌ WRONG: No error handling
const valid = await schema.validate(data); // Throws on error
```

### ✅ REQUIRED: Chain Validations

```typescript
// ✅ CORRECT: Multiple validations
const email = yup
  .string()
  .email("Invalid email")
  .required("Email is required")
  .max(100, "Too long");

// ❌ WRONG: Single validation
const email = yup.string();
```

---

## Conventions

Refer to conventions for:

- Error handling

Refer to typescript for:

- Type inference from schemas

### Yup Specific

- Define schemas with proper types
- Use TypeScript's InferType for type extraction
- Implement custom validation methods
- Handle validation errors appropriately
- Use schema composition

---

## Decision Tree

**String validation?** → Use `.string()` with `.email()`, `.url()`, `.min()`, `.max()`, `.matches()`.

**Number validation?** → Use `.number()` with `.positive()`, `.integer()`, `.min()`, `.max()`.

**Optional field?** → Use `.nullable()` or `.notRequired()`. Use `.default()` for default values.

**Conditional validation?** → Use `.when('field', { is: value, then: schema })` for dependent fields.

**Custom validation?** → Use `.test('name', 'message', (value) => boolean)`.

**Async validation?** → Use `.test()` with async function, handle promises.

**Schema composition?** → Use `.concat()` to merge schemas or extract common schemas.

**Array validation?** → Use `.array(itemSchema)` with `.min()`, `.max()`, `.of()`.

---

## Example

```typescript
import * as yup from "yup";

const userSchema = yup.object({
  name: yup.string().required("Name is required"),
  email: yup.string().email("Invalid email").required("Email is required"),
  age: yup.number().positive().integer().min(18, "Must be 18 or older"),
});

type User = yup.InferType<typeof userSchema>;

try {
  const validUser: User = await userSchema.validate({
    name: "John",
    email: "john@example.com",
    age: 25,
  });
} catch (error) {
  if (error instanceof yup.ValidationError) {
    console.error(error.message);
  }
}
```

---

## Edge Cases

**Circular references:** Use `yup.lazy()` for recursive schemas that reference themselves.

**Transform values:** Use `.transform((value, original) => transformed)` to modify values during validation.

**Strict vs default:** Yup removes unknown keys by default. Use `.strict()` to throw error on unknown keys.

**Multiple errors:** Use `.abortEarly: false` in validate options to collect all errors, not just first.

**Nullable vs optional:** `.nullable()` allows null, `.notRequired()` allows undefined. `.optional()` is alias for `.notRequired()`.

---

## References

- https://github.com/jquense/yup
