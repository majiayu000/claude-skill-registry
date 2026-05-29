---
name: streams-playground-system
description: Unified stress-test scenario engine for TMNL. Invoke when implementing real-time data streams, payload generators, throughput monitoring, or circuit breaker patterns. Provides EmissionEngine, reservoir sampling, and D3 visualizations.
model_invoked: true
triggers:
  - "streams"
  - "StreamsPlayground"
  - "EmissionEngine"
  - "payload generator"
  - "SenML"
  - "OPC-UA"
  - "Prometheus"
  - "throughput"
  - "circuit breaker"
  - "reservoir sampling"
  - "RawEventsPanel"
  - "real-time data"
---

# Streams Playground System for TMNL

## Overview

A unified stress-test scenario engine for validating real-time data architectures:
- **EmissionEngine** — Hybrid rAF + Effect Queue for high-frequency event emission
- **Payload Generators** — SenML, OPC-UA, Prometheus schema-compliant payloads
- **Reservoir Sampling** — Fixed-size latency sampling for high-throughput metrics
- **D3 Visualizations** — Line charts, histograms, gauges, topology graphs
- **Circuit Breaker** — Effect-based failure isolation with configurable thresholds

## Canonical Sources

### TMNL Implementations

| File | Purpose | Pattern |
|------|---------|---------|
| `src/lib/streams/playground/EmissionEngine.ts` | Hybrid emission scheduler | rAF + Effect Queue |
| `src/lib/streams/playground/timing.ts` | High-resolution timing utilities | performance.now() |
| `src/lib/streams/playground/scenarios/` | Scenario definitions | Tagged structs |
| `src/lib/streams/playground/scenarios/generators/` | Protocol payloads | SenML/OPC-UA/Prometheus |
| `src/lib/streams/playground/atoms/index.ts` | Reactive state | Atom-as-State |
| `src/components/playground/streams/StreamsPlayground.tsx` | Main component | Panel composition |
| `src/components/playground/streams/panels/` | Metric panels | RawEvents, Throughput, etc. |
| `src/components/playground/streams/viz/` | D3 visualizations | Line, Histogram, Gauge |

### Testbeds

- **StreamsPlayground**: `/testbed/streams-playground` — Full scenario engine demonstration

---

## Pattern 1: EmissionEngine — HYBRID rAF + EFFECT QUEUE

**When:** Emitting high-frequency events (10k+ events/sec) with frame-synchronized batching.

The EmissionEngine uses a hybrid approach:
1. **rAF loop** for frame-synchronized state updates (60 FPS ceiling)
2. **Effect Queue** for backpressure-aware event dispatch
3. **Reservoir sampling** for latency metrics without memory explosion

```typescript
import { Effect, Queue } from 'effect'

interface EmissionEngine {
  readonly start: Effect.Effect<void>
  readonly stop: Effect.Effect<void>
  readonly emit: (payload: unknown) => Effect.Effect<void>
  readonly getMetrics: Effect.Effect<EmissionMetrics>
}

// Hybrid scheduler
const createEngine = Effect.gen(function*() {
  const queue = yield* Queue.bounded<Event>(10_000)
  let rafId: number | null = null
  let lastFrameTime = performance.now()

  const frameLoop = () => {
    const now = performance.now()
    const delta = now - lastFrameTime
    lastFrameTime = now

    // Batch process queue items per frame
    Effect.runPromise(
      Queue.takeBetween(queue, 1, 100).pipe(
        Effect.flatMap(events => processBatch(events, delta))
      )
    )

    rafId = requestAnimationFrame(frameLoop)
  }

  return {
    start: Effect.sync(() => { rafId = requestAnimationFrame(frameLoop) }),
    stop: Effect.sync(() => { if (rafId) cancelAnimationFrame(rafId) }),
    emit: (payload) => Queue.offer(queue, payload),
  }
})
```

**Key Pattern**: rAF provides frame budget (16.67ms), Effect Queue provides backpressure.

**TMNL Location**: `src/lib/streams/playground/EmissionEngine.ts`

---

## Pattern 2: Reservoir Sampling — FIXED-SIZE LATENCY METRICS

**When:** Collecting latency samples from millions of events without memory exhaustion.

