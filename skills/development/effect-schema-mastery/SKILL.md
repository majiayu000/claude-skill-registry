---
name: effect-schema-mastery
description: Schema.TaggedStruct, Schema.TaggedClass, branded types, refinements, transformations. Pattern matching on _tag. Covers runtime validation, type inference, and schema composition for Effect-TS.
model_invoked: true
triggers:
  - "Schema"
  - "TaggedStruct"
  - "TaggedClass"
  - "branded"
  - "refinement"
  - "validation"
---

# Effect Schema Mastery

## Overview

**Effect Schema** is the runtime validation and type inference system for Effect-TS. In TMNL, **all domain types MUST be defined as Schemas** (not raw TypeScript interfaces).

This enables:
- **Runtime validation** — Catch invalid data at boundaries
- **Encode/decode transformations** — Bidirectional data conversions
- **JSON Schema generation** — Auto-generate API docs
- **Type inference** — Derive TypeScript types from schemas
- **EventLog integration** — Event payloads require Schema-backed types

**CRITICAL DOCTRINE (from CLAUDE.md):**
> Use Effect Schema instead of raw TypeScript interfaces/types. This is non-negotiable for domain types.

## Canonical Sources

### Effect Schema Core
- **Submodule**: `../../submodules/effect/packages/schema/src/`
  - `Schema.ts` — Core schema constructors
  - `TaggedStruct.ts` — Discriminated union data structures
  - `TaggedClass.ts` — Entities with methods

### Effect Website Documentation
- **Submodule**: `../../submodules/website/content/src/content/docs/docs/schema/`
  - Multiple `.mdx` files on schema usage, transformations, validation

### TMNL Battle-tested Implementations
- **Search schemas** — `src/lib/search/schemas.ts` (Schema.Struct, refinements, filters)
- **Query DSL schemas** — `src/lib/search/query/schemas.ts` (Literal enums, tagged unions)
- **AMS schemas** — `src/lib/ams/v2/base/events/schema.ts` (EventLog integration)

## Patterns

### Decision Tree: Which Schema Pattern?

```
Need to define a type?
│
├─ Discriminated data (events, messages, commands)?
│  └─ Use: Schema.TaggedStruct("Tag", { fields })
│     Pattern matching on _tag
│
├─ Entity with methods (domain objects)?
│  └─ Use: Schema.TaggedClass<T>()("Tag", { fields })
│     Methods + data in one class
│
├─ Enum-like values?
│  └─ Use: Schema.Literal("a", "b", "c")
│     Runtime + type representation
│
├─ Constrained primitives (non-empty string, positive int)?
│  └─ Use: Schema.filter(predicate)
│     Refinement types
│
├─ Bidirectional transformation (Date ↔ ISO string)?
│  └─ Use: Schema.transform(encode, decode)
│     Type-safe conversions
│
└─ Unique identifiers (UserId, OrderId)?
   └─ Use: Schema.brand("BrandName")
      Branded primitives for type safety
```

---

### Pattern 1: Schema.TaggedStruct — DISCRIMINATED DATA

**When to use:**
- Events, messages, commands
- Discriminated unions for pattern matching
- Data structures without behavior
- Need `_tag` field for type narrowing

**Signature:**
```typescript
const MyData = Schema.TaggedStruct("MyData", {
  field1: Schema.String,
  field2: Schema.Number,
})
type MyData = typeof MyData.Type
// { readonly _tag: "MyData"; readonly field1: string; readonly field2: number }
```

**Full Example:**
```typescript
import { Schema } from 'effect'

// Define tagged structs
const UserCreated = Schema.TaggedStruct('UserCreated', {
  userId: Schema.String,
  email: Schema.String,
  timestamp: Schema.DateFromSelf,
})

const UserDeleted = Schema.TaggedStruct('UserDeleted', {
  userId: Schema.String,
  reason: Schema.optional(Schema.String),
  timestamp: Schema.DateFromSelf,
})

// Union for pattern matching
const UserEvent = Schema.Union(UserCreated, UserDeleted)
type UserEvent = typeof UserEvent.Type

// Pattern match on _tag
function handleEvent(event: UserEvent) {
  switch (event._tag) {
    case 'UserCreated':
      console.log(`User ${event.userId} created at ${event.timestamp}`)
      return startOnboarding(event.email)

    case 'UserDeleted':
      console.log(`User ${event.userId} deleted: ${event.reason ?? 'no reason'}`)
      return cleanupData(event.userId)
  }
}

// Runtime validation
const parseEvent = Schema.decodeUnknownSync(UserEvent)
const event = parseEvent({ _tag: 'UserCreated', userId: '123', email: 'a@b.com', timestamp: new Date() })
```

