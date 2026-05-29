---
name: data-manager-system
description: Service-scoped data orchestration for TMNL. Invoke when implementing search, data streams, kernel systems, or Effect-based DAQ. Covers hybrid dispatch (fibers + workers), Atom-as-State pattern, and progressive streaming.
model_invoked: true
triggers:
  - "DataManager"
  - "SearchKernel"
  - "data orchestration"
  - "progressive streaming"
  - "Effect.Service"
  - "kernel system"
  - "DAQ"
  - "data acquisition"
  - "FlexSearch"
  - "Atom.runtime"
  - "namespace kernel"
---

# DataManager System for TMNL

## Overview

Service-scoped data orchestration with:
- **Hybrid dispatch** via Effect (fibers traced/untraced + Web Workers)
- **Kernel architecture** for pluggable data operations (search, index, transform, persist)
- **Progressive streaming** with Stream-first APIs
- **Two versions**: v1 (single-instance Service), v2 (multi-instance namespaced kernels)
- **Atom-as-State pattern** for React integration

## Canonical Sources

### TMNL Implementations

| File | Purpose | Pattern |
|------|---------|---------|
| `src/lib/data-manager/v1/DataManager.ts` | Effect.Service<>() orchestrator | Service with Effect.Ref state |
| `src/lib/data-manager/v1/types.ts` | Core types (Task, Kernel, KernelResult) | Schema candidates |
| `src/lib/data-manager/v1/kernels/SearchKernel.ts` | Search kernel with FlexSearch/Linear drivers | Effect.Service kernel |
| `src/lib/data-manager/v1/atoms/index.ts` | Materialized view atoms | Atom.make + FnContext.set |
| `src/lib/data-manager/v2/types.ts` | Universal DAQ types | Namespace keys, kernel shapes |
| `src/lib/data-manager/v2/KernelRegistry.ts` | Multi-instance kernel registry | Effect.Service<>() registry |
| `src/lib/data-manager/v2/atoms.ts` | Atom families for namespacing | Atom.family pattern |
| `src/lib/data-manager/v2/useKernel.ts` | React hooks for kernel access | Hook composition |

### Testbeds

- **DataManagerTestbed**: `/testbed/data-manager` — v1 with antipattern documentation
- **EffectAtomTestbed**: `/testbed/effect-atom` — Related atom patterns

---

## Pattern 1: Effect.Service<>() DataManager — ORCHESTRATOR

**When:** Building a top-level data orchestrator with stateful operations.

DataManager uses `Effect.Service<>()` (not `Context.Tag`) because it's a **singleton service with internal state** managed via `Effect.Ref`.

```typescript
import * as Effect from "effect/Effect"
import * as Ref from "effect/Ref"
import { Atom } from "@effect-atom/atom-react"

/**
 * DataManager Service - Top-level data orchestrator
 *
 * Pattern: Effect.Service<>() with Effect.Ref for state
 */
export class DataManager<T = unknown> extends Effect.Service<DataManager<T>>()("tmnl/data-manager/DataManager", {
  effect: Effect.gen(function* () {
    // ─────────────────────────────────────────────────────────────────────────
    // Canonical State (Effect.Ref)
    // ─────────────────────────────────────────────────────────────────────────

    const stateRef = yield* Ref.make<DataManagerState<T>>(initialState<T>())
    const resultsRef = yield* Ref.make<readonly SearchResult<T>[]>([])
    const statusRef = yield* Ref.make<StreamStatus>("idle")
    const statsRef = yield* Ref.make<StreamStats>({ chunks: 0, items: 0, ms: 0 })

    // ─────────────────────────────────────────────────────────────────────────
    // Service-Scoped Atoms (Created in Service, Not Shared)
    // ─────────────────────────────────────────────────────────────────────────

    const atoms: DataManagerAtoms<T> = {
      results: Atom.make<readonly SearchResult<T>[]>([]),
      status: Atom.make<StreamStatus>("idle"),
      stats: Atom.make<StreamStats>({ chunks: 0, items: 0, ms: 0 }),
      drivers: Atom.make<DriverState<T>>({
        flex: null,
        linear: null,
        active: "flex",
      }),
      isIndexing: Atom.make<boolean>(false),
      query: Atom.make<string>(""),
      searchResult: Atom.make<Result.Result<readonly SearchResult<T>[], Error>>(
        Result.initial()
      ),
    }

    // ─────────────────────────────────────────────────────────────────────────
    // Return Service Interface
    // ─────────────────────────────────────────────────────────────────────────

    return {
      // Kernel management (internal)
      registerKernel,
      getKernel,
      // Dispatch operations
      dispatch,
      dispatchHot,
      dispatchInWorker,
      // Search operations
      search,
      index,
      // Stats
      getStats,
      // Service-scoped atoms
      atoms,
    } as const
  }),
}) {}
```

