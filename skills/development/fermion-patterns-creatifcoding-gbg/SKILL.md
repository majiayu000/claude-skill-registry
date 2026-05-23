---
name: fermion-patterns
description: Schema-driven Atom.family patterns for TMNL. Covers Fermion builder API, registry patterns, algebra interpreters, and React integration. (project)
model_invoked: true
triggers:
  - "Fermion"
  - "fromSchema"
  - "Atom.family"
  - "FermionAlgebra"
  - "withKey"
  - "withCompositeKey"
  - "registry.set"
  - "registry.get"
  - "RegistryProvider"
  - "IoT"
  - "sensor"
  - "entity cache"
  - "memoized atom"
---

# Fermion Patterns

Schema-driven Atom.family library for TMNL. Fermion provides type-safe, memoized
atom families with Effect-based CRUD operations.

The name "Fermion" comes from fundamental particles that obey the Pauli exclusion
principle - no two fermions can share the same quantum state. This maps to
Atom.family memoization where each key gets exactly one atom.

---

## Decision Tree

```
Need per-entity reactive state?
├── Single entity type with ID?
│   └── Fermion.fromSchema(Schema).withKey("id")
├── Composite key (userId + orderId)?
│   └── Fermion.fromSchema(Schema).withCompositeKey(["userId", "orderId"])
├── Need async fetch on access?
│   └── .withFetch((key) => Effect.tryPromise(...))
├── Need persistence?
│   └── .withPersist((value) => Effect.tryPromise(...))
└── Testing / local state only?
    └── .provideLayer(makeMemoryAlgebra())
```

---

## CRITICAL: Registry Pattern

**This is the most common source of bugs with effect-atom and Fermion.**

### The Problem

`Atom.set()` and `Atom.get()` return **Effects** that require `AtomRegistry` context:

```typescript
// Atom.set() returns Effect<void, never, AtomRegistry>
// Atom.get() returns Effect<A, never, AtomRegistry>

// WRONG - This does NOTHING! The Effect is never executed
Atom.set(myAtom, newValue)  // ❌ Returns Effect, doesn't mutate

// WRONG - This returns an Effect, not the value
const value = Atom.get(myAtom)  // ❌ Returns Effect<A>, not A
```

### The Solution: Registry Singleton

Create a registry singleton and use `registry.set()` / `registry.get()` for
synchronous mutations:

```typescript
import { Registry, RegistryContext } from "@effect-atom/atom-react"

// 1. Create singleton registry at module level
export const myRegistry = Registry.make()

// 2. Create Provider wrapper
export function MyRegistryProvider({ children }: { children: React.ReactNode }) {
  return (
    <RegistryContext.Provider value={myRegistry}>
      {children}
    </RegistryContext.Provider>
  )
}

// 3. Use registry.set() / registry.get() for sync mutations
function handleUpdate(newValue: string) {
  // ✓ Synchronous - mutates immediately
  myRegistry.set(myAtom, newValue)

  // ✓ Synchronous - returns value immediately
  const current = myRegistry.get(myAtom)
}
```

### When to Use Which

| Context | Pattern | Why |
|---------|---------|-----|
| Inside `Effect.gen()` | `Atom.set()` / `Atom.get()` | Effect context provides AtomRegistry |
| Inside `runtimeAtom.fn()` | `ctx.set()` / `ctx.get()` | Context parameter provides access |
| React callback / event handler | `registry.set()` / `registry.get()` | Synchronous, no Effect needed |
| Outside any context | `registry.set()` / `registry.get()` | Only option for sync access |

### Complete Example: IoT Sensor Pattern

