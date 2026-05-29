---
name: Schema
description: This skill should be used when the user asks about "Effect Schema", "Schema.Struct", "Schema.decodeUnknown", "data validation", "parsing", "Schema.transform", "Schema filters", "Schema annotations", "JSON Schema", "Schema.Class", "Schema branded types", "encoding", "decoding", "Schema.parseJson", or needs to understand how Effect handles data validation and transformation.
version: 1.0.0
---

# Schema in Effect

## Overview

Effect Schema provides:

- **Type-safe validation** - Runtime checks with TypeScript inference
- **Bidirectional transformation** - Decode from external, encode for output
- **Composable schemas** - Build complex types from primitives
- **Error messages** - Detailed, customizable validation errors
- **Interop** - JSON Schema, Pretty Printing, Arbitrary generation

## Schema Best Practices

### 1. Tagged Unions Over Optional Properties

**AVOID optional properties. USE tagged unions instead.** This makes states explicit and enables exhaustive pattern matching.

```typescript
// ❌ BAD: Optional properties hide state complexity
const User = Schema.Struct({
  id: Schema.String,
  name: Schema.String,
  email: Schema.optional(Schema.String),
  verifiedAt: Schema.optional(Schema.Date),
  suspendedReason: Schema.optional(Schema.String)
})
// Unclear: Can a user be both verified AND suspended? What if email is missing?

// ✅ GOOD: Tagged union makes states explicit
const User = Schema.Union(
  Schema.Struct({
    _tag: Schema.Literal("Unverified"),
    id: Schema.String,
    name: Schema.String
  }),
  Schema.Struct({
    _tag: Schema.Literal("Active"),
    id: Schema.String,
    name: Schema.String,
    email: Schema.String,
    verifiedAt: Schema.Date
  }),
  Schema.Struct({
    _tag: Schema.Literal("Suspended"),
    id: Schema.String,
    name: Schema.String,
    email: Schema.String,
    suspendedReason: Schema.String
  })
)
// Clear: Each state has exactly the fields it needs
```

**Why tagged unions:**
- No impossible states (suspended user always has a reason)
- Exhaustive matching catches missing cases
- Self-documenting state machine
- Works perfectly with Match.tag

### 2. Class-Based Schemas Over Struct Schemas

**PREFER Schema.Class over Schema.Struct.** Classes give you methods, Schema.is() type guards, and better ergonomics.

```typescript
// ❌ AVOID: Plain Struct (no methods, no Schema.is() support)
const UserStruct = Schema.Struct({
  id: Schema.String,
  firstName: Schema.String,
  lastName: Schema.String,
  email: Schema.String
})
type User = Schema.Schema.Type<typeof UserStruct>

// ✅ PREFER: Class-based Schema
class User extends Schema.Class<User>("User")({
  id: Schema.String,
  firstName: Schema.String,
  lastName: Schema.String,
  email: Schema.String
}) {
  get fullName() {
    return `${this.firstName} ${this.lastName}`
  }

  get emailDomain() {
    return this.email.split("@")[1]
  }

  withEmail(email: string) {
    return new User({ ...this, email })
  }
}

// Usage:
const user = Schema.decodeUnknownSync(User)(data)
console.log(user.fullName)        // "John Doe"
console.log(Schema.is(User)(user)) // true - use Schema.is() for type checks
```

**For tagged unions with classes:**

```typescript
class Unverified extends Schema.TaggedClass<Unverified>()("Unverified", {
  id: Schema.String,
  name: Schema.String
}) {}

class Active extends Schema.TaggedClass<Active>()("Active", {
  id: Schema.String,
  name: Schema.String,
  email: Schema.String,
  verifiedAt: Schema.Date
}) {
  get isRecent() {
    return Date.now() - this.verifiedAt.getTime() < 86400000
  }
}

class Suspended extends Schema.TaggedClass<Suspended>()("Suspended", {
  id: Schema.String,
  name: Schema.String,
  suspendedReason: Schema.String
}) {}

const User = Schema.Union(Unverified, Active, Suspended)
type User = Schema.Schema.Type<typeof User>
```

### 3. Schema.is() with Match Patterns

**USE Schema.is() as type guards in Match.when patterns.** This combines Schema validation with Match's exhaustive checking.

