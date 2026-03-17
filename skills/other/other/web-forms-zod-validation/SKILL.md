---
name: web-forms-zod-validation
description: Zod schema validation patterns for TypeScript - schema definitions, type inference, refinements, transforms, discriminated unions
---

# Zod Schema Validation Patterns

> **Quick Guide:** Use Zod for runtime validation of untrusted data (API responses, form inputs, config). Define schemas once, infer TypeScript types with `z.infer`. Use `safeParse` for error handling, `refine` for custom validation, `transform` for data transformation.
>
> **Version Note:** This skill documents Zod v3.23 patterns. Zod v4 is available with major performance improvements (14.7x faster string parsing, 100x fewer TypeScript instantiations) and new APIs (`z.email()`, `z.iso.*`, `z.templateLiteral()`, `z.codec()`). For v4 migration, see [zod.dev/v4](https://zod.dev/v4).

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST use `safeParse` instead of `parse` for user-facing validation - prevents unhandled exceptions)**

**(You MUST use `z.infer<typeof schema>` to derive types - never duplicate schema as separate interface)**

**(You MUST validate at trust boundaries - API responses, form inputs, config files, URL params)**

**(You MUST use named constants for validation limits - NO magic numbers in `.min()`, `.max()`, `.length()`)**

</critical_requirements>

---

**Auto-detection:** Zod schemas, z.object, z.string, z.number, z.infer, safeParse, refine, transform, discriminatedUnion, z.coerce, z.pipe, z.catch, z.brand, z.lazy

**When to use:**

- Validating API responses before using data
- Parsing form input data with type safety
- Validating configuration files or environment variables
- Defining contracts between systems (frontend/backend shared schemas)
- Runtime type checking for data from untrusted sources

**When NOT to use:**

- Internal function parameters (TypeScript is sufficient for trusted data)
- Simple boolean checks that don't need schema definition
- Performance-critical hot paths where validation overhead matters

**Detailed Resources:**

- For code examples, see [examples/](examples/)
- For decision frameworks and anti-patterns, see [reference.md](reference.md)

---

<philosophy>

## Philosophy

TypeScript provides compile-time type safety for code you control. Zod provides **runtime validation** for data you don't control - API responses, user input, configuration files, URL parameters. Use TypeScript for internal contracts; use Zod at **trust boundaries** where external data enters your system.

**Key principle:** Define the schema once, derive the type. Never maintain parallel type definitions and validation logic - they will drift apart.

```typescript
// Schema is the source of truth
const UserSchema = z.object({
  name: z.string(),
  email: z.string().email(),
});

// Type is derived, always in sync
type User = z.infer<typeof UserSchema>;
```

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Schema Definition Basics

Define schemas using Zod's fluent API. Compose complex schemas from primitives.

#### Primitives and Objects

```typescript
import { z } from "zod";

// Validation limits as named constants
const MIN_USERNAME_LENGTH = 3;
const MAX_USERNAME_LENGTH = 50;
const MIN_AGE = 0;
const MAX_AGE = 150;

// ✅ Good Example - Named constants, descriptive error messages
const UserSchema = z.object({
  username: z
    .string()
    .min(
      MIN_USERNAME_LENGTH,
      `Username must be at least ${MIN_USERNAME_LENGTH} characters`,
    )
    .max(
      MAX_USERNAME_LENGTH,
      `Username cannot exceed ${MAX_USERNAME_LENGTH} characters`,
    ),
  email: z.string().email("Invalid email format"),
  age: z
    .number()
    .int("Age must be a whole number")
    .min(MIN_AGE, "Age cannot be negative")
    .max(MAX_AGE, `Age cannot exceed ${MAX_AGE}`),
});

// Derive type from schema
type User = z.infer<typeof UserSchema>;
```

**Why good:** named constants make limits discoverable and maintainable, custom error messages improve UX, type is derived from schema ensuring sync

```typescript
// ❌ Bad Example - Magic numbers, no error messages
const UserSchema = z.object({
  username: z.string().min(3).max(50), // What are these limits?
  email: z.string().email(),
  age: z.number().int().min(0).max(150),
});

// Separate interface duplicates schema
interface User {
  username: string;
  email: string;
  age: number;
}
```

