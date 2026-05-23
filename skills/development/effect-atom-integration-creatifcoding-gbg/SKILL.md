---
name: effect-atom-integration
description: Atom.runtime, Atom.make, runtimeAtom.fn, operation atoms, Result handling. Atom-as-State doctrine for integrating Effect services with React.
model_invoked: true
triggers:
  - "Atom.runtime"
  - "Atom.make"
  - "effect-atom"
  - "runtimeAtom"
  - "operation atom"
  - "Result"
---

# Effect-Atom Integration

## Overview

**effect-atom** bridges Effect-TS services with React via reactive atoms. This is the canonical state management pattern for TMNL.

**CRITICAL DOCTRINE: Atom-as-State**

From `.edin/EFFECT_PATTERNS.md`:
> **NO EFFECT.REF. EVER.**
>
> When React is the consumer via effect-atom, `Atom.make()` is the primary state mechanism—not `Effect.Ref` inside services.
>
> - Service methods mutate Atoms directly (`Atom.set`, `ctx.set`)
> - React subscribes directly to atoms
> - This eliminates the Ref→Atom bridge: no polling, no SubscriptionRef, no streams-to-consume-streams

## Canonical Sources

### effect-atom Core
- **Submodule**: `../../submodules/effect-atom/packages/atom/src/`
  - `Atom.ts:370-391` — Atom.make (Effect detection)
  - `Atom.ts:458-463` — Writable atoms
  - `Atom.ts:328-338` — Readable (derived) atoms
  - `Atom.ts:643-715` — Atom.runtime
  - `Atom.ts:553-588` — AtomRuntime.fn (operation atoms)
  - `Atom.ts:1316-1351` — Atom.family

### effect-atom Tests
- **Submodule**: `../../submodules/effect-atom/packages/atom/test/`
  - `Atom.test.ts` — Canonical usage patterns
  - `Result.test.ts` — Result type handling

### TMNL Battle-tested Implementations
- **DataManager atoms** — `src/lib/data-manager/v1/atoms/index.ts` (canonical Atom-as-State)
- **Slider atoms** — `src/lib/slider/v1/atoms/index.ts` (runtime factories)
- **Testbed** — `src/components/testbed/EffectAtomTestbed.tsx` (comprehensive examples)

## Patterns

### Decision Tree: Which Atom Pattern?

```
Need reactive state?
│
├─ Simple mutable state (counter, toggle)?
│  └─ Use: Atom.make(value) → Writable<A>
│     Read: get(atom), Write: ctx.set(atom, value)
│
├─ Derived from other atoms (computed value)?
│  └─ Use: Atom.make((get) => ...) → Atom<A> (readonly)
│     Auto-tracks dependencies
│
├─ Async data (API call, database query)?
│  └─ Use: Atom.make(Effect) → Atom<Result<A, E>>
│     Result.isSuccess, Result.isFailure, Result.isInitial
│
├─ Service access (yield* MyService)?
│  └─ Use: Atom.runtime(Layer) → AtomRuntime<R, E>
│     Create atoms with service dependencies
│
├─ Mutation/action (searchOp, clearOp)?
│  └─ Use: runtime.fn<Arg>()((arg, ctx) => Effect)
│     Trigger with useSetAtom(op)(arg)
│
├─ Stream data (progressive, ticking)?
│  └─ Use: Atom.make(Stream) → Atom<Result<A, E>>
│     Updates progressively as stream emits
│
└─ Keyed atoms (layer-123, user-456)?
   └─ Use: Atom.family((key) => Atom.make(...))
      Stable references via WeakRef
```

---

### Pattern 1: Atom.make — PRIMITIVE ATOMS

**When to use:**
- Simple mutable state
- UI toggles, counters, input bindings
- State that doesn't derive from async sources

**Signature:**
```typescript
Atom.make<A>(initialValue: A): Atom.Writable<A>
```

