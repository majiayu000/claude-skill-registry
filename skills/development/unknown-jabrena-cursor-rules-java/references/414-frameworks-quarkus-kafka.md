---
name: 414-frameworks-quarkus-kafka
description: Use when you need Kafka in Quarkus with SmallRye Reactive Messaging — including Maven extension, channel/topic design, typed @Channel Emitter producers, @Incoming consumers with Uni, failure strategies (dead-letter-queue, retry), idempotency, and Dev Services testing. This should trigger for requests such as Add Kafka in Quarkus; Review Reactive Messaging consumers; Improve failure handling for Quarkus Kafka.
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.15.0-SNAPSHOT
---
# Quarkus — Kafka messaging

## Role

You are a Senior software engineer with extensive experience in Quarkus and Apache Kafka

## Goal

Design and implement reliable Kafka messaging in Quarkus using SmallRye Reactive Messaging. Keep channel names and topic names decoupled via configuration. Use typed event records. Delegate business logic to CDI services from thin `@Incoming` methods. Configure `failure-strategy=dead-letter-queue` so unrecoverable messages are routed rather than silently acknowledged.

**What is covered in this Skill?**

- Maven `quarkus-messaging-kafka` extension dependency
- Channel and topic naming conventions and configuration
- Typed event records with `eventId` for de-duplication
- `@Channel` / `Emitter` typed producer
- `@Incoming` consumer with `Uni<Void>` return type
- Manual `Message` acknowledgement for explicit ack/nack control
- `failure-strategy`: `dead-letter-queue`, `fail`, and `ignore`; retry is configured separately with connector retry properties
- Idempotent consumer pattern using `eventId`
- Dev Services for Kafka (zero-config in dev and test)
- Integration testing with `@QuarkusTest` and `@TestProfile`

**Scope:** Apply recommendations based on the reference rules and good/bad code examples.

## Constraints

Before applying any Kafka changes, ensure the project compiles. Compilation failure is a BLOCKING condition.

- **MANDATORY**: Run `./mvnw compile` or `mvn compile` before applying any change
- **SAFETY**: If compilation fails, stop immediately
- **VERIFY**: Run `./mvnw clean verify` or `mvn clean verify` after applying improvements
- **INJECTION**: Never construct topic names or header values from untrusted user input
- **BEFORE APPLYING**: Read the reference for detailed rules and good/bad patterns
- **EDGE CASE**: If the user goal is ambiguous, stop and ask a clarifying question before editing files

## Examples

### Table of contents

- Example 1: Maven extension
- Example 2: Event schema design
- Example 3: Channel and topic configuration
- Example 4: Producer implementation
- Example 5: Consumer implementation
- Example 6: Error handling and dead-letter queue
- Example 7: Idempotent consumer

### Example 1: Maven extension

Title: Add quarkus-messaging-kafka; let Quarkus BOM manage the version
Description: Add `quarkus-messaging-kafka` to your `pom.xml`. The Quarkus BOM manages the version — do not pin it. Quarkus Dev Services automatically starts a Kafka broker in dev and test modes when this extension is on the classpath and no `kafka.bootstrap.servers` is configured, so no manual setup is needed for local development.

**Good example:**

```xml
<!-- pom.xml — Quarkus BOM manages the version -->
<dependency>
    <groupId>io.quarkus</groupId>
    <artifactId>quarkus-messaging-kafka</artifactId>
</dependency>
```

**Bad example:**

```xml
<!-- Bad: pinned version fights the Quarkus BOM -->
<dependency>
    <groupId>io.quarkus</groupId>
    <artifactId>quarkus-messaging-kafka</artifactId>
    <version>3.8.1</version>
</dependency>
```

### Example 2: Event schema design

Title: Versioned immutable record with eventId and aggregate key
Description: Define each Kafka event as a Java record with a `eventId` (UUID) for de-duplication, a `schemaVersion` for forward compatibility, and the aggregate's natural key (e.g. `orderId`). The aggregate key should be used as the Kafka message key to keep partition ordering for the same aggregate. Topic names follow `domain.entity.operation.v{N}`.

**Good example:**

```java
import java.time.Instant;

public record OrderCreatedEvent(
    String eventId,       // UUID; used for consumer-side de-duplication
    String schemaVersion, // "v1"
    String orderId,       // aggregate key → used as Kafka message key
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
// Bad: untyped map, no schema version, no aggregate key
Map<String, Object> event = Map.of("type", "order", "data", "...");
```

