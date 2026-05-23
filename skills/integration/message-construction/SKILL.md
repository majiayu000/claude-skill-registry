---
name: message-construction
description: |
    Use when designing message structure, intent, and metadata for enterprise messaging systems based on Enterprise Integration Patterns (Hohpe & Woolf).
    USE FOR: message types, command vs event vs document messages, request-reply, correlation, message sequencing, expiration, format indicators
    DO NOT USE FOR: channel selection (use messaging-channels), routing rules (use message-routing)
license: MIT
metadata:
  displayName: "Message Construction"
  author: "Tyler-R-Kendrick"
compatibility: claude, copilot, cursor
references:
  - title: "Enterprise Integration Patterns — Message Construction"
    url: "https://www.enterpriseintegrationpatterns.com/patterns/messaging/MessageConstructionIntro.html"
  - title: "Enterprise Integration Patterns — Hohpe & Woolf"
    url: "https://www.enterpriseintegrationpatterns.com/"
---

# Message Construction

## Overview
Message Construction patterns define what goes inside a message -- its intent, structure, metadata, and lifecycle. A well-constructed message is self-describing, carries the right amount of data, and enables the messaging system to route, correlate, and expire it correctly. Hohpe & Woolf identify patterns that address the intent of a message, how to correlate requests with replies, and how to manage message lifecycles.

## Patterns

### Command Message
Encodes an instruction to perform an action. Sent to a specific receiver on a Point-to-Point Channel.

```json
{
  "messageType": "command",
  "command": "PlaceOrder",
  "messageId": "cmd-8a3f-4b2c",
  "timestamp": "2025-01-15T10:30:00Z",
  "body": {
    "customerId": "cust-001",
    "items": [
      { "sku": "WIDGET-42", "quantity": 3 }
    ],
    "shippingAddress": "123 Main St"
  }
}
```

**When to use:** Invoking a specific action on a specific system -- order placement, account creation, state mutations.

### Document Message
Carries data without prescribing what the receiver should do with it. The sender transfers information; the receiver decides the action.

```json
{
  "messageType": "document",
  "documentType": "CustomerProfile",
  "messageId": "doc-9c4e-7d1a",
  "timestamp": "2025-01-15T10:31:00Z",
  "body": {
    "customerId": "cust-001",
    "name": "Jane Smith",
    "email": "jane@example.com",
    "tier": "gold",
    "lifetimeValue": 12500.00
  }
}
```

**When to use:** Data synchronisation, reporting feeds, transferring reference data between systems.

### Event Message
Notifies subscribers that something has happened. The sender does not dictate what receivers should do.

```json
{
  "messageType": "event",
  "eventType": "OrderPlaced",
  "messageId": "evt-2b7d-9e4f",
  "timestamp": "2025-01-15T10:32:00Z",
  "body": {
    "orderId": "order-5678",
    "customerId": "cust-001",
    "totalAmount": 149.97,
    "placedAt": "2025-01-15T10:30:00Z"
  }
}
```

**When to use:** Decoupled notification -- order placed, payment received, user registered. Publish on a Pub-Sub Channel.

### Request-Reply
A two-message exchange: the requestor sends a request and waits for a reply on a dedicated reply channel.

```json
// Request
{
  "messageType": "request",
  "messageId": "req-3c8a-1f2e",
  "replyTo": "channel://inventory-replies",
  "timestamp": "2025-01-15T10:33:00Z",
  "body": {
    "query": "CheckStock",
    "sku": "WIDGET-42"
  }
}

// Reply
{
  "messageType": "reply",
  "messageId": "rpl-7d4b-5a3c",
  "correlationId": "req-3c8a-1f2e",
  "timestamp": "2025-01-15T10:33:02Z",
  "body": {
    "sku": "WIDGET-42",
    "availableQuantity": 150,
    "warehouse": "US-EAST"
  }
}
```

**When to use:** When the sender needs a response but still wants temporal decoupling -- stock checks, credit approvals, price lookups.

### Return Address
Embeds the reply channel address in the request message so the receiver knows where to send the reply.

```json
{
  "messageId": "req-4a9b-2c1d",
  "replyTo": "channel://order-service/replies",
  "body": { "query": "GetOrderStatus", "orderId": "order-5678" }
}
```

