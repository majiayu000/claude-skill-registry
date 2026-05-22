---
name: event-driven-architect
description: Design event-driven architectures using Kafka, RabbitMQ, event sourcing, CQRS, and saga patterns. Activates when users need help with event-driven design, message queues, event sourcing, or asynchronous communication patterns.
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob]
---

# Event-Driven Architect

Design robust event-driven architectures for scalable, loosely-coupled microservices.

## When to Use

- Designing event-driven microservices
- Implementing event sourcing and CQRS
- Setting up Kafka, RabbitMQ, or similar
- Designing saga patterns for distributed transactions
- Implementing eventual consistency
- Building real-time data pipelines
- Designing publish-subscribe patterns

## Key Patterns

### Event Sourcing
Store all changes as events, reconstruct state by replaying events.

### CQRS (Command Query Responsibility Segregation)
Separate read and write models for better scalability.

### Saga Pattern
Manage distributed transactions across microservices.

### Event Streaming
Process continuous streams of events in real-time.

## Kafka Configuration Example

```yaml
# Kafka topic configuration
apiVersion: kafka.strimzi.io/v1beta2
kind: KafkaTopic
metadata:
  name: order-events
spec:
  partitions: 10
  replicas: 3
  config:
    retention.ms: 604800000  # 7 days
    compression.type: snappy
    max.message.bytes: 1048576
---
# Event schema (Avro)
{
  "type": "record",
  "name": "OrderCreated",
  "namespace": "com.example.events",
  "fields": [
    {"name": "orderId", "type": "string"},
    {"name": "customerId", "type": "string"},
    {"name": "items", "type": {"type": "array", "items": "OrderItem"}},
    {"name": "totalAmount", "type": "double"},
    {"name": "timestamp", "type": "long"}
  ]
}
```

## Event Sourcing Implementation

```typescript
// Event store
class OrderEventStore {
  async appendEvent(event: DomainEvent): Promise<void> {
    await this.eventStore.append({
      aggregateId: event.aggregateId,
      eventType: event.constructor.name,
      eventData: JSON.stringify(event),
      timestamp: new Date(),
      version: event.version
    });
    
    // Publish to event bus
    await this.eventBus.publish(event);
  }

  async getEvents(aggregateId: string): Promise<DomainEvent[]> {
    const events = await this.eventStore.find({
      aggregateId,
      orderBy: { version: 'asc' }
    });
    return events.map(e => this.deserialize(e));
  }

  reconstructAggregate(events: DomainEvent[]): Order {
    const order = new Order();
    events.forEach(event => order.apply(event));
    return order;
  }
}

// Domain events
class OrderCreatedEvent {
  constructor(
    public orderId: string,
    public customerId: string,
    public items: OrderItem[],
    public totalAmount: number
  ) {}
}

class OrderConfirmedEvent {
  constructor(public orderId: string) {}
}

// Aggregate
class Order {
  private id: string;
  private status: OrderStatus;
  private items: OrderItem[];

  apply(event: DomainEvent) {
    if (event instanceof OrderCreatedEvent) {
      this.id = event.orderId;
      this.status = 'pending';
      this.items = event.items;
    } else if (event instanceof OrderConfirmedEvent) {
      this.status = 'confirmed';
    }
  }
}
```

## CQRS Pattern

```typescript
// Command side (write model)
class CreateOrderCommand {
  constructor(
    public customerId: string,
    public items: OrderItem[]
  ) {}
}

class OrderCommandHandler {
  async handle(command: CreateOrderCommand): Promise<string> {
    // Validate
    this.validateCommand(command);
    
    // Create event
    const orderId = uuid();
    const event = new OrderCreatedEvent(
      orderId,
      command.customerId,
      command.items,
      this.calculateTotal(command.items)
    );
    
    // Store event
    await this.eventStore.appendEvent(event);
    
    return orderId;
  }
}

// Query side (read model)
class OrderQueryModel {
  async getOrderById(orderId: string): Promise<OrderDTO> {
    // Read from optimized read database (e.g., MongoDB)
    return await this.orderReadRepo.findById(orderId);
  }

  async getOrdersByCustomer(customerId: string): Promise<OrderDTO[]> {
    return await this.orderReadRepo.find({ customerId });
  }
}

// Projection (updates read model from events)
class OrderProjection {
  @EventHandler(OrderCreatedEvent)
  async onOrderCreated(event: OrderCreatedEvent) {
    await this.orderReadRepo.create({
      id: event.orderId,
      customerId: event.customerId,
      items: event.items,
      totalAmount: event.totalAmount,
      status: 'pending',
      createdAt: new Date()
    });
  }

  @EventHandler(OrderConfirmedEvent)
  async onOrderConfirmed(event: OrderConfirmedEvent) {
    await this.orderReadRepo.update(event.orderId, {
      status: 'confirmed'
    });
  }
}
```

## Saga Pattern (Orchestration)

```typescript
// Saga orchestrator for order creation
class OrderCreationSaga {
  async execute(orderId: string) {
    try {
      // Step 1: Reserve inventory
      await this.inventoryService.reserve(orderId);
      await this.sagaStore.recordStep(orderId, 'inventory_reserved');

      // Step 2: Process payment
      await this.paymentService.charge(orderId);
      await this.sagaStore.recordStep(orderId, 'payment_processed');

      // Step 3: Confirm order
      await this.orderService.confirm(orderId);
      await this.sagaStore.recordStep(orderId, 'order_confirmed');

      // Success
      await this.sagaStore.complete(orderId);

    } catch (error) {
      // Compensate (rollback)
      await this.compensate(orderId);
      throw new SagaFailedError(orderId, error);
    }
  }

  private async compensate(orderId: string) {
    const steps = await this.sagaStore.getCompletedSteps(orderId);
    
    // Rollback in reverse order
    if (steps.includes('payment_processed')) {
      await this.paymentService.refund(orderId);
    }
    if (steps.includes('inventory_reserved')) {
      await this.inventoryService.release(orderId);
    }
    
    await this.orderService.cancel(orderId);
  }
}
```

## Best Practices

- ✅ Use event versioning from day one
- ✅ Implement idempotent event handlers
- ✅ Design for eventual consistency
- ✅ Use schema registry (Avro, Protobuf)
- ✅ Implement dead letter queues
- ✅ Monitor event lag and throughput
- ✅ Use correlation IDs for tracing
- ✅ Handle duplicate events gracefully

## Related Skills

- `microservices-orchestrator` - Service design
- `distributed-tracing-setup` - Event tracing
- `chaos-engineering-setup` - Resilience testing

