---
name: iiot-unified-namespace
description: Unified Namespace (UNS) architecture for IIoT. Topic hierarchy, NATS subjects, and data flow patterns.
triggers:
  - "UNS"
  - "Unified Namespace"
  - "topic hierarchy"
  - "MQTT topics"
  - "NATS subjects"
  - "Sparkplug"
  - "IIoT topics"
---

# IIoT Unified Namespace

## Overview

The Unified Namespace (UNS) is a centralized, real-time data hub that organizes all IIoT data following the ISA-95 hierarchy. It provides a single source of truth for all operational data.

## Core Principles

1. **Single Source of Truth** - All data flows through UNS
2. **ISA-95 Aligned** - Topic structure mirrors equipment hierarchy
3. **Report-by-Exception** - Only publish changes, not constant polling
4. **Decoupled Architecture** - Producers and consumers are independent

## Topic Hierarchy

### NATS Subject Pattern

```
iiot.{site}.{area}.{line}.{machine}.{sensor}.{metric}

Examples:
iiot.chicago.plant-a.line-001.mch-001.tmp-001.value
iiot.chicago.plant-a.line-001.mch-001.tmp-001.quality
iiot.chicago.plant-a.line-001.mch-001.>.alarms
```

### Hierarchy Levels

| Level | NATS Token | Example | Description |
|-------|------------|---------|-------------|
| 1 | `iiot` | `iiot` | Root namespace |
| 2 | `{site}` | `chicago` | Physical location |
| 3 | `{area}` | `plant-a` | Plant/Area |
| 4 | `{line}` | `line-001` | Production line |
| 5 | `{machine}` | `mch-001` | Equipment |
| 6 | `{sensor}` | `tmp-001` | Device ID |
| 7 | `{metric}` | `value` | Data type |

### Metric Types

| Metric | Description | Payload |
|--------|-------------|---------|
| `value` | Current reading | `{ value: number, time: string }` |
| `quality` | Data quality | `{ quality: number, time: string }` |
| `alarms` | Active alarms | `{ id, severity, message, time }` |
| `state` | Equipment state | `{ state: string, since: string }` |
| `config` | Configuration | Device-specific config |

## Wildcard Subscriptions

NATS supports powerful wildcard patterns:

```typescript
// All sensors on a specific machine
'iiot.chicago.plant-a.line-001.mch-001.>'

// All temperature sensors across entire site
'iiot.chicago.*.*.*.tmp-*.value'

// All alarms enterprise-wide
'iiot.*.*.*.*.*.alarms'

// All values from a specific line
'iiot.chicago.plant-a.line-001.*.*.value'

// Single-level wildcard (specific position)
'iiot.chicago.plant-a.*.mch-001.*.value'  // Machine across all lines
```

## TMNL + NATS Integration

### Subject Builder

```typescript
// src/lib/iiot/uns/subject-builder.ts

import { Schema, Effect } from 'effect'
import type { DeviceId, PlantId, LineId, MachineId } from '@/lib/iiot/schemas'

// Metric types
export const UNSMetric = Schema.Literal('value', 'quality', 'alarms', 'state', 'config')
export type UNSMetric = Schema.Schema.Type<typeof UNSMetric>

// Build a UNS subject from components
export const buildSubject = (
  site: string,
  area: string,
  line: string,
  machine: string,
  sensor: string,
  metric: UNSMetric = 'value'
): string => `iiot.${site}.${area}.${line}.${machine}.${sensor}.${metric}`

// Sensor hierarchy type
export interface SensorHierarchy {
  site: string
  area: string
  lineName: string
  machineName: string
  deviceId: string
}

// Build subject from hierarchy object
export const hierarchyToSubject = (
  h: SensorHierarchy,
  metric: UNSMetric = 'value'
): string =>
  `iiot.${h.site}.${h.area}.${h.lineName}.${h.machineName}.${h.deviceId}.${metric}`

// Parse a subject back to components
export const parseSubject = (subject: string): SensorHierarchy | null => {
  const parts = subject.split('.')
  if (parts.length < 7 || parts[0] !== 'iiot') return null

  return {
    site: parts[1],
    area: parts[2],
    lineName: parts[3],
    machineName: parts[4],
    deviceId: parts[5],
  }
}
```

