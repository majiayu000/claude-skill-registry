---
name: bdd-test-implementation
description: |
  Implementing BDD specifications in TypeScript with Vitest and Effect.
  Covers step definitions, hooks, context sharing, and Effect-based test patterns.
  Maps Gherkin scenarios to executable Effect.gen programs.
triggers:
  - "implement.*bdd"
  - "step definition"
  - "it.effect"
  - "@effect/vitest"
  - "test.*effect"
---

# BDD Test Implementation Patterns

## Philosophy: Specifications Drive Implementation

BDD test implementation is NOT "writing tests" - it is **making specifications executable**.

The specification (`.feature` file or hypothesis declaration) already exists. Your job is to:

1. **Translate Given/When/Then into Effect.gen programs**
2. **Provide the Effect Layer dependencies** for service isolation
3. **Assert on outcomes, not function calls** (verify gridData.length > 0, not "setGridData was called")
4. **Maintain step definitions as living documentation** (clear, readable, 1:1 with specs)

**Canonical principle:** If your step definition contains complex logic, the specification is wrong. Fix the spec first.

---

## Canonical Sources

### Primary Test References

**Effect Service Testing:**
- `submodules/effect/packages/*/test/*.test.ts` - Canonical Effect testing patterns
- `submodules/effect-atom/packages/atom/test/*.test.ts` - Atom testing patterns
- `src/lib/streams/__tests__/ChannelService.test.ts` - Effect.Service lifecycle tests
- `src/lib/ams/v2/__tests__/integration.test.ts` - Multi-service integration tests

**TMNL Testbed Patterns:**
- `src/components/testbed/DataManagerTestbed.tsx` - Hypothesis-driven implementation
- `src/components/testbed/shared/hypothesis.tsx` - Validation components
- `.edin/EFFECT_PATTERNS.md` - Effect-atom state patterns

**Testing Documentation:**
- `.edin/EFFECT_TESTING_PATTERNS.md` - @effect/vitest patterns
- `CLAUDE.md` — Submodule testing patterns

---

## Pattern 1: @effect/vitest Setup

### Core API: it.effect()

**@effect/vitest** extends Vitest with `it.effect()` for Effect-based tests:

```typescript
import { describe, it, expect } from '@effect/vitest'
import { Effect } from 'effect'

describe("MyService", () => {
  // Standard Vitest test
  it("synchronous assertion", () => {
    expect(1 + 1).toBe(2)
  })

  // Effect test - returns Effect, not Promise
  it.effect("asynchronous Effect test", () =>
    Effect.gen(function* () {
      const service = yield* MyService
      const result = yield* service.doThing("input")
      expect(result).toBe(42)
    }).pipe(Effect.provide(MyService.Default))
  )
})
```

**Key Difference from Regular Vitest:**

- **Regular `it()`** - Returns `void` or `Promise<void>`
- **`it.effect()`** - Returns `Effect<void, never, ...>`
- **Effect.provide()** required - Must provide Layer dependencies

---

## Pattern 2: Effect Service Step Definitions

### Scenario: Channel Lifecycle

**Specification:**

```gherkin
Scenario: Channel opens successfully
  Given I have registered a channel "test-channel"
  When I open the channel
  Then the channel status should be "open"
  And the openedAt timestamp should be set
```

**Implementation:**

```typescript
// ChannelService.test.ts
import { describe, it, expect } from '@effect/vitest'
import { Effect, Option } from 'effect'
import { ChannelService, ChannelServiceLive } from './ChannelService'
import { ChannelBuilder } from './ChannelBuilder'
import type { ChannelId } from './Channel'

describe("ChannelService Lifecycle", () => {
  it.effect("open() transitions to open state", () =>
    Effect.gen(function* () {
      // GIVEN: I have registered a channel
      const service = yield* ChannelService
      const builder = ChannelBuilder.create("test-channel")
        .inlet("in")
        .outlet("out")
        .wire("in", "out")
      const channelId = yield* service.register(builder)

      // WHEN: I open the channel
      yield* service.open(channelId)

      // THEN: the channel status should be "open"
      const state = yield* service.getState(channelId)
      expect(Option.isSome(state)).toBe(true)

      if (Option.isSome(state)) {
        expect(state.value.status).toBe("open")
        // AND: the openedAt timestamp should be set
        expect(state.value.openedAt).toBeGreaterThan(0)
      }
    }).pipe(Effect.provide(ChannelServiceLive))
  )
})
```

**Pattern Breakdown:**

