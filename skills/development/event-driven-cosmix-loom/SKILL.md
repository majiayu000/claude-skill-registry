---
name: event-driven
description: Event-driven architecture patterns including message queues, pub/sub, event sourcing, CQRS, and sagas. Use when implementing async messaging, distributed transactions, event stores, command query separation, domain events, integration events, data streaming, choreography, orchestration, or integrating with RabbitMQ, Kafka, Apache Pulsar, AWS SQS, AWS SNS, NATS, event buses, or message brokers.
triggers:
  - event
  - message
  - messaging
  - pub/sub
  - pubsub
  - publish/subscribe
  - kafka
  - rabbitmq
  - sqs
  - sns
  - nats
  - pulsar
  - event sourcing
  - CQRS
  - saga
  - choreography
  - orchestration
  - event store
  - domain event
  - integration event
  - message queue
  - message broker
  - event bus
  - data streaming
  - stream processing
  - event-driven
---

# Event-Driven Architecture

## Overview

Event-driven architecture (EDA) enables loosely coupled, scalable systems by communicating through events rather than direct calls. This skill covers message queues, pub/sub patterns, event sourcing, CQRS, distributed transaction management with sagas, and data streaming with Kafka.

## Available Agents

- **senior-software-engineer** (Opus) - Architecture design, pattern selection, distributed system design
- **software-engineer** (Sonnet) - Event handler implementation, consumer/producer code
- **security-engineer** (Opus) - Event security, authorization patterns, message encryption
- **senior-infrastructure-engineer** (Opus) - Message broker setup, Kafka clusters, queue configuration

## Key Concepts

### Message Queues

**RabbitMQ Implementation**:

```typescript
import amqp, { Channel, Connection } from "amqplib";

interface QueueConfig {
  name: string;
  durable: boolean;
  deadLetterExchange?: string;
  messageTtl?: number;
  maxRetries?: number;
}

class RabbitMQClient {
  private connection: Connection | null = null;
  private channel: Channel | null = null;

  async connect(url: string): Promise<void> {
    this.connection = await amqp.connect(url);
    this.channel = await this.connection.createChannel();

    // Handle connection errors
    this.connection.on("error", (err) => {
      console.error("RabbitMQ connection error:", err);
      this.reconnect(url);
    });
  }

  async setupQueue(config: QueueConfig): Promise<void> {
    if (!this.channel) throw new Error("Not connected");

    const options: amqp.Options.AssertQueue = {
      durable: config.durable,
      arguments: {},
    };

    if (config.deadLetterExchange) {
      options.arguments!["x-dead-letter-exchange"] = config.deadLetterExchange;
    }
    if (config.messageTtl) {
      options.arguments!["x-message-ttl"] = config.messageTtl;
    }

    await this.channel.assertQueue(config.name, options);
  }

  async publish(
    queue: string,
    message: unknown,
    options?: PublishOptions
  ): Promise<void> {
    if (!this.channel) throw new Error("Not connected");

    const content = Buffer.from(JSON.stringify(message));
    const publishOptions: amqp.Options.Publish = {
      persistent: true,
      messageId: options?.messageId || crypto.randomUUID(),
      timestamp: Date.now(),
      headers: options?.headers,
    };

    this.channel.sendToQueue(queue, content, publishOptions);
  }

  async consume<T>(
    queue: string,
    handler: (
      message: T,
      ack: () => void,
      nack: (requeue?: boolean) => void
    ) => Promise<void>,
    options?: ConsumeOptions
  ): Promise<void> {
    if (!this.channel) throw new Error("Not connected");

    await this.channel.prefetch(options?.prefetch || 10);

    await this.channel.consume(queue, async (msg) => {
      if (!msg) return;

      try {
        const content: T = JSON.parse(msg.content.toString());
        const retryCount =
          (msg.properties.headers?.["x-retry-count"] as number) || 0;

        await handler(
          content,
          () => this.channel!.ack(msg),
          (requeue = false) => {
            if (requeue && retryCount < (options?.maxRetries || 3)) {
              // Requeue with incremented retry count
              this.channel!.nack(msg, false, false);
              this.publish(queue, content, {
                headers: { "x-retry-count": retryCount + 1 },
              });
            } else {
              this.channel!.nack(msg, false, false); // Send to DLQ
            }
          }
        );
      } catch (error) {
        console.error("Message processing error:", error);
        this.channel!.nack(msg, false, false);
      }
    });
  }
}
```

**AWS SQS Implementation**:

