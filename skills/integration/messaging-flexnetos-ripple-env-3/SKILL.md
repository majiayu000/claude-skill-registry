---
name: Messaging & Event Systems
description: "Messaging and event-driven architecture. Activate when: (1) Working with NATS pub/sub, (2) Configuring Temporal workflows, (3) Implementing event sourcing, (4) Setting up message queues, or (5) Designing async communication patterns."
---

# Messaging & Event Systems

## Overview

This skill covers messaging systems (NATS), workflow orchestration (Temporal), and event-driven architecture patterns.

## NATS

### Core Concepts

| Concept | Description |
|---------|-------------|
| Subject | Message address/topic (e.g., `orders.created`) |
| Publisher | Sends messages to subjects |
| Subscriber | Receives messages from subjects |
| Queue Group | Load-balanced message distribution |
| JetStream | Persistence and streaming layer |
| KV Store | Key-value storage built on JetStream |

### NATS CLI

```bash
# Connect
nats context add local --server nats://localhost:4222
nats context select local

# Pub/Sub
nats pub orders.created '{"id": 123}'
nats sub 'orders.>'                    # Wildcard subscription

# Request/Reply
nats reply 'service.ping' 'pong'       # In terminal 1
nats request 'service.ping' ''         # In terminal 2

# JetStream
nats stream add ORDERS --subjects "orders.>" --retention limits
nats stream info ORDERS
nats consumer add ORDERS processor --pull --ack explicit

# KV Store
nats kv add CONFIG
nats kv put CONFIG app.setting "value"
nats kv get CONFIG app.setting
nats kv watch CONFIG
```

### NATS Server Configuration

```hcl
# nats.conf
port: 4222

jetstream {
  store_dir: /data/jetstream
  max_mem: 1G
  max_file: 10G
}

cluster {
  name: my-cluster
  port: 6222
  routes: [
    nats-route://nats-1:6222
    nats-route://nats-2:6222
  ]
}
```

### NATS Client (Rust)

```rust
use async_nats;

#[tokio::main]
async fn main() -> Result<(), async_nats::Error> {
    let client = async_nats::connect("nats://localhost:4222").await?;

    // Publish
    client.publish("events.user.created", "user data".into()).await?;

    // Subscribe
    let mut subscriber = client.subscribe("events.>").await?;
    while let Some(message) = subscriber.next().await {
        println!("Received: {:?}", message);
    }

    Ok(())
}
```

### NATS Client (Python)

```python
import asyncio
import nats

async def main():
    nc = await nats.connect("nats://localhost:4222")

    # Subscribe
    async def message_handler(msg):
        print(f"Received: {msg.subject}: {msg.data.decode()}")

    await nc.subscribe("events.>", cb=message_handler)

    # Publish
    await nc.publish("events.user.created", b'{"user_id": 123}')

    # Request/Reply
    response = await nc.request("service.ping", b'', timeout=1)
    print(f"Response: {response.data.decode()}")

asyncio.run(main())
```

## Temporal

### Core Concepts

| Concept | Description |
|---------|-------------|
| Workflow | Durable, long-running business process |
| Activity | A single unit of work (can fail/retry) |
| Worker | Executes workflows and activities |
| Task Queue | Routes work to workers |
| Signal | External event sent to running workflow |
| Query | Read workflow state without affecting it |

### Workflow Definition (Python)

```python
from temporalio import workflow, activity
from datetime import timedelta

@activity.defn
async def send_email(to: str, subject: str) -> str:
    # Actual email sending logic
    return f"Email sent to {to}"

@activity.defn
async def process_payment(order_id: str, amount: float) -> bool:
    # Payment processing logic
    return True

@workflow.defn
class OrderWorkflow:
    @workflow.run
    async def run(self, order_id: str) -> str:
        # Activities with retry policy
        payment_result = await workflow.execute_activity(
            process_payment,
            args=[order_id, 99.99],
            start_to_close_timeout=timedelta(seconds=30),
            retry_policy=RetryPolicy(maximum_attempts=3)
        )

        if payment_result:
            await workflow.execute_activity(
                send_email,
                args=["customer@example.com", "Order Confirmed"],
                start_to_close_timeout=timedelta(seconds=10)
            )

        return f"Order {order_id} completed"
```

