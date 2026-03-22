---
name: arktype
description: >-
  Define runtime-validated types with ArkType — TypeScript's 1:1 validator.
  Use when someone asks to "validate data in TypeScript", "runtime type
  checking", "ArkType", "type-safe validation", "alternative to Zod", "faster
  validation library", or "validate with TypeScript syntax". Covers type
  definitions, validation, morphs (transforms), scopes, and comparison with Zod.
license: Apache-2.0
compatibility: "TypeScript 5.1+. Node.js/Bun/Deno/browser."
metadata:
  author: terminal-skills
  version: "1.0.0"
  category: development
  tags: ["validation", "typescript", "arktype", "runtime-types", "schema"]
---

# ArkType

## Overview

ArkType is a runtime validation library that uses TypeScript's own syntax for type definitions. Instead of learning a new API (`z.string().email()`), you write types the way you already know (`"string.email"`). It's the fastest TypeScript validator — 100x faster than Zod for complex schemas — with better error messages and 1:1 correspondence between your types and validators.

## When to Use

- Runtime validation where performance matters (hot paths, large payloads)
- Want to write validators using TypeScript syntax (not a builder API)
- Need detailed, human-readable error messages
- Replacing Zod in performance-critical applications
- Type-safe data transformations (morphs)

## Instructions

### Setup

```bash
npm install arktype
```

### Basic Types

```typescript
// types.ts — Define types using TypeScript syntax
import { type } from "arktype";

// String with constraints
const email = type("string.email");
const result = email("user@example.com");  // "user@example.com"
const error = email("not-an-email");       // ArkErrors: must be an email address

// Object types — looks like TypeScript
const User = type({
  name: "string >= 2",            // String with min length 2
  email: "string.email",
  age: "number.integer >= 13",    // Integer, min 13
  role: "'admin' | 'user'",       // Literal union
  "bio?": "string <= 500",        // Optional, max 500 chars
});

// Infer the TypeScript type — no separate interface needed
type User = typeof User.infer;
// { name: string; email: string; age: number; role: "admin" | "user"; bio?: string }

// Validate
const valid = User({
  name: "Kai",
  email: "kai@example.com",
  age: 25,
  role: "user",
});

if (valid instanceof type.errors) {
  console.log(valid.summary);  // Human-readable error message
} else {
  console.log(valid.name);     // Typed as User
}
```

### Arrays and Nested Types

```typescript
// complex.ts — Complex nested types
import { type } from "arktype";

const Address = type({
  street: "string",
  city: "string",
  zip: "string.numeric",      // Numeric string
  country: "string == 2",     // Exactly 2 characters (ISO code)
});

const Order = type({
  id: "string.uuid",
  items: type({
    productId: "string",
    quantity: "number.integer > 0",
    price: "number > 0",
  }).array(),                   // Array of items
  shippingAddress: Address,
  total: "number > 0",
  status: "'pending' | 'shipped' | 'delivered'",
  createdAt: "Date",
});

type Order = typeof Order.infer;
```

### Morphs (Transforms)

```typescript
// morphs.ts — Transform data during validation
import { type } from "arktype";

// Parse string to number
const numericString = type("string.numeric").pipe((s) => Number(s));
numericString("42");  // 42 (number)

// Parse and transform API input
const CreateUserInput = type({
  name: "string.trim",                          // Auto-trim
  email: type("string.email").pipe((e) => e.toLowerCase()),  // Lowercase
  age: type("string.numeric").pipe(Number),     // String → number
  tags: type("string").pipe((s) => s.split(",")), // "a,b,c" → ["a","b","c"]
});
```

### Scopes (Reusable Type Systems)

```typescript
// scope.ts — Define interconnected types
import { scope } from "arktype";

const types = scope({
  user: {
    id: "string.uuid",
    name: "string >= 2",
    email: "string.email",
    posts: "post[]",
  },
  post: {
    id: "string.uuid",
    title: "string >= 1",
    content: "string",
    author: "user",            // Recursive reference
    tags: "string[]",
  },
}).export();

const user = types.user(data);
```

## Examples

### Example 1: Validate API request bodies

**User prompt:** "Validate incoming POST requests in my Express API with clear error messages."

The agent will define ArkType schemas for each endpoint's body, create validation middleware, and return structured error responses.

### Example 2: Replace Zod with ArkType

**User prompt:** "My Zod validation is slow on large payloads. Switch to something faster."

The agent will translate Zod schemas to ArkType syntax, update validation middleware, and benchmark the improvement.

## Guidelines

- **TypeScript syntax** — `"string.email"` not `z.string().email()`
- **`type.errors` for error checking** — `result instanceof type.errors`
- **`.infer` for TypeScript type** — no duplicate interface definitions
- **Morphs for transforms** — `.pipe()` to transform during validation
- **Scopes for complex schemas** — define interconnected types with forward references
- **100x faster than Zod** — matters for hot paths and large payloads
- **Error messages are human-readable** — `result.summary` for display
- **`?` suffix for optional** — `"bio?": "string"` makes bio optional
- **Constraints in the type** — `"number >= 0 < 100"` is a range
- **Not as battle-tested as Zod** — newer library, smaller ecosystem
