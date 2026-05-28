---
name: tes-events
description: Emit TES events, build event handlers, or work with the event spine. TES is the canonical event ledger - if it didn't emit a TES event, it didn't happen.
allowed-tools: Read, Grep, Glob, Edit, Write
---

# TES Events Skill

## Core Principle

**If it didn't emit a TES event, it didn't happen.**

TES (Takeback Event System) is the canonical event ledger. All meaningful actions across Wallet, Marketplace, Control Plane, Pricing, PINs, and Agents MUST emit TES events.

---

## Event Structure

### Mandatory Fields

```javascript
const event = {
  id: "ptc_evt_" + crypto.randomUUID(),
  type: "item.captured",  // See taxonomy below
  correlation_id: context.correlationId,  // REQUIRED
  causation_id: context.causationId,      // What triggered this
  idempotency_key: request.idempotencyKey,
  timestamp: new Date().toISOString(),
  entity_type: "item",
  entity_id: "ptc_item_abc123",
  source: {
    service: "consumer-wallet",
    version: "1.2.0",
    model: "qwen2.5-vl:32b",
  },
  payload: { /* event-specific */ },
  schema_version: "v1",
};
```

---

## Event Taxonomy

### Item Events
| Type | When |
|------|------|
| `item.captured` | Photo taken |
| `item.identified` | Product matched |
| `item.enriched` | Attributes extracted |
| `item.listed` | Put on marketplace |
| `item.sold` | Transaction completed |
| `item.shipped` | Shipped to buyer |

### Value Events
| Type | When |
|------|------|
| `value.estimated` | Price estimate generated |
| `value.calibrated` | Model updated |
| `value.realised` | Actual sale recorded |

### Agent Events
| Type | When |
|------|------|
| `agent.plan_created` | Agent made a plan |
| `agent.action_executed` | Agent took action |
| `policy.blocked` | Policy gate blocked |

---

## Emitter Implementation

```javascript
const TES_ENDPOINT = "https://tes.pentatonic.com/api/v1/events";

export async function emitTESEvent(event, env, context) {
  if (!event.correlation_id) {
    throw new Error("TES event must have correlation_id");
  }

  const fullEvent = {
    id: event.id || `ptc_evt_${crypto.randomUUID()}`,
    timestamp: new Date().toISOString(),
    schema_version: "v1",
    ...event,
    source: { service: context.serviceName, ...event.source },
  };

  try {
    const response = await fetch(TES_ENDPOINT, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(fullEvent),
    });
    return { success: true, eventId: fullEvent.id };
  } catch (error) {
    await env.TES_RETRY_QUEUE.send({ event: fullEvent, attempt: 1 });
    return { success: false, queued: true };
  }
}
```

---

## Correlation ID Propagation

```javascript
// Entry point - get or create
const correlationId = request.headers.get("X-Correlation-ID") || crypto.randomUUID();

// Service-to-service - always forward
await fetch(url, {
  headers: {
    "X-Correlation-ID": context.correlationId,
    "X-Causation-ID": currentEventId,
  },
});
```

---

## Anti-Patterns

- Missing correlation_id
- Silently swallowing errors
- Mutating state without event
- Inventing IDs without ptc_ prefix
