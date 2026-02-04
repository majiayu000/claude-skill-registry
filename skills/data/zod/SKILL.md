---
name: "Zod v4"
description: "TypeScript-first schema validation library with static type inference and runtime validation"
when_to_use: "When you need robust data validation, type safety, schema definitions, or input validation in TypeScript/JavaScript applications"
---

# Zod v4 - Schema Validation Skill

Zod v4 is a TypeScript-first schema declaration and validation library that provides static type inference, runtime validation, and exceptional performance. Version 4 delivers 14x faster parsing and 66% smaller bundles while maintaining full type safety.

## Quick Start

```bash
npm install zod@^4.0.0
```

```typescript
import * as z from "zod";

// Basic schema creation and validation
const UserSchema = z.object({
  id: z.number().int().positive(),
  email: z.email(),
  username: z.string().min(3).max(20),
  age: z.number().int().min(18).optional(),
});

type User = z.infer<typeof UserSchema>;

// Parse and validate
const user = UserSchema.parse({
  id: 1,
  email: "user@example.com",
  username: "johndoe",
  age: 25,
});

// Safe parsing with error handling
const result = UserSchema.safeParse(input);
if (!result.success) {
  console.log(result.error);
}
```

## Common Patterns

### Object Schemas with Validation

```typescript
// Comprehensive user validation
const UserProfile = z.object({
  id: z.number().int().positive(),
  email: z.email(),
  username: z
    .string()
    .min(3, "Username must be at least 3 characters")
    .max(20, "Username cannot exceed 20 characters")
    .regex(/^[a-zA-Z0-9_]+$/, "Only alphanumeric characters and underscores"),
  age: z.number().int().min(13).max(120),
  role: z.enum(["user", "admin", "moderator"]).default("user"),
  bio: z.string().max(500).optional(),
  website: z.url().optional(),
  createdAt: z.date().default(() => new Date()),
});

// Extending schemas
const AdminProfile = UserProfile.extend({
  permissions: z.array(z.string()),
  accessLevel: z.number().min(1).max(10),
});
```

### String Format Validation

```typescript
// Built-in format validators
const Validations = {
  email: z.email(),
  uuid: z.uuidv4(),
  url: z.url(),
  ipv4: z.ipv4(),
  ipv6: z.ipv6(),
  base64: z.base64(),
  jwt: z.jwt(),

  // ISO formats
  isoDate: z.iso.date(),
  isoDateTime: z.iso.datetime(),
  isoTime: z.iso.time(),

  // Custom email with specific pattern
  strictEmail: z.email({ pattern: z.regexes.rfc5322Email }),
};

// Template literal validation
const VersionString = z.templateLiteral([
  z.number(),
  ".",
  z.number(),
  ".",
  z.number(),
]);

const CSSValue = z.templateLiteral([
  z.number(),
  z.enum(["px", "em", "rem", "%", "vh", "vw"]),
]);
```

### Array and Collection Validation

```typescript
// Array with constraints
const NumberArray = z.array(z.number()).min(1).max(100);

// Tuple validation
const Coordinates = z.tuple([z.number(), z.number()]);
const MixedTuple = z.tuple([z.string(), z.number()], z.boolean());

// Set validation
const UniqueStrings = z.set(z.string()).min(3);

// Map validation
const UserPermissions = z.map(
  z.string(), // user ID
  z.array(z.string()), // permissions
);

// Record validation
const StringToNumber = z.record(z.string(), z.number());
const StatusRecord = z.record(
  z.enum(["pending", "active", "complete"]),
  z.boolean(),
);
```

### Union and Discriminated Unions

```typescript
// Simple union
const StringOrNumber = z.union([z.string(), z.number()]);

// Discriminated union for API responses
const ApiResponse = z.discriminatedUnion("status", [
  z.object({
    status: z.literal("success"),
    data: z.unknown(),
  }),
  z.object({
    status: z.literal("error"),
    error: z.string(),
    code: z.number(),
  }),
  z.object({
    status: z.literal("loading"),
    message: z.string().optional(),
  }),
]);

// Nested discriminated unions
const BaseError = z.object({
  status: z.literal("error"),
  message: z.string(),
});

const DetailedError = z.discriminatedUnion("code", [
  BaseError.extend({ code: z.literal(400), field: z.string() }),
  BaseError.extend({ code: z.literal(401), realm: z.string() }),
  BaseError.extend({ code: z.literal(500), stack: z.string() }),
]);
```

### Custom Refinements and Validation

