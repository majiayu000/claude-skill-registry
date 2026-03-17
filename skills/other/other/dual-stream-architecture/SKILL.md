---
name: dual-stream-architecture
model: reasoning
description: Dual-stream event publishing combining Kafka for durability with Redis Pub/Sub for real-time delivery. Use when building event-driven systems needing both guaranteed delivery and low-latency updates. Triggers on dual stream, event publishing, Kafka Redis, real-time events, pub/sub, streaming architecture.
---

# Dual-Stream Architecture

Publish events to Kafka (durability) and Redis Pub/Sub (real-time) simultaneously for systems needing both guaranteed delivery and instant updates.


## Installation

### OpenClaw / Moltbot / Clawbot

```bash
npx clawhub@latest install dual-stream-architecture
```


---

## When to Use

- Event-driven systems needing both durability AND real-time
- WebSocket/SSE backends that push live updates
- Dashboards showing events as they happen
- Kafka consumers have lag but users expect instant updates

---

## Core Pattern

```go
type DualPublisher struct {
    kafka  *kafka.Writer
    redis  *redis.Client
    logger *slog.Logger
}

func (p *DualPublisher) Publish(ctx context.Context, event Event) error {
    // 1. Kafka: Critical path - must succeed
    payload, _ := json.Marshal(event)
    err := p.kafka.WriteMessages(ctx, kafka.Message{
        Key:   []byte(event.SourceID),
        Value: payload,
    })
    if err != nil {
        return fmt.Errorf("kafka publish failed: %w", err)
    }

    // 2. Redis: Best-effort - don't fail the operation
    p.publishToRedis(ctx, event)

    return nil
}

func (p *DualPublisher) publishToRedis(ctx context.Context, event Event) {
    // Lightweight payload (full event in Kafka)
    notification := map[string]interface{}{
        "id":        event.ID,
        "type":      event.Type,
        "source_id": event.SourceID,
    }

    payload, _ := json.Marshal(notification)
    channel := fmt.Sprintf("events:%s:%s", event.SourceType, event.SourceID)

    // Fire and forget - log errors but don't propagate
    if err := p.redis.Publish(ctx, channel, payload).Err(); err != nil {
        p.logger.Warn("redis publish failed", "error", err)
    }
}
```

---

## Architecture

```
┌──────────────┐     ┌─────────────────┐     ┌──────────────┐
│   Ingester   │────▶│  DualPublisher  │────▶│    Kafka     │──▶ Event Processor
│              │     │                 │     │  (durable)   │
└──────────────┘     │                 │     └──────────────┘
                     │                 │     ┌──────────────┐
                     │                 │────▶│ Redis PubSub │──▶ WebSocket Gateway
                     │                 │     │ (real-time)  │
                     └─────────────────┘     └──────────────┘
```

---

## Channel Naming Convention

```
events:{source_type}:{source_id}

Examples:
- events:user:octocat      - Events for user octocat
- events:repo:owner/repo   - Events for a repository
- events:org:microsoft     - Events for an organization
```

---

## Batch Publishing

For high throughput:

```go
func (p *DualPublisher) PublishBatch(ctx context.Context, events []Event) error {
    // 1. Batch to Kafka
    messages := make([]kafka.Message, len(events))
    for i, event := range events {
        payload, _ := json.Marshal(event)
        messages[i] = kafka.Message{
            Key:   []byte(event.SourceID),
            Value: payload,
        }
    }

    if err := p.kafka.WriteMessages(ctx, messages...); err != nil {
        return fmt.Errorf("kafka batch failed: %w", err)
    }

    // 2. Redis: Pipeline for efficiency
    pipe := p.redis.Pipeline()
    for _, event := range events {
        channel := fmt.Sprintf("events:%s:%s", event.SourceType, event.SourceID)
        notification, _ := json.Marshal(map[string]interface{}{
            "id":   event.ID,
            "type": event.Type,
        })
        pipe.Publish(ctx, channel, notification)
    }
    
    if _, err := pipe.Exec(ctx); err != nil {
        p.logger.Warn("redis batch failed", "error", err)
    }

    return nil
}
```

---

## Decision Tree

| Requirement | Stream | Why |
|-------------|--------|-----|
| Must not lose event | Kafka only | Ack required, replicated |
| User sees immediately | Redis only | Sub-ms delivery |
| Both durability + real-time | Dual stream | This pattern |
| High volume (>10k/sec) | Kafka, batch Redis | Redis can bottleneck |
| Many subscribers per channel | Redis + local fan-out | Don't hammer Redis |

---

## Related Skills

- **Meta-skill:** [ai/skills/meta/realtime-dashboard/](../../meta/realtime-dashboard/) — Complete realtime dashboard guide
- [websocket-hub-patterns](../websocket-hub-patterns/) — WebSocket gateway
- [backend/service-layer-architecture](../../backend/service-layer-architecture/) — Service integration

---

## NEVER Do

- **NEVER fail on Redis errors** — Redis is best-effort. Log and continue.
- **NEVER send full payload to Redis** — Send IDs only, clients fetch from API.
- **NEVER create one Redis channel per event** — Use source-level channels.
- **NEVER skip Kafka for "unimportant" events** — All events go to Kafka for replay.
- **NEVER use Redis Pub/Sub for persistence** — Messages are fire-and-forget.

---

## Edge Cases

| Case | Solution |
|------|----------|
| Redis down | Log warning, continue with Kafka only |
| Client connects mid-stream | Query API for recent events, then subscribe |
| High channel cardinality | Use wildcard patterns or aggregate channels |
| Kafka backpressure | Buffer in memory with timeout, fail if full |
| Need event replay | Consume from Kafka from offset, not Redis |