```typescript
import { Schema, Match } from "effect"

// Define schemas
class Circle extends Schema.TaggedClass<Circle>()("Circle", {
  radius: Schema.Number
}) {
  get area() { return Math.PI * this.radius ** 2 }
}

class Rectangle extends Schema.TaggedClass<Rectangle>()("Rectangle", {
  width: Schema.Number,
  height: Schema.Number
}) {
  get area() { return this.width * this.height }
}

const Shape = Schema.Union(Circle, Rectangle)
type Shape = Schema.Schema.Type<typeof Shape>

// Use Schema.is() in Match patterns
const describeShape = (shape: Shape) =>
  Match.value(shape).pipe(
    Match.when(Schema.is(Circle), (c) => `Circle with radius ${c.radius}`),
    Match.when(Schema.is(Rectangle), (r) => `${r.width}x${r.height} rectangle`),
    Match.exhaustive
  )

// Schema.is() also works for runtime type checking
const processUnknown = (input: unknown) => {
  if (Schema.is(Circle)(input)) {
    console.log(`Circle area: ${input.area}`)
  }
}
```

**Schema.is() vs Match.tag:**

```typescript
// Match.tag - when you already know it's the union type
const handleUser = (user: User) =>
  Match.value(user).pipe(
    Match.tag("Active", (u) => sendEmail(u.email)),
    Match.tag("Suspended", (u) => logSuspension(u.suspendedReason)),
    Match.tag("Unverified", () => sendVerificationReminder()),
    Match.exhaustive
  )

// Schema.is() - when validating unknown data or need class features
const handleUnknown = (input: unknown) =>
  Match.value(input).pipe(
    Match.when(Schema.is(Active), (u) => u.isRecent),  // Can use class methods
    Match.when(Schema.is(Suspended), () => false),
    Match.orElse(() => false)
  )
```

**NEVER access `._tag` directly:**

```typescript
// ❌ FORBIDDEN - direct ._tag access
if (user._tag === "Active") { ... }
const isActive = user._tag === "Active"

// ❌ FORBIDDEN - ._tag in type definitions
type UserTag = User["_tag"]  // Never extract _tag as a type

// ❌ FORBIDDEN - ._tag in array predicates
const hasActive = users.some((u) => u._tag === "Active")
const activeUsers = users.filter((u) => u._tag === "Active")
const activeCount = users.filter((u) => u._tag === "Active").length

// ✅ REQUIRED - Schema.is() as array predicate
const hasActive = users.some(Schema.is(Active))
const activeUsers = users.filter(Schema.is(Active))
const activeCount = users.filter(Schema.is(Active)).length

// ✅ REQUIRED - use Match.tag or Schema.is()
const handleUser = Match.type<User>().pipe(
  Match.tag("Active", (u) => ...),
  Match.exhaustive
)

// ✅ REQUIRED - Schema.is() for type guards
const isActive = Schema.is(Active)
if (isActive(user)) { ... }
```

### 4. Never Use Schema.Any or Schema.Unknown for Type Weakening

**`Schema.Any` and `Schema.Unknown` are ONLY permitted when the value is genuinely unconstrained at the domain level.** Using them to avoid writing a proper schema is type weakening and defeats the purpose of Schema-first modeling.

**Semantically correct uses (ALLOWED):**

```typescript
// ✅ Error `cause` capturing arbitrary caught exceptions - the value is genuinely unknown
class NetworkError extends Schema.TaggedError<NetworkError>()(
  "NetworkError",
  { url: Schema.String, cause: Schema.Unknown }
) {}

// ✅ A generic container that truly accepts any value (e.g., a cache, event metadata)
class CacheEntry extends Schema.Class<CacheEntry>("CacheEntry")({
  key: Schema.String,
  value: Schema.Unknown,   // Cache genuinely stores arbitrary data
  ttl: Schema.Number
}) {}

// ✅ Schema.parseJson without a target schema to get raw parsed JSON
const RawJson = Schema.parseJson()  // Produces Schema<unknown>
// This is fine as an intermediate step before further validation
```

**Type weakening (FORBIDDEN):**

