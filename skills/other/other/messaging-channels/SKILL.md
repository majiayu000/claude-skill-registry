---
name: messaging-channels
description: |
    Use when designing how messages travel between applications -- channel types, delivery guarantees, and bridging strategies from Enterprise Integration Patterns (Hohpe & Woolf).
    USE FOR: choosing channel types, point-to-point vs pub-sub, guaranteed delivery, dead letter handling, channel adapters, message bus topology
    DO NOT USE FOR: message format/structure (use message-construction), routing logic (use message-routing)
license: MIT
metadata:
  displayName: "Messaging Channels"
  author: "Tyler-R-Kendrick"
compatibility: claude, copilot, cursor
references:
  - title: "Enterprise Integration Patterns — Messaging Channels"
    url: "https://www.enterpriseintegrationpatterns.com/patterns/messaging/MessagingChannelsIntro.html"
  - title: "Enterprise Integration Patterns — Hohpe & Woolf"
    url: "https://www.enterpriseintegrationpatterns.com/"
---

# Messaging Channels

## Overview
Messaging Channels are the pipes in a pipes-and-filters architecture. They define how messages travel from sender to receiver, what delivery guarantees are provided, and how disparate systems connect to the messaging infrastructure. Hohpe & Woolf identify several channel patterns, each addressing a different integration concern.

## Patterns

### Point-to-Point Channel
Ensures a message is consumed by exactly one receiver. Used for command-style messages where only one consumer should act.

```
┌──────────┐         ┌─────────────────┐         ┌──────────┐
│ Sender   │────────>│  P2P Channel    │────────>│ Receiver │
└──────────┘         │  (one consumer) │         └──────────┘
                     └─────────────────┘
```

**When to use:** Task distribution, command dispatch, work queues where each message must be processed once.

### Publish-Subscribe Channel
Delivers a copy of each message to every subscriber. Used for event notification where multiple systems need to react.

```
                                          ┌──────────────┐
                                     ┌───>│ Subscriber A │
┌──────────┐     ┌──────────────┐    │    └──────────────┘
│ Publisher │────>│ Pub-Sub      │────┤
└──────────┘     │ Channel      │    │    ┌──────────────┐
                 └──────────────┘    └───>│ Subscriber B │
                                          └──────────────┘
```

**When to use:** Event broadcasting, notification fan-out, audit logging, keeping multiple systems in sync.

### Datatype Channel
Dedicates a channel to a single message type so consumers know exactly what to expect without inspecting message content.

```
┌──────────┐     ┌─────────────────────┐     ┌──────────┐
│ Sender   │────>│ "OrderCreated"      │────>│ Consumer │
└──────────┘     │  Channel            │     └──────────┘
                 └─────────────────────┘
┌──────────┐     ┌─────────────────────┐     ┌──────────┐
│ Sender   │────>│ "PaymentReceived"   │────>│ Consumer │
└──────────┘     │  Channel            │     └──────────┘
                 └─────────────────────┘
```

**When to use:** When consumers are type-specific, to avoid content-based filtering on the consumer side, and to simplify deserialization.

### Invalid Message Channel
A dedicated channel where the messaging system routes messages that cannot be processed -- malformed, unrecognised, or schema-violating.

```
┌──────────┐     ┌─────────────┐──── OK ────>┌──────────┐
│ Sender   │────>│  Validator  │             │ Consumer │
└──────────┘     └─────────────┘             └──────────┘
                       │
                    INVALID
                       │
                       v
                 ┌─────────────────┐
                 │ Invalid Message │
                 │ Channel         │
                 └─────────────────┘
```

**When to use:** Capturing malformed input for analysis without blocking the main processing pipeline.

### Dead Letter Channel
Receives messages that the messaging system could not deliver after all retry attempts are exhausted. A safety net for every queue.

```
┌──────────┐     ┌──────────┐     ┌──────────┐
│ Sender   │────>│ Channel  │────>│ Consumer │
└──────────┘     └──────────┘     └──────────┘
                      │                 │
                  undeliverable    processing
                  after retries    failure
                      │                │
                      v                v
                 ┌────────────────────────┐
                 │  Dead Letter Channel   │
                 └────────────────────────┘
```

**When to use:** Every production queue should have a dead letter channel. Essential for diagnosing delivery failures and preventing message loss.

### Guaranteed Delivery
Persists messages to durable storage before acknowledging the send, ensuring no message is lost even if the broker crashes.

```
┌──────────┐     ┌──────────────────────────┐     ┌──────────┐
│ Sender   │────>│ Channel                  │────>│ Receiver │
└──────────┘     │  ┌──────────────────┐    │     └──────────┘
                 │  │ Persistent Store │    │
                 │  │ (disk / DB)      │    │
                 │  └──────────────────┘    │
                 └──────────────────────────┘
```

**When to use:** Financial transactions, order processing, any message that must not be lost. Trade-off: higher latency for durability.

### Channel Adapter
Connects a non-messaging application to the messaging system, translating between the application's native API and the channel interface.

```
┌──────────────┐     ┌─────────────┐     ┌─────────────┐
│ Legacy App   │────>│  Channel    │────>│  Message     │
│ (HTTP, DB,   │     │  Adapter    │     │  Channel     │
│  file, etc.) │     └─────────────┘     └─────────────┘
└──────────────┘
```

**When to use:** Integrating legacy systems, databases, file systems, or REST APIs into a messaging topology without modifying the original application.

### Messaging Bridge
Connects two separate messaging systems, translating protocols and message formats between them.

```
┌───────────────┐     ┌───────────────┐     ┌───────────────┐
│  Messaging    │────>│   Messaging   │────>│  Messaging    │
│  System A     │     │   Bridge      │     │  System B     │
│  (RabbitMQ)   │     └───────────────┘     │  (Kafka)      │
└───────────────┘                           └───────────────┘
```

**When to use:** Migrating between brokers, connecting cloud and on-premise messaging, bridging organizational boundaries.

### Message Bus
A shared messaging infrastructure that all applications connect to, providing a common communication backbone with standardised message formats.

```
┌───────┐  ┌───────┐  ┌───────┐  ┌───────┐
│ App A │  │ App B │  │ App C │  │ App D │
└───┬───┘  └───┬───┘  └───┬───┘  └───┬───┘
    │          │          │          │
════╪══════════╪══════════╪══════════╪════
              Message Bus
══════════════════════════════════════════
```

**When to use:** Enterprise-wide integration where applications share a common canonical data model and communication infrastructure.

## Choosing the Right Channel

| Requirement | Pattern |
|-------------|---------|
| One consumer per message | Point-to-Point Channel |
| Multiple consumers per message | Publish-Subscribe Channel |
| Type-safe consumers | Datatype Channel |
| Handle malformed messages | Invalid Message Channel |
| Handle undeliverable messages | Dead Letter Channel |
| No message loss | Guaranteed Delivery |
| Connect non-messaging apps | Channel Adapter |
| Bridge two brokers | Messaging Bridge |
| Shared enterprise backbone | Message Bus |

## Best Practices
- Always configure a Dead Letter Channel for every production queue.
- Use Datatype Channels to keep consumers simple and avoid content inspection.
- Enable Guaranteed Delivery for any message whose loss has business impact.
- Prefer Publish-Subscribe for events and Point-to-Point for commands.
- Use Channel Adapters to isolate legacy integration code from business logic.
- Monitor channel depth and throughput; a growing queue signals a consumer that cannot keep up.
- Name channels after the message type or business purpose, not the producer or consumer.