**Full Example:**
```typescript
import { Atom } from '@effect-atom/atom-react'
import { useAtomValue, useSetAtom } from '@effect-rx/rx-react'

// Module-level atoms (stable references)
const countAtom = Atom.make(0)
const nameAtom = Atom.make('')
const isOpenAtom = Atom.make(false)

// React component
function Counter() {
  const count = useAtomValue(countAtom)
  const setCount = useSetAtom(countAtom)

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => setCount(count + 1)}>Increment</button>
    </div>
  )
}
```

**Key Features:**
- **Writable** — Can read AND write
- **Stable references** — Define at module level
- **Type-safe** — TypeScript infers `Atom.Writable<number>`

**TMNL Example** (`src/lib/data-manager/v1/atoms/index.ts:51`):
```typescript
// State atoms (readonly from components)
export const resultsAtom = Atom.make<SearchResult[]>([])
export const statusAtom = Atom.make<StreamStatus>('idle')
export const statsAtom = Atom.make<StreamStats>({ chunks: 0, items: 0, ms: 0 })
```

---

### Pattern 2: Atom.make with Getter — DERIVED ATOMS

**When to use:**
- Computed values from other atoms
- Derived state (fullName from firstName + lastName)
- Auto-tracking dependencies

**Signature:**
```typescript
Atom.make<A>((get) => A): Atom.Atom<A>  // Readonly
```

**Full Example:**
```typescript
import { Atom } from '@effect-atom/atom-react'

const firstNameAtom = Atom.make('John')
const lastNameAtom = Atom.make('Doe')

// Derived atom (auto-tracks dependencies)
const fullNameAtom = Atom.make((get) => {
  const first = get(firstNameAtom)
  const last = get(lastNameAtom)
  return `${first} ${last}`
})

// Another derived atom
const greetingAtom = Atom.make((get) => {
  const name = get(fullNameAtom)
  return `Hello, ${name}!`
})

// React component
function Greeting() {
  const greeting = useAtomValue(greetingAtom)
  return <h1>{greeting}</h1>  // "Hello, John Doe!"
}
```

**Key Features:**
- **Readonly** — Cannot be written to directly
- **Auto-tracks** — Re-computes when dependencies change
- **Lazy** — Only computes when subscribed

**TMNL Example** (`src/lib/data-manager/v1/atoms/index.ts:94`):
```typescript
export const isSearchingAtom = Atom.make((get) => {
  const status = get(statusAtom)
  return status === 'streaming'
})

export const hasResultsAtom = Atom.make((get) => {
  const results = get(resultsAtom)
  return results.length > 0
})
```

---

### Pattern 3: Atom.make with Effect — RESULT ATOMS

**When to use:**
- Async data (API calls, database queries)
- Fallible operations (can fail with typed errors)
- Need `Initial | Success | Failure` states

**Signature:**
```typescript
Atom.make<A, E>(effect: Effect.Effect<A, E>): Atom.Atom<Result<A, E>>
```

**Result Type:**
```typescript
type Result<A, E> =
  | { readonly _tag: 'Initial' }
  | { readonly _tag: 'Success'; readonly value: A }
  | { readonly _tag: 'Failure'; readonly error: E }
```

**Full Example:**
```typescript
import { Atom } from '@effect-atom/atom-react'
import { Effect, Result } from 'effect'
import { useAtomValue } from '@effect-rx/rx-react'

// Effect atom
const userAtom = Atom.make(
  Effect.gen(function* () {
    yield* Effect.sleep('100 millis')
    const response = yield* Effect.tryPromise(() =>
      fetch('/api/user').then(r => r.json())
    )
    return response
  })
)

// React component
function UserProfile() {
  const result = useAtomValue(userAtom)

  // Pattern match on Result
  if (Result.isInitial(result)) {
    return <div>Loading...</div>
  }

  if (Result.isFailure(result)) {
    return <div>Error: {result.error.message}</div>
  }

  // Result.isSuccess
  return <div>User: {result.value.name}</div>
}
```

**Key Features:**
- **Three states** — Initial, Success, Failure
- **Type-safe errors** — `E` is typed
- **Pattern matching** — `Result.isSuccess`, `Result.isFailure`, `Result.isInitial`