```typescript
// Custom validation with refinements
const PasswordSchema = z
  .string()
  .min(8, "Password must be at least 8 characters")
  .refine((val) => /[A-Z]/.test(val), "Must contain uppercase letter")
  .refine((val) => /[a-z]/.test(val), "Must contain lowercase letter")
  .refine((val) => /[0-9]/.test(val), "Must contain number")
  .refine((val) => /[^A-Za-z0-9]/.test(val), "Must contain special character");

// Complex validation with superRefine
const UserRegistration = z
  .object({
    email: z.email(),
    password: z.string(),
    confirmPassword: z.string(),
    age: z.number(),
    termsAccepted: z.boolean(),
  })
  .superRefine((data, ctx) => {
    if (data.password !== data.confirmPassword) {
      ctx.addIssue({
        code: "custom",
        path: ["confirmPassword"],
        message: "Passwords must match",
      });
    }

    if (data.age < 18 && !data.termsAccepted) {
      ctx.addIssue({
        code: "custom",
        path: ["termsAccepted"],
        message: "Parental consent required for users under 18",
      });
    }
  });
```

### Transformations and Data Processing

```typescript
// Transform data during validation
const StringToNumber = z
  .string()
  .transform((val) => parseInt(val, 10))
  .refine((val) => !isNaN(val), "Must be a valid number");

const TimestampToDate = z
  .number()
  .transform((timestamp) => new Date(timestamp));

const NormalizeEmail = z.string().transform((val) => val.toLowerCase().trim());

// Overwrite for type-preserving transforms
const RoundNumber = z.number().overwrite((val) => Math.round(val));

// Pipeline transformations
const ProcessUrl = z
  .string()
  .transform((val) => val.trim())
  .transform((val) => val.toLowerCase())
  .transform((val) => {
    try {
      return new URL(val);
    } catch {
      throw new Error("Invalid URL format");
    }
  });
```

### Recursive Schemas

```typescript
// Recursive category structure
const Category = z.object({
  id: z.number(),
  name: z.string(),
  get subcategories() {
    return z.array(Category);
  },
});

// Mutually recursive types
const User = z.object({
  id: z.number(),
  name: z.string(),
  get posts() {
    return z.array(Post);
  },
});

const Post = z.object({
  id: z.number(),
  title: z.string(),
  content: z.string(),
  get author() {
    return User;
  },
  get comments() {
    return z.array(Comment);
  },
});

const Comment = z.object({
  id: z.number(),
  text: z.string(),
  get author() {
    return User.pick({ id: true, name: true });
  },
});
```

### File Validation

```typescript
// File upload validation
const ImageUpload = z.object({
  avatar: z
    .file()
    .max(5_000_000, "File must be less than 5MB")
    .mime(["image/jpeg", "image/png", "image/webp"], "Must be an image"),

  banner: z
    .file()
    .max(10_000_000, "File must be less than 10MB")
    .mime(["image/jpeg", "image/png"], "Must be JPEG or PNG")
    .optional(),
});

// Document validation
const DocumentUpload = z
  .file()
  .min(1000, "File must be at least 1KB")
  .max(50_000_000, "File must be less than 50MB")
  .mime([
    "application/pdf",
    "application/msword",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
  ]);
```

### Function Validation

```typescript
// Define validated functions
const CalculateTax = z.function({
  input: [z.number().min(0), z.number().min(0).max(1)],
  output: z.number(),
});

const taxCalculator = CalculateTax.implement((amount, rate) => {
  return amount * rate;
});

// Async function validation
const FetchUser = z.function({
  input: [z.number().int().positive()],
  output: z.object({
    id: z.number(),
    name: z.string(),
    email: z.email(),
  }),
});

const getUser = FetchUser.implementAsync(async (id) => {
  const response = await fetch(`/api/users/${id}`);
  return response.json();
});
```

### Error Handling

```typescript
// Custom error messages
const CustomValidation = z.object({
  username: z
    .string({
      error: (issue) => {
        if (issue.input === undefined) return "Username is required";
        if (typeof issue.input !== "string") return "Username must be a string";
        return "Invalid username";
      },
    })
    .min(3, "Username must be at least 3 characters"),
});

// Error handling patterns
const validateInput = (input: unknown) => {
  const result = UserSchema.safeParse(input);

  if (!result.success) {
    const error = result.error;

    // Pretty print errors
    console.log(z.prettifyError(error));

    // Extract field errors
    const fieldErrors = error.issues.reduce(
      (acc, issue) => {
        const field = issue.path.join(".");
        acc[field] = issue.message;
        return acc;
      },
      {} as Record<string, string>,
    );

    return { success: false, errors: fieldErrors };
  }

  return { success: true, data: result.data };
};
```

### Default Values and Coercion

