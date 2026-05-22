---
name: zod-validation
description: Runtime type validation with Zod for schema definition, form validation, API contracts, and TypeScript type inference. Use when validating user input, defining API schemas, or building type-safe data pipelines.
---

# Zod Validation Skill

> TypeScript-first schema validation with static type inference

## Quick Reference

```typescript
import { z } from "zod";

// Define schema
const UserSchema = z.object({
  id: z.string().uuid(),
  email: z.string().email(),
  age: z.number().min(18).optional(),
});

// Infer TypeScript type
type User = z.infer<typeof UserSchema>;

// Validate data
const result = UserSchema.safeParse(data);
if (result.success) {
  console.log(result.data); // Typed as User
} else {
  console.log(result.error.issues);
}
```

---

## Schema Primitives

### Basic Types

```typescript
// Strings
z.string();
z.string().min(1); // Non-empty
z.string().max(100);
z.string().length(5);
z.string().email();
z.string().url();
z.string().uuid();
z.string().cuid();
z.string().regex(/^[a-z]+$/);
z.string().startsWith("https://");
z.string().endsWith(".com");
z.string().trim(); // Trims whitespace
z.string().toLowerCase();
z.string().toUpperCase();

// Numbers
z.number();
z.number().int();
z.number().positive();
z.number().negative();
z.number().nonnegative();
z.number().min(0);
z.number().max(100);
z.number().multipleOf(5);
z.number().finite();
z.number().safe(); // Number.MIN_SAFE_INTEGER to MAX_SAFE_INTEGER

// Booleans
z.boolean();

// Dates
z.date();
z.date().min(new Date("2020-01-01"));
z.date().max(new Date());

// Special types
z.undefined();
z.null();
z.void();
z.any();
z.unknown();
z.never();
z.nan();
```

### Literals and Enums

```typescript
// Literals
const StatusLiteral = z.literal("active");
const CodeLiteral = z.literal(200);

// Native enums
enum Role {
  Admin = "admin",
  User = "user",
}
const RoleSchema = z.nativeEnum(Role);

// Zod enums (preferred)
const StatusEnum = z.enum(["pending", "active", "archived"]);
type Status = z.infer<typeof StatusEnum>; // "pending" | "active" | "archived"

// Extract enum values
StatusEnum.options; // ["pending", "active", "archived"]
StatusEnum.enum.pending; // "pending"
```

---

## Object Schemas

### Basic Objects

```typescript
const UserSchema = z.object({
  id: z.string(),
  name: z.string(),
  email: z.string().email(),
  age: z.number().optional(),
  role: z.enum(["admin", "user"]).default("user"),
});

type User = z.infer<typeof UserSchema>;
// { id: string; name: string; email: string; age?: number; role: "admin" | "user" }
```

### Object Modifiers

```typescript
const BaseSchema = z.object({
  id: z.string(),
  name: z.string(),
  email: z.string(),
  password: z.string(),
});

// Partial - all fields optional
const PartialUser = BaseSchema.partial();

// Required - all fields required
const RequiredUser = BaseSchema.required();

// Pick specific fields
const UserCredentials = BaseSchema.pick({ email: true, password: true });

// Omit fields
const PublicUser = BaseSchema.omit({ password: true });

// Extend with new fields
const AdminSchema = BaseSchema.extend({
  permissions: z.array(z.string()),
});

// Merge two schemas
const MergedSchema = BaseSchema.merge(z.object({ createdAt: z.date() }));

// Make specific fields optional
const CreateUserSchema = BaseSchema.partial({ id: true });

// Strict mode - fail on unknown keys
const StrictSchema = BaseSchema.strict();

// Passthrough - allow unknown keys
const PassthroughSchema = BaseSchema.passthrough();

// Strip unknown keys (default behavior)
const StrippedSchema = BaseSchema.strip();
```

### Nested Objects

```typescript
const AddressSchema = z.object({
  street: z.string(),
  city: z.string(),
  zipCode: z.string().regex(/^\d{5}$/),
  country: z.string().default("US"),
});

const CompanySchema = z.object({
  name: z.string(),
  address: AddressSchema,
  employees: z.array(UserSchema),
});

type Company = z.infer<typeof CompanySchema>;
```

---

## Arrays, Tuples, and Records

### Arrays

