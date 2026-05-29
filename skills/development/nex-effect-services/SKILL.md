---
name: nex-effect-services
description: Build NEX-integrated services using Effect-TS. Workload clients, RPC patterns, event subscriptions.
triggers:
  - "NEX Effect"
  - "NEX service"
  - "NEX TypeScript"
  - "workload Effect"
  - "NATS RPC Effect"
  - "NEX client Effect"
---

# NEX + Effect Services

## Overview

This skill covers building NEX-aware services in TypeScript using Effect-TS and the existing `NatsInnerService` from holonet. All patterns use **MessageDecoder** for Effect-native encoding/decoding (no try/catch, no JSON.stringify/parse).

## Architecture Pattern

```
┌─────────────────────────────────────────────────────────────────────┐
│                    Effect Service Layer                              │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐  │
│  │  NexClientSvc   │    │  WorkloadSvc    │    │  EventWatcher   │  │
│  │  (auction/dep)  │    │  (RPC handlers) │    │  (lifecycle)    │  │
│  └────────┬────────┘    └────────┬────────┘    └────────┬────────┘  │
│           │                      │                      │            │
│           └──────────────────────┼──────────────────────┘            │
│                                  │                                   │
│                    ┌─────────────┴─────────────┐                     │
│                    │    MessageDecoder         │                     │
│                    │  (Schema.parseJson based) │                     │
│                    └─────────────┬─────────────┘                     │
│                                  │                                   │
│                    ┌─────────────┴─────────────┐                     │
│                    │    NatsInnerService       │                     │
│                    │  (holonet/nats/inner)     │                     │
│                    └───────────────────────────┘                     │
└─────────────────────────────────────────────────────────────────────┘
```

## MessageDecoder Service

The foundation for Effect-native encoding/decoding. Uses `Schema.parseJson` internally to combine JSON parsing + schema validation in one step.

```typescript
// src/lib/holonet/decoder.ts

import { Effect, Schema, ParseResult, Data } from 'effect'

// ─── Decode Errors ────────────────────────────────────────────────────

export class DecodeError extends Data.TaggedError('DecodeError')<{
  readonly message: string
  readonly cause: ParseResult.ParseError
}> {}

// ─── MessageDecoder Service ───────────────────────────────────────────

export class MessageDecoder extends Effect.Service<MessageDecoder>()(
  'holonet/MessageDecoder',
  {
    effect: Effect.succeed({
      /**
       * Decode a JSON string using a schema.
       * Uses Schema.parseJson internally - no try/catch needed.
       */
      decodeJson: <A, I, R>(schema: Schema.Schema<A, I, R>) => {
        const parser = Schema.decodeUnknown(Schema.parseJson(schema))
        return (raw: string): Effect.Effect<A, DecodeError, R> =>
          parser(raw).pipe(
            Effect.mapError((cause) =>
              new DecodeError({
                message: `Failed to decode JSON: ${ParseResult.TreeFormatter.formatErrorSync(cause)}`,
                cause,
              })
            )
          )
      },

      /**
       * Decode a Uint8Array (NATS message) using a schema.
       */
      decodeBytes: <A, I, R>(schema: Schema.Schema<A, I, R>) => {
        const parser = Schema.decodeUnknown(Schema.parseJson(schema))
        return (raw: Uint8Array): Effect.Effect<A, DecodeError, R> =>
          parser(new TextDecoder().decode(raw)).pipe(
            Effect.mapError((cause) =>
              new DecodeError({
                message: `Failed to decode bytes: ${ParseResult.TreeFormatter.formatErrorSync(cause)}`,
                cause,
              })
            )
          )
      },

      /**
       * Encode a value to JSON string using a schema.
       */
      encodeJson: <A, I, R>(schema: Schema.Schema<A, I, R>) => {
        const encoder = Schema.encode(Schema.parseJson(schema))
        return (value: A): Effect.Effect<string, DecodeError, R> =>
          encoder(value).pipe(
            Effect.mapError((cause) =>
              new DecodeError({
                message: `Failed to encode to JSON: ${ParseResult.TreeFormatter.formatErrorSync(cause)}`,
                cause,
              })
            )
          )
      },

      /**
       * Encode a value to Uint8Array (for NATS publish).
       */
      encodeBytes: <A, I, R>(schema: Schema.Schema<A, I, R>) => {
        const encoder = Schema.encode(Schema.parseJson(schema))
        return (value: A): Effect.Effect<Uint8Array, DecodeError, R> =>
          encoder(value).pipe(
            Effect.map((json) => new TextEncoder().encode(json)),
            Effect.mapError((cause) =>
              new DecodeError({
                message: `Failed to encode to bytes: ${ParseResult.TreeFormatter.formatErrorSync(cause)}`,
                cause,
              })
            )
          )
      },
    } as const),
  }
) {}
```