```typescript
// atoms/index.ts
import { Atom, Registry, RegistryContext } from "@effect-atom/atom-react"
import * as Fermion from "@/lib/fermion"
import { Schema, Effect } from "effect"

// ─── Registry Singleton ───────────────────────────────────────
export const iotRegistry = Registry.make()

export function IoTRegistryProvider({ children }: { children: React.ReactNode }) {
  return React.createElement(
    RegistryContext.Provider,
    { value: iotRegistry },
    children
  )
}

// ─── Sensor Schema ────────────────────────────────────────────
const SensorSchema = Schema.Struct({
  id: Schema.String.pipe(Schema.brand("SensorId")),
  name: Schema.NonEmptyString,
  value: Schema.Number,
  unit: Schema.String,
  lastUpdate: Schema.DateFromSelf,
})
type Sensor = typeof SensorSchema.Type

// ─── Fermion Family ───────────────────────────────────────────
export const sensorFamily = Fermion.fromSchema(SensorSchema)
  .withKey("id")
  .withFetch((id) =>
    Effect.tryPromise(() =>
      fetch(`/api/sensors/${id}`).then(r => r.json())
    )
  )
  .build()

// ─── Log Atom (for debugging) ─────────────────────────────────
export const iotLogAtom = Atom.make<readonly string[]>([])

// ─── Sync Mutation Helper ─────────────────────────────────────
export function logMessage(msg: string) {
  const timestamp = new Date().toISOString().slice(11, 19)
  const current = iotRegistry.get(iotLogAtom)
  // Keep last 15 messages
  iotRegistry.set(iotLogAtom, [...current.slice(-14), `${timestamp}: ${msg}`])
}
```

```tsx
// Component.tsx
import { useAtomValue } from "@effect-atom/atom-react"
import { sensorFamily, iotLogAtom, logMessage, IoTRegistryProvider } from "./atoms"
import * as Result from "@effect-atom/atom/Result"

function SensorDisplay({ sensorId }: { sensorId: string }) {
  const sensorResult = useAtomValue(sensorFamily(sensorId))

  useEffect(() => {
    // Trigger fetch
    sensorFamily.fetch(sensorId).pipe(Effect.runPromise)
    logMessage(`Fetching sensor ${sensorId}`)
  }, [sensorId])

  return Result.match(sensorResult, {
    onInitial: () => <Loading />,
    onSuccess: (sensor) => (
      <div>
        <span>{sensor.name}</span>
        <span>{sensor.value} {sensor.unit}</span>
      </div>
    ),
    onFailure: (error) => <Error error={error} />,
  })
}

function SensorLog() {
  const logs = useAtomValue(iotLogAtom)
  return (
    <pre className="text-xs">
      {logs.join("\n")}
    </pre>
  )
}

// App must wrap with provider
function App() {
  return (
    <IoTRegistryProvider>
      <SensorDisplay sensorId="temp-001" />
      <SensorLog />
    </IoTRegistryProvider>
  )
}
```

---

## Builder API Reference

### Entry Point: `fromSchema()`

```typescript
import * as Fermion from "@/lib/fermion"
import { Schema } from "effect"

const UserSchema = Schema.Struct({
  id: Schema.String.pipe(Schema.brand("UserId")),
  name: Schema.NonEmptyString,
  email: Schema.String,
})

const userFamily = Fermion.fromSchema(UserSchema)
  .withKey("id")
  .withFetch(...)
  .build()
```

### Key Configuration

#### Single Key: `.withKey(field)`

```typescript
// Key type inferred from schema field
const family = Fermion.fromSchema(UserSchema)
  .withKey("id")  // Key type: string & Brand<"UserId">
```

#### Composite Key: `.withCompositeKey([...fields])`

```typescript
const OrderSchema = Schema.Struct({
  userId: Schema.String.pipe(Schema.brand("UserId")),
  orderId: Schema.String.pipe(Schema.brand("OrderId")),
  items: Schema.Array(OrderItemSchema),
})

const orderFamily = Fermion.fromSchema(OrderSchema)
  .withCompositeKey(["userId", "orderId"])
  // Key type: { readonly userId: string; readonly orderId: string }

// Usage
const orderAtom = orderFamily({ userId: "u-1", orderId: "o-42" })
```

### Operations

#### `.withFetch()` - Required

```typescript
.withFetch((id) =>
  Effect.tryPromise(() =>
    fetch(`/api/users/${id}`).then(r => r.json())
  )
)

// With service dependency
.withFetch((id) =>
  Effect.gen(function* () {
    const api = yield* UserApi
    return yield* api.fetchUser(id)
  })
)
```

#### `.withPersist()` - Optional