```typescript
import {
  SQSClient,
  SendMessageCommand,
  ReceiveMessageCommand,
  DeleteMessageCommand,
} from "@aws-sdk/client-sqs";

interface SQSMessage<T> {
  id: string;
  body: T;
  receiptHandle: string;
  approximateReceiveCount: number;
}

class SQSQueue<T> {
  private client: SQSClient;
  private queueUrl: string;

  constructor(queueUrl: string, region: string = "us-east-1") {
    this.client = new SQSClient({ region });
    this.queueUrl = queueUrl;
  }

  async send(
    message: T,
    options?: { delaySeconds?: number; deduplicationId?: string }
  ): Promise<string> {
    const command = new SendMessageCommand({
      QueueUrl: this.queueUrl,
      MessageBody: JSON.stringify(message),
      DelaySeconds: options?.delaySeconds,
      MessageDeduplicationId: options?.deduplicationId,
      MessageGroupId: options?.deduplicationId ? "default" : undefined,
    });

    const response = await this.client.send(command);
    return response.MessageId!;
  }

  async receive(
    maxMessages: number = 10,
    waitTimeSeconds: number = 20
  ): Promise<SQSMessage<T>[]> {
    const command = new ReceiveMessageCommand({
      QueueUrl: this.queueUrl,
      MaxNumberOfMessages: maxMessages,
      WaitTimeSeconds: waitTimeSeconds,
      AttributeNames: ["ApproximateReceiveCount"],
    });

    const response = await this.client.send(command);

    return (response.Messages || []).map((msg) => ({
      id: msg.MessageId!,
      body: JSON.parse(msg.Body!) as T,
      receiptHandle: msg.ReceiptHandle!,
      approximateReceiveCount: parseInt(
        msg.Attributes?.ApproximateReceiveCount || "1"
      ),
    }));
  }

  async delete(receiptHandle: string): Promise<void> {
    const command = new DeleteMessageCommand({
      QueueUrl: this.queueUrl,
      ReceiptHandle: receiptHandle,
    });
    await this.client.send(command);
  }

  async processMessages(
    handler: (message: T) => Promise<void>,
    options?: { maxRetries?: number; pollInterval?: number }
  ): Promise<void> {
    const maxRetries = options?.maxRetries || 3;

    while (true) {
      const messages = await this.receive();

      await Promise.all(
        messages.map(async (msg) => {
          try {
            await handler(msg.body);
            await this.delete(msg.receiptHandle);
          } catch (error) {
            console.error(`Error processing message ${msg.id}:`, error);

            if (msg.approximateReceiveCount >= maxRetries) {
              // Message will go to DLQ after visibility timeout
              console.warn(`Message ${msg.id} exceeded max retries`);
            }
            // Don't delete - will be reprocessed after visibility timeout
          }
        })
      );

      if (messages.length === 0 && options?.pollInterval) {
        await new Promise((r) => setTimeout(r, options.pollInterval));
      }
    }
  }
}
```

### Pub/Sub Patterns

**Kafka Implementation**:

```typescript
import { Kafka, Producer, Consumer, EachMessagePayload } from "kafkajs";

interface Event<T = unknown> {
  id: string;
  type: string;
  timestamp: Date;
  source: string;
  data: T;
  metadata?: Record<string, string>;
}

class KafkaEventBus {
  private kafka: Kafka;
  private producer: Producer | null = null;
  private consumers: Map<string, Consumer> = new Map();

  constructor(config: { brokers: string[]; clientId: string }) {
    this.kafka = new Kafka({
      clientId: config.clientId,
      brokers: config.brokers,
    });
  }

  async connect(): Promise<void> {
    this.producer = this.kafka.producer({
      idempotent: true,
      maxInFlightRequests: 5,
    });
    await this.producer.connect();
  }

  async publish<T>(
    topic: string,
    event: Omit<Event<T>, "id" | "timestamp">
  ): Promise<void> {
    if (!this.producer) throw new Error("Producer not connected");

    const fullEvent: Event<T> = {
      ...event,
      id: crypto.randomUUID(),
      timestamp: new Date(),
    };

    await this.producer.send({
      topic,
      messages: [
        {
          key:
            event.data && typeof event.data === "object" && "id" in event.data
              ? String((event.data as { id: unknown }).id)
              : fullEvent.id,
          value: JSON.stringify(fullEvent),
          headers: {
            "event-type": event.type,
            "event-source": event.source,
          },
        },
      ],
    });
  }

  async subscribe<T>(
    topics: string[],
    groupId: string,
    handler: (event: Event<T>) => Promise<void>,
    options?: { fromBeginning?: boolean }
  ): Promise<void> {
    const consumer = this.kafka.consumer({ groupId });
    await consumer.connect();

    for (const topic of topics) {
      await consumer.subscribe({
        topic,
        fromBeginning: options?.fromBeginning,
      });
    }

    this.consumers.set(groupId, consumer);

    await consumer.run({
      eachMessage: async ({
        topic,
        partition,
        message,
      }: EachMessagePayload) => {
        try {
          const event: Event<T> = JSON.parse(message.value!.toString());
          await handler(event);
        } catch (error) {
          console.error(
            `Error processing message from ${topic}:${partition}:`,
            error
          );
          throw error; // Will trigger retry based on consumer config
        }
      },
    });
  }

  async disconnect(): Promise<void> {
    await this.producer?.disconnect();
    for (const consumer of this.consumers.values()) {
      await consumer.disconnect();
    }
  }
}

// Usage
const eventBus = new KafkaEventBus({
  brokers: ["localhost:9092"],
  clientId: "order-service",
});

await eventBus.connect();

// Publish
await eventBus.publish<OrderCreatedData>("orders", {
  type: "order.created",
  source: "order-service",
  data: { orderId: "123", items: [], total: 99.99 },
});

// Subscribe
await eventBus.subscribe<OrderCreatedData>(
  ["orders"],
  "inventory-service",
  async (event) => {
    if (event.type === "order.created") {
      await reserveInventory(event.data);
    }
  }
);
```

**NATS Implementation**:

```typescript
import {
  connect,
  NatsConnection,
  StringCodec,
  JetStreamManager,
  JetStreamClient,
} from "nats";

class NATSEventBus {
  private nc: NatsConnection | null = null;
  private js: JetStreamClient | null = null;
  private sc = StringCodec();

  async connect(servers: string[]): Promise<void> {
    this.nc = await connect({ servers });

    // Setup JetStream for persistence
    const jsm = await this.nc.jetstreamManager();
    this.js = this.nc.jetstream();

    // Create stream if not exists
    try {
      await jsm.streams.add({
        name: "EVENTS",
        subjects: ["events.*"],
        retention: "limits",
        max_msgs: 1000000,
        max_age: 7 * 24 * 60 * 60 * 1000000000, // 7 days in nanoseconds
      });
    } catch (e) {
      // Stream might already exist
    }
  }

  async publish(subject: string, data: unknown): Promise<void> {
    if (!this.js) throw new Error("Not connected");

    await this.js.publish(
      `events.${subject}`,
      this.sc.encode(JSON.stringify(data))
    );
  }

  async subscribe(
    subject: string,
    durableName: string,
    handler: (data: unknown) => Promise<void>
  ): Promise<void> {
    if (!this.js) throw new Error("Not connected");

    const consumer = await this.js.consumers
      .get("EVENTS", durableName)
      .catch(async () => {
        // Create consumer if not exists
        const jsm = await this.nc!.jetstreamManager();
        await jsm.consumers.add("EVENTS", {
          durable_name: durableName,
          filter_subject: `events.${subject}`,
          ack_policy: "explicit",
          max_deliver: 3,
        });
        return this.js!.consumers.get("EVENTS", durableName);
      });

    const messages = await consumer.consume();

    for await (const msg of messages) {
      try {
        const data = JSON.parse(this.sc.decode(msg.data));
        await handler(data);
        msg.ack();
      } catch (error) {
        console.error("Error processing message:", error);
        msg.nak();
      }
    }
  }
}
```

