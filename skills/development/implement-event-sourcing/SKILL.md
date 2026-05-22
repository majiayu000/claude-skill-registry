---
name: implement-event-sourcing
description: "Step-by-step guide for implementing event sourcing with event store, aggregate replay, snapshots, projections, and schema evolution."
tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
context:
  - docs/architecture
  - docs/patterns
---

# Skill: Implement Event Sourcing

This skill teaches event sourcing following  patterns. Event sourcing stores all state changes as an append-only log of immutable events - current state is computed by replaying events. History is never lost, and projections can be rebuilt anytime.

## Prerequisites

- Understanding of DDD aggregates and Clean Architecture
- Knowledge of the Aggregate Root Pattern and consistency boundaries
- Familiarity with event-driven architecture principles
- Understanding of CQRS pattern and read/write model separation
- Database configured for event storage

## Overview

1. Design event stream structure
2. Create event store (stream ID as PK, version as SK)
3. Implement aggregate with event replay
4. Add snapshots for performance
5. Build projections from events
6. Handle event versioning (schema evolution)
7. Test replay and projections

## Step 1: Design the Event Stream Structure

```pseudocode
// Pattern: Domain Event Interface
// All domain events must implement this interface

INTERFACE Event
    METHOD EventID() RETURNS String
    METHOD EventType() RETURNS String
    METHOD AggregateID() RETURNS String
    METHOD AggregateType() RETURNS String
    METHOD Sequence() RETURNS Integer
    METHOD OccurredAt() RETURNS Timestamp
    METHOD SchemaVersion() RETURNS String
END INTERFACE

// Pattern: Base Event with common fields
// Embed in concrete events to provide common functionality

TYPE BaseEvent
    id: String
    type: String
    aggregateId: String
    aggregateType: String
    sequence: Integer
    occurred: Timestamp
    version: String
    correlationId: String

METHOD BaseEvent.EventID() RETURNS String
    RETURN this.id
END METHOD

METHOD BaseEvent.EventType() RETURNS String
    RETURN this.type
END METHOD

METHOD BaseEvent.AggregateID() RETURNS String
    RETURN this.aggregateId
END METHOD

METHOD BaseEvent.AggregateType() RETURNS String
    RETURN this.aggregateType
END METHOD

METHOD BaseEvent.Sequence() RETURNS Integer
    RETURN this.sequence
END METHOD

METHOD BaseEvent.OccurredAt() RETURNS Timestamp
    RETURN this.occurred
END METHOD

METHOD BaseEvent.SchemaVersion() RETURNS String
    RETURN this.version
END METHOD

CONSTRUCTOR NewBaseEvent(eventType: String, aggregateId: String, aggregateType: String, seq: Integer) RETURNS BaseEvent
    RETURN BaseEvent{
        id: GenerateUUID(),
        type: eventType,
        aggregateId: aggregateId,
        aggregateType: aggregateType,
        sequence: seq,
        occurred: CurrentTimestamp(),
        version: "1.0.0"
    }
END CONSTRUCTOR
```

### Stored Event Envelope

```pseudocode
// Pattern: Event Envelope separates routing from domain data
// StoredEvent is the persistence format

TYPE StoredEvent
    eventId: String
    eventType: String
    aggregateId: String
    aggregateType: String
    sequence: Integer
    occurredAt: Timestamp
    schemaVersion: String
    payload: RawJSON
    metadata: EventMetadata

TYPE EventMetadata
    correlationId: String
    causationId: String
    userId: String
```

## Step 2: Create the Event Store

