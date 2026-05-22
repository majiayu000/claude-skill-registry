---
name: effect-schema
description: Use when @effect/schema patterns including schema definition, validation, parsing, encoding, and transformations. Use for type-safe data validation in Effect applications.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
---

# Effect Schema

Master type-safe data validation and transformation with @effect/schema. This
skill covers schema definition, parsing, encoding, and advanced schema patterns
for building robust data pipelines.

## Basic Schema Types

### Primitive Schemas

```typescript
import { Schema } from "@effect/schema"

// Primitive types
const StringSchema = Schema.String
const NumberSchema = Schema.Number
const BooleanSchema = Schema.Boolean
const BigIntSchema = Schema.BigInt
const SymbolSchema = Schema.Symbol

// Special types
const UndefinedSchema = Schema.Undefined
const VoidSchema = Schema.Void
const NullSchema = Schema.Null
const UnknownSchema = Schema.Unknown
const AnySchema = Schema.Any
```

### Literal Values

```typescript
import { Schema } from "@effect/schema"

// String literal
const HelloSchema = Schema.Literal("hello")

// Number literal
const FortyTwoSchema = Schema.Literal(42)

// Boolean literal
const TrueSchema = Schema.Literal(true)

// Multiple literals (union)
const StatusSchema = Schema.Literal("pending", "approved", "rejected")
```

## Struct Schemas

### Basic Struct

```typescript
import { Schema } from "@effect/schema"

// Define user schema
const UserSchema = Schema.Struct({
  id: Schema.String,
  name: Schema.String,
  age: Schema.Number,
  email: Schema.String
})

// Infer TypeScript type
type User = Schema.Schema.Type<typeof UserSchema>
// { id: string; name: string; age: number; email: string }
```

### Optional Fields

```typescript
import { Schema } from "@effect/schema"

const PersonSchema = Schema.Struct({
  name: Schema.String,
  age: Schema.Number,
  email: Schema.optional(Schema.String),
  phone: Schema.optional(Schema.String)
})

type Person = Schema.Schema.Type<typeof PersonSchema>
// { name: string; age: number; email?: string; phone?: string }
```

### Nested Schemas

```typescript
import { Schema } from "@effect/schema"

const AddressSchema = Schema.Struct({
  street: Schema.String,
  city: Schema.String,
  zipCode: Schema.String
})

const UserWithAddressSchema = Schema.Struct({
  id: Schema.String,
  name: Schema.String,
  address: AddressSchema
})
```

## Arrays and Collections

### Array Schemas

```typescript
import { Schema } from "@effect/schema"

// Array of strings
const StringArraySchema = Schema.Array(Schema.String)

// Array of numbers
const NumberArraySchema = Schema.Array(Schema.Number)

// Array of complex objects
const UsersSchema = Schema.Array(UserSchema)

// Non-empty array
const NonEmptyStringArray = Schema.NonEmptyArray(Schema.String)
```

### Tuple Schemas

```typescript
import { Schema } from "@effect/schema"

// Fixed tuple
const CoordinatesSchema = Schema.Tuple(
  Schema.Number, // latitude
  Schema.Number  // longitude
)

// Tuple with optional elements
const ResponseSchema = Schema.Tuple(
  Schema.Number,                    // status code
  Schema.String,                    // message
  Schema.optional(Schema.Unknown)   // optional data
)
```

### Record Schemas

```typescript
import { Schema } from "@effect/schema"

// String keys, number values
const ScoresSchema = Schema.Record({
  key: Schema.String,
  value: Schema.Number
})

// Using template literals for keys
const ConfigSchema = Schema.Record({
  key: Schema.TemplateLiteral("config.", Schema.String),
  value: Schema.String
})
```

## Union and Intersection

### Union Types

```typescript
import { Schema } from "@effect/schema"

// Simple union
const StringOrNumberSchema = Schema.Union(
  Schema.String,
  Schema.Number
)

// Tagged union (discriminated)
const ShapeSchema = Schema.Union(
  Schema.Struct({
    kind: Schema.Literal("circle"),
    radius: Schema.Number
  }),
  Schema.Struct({
    kind: Schema.Literal("rectangle"),
    width: Schema.Number,
    height: Schema.Number
  })
)

type Shape = Schema.Schema.Type<typeof ShapeSchema>
// { kind: "circle"; radius: number } | { kind: "rectangle"; width: number; height: number }
```

### Intersection Types