```typescript
.withPersist((user) =>
  Effect.tryPromise(() =>
    fetch(`/api/users/${user.id}`, {
      method: "PUT",
      body: JSON.stringify(user)
    })
  )
)
```

#### `.withRemove()` - Optional

```typescript
.withRemove((id) =>
  Effect.tryPromise(() =>
    fetch(`/api/users/${id}`, { method: "DELETE" })
  )
)
```

### Lifecycle Hooks

#### `.withBeforeFetch()`

```typescript
.withBeforeFetch((id) =>
  Effect.log(`Fetching user ${id}`)
)
```

#### `.withAfterFetch()`

```typescript
.withAfterFetch((id, user) =>
  Effect.gen(function* () {
    yield* Effect.log(`Fetched user ${user.name}`)
    // Can transform the value
    return { ...user, fetchedAt: new Date() }
  })
)
```

### Dependency Injection

#### `.provideLayer()`

```typescript
.provideLayer(HttpClient.layer)
.provideLayer(UserCacheLive)
```

#### `.provideService()`

```typescript
.provideService(UserCache, {
  get: (id) => Effect.succeed(undefined),
  set: (id, user) => Effect.void,
})
```

### Configuration

#### `.withLifecycle()`

```typescript
// Entity cache - persist indefinitely (default)
.withLifecycle({ keepAlive: true })

// Transient data - reset when no subscribers
.withLifecycle({ keepAlive: false })

// Time-limited cache
.withLifecycle({ keepAlive: true, ttl: Duration.minutes(5) })
```

#### `.withTTL()` - Shorthand

```typescript
// Equivalent to .withLifecycle({ keepAlive: true, ttl })
.withTTL(Duration.minutes(5))
```

#### `.withReactivity()` - Fine-grained subscriptions

```typescript
.withReactivity((key, user) => [user.email, user.role])
```

### Terminal Operations

#### `.build()` - All dependencies satisfied

```typescript
// Type-safe: fails to compile if R is not `never`
const family = Fermion.fromSchema(UserSchema)
  .withKey("id")
  .withFetch(...)
  .provideLayer(HttpClient.layer)  // Satisfies HttpClient requirement
  .build()  // ✓ Compiles
```

#### `.buildWithDeps()` - Runtime dependency injection

```typescript
// Use when layers will be provided at runtime via Atom.runtime
const family = Fermion.fromSchema(UserSchema)
  .withKey("id")
  .withFetch((id) => Effect.flatMap(UserApi, api => api.fetch(id)))
  .buildWithDeps()  // R = UserApi

// Provide at runtime
const runtimeAtom = Atom.runtime(UserApiLive)
```

---

## Fermion Interface

Once built, a Fermion family provides:

```typescript
interface Fermion<A, I, E, R, K> {
  // Callable - get atom for key (memoized)
  (key: K): Atom<Result<A, E>>

  // Same as callable
  atomFor(key: K): Atom<Result<A, E>>

  // Effectful operations (require AtomRegistry)
  fetch(key: K): Effect<A, E, R | AtomRegistry>
  persist(value: A): Effect<void, E, R | AtomRegistry>
  remove(key: K): Effect<void, E, R | AtomRegistry>

  // Utilities
  invalidate(key: K): Effect<void, never, AtomRegistry>
  prefetch(keys: readonly K[]): Effect<void, E, R | AtomRegistry>

  // Metadata
  schema: Schema<A, I, R>
  keyField: string | readonly string[]
}
```

### Usage

```typescript
// Get atom (memoized - same key always returns same atom)
const userAtom = userFamily("user-123")
const sameAtom = userFamily("user-123")  // Same reference

// React subscription
const userResult = useAtomValue(userFamily(userId))

// Trigger fetch
await userFamily.fetch(userId).pipe(Effect.runPromise)

// Persist changes
await userFamily.persist(updatedUser).pipe(Effect.runPromise)

// Remove entity
await userFamily.remove(userId).pipe(Effect.runPromise)

// Invalidate (force refetch on next access)
await userFamily.invalidate(userId).pipe(Effect.runPromise)

// Prefetch multiple
await userFamily.prefetch(["u-1", "u-2", "u-3"]).pipe(Effect.runPromise)
```