**Key Pattern**: Atoms are **service-scoped** (created inside service), not module-level.

**TMNL Location**: `src/lib/data-manager/v1/DataManager.ts:73`

---

## Pattern 2: Hybrid Dispatch — THREE EXECUTION MODES

**When:** Implementing operations with different performance/observability tradeoffs.

DataManager provides three dispatch modes for kernel execution:

### 1. Traced Dispatch (Service Methods)

Use for: lifecycle operations, error paths, admin functions.

```typescript
/**
 * Dispatch task to kernel (traced, fiber)
 *
 * Adds Effect.withSpan for observability.
 */
const dispatch = <R>(
  kernelType: KernelType,
  task: Task<R>
): Effect.Effect<KernelResult<R>> =>
  Effect.gen(function* () {
    const kernel = yield* getKernel(kernelType)

    if (!kernel) {
      return yield* Effect.fail(new Error(`Kernel not found: ${kernelType}`))
    }

    // Update queued count
    yield* Ref.update(stateRef, (s) => ({
      ...s,
      tasksQueued: s.tasksQueued + 1,
    }))

    // Execute with tracing
    const result = yield* kernel.execute(task as Task<unknown, unknown>) as Effect.Effect<KernelResult<R>>

    // Update completed stats
    yield* Ref.update(stateRef, (s) => ({
      ...s,
      tasksQueued: s.tasksQueued - 1,
      tasksCompleted: s.tasksCompleted + 1,
      totalDurationMs: s.totalDurationMs + result.durationMs,
    }))

    return result
  }).pipe(Effect.withSpan(`DataManager.dispatch.${kernelType}`))
```

### 2. Untraced Dispatch (Hot Path)

Use for: search execution, stream processing.

```typescript
/**
 * Dispatch task (untraced, hot path)
 *
 * Skips Effect.withSpan to reduce overhead.
 */
const dispatchHot = <R>(
  kernelType: KernelType,
  task: Task<R>
): Effect.Effect<KernelResult<R>> =>
  Effect.gen(function* () {
    const kernel = yield* getKernel(kernelType)

    if (!kernel) {
      return yield* Effect.fail(new Error(`Kernel not found: ${kernelType}`))
    }

    // Execute without tracing (hot path)
    const result = yield* kernel.executeHot(task as Task<unknown, unknown>) as Effect.Effect<KernelResult<R>>

    // Update stats atomically (no tracing overhead)
    yield* Ref.update(stateRef, (s) => ({
      ...s,
      tasksCompleted: s.tasksCompleted + 1,
      totalDurationMs: s.totalDurationMs + result.durationMs,
    }))

    return result
  })
```

### 3. Worker Dispatch (CPU-Heavy)

Use for: indexing large datasets, batch transforms.

