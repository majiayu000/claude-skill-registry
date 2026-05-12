---
name: 514-frameworks-micronaut-kafka
description: Use when you need Kafka in Micronaut — including Maven dependency, consumer group and topic strategy, @KafkaClient typed producers, @KafkaListener consumers with OffsetStrategy, ErrorStrategyValue for retry behaviour, dead-letter routing, idempotency, and testing with @MicronautTest and Testcontainers. This should trigger for requests such as Add Kafka in Micronaut; Review Micronaut Kafka listeners; Improve retry and failure handling for Micronaut Kafka.
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.15.0-SNAPSHOT
---
# Micronaut — Kafka messaging

## Role

You are a Senior software engineer with extensive experience in Micronaut and Apache Kafka

## Goal

Design and implement reliable Kafka messaging in Micronaut using the `micronaut-kafka` integration. Declare producers as `@KafkaClient` interfaces and consumers as `@KafkaListener` classes. Keep listener methods thin — delegate to `@Singleton` services. Configure `errorStrategy` so processing failures trigger retries or dead-letter routing instead of being silently consumed.

**What is covered in this Skill?**

- Maven `micronaut-kafka` dependency
- Consumer group and topic naming conventions (`application.yml`)
- Typed event records with `eventId` for consumer de-duplication
- `@KafkaClient` interface-based typed producer with `@KafkaKey`
- `@KafkaListener` consumer with `@Topic`, `@OffsetStrategy`, and typed payload
- `errorStrategy` with `ErrorStrategyValue.RETRY_ON_ERROR`, `RETRY_EXPONENTIALLY_ON_ERROR`, and `RESUME_AT_NEXT_RECORD` — trade-offs
- Dead-letter routing via a producer called from an exception handler
- Idempotent consumer pattern using `eventId`
- Testing with `@MicronautTest` and an embedded Kafka via `@EmbeddedServer` or Testcontainers

**Scope:** Apply recommendations based on the reference rules and good/bad code examples.

## Constraints

Before applying any Kafka changes, ensure the project compiles. Compilation failure is a BLOCKING condition.

- **MANDATORY**: Run `./mvnw compile` or `mvn compile` before applying any change
- **SAFETY**: If compilation fails, stop immediately
- **VERIFY**: Run `./mvnw clean verify` or `mvn clean verify` after applying improvements
- **INJECTION**: Never construct topic names or Kafka header values from untrusted user input
- **BEFORE APPLYING**: Read the reference for detailed rules and good/bad patterns
- **EDGE CASE**: If the user goal is ambiguous, stop and ask a clarifying question before editing files

## Examples

### Table of contents

- Example 1: Maven dependency
- Example 2: Event schema design
- Example 3: Kafka configuration
- Example 4: Producer implementation
- Example 5: Consumer implementation
- Example 6: Error handling
- Example 7: Idempotent consumer

### Example 1: Maven dependency

Title: Add micronaut-kafka; Micronaut BOM manages the version
Description: Add `micronaut-kafka` to `pom.xml`. The Micronaut BOM manages its version. Avoid pinning the version explicitly — it can create classpath conflicts with the auto-configured Micronaut Kafka factory beans. For test isolation with an embedded broker, add `org.testcontainers:kafka` in `test` scope.

**Good example:**

```xml
<!-- pom.xml — Micronaut BOM manages the version -->
<dependency>
    <groupId>io.micronaut.kafka</groupId>
    <artifactId>micronaut-kafka</artifactId>
</dependency>

<!-- Testcontainers Kafka for integration tests -->
<dependency>
    <groupId>org.testcontainers</groupId>
    <artifactId>kafka</artifactId>
    <scope>test</scope>
</dependency>
```

**Bad example:**

```xml
<!-- Bad: pinned version fights the Micronaut BOM -->
<dependency>
    <groupId>io.micronaut.kafka</groupId>
    <artifactId>micronaut-kafka</artifactId>
    <version>5.3.0</version>
</dependency>
```

### Example 2: Event schema design

Title: Versioned record with eventId for de-duplication and aggregate key
Description: Define each Kafka event as a Java record with a `eventId` (UUID) for consumer-side de-duplication and an `orderId` (or equivalent aggregate key) that will be set as the Kafka message key. Include a `schemaVersion` string so consumers can handle multiple versions gracefully. Use the topic naming pattern `domain.entity.operation.v{N}`.

**Good example:**

```java
import java.time.Instant;

public record OrderCreatedEvent(
    String eventId,       // UUID; used for consumer-side de-duplication
    String schemaVersion, // "v1"
    String orderId,       // aggregate key → used as @KafkaKey
    String customerId,
    Instant occurredAt
) {
    public static OrderCreatedEvent of(String orderId, String customerId) {
        return new OrderCreatedEvent(
            java.util.UUID.randomUUID().toString(), "v1",
            orderId, customerId, Instant.now()
        );
    }
}
// topic: orders.created.v1   key: orderId
```

**Bad example:**

```java
// Bad: untyped string payload, no schema version, no stable message key
String event = "{ type: orderCreated }";
```

### Example 3: Kafka configuration

