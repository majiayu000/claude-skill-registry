---
name: cqrs-patterns
description: CQRS (Command Query Responsibility Segregation) patterns for separating read and write models. Use when optimizing read-heavy systems, implementing event sourcing, or building systems with different read/write scaling requirements.
context: fork
agent: event-driven-architect
version: 1.0.0
tags: [cqrs, command-query, read-model, write-model, projection, event-sourcing, 2026]
author: SkillForge
user-invocable: false
---

# CQRS Patterns

Separate read and write concerns for optimized data access.

## When to Use

- Read-heavy workloads with complex queries
- Different scaling requirements for reads vs writes
- Event sourcing implementations
- Multiple read model representations of same data
- Complex domain models with simple read requirements

## When NOT to Use

- Simple CRUD applications
- Strong consistency requirements everywhere
- Small datasets with simple queries

## Architecture Overview

```
┌─────────────────┐         ┌─────────────────┐
│   Write Side    │         │   Read Side     │
├─────────────────┤         ├─────────────────┤
│  ┌───────────┐  │         │  ┌───────────┐  │
│  │ Commands  │  │         │  │  Queries  │  │
│  └─────┬─────┘  │         │  └─────┬─────┘  │
│  ┌─────▼─────┐  │         │  ┌─────▼─────┐  │
│  │ Aggregate │  │         │  │Read Model │  │
│  └─────┬─────┘  │         │  └───────────┘  │
│  ┌─────▼─────┐  │         │        ▲        │
│  │  Events   │──┼─────────┼────────┘        │
│  └───────────┘  │ Publish │   Project       │
└─────────────────┘         └─────────────────┘
```

## Command Side (Write Model)

### Command and Handler

```python
from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from datetime import datetime, timezone
from abc import ABC, abstractmethod

class Command(BaseModel):
    """Base command with metadata."""
    command_id: UUID = Field(default_factory=uuid4)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    user_id: UUID | None = None

class CreateOrder(Command):
    customer_id: UUID
    items: list[OrderItem]
    shipping_address: Address

class CommandHandler(ABC):
    @abstractmethod
    async def handle(self, command: Command) -> list["DomainEvent"]:
        pass

class CreateOrderHandler(CommandHandler):
    def __init__(self, order_repo, inventory_service):
        self.order_repo = order_repo
        self.inventory = inventory_service

    async def handle(self, command: CreateOrder) -> list[DomainEvent]:
        for item in command.items:
            if not await self.inventory.check_availability(item.product_id, item.quantity):
                raise InsufficientInventoryError(item.product_id)

        order = Order.create(
            customer_id=command.customer_id,
            items=command.items,
            shipping_address=command.shipping_address,
        )
        await self.order_repo.save(order)
        return order.pending_events

class CommandBus:
    def __init__(self):
        self._handlers: dict[type, CommandHandler] = {}

    def register(self, command_type: type, handler: CommandHandler):
        self._handlers[command_type] = handler

    async def dispatch(self, command: Command) -> list[DomainEvent]:
        handler = self._handlers.get(type(command))
        if not handler:
            raise NoHandlerFoundError(type(command))
        events = await handler.handle(command)
        for event in events:
            await self.event_publisher.publish(event)
        return events
```

### Write Model (Aggregate)

```python
from dataclasses import dataclass, field

@dataclass
class Order:
    id: UUID
    customer_id: UUID
    items: list[OrderItem]
    status: OrderStatus
    _pending_events: list[DomainEvent] = field(default_factory=list)

    @classmethod
    def create(cls, customer_id: UUID, items: list, shipping_address: Address) -> "Order":
        order = cls(id=uuid4(), customer_id=customer_id, items=[], status=OrderStatus.PENDING)
        for item in items:
            order.items.append(item)
            order._raise_event(OrderItemAdded(order_id=order.id, product_id=item.product_id))
        order._raise_event(OrderCreated(order_id=order.id, customer_id=customer_id))
        return order

    def cancel(self, reason: str):
        if self.status == OrderStatus.SHIPPED:
            raise InvalidOperationError("Cannot cancel shipped order")
        self.status = OrderStatus.CANCELLED
        self._raise_event(OrderCancelled(order_id=self.id, reason=reason))

    def _raise_event(self, event: DomainEvent):
        self._pending_events.append(event)

    @property
    def pending_events(self) -> list[DomainEvent]:
        events = self._pending_events.copy()
        self._pending_events.clear()
        return events
```