```typescript
import { Schema } from "@effect/schema"

const TimestampsSchema = Schema.Struct({
  createdAt: Schema.Date,
  updatedAt: Schema.Date
})

const UserWithTimestampsSchema = Schema.extend(
  UserSchema,
  TimestampsSchema
)

// Equivalent to intersection
const ManualIntersection = Schema.Struct({
  ...UserSchema.fields,
  ...TimestampsSchema.fields
})
```

## Parsing and Validation

### Synchronous Parsing

```typescript
import { Schema } from "@effect/schema"

const UserSchema = Schema.Struct({
  name: Schema.String,
  age: Schema.Number
})

// Parse unknown data
const parseUser = Schema.decodeUnknownSync(UserSchema)

try {
  const user = parseUser({ name: "Alice", age: 30 })
  console.log(user) // { name: "Alice", age: 30 }
} catch (error) {
  console.error("Validation failed:", error)
}

// Invalid data throws
parseUser({ name: "Bob" }) // Throws: missing 'age' field
```

### Effect-Based Parsing

```typescript
import { Schema } from "@effect/schema"
import { Effect } from "effect"

const parseUserEffect = Schema.decodeUnknown(UserSchema)

const program = Effect.gen(function* () {
  const user = yield* parseUserEffect({ name: "Alice", age: 30 })
  return user
})

// Handle parse errors
const safeProgram = program.pipe(
  Effect.catchTag("ParseError", (error) =>
    Effect.sync(() => {
      console.error("Parse error:", error.message)
      return null
    })
  )
)
```

### Encoding

```typescript
import { Schema } from "@effect/schema"

// Encode typed data back to raw format
const encodeUser = Schema.encodeSync(UserSchema)

const user: User = { name: "Alice", age: 30 }
const encoded = encodeUser(user)
// { name: "Alice", age: 30 }
```

## Schema Transformations

### Transform Schemas

```typescript
import { Schema } from "@effect/schema"

// String to Date transformation
const DateFromString = Schema.transform(
  Schema.String,
  Schema.Date,
  {
    decode: (s) => new Date(s),
    encode: (d) => d.toISOString()
  }
)

// Parse ISO string to Date
const parseDate = Schema.decodeUnknownSync(DateFromString)
const date = parseDate("2024-01-01T00:00:00Z")
// Date object

// Encode Date back to string
const encodeDate = Schema.encodeSync(DateFromString)
const isoString = encodeDate(new Date())
// "2024-01-01T00:00:00.000Z"
```

### Validated Transformations

```typescript
import { Schema } from "@effect/schema"
import { ParseResult } from "@effect/schema/ParseResult"

// Email validation and transformation
const EmailSchema = Schema.transformOrFail(
  Schema.String,
  Schema.String,
  {
    decode: (s) => {
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(s)) {
        return ParseResult.fail(
          ParseResult.type(Schema.String.ast, s, "Invalid email format")
        )
      }
      return ParseResult.succeed(s.toLowerCase())
    },
    encode: (s) => ParseResult.succeed(s)
  }
)
```

## Refinements and Constraints

### String Refinements

```typescript
import { Schema } from "@effect/schema"

// Min/max length
const UsernameSchema = Schema.String.pipe(
  Schema.minLength(3),
  Schema.maxLength(20)
)

// Pattern matching
const UUIDSchema = Schema.String.pipe(
  Schema.pattern(/^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i)
)

// Email
const EmailSchema = Schema.String.pipe(Schema.pattern(/^[^\s@]+@[^\s@]+\.[^\s@]+$/))

// Starts with
const HttpUrlSchema = Schema.String.pipe(Schema.startsWith("http"))
```

### Number Refinements

```typescript
import { Schema } from "@effect/schema"

// Positive numbers
const PositiveSchema = Schema.Number.pipe(Schema.positive())

// Range
const AgeSchema = Schema.Number.pipe(
  Schema.greaterThanOrEqualTo(0),
  Schema.lessThanOrEqualTo(120)
)

// Integer
const IntegerSchema = Schema.Number.pipe(Schema.int())

// Multiple of
const EvenSchema = Schema.Number.pipe(Schema.multipleOf(2))
```

### Custom Refinements

```typescript
import { Schema } from "@effect/schema"

const PasswordSchema = Schema.String.pipe(
  Schema.minLength(8),
  Schema.filter((s) => ({
    message: () => "Password must contain uppercase, lowercase, and number",
    test: () =>
      /[A-Z]/.test(s) &&
      /[a-z]/.test(s) &&
      /[0-9]/.test(s)
  }))
)
```

## Common Schema Patterns

### API Response Schema