### Usage Pattern (No try/catch)

```typescript
// Define schema once
const MyEventSchema = Schema.TaggedStruct('MyEvent', {
  id: Schema.String,
  timestamp: Schema.DateFromString,
})

// In service that consumes NATS messages
const processMessage = (msg: Msg) =>
  Effect.gen(function* () {
    const decoder = yield* MessageDecoder

    // Effect-native decode - no try/catch
    const event = yield* decoder.decodeBytes(MyEventSchema)(msg.data)

    // Process event...
    yield* Effect.log(`Received event: ${event.id}`)
  })
```

---

## NEX Client Service

Wrap NEX client operations in an Effect service.

```typescript
// src/lib/nex/client.ts

import { Effect, Schema, Data } from 'effect'
import { NatsInnerService } from '@/lib/holonet/nats/inner'
import { MessageDecoder, DecodeError } from '@/lib/holonet/decoder'

// ─── Schemas ──────────────────────────────────────────────────────────

const AuctionRequest = Schema.Struct({
  type: Schema.String,
  tags: Schema.Record({ key: Schema.String, value: Schema.String }),
  lifecycle: Schema.Literal('service', 'job', 'function'),
})

const AuctionResponse = Schema.Struct({
  bidderId: Schema.String,
  nodeId: Schema.String,
  tags: Schema.Record({ key: Schema.String, value: Schema.String }),
  lifecycles: Schema.Array(Schema.Literal('service', 'job', 'function')),
})

const StartWorkloadRequest = Schema.Struct({
  name: Schema.String,
  description: Schema.optional(Schema.String),
  type: Schema.String,
  lifecycle: Schema.Literal('service', 'job', 'function'),
  startRequest: Schema.Unknown, // Agent-specific JSON
  tags: Schema.Record({ key: Schema.String, value: Schema.String }),
})

const WorkloadDeployResponse = Schema.Struct({
  workloadId: Schema.String,
  nodeId: Schema.String,
  status: Schema.String,
})

const WorkloadListResponse = Schema.Struct({
  workloads: Schema.Array(Schema.Struct({
    workloadId: Schema.String,
    name: Schema.String,
    type: Schema.String,
    lifecycle: Schema.String,
    nodeId: Schema.String,
  })),
})

// ─── Errors ───────────────────────────────────────────────────────────

export class NexError extends Data.TaggedError('NexError')<{
  readonly message: string
  readonly operation: string
}> {}

// ─── Service ──────────────────────────────────────────────────────────

export class NexClientService extends Effect.Service<NexClientService>()(
  'nex/Client',
  {
    effect: Effect.gen(function* () {
      const nats = yield* NatsInnerService
      const decoder = yield* MessageDecoder
      const namespace = 'default' // Or from config

      // Auction for workload placement
      const auction = (
        type: string,
        tags: Record<string, string>,
        lifecycle: 'service' | 'job' | 'function' = 'service',
        timeoutMs = 500
      ) =>
        Effect.gen(function* () {
          const subject = `$NEX.SVC.${namespace}.control.AUCTION`

          // Encode request using MessageDecoder
          const payload = yield* decoder.encodeBytes(AuctionRequest)({
            type,
            tags,
            lifecycle,
          })

          // Use requestMany to collect bids
          const responses: Schema.Schema.Type<typeof AuctionResponse>[] = []

          // Simplified: single request with timeout
          // In production, use RequestMany pattern for multiple bids
          const response = yield* Effect.tryPromise({
            try: () => nats.core.request(subject, payload, { timeout: timeoutMs }),
            catch: (e) => new NexError({ message: String(e), operation: 'auction' }),
          }).pipe(Effect.option)

          if (response._tag === 'Some') {
            const bid = yield* decoder.decodeBytes(AuctionResponse)(response.value.data)
            responses.push(bid)
          }

          return responses
        })

      // Deploy workload to winning bidder
      const startWorkload = (
        bidderId: string,
        request: Schema.Schema.Type<typeof StartWorkloadRequest>
      ) =>
        Effect.gen(function* () {
          const subject = `$NEX.SVC.${namespace}.control.AUCTIONDEPLOY.${bidderId}`

          const payload = yield* decoder.encodeBytes(StartWorkloadRequest)(request)

          const response = yield* Effect.tryPromise({
            try: () => nats.core.request(subject, payload, { timeout: 30000 }),
            catch: (e) => new NexError({ message: String(e), operation: 'startWorkload' }),
          })

          return yield* decoder.decodeBytes(WorkloadDeployResponse)(response.data)
        })

      // List running workloads
      const listWorkloads = () =>
        Effect.gen(function* () {
          const subject = `$NEX.SVC.${namespace}.workloads.LIST`
          const payload = new TextEncoder().encode('{}')

          const response = yield* Effect.tryPromise({
            try: () => nats.core.request(subject, payload, { timeout: 5000 }),
            catch: (e) => new NexError({ message: String(e), operation: 'listWorkloads' }),
          })

          return yield* decoder.decodeBytes(WorkloadListResponse)(response.data)
        })

      // Stop a workload
      const stopWorkload = (workloadId: string) =>
        Effect.gen(function* () {
          const subject = `$NEX.SVC.${namespace}.workloads.STOP`

          const StopRequest = Schema.Struct({ workloadId: Schema.String })
          const payload = yield* decoder.encodeBytes(StopRequest)({ workloadId })

          yield* Effect.tryPromise({
            try: () => nats.core.publish(subject, payload),
            catch: (e) => new NexError({ message: String(e), operation: 'stopWorkload' }),
          })
        })

      return {
        auction,
        startWorkload,
        listWorkloads,
        stopWorkload,
      } as const
    }),
    dependencies: [NatsInnerService.Default, MessageDecoder.Default],
  }
) {}
```