### Publishing Readings via Holonet

```typescript
// src/lib/iiot/uns/publisher.ts

import { Effect, Schema, Stream } from 'effect'
import { NatsInnerService } from '@/lib/holonet/nats/inner'
import { MessageDecoder } from '@/lib/holonet/decoder'
import { buildSubject, hierarchyToSubject, type SensorHierarchy } from './subject-builder'

// Sensor reading schema
const SensorReading = Schema.Struct({
  deviceId: Schema.String,
  value: Schema.Number,
  quality: Schema.Number.pipe(Schema.int()),
  time: Schema.DateFromString,
})
type SensorReading = Schema.Schema.Type<typeof SensorReading>

// UNS value payload (what gets published)
const UNSValuePayload = Schema.Struct({
  value: Schema.Number,
  quality: Schema.Number,
  time: Schema.String,
})

export class UNSPublisher extends Effect.Service<UNSPublisher>()(
  'iiot/UNSPublisher',
  {
    effect: Effect.gen(function* () {
      const nats = yield* NatsInnerService
      const decoder = yield* MessageDecoder

      // Publish a single reading
      const publishReading = (
        hierarchy: SensorHierarchy,
        reading: SensorReading
      ) =>
        Effect.gen(function* () {
          const subject = hierarchyToSubject(hierarchy, 'value')

          // Encode using MessageDecoder (no JSON.stringify)
          const payload = yield* decoder.encodeBytes(UNSValuePayload)({
            value: reading.value,
            quality: reading.quality,
            time: reading.time.toISOString(),
          })

          // Publish to JetStream for persistence
          yield* nats.jsPublish(subject, payload)

          yield* Effect.log(`Published to ${subject}: ${reading.value}`)
        })

      // Publish quality update
      const publishQuality = (
        hierarchy: SensorHierarchy,
        quality: number,
        time: Date
      ) =>
        Effect.gen(function* () {
          const subject = hierarchyToSubject(hierarchy, 'quality')

          const QualityPayload = Schema.Struct({
            quality: Schema.Number,
            time: Schema.String,
          })

          const payload = yield* decoder.encodeBytes(QualityPayload)({
            quality,
            time: time.toISOString(),
          })

          yield* nats.jsPublish(subject, payload)
        })

      return {
        publishReading,
        publishQuality,
      } as const
    }),
    dependencies: [NatsInnerService.Default, MessageDecoder.Default],
  }
) {}
```

### Subscribing to UNS Data