**Why bad:** magic numbers have no context when reading code, parallel interface will drift from schema over time, default error messages are not user-friendly

---

### Pattern 2: Type Inference with z.infer

Use `z.infer` to extract TypeScript types from schemas. Use `z.input` and `z.output` when transforms change the type.

```typescript
import { z } from "zod";

// ✅ Good Example - Type derived from schema
const ProductSchema = z.object({
  id: z.string().uuid(),
  name: z.string(),
  price: z.number().positive(),
  createdAt: z.string().datetime(),
});

// Single source of truth - type always matches schema
type Product = z.infer<typeof ProductSchema>;

// For schemas with transforms, use input/output types
const DateSchema = z.string().transform((str) => new Date(str));

type DateInput = z.input<typeof DateSchema>; // string
type DateOutput = z.output<typeof DateSchema>; // Date
```

**Why good:** type is automatically derived ensuring compile-time and runtime validation match, input/output types handle transform cases correctly

```typescript
// ❌ Bad Example - Manually defining interface
const ProductSchema = z.object({
  id: z.string().uuid(),
  name: z.string(),
  price: z.number().positive(),
});

// Manual interface - can drift from schema
interface Product {
  id: string;
  name: string;
  price: number;
  description?: string; // Added here but not in schema!
}
```

**Why bad:** manual interface has extra field `description` that schema doesn't validate, creating false confidence that data has been validated

---

### Pattern 3: Safe Parsing for Error Handling

Use `safeParse` for graceful error handling. Reserve `parse` for cases where invalid data is a programming error.

```typescript
import { z } from "zod";

const UserSchema = z.object({
  email: z.string().email(),
  name: z.string().min(1),
});

// ✅ Good Example - safeParse with discriminated union result
function validateUserInput(
  data: unknown,
):
  | { success: true; user: User }
  | { success: false; errors: Record<string, string> } {
  const result = UserSchema.safeParse(data);

  if (!result.success) {
    // Format errors for display
    const errors = result.error.errors.reduce(
      (acc, err) => {
        const field = err.path.join(".");
        acc[field] = err.message;
        return acc;
      },
      {} as Record<string, string>,
    );

    return { success: false, errors };
  }

  return { success: true, user: result.data };
}

type User = z.infer<typeof UserSchema>;
```

**Why good:** safeParse never throws so validation errors are handled explicitly, error formatting provides useful feedback, discriminated union return type is type-safe

```typescript
// ❌ Bad Example - Using parse for user input
function validateUserInput(data: unknown) {
  try {
    const user = UserSchema.parse(data); // Throws on invalid!
    return { success: true, user };
  } catch (error) {
    // Generic catch loses type information
    return { success: false, error: "Validation failed" };
  }
}
```

**Why bad:** parse throws exceptions for expected invalid input creating noisy error handling, catch block loses detailed error information, less explicit control flow

---

### Pattern 4: Refinements for Custom Validation

Use `refine` for custom validation logic that primitives can't express. Use `superRefine` for complex cross-field validation.

```typescript
import { z } from "zod";

// ✅ Good Example - Custom refinement with clear error
const PasswordSchema = z
  .string()
  .min(8, "Password must be at least 8 characters")
  .refine((pwd) => /[A-Z]/.test(pwd), {
    message: "Password must contain at least one uppercase letter",
  })
  .refine((pwd) => /[0-9]/.test(pwd), {
    message: "Password must contain at least one number",
  })
  .refine((pwd) => /[!@#$%^&*]/.test(pwd), {
    message: "Password must contain at least one special character (!@#$%^&*)",
  });

// Cross-field validation with superRefine
const PasswordFormSchema = z
  .object({
    password: z.string().min(8),
    confirmPassword: z.string(),
  })
  .superRefine((data, ctx) => {
    if (data.password !== data.confirmPassword) {
      ctx.addIssue({
        code: z.ZodIssueCode.custom,
        message: "Passwords do not match",
        path: ["confirmPassword"],
      });
    }
  });
```

**Why good:** refine allows arbitrary validation logic, custom messages explain exact requirement, superRefine enables cross-field validation with specific error paths