## Query Side (Read Model)

### Query Handler

```python
class Query(BaseModel):
    pass

class GetOrderById(Query):
    order_id: UUID

class GetOrdersByCustomer(Query):
    customer_id: UUID
    status: OrderStatus | None = None
    page: int = 1
    page_size: int = 20

class GetOrderByIdHandler:
    def __init__(self, read_db):
        self.db = read_db

    async def handle(self, query: GetOrderById) -> OrderView | None:
        row = await self.db.fetchrow(
            "SELECT * FROM order_summary WHERE id = $1", query.order_id
        )
        return OrderView(**row) if row else None

class OrderView(BaseModel):
    """Denormalized read model for orders."""
    id: UUID
    customer_id: UUID
    customer_name: str  # Denormalized
    status: str
    total_amount: float
    item_count: int
    created_at: datetime
```

## Projections

```python
class OrderProjection:
    """Projects events to read models."""
    def __init__(self, read_db, customer_service):
        self.db = read_db
        self.customers = customer_service

    async def handle(self, event: DomainEvent):
        match event:
            case OrderCreated():
                await self._on_order_created(event)
            case OrderItemAdded():
                await self._on_item_added(event)
            case OrderCancelled():
                await self._on_order_cancelled(event)

    async def _on_order_created(self, event: OrderCreated):
        customer = await self.customers.get(event.customer_id)
        await self.db.execute(
            """INSERT INTO order_summary (id, customer_id, customer_name, status, total_amount, item_count, created_at)
               VALUES ($1, $2, $3, 'pending', 0.0, 0, $4)
               ON CONFLICT (id) DO UPDATE SET customer_name = $3""",
            event.order_id, event.customer_id, customer.name, event.timestamp,
        )

    async def _on_item_added(self, event: OrderItemAdded):
        subtotal = event.quantity * event.unit_price
        await self.db.execute(
            "UPDATE order_summary SET total_amount = total_amount + $1, item_count = item_count + 1 WHERE id = $2",
            subtotal, event.order_id,
        )

    async def _on_order_cancelled(self, event: OrderCancelled):
        await self.db.execute(
            "UPDATE order_summary SET status = 'cancelled' WHERE id = $1", event.order_id
        )
```

## FastAPI Integration

```python
from fastapi import FastAPI, Depends, HTTPException

app = FastAPI()

@app.post("/api/v1/orders", status_code=201)
async def create_order(request: CreateOrderRequest, bus: CommandBus = Depends(get_command_bus)):
    command = CreateOrder(
        customer_id=request.customer_id,
        items=request.items,
        shipping_address=request.shipping_address,
    )
    try:
        events = await bus.dispatch(command)
        return {"order_id": events[0].order_id}
    except InsufficientInventoryError as e:
        raise HTTPException(400, f"Insufficient inventory: {e}")

@app.get("/api/v1/orders/{order_id}")
async def get_order(order_id: UUID, bus: QueryBus = Depends(get_query_bus)):
    order = await bus.dispatch(GetOrderById(order_id=order_id))
    if not order:
        raise HTTPException(404, "Order not found")
    return order
```

## Key Decisions

| Decision | Recommendation |
|----------|----------------|
| Consistency | Eventual consistency between write and read models |
| Event storage | Event store for write side, denormalized tables for read |
| Projection lag | Monitor and alert on projection delay |
| Read model count | Start with one, add more for specific query needs |
| Rebuild strategy | Ability to rebuild projections from events |

## Anti-Patterns (FORBIDDEN)

```python
# NEVER query write model for reads
order = await aggregate_repo.get(order_id)  # WRONG

# CORRECT: Use read model
order = await query_bus.dispatch(GetOrderById(order_id=order_id))

# NEVER modify read model directly
await read_db.execute("UPDATE orders SET status = $1", status)  # WRONG

# CORRECT: Dispatch command, let projection update
await bus.dispatch(UpdateOrderStatus(order_id=order_id, status=status))

# NEVER skip projection idempotency - use UPSERT
await self.db.execute("INSERT INTO ... ON CONFLICT (id) DO UPDATE SET ...")
```

## Related Skills

- `event-sourcing` - Event-sourced write models
- `saga-patterns` - Cross-aggregate transactions
- `database-schema-designer` - Read model schema design
