---
name: effect-service-authoring
description: Creating Effect.Service<>() classes, Context.Tag patterns, Layer composition. Decision trees for when to use which pattern. Covers service definition, dependency injection, and layer management.
model_invoked: true
triggers:
  - "Effect.Service"
  - "Context.Tag"
  - "Layer"
  - "service"
  - "dependency injection"
  - "DI"
---

# Effect Service Authoring

## Overview

This skill covers the **three canonical patterns** for defining Effect-TS services in TMNL:

1. **Effect.Service<>()** — Auto-layered services with effectful construction (RECOMMENDED DEFAULT)
2. **Context.Tag** — Strategy Pattern for swappable implementations
3. **Context.Tag + Config** — Parameterized services with configuration injection

Master these patterns to build composable, testable, type-safe service architectures.

## Canonical Sources

### Effect-TS Core
- **Submodule**: `../../submodules/effect/packages/effect/src/`
  - `Context.ts:507-585` — Context.Tag and Context.Reference
  - `Layer.ts:289-292` — Layer.effect (effectful construction)
  - `Layer.ts:772-775` — Layer.succeed (synchronous construction)
  - `Layer.ts:727-735` — Layer.scoped (resource management)
  - `Layer.ts:583-589` — Layer.mergeAll (composition)

### Effect Website Documentation
- **Submodule**: `../../submodules/website/content/src/content/docs/docs/`
  - `requirements-management/services.mdx` — Service patterns
  - `requirements-management/layers.mdx` — Layer composition
  - `requirements-management/default-services.mdx` — Default layers

### TMNL Battle-tested Implementations
- **SliderBehavior** — `src/lib/slider/v1/services/SliderBehavior.ts:15` (Strategy Pattern, 5 variants)
- **DataManager** — `src/lib/data-manager/v1/DataManager.ts:73` (Effect.Service with dependencies)
- **SearchKernel** — `src/lib/data-manager/v1/kernels/SearchKernel.ts:308` (Effect.Service)
- **IdGenerator** — `src/lib/layers/v1/services/IdGenerator.ts:34` (Config + Service)

## Patterns

### Decision Tree: Which Service Pattern?

```
Need a service?
│
├─ Multiple swappable implementations (Strategy Pattern)?
│  └─ Use: class extends Context.Tag
│     Example: SliderBehavior (linear, log, decibel, exponential, stepped)
│
├─ Effectful construction or service dependencies?
│  └─ Use: class extends Effect.Service<>()
│     Example: DataManager (depends on SearchKernel)
│
└─ Simple configuration tag?
   └─ Use: class extends Context.Tag
      with Static Default + Custom factories
      Example: IdGeneratorConfig
```

---

### Pattern 1: Effect.Service<>() — RECOMMENDED DEFAULT

**When to use:**
- Service has dependencies on other services
- Construction is effectful (async, fallible, requires resources)
- You want auto-generated `.Default` layer
- Default choice for most new services

**Signature:**
```typescript
class ServiceName extends Effect.Service<ServiceName>()(
  "app/namespace/ServiceName",
  {
    effect: Effect.Effect<Interface>,
    dependencies?: Layer.Layer<Deps>[]
  }
) {}
```

**Full Example:**
```typescript
import { Effect, Context, Layer } from 'effect'

// Define interface
interface DatabaseService {
  readonly query: (sql: string) => Effect.Effect<unknown[]>
  readonly execute: (sql: string) => Effect.Effect<void>
}

// Define service with effectful construction
class Database extends Effect.Service<Database>()(
  "app/Database",
  {
    effect: Effect.gen(function* () {
      // Yield dependencies
      const config = yield* DatabaseConfig

      // Effectful construction
      const pool = yield* Effect.tryPromise(() =>
        createPool(config.connectionString)
      )

      // Define interface methods
      const query = (sql: string) =>
        Effect.tryPromise(() => pool.query(sql))

      const execute = (sql: string) =>
        Effect.tryPromise(() => pool.execute(sql))

      return { query, execute } as const
    }),
    dependencies: [DatabaseConfig.Default]
  }
) {}

// Auto-generated layer available at:
Database.Default

// Usage in other services:
const userService = Effect.gen(function* () {
  const db = yield* Database
  const users = yield* db.query('SELECT * FROM users')
  return users
})
```