### Event Sourcing

```typescript
interface DomainEvent {
  id: string;
  aggregateId: string;
  aggregateType: string;
  type: string;
  version: number;
  timestamp: Date;
  data: unknown;
  metadata: {
    userId?: string;
    correlationId?: string;
    causationId?: string;
  };
}

interface EventStore {
  append(events: DomainEvent[]): Promise<void>;
  getEvents(aggregateId: string, fromVersion?: number): Promise<DomainEvent[]>;
  getEventsByType(type: string, fromTimestamp?: Date): Promise<DomainEvent[]>;
}

// PostgreSQL Event Store
class PostgresEventStore implements EventStore {
  constructor(private pool: Pool) {}

  async append(events: DomainEvent[]): Promise<void> {
    const client = await this.pool.connect();

    try {
      await client.query("BEGIN");

      for (const event of events) {
        // Optimistic concurrency check
        const { rows } = await client.query(
          "SELECT MAX(version) as max_version FROM events WHERE aggregate_id = $1",
          [event.aggregateId]
        );

        const currentVersion = rows[0]?.max_version || 0;
        if (event.version !== currentVersion + 1) {
          throw new ConcurrencyError(
            `Expected version ${currentVersion + 1}, got ${event.version}`
          );
        }

        await client.query(
          `INSERT INTO events (id, aggregate_id, aggregate_type, type, version, timestamp, data, metadata)
           VALUES ($1, $2, $3, $4, $5, $6, $7, $8)`,
          [
            event.id,
            event.aggregateId,
            event.aggregateType,
            event.type,
            event.version,
            event.timestamp,
            JSON.stringify(event.data),
            JSON.stringify(event.metadata),
          ]
        );
      }

      await client.query("COMMIT");

      // Publish to event bus for projections
      for (const event of events) {
        await this.eventBus.publish(event);
      }
    } catch (error) {
      await client.query("ROLLBACK");
      throw error;
    } finally {
      client.release();
    }
  }

  async getEvents(
    aggregateId: string,
    fromVersion: number = 0
  ): Promise<DomainEvent[]> {
    const { rows } = await this.pool.query(
      `SELECT * FROM events
       WHERE aggregate_id = $1 AND version > $2
       ORDER BY version ASC`,
      [aggregateId, fromVersion]
    );

    return rows.map(this.rowToEvent);
  }
}

// Aggregate base class
abstract class Aggregate {
  private _id: string;
  private _version: number = 0;
  private _uncommittedEvents: DomainEvent[] = [];

  get id(): string {
    return this._id;
  }
  get version(): number {
    return this._version;
  }

  constructor(id: string) {
    this._id = id;
  }

  protected apply(
    event: Omit<
      DomainEvent,
      "id" | "aggregateId" | "aggregateType" | "version" | "timestamp"
    >
  ): void {
    const domainEvent: DomainEvent = {
      ...event,
      id: crypto.randomUUID(),
      aggregateId: this._id,
      aggregateType: this.constructor.name,
      version: this._version + 1,
      timestamp: new Date(),
    };

    this.when(domainEvent);
    this._version = domainEvent.version;
    this._uncommittedEvents.push(domainEvent);
  }

  protected abstract when(event: DomainEvent): void;

  loadFromHistory(events: DomainEvent[]): void {
    for (const event of events) {
      this.when(event);
      this._version = event.version;
    }
  }

  getUncommittedEvents(): DomainEvent[] {
    return [...this._uncommittedEvents];
  }

  clearUncommittedEvents(): void {
    this._uncommittedEvents = [];
  }
}

// Example: Order Aggregate
class Order extends Aggregate {
  private status:
    | "pending"
    | "confirmed"
    | "shipped"
    | "delivered"
    | "cancelled" = "pending";
  private items: OrderItem[] = [];
  private total: number = 0;

  static create(id: string, customerId: string, items: OrderItem[]): Order {
    const order = new Order(id);
    order.apply({
      type: "OrderCreated",
      data: { customerId, items },
      metadata: {},
    });
    return order;
  }

  confirm(): void {
    if (this.status !== "pending") {
      throw new Error("Can only confirm pending orders");
    }
    this.apply({
      type: "OrderConfirmed",
      data: { confirmedAt: new Date() },
      metadata: {},
    });
  }

  cancel(reason: string): void {
    if (["shipped", "delivered", "cancelled"].includes(this.status)) {
      throw new Error("Cannot cancel order in current status");
    }
    this.apply({
      type: "OrderCancelled",
      data: { reason, cancelledAt: new Date() },
      metadata: {},
    });
  }

  protected when(event: DomainEvent): void {
    switch (event.type) {
      case "OrderCreated":
        const data = event.data as { items: OrderItem[] };
        this.items = data.items;
        this.total = data.items.reduce(
          (sum, item) => sum + item.price * item.quantity,
          0
        );
        this.status = "pending";
        break;
      case "OrderConfirmed":
        this.status = "confirmed";
        break;
      case "OrderCancelled":
        this.status = "cancelled";
        break;
    }
  }
}
```

### CQRS (Command Query Responsibility Segregation)