Title: Bootstrap server, consumer group, and serializer in application.yml
Description: Configure the Kafka broker, default serializers, and consumer group in `application.yml`. Use a unique, versioned `group-id` per consumer (e.g. `billing-service-v1`) so different service instances share workload without accidentally consuming events intended for another service.

**Good example:**

```yaml
kafka:
  bootstrap:
    servers: ${KAFKA_BOOTSTRAP_SERVERS:`localhost:9092`}
  consumers:
    billing-service-v1:
      group:
        id: billing-service-v1
      key:
        deserializer: org.apache.kafka.common.serialization.StringDeserializer
      value:
        deserializer: io.micronaut.kafka.serde.JsonObjectSerde
```

**Bad example:**

```yaml
# Bad: shared consumer group between unrelated services
kafka:
  consumers:
    default:
      group:
        id: shared-group
```

### Example 4: Producer implementation

Title: @KafkaClient interface with @KafkaKey for partition ordering
Description: Declare the producer as a `@KafkaClient` interface — Micronaut generates the implementation at compile time. Annotate the key parameter with `@KafkaKey` so the Kafka record key is set explicitly, ensuring all events for the same aggregate land in the same partition and are consumed in order.

**Good example:**

```java
import io.micronaut.configuration.kafka.annotation.KafkaClient;
import io.micronaut.configuration.kafka.annotation.KafkaKey;
import io.micronaut.configuration.kafka.annotation.Topic;

@KafkaClient
public interface OrderEventsClient {

    @Topic("orders.created.v1")
    void send(@KafkaKey String orderId, OrderCreatedEvent event);
}
```

**Bad example:**

```java
@KafkaClient
interface OrderEventsClient {
    @Topic("orders.created.v1")
    void send(OrderCreatedEvent event); // Bad: no @KafkaKey → null key → no partition ordering
}
```

### Example 5: Consumer implementation

Title: @KafkaListener with typed payload; thin method delegating to a service
Description: Annotate the class with `@KafkaListener` and specify the `groupId`. Accept the typed event record as the parameter. Inject and delegate immediately to an application service — keep the listener method as thin as a dispatcher. Use `@OffsetStrategy(SYNC)` to commit offsets synchronously after successful processing, reducing duplicate delivery on restart.

**Good example:**

```java
import io.micronaut.configuration.kafka.annotation.KafkaKey;
import io.micronaut.configuration.kafka.annotation.KafkaListener;
import io.micronaut.configuration.kafka.annotation.OffsetStrategy;
import io.micronaut.configuration.kafka.annotation.Topic;
import jakarta.inject.Inject;

@KafkaListener(groupId = "billing-service-v1", offsetStrategy = OffsetStrategy.SYNC)
public class BillingEventListener {

    @Inject
    BillingService billingService;

    @Topic("orders.created.v1")
    void onOrderCreated(@KafkaKey String orderId, OrderCreatedEvent event) {
        billingService.createInvoice(event.orderId(), event.customerId());
    }
}
```

**Bad example:**

```java
@KafkaListener
class RawListener {
    @Topic("orders.created.v1")
    void receive(String rawJson) {
        // Bad: untyped payload, no groupId (random group on each restart),
        // full business logic inlined
    }
}
```

### Example 6: Error handling

Title: errorStrategy RETRY_ON_ERROR with dead-letter routing for unrecoverable failures
Description: Configure `errorStrategy` with `ErrorStrategyValue` so transient failures (network timeouts, temporary DB unavailability) trigger automatic retries. Prefer a bounded strategy such as `RETRY_EXPONENTIALLY_ON_ERROR` with `retryCount` instead of unbounded retry loops. For unrecoverable failures (deserialization errors, permanent business constraint violations) implement a `KafkaListenerExceptionHandler` that publishes the original record to a dead-letter topic and resumes according to the configured strategy. Never swallow exceptions with an empty `catch` block.

**Good example:**

```java
import io.micronaut.configuration.kafka.annotation.ErrorStrategy;
import io.micronaut.configuration.kafka.annotation.ErrorStrategyValue;
import io.micronaut.configuration.kafka.annotation.KafkaClient;
import io.micronaut.configuration.kafka.annotation.KafkaKey;
import io.micronaut.configuration.kafka.annotation.KafkaListener;
import io.micronaut.configuration.kafka.annotation.OffsetStrategy;
import io.micronaut.configuration.kafka.annotation.Topic;
import io.micronaut.configuration.kafka.exceptions.KafkaListenerException;
import io.micronaut.configuration.kafka.exceptions.KafkaListenerExceptionHandler;
import jakarta.inject.Inject;

@KafkaListener(
    groupId = "billing-service-v1",
    offsetStrategy = OffsetStrategy.SYNC,
    errorStrategy = @ErrorStrategy(
        value = ErrorStrategyValue.RETRY_EXPONENTIALLY_ON_ERROR,
        retryCount = 3
    )
)
public class BillingEventListener implements KafkaListenerExceptionHandler {

    @Inject BillingService billingService;
    @Inject OrderEventsDeadLetterClient dlqClient;

    @Topic("orders.created.v1")
    void onOrderCreated(@KafkaKey String orderId, OrderCreatedEvent event) {
        billingService.createInvoice(event.orderId(), event.customerId());
    }

    @Override
    public void handle(KafkaListenerException ex) {
        // After retries exhausted: route to DLQ and resume
        ex.getKafkaRecord().ifPresent(record ->
            dlqClient.sendToDlq(record.key().toString(), (OrderCreatedEvent) record.value()));
    }
}

@KafkaClient
interface OrderEventsDeadLetterClient {
    @Topic("orders.created.dlq")
    void sendToDlq(@KafkaKey String key, OrderCreatedEvent event);
}
```