Reservoir sampling maintains a fixed-size sample (e.g., 1000 items) with uniform probability:

```typescript
const RESERVOIR_SIZE = 1000
let latencyReservoir: number[] = new Array(RESERVOIR_SIZE)
let latencySampleCount = 0

function reservoirSample(value: number): void {
  if (latencySampleCount < RESERVOIR_SIZE) {
    // Fill phase: accept all samples
    latencyReservoir[latencySampleCount] = value
  } else {
    // Replacement phase: probabilistic inclusion
    const j = Math.floor(Math.random() * (latencySampleCount + 1))
    if (j < RESERVOIR_SIZE) {
      latencyReservoir[j] = value
    }
  }
  latencySampleCount++
}

// Compute percentiles from reservoir
function getPercentile(p: number): number {
  const sorted = [...latencyReservoir].slice(0, Math.min(latencySampleCount, RESERVOIR_SIZE)).sort((a, b) => a - b)
  const idx = Math.floor(sorted.length * (p / 100))
  return sorted[idx]
}
```

**Statistical Property**: Each item has equal probability (k/n) of being in the final sample.

**TMNL Location**: `src/lib/streams/playground/timing.ts`

---

## Pattern 3: Payload Generators — PROTOCOL-COMPLIANT SCHEMAS

**When:** Generating test payloads that match real-world IoT/telemetry protocols.

### SenML (Sensor Measurement Lists)

RFC 8428 compliant sensor payloads:

```typescript
import { Schema } from 'effect'

const SenMLRecord = Schema.Struct({
  bn: Schema.optional(Schema.String),  // Base Name
  bt: Schema.optional(Schema.Number),  // Base Time
  bu: Schema.optional(Schema.String),  // Base Unit
  n: Schema.String,                     // Name
  u: Schema.optional(Schema.String),   // Unit
  v: Schema.optional(Schema.Number),   // Value
  vs: Schema.optional(Schema.String),  // String Value
  vb: Schema.optional(Schema.Boolean), // Boolean Value
  t: Schema.optional(Schema.Number),   // Time
})

const generateSenML = (sensorId: string, value: number): SenMLRecord => ({
  n: `urn:dev:mac:${sensorId}`,
  u: 'Cel',
  v: value,
  t: Date.now() / 1000,
})
```

### OPC-UA (Open Platform Communications)

Industrial automation protocol payloads:

```typescript
const OPCUADataValue = Schema.Struct({
  nodeId: Schema.String,           // e.g., "ns=2;s=Temperature"
  value: Schema.Unknown,
  statusCode: Schema.Number,       // 0 = Good
  sourceTimestamp: Schema.String,  // ISO 8601
  serverTimestamp: Schema.String,
})

const generateOPCUA = (nodeId: string, value: number) => ({
  nodeId,
  value,
  statusCode: 0,
  sourceTimestamp: new Date().toISOString(),
  serverTimestamp: new Date().toISOString(),
})
```

### Prometheus

Time-series metrics format:

```typescript
const PrometheusMetric = Schema.Struct({
  name: Schema.String,
  labels: Schema.Record({ key: Schema.String, value: Schema.String }),
  value: Schema.Number,
  timestamp: Schema.Number,  // Unix epoch ms
})

const generatePrometheus = (name: string, value: number, labels: Record<string, string>) => ({
  name,
  labels,
  value,
  timestamp: Date.now(),
})
```

**TMNL Location**: `src/lib/streams/playground/scenarios/generators/`

---

## Pattern 4: Scenario Config — DECLARATIVE STRESS TESTS

**When:** Defining reproducible test scenarios with consistent parameters.