---

## Algebra Patterns

### What is FermionAlgebra?

The algebra defines the data operations (fetch, persist, remove) that power a
Fermion family. Different interpreters implement the same interface for
different backends.

```typescript
interface FermionAlgebra<A, E, R, K> {
  readonly fetch: (key: K) => Effect<A, E, R>
  readonly persist?: (value: A) => Effect<void, E, R>
  readonly remove?: (key: K) => Effect<void, E, R>
  readonly beforeFetch?: (key: K) => Effect<void, E, R>
  readonly afterFetch?: (key: K, value: A) => Effect<A, E, R>
}
```

### Built-in Interpreters

#### `fromFunctions()` - Effect-based CRUD

```typescript
import { fromFunctions } from "@/lib/fermion"

const userAlgebra = fromFunctions({
  fetch: (id: string) =>
    Effect.tryPromise(() => api.getUser(id)),
  persist: (user: User) =>
    Effect.tryPromise(() => api.updateUser(user)),
  remove: (id: string) =>
    Effect.tryPromise(() => api.deleteUser(id)),
})
```

#### `fromFetch()` - HTTP endpoints

```typescript
import { fromFetch } from "@/lib/fermion"

const userAlgebra = fromFetch({
  baseUrl: "/api/users",
  // GET /api/users/{id}
  // PUT /api/users/{id}
  // DELETE /api/users/{id}
})
```

#### `makeMemoryAlgebra()` - Testing / local state

```typescript
import { makeMemoryAlgebra } from "@/lib/fermion"

// Creates in-memory storage with full CRUD
const testAlgebra = makeMemoryAlgebra<User, string>()

// Usage in tests
const family = Fermion.fromSchema(UserSchema)
  .withKey("id")
  .withFetch(testAlgebra.fetch)
  .withPersist(testAlgebra.persist)
  .withRemove(testAlgebra.remove)
  .build()
```

### Composing Algebras

#### `composeAlgebra()` - Merge operations

```typescript
import { composeAlgebra } from "@/lib/fermion"

const cacheAlgebra = fromFunctions({ fetch: cacheGet })
const apiAlgebra = fromFunctions({ fetch: apiFetch })

// Cache-then-API pattern
const composedAlgebra = composeAlgebra(cacheAlgebra, apiAlgebra)
```

#### `withHooks()` - Add lifecycle hooks

```typescript
import { withHooks } from "@/lib/fermion"

const hookedAlgebra = withHooks(baseAlgebra, {
  beforeFetch: (key) => Effect.log(`Fetching ${key}`),
  afterFetch: (key, value) => {
    analytics.track("entity_fetched", { key })
    return Effect.succeed(value)
  },
})
```

---

## React Integration

### Basic Pattern

```tsx
import { useAtomValue } from "@effect-atom/atom-react"
import * as Result from "@effect-atom/atom/Result"
import { userFamily } from "./atoms"

function UserProfile({ userId }: { userId: string }) {
  const userResult = useAtomValue(userFamily(userId))

  // Trigger fetch on mount
  useEffect(() => {
    userFamily.fetch(userId).pipe(Effect.runPromise)
  }, [userId])

  return Result.match(userResult, {
    onInitial: () => <Skeleton />,
    onSuccess: (user) => <ProfileCard user={user} />,
    onFailure: (error) => <ErrorBanner error={error} />,
  })
}
```

### With Loading States

```tsx
function UserProfile({ userId }: { userId: string }) {
  const userResult = useAtomValue(userFamily(userId))
  const [isRefreshing, setIsRefreshing] = useState(false)

  const handleRefresh = async () => {
    setIsRefreshing(true)
    await userFamily.fetch(userId).pipe(Effect.runPromise)
    setIsRefreshing(false)
  }

  return (
    <div>
      {Result.isSuccess(userResult) && (
        <ProfileCard user={userResult.value} />
      )}
      <button onClick={handleRefresh} disabled={isRefreshing}>
        {isRefreshing ? "Refreshing..." : "Refresh"}
      </button>
    </div>
  )
}
```

