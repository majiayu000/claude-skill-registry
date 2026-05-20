---
name: atom-state
description: Implement reactive state management with Effect Atom for React applications
---

# Effect Atom State Management

Effect Atom is a reactive state management library for Effect that seamlessly integrates with React.

## Core Concepts

### Atoms as References

Atoms work **by reference** - they are stable containers for reactive state:

```typescript
import * as Atom from "@effect-atom/atom-react"

// Atoms are created once and referenced throughout the app
export const counterAtom = Atom.make(0)

// Multiple components can reference the same atom
// All update when the atom value changes
```

### Automatic Cleanup

Atoms automatically reset when no subscribers remain (unless marked with `keepAlive`):

```typescript
// Resets when last subscriber unmounts
export const temporaryState = Atom.make(initialValue)

// Persists across component lifecycles
export const persistentState = Atom.make(initialValue).pipe(Atom.keepAlive)
```

### Lazy Evaluation

Atom values are computed on-demand when subscribers access them.

## Pattern: Basic Atoms

```typescript
import * as Atom from "@effect-atom/atom-react"

// Simple atom
export const count = Atom.make(0)

// Atom with object state
export interface CartState {
  readonly items: ReadonlyArray<Item>
  readonly total: number
}

export const cart = Atom.make<CartState>({
  items: [],
  total: 0
})
```

## Pattern: Derived Atoms

Use `Atom.map` or computed atoms with the `get` parameter:

```typescript
// Derived via map
export const itemCount = Atom.map(cart, (c) => c.items.length)
export const isEmpty = Atom.map(cart, (c) => c.items.length === 0)

// Computed atom accessing other atoms
export const cartSummary = Atom.make((get) => {
  const cartData = get(cart)
  const count = get(itemCount)

  return {
    itemCount: count,
    total: cartData.total,
    isEmpty: count === 0
  }
})
```

## Pattern: Atom Family (Dynamic Atoms)

Use `Atom.family` for stable references to dynamically created atoms:

```typescript
// Create atoms per entity ID
export const userAtoms = Atom.family((userId: string) =>
  Atom.make<User | null>(null).pipe(Atom.keepAlive)
)

// Usage - always returns the same atom for a given ID
const userAtom = userAtoms(userId)
```

## Pattern: Function Atoms (Side Effects)

Use `Atom.fn` for operations with side effects:

```typescript
import { Effect } from "effect"

// Function atom for side effects
export const addItem = Atom.fn(
  Effect.fnUntraced(function* (item: Item) {
    const current = yield* Atom.get(cart)

    yield* Atom.set(cart, {
      items: [...current.items, item],
      total: current.total + item.price
    })
  })
)

// Clear cart operation
export const clearCart = Atom.fn(
  Effect.fnUntraced(function* () {
    yield* Atom.set(cart, { items: [], total: 0 })
  })
)
```

## Pattern: Runtime with Services

Wrap Effect layers/services for use in atoms:

```typescript
import { Layer } from "effect"

// Create runtime with services
export const runtime = Atom.runtime(
  Layer.mergeAll(
    DatabaseService.Live,
    LoggerService.Live,
    ApiClient.Live
  )
)

// Use services in function atoms
export const fetchUserData = runtime.fn(
  Effect.fnUntraced(function* (userId: string) {
    const db = yield* DatabaseService
    const user = yield* db.getUser(userId)

    yield* Atom.set(userAtoms(userId), user)
    return user
  })
)
```

### Global Layers

Configure global layers once at app initialization:

```typescript
// App setup
Atom.runtime.addGlobalLayer(
  Layer.mergeAll(
    Logger.Live,
    Tracer.Live,
    Config.Live
  )
)
```

## Pattern: Result Types (Error Handling)

Atoms can return `Result` types for explicit error handling:

```typescript
import * as Result from "@effect-atom/atom/Result"

export const userData = Atom.make<Result.Result<User, Error>>(
  Result.initial
)

// In component
const result = useAtomValue(userData)

Result.match(result, {
  Initial: () => <Loading />,
  Failure: (error) => <Error message={error.message} />,
  Success: (user) => <UserProfile user={user} />
})
```

## Pattern: Stream Integration

Convert streams into atoms that capture the latest value:

```typescript
import { Stream } from "effect"

// Infinite stream becomes reactive atom
export const notifications = Atom.make(
  Stream.fromEventListener(window, "notification").pipe(
    Stream.map(parseNotification),
    Stream.filter(isValid),
    Stream.scan([], (acc, n) => [...acc, n].slice(-10))
  )
)
```

## Pattern: Pull Atoms (Pagination)

Use `Atom.pull` for stream-based pagination:

