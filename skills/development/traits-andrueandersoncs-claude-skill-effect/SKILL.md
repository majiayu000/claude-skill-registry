---
name: Traits
description: This skill should be used when the user asks about "Effect Equal", "Effect Hash", "Equivalence", "Order", "structural equality", "custom equality", "comparing objects", "sorting", "Equal.equals", "Hash.hash", "Equivalence.make", "Order.lessThan", "comparable types", or needs to understand how Effect handles equality, hashing, and ordering of values.
version: 1.0.0
---

# Traits in Effect

## Overview

Effect provides trait-based abstractions for:

- **Equal** - Structural equality comparison
- **Hash** - Hash code generation
- **Equivalence** - Custom equality relations
- **Order** - Ordering and comparison

These enable consistent behavior across Effect's data structures.

## Equal - Structural Equality

### The Equal Interface

```typescript
import { Equal } from "effect"

Equal.equals(a, b)

import { Data } from "effect"

class Person extends Data.Class<{
  name: string
  age: number
}> {}

const p1 = new Person({ name: "Alice", age: 30 })
const p2 = new Person({ name: "Alice", age: 30 })

Equal.equals(p1, p2)
p1 === p2
```

### Implementing Equal (Recommended: Use Data.Class)

**PREFER Data.Class** which provides Equal and Hash automatically:

```typescript
import { Data, Equal } from "effect"

// Data.Class provides Equal and Hash automatically
class Point extends Data.Class<{ readonly x: number; readonly y: number }> {}

const p1 = new Point({ x: 1, y: 2 })
const p2 = new Point({ x: 1, y: 2 })

Equal.equals(p1, p2)
```

For Schema types, use Schema.Class which also provides Equal:

```typescript
import { Schema, Equal } from "effect"

class Point extends Schema.Class<Point>("Point")({
  x: Schema.Number,
  y: Schema.Number
}) {}

const p1 = new Point({ x: 1, y: 2 })
const p2 = new Point({ x: 1, y: 2 })

Equal.equals(p1, p2) // true
```

### Why Equal Matters

Effect's collections (HashMap, HashSet) use Equal for lookups:

```typescript
import { HashMap, Data } from "effect"

class UserId extends Data.Class<{ id: string }> {}

const map = HashMap.make([
  [new UserId({ id: "1" }), "Alice"],
  [new UserId({ id: "2" }), "Bob"]
])

// Works because UserId implements Equal
HashMap.get(map, new UserId({ id: "1" })) // Option.some("Alice")
```

## Hash - Hash Code Generation

### The Hash Interface

```typescript
import { Hash } from "effect"

Hash.hash(value)

Hash.string("hello")
Hash.number(42)
Hash.combine(h1)(h2)
Hash.array([1, 2, 3])
```

### Hash Contract

Objects that are Equal MUST have the same hash:

```typescript
// If Equal.equals(a, b) === true
// Then Hash.hash(a) === Hash.hash(b)

// The reverse is NOT required:
// Same hash does NOT mean equal (hash collisions are allowed)
```

### Hash with Data.Class (Recommended)

**Data.Class provides both Equal and Hash automatically:**

```typescript
import { Data, Hash, Equal } from "effect"

class Rectangle extends Data.Class<{
  readonly width: number
  readonly height: number
}> {}

const r1 = new Rectangle({ width: 10, height: 5 })
const r2 = new Rectangle({ width: 10, height: 5 })

Equal.equals(r1, r2)
Hash.hash(r1) === Hash.hash(r2)
```

## Equivalence - Custom Equality Relations

### Creating Equivalences

```typescript
import { Equivalence } from "effect"

const caseInsensitive = Equivalence.make<string>(
  (a, b) => a.toLowerCase() === b.toLowerCase()
)

caseInsensitive("Hello", "hello")
caseInsensitive("Hello", "HELLO")

Equivalence.string
Equivalence.number
Equivalence.boolean
Equivalence.strict
```

### Transforming Equivalences