---

## RPC Handler Service

Build request-reply services using MessageDecoder.

```typescript
// src/lib/nex/rpc.ts

import { Effect, Schema, Stream, Data } from 'effect'
import { NatsInnerService } from '@/lib/holonet/nats/inner'
import { MessageDecoder, DecodeError } from '@/lib/holonet/decoder'
import type { Msg } from 'nats'

// ─── RPC Schemas ──────────────────────────────────────────────────────

const RpcRequest = Schema.Struct({
  method: Schema.String,
  params: Schema.Unknown,
})

const RpcResponse = Schema.Struct({
  result: Schema.Unknown,
  error: Schema.optional(Schema.String),
})

// ─── Errors ───────────────────────────────────────────────────────────

export class RpcError extends Data.TaggedError('RpcError')<{
  readonly message: string
  readonly method?: string
}> {}

// ─── Service ──────────────────────────────────────────────────────────

export class RpcService extends Effect.Service<RpcService>()(
  'nex/Rpc',
  {
    effect: Effect.gen(function* () {
      const nats = yield* NatsInnerService
      const decoder = yield* MessageDecoder

      // Register an RPC handler on a subject
      const registerHandler = <A, E, R>(
        subject: string,
        handler: (method: string, params: unknown) => Effect.Effect<A, E, R>
      ) =>
        Effect.gen(function* () {
          const sub = yield* Effect.tryPromise(() => nats.core.subscribe(subject))

          const processMessages = Stream.fromAsyncIterable(
            sub[Symbol.asyncIterator](),
            (e) => e as Error
          ).pipe(
            Stream.mapEffect((msg: Msg) =>
              Effect.gen(function* () {
                // Decode request
                const decodeResult = yield* decoder
                  .decodeBytes(RpcRequest)(msg.data)
                  .pipe(Effect.either)

                if (decodeResult._tag === 'Left') {
                  // Decode failed - send error response
                  if (msg.reply) {
                    const errorPayload = yield* decoder.encodeBytes(RpcResponse)({
                      result: null,
                      error: `Decode error: ${decodeResult.left.message}`,
                    })
                    yield* Effect.tryPromise(() =>
                      nats.core.publish(msg.reply, errorPayload)
                    )
                  }
                  return
                }

                const request = decodeResult.right

                // Execute handler
                const handlerResult = yield* handler(request.method, request.params).pipe(
                  Effect.either,
                )

                // Send response
                if (msg.reply) {
                  if (handlerResult._tag === 'Left') {
                    const errorPayload = yield* decoder.encodeBytes(RpcResponse)({
                      result: null,
                      error: String(handlerResult.left),
                    })
                    yield* Effect.tryPromise(() =>
                      nats.core.publish(msg.reply, errorPayload)
                    )
                  } else {
                    const successPayload = yield* decoder.encodeBytes(RpcResponse)({
                      result: handlerResult.right,
                    })
                    yield* Effect.tryPromise(() =>
                      nats.core.publish(msg.reply, successPayload)
                    )
                  }
                }
              })
            )
          )

          return { subject, stream: processMessages }
        })

      // Make an RPC call
      const call = <A>(
        subject: string,
        method: string,
        params: unknown,
        timeout = 5000
      ) =>
        Effect.gen(function* () {
          const payload = yield* decoder.encodeBytes(RpcRequest)({ method, params })

          const response = yield* Effect.tryPromise({
            try: () => nats.core.request(subject, payload, { timeout }),
            catch: (e) => new RpcError({ message: String(e), method }),
          })

          const parsed = yield* decoder.decodeBytes(RpcResponse)(response.data)

          if (parsed.error) {
            return yield* Effect.fail(new RpcError({
              message: parsed.error,
              method,
            }))
          }

          return parsed.result as A
        })

      return { registerHandler, call } as const
    }),
    dependencies: [NatsInnerService.Default, MessageDecoder.Default],
  }
) {}
```

