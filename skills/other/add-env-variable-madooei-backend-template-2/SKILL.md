---
name: add-env-variable
description: Add a new environment variable to the application. Use when adding configuration for external services, feature flags, or application settings. Triggers on "add env", "environment variable", "config variable".
---

# Add Environment Variable

Adds a new environment variable with Zod validation. All environment variables must be defined in `src/env.ts` and documented in `.env.example`.

## Quick Reference

**Files to modify**:

1. `src/env.ts` - Add to schema and mapping
2. `.env.example` - Document the variable
3. `tests/env.test.ts` - Add validation tests

## Instructions

### Step 1: Add to Schema in `src/env.ts`

Add the variable to the `envSchema` object:

```typescript
const envSchema = z.object({
  // ... existing variables ...

  // Your new variable (with comment explaining purpose)
  NEW_VARIABLE: z.string(), // Required string
  // OR
  NEW_VARIABLE: z.string().optional(), // Optional string
  // OR
  NEW_VARIABLE: z.string().default("default-value"), // With default
  // OR
  NEW_VARIABLE: z.coerce.number().default(3000), // Number with coercion
  // OR
  NEW_VARIABLE: z.string().url(), // URL validation
});
```

### Step 2: Add to Mapping Object

Add the variable to `mappedEnv` using the `getEnv()` helper (which reads prefixed variables):

```typescript
const mappedEnv = {
  // ... existing mappings ...
  NEW_VARIABLE: getEnv("NEW_VARIABLE"),
};
```

### Step 3: Document in `.env.example`

Add the variable with a descriptive comment, using the prefix (default: `BT_`):

```bash
# Description of what this variable is for
BT_NEW_VARIABLE=example-value
```

> **Note**: The prefix is defined in `src/env.ts` as `const PREFIX = "BT"`. Change this when creating a new service from the template.

### Step 4: Add Tests in `tests/env.test.ts`

Add test cases for the new variable:

```typescript
it("accepts valid NEW_VARIABLE", () => {
  const parsed = envSchema.parse({ NEW_VARIABLE: "valid-value" });
  expect(parsed.NEW_VARIABLE).toBe("valid-value");
});

it("defaults NEW_VARIABLE if missing", () => {
  const parsed = envSchema.parse({});
  expect(parsed.NEW_VARIABLE).toBe("default-value");
});

// OR for optional
it("accepts missing NEW_VARIABLE", () => {
  const parsed = envSchema.parse({});
  expect(parsed.NEW_VARIABLE).toBeUndefined();
});

// OR for required
it("rejects missing NEW_VARIABLE", () => {
  expect(() => envSchema.parse({})).toThrow();
});
```

## Common Patterns

All examples use the `getEnv()` helper and `BT_` prefix:

### Required String

```typescript
// Schema
MY_API_KEY: z.string(),

// Mapping
MY_API_KEY: getEnv("MY_API_KEY"),

// .env.example
BT_MY_API_KEY=your-api-key-here
```

### Optional String

```typescript
// Schema
OPTIONAL_FEATURE: z.string().optional(),

// Mapping
OPTIONAL_FEATURE: getEnv("OPTIONAL_FEATURE"),

// .env.example
# Optional: Enable feature X
# BT_OPTIONAL_FEATURE=enabled
```

### String with Default

```typescript
// Schema
LOG_LEVEL: z.string().default("info"),

// Mapping
LOG_LEVEL: getEnv("LOG_LEVEL"),

// .env.example
BT_LOG_LEVEL=info
```

### Number with Coercion

```typescript
// Schema
RATE_LIMIT: z.coerce.number().default(100),

// Mapping
RATE_LIMIT: getEnv("RATE_LIMIT"),

// .env.example
BT_RATE_LIMIT=100
```

### URL Validation

```typescript
// Schema
WEBHOOK_URL: z.string().url().optional(),

// Mapping
WEBHOOK_URL: getEnv("WEBHOOK_URL"),

// .env.example
# Webhook endpoint for notifications
BT_WEBHOOK_URL=https://example.com/webhook
```

### Enum Values

```typescript
// Schema
NODE_ENV: z.enum(["development", "test", "production"]).default("development"),

// Mapping
NODE_ENV: getEnv("NODE_ENV"),

// .env.example
BT_NODE_ENV=development
```

### Boolean (as string)

```typescript
// Schema
ENABLE_FEATURE: z.string().transform(v => v === "true").default("false"),

// Mapping
ENABLE_FEATURE: getEnv("ENABLE_FEATURE"),

// .env.example
BT_ENABLE_FEATURE=false
```

## Usage in Code

Always import from `@/env`, never use `process.env` directly:

```typescript
import { env } from "@/env";

// Correct
const apiKey = env.MY_API_KEY;

// Wrong - bypasses validation
const apiKey = process.env.MY_API_KEY;
```

## Full Example: Adding Email Service Config

### 1. Update `src/env.ts`

```typescript
const envSchema = z.object({
  // ... existing ...

  // Email service configuration
  EMAIL_API_KEY: z.string().optional(),
  EMAIL_FROM_ADDRESS: z.string().email().optional(),
  EMAIL_PROVIDER: z.enum(["sendgrid", "mailgun"]).default("sendgrid"),
});

const mappedEnv = {
  // ... existing ...
  EMAIL_API_KEY: getEnv("EMAIL_API_KEY"),
  EMAIL_FROM_ADDRESS: getEnv("EMAIL_FROM_ADDRESS"),
  EMAIL_PROVIDER: getEnv("EMAIL_PROVIDER"),
};
```

### 2. Update `.env.example`

```bash
# Email service configuration
BT_EMAIL_API_KEY=your-email-api-key
BT_EMAIL_FROM_ADDRESS=noreply@example.com
BT_EMAIL_PROVIDER=sendgrid
```

### 3. Update `tests/env.test.ts`

```typescript
it("accepts valid email configuration", () => {
  const parsed = envSchema.parse({
    EMAIL_API_KEY: "test-key",
    EMAIL_FROM_ADDRESS: "test@example.com",
    EMAIL_PROVIDER: "mailgun",
  });
  expect(parsed.EMAIL_API_KEY).toBe("test-key");
  expect(parsed.EMAIL_FROM_ADDRESS).toBe("test@example.com");
  expect(parsed.EMAIL_PROVIDER).toBe("mailgun");
});

it("defaults EMAIL_PROVIDER to sendgrid", () => {
  const parsed = envSchema.parse({});
  expect(parsed.EMAIL_PROVIDER).toBe("sendgrid");
});

it("rejects invalid EMAIL_FROM_ADDRESS", () => {
  expect(() =>
    envSchema.parse({ EMAIL_FROM_ADDRESS: "not-an-email" }),
  ).toThrow();
});

it("rejects invalid EMAIL_PROVIDER", () => {
  expect(() => envSchema.parse({ EMAIL_PROVIDER: "invalid" })).toThrow();
});
```

## What NOT to Do

- Do NOT use `process.env` directly in application code
- Do NOT forget to add the mapping in `mappedEnv`
- Do NOT skip documenting in `.env.example`
- Do NOT skip adding tests for validation rules
- Do NOT store secrets in `.env.example` (use placeholder values)

## See Also

- `create-utility-service` - Services that use environment config
- `test-schema` - Testing Zod schemas (similar patterns)