**Key Features:**
- **Double `()()` syntax**: First `()` parameterizes generic type, second `()` provides config
- **`dependencies: [...]`**: Auto-provides required layers (optional but recommended)
- **`as const`**: Ensures readonly interface, prevents accidental mutations
- **Auto-generated `.Default`**: Layer is automatically created

**TMNL Example** (`src/lib/data-manager/v1/DataManager.ts:73`):
```typescript
class DataManager extends Effect.Service<DataManager>()(
  "tmnl/data-manager/DataManager",
  {
    effect: Effect.gen(function* () {
      const kernel = yield* SearchKernel

      const search = (query: string, limit: number) =>
        Effect.gen(function* () {
          const results = yield* kernel.search(query, limit)
          return results
        })

      return { search } as const
    }),
    dependencies: [SearchKernel.Default]
  }
) {}
```

---

### Pattern 2: Context.Tag — STRATEGY PATTERN

**When to use:**
- Multiple implementations of same interface (Strategy Pattern)
- Runtime behavior swapping
- Need to export both `.Default` (Layer) AND `.shape` (direct access)

**Signature:**
```typescript
class TagName extends Context.Tag("namespace/TagName")<
  TagName,
  InterfaceShape
>() {}
```

**Full Example:**
```typescript
import { Context, Layer } from 'effect'

// 1. Define interface shape
interface TransformBehavior {
  readonly id: string
  readonly transform: (value: number) => number
  readonly inverse: (value: number) => number
}

// 2. Define tag
class ValueTransform extends Context.Tag("app/ValueTransform")<
  ValueTransform,
  TransformBehavior
>() {}

// 3. Create implementations
const linearImpl: TransformBehavior = {
  id: 'linear',
  transform: (v) => v,
  inverse: (v) => v,
}

const logarithmicImpl: TransformBehavior = {
  id: 'logarithmic',
  transform: (v) => Math.log(v),
  inverse: (v) => Math.exp(v),
}

// 4. Export BOTH .Default AND .shape
export const LinearTransform = {
  Default: Layer.succeed(ValueTransform, linearImpl),
  shape: linearImpl,  // Direct access without Layer
}

export const LogarithmicTransform = {
  Default: Layer.succeed(ValueTransform, logarithmicImpl),
  shape: logarithmicImpl,
}

// 5. Runtime swapping
const withLinear = program.pipe(Effect.provide(LinearTransform.Default))
const withLog = program.pipe(Effect.provide(LogarithmicTransform.Default))
```

**Key Features:**
- **Export `.shape`**: Allows direct access without Effect runtime
- **Export `.Default`**: Layer for Effect programs
- **Layer.succeed**: Creates layer from synchronous value
- **Swappable**: Change behavior via `Effect.provide`

**TMNL Example** (`src/lib/slider/v1/services/SliderBehavior.ts`):
```typescript
// Interface
interface SliderBehaviorShape {
  readonly id: string
  readonly normalize: (value: number, min: number, max: number) => number
  readonly denormalize: (normalized: number, min: number, max: number) => number
  readonly format: (value: number, precision: number, unit: string) => string
}

// Tag
class SliderBehavior extends Context.Tag('tmnl/slider/SliderBehavior')<
  SliderBehavior,
  SliderBehaviorShape
>() {}

// Linear implementation
const linearBehavior: SliderBehaviorShape = {
  id: 'linear',
  normalize(value, min, max) {
    return (value - min) / (max - min)
  },
  denormalize(normalized, min, max) {
    return min + normalized * (max - min)
  },
  format(value, precision, unit) {
    return `${value.toFixed(precision)}${unit}`
  },
}

export const LinearBehavior = {
  Default: Layer.succeed(SliderBehavior, linearBehavior),
  shape: linearBehavior,
}

// 4 more behaviors: Logarithmic, Decibel, Exponential, Stepped
// Each follows same pattern: implementation + { Default, shape }
```

---

### Pattern 3: Context.Tag + Config — PARAMETERIZED SERVICE