```typescript
// Commands
interface Command {
  type: string;
  payload: unknown;
  metadata: {
    userId: string;
    correlationId: string;
    timestamp: Date;
  };
}

interface CommandHandler<T extends Command> {
  handle(command: T): Promise<void>;
}

// Command Bus
class CommandBus {
  private handlers: Map<string, CommandHandler<Command>> = new Map();

  register<T extends Command>(type: string, handler: CommandHandler<T>): void {
    this.handlers.set(type, handler as CommandHandler<Command>);
  }

  async dispatch(command: Command): Promise<void> {
    const handler = this.handlers.get(command.type);
    if (!handler) {
      throw new Error(`No handler registered for command: ${command.type}`);
    }
    await handler.handle(command);
  }
}

// Queries
interface Query<TResult> {
  type: string;
  params: unknown;
}

interface QueryHandler<TQuery extends Query<TResult>, TResult> {
  handle(query: TQuery): Promise<TResult>;
}

// Query Bus
class QueryBus {
  private handlers: Map<string, QueryHandler<Query<unknown>, unknown>> =
    new Map();

  register<TQuery extends Query<TResult>, TResult>(
    type: string,
    handler: QueryHandler<TQuery, TResult>
  ): void {
    this.handlers.set(type, handler as QueryHandler<Query<unknown>, unknown>);
  }

  async execute<TResult>(query: Query<TResult>): Promise<TResult> {
    const handler = this.handlers.get(query.type);
    if (!handler) {
      throw new Error(`No handler registered for query: ${query.type}`);
    }
    return handler.handle(query) as Promise<TResult>;
  }
}

// Read Model (Projection)
interface OrderReadModel {
  id: string;
  customerId: string;
  customerName: string;
  status: string;
  items: Array<{
    productId: string;
    productName: string;
    quantity: number;
    price: number;
  }>;
  total: number;
  createdAt: Date;
  updatedAt: Date;
}

class OrderProjection {
  constructor(private db: Database, private eventBus: EventBus) {
    this.setupSubscriptions();
  }

  private setupSubscriptions(): void {
    this.eventBus.subscribe("OrderCreated", this.onOrderCreated.bind(this));
    this.eventBus.subscribe("OrderConfirmed", this.onOrderConfirmed.bind(this));
    this.eventBus.subscribe("OrderCancelled", this.onOrderCancelled.bind(this));
  }

  private async onOrderCreated(event: DomainEvent): Promise<void> {
    const data = event.data as OrderCreatedData;

    // Enrich with customer data
    const customer = await this.db.customers.findById(data.customerId);

    // Enrich with product data
    const items = await Promise.all(
      data.items.map(async (item) => {
        const product = await this.db.products.findById(item.productId);
        return {
          ...item,
          productName: product.name,
        };
      })
    );

    await this.db.orderReadModels.create({
      id: event.aggregateId,
      customerId: data.customerId,
      customerName: customer.name,
      status: "pending",
      items,
      total: items.reduce((sum, i) => sum + i.price * i.quantity, 0),
      createdAt: event.timestamp,
      updatedAt: event.timestamp,
    });
  }

  private async onOrderConfirmed(event: DomainEvent): Promise<void> {
    await this.db.orderReadModels.update(event.aggregateId, {
      status: "confirmed",
      updatedAt: event.timestamp,
    });
  }

  private async onOrderCancelled(event: DomainEvent): Promise<void> {
    await this.db.orderReadModels.update(event.aggregateId, {
      status: "cancelled",
      updatedAt: event.timestamp,
    });
  }
}
```

### Saga Pattern for Distributed Transactions

```typescript
interface SagaStep<TData> {
  name: string;
  execute: (data: TData) => Promise<void>;
  compensate: (data: TData) => Promise<void>;
}

interface SagaDefinition<TData> {
  name: string;
  steps: SagaStep<TData>[];
}

interface SagaInstance {
  id: string;
  sagaName: string;
  data: unknown;
  currentStep: number;
  status: "running" | "completed" | "compensating" | "failed";
  completedSteps: string[];
  error?: string;
  startedAt: Date;
  updatedAt: Date;
}

class SagaOrchestrator {
  private sagas: Map<string, SagaDefinition<unknown>> = new Map();
  private store: SagaStore;

  register<TData>(saga: SagaDefinition<TData>): void {
    this.sagas.set(saga.name, saga as SagaDefinition<unknown>);
  }

  async start<TData>(sagaName: string, data: TData): Promise<string> {
    const saga = this.sagas.get(sagaName);
    if (!saga) throw new Error(`Saga not found: ${sagaName}`);

    const instance: SagaInstance = {
      id: crypto.randomUUID(),
      sagaName,
      data,
      currentStep: 0,
      status: "running",
      completedSteps: [],
      startedAt: new Date(),
      updatedAt: new Date(),
    };

    await this.store.save(instance);
    await this.executeNextStep(instance, saga);

    return instance.id;
  }

  private async executeNextStep(
    instance: SagaInstance,
    saga: SagaDefinition<unknown>
  ): Promise<void> {
    if (instance.currentStep >= saga.steps.length) {
      instance.status = "completed";
      await this.store.save(instance);
      return;
    }

    const step = saga.steps[instance.currentStep];

    try {
      await step.execute(instance.data);

      instance.completedSteps.push(step.name);
      instance.currentStep++;
      instance.updatedAt = new Date();
      await this.store.save(instance);

      await this.executeNextStep(instance, saga);
    } catch (error) {
      instance.status = "compensating";
      instance.error = error instanceof Error ? error.message : String(error);
      await this.store.save(instance);

      await this.compensate(instance, saga);
    }
  }

  private async compensate(
    instance: SagaInstance,
    saga: SagaDefinition<unknown>
  ): Promise<void> {
    // Execute compensations in reverse order
    for (let i = instance.completedSteps.length - 1; i >= 0; i--) {
      const stepName = instance.completedSteps[i];
      const step = saga.steps.find((s) => s.name === stepName);

      if (step) {
        try {
          await step.compensate(instance.data);
        } catch (error) {
          console.error(`Compensation failed for step ${stepName}:`, error);
          // Continue with other compensations
        }
      }
    }

    instance.status = "failed";
    instance.updatedAt = new Date();
    await this.store.save(instance);
  }
}

// Example: Order Fulfillment Saga
interface OrderFulfillmentData {
  orderId: string;
  customerId: string;
  items: Array<{ productId: string; quantity: number; price: number }>;
  paymentId?: string;
  shipmentId?: string;
}

const orderFulfillmentSaga: SagaDefinition<OrderFulfillmentData> = {
  name: "order-fulfillment",
  steps: [
    {
      name: "reserve-inventory",
      execute: async (data) => {
        await inventoryService.reserve(data.items);
      },
      compensate: async (data) => {
        await inventoryService.release(data.items);
      },
    },
    {
      name: "process-payment",
      execute: async (data) => {
        const total = data.items.reduce(
          (sum, i) => sum + i.price * i.quantity,
          0
        );
        const payment = await paymentService.charge(data.customerId, total);
        data.paymentId = payment.id;
      },
      compensate: async (data) => {
        if (data.paymentId) {
          await paymentService.refund(data.paymentId);
        }
      },
    },
    {
      name: "create-shipment",
      execute: async (data) => {
        const shipment = await shippingService.createShipment(
          data.orderId,
          data.items
        );
        data.shipmentId = shipment.id;
      },
      compensate: async (data) => {
        if (data.shipmentId) {
          await shippingService.cancelShipment(data.shipmentId);
        }
      },
    },
    {
      name: "confirm-order",
      execute: async (data) => {
        await orderService.confirm(data.orderId);
      },
      compensate: async (data) => {
        await orderService.cancel(data.orderId, "Saga compensation");
      },
    },
  ],
};
```