```typescript
// ❌ FORBIDDEN: Lazy schema definition - write the actual shape
const UserResponse = Schema.Struct({
  data: Schema.Unknown  // What is "data"? Define it!
})

// ❌ FORBIDDEN: Avoiding nested schema definition
const ApiResponse = Schema.Struct({
  body: Schema.Any  // Write the actual body schema
})

// ❌ FORBIDDEN: Using Schema.Unknown for "I'll validate later"
const input: Schema.Schema<unknown> = Schema.Unknown
// Define the correct schema upfront

// ❌ FORBIDDEN: Using Schema.Any to bypass type checking
const config = Schema.Struct({
  settings: Schema.Any  // Define the settings shape!
})
```

**How to fix type-weakened schemas:**

```typescript
// ❌ Before: type-weakened
const ApiResponse = Schema.Struct({
  data: Schema.Unknown,
  meta: Schema.Any
})

// ✅ After: properly typed
class ApiResponse extends Schema.Class<ApiResponse>("ApiResponse")({
  data: Schema.Struct({
    users: Schema.Array(User),
    total: Schema.Number
  }),
  meta: Schema.Struct({
    page: Schema.Number,
    perPage: Schema.Number,
    requestId: Schema.String
  })
}) {}
```

**Rule of thumb:** If you can describe the shape of the data, you MUST define a proper schema. `Schema.Unknown` is only for values that are genuinely opaque (caught exceptions, plugin payloads from unknown sources, serialized blobs you pass through without inspecting). `Schema.Any` should almost never appear in application code.

## Basic Schemas

```typescript
import { Schema } from "effect"

// Primitives
const str = Schema.String
const num = Schema.Number
const bool = Schema.Boolean
const bigint = Schema.BigInt

// Literals
const status = Schema.Literal("pending", "active", "completed")

// Enums
enum Color { Red, Green, Blue }
const color = Schema.Enums(Color)
```

## Decoding and Encoding

### Decoding (External → Internal)

```typescript
const Person = Schema.Struct({
  name: Schema.String,
  age: Schema.Number
})

// Sync decode (throws on error)
const person = Schema.decodeUnknownSync(Person)({ name: "Alice", age: 30 })

// Effect-based decode
const person = yield* Schema.decodeUnknown(Person)(input)

// Either result
const result = Schema.decodeUnknownEither(Person)(input)
```

### Encoding (Internal → External)

```typescript
const encoded = Schema.encodeSync(Person)(person)
const encoded = yield* Schema.encode(Person)(person)
```

## Struct Schemas

```typescript
const User = Schema.Struct({
  id: Schema.Number,
  name: Schema.String,
  email: Schema.String,
  createdAt: Schema.Date
})

// Optional fields
const UserWithOptional = Schema.Struct({
  id: Schema.Number,
  name: Schema.String,
  nickname: Schema.optional(Schema.String)
})

// Optional with default
const UserWithDefault = Schema.Struct({
  id: Schema.Number,
  role: Schema.optional(Schema.String).pipe(
    Schema.withDefault(() => "user")
  )
})
```

## Array and Record

```typescript
// Array
const Numbers = Schema.Array(Schema.Number)
const Users = Schema.Array(User)

// Non-empty array
const NonEmptyStrings = Schema.NonEmptyArray(Schema.String)

// Record
const StringRecord = Schema.Record({
  key: Schema.String,
  value: Schema.Number
})
```

## Union and Discriminated Unions

```typescript
// Simple union
const StringOrNumber = Schema.Union(Schema.String, Schema.Number)

// Discriminated union (recommended)
const Shape = Schema.Union(
  Schema.Struct({
    _tag: Schema.Literal("Circle"),
    radius: Schema.Number
  }),
  Schema.Struct({
    _tag: Schema.Literal("Rectangle"),
    width: Schema.Number,
    height: Schema.Number
  })
)
```

## Transformations

### Schema.transform

```typescript
// String ↔ Number
const NumberFromString = Schema.transform(
  Schema.String,
  Schema.Number,
  {
    decode: (s) => parseFloat(s),
    encode: (n) => String(n)
  }
)

// Usage: "42" decodes to 42, 42 encodes to "42"
```

### Built-in Transformations

```typescript
// String to Number
const num = Schema.NumberFromString

// String to Date
const date = Schema.DateFromString

// Parse JSON string
const jsonData = Schema.parseJson(Schema.Struct({
  name: Schema.String
}))
```

## JSON Parsing with Schema.parseJson

**NEVER use `JSON.parse()` directly.** Always use `Schema.parseJson` to combine JSON parsing with schema validation in one step.