1. **Given** - Service acquisition + precondition setup
2. **When** - Service method invocation (pure Effect)
3. **Then** - Assertions on returned values
4. **Effect.provide()** - Dependency injection at test boundary

---

## Pattern 3: Effect.either for Error Assertions

### Scenario: Error Handling

**Specification:**

```gherkin
Scenario: Opening non-existent channel fails
  When I try to open channel "missing-channel"
  Then I should receive a CHANNEL_NOT_FOUND error
  And the error should contain the channel ID
```

**Implementation:**

```typescript
it.effect("open() on non-existent channel fails", () =>
  Effect.gen(function* () {
    const service = yield* ChannelService

    // WHEN: Try to open non-existent channel
    const result = yield* service
      .open("missing-channel" as ChannelId)
      .pipe(Effect.either)

    // THEN: Should receive error
    expect(result._tag).toBe("Left")

    if (result._tag === "Left") {
      // AND: Error code should be CHANNEL_NOT_FOUND
      expect(result.left.code).toBe("CHANNEL_NOT_FOUND")
      // AND: Error should contain channel ID
      expect(result.left.channelId).toBe("missing-channel")
      expect(result.left.message).toContain("missing-channel")
    }
  }).pipe(Effect.provide(ChannelServiceLive))
)
```

**Effect.either Pattern:**

```typescript
// Without .either - throws error
yield* service.open("missing") // ❌ Uncaught ChannelServiceError

// With .either - returns Either<Error, Success>
const result = yield* service.open("missing").pipe(Effect.either)
// result: Either<ChannelServiceError, void>

if (result._tag === "Left") {
  // Access error via result.left
  expect(result.left.code).toBe("CHANNEL_NOT_FOUND")
} else {
  // Success path
  const success = result.right
}
```

---

## Pattern 4: Shared Test Fixtures (Background)

### Scenario: Common Setup

**Specification:**

```gherkin
Background:
  Given the ChannelService is initialized
  And I have 3 registered channels

Scenario: List all channel IDs
  When I list channel IDs
  Then I should receive 3 IDs
```

**Implementation:**

```typescript
describe("ChannelService Retrieval", () => {
  // Shared fixture factory
  const setupChannels = () =>
    Effect.gen(function* () {
      const service = yield* ChannelService

      const minimalBuilder = (id: string) =>
        ChannelBuilder.create(id).inlet("in").outlet("out").wire("in", "out")

      yield* service.register(minimalBuilder("ch-1"))
      yield* service.register(minimalBuilder("ch-2"))
      yield* service.register(minimalBuilder("ch-3"))

      return { service }
    })

  it.effect("listIds() returns all channel IDs", () =>
    Effect.gen(function* () {
      // GIVEN: 3 registered channels
      const { service } = yield* setupChannels()

      // WHEN: I list channel IDs
      const ids = yield* service.listIds()

      // THEN: I should receive 3 IDs
      expect(ids).toHaveLength(3)
      expect(ids).toContain("ch-1")
      expect(ids).toContain("ch-2")
      expect(ids).toContain("ch-3")
    }).pipe(Effect.provide(ChannelServiceLive))
  )
})
```

**Pattern:** Shared setup as Effect.gen factory, not `beforeEach()`.

---

## Pattern 5: Data Table Scenarios

### Scenario: Parameterized Tests

**Specification:**

```gherkin
Scenario Outline: Channel state transitions
  Given a channel in <initial_state>
  When I perform <operation>
  Then the channel should be in <final_state>
  And the operation should <error_expectation>

  Examples:
    | initial_state | operation | final_state | error_expectation |
    | idle          | open      | open        | succeed           |
    | open          | open      | open        | succeed (idempotent) |
    | open          | close     | closed      | succeed           |
    | closed        | open      | open        | succeed           |
```

**Implementation:**

```typescript
describe("ChannelService State Transitions", () => {
  const scenarios = [
    { initial: 'idle', op: 'open', final: 'open', shouldSucceed: true },
    { initial: 'open', op: 'open', final: 'open', shouldSucceed: true },
    { initial: 'open', op: 'close', final: 'closed', shouldSucceed: true },
    { initial: 'closed', op: 'open', final: 'open', shouldSucceed: true },
  ]

  scenarios.forEach(({ initial, op, final, shouldSucceed }) => {
    it.effect(`${initial} → ${op} → ${final}`, () =>
      Effect.gen(function* () {
        const service = yield* ChannelService
        const builder = testBuilder()
        const channelId = yield* service.register(builder)

        // Setup initial state
        if (initial === 'open') yield* service.open(channelId)
        if (initial === 'closed') {
          yield* service.open(channelId)
          yield* service.close(channelId)
        }

        // Perform operation
        if (op === 'open') yield* service.open(channelId)
        if (op === 'close') yield* service.close(channelId)

        // Verify final state
        const state = yield* service.getState(channelId)
        if (Option.isSome(state)) {
          expect(state.value.status).toBe(final)
        }
      }).pipe(Effect.provide(ChannelServiceLive))
    )
  })
})
```