```typescript
/**
 * Dispatch to Web Worker (CPU-heavy operations)
 *
 * Use for: indexing 36K movies, batch transforms
 */
const dispatchInWorker = <R>(
  kernelType: KernelType,
  task: Task<R>
): Effect.Effect<KernelResult<R>> =>
  Effect.gen(function* () {
    const kernel = yield* getKernel(kernelType)

    if (!kernel) {
      return yield* Effect.fail(new Error(`Kernel not found: ${kernelType}`))
    }

    // Update queued count
    yield* Ref.update(stateRef, (s) => ({
      ...s,
      tasksQueued: s.tasksQueued + 1,
    }))

    // Execute in worker
    const result = yield* kernel.executeInWorker(task as Task<unknown, unknown>) as Effect.Effect<KernelResult<R>>

    // Update completed stats
    yield* Ref.update(stateRef, (s) => ({
      ...s,
      tasksQueued: s.tasksQueued - 1,
      tasksCompleted: s.tasksCompleted + 1,
      totalDurationMs: s.totalDurationMs + result.durationMs,
    }))

    return result
  }).pipe(Effect.withSpan(`DataManager.dispatchInWorker.${kernelType}`))
```

**Decision Tree**:
- Admin/lifecycle → `dispatch` (traced)
- Search/streaming → `dispatchHot` (untraced)
- Indexing 10K+ items → `dispatchInWorker`

**TMNL Location**: `src/lib/data-manager/v1/DataManager.ts:121-215`

---

## Pattern 3: Kernel Interface — PLUGGABLE OPERATIONS

**When:** Adding new data operation types (search, index, transform, persist).

All kernels implement the `Kernel<T, P>` interface with three execution modes.

```typescript
/**
 * Kernel type discriminator
 */
export type KernelType = "search" | "index" | "transform" | "persist"

/**
 * Kernel interface - worker unit with hybrid dispatch
 *
 * @template T - Result type
 * @template P - Payload type
 */
export interface Kernel<T = unknown, P = unknown> {
  readonly type: KernelType

  /**
   * Execute with tracing (adds Effect span)
   * Use for: service methods, lifecycle ops, error paths
   */
  readonly execute: (task: Task<T, P>) => Effect.Effect<KernelResult<T>>

  /**
   * Execute without tracing (hot path)
   * Use for: search execution, stream processing
   */
  readonly executeHot: (task: Task<T, P>) => Effect.Effect<KernelResult<T>>

  /**
   * Execute in Web Worker (CPU-heavy operations)
   * Use for: indexing 36K movies, batch transforms
   */
  readonly executeInWorker: (task: Task<T, P>) => Effect.Effect<KernelResult<T>>
}

/**
 * Task wrapper for kernel dispatch
 */
export interface Task<T, P = unknown> {
  readonly id: string
  readonly type: KernelType
  readonly payload: P
  readonly priority?: "high" | "normal" | "low"
  readonly timeout?: number
}

/**
 * Kernel execution result
 */
export interface KernelResult<T> {
  readonly taskId: string
  readonly value: T
  readonly durationMs: number
  readonly executionMode: "fiber" | "fiber-untraced" | "worker"
}
```

**TMNL Location**: `src/lib/data-manager/v1/types.ts:22-74`

---

## Pattern 4: SearchKernel — EFFECT.SERVICE KERNEL

**When:** Implementing a search kernel with driver management.

SearchKernel wraps FlexSearch and Linear drivers with the Kernel interface.