```pseudocode
// Pattern: Event Store Port (Repository Pattern)
// Interface for event persistence - adapters implement this

INTERFACE EventStore
    METHOD Append(ctx: Context, events: List<StoredEvent>, expectedVersion: Integer) RETURNS Result<Void, Error>
    METHOD Load(ctx: Context, aggregateId: String, aggregateType: String, fromSequence: Integer) RETURNS Result<List<StoredEvent>, Error>
    METHOD LoadSnapshot(ctx: Context, aggregateId: String, aggregateType: String) RETURNS Result<Snapshot, Error>
    METHOD SaveSnapshot(ctx: Context, snapshot: Snapshot) RETURNS Result<Void, Error>
END INTERFACE

// Pattern: Optimistic Concurrency Control
CONSTANT ErrOptimisticConcurrency = Error("optimistic concurrency violation")

// Pattern: Single-Table Design for Event Store
// Data model: PK=STREAM#{type}#{id}, SK=SEQ#{sequence}

TYPE EventStoreImpl
    client: DataStoreClient
    tableName: String

TYPE eventItem
    pk: String              // STREAM#{type}#{id}
    sk: String              // SEQ#{sequence}
    eventId: String
    eventType: String
    aggregateId: String
    aggregateType: String
    sequence: Integer
    occurredAt: String
    schemaVersion: String
    payload: String

METHOD EventStoreImpl.Append(ctx: Context, events: List<StoredEvent>, expectedVersion: Integer) RETURNS Result<Void, Error>
    IF events.Length() == 0 THEN
        RETURN Ok()
    END IF

    transactItems = []
    FOR EACH event IN events DO
        item = eventItem{
            pk: "STREAM#" + event.aggregateType + "#" + event.aggregateId,
            sk: FormatPadded("SEQ#%020d", event.sequence),
            eventId: event.eventId,
            eventType: event.eventType,
            aggregateId: event.aggregateId,
            aggregateType: event.aggregateType,
            sequence: event.sequence,
            occurredAt: FormatTimestamp(event.occurredAt),
            schemaVersion: event.schemaVersion,
            payload: ToString(event.payload)
        }

        // Pattern: Conditional Write for Optimistic Concurrency
        transactItems.append(TransactWriteItem{
            put: PutItem{
                tableName: this.tableName,
                item: item,
                conditionExpression: "attribute_not_exists(PK)"
            }
        })
    END FOR

    result = this.client.TransactWriteItems(ctx, transactItems)
    IF result.IsError() THEN
        IF result.Error() IS TransactionCanceledException THEN
            RETURN ErrOptimisticConcurrency
        END IF
        RETURN Error("transact write: " + result.Error())
    END IF

    RETURN Ok()
END METHOD

METHOD EventStoreImpl.Load(ctx: Context, aggregateId: String, aggregateType: String, fromSequence: Integer) RETURNS Result<List<StoredEvent>, Error>
    pk = "STREAM#" + aggregateType + "#" + aggregateId

    result = this.client.Query(ctx, QueryInput{
        tableName: this.tableName,
        keyConditionExpression: "PK = :pk AND SK >= :sk",
        expressionAttributeValues: {
            ":pk": pk,
            ":sk": FormatPadded("SEQ#%020d", fromSequence)
        },
        scanIndexForward: true
    })

    IF result.IsError() THEN
        RETURN Error(result.Error())
    END IF

    events = []
    FOR EACH item IN result.Value().Items DO
        ei = UnmarshalEventItem(item)
        occurredAt = ParseTimestamp(ei.occurredAt)

        events.append(StoredEvent{
            eventId: ei.eventId,
            eventType: ei.eventType,
            aggregateId: ei.aggregateId,
            aggregateType: ei.aggregateType,
            sequence: ei.sequence,
            occurredAt: occurredAt,
            schemaVersion: ei.schemaVersion,
            payload: RawJSON(ei.payload)
        })
    END FOR

    RETURN Ok(events)
END METHOD
```

## Step 3: Implement Aggregate with Event Replay

```pseudocode
// Pattern: Aggregate Root Base Type
// Base type for event-sourced aggregates

TYPE AggregateRoot
    id: String
    aggregateType: String
    version: Integer
    uncommittedEvents: List<Event>

METHOD AggregateRoot.ID() RETURNS String
    RETURN this.id
END METHOD

METHOD AggregateRoot.Version() RETURNS Integer
    RETURN this.version
END METHOD

METHOD AggregateRoot.SetVersion(v: Integer)
    this.version = v
END METHOD

METHOD AggregateRoot.UncommittedEvents() RETURNS List<Event>
    RETURN this.uncommittedEvents
END METHOD

METHOD AggregateRoot.ClearUncommittedEvents()
    this.uncommittedEvents = []
END METHOD

METHOD AggregateRoot.Raise(event: Event)
    this.uncommittedEvents.append(event)
    this.version = event.Sequence()
END METHOD
```

### Concrete Aggregate