**Key Features:**
- **Auto-generates `_tag`**: Discriminator field for pattern matching
- **Readonly by default**: All fields are `readonly`
- **Type inference**: `typeof Schema.Type` gives you the TypeScript type
- **Union support**: Combine multiple tagged structs with `Schema.Union`

**TMNL Example** (`src/lib/search/query/schemas.ts`):
```typescript
const ExactMatch = Schema.TaggedStruct('ExactMatch', {
  query: Schema.String,
})

const RegexMatch = Schema.TaggedStruct('RegexMatch', {
  pattern: Schema.String,
  flags: Schema.optional(Schema.String),
})

const QueryTerm = Schema.Union(ExactMatch, RegexMatch)
type QueryTerm = typeof QueryTerm.Type

// Pattern matching
function executeQuery(term: QueryTerm) {
  switch (term._tag) {
    case 'ExactMatch':
      return index.search(term.query)
    case 'RegexMatch':
      return index.searchRegex(new RegExp(term.pattern, term.flags))
  }
}
```

---

### Pattern 2: Schema.TaggedClass — ENTITIES WITH METHODS

**When to use:**
- Domain entities that need behavior
- Objects with both data and methods
- Want class-based syntax with validation

**Signature:**
```typescript
class EntityName extends Schema.TaggedClass<EntityName>()(
  "EntityName",
  {
    field1: Schema.String,
    field2: Schema.Number,
  }
) {
  // Methods here
  get computed() { return this.field1 + this.field2 }
  withField1(value: string) { return new EntityName({ ...this, field1: value }) }
}
```

**Full Example:**
```typescript
import { Schema } from 'effect'

class User extends Schema.TaggedClass<User>()(
  'User',
  {
    id: Schema.String,
    name: Schema.NonEmptyString,
    email: Schema.String,
    createdAt: Schema.DateFromSelf,
  }
) {
  // Computed properties
  get displayName() {
    return `${this.name} <${this.email}>`
  }

  // Methods (immutable updates)
  withName(name: string) {
    return new User({ ...this, name })
  }

  withEmail(email: string) {
    return new User({ ...this, email })
  }

  // Domain logic
  isActive(now: Date = new Date()) {
    const daysSinceCreation = (now.getTime() - this.createdAt.getTime()) / (1000 * 60 * 60 * 24)
    return daysSinceCreation <= 30
  }
}

// Usage
const user = new User({
  id: '123',
  name: 'Alice',
  email: 'alice@example.com',
  createdAt: new Date(),
})

console.log(user._tag)           // "User"
console.log(user.displayName)     // "Alice <alice@example.com>"
console.log(user.isActive())      // true

const updated = user.withName('Alice Smith')
```

**Key Features:**
- **Class-based**: Use `new ClassName(data)` syntax
- **Methods**: Define computed properties and domain logic
- **Immutable updates**: Use `new ClassName({ ...this, field: newValue })`
- **Still a Schema**: Can be used in `Schema.Array(User)`, `Schema.Union`, etc.

**TMNL Pattern** (Schema.Class for entities):
```typescript
import { Schema } from 'effect'

class GridColumn extends Schema.Class<GridColumn>('GridColumn')({
  field: Schema.String,
  headerName: Schema.String,
  width: Schema.optional(Schema.Number),
  sortable: Schema.optional(Schema.Boolean),
}) {
  get displayWidth() {
    return this.width ?? 150
  }

  withWidth(width: number) {
    return new GridColumn({ ...this, width })
  }

  isSortable() {
    return this.sortable ?? true
  }
}
```

---