```typescript
// Basic array
const StringArray = z.array(z.string());

// Array with constraints
const NonEmptyArray = z.array(z.number()).nonempty();
const LimitedArray = z.array(z.string()).min(1).max(10);

// Array of objects
const UsersArray = z.array(UserSchema);

// Set (unique values)
const UniqueStrings = z.set(z.string());
```

### Tuples

```typescript
// Fixed-length array with specific types
const CoordinateTuple = z.tuple([z.number(), z.number()]);
type Coordinate = z.infer<typeof CoordinateTuple>; // [number, number]

// Tuple with rest elements
const NamedCoordinate = z.tuple([z.string(), z.number(), z.number()]);
// ["label", x, y]

// Variadic tuples
const AtLeastTwo = z.tuple([z.string(), z.string()]).rest(z.string());
```

### Records and Maps

```typescript
// Record with string keys
const StringRecord = z.record(z.string(), z.number());
type StringToNumber = z.infer<typeof StringRecord>; // Record<string, number>

// Record with enum keys
const RolePermissions = z.record(
  z.enum(["admin", "user", "guest"]),
  z.array(z.string()),
);

// Map type
const UserMap = z.map(z.string(), UserSchema);
```

---

## Unions and Discriminated Unions

### Basic Unions

```typescript
// Simple union
const StringOrNumber = z.union([z.string(), z.number()]);
// Shorthand
const StringOrNumberAlt = z.string().or(z.number());

// Nullable (T | null)
const NullableString = z.string().nullable();

// Nullish (T | null | undefined)
const NullishString = z.string().nullish();

// Optional (T | undefined)
const OptionalString = z.string().optional();
```

### Discriminated Unions

```typescript
// Best for API responses and state machines
const ResultSchema = z.discriminatedUnion("status", [
  z.object({
    status: z.literal("success"),
    data: z.object({ id: z.string(), name: z.string() }),
  }),
  z.object({
    status: z.literal("error"),
    error: z.object({ code: z.number(), message: z.string() }),
  }),
]);

type Result = z.infer<typeof ResultSchema>;

// Usage
function handleResult(result: Result) {
  if (result.status === "success") {
    console.log(result.data.name); // TypeScript knows data exists
  } else {
    console.log(result.error.message); // TypeScript knows error exists
  }
}

// API response pattern
const ApiResponseSchema = z.discriminatedUnion("type", [
  z.object({ type: z.literal("user"), user: UserSchema }),
  z.object({ type: z.literal("users"), users: z.array(UserSchema) }),
  z.object({ type: z.literal("error"), message: z.string() }),
]);
```

---

## Refinements and Transforms

### Refinements (Custom Validation)

```typescript
// Simple refinement
const PositiveNumber = z.number().refine((n) => n > 0, {
  message: "Number must be positive",
});

// Refinement with path
const PasswordSchema = z
  .object({
    password: z.string().min(8),
    confirmPassword: z.string(),
  })
  .refine((data) => data.password === data.confirmPassword, {
    message: "Passwords don't match",
    path: ["confirmPassword"], // Error appears on this field
  });

// Async refinement
const UniqueEmailSchema = z
  .string()
  .email()
  .refine(
    async (email) => {
      const exists = await checkEmailExists(email);
      return !exists;
    },
    { message: "Email already registered" },
  );

// Super refine for complex validation
const ComplexSchema = z
  .object({
    type: z.enum(["personal", "business"]),
    taxId: z.string().optional(),
  })
  .superRefine((data, ctx) => {
    if (data.type === "business" && !data.taxId) {
      ctx.addIssue({
        code: z.ZodIssueCode.custom,
        message: "Tax ID required for business accounts",
        path: ["taxId"],
      });
    }
  });
```

### Transforms

```typescript
// Transform string to number
const StringToNumber = z.string().transform((val) => parseInt(val, 10));

// Transform with validation
const SafeStringToNumber = z
  .string()
  .transform((val) => parseInt(val, 10))
  .refine((n) => !isNaN(n), { message: "Invalid number" });

// Pipe for transform + validate
const NumberFromString = z
  .string()
  .transform((val) => parseInt(val, 10))
  .pipe(z.number().min(0).max(100));

// Default values
const WithDefault = z.string().default("unknown");
const WithDefaultFn = z.date().default(() => new Date());

// Catch (use default on parse failure)
const SafeNumber = z.number().catch(0);
const SafeString = z.string().catch("fallback");

// Preprocess (run before parsing)
const TrimmedString = z.preprocess(
  (val) => (typeof val === "string" ? val.trim() : val),
  z.string(),
);
```

---

## Coercion

