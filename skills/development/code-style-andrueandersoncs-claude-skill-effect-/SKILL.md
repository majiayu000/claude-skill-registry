---
name: Code Style
description: This skill should be used EVERY TIME you're writing TypeScript with Effect, especially when the user asks about "Effect best practices", "Effect code style", "idiomatic Effect", "functional programming", "no loops", "no for loops", "avoid imperative", "Effect Array", "Effect Record", "Effect Struct", "Effect Tuple", "Effect Predicate", "Schema-first", "Match-first", "when to use Schema", "when to use Match", "branded types", "dual APIs", "Effect guidelines", "do notation", "Effect.gen", "pipe vs method chaining", "Effect naming conventions", "Effect project structure", "data modeling in Effect", or needs to understand idiomatic Effect-TS patterns and conventions.
version: 1.1.0
---

# Code Style in Effect

## Overview

Effect's idiomatic style centers on three core principles:

1. **Functional Programming Only** - No imperative logic (loops, mutation, conditionals)
2. **Schema-First Data Modeling** - Define ALL data structures as Effect Schemas
3. **Match-First Control Flow** - Define ALL conditional logic using Effect Match

Additional patterns include:

- **Branded types** - Nominal typing for primitives (built into Schema)
- **Dual APIs** - Both data-first and data-last
- **Generator syntax** - Effect.gen for readability
- **Project organization** - Layers, services, domains

## Core Principles

### 0. No Imperative Logic - Functional Programming Only

**NEVER use imperative constructs.** All code must follow functional programming principles:

- **No conditionals**: `if/else`, `switch/case`, ternary operators
- **No loops**: `for`, `while`, `do...while`, `for...of`, `for...in`
- **No mutation**: Reassignment, push/pop/splice, property mutation

**Use instead:**

- Pattern matching (`Match`, `Option.match`, `Either.match`, `Array.match`)
- Effect's `Array` module (`Array.map`, `Array.filter`, `Array.reduce`, `Array.flatMap`, `Array.filterMap`, etc.)
- Effect's `Record` module (`Record.map`, `Record.filter`, `Record.get`, `Record.keys`, `Record.values`, etc.)
- Effect's `Struct` module (`Struct.pick`, `Struct.omit`, `Struct.evolve`, `Struct.get`, etc.)
- Effect's `Tuple` module (`Tuple.make`, `Tuple.getFirst`, `Tuple.mapBoth`, etc.)
- Effect's `Predicate` module (`Predicate.and`, `Predicate.or`, `Predicate.not`, `Predicate.struct`, etc.)
- Effect combinators (`Effect.forEach`, `Effect.all`, `Effect.reduce`)
- Effect's `Function` module (`pipe`, `flow`, `identity`, `constant`, `compose`)
- Recursion for complex iteration
- First-class functions (pass functions as arguments, return functions)

#### Conditionals - Use Pattern Matching

- **`if/else` chains** → `Match.value` + `Match.when`
- **`switch/case` statements** → `Match.type` + `Match.tag` or `Match.when`
- **Ternary operators (`? :`)** → `Match.value` + `Match.when`
- **Optional chaining conditionals** → `Option.match`
- **Result/error conditionals** → `Either.match` or `Effect.match`

```typescript
// ❌ FORBIDDEN: if/else
if (user.role === "admin") {
  return "full access"
} else if (user.role === "user") {
  return "limited access"
} else {
  return "no access"
}

// ❌ FORBIDDEN: switch/case
switch (status) {
  case "pending": return "waiting"
  case "active": return "running"
  default: return "unknown"
}

// ❌ FORBIDDEN: ternary
const message = isError ? "Failed" : "Success"

// ❌ FORBIDDEN: direct ._tag access
if (event._tag === "UserCreated") { ... }
const isCreated = event._tag === "UserCreated"

// ❌ FORBIDDEN: ._tag in type definitions
type ConflictTag = Conflict["_tag"]  // Never extract _tag as a type

// ❌ FORBIDDEN: ._tag in array predicates
const hasConflict = conflicts.some((c) => c._tag === "MergeConflict")
const mergeConflicts = conflicts.filter((c) => c._tag === "MergeConflict")
const countMerge = conflicts.filter((c) => c._tag === "MergeConflict").length

// ✅ REQUIRED: Schema.is() as predicate
const hasConflict = conflicts.some(Schema.is(MergeConflict))
const mergeConflicts = conflicts.filter(Schema.is(MergeConflict))
const countMerge = conflicts.filter(Schema.is(MergeConflict)).length

// ✅ REQUIRED: Match.value
const getAccess = (user: User) =>
  Match.value(user.role).pipe(
    Match.when("admin", () => "full access"),
    Match.when("user", () => "limited access"),
    Match.orElse(() => "no access")
  )

// ✅ REQUIRED: Match.type
const getStatusMessage = Match.type<Status>().pipe(
  Match.when("pending", () => "waiting"),
  Match.when("active", () => "running"),
  Match.exhaustive
)

// ✅ REQUIRED: Option.match for nullable/optional
const displayName = Option.match(maybeUser, {
  onNone: () => "Guest",
  onSome: (user) => user.name
})

// ✅ REQUIRED: Either.match for results
const result = Either.match(parseResult, {
  onLeft: (error) => `Error: ${error}`,
  onRight: (value) => `Success: ${value}`
})

// ✅ REQUIRED: Match.tag for discriminated unions (not ._tag access)
const handleEvent = Match.type<AppEvent>().pipe(
  Match.tag("UserCreated", (e) => notifyAdmin(e.userId)),
  Match.tag("UserDeleted", (e) => cleanupData(e.userId)),
  Match.exhaustive
)

// ✅ REQUIRED: Schema.is() for type guards on Schema types (Schema.TaggedClass)
if (Schema.is(UserCreated)(event)) {
  // event is narrowed to UserCreated
}

// Schema.TaggedError works with Schema.is(), Effect.catchTag, and Match.tag.
// Always use Schema.TaggedError for domain errors.
```

