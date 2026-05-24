---
name: Pattern Matching
description: This skill should be used when the user asks about "Effect Match", "pattern matching", "Match.type", "Match.tag", "Match.when", "Schema.is()", "Schema.is with Match", "exhaustive matching", "discriminated unions", "Match.value", "converting switch to Match", "converting if/else to Match", "TaggedClass with Match", or needs to understand how Effect provides type-safe exhaustive pattern matching.
version: 1.0.0
---

# Pattern Matching in Effect

## Overview

**Pattern matching replaces ALL imperative control flow in Effect code.** There should be ZERO `if/else` statements, `switch/case` blocks, or ternary operators in idiomatic Effect code.

Effect's `Match` module provides:

- **Exhaustive matching** - Compiler ensures all cases handled
- **Type narrowing** - Automatic type inference in each branch
- **Composable matchers** - Build complex patterns from simple ones
- **Predicate support** - Match on conditions, not just values

### What to Use Instead of Imperative Code

| Imperative Pattern | Effect Replacement |
|-------------------|-------------------|
| `if/else` chains | `Match.value` + `Match.when` |
| `switch/case` statements | `Match.type` + `Match.tag` |
| Ternary operators (`? :`) | `Match.value` + `Match.when` |
| Null checks | `Option.match` |
| Error checks | `Either.match` or `Effect.match` |
| Type guards | `Match.when` with `Schema.is()` |

**When you encounter imperative control flow, refactor it to pattern matching immediately.**

## Basic Matching

### Match.value - Match a Value

```typescript
import { Match } from "effect"

const result = Match.value(input).pipe(
  Match.when("admin", () => "Full access"),
  Match.when("user", () => "Limited access"),
  Match.when("guest", () => "Read only"),
  Match.exhaustive
)
```

### Match.type - Create Reusable Matcher

```typescript
const rolePermissions = Match.type<"admin" | "user" | "guest">().pipe(
  Match.when("admin", () => "Full access"),
  Match.when("user", () => "Limited access"),
  Match.when("guest", () => "Read only"),
  Match.exhaustive
)

// Use multiple times
const perm1 = rolePermissions("admin")
const perm2 = rolePermissions("guest")
```

## Matching Discriminated Unions

### Match.tag - Match by _tag

```typescript
type Shape =
  | { _tag: "Circle"; radius: number }
  | { _tag: "Rectangle"; width: number; height: number }
  | { _tag: "Triangle"; base: number; height: number }

const area = Match.type<Shape>().pipe(
  Match.tag("Circle", ({ radius }) => Math.PI * radius ** 2),
  Match.tag("Rectangle", ({ width, height }) => width * height),
  Match.tag("Triangle", ({ base, height }) => (base * height) / 2),
  Match.exhaustive
)

area({ _tag: "Circle", radius: 5 }) // 78.54...
```

### Handling Effect Errors

```typescript
type AppError =
  | { _tag: "NetworkError"; url: string }
  | { _tag: "ValidationError"; field: string; message: string }
  | { _tag: "AuthError"; reason: string }

const handleError = Match.type<AppError>().pipe(
  Match.tag("NetworkError", (e) => `Failed to fetch ${e.url}`),
  Match.tag("ValidationError", (e) => `${e.field}: ${e.message}`),
  Match.tag("AuthError", (e) => `Auth failed: ${e.reason}`),
  Match.exhaustive
)
```

## Conditional Matching

### Match.when - Match with Predicate

```typescript
const describeNumber = Match.type<number>().pipe(
  Match.when((n) => n < 0, () => "negative"),
  Match.when((n) => n === 0, () => "zero"),
  Match.when((n) => n > 0 && n < 10, () => "small positive"),
  Match.when((n) => n >= 10, () => "large positive"),
  Match.exhaustive
)
```

### Match.when with Refinement

```typescript
const processInput = Match.type<string | number | boolean>().pipe(
  Match.when(
    (x): x is string => typeof x === "string",
    (s) => `String: ${s.toUpperCase()}`
  ),
  Match.when(
    (x): x is number => typeof x === "number",
    (n) => `Number: ${n * 2}`
  ),
  Match.when(
    (x): x is boolean => typeof x === "boolean",
    (b) => `Boolean: ${!b}`
  ),
  Match.exhaustive
)
```

## Non-Exhaustive Matching

### Match.orElse - Provide Default

```typescript
const greet = Match.type<string>().pipe(
  Match.when("morning", () => "Good morning!"),
  Match.when("evening", () => "Good evening!"),
  Match.orElse(() => "Hello!")
)

greet("morning")  // "Good morning!"
greet("afternoon") // "Hello!"
```

### Match.orElseAbsurd - Assert Exhaustive