### Why Schema.parseJson over JSON.parse

```typescript
// ❌ BAD: JSON.parse gives you `any` and can throw
const data = JSON.parse(jsonString)  // type: any, throws on invalid JSON

// ❌ BAD: Even with Schema, this is two separate failure points
const parsed = JSON.parse(jsonString)  // Can throw!
const validated = Schema.decodeUnknownSync(MySchema)(parsed)

// ✅ GOOD: Schema.parseJson handles both in one type-safe step
const MyData = Schema.parseJson(Schema.Struct({
  name: Schema.String,
  count: Schema.Number
}))

// Sync version - throws ParseError (not generic Error)
const data = Schema.decodeUnknownSync(MyData)('{"name": "test", "count": 42}')

// Effect version - typed error handling
const program = Schema.decodeUnknown(MyData)(jsonString)
// Effect<{ name: string, count: number }, ParseError, never>
```

### Schema.parseJson Benefits

1. **Single failure point** - Invalid JSON or invalid structure both produce ParseError
2. **Type safety** - Result is fully typed, never `any`
3. **Effect integration** - Works seamlessly with Effect error handling
4. **Detailed errors** - ParseError includes path and validation details

### Common Patterns

```typescript
// API response parsing
const ApiResponse = Schema.parseJson(Schema.Struct({
  success: Schema.Boolean,
  data: Schema.Struct({
    id: Schema.String,
    name: Schema.String
  })
}))

// With optional reviver schema for complex decoding
const WithDate = Schema.parseJson(Schema.Struct({
  createdAt: Schema.Date  // Automatically handles ISO date strings
}))

// Nested JSON (JSON string containing JSON string)
const NestedConfig = Schema.parseJson(Schema.Struct({
  settings: Schema.parseJson(Schema.Struct({
    theme: Schema.String
  }))
}))
```

### In Effect Programs

```typescript
import { Effect, Schema } from "effect"

const ConfigSchema = Schema.parseJson(Schema.Struct({
  apiKey: Schema.String,
  endpoint: Schema.String,
  retries: Schema.Number
}))

const loadConfig = (jsonString: string) =>
  Effect.gen(function* () {
    const config = yield* Schema.decodeUnknown(ConfigSchema)(jsonString)
    return config
  })

// Errors are typed and can be handled with Effect.catchTag
const program = loadConfig(rawJson).pipe(
  Effect.catchTag("ParseError", (e) =>
    Effect.fail(new ConfigurationError({ cause: e }))
  )
)
```

## Filters (Validation)

```typescript
// String constraints
const Email = Schema.String.pipe(
  Schema.pattern(/^[^@]+@[^@]+\.[^@]+$/),
  Schema.annotations({ identifier: "Email" })
)

const Username = Schema.String.pipe(
  Schema.minLength(3),
  Schema.maxLength(20),
  Schema.pattern(/^[a-z0-9_]+$/)
)

// Number constraints
const Age = Schema.Number.pipe(
  Schema.int(),
  Schema.between(0, 150)
)

const PositiveNumber = Schema.Number.pipe(
  Schema.positive()
)

// Custom filter
const EvenNumber = Schema.Number.pipe(
  Schema.filter((n) => n % 2 === 0, {
    message: () => "Expected even number"
  })
)
```

## Branded Types

```typescript
const UserId = Schema.String.pipe(
  Schema.brand("UserId")
)
type UserId = Schema.Schema.Type<typeof UserId>
// type UserId = string & Brand<"UserId">

const OrderId = Schema.Number.pipe(
  Schema.int(),
  Schema.positive(),
  Schema.brand("OrderId")
)
```

## Class-Based Schemas

```typescript
class Person extends Schema.Class<Person>("Person")({
  id: Schema.Number,
  name: Schema.String,
  email: Schema.String
}) {
  get displayName() {
    return `${this.name} (${this.email})`
  }
}

// Decode creates Person instance
const person = Schema.decodeUnknownSync(Person)({
  id: 1,
  name: "Alice",
  email: "alice@example.com"
})
console.log(person.displayName) // "Alice (alice@example.com)"
```

## Tagged Errors with Schema