```typescript
// ❌ Bad Example - Validation outside schema
const PasswordSchema = z.string().min(8);

function validatePassword(pwd: string): string[] {
  const errors = [];
  if (!/[A-Z]/.test(pwd)) errors.push("Need uppercase");
  if (!/[0-9]/.test(pwd)) errors.push("Need number");
  return errors;
}

// Now validation is split between schema and function
```

**Why bad:** validation logic is split making it easy to forget one check, errors from function aren't integrated with Zod's error system, harder to compose with other schemas

---

### Pattern 5: Transforms for Data Conversion

Use `transform` to convert data during validation. Input type differs from output type.

```typescript
import { z } from "zod";

// ✅ Good Example - Transform string to Date
const EventSchema = z.object({
  name: z.string(),
  date: z
    .string()
    .datetime()
    .transform((str) => new Date(str)),
  attendees: z.string().transform((str) => parseInt(str, 10)),
});

// Input: { name: string, date: string, attendees: string }
// Output: { name: string, date: Date, attendees: number }
type EventInput = z.input<typeof EventSchema>;
type Event = z.output<typeof EventSchema>;

// Validate then transform
const result = EventSchema.safeParse({
  name: "Conference",
  date: "2025-06-15T09:00:00Z",
  attendees: "150",
});

if (result.success) {
  result.data.date.getFullYear(); // Date methods available
}
```

**Why good:** transform happens after validation ensuring valid input, separate input/output types provide correct typing, common use case for API responses where numbers arrive as strings

---

### Pattern 6: Discriminated Unions for Type Narrowing

Use `discriminatedUnion` when validating objects that share a common discriminator field. Provides better error messages than `union`.

```typescript
import { z } from "zod";

// ✅ Good Example - Discriminated union with clear discriminator
const NotificationSchema = z.discriminatedUnion("type", [
  z.object({
    type: z.literal("email"),
    email: z.string().email(),
    subject: z.string(),
  }),
  z.object({
    type: z.literal("sms"),
    phone: z.string(),
    message: z.string(),
  }),
  z.object({
    type: z.literal("push"),
    deviceId: z.string(),
    title: z.string(),
  }),
]);

type Notification = z.infer<typeof NotificationSchema>;

// Type narrowing works correctly
function sendNotification(notification: Notification) {
  switch (notification.type) {
    case "email":
      // notification.email is available (string)
      break;
    case "sms":
      // notification.phone is available (string)
      break;
    case "push":
      // notification.deviceId is available (string)
      break;
  }
}
```

**Why good:** discriminatedUnion uses the type field to determine which schema to validate against, provides specific error messages about the failing variant, TypeScript narrows type correctly in switch statements

```typescript
// ❌ Bad Example - Plain union without discriminator
const NotificationSchema = z.union([
  z.object({ email: z.string().email(), subject: z.string() }),
  z.object({ phone: z.string(), message: z.string() }),
]);

// Error messages are vague: "Invalid input"
// No type narrowing in code
```

**Why bad:** union tries all schemas and reports combined errors making debugging difficult, no clear way to narrow types in consuming code

---

### Pattern 7: Optional, Nullable, and Nullish

Understand the difference: `optional` allows undefined, `nullable` allows null, `nullish` allows both.

```typescript
import { z } from "zod";

// ✅ Good Example - Explicit null handling
const ProfileSchema = z.object({
  // Required - must be present
  name: z.string(),

  // Optional - can be undefined or omitted entirely
  bio: z.string().optional(), // string | undefined

  // Nullable - must be present but can be null
  avatar: z.string().url().nullable(), // string | null

  // Nullish - can be undefined, null, or omitted
  nickname: z.string().nullish(), // string | null | undefined

  // Default - provides fallback value
  theme: z.string().default("light"), // string (always defined)
});

type Profile = z.infer<typeof ProfileSchema>;
// { name: string; bio?: string; avatar: string | null; nickname?: string | null; theme: string }
```

**Why good:** explicit about what each field accepts, matches common API patterns where null means "explicitly not set" vs undefined means "not provided"

---

### Pattern 8: Coercion for Type Conversion

Use `z.coerce` to convert input types before validation. Useful for form data and URL params that arrive as strings.

