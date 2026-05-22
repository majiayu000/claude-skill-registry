---
name: bdd-specification-patterns
description: |
  Writing Given/When/Then specifications in Behavior-Driven Development.
  Covers feature files, scenario outlines, data tables, and mapping specs to implementations.
  BDD is a discipline - specifications ARE the requirements, not documentation of code.
triggers:
  - "write.*bdd"
  - "gherkin"
  - "given.*when.*then"
  - "feature.*scenario"
  - "specification"
---

# BDD Specification Patterns

## Philosophy: Specifications Are Executable Requirements

BDD is NOT "testing with different words." It is a **design discipline** where:

1. **Specifications precede implementation** - The `.feature` file is written BEFORE code exists
2. **Specifications ARE the requirements** - Not documentation, not tests dressed up with Given/When/Then
3. **Specifications drive architecture** - They reveal service boundaries, data flows, and invariants
4. **Specifications are living artifacts** - They evolve with the system and remain executable

**Canonical principle:** If you cannot express a requirement as a concrete scenario, you do not understand it well enough to implement it.

---

## Canonical Sources

### Primary References

**Effect-TS Testing Patterns:**
- `submodules/effect/packages/*/test/*.test.ts` - Effect service testing patterns
- `src/lib/streams/__tests__/ChannelService.test.ts` - Effect.gen + descriptive scenarios
- `src/lib/ams/v2/__tests__/integration.test.ts` - Cross-module composition scenarios

**TMNL Testbed Patterns:**
- `src/components/testbed/DataManagerTestbed.tsx` - Hypothesis-driven BDD
- `src/components/testbed/shared/hypothesis.tsx` - Hypothesis tracking components
- `.edin/EFFECT_PATTERNS.md` - Effect-atom state patterns

**EDIN Methodology:**
- `CLAUDE.md` — EDIN phases (Experiment, Design, Implement, Negotiate)

### External Resources