```typescript
// Automatic type coercion
const CoercedString = z.coerce.string(); // Calls String(value)
const CoercedNumber = z.coerce.number(); // Calls Number(value)
const CoercedBoolean = z.coerce.boolean(); // Calls Boolean(value)
const CoercedDate = z.coerce.date(); // Calls new Date(value)
const CoercedBigInt = z.coerce.bigint(); // Calls BigInt(value)

// Common use: form inputs (always strings)
const FormSchema = z.object({
  name: z.string().min(1),
  age: z.coerce.number().min(0).max(150),
  birthDate: z.coerce.date(),
  subscribe: z.coerce.boolean(),
});

// Parse form data
const formData = {
  name: "John",
  age: "25", // String from input
  birthDate: "1995-06-15",
  subscribe: "true",
};
const result = FormSchema.parse(formData);
// { name: "John", age: 25, birthDate: Date, subscribe: true }
```

---

## Custom Error Messages

```typescript
// Per-validation messages
const EmailSchema = z
  .string({
    required_error: "Email is required",
    invalid_type_error: "Email must be a string",
  })
  .email({ message: "Invalid email format" });

// Object-level messages
const UserSchema = z.object({
  name: z.string().min(1, "Name cannot be empty"),
  email: z.string().email("Please enter a valid email"),
  age: z
    .number()
    .min(18, "Must be at least 18 years old")
    .max(120, "Invalid age"),
});

// Custom error map (global)
const customErrorMap: z.ZodErrorMap = (issue, ctx) => {
  if (issue.code === z.ZodIssueCode.invalid_type) {
    if (issue.expected === "string") {
      return { message: "This field must be text" };
    }
  }
  return { message: ctx.defaultError };
};

z.setErrorMap(customErrorMap);

// Format errors for display
function formatZodErrors(error: z.ZodError): Record<string, string> {
  const errors: Record<string, string> = {};
  for (const issue of error.issues) {
    const path = issue.path.join(".");
    if (!errors[path]) {
      errors[path] = issue.message;
    }
  }
  return errors;
}
```

---

## Form Validation (react-hook-form)

```typescript
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";

const SignupSchema = z.object({
  email: z.string().email("Invalid email"),
  password: z.string()
    .min(8, "Password must be at least 8 characters")
    .regex(/[A-Z]/, "Must contain uppercase letter")
    .regex(/[0-9]/, "Must contain number"),
  confirmPassword: z.string(),
}).refine((data) => data.password === data.confirmPassword, {
  message: "Passwords don't match",
  path: ["confirmPassword"],
});

type SignupForm = z.infer<typeof SignupSchema>;

function SignupForm() {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<SignupForm>({
    resolver: zodResolver(SignupSchema),
  });

  const onSubmit = (data: SignupForm) => {
    console.log("Valid data:", data);
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input {...register("email")} />
      {errors.email && <span>{errors.email.message}</span>}

      <input type="password" {...register("password")} />
      {errors.password && <span>{errors.password.message}</span>}

      <input type="password" {...register("confirmPassword")} />
      {errors.confirmPassword && <span>{errors.confirmPassword.message}</span>}

      <button type="submit">Sign Up</button>
    </form>
  );
}
```

---

## API Contract Validation

### Request/Response Validation

```typescript
// API schemas
const CreateUserRequest = z.object({
  name: z.string().min(1),
  email: z.string().email(),
  role: z.enum(["admin", "user"]).default("user"),
});

const UserResponse = z.object({
  id: z.string().uuid(),
  name: z.string(),
  email: z.string().email(),
  role: z.enum(["admin", "user"]),
  createdAt: z.string().datetime(),
});

const ApiError = z.object({
  code: z.string(),
  message: z.string(),
  details: z.record(z.string()).optional(),
});

// Type-safe API client
async function createUser(
  input: z.infer<typeof CreateUserRequest>,
): Promise<z.infer<typeof UserResponse>> {
  const validatedInput = CreateUserRequest.parse(input);

  const response = await fetch("/api/users", {
    method: "POST",
    body: JSON.stringify(validatedInput),
  });

  const data = await response.json();
  return UserResponse.parse(data);
}

// Express middleware
function validateBody<T extends z.ZodSchema>(schema: T) {
  return (req: Request, res: Response, next: NextFunction) => {
    const result = schema.safeParse(req.body);
    if (!result.success) {
      return res.status(400).json({
        code: "VALIDATION_ERROR",
        errors: result.error.flatten().fieldErrors,
      });
    }
    req.body = result.data;
    next();
  };
}

// Usage
app.post("/users", validateBody(CreateUserRequest), (req, res) => {
  // req.body is typed and validated
});
```