### Idempotency and Exactly-Once Delivery

```typescript
interface IdempotencyKey {
  key: string;
  response?: unknown;
  createdAt: Date;
  expiresAt: Date;
}

class IdempotencyService {
  constructor(private redis: Redis) {}

  async process<T>(
    key: string,
    operation: () => Promise<T>,
    ttlSeconds: number = 86400 // 24 hours
  ): Promise<T> {
    const lockKey = `idempotency:lock:${key}`;
    const dataKey = `idempotency:data:${key}`;

    // Try to acquire lock
    const locked = await this.redis.set(lockKey, "1", "EX", 30, "NX");

    if (!locked) {
      // Another process is handling this request, wait for result
      return this.waitForResult<T>(dataKey);
    }

    try {
      // Check if already processed
      const existing = await this.redis.get(dataKey);
      if (existing) {
        return JSON.parse(existing) as T;
      }

      // Execute operation
      const result = await operation();

      // Store result
      await this.redis.setex(dataKey, ttlSeconds, JSON.stringify(result));

      return result;
    } finally {
      await this.redis.del(lockKey);
    }
  }

  private async waitForResult<T>(
    dataKey: string,
    maxWaitMs: number = 30000
  ): Promise<T> {
    const startTime = Date.now();

    while (Date.now() - startTime < maxWaitMs) {
      const data = await this.redis.get(dataKey);
      if (data) {
        return JSON.parse(data) as T;
      }
      await new Promise((r) => setTimeout(r, 100));
    }

    throw new Error("Timeout waiting for idempotent operation result");
  }
}

// Message deduplication for consumers
class DeduplicatingConsumer<T> {
  constructor(
    private redis: Redis,
    private windowSeconds: number = 3600 // 1 hour dedup window
  ) {}

  async process(
    messageId: string,
    handler: () => Promise<T>
  ): Promise<{ result: T; duplicate: boolean }> {
    const dedupKey = `dedup:${messageId}`;

    // Check if already processed
    const existing = await this.redis.get(dedupKey);
    if (existing) {
      return { result: JSON.parse(existing) as T, duplicate: true };
    }

    // Process message
    const result = await handler();

    // Mark as processed
    await this.redis.setex(
      dedupKey,
      this.windowSeconds,
      JSON.stringify(result)
    );

    return { result, duplicate: false };
  }
}
```

### Dead Letter Queues

```typescript
interface DeadLetterMessage {
  id: string;
  originalQueue: string;
  originalMessage: unknown;
  error: string;
  failedAt: Date;
  retryCount: number;
  lastRetryAt?: Date;
}

class DeadLetterQueueManager {
  constructor(
    private dlqStore: DLQStore,
    private originalQueue: MessageQueue
  ) {}

  async moveToDeadLetter(
    message: unknown,
    originalQueue: string,
    error: Error,
    retryCount: number
  ): Promise<void> {
    const dlqMessage: DeadLetterMessage = {
      id: crypto.randomUUID(),
      originalQueue,
      originalMessage: message,
      error: error.message,
      failedAt: new Date(),
      retryCount,
    };

    await this.dlqStore.save(dlqMessage);

    // Alert on DLQ growth
    const dlqSize = await this.dlqStore.count(originalQueue);
    if (dlqSize > 100) {
      await this.alerting.warn({
        title: "DLQ Size Warning",
        message: `Dead letter queue for ${originalQueue} has ${dlqSize} messages`,
      });
    }
  }

  async retry(messageId: string): Promise<void> {
    const dlqMessage = await this.dlqStore.get(messageId);
    if (!dlqMessage) throw new Error("Message not found in DLQ");

    try {
      await this.originalQueue.publish(
        dlqMessage.originalQueue,
        dlqMessage.originalMessage
      );
      await this.dlqStore.delete(messageId);
    } catch (error) {
      dlqMessage.lastRetryAt = new Date();
      dlqMessage.retryCount++;
      await this.dlqStore.save(dlqMessage);
      throw error;
    }
  }

  async retryAll(queue: string): Promise<{ success: number; failed: number }> {
    const messages = await this.dlqStore.getByQueue(queue);
    let success = 0;
    let failed = 0;

    for (const message of messages) {
      try {
        await this.retry(message.id);
        success++;
      } catch {
        failed++;
      }
    }

    return { success, failed };
  }

  async purge(queue: string, olderThan?: Date): Promise<number> {
    return this.dlqStore.deleteByQueue(queue, olderThan);
  }
}
```