```typescript
/**
 * Create a SearchKernel instance
 *
 * Wraps FlexSearch and Linear drivers with Kernel interface.
 */
export const createSearchKernel = <T extends Indexable>(): Effect.Effect<
  Kernel<SearchResultPayload<T>, SearchPayload> & {
    readonly index: (items: readonly T[], config: IndexConfig<T>) => Effect.Effect<void>
    readonly setActiveDriver: (driver: "flex" | "linear") => Effect.Effect<void>
    readonly getDriverInstance: () => Effect.Effect<DriverInstance<T> | null>
    readonly search: (query: SearchQuery) => Stream.Stream<SearchResult<T>>
  }
> =>
  Effect.gen(function* () {
    // Internal state
    const stateRef = yield* Ref.make<SearchKernelState<T>>(initialState<T>())

    /**
     * Initialize drivers
     */
    const initDrivers = (): Effect.Effect<void> =>
      Effect.gen(function* () {
        const flex = yield* createFlexSearchDriver<T>()
        const linear = yield* createLinearDriver<T>()

        yield* Ref.update(stateRef, (s) => ({
          ...s,
          flexDriver: flex,
          linearDriver: linear,
        }))
      })

    // Initialize on creation
    yield* initDrivers()

    /**
     * Get active driver
     */
    const getActiveDriver = (): Effect.Effect<SearchServiceImpl<T>> =>
      Effect.gen(function* () {
        const state = yield* Ref.get(stateRef)
        const driver = state.activeDriver === "flex"
          ? state.flexDriver
          : state.linearDriver

        if (!driver) {
          return yield* Effect.fail(new Error("Search driver not initialized"))
        }

        return driver
      })

    /**
     * Search with streaming results
     */
    const search = (query: SearchQuery): Stream.Stream<SearchResult<T>> =>
      Stream.unwrap(
        Effect.gen(function* () {
          const driver = yield* getActiveDriver()
          return driver.search(query.query, {
            limit: query.limit,
            chunkSize: query.chunkSize,
          }) as Stream.Stream<SearchResult<T>>
        })
      )

    /**
     * Execute search task (traced)
     */
    const execute = (
      task: Task<SearchResultPayload<T>, SearchPayload>
    ): Effect.Effect<KernelResult<SearchResultPayload<T>>> =>
      Effect.gen(function* () {
        const startTime = Date.now()
        const driver = yield* getActiveDriver()

        // Collect stream results
        const results = yield* Stream.runCollect(
          driver.search(task.payload.query, task.payload.options)
        )

        const durationMs = Date.now() - startTime

        return {
          taskId: task.id,
          value: {
            results: Array.from(results) as readonly SearchResult<T>[],
            totalMs: durationMs,
          },
          durationMs,
          executionMode: "fiber" as const,
        }
      }).pipe(Effect.withSpan(`SearchKernel.execute.${task.id}`))

    /**
     * Execute search task (untraced, hot path)
     */
    const executeHot = (
      task: Task<SearchResultPayload<T>, SearchPayload>
    ): Effect.Effect<KernelResult<SearchResultPayload<T>>> =>
      Effect.gen(function* () {
        const startTime = Date.now()
        const driver = yield* getActiveDriver()

        // Collect stream results (no tracing overhead)
        const results = yield* Stream.runCollect(
          driver.search(task.payload.query, task.payload.options)
        )

        const durationMs = Date.now() - startTime

        return {
          taskId: task.id,
          value: {
            results: Array.from(results) as readonly SearchResult<T>[],
            totalMs: durationMs,
          },
          durationMs,
          executionMode: "fiber-untraced" as const,
        }
      })

    return {
      type: "search" as const,
      execute,
      executeHot,
      executeInWorker,
      // Extensions (not part of base Kernel interface)
      index,
      setActiveDriver,
      getDriverInstance,
      search,
    }
  })

/**
 * SearchKernel as Effect.Service
 */
export class SearchKernel extends Effect.Service<SearchKernel>()("tmnl/data-manager/SearchKernel", {
  effect: createSearchKernel(),
}) {}
```

**TMNL Location**: `src/lib/data-manager/v1/kernels/SearchKernel.ts:54-310`

---

## Pattern 5: Atom-as-State — MATERIALIZED VIEWS

**When:** Bridging Effect services with React components.

**CRITICAL PATTERN**: Use `Atom.make()` at module level + `FnContext.set()` in operations.