---

## Pattern 6: Effect-Atom State Assertions

### Scenario: Atom Updates

**Specification:**

```gherkin
Hypothesis: H1 - Search results flow to grid
  Given the search driver is indexed
  When I search for "matrix"
  Then resultsAtom should contain results
  And gridData should have length > 0
```

**Implementation (React Component Test):**

```typescript
// DataManagerTestbed.tsx (hypothesis validation)
useEffect(() => {
  // THEN: resultsAtom should contain results
  // AND: gridData should have length > 0
  if (
    results.length > 0 &&
    gridData.length > 0 &&
    hypotheses.find((h) => h.id === 'H1')?.status === 'testing'
  ) {
    updateHypothesis('H1', {
      status: 'passed',
      evidence: `${results.length} results → ${gridData.length} grid rows. Search → Grid flow verified.`,
    })
  }
}, [results, gridData, hypotheses, updateHypothesis])
```

**CRITICAL: Verify Outcomes, Not Function Calls**

```typescript
// ❌ BAD - Tracks function call
useEffect(() => {
  if (gridData) {  // gridData exists (even if empty [])
    updateHypothesis('H1', 'passed')  // FALSE POSITIVE
  }
}, [gridData])

// ✅ GOOD - Verifies actual outcome
useEffect(() => {
  if (gridData.length > 0) {  // Actually has results
    updateHypothesis('H1', 'passed', `${gridData.length} rows in grid`)
  }
}, [gridData])
```

---

## Pattern 7: Effect.Scope for Resource Management

### Scenario: Cleanup After Tests

**Specification:**

```gherkin
Scenario: Outlet subscription is released
  Given I subscribe to an outlet
  When the subscription goes out of scope
  Then the subscriber count should decrement
```

**Implementation:**

```typescript
it.effect("subscribeOutlet() increments and decrements subscriber count", () =>
  Effect.gen(function* () {
    const service = yield* ChannelService
    const builder = testBuilder()
    const channelId = yield* service.register(builder)
    yield* service.open(channelId)
    const outletId = `${channelId}:outlet:out1` as OutletId

    // Subscribe within a scope
    yield* Effect.scoped(
      Effect.gen(function* () {
        yield* service.subscribeOutlet(channelId, outletId)

        // Verify increment
        const state = yield* service.getState(channelId)
        if (Option.isSome(state)) {
          const outlet = state.value.topology.outlets.find(o => o.id === outletId)
          expect(outlet?.subscriberCount).toBe(1)
        }
      })
    )

    // After scope closes, verify decrement
    const state = yield* service.getState(channelId)
    if (Option.isSome(state)) {
      const outlet = state.value.topology.outlets.find(o => o.id === outletId)
      expect(outlet?.subscriberCount).toBe(0)
    }
  }).pipe(Effect.scoped, Effect.provide(ChannelServiceLive))
)
```

**Pattern:** Use `Effect.scoped()` to test cleanup behavior.

---

## Pattern 8: Stream Assertions

### Scenario: Progressive Data Flow

**Specification:**

```gherkin
Scenario: Search stream emits results progressively
  Given a search with chunkSize=5
  When I search for "matrix"
  Then I should receive multiple chunks
  And each chunk should have <= 5 items
  And total items should match the limit
```

**Implementation:**

```typescript
it.effect("search stream emits progressive chunks", () =>
  Effect.gen(function* () {
    const driver = yield* Effect.promise(() =>
      Effect.runPromise(createFlexSearchDriver<MovieItem>())
    )

    const movies = processMovies(1000)
    yield* Effect.promise(() =>
      Effect.runPromise(driver.index(movies, {
        fields: ['title', 'cast'],
        store: true,
      }))
    )

    let chunkCount = 0
    let itemCount = 0

    // WHEN: Search with chunkSize=5
    const searchStream = driver.search("matrix", { limit: 20, chunkSize: 5 })

    yield* searchStream.pipe(
      Stream.tap(() => Effect.sync(() => chunkCount++)),
      Stream.runForEach((result) =>
        Effect.sync(() => {
          itemCount++
        })
      )
    )

    // THEN: Multiple chunks
    expect(chunkCount).toBeGreaterThan(1)
    // AND: Total items <= limit
    expect(itemCount).toBeLessThanOrEqual(20)
  })
)
```

