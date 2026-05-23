---
name: implement-choreography
description: "Step-by-step guide for implementing choreography patterns with event bus, idempotent consumers, correlation ID propagation, and query views."
---

# Skill: Implement Choreography Pattern

This skill teaches choreography pattern implementation following  principles. In choreography, there is no central coordinator - each service reacts to events and publishes its own. The workflow emerges from the chain of reactions between independent services.

Choreography provides maximum autonomy. Producers don't know consumers - adding new consumers requires no producer changes. This autonomy requires strong observability through correlation IDs and idempotent consumers.

## Prerequisites

- Understanding of DDD and event-driven architecture
- Familiarity with message brokers and event buses
- Database for idempotency tracking

## Overview

1. Identify event flow between services
2. Design events for each service
3. Implement event publishers
4. Implement idempotent consumers
5. Add correlation ID propagation
6. Build query view for progress
7. Test event chains

## Step 1: Identify the Event Flow

Map the event chain showing how services react and what they produce.

```text
OrderService publishes:  order.placed { orderId, items }
    |
PaymentService reacts -> publishes: payment.succeeded OR payment.failed
    |
 InventoryService reacts -> publishes: inventory.reserved
    |
ShippingService reacts -> publishes: shipment.scheduled

All events share correlationId for distributed tracing.
```

Key principles:
- Each service only knows events it consumes and produces
- Services communicate through events, not direct calls
- Correlation ID ties all events together

### Define Event Types

```pseudocode
// EventEnvelope wraps domain events with routing metadata
TYPE EventEnvelope
    eventId: String
    eventType: String
    schemaVersion: String
    occurredAt: Timestamp
    aggregateId: String
    correlationId: String
    causationId: String
    payload: Any

CONSTRUCTOR NewEventEnvelope(eventType: String, aggregateId: String, correlationId: String, payload: Any) RETURNS EventEnvelope
    RETURN EventEnvelope{
        eventId: GenerateUUID(),
        eventType: eventType,
        schemaVersion: "1.0.0",
        occurredAt: CurrentTimestamp(),
        aggregateId: aggregateId,
        correlationId: correlationId,
        payload: payload
    }
END CONSTRUCTOR

METHOD EventEnvelope.WithCausation(causationId: String) RETURNS EventEnvelope
    this.causationId = causationId
    RETURN this
END METHOD

// Domain events
TYPE OrderPlaced
    orderId: String
    customerId: String
    totalCents: Integer

TYPE PaymentSucceeded
    orderId: String
    paymentId: String
    amountCents: Integer

TYPE InventoryReserved
    orderId: String
    reservationId: String
    expiresAt: Timestamp

TYPE ShipmentScheduled
    orderId: String
    shipmentId: String
    carrier: String
```

## Step 2: Design Event Bus Infrastructure

```pseudocode
// Event routing rules configuration
TYPE EventBusConfig
    busName: String
    rules: List<EventRule>

TYPE EventRule
    name: String
    source: String
    eventType: String
    target: String

// Example configuration
CONSTANT OrderEventBusConfig = EventBusConfig{
    busName: "orders-event-bus",
    rules: [
        // Route order.placed to Payment Service
        EventRule{
            name: "order-placed-to-payment",
            source: "order-service",
            eventType: "order.placed",
            target: "payment-handler"
        },
        // Route payment.succeeded to Inventory Service
        EventRule{
            name: "payment-to-inventory",
            source: "payment-service",
            eventType: "payment.succeeded",
            target: "inventory-handler"
        },
        // Route inventory.reserved to Shipping Service
        EventRule{
            name: "inventory-to-shipping",
            source: "inventory-service",
            eventType: "inventory.reserved",
            target: "shipping-handler"
        }
    ]
}
```

## Step 3: Implement Event Publishers

```pseudocode
// Publisher sends events to the event bus
INTERFACE EventBusClient
    METHOD PutEvents(ctx: Context, input: PutEventsInput) RETURNS Result<PutEventsOutput, Error>

TYPE Publisher
    client: EventBusClient
    eventBusName: String
    source: String

CONSTRUCTOR NewPublisher(client: EventBusClient, busName: String, source: String) RETURNS Publisher
    RETURN Publisher{
        client: client,
        eventBusName: busName,
        source: source
    }
END CONSTRUCTOR

METHOD Publisher.Publish(ctx: Context, envelope: EventEnvelope) RETURNS Result<Void, Error>
    detail = SerializeJSON(envelope)

    result = this.client.PutEvents(ctx, PutEventsInput{
        entries: [
            PutEventsEntry{
                eventBusName: this.eventBusName,
                source: this.source,
                detailType: envelope.eventType,
                detail: detail,
                time: envelope.occurredAt
            }
        ]
    })

    IF result.IsError() THEN
        RETURN Error("put events: " + result.Error())
    END IF

    IF result.Value().FailedEntryCount > 0 THEN
        RETURN Error("publish failed: " + result.Value().Entries[0].ErrorMessage)
    END IF

    RETURN Ok()
END METHOD
```