### Pattern 3: Schema.Literal — ENUM-LIKE VALUES

**When to use:**
- Fixed set of string/number values
- Want both runtime validation AND type representation
- Replacing TypeScript `type Status = "pending" | "active"`

**Signature:**
```typescript
const StatusSchema = Schema.Literal("pending", "active", "archived")
type Status = typeof StatusSchema.Type  // "pending" | "active" | "archived"
```

**Full Example:**
```typescript
import { Schema } from 'effect'

// Define literal schema
const Status = Schema.Literal('pending', 'active', 'archived')
type Status = typeof Status.Type

const Priority = Schema.Literal(1, 2, 3, 4, 5)
type Priority = typeof Priority.Type

// Use in structs
const Task = Schema.Struct({
  id: Schema.String,
  title: Schema.String,
  status: Status,
  priority: Priority,
})

// Runtime validation
const decodeTask = Schema.decodeUnknownSync(Task)
const task = decodeTask({
  id: '1',
  title: 'Fix bug',
  status: 'active',  // ✅ Valid
  priority: 3,       // ✅ Valid
})

// This throws:
// decodeTask({ ...task, status: 'invalid' })  // ❌ Not in literal set
```

**Key Features:**
- **Runtime validation**: Rejects values not in the literal set
- **Type inference**: Automatically creates union type
- **Better than raw types**: Raw `type X = "a" | "b"` has no runtime representation

**TMNL Example** (`src/lib/search/schemas.ts`):
```typescript
export const SearchStrategySchema = Schema.Literal('exact', 'prefix', 'fuzzy', 'auto')
export type SearchStrategy = typeof SearchStrategySchema.Type

export const SearchOptionsSchema = Schema.Struct({
  limit: Schema.optional(Schema.Number.pipe(Schema.positive())),
  strategy: Schema.optional(SearchStrategySchema),
  fuzzyThreshold: Schema.optional(Schema.Number.pipe(Schema.filter((n) => n >= 0 && n <= 1))),
})
```

---

### Pattern 4: Schema.filter — REFINEMENT TYPES

**When to use:**
- Constrain primitives (positive numbers, non-empty strings, email format)
- Add validation rules to existing schemas
- Create custom predicates

**Signature:**
```typescript
const PositiveInt = Schema.Number.pipe(
  Schema.filter((n) => n > 0 && Number.isInteger(n), {
    message: () => "Must be a positive integer"
  })
)
```

**Full Example:**
```typescript
import { Schema } from 'effect'

// Non-empty string
const NonEmptyString = Schema.String.pipe(
  Schema.filter((s) => s.length > 0, {
    message: () => "String cannot be empty"
  })
)

// Email (simple validation)
const Email = Schema.String.pipe(
  Schema.filter((s) => s.includes('@'), {
    message: () => "Invalid email format"
  })
)

// Score between 0 and 1
const Score = Schema.Number.pipe(
  Schema.filter((n) => n >= 0 && n <= 1, {
    message: () => "Score must be between 0 and 1"
  })
)

// Age (positive integer)
const Age = Schema.Number.pipe(
  Schema.filter((n) => n > 0 && Number.isInteger(n), {
    message: () => "Age must be a positive integer"
  })
)

// Use in struct
const Person = Schema.Struct({
  name: NonEmptyString,
  email: Email,
  age: Age,
})

// Validation
const decodePerson = Schema.decodeUnknownSync(Person)
const person = decodePerson({
  name: 'Alice',
  email: 'alice@example.com',
  age: 30,
})

// Throws: decodePerson({ name: '', email: 'alice@example.com', age: 30 })
// Throws: decodePerson({ name: 'Alice', email: 'invalid', age: 30 })
// Throws: decodePerson({ name: 'Alice', email: 'alice@example.com', age: -5 })
```

**Key Features:**
- **Predicate function**: `(value) => boolean`
- **Custom error messages**: `message: () => string`
- **Composable**: Chain multiple filters with `.pipe()`

**Built-in refinements:**
```typescript
Schema.NonEmptyString  // String with length > 0
Schema.positive()      // Number > 0
Schema.negative()      // Number < 0
Schema.int()           // Integer
Schema.minLength(5)    // String/Array with min length
Schema.maxLength(10)   // String/Array with max length
Schema.pattern(/^\d{3}-\d{4}$/)  // Regex validation
```