---

## Pattern 9: Multi-Service Integration Tests

### Scenario: Cross-Module Composition

**Specification:**

```gherkin
Scenario: Asset location uses Core identifiers
  Given I create a Site with id "site-01"
  And I create a Sector within the Site
  When I create an Asset with that location
  Then the Asset.siteId should match the Site.id
  And the location hierarchy should be valid
```

**Implementation:**

```typescript
// ams/v2/__tests__/integration.test.ts
it.effect('Location hierarchy composes correctly', () =>
  Effect.gen(function* () {
    const now = DateTime.unsafeNow()

    // GIVEN: Site
    const site = new AMS.Base.Site({
      id: 'site-01' as AMS.Core.SiteId,
      bfoClass: 'site' as AMS.Core.BfoSite,
      name: 'Main Warehouse',
      geoFrame: new AMS.Base.GeoFrame({
        crs: 'EPSG:4326',
        origin: new AMS.Base.GeoPoint({ lat: 37.7749, lon: -122.4194 }),
      }),
      createdAt: now as AMS.Core.CreatedAt,
      updatedAt: now as AMS.Core.UpdatedAt,
    })

    // AND: Sector within Site
    const sector = new AMS.Base.Sector({
      id: 'sector-A' as AMS.Core.SectorId,
      bfoClass: 'spatial_region' as AMS.Core.BfoSpatialRegion,
      siteId: site.id,
      // ... other fields
    })

    // WHEN: Create Asset with location
    const location = new AMS.Base.AssetLocation({
      siteId: site.id,
      sectorId: sector.id,
    })

    const asset = new AMS.Base.Asset({
      id: 'asset-001' as AMS.Core.AssetId,
      location,
      // ... other fields
    })

    // THEN: Asset.siteId matches Site.id
    expect(asset.siteId).toBe(site.id)
    // AND: Location hierarchy valid
    expect(asset.location.sectorId).toBe(sector.id)
    expect(sector.siteId).toBe(site.id)
  })
)
```

---

## Pattern 10: Skipping Tests (WIP Scenarios)

### When to Skip

- **Feature not yet implemented** - Use `it.effect.skip()`
- **Known failing test** - Document with TODO comment
- **Long-running tests** - Use `it.effect.only()` during development

```typescript
describe("ChannelService Data Flow", () => {
  // TODO: Data routing not yet wired
  it.effect.skip("data flows from inlet to outlet", () =>
    Effect.gen(function* () {
      // Step definitions here - will be implemented later
    }).pipe(Effect.provide(ChannelServiceLive))
  )

  it.effect.only("subscriber count increments", () =>
    Effect.gen(function* () {
      // Only this test runs when debugging
    }).pipe(Effect.provide(ChannelServiceLive))
  )
})
```

**Comment Convention:**

```typescript
// TODO: Data routing between inlet and outlet not yet wired
it.effect.skip("data flows from inlet to outlet", () => ...)

// FIXME: Flaky test - race condition in stream cleanup
it.effect.skip("stream completes after unsubscribe", () => ...)

// PERF: Slow test (5s) - run in @slow suite
it.effect.skip("10K movie indexing completes", () => ...)
```

---

## Pattern 11: Test Contexts (Shared State)

### Context Pattern (NOT Recommended for Effect)

Traditional BDD frameworks use "world" or "context" objects. **With Effect, use service state instead:**

```typescript
// ❌ BAD - Mutable context object
class TestContext {
  channelId?: ChannelId
  service?: ChannelService

  async givenRegisteredChannel() {
    this.channelId = await service.register(...)
  }
}

// ✅ GOOD - Effect.gen with lexical scope
it.effect("scenario with shared state", () =>
  Effect.gen(function* () {
    const service = yield* ChannelService

    // State lives in Effect.gen scope
    const channelId = yield* service.register(builder)

    // State flows naturally through yield*
    yield* service.open(channelId)
    const state = yield* service.getState(channelId)

    expect(state.value.status).toBe("open")
  }).pipe(Effect.provide(ChannelServiceLive))
)
```

---

## Pattern 12: Hypothesis-Driven Implementation

### TMNL-Specific: Testbed Validation

**Hypothesis Declaration:**

```typescript
// DataManagerTestbed.tsx
const HYPOTHESES: Hypothesis[] = [
  {
    id: 'H1',
    label: 'Search → Grid Flow',
    description: 'Search results flow correctly to AG-Grid rowData',
    status: 'pending',
  },
  {
    id: 'H2',
    label: 'Progressive Streaming',
    description: 'Stream emits results progressively (not all at once)',
    status: 'pending',
  },
]
```