```pseudocode
// Pattern: Enumeration as Value Object
TYPE OrderStatus
    CONSTANT Pending = "pending"
    CONSTANT Confirmed = "confirmed"

// Pattern: Event-Sourced Aggregate
TYPE Order
    AggregateRoot           // Embedded base type
    customerId: String
    items: List<OrderItem>
    status: OrderStatus

// Pattern: Value Object
TYPE OrderItem
    productId: String
    quantity: Integer
    unitPrice: Money

TYPE Money
    amount: Integer
    currency: String

// Pattern: Domain Events as Past-Tense Facts
TYPE OrderCreated EXTENDS BaseEvent
    customerId: String
    items: List<OrderItem>
    totalAmount: Money

TYPE OrderConfirmed EXTENDS BaseEvent
    // No additional fields

// Pattern: Factory Constructor with Validation
CONSTRUCTOR NewOrder(id: String, customerId: String, items: List<OrderItem>) RETURNS Result<Order, Error>
    IF customerId == "" OR items.Length() == 0 THEN
        RETURN Error("invalid order")
    END IF

    order = Order{}
    event = NewOrderCreated(id, customerId, items)
    order.Apply(event)
    order.Raise(event)

    RETURN Ok(order)
END CONSTRUCTOR

// Pattern: Apply Method - Pure State Reconstruction
// Apply rebuilds state from event - pure, no side effects
METHOD Order.Apply(event: Event)
    MATCH event TYPE
        CASE OrderCreated:
            e = event AS OrderCreated
            this.id = e.AggregateID()
            this.customerId = e.customerId
            this.items = e.items
            this.status = OrderStatus.Pending
            this.aggregateType = "Order"
        CASE OrderConfirmed:
            this.status = OrderStatus.Confirmed
    END MATCH
    this.SetVersion(event.Sequence())
END METHOD

// Pattern: Command Method - Validate Then Raise
METHOD Order.Confirm() RETURNS Result<Void, Error>
    IF this.status != OrderStatus.Pending THEN
        RETURN Error("invalid status")
    END IF

    event = NewOrderConfirmed(this.ID(), this.Version() + 1)
    this.Apply(event)
    this.Raise(event)

    RETURN Ok()
END METHOD

// Pattern: Aggregate Rehydration from Event History
FUNCTION LoadFromHistory(events: List<StoredEvent>) RETURNS Result<Order, Error>
    IF events.Length() == 0 THEN
        RETURN Error("no events")
    END IF

    order = Order{}
    FOR EACH stored IN events DO
        eventResult = deserializeEvent(stored)
        IF eventResult.IsError() THEN
            RETURN Error(eventResult.Error())
        END IF
        order.Apply(eventResult.Value())
    END FOR

    RETURN Ok(order)
END FUNCTION

// Pattern: Event Deserialization Registry
FUNCTION deserializeEvent(stored: StoredEvent) RETURNS Result<Event, Error>
    MATCH stored.eventType
        CASE "order.created":
            e = DeserializeJSON<OrderCreated>(stored.payload)
            e.BaseEvent = NewBaseEvent(stored.eventType, stored.aggregateId, stored.aggregateType, stored.sequence)
            RETURN Ok(e)
        CASE "order.confirmed":
            e = DeserializeJSON<OrderConfirmed>(stored.payload)
            e.BaseEvent = NewBaseEvent(stored.eventType, stored.aggregateId, stored.aggregateType, stored.sequence)
            RETURN Ok(e)
        DEFAULT:
            RETURN Error("unknown type: " + stored.eventType)
    END MATCH
END FUNCTION
```

## Step 4: Create Snapshots for Performance

```pseudocode
// Pattern: Snapshot for Performance Optimization
// Snapshot stores aggregate state at a point in time

TYPE Snapshot
    aggregateId: String
    aggregateType: String
    version: Integer
    state: RawJSON
    createdAt: Timestamp

// Pattern: Snapshotter Interface
// Interface for aggregates that support snapshots
INTERFACE Snapshotter
    METHOD ToSnapshot() RETURNS Result<RawJSON, Error>
    METHOD FromSnapshot(state: RawJSON, version: Integer) RETURNS Result<Void, Error>
END INTERFACE

// Pattern: Internal Snapshot State
TYPE orderSnapshot
    customerId: String
    items: List<OrderItem>
    status: String

METHOD Order.ToSnapshot() RETURNS Result<RawJSON, Error>
    snap = orderSnapshot{
        customerId: this.customerId,
        items: this.items,
        status: this.status
    }
    RETURN SerializeJSON(snap)
END METHOD

METHOD Order.FromSnapshot(state: RawJSON, version: Integer) RETURNS Result<Void, Error>
    snap = DeserializeJSON<orderSnapshot>(state)
    IF snap.IsError() THEN
        RETURN Error(snap.Error())
    END IF

    this.customerId = snap.customerId
    this.items = snap.items
    this.status = OrderStatus(snap.status)
    this.SetVersion(version)

    RETURN Ok()
END METHOD
```