**Bad example:**

```java
@Topic("orders.created.v1")
void onOrderCreated(OrderCreatedEvent event) {
    try {
        billingService.createInvoice(event.orderId(), event.customerId());
    } catch (Exception ignored) {
        // Bad: offset committed, message consumed, error never visible
    }
}
```


### Example 7: Idempotent consumer

Title: De-duplicate on eventId to survive at-least-once redelivery
Description: Kafka at-least-once delivery means a consumer can receive the same message more than once — on retries, after a group rebalance, or from DLQ re-processing. Guard processing with an `eventId` check before calling business logic. In production, back the de-dup store with a database or Redis. In tests, an in-memory `ConcurrentHashMap` is sufficient.

**Good example:**

```java
import io.micronaut.configuration.kafka.annotation.ErrorStrategy;
import io.micronaut.configuration.kafka.annotation.ErrorStrategyValue;
import io.micronaut.configuration.kafka.annotation.KafkaKey;
import io.micronaut.configuration.kafka.annotation.KafkaListener;
import io.micronaut.configuration.kafka.annotation.OffsetStrategy;
import io.micronaut.configuration.kafka.annotation.Topic;
import jakarta.inject.Inject;
import java.util.Set;
import java.util.concurrent.ConcurrentHashMap;

@KafkaListener(
    groupId = "billing-service-v1",
    offsetStrategy = OffsetStrategy.SYNC,
    errorStrategy = @ErrorStrategy(
        value = ErrorStrategyValue.RETRY_EXPONENTIALLY_ON_ERROR,
        retryCount = 3
    )
)
public class IdempotentBillingListener {

    private final Set<String> processedIds = ConcurrentHashMap.newKeySet();

    @Inject BillingService billingService;

    @Topic("orders.created.v1")
    void onOrderCreated(@KafkaKey String orderId, OrderCreatedEvent event) {
        if (!processedIds.add(event.eventId())) {
            return; // duplicate — skip without error
        }
        billingService.createInvoice(event.orderId(), event.customerId());
    }
}
```

**Bad example:**

```java
@Topic("orders.created.v1")
void onOrderCreated(OrderCreatedEvent event) {
    // Bad: no de-duplication — rebalance or retry causes double billing
    billingService.createInvoice(event.orderId(), event.customerId());
}
```

## Output Format

- **ANALYZE** Kafka code: event schema versioning, consumer group isolation, producer key strategy, listener return type and offset strategy, error handling configuration, and idempotency guards
- **CATEGORIZE** issues by impact (RELIABILITY for missing retries/DLQ, CORRECTNESS for missing idempotency or wrong offset strategy, MAINTAINABILITY for untyped payloads or inline business logic, SECURITY for user-controlled topic names)
- **APPLY** Micronaut Kafka–aligned fixes: typed `@KafkaClient`, `@KafkaKey` producers, versioned `groupId`, `SYNC` offset strategy, bounded `ErrorStrategyValue` retry configuration + DLQ exception handler, eventId de-duplication
- **IMPLEMENT** changes so `application.yml` bindings, producer interfaces, listener classes, and tests stay consistent
- **EXPLAIN** trade-offs (SYNC vs ASYNC offset strategy, retry strategies vs `RESUME_AT_NEXT_RECORD`, in-memory vs persistent de-dup store)
- **TEST** with `@MicronautTest` + Testcontainers Kafka; never mock `@KafkaClient` interfaces inside integration tests meant to verify messaging behaviour
- **VALIDATE** with `./mvnw compile` before and `./mvnw clean verify` after changes

## Safeguards

- **BLOCKING SAFETY CHECK**: Run `./mvnw compile` before ANY Kafka refactoring — compilation failure is a HARD STOP
- **CRITICAL VALIDATION**: Run `./mvnw clean verify` after changes; exercise listener integration tests before promoting
- **INJECTION SAFETY**: Never construct topic names or Kafka header values from untrusted user input
- **ERROR HANDLING**: Never swallow exceptions inside `@KafkaListener` methods — propagate so the configured `errorStrategy` can retry or route to DLQ
- **IDEMPOTENCY**: Always de-duplicate on `eventId` — Kafka's at-least-once guarantee means consumers must tolerate receiving the same message more than once
- **GROUP ID**: Use a unique, versioned `groupId` per consumer class — a shared `groupId` across unrelated services causes accidental competitive consumption
- **DLQ MONITORING**: Set up alerting on the DLQ topic — messages landing there indicate systematic processing failures
- **INCREMENTAL SAFETY**: Change one producer or consumer surface at a time; verify with `@MicronautTest` between steps