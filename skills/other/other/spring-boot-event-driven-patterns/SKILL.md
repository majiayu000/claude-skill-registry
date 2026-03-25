---
name: spring-boot-event-driven-patterns
description: Provides Event-Driven Architecture (EDA) patterns for Spring Boot — creates domain events, configures ApplicationEvent and @TransactionalEventListener, sets up Kafka producers and consumers, and implements the transactional outbox pattern for reliable distributed messaging. Use when implementing event-driven systems in Spring Boot, setting up async messaging with Kafka, publishing domain events from DDD aggregates, or needing reliable event publishing with the outbox pattern.
allowed-tools: Read, Write, Edit, Bash
---

# Spring Boot Event-Driven Patterns

## Overview

Implement Event-Driven Architecture (EDA) patterns in Spring Boot 3.x using domain events, ApplicationEventPublisher, `@TransactionalEventListener`, and distributed messaging with Kafka and Spring Cloud Stream.

## When to Use

- Implementing event-driven microservices with Kafka messaging
- Publishing domain events from aggregate roots in DDD architectures
- Setting up transactional event listeners that fire after database commits
- Adding async messaging with producers and consumers via Spring Kafka
- Ensuring reliable event delivery using the transactional outbox pattern
- Replacing synchronous calls with event-based communication between services

## Quick Reference

| Concept | Description |
|---------|-------------|
| **Domain Events** | Immutable events extending `DomainEvent` base class with eventId, occurredAt, correlationId |
| **Event Publishing** | `ApplicationEventPublisher.publishEvent()` for local, `KafkaTemplate` for distributed |
| **Event Listening** | `@TransactionalEventListener(phase = AFTER_COMMIT)` for reliable handling |
| **Kafka** | `@KafkaListener(topics = "...")` for distributed event consumption |
| **Spring Cloud Stream** | Functional programming model with `Consumer` beans |
| **Outbox Pattern** | Atomic event storage with business data, scheduled publisher |

## Examples

### Monolithic to Event-Driven Refactoring

**Before (Anti-Pattern):**
```java
@Transactional
public Order processOrder(OrderRequest request) {
    Order order = orderRepository.save(request);
    inventoryService.reserve(order.getItems()); // Blocking
    paymentService.charge(order.getPayment()); // Blocking
    emailService.sendConfirmation(order); // Blocking
    return order;
}
```

**After (Event-Driven):**
```java
@Transactional
public Order processOrder(OrderRequest request) {
    Order order = Order.create(request);
    orderRepository.save(order);

    // Publish event after transaction commits
    eventPublisher.publishEvent(new OrderCreatedEvent(order.getId(), order.getItems()));

    return order;
}

@Component
public class OrderEventHandler {
    @TransactionalEventListener(phase = TransactionPhase.AFTER_COMMIT)
    public void handleOrderCreated(OrderCreatedEvent event) {
        // Execute asynchronously after the order is saved
        inventoryService.reserve(event.getItems());
        paymentService.charge(event.getPayment());
    }
}
```

See [examples.md](references/examples.md) for complete working examples.

## Instructions

### 1. Design Domain Events

Create immutable event classes extending a base `DomainEvent` class:

```java
public abstract class DomainEvent {
    private final UUID eventId;
    private final LocalDateTime occurredAt;
    private final UUID correlationId;
}

public class ProductCreatedEvent extends DomainEvent {
    private final ProductId productId;
    private final String name;
    private final BigDecimal price;
}
```

See [domain-events-design.md](references/domain-events-design.md) for patterns.

### 2. Publish Events from Aggregates

Add domain events to aggregate roots, publish via `ApplicationEventPublisher`:

```java
@Service
@Transactional
public class ProductService {
    public Product createProduct(CreateProductRequest request) {
        Product product = Product.create(request.getName(), request.getPrice(), request.getStock());
        repository.save(product);

        product.getDomainEvents().forEach(eventPublisher::publishEvent);
        product.clearDomainEvents();

        return product;
    }
}
```

See [aggregate-root-patterns.md](references/aggregate-root-patterns.md) for DDD patterns.

### 3. Handle Events Transactionally

Use `@TransactionalEventListener` for reliable event handling:

```java
@Component
public class ProductEventHandler {
    @TransactionalEventListener(phase = TransactionPhase.AFTER_COMMIT)
    public void onProductCreated(ProductCreatedEvent event) {
        notificationService.sendProductCreatedNotification(event.getName());
    }
}
```

**Validate:** Confirm the event handler fires only after the transaction commits by checking that the database state is committed before the handler executes.

See [event-handling.md](references/event-handling.md) for handling patterns.

### 4. Configure Kafka Infrastructure

Configure KafkaTemplate for publishing, `@KafkaListener` for consuming:

```yaml
spring:
  kafka:
    bootstrap-servers: localhost:9092
    producer:
      value-serializer: org.springframework.kafka.support.serializer.JsonSerializer
```

**Validate:** Send a test event via `KafkaTemplate` and confirm it appears in the consumer logs before proceeding to production patterns.

See [dependency-setup.md](references/dependency-setup.md) and [configuration.md](references/configuration.md).

### 5. Implement Outbox Pattern

Create `OutboxEvent` entity for atomic event storage:

```java
@Entity
public class OutboxEvent {
    private UUID id;
    private String aggregateId;
    private String eventType;
    private String payload;
    private LocalDateTime publishedAt;
}
```

**Validate:** Confirm the scheduled processor picks up pending events by checking the `publishedAt` timestamp is set after the scheduled run.

Scheduled processor publishes pending events. See [outbox-pattern.md](references/outbox-pattern.md).

### 6. Handle Failure Scenarios

Implement retry logic, dead-letter queues, idempotent handlers:

```java
@RetryableTopic(attempts = "3")
@KafkaListener(topics = "product-events")
public void handleProductEvent(ProductCreatedEventDto event) {
    orderService.onProductCreated(event);
}
```

**Validate:** Confirm messages reach the dead-letter topic after exhausting retries before moving to observability.

### 7. Add Observability

Enable Spring Cloud Sleuth for distributed tracing, monitor metrics.

## Best Practices

- **Use past tense naming**: `ProductCreated` (not `CreateProduct`)
- **Keep events immutable**: All fields should be final
- **Include correlation IDs**: For tracing events across services
- **Use AFTER_COMMIT phase**: Ensures events are published after successful database transaction
- **Implement idempotent handlers**: Handle duplicate events gracefully
- **Add retry mechanisms**: For failed event processing with exponential backoff
- **Implement dead-letter queues**: For events that fail processing after retries
- **Log all failures**: Include sufficient context for debugging
- **Make handlers order-independent**: Event ordering is not guaranteed in distributed systems
- **Batch event processing**: When handling high volumes
- **Monitor event latencies**: Set up alerts for slow processing

## References

- **[dependency-setup.md](references/dependency-setup.md)** — Maven/Gradle dependencies
- **[configuration.md](references/configuration.md)** — Kafka and Spring Cloud Stream configuration
- **[domain-events-design.md](references/domain-events-design.md)** — Domain event design patterns
- **[aggregate-root-patterns.md](references/aggregate-root-patterns.md)** — Aggregate root with event publishing
- **[event-publishing.md](references/event-publishing.md)** — Local and distributed event publishing
- **[event-handling.md](references/event-handling.md)** — Event handling and consumption patterns
- **[outbox-pattern.md](references/outbox-pattern.md)** — Transactional outbox pattern for reliability
- **[testing-strategies.md](references/testing-strategies.md)** — Unit and integration testing approaches
- **[examples.md](references/examples.md)** — Complete working examples
- **[event-driven-patterns-reference.md](references/event-driven-patterns-reference.md)** — Detailed reference documentation

## Constraints and Warnings

- Events published with `@TransactionalEventListener` only fire after transaction commit
- Avoid publishing large objects in events (memory pressure, serialization issues)
- Be cautious with async event handlers (separate threads, concurrency issues)
- Kafka consumers must handle duplicate messages (implement idempotent processing)
- Event ordering is not guaranteed in distributed systems (design handlers to be order-independent)
- Never perform blocking operations in event listeners on the main transaction thread
- Monitor for event processing backlogs (indicate system capacity issues)

## Related Skills

- `spring-boot-security-jwt` — JWT authentication for secure event publishing
- `spring-boot-test-patterns` — Testing event-driven applications
- `aws-sdk-java-v2-lambda` — Event-driven processing with AWS Lambda
- `langchain4j-tool-function-calling-patterns` — AI-driven event processing