### Snapshot-Aware Repository

```pseudocode
// Pattern: Snapshot-Aware Repository
// Loads from snapshot then replays remaining events

TYPE OrderRepository
    eventStore: EventStore

METHOD OrderRepository.Load(ctx: Context, orderId: String) RETURNS Result<Order, Error>
    // Step 1: Try to load snapshot
    snapshotResult = this.eventStore.LoadSnapshot(ctx, orderId, "Order")

    order = NULL
    fromSequence = 0

    IF snapshotResult.IsOk() AND snapshotResult.Value() != NULL THEN
        snapshot = snapshotResult.Value()
        order = Order{}
        order.FromSnapshot(snapshot.state, snapshot.version)
        fromSequence = snapshot.version + 1
    END IF

    // Step 2: Load events after snapshot
    eventsResult = this.eventStore.Load(ctx, orderId, "Order", fromSequence)
    IF eventsResult.IsError() THEN
        RETURN Error(eventsResult.Error())
    END IF
    events = eventsResult.Value()

    // Step 3: Handle not found case
    IF order == NULL AND events.Length() == 0 THEN
        RETURN Error("order not found")
    END IF

    // Step 4: Rebuild from history if no snapshot
    IF order == NULL THEN
        RETURN LoadFromHistory(events)
    END IF

    // Step 5: Replay events after snapshot
    FOR EACH e IN events DO
        eventResult = deserializeEvent(e)
        IF eventResult.IsError() THEN
            RETURN Error(eventResult.Error())
        END IF
        order.Apply(eventResult.Value())
    END FOR

    RETURN Ok(order)
END METHOD
```

## Step 5: Build Projections from Events

```pseudocode
// Pattern: Read Model / Projection
// Optimized view for queries

TYPE OrderSummaryView
    orderId: String
    customerId: String
    status: String
    totalAmount: Integer
    itemCount: Integer
    gsi1pk: String          // CUSTOMER#{id}
    gsi1sk: String          // ORDER#{time}

// Pattern: Projection Handler
// Processes events to update read model

TYPE OrderSummaryProjection
    client: DataStoreClient
    tableName: String

METHOD OrderSummaryProjection.Handle(ctx: Context, stored: StoredEvent) RETURNS Result<Void, Error>
    MATCH stored.eventType
        CASE "order.created":
            payload = DeserializeJSON<OrderCreatedPayload>(stored.payload)

            view = OrderSummaryView{
                orderId: stored.aggregateId,
                customerId: payload.customerId,
                status: "pending",
                totalAmount: payload.totalAmount,
                itemCount: payload.items.Length(),
                gsi1pk: "CUSTOMER#" + payload.customerId,
                gsi1sk: "ORDER#" + FormatTimestamp(stored.occurredAt)
            }

            this.client.PutItem(ctx, PutItemInput{
                tableName: this.tableName,
                item: view
            })

        CASE "order.confirmed":
            // Update status field
            this.client.UpdateItem(ctx, UpdateItemInput{
                tableName: this.tableName,
                key: {orderId: stored.aggregateId},
                updateExpression: "SET #status = :status",
                expressionAttributeNames: {"#status": "status"},
                expressionAttributeValues: {":status": "confirmed"}
            })
    END MATCH

    RETURN Ok()
END METHOD

// Pattern: Projection Rebuild
// Rebuild entire projection from event log

METHOD OrderSummaryProjection.Rebuild(ctx: Context, eventStore: EventStoreWithLoadAll) RETURNS Result<Void, Error>
    eventsResult = eventStore.LoadAll(ctx, "Order")
    IF eventsResult.IsError() THEN
        RETURN Error(eventsResult.Error())
    END IF

    FOR EACH event IN eventsResult.Value() DO
        this.Handle(ctx, event)
    END FOR

    RETURN Ok()
END METHOD
```

## Step 6: Handle Event Versioning