- [Cucumber Gherkin Reference](https://cucumber.io/docs/gherkin/reference/) - Syntax specification
- [BDD in Action (John Ferguson Smart)](https://www.manning.com/books/bdd-in-action) - BDD philosophy

---

## Pattern 1: Scenario Structure (Given/When/Then)

### Anatomy of a Scenario

```gherkin
Feature: Search Service Integration
  As a system operator
  I want search results to flow to AG-Grid
  So that I can visualize data in real-time

  Background:
    Given the search driver is initialized
    And 10000 movies are indexed

  Scenario: Basic search returns results
    Given I have indexed movie data
    When I search for "matrix"
    Then the results should contain "The Matrix"
    And the grid should display at least 1 row
    And the search status should be "complete"

  Scenario Outline: Driver switching preserves state
    Given I am using the <initial_driver> driver
    And I have searched for "<query>"
    When I switch to the <new_driver> driver
    And I search again for the same query
    Then the result count should be <expected_delta>% of the original

    Examples:
      | initial_driver | new_driver | query      | expected_delta |
      | flex           | linear     | "star wars"| 90-110         |
      | linear         | flex       | "godfather"| 90-110         |
```

### TMNL-Specific: Hypothesis-Driven Scenarios

TMNL testbeds use **hypothesis validation** as executable specifications:

```gherkin
Feature: DataManager Effect-Atom Integration (EPOCH-0002)

  Hypothesis: H1 - Search results flow to AG-Grid
    Given the DataManager service is initialized
    And the FlexSearch driver is indexed with 10K movies
    When I execute a search for "matrix"
    Then resultsAtom should contain SearchResult[]
    And gridData should have length > 0
    And H1 status should transition to "passed"

  Hypothesis: H2 - Progressive streaming updates
    Given a search stream with chunkSize=5
    When I search for "star"
    Then the grid should receive multiple progressive updates
    And progressiveUpdateCount should be > 1
    And each update should append to results (not replace)

  Hypothesis: H5 - Driver switching is seamless
    Given I have results from FlexSearch driver
    When I switch to Linear driver
    And I re-run the search
    Then the new results should be non-empty
    And the search should complete without errors
    And H5 status should transition to "passed"
```

**Mapping to Code:**

```tsx
// DataManagerTestbed.tsx implements these scenarios
const HYPOTHESES: Hypothesis[] = [
  {
    id: 'H1',
    label: 'Search → Grid Flow',
    description: 'Search results flow correctly to AG-Grid rowData',
    status: 'pending',
  },
  // ...
]

// Scenario execution
useEffect(() => {
  if (results.length > 0 && gridData.length > 0) {
    updateHypothesis('H1', {
      status: 'passed',
      evidence: `${results.length} results → ${gridData.length} grid rows`,
    })
  }
}, [results, gridData])
```

---

## Pattern 2: Data Tables (Parameterized Scenarios)

### When to Use Data Tables

- **Multiple inputs/outputs** - Testing search with various queries
- **State transitions** - Channel lifecycle states
- **Configuration variants** - Slider behaviors with different curves

### Example: Search Query Variants

```gherkin
Scenario: Search handles various query patterns
  Given the search index contains 10000 movies
  When I execute searches with the following queries:
    | query          | min_results | max_results |
    | "matrix"       | 5           | 50          |
    | "star wars"    | 10          | 100         |
    | "godfather"    | 3           | 30          |
    | "nonexistent"  | 0           | 0           |
  Then each search should return within the expected range
  And search metrics should reflect accurate throughput
```

### Example: Channel Lifecycle (Effect Service)

```gherkin
Scenario: Channel state transitions
  Given the ChannelService is initialized
  When I perform the following operations:
    | operation      | channel_id | expected_status | expected_error |
    | register       | ch-1       | idle            | none           |
    | open           | ch-1       | open            | none           |
    | open           | ch-1       | open            | none           | # idempotent
    | close          | ch-1       | closed          | none           |
    | open           | missing    | -               | CHANNEL_NOT_FOUND |
  Then each operation should match the expected outcome
```

**Implementation Pattern:**

```typescript
// ChannelService.test.ts
describe("ChannelService Lifecycle", () => {
  const scenarios = [
    { op: 'open', id: 'ch-1', expectedStatus: 'open', expectedError: null },
    { op: 'open', id: 'missing', expectedStatus: null, expectedError: 'CHANNEL_NOT_FOUND' },
    // ...
  ]

  scenarios.forEach(({ op, id, expectedStatus, expectedError }) => {
    it.effect(`${op}(${id}) → ${expectedStatus || expectedError}`, () =>
      Effect.gen(function* () {
        const service = yield* ChannelService
        const result = yield* service[op](id as ChannelId).pipe(Effect.either)

        if (expectedError) {
          expect(result._tag).toBe("Left")
          expect(result.left.code).toBe(expectedError)
        } else {
          const state = yield* service.getState(id)
          expect(state.value.status).toBe(expectedStatus)
        }
      }).pipe(Effect.provide(ChannelServiceLive))
    )
  })
})
```

---

## Pattern 3: Scenario Outlines (Parameterized Examples)

### When to Use Scenario Outlines

- **Same behavior, different data** - Testing search with multiple queries
- **Edge cases** - Boundary conditions (min, max, zero, negative)
- **Cross-product testing** - Driver combinations, config variants

### Example: Slider Behavior Variants

```gherkin
Scenario Outline: Slider behaviors map values correctly
  Given a slider with <behavior> behavior
  And min=<min>, max=<max>
  When the normalized value is <normalized>
  Then the display value should be <display>
  And the internal calculation should use <formula>

  Examples: Linear Behavior
    | behavior | min | max  | normalized | display | formula        |
    | linear   | 0   | 100  | 0.5        | 50      | lerp(0,100,t)  |
    | linear   | -10 | 10   | 0.0        | -10     | lerp(-10,10,t) |

  Examples: Decibel Behavior
    | behavior | min  | max | normalized | display | formula           |
    | decibel  | -48  | 12  | 0.5        | ~-18    | 20*log10(t)       |
    | decibel  | -48  | 12  | 1.0        | 12      | max               |

  Examples: Logarithmic Behavior
    | behavior     | min | max   | normalized | display | formula         |
    | logarithmic  | 20  | 20000 | 0.5        | ~632    | exp(lerp(ln...)) |
```

**Implementation:**

```typescript
// SliderBehavior.test.ts
const behaviorCases = [
  { behavior: LinearBehavior, min: 0, max: 100, normalized: 0.5, expected: 50 },
  { behavior: DecibelBehavior, min: -48, max: 12, normalized: 0.5, expected: -18 },
  // ...
]

behaviorCases.forEach(({ behavior, min, max, normalized, expected }) => {
  it(`${behavior.name}: toDisplay(${normalized}) = ${expected}`, () => {
    const display = behavior.toDisplay(normalized, min, max)
    expect(display).toBeCloseTo(expected, 1)
  })
})
```

---

## Pattern 4: Background (Shared Setup)

### When to Use Background

- **Common preconditions** - All scenarios need indexed data
- **Service initialization** - Effect runtime setup
- **State reset** - Clean slate for each scenario

```gherkin
Feature: Effect-Atom Search Integration

  Background:
    Given the Effect runtime is initialized with:
      | service        | layer                  |
      | IdGenerator    | IdGenerator.Default    |
      | SearchKernel   | SearchKernel.Default   |
      | DataManager    | DataManager.Default    |
    And the FlexSearch driver is created
    And 10000 movies are indexed with fields:
      | field   |
      | title   |
      | cast    |
      | genres  |
      | extract |

  Scenario: Search with empty query
    When I search for ""
    Then the results should be empty
    And no error should occur

  Scenario: Search with valid query
    When I search for "matrix"
    Then the results should contain matches
```

**Implementation:**

```typescript
describe("Effect-Atom Search Integration", () => {
  let driver: SearchServiceImpl<MovieItem>
  let movies: MovieItem[]

  beforeEach(async () => {
    // Background setup
    movies = processMovies(10000)
    driver = await Effect.runPromise(createFlexSearchDriver<MovieItem>())
    await Effect.runPromise(driver.index(movies, {
      fields: ['title', 'cast', 'genres', 'extract'],
      store: true,
    }))
  })

  it.effect("search with empty query returns empty", () =>
    Effect.gen(function* () {
      const results = yield* driver.search("", { limit: 10 })
        .pipe(Stream.runCollect)
      expect(Chunk.toArray(results)).toEqual([])
    })
  )
})
```

---

## Pattern 5: Tagging Scenarios (Organizing Execution)

### Tag Semantics

```gherkin
@smoke @critical
Scenario: Core search flow works end-to-end
  Given the search service is initialized
  When I search for "matrix"
  Then results should appear in the grid

@integration @slow
Scenario: 10K movie indexing completes
  Given I have 10000 raw movie records
  When I index them with FlexSearch
  Then indexing should complete in < 5 seconds

@hypothesis:H1
Scenario: Search → Grid flow validation
  # Maps to HYPOTHESES array in testbed
  ...

@wip @skip
Scenario: Fuzzy search with Levenshtein distance
  # Not yet implemented - work in progress
  ...
```

**Mapping to Test Execution:**

```typescript
// vitest.config.ts
export default defineConfig({
  test: {
    include: ['**/__tests__/**/*.test.ts'],
    exclude: ['**/*.skip.test.ts', '**/@wip/**'],
  },
})

// Test file
describe("Search Service", () => {
  describe("@smoke", () => {
    it.effect("core search flow", () => /* ... */)
  })

  describe("@integration @slow", () => {
    it.effect("10K indexing", () => /* ... */)
  })

  describe.skip("@wip", () => {
    it.effect("fuzzy search", () => /* ... */)
  })
})
```

---

## Pattern 6: Mapping Specifications to Effect Services

### Gherkin → Effect.gen Translation

**Specification:**

```gherkin
Scenario: Channel opens successfully
  Given I have registered a channel "test-channel"
  When I open the channel
  Then the channel status should be "open"
  And the openedAt timestamp should be set
  And a ChannelOpened event should be emitted
```

**Implementation:**

```typescript
// ChannelService.test.ts
describe("ChannelService Lifecycle", () => {
  it.effect("open() transitions to open state", () =>
    Effect.gen(function* () {
      // Given: registered channel
      const service = yield* ChannelService
      const builder = testBuilder()
      const channelId = yield* service.register(builder)

      // When: open the channel
      yield* service.open(channelId)

      // Then: verify state
      const state = yield* service.getState(channelId)
      expect(Option.isSome(state)).toBe(true)
      if (Option.isSome(state)) {
        expect(state.value.status).toBe("open")
        expect(state.value.openedAt).toBeGreaterThan(0)
      }

      // And: verify event
      const eventQueue = yield* service.subscribeEvents()
      const event = yield* Queue.take(eventQueue)
      expect(event._tag).toBe("ChannelOpened")
    }).pipe(Effect.provide(ChannelServiceLive))
  )
})
```

**Key Principles:**

1. **Given** → Service initialization + preconditions
2. **When** → Service method invocation
3. **Then** → Assertions on returned values
4. **And** → Additional assertions (state, events, side effects)

---

## Pattern 7: Anti-Patterns (What NOT to Do)

### ❌ Vague Specifications

```gherkin
# BAD - No concrete assertions
Scenario: Search works
  When I search
  Then it should work
```

```gherkin
# GOOD - Concrete, verifiable
Scenario: Search returns top 10 results by score
  Given 100 indexed movies
  When I search for "matrix" with limit=10
  Then the results should have length 10
  And the first result should have score > 0.8
  And results should be sorted descending by score
```

### ❌ Implementation Details in Specs

```gherkin
# BAD - Coupled to implementation
Scenario: Search uses FlexSearch driver
  Given the FlexSearchDriver is instantiated
  When I call driver.search() with query="matrix"
  Then the driver should invoke index.search()
  And return SearchResult<MovieItem>[]
```

```gherkin
# GOOD - Describes behavior, not implementation
Scenario: Search returns fuzzy matches
  Given indexed movies include "The Matrix"
  When I search for "matix" (typo)
  Then "The Matrix" should appear in results
  And the match score should reflect edit distance
```

### ❌ Testing Framework Leakage

```gherkin
# BAD - Mentions Effect.gen, expect(), etc.
Scenario: Effect.gen yields search results
  When I yield* searchKernel.search(query)
  Then expect(results).toHaveLength(10)
```

```gherkin
# GOOD - Framework-agnostic behavior
Scenario: Search yields exactly 10 results
  When I search with limit=10
  Then exactly 10 results are returned
```

### ❌ Hypothesis Tracking Without Verification

```gherkin
# BAD - Tracks function call, not outcome
Scenario: H1 validates search flow
  When I call doSearch()
  Then setGridData should have been called
  And H1 status should be "passed"
```

```gherkin
# GOOD - Verifies actual outcome
Scenario: H1 validates search → grid data flow
  When I search for "matrix"
  Then the grid should contain > 0 rows
  And each row should have id, name, value, status fields
  And H1 status should be "passed" with evidence
```

---

## Pattern 8: Acceptance Criteria Mapping

### From User Story to Specification

**User Story:**

```
As a system operator
I want to switch between search drivers (FlexSearch, Linear)
So that I can compare results and performance
```

**Acceptance Criteria:**

```gherkin
Feature: Driver Switching

  Scenario: Switch from FlexSearch to Linear
    Given I am using FlexSearch driver
    And I have searched for "matrix"
    And I have 10 results
    When I switch to Linear driver
    And I search for "matrix" again
    Then I should receive new results
    And the new results should be non-empty
    And the search should complete without errors

  Scenario: Driver state is isolated
    Given I have indexed 1000 movies in FlexSearch
    And I have indexed 500 movies in Linear
    When I switch between drivers
    Then each driver should retain its own index
    And search results should reflect the correct index size
```

**Implementation (from DataManagerTestbed.tsx):**

```typescript
const handleDriverSwitch = useCallback(() => {
  const newDriverType = activeDriver === 'flex' ? 'linear' : 'flex'
  const newDriverInstance = newDriverType === 'flex' ? flexDriver : linearDriver

  // Acceptance: Switch should be seamless
  setActiveDriver(newDriverType)

  // Acceptance: Search should work with new driver
  if (query.trim()) {
    const program = newDriverInstance
      .search(query.trim(), { limit: 50 })
      .pipe(
        Stream.runForEach(result => Effect.sync(() => {
          setResults(prev => [...prev, result])
        })),
        Effect.ensuring(Effect.sync(() => {
          // Acceptance: Results should be non-empty
          if (itemCount > 0) {
            updateHypothesis('H5', {
              status: 'passed',
              evidence: `Switched to ${newDriverType}, got ${itemCount} results`,
            })
          }
        }))
      )
    Effect.runFork(program)
  }
}, [activeDriver, flexDriver, linearDriver, query])
```

---

## Summary: BDD Specification Discipline

### Core Principles

1. **Specifications precede implementation** - Write `.feature` files BEFORE code
2. **Specifications are executable** - They run as tests via step definitions
3. **Specifications are living requirements** - Update them as the system evolves
4. **Specifications reveal architecture** - Service boundaries emerge from scenarios

### TMNL-Specific Patterns

- **Hypothesis-driven scenarios** - Map to testbed validation (H1, H2, H3...)
- **Effect.gen step definitions** - Use `it.effect()` for Effect-based assertions
- **Atom state verification** - Assert on atom values, not implementation details
- **Evidence tracking** - Include concrete evidence strings in hypothesis updates

### Canonical References

- `src/lib/streams/__tests__/ChannelService.test.ts` - Effect service BDD patterns
- `src/components/testbed/DataManagerTestbed.tsx` - Hypothesis validation
- `.edin/EFFECT_PATTERNS.md` - Effect-atom state patterns

**When in doubt:** If you cannot write a concrete, verifiable scenario, you do not understand the requirement. Go back to the specification phase.