```typescript
import { Schema } from 'effect'

const ScenarioConfig = Schema.Struct({
  _tag: Schema.Literal('ScenarioConfig'),
  name: Schema.String,
  description: Schema.String,

  // Emission parameters
  targetEps: Schema.Number,          // Events per second
  burstSize: Schema.Number,          // Batch size
  duration: Schema.Number,           // Test duration (ms)

  // Payload configuration
  payloadType: Schema.Literal('senml', 'opcua', 'prometheus', 'custom'),
  payloadSizeBytes: Schema.Number,

  // Failure injection
  errorRate: Schema.Number,          // 0-1 probability
  latencySpike: Schema.optional(Schema.Struct({
    probability: Schema.Number,
    durationMs: Schema.Number,
  })),

  // Circuit breaker
  circuitBreaker: Schema.optional(Schema.Struct({
    failureThreshold: Schema.Number,
    resetTimeoutMs: Schema.Number,
  })),
})

// Preset scenarios
const SCENARIOS = {
  warmup: {
    _tag: 'ScenarioConfig' as const,
    name: 'Warmup',
    targetEps: 100,
    burstSize: 10,
    duration: 5000,
    payloadType: 'senml' as const,
    payloadSizeBytes: 128,
    errorRate: 0,
  },
  stressTest: {
    _tag: 'ScenarioConfig' as const,
    name: 'Stress Test',
    targetEps: 10_000,
    burstSize: 100,
    duration: 30_000,
    payloadType: 'senml' as const,
    payloadSizeBytes: 256,
    errorRate: 0.001,
    circuitBreaker: {
      failureThreshold: 50,
      resetTimeoutMs: 5000,
    },
  },
}
```

**TMNL Location**: `src/lib/streams/playground/scenarios/types.ts`

---

## Pattern 5: RawEventsPanel — SCHEMA-DERIVED COLUMNS

**When:** Displaying raw event data in AG-Grid with automatic column generation.

```tsx
import { AgGridReact } from 'ag-grid-react'
import { Schema } from 'effect'

// Derive column definitions from Schema
function schemaToColumnDefs<A>(schema: Schema.Schema<A>): ColDef[] {
  const ast = schema.ast
  // Walk AST to extract field names and types
  if (ast._tag === 'TypeLiteral') {
    return ast.propertySignatures.map(prop => ({
      field: prop.name,
      headerName: formatHeader(prop.name),
      valueFormatter: getFormatterForType(prop.type),
    }))
  }
  return []
}

function RawEventsPanel({ events, schema }: Props) {
  const columnDefs = useMemo(() => schemaToColumnDefs(schema), [schema])

  return (
    <AgGridReact
      rowData={events}
      columnDefs={columnDefs}
      getRowId={(params) => params.data.id}
      animateRows={false}  // Performance: disable for high-frequency updates
      suppressCellFlash={true}
    />
  )
}
```

**Key Pattern**: Schema → ColDef transformation enables type-safe, auto-generated grids.

**TMNL Location**: `src/components/playground/streams/panels/RawEventsPanel.tsx`

---

## Pattern 6: ThroughputPanel — REAL-TIME METRICS

**When:** Displaying events/second, bytes/second, and moving averages.

```tsx
import { useAtomValue } from '@effect-rx/rx-react'
import { D3LineChart } from '../viz/D3LineChart'

function ThroughputPanel() {
  const metrics = useAtomValue(throughputMetricsAtom)

  return (
    <div className="grid grid-cols-3 gap-4">
      <MetricCard
        label="Events/sec"
        value={metrics.eventsPerSecond}
        trend={metrics.epsTrend}
      />
      <MetricCard
        label="Bytes/sec"
        value={formatBytes(metrics.bytesPerSecond)}
        trend={metrics.bpsTrend}
      />
      <MetricCard
        label="Avg Latency"
        value={`${metrics.avgLatencyMs.toFixed(2)}ms`}
        trend={metrics.latencyTrend}
      />

      <div className="col-span-3">
        <D3LineChart
          data={metrics.history}
          xAccessor={d => d.timestamp}
          yAccessor={d => d.eps}
          height={120}
        />
      </div>
    </div>
  )
}
```

**TMNL Location**: `src/components/playground/streams/panels/ThroughputPanel.tsx`

---

## Pattern 7: CircuitBreakerPanel — FAILURE ISOLATION

**When:** Implementing resilient event processing with automatic failure detection.