**When to use:**
- Service needs configuration injection
- Configuration should be overridable at composition time
- Want to separate config from service logic

**Critical Rule:** **Define Config tag BEFORE Service** (avoids circular dependencies)

**Full Example:**
```typescript
import { Context, Effect, Layer } from 'effect'

// 1. Config tag FIRST
class ApiConfig extends Context.Tag("app/ApiConfig")<
  ApiConfig,
  { readonly baseUrl: string; readonly timeout: number }
>() {
  static Default = Layer.succeed(this, {
    baseUrl: 'https://api.example.com',
    timeout: 5000
  })

  static Custom = (config: { baseUrl: string; timeout: number }) =>
    Layer.succeed(this, config)
}

// 2. Service depends on config
class ApiClient extends Effect.Service<ApiClient>()(
  "app/ApiClient",
  {
    effect: Effect.gen(function* () {
      const config = yield* ApiConfig  // Dependency on config

      const fetch = (path: string) =>
        Effect.tryPromise(() =>
          window.fetch(`${config.baseUrl}${path}`, {
            signal: AbortSignal.timeout(config.timeout)
          })
        )

      return { fetch } as const
    }),
    dependencies: [ApiConfig.Default]
  }
) {}

// 3. Override config at composition
const productionLayer = ApiClient.Default.pipe(
  Layer.provide(ApiConfig.Custom({
    baseUrl: 'https://prod.example.com',
    timeout: 10000
  }))
)

const testLayer = ApiClient.Default.pipe(
  Layer.provide(ApiConfig.Custom({
    baseUrl: 'http://localhost:3000',
    timeout: 1000
  }))
)
```

**Key Features:**
- **Static `.Default`**: Default configuration
- **Static `.Custom`**: Factory for custom configuration
- **Order matters**: Config tag MUST be defined before service
- **Layer.provide**: Override dependencies at composition

**TMNL Example** (`src/lib/layers/v1/services/IdGenerator.ts`):
```typescript
// Config FIRST
class IdGeneratorConfig extends Context.Tag('app/layers/IdGeneratorConfig')<
  IdGeneratorConfig,
  { strategy: 'nanoid' | 'uuid' | 'custom'; customFn?: () => string }
>() {
  static Default = Layer.succeed(this, { strategy: 'nanoid' })
  static Custom = (config: { strategy: 'nanoid' | 'uuid' | 'custom'; customFn?: () => string }) =>
    Layer.succeed(this, config)
}

// Service SECOND
class IdGenerator extends Effect.Service<IdGenerator>()(
  "app/layers/IdGenerator",
  {
    effect: Effect.gen(function* () {
      const config = yield* IdGeneratorConfig

      const generate = () => {
        switch (config.strategy) {
          case 'nanoid': return nanoid()
          case 'uuid': return uuidv4()
          case 'custom': return config.customFn?.() ?? nanoid()
        }
      }

      return { generate } as const
    }),
    dependencies: [IdGeneratorConfig.Default]
  }
) {}
```

---

### Pattern 4: Layer Composition

**Layer.mergeAll** — Combine multiple service layers:

```typescript
import { Layer } from 'effect'

// Individual service layers
const configLayer = ConfigService.Default
const loggerLayer = LoggerService.Default
const dbLayer = DatabaseService.Default

// Merge into single runtime layer
const AppLayer = Layer.mergeAll(
  configLayer,
  loggerLayer,
  dbLayer
)

// Use with effect-atom
const appRuntime = Atom.runtime(AppLayer)
```

**Layer.provide** — Inject dependencies:

```typescript
// Service depends on Database
const UserServiceLive = Layer.effect(
  UserService,
  Effect.gen(function* () {
    const db = yield* Database
    return { findUser: (id) => db.query(`SELECT * FROM users WHERE id = ${id}`) }
  })
).pipe(
  Layer.provide(Database.Default)  // Inject dependency
)
```

**Layer chains** — Complex dependency graphs:

```typescript
// A → B → C (A depends on B, B depends on C)
const CLayer = ConfigService.Default
const BLayer = DatabaseService.Default.pipe(Layer.provide(CLayer))
const ALayer = UserService.Default.pipe(Layer.provide(BLayer))

// All dependencies satisfied
const program = Effect.gen(function* () {
  const users = yield* UserService
  return users
}).pipe(Effect.provide(ALayer))
```

---

### Pattern 5: Resource Management with Layer.scoped

**When to use:**
- Service acquires resources (connections, file handles, subscriptions)
- Resources need cleanup on shutdown
- Want automatic resource disposal

**Example:**
```typescript
import { Effect, Layer } from 'effect'

class ConnectionPool extends Context.Tag("app/ConnectionPool")<
  ConnectionPool,
  { query: (sql: string) => Effect.Effect<unknown[]> }
>() {}

const ConnectionPoolLive = Layer.scoped(
  ConnectionPool,
  Effect.acquireRelease(
    // Acquire
    Effect.gen(function* () {
      const pool = yield* Effect.tryPromise(() => createPool())
      yield* Effect.log("Pool created")
      return { query: (sql) => Effect.tryPromise(() => pool.query(sql)) }
    }),
    // Release (called on layer disposal)
    (pool) => Effect.gen(function* () {
      yield* Effect.log("Closing pool")
      yield* Effect.tryPromise(() => pool.close())
    })
  )
)
```

## Examples

### Example 1: Simple Service with No Dependencies

```typescript
import { Effect } from 'effect'

class RandomService extends Effect.Service<RandomService>()(
  "app/RandomService",
  {
    effect: Effect.gen(function* () {
      const randomInt = (max: number) =>
        Effect.sync(() => Math.floor(Math.random() * max))

      const randomString = (length: number) =>
        Effect.sync(() =>
          Array.from({ length }, () =>
            String.fromCharCode(97 + Math.floor(Math.random() * 26))
          ).join('')
        )

      return { randomInt, randomString } as const
    })
  }
) {}

// Usage
const program = Effect.gen(function* () {
  const random = yield* RandomService
  const n = yield* random.randomInt(100)
  const s = yield* random.randomString(10)
  console.log({ n, s })
})
```

### Example 2: Service with Multiple Dependencies

```typescript
import { Effect, Layer } from 'effect'

// Service A
class Logger extends Effect.Service<Logger>()(
  "app/Logger",
  {
    effect: Effect.succeed({
      log: (msg: string) => Effect.sync(() => console.log(msg))
    })
  }
) {}

// Service B
class Config extends Effect.Service<Config>()(
  "app/Config",
  {
    effect: Effect.succeed({
      apiKey: "secret-key",
      baseUrl: "https://api.example.com"
    })
  }
) {}

// Service C depends on A and B
class ApiClient extends Effect.Service<ApiClient>()(
  "app/ApiClient",
  {
    effect: Effect.gen(function* () {
      const logger = yield* Logger
      const config = yield* Config

      const fetch = (path: string) =>
        Effect.gen(function* () {
          yield* logger.log(`Fetching: ${config.baseUrl}${path}`)
          const response = yield* Effect.tryPromise(() =>
            window.fetch(`${config.baseUrl}${path}`)
          )
          return response
        })

      return { fetch } as const
    }),
    dependencies: [Logger.Default, Config.Default]
  }
) {}

// All dependencies auto-satisfied
const program = Effect.gen(function* () {
  const api = yield* ApiClient
  yield* api.fetch('/users')
})
```

### Example 3: Swappable Behaviors (Strategy Pattern)

```typescript
import { Context, Effect, Layer } from 'effect'

interface CacheStrategy {
  readonly name: string
  readonly get: <A>(key: string) => Effect.Effect<A | null>
  readonly set: <A>(key: string, value: A) => Effect.Effect<void>
}

class Cache extends Context.Tag("app/Cache")<Cache, CacheStrategy>() {}

// In-memory implementation
const memoryCache: CacheStrategy = {
  name: 'memory',
  get: (key) => Effect.sync(() => memoryStore.get(key) ?? null),
  set: (key, value) => Effect.sync(() => memoryStore.set(key, value)),
}

// Redis implementation
const redisCache: CacheStrategy = {
  name: 'redis',
  get: (key) => Effect.tryPromise(() => redis.get(key)),
  set: (key, value) => Effect.tryPromise(() => redis.set(key, value)),
}

export const MemoryCache = {
  Default: Layer.succeed(Cache, memoryCache),
  shape: memoryCache,
}

export const RedisCache = {
  Default: Layer.succeed(Cache, redisCache),
  shape: redisCache,
}

// Swap implementations
const dev = program.pipe(Effect.provide(MemoryCache.Default))
const prod = program.pipe(Effect.provide(RedisCache.Default))
```