---

## Event Subscription Service

Monitor NEX lifecycle events.

```typescript
// src/lib/nex/events.ts

import { Effect, Stream, Schema, Option } from 'effect'
import { NatsInnerService } from '@/lib/holonet/nats/inner'
import { MessageDecoder } from '@/lib/holonet/decoder'
import type { Msg } from 'nats'

// ─── Event Schemas ────────────────────────────────────────────────────

const WorkloadStartedEvent = Schema.TaggedStruct('WorkloadStarted', {
  workloadId: Schema.String,
  nodeId: Schema.String,
  name: Schema.String,
  namespace: Schema.String,
  type: Schema.String,
  lifecycle: Schema.String,
  timestamp: Schema.optional(Schema.String),
})

const WorkloadStoppedEvent = Schema.TaggedStruct('WorkloadStopped', {
  workloadId: Schema.String,
  nodeId: Schema.String,
  error: Schema.optional(Schema.String),
  exitCode: Schema.optional(Schema.Number),
  timestamp: Schema.optional(Schema.String),
})

const NodeStartedEvent = Schema.TaggedStruct('NodeStarted', {
  nodeId: Schema.String,
  name: Schema.String,
  namespace: Schema.String,
  timestamp: Schema.optional(Schema.String),
})

const NodeStoppedEvent = Schema.TaggedStruct('NodeStopped', {
  nodeId: Schema.String,
  timestamp: Schema.optional(Schema.String),
})

// Union of all events
const NexEvent = Schema.Union(
  WorkloadStartedEvent,
  WorkloadStoppedEvent,
  NodeStartedEvent,
  NodeStoppedEvent
)
type NexEvent = Schema.Schema.Type<typeof NexEvent>

// ─── Service ──────────────────────────────────────────────────────────

export class NexEventWatcher extends Effect.Service<NexEventWatcher>()(
  'nex/EventWatcher',
  {
    effect: Effect.gen(function* () {
      const nats = yield* NatsInnerService
      const decoder = yield* MessageDecoder
      const namespace = 'default'

      // Subscribe to all NEX events
      const watchEvents = () =>
        Effect.gen(function* () {
          const subject = `$NEX.FEED.${namespace}.event.>`
          const sub = yield* Effect.tryPromise(() => nats.core.subscribe(subject))

          return Stream.fromAsyncIterable(
            sub[Symbol.asyncIterator](),
            (e) => e as Error
          ).pipe(
            Stream.mapEffect((msg: Msg) =>
              decoder.decodeBytes(NexEvent)(msg.data).pipe(
                Effect.tapError((err) =>
                  Effect.log(`Event decode error: ${err.message}`)
                ),
                Effect.option,
              )
            ),
            Stream.filterMap((opt) => opt),
          )
        })

      // Watch for specific event types
      const watchWorkloadStarted = () =>
        Effect.gen(function* () {
          const subject = `$NEX.FEED.${namespace}.event.WorkloadStarted`
          const sub = yield* Effect.tryPromise(() => nats.core.subscribe(subject))

          return Stream.fromAsyncIterable(
            sub[Symbol.asyncIterator](),
            (e) => e as Error
          ).pipe(
            Stream.mapEffect((msg: Msg) =>
              decoder.decodeBytes(WorkloadStartedEvent)(msg.data).pipe(Effect.option)
            ),
            Stream.filterMap((opt) => opt),
          )
        })

      const watchWorkloadStopped = () =>
        Effect.gen(function* () {
          const subject = `$NEX.FEED.${namespace}.event.WorkloadStopped`
          const sub = yield* Effect.tryPromise(() => nats.core.subscribe(subject))

          return Stream.fromAsyncIterable(
            sub[Symbol.asyncIterator](),
            (e) => e as Error
          ).pipe(
            Stream.mapEffect((msg: Msg) =>
              decoder.decodeBytes(WorkloadStoppedEvent)(msg.data).pipe(Effect.option)
            ),
            Stream.filterMap((opt) => opt),
          )
        })

      // Subscribe to workload logs (plain text)
      const watchLogs = (workloadId?: string) =>
        Effect.gen(function* () {
          const subject = workloadId
            ? `$NEX.FEED.${namespace}.logs.${workloadId}.>`
            : `$NEX.FEED.${namespace}.logs.>`

          const sub = yield* Effect.tryPromise(() => nats.core.subscribe(subject))

          return Stream.fromAsyncIterable(
            sub[Symbol.asyncIterator](),
            (e) => e as Error
          ).pipe(
            Stream.map((msg: Msg) => {
              const parts = msg.subject.split('.')
              return {
                workloadId: parts[4] ?? 'unknown',
                stream: msg.subject.endsWith('.out') ? 'stdout' as const : 'stderr' as const,
                data: new TextDecoder().decode(msg.data),
                timestamp: new Date(),
              }
            })
          )
        })

      return {
        watchEvents,
        watchWorkloadStarted,
        watchWorkloadStopped,
        watchLogs,
      } as const
    }),
    dependencies: [NatsInnerService.Default, MessageDecoder.Default],
  }
) {}
```