**Hypothesis Validation:**

```typescript
// H1: Search → Grid Flow
useEffect(() => {
  if (
    results.length > 0 &&
    gridData.length > 0 &&
    hypotheses.find((h) => h.id === 'H1')?.status === 'testing'
  ) {
    updateHypothesis('H1', {
      status: 'passed',
      evidence: `${results.length} results → ${gridData.length} grid rows.`,
    })
  }
}, [results, gridData])

// H2: Progressive Streaming
useEffect(() => {
  if (itemCount > 0 && progressiveUpdateCount > 1) {
    updateHypothesis('H2', {
      status: 'passed',
      evidence: `${itemCount} results in ${progressiveUpdateCount} progressive updates`,
    })
  }
}, [itemCount, progressiveUpdateCount])
```

**Pattern:** Hypotheses are specifications. The testbed implementation IS the step definition.

---

## Anti-Patterns (Avoid These)

### ❌ Mocking Effect Services

```typescript
// BAD - Defeats Effect's dependency injection
const mockService = {
  open: vi.fn().mockResolvedValue(undefined),
  getState: vi.fn().mockResolvedValue({ status: 'open' }),
}

it.effect("uses mock", () =>
  Effect.gen(function* () {
    const state = yield* mockService.getState() // ❌ Not an Effect!
  })
)
```

```typescript
// GOOD - Provide test implementation via Layer
const TestChannelServiceLive = Layer.succeed(ChannelService, {
  open: (id) => Effect.succeed(undefined),
  getState: (id) => Effect.succeed(Option.some({ status: 'open' })),
  // ... other methods
})

it.effect("uses test service", () =>
  Effect.gen(function* () {
    const service = yield* ChannelService
    const state = yield* service.getState("ch-1")
    expect(Option.isSome(state)).toBe(true)
  }).pipe(Effect.provide(TestChannelServiceLive))
)
```

### ❌ Mixing Effect.runPromise in it.effect()

```typescript
// BAD - Breaks Effect composition
it.effect("searches for movies", () =>
  Effect.gen(function* () {
    const driver = yield* Effect.promise(async () => {
      return await Effect.runPromise(createFlexSearchDriver()) // ❌ Nested runPromise
    })
  })
)
```

```typescript
// GOOD - Use Effect all the way
it.effect("searches for movies", () =>
  Effect.gen(function* () {
    const driver = yield* createFlexSearchDriver() // ✅ Pure Effect
  })
)
```

### ❌ Testing Implementation Details

```typescript
// BAD - Couples to internal state
it.effect("driver uses FlexSearch instance", () =>
  Effect.gen(function* () {
    const driver = yield* createFlexSearchDriver()
    expect(driver.flexInstance).toBeDefined() // ❌ Implementation detail
  })
)
```

```typescript
// GOOD - Tests behavior
it.effect("driver indexes and searches", () =>
  Effect.gen(function* () {
    const driver = yield* createFlexSearchDriver()
    yield* driver.index(movies, { fields: ['title'] })
    const results = yield* driver.search("matrix", { limit: 10 })
      .pipe(Stream.runCollect)
    expect(Chunk.size(results)).toBeGreaterThan(0)
  })
)
```

---

## Summary: BDD Implementation Discipline

### Core Principles

1. **it.effect() for all Effect-based tests** - Never use regular `it()` for Effects
2. **Effect.provide() at test boundary** - Inject dependencies via Layers
3. **Effect.either() for error assertions** - Don't throw, pattern match on Either
4. **Verify outcomes, not function calls** - Assert on actual results, not mocks
5. **Shared fixtures as Effect.gen factories** - Not `beforeEach()` hooks

### TMNL-Specific Patterns

- **Hypothesis validation in testbeds** - Map H1/H2/H3 to useEffect assertions
- **Atom state verification** - Assert on atom values (`results.length > 0`)
- **Evidence tracking** - Include concrete metrics in hypothesis updates
- **Direct driver pattern** - Store drivers in useState, not atoms with Ref

### Canonical Test Files

- `src/lib/streams/__tests__/ChannelService.test.ts` - Effect.Service lifecycle
- `src/lib/ams/v2/__tests__/integration.test.ts` - Multi-service composition
- `src/components/testbed/DataManagerTestbed.tsx` - Hypothesis implementation

**When in doubt:** If your step definition has complex logic, the specification is wrong. Simplify the spec, then implement it directly in Effect.gen.