**When you encounter imperative conditionals in existing code, refactor them immediately.**

#### Loops - Use Effect's Array Module and Recursion

**NEVER use `for`, `while`, `do...while`, `for...of`, or `for...in` loops.** Use Effect's functional alternatives.

**Why Effect's Array module over native Array methods:**

- `Array.findFirst` returns `Option<A>` instead of `A | undefined`
- `Array.get` returns `Option<A>` for safe indexing
- `Array.filterMap` combines filter and map in one pass
- `Array.partition` returns typed tuple `[excluded, satisfying]`
- `Array.groupBy` returns `Record<K, NonEmptyArray<A>>`
- `Array.match` provides exhaustive empty/non-empty handling
- All functions work with `pipe` for composable pipelines
- Consistent dual API (data-first and data-last)

```typescript
import { Array, pipe } from "effect"

// ❌ FORBIDDEN: for loop
const doubled = []
for (let i = 0; i < numbers.length; i++) {
  doubled.push(numbers[i] * 2)
}

// ❌ FORBIDDEN: for...of loop
const results = []
for (const item of items) {
  results.push(process(item))
}

// ❌ FORBIDDEN: while loop
let sum = 0
let i = 0
while (i < numbers.length) {
  sum += numbers[i]
  i++
}

// ❌ FORBIDDEN: forEach with mutation
const output = []
items.forEach(item => output.push(transform(item)))

// ✅ REQUIRED: Array.map for transformation
const doubled = Array.map(numbers, (n) => n * 2)
// or with pipe
const doubled = pipe(numbers, Array.map((n) => n * 2))

// ✅ REQUIRED: Array.filter for selection
const adults = Array.filter(users, (u) => u.age >= 18)

// ✅ REQUIRED: Array.reduce for accumulation
const sum = Array.reduce(numbers, 0, (acc, n) => acc + n)

// ✅ REQUIRED: Array.flatMap for one-to-many
const allTags = Array.flatMap(posts, (post) => post.tags)

// ✅ REQUIRED: Array.findFirst for search (returns Option)
const admin = Array.findFirst(users, (u) => u.role === "admin")

// ✅ REQUIRED: Array.some/every for predicates
const hasAdmin = Array.some(users, (u) => u.role === "admin")
const allVerified = Array.every(users, (u) => u.verified)

// ✅ REQUIRED: Array.filterMap for filter + transform in one pass
const validEmails = Array.filterMap(users, (u) =>
  isValidEmail(u.email) ? Option.some(u.email) : Option.none()
)

// ✅ REQUIRED: Array.partition to split by predicate
const [minors, adults] = Array.partition(users, (u) => u.age >= 18)

// ✅ REQUIRED: Array.groupBy for grouping
const usersByRole = Array.groupBy(users, (u) => u.role)

// ✅ REQUIRED: Array.dedupe for removing duplicates
const uniqueIds = Array.dedupe(ids)

// ✅ REQUIRED: Array.match for empty vs non-empty handling
const message = Array.match(items, {
  onEmpty: () => "No items",
  onNonEmpty: (items) => `${items.length} items`
})
```

**Record operations - use Effect's Record module:**

```typescript
import { Record, pipe } from "effect"

// ✅ REQUIRED: Record.map for transforming values
const doubled = Record.map(prices, (price) => price * 2)

// ✅ REQUIRED: Record.filter for filtering entries
const expensive = Record.filter(prices, (price) => price > 100)

// ✅ REQUIRED: Record.get for safe access (returns Option)
const price = Record.get(prices, "item1")

// ✅ REQUIRED: Record.keys and Record.values
const allKeys = Record.keys(config)
const allValues = Record.values(config)

// ✅ REQUIRED: Record.fromEntries and Record.toEntries
const record = Record.fromEntries([["a", 1], ["b", 2]])
const entries = Record.toEntries(record)

// ✅ REQUIRED: Record.filterMap for filter + transform
const validPrices = Record.filterMap(rawPrices, (value) =>
  typeof value === "number" ? Option.some(value) : Option.none()
)
```

**Struct operations - use Effect's Struct module:**

```typescript
import { Struct, pipe } from "effect"

// ✅ REQUIRED: Struct.pick for selecting properties
const namePart = Struct.pick(user, "firstName", "lastName")

// ✅ REQUIRED: Struct.omit for excluding properties
const publicUser = Struct.omit(user, "password", "ssn")

// ✅ REQUIRED: Struct.evolve for transforming specific fields
const updated = Struct.evolve(user, {
  age: (age) => age + 1,
  name: (name) => name.toUpperCase()
})

// ✅ REQUIRED: Struct.get for property access
const getName = Struct.get("name")
const name = getName(user)
```