```typescript
// Use when you believe all cases are covered
// Throws at runtime if unhandled case reached
const handle = Match.type<"a" | "b">().pipe(
  Match.when("a", () => 1),
  Match.when("b", () => 2),
  Match.orElseAbsurd
)
```

## Advanced Patterns

### Match.not - Negative Matching

```typescript
const classify = Match.type<number>().pipe(
  Match.when((n) => n === 0, () => "zero"),
  Match.not((n) => n > 0, () => "negative"),  // Matches when NOT positive
  Match.orElse(() => "positive")
)
```

### Match.whenOr - Multiple Patterns

```typescript
const isWeekend = Match.type<string>().pipe(
  Match.whenOr("Saturday", "Sunday", () => true),
  Match.orElse(() => false)
)
```

### Match.whenAnd - Combined Conditions

```typescript
interface User {
  role: "admin" | "user"
  verified: boolean
}

const canDelete = Match.type<User>().pipe(
  Match.whenAnd(
    { role: "admin" },
    (u) => u.verified,
    () => true
  ),
  Match.orElse(() => false)
)
```

## Pattern Objects

### Matching Object Shapes

```typescript
const processEvent = Match.type<Event>().pipe(
  Match.when({ type: "click" }, (e) => handleClick(e)),
  Match.when({ type: "keydown" }, (e) => handleKeydown(e)),
  Match.when({ type: "submit" }, (e) => handleSubmit(e)),
  Match.orElse(() => { /* unknown event */ })
)
```

### Nested Pattern Matching

```typescript
interface Response {
  status: number
  data: { type: string; value: unknown }
}

const handleResponse = Match.type<Response>().pipe(
  Match.when(
    { status: 200, data: { type: "user" } },
    (r) => `User: ${r.data.value}`
  ),
  Match.when(
    { status: 200, data: { type: "product" } },
    (r) => `Product: ${r.data.value}`
  ),
  Match.when({ status: 404 }, () => "Not found"),
  Match.when({ status: 500 }, () => "Server error"),
  Match.orElse(() => "Unknown response")
)
```

## Converting from if/else

### Before (if/else)

```typescript
function processStatus(status: Status): string {
  if (status === "pending") {
    return "Waiting..."
  } else if (status === "active") {
    return "In progress"
  } else if (status === "completed") {
    return "Done!"
  } else if (status === "failed") {
    return "Error occurred"
  } else {
    return "Unknown"
  }
}
```

### After (Match)

```typescript
const processStatus = Match.type<Status>().pipe(
  Match.when("pending", () => "Waiting..."),
  Match.when("active", () => "In progress"),
  Match.when("completed", () => "Done!"),
  Match.when("failed", () => "Error occurred"),
  Match.exhaustive // Compile error if status type changes!
)
```

## Converting from switch

### Before (switch)

```typescript
function getDiscount(userType: UserType): number {
  switch (userType) {
    case "regular":
      return 0
    case "premium":
      return 10
    case "vip":
      return 20
    default:
      return 0
  }
}
```

### After (Match)

```typescript
const getDiscount = Match.type<UserType>().pipe(
  Match.when("regular", () => 0),
  Match.when("premium", () => 10),
  Match.when("vip", () => 20),
  Match.exhaustive
)
```

## With Effects

```typescript
const handleError = (error: AppError) =>
  Match.value(error).pipe(
    Match.tag("NetworkError", (e) =>
      Effect.gen(function* () {
        yield* Effect.logError("Network failure", { url: e.url })
        return yield* Effect.fail(e)
      })
    ),
    Match.tag("ValidationError", (e) =>
      Effect.succeed({ field: e.field, message: e.message })
    ),
    Match.tag("AuthError", () =>
      Effect.redirect("/login")
    ),
    Match.exhaustive
  )
```

## Schema.is() with Match (For Schema Types Only)

**Use Schema.is() in Match.when patterns** to combine Schema validation with pattern matching. This works with `Schema.TaggedClass` and other Schema types.

**Use `Schema.TaggedError` for domain errors** - they work with `Schema.is()`, `Effect.catchTag`, and `Match.tag`:
- Use `Schema.is(ErrorClass)` for type guards on errors
- Use `Effect.catchTag("ErrorName", ...)` for error handling
- Use `Match.tag("ErrorName", ...)` when matching on errors (including predicates)

### Schema.is() as Type Guard