```typescript
import { Atom } from '@effect-atom/atom-react';
import * as Effect from 'effect/Effect';
import * as Stream from 'effect/Stream';

// ─────────────────────────────────────────────────────────────────────────────
// Materialized View Atoms (Module-Level Singletons)
// Must be Writable for FnContext.set() to work
// ─────────────────────────────────────────────────────────────────────────────

/**
 * Search Results Atom
 *
 * Progressive search results from active stream.
 * Updated by searchOps.search as stream emits chunks.
 */
export const resultsAtom = Atom.make<readonly SearchResult<unknown>[]>([]);

/**
 * Stream Status Atom
 */
export const statusAtom = Atom.make<StreamStatus>('idle');

/**
 * Stream Stats Atom
 */
export const statsAtom = Atom.make<StreamStats>({ chunks: 0, items: 0, ms: 0 });

// ─────────────────────────────────────────────────────────────────────────────
// Derived Atoms (Computed from Materialized Views)
// ─────────────────────────────────────────────────────────────────────────────

/**
 * Is Searching Atom
 */
export const isSearchingAtom = Atom.make((get) => {
  const status = get(statusAtom);
  return status === 'streaming';
});

/**
 * Throughput Atom
 */
export const throughputAtom = Atom.make((get) => {
  const stats = get(statsAtom);
  if (stats.ms > 0) {
    return (stats.items / stats.ms) * 1000; // items per second
  }
  return 0;
});

// ─────────────────────────────────────────────────────────────────────────────
// Runtime Atom (For Effect Operations)
// ─────────────────────────────────────────────────────────────────────────────

/**
 * DataManager Runtime Atom
 */
export const dataManagerRuntimeAtom = Atom.runtime(SearchKernel.Default);

// ─────────────────────────────────────────────────────────────────────────────
// Operation Atoms (Mutations via Effect)
// ─────────────────────────────────────────────────────────────────────────────

/**
 * Search Operations
 *
 * Mutation atoms for triggering search operations.
 * These update the materialized view atoms via FnContext.set()
 */
export const searchOps = {
  /**
   * Execute search and update materialized views
   *
   * Key: Use `ctx.set(atom, value)` to update materialized views
   */
  search: dataManagerRuntimeAtom.fn<SearchQuery>()((query, ctx) =>
    Effect.gen(function* () {
      // Reset materialized views via FnContext.set()
      ctx.set(resultsAtom, []);
      ctx.set(statusAtom, 'streaming');
      ctx.set(statsAtom, { chunks: 0, items: 0, ms: 0 });
      ctx.set(queryAtom, query.query);

      const startTime = Date.now();
      const kernel = yield* SearchKernel;

      // Get driver instance for searching
      const driver = yield* kernel.getDriverInstance();

      if (!driver) {
        ctx.set(statusAtom, 'error');
        return yield* Effect.fail(
          new Error('No search driver available. Index data first.')
        );
      }

      // Collect all results from stream
      const allResults: SearchResult<unknown>[] = [];

      yield* Stream.runForEach(driver.search(query), (result) =>
        Effect.sync(() => {
          allResults.push(result as SearchResult<unknown>);

          // Progressive update every 50 results
          if (allResults.length % 50 === 0) {
            ctx.set(resultsAtom, [...allResults]);
            ctx.set(statsAtom, {
              chunks: Math.ceil(allResults.length / 50),
              items: allResults.length,
              ms: Date.now() - startTime,
            });
          }
        })
      );

      // Final update
      const finalMs = Date.now() - startTime;

      ctx.set(resultsAtom, allResults);
      ctx.set(statusAtom, 'complete');
      ctx.set(statsAtom, {
        chunks: Math.ceil(allResults.length / 50),
        items: allResults.length,
        ms: finalMs,
      });

      return allResults;
    })
  ),
};
```

**Key Pattern**: `ctx.set(atom, value)` inside `runtimeAtom.fn()` updates module-level atoms.

**TMNL Location**: `src/lib/data-manager/v1/atoms/index.ts:44-262`

---

## Pattern 6: Progressive Streaming — STREAM-FIRST API

**When:** Implementing search with incremental results.

DataManager's search returns `Stream.Stream<SearchResult<T>>` for progressive updates.

