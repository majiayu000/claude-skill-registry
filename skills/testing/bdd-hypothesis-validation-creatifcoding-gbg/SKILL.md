---
name: bdd-hypothesis-validation
description: |
  Using BDD to validate architectural hypotheses in TMNL.
  Covers H1/H2/H3 hypothesis patterns from testbeds, connecting specs to acceptance criteria,
  and damage reports for antipattern discovery. EDIN-aligned experimentation.
triggers:
  - "hypothesis"
  - "H1.*H2.*H3"
  - "validation.*hypothesis"
  - "testbed.*hypothesis"
  - "damage report"
---

# BDD Hypothesis Validation Patterns

## Philosophy: Hypotheses Are Executable Experiments

In TMNL, **hypotheses are BDD specifications for architectural experiments**. They are NOT:

- Wishful thinking ("I hope this works")
- Implementation plans ("We'll use FlexSearch")
- Vague goals ("Make search faster")

Hypotheses ARE:

- **Falsifiable claims** - "Search results flow to AG-Grid rowData with length > 0"
- **Measurable outcomes** - "Progressive streaming produces > 1 update, not a single batch"
- **Evidence-backed** - "Switched to linear driver, got 50 results in 12.3ms"
- **Living documentation** - Updated in real-time as code executes

**Canonical principle:** A hypothesis without concrete acceptance criteria is not a hypothesis. It's a hope.

---

## Canonical Sources

### Primary References

**TMNL Testbed Patterns:**
- `src/components/testbed/DataManagerTestbed.tsx` - H1-H5 hypothesis validation
- `src/components/testbed/shared/hypothesis.tsx` - Validation UI components
- `src/components/testbed/EffectAtomTestbed.tsx` - Damage report pattern
- `.edin/EFFECT_PATTERNS.md` - Effect-atom state patterns

**EDIN Methodology:**
- `CLAUDE.md` — EDIN phases (Experiment, Design, Implement, Negotiate)
- `.agents/index.md` — Session journal with hypothesis tracking

**Effect Testing:**
- `src/lib/streams/__tests__/ChannelService.test.ts` - Effect.gen assertions
- `src/lib/ams/v2/__tests__/integration.test.ts` - Multi-hypothesis integration

---

## Pattern 1: Hypothesis Declaration

### Hypothesis Structure

A hypothesis in TMNL has:

1. **ID** - Unique identifier (H1, H2, H3...) for tracking
2. **Label** - Short, memorable name (e.g., "Search → Grid Flow")
3. **Description** - Concrete, falsifiable claim
4. **Status** - `pending`, `testing`, `passed`, `failed`
5. **Evidence** - Concrete metrics that prove/disprove the claim

### Example: DataManager Hypotheses (EPOCH-0002)

```typescript
// src/components/testbed/DataManagerTestbed.tsx

interface Hypothesis {
  id: string
  label: string
  description: string
  status: 'pending' | 'testing' | 'passed' | 'failed'
  evidence?: string
}

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
  {
    id: 'H3',
    label: 'Stream-First DX',
    description: 'Effect Stream + Fiber cancellation works cleanly',
    status: 'pending',
  },
  {
    id: 'H4',
    label: 'Real-time Metrics',
    description: 'Throughput (items/sec) calculated in real-time',
    status: 'pending',
  },
  {
    id: 'H5',
    label: 'Driver Switching',
    description: 'Switching between flex/linear drivers is seamless',
    status: 'pending',
  },
]
```

---

## Pattern 2: Hypothesis Validation (Acceptance Criteria)

### H1: Search → Grid Flow

**Hypothesis:**

```
Search results flow correctly to AG-Grid rowData.
```

**Acceptance Criteria:**

1. Search returns `SearchResult<MovieItem>[]` with length > 0
2. `gridData` receives transformed results with length > 0
3. Grid renders rows matching `gridData.length`

**Implementation:**

