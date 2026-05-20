---
name: analyzing-messaging-layer
description: Use when analyzing event-driven systems, message queues, async processing, and pub/sub patterns
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash(mkdir:*, ls:*)
  - Write(docs/unwind/**)
  - Edit(docs/unwind/**)
---

# Analyzing Messaging Layer

**Output:** `docs/unwind/layers/messaging/` (folder with index.md + section files)

**Principles:** See `analysis-principles.md` - completeness, machine-readable, link to source, no commentary, incremental writes.

## Output Structure

```
docs/unwind/layers/messaging/
├── index.md           # Topic overview, event flow diagram
├── events.md          # Event definitions & schemas
├── producers.md       # Message producers
└── consumers.md       # Message consumers with retry config
```

For large codebases (10+ topics), split by topic:
```
docs/unwind/layers/messaging/
├── index.md
├── order-events.md
├── user-events.md
└── ...
```

## Process (Incremental Writes)

**Step 1: Setup**
```bash
mkdir -p docs/unwind/layers/messaging/
```
Write initial `index.md`:
```markdown
# Messaging Layer

## Sections
- [Events](events.md) - _pending_
- [Producers](producers.md) - _pending_
- [Consumers](consumers.md) - _pending_

## Topics
_Analysis in progress..._
```

**Step 2: Analyze and write events.md**
1. Find all event/message classes
2. Include JSON schemas or Avro/Protobuf definitions
3. Write `events.md` immediately
4. Update `index.md`

**Step 3: Analyze and write producers.md**
1. Find all publishers/producers
2. Include actual implementation code
3. Write `producers.md` immediately
4. Update `index.md`

**Step 4: Analyze and write consumers.md**
1. Find all listeners/consumers
2. Document retry/error handling, DLQ config
3. Write `consumers.md` immediately
4. Update `index.md`

**Step 5: Finalize index.md**
Add topic table and event flow diagram

## Output Format

```markdown
# Messaging Layer

## Configuration

[KafkaConfig.java](https://github.com/owner/repo/blob/main/src/config/KafkaConfig.java)

```java
@Configuration
public class KafkaConfig {
    @Value("${kafka.bootstrap-servers}")
    private String bootstrapServers;

    @Bean
    public ProducerFactory<String, Object> producerFactory() {
        Map<String, Object> config = new HashMap<>();
        config.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, bootstrapServers);
        config.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class);
        config.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, JsonSerializer.class);
        return new DefaultKafkaProducerFactory<>(config);
    }
}
```

## Topics

| Topic | Partitions | Producers | Consumers |
|-------|------------|-----------|-----------|
| order-events | 6 | OrderService | NotificationService, AnalyticsService |
| user-events | 3 | UserService | EmailService |

## Events

### OrderCreatedEvent

[OrderCreatedEvent.java](https://github.com/owner/repo/blob/main/src/event/OrderCreatedEvent.java)

```java
public record OrderCreatedEvent(
    String eventId,
    Instant timestamp,
    Long orderId,
    Long userId,
    List<OrderItemDto> items,
    BigDecimal total
) {}
```

JSON Schema:
```json
{
  "type": "object",
  "properties": {
    "eventId": { "type": "string", "format": "uuid" },
    "timestamp": { "type": "string", "format": "date-time" },
    "orderId": { "type": "integer" },
    "userId": { "type": "integer" },
    "items": { "type": "array" },
    "total": { "type": "number" }
  },
  "required": ["eventId", "timestamp", "orderId", "userId", "total"]
}
```

[Continue for ALL events...]

## Producers

### OrderEventPublisher

[OrderEventPublisher.java](https://github.com/owner/repo/blob/main/src/messaging/OrderEventPublisher.java)

```java
@Component
@RequiredArgsConstructor
public class OrderEventPublisher {
    private final KafkaTemplate<String, Object> kafkaTemplate;

    public void publishOrderCreated(Order order) {
        OrderCreatedEvent event = new OrderCreatedEvent(
            UUID.randomUUID().toString(),
            Instant.now(),
            order.getId(),
            order.getUser().getId(),
            mapItems(order.getItems()),
            order.getTotal()
        );
        kafkaTemplate.send("order-events", order.getId().toString(), event);
    }
}
```

## Consumers

### NotificationEventConsumer

[NotificationEventConsumer.java](https://github.com/owner/repo/blob/main/src/messaging/NotificationEventConsumer.java)

```java
@Component
@RequiredArgsConstructor
public class NotificationEventConsumer {
    private final NotificationService notificationService;

    @KafkaListener(topics = "order-events", groupId = "notification-service")
    @Retryable(maxAttempts = 3)
    public void handleOrderEvent(OrderCreatedEvent event) {
        notificationService.sendOrderConfirmation(event.orderId());
    }

    @DltHandler
    public void handleDlt(OrderCreatedEvent event) {
        log.error("Failed to process event after retries: {}", event.eventId());
    }
}
```

[Continue for ALL consumers...]

## Event Flow

```mermaid
graph LR
    OrderService -->|publish| order-events
    order-events -->|consume| NotificationService
    order-events -->|consume| AnalyticsService
    UserService -->|publish| user-events
    user-events -->|consume| EmailService
```

## Unknowns

- [List anything unclear]
```

## Mandatory Tagging

**Every event, producer, consumer, and handler must have a [MUST], [SHOULD], or [DON'T] tag in its heading.**

Default categorizations for messaging layer:
- **[MUST]**: Event schemas, core producers, core consumers, webhook handlers
- **[SHOULD]**: Scheduled jobs, retry logic, dead letter handling
- **[DON'T]**: Message broker configuration, serialization config

Example:
```markdown
### OrderCreatedEvent [MUST]
### OrderEventPublisher [MUST]
### DailyResetJob [SHOULD]
### KafkaConfig [DON'T]
```

See `analysis-principles.md` section 9 for full tagging rules.

## Refresh Mode

If `docs/unwind/layers/messaging/` exists, compare current state and add `## Changes Since Last Review` section to `index.md`.