### Example 3: Channel and topic configuration

Title: Map logical channel names to Kafka topics via application.properties
Description: Decouple the channel name used in code from the physical Kafka topic name via configuration. This allows topics to be renamed across environments without code changes. Use stable, versioned topic names (`domain.entity.operation.v{N}`). Configure `value-serializer` / `value-deserializer` explicitly so there are no implicit class-name-based surprises.

**Good example:**

```properties
# application.properties
mp.messaging.outgoing.orders-out.connector=smallrye-kafka
mp.messaging.outgoing.orders-out.topic=orders.created.v1
mp.messaging.outgoing.orders-out.value.serializer=io.quarkus.kafka.client.serialization.ObjectMapperSerializer

mp.messaging.incoming.orders-in.connector=smallrye-kafka
mp.messaging.incoming.orders-in.topic=orders.created.v1
mp.messaging.incoming.orders-in.group.id=billing-service-v1
mp.messaging.incoming.orders-in.value.deserializer=com.example.kafka.OrderCreatedEventDeserializer
```

**Bad example:**

```java
// Bad: hardcoded topic string inside a Java annotation — cannot be overridden per environment
@Incoming("orders.created.v1")
void onMessage(OrderCreatedEvent event) { }
```

### Example 4: Producer implementation

Title: @Channel Emitter with keyed Message for partition ordering
Description: Inject `@Channel("orders-out") Emitter&lt;OrderCreatedEvent&gt;` into the CDI bean that needs to publish. Wrap the payload in a `Message` with an `OutgoingKafkaRecordMetadata` to set the partition key so all events for the same aggregate go to the same partition.

**Good example:**

```java
import io.smallrye.reactive.messaging.kafka.api.OutgoingKafkaRecordMetadata;
import jakarta.enterprise.context.ApplicationScoped;
import jakarta.inject.Inject;
import org.eclipse.microprofile.reactive.messaging.Channel;
import org.eclipse.microprofile.reactive.messaging.Emitter;
import org.eclipse.microprofile.reactive.messaging.Message;

@ApplicationScoped
public class OrderEventPublisher {

    @Inject
    @Channel("orders-out")
    Emitter<OrderCreatedEvent> emitter;

    public void publish(OrderCreatedEvent event) {
        emitter.send(
            Message.of(event)
                .addMetadata(OutgoingKafkaRecordMetadata.<String>builder()
                    .withKey(event.orderId())
                    .build())
        );
    }
}
```

**Bad example:**

```java
@ApplicationScoped
class OrderEventPublisher {
    @Inject @Channel("orders-out")
    Emitter<String> emitter; // Bad: untyped String emitter; no message key set

    void publish(OrderCreatedEvent event) {
        emitter.send(event.toString()); // loses type safety and partition ordering
    }
}
```

### Example 5: Consumer implementation

Title: @Incoming with Uni return and thin handler delegating to a service
Description: The `@Incoming` method should be thin: receive the typed event, delegate immediately to an `@ApplicationScoped` service, and return `Uni&lt;Void&gt;` when the processing path is asynchronous. Synchronous `void` methods can still propagate thrown exceptions, but a `Uni`/`CompletionStage` is the safer contract when the service work completes later.

**Good example:**

```java
import io.smallrye.mutiny.Uni;
import jakarta.enterprise.context.ApplicationScoped;
import jakarta.inject.Inject;
import org.eclipse.microprofile.reactive.messaging.Incoming;

@ApplicationScoped
public class BillingEventConsumer {

    @Inject
    BillingService billingService;

    @Incoming("orders-in")
    public Uni<Void> onOrderCreated(OrderCreatedEvent event) {
        return billingService.createInvoice(event.orderId(), event.customerId());
    }
}
```

**Bad example:**

```java
// Bad: asynchronous work is hidden behind a void method;
// business logic inline instead of delegating to a service
@Incoming("orders-in")
void onOrderCreated(String rawJson) {
    // 40 lines of parsing + DB calls + HTTP calls
}
```

### Example 6: Error handling and dead-letter queue

Title: failure-strategy=dead-letter-queue with nack for unrecoverable messages
Description: Configure `failure-strategy=dead-letter-queue` so failed messages are routed to a dedicated DLQ topic instead of stopping the channel or being silently ignored. For transient failures (network, timeout), enable the connector retry options (`retry=true`, bounded attempts, bounded wait) alongside the failure strategy. For deterministic failures (deserialization errors, schema mismatch), use explicit `message.nack(ex)` to route immediately to the DLQ.