**Tuple operations - use Effect's Tuple module:**

```typescript
import { Tuple } from "effect"

// ✅ REQUIRED: Tuple.make for creating tuples
const pair = Tuple.make("key", 42)

// ✅ REQUIRED: Tuple.getFirst/getSecond for access
const key = Tuple.getFirst(pair)
const value = Tuple.getSecond(pair)

// ✅ REQUIRED: Tuple.mapFirst/mapSecond/mapBoth for transformation
const upperKey = Tuple.mapFirst(pair, (s) => s.toUpperCase())
const doubled = Tuple.mapSecond(pair, (n) => n * 2)
const both = Tuple.mapBoth(pair, {
  onFirst: (s) => s.toUpperCase(),
  onSecond: (n) => n * 2
})

// ✅ REQUIRED: Tuple.at for indexed access
const first = Tuple.at(tuple, 0)
```

**Predicate operations - use Effect's Predicate module:**

```typescript
import { Predicate } from "effect"

// ✅ REQUIRED: Predicate.and/or/not for combining predicates
const isPositive = (n: number) => n > 0
const isEven = (n: number) => n % 2 === 0
const isPositiveAndEven = Predicate.and(isPositive, isEven)
const isPositiveOrEven = Predicate.or(isPositive, isEven)
const isNegative = Predicate.not(isPositive)

// ✅ REQUIRED: Predicate.struct for validating object shapes
const isValidUser = Predicate.struct({
  name: Predicate.isString,
  age: Predicate.isNumber
})

// ✅ REQUIRED: Predicate.tuple for validating tuple shapes
const isStringNumberPair = Predicate.tuple(Predicate.isString, Predicate.isNumber)

// ✅ REQUIRED: Built-in type guards
Predicate.isString(value)
Predicate.isNumber(value)
Predicate.isNullable(value)
Predicate.isNotNullable(value)
Predicate.isRecord(value)
```

**Effect loops - use Effect combinators:**

```typescript
// ❌ FORBIDDEN: for...of with yield*
const processAll = Effect.gen(function* () {
  const results = []
  for (const item of items) {
    const result = yield* processItem(item)
    results.push(result)
  }
  return results
})

// ✅ REQUIRED: Effect.forEach for sequential
const processAll = Effect.forEach(items, processItem)

// ✅ REQUIRED: Effect.all for parallel (when items are Effects)
const results = Effect.all(effects)

// ✅ REQUIRED: Effect.all with concurrency
const results = Effect.all(effects, { concurrency: 10 })

// ✅ REQUIRED: Effect.reduce for accumulation
const total = Effect.reduce(items, 0, (acc, item) =>
  getPrice(item).pipe(Effect.map((price) => acc + price))
)

// ✅ REQUIRED: Stream for large/infinite sequences
const processed = Stream.fromIterable(items).pipe(
  Stream.mapEffect(processItem),
  Stream.runCollect
)
```

**Recursion for complex iteration:**

```typescript
// ❌ FORBIDDEN: while loop for tree traversal
const collectLeaves = (node) => {
  const leaves = []
  const stack = [node]
  while (stack.length > 0) {
    const current = stack.pop()
    if (current.children.length === 0) {
      leaves.push(current)
    } else {
      stack.push(...current.children)
    }
  }
  return leaves
}

// ✅ REQUIRED: Recursion for tree traversal
const collectLeaves = (node: TreeNode): ReadonlyArray<TreeNode> =>
  Array.match(node.children, {
    onEmpty: () => [node],
    onNonEmpty: (children) => Array.flatMap(children, collectLeaves)
  })

// ✅ REQUIRED: Recursion with Effect
const processTree = (node: TreeNode): Effect.Effect<Result> =>
  node.children.length === 0
    ? processLeaf(node)
    : Effect.forEach(node.children, processTree).pipe(
        Effect.flatMap(combineResults)
      )
```

**First-class functions - use Effect's Function module:**

```typescript
import { Array, Function, pipe, flow } from "effect"

// ❌ BAD: Inline logic repeated
const processUsers = (users: Array<User>) =>
  users.filter((u) => u.active).map((u) => u.email)
const processOrders = (orders: Array<Order>) =>
  orders.filter((o) => o.active).map((o) => o.total)

// ✅ GOOD: Extract reusable predicates and transformers
const isActive = <T extends { active: boolean }>(item: T) => item.active
const getEmail = (user: User) => user.email
const getTotal = (order: Order) => order.total

// ✅ GOOD: Use pipe for data transformation pipelines
const processUsers = (users: Array<User>) =>
  pipe(users, Array.filter(isActive), Array.map(getEmail))

const processOrders = (orders: Array<Order>) =>
  pipe(orders, Array.filter(isActive), Array.map(getTotal))

// ✅ GOOD: Use flow to compose reusable pipelines
const getActiveEmails = flow(
  Array.filter(isActive<User>),
  Array.map(getEmail)
)

const getActiveTotals = flow(
  Array.filter(isActive<Order>),
  Array.map(getTotal)
)

// ✅ GOOD: Use Function.compose for simple composition
const parseAndValidate = Function.compose(parse, validate)

// ✅ GOOD: Use Function.identity for pass-through
const transform = shouldTransform ? myTransform : Function.identity

// ✅ GOOD: Use Function.constant for fixed values
const getDefaultUser = Function.constant(defaultUser)
```