```typescript
import { Schema } from "@effect/schema"

const ApiResponseSchema = <A, I, R>(dataSchema: Schema.Schema<A, I, R>) =>
  Schema.Struct({
    success: Schema.Boolean,
    data: Schema.optional(dataSchema),
    error: Schema.optional(Schema.String)
  })

const UserResponseSchema = ApiResponseSchema(UserSchema)

type UserResponse = Schema.Schema.Type<typeof UserResponseSchema>
// { success: boolean; data?: User; error?: string }
```

### Paginated Response

```typescript
import { Schema } from "@effect/schema"

const PaginatedSchema = <A, I, R>(itemSchema: Schema.Schema<A, I, R>) =>
  Schema.Struct({
    items: Schema.Array(itemSchema),
    total: Schema.Number,
    page: Schema.Number,
    pageSize: Schema.Number
  })

const PaginatedUsersSchema = PaginatedSchema(UserSchema)
```

### Form Data Schema

```typescript
import { Schema } from "@effect/schema"

const SignupFormSchema = Schema.Struct({
  email: Schema.String.pipe(
    Schema.pattern(/^[^\s@]+@[^\s@]+\.[^\s@]+$/)
  ),
  password: Schema.String.pipe(
    Schema.minLength(8)
  ),
  confirmPassword: Schema.String,
  acceptTerms: Schema.Literal(true)
}).pipe(
  Schema.filter((data) => ({
    message: () => "Passwords must match",
    test: () => data.password === data.confirmPassword
  }))
)
```

## Integration with Effect

### Parsing in Effect Pipelines

```typescript
import { Schema } from "@effect/schema"
import { Effect } from "effect"

const processUserData = (rawData: unknown) =>
  Effect.gen(function* () {
    // Parse data
    const user = yield* Schema.decodeUnknown(UserSchema)(rawData)

    // Use parsed data
    const saved = yield* saveUser(user)
    const notified = yield* sendNotification(user.email)

    return saved
  })
```

### Handling Parse Errors

```typescript
import { Schema } from "@effect/schema"
import { Effect } from "effect"

const safeParseUser = (data: unknown) =>
  Schema.decodeUnknown(UserSchema)(data).pipe(
    Effect.catchTag("ParseError", (error) =>
      Effect.fail({
        _tag: "ValidationError",
        message: error.message,
        errors: error.errors
      })
    )
  )
```

## Best Practices

1. **Define Schemas Centrally**: Keep schema definitions in a shared module.

2. **Use Type Inference**: Let TypeScript infer types from schemas with
   `Schema.Schema.Type`.

3. **Compose Small Schemas**: Build complex schemas from smaller, reusable
   pieces.

4. **Validate at Boundaries**: Parse external data at API boundaries.

5. **Use Tagged Unions**: Add discriminant fields for union types.

6. **Document Schemas**: Add JSDoc comments to schema definitions.

7. **Test Schemas**: Write tests for schema validation logic.

8. **Use Transformations**: Convert between internal and external
   representations.

9. **Handle Errors Gracefully**: Provide meaningful error messages.

10. **Version Schemas**: Consider versioning for API schemas.

## Common Pitfalls

1. **Over-Validation**: Validating internal data unnecessarily.

2. **Weak Constraints**: Not adding sufficient refinements.

3. **Missing Optional Fields**: Forgetting to mark optional fields.

4. **Wrong Union Order**: Putting general schemas before specific ones.

5. **Not Handling Parse Errors**: Assuming parsing always succeeds.

6. **Circular References**: Creating schemas with circular dependencies.

7. **Performance**: Validating large datasets synchronously.

8. **Type Mismatches**: Schema and TypeScript type definitions diverging.

9. **Missing Transformations**: Not transforming between formats.

10. **Exposing Internal Types**: Returning internal types from APIs.

## When to Use This Skill

Use effect-schema when you need to:

- Validate API request/response data
- Parse configuration files
- Validate form inputs
- Transform data between formats
- Ensure data integrity at boundaries
- Generate TypeScript types from schemas
- Build type-safe data pipelines
- Validate database queries and results
- Parse environment variables
- Build robust data validation layers

## Resources

### Official Documentation

- [Effect Schema Introduction](https://effect.website/docs/schema/introduction)
- [Basic Usage](https://effect.website/docs/schema/basic-usage)
- [Built-in Schemas](https://effect.website/docs/schema/built-in-schemas)
- [Transformations](https://effect.website/docs/schema/transformations)
- [API Reference](https://effect-ts.github.io/effect/schema/Schema.ts.html)

### Related Skills

- effect-core-patterns - Basic Effect operations
- effect-error-handling - Handling parse errors