```typescript
// Schema with defaults
const ConfigSchema = z.object({
  theme: z.enum(["light", "dark"]).default("light"),
  notifications: z.boolean().default(true),
  fontSize: z.number().min(10).max(30).default(14),
  timeout: z.number().default(5000),
});

// Type coercion
const CoercedConfig = z.object({
  port: z.coerce.number().default(3000),
  https: z.coerce.boolean().default(false),
  maxConnections: z.coerce.number().int().positive().default(100),
});

// Environment variable parsing
const EnvSchema = z.object({
  NODE_ENV: z
    .enum(["development", "production", "test"])
    .default("development"),
  PORT: z.coerce.number().default(3000),
  DEBUG: z.stringbool().default("false"),
});
```

### Zod Mini (Tree-Shakable)

```typescript
import * as z from "zod/mini";

// Functional API for smaller bundles
const OptionalString = z.optional(z.string());
const StringArray = z.array(z.string());
const StringOrNumber = z.union([z.string(), z.number()]);

// Check functions for validations
const ValidatedEmail = z
  .string()
  .check(z.regex(/@/), z.minLength(5), z.maxLength(100));

const PositiveInt = z.number().check(z.int(), z.positive(), z.lt(1000));

const NonEmptyArray = z.array(z.any()).check(z.minSize(1));
```

## Practical Examples

### Form Validation

```typescript
// Contact form validation
const ContactForm = z.object({
  name: z.string().min(1, "Name is required").max(100),
  email: z.email("Please provide a valid email"),
  subject: z.string().min(5, "Subject must be at least 5 characters"),
  message: z.string().min(10, "Message must be at least 10 characters"),
  newsletter: z.boolean().default(false),
});

// React form integration
const handleSubmit = (formData: FormData) => {
  const data = {
    name: formData.get("name"),
    email: formData.get("email"),
    subject: formData.get("subject"),
    message: formData.get("message"),
    newsletter: formData.get("newsletter") === "on",
  };

  const result = ContactForm.safeParse(data);
  if (!result.success) {
    const errors = result.error.flatten();
    return { errors: errors.fieldErrors };
  }

  // Process valid data
  return { success: true, data: result.data };
};
```

### API Response Validation

```typescript
// API response schemas
const UserResponse = z.object({
  data: z.object({
    id: z.number(),
    name: z.string(),
    email: z.email(),
    createdAt: z.string().transform((val) => new Date(val)),
  }),
  meta: z.object({
    total: z.number(),
    page: z.number(),
    totalPages: z.number(),
  }),
});

// Typed API client
const apiClient = {
  async getUser(id: number): Promise<z.infer<typeof UserResponse>["data"]> {
    const response = await fetch(`/api/users/${id}`);
    const data = await response.json();

    const result = UserResponse.safeParse(data);
    if (!result.success) {
      throw new Error(`Invalid API response: ${result.error.message}`);
    }

    return result.data.data;
  },
};
```

### Configuration Validation

```typescript
// Application configuration
const AppConfig = z.object({
  server: z.object({
    port: z.coerce.number().min(1).max(65535).default(3000),
    host: z.string().default("localhost"),
    cors: z.boolean().default(true),
  }),
  database: z.object({
    url: z.string(),
    ssl: z.boolean().default(false),
    maxConnections: z.coerce.number().int().positive().default(10),
  }),
  auth: z.object({
    jwtSecret: z.string().min(32),
    tokenExpiry: z.string().default("24h"),
    refreshExpiry: z.string().default("7d"),
  }),
});

// Load and validate config
const loadConfig = (configPath: string) => {
  const rawConfig = require(configPath);
  const config = AppConfig.parse(rawConfig);
  return config;
};
```

## Requirements

- **TypeScript**: 4.5+ (recommended for best inference)
- **Runtime**: Node.js, browsers, Deno, Bun
- **Bundle size**: 5.36kb gzipped (full), 1.88kb gzipped (mini)

## Installation

```bash
# Full Zod v4
npm install zod@^4.0.0

# For minimal bundle size
npm install zod@^4.0.0
# Then import from "zod/mini"
```

## Key Features

- **Static Type Inference**: Automatic TypeScript type generation from schemas
- **Runtime Validation**: Comprehensive input validation with detailed errors
- **Performance**: 14x faster parsing than v3, optimized for production
- **Tree Shakable**: Zod Mini provides 85% bundle size reduction
- **Template Literals**: Validate string patterns matching TypeScript template literals
- **File Validation**: Built-in File object validation with size and MIME type constraints
- **Recursive Types**: Full support for recursive and self-referential schemas
- **JSON Schema**: First-party JSON Schema generation
- **Function Validation**: Type-safe function definitions with validated inputs/outputs