**When you encounter imperative loops in existing code, refactor them immediately.** This is not optional - imperative logic is a code smell that must be eliminated.

### 1. Schema-First Data Modeling

**Define ALL data structures as Effect Schemas.** This is the foundation of type-safe Effect code.

**Key principles:**

- **Use Schema.Class over Schema.Struct** - Get methods and Schema.is() type guards
- **Use tagged unions over optional properties** - Make states explicit
- **Use Schema.is() in Match patterns** - Combine validation with matching

```typescript
import { Schema, Match } from "effect";

// ✅ GOOD: Class-based schema with methods
class User extends Schema.Class<User>("User")({
  id: Schema.String.pipe(Schema.brand("UserId")),
  email: Schema.String.pipe(Schema.pattern(/^[^@]+@[^@]+\.[^@]+$/)),
  name: Schema.String.pipe(Schema.nonEmptyString()),
  createdAt: Schema.Date,
}) {
  get emailDomain() {
    return this.email.split("@")[1];
  }
}

// ✅ GOOD: Tagged union over optional properties
class Pending extends Schema.TaggedClass<Pending>()("Pending", {
  orderId: Schema.String,
  items: Schema.Array(Schema.String),
}) {}

class Shipped extends Schema.TaggedClass<Shipped>()("Shipped", {
  orderId: Schema.String,
  items: Schema.Array(Schema.String),
  trackingNumber: Schema.String,
  shippedAt: Schema.Date,
}) {}

class Delivered extends Schema.TaggedClass<Delivered>()("Delivered", {
  orderId: Schema.String,
  items: Schema.Array(Schema.String),
  deliveredAt: Schema.Date,
}) {}

const Order = Schema.Union(Pending, Shipped, Delivered);
type Order = Schema.Schema.Type<typeof Order>;

// ✅ GOOD: Schema.is() in Match patterns
const getOrderStatus = (order: Order) =>
  Match.value(order).pipe(
    Match.when(Schema.is(Pending), () => "Awaiting shipment"),
    Match.when(Schema.is(Shipped), (o) => `Tracking: ${o.trackingNumber}`),
    Match.when(Schema.is(Delivered), (o) => `Delivered ${o.deliveredAt}`),
    Match.exhaustive,
  );
```

```typescript
// ❌ BAD: Optional properties hide state complexity
const Order = Schema.Struct({
  orderId: Schema.String,
  items: Schema.Array(Schema.String),
  trackingNumber: Schema.optional(Schema.String), // When is this set?
  shippedAt: Schema.optional(Schema.Date), // Unclear state
  deliveredAt: Schema.optional(Schema.Date), // Can be shipped AND delivered?
});
```

**Why Schema for everything:**

- Runtime validation at system boundaries
- Automatic type inference (no duplicate type definitions)
- Encode/decode for serialization
- JSON Schema generation for API docs
- Branded types built-in
- Composable transformations

### 2. Match-First Control Flow

**Define ALL conditional logic and algorithms using Effect Match.** Replace if/else chains, switch statements, and ternaries with exhaustive pattern matching.

```typescript
import { Match } from "effect";

// Process by discriminated union - use Match
const handleEvent = Match.type<AppEvent>().pipe(
  Match.tag("UserCreated", (event) => notifyAdmin(event.userId)),
  Match.tag("UserDeleted", (event) => cleanupData(event.userId)),
  Match.tag("OrderPlaced", (event) => processOrder(event.orderId)),
  Match.exhaustive,
);

// Transform values - use Match
const toHttpStatus = Match.type<AppError>().pipe(
  Match.tag("NotFound", () => 404),
  Match.tag("Unauthorized", () => 401),
  Match.tag("ValidationError", () => 400),
  Match.tag("InternalError", () => 500),
  Match.exhaustive,
);

// Handle options - use Option.match
const displayUser = (maybeUser: Option<User>) =>
  Option.match(maybeUser, {
    onNone: () => "Guest user",
    onSome: (user) => `Welcome, ${user.name}`
  });

// Multi-condition logic - use Match.when
const calculateDiscount = (order: Order) =>
  Match.value(order).pipe(
    Match.when({ total: (t) => t > 1000, isPremium: true }, () => 0.25),
    Match.when({ total: (t) => t > 1000 }, () => 0.15),
    Match.when({ isPremium: true }, () => 0.1),
    Match.when({ itemCount: (c) => c > 10 }, () => 0.05),
    Match.orElse(() => 0),
  );
```

**Why Match for everything:**

- Exhaustive checking catches missing cases at compile time
- Self-documenting code structure
- No forgotten else branches
- Easy to extend with new cases
- Works perfectly with Schema discriminated unions

### 3. Property-Based Testing with Schema Arbitrary

**Every Schema generates test data via `Arbitrary.make()`.** This is the foundation of Effect testing — never hand-craft test objects.

> **CRITICAL: See the [Testing Skill](../testing/SKILL.md) for comprehensive testing guidance.** This section covers Schema-driven Arbitrary patterns; the Testing skill covers `@effect/vitest`, `it.effect`, `it.prop`, test layers, and the full service-oriented testing pattern.

**Key principles:**

- **Schema constraints generate constrained Arbitraries** — Filters are built into Schema, not fast-check
- **NEVER use fast-check `.filter()`** — Use properly-constrained Schemas instead
- **Use `it.prop` from `@effect/vitest`** — Integrates Schema Arbitrary directly
- **Test round-trips for every Schema** — Encode/decode must be lossless