### Worker Setup

```python
from temporalio.client import Client
from temporalio.worker import Worker

async def main():
    client = await Client.connect("localhost:7233")

    worker = Worker(
        client,
        task_queue="order-queue",
        workflows=[OrderWorkflow],
        activities=[send_email, process_payment]
    )

    await worker.run()

asyncio.run(main())
```

### Start Workflow

```python
async def start_order():
    client = await Client.connect("localhost:7233")

    result = await client.execute_workflow(
        OrderWorkflow.run,
        "order-123",
        id="order-workflow-123",
        task_queue="order-queue"
    )

    print(f"Result: {result}")
```

### Temporal CLI

```bash
# Start workflow
temporal workflow start \
  --task-queue order-queue \
  --type OrderWorkflow \
  --input '"order-123"'

# List workflows
temporal workflow list

# Describe workflow
temporal workflow describe --workflow-id order-workflow-123

# Signal workflow
temporal workflow signal \
  --workflow-id order-workflow-123 \
  --name cancel \
  --input '"reason"'

# Query workflow
temporal workflow query \
  --workflow-id order-workflow-123 \
  --name status
```

## Event-Driven Patterns

### Event Sourcing

```python
from dataclasses import dataclass
from typing import List
from datetime import datetime

@dataclass
class Event:
    id: str
    timestamp: datetime
    type: str
    data: dict

class OrderAggregate:
    def __init__(self, order_id: str):
        self.id = order_id
        self.status = "pending"
        self.items = []
        self.events: List[Event] = []

    def apply(self, event: Event):
        if event.type == "OrderCreated":
            self.status = "created"
            self.items = event.data["items"]
        elif event.type == "OrderPaid":
            self.status = "paid"
        elif event.type == "OrderShipped":
            self.status = "shipped"

    def add_item(self, item: dict):
        event = Event(
            id=str(uuid4()),
            timestamp=datetime.utcnow(),
            type="ItemAdded",
            data={"item": item}
        )
        self.events.append(event)
        self.apply(event)
```

### CQRS Pattern

```python
# Command Handler
class CreateOrderCommand:
    def __init__(self, customer_id: str, items: list):
        self.customer_id = customer_id
        self.items = items

async def handle_create_order(cmd: CreateOrderCommand):
    order = Order.create(cmd.customer_id, cmd.items)
    await event_store.append(order.id, order.events)
    await nats.publish("orders.created", order.to_json())

# Query Handler (separate read model)
async def get_order_summary(order_id: str) -> dict:
    return await read_db.query(
        "SELECT * FROM order_summaries WHERE id = $1",
        order_id
    )
```

### Saga Pattern

```python
@workflow.defn
class OrderSaga:
    @workflow.run
    async def run(self, order: dict) -> str:
        try:
            # Step 1: Reserve inventory
            reservation = await workflow.execute_activity(
                reserve_inventory, args=[order["items"]]
            )

            # Step 2: Process payment
            payment = await workflow.execute_activity(
                process_payment, args=[order["total"]]
            )

            # Step 3: Ship order
            shipping = await workflow.execute_activity(
                create_shipment, args=[order["address"]]
            )

            return "Order completed"

        except Exception as e:
            # Compensating transactions
            if reservation:
                await workflow.execute_activity(release_inventory)
            if payment:
                await workflow.execute_activity(refund_payment)
            raise
```

## External Links

- [NATS Documentation](https://docs.nats.io/)
- [Temporal Documentation](https://docs.temporal.io/)
- [Event Sourcing Pattern](https://microservices.io/patterns/data/event-sourcing.html)
- [CQRS Pattern](https://microservices.io/patterns/data/cqrs.html)