---

## NATS Subject Patterns

| Subject | Purpose | Direction |
|---------|---------|-----------|
| `$NEX.SVC.<ns>.control.AUCTION` | Workload placement | Request |
| `$NEX.SVC.<ns>.control.AUCTIONDEPLOY.<bid>` | Deploy to winner | Request |
| `$NEX.SVC.<ns>.workloads.LIST` | List workloads | Request |
| `$NEX.SVC.<ns>.workloads.STOP` | Stop workload | Publish |
| `$NEX.FEED.<ns>.event.*` | Lifecycle events | Subscribe |
| `$NEX.FEED.<ns>.logs.<wid>.out` | Stdout | Subscribe |
| `$NEX.FEED.<ns>.logs.<wid>.err` | Stderr | Subscribe |
| `$NEX.FEED.<ns>.metrics.<wid>` | Metrics | Subscribe |

---

## Workload Environment Variables

NEX injects these into every workload:

| Variable | Description |
|----------|-------------|
| `NEX_WORKLOAD_NATS_SERVERS` | NATS server URLs |
| `NEX_WORKLOAD_NATS_NKEY` | NKey for auth |
| `NEX_WORKLOAD_NATS_B64_JWT` | Base64-encoded JWT |
| `NEX_WORKLOAD_ID` | Unique workload ID |
| `NEX_NAMESPACE` | Current namespace |
| `NEX_NODE_ID` | Host node ID |