```typescript
import { Effect, Schedule, Duration } from 'effect'

type CircuitState = 'closed' | 'open' | 'half-open'

interface CircuitBreaker {
  state: CircuitState
  failures: number
  successesSinceHalfOpen: number
  lastFailure: number | null
}

const createCircuitBreaker = (config: {
  failureThreshold: number
  resetTimeout: Duration.Duration
  successThreshold: number
}) => {
  let state: CircuitBreaker = {
    state: 'closed',
    failures: 0,
    successesSinceHalfOpen: 0,
    lastFailure: null,
  }

  return {
    execute: <A>(effect: Effect.Effect<A>): Effect.Effect<A> =>
      Effect.gen(function*() {
        if (state.state === 'open') {
          const elapsed = Date.now() - (state.lastFailure ?? 0)
          if (elapsed > Duration.toMillis(config.resetTimeout)) {
            state = { ...state, state: 'half-open' }
          } else {
            return yield* Effect.fail(new CircuitOpenError())
          }
        }

        const result = yield* effect.pipe(
          Effect.tapError(() => {
            state = {
              ...state,
              failures: state.failures + 1,
              lastFailure: Date.now(),
            }
            if (state.failures >= config.failureThreshold) {
              state = { ...state, state: 'open' }
            }
          }),
          Effect.tap(() => {
            if (state.state === 'half-open') {
              state = {
                ...state,
                successesSinceHalfOpen: state.successesSinceHalfOpen + 1,
              }
              if (state.successesSinceHalfOpen >= config.successThreshold) {
                state = { ...state, state: 'closed', failures: 0 }
              }
            }
          })
        )

        return result
      }),

    getState: () => state,
  }
}
```

**TMNL Location**: `src/components/playground/streams/panels/CircuitBreakerPanel.tsx`

---

## Pattern 8: D3 Visualizations — COMPOSABLE CHARTS

**When:** Rendering real-time metrics with D3.js.

### Line Chart

```tsx
import * as d3 from 'd3'
import { useRef, useEffect } from 'react'

function D3LineChart<T>({
  data,
  xAccessor,
  yAccessor,
  width = 300,
  height = 120,
}: Props<T>) {
  const svgRef = useRef<SVGSVGElement>(null)

  useEffect(() => {
    if (!svgRef.current || !data.length) return

    const svg = d3.select(svgRef.current)
    const margin = { top: 10, right: 10, bottom: 20, left: 40 }
    const innerWidth = width - margin.left - margin.right
    const innerHeight = height - margin.top - margin.bottom

    const xScale = d3.scaleTime()
      .domain(d3.extent(data, xAccessor) as [Date, Date])
      .range([0, innerWidth])

    const yScale = d3.scaleLinear()
      .domain([0, d3.max(data, yAccessor) ?? 0])
      .range([innerHeight, 0])

    const line = d3.line<T>()
      .x(d => xScale(xAccessor(d)))
      .y(d => yScale(yAccessor(d)))
      .curve(d3.curveMonotoneX)

    svg.select('.line')
      .datum(data)
      .attr('d', line)
  }, [data, xAccessor, yAccessor, width, height])

  return (
    <svg ref={svgRef} width={width} height={height}>
      <g transform={`translate(${margin.left},${margin.top})`}>
        <path className="line" fill="none" stroke="var(--tmnl-cyan)" strokeWidth={2} />
      </g>
    </svg>
  )
}
```

**TMNL Location**: `src/components/playground/streams/viz/D3LineChart.tsx`

---

## Pattern 9: High-Resolution Timing — PERFORMANCE.NOW()

**When:** Measuring sub-millisecond latencies for accurate metrics.

```typescript
// Use performance.now() for high-resolution timestamps
const measureLatency = <A>(effect: Effect.Effect<A>): Effect.Effect<{ result: A; latencyMs: number }> =>
  Effect.gen(function*() {
    const start = performance.now()
    const result = yield* effect
    const end = performance.now()
    return { result, latencyMs: end - start }
  })

// Batch timing for aggregate metrics
interface TimingBatch {
  startTime: number
  samples: number[]

  start(): void {
    this.startTime = performance.now()
  }

  sample(): void {
    this.samples.push(performance.now() - this.startTime)
  }

  getStats(): { min: number; max: number; avg: number; p50: number; p99: number } {
    const sorted = [...this.samples].sort((a, b) => a - b)
    return {
      min: sorted[0],
      max: sorted[sorted.length - 1],
      avg: sorted.reduce((a, b) => a + b, 0) / sorted.length,
      p50: sorted[Math.floor(sorted.length * 0.5)],
      p99: sorted[Math.floor(sorted.length * 0.99)],
    }
  }
}
```