```typescript
/**
 * Search with progressive streaming
 *
 * Updates atoms as stream progresses for reactive UI
 */
const search = (query: SearchQuery): Stream.Stream<SearchResult<T>> =>
  Stream.unwrap(
    Effect.gen(function* () {
      const state = yield* Ref.get(stateRef)
      const driver = state.drivers.active === "flex"
        ? state.drivers.flex
        : state.drivers.linear

      if (!driver) {
        return Stream.fail(new Error("No search driver available"))
      }

      // Reset state for new search
      yield* Ref.set(resultsRef, [])
      yield* Ref.set(statusRef, "streaming")
      yield* Ref.set(statsRef, { chunks: 0, items: 0, ms: 0 })
      yield* Ref.update(stateRef, (s) => ({ ...s, currentQuery: query.query }))

      const startTime = Date.now()

      // Create progressive stream with atom updates
      return driver.search(query).pipe(
        Stream.tap((result) =>
          Effect.gen(function* () {
            yield* Ref.update(resultsRef, (results) => [...results, result as SearchResult<T>])
            yield* Ref.update(statsRef, (stats) => ({
              ...stats,
              items: stats.items + 1,
              ms: Date.now() - startTime,
            }))
          })
        ),
        Stream.onDone(() =>
          Effect.gen(function* () {
            yield* Ref.set(statusRef, "complete")
            yield* Ref.update(statsRef, (stats) => ({
              ...stats,
              ms: Date.now() - startTime,
              throughput: stats.items / ((Date.now() - startTime) / 1000),
            }))
          })
        )
      ) as Stream.Stream<SearchResult<T>>
    })
  )
```

**React Integration**:

```typescript
import { useAtomValue } from '@effect-atom/atom-react'
import { resultsAtom, statusAtom, statsAtom, throughputAtom } from './atoms'

function SearchResults() {
  const results = useAtomValue(resultsAtom)
  const status = useAtomValue(statusAtom)
  const stats = useAtomValue(statsAtom)
  const throughput = useAtomValue(throughputAtom)

  return (
    <div>
      <div>Status: {status}</div>
      <div>Results: {results.length}</div>
      <div>Throughput: {throughput.toFixed(0)}/s</div>
      <div>Duration: {stats.ms}ms</div>
    </div>
  )
}
```

**TMNL Location**: `src/lib/data-manager/v1/DataManager.ts:226-270`

---

## Pattern 7: DataManager v2 — NAMESPACE KERNELS

**When:** Using multi-instance kernels with namespace isolation.

V2 introduces `NamespaceKey` pattern for multiple independent kernel instances.

```typescript
/**
 * Namespace key format: `${kernelType}:${instanceName}`
 *
 * Examples:
 * - "search:movies" - SearchKernel for movie data
 * - "network:trading" - WebSocket kernel for trading data
 * - "filesystem:logs" - File watcher for log files
 * - "serial:arduino" - Serial port kernel for hardware
 */
export type NamespaceKey = `${KernelType}:${string}`

/**
 * Universal DAQ Kernel Types
 */
export type KernelType =
  | "search"      // FlexSearch, Linear, future backends
  | "network"     // WebSocket, WebTransport, SSE, HTTP polling
  | "filesystem"  // File watch, directory scan, log tail
  | "serial"      // Web Serial API
  | "hardware"    // WebUSB, WebHID
  | "custom"      // User-defined kernels
```

### Using v2 Search Kernel

```typescript
import { useSearchKernel } from '@/lib/data-manager/v2'

function MovieSearch() {
  const { atoms, search, index, isReady } = useSearchKernel<Movie>("movies")

  // Index on mount
  useEffect(() => {
    index(movies, { fields: ["title", "cast"] })
  }, [])

  // Search
  const handleSearch = () => search({ query: inputValue })

  // Read atoms
  const results = useAtomValue(atoms.results)
  const status = useAtomValue(atoms.status)
}
```

### Multiple Namespaces

```typescript
// Two independent search kernels
const movies = useSearchKernel<Movie>("movies")
const users = useSearchKernel<User>("users")

// Each has isolated state
movies.atoms.results  // → ScoredResult<Movie>[]
users.atoms.results   // → ScoredResult<User>[]
```

### Provider Pattern

```typescript
import { SearchKernelProvider, useSearchOpsFromContext } from '@/lib/data-manager/v2'

function App() {
  return (
    <SearchKernelProvider instance="movies">
      <MovieSearch />
      <MovieResults />
    </SearchKernelProvider>
  )
}

function MovieSearch() {
  const { search, isReady } = useSearchOpsFromContext()
  // ...
}
```

**TMNL Location**: `src/lib/data-manager/v2/`

---

## Decision Tree: Which Version?