```typescript
import { z } from "zod";

// ✅ Good Example - Coerce string inputs to proper types
const PaginationSchema = z.object({
  page: z.coerce.number().int().positive().default(1),
  limit: z.coerce.number().int().positive().max(100).default(20),
  includeDeleted: z.coerce.boolean().default(false),
});

// Works with string inputs from query params
const result = PaginationSchema.parse({
  page: "3", // Coerced to 3
  limit: "50", // Coerced to 50
  includeDeleted: "true", // Coerced to true
});

// result.page is number, not string
```

**Why good:** coerce handles common string-to-type conversions automatically, works with query strings and form data, default values provide sensible fallbacks

```typescript
// ❌ Bad Example - Manual parsing before validation
const page = parseInt(queryParams.page, 10);
const limit = parseInt(queryParams.limit, 10);

// Validation is separate from parsing
if (isNaN(page) || page < 1) {
  // Handle error
}
```

**Why bad:** parsing and validation are split across multiple statements, error handling is manual and verbose, easy to forget edge cases like NaN

---

### Pattern 9: Schema Composition and Extension

Compose schemas using `extend`, `merge`, `pick`, `omit`, and `partial` for reusability.

```typescript
import { z } from "zod";

// Base schema
const BaseEntitySchema = z.object({
  id: z.string().uuid(),
  createdAt: z.string().datetime(),
  updatedAt: z.string().datetime(),
});

// ✅ Good Example - Extend base schema
const UserSchema = BaseEntitySchema.extend({
  email: z.string().email(),
  name: z.string(),
});

// Pick specific fields for API response
const UserSummarySchema = UserSchema.pick({
  id: true,
  name: true,
});

// Omit sensitive fields
const PublicUserSchema = UserSchema.omit({
  email: true,
});

// Partial for updates (all fields optional)
const UpdateUserSchema = UserSchema.partial().omit({
  id: true,
  createdAt: true,
  updatedAt: true,
});

// Merge two schemas
const UserWithPrefsSchema = UserSchema.merge(
  z.object({
    preferences: z.object({
      theme: z.string(),
      language: z.string(),
    }),
  }),
);
```

**Why good:** DRY schemas avoid duplication, pick/omit create focused schemas for specific use cases, partial enables PATCH-style updates

---

### Pattern 10: Async Validation

Use `refine` with async functions for validations that require network calls. Use `safeParseAsync`.

```typescript
import { z } from "zod";

// ✅ Good Example - Async refinement for uniqueness check
const RegistrationSchema = z.object({
  email: z.string().email(),
  username: z
    .string()
    .min(3)
    .refine(
      async (username) => {
        // Check if username is available (async operation)
        const isAvailable = await checkUsernameAvailability(username);
        return isAvailable;
      },
      { message: "Username is already taken" },
    ),
});

// MUST use async parse methods
async function validateRegistration(data: unknown) {
  const result = await RegistrationSchema.safeParseAsync(data);

  if (!result.success) {
    return { errors: result.error.flatten().fieldErrors };
  }

  return { user: result.data };
}
```

**Why good:** async refinement integrates network validation into schema, safeParseAsync handles async properly, validation logic is centralized

**When to use:** Database uniqueness checks, external API validation, permission checks requiring network calls

</patterns>

---

<integration>

## Integration Guide

**Zod is a standalone validation library.** It validates data and infers types. How you use the validated data depends on your form library, API layer, or database.

**Integration points:**

- Form validation: Schemas integrate via resolver patterns (see form library skill)
- API responses: Use schemas to validate and type response data
- Configuration: Validate environment variables and config files
- URL parameters: Use coercion for query string parsing

**Zod handles validation only.** For form state, API calls, or database operations, use the appropriate skill.

</integration>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md**

**(You MUST use `safeParse` instead of `parse` for user-facing validation - prevents unhandled exceptions)**

**(You MUST use `z.infer<typeof schema>` to derive types - never duplicate schema as separate interface)**

**(You MUST validate at trust boundaries - API responses, form inputs, config files, URL params)**

**(You MUST use named constants for validation limits - NO magic numbers in `.min()`, `.max()`, `.length()`)**

**Failure to follow these rules will create type mismatches, unhandled exceptions, and unmaintainable validation code.**

</critical_reminders>