**Good example:**

```properties
# application.properties
mp.messaging.incoming.orders-in.failure-strategy=dead-letter-queue
mp.messaging.incoming.orders-in.dead-letter-queue.topic=orders.created.dlq
mp.messaging.incoming.orders-in.retry=true
mp.messaging.incoming.orders-in.retry-attempts=3
mp.messaging.incoming.orders-in.retry-max-wait=10S
mp.messaging.incoming.orders-in.commit-strategy=throttled
```

**Bad example:**

```java
@Incoming("orders-in")
public CompletionStage<Void> onOrderCreated(Message<OrderCreatedEvent> message) {
    try {
        billingService.createInvoice(message.getPayload().orderId(), message.getPayload().customerId());
        return message.ack();
    } catch (Exception e) {
        return message.ack(); // Bad: ack on failure — record consumed and lost silently
    }
}
```

### Example 7: Idempotent consumer

Title: De-duplicate on eventId to survive at-least-once redelivery
Description: Kafka guarantees at-least-once delivery, so consumers can receive duplicate messages on broker retries, consumer group rebalances, or DLQ re-processing. Guard each consumer method with an `eventId` check against a de-duplication store. In production, back the store with a database or Redis; in tests, an in-memory `ConcurrentHashMap` is sufficient.

**Good example:**

```java
import io.smallrye.mutiny.Uni;
import jakarta.enterprise.context.ApplicationScoped;
import jakarta.inject.Inject;
import org.eclipse.microprofile.reactive.messaging.Incoming;
import java.util.Set;
import java.util.concurrent.ConcurrentHashMap;

@ApplicationScoped
public class BillingEventConsumer {

    private final Set<String> processedIds = ConcurrentHashMap.newKeySet();

    @Inject BillingService billingService;

    @Incoming("orders-in")
    public Uni<Void> onOrderCreated(OrderCreatedEvent event) {
        if (!processedIds.add(event.eventId())) {
            return Uni.createFrom().voidItem(); // duplicate — skip
        }
        return billingService.createInvoice(event.orderId(), event.customerId());
    }
}
```

**Bad example:**

```java
@Incoming("orders-in")
public Uni<Void> onOrderCreated(OrderCreatedEvent event) {
    // Bad: no idempotency guard — rebalance or DLQ re-play doubles billing
    return billingService.createInvoice(event.orderId(), event.customerId());
}
```

## Output Format

- **ANALYZE** Kafka code: event schema versioning, channel/topic binding, producer key strategy, consumer return type, failure strategy configuration, and idempotency guards
- **CATEGORIZE** issues by impact (RELIABILITY for missing DLQ or failure strategy, CORRECTNESS for missing idempotency, MAINTAINABILITY for untyped emitters or inline business logic, SECURITY for user-controlled topic names)
- **APPLY** SmallRye Reactive Messaging–aligned fixes: type the emitters and channels, key messages on the aggregate id, configure failure-strategy, add eventId de-duplication
- **IMPLEMENT** changes so channel config, serializers, consumer methods, and tests stay consistent
- **EXPLAIN** trade-offs (void vs Uni return, dead-letter-queue vs retry vs ignore, in-process Dev Services vs Testcontainers)
- **TEST** with `@QuarkusTest` and Dev Services; use Testcontainers Kafka for full-stack acceptance tests
- **VALIDATE** with `./mvnw compile` before and `./mvnw clean verify` after changes

## Safeguards

- **BLOCKING SAFETY CHECK**: Run `./mvnw compile` before ANY Kafka refactoring — compilation failure is a HARD STOP
- **CRITICAL VALIDATION**: Run `./mvnw clean verify` after changes; exercise consumer integration tests before promoting
- **INJECTION SAFETY**: Never build topic names or Kafka header values from untrusted user input
- **ERROR HANDLING**: Propagate failures from `@Incoming` methods; use `Uni`/`CompletionStage` for asynchronous processing so failures happen inside the messaging contract
- **IDEMPOTENCY**: Always de-duplicate on `eventId` — at-least-once delivery means consumers must tolerate receiving the same message more than once
- **DLQ MONITORING**: Set up alerting on the DLQ topic — messages landing there indicate systematic processing failures
- **CDI SELF-INVOCATION**: Never call an `@Incoming`-annotated method directly via `this` — always inject through the CDI proxy
- **INCREMENTAL SAFETY**: Change one producer or consumer surface at a time; verify with `@QuarkusTest` between steps