```pseudocode
// Pattern: Event Upcaster
// Transforms old event versions to current version

INTERFACE EventUpcaster
    METHOD CanUpcast(eventType: String, version: String) RETURNS Boolean
    METHOD Upcast(payload: RawJSON, fromVersion: String) RETURNS Result<Tuple<RawJSON, String>, Error>
END INTERFACE

// Pattern: Concrete Upcaster for Schema Evolution
// Upcaster for OrderCreated v1 to v2

TYPE OrderCreatedUpcaster

METHOD OrderCreatedUpcaster.CanUpcast(eventType: String, version: String) RETURNS Boolean
    RETURN eventType == "order.created" AND version == "1.0.0"
END METHOD

// v1: "price" field -> v2: "unit_price" with currency
METHOD OrderCreatedUpcaster.Upcast(payload: RawJSON, fromVersion: String) RETURNS Result<Tuple<RawJSON, String>, Error>
    v1 = DeserializeJSON<OrderCreatedV1>(payload)

    v2 = OrderCreatedV2{
        customerId: v1.customerId,
        items: [],
        totalAmount: Money{amount: v1.totalCents, currency: "USD"}
    }

    FOR EACH item IN v1.items DO
        v2.items.append(OrderItem{
            productId: item.productId,
            quantity: item.quantity,
            unitPrice: Money{amount: item.price, currency: "USD"}
        })
    END FOR

    result = SerializeJSON(v2)
    RETURN Ok(Tuple(result, "2.0.0"))
END METHOD

// Pattern: Upcaster Chain
// Applies upcasters in sequence until current version

TYPE UpcasterChain
    upcasters: List<EventUpcaster>

METHOD UpcasterChain.Upcast(eventType: String, payload: RawJSON, version: String) RETURNS Result<Tuple<RawJSON, String>, Error>
    currentPayload = payload
    currentVersion = version

    FOR EACH u IN this.upcasters DO
        IF u.CanUpcast(eventType, currentVersion) THEN
            result = u.Upcast(currentPayload, currentVersion)
            IF result.IsError() THEN
                RETURN Error(result.Error())
            END IF
            currentPayload, currentVersion = result.Value()
        END IF
    END FOR

    RETURN Ok(Tuple(currentPayload, currentVersion))
END METHOD
```

## Step 7: Test Replay and Projections

```pseudocode
// Test: Load order from history
TEST Order_LoadFromHistory
    events = [
        StoredEvent{
            eventId: "evt-1",
            eventType: "order.created",
            aggregateId: "order-123",
            sequence: 1,
            payload: RawJSON('{"customer_id":"cust-1","items":[{"product_id":"prod-1","quantity":2}]}')
        },
        StoredEvent{
            eventId: "evt-2",
            eventType: "order.confirmed",
            aggregateId: "order-123",
            sequence: 2,
            payload: RawJSON('{}')
        }
    ]

    orderResult = LoadFromHistory(events)

    ASSERT orderResult.IsOk()
    order = orderResult.Value()
    ASSERT order.ID() == "order-123"
    ASSERT order.Status() == OrderStatus.Confirmed
    ASSERT order.Version() == 2
END TEST

// Test: Snapshot round trip
TEST Order_SnapshotRoundTrip
    items = [OrderItem{
        productId: "prod-1",
        quantity: 2,
        unitPrice: Money{amount: 1000, currency: "USD"}
    }]

    originalResult = NewOrder("order-1", "cust-1", items)
    original = originalResult.Value()
    original.Confirm()

    stateResult = original.ToSnapshot()
    state = stateResult.Value()

    restored = Order{}
    restored.FromSnapshot(state, original.Version())

    ASSERT original.Status() == restored.Status()
END TEST

// Test: Projection rebuild
TEST Projection_Rebuild
    store = InMemoryEventStore.New()
    store.Append(ctx, [
        createOrderEvent("order-1", "cust-1"),
        confirmOrderEvent("order-1")
    ], 0)

    projection = NewOrderSummaryProjection(testDB, "projections")
    projection.Rebuild(ctx, store)

    summary = projection.Get(ctx, "order-1")
    ASSERT summary.status == "confirmed"
END TEST
```

## Verification Checklist

After implementing event sourcing, verify:

- [ ] Events are immutable facts (past tense, complete data)
- [ ] Event store enforces append-only with optimistic concurrency
- [ ] Aggregates rebuild from event replay
- [ ] Apply method is pure (no side effects, no validation)
- [ ] Command methods validate first, then raise events
- [ ] Snapshots are optimization, not required for correctness
- [ ] Projections rebuild from event log
- [ ] Event versioning uses upcasters - never modify stored events
- [ ] Sequence numbers ensure ordering
- [ ] Events include schema version
- [ ] Tests verify replay and projection consistency