#### Why Schema Constraints Over Fast-Check Filters

Fast-check filters (`.filter()`) discard generated values that don't match the predicate. This is:
- **Inefficient** — Generates and throws away invalid values
- **Fragile** — Can fail to find valid values if filter is too restrictive
- **Duplicative** — Your Schema already defines the constraints

The correct approach: **define constraints in your Schema**, then `Arbitrary.make()` generates valid values directly.

```typescript
import { Schema, Arbitrary } from "effect"
import * as fc from "fast-check"

// ❌ FORBIDDEN: Using fast-check filter
const badArbitrary = fc.integer().filter((n) => n >= 18 && n <= 100)
// Problem: Generates integers, throws away 99% of them

// ❌ FORBIDDEN: Filter on Schema Arbitrary
const UserArbitrary = Arbitrary.make(User)
const badFiltered = UserArbitrary(fc).filter((u) => u.age >= 18)
// Problem: Duplicates constraint logic, wasteful generation

// ✅ REQUIRED: Constraints in Schema definition
const Age = Schema.Number.pipe(
  Schema.int(),
  Schema.between(18, 100)  // Constraint built into Schema
)

class User extends Schema.Class<User>("User")({
  id: Schema.String.pipe(Schema.minLength(1)),
  name: Schema.String.pipe(Schema.nonEmptyString()),
  age: Age  // Uses constrained Age schema
}) {}

// ✅ REQUIRED: Arbitrary generates ONLY valid values
const UserArbitrary = Arbitrary.make(User)
fc.sample(UserArbitrary(fc), 5)
// All 5 users have age between 18-100, guaranteed
```

#### Common Schema Constraints for Arbitrary Generation

Use these Schema combinators to constrain generation (never filter):

```typescript
import { Schema } from "effect"

// Numeric constraints
Schema.Number.pipe(Schema.int())                    // Integers only
Schema.Number.pipe(Schema.positive())               // > 0
Schema.Number.pipe(Schema.nonNegative())            // >= 0
Schema.Number.pipe(Schema.between(1, 100))          // 1 <= n <= 100
Schema.Number.pipe(Schema.greaterThan(0))           // > 0
Schema.Number.pipe(Schema.lessThanOrEqualTo(100))   // <= 100

// String constraints
Schema.String.pipe(Schema.minLength(1))             // Non-empty
Schema.String.pipe(Schema.maxLength(100))           // Max 100 chars
Schema.String.pipe(Schema.length(10))               // Exactly 10 chars
Schema.String.pipe(Schema.nonEmptyString())         // Non-empty (alias)
Schema.String.pipe(Schema.pattern(/^[A-Z]{3}$/))    // Matches regex

// Array constraints
Schema.Array(Item).pipe(Schema.minItems(1))         // Non-empty array
Schema.Array(Item).pipe(Schema.maxItems(10))        // Max 10 items
Schema.Array(Item).pipe(Schema.itemsCount(5))       // Exactly 5 items
Schema.NonEmptyArray(Item)                          // Non-empty array

// Built-in constrained types
Schema.NonEmptyString                               // String with minLength(1)
Schema.Positive                                     // Number > 0
Schema.NonNegative                                  // Number >= 0
Schema.Int                                          // Integer
```

#### Custom Arbitrary Annotations (When Needed)

For complex constraints that Schema combinators can't express, use `arbitrary` annotation:

```typescript
import { Schema, Arbitrary } from "effect"
import * as fc from "fast-check"

// Custom email generation (pattern too complex for generation)
const Email = Schema.String.pipe(
  Schema.pattern(/^[^@]+@[^@]+\.[^@]+$/),
  Schema.annotations({
    arbitrary: () => (fc) => fc.emailAddress()  // Use fast-check's generator
  })
)

// Custom UUID generation
const UserId = Schema.String.pipe(
  Schema.annotations({
    arbitrary: () => (fc) => fc.uuid()
  })
)

// Custom date range
const BirthDate = Schema.Date.pipe(
  Schema.annotations({
    arbitrary: () => (fc) =>
      fc.date({
        min: new Date("1900-01-01"),
        max: new Date("2010-01-01")
      })
  })
)
```

#### Property Testing with it.prop

Use `it.prop` from `@effect/vitest` for property-based tests (see [Testing Skill](../testing/SKILL.md) for full details):

```typescript
import { it, expect } from "@effect/vitest"
import { Schema, Arbitrary } from "effect"

// Array form
it.prop("validates all generated users", [Arbitrary.make(User)], ([user]) => {
  expect(user.age).toBeGreaterThanOrEqual(18)
  expect(user.name.length).toBeGreaterThan(0)
})

// Object form
it.prop(
  "round-trip preserves data",
  { user: Arbitrary.make(User) },
  ({ user }) => {
    const encoded = Schema.encodeSync(User)(user)
    const decoded = Schema.decodeUnknownSync(User)(encoded)
    expect(decoded).toEqual(user)
  }
)

// Effect-based property test
it.effect.prop(
  "processes all order states",
  [Arbitrary.make(Order)],
  ([order]) =>
    Effect.gen(function* () {
      const result = yield* processOrder(order)
      expect(result).toBeDefined()
    })
)
```

### 4. Schema + Match Together