**TMNL Example** (`src/lib/search/schemas.ts`):
```typescript
export const ValidSearchResultSchema = Schema.Struct({
  item: Schema.Unknown,
  score: Schema.Number.pipe(
    Schema.filter((n) => n >= 0 && n <= 1, {
      message: () => 'Score must be between 0 and 1',
    })
  ),
  matches: Schema.optional(Schema.Array(FieldMatchSchema)),
})
```

---

### Pattern 5: Schema.brand — BRANDED PRIMITIVES

**When to use:**
- Create unique identifier types (UserId, OrderId)
- Prevent accidental mixing of semantically different values
- Want nominal typing (not structural)

**Signature:**
```typescript
const UserId = Schema.String.pipe(Schema.brand("UserId"))
type UserId = typeof UserId.Type  // string & Brand<"UserId">
```

**Full Example:**
```typescript
import { Schema } from 'effect'

// Define branded types
const UserId = Schema.String.pipe(
  Schema.brand("UserId"),
  Schema.minLength(1)
)
type UserId = typeof UserId.Type

const OrderId = Schema.String.pipe(
  Schema.brand("OrderId"),
  Schema.minLength(1)
)
type OrderId = typeof OrderId.Type

const Email = Schema.String.pipe(
  Schema.brand("Email"),
  Schema.pattern(/@/)
)
type Email = typeof Email.Type

// These are different types!
const userId: UserId = "user-123" as UserId
const orderId: OrderId = "order-456" as OrderId

// Type error: Type 'UserId' is not assignable to type 'OrderId'
// const wrong: OrderId = userId  // ❌ Compile error

// Use in functions
function getUser(id: UserId) {
  return db.users.find(id)
}

function getOrder(id: OrderId) {
  return db.orders.find(id)
}

getUser(userId)    // ✅
getOrder(orderId)  // ✅
// getUser(orderId)  // ❌ Type error
```

**Key Features:**
- **Nominal typing**: `UserId` ≠ `OrderId` even though both are strings
- **Compile-time safety**: Prevents mixing semantically different values
- **Runtime validation**: Can combine with refinements

**Advanced: Branded + Refinement**
```typescript
const PositiveInt = Schema.Number.pipe(
  Schema.int(),
  Schema.positive(),
  Schema.brand("PositiveInt")
)
type PositiveInt = typeof PositiveInt.Type
```

---

### Pattern 6: Schema.transform — BIDIRECTIONAL TRANSFORMATIONS

**When to use:**
- Convert between representations (Date ↔ ISO string, number ↔ string)
- Decode external data formats
- Normalize data on input, denormalize on output

**Signature:**
```typescript
const MySchema = Schema.transform(
  fromSchema,
  toSchema,
  {
    decode: (from) => to,
    encode: (to) => from
  }
)
```

**Full Example:**
```typescript
import { Schema } from 'effect'

// Date ↔ ISO string
const DateFromString = Schema.transform(
  Schema.String,
  Schema.DateFromSelf,
  {
    decode: (s) => new Date(s),
    encode: (d) => d.toISOString(),
  }
)

// Parse JSON string ↔ object
const JsonString = <A>(schema: Schema.Schema<A>) =>
  Schema.transform(
    Schema.String,
    schema,
    {
      decode: (s) => JSON.parse(s),
      encode: (obj) => JSON.stringify(obj),
    }
  )

// Normalize whitespace
const TrimmedString = Schema.transform(
  Schema.String,
  Schema.String,
  {
    decode: (s) => s.trim(),
    encode: (s) => s,
  }
)

// Use in struct
const Event = Schema.Struct({
  id: Schema.String,
  timestamp: DateFromString,
  metadata: JsonString(Schema.Struct({ key: Schema.String })),
  description: TrimmedString,
})

// Decode from wire format
const decodeEvent = Schema.decodeUnknownSync(Event)
const event = decodeEvent({
  id: '123',
  timestamp: '2025-01-01T00:00:00.000Z',
  metadata: '{"key":"value"}',
  description: '  whitespace  ',
})

console.log(event.timestamp)  // Date object
console.log(event.metadata)   // { key: 'value' }
console.log(event.description)  // "whitespace" (trimmed)

// Encode to wire format
const encodeEvent = Schema.encodeSync(Event)
const wire = encodeEvent(event)
console.log(wire.timestamp)  // "2025-01-01T00:00:00.000Z"
console.log(wire.metadata)   // '{"key":"value"}'
```