### Optimistic Updates

```tsx
function EditableUser({ userId }: { userId: string }) {
  const userResult = useAtomValue(userFamily(userId))

  const handleUpdate = async (newName: string) => {
    if (!Result.isSuccess(userResult)) return

    const user = userResult.value
    const updated = { ...user, name: newName }

    // Optimistic update via registry
    myRegistry.set(userFamily(userId), Result.success(updated))

    try {
      await userFamily.persist(updated).pipe(Effect.runPromise)
    } catch {
      // Rollback on failure
      myRegistry.set(userFamily(userId), Result.success(user))
    }
  }

  // ...
}
```

---

## Testing Patterns

### Isolated Registry

```typescript
import { Registry } from "@effect-atom/atom-react"
import { makeMemoryAlgebra } from "@/lib/fermion"

describe("UserFamily", () => {
  let testRegistry: Registry
  let testFamily: Fermion<User, ...>

  beforeEach(() => {
    testRegistry = Registry.make()

    const memoryAlgebra = makeMemoryAlgebra<User, string>()
    testFamily = Fermion.fromSchema(UserSchema)
      .withKey("id")
      .withFetch(memoryAlgebra.fetch)
      .withPersist(memoryAlgebra.persist)
      .build()
  })

  it("fetches user by id", async () => {
    // Seed data
    await testFamily.persist({
      id: "u-1",
      name: "Alice",
      email: "alice@test.com",
    }).pipe(Effect.runPromise)

    // Fetch
    const user = await testFamily.fetch("u-1").pipe(Effect.runPromise)

    expect(user.name).toBe("Alice")
  })

  it("updates atom on fetch", async () => {
    await testFamily.fetch("u-1").pipe(Effect.runPromise)

    const atomValue = testRegistry.get(testFamily("u-1"))
    expect(Result.isSuccess(atomValue)).toBe(true)
  })
})
```

### Snapshot Testing

```typescript
it("matches family state snapshot", () => {
  // ... setup and operations

  const state = testRegistry.get(testFamily("u-1"))
  expect(state).toMatchSnapshot()
})
```

---

## Anti-Patterns

### ANTIPATTERN:ATOM_SET_WITHOUT_REGISTRY

```typescript
// ❌ WRONG - Returns Effect, never executed
function handleClick() {
  Atom.set(myAtom, newValue)  // Does nothing!
}

// ✓ CORRECT - Use registry for sync mutations
function handleClick() {
  myRegistry.set(myAtom, newValue)  // Mutates immediately
}
```

### ANTIPATTERN:FAMILY_IN_COMPONENT

```typescript
// ❌ WRONG - Creates new family on every render
function Bad({ schema }) {
  const family = Fermion.fromSchema(schema).withKey("id").build()
  return <Child family={family} />
}

// ✓ CORRECT - Define at module level
const userFamily = Fermion.fromSchema(UserSchema).withKey("id").build()

function Good() {
  return <Child family={userFamily} />
}
```

### ANTIPATTERN:MISSING_PROVIDER

```typescript
// ❌ WRONG - No registry context, useAtomValue may not work
function App() {
  return <UserProfile userId="123" />
}

// ✓ CORRECT - Wrap with registry provider
function App() {
  return (
    <MyRegistryProvider>
      <UserProfile userId="123" />
    </MyRegistryProvider>
  )
}
```

### ANTIPATTERN:FORGETTING_EFFECT_EXECUTION

```typescript
// ❌ WRONG - Effect returned but never run
function handleFetch() {
  userFamily.fetch(userId)  // Returns Effect, doesn't execute!
}

// ✓ CORRECT - Run the Effect
function handleFetch() {
  userFamily.fetch(userId).pipe(Effect.runPromise)
}

// ✓ ALSO CORRECT - In Effect context
const program = Effect.gen(function* () {
  const user = yield* userFamily.fetch(userId)
})
```

---

## Canonical Files