**TMNL Example** (`src/components/testbed/EffectAtomTestbed.tsx:1016`):
```typescript
const dataAtom = Atom.make(
  Effect.gen(function* () {
    yield* Effect.sleep('500 millis')
    return { message: 'Hello from Effect!' }
  })
)

function EffectExample() {
  const result = useAtomValue(dataAtom)

  return (
    <div>
      {Result.isInitial(result) && <Spinner />}
      {Result.isSuccess(result) && <div>{result.value.message}</div>}
      {Result.isFailure(result) && <Error error={result.error} />}
    </div>
  )
}
```

---

### Pattern 4: Atom.runtime — SERVICE COMPOSITION

**When to use:**
- Need access to Effect services in atoms
- Compose multiple service layers
- Create service-scoped atom runtime

**Signature:**
```typescript
Atom.runtime<R, E>(layer: Layer.Layer<R, E>): AtomRuntime<R, E>
```

**Full Example:**
```typescript
import { Atom } from '@effect-atom/atom-react'
import { Effect, Layer } from 'effect'

// Services
class Logger extends Effect.Service<Logger>()(
  "app/Logger",
  { effect: Effect.succeed({ log: (msg: string) => Effect.sync(() => console.log(msg)) }) }
) {}

class ApiClient extends Effect.Service<ApiClient>()(
  "app/ApiClient",
  {
    effect: Effect.gen(function* () {
      const logger = yield* Logger
      return {
        fetchUsers: () => Effect.gen(function* () {
          yield* logger.log('Fetching users...')
          return yield* Effect.tryPromise(() => fetch('/api/users').then(r => r.json()))
        })
      } as const
    }),
    dependencies: [Logger.Default]
  }
) {}

// Create runtime from composed layers
export const appRuntime = Atom.runtime(
  Layer.mergeAll(Logger.Default, ApiClient.Default)
)

// Create atoms with service access
export const usersAtom = appRuntime.atom(
  Effect.gen(function* () {
    const api = yield* ApiClient
    return yield* api.fetchUsers()
  })
)

// React component
function UserList() {
  const result = useAtomValue(usersAtom)

  if (Result.isSuccess(result)) {
    return <List items={result.value} />
  }

  return <Loading />
}
```

**Key Methods on AtomRuntime:**
- `runtime.atom(effect)` — Create Result atom with service access
- `runtime.fn<Arg>()((arg, ctx) => effect)` — Create operation atom
- `runtime.pull(stream)` — Create pull-based stream atom

**TMNL Example** (`src/lib/data-manager/v1/atoms/index.ts:142`):
```typescript
export const runtimeAtom = Atom.runtime(
  Layer.mergeAll(
    IdGenerator.Default,
    SearchKernel.Default,
    DataManager.Default
  )
)
```

---

### Pattern 5: runtimeAtom.fn — OPERATION ATOMS

**When to use:**
- Mutations (create, update, delete)
- Actions (search, submit, clear)
- Operations that update other atoms

**Signature:**
```typescript
runtime.fn<Arg>()((arg, ctx) => Effect.Effect<A, E>): AtomResultFn<Arg, A, E>
```

**Full Example:**
```typescript
import { Atom } from '@effect-atom/atom-react'
import { Effect } from 'effect'
import { useSetAtom, useAtomValue } from '@effect-rx/rx-react'

// State atoms
const resultsAtom = Atom.make<string[]>([])
const statusAtom = Atom.make<'idle' | 'loading' | 'complete'>('idle')

// Operation atom
const searchOp = runtimeAtom.fn<string>()((query, ctx) =>
  Effect.gen(function* () {
    const api = yield* ApiClient

    // Update state
    ctx.set(statusAtom, 'loading')
    ctx.set(resultsAtom, [])

    // Perform search
    const results = yield* api.search(query)

    // Update state
    ctx.set(resultsAtom, results)
    ctx.set(statusAtom, 'complete')

    return results
  })
)

// React component
function SearchBox() {
  const doSearch = useSetAtom(searchOp)
  const results = useAtomValue(resultsAtom)
  const status = useAtomValue(statusAtom)

  return (
    <div>
      <input onChange={(e) => doSearch(e.target.value)} />
      {status === 'loading' && <Spinner />}
      <List items={results} />
    </div>
  )
}
```