**Key Features:**
- **Bidirectional**: Both `decode` (parse) and `encode` (serialize)
- **Type-safe**: Input and output types are tracked
- **Composable**: Use in `Schema.Struct`, `Schema.Array`, etc.

**Built-in transformations:**
```typescript
Schema.DateFromSelf       // Date (no transformation)
Schema.DateFromString     // string → Date
Schema.NumberFromString   // "123" → 123
Schema.parseJson(schema)  // JSON string → typed object
```

---

### Pattern 7: Schema.Struct — OBJECT SCHEMAS

**When to use:**
- Define object shapes
- Validate API responses
- Type-safe configuration objects

**Full Example:**
```typescript
import { Schema } from 'effect'

const User = Schema.Struct({
  id: Schema.String,
  name: Schema.String,
  email: Schema.String,
  age: Schema.Number,
  role: Schema.Literal('admin', 'user', 'guest'),
  metadata: Schema.optional(Schema.Record({ key: Schema.String, value: Schema.Unknown })),
})

type User = typeof User.Type

// Optional fields
const PartialUser = Schema.partial(User)

// Pick fields
const UserSummary = Schema.pick(User, 'id', 'name', 'email')

// Omit fields
const UserWithoutMetadata = Schema.omit(User, 'metadata')
```

---

### Pattern 8: Schema.Array — ARRAY SCHEMAS

**Full Example:**
```typescript
import { Schema } from 'effect'

const StringArray = Schema.Array(Schema.String)
const UserArray = Schema.Array(User)

// Non-empty array
const NonEmptyStringArray = Schema.Array(Schema.String).pipe(
  Schema.filter((arr) => arr.length > 0, {
    message: () => "Array cannot be empty"
  })
)

// Min/max length
const BoundedArray = Schema.Array(Schema.String).pipe(
  Schema.minItems(1),
  Schema.maxItems(10)
)
```

---

### Pattern 9: Schema.Record — MAP/DICTIONARY SCHEMAS

**Full Example:**
```typescript
import { Schema } from 'effect'

// Record<string, number>
const StringToNumber = Schema.Record({ key: Schema.String, value: Schema.Number })

// Record<string, User>
const UserMap = Schema.Record({ key: Schema.String, value: User })

// Constrained keys
const StatusCounts = Schema.Record({
  key: Schema.Literal('pending', 'active', 'archived'),
  value: Schema.Number,
})
```

## Examples

### Example 1: EventLog Integration (CRITICAL for TMNL)

EventLog requires Schema-backed payloads. This is non-negotiable.

```typescript
import { Event, EventGroup } from '@effect/experimental'
import { Schema } from 'effect'

// Event payload MUST be Schema
const UserCreatedPayload = Schema.Struct({
  id: Schema.String,
  name: Schema.NonEmptyString,
  email: Schema.String,
  createdAt: Schema.DateFromSelf,
})

const UserCreated = Event.make({
  tag: 'UserCreated',
  primaryKey: (payload) => payload.id,
  payload: UserCreatedPayload,
  success: Schema.Void,
})

// Use in EventGroup
const userEvents = EventGroup.make({
  UserCreated,
  // ... other events
})
```

### Example 2: API Response Validation

```typescript
import { Schema, Effect } from 'effect'

const ApiResponse = Schema.Struct({
  status: Schema.Literal('success', 'error'),
  data: Schema.optional(Schema.Unknown),
  error: Schema.optional(Schema.String),
  timestamp: Schema.DateFromString,
})

const fetchUser = (id: string) =>
  Effect.gen(function* () {
    const response = yield* Effect.tryPromise(() =>
      fetch(`/api/users/${id}`).then(r => r.json())
    )

    // Validate response
    const validated = yield* Schema.decodeUnknown(ApiResponse)(response)

    if (validated.status === 'error') {
      return yield* Effect.fail(new Error(validated.error ?? 'Unknown error'))
    }

    return validated.data
  })
```