```typescript
// DataManagerTestbed.tsx

// 1. Search execution
const handleSearch = useCallback(() => {
  const searchStream = currentDriver
    .search(query.trim(), { limit: 100, chunkSize: 5 })
    .pipe(withMinScore<MovieItem, unknown>(0.1))

  const program = searchStream.pipe(
    Stream.runForEach((result) =>
      Effect.sync(() => {
        itemCount++
        setResults((prev) => [...prev, result]) // Accumulate results
      })
    )
  )

  fiberRef.current = Effect.runFork(program)
}, [query, currentDriver])

// 2. Transform results → gridData
const gridData: DataGridRow[] = results.slice(0, 100).map((r) => ({
  id: r.item.id,
  name: r.item.title,
  value: Math.round(r.score * 100),
  status: r.score > 0.8 ? 'active' : 'pending',
}))

// 3. Validate hypothesis when data flows
useEffect(() => {
  // H1 passes when: we have results AND they flowed to gridData
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
// ❌ BAD - Tracks function call, not outcome
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

## Pattern 3: Progressive Validation (H2)

### H2: Progressive Streaming

**Hypothesis:**

```
Stream emits results progressively (not all at once).
```

**Acceptance Criteria:**

1. Search stream chunks results (chunkSize=5)
2. `progressiveUpdateCount` increments multiple times (> 1)
3. Each update appends to results, not replaces

**Implementation:**

```typescript
const handleSearch = useCallback(() => {
  let chunkCount = 0
  let itemCount = 0
  let progressiveUpdateCount = 0

  const searchStream = currentDriver
    .search(query.trim(), { limit: 100, chunkSize: 5 })
    .pipe(withMinScore<MovieItem, unknown>(0.1))

  const program = searchStream.pipe(
    Stream.tap(() =>
      Effect.sync(() => {
        chunkCount++
      })
    ),
    Stream.runForEach((result) =>
      Effect.sync(() => {
        itemCount++
        setResults((prev) => [...prev, result]) // ← Append, not replace

        // Track progressive updates
        progressiveUpdateCount++
      })
    ),
    Effect.ensuring(
      Effect.sync(() => {
        // H2: Progressive streaming verified if > 1 update
        if (itemCount > 0 && progressiveUpdateCount > 1) {
          updateHypothesis('H2', {
            status: 'passed',
            evidence: `${itemCount} results in ${progressiveUpdateCount} progressive updates`,
          })
        } else if (itemCount > 0) {
          updateHypothesis('H2', {
            status: 'failed',
            evidence: `${itemCount} results in single batch (not progressive)`,
          })
        }
      })
    )
  )

  fiberRef.current = Effect.runFork(program)
}, [query, currentDriver])
```

**Pattern:** Use `Stream.tap()` to track chunks, `Effect.ensuring()` to validate after stream completes.

---

## Pattern 4: Real-Time Metrics (H4)

### H4: Real-time Metrics

**Hypothesis:**

```
Throughput (items/sec) is calculated in real-time.
```

**Acceptance Criteria:**

1. `stats.ms` reflects elapsed time
2. `throughput = (items / ms) * 1000` is > 0 for successful searches
3. Metrics update during stream execution (not just at end)

**Implementation:**

```typescript
const handleSearch = useCallback(() => {
  const startTime = performance.now()
  let itemCount = 0

  const program = searchStream.pipe(
    Stream.runForEach((result) =>
      Effect.sync(() => {
        itemCount++
        setResults((prev) => [...prev, result])

        // Update metrics DURING stream (real-time)
        const elapsed = performance.now() - startTime
        setStats({
          chunks: chunkCount,
          items: itemCount,
          ms: Math.round(elapsed),
        })
      })
    ),
    Effect.ensuring(
      Effect.sync(() => {
        const finalMs = performance.now() - startTime

        // H4: Throughput verification
        const currentThroughput = itemCount > 0 && finalMs > 0
          ? (itemCount / finalMs) * 1000
          : 0

        if (currentThroughput > 0) {
          updateHypothesis('H4', {
            status: 'passed',
            evidence: `${currentThroughput.toFixed(0)} items/sec (${itemCount} items in ${finalMs.toFixed(1)}ms)`,
          })
        } else {
          updateHypothesis('H4', {
            status: 'failed',
            evidence: `No throughput measurable`,
          })
        }
      })
    )
  )

  fiberRef.current = Effect.runFork(program)
}, [query, currentDriver])
```

**Pattern:** Calculate metrics DURING stream (not just `Effect.ensuring`), validate concrete values (not just presence).

---

## Pattern 5: Driver Switching (H5)

### H5: Driver Switching

**Hypothesis:**

```
Switching between flex/linear drivers is seamless.
```

**Acceptance Criteria:**

1. `setActiveDriver()` toggles between drivers
2. Search with new driver returns results (length > 0)
3. No errors during switch or subsequent search

**Implementation:**

```typescript
const handleDriverSwitch = useCallback(() => {
  const newDriverType = activeDriver === 'flex' ? 'linear' : 'flex'
  const newDriverInstance = newDriverType === 'flex' ? flexDriver : linearDriver

  console.log('[Testbed] Switching to:', newDriverType)
  updateHypothesis('H5', { status: 'testing', evidence: `Switching to ${newDriverType}...` })

  if (!newDriverInstance) {
    updateHypothesis('H5', { status: 'failed', evidence: `${newDriverType} driver not available` })
    return
  }

  setActiveDriver(newDriverType)

  // Re-run search with new driver to verify
  if (query.trim()) {
    setResults([])
    setStatus('streaming')

    let itemCount = 0
    const startTime = performance.now()

    const searchStream = newDriverInstance
      .search(query.trim(), { limit: 50, chunkSize: 5 })
      .pipe(withMinScore<MovieItem, unknown>(0.1))

    const program = searchStream.pipe(
      Stream.runForEach((result) =>
        Effect.sync(() => {
          itemCount++
          setResults((prev) => [...prev, result])
        })
      ),
      Effect.ensuring(
        Effect.sync(() => {
          const ms = performance.now() - startTime
          setStatus('complete')

          // H5 passes if new driver returns results
          if (itemCount > 0) {
            updateHypothesis('H5', {
              status: 'passed',
              evidence: `Switched to ${newDriverType}, got ${itemCount} results in ${ms.toFixed(1)}ms`,
            })
          } else {
            updateHypothesis('H5', {
              status: 'failed',
              evidence: `Switched to ${newDriverType}, but search returned 0 results`,
            })
          }
        })
      )
    )

    Effect.runFork(program)
  } else {
    updateHypothesis('H5', {
      status: 'passed',
      evidence: `Switched to ${newDriverType}. Enter a query to verify search.`,
    })
  }
}, [activeDriver, flexDriver, linearDriver, query, updateHypothesis])
```

**Pattern:** Verify switch by executing actual operation (search), not just checking state.

---

## Pattern 6: Damage Reports (Antipattern Discovery)

### Purpose of Damage Reports

When hypotheses FAIL, document the **antipattern discovered** and the **fix applied**. This becomes living documentation.

### Example: DataManager Antipatterns (EPOCH-0002)

```typescript
// DataManagerTestbed.tsx