**Context API (`ctx`):**
- `ctx.get(atom)` — Read atom value
- `ctx.set(atom, value)` — Write atom value
- `ctx.setSelf(value)` — Write to operation's result atom

**Key Features:**
- **Writable** — Trigger with `useSetAtom(op)(arg)`
- **Service access** — `yield* ServiceName` in Effect
- **State updates** — `ctx.set(atom, value)` directly

**TMNL Example** (`src/lib/data-manager/v1/atoms/index.ts:166`):
```typescript
export const doSearch = runtimeAtom.fn<{ query: string; limit: number }>()(
  ({ query, limit }, ctx) =>
    Effect.gen(function* () {
      const dm = yield* DataManager

      ctx.set(statusAtom, 'streaming')
      ctx.set(resultsAtom, [])

      const stream = yield* dm.searchStream(query, limit)

      yield* Stream.runForEach(stream, (result) =>
        Effect.sync(() => {
          const prev = ctx.get(resultsAtom)
          ctx.set(resultsAtom, [...prev, result])
        })
      )

      ctx.set(statusAtom, 'complete')
    })
)
```

---

### Pattern 6: Atom.family — KEYED ATOMS

**When to use:**
- Dynamic atom creation (layer-123, user-456)
- Stable references for same key
- Per-entity atoms

**Signature:**
```typescript
Atom.family<K, A>((key: K) => Atom.Atom<A>): (key: K) => Atom.Atom<A>
```

**Full Example:**
```typescript
import { Atom } from '@effect-atom/atom-react'
import { Effect } from 'effect'

// Family of user atoms
const userAtom = Atom.family((id: string) =>
  Atom.make(
    Effect.gen(function* () {
      const api = yield* ApiClient
      return yield* api.fetchUser(id)
    })
  )
)

// Same ID returns same atom instance
const alice1 = userAtom('alice')
const alice2 = userAtom('alice')
console.log(alice1 === alice2)  // true

// React component
function UserCard({ userId }: { userId: string }) {
  const result = useAtomValue(userAtom(userId))

  if (Result.isSuccess(result)) {
    return <div>{result.value.name}</div>
  }

  return <Loading />
}

// Render multiple users
<div>
  <UserCard userId="alice" />
  <UserCard userId="bob" />
  <UserCard userId="charlie" />
</div>
```

**Key Features:**
- **Stable references** — Same key = same atom
- **Weak references** — Garbage collected when unused
- **Type-safe keys** — Can use objects, not just strings

**TMNL Example** (`src/components/testbed/EffectAtomTestbed.tsx:1026`):
```typescript
const itemAtom = Atom.family((id: string) =>
  Atom.make(
    Effect.gen(function* () {
      yield* Effect.sleep('200 millis')
      return { id, name: `Item ${id}`, timestamp: Date.now() }
    })
  )
)
```

---

### Pattern 7: Materialized View Pattern

**When to use:**
- Separate state (readonly views) from operations (write-only actions)
- Service methods update state via `ctx.set`
- Clean separation of concerns

**Structure:**
```
atoms/
├── state/
│   ├── resultsAtom      ← Primitive, readonly from components
│   ├── statusAtom       ← Primitive, readonly from components
│   └── statsAtom        ← Derived from above
└── operations/
    ├── searchOp         ← runtime.fn, writes to state
    └── clearOp          ← runtime.fn, writes to state
```