The most powerful pattern: **TaggedClass for data, Schema.is() in Match for logic.**

```typescript
import { Schema, Match } from "effect";

// Define all variants with TaggedClass (not Struct)
class CreditCard extends Schema.TaggedClass<CreditCard>()("CreditCard", {
  last4: Schema.String,
  expiryMonth: Schema.Number,
  expiryYear: Schema.Number,
}) {
  get isExpired() {
    const now = new Date();
    return (
      this.expiryYear < now.getFullYear() ||
      (this.expiryYear === now.getFullYear() && this.expiryMonth < now.getMonth() + 1)
    );
  }
}

class BankTransfer extends Schema.TaggedClass<BankTransfer>()("BankTransfer", {
  accountId: Schema.String,
  routingNumber: Schema.String,
}) {}

class Crypto extends Schema.TaggedClass<Crypto>()("Crypto", {
  walletAddress: Schema.String,
  network: Schema.Literal("ethereum", "bitcoin", "solana"),
}) {}

const PaymentMethod = Schema.Union(CreditCard, BankTransfer, Crypto);
type PaymentMethod = Schema.Schema.Type<typeof PaymentMethod>;

// Process with Schema.is() to access class methods
const processPayment = (method: PaymentMethod, amount: number) =>
  Match.value(method).pipe(
    Match.when(Schema.is(CreditCard), (card) =>
      card.isExpired ? Effect.fail("Card expired") : chargeCard(card.last4, amount),
    ),
    Match.when(Schema.is(BankTransfer), (bank) => initiateBankTransfer(bank.accountId, bank.routingNumber, amount)),
    Match.when(Schema.is(Crypto), (crypto) => sendCrypto(crypto.walletAddress, crypto.network, amount)),
    Match.exhaustive,
  );

// Also works with Match.tag for simple cases
const getPaymentLabel = (method: PaymentMethod) =>
  Match.value(method).pipe(
    Match.tag("CreditCard", (c) => `Card ending ${c.last4}`),
    Match.tag("BankTransfer", (b) => `Bank ${b.accountId}`),
    Match.tag("Crypto", (c) => `${c.network}: ${c.walletAddress.slice(0, 8)}...`),
    Match.exhaustive,
  );
```

## Branded Types

Prevent mixing up values of the same underlying type:

```typescript
import { Brand } from "effect";

// Define branded types
type UserId = string & Brand.Brand<"UserId">;
type OrderId = string & Brand.Brand<"OrderId">;

// Constructors
const UserId = Brand.nominal<UserId>();
const OrderId = Brand.nominal<OrderId>();

// Usage
const userId: UserId = UserId("user-123");
const orderId: OrderId = OrderId("order-456");

// Type error: can't assign UserId to OrderId
// const wrong: OrderId = userId
```

### With Validation

```typescript
import { Brand, Either } from "effect";

type Email = string & Brand.Brand<"Email">;

const Email = Brand.refined<Email>(
  (s) => /^[^@]+@[^@]+\.[^@]+$/.test(s),
  (s) => Brand.error(`Invalid email: ${s}`),
);

// Returns Either
const result = Email.either("test@example.com");
// Or throws
const email = Email("test@example.com");
```

### With Schema

```typescript
import { Schema } from "effect";

const UserId = Schema.String.pipe(Schema.brand("UserId"));
type UserId = Schema.Schema.Type<typeof UserId>;

const Email = Schema.String.pipe(Schema.pattern(/^[^@]+@[^@]+\.[^@]+$/), Schema.brand("Email"));
```

## Dual APIs

Most Effect functions support both styles:

### Data-Last (Pipeable) - Recommended

```typescript
import { Effect, pipe } from "effect";

// Using pipe
const result = pipe(
  Effect.succeed(1),
  Effect.map((n) => n + 1),
  Effect.flatMap((n) => Effect.succeed(n * 2)),
);

// Using method chaining
const result = Effect.succeed(1).pipe(
  Effect.map((n) => n + 1),
  Effect.flatMap((n) => Effect.succeed(n * 2)),
);
```

### Data-First

```typescript
// Useful for single transformations
const mapped = Effect.map(Effect.succeed(1), (n) => n + 1);
```

### Convention

- **Use data-last** for pipelines
- **Use data-first** for single operations
- **Be consistent** within a codebase

## Generator Syntax (Effect.gen)

The preferred way to write sequential Effect code:

```typescript
// Generator style - recommended
const program = Effect.gen(function* () {
  const user = yield* getUser(id);
  const orders = yield* getOrders(user.id);
  const enriched = yield* enrichOrders(orders);
  return { user, orders: enriched };
});

// Equivalent flatMap chain
const program = getUser(id).pipe(
  Effect.flatMap((user) =>
    getOrders(user.id).pipe(
      Effect.flatMap((orders) => enrichOrders(orders).pipe(Effect.map((enriched) => ({ user, orders: enriched })))),
    ),
  ),
);
```

### When to Use Effect.gen

- Sequential operations
- Complex control flow
- When readability matters
- Error handling with yield\*

### When to Use pipe

- Simple transformations
- Parallel operations
- Single-line operations

## Do Notation (Simplifying Nesting)

Alternative to generators for some cases:

```typescript
import { Effect } from "effect";

const program = Effect.Do.pipe(
  Effect.bind("user", () => getUser(id)),
  Effect.bind("orders", ({ user }) => getOrders(user.id)),
  Effect.bind("enriched", ({ orders }) => enrichOrders(orders)),
  Effect.map(({ user, enriched }) => ({ user, orders: enriched })),
);
```

## Project Structure

### Recommended Layout

```
src/
├── domain/           # Domain types and errors
│   ├── User.ts
│   ├── Order.ts
│   └── errors.ts
├── services/         # Service interfaces
│   ├── UserRepository.ts
│   └── OrderService.ts
├── implementations/  # Service implementations
│   ├── UserRepositoryLive.ts
│   └── OrderServiceLive.ts
├── layers/          # Layer composition
│   ├── AppLive.ts
│   └── TestLive.ts
├── http/            # HTTP handlers
│   └── routes.ts
└── main.ts          # Entry point
```

### Service Definition Pattern

```typescript
// services/UserRepository.ts
import { Context, Effect } from "effect";
import { User, UserId } from "../domain/User";
import { UserNotFound } from "../domain/errors";

export class UserRepository extends Context.Tag("UserRepository")<
  UserRepository,
  {
    readonly findById: (id: UserId) => Effect.Effect<User, UserNotFound>;
    readonly findByEmail: (email: string) => Effect.Effect<User, UserNotFound>;
    readonly save: (user: User) => Effect.Effect<void>;
    readonly delete: (id: UserId) => Effect.Effect<void>;
  }
>() {}
```

### Layer Composition Pattern

```typescript
// layers/AppLive.ts
import { Layer } from "effect";

// Infrastructure
const InfraLive = Layer.mergeAll(DatabaseLive, HttpClientLive, LoggerLive);

// Repositories
const RepositoriesLive = Layer.mergeAll(UserRepositoryLive, OrderRepositoryLive).pipe(Layer.provide(InfraLive));

// Services
const ServicesLive = Layer.mergeAll(UserServiceLive, OrderServiceLive).pipe(Layer.provide(RepositoriesLive));

// Full application
export const AppLive = ServicesLive;
```

## Naming Conventions

### Types and Interfaces

```typescript
// Domain types - PascalCase
interface User { ... }
interface Order { ... }

// Branded types - PascalCase
type UserId = string & Brand.Brand<"UserId">
type Email = string & Brand.Brand<"Email">

// Error types - PascalCase with descriptive suffix
class UserNotFound extends Schema.TaggedError<UserNotFound>()("UserNotFound", {...}) {}
class ValidationError extends Schema.TaggedError<ValidationError>()("ValidationError", {...}) {}
```

### Services

```typescript
// Service tag - PascalCase
class UserRepository extends Context.Tag("UserRepository")<...>() {}

// Layer implementations - PascalCase with Live/Test suffix
const UserRepositoryLive = Layer.effect(...)
const UserRepositoryTest = Layer.succeed(...)
```

### Functions

```typescript
// Effect-returning functions - camelCase
const getUser = (id: UserId): Effect.Effect<User, UserNotFound> => ...
const createOrder = (data: OrderData): Effect.Effect<Order, ValidationError> => ...

// Constructors - matching type name
const UserId = Brand.nominal<UserId>()
const User = (data: UserData): User => ...
```

## Error Handling Style

### Tagged Errors

```typescript
import { Schema } from "effect";

// Always use Schema.TaggedError for domain errors
class UserNotFound extends Schema.TaggedError<UserNotFound>()("UserNotFound", { userId: Schema.String }) {}

class ValidationError extends Schema.TaggedError<ValidationError>()("ValidationError", {
  field: Schema.String,
  message: Schema.String,
}) {}

// Use in services
const getUser = (id: string): Effect.Effect<User, UserNotFound> =>
  Effect.gen(function* () {
    const user = yield* findInDb(id);
    if (!user) {
      return yield* Effect.fail(new UserNotFound({ userId: id }));
    }
    return user;
  });
```

### Error Recovery Pattern

```typescript
const program = getUser(id).pipe(
  // Specific error handling
  Effect.catchTag("UserNotFound", (error) => Effect.succeed(defaultUser)),
  // Or match all errors
  Effect.catchTags({
    UserNotFound: () => Effect.succeed(defaultUser),
    ValidationError: (e) => Effect.fail(new BadRequest(e.message)),
  }),
);
```

## Best Practices Summary

### Do

- **ELIMINATE all imperative logic** - no if/else, switch/case, ternaries, for/while loops
- **Use Effect's data modules** - `Array`, `Record`, `Struct`, `Tuple` for data manipulation
- **Use Effect's Predicate module** - `Predicate.and`, `Predicate.or`, `Predicate.struct` for composing predicates
- **Use Effect's Function module** - `pipe`, `flow`, `identity`, `constant`, `compose`
- **Refactor imperative code on sight** - this is mandatory, not optional
- **Use Schema.Class/TaggedClass** - not Schema.Struct for domain entities
- **Use tagged unions over optional properties** - make states explicit
- **Use Schema.is() in Match.when patterns** - combine validation with matching
- **Use Match for ALL conditional logic** - replace if/else, switch, ternaries
- **Wrap ALL external dependencies in Services** - API calls, databases, file I/O, third-party SDKs, email, caches, queues MUST go through `Context.Tag` services
- **Create Test Layers for every Service** - `*Live` for production, `*Test` for testing. This is required for 100% test coverage.
- **Use `@effect/vitest` for ALL tests** - `it.effect`, `it.scoped`, `it.live`, `it.layer`, `it.prop` (see [Testing Skill](../testing/SKILL.md))
- **Use `Arbitrary.make(Schema)` for ALL test data** - Never hand-craft test objects
- **Define constraints in Schema, not fast-check filters** - `Schema.between()`, `Schema.minLength()`, etc. generate constrained values directly
- **Combine service test layers + Arbitrary** - Services control I/O, Arbitrary generates data — together they enable 100% coverage
- Use Effect.gen for sequential code
- Define services with Context.Tag
- Compose layers bottom-up
- Use Schema.TaggedError for domain errors (works with Match.tag and Schema.is())