### Data Streaming with Kafka

**Stream Processing**:

```typescript
import { Kafka, CompressionTypes } from "kafkajs";

interface StreamRecord<T> {
  key: string;
  value: T;
  timestamp: number;
  partition: number;
  offset: string;
}

class KafkaStreamProcessor {
  private kafka: Kafka;

  constructor(brokers: string[]) {
    this.kafka = new Kafka({
      clientId: "stream-processor",
      brokers,
    });
  }

  // Stateful stream aggregation
  async aggregateStream<TInput, TState>(
    inputTopic: string,
    outputTopic: string,
    groupId: string,
    initialState: TState,
    aggregator: (state: TState, record: TInput) => TState,
    windowMs: number = 60000
  ): Promise<void> {
    const consumer = this.kafka.consumer({ groupId });
    const producer = this.kafka.producer({
      compression: CompressionTypes.GZIP,
    });

    await consumer.connect();
    await producer.connect();
    await consumer.subscribe({ topic: inputTopic });

    const stateByKey = new Map<string, TState>();
    const windowTimers = new Map<string, NodeJS.Timeout>();

    await consumer.run({
      eachMessage: async ({ message }) => {
        const key = message.key?.toString() || "default";
        const value: TInput = JSON.parse(message.value!.toString());

        // Get or initialize state
        const currentState = stateByKey.get(key) || initialState;
        const newState = aggregator(currentState, value);
        stateByKey.set(key, newState);

        // Clear existing window timer
        const existingTimer = windowTimers.get(key);
        if (existingTimer) clearTimeout(existingTimer);

        // Set new window timer to emit aggregated state
        const timer = setTimeout(async () => {
          const finalState = stateByKey.get(key);
          await producer.send({
            topic: outputTopic,
            messages: [
              {
                key,
                value: JSON.stringify(finalState),
                timestamp: Date.now().toString(),
              },
            ],
          });
          stateByKey.delete(key);
          windowTimers.delete(key);
        }, windowMs);

        windowTimers.set(key, timer);
      },
    });
  }

  // Stream joins
  async joinStreams<TLeft, TRight, TResult>(
    leftTopic: string,
    rightTopic: string,
    outputTopic: string,
    groupId: string,
    joiner: (left: TLeft, right: TRight) => TResult,
    windowMs: number = 30000
  ): Promise<void> {
    const consumer = this.kafka.consumer({ groupId });
    const producer = this.kafka.producer();

    await consumer.connect();
    await producer.connect();
    await consumer.subscribe({ topics: [leftTopic, rightTopic] });

    const leftCache = new Map<string, { data: TLeft; timestamp: number }>();
    const rightCache = new Map<string, { data: TRight; timestamp: number }>();

    await consumer.run({
      eachMessage: async ({ topic, message }) => {
        const key = message.key?.toString() || "default";
        const timestamp = parseInt(message.timestamp);
        const now = Date.now();

        // Clean old entries
        this.cleanOldEntries(leftCache, now, windowMs);
        this.cleanOldEntries(rightCache, now, windowMs);

        if (topic === leftTopic) {
          const leftData: TLeft = JSON.parse(message.value!.toString());
          leftCache.set(key, { data: leftData, timestamp });

          // Try to join with right
          const rightEntry = rightCache.get(key);
          if (
            rightEntry &&
            Math.abs(timestamp - rightEntry.timestamp) <= windowMs
          ) {
            const result = joiner(leftData, rightEntry.data);
            await producer.send({
              topic: outputTopic,
              messages: [{ key, value: JSON.stringify(result) }],
            });
          }
        } else {
          const rightData: TRight = JSON.parse(message.value!.toString());
          rightCache.set(key, { data: rightData, timestamp });

          // Try to join with left
          const leftEntry = leftCache.get(key);
          if (
            leftEntry &&
            Math.abs(timestamp - leftEntry.timestamp) <= windowMs
          ) {
            const result = joiner(leftEntry.data, rightData);
            await producer.send({
              topic: outputTopic,
              messages: [{ key, value: JSON.stringify(result) }],
            });
          }
        }
      },
    });
  }

  private cleanOldEntries<T>(
    cache: Map<string, { data: T; timestamp: number }>,
    now: number,
    windowMs: number
  ): void {
    for (const [key, entry] of cache.entries()) {
      if (now - entry.timestamp > windowMs) {
        cache.delete(key);
      }
    }
  }
}

// Kafka Streams-style operations
class KafkaStream<T> {
  constructor(private kafka: Kafka, private topic: string) {}

  // Map transformation
  map<R>(mapper: (value: T) => R): KafkaStream<R> {
    const outputTopic = `${this.topic}-mapped`;
    this.processStream(outputTopic, async (record) => ({
      key: record.key,
      value: mapper(record.value),
    }));
    return new KafkaStream<R>(this.kafka, outputTopic);
  }

  // Filter transformation
  filter(predicate: (value: T) => boolean): KafkaStream<T> {
    const outputTopic = `${this.topic}-filtered`;
    this.processStream(outputTopic, async (record) =>
      predicate(record.value) ? record : null
    );
    return new KafkaStream<T>(this.kafka, outputTopic);
  }

  // Group by key and aggregate
  groupBy<K, V>(
    keyExtractor: (value: T) => K,
    aggregator: (key: K, values: T[]) => V,
    windowMs: number = 60000
  ): KafkaStream<V> {
    const outputTopic = `${this.topic}-grouped`;
    const groups = new Map<string, T[]>();
    const timers = new Map<string, NodeJS.Timeout>();

    this.processStream(outputTopic, async (record, producer) => {
      const key = String(keyExtractor(record.value));
      const values = groups.get(key) || [];
      values.push(record.value);
      groups.set(key, values);

      const existingTimer = timers.get(key);
      if (existingTimer) clearTimeout(existingTimer);

      const timer = setTimeout(async () => {
        const groupValues = groups.get(key) || [];
        const result = aggregator(keyExtractor(record.value), groupValues);
        await producer.send({
          topic: outputTopic,
          messages: [{ key, value: JSON.stringify(result) }],
        });
        groups.delete(key);
        timers.delete(key);
      }, windowMs);

      timers.set(key, timer);

      return null; // Don't emit immediately
    });

    return new KafkaStream<V>(this.kafka, outputTopic);
  }

  private async processStream(
    outputTopic: string,
    processor: (
      record: StreamRecord<T>,
      producer: any
    ) => Promise<{ key: string; value: any } | null>
  ): Promise<void> {
    const consumer = this.kafka.consumer({
      groupId: `${this.topic}-processor`,
    });
    const producer = this.kafka.producer();

    await consumer.connect();
    await producer.connect();
    await consumer.subscribe({ topic: this.topic });

    await consumer.run({
      eachMessage: async ({ message, partition }) => {
        const record: StreamRecord<T> = {
          key: message.key?.toString() || "default",
          value: JSON.parse(message.value!.toString()),
          timestamp: parseInt(message.timestamp),
          partition,
          offset: message.offset,
        };

        const result = await processor(record, producer);
        if (result) {
          await producer.send({
            topic: outputTopic,
            messages: [
              {
                key: result.key,
                value: JSON.stringify(result.value),
              },
            ],
          });
        }
      },
    });
  }
}
```