```typescript
export const pagedItems = Atom.pull(
  Stream.fromIterable(itemsSource).pipe(
    Stream.grouped(10) // Pages of 10 items
  )
)

// In component - automatically fetches next page when called
const loadMore = useAtomSet(pagedItems)
```

## Pattern: Persistence

Use `Atom.kvs` for persisted state:

```typescript
import { BrowserKeyValueStore } from "@effect/platform-browser"
import * as Schema from "effect/Schema"

export const userSettings = Atom.kvs({
  runtime: Atom.runtime(BrowserKeyValueStore.layerLocalStorage),
  key: "user-settings",
  schema: Schema.Struct({
    theme: Schema.Literal("light", "dark"),
    notifications: Schema.Boolean,
    language: Schema.String
  }),
  defaultValue: () => ({
    theme: "light",
    notifications: true,
    language: "en"
  })
})
```

## React Integration

### Hooks

```typescript
import { useAtomValue, useAtomSet, useAtom, useAtomSetPromise } from "@effect-atom/atom-react"

export function CartView() {
  // Read only
  const cartData = useAtomValue(cart)
  const isEmpty = useAtomValue(isEmpty)

  // Write only
  const addItem = useAtomSet(addItem)
  const clearCart = useAtomSet(clearCart)

  // Both read and write
  const [count, setCount] = useAtom(counterAtom)

  // For async function atoms
  const fetchData = useAtomSetPromise(fetchUserData)

  return (
    <div>
      <div>Items: {cartData.items.length}</div>
      <button onClick={() => addItem(newItem)}>Add</button>
      <button onClick={() => clearCart()}>Clear</button>
    </div>
  )
}
```

### Separation of Concerns

Different components can read/write the same atom reactively:

```typescript
// Component A - reads state
function CartDisplay() {
  const cart = useAtomValue(cart)
  return <div>Items: {cart.items.length}</div>
}

// Component B - modifies state
function CartActions() {
  const addItem = useAtomSet(addItem)
  return <button onClick={() => addItem(item)}>Add</button>
}

// Both update reactively when atom changes
```

## Scoped Resources & Finalizers

Atoms support scoped effects with automatic cleanup:

```typescript
export const wsConnection = Atom.make(
  Effect.gen(function* () {
    // Acquire resource
    const ws = yield* Effect.acquireRelease(
      connectWebSocket(),
      (ws) => Effect.sync(() => ws.close())
    )

    return ws
  })
)

// Finalizer runs when atom rebuilds or becomes unused
```

## Key Principles

1. **Reference Stability**: Use `Atom.family` for dynamically generated atom sets
2. **Lazy Evaluation**: Values computed on-demand when accessed
3. **Automatic Cleanup**: Atoms reset when unused (unless `keepAlive`)
4. **Derive, Don't Coordinate**: Use computed atoms to derive state
5. **Result Types**: Handle errors explicitly with Result.match
6. **Services in Runtime**: Wrap layers once, use in multiple atoms
7. **Immutable Updates**: Always create new values, never mutate
8. **Scoped Effects**: Leverage finalizers for resource cleanup

## Common Patterns

### Loading States

```typescript
export const userDataAtom = Atom.make<Result.Result<User, Error>>(
  Result.initial
)

export const loadUser = runtime.fn(
  Effect.fnUntraced(function* (id: string) {
    yield* Atom.set(userDataAtom, Result.initial)

    const result = yield* Effect.either(
      userService.fetchUser(id)
    )

    yield* Atom.set(
      userDataAtom,
      result._tag === "Right"
        ? Result.success(result.right)
        : Result.failure(result.left)
    )
  })
)
```

### Optimistic Updates

```typescript
export const updateItem = runtime.fn(
  Effect.fnUntraced(function* (id: string, updates: Partial<Item>) {
    const current = yield* Atom.get(itemsAtom)

    // Optimistic update
    yield* Atom.set(
      itemsAtom,
      current.map(item => item.id === id ? { ...item, ...updates } : item)
    )

    // Persist to server
    const result = yield* Effect.either(api.updateItem(id, updates))

    // Revert on failure
    if (result._tag === "Left") {
      yield* Atom.set(itemsAtom, current)
    }
  })
)
```

### Computed Queries

```typescript
// Filter atom accessing other atoms
export const filteredItems = Atom.make((get) => {
  const items = get(itemsAtom)
  const searchTerm = get(searchAtom)
  const activeFilters = get(filtersAtom)

  return items.filter(item =>
    item.name.includes(searchTerm) &&
    activeFilters.every(f => f.predicate(item))
  )
})
```

Effect Atom bridges Effect's powerful type system with React's rendering model, providing type-safe reactive state management with automatic cleanup and seamless Effect integration.
