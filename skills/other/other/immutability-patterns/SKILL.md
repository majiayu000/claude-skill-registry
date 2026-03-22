---
name: immutability-patterns
description: >
  Enforce immutable data patterns across JavaScript, TypeScript, Python, and Go.
  Use when the user writes code that mutates objects, arrays, or state. Apply whenever
  modifying data structures, updating state, or reviewing code for mutation bugs.
  Always prefer immutable patterns over in-place mutation.
---

# Immutability Patterns

Create new objects instead of mutating existing ones. Immutability prevents shared-state bugs, makes code easier to reason about, and enables reliable change detection.

## When to Use

- Writing any function that transforms data
- Updating React/Vue/Svelte state
- Working with Redux or other state management
- Reviewing code that modifies objects or arrays in place
- Any time `.push()`, `.splice()`, `delete`, or direct property assignment appears on shared data

## Core Patterns

### JavaScript/TypeScript: Object Updates

```typescript
// WRONG: Mutation
function updateUser(user: User, name: string): User {
  user.name = name;  // Mutates the original!
  return user;
}

// CORRECT: Spread operator
function updateUser(user: User, name: string): User {
  return { ...user, name };
}

// CORRECT: Nested object update
function updateAddress(user: User, city: string): User {
  return {
    ...user,
    address: {
      ...user.address,
      city,
    },
  };
}

// CORRECT: Conditional field update
function toggleAdmin(user: User): User {
  return {
    ...user,
    role: user.role === "admin" ? "user" : "admin",
  };
}
```

### JavaScript/TypeScript: Array Operations

```typescript
// WRONG: Mutating arrays
function addItem(items: Item[], item: Item): Item[] {
  items.push(item);   // Mutates!
  return items;
}

// CORRECT: Immutable array operations
const added = [...items, newItem];                          // append
const prepended = [newItem, ...items];                      // prepend
const removed = items.filter((item) => item.id !== id);     // remove
const updated = items.map((item) =>                         // update
  item.id === id ? { ...item, name: "new" } : item
);
const inserted = [                                          // insert at index
  ...items.slice(0, index),
  newItem,
  ...items.slice(index),
];
```

### TypeScript: Readonly Types

```typescript
// Mark data as immutable at the type level
interface Config {
  readonly apiUrl: string;
  readonly timeout: number;
  readonly retries: number;
}

// Readonly arrays
function processItems(items: readonly Item[]): readonly Item[] {
  // items.push(x) -> TypeScript error!
  return items.filter((item) => item.active);
}

// Deep readonly utility
type DeepReadonly<T> = {
  readonly [K in keyof T]: T[K] extends object ? DeepReadonly<T[K]> : T[K];
};

// Readonly records
const routes: Readonly<Record<string, string>> = {
  home: "/",
  login: "/auth/login",
  dashboard: "/app/dashboard",
};
```

### Deep Cloning and Complex Updates

```typescript
// structuredClone for deep copies (no functions or symbols)
const copy = structuredClone(complexObject);

// Object.freeze for shallow immutability (runtime enforcement)
const config = Object.freeze({
  api: "https://api.example.com",
  timeout: 5000,
});
// config.timeout = 3000; -> throws in strict mode, silent in sloppy mode

// For complex nested updates, use a library like immer
import { produce } from "immer";

const nextState = produce(state, (draft) => {
  draft.users[0].address.city = "New York";  // Looks like mutation
  draft.items.push(newItem);                  // but produces a new object
});
```

### Python: Immutable Patterns

```python
from dataclasses import dataclass, replace
from typing import NamedTuple

# Use frozen dataclasses
@dataclass(frozen=True)
class User:
    name: str
    email: str
    role: str = "user"

# Create updated copy with replace()
user = User(name="Alice", email="alice@example.com")
updated = replace(user, role="admin")  # New object, original unchanged

# Use tuples instead of lists for fixed collections
ALLOWED_ROLES = ("admin", "user", "viewer")

# Use frozenset for immutable sets
VALID_STATUSES = frozenset({"active", "inactive", "pending"})

# NamedTuple for immutable records
class Point(NamedTuple):
    x: float
    y: float

# Dict updates without mutation
original = {"a": 1, "b": 2}
updated = {**original, "b": 3, "c": 4}  # New dict
```

### Go: Immutable Patterns

```go
// Return new structs instead of modifying pointers
type User struct {
    Name  string
    Email string
    Role  string
}

// WRONG: Mutation via pointer
func (u *User) SetRole(role string) {
    u.Role = role
}

// CORRECT: Return new value
func (u User) WithRole(role string) User {
    u.Role = role  // Modifying the copy (value receiver)
    return u
}

// Immutable slice operations
func appendItem(items []Item, item Item) []Item {
    result := make([]Item, len(items)+1)
    copy(result, items)
    result[len(items)] = item
    return result
}

func removeItem(items []Item, index int) []Item {
    result := make([]Item, 0, len(items)-1)
    result = append(result, items[:index]...)
    result = append(result, items[index+1:]...)
    return result
}
```

## Anti-Patterns

### What NOT to Do

- **Direct property assignment on shared objects**: `user.name = "new"` — always spread into a new object.
- **Array mutators on shared arrays**: `.push()`, `.pop()`, `.splice()`, `.sort()`, `.reverse()` — use immutable alternatives or call on a copy.
- **Assuming Object.freeze is deep**: It only freezes the top level. Nested objects are still mutable.
- **Over-cloning**: Do not `structuredClone` on every operation — use spread for shallow updates, deep clone only when needed.

```typescript
// BAD: Sorting mutates the original array
const sorted = items.sort((a, b) => a.name.localeCompare(b.name));

// GOOD: toSorted (ES2023) or spread + sort
const sorted = items.toSorted((a, b) => a.name.localeCompare(b.name));
const sorted = [...items].sort((a, b) => a.name.localeCompare(b.name));

// BAD: Reversing mutates
const reversed = items.reverse();

// GOOD: toReversed (ES2023) or spread + reverse
const reversed = items.toReversed();
const reversed = [...items].reverse();
```

## Quick Reference

```
JavaScript/TypeScript Immutable Operations:
  Object update:    { ...obj, key: value }
  Array append:     [...arr, item]
  Array remove:     arr.filter(x => x.id !== id)
  Array update:     arr.map(x => x.id === id ? { ...x, ...changes } : x)
  Array sort:       arr.toSorted(fn)  or  [...arr].sort(fn)
  Array reverse:    arr.toReversed()  or  [...arr].reverse()
  Deep clone:       structuredClone(obj)
  Nested update:    immer produce()

TypeScript Types:
  readonly prop     Readonly<T>     ReadonlyArray<T>     as const

Python:
  @dataclass(frozen=True)   replace(obj, field=val)
  tuple()   frozenset()     {**dict, key: val}

Go:
  Value receivers   Return new structs   copy() for slices

Mutating Methods to AVOID (on shared data):
  .push() .pop() .shift() .unshift() .splice()
  .sort() .reverse() .fill() delete obj.key
```