```typescript
import { Schema, Match } from "effect"

// Define schemas with TaggedClass for methods
class Circle extends Schema.TaggedClass<Circle>()("Circle", {
  radius: Schema.Number
}) {
  get area() { return Math.PI * this.radius ** 2 }
  get circumference() { return 2 * Math.PI * this.radius }
}

class Rectangle extends Schema.TaggedClass<Rectangle>()("Rectangle", {
  width: Schema.Number,
  height: Schema.Number
}) {
  get area() { return this.width * this.height }
  get perimeter() { return 2 * (this.width + this.height) }
}

const Shape = Schema.Union(Circle, Rectangle)
type Shape = Schema.Schema.Type<typeof Shape>

// Schema.is() provides type guard + access to class methods
const describeShape = (shape: Shape) =>
  Match.value(shape).pipe(
    Match.when(Schema.is(Circle), (c) =>
      `Circle: area=${c.area.toFixed(2)}, circumference=${c.circumference.toFixed(2)}`
    ),
    Match.when(Schema.is(Rectangle), (r) =>
      `Rectangle: area=${r.area}, perimeter=${r.perimeter}`
    ),
    Match.exhaustive
  )
```

### Schema.is() vs Match.tag

```typescript
// Match.tag - simpler, when you just need the data
const getShapeName = (shape: Shape) =>
  Match.value(shape).pipe(
    Match.tag("Circle", () => "circle"),
    Match.tag("Rectangle", () => "rectangle"),
    Match.exhaustive
  )

// Schema.is() - when you need class methods or type narrowing
const processShape = (shape: Shape) =>
  Match.value(shape).pipe(
    Match.when(Schema.is(Circle), (c) => c.area),      // Can use .area method
    Match.when(Schema.is(Rectangle), (r) => r.area),   // Can use .area method
    Match.exhaustive
  )
```

### Validating Unknown Data with Schema.is()

```typescript
// Schema.is() also works for runtime validation of unknown data
const handleUnknown = (input: unknown) =>
  Match.value(input).pipe(
    Match.when(Schema.is(Circle), (c) => `Valid circle with radius ${c.radius}`),
    Match.when(Schema.is(Rectangle), (r) => `Valid rectangle ${r.width}x${r.height}`),
    Match.orElse(() => "Invalid shape")
  )

// Or use for type narrowing
const processInput = (input: unknown) => {
  if (Schema.is(Circle)(input)) {
    console.log(`Circle area: ${input.area}`)  // Type is Circle, has methods
  }
}
```

### Complete Example: State Machine

```typescript
import { Schema, Match, Effect } from "effect"

// Define states with TaggedClass
class Draft extends Schema.TaggedClass<Draft>()("Draft", {
  content: Schema.String
}) {
  get isEmpty() { return this.content.trim().length === 0 }
}

class Published extends Schema.TaggedClass<Published>()("Published", {
  content: Schema.String,
  publishedAt: Schema.Date
}) {
  get daysSincePublish() {
    return Math.floor((Date.now() - this.publishedAt.getTime()) / 86400000)
  }
}

class Archived extends Schema.TaggedClass<Archived>()("Archived", {
  content: Schema.String,
  archivedReason: Schema.String
}) {}

const Article = Schema.Union(Draft, Published, Archived)
type Article = Schema.Schema.Type<typeof Article>

// Process with Schema.is() to access class methods
const getArticleStatus = (article: Article) =>
  Match.value(article).pipe(
    Match.when(Schema.is(Draft), (d) =>
      d.isEmpty ? "Empty draft" : "Draft with content"
    ),
    Match.when(Schema.is(Published), (p) =>
      `Published ${p.daysSincePublish} days ago`
    ),
    Match.when(Schema.is(Archived), (a) =>
      `Archived: ${a.archivedReason}`
    ),
    Match.exhaustive
  )
```

## Best Practices

### CRITICAL: No Imperative Code

1. **NEVER use if/else** - Replace with Match.value + Match.when
2. **NEVER use switch/case** - Replace with Match.type + Match.tag
3. **NEVER use ternary operators** - Replace with Match.value + Match.when
4. **NEVER use `if (x != null)`** - Replace with Option.match
5. **NEVER check error flags** - Replace with Either.match or Effect.match
6. **NEVER access `._tag` directly** - Replace with Match.tag or Schema.is()
7. **Refactor imperative code immediately** - This is mandatory, not optional

### General Best Practices

1. **Use Schema.is() in Match.when** - Access class methods with proper type narrowing
2. **Use Schema.TaggedClass with Match** - Define unions with classes, match with Schema.is()
3. **Prefer Match.exhaustive** - Catch missing cases at compile time
4. **Use Match.tag for simple cases** - When you don't need class methods
5. **Create reusable matchers** - Use Match.type() for repeated patterns
6. **Handle edge cases with Match.when** - Predicates for complex logic

## Additional Resources

For comprehensive pattern matching documentation, consult `${CLAUDE_PLUGIN_ROOT}/references/llms-full.txt`.

Search for these sections:
- "Pattern Matching" for full API reference
