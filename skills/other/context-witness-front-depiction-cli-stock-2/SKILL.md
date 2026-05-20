---
name: context-witness
description: Decide between Context Tag witness and capability patterns for dependency injection, understanding coupling trade-offs
---

# Context Witness Pattern

Choose between witness (existence) and capability (behavior) patterns for Context Tags.

## Coupling: Hard vs Soft

**Some coupling is necessary and good** - but move it from hard to soft coupling.

### Hard Coupling (Schema)

Field exists in the schema - tightly coupled to domain model:

```typescript
// ❌ HARD COUPLING - Serial is part of the schema
export const PaymentIntent = Schema.Struct({
  id: Schema.String,
  serial: Schema.String,  // In schema = hard coupled
  amount: Schema.BigInt
})

// Every PaymentIntent MUST have a serial
// Serialization/validation requires serial
// Cannot create without providing serial
// Schema change needed to remove/change serial
```

### Soft Coupling (Witness)

Field **removed from schema**, only injected in code:

```typescript
// ✅ SOFT COUPLING - Serial not in schema
export const PaymentIntent = Schema.Struct({
  id: Schema.String,
  amount: Schema.BigInt
  // No serial field!
})

// Serial is a witness - required but injected via Context
class Serial extends Context.Tag("Serial")<Serial, string>() {}

const createPaymentIntent = (amount: bigint) =>
  Effect.gen(function* () {
    const serial = yield* Serial  // Injected from context

    // Use serial in business logic, logging, etc.
    // but it's not part of the persisted data
    yield* Logger.info(`Creating payment intent ${serial}`)

    return PaymentIntent.make({ id: generateId(), amount })
  })

// Type: Effect<PaymentIntent, never, Serial>
```

**Key insight:** `schema (hard coupling) => witness (soft coupling)`

By removing the field from the schema and injecting it only where needed, you:
- Keep domain models minimal
- Avoid unnecessary persistence
- Easy to test (provide test serial)
- Easy to remove/change (just change injection)
- Explicit dependencies in type signature

**When to use witnesses:**
- Correlation IDs (for tracing, not persistence)
- Request IDs (for logging, not data)
- Transaction contexts (for coordination, not storage)
- Tenant/Region markers (for routing, not schema)

## Witness: Existence Only

Use when you only need to know something **exists** in the environment:

```typescript
// Witness - a serial number exists
export class Serial extends Context.Tag("Serial")<Serial, string>() {}

const createPaymentIntent = Effect.gen(function* () {
  const serial = yield* Serial  // Pull from environment
  return PaymentIntent.make({ serial, ...other })
})

// Type: Effect<PaymentIntent, never, Serial>
```

## Capability: Behavior

Use when you need **operations**:

```typescript
// Capability - can generate/validate
export class SerialService extends Context.Tag("SerialService")<
  SerialService,
  {
    readonly next: () => string
    readonly validate: (s: string) => boolean
  }
>() {}

const createPaymentIntent = Effect.gen(function* () {
  const svc = yield* SerialService
  const serial = svc.next()  // Behavior
  return PaymentIntent.make({ serial, ...other })
})

// Type: Effect<PaymentIntent, never, SerialService>
```

## Decision Framework

| Need | Pattern |
|------|---------|
| Just presence/value | Witness |
| Operations/generation | Capability |
| Precondition marker | Witness |
| Side effects | Capability |
| Multiple implementations | Capability |
| Mocking behavior | Capability |
| Correlation ID | Witness |
| Transaction context | Witness |
| Logger | Capability |
| Database | Capability |

## When to Use Witness

Good fits:
- **Request ID** - must exist for tracing
- **Transaction context** - must be established
- **Tenant/Region** - required for data boundary
- **Pre-validated tokens** - already verified

## When to Use Capability

Good fits:
- **Serial generation** - create/validate operations
- **Clock** - `now()` operation
- **Logger** - structured logging methods
- **Database** - query/transact operations
- **HTTP clients** - fetch/post operations

## Testing Implications

Witnesses are trivial to provide:
```typescript
const test = myProgram.pipe(
  Effect.provideService(Serial, "test-serial-123")
)
```

Capabilities need implementation:
```typescript
const test = myProgram.pipe(
  Effect.provideService(SerialService, {
    next: () => "test-serial-123",
    validate: () => true
  })
)
```

## Coupling Strategy

**Rule of thumb**: Remove non-essential fields from schema, inject via witness instead.

**Ask yourself:** Does this need to be persisted/serialized?
- **No** → Remove from schema, inject via witness
- **Yes** → Keep in schema

```typescript
// ✅ Domain model - only persisted data
export const Order = Schema.Struct({
  id: Schema.String,
  items: Schema.Array(LineItem),
  total: Schema.BigInt
  // No correlationId - not persisted!
  // No timestamp - derived from system!
})

// Witnesses for runtime context
class CorrelationId extends Context.Tag("CorrelationId")<CorrelationId, string>() {}
class RequestId extends Context.Tag("RequestId")<RequestId, string>() {}

// Use in code, not in data
const createOrder = (items: Array<LineItem>) =>
  Effect.gen(function* () {
    const correlationId = yield* CorrelationId  // For tracing
    const requestId = yield* RequestId          // For logging
    const clock = yield* Clock                  // For timestamp

    yield* Logger.info({
      message: "Creating order",
      correlationId,    // Used for tracing
      requestId,        // Used for logging
      timestamp: Clock.currentTimeMillis(clock)
    })

    // Data only contains what's persisted
    return Order.make({
      id: generateId(),
      items,
      total: calculateTotal(items)
    })
  })

// Type: Effect<Order, never, CorrelationId | RequestId | Clock>
```

**Benefits:**
- Minimal schemas (only persisted data)
- Context values available when needed
- Easy to test with different context
- Can add/remove context without schema changes
- Explicit dependencies in type signatures

Choose witness for simplicity, capability for flexibility.
