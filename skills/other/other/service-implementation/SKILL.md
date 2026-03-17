---
name: service-implementation
description: Implement Effect services as fine-grained capabilities avoiding monolithic designs
---

# Service Implementation Skill

Design and implement Effect services as focused capabilities that compose into complete solutions.

## Anti-Pattern: Monolithic Services

```typescript
// ❌ WRONG - Mixed concerns in one service
export class PaymentService extends Context.Tag("PaymentService")<
  PaymentService,
  {
    readonly processPayment: ...
    readonly validateWebhook: ...
    readonly refund: ...
    readonly sendReceipt: ...       // Notification concern
    readonly generateReport: ...    // Reporting concern
  }
>() {}
```

## Pattern: Capability-Based Services

Each service represents ONE cohesive capability:

```typescript
// ✅ CORRECT - Focused capabilities

export class PaymentGateway extends Context.Tag(
  "@services/payment/PaymentGateway"
)<
  PaymentGateway,
  {
    readonly handoff: (
      intent: Doc<"paymentIntents">
    ) => Effect.Effect<HandoffResult, HandoffError, never>
    //                                                 ▲
    //                                    No requirements leaked
  }
>() {}

export class PaymentWebhookGateway extends Context.Tag(
  "@services/payment/PaymentWebhookGateway"
)<
  PaymentWebhookGateway,
  {
    readonly validateWebhook: (
      payload: WebhookPayload
    ) => Effect.Effect<void, WebhookValidationError, never>
  }
>() {}

export class PaymentRefundGateway extends Context.Tag(
  "@services/payment/PaymentRefundGateway"
)<
  PaymentRefundGateway,
  {
    readonly refund: (
      paymentId: PaymentId,
      amount: Cents
    ) => Effect.Effect<RefundResult, RefundError, never>
  }
>() {}
```

## Pattern: No Requirement Leakage

Service operations should **never** have requirements:

```typescript
// The service interface stays clean
export class Database extends Context.Tag("Database")<
  Database,
  {
    readonly query: (
      sql: string
    ) => Effect.Effect<QueryResult, QueryError, never>
    //                                             ▲
    //                                  Requirements = never
  }
>() {}
```

Dependencies are handled during **layer construction**, not in the service interface:

```typescript
// Dependencies live in the layer
export const DatabaseLive = Layer.effect(
  Database,
  Effect.gen(function* () {
    const config = yield* Config    // Dependency
    const logger = yield* Logger    // Dependency

    return Database.of({
      query: (sql) =>
        Effect.gen(function* () {
          yield* logger.log(`Executing: ${sql}`)
          const { connection } = yield* config.getConfig
          return executeQuery(connection, sql)
        })
    })
  })
)
```

## Pattern: Composing Capabilities

Different implementations support different capabilities:

```typescript
// Cash payments: Basic handoff only
export const CashGatewayLive = Layer.succeed(
  PaymentGateway,
  PaymentGateway.of({
    handoff: (intent) => fulfillCashPayment(intent)
  })
)

// Stripe: Full capability suite
export const StripeGatewayLive = Layer.mergeAll(
  StripeHandoffLive,      // Implements PaymentGateway
  StripeWebhookLive,      // Implements PaymentWebhookGateway
  StripeRefundLive        // Implements PaymentRefundGateway
)
```

## Pattern: Optional Capabilities

Use `Effect.serviceOption` for capabilities that may not be available:

```typescript
const processPayment = (order: Order) =>
  Effect.gen(function* () {
    const handoff = yield* PaymentGateway
    const result = yield* handoff.handoff(order.paymentIntent)

    // Optional capability - check if available
    const refundGateway = yield* Effect.serviceOption(PaymentRefundGateway)

    if (Option.isSome(refundGateway)) {
      yield* setupRefundPolicy(refundGateway.value, order)
    }

    return result
  })
```

## Testing Benefits

Each capability can be tested in isolation:

```typescript
const TestWebhook = Layer.succeed(
  PaymentWebhookGateway,
  PaymentWebhookGateway.of({
    validateWebhook: (payload) =>
      payload.signature === "valid"
        ? Effect.succeed(undefined)
        : Effect.fail(new WebhookValidationError({ reason: "Invalid" }))
  })
)

// Test only webhook validation, no other payment concerns
const testProgram = handleWebhook(payload).pipe(
  Effect.provide(TestWebhook)
)
```

## Naming Convention

Use descriptive capability names:
- `*Gateway` - External system integration
- `*Repository` - Data persistence
- `*Domain` - Business logic
- `*Service` - General capability (use sparingly)

Tag identifiers should include namespace:
- `"@services/payment/PaymentGateway"`
- `"@repositories/user/UserRepository"`
- `"@domain/order/OrderDomain"`

## Quality Checklist

- [ ] Service represents single capability
- [ ] All operations have Requirements = never
- [ ] Tagged with descriptive namespace
- [ ] Dependencies handled in layer
- [ ] Can be tested in isolation
- [ ] Can be composed with other capabilities
- [ ] JSDoc with purpose and usage

Keep services focused, composable, and free of leaked requirements.