| File | Purpose |
|------|---------|
| `src/lib/fermion/index.ts` | Public API exports |
| `src/lib/fermion/Fermion.ts` | Builder implementation |
| `src/lib/fermion/types.ts` | Type definitions |
| `src/lib/fermion/algebra/` | Algebra interface and composition |
| `src/lib/fermion/interpreters/` | Built-in interpreters (effect, memory) |
| `src/components/testbed/FermionTestbed.tsx` | Usage examples with registry pattern |

---

## Advanced Atom.family Patterns

### Keying Strategies

#### String Keys (Simple)
```typescript
const userFamily = Atom.family((id: string) => Atom.make<User | null>(null))
```

#### Composite Keys (Tuple)
```typescript
// For multi-part keys, use object or tuple
const orderFamily = Atom.family(
  ({ userId, orderId }: { userId: string; orderId: string }) =>
    Atom.make<Order | null>(null)
)

// Usage
const orderAtom = orderFamily({ userId: "u-1", orderId: "o-42" })
```

#### Hash-based Keys (Complex Objects)
```typescript
import { Hash } from "effect"

// When key is complex object, provide hash function
const queryFamily = Atom.family(
  (query: SearchQuery) => Atom.make<SearchResult | null>(null),
  {
    // Custom equality for memoization
    isEqual: (a, b) => Hash.hash(a) === Hash.hash(b)
  }
)
```

### Garbage Collection

Atom.family uses `WeakRef` + `FinalizationRegistry` when available:

```typescript
// Atoms are garbage collected when:
// 1. No subscribers (React components)
// 2. Not keepAlive
// 3. No strong references

// Force keepAlive for cache scenarios
const cachedFamily = Atom.family((id: string) =>
  Atom.make<Data | null>(null).pipe(Atom.keepAlive)
)

// Explicit cleanup
registry.dispose(userFamily("u-123"))
```

### Cache Invalidation

```typescript
// Invalidate single entry
registry.refresh(userFamily("u-123"))

// Invalidate with Reactivity
const userAtom = Atom.make(() => fetchUser()).pipe(
  Atom.withReactivity(["users", "user:123"])
)

// Invalidate by key
runtimeAtom.fn(Effect.gen(function* () {
  yield* updateUser(data)
  yield* Reactivity.invalidate("user:123")
}))
```

---

## Atom.runtime Patterns

### Basic Runtime Setup

```typescript
import { Atom } from "@effect-atom/atom"
import { Layer } from "effect"

// Create runtime with service layer
const appRuntime = Atom.runtime(
  Layer.mergeAll(
    DatabaseService.Default,
    CacheService.Default,
    LoggingService.Default
  )
)

// Effectful atom using services
const usersAtom = appRuntime.atom(
  Effect.gen(function* () {
    const db = yield* DatabaseService
    return yield* db.query("SELECT * FROM users")
  })
)
```

### Global Layers

```typescript
// Add cross-cutting concerns globally
Atom.runtime.addGlobalLayer(
  Layer.setTracerEnabled(true)
)

Atom.runtime.addGlobalLayer(
  Layer.setConfigProvider(ConfigProvider.fromEnv())
)
```

### Runtime Functions (runtimeAtom.fn)

```typescript
// Create effectful operations callable from React
const ops = {
  fetchUser: appRuntime.fn<string>()(
    (userId) => Effect.gen(function* () {
      const api = yield* UserApi
      return yield* api.fetch(userId)
    })
  ),

  updateUser: appRuntime.fn<User>()(
    (user, ctx) => Effect.gen(function* () {
      yield* UserApi.update(user)
      // ctx.set for sync atom updates within Effect
      ctx.set(userAtom, Result.success(user))
    })
  )
}

// Usage in React
const handleSave = () => {
  registry.set(ops.updateUser, updatedUser)
}
```

### Stream-backed Atoms (Atom.pull)

```typescript
// Paginated/infinite data
const messagesAtom = Atom.pull(
  Stream.paginateChunkEffect(0, (page) =>
    Effect.gen(function* () {
      const api = yield* MessagesApi
      const chunk = yield* api.getPage(page)
      const next = chunk.hasMore ? Option.some(page + 1) : Option.none()
      return [chunk.messages, next]
    })
  )
)

// Usage: pull next chunk
registry.set(messagesAtom, void 0) // Triggers next chunk
```