```typescript
// Map to compare by derived value
const byLength = Equivalence.string.pipe(
  Equivalence.mapInput((s: string) => s.length.toString())
)

// Actually, better approach:
const byLength = Equivalence.make<string>(
  (a, b) => a.length === b.length
)

// Combine equivalences
const userEquivalence = Equivalence.make<User>(
  (a, b) =>
    Equivalence.string(a.name, b.name) &&
    Equivalence.number(a.age, b.age)
)
```

### Using with Collections

```typescript
import { Array as Arr } from "effect"

const users = [
  { name: "Alice", age: 30 },
  { name: "Bob", age: 25 },
  { name: "alice", age: 30 } // Same as Alice?
]

// Dedupe with custom equivalence
const byNameIgnoreCase = Equivalence.make<User>(
  (a, b) => a.name.toLowerCase() === b.name.toLowerCase()
)

const unique = Arr.dedupe(users) // Uses default equality
const uniqueByName = Arr.dedupeWith(users, byNameIgnoreCase)
```

## Order - Comparison and Sorting

### The Order Interface

```typescript
import { Order } from "effect"

Order.string("a", "b")
Order.string("b", "a")
Order.string("a", "a")

Order.lessThan(Order.number)(5, 10)
Order.greaterThan(Order.number)(5, 10)
Order.lessThanOrEqualTo(Order.number)(5, 5)
Order.between(Order.number)({ minimum: 0, maximum: 10 })(5)

Order.min(Order.number)(3, 7)
Order.max(Order.number)(3, 7)

Order.clamp(Order.number)({ minimum: 0, maximum: 100 })(150)
```

### Built-in Orders

```typescript
Order.string
Order.number
Order.boolean
Order.bigint
Order.Date
```

### Creating Custom Orders

```typescript
const byAge = Order.make<Person>((a, b) =>
  a.age < b.age ? -1 : a.age > b.age ? 1 : 0
)

const byName = Order.mapInput(Order.string, (p: Person) => p.name)
const byAge = Order.mapInput(Order.number, (p: Person) => p.age)
```

### Combining Orders

```typescript
const byAgeThenName = Order.combine(
  byAge,
  byName
)

const byAgeDesc = Order.reverse(byAge)

const sortUsers = Order.combine(
  Order.mapInput(Order.string, (u: User) => u.department),
  Order.combine(
    Order.reverse(Order.mapInput(Order.number, (u: User) => u.salary)),
    Order.mapInput(Order.string, (u: User) => u.name)
  )
)
```

### Sorting with Order

```typescript
import { Array as Arr } from "effect"

const people = [
  { name: "Charlie", age: 35 },
  { name: "Alice", age: 30 },
  { name: "Bob", age: 30 }
]

const byAge = Arr.sort(people, Order.mapInput(Order.number, (p) => p.age))

const sorted = Arr.sort(people, Order.combine(
  Order.mapInput(Order.number, (p) => p.age),
  Order.mapInput(Order.string, (p) => p.name)
))
```

## Data.Class - Automatic Implementation

Using `Data.Class` automatically implements Equal and Hash:

```typescript
import { Data, Equal, Hash } from "effect"

class User extends Data.Class<{
  id: string
  name: string
  email: string
}> {}

const u1 = new User({ id: "1", name: "Alice", email: "a@example.com" })
const u2 = new User({ id: "1", name: "Alice", email: "a@example.com" })

Equal.equals(u1, u2) // true
Hash.hash(u1) === Hash.hash(u2) // true
```

## Best Practices

1. **Use Data.Class for value objects** - Automatic Equal/Hash
2. **Implement both Equal and Hash together** - Required for collections
3. **Use Order.mapInput for simple ordering** - Cleaner than manual comparison
4. **Combine orders for complex sorting** - More composable than custom compare
5. **Consider Equivalence for custom equality** - When default equality isn't enough

## Additional Resources

For comprehensive trait documentation, consult `${CLAUDE_PLUGIN_ROOT}/references/llms-full.txt`.

Search for these sections:
- "Equal" for equality comparison
- "Hash" for hash code generation
- "Equivalence" for custom equality relations
- "Order" for ordering and comparison