### Using Credentials in Effect Service

```typescript
// src/lib/nex/workload-nats.ts

import { Effect, Schema, Config } from 'effect'
import { connect, jwtAuthenticator } from 'nats'

// Config from environment
const NexWorkloadConfig = Schema.Struct({
  servers: Schema.String,
  nkey: Schema.String,
  jwt: Schema.String,
  workloadId: Schema.String,
})

// Create NATS connection using NEX-provided credentials
export const createWorkloadNats = Effect.gen(function* () {
  const servers = yield* Config.string('NEX_WORKLOAD_NATS_SERVERS')
  const nkey = yield* Config.string('NEX_WORKLOAD_NATS_NKEY')
  const jwtB64 = yield* Config.string('NEX_WORKLOAD_NATS_B64_JWT')

  const jwt = Buffer.from(jwtB64, 'base64').toString()

  const nc = yield* Effect.tryPromise({
    try: () => connect({
      servers: servers.split(','),
      authenticator: jwtAuthenticator(jwt, new TextEncoder().encode(nkey)),
    }),
    catch: (e) => new Error(`Failed to connect: ${e}`),
  })

  yield* Effect.log(`Connected to NATS as workload`)

  return nc
})
```

---

## Credential Scoping

Workloads receive limited NATS permissions:

| Permission | Subject | Purpose |
|------------|---------|---------|
| Publish | `_INBOX.>` | Request-reply responses |
| Subscribe | `logs.{namespace}.>` | Workload-specific logs |
| Subscribe | `_INBOX.>` | Receive request-reply |
| Response | 1 per request | Rate limiting |

This prevents workloads from:
- Publishing to arbitrary subjects
- Subscribing to other workloads' traffic
- Flooding the system with messages

---

## Best Practices

### 1. Always Use MessageDecoder

```typescript
// ❌ WRONG - manual JSON handling
const data = JSON.parse(new TextDecoder().decode(msg.data))

// ✅ CORRECT - Effect-native decoding
const data = yield* decoder.decodeBytes(MySchema)(msg.data)
```

### 2. Handle Decode Errors Gracefully

```typescript
// In streams, convert failures to Option
Stream.mapEffect((msg) =>
  decoder.decodeBytes(MySchema)(msg.data).pipe(
    Effect.tapError((err) => Effect.log(`Decode error: ${err.message}`)),
    Effect.option,
  )
),
Stream.filterMap((opt) => opt), // Filter out failures
```

### 3. Define Schemas at Module Level

```typescript
// ✅ Define once at module level
const MyEvent = Schema.TaggedStruct('MyEvent', {
  id: Schema.String,
  timestamp: Schema.DateFromString,
})

// ❌ Don't define inside functions
const handler = () => {
  const MyEvent = Schema.Struct({ ... }) // Bad - recreated every call
}
```

### 4. Use Tagged Errors

```typescript
// ✅ Tagged errors for type-safe error handling
export class NexError extends Data.TaggedError('NexError')<{
  readonly message: string
  readonly operation: string
}> {}

// ❌ Don't throw plain Error
throw new Error('Something went wrong')
```

---

## Related Skills

- `/nex-codebase-navigation` - Source code exploration
- `/nex-cli-guide` - CLI reference
- `/iiot-unified-namespace` - UNS + NATS patterns
- `/effect-service-authoring` - Effect service patterns
- `/effect-stream-patterns` - Stream processing

## References

- [NEX GitHub](https://github.com/synadia-io/nex)
- [NATS.js Documentation](https://github.com/nats-io/nats.js)
- [Effect-TS Schema](https://effect.website/docs/schema)