### SubscriptionRef Integration

```typescript
// Backed by SubscriptionRef for external updates
const priceAtom = appRuntime.subscriptionRef(
  Effect.gen(function* () {
    const ws = yield* WebSocketService
    return yield* ws.subscribe("prices")
  })
)
```

---

## Result Handling Patterns

### The Result Type

```typescript
import * as Result from "@effect-atom/atom/Result"

type Result<A, E = never> =
  | { _tag: "Initial" }                    // Never fetched
  | { _tag: "Waiting"; previous?: A }      // Fetching (with optional stale data)
  | { _tag: "Success"; value: A }          // Success
  | { _tag: "Failure"; cause: Cause<E> }   // Failed
```

### Pattern Matching

```typescript
// Full match
Result.match(result, {
  onInitial: () => <Skeleton />,
  onWaiting: (previous) => previous
    ? <StaleData data={previous} isRefreshing />
    : <Loading />,
  onSuccess: (data) => <Content data={data} />,
  onFailure: (cause) => <Error cause={cause} />
})

// Guards
if (Result.isSuccess(result)) {
  console.log(result.value)
}
if (Result.isFailure(result)) {
  console.log(Cause.pretty(result.cause))
}
```

### Derived Results

```typescript
// Map over success
const nameResult = Result.map(userResult, user => user.name)

// FlatMap for dependent fetches
const profileResult = Result.flatMap(userResult, user =>
  registry.get(profileFamily(user.profileId))
)
```

### Stale-While-Revalidate

```typescript
function useStaleWhileRevalidate<A>(atom: Atom<Result<A>>) {
  const result = useAtomValue(atom)

  // Show previous data while revalidating
  const data = Result.match(result, {
    onInitial: () => null,
    onWaiting: (prev) => prev ?? null,
    onSuccess: (v) => v,
    onFailure: () => null
  })

  const isLoading = Result.isWaiting(result)
  const error = Result.isFailure(result) ? result.cause : null

  return { data, isLoading, error }
}
```

---

## Domain Pattern Generalizations

### Pattern: IoT Sensor Data

```typescript
// Keyed by sensor ID, with polling refresh
const SensorSchema = Schema.Struct({
  id: Schema.String.pipe(Schema.brand("SensorId")),
  value: Schema.Number,
  unit: Schema.String,
  timestamp: Schema.DateFromSelf
})

const sensorFamily = Fermion.fromSchema(SensorSchema)
  .withKey("id")
  .withFetch((id) => SensorApi.read(id))
  .withTTL(Duration.seconds(5))  // Auto-refresh every 5s
  .build()

// Aggregate atom for dashboard
const sensorSummaryAtom = Atom.make((get) => {
  const sensors = ["temp-1", "humidity-1", "pressure-1"]
  const results = sensors.map(id => get.result(sensorFamily(id)))

  if (results.some(Result.isFailure)) {
    return { status: "error" }
  }
  if (results.some(r => !Result.isSuccess(r))) {
    return { status: "loading" }
  }

  const values = results.map(r => (r as Result.Success<Sensor>).value)
  return {
    status: "ready",
    avgTemp: values.find(s => s.id.startsWith("temp"))?.value,
    humidity: values.find(s => s.id.startsWith("humidity"))?.value
  }
})
```

### Pattern: Financial Tick Data

```typescript
// High-frequency updates with batching
const tickAtom = Atom.make<Tick | null>(null).pipe(Atom.keepAlive)
const tickHistoryAtom = Atom.make<Tick[]>([]).pipe(Atom.keepAlive)

// Batch rapid updates
const processTick = (tick: Tick) => {
  Atom.batch(() => {
    registry.set(tickAtom, tick)
    const history = registry.get(tickHistoryAtom)
    registry.set(tickHistoryAtom, [...history.slice(-99), tick])
  })
}

// Stream-backed for WebSocket
const liveTicksAtom = appRuntime.atom(
  Effect.gen(function* () {
    const ws = yield* TradingWebSocket
    return yield* ws.subscribe("ticks")
  })
)
```

### Pattern: Chat/Messaging