```
What are you building?
│
├─ Single search kernel for entire app?
│  └─ DataManager v1
│
├─ Multiple independent search instances?
│  └─ DataManager v2 (namespace pattern)
│
├─ Network/filesystem/serial DAQ?
│  └─ DataManager v2 (universal kernel types)
│
└─ Complex orchestration with multiple kernel types?
   └─ DataManager v2 (KernelRegistry)
```

---

## Anti-Patterns

### Don't: Use Atom.runtime(Layer) with Stateful Services

```typescript
// BANNED - Each runtimeAtom.fn() call creates fresh service instance
const runtimeAtom = Atom.runtime(SearchKernel.Default)
const searchOps = {
  search: runtimeAtom.fn<Query>()((query, ctx) =>
    Effect.gen(function*() {
      const kernel = yield* SearchKernel // ← Fresh instance!
      return yield* kernel.search(query) // ← Empty driver!
    })
  )
}

// CORRECT - Direct driver pattern with useState
const [driver, setDriver] = useState<SearchServiceImpl | null>(null)

useEffect(() => {
  const init = async () => {
    const flex = await Effect.runPromise(createFlexSearchDriver())
    await Effect.runPromise(flex.index(items, config))
    setDriver(flex) // ← Persists across operations
  }
  init()
}, [])
```

**See**: `DataManagerTestbed.tsx:17-51` for full antipattern documentation.

### Don't: Track Function Calls Instead of Outcomes

```typescript
// BANNED - Hypothesis passes when function is called, not when outcome achieved
useEffect(() => {
  if (gridData) {  // ← gridData exists (even if empty [])
    updateHypothesis('H1', 'passed')  // ← FALSE POSITIVE
  }
}, [gridData])

// CORRECT - Verify actual outcome
useEffect(() => {
  if (gridData.length > 0) {  // ← Actually has results
    updateHypothesis('H1', 'passed', `${gridData.length} rows in grid`)
  }
}, [gridData, updateHypothesis])
```

### Don't: Skip Progressive Updates

```typescript
// BANNED - Collect all results, then set atom once
const allResults = yield* Stream.runCollect(searchStream)
ctx.set(resultsAtom, allResults) // ← Blocks until complete

// CORRECT - Update atom progressively as stream emits
yield* Stream.runForEach(searchStream, (result) =>
  Effect.sync(() => {
    allResults.push(result)
    if (allResults.length % 50 === 0) {
      ctx.set(resultsAtom, [...allResults]) // ← Progressive updates
    }
  })
)
```

---

## Integration Points

**Depends on:**
- `effect-patterns` — Effect.Service<>(), Effect.Ref, Stream
- `effect-atom-integration` — Atom.make, Atom.runtime, FnContext.set
- `effect-stream-patterns` — Stream.tap, Stream.runForEach, Stream.unwrap

**Used by:**
- `ag-grid-patterns` — DataGrid consumes search results
- `react-state-migration` — useState → Atom.make migration
- `tmnl-testbed-patterns` — Hypothesis validation testbeds

---

## Quick Reference

| Task | Pattern | File |
|------|---------|------|
| Create DataManager service | `Effect.Service<>()` with Effect.Ref | v1/DataManager.ts:73 |
| Implement kernel | `Kernel<T, P>` interface with 3 modes | v1/types.ts:54 |
| Traced dispatch | `dispatch(kernelType, task)` | v1/DataManager.ts:121 |
| Untraced dispatch (hot) | `dispatchHot(kernelType, task)` | v1/DataManager.ts:157 |
| Worker dispatch | `dispatchInWorker(kernelType, task)` | v1/DataManager.ts:186 |
| Progressive streaming | `Stream.tap` + `ctx.set(atom)` | v1/atoms/index.ts:205 |
| Multi-instance kernels | `useSearchKernel<T>("namespace")` | v2/useKernel.ts |
| Namespace atoms | `getNamespaceAtoms(key)` | v2/atoms.ts |
| Provider pattern | `<SearchKernelProvider instance="...">` | v2/KernelProvider.tsx |