### Event Sourcing Patterns

**Snapshots for Performance**:

```typescript
interface Snapshot {
  aggregateId: string;
  version: number;
  state: unknown;
  timestamp: Date;
}

class SnapshotStore {
  constructor(private db: Database) {}

  async save(snapshot: Snapshot): Promise<void> {
    await this.db.snapshots.upsert({
      aggregateId: snapshot.aggregateId,
      version: snapshot.version,
      state: JSON.stringify(snapshot.state),
      timestamp: snapshot.timestamp,
    });
  }

  async getLatest(aggregateId: string): Promise<Snapshot | null> {
    const row = await this.db.snapshots.findOne(
      { aggregateId },
      { orderBy: { version: "desc" } }
    );
    return row
      ? {
          aggregateId: row.aggregateId,
          version: row.version,
          state: JSON.parse(row.state),
          timestamp: row.timestamp,
        }
      : null;
  }
}

// Enhanced aggregate with snapshots
abstract class SnapshotAggregate extends Aggregate {
  private static SNAPSHOT_FREQUENCY = 100; // Snapshot every 100 events

  async load(
    eventStore: EventStore,
    snapshotStore: SnapshotStore
  ): Promise<void> {
    // Try to load from snapshot first
    const snapshot = await snapshotStore.getLatest(this.id);
    if (snapshot) {
      this.applySnapshot(snapshot.state);
      this._version = snapshot.version;

      // Load events since snapshot
      const events = await eventStore.getEvents(this.id, snapshot.version);
      this.loadFromHistory(events);
    } else {
      // No snapshot, load all events
      const events = await eventStore.getEvents(this.id);
      this.loadFromHistory(events);
    }
  }

  async save(
    eventStore: EventStore,
    snapshotStore: SnapshotStore
  ): Promise<void> {
    const events = this.getUncommittedEvents();
    await eventStore.append(events);
    this.clearUncommittedEvents();

    // Create snapshot if needed
    if (this.version % SnapshotAggregate.SNAPSHOT_FREQUENCY === 0) {
      await snapshotStore.save({
        aggregateId: this.id,
        version: this.version,
        state: this.createSnapshot(),
        timestamp: new Date(),
      });
    }
  }

  protected abstract createSnapshot(): unknown;
  protected abstract applySnapshot(state: unknown): void;
}
```

**Event Upcasting (Schema Migration)**:

```typescript
interface EventUpcaster {
  eventType: string;
  fromVersion: number;
  toVersion: number;
  upcast: (event: DomainEvent) => DomainEvent;
}

class EventStoreWithUpcasting implements EventStore {
  private upcasters: Map<string, EventUpcaster[]> = new Map();

  registerUpcaster(upcaster: EventUpcaster): void {
    const existing = this.upcasters.get(upcaster.eventType) || [];
    existing.push(upcaster);
    existing.sort((a, b) => a.fromVersion - b.fromVersion);
    this.upcasters.set(upcaster.eventType, existing);
  }

  async getEvents(
    aggregateId: string,
    fromVersion: number = 0
  ): Promise<DomainEvent[]> {
    const rawEvents = await this.rawEventStore.getEvents(
      aggregateId,
      fromVersion
    );

    return rawEvents.map((event) => this.upcastEvent(event));
  }

  private upcastEvent(event: DomainEvent): DomainEvent {
    const upcasters = this.upcasters.get(event.type) || [];
    let currentEvent = event;

    for (const upcaster of upcasters) {
      const eventVersion = (currentEvent.data as any)?.schemaVersion || 1;
      if (eventVersion === upcaster.fromVersion) {
        currentEvent = upcaster.upcast(currentEvent);
      }
    }

    return currentEvent;
  }
}

// Example upcaster
const orderCreatedV1toV2: EventUpcaster = {
  eventType: "OrderCreated",
  fromVersion: 1,
  toVersion: 2,
  upcast: (event) => ({
    ...event,
    data: {
      ...(event.data as any),
      // V2 added shipping address separate from billing
      shippingAddress: (event.data as any).address,
      billingAddress: (event.data as any).address,
      schemaVersion: 2,
    },
  }),
};
```