```typescript
class UserNotFound extends Schema.TaggedError<UserNotFound>()(
  "UserNotFound",
  { userId: Schema.String }
) {}

class ValidationError extends Schema.TaggedError<ValidationError>()(
  "ValidationError",
  { errors: Schema.Array(Schema.String) }
) {}
```

## Annotations

```typescript
const User = Schema.Struct({
  id: Schema.Number.pipe(
    Schema.annotations({
      identifier: "UserId",
      title: "User ID",
      description: "Unique user identifier",
      examples: [1, 2, 3]
    })
  ),
  email: Schema.String.pipe(
    Schema.annotations({
      identifier: "Email",
      description: "User email address"
    })
  )
})
```

## Error Messages

### Custom Messages

```typescript
const Password = Schema.String.pipe(
  Schema.minLength(8, {
    message: () => "Password must be at least 8 characters"
  }),
  Schema.pattern(/[A-Z]/, {
    message: () => "Password must contain uppercase letter"
  }),
  Schema.pattern(/[0-9]/, {
    message: () => "Password must contain a number"
  })
)
```

### Formatting Errors

```typescript
import { TreeFormatter, ArrayFormatter } from "effect/ParseResult"

const result = Schema.decodeUnknownEither(User)(input)
Either.match(result, {
  onLeft: (error) => {
    // Tree format
    console.log(TreeFormatter.formatErrorSync(error))

    // Array format
    console.log(ArrayFormatter.formatErrorSync(error))
  },
  onRight: () => {
    // Valid input, no errors to format
  }
})
```

## JSON Schema Export

```typescript
import { JSONSchema } from "effect"

const jsonSchema = JSONSchema.make(User)
// Produces JSON Schema compatible output
```

## Common Patterns

### API Response Validation

```typescript
const ApiResponse = <A>(dataSchema: Schema.Schema<A>) =>
  Schema.Struct({
    success: Schema.Boolean,
    data: dataSchema,
    timestamp: Schema.DateFromString
  })

const UserResponse = ApiResponse(User)
```

### Form Validation

```typescript
const RegistrationForm = Schema.Struct({
  username: Schema.String.pipe(
    Schema.minLength(3),
    Schema.maxLength(20)
  ),
  email: Schema.String.pipe(Schema.pattern(emailRegex)),
  password: Schema.String.pipe(Schema.minLength(8)),
  confirmPassword: Schema.String
}).pipe(
  Schema.filter((form) =>
    form.password === form.confirmPassword
      ? undefined
      : "Passwords must match"
  )
)
```

### Recursive Schemas

```typescript
interface Category {
  name: string
  subcategories: readonly Category[]
}

const Category: Schema.Schema<Category> = Schema.Struct({
  name: Schema.String,
  subcategories: Schema.Array(Schema.suspend(() => Category))
})
```

## Best Practices Summary

### Do

1. **Use tagged unions over optional properties** - Make states explicit
2. **Use Schema.Class/TaggedClass over Struct** - Get methods and Schema.is() type guards
3. **Use Schema.is() in Match patterns** - Combine validation with matching
4. **Brand IDs and sensitive types** - Prevent mixing up values
5. **Annotate for documentation** - Descriptions flow to JSON Schema
6. **Transform at boundaries** - Parse external data early

### Don't

1. **Don't use optional properties for state** - Use tagged unions instead
2. **Don't use plain Struct for domain entities** - Use Schema.Class
3. **Don't validate manually** - Use Schema.is() with Match
4. **Don't mix branded types** - Each ID type should be distinct
5. **NEVER access `._tag` directly** - Use Match.tag or Schema.is() instead
6. **NEVER extract `._tag` as a type** - e.g., `type Tag = Foo["_tag"]` is forbidden
7. **NEVER use `._tag` in predicates** - Use Schema.is(Variant) with .some()/.filter()
8. **NEVER use Schema.Any or Schema.Unknown to avoid writing a proper schema** - These are only permitted when the value is genuinely unconstrained (e.g., caught exception causes, opaque plugin payloads). If you can describe the data shape, define a real schema.

## Additional Resources

For comprehensive Schema documentation, consult `${CLAUDE_PLUGIN_ROOT}/references/llms-full.txt`.

Search for these sections:
- "Introduction to Effect Schema" for overview
- "Basic Usage" for getting started
- "Transformations" for bidirectional transforms
- "Filters" for validation rules
- "Class APIs" for class-based schemas
- "Error Formatters" for error handling