### Order Service Example

```pseudocode
TYPE CreateOrderRequest
    customerId: String
    totalCents: Integer

TYPE CreateOrderResponse
    orderId: String
    correlationId: String

FUNCTION HandleCreateOrder(ctx: Context, req: CreateOrderRequest) RETURNS Result<CreateOrderResponse, Error>
    orderId = GenerateUUID()
    correlationId = GenerateUUID()

    envelope = NewEventEnvelope("order.placed", orderId, correlationId,
        OrderPlaced{
            orderId: orderId,
            customerId: req.customerId,
            totalCents: req.totalCents
        }
    )

    publishResult = publisher.Publish(ctx, envelope)
    IF publishResult.IsError() THEN
        RETURN Error(publishResult.Error())
    END IF

    RETURN Ok(CreateOrderResponse{orderId: orderId, correlationId: correlationId})
END FUNCTION
```

## Step 4: Implement Idempotent Consumers

Consumers must handle duplicate events safely using event ID for deduplication.

### Idempotency Store

```pseudocode
// IdempotencyStore tracks processed events
INTERFACE DataStoreClient
    METHOD GetItem(ctx: Context, input: GetItemInput) RETURNS Result<GetItemOutput, Error>
    METHOD PutItem(ctx: Context, input: PutItemInput) RETURNS Result<Void, Error>

TYPE IdempotencyStore
    client: DataStoreClient
    tableName: String

CONSTRUCTOR NewIdempotencyStore(client: DataStoreClient, tableName: String) RETURNS IdempotencyStore
    RETURN IdempotencyStore{client: client, tableName: tableName}
END CONSTRUCTOR

METHOD IdempotencyStore.AlreadyProcessed(ctx: Context, eventId: String) RETURNS Result<Boolean, Error>
    result = this.client.GetItem(ctx, GetItemInput{
        tableName: this.tableName,
        key: {"PK": "EVENT#" + eventId}
    })

    IF result.IsError() THEN
        RETURN Error(result.Error())
    END IF

    RETURN Ok(result.Value().Item != NULL)
END METHOD

METHOD IdempotencyStore.MarkProcessed(ctx: Context, eventId: String, eventType: String) RETURNS Result<Void, Error>
    ttl = CurrentTimestamp().AddDays(7).Unix()

    result = this.client.PutItem(ctx, PutItemInput{
        tableName: this.tableName,
        item: {
            "PK": "EVENT#" + eventId,
            "event_type": eventType,
            "ttl": ttl
        },
        conditionExpression: "attribute_not_exists(PK)"
    })

    RETURN result
END METHOD
```

### Payment Service Consumer

```pseudocode
// Payment Service handles order.placed events
FUNCTION HandleOrderPlacedEvent(ctx: Context, rawEvent: RawEvent) RETURNS Result<Void, Error>
    envelope = DeserializeJSON<EventEnvelope>(rawEvent.Detail)

    // Idempotency check
    alreadyResult = idempotencyStore.AlreadyProcessed(ctx, envelope.eventId)
    IF alreadyResult.IsOk() AND alreadyResult.Value() == true THEN
        Logger.Info(ctx, "skipping duplicate", "event_id", envelope.eventId)
        RETURN Ok()
    END IF

    orderPlaced = DeserializeJSON<OrderPlaced>(envelope.payload)

    Logger.Info(ctx, "processing payment",
        "correlation_id", envelope.correlationId,
        "order_id", orderPlaced.orderId
    )

    // Process payment logic here...
    paymentId = GenerateUUID()

    // Publish result with same correlation ID
    resultEvent = NewEventEnvelope("payment.succeeded", orderPlaced.orderId, envelope.correlationId,
        PaymentSucceeded{
            orderId: orderPlaced.orderId,
            paymentId: paymentId,
            amountCents: orderPlaced.totalCents
        }
    ).WithCausation(envelope.eventId)

    publishResult = publisher.Publish(ctx, resultEvent)
    IF publishResult.IsError() THEN
        RETURN Error("publish result: " + publishResult.Error())
    END IF

    idempotencyStore.MarkProcessed(ctx, envelope.eventId, envelope.eventType)

    RETURN Ok()
END FUNCTION
```

## Step 5: Add Correlation ID Propagation

```pseudocode
// Context key for correlation ID
TYPE contextKey = String
CONSTANT correlationIDKey contextKey = "correlation_id"

FUNCTION WithCorrelationID(ctx: Context, id: String) RETURNS Context
    RETURN ctx.WithValue(correlationIDKey, id)
END FUNCTION

FUNCTION CorrelationID(ctx: Context) RETURNS String
    value = ctx.Value(correlationIDKey)
    IF value IS String THEN
        RETURN value
    END IF
    RETURN ""
END FUNCTION

FUNCTION LoggerWithCorrelation(ctx: Context) RETURNS Logger
    RETURN DefaultLogger().With("correlation_id", CorrelationID(ctx))
END FUNCTION
```