interface AntipatternEntry {
  id: string
  title: string
  severity: 'critical' | 'warning' | 'info'
  status: 'fixed' | 'active' | 'mitigated'
  problem: string
  codeExample?: { bad: string; good: string }
  fix: string
}

const DAMAGE_REPORT: AntipatternEntry[] = [
  {
    id: 'DM-001',
    title: 'Atom.runtime(Layer) + Stateful Services',
    severity: 'critical',
    status: 'fixed',
    problem: 'Atom.runtime(Layer) with services using Effect.Ref creates fresh state per operation. doIndex() populates Kernel#1, doSearch() creates Kernel#2 with empty state.',
    codeExample: {
      bad: `// ANTIPATTERN: Layer-per-operation isolation
const runtimeAtom = Atom.runtime(SearchKernel.Default)
const searchOps = {
  search: runtimeAtom.fn<Query>()((query, ctx) =>
    Effect.gen(function*() {
      const kernel = yield* SearchKernel // ← Fresh instance!
      return yield* kernel.search(query) // ← Empty driver!
    })
  )
}`,
      good: `// FIXED: Direct driver pattern with useState
const [driver, setDriver] = useState<SearchServiceImpl | null>(null)

useEffect(() => {
  const init = async () => {
    const flex = await Effect.runPromise(createFlexSearchDriver())
    await Effect.runPromise(flex.index(items, config))
    setDriver(flex) // ← Persists across operations
  }
  init()
}, [])`
    },
    fix: 'Bypass atom layer. Store driver instances in React useState. Use Effect.runPromise for initialization, Effect.runFork for streaming operations.',
  },
  {
    id: 'DM-002',
    title: 'Hypothesis Tracking: Function Call vs Outcome',
    severity: 'warning',
    status: 'fixed',
    problem: 'All 5 hypotheses marked "passed" despite grid showing 0 rows. Hypotheses tracked "function was called" (e.g., setGridData invoked) not "outcome achieved" (e.g., gridData.length > 0).',
    codeExample: {
      bad: `// ANTIPATTERN: Track function call, not outcome
useEffect(() => {
  if (gridData) {  // ← gridData exists (even if empty [])
    updateHypothesis('H1', 'passed')  // ← FALSE POSITIVE
  }
}, [gridData])`,
      good: `// FIXED: Verify actual outcome
useEffect(() => {
  if (gridData.length > 0) {  // ← Actually has results
    updateHypothesis('H1', 'passed', \`\${gridData.length} rows in grid\`)
  }
}, [gridData, updateHypothesis])`
    },
    fix: 'Track actual outcomes: gridData.length > 0, progressiveUpdateCount > 1, throughput > 0 && stats.items > 0, etc.',
  },
]
```

### Damage Report UI Component

```typescript
// src/components/testbed/shared/hypothesis.tsx

