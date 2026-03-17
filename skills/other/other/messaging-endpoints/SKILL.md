---
name: messaging-endpoints
description: |
    Use when designing how applications connect to and consume messages from a messaging system based on Enterprise Integration Patterns (Hohpe & Woolf).
    USE FOR: consumer patterns, polling vs event-driven consumers, competing consumers, idempotent receivers, transactional messaging, durable subscribers, service activators
    DO NOT USE FOR: channel types (use messaging-channels), routing logic (use message-routing)
license: MIT
metadata:
  displayName: "Messaging Endpoints"
  author: "Tyler-R-Kendrick"
compatibility: claude, copilot, cursor
references:
  - title: "Enterprise Integration Patterns — Messaging Endpoints"
    url: "https://www.enterpriseintegrationpatterns.com/patterns/messaging/MessagingEndpointsIntro.html"
  - title: "Enterprise Integration Patterns — Hohpe & Woolf"
    url: "https://www.enterpriseintegrationpatterns.com/"
---

# Messaging Endpoints

## Overview
Messaging Endpoints are the connection points where applications meet the messaging system. They encapsulate the messaging API, shielding application code from infrastructure details. These patterns address how consumers receive messages, how to scale consumption, how to handle duplicates and transactions, and how to activate business logic from incoming messages.

## Patterns

### Polling Consumer
The consumer actively polls the channel at intervals, pulling messages when available.

```
┌──────────┐         ┌──────────┐
│ Channel  │<──poll──│ Consumer │
│          │──msg───>│          │
│          │         │ (timer:  │
│          │<──poll──│  every   │
│          │──empty─>│  500ms)  │
└──────────┘         └──────────┘
```

**When to use:** Batch processing, scheduled jobs, when the consumer needs to control its own processing rate. Good for systems that cannot accept inbound connections.

**Trade-offs:** Simple to implement, but introduces latency (up to one poll interval). Polling an empty queue wastes resources.

### Event-Driven Consumer
The consumer registers a callback or handler that the messaging system invokes when a message arrives.

```
┌──────────┐         ┌──────────┐
│ Channel  │──push──>│ Consumer │
│          │         │ (handler │
│          │──push──>│  invoked │
│          │         │  on each │
│          │──push──>│  message)│
└──────────┘         └──────────┘
```

**When to use:** Low-latency processing, real-time event handling, when the messaging infrastructure supports push delivery. The most common consumer pattern.

**Trade-offs:** Lower latency than polling, but the consumer must handle backpressure if messages arrive faster than processing speed.

### Competing Consumers
Multiple consumers read from the same Point-to-Point Channel, competing for messages. Each message is delivered to exactly one consumer.

```
                     ┌────────────┐
                ┌───>│ Consumer 1 │
┌──────────┐    │    └────────────┘
│ Channel  │────┤    ┌────────────┐
│ (queue)  │────┤───>│ Consumer 2 │
└──────────┘    │    └────────────┘
                │    ┌────────────┐
                └───>│ Consumer 3 │
                     └────────────┘
         (each message goes to exactly one)
```

**When to use:** Horizontal scaling of message processing. Add consumers to increase throughput, remove them to save resources. Essential for work-queue patterns.

**Trade-offs:** Message ordering is not guaranteed across consumers. If ordering matters, use a single consumer or partition by key.

### Message Dispatcher
A single endpoint receives messages and dispatches them to the appropriate handler based on message type.

```
┌──────────┐    ┌────────────────┐    ┌─────────────────┐
│ Channel  │───>│   Dispatcher   │───>│ OrderHandler    │
└──────────┘    │                │    └─────────────────┘
                │ (inspects type │    ┌─────────────────┐
                │  and routes    │───>│ PaymentHandler  │
                │  to handler)   │    └─────────────────┘
                └────────────────┘    ┌─────────────────┐
                                 └───>│ ShippingHandler │
                                      └─────────────────┘
```

**When to use:** When a single channel carries multiple message types and you want to route to type-specific handlers in-process. Keeps channel topology simple.

### Selective Consumer
A consumer that filters messages on the channel, only accepting those matching specific criteria. Unmatched messages remain on the channel for other consumers.

```
┌──────────┐         ┌─────────────────┐
│ Channel  │────────>│ Consumer        │
│          │         │ (filter:        │
│ [A,B,A,C]│         │  type == "A")   │
│          │         │                 │
└──────────┘         │ Accepts: A, A   │
                     │ Ignores: B, C   │
                     └─────────────────┘
```

**When to use:** When multiple consumer types share a channel and each should only process its relevant messages. Alternative to Datatype Channels when channel proliferation is undesirable.

### Durable Subscriber
A subscriber whose subscription persists even when the subscriber is offline. Messages published while the subscriber is disconnected are stored and delivered when it reconnects.

```
┌───────────┐     ┌───────────────┐     ┌──────────────────┐
│ Publisher │────>│ Pub-Sub       │────>│ Durable          │
└───────────┘     │ Channel       │     │ Subscriber       │
                  │               │     │ (offline OK --   │
                  │ ┌───────────┐ │     │  messages queued)│
                  │ │ Stored    │ │     └──────────────────┘
                  │ │ Messages  │ │
                  │ └───────────┘ │
                  └───────────────┘
```