**TMNL Location**: `src/lib/streams/playground/timing.ts`

---

## Pattern 10: Atom-as-State — REACTIVE METRICS

**When:** Bridging Effect computations to React via effect-atom.

```typescript
import { Atom } from '@effect-rx/rx-react'
import { Effect, Stream } from 'effect'

// Metrics atom updated by emission engine
const metricsAtom = Atom.make<EmissionMetrics>({
  eventsEmitted: 0,
  eventsProcessed: 0,
  bytesProcessed: 0,
  avgLatencyMs: 0,
  p99LatencyMs: 0,
  reservoirSamples: [],
})

// Stream subscription that updates atom
const subscribeToMetrics = (engine: EmissionEngine) =>
  Effect.gen(function*() {
    const metricsStream = yield* engine.getMetricsStream()

    yield* metricsStream.pipe(
      Stream.runForEach(metrics =>
        Effect.sync(() => Atom.set(metricsAtom, metrics))
      )
    )
  })

// React component subscribes directly
function MetricsDisplay() {
  const metrics = useAtomValue(metricsAtom)

  return (
    <div>
      <span>Events: {metrics.eventsProcessed.toLocaleString()}</span>
      <span>Latency P99: {metrics.p99LatencyMs.toFixed(2)}ms</span>
    </div>
  )
}
```

**Key Pattern**: Effect.Stream → Atom.set → useAtomValue — unidirectional reactive flow.

**TMNL Location**: `src/lib/streams/playground/atoms/index.ts`

---

## Decision Tree: Component Selection

```
What are you building?
│
├─ High-frequency event emission?
│  └─ EmissionEngine (Pattern 1)
│
├─ Latency metrics from millions of events?
│  └─ Reservoir Sampling (Pattern 2)
│
├─ Protocol-compliant test payloads?
│  ├─ IoT sensors? → SenML generator
│  ├─ Industrial automation? → OPC-UA generator
│  └─ Time-series metrics? → Prometheus generator
│
├─ Raw event inspection?
│  └─ RawEventsPanel with schema-derived columns
│
├─ Real-time charts?
│  ├─ Time series? → D3LineChart
│  ├─ Distribution? → D3Histogram
│  └─ Single value? → D3Gauge
│
└─ Failure resilience?
   └─ CircuitBreaker (Pattern 7)
```

---

## Anti-Patterns

### Don't: Use setInterval for high-frequency emission

```typescript
// BANNED - Drift, no frame synchronization
setInterval(() => emit(payload), 1)

// CORRECT - rAF-synchronized batching
requestAnimationFrame(frameLoop)
```

### Don't: Store all latency samples

```typescript
// BANNED - Memory explosion at 10k events/sec
const allLatencies: number[] = []
allLatencies.push(latency)  // Unbounded growth

// CORRECT - Reservoir sampling
reservoirSample(latency)  // Fixed memory (1000 samples)
```

### Don't: Block on every event

```typescript
// BANNED - Serializes processing
for (const event of events) {
  await processEvent(event)  // One at a time
}

// CORRECT - Batch with Queue
yield* Queue.offerAll(queue, events)  // Batched
```

---

## Integration Points

**Depends on:**
- `effect-patterns` — Effect.Service, Stream, Queue
- `effect-stream-patterns` — Stream operators, backpressure
- `ag-grid-patterns` — RawEventsPanel grid integration

**Used by:**
- `data-manager-system` — Throughput monitoring patterns
- `tmnl-testbed-patterns` — Playground testbed structure

---

## Quick Reference

| Task | Pattern | File |
|------|---------|------|
| Emit events at 10k/sec | EmissionEngine | playground/EmissionEngine.ts |
| Sample latencies | Reservoir Sampling | playground/timing.ts |
| Generate SenML payloads | Payload Generators | scenarios/generators/senml.ts |
| Display raw events | RawEventsPanel | panels/RawEventsPanel.tsx |
| Show throughput metrics | ThroughputPanel | panels/ThroughputPanel.tsx |
| Implement circuit breaker | CircuitBreakerPanel | panels/CircuitBreakerPanel.tsx |
| Render time series | D3LineChart | viz/D3LineChart.tsx |
| Measure sub-ms latency | performance.now() | playground/timing.ts |