```typescript
// src/lib/iiot/uns/subscriber.ts

import { Effect, Stream, Schema, Option } from 'effect'
import { NatsInnerService } from '@/lib/holonet/nats/inner'
import { MessageDecoder } from '@/lib/holonet/decoder'
import { parseSubject } from './subject-builder'

// Incoming UNS message with parsed metadata
const UNSMessage = Schema.Struct({
  subject: Schema.String,
  hierarchy: Schema.Struct({
    site: Schema.String,
    area: Schema.String,
    lineName: Schema.String,
    machineName: Schema.String,
    deviceId: Schema.String,
  }),
  value: Schema.Number,
  quality: Schema.Number,
  time: Schema.DateFromString,
})
type UNSMessage = Schema.Schema.Type<typeof UNSMessage>

export class UNSSubscriber extends Effect.Service<UNSSubscriber>()(
  'iiot/UNSSubscriber',
  {
    effect: Effect.gen(function* () {
      const nats = yield* NatsInnerService
      const decoder = yield* MessageDecoder

      // Subscribe to a UNS pattern
      const subscribe = (pattern: string) =>
        Effect.gen(function* () {
          const sub = yield* nats.core.subscribe(pattern)

          const ValuePayload = Schema.Struct({
            value: Schema.Number,
            quality: Schema.Number,
            time: Schema.String,
          })

          return Stream.fromAsyncIterable(
            sub[Symbol.asyncIterator](),
            (e) => e as Error
          ).pipe(
            Stream.mapEffect((msg) =>
              Effect.gen(function* () {
                const hierarchy = parseSubject(msg.subject)
                if (!hierarchy) {
                  yield* Effect.log(`Invalid subject: ${msg.subject}`)
                  return Option.none()
                }

                // Decode payload using MessageDecoder
                const payloadResult = yield* decoder
                  .decodeBytes(ValuePayload)(msg.data)
                  .pipe(Effect.either)

                if (payloadResult._tag === 'Left') {
                  yield* Effect.log(`Decode error: ${payloadResult.left.message}`)
                  return Option.none()
                }

                const payload = payloadResult.right

                return Option.some({
                  subject: msg.subject,
                  hierarchy,
                  value: payload.value,
                  quality: payload.quality,
                  time: new Date(payload.time),
                })
              })
            ),
            Stream.filterMap((opt) => opt)
          )
        })

      // Subscribe to all values from a machine
      const subscribeToMachine = (
        site: string,
        area: string,
        line: string,
        machine: string
      ) => subscribe(`iiot.${site}.${area}.${line}.${machine}.*.value`)

      // Subscribe to all values from a line
      const subscribeToLine = (
        site: string,
        area: string,
        line: string
      ) => subscribe(`iiot.${site}.${area}.${line}.*.*.value`)

      // Subscribe to all alarms
      const subscribeToAlarms = (site?: string) =>
        subscribe(site ? `iiot.${site}.*.*.*.*.alarms` : 'iiot.*.*.*.*.*.alarms')

      return {
        subscribe,
        subscribeToMachine,
        subscribeToLine,
        subscribeToAlarms,
      } as const
    }),
    dependencies: [NatsInnerService.Default, MessageDecoder.Default],
  }
) {}
```

## JetStream Streams for UNS

### Stream Configuration

```typescript
// src/lib/iiot/uns/streams.ts

import { Effect } from 'effect'
import { NatsInnerService } from '@/lib/holonet/nats/inner'
import type { StreamConfig } from 'nats'

// UNS stream configuration
export const UNS_STREAM_CONFIG: Partial<StreamConfig> = {
  name: 'UNS_IIOT',
  subjects: ['iiot.>'],  // Capture all UNS traffic
  storage: 'file',
  retention: 'limits',
  max_age: 30 * 24 * 60 * 60 * 1_000_000_000, // 30 days in nanos
  max_bytes: 10 * 1024 * 1024 * 1024, // 10GB
  max_msgs_per_subject: 1_000_000, // 1M messages per device
  discard: 'old',
  num_replicas: 1,  // Increase for production
}

// Alarm stream (longer retention)
export const UNS_ALARMS_STREAM_CONFIG: Partial<StreamConfig> = {
  name: 'UNS_ALARMS',
  subjects: ['iiot.*.*.*.*.*.alarms'],
  storage: 'file',
  retention: 'limits',
  max_age: 365 * 24 * 60 * 60 * 1_000_000_000, // 1 year
  max_bytes: 1 * 1024 * 1024 * 1024, // 1GB
  discard: 'old',
  num_replicas: 1,
}

// Create UNS streams
export const createUNSStreams = Effect.gen(function* () {
  const nats = yield* NatsInnerService
  const js = yield* nats.jetstream()

  // Create main UNS stream
  yield* Effect.tryPromise(() =>
    js.streams.add(UNS_STREAM_CONFIG as StreamConfig)
  ).pipe(
    Effect.catchTag('UnknownException', () =>
      Effect.log('UNS_IIOT stream may already exist')
    )
  )

  // Create alarms stream
  yield* Effect.tryPromise(() =>
    js.streams.add(UNS_ALARMS_STREAM_CONFIG as StreamConfig)
  ).pipe(
    Effect.catchTag('UnknownException', () =>
      Effect.log('UNS_ALARMS stream may already exist')
    )
  )

  yield* Effect.log('UNS streams initialized')
})
```