## Step 6: Build Query View for Workflow Progress

Since choreography has no central coordinator, build a projection to track progress.

```pseudocode
// OrderStatusView tracks order progress across all services
TYPE OrderStatusView
    orderId: String
    correlationId: String
    status: String
    events: List<String>

TYPE OrderStatusProjection
    client: DataStoreClient
    tableName: String

CONSTRUCTOR NewOrderStatusProjection(client: DataStoreClient, table: String) RETURNS OrderStatusProjection
    RETURN OrderStatusProjection{client: client, tableName: table}
END CONSTRUCTOR

METHOD OrderStatusProjection.Handle(ctx: Context, envelope: EventEnvelope) RETURNS Result<Void, Error>
    orderId = envelope.aggregateId

    updateExpr = "SET correlation_id = :cid, last_updated = :ts, #events = list_append(if_not_exists(#events, :empty), :evt)"
    exprNames = {"#events": "events"}
    exprValues = {
        ":cid": envelope.correlationId,
        ":ts": FormatTimestamp(CurrentTimestamp()),
        ":evt": [envelope.eventType],
        ":empty": []
    }

    statusMap = {
        "order.placed": "pending_payment",
        "payment.succeeded": "pending_inventory",
        "inventory.reserved": "pending_shipping",
        "shipment.scheduled": "shipped"
    }

    IF statusMap.Contains(envelope.eventType) THEN
        updateExpr = updateExpr + ", #status = :status"
        exprNames["#status"] = "status"
        exprValues[":status"] = statusMap[envelope.eventType]
    END IF

    result = this.client.UpdateItem(ctx, UpdateItemInput{
        tableName: this.tableName,
        key: {
            "PK": "ORDER#" + orderId,
            "SK": "STATUS"
        },
        updateExpression: updateExpr,
        expressionAttributeNames: exprNames,
        expressionAttributeValues: exprValues
    })

    RETURN result
END METHOD

METHOD OrderStatusProjection.Get(ctx: Context, orderId: String) RETURNS Result<OrderStatusView, Error>
    result = this.client.GetItem(ctx, GetItemInput{
        tableName: this.tableName,
        key: {
            "PK": "ORDER#" + orderId,
            "SK": "STATUS"
        }
    })

    IF result.IsError() OR result.Value().Item == NULL THEN
        RETURN Error("order not found: " + orderId)
    END IF

    view = UnmarshalOrderStatusView(result.Value().Item)
    RETURN Ok(view)
END METHOD
```

## Step 7: Test Event Chains

```pseudocode
// Test: Full order fulfillment choreography
TEST OrderFulfillmentChoreography
    ctx = Context.Background()
    orderId = "test-order-123"
    correlationId = "test-corr-456"

    envelope = NewEventEnvelope("order.placed", orderId, correlationId,
        OrderPlaced{
            orderId: orderId,
            customerId: "cust-789",
            totalCents: 2000
        }
    )

    publishResult = publisher.Publish(ctx, envelope)
    ASSERT publishResult.IsOk()

    // Wait for event chain to complete
    status = NULL
    FOR i = 0; i < 30; i++ DO
        Sleep(1 * Second)
        statusResult = projection.Get(ctx, orderId)
        IF statusResult.IsOk() AND statusResult.Value().status == "shipped" THEN
            status = statusResult.Value()
            BREAK
        END IF
    END FOR

    ASSERT status != NULL
    ASSERT status.status == "shipped"
    ASSERT status.correlationId == correlationId
END TEST

// Test: Idempotent consumer handles duplicate events
TEST IdempotentConsumer
    ctx = Context.Background()

    envelope = NewEventEnvelope("order.placed", "idem-order", "corr-1",
        OrderPlaced{
            orderId: "idem-order",
            customerId: "c1",
            totalCents: 1000
        }
    )

    // Publish same event 3 times
    FOR i = 0; i < 3; i++ DO
        result = publisher.Publish(ctx, envelope)
        ASSERT result.IsOk()
    END FOR

    Sleep(5 * Second)

    statusResult = projection.Get(ctx, "idem-order")
    status = statusResult.Value()

    // Count occurrences of order.placed in events list
    count = 0
    FOR EACH e IN status.events DO
        IF e == "order.placed" THEN
            count = count + 1
        END IF
    END FOR

    ASSERT count == 1, "event processed only once"
END TEST
```

## Verification Checklist

After implementing choreography, verify:

- [ ] Each service only knows events it consumes and produces
- [ ] No service knows the complete workflow - it emerges from event chains
- [ ] Correlation ID flows through all events in the chain
- [ ] Causation ID links each event to its triggering event
- [ ] All consumers are idempotent using event ID for deduplication
- [ ] Events are facts (past tense) not commands
- [ ] Event payloads contain all data consumers need
- [ ] Query view provides visibility into workflow progress
- [ ] Schema versioning follows semver rules
- [ ] Failed events logged with correlation ID for debugging
- [ ] Event routing rules route events to correct consumers
- [ ] Dead letter queues capture unprocessable events