**Full Example:**
```typescript
import { Atom } from '@effect-atom/atom-react'
import { Effect } from 'effect'

// ====== STATE (Readonly Views) ======
export const resultsAtom = Atom.make<SearchResult[]>([])
export const statusAtom = Atom.make<'idle' | 'loading' | 'complete'>('idle')
export const statsAtom = Atom.make((get) => {
  const results = get(resultsAtom)
  return {
    count: results.length,
    hasResults: results.length > 0
  }
})

// ====== OPERATIONS (Write-Only Actions) ======
export const searchOp = runtimeAtom.fn<string>()((query, ctx) =>
  Effect.gen(function* () {
    const api = yield* ApiClient

    ctx.set(statusAtom, 'loading')
    ctx.set(resultsAtom, [])

    const results = yield* api.search(query)

    ctx.set(resultsAtom, results)
    ctx.set(statusAtom, 'complete')
  })
)

export const clearOp = runtimeAtom.fn<void>()((_, ctx) =>
  Effect.sync(() => {
    ctx.set(resultsAtom, [])
    ctx.set(statusAtom, 'idle')
  })
)

// ====== REACT COMPONENT ======
function SearchUI() {
  const results = useAtomValue(resultsAtom)
  const status = useAtomValue(statusAtom)
  const stats = useAtomValue(statsAtom)

  const doSearch = useSetAtom(searchOp)
  const clear = useSetAtom(clearOp)

  return (
    <div>
      <input onChange={(e) => doSearch(e.target.value)} />
      <button onClick={() => clear()}>Clear</button>
      {status === 'loading' && <Spinner />}
      <div>Found {stats.count} results</div>
      <List items={results} />
    </div>
  )
}
```

**Key Pattern:**
1. **State atoms** — Define at module level, readonly from components
2. **Operation atoms** — Define with `runtime.fn`, write to state atoms via `ctx.set`
3. **Components** — Subscribe to state, trigger operations

**TMNL Example** (`src/lib/data-manager/v1/atoms/index.ts:34`):
```typescript
// State atoms
export const resultsAtom = Atom.make<SearchResult[]>([])
export const statusAtom = Atom.make<StreamStatus>('idle')

// Operations
export const doSearch = runtimeAtom.fn<{ query: string; limit: number }>()(...)
export const clearResults = runtimeAtom.fn<void>()(...)
```

---

### Pattern 8: Parallel Atom Setup (Effect.all)

**When to use:**
- Setting multiple atoms from within an Effect
- Initializing UI state before opening drawer/modal
- Resetting multiple atoms at once

**Anti-pattern (sequential):**
```typescript
// DON'T — Sequential updates
yield* Effect.sync(() => registry.set(modeAtom, 'command'))
yield* Effect.sync(() => registry.set(promptAtom, 'M-x '))
yield* Effect.sync(() => registry.set(inputAtom, ''))
yield* Effect.sync(() => registry.set(selectedIndexAtom, 0))
```

**Pattern (parallel):**
```typescript
// DO — Parallel updates with Effect.all
yield* Effect.all([
  Effect.sync(() => registry.set(modeAtom, 'command')),
  Effect.sync(() => registry.set(promptAtom, 'M-x ')),
  Effect.sync(() => registry.set(inputAtom, '')),
  Effect.sync(() => registry.set(selectedIndexAtom, 0)),
], { concurrency: 'unbounded' })
```

**Key Features:**
- **Parallel execution** — All updates happen at once
- **Effect.sync** — Wrap synchronous registry operations
- **concurrency: 'unbounded'** — No limit on parallelism

**TMNL Example** (`src/lib/minibuffer/hooks/useMinibuffer.tsx:124`):
```typescript
const openCommandMode = runtimeAtom.fn<void>()((_, ctx) =>
  Effect.gen(function* () {
    yield* Effect.all([
      Effect.sync(() => ctx.set(modeAtom, 'command')),
      Effect.sync(() => ctx.set(promptAtom, 'M-x ')),
      Effect.sync(() => ctx.set(inputAtom, '')),
    ], { concurrency: 'unbounded' })
  })
)
```

---

### Pattern 9: Atom Lifecycle

**keepAlive** — Prevent disposal:
```typescript
const runtimeAtom = Atom.keepAlive(Atom.runtime(ServiceLayer))
```

