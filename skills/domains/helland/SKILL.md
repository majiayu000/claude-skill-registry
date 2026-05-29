---
name: helland-distributed-data
description: Design scalable data systems in the style of Pat Helland, distributed systems veteran from Tandem, Microsoft, and Amazon. Emphasizes life beyond distributed transactions, idempotency, and practical patterns for data at scale. Use when building systems that must scale beyond single-node ACID transactions.
---

# Pat Helland Style Guide

## Overview

Pat Helland has worked on distributed systems for 40+ years at Tandem (fault-tolerant transaction systems), Microsoft (SQL Server, Cosmos DB), and Amazon. His papers on scalable data patterns—especially "Life Beyond Distributed Transactions"—have shaped how the industry builds large-scale systems.

## Core Philosophy

> "In a world with unbounded scale, you cannot have distributed transactions."

> "Idempotency is the key to building reliable systems."

> "Data on the inside is not the same as data on the outside."

Helland believes that as systems scale, traditional ACID transactions become impractical. Instead, we need new patterns: idempotent operations, entity-based partitioning, and application-level consistency.

## Design Principles

1. **Entities, Not Tables**: Think in terms of independently scalable entities, not relational tables.

2. **Idempotency Everywhere**: Operations must be safely retryable.

3. **Messages, Not Transactions**: Cross-entity consistency happens via messaging, not 2PC.

4. **Scale Agnosticism**: Design as if you don't know (or care) how many nodes exist.

5. **Inside vs Outside Data**: Internal data is mutable and rich; external data is immutable and simple.

## When Designing Distributed Data Systems

### Always

- Design entities that can be independently scaled and partitioned
- Make all operations idempotent (same request twice = same result)
- Use unique request IDs to detect and deduplicate retries
- Accept that cross-entity operations are eventually consistent
- Version your external data contracts
- Plan for messages to be delivered at-least-once

### Never

- Depend on distributed transactions for correctness at scale
- Assume exactly-once message delivery
- Share mutable state across service boundaries
- Design entities that require coordination with other entities for basic operations
- Ignore the CAP theorem implications of your design

### Prefer

- Idempotent operations over exactly-once semantics
- Event sourcing over mutable state
- Saga pattern over 2PC
- Entity-based partitioning over arbitrary sharding
- Immutable messages over mutable shared state

## Code Patterns

### Idempotent Operations

```python
class IdempotentPaymentService:
    """
    Helland's key insight: if operations are idempotent,
    retries are safe, and you don't need exactly-once delivery.
    """
    
    def __init__(self, db):
        self.db = db
    
    def process_payment(self, request_id: str, account_id: str, amount: Decimal):
        # Check if we've already processed this request
        existing = self.db.get_processed_request(request_id)
        if existing:
            return existing.result  # Return same result as before
        
        # Process the payment
        with self.db.transaction():
            account = self.db.get_account(account_id)
            account.balance -= amount
            
            result = PaymentResult(
                request_id=request_id,
                status='completed',
                new_balance=account.balance
            )
            
            # Record that we processed this request (atomically with the change)
            self.db.save_processed_request(request_id, result)
            self.db.save_account(account)
        
        return result
```

### Entity-Based Design

```python
class Order:
    """
    Helland's entity pattern: each entity is an island of consistency.
    Cross-entity operations happen via messaging, not transactions.
    """
    
    def __init__(self, order_id: str):
        self.order_id = order_id
        self.items = []
        self.status = 'pending'
        self.version = 0
        
        # Outbox: messages to send (part of entity's transaction)
        self.outbox = []
    
    def add_item(self, product_id: str, quantity: int, request_id: str):
        """All mutations include request_id for idempotency."""
        if self.has_processed(request_id):
            return  # Already did this
        
        self.items.append(OrderItem(product_id, quantity))
        self.record_processed(request_id)
        self.version += 1
    
    def submit(self, request_id: str):
        if self.has_processed(request_id):
            return
        
        self.status = 'submitted'
        self.record_processed(request_id)
        self.version += 1
        
        # Queue message for inventory service (not a distributed txn!)
        self.outbox.append(Message(
            type='OrderSubmitted',
            order_id=self.order_id,
            items=self.items
        ))
```

### Inside Data vs Outside Data