### Don't - FORBIDDEN Patterns

- **NEVER call external APIs/databases/file systems directly in business logic** - always go through a `Context.Tag` service. Direct external calls make code untestable.
- **NEVER skip writing test Layers** - every service MUST have a test layer. Without test layers, coverage is incomplete.
- **NEVER use if/else** - always use Match.value + Match.when
- **NEVER use switch/case** - always use Match.type + Match.tag
- **NEVER use ternary operators** - always use Match.value + Match.when
- **NEVER use `if (x != null)`** - always use Option.match
- **NEVER use for/while/do...while loops** - use Effect's `Array.map`/`Array.filter`/`Array.reduce` or `Effect.forEach`
- **NEVER use for...of/for...in loops** - use Effect's `Array` module or `Effect` combinators
- **NEVER mutate arrays** (push/pop/splice) - use `Array.append`, `Array.prepend`, spread, or immutable operations
- **NEVER reassign variables** - use const and functional transformations
- **NEVER use native `Array.prototype.find`** - use `Array.findFirst` which returns `Option`
- **NEVER use native `array[index]`** - use `Array.get(array, index)` which returns `Option`
- **NEVER use native `Object.keys/values/entries`** - use `Record.keys`, `Record.values`, `Record.toEntries`
- **NEVER use native `record[key]`** - use `Record.get(record, key)` which returns `Option`
- **NEVER use manual `&&`/`||` for predicates** - use `Predicate.and`, `Predicate.or`, `Predicate.not`
- **NEVER check `.success` or similar** - always use Either.match or Effect.match
- **NEVER access `._tag` directly** - always use Match.tag or Schema.is() (for Schema types only)
- **NEVER extract `._tag` as a type** - e.g., `type Tag = Foo["_tag"]` is forbidden
- **NEVER use `._tag` in predicates** - use Schema.is(Variant) with .some()/.filter()
- **NEVER use JSON.parse()** - always use Schema.parseJson with a schema
- **NEVER use Schema.Any or Schema.Unknown as type weakening** - these are only permitted when the value is genuinely unconstrained at the domain level (e.g., `cause` field on error types capturing arbitrary caught exceptions, opaque pass-through payloads). If you can describe the data shape, define a proper schema instead.
- Use Schema.Struct for domain entities (use Schema.Class)
- Use optional properties for state (use tagged unions)
- Use plain TypeScript interfaces/types without Schema
- Mix async/await with Effect (except at boundaries)
- Use bare try/catch (use Effect.try)
- Create services without layers
- Throw exceptions (use Effect.fail)
- **NEVER use `Effect.runPromise` in tests** - use `it.effect` from `@effect/vitest`
- **NEVER import `it` from `vitest`** in Effect test files - import from `@effect/vitest`
- **NEVER hand-craft test data** - use `Arbitrary.make(Schema)` or `it.prop`
- **NEVER use fast-check `.filter()`** - define constraints in Schema (`Schema.between()`, `Schema.minLength()`, etc.) so Arbitrary generates valid values directly

## Related Skills

This skill covers high-level patterns and conventions. For detailed API usage and specific topics, consult these specialized skills:

> **CRITICAL: Always consult the [Testing Skill](../testing/SKILL.md) when writing tests.** It covers the full service-oriented testing pattern, `@effect/vitest` APIs (`it.effect`, `it.prop`, `it.layer`), test layers, and achieving 100% test coverage.

| Skill | Purpose | Key Topics |
|-------|---------|------------|
| [Testing](../testing/SKILL.md) | **Effect testing patterns** | **@effect/vitest, it.effect, it.prop, test layers, service mocking, Arbitrary** |
| [Effect Core](../effect-core/SKILL.md) | Core Effect type and APIs | Creating Effects, Effect.gen, pipe, map, flatMap, running Effects |
| [Error Management](../error-management/SKILL.md) | Typed error handling | catchTag, catchAll, mapError, orElse, error accumulation |
| [Pattern Matching](../pattern-matching/SKILL.md) | Match module APIs | Match.value, Match.type, Match.tag, Match.when, exhaustive matching |
| [Schema](../schema/SKILL.md) | Data modeling and validation | Schema.Class, Schema.Struct, parsing, transformations, filters |

These skills work together: this Code Style skill defines the **what** (patterns to follow), while the specialized skills define the **how** (API details).

## Additional Resources

For comprehensive code style documentation, consult `${CLAUDE_PLUGIN_ROOT}/references/llms-full.txt`.

Search for these sections:

- "Branded Types" for nominal typing
- "Dual APIs" for function styles
- "Guidelines" for best practices
- "Simplifying Excessive Nesting" for do notation