```typescript
// Conversation family keyed by chat ID
const ConversationSchema = Schema.Struct({
  chatId: Schema.String.pipe(Schema.brand("ChatId")),
  messages: Schema.Array(MessageSchema),
  participants: Schema.Array(Schema.String)
})

const conversationFamily = Fermion.fromSchema(ConversationSchema)
  .withKey("chatId")
  .withFetch((id) => ChatApi.getConversation(id))
  .withPersist((conv) => ChatApi.updateConversation(conv))
  .build()

// Optimistic message append
const sendMessage = (chatId: string, content: string) => {
  const convAtom = conversationFamily(chatId)
  const result = registry.get(convAtom)

  if (Result.isSuccess(result)) {
    const conv = result.value
    const optimisticMsg = { id: crypto.randomUUID(), content, pending: true }

    // Optimistic update
    registry.set(convAtom, Result.success({
      ...conv,
      messages: [...conv.messages, optimisticMsg]
    }))

    // Actual send
    ChatApi.sendMessage(chatId, content).pipe(
      Effect.tap(() => conversationFamily.fetch(chatId)),
      Effect.runPromise
    )
  }
}
```

### Pattern: Form State

```typescript
// Field atoms for granular reactivity
const formFieldAtom = Atom.family((field: string) =>
  Atom.make({ value: "", error: null as string | null, touched: false })
)

// Validation derived atom
const formValidAtom = Atom.make((get) => {
  const fields = ["email", "password", "name"]
  return fields.every(f => {
    const field = get(formFieldAtom(f))
    return field.touched && !field.error
  })
})

// Batch field updates
const updateField = (name: string, value: string) => {
  Atom.batch(() => {
    const field = registry.get(formFieldAtom(name))
    const error = validateField(name, value)
    registry.set(formFieldAtom(name), {
      value,
      error,
      touched: true
    })
  })
}

// Submit with all fields
const submitForm = () => {
  const fields = ["email", "password", "name"]
  const data = Object.fromEntries(
    fields.map(f => [f, registry.get(formFieldAtom(f)).value])
  )
  return FormApi.submit(data)
}
```

### Pattern: Data Grid State

```typescript
// Grid state atoms
const gridSelectionAtom = Atom.make<Set<string>>(new Set())
const gridSortAtom = Atom.make<{ column: string; dir: "asc" | "desc" } | null>(null)
const gridPageAtom = Atom.make({ page: 0, pageSize: 50 })

// Row data family
const gridRowFamily = Atom.family((id: string) =>
  Atom.make<GridRow | null>(null)
)

// Derived: visible rows
const visibleRowsAtom = Atom.make((get) => {
  const { page, pageSize } = get(gridPageAtom)
  const sort = get(gridSortAtom)
  const allIds = get(allRowIdsAtom)

  let ids = [...allIds]
  if (sort) {
    ids.sort((a, b) => {
      const rowA = get(gridRowFamily(a))
      const rowB = get(gridRowFamily(b))
      // Sort logic...
    })
  }

  return ids.slice(page * pageSize, (page + 1) * pageSize)
})

// Batch selection
const selectRows = (ids: string[]) => {
  Atom.batch(() => {
    const current = registry.get(gridSelectionAtom)
    registry.set(gridSelectionAtom, new Set([...current, ...ids]))
  })
}
```

---

## Keyphrase Triggers

This skill responds to:
- `[EFFECT:ATOM:SYNC]` - registry.set/get patterns
- `[EFFECT:ATOM:EFFECT]` - Atom.set/get inside Effect.gen
- `[EFFECT:ATOM:FAMILY]` - Atom.family patterns
- `[EFFECT:ATOM:RUNTIME]` - Atom.runtime patterns
- `[EFFECT:ATOM:RESULT]` - Result type handling
- `[EFFECT:ATOM:BATCH]` - Atom.batch patterns

---

## Related Skills

- `/effect-atom-integration` - Atom.runtime, Atom.make, operation atoms
- `/effect-schema-mastery` - Schema.TaggedStruct, branded types
- `/effect-service-authoring` - Effect.Service patterns for algebras
- `/effect-patterns` - General Effect-TS patterns