---

## Environment Variable Validation

```typescript
const EnvSchema = z.object({
  NODE_ENV: z
    .enum(["development", "production", "test"])
    .default("development"),
  PORT: z.coerce.number().default(3000),
  DATABASE_URL: z.string().url(),
  API_KEY: z.string().min(1),
  REDIS_URL: z.string().url().optional(),
  LOG_LEVEL: z.enum(["debug", "info", "warn", "error"]).default("info"),
  ENABLE_CACHE: z.coerce.boolean().default(true),
});

// Parse and validate
function loadEnv() {
  const result = EnvSchema.safeParse(process.env);

  if (!result.success) {
    console.error("❌ Invalid environment variables:");
    console.error(result.error.flatten().fieldErrors);
    process.exit(1);
  }

  return result.data;
}

export const env = loadEnv();

// Type-safe access
console.log(env.PORT); // number
console.log(env.NODE_ENV); // "development" | "production" | "test"
```

---

## Best Practices

### 1. Schema Organization

```typescript
// schemas/user.ts
export const UserSchema = z.object({...});
export type User = z.infer<typeof UserSchema>;

export const CreateUserSchema = UserSchema.omit({ id: true, createdAt: true });
export type CreateUser = z.infer<typeof CreateUserSchema>;

export const UpdateUserSchema = CreateUserSchema.partial();
export type UpdateUser = z.infer<typeof UpdateUserSchema>;
```

### 2. Reusable Validators

```typescript
// schemas/common.ts
export const id = z.string().uuid();
export const email = z.string().email().toLowerCase();
export const password = z.string().min(8).max(100);
export const timestamp = z.string().datetime();
export const pagination = z.object({
  page: z.coerce.number().min(1).default(1),
  limit: z.coerce.number().min(1).max(100).default(20),
});
```

### 3. Brand Types for Type Safety

```typescript
const UserId = z.string().uuid().brand<"UserId">();
const OrderId = z.string().uuid().brand<"OrderId">();

type UserId = z.infer<typeof UserId>;
type OrderId = z.infer<typeof OrderId>;

// These are now incompatible types
function getUser(id: UserId) {
  /* ... */
}
function getOrder(id: OrderId) {
  /* ... */
}

const userId = UserId.parse("123e4567-e89b-12d3-a456-426614174000");
const orderId = OrderId.parse("123e4567-e89b-12d3-a456-426614174000");

getUser(userId); // ✅ OK
getUser(orderId); // ❌ Type error
```

### 4. Lazy Schemas (Recursive Types)

```typescript
interface Category {
  name: string;
  subcategories: Category[];
}

const CategorySchema: z.ZodType<Category> = z.lazy(() =>
  z.object({
    name: z.string(),
    subcategories: z.array(CategorySchema),
  }),
);
```

### 5. Error Handling Pattern

```typescript
function parseOrThrow<T extends z.ZodSchema>(
  schema: T,
  data: unknown,
  context?: string,
): z.infer<T> {
  const result = schema.safeParse(data);
  if (!result.success) {
    const message = context
      ? `Validation failed for ${context}`
      : "Validation failed";
    throw new ValidationError(message, result.error);
  }
  return result.data;
}

class ValidationError extends Error {
  constructor(
    message: string,
    public readonly zodError: z.ZodError,
  ) {
    super(message);
    this.name = "ValidationError";
  }
}
```

---

## Common Patterns

| Pattern          | Schema                                   |
| ---------------- | ---------------------------------------- |
| Non-empty string | `z.string().min(1)`                      |
| Positive integer | `z.number().int().positive()`            |
| URL string       | `z.string().url()`                       |
| ISO date string  | `z.string().datetime()`                  |
| UUID             | `z.string().uuid()`                      |
| Slug             | `z.string().regex(/^[a-z0-9-]+$/)`       |
| Phone            | `z.string().regex(/^\+?[1-9]\d{1,14}$/)` |
| Hex color        | `z.string().regex(/^#[0-9A-Fa-f]{6}$/)`  |

---

## Resources

- [Zod Documentation](https://zod.dev)
- [Zod GitHub](https://github.com/colinhacks/zod)
- [react-hook-form + Zod](https://react-hook-form.com/get-started#SchemaValidation)