export interface DamageReportFinding {
  id: string
  severity: 'critical' | 'warning' | 'info' | 'resolved'
  title: string
  description?: string
  hypothesis?: string
}

export function DamageReport({ findings }: { findings: DamageReportFinding[] }) {
  const activeFindingsCount = findings.filter((f) => f.severity !== 'resolved').length

  return (
    <div className="border border-neutral-800 rounded-lg">
      <div className="px-4 py-3 bg-neutral-900/50 flex items-center justify-between">
        <span className="font-mono text-neutral-400 uppercase">DAMAGE REPORT</span>
        <span className={activeFindingsCount > 0 ? 'text-amber-400' : 'text-green-400'}>
          {activeFindingsCount > 0 ? `${activeFindingsCount} ACTIVE` : 'ALL CLEAR'}
        </span>
      </div>

      <div className="divide-y divide-neutral-800">
        {findings.map((finding) => (
          <div key={finding.id} className="p-3">
            <div className="flex items-center gap-2">
              <span className="font-mono">{finding.title}</span>
              {finding.hypothesis && (
                <span className="font-mono text-neutral-500">[{finding.hypothesis}]</span>
              )}
            </div>
            {finding.description && (
              <p className="text-neutral-400 mt-1">{finding.description}</p>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}
```

---

## Pattern 7: Hypothesis UI Components

### HypothesisBadge

```typescript
// src/components/testbed/shared/hypothesis.tsx

export type ValidationStatus = 'validated' | 'failed' | 'pending' | 'partial' | 'unknown'

export function HypothesisBadge({ id, status }: { id: string; status: ValidationStatus }) {
  const statusConfig = {
    validated: { bg: 'bg-green-900/30', text: 'text-green-400', icon: CheckCircle },
    failed: { bg: 'bg-red-900/30', text: 'text-red-400', icon: XCircle },
    pending: { bg: 'bg-amber-900/30', text: 'text-amber-400', icon: Clock },
    partial: { bg: 'bg-cyan-900/30', text: 'text-cyan-400', icon: AlertTriangle },
    unknown: { bg: 'bg-neutral-800/50', text: 'text-neutral-400', icon: Info },
  }

  const config = statusConfig[status]
  const Icon = config.icon

  return (
    <span className={`inline-flex items-center gap-1 px-2 py-0.5 ${config.bg} ${config.text}`}>
      <Icon size={10} />
      {id}
    </span>
  )
}
```

### HypothesisSection

```typescript
export function HypothesisSection({
  id,
  title,
  description,
  status,
  children,
}: {
  id: string
  title: string
  description: string
  status: ValidationStatus
  children: ReactNode
}) {
  const [isExpanded, setIsExpanded] = useState(true)

  return (
    <section className="border border-neutral-800 rounded-lg">
      <button
        onClick={() => setIsExpanded(!isExpanded)}
        className="w-full p-4 bg-neutral-900/50 flex items-center justify-between"
      >
        <div className="flex items-center gap-3">
          <HypothesisBadge id={id} status={status} compact />
          <div className="text-left">
            <h3 className="font-mono text-neutral-200">{title}</h3>
            <p className="text-neutral-500">{description}</p>
          </div>
        </div>
        <span className="text-neutral-500">{isExpanded ? '−' : '+'}</span>
      </button>
      {isExpanded && <div className="p-4 border-t border-neutral-800">{children}</div>}
    </section>
  )
}
```

### HypothesisCard (for Grid Display)

```typescript
function HypothesisCard({ hypothesis }: { hypothesis: Hypothesis }) {
  const statusColors = {
    pending: 'border-neutral-700 text-neutral-600',
    testing: 'border-amber-500/50 text-amber-500 animate-pulse',
    passed: 'border-emerald-500/50 text-emerald-500',
    failed: 'border-red-500/50 text-red-500',
  }

  const statusIcons = {
    pending: '○',
    testing: '◐',
    passed: '●',
    failed: '✕',
  }

  return (
    <div className={`border p-3 ${statusColors[hypothesis.status]}`}>
      <div className="flex items-start gap-2">
        <span className="font-mono">{statusIcons[hypothesis.status]}</span>
        <div className="flex-1">
          <div className="font-mono uppercase">{hypothesis.id}: {hypothesis.label}</div>
          <div className="font-mono text-neutral-500">{hypothesis.description}</div>
          {hypothesis.evidence && (
            <div className="font-mono text-neutral-600 mt-2 border-t pt-2">
              Evidence: {hypothesis.evidence}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
```

---

## Pattern 8: EDIN Integration (Experiment Phase)

### EDIN Phases and Hypothesis Flow

**EDIN Cycle:**

1. **Experiment** - Define hypotheses, validate assumptions
2. **Design** - Convert proven hypotheses into Operations
3. **Implement** - Execute Operations with bounded Tasks
4. **Negotiate** - Debrief, update Proposals, reallocate

**Hypothesis in Experiment Phase:**

```typescript
// .edin/experiments/EPOCH-0002-data-manager.md

## Experiment: DataManager Effect-Atom Integration

### Hypotheses

**H1: Search → Grid Flow**
- Claim: Search results flow correctly to AG-Grid rowData
- Acceptance: gridData.length > 0 after search completes
- Status: PASSED
- Evidence: 50 results → 50 grid rows in 12.3ms

**H2: Progressive Streaming**
- Claim: Stream emits results progressively (not all at once)
- Acceptance: progressiveUpdateCount > 1
- Status: PASSED
- Evidence: 50 results in 10 progressive updates

**H3: Stream-First DX**
- Claim: Effect Stream + Fiber cancellation works cleanly
- Acceptance: No errors, clean cancellation on unmount
- Status: PASSED
- Evidence: 5 searches with cancellations, 0 errors

**H4: Real-time Metrics**
- Claim: Throughput (items/sec) calculated in real-time
- Acceptance: stats.ms and throughput update during stream
- Status: PASSED
- Evidence: 4065 items/sec (50 items in 12.3ms)

**H5: Driver Switching**
- Claim: Switching between flex/linear drivers is seamless
- Acceptance: Search after switch returns results
- Status: PASSED
- Evidence: Switched to linear, got 50 results in 8.9ms

### Damage Report

**DM-001: Atom.runtime + Stateful Services (CRITICAL, FIXED)**
- Problem: Effect.Ref creates fresh state per operation
- Fix: Direct driver pattern with useState

**DM-002: Hypothesis Tracking (WARNING, FIXED)**
- Problem: Tracked function calls, not outcomes
- Fix: Verify gridData.length > 0, not just gridData existence

### Negotiation

All hypotheses PASSED. Transition to Design phase:
- Define Operations for DataManager integration
- Extract reusable patterns to .edin/EFFECT_PATTERNS.md
- Update Proposals queue with DataManager v2 features
```

---

## Pattern 9: Multi-Hypothesis Testbeds

### Organizing Multiple Hypotheses

```typescript
// Testbed with 5 hypotheses
export function DataManagerTestbed() {
  const [hypotheses, setHypotheses] = useState(HYPOTHESES)

  const updateHypothesis = useCallback((id: string, updates: Partial<Hypothesis>) => {
    setHypotheses((prev) =>
      prev.map((h) => (h.id === id ? { ...h, ...updates } : h))
    )
  }, [])

  return (
    <div>
      {/* Hypothesis Grid */}
      <section>
        <SectionLabel>Experiment Hypotheses</SectionLabel>
        <div className="grid grid-cols-5 gap-3">
          {hypotheses.map((h) => (
            <HypothesisCard key={h.id} hypothesis={h} />
          ))}
        </div>
      </section>

      {/* Search Interface (triggers H1, H2, H4) */}
      <section>
        <SectionLabel>Search Interface</SectionLabel>
        <input value={query} onChange={(e) => setQuery(e.target.value)} />
        <button onClick={handleSearch}>Search</button>
      </section>

      {/* Driver Toggle (triggers H5) */}
      <section>
        <button onClick={handleDriverSwitch}>
          Switch to {activeDriver === 'flex' ? 'linear' : 'flex'}
        </button>
      </section>

      {/* Results Grid (validates H1) */}
      <section>
        <DataGrid rowData={gridData} />
      </section>

      {/* Damage Report */}
      <section>
        <SectionLabel>Damage Report</SectionLabel>
        <DamageReportPanel findings={DAMAGE_REPORT} />
      </section>
    </div>
  )
}
```

---

## Pattern 10: Hypothesis-Driven Test Suites

### Mapping Hypotheses to it.effect() Tests

```typescript
// DataManager.test.ts (if we extract testbed to unit tests)

describe("DataManager Hypotheses (EPOCH-0002)", () => {
  describe("H1: Search → Grid Flow", () => {
    it.effect("search results flow to grid data transformation", () =>
      Effect.gen(function* () {
        const driver = yield* createFlexSearchDriver<MovieItem>()
        const movies = processMovies(100)
        yield* driver.index(movies, { fields: ['title'] })

        const results = yield* driver.search("matrix", { limit: 10 })
          .pipe(Stream.runCollect)

        const gridData = Chunk.toArray(results).map((r) => ({
          id: r.item.id,
          name: r.item.title,
          value: Math.round(r.score * 100),
        }))

        // H1 acceptance criteria
        expect(Chunk.size(results)).toBeGreaterThan(0)
        expect(gridData.length).toBeGreaterThan(0)
        expect(gridData.length).toBe(Chunk.size(results))
      })
    )
  })

  describe("H2: Progressive Streaming", () => {
    it.effect("stream emits multiple chunks", () =>
      Effect.gen(function* () {
        const driver = yield* createFlexSearchDriver<MovieItem>()
        const movies = processMovies(100)
        yield* driver.index(movies, { fields: ['title'] })

        let chunkCount = 0
        let itemCount = 0

        yield* driver.search("matrix", { limit: 20, chunkSize: 5 })
          .pipe(
            Stream.tap(() => Effect.sync(() => chunkCount++)),
            Stream.runForEach(() => Effect.sync(() => itemCount++))
          )

        // H2 acceptance criteria
        expect(chunkCount).toBeGreaterThan(1)
        expect(itemCount).toBeGreaterThan(0)
      })
    )
  })
})
```

---

## Anti-Patterns (Avoid These)

### ❌ Vague Hypotheses

```typescript
// BAD - Not falsifiable
{
  id: 'H1',
  label: 'Search works',
  description: 'Search should work correctly',
  status: 'pending',
}
```

```typescript
// GOOD - Concrete, measurable
{
  id: 'H1',
  label: 'Search → Grid Flow',
  description: 'Search results flow correctly to AG-Grid rowData with length > 0',
  status: 'pending',
}
```

### ❌ Tracking Function Calls Instead of Outcomes

```typescript
// BAD - False positive
useEffect(() => {
  if (gridData) {  // Empty [] is truthy!
    updateHypothesis('H1', 'passed')
  }
}, [gridData])
```

```typescript
// GOOD - Verify actual outcome
useEffect(() => {
  if (gridData.length > 0) {
    updateHypothesis('H1', 'passed', `${gridData.length} rows`)
  }
}, [gridData])
```

### ❌ Missing Evidence

```typescript
// BAD - No concrete metrics
updateHypothesis('H4', { status: 'passed' })
```

```typescript
// GOOD - Include evidence
updateHypothesis('H4', {
  status: 'passed',
  evidence: `4065 items/sec (50 items in 12.3ms)`,
})
```

### ❌ Hypothesis Without Acceptance Criteria

```typescript
// BAD - How do we know when it passes?
{
  id: 'H3',
  label: 'Effect Integration',
  description: 'Effect works with atoms',
  status: 'pending',
}
```

```typescript
// GOOD - Clear acceptance criteria
{
  id: 'H3',
  label: 'Stream-First DX',
  description: 'Effect Stream + Fiber cancellation works cleanly (0 errors, clean unmount)',
  status: 'pending',
}
```

---

## Summary: Hypothesis Validation Discipline

### Core Principles

1. **Hypotheses are falsifiable claims** - Not wishes, concrete outcomes
2. **Status transitions require evidence** - "passed" needs metrics, not just code execution
3. **Damage reports document antipatterns** - Failed hypotheses become learning
4. **UI components visualize validation** - HypothesisBadge, HypothesisCard, DamageReport
5. **EDIN integration** - Hypotheses in Experiment phase, Operations in Design

### TMNL-Specific Patterns

- **H1-H5 naming** - Sequential IDs for tracking across testbeds
- **Evidence strings** - Concrete metrics in updateHypothesis()
- **Damage report severity** - critical/warning/info for antipattern classification
- **Testbed UI** - Grid layout for hypotheses, collapsible damage reports

### Canonical Testbeds

- `src/components/testbed/DataManagerTestbed.tsx` - 5-hypothesis validation
- `src/components/testbed/EffectAtomTestbed.tsx` - Damage report pattern
- `src/components/testbed/shared/hypothesis.tsx` - UI components

**When in doubt:** If you cannot write concrete acceptance criteria with measurable outcomes, the hypothesis is not ready. Refine it until you can specify exactly what "passed" means.