**When to use:** When subscribers may have downtime (deployments, maintenance, crashes) and must not miss any events. Standard for production event-driven systems.

### Idempotent Receiver
A consumer that can safely process the same message multiple times, producing the same result. Essential for at-least-once delivery systems.

```
┌──────────┐    ┌─────────────────────────────────────┐
│ Channel  │───>│ Idempotent Receiver                 │
│          │    │                                     │
│ msg-001  │    │  1. Check: seen msg-001 before?     │
│ msg-001  │    │     YES -> skip (already processed) │
│ (retry)  │    │     NO  -> process and record ID    │
└──────────┘    │                                     │
                │  ┌────────────────┐                 │
                │  │ Processed IDs  │                 │
                │  │ { msg-001 }    │                 │
                │  └────────────────┘                 │
                └─────────────────────────────────────┘
```

**When to use:** Always. Most messaging systems provide at-least-once delivery, meaning duplicates are possible. Idempotent receivers are the standard defence.

**Implementation strategies:**
- **Deduplication table:** Store processed message IDs, check before processing.
- **Natural idempotency:** Design operations to be inherently idempotent (e.g., "set balance to X" vs. "add X to balance").
- **Idempotency key:** Use a business key (orderId + operation) rather than just messageId.

### Transactional Client
Coordinates message consumption with local data changes in a single transaction, ensuring messages are acknowledged only when processing succeeds.

```
┌──────────┐    ┌───────────────────────────────────┐
│ Channel  │───>│ Transactional Client              │
└──────────┘    │                                   │
                │  BEGIN TRANSACTION                 │
                │    1. Receive message              │
                │    2. Update database              │
                │    3. Send outgoing message        │
                │  COMMIT (or ROLLBACK)              │
                │                                   │
                │  Message ACK only on COMMIT       │
                └───────────────────────────────────┘
```

**When to use:** When message processing must be atomic with database changes. Common in financial systems, inventory management, and any system where partial processing is unacceptable.

**Trade-offs:** Distributed transactions (2PC) are expensive. Prefer the Outbox Pattern (store outgoing messages in the local DB, publish asynchronously) when cross-resource transactions are unavailable.

### Service Activator
Connects a service to the messaging system, invoking the service when a message arrives and optionally sending a reply.

```
┌──────────┐    ┌──────────────────┐    ┌──────────────┐
│ Request  │───>│ Service          │───>│ Business     │
│ Channel  │    │ Activator        │    │ Service      │
└──────────┘    │ (adapter layer)  │    │ (no messaging│
                └──────────────────┘    │  dependency) │
                         │              └──────────────┘
                         v
                ┌──────────────┐
                │ Reply Channel│
                └──────────────┘
```

**When to use:** Exposing an existing service (designed for synchronous calls) via messaging without modifying the service itself. Separates messaging infrastructure from business logic.

## At-Least-Once vs. Exactly-Once Delivery

| Guarantee | Description | Achievable? |
|-----------|-------------|-------------|
| **At-most-once** | Message delivered 0 or 1 times; may be lost | Yes (fire and forget) |
| **At-least-once** | Message delivered 1 or more times; may be duplicated | Yes (ACK after processing) |
| **Exactly-once** | Message delivered exactly 1 time | Effectively yes, via idempotent processing |

**Practical reality:** True exactly-once delivery across distributed systems is theoretically impossible in the general case. The industry standard is **at-least-once delivery + idempotent receivers**, which provides effectively-exactly-once processing semantics.

```
At-Least-Once Delivery + Idempotent Receiver = Effectively Exactly-Once Processing
```

## Choosing the Right Endpoint Pattern

| Requirement | Pattern |
|-------------|---------|
| Consumer controls processing pace | Polling Consumer |
| Lowest latency message handling | Event-Driven Consumer |
| Scale out message processing | Competing Consumers |
| Route to type-specific handlers in-process | Message Dispatcher |
| Consumer picks only relevant messages | Selective Consumer |
| Survive consumer downtime | Durable Subscriber |
| Handle duplicate messages safely | Idempotent Receiver |
| Atomic processing with data store | Transactional Client |
| Connect existing service to messaging | Service Activator |

## Best Practices
- Default to Event-Driven Consumer; use Polling Consumer only when you need explicit rate control or batch processing.
- Always implement Idempotent Receiver -- treat it as a non-negotiable baseline, not an optimisation.
- Use Competing Consumers for horizontal scaling, but be aware of ordering implications.
- Prefer Durable Subscriber for all production pub-sub subscriptions; non-durable subscriptions lose messages during deployments.
- Use the Outbox Pattern as a practical alternative to distributed transactions in Transactional Client scenarios.
- Service Activator is the pattern that keeps your business logic testable -- it should never import messaging libraries.
- Monitor consumer lag (the gap between published and consumed messages) as a key health metric.
- Set appropriate prefetch counts and concurrency limits; unbounded consumption can overwhelm downstream resources.