## Anti-Patterns

### 1. Missing Double `()()` Syntax

```typescript
// WRONG
class MyService extends Effect.Service<MyService>("id", { effect: ... }) {}

// CORRECT
class MyService extends Effect.Service<MyService>()("id", { effect: ... }) {}
```

### 2. Config AFTER Service (Circular Dependency)

```typescript
// WRONG — Circular dependency!
class MyService extends Effect.Service<MyService>()("id", {
  effect: Effect.gen(function* () {
    const config = yield* MyConfig  // MyConfig not defined yet!
  }),
}) {}
class MyConfig extends Context.Tag("config")<...>() {}

// CORRECT — Config first
class MyConfig extends Context.Tag("config")<...>() {}
class MyService extends Effect.Service<MyService>()("id", { ... }) {}
```

### 3. Forgetting `as const`

```typescript
// WRONG — Mutable interface
return { doThing }

// CORRECT — Readonly interface
return { doThing } as const
```

### 4. Not Exporting `.shape` for Strategy Pattern

```typescript
// WRONG — Missing direct access
export const LinearBehavior = {
  Default: Layer.succeed(Behavior, linearImpl),
}

// CORRECT — Export both Layer and shape
export const LinearBehavior = {
  Default: Layer.succeed(Behavior, linearImpl),
  shape: linearImpl,  // Direct access without Layer
}
```

### 5. Using Effect.Ref in React-consumed Services

```typescript
// WRONG — Ref + Atom bridging complexity
const service = Effect.gen(function* () {
  const stateRef = yield* Ref.make(initial)
  // Now need: polling, SubscriptionRef, streams-to-consume-streams
})

// CORRECT — Atom-as-State pattern
const stateAtom = Atom.make(initial)
const service = {
  update: (value) => Effect.sync(() => Atom.set(stateAtom, value))
}
```

## Pattern Comparison

| Feature | `Effect.Service<>()` | `Context.Tag` (Strategy) | `Context.Tag + Config` |
|---------|---------------------|--------------------------|------------------------|
| Auto-generates `.Default` | ✅ Yes | ❌ Manual `Layer.succeed` | ⚠️ Config: manual, Service: auto |
| Effectful construction | ✅ `Effect.gen` | ⚠️ Needs `Layer.effect` | ✅ Service uses `Effect.gen` |
| Dependencies array | ✅ `dependencies: [...]` | ❌ Manual `Layer.provide` | ✅ Service has dependencies |
| Multiple implementations | ⚠️ Possible but awkward | ✅ Idiomatic | ❌ Not applicable |
| Configuration injection | ⚠️ Needs separate Config tag | ❌ Not applicable | ✅ Built for this |
| **Recommended for** | **Default choice** | **Strategy Pattern only** | **Configurable services** |

## Quick Reference

| I need to... | Use this pattern |
|--------------|------------------|
| Create a new service with dependencies | `Effect.Service<>()` with `dependencies: [...]` |
| Swap implementations at runtime | `Context.Tag` with multiple `{ Default, shape }` exports |
| Inject configuration into a service | `Context.Tag` for config + `Effect.Service<>()` for service |
| Manage resources (connections, files) | `Layer.scoped` with `Effect.acquireRelease` |
| Compose multiple services | `Layer.mergeAll([...layers])` |
| Override a dependency | `Layer.provide(dependencyLayer)` |
| Access service in Effect program | `yield* ServiceName` |

## Related Skills

- **effect-schema-mastery** — Schema validation for service inputs/outputs
- **effect-atom-integration** — Integrating services with React via effect-atom
- **effect-testing-patterns** — Testing services in isolation