```python
# INSIDE DATA: Rich, mutable, internal representation
class InternalOrder:
    order_id: str
    customer: Customer              # Full customer object
    items: List[OrderItem]          # Mutable list
    shipping_address: Address       # Complex nested object
    internal_notes: str             # Internal-only field
    audit_log: List[AuditEntry]     # Full history
    version: int                    # Optimistic concurrency
    
    def to_external(self) -> 'ExternalOrder':
        """Convert to outside representation for APIs/messages."""
        return ExternalOrder(
            order_id=self.order_id,
            customer_id=self.customer.id,  # Just the ID, not full object
            item_ids=[i.id for i in self.items],  # Just IDs
            submitted_at=self.audit_log[0].timestamp  # Simplified
        )


# OUTSIDE DATA: Simple, immutable, versioned contract
@dataclass(frozen=True)  # Immutable!
class ExternalOrder:
    """
    Helland's rule: data on the outside is:
    - Immutable (represents a point in time)
    - Versioned (schema can evolve)
    - Simple (no complex nested structures)
    - Self-describing (includes type info)
    """
    order_id: str
    customer_id: str
    item_ids: List[str]
    submitted_at: datetime
    schema_version: str = "1.0"
```

### Saga Pattern (Instead of Distributed Transactions)

```python
class OrderSaga:
    """
    Helland's alternative to 2PC: sagas with compensating actions.
    Each step is a local transaction + message to next step.
    Failures trigger compensating transactions.
    """
    
    def __init__(self, order_id: str):
        self.order_id = order_id
        self.state = 'started'
        self.completed_steps = []
    
    async def execute(self):
        try:
            # Step 1: Reserve inventory (local txn in Inventory service)
            await self.reserve_inventory()
            self.completed_steps.append('inventory_reserved')
            
            # Step 2: Charge payment (local txn in Payment service)
            await self.charge_payment()
            self.completed_steps.append('payment_charged')
            
            # Step 3: Ship order (local txn in Shipping service)
            await self.ship_order()
            self.completed_steps.append('order_shipped')
            
            self.state = 'completed'
            
        except Exception as e:
            # Compensate in reverse order
            await self.compensate()
            self.state = 'compensated'
            raise
    
    async def compensate(self):
        """Undo completed steps in reverse order."""
        for step in reversed(self.completed_steps):
            if step == 'order_shipped':
                await self.cancel_shipment()
            elif step == 'payment_charged':
                await self.refund_payment()
            elif step == 'inventory_reserved':
                await self.release_inventory()
```

### Outbox Pattern for Reliable Messaging

```python
class OutboxPublisher:
    """
    Helland's insight: you can't atomically update DB and send a message.
    Solution: write message to outbox table in same transaction,
    then publish from outbox asynchronously.
    """
    
    def __init__(self, db, message_broker):
        self.db = db
        self.broker = message_broker
    
    def update_with_message(self, entity, message):
        """Atomically update entity and queue message."""
        with self.db.transaction():
            self.db.save(entity)
            self.db.insert_outbox(OutboxEntry(
                id=uuid4(),
                message=message,
                status='pending',
                created_at=datetime.utcnow()
            ))
    
    async def publish_outbox(self):
        """Background process: publish pending messages."""
        while True:
            pending = self.db.get_pending_outbox_entries(limit=100)
            
            for entry in pending:
                try:
                    await self.broker.publish(entry.message)
                    self.db.mark_outbox_published(entry.id)
                except Exception:
                    # Will retry on next iteration
                    pass
            
            await asyncio.sleep(1)
```

### Request-Response with Correlation

```python
class AsyncRequestResponse:
    """
    Helland's pattern for async request-response:
    include correlation ID, expect response via messaging.
    """
    
    def __init__(self, outbox, response_handler):
        self.outbox = outbox
        self.pending_requests = {}
        self.response_handler = response_handler
    
    async def send_request(self, target_service: str, payload: dict) -> str:
        correlation_id = str(uuid4())
        
        request = Message(
            correlation_id=correlation_id,
            reply_to='my-service-responses',
            target=target_service,
            payload=payload
        )
        
        self.pending_requests[correlation_id] = {
            'sent_at': datetime.utcnow(),
            'request': request
        }
        
        await self.outbox.publish(request)
        return correlation_id
    
    async def handle_response(self, message: Message):
        correlation_id = message.correlation_id
        
        if correlation_id in self.pending_requests:
            original = self.pending_requests.pop(correlation_id)
            await self.response_handler(original['request'], message)
```

## Mental Model

Helland approaches distributed data design by asking:

1. **What are the entities?** What are the natural units of consistency?
2. **How do entities interact?** Via messages, not shared transactions
3. **What if this message is delivered twice?** Design for idempotency
4. **What if this operation fails halfway?** Design compensating actions
5. **What data crosses boundaries?** Keep it simple and immutable

## Signature Helland Moves

- Idempotent operations with request IDs
- Entity-based partitioning
- Outbox pattern for reliable messaging
- Saga pattern instead of 2PC
- Inside data vs outside data distinction
- At-least-once delivery with deduplication
- Immutable external data contracts

## Key Papers

- "Life Beyond Distributed Transactions: An Apostate's Opinion" (2007, 2016)
- "Data on the Outside vs Data on the Inside" (2005)
- "Building on Quicksand" (2009)
- "Immutability Changes Everything" (2015)
- "Standing on Distributed Shoulders of Giants" (2016)