### Saga Patterns

**Choreography vs Orchestration**:

```typescript
// CHOREOGRAPHY: Services react to events independently
class OrderService {
  async onOrderCreated(event: OrderCreatedEvent): Promise<void> {
    // Publish event, other services react
    await this.eventBus.publish("order.created", {
      orderId: event.orderId,
      customerId: event.customerId,
      items: event.items,
    });
  }
}

class InventoryService {
  constructor(private eventBus: EventBus) {
    // Listen and react to order events
    this.eventBus.subscribe("order.created", this.reserveInventory.bind(this));
  }

  private async reserveInventory(event: OrderCreatedEvent): Promise<void> {
    try {
      await this.reserve(event.items);
      // Publish success event
      await this.eventBus.publish("inventory.reserved", {
        orderId: event.orderId,
      });
    } catch (error) {
      // Publish failure event
      await this.eventBus.publish("inventory.reservation-failed", {
        orderId: event.orderId,
        reason: error.message,
      });
    }
  }
}

class PaymentService {
  constructor(private eventBus: EventBus) {
    // Wait for inventory before processing payment
    this.eventBus.subscribe(
      "inventory.reserved",
      this.processPayment.bind(this)
    );
  }

  private async processPayment(event: InventoryReservedEvent): Promise<void> {
    // Process payment and publish result...
  }
}

// ORCHESTRATION: Central coordinator controls flow
class OrderFulfillmentOrchestrator {
  async fulfillOrder(orderId: string): Promise<void> {
    try {
      // Step 1: Reserve inventory
      await this.inventoryService.reserve(orderId);

      // Step 2: Process payment
      await this.paymentService.charge(orderId);

      // Step 3: Create shipment
      await this.shippingService.createShipment(orderId);

      // Step 4: Confirm order
      await this.orderService.confirm(orderId);
    } catch (error) {
      // Explicit compensation
      await this.compensate(orderId);
    }
  }

  private async compensate(orderId: string): Promise<void> {
    // Undo in reverse order
    await this.shippingService.cancelShipment(orderId);
    await this.paymentService.refund(orderId);
    await this.inventoryService.release(orderId);
    await this.orderService.cancel(orderId);
  }
}
```

**Saga State Machine**:

```typescript
type SagaState =
  | "STARTED"
  | "INVENTORY_RESERVED"
  | "PAYMENT_PROCESSED"
  | "SHIPPED"
  | "COMPLETED"
  | "COMPENSATING"
  | "FAILED";

interface SagaStateMachine<TData> {
  state: SagaState;
  data: TData;
  transitions: Map<SagaState, SagaTransition<TData>>;
}

interface SagaTransition<TData> {
  onEnter: (data: TData) => Promise<void>;
  onSuccess: SagaState;
  onFailure: SagaState;
  compensate?: (data: TData) => Promise<void>;
}

class StatefulSagaOrchestrator<TData> {
  async execute(saga: SagaStateMachine<TData>): Promise<void> {
    let currentState = saga.state;

    while (currentState !== "COMPLETED" && currentState !== "FAILED") {
      const transition = saga.transitions.get(currentState);
      if (!transition)
        throw new Error(`No transition for state: ${currentState}`);

      try {
        await transition.onEnter(saga.data);
        currentState = transition.onSuccess;
        saga.state = currentState;
        await this.persistSaga(saga); // Save state
      } catch (error) {
        // Compensation
        if (transition.compensate) {
          await transition.compensate(saga.data);
        }
        currentState = transition.onFailure;
        saga.state = currentState;
        await this.persistSaga(saga);
      }
    }
  }

  private async persistSaga(saga: SagaStateMachine<TData>): Promise<void> {
    // Save saga state for recovery
    await this.sagaStore.save({
      id: (saga.data as any).orderId,
      state: saga.state,
      data: saga.data,
      updatedAt: new Date(),
    });
  }
}
```

## Best Practices

1. **Event Design**

   - Events should be immutable and represent facts
   - Use past tense naming (OrderCreated, not CreateOrder)
   - Include all necessary data; avoid references to mutable state
   - Version your events for schema evolution

2. **Idempotency**

   - Always design consumers to be idempotent
   - Use unique message IDs for deduplication
   - Store processing state to handle retries

3. **Error Handling**

   - Implement dead letter queues for failed messages
   - Set reasonable retry limits with exponential backoff
   - Monitor DLQ size and alert on growth

4. **Ordering**

   - Use partition keys for ordering guarantees in Kafka
   - Understand at-least-once vs exactly-once semantics
   - Design for out-of-order message handling when needed

5. **Monitoring**
   - Track message lag, processing time, and error rates
   - Set up alerts for consumer lag
   - Monitor event store growth and query performance

## Examples

### Complete Order Processing Flow

```typescript
// 1. API receives order request
app.post("/orders", async (req, res) => {
  const command: CreateOrderCommand = {
    type: "CreateOrder",
    payload: req.body,
    metadata: {
      userId: req.user.id,
      correlationId: req.headers["x-correlation-id"] as string,
      timestamp: new Date(),
    },
  };

  await commandBus.dispatch(command);
  res.status(202).json({ message: "Order creation initiated" });
});

// 2. Command handler creates aggregate and persists events
class CreateOrderHandler implements CommandHandler<CreateOrderCommand> {
  async handle(command: CreateOrderCommand): Promise<void> {
    const order = Order.create(
      crypto.randomUUID(),
      command.payload.customerId,
      command.payload.items
    );

    await this.eventStore.append(order.getUncommittedEvents());
  }
}

// 3. Event published to Kafka, projections update read models
// 4. Saga orchestrator starts fulfillment process
// 5. Each saga step publishes events that update projections
```
