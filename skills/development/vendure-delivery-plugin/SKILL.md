---
name: vendure-delivery-plugin
description: Build delivery and fulfillment plugins for Vendure with idempotency, capacity management, timezone handling, and N+1 prevention. Covers ShippingCalculator, FulfillmentHandler, and slot reservation patterns. Use when implementing delivery features.
version: 1.0.0
---

# Vendure Delivery Plugin

## Purpose

Guide creation of delivery and fulfillment features in Vendure with production-grade patterns for concurrency, performance, and reliability.

## When NOT to Use

- Generic plugin structure (use vendure-plugin-writing)
- Simple CRUD operations (use vendure-entity-writing)
- Standard GraphQL endpoints (use vendure-graphql-writing)

---

## CRITICAL Patterns

For detailed critical patterns with code examples:
- Idempotency for Slot Operations
- Pessimistic Locking for Capacity
- UTC Timezone Storage
- N+1 Query Prevention

See `references/CRITICAL-PATTERNS.md` for complete implementations.

## Shop API & Entity Patterns

For detailed Shop API patterns (IDOR prevention, customer-facing resolvers) and Entity patterns, see `references/API-ENTITY-PATTERNS.md`.

## GraphQL Schema

```typescript
export const deliveryShopSchema = gql`
  type AvailableDeliverySlotsResponse {
    availableSlots: [DeliveryTimeBlock!]!
    cutoffTime: String!
    blackoutDates: [DateTime!]!
  }

  type DeliveryTimeBlock {
    id: ID!
    startTime: String!
    endTime: String!
    fee: Int!
    currencyCode: String!
    remainingCapacity: Int
  }

  extend type Query {
    availableDeliveryTimeBlocks(
      date: DateTime!
      timezone: String
    ): AvailableDeliverySlotsResponse!

    isDeliveryTimeBlockAvailable(
      timeBlockId: ID!
      date: DateTime!
      timezone: String
    ): Boolean!

    isDeliveryAvailableForAddress(city: String!): Boolean!
  }

  extend type Mutation {
    setOrderDeliveryTimeBlock(
      orderId: ID!
      timeBlockId: ID!
      deliveryDate: DateTime!
      timezone: String
    ): Order!

    releaseOrderDeliveryTimeBlock(orderId: ID!): Order!
  }
`;
```

---

## Idempotency Interceptor

```typescript
@Injectable()
export class IdempotencyInterceptor implements NestInterceptor {
  intercept(context: ExecutionContext, next: CallHandler): Observable<unknown> {
    const gqlContext = GqlExecutionContext.create(context);
    const ctx = gqlContext.getContext().req;

    // Extract X-Idempotency-Key header
    const idempotencyKey = ctx.headers?.["x-idempotency-key"];

    if (idempotencyKey) {
      // Attach to RequestContext for service use
      (ctx as IdempotentRequestContext).idempotencyKey = idempotencyKey;
      (ctx as IdempotentRequestContext).graphqlArgs = gqlContext.getArgs();
    }

    return next.handle();
  }
}
```

---

## Testing Patterns

```typescript
describe("DeliveryReservationService", () => {
  it("should prevent double booking with pessimistic lock", async () => {
    // Create time block with capacity 1
    const block = await createTimeBlock({ maxDeliveries: 1 });

    // Simulate concurrent requests
    const [result1, result2] = await Promise.allSettled([
      service.reserveSlot(ctx, order1.id, block.id, date),
      service.reserveSlot(ctx, order2.id, block.id, date),
    ]);

    // One should succeed, one should fail
    const successes = [result1, result2].filter(
      (r) => r.status === "fulfilled",
    );
    const failures = [result1, result2].filter((r) => r.status === "rejected");

    expect(successes).toHaveLength(1);
    expect(failures).toHaveLength(1);
  });

  it("should handle idempotent requests", async () => {
    const key = "unique-key-123";
    const hash = service.generateRequestHash({ orderId: order.id });

    // First request succeeds
    await service.reserveSlot(ctx, order.id, block.id, date, key, hash);

    // Second request with same key returns cached response
    const result2 = await service.reserveSlot(
      ctx,
      order.id,
      block.id,
      date,
      key,
      hash,
    );
    expect(result2).toBe(true);
  });
});
```

---

## Troubleshooting

| Problem                    | Cause                    | Solution                             |
| -------------------------- | ------------------------ | ------------------------------------ |
| Race condition on booking  | Missing pessimistic lock | Use `setLock('pessimistic_write')`   |
| Wrong date in different TZ | Storing local time       | Always convert to UTC for storage    |
| Slow slot availability     | N+1 queries              | Use batch counting with GROUP BY     |
| Duplicate reservations     | Missing idempotency      | Implement X-Idempotency-Key handling |
| IDOR vulnerability         | No ownership check       | Call `verifyOrderOwnership()` first  |

---

## Related Skills

- **vendure-plugin-writing** - Plugin structure
- **vendure-entity-writing** - Entity patterns
- **vendure-graphql-writing** - GraphQL patterns