**When to use:** Any Request-Reply scenario. Essential when multiple requestors share the same request channel.

### Correlation Identifier
A unique identifier placed in the reply message that references the original request, allowing the requestor to match replies to their requests.

```json
// Request (contains messageId)
{
  "messageId": "req-5b0c-3d2e",
  "replyTo": "channel://replies",
  "body": { "action": "ValidateAddress", "address": "123 Main St" }
}

// Reply (correlationId matches the request's messageId)
{
  "messageId": "rpl-8e1f-6a4b",
  "correlationId": "req-5b0c-3d2e",
  "body": { "valid": true, "normalised": "123 Main Street, Suite 100" }
}
```

**When to use:** Always use with Request-Reply. Critical when a requestor has multiple outstanding requests.

### Message Sequence
Marks messages as part of an ordered series when a large dataset must be split across multiple messages.

```json
{
  "messageId": "seq-6c1d-4e3f",
  "sequenceId": "batch-2025-01-15",
  "sequencePosition": 2,
  "sequenceSize": 5,
  "isLast": false,
  "body": {
    "records": [
      { "id": "rec-101", "value": "..." },
      { "id": "rec-102", "value": "..." }
    ]
  }
}
```

**When to use:** Transferring large datasets that exceed message size limits, ordered batch processing, streaming results.

### Message Expiration
Sets a time-to-live (TTL) on a message so it is discarded if not consumed before the deadline.

```json
{
  "messageId": "exp-7d2e-5f4a",
  "timestamp": "2025-01-15T10:30:00Z",
  "expiration": "2025-01-15T10:35:00Z",
  "body": {
    "type": "FlashSalePrice",
    "sku": "WIDGET-42",
    "price": 9.99
  }
}
```

**When to use:** Time-sensitive data (price quotes, session tokens, flash sales), preventing stale commands from executing.

### Format Indicator
Embeds version or format metadata in the message so consumers can handle multiple message schema versions.

```json
{
  "messageId": "fmt-8e3f-6a5b",
  "schemaVersion": "2.1",
  "contentType": "application/vnd.mycompany.order.v2+json",
  "body": {
    "orderId": "order-5678",
    "lineItems": [
      { "sku": "WIDGET-42", "qty": 3, "unitPrice": 49.99 }
    ]
  }
}
```

**When to use:** Schema evolution, multi-version consumers, gradual migration between message formats.

## Message Anatomy Reference

```json
{
  "messageId": "unique-id",
  "correlationId": "original-request-id",
  "causationId": "immediate-cause-message-id",
  "messageType": "command | event | document | request | reply",
  "schemaVersion": "1.0",
  "contentType": "application/json",
  "timestamp": "2025-01-15T10:30:00Z",
  "expiration": "2025-01-15T11:30:00Z",
  "replyTo": "channel://replies",
  "sequenceId": "batch-id",
  "sequencePosition": 1,
  "sequenceSize": 10,
  "headers": {
    "source": "order-service",
    "tenantId": "tenant-42"
  },
  "body": { }
}
```

## Choosing the Right Message Type

| Intent | Pattern |
|--------|---------|
| Tell a system to do something | Command Message |
| Transfer data without prescribing action | Document Message |
| Announce something happened | Event Message |
| Ask a question and wait for an answer | Request-Reply |
| Match a reply to its request | Correlation Identifier + Return Address |
| Send large data across multiple messages | Message Sequence |
| Prevent stale messages from being processed | Message Expiration |
| Support multiple schema versions | Format Indicator |

## Best Practices
- Give every message a unique `messageId` -- it is the foundation of idempotency, deduplication, and correlation.
- Prefer Event Messages for cross-service communication; they create the loosest coupling.
- Use Command Messages only when you intend exactly one receiver to act.
- Always include a `correlationId` in replies so requestors can match responses.
- Set `expiration` on time-sensitive messages rather than relying on consumers to check timestamps.
- Version your message schemas from day one using Format Indicator; schema evolution is inevitable.
- Keep message bodies lean -- carry references (IDs, URIs) rather than full object graphs when possible.
- Include `timestamp` and `source` in every message for observability and debugging.