### KV Store for Asset State

```typescript
// src/lib/iiot/uns/state-store.ts

import { Effect, Schema } from 'effect'
import { NatsInnerService } from '@/lib/holonet/nats/inner'
import { MessageDecoder } from '@/lib/holonet/decoder'

// Asset state schema
const AssetState = Schema.Struct({
  deviceId: Schema.String,
  lastValue: Schema.Number,
  lastQuality: Schema.Number,
  lastUpdated: Schema.String,
  status: Schema.Literal('online', 'offline', 'stale', 'error'),
})
type AssetState = Schema.Schema.Type<typeof AssetState>

export class UNSStateStore extends Effect.Service<UNSStateStore>()(
  'iiot/UNSStateStore',
  {
    effect: Effect.gen(function* () {
      const nats = yield* NatsInnerService
      const decoder = yield* MessageDecoder

      const BUCKET_NAME = 'uns-assets'

      // Get or create KV bucket
      const getBucket = () =>
        Effect.gen(function* () {
          const js = yield* nats.jetstream()
          return yield* Effect.tryPromise(() =>
            js.views.kv(BUCKET_NAME, { history: 5 })
          )
        })

      // Build KV key from hierarchy
      const buildKey = (
        site: string,
        area: string,
        line: string,
        machine: string,
        sensor: string
      ) => `${site}/${area}/${line}/${machine}/${sensor}`

      // Update asset state
      const updateState = (
        site: string,
        area: string,
        line: string,
        machine: string,
        sensor: string,
        state: AssetState
      ) =>
        Effect.gen(function* () {
          const bucket = yield* getBucket()
          const key = buildKey(site, area, line, machine, sensor)
          const payload = yield* decoder.encodeJson(AssetState)(state)
          yield* Effect.tryPromise(() => bucket.putString(key, payload))
        })

      // Get asset state
      const getState = (
        site: string,
        area: string,
        line: string,
        machine: string,
        sensor: string
      ) =>
        Effect.gen(function* () {
          const bucket = yield* getBucket()
          const key = buildKey(site, area, line, machine, sensor)
          const entry = yield* Effect.tryPromise(() => bucket.get(key))
          if (!entry?.string()) return null
          return yield* decoder.decodeJson(AssetState)(entry.string())
        })

      return {
        updateState,
        getState,
        buildKey,
      } as const
    }),
    dependencies: [NatsInnerService.Default, MessageDecoder.Default],
  }
) {}
```

## Report-by-Exception Pattern

Only publish when values change significantly:

```typescript
// src/lib/iiot/uns/rbe.ts

import { Effect, Stream, Ref, Option } from 'effect'

interface RBEConfig {
  deadband: number  // Absolute change threshold
  percentDeadband?: number  // Percentage change threshold
  maxInterval?: number  // Max ms between updates (heartbeat)
}

// Report-by-Exception filter for a stream
export const withReportByException = <A extends { value: number }>(
  config: RBEConfig
) => {
  return (stream: Stream.Stream<A>) =>
    Effect.gen(function* () {
      const lastValueRef = yield* Ref.make<Option.Option<{ value: number; time: number }>>(
        Option.none()
      )

      return stream.pipe(
        Stream.filterEffect((reading) =>
          Effect.gen(function* () {
            const lastOpt = yield* Ref.get(lastValueRef)
            const now = Date.now()

            if (Option.isNone(lastOpt)) {
              // First reading - always publish
              yield* Ref.set(lastValueRef, Option.some({ value: reading.value, time: now }))
              return true
            }

            const last = lastOpt.value

            // Check deadband
            const absoluteChange = Math.abs(reading.value - last.value)
            const percentChange = last.value !== 0
              ? (absoluteChange / Math.abs(last.value)) * 100
              : absoluteChange > 0 ? 100 : 0

            const exceedsDeadband = absoluteChange >= config.deadband
            const exceedsPercent = config.percentDeadband
              ? percentChange >= config.percentDeadband
              : false

            // Check heartbeat interval
            const timeSinceLast = now - last.time
            const needsHeartbeat = config.maxInterval
              ? timeSinceLast >= config.maxInterval
              : false

            if (exceedsDeadband || exceedsPercent || needsHeartbeat) {
              yield* Ref.set(lastValueRef, Option.some({ value: reading.value, time: now }))
              return true
            }

            return false
          })
        )
      )
    })
}

// Example usage:
// const rbeStream = yield* withReportByException({ deadband: 0.1, maxInterval: 60000 })(rawStream)
```

## Sparkplug B Compatibility

For Sparkplug B compliance, use this topic structure:

```
spBv1.0/{namespace}/{group_id}/{message_type}/{edge_node_id}/{device_id}

Message types:
- NBIRTH: Node birth certificate
- NDEATH: Node death certificate
- DBIRTH: Device birth certificate
- DDEATH: Device death certificate
- NDATA: Node data
- DDATA: Device data
- NCMD: Node command
- DCMD: Device command
```

### Sparkplug Topic Builder

```typescript
// src/lib/iiot/uns/sparkplug.ts

export type SparkplugMessageType =
  | 'NBIRTH' | 'NDEATH'
  | 'DBIRTH' | 'DDEATH'
  | 'NDATA' | 'DDATA'
  | 'NCMD' | 'DCMD'

export const buildSparkplugTopic = (
  namespace: string,
  groupId: string,
  messageType: SparkplugMessageType,
  edgeNodeId: string,
  deviceId?: string
): string => {
  const base = `spBv1.0/${namespace}/${groupId}/${messageType}/${edgeNodeId}`
  return deviceId ? `${base}/${deviceId}` : base
}

// Example:
// buildSparkplugTopic('Factory', 'Chicago', 'DDATA', 'LINE-001', 'TMP-001')
// => 'spBv1.0/Factory/Chicago/DDATA/LINE-001/TMP-001'
```

## Best Practices

### Topic Design

1. **Keep it flat** - Avoid deep nesting beyond 7 levels
2. **Use lowercase** - Consistent casing prevents mismatches
3. **Use hyphens** - `line-001` not `line_001` or `line.001`
4. **Version namespace** - `iiot.v1` allows future changes

### Performance

1. **Use JetStream** - Enables replay, persistence, exactly-once
2. **Partition by device** - Avoids hot partitions
3. **Report-by-exception** - Reduces message volume 90%+
4. **Compress payloads** - Use MessagePack or CBOR for high-frequency data

### Security

1. **Per-device credentials** - Scoped NATS users per device
2. **Subject-based ACLs** - Restrict pub/sub by hierarchy
3. **TLS everywhere** - Encrypt all traffic

## Related Skills

- `/iiot-isa95-hierarchy` - Equipment hierarchy modeling
- `/nex-effect-services` - Effect-TS NATS patterns
- `/effect-stream-patterns` - Stream processing patterns

## References

- [UNS Complete Guide (SymphonyAI)](https://www.symphonyai.com/industrial/unified-namespace-complete-guide/)
- [UNS with MQTT Sparkplug (HiveMQ)](https://www.hivemq.com/blog/implementing-unified-namespace-uns-mqtt-sparkplug/)
- [Sparkplug B Specification](https://sparkplug.eclipse.org/)
- [NATS Subjects Best Practices](https://docs.nats.io/nats-concepts/subjects)