### Example 3: Query DSL (TMNL Pattern)

```typescript
import { Schema } from 'effect'

const ExactQuery = Schema.TaggedStruct('Exact', {
  term: Schema.String,
})

const RegexQuery = Schema.TaggedStruct('Regex', {
  pattern: Schema.String,
  flags: Schema.optional(Schema.String),
})

const RangeQuery = Schema.TaggedStruct('Range', {
  field: Schema.String,
  min: Schema.Number,
  max: Schema.Number,
})

const Query = Schema.Union(ExactQuery, RegexQuery, RangeQuery)
type Query = typeof Query.Type

function executeQuery(query: Query) {
  switch (query._tag) {
    case 'Exact':
      return searchExact(query.term)
    case 'Regex':
      return searchRegex(query.pattern, query.flags)
    case 'Range':
      return searchRange(query.field, query.min, query.max)
  }
}
```

## Anti-Patterns

### 1. Raw TypeScript Types (BANNED)

```typescript
// WRONG — No runtime validation
interface User {
  id: string
  name: string
  email: string
}

// CORRECT
const User = Schema.Struct({
  id: Schema.String,
  name: Schema.String,
  email: Schema.String,
})
type User = typeof User.Type
```

### 2. String Literals Without Schema.Literal

```typescript
// WRONG — No runtime representation
type Status = "pending" | "active" | "archived"

// CORRECT
const Status = Schema.Literal("pending", "active", "archived")
type Status = typeof Status.Type
```

### 3. Missing `_tag` for Discriminated Unions

```typescript
// WRONG — Manual _tag field
const UserCreated = Schema.Struct({
  _tag: Schema.Literal('UserCreated'),
  userId: Schema.String,
})

// CORRECT — TaggedStruct auto-generates _tag
const UserCreated = Schema.TaggedStruct('UserCreated', {
  userId: Schema.String,
})
```

### 4. Not Using Built-in Refinements

```typescript
// WRONG — Manual filter
const PositiveNumber = Schema.Number.pipe(
  Schema.filter((n) => n > 0)
)

// CORRECT — Built-in refinement
const PositiveNumber = Schema.Number.pipe(Schema.positive())
```

## Quick Reference

| Need | Schema Constructor | Example |
|------|-------------------|---------|
| Plain object | `Schema.Struct({ ... })` | `Schema.Struct({ name: Schema.String })` |
| Discriminated union | `Schema.TaggedStruct("Tag", { ... })` | `Schema.TaggedStruct("UserCreated", { id: Schema.String })` |
| Entity with methods | `Schema.TaggedClass<T>()("Tag", { ... })` | `class User extends Schema.TaggedClass<User>()("User", { ... })` |
| Enum values | `Schema.Literal("a", "b")` | `Schema.Literal("pending", "active")` |
| Array | `Schema.Array(itemSchema)` | `Schema.Array(Schema.String)` |
| Dictionary | `Schema.Record({ key, value })` | `Schema.Record({ key: Schema.String, value: Schema.Number })` |
| Optional field | `Schema.optional(schema)` | `Schema.optional(Schema.String)` |
| Nullable | `Schema.NullOr(schema)` | `Schema.NullOr(Schema.String)` |
| Refinement | `schema.pipe(Schema.filter(...))` | `Schema.Number.pipe(Schema.positive())` |
| Branded type | `schema.pipe(Schema.brand("Name"))` | `Schema.String.pipe(Schema.brand("UserId"))` |
| Transformation | `Schema.transform(from, to, { decode, encode })` | `Schema.DateFromString` |
| Union | `Schema.Union(A, B, C)` | `Schema.Union(ExactQuery, RegexQuery)` |

## Related Skills

- **effect-service-authoring** — Use schemas in service interfaces
- **effect-atom-integration** — Validate atom values with schemas
- **effect-testing-patterns** — Test schema validation