**setIdleTTL** — Dispose after idle:
```typescript
const cachedAtom = Atom.setIdleTTL(Atom.make(expensiveFetch), '5 minutes')
```

**autoDispose** — Default behavior (dispose when no subscribers).

## Examples

### Example 1: Counter (Primitive Atom)

```typescript
import { Atom } from '@effect-atom/atom-react'
import { useAtomValue, useSetAtom } from '@effect-rx/rx-react'

const countAtom = Atom.make(0)

function Counter() {
  const count = useAtomValue(countAtom)
  const setCount = useSetAtom(countAtom)

  return (
    <div>
      <p>{count}</p>
      <button onClick={() => setCount(count + 1)}>+</button>
    </div>
  )
}
```

### Example 2: Todo List (Operation Atoms)

```typescript
import { Atom } from '@effect-atom/atom-react'
import { Effect } from 'effect'

type Todo = { id: string; text: string; done: boolean }

const todosAtom = Atom.make<Todo[]>([])

const addTodoOp = runtimeAtom.fn<string>()((text, ctx) =>
  Effect.sync(() => {
    const todos = ctx.get(todosAtom)
    ctx.set(todosAtom, [...todos, { id: nanoid(), text, done: false }])
  })
)

const toggleTodoOp = runtimeAtom.fn<string>()((id, ctx) =>
  Effect.sync(() => {
    const todos = ctx.get(todosAtom)
    ctx.set(todosAtom, todos.map(t => t.id === id ? { ...t, done: !t.done } : t))
  })
)

function TodoList() {
  const todos = useAtomValue(todosAtom)
  const addTodo = useSetAtom(addTodoOp)
  const toggleTodo = useSetAtom(toggleTodoOp)

  return (
    <div>
      <input onKeyDown={(e) => {
        if (e.key === 'Enter') addTodo(e.currentTarget.value)
      }} />
      <ul>
        {todos.map(todo => (
          <li key={todo.id} onClick={() => toggleTodo(todo.id)}>
            {todo.done ? '✅' : '⬜'} {todo.text}
          </li>
        ))}
      </ul>
    </div>
  )
}
```

## Anti-Patterns

### 1. Effect.Ref in React-consumed Services (BANNED)

```typescript
// WRONG — Ref + Atom bridging complexity
const service = Effect.gen(function* () {
  const stateRef = yield* Ref.make(initial)
  // Now need: polling, SubscriptionRef, streams-to-consume-streams
})

// CORRECT — Atom-as-State
const stateAtom = Atom.make(initial)
const service = {
  update: (value) => Effect.sync(() => Atom.set(stateAtom, value))
}
```

### 2. Atoms Inside Components

```typescript
// WRONG — Creates new atom every render
function MyComponent() {
  const atom = Atom.make(0)  // ❌ New atom every render!
  return <div>{useAtomValue(atom)}</div>
}

// CORRECT — Module-level atom
const countAtom = Atom.make(0)
function MyComponent() {
  return <div>{useAtomValue(countAtom)}</div>
}
```

### 3. useState for Cross-Component State

```typescript
// WRONG — useState for shared state
const [results, setResults] = useState([])
const [status, setStatus] = useState('idle')

// CORRECT — Atoms
const resultsAtom = Atom.make([])
const statusAtom = Atom.make('idle')
```

## Quick Reference

| Pattern | Constructor | Use Case |
|---------|-------------|----------|
| Primitive atom | `Atom.make(value)` | Simple mutable state |
| Derived atom | `Atom.make((get) => ...)` | Computed from other atoms |
| Effect atom | `Atom.make(Effect)` | Async data with Result |
| Runtime | `Atom.runtime(Layer)` | Service composition |
| Operation | `runtime.fn<Arg>()` | Mutations/actions |
| Family | `Atom.family((key) => ...)` | Keyed atoms |

## Related Skills

- **effect-service-authoring** — Create services for use with runtimeAtom
- **effect-stream-patterns** — Use streams with Atom.make(Stream)
- **effect-testing-patterns** — Test atom-based code
