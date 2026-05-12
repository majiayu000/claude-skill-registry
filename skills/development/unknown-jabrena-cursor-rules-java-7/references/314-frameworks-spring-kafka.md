---
name: 314-frameworks-spring-kafka
description: Use when you need Kafka with Spring Boot (`spring-kafka`) — including Maven dependencies, topic and event schema design, typed KafkaTemplate producers, @KafkaListener consumers, retries with DefaultErrorHandler, dead-letter topics, idempotent consumers, and integration testing with @EmbeddedKafka. This should trigger for requests such as Add Kafka in Spring Boot; Review Spring Kafka consumers; Improve retries and DLT in Spring Kafka.
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.15.0-SNAPSHOT
---
# Spring Boot — Kafka messaging

## Role

You are a Senior software engineer with extensive experience in Spring Boot and Apache Kafka

## Goal

Design and implement reliable Kafka messaging in Spring Boot using `spring-kafka`. Prefer typed event records, keyed producers for ordered processing, and declarative error handling with dead-letter topics over silent exception swallowing. Keep listeners thin — delegate business logic to services. Guard consumers against poison messages and replay with idempotency on the eventId.

**What is covered in this Skill?**

- Maven `spring-kafka` dependency aligned with the Spring Boot BOM
- Versioned event schemas as Java records with explicit `eventId`, `schemaVersion`, and aggregate key
- Topic naming conventions (`domain.entity.operation.v{N}`)
- `KafkaTemplate<K, V>` typed producer with explicit key strategy
- `@KafkaListener` consumer with explicit `groupId`, `topics`, and typed payload
- `ConcurrentKafkaListenerContainerFactory` for concurrency and batch vs. single-record modes
- `DefaultErrorHandler` with `FixedBackOff` / `ExponentialBackOff` and `DeadLetterPublishingRecoverer`
- Idempotent consumer pattern using `eventId` de-duplication store
- Kafka transactions for exactly-once producer semantics
- Testing with `@EmbeddedKafka` and `EmbeddedKafkaBroker`

**Scope:** Apply recommendations based on the reference rules and good/bad code examples.

## Constraints

Before applying any Kafka changes, ensure the project compiles. Compilation failure is a BLOCKING condition.

- **MANDATORY**: Run `./mvnw compile` or `mvn compile` before applying any change
- **SAFETY**: If compilation fails, stop immediately
- **VERIFY**: Run `./mvnw clean verify` or `mvn clean verify` after applying improvements
- **INJECTION**: Never build topic names or Kafka header values from untrusted user input
- **BEFORE APPLYING**: Read the reference for detailed rules and good/bad patterns
- **EDGE CASE**: If the user goal is ambiguous, stop and ask a clarifying question before editing files
- **EDGE CASE**: If required context, files, or tools are missing, report the blocker explicitly

## Examples

### Table of contents

- Example 1: Maven dependency
- Example 2: Event schema design
- Example 3: Producer implementation
- Example 4: Consumer implementation
- Example 5: Error handling and dead-letter topic
- Example 6: Idempotent consumer
- Example 7: Integration testing

### Example 1: Maven dependency

Title: Add spring-kafka via the Spring Boot BOM; never pin the version manually
Description: Spring Boot manages the `spring-kafka` version via its BOM. Declaring an explicit version pins the library and can cause incompatibility with the auto-configured `KafkaAutoConfiguration`. Use the starter form when using Spring Boot; add the raw `spring-kafka` artifact for library modules that do not depend on Spring Boot auto-configuration.

**Good example:**

```xml
<!-- pom.xml — Spring Boot manages the version via its BOM -->
<dependency>
    <groupId>org.springframework.kafka</groupId>
    <artifactId>spring-kafka</artifactId>
</dependency>
```

**Bad example:**

```xml
<!-- Bad: explicit version fights the BOM and can cause classpath conflicts -->
<dependency>
    <groupId>org.springframework.kafka</groupId>
    <artifactId>spring-kafka</artifactId>
    <version>3.1.0</version>
</dependency>
```

### Example 2: Event schema design

Title: Versioned immutable records with eventId and aggregate key
Description: Define each Kafka event as a Java record. Include a unique `eventId` (UUID) for consumer de-duplication, a `schemaVersion` string for forward compatibility, and the aggregate's natural key (e.g. `orderId`). Use the aggregate key as the Kafka message key so all events for the same aggregate land in the same partition, preserving ordering. Topic names follow the pattern `domain.entity.operation.v{N}` to allow parallel consumers on older and newer versions.

**Good example:**

```java
import java.time.Instant;

// Immutable event schema — one record per event type
public record OrderCreatedEvent(
    String eventId,       // UUID; used for consumer-side de-duplication
    String schemaVersion, // "v1"; bump when non-backward-compatible fields change
    String orderId,       // aggregate key → use as Kafka message key
    String customerId,
    Instant occurredAt
) {
    public static OrderCreatedEvent of(String orderId, String customerId) {
        return new OrderCreatedEvent(
            java.util.UUID.randomUUID().toString(),
            "v1",
            orderId,
            customerId,
            Instant.now()
        );
    }
}
// topic: orders.created.v1  key: orderId
```

**Bad example:**

```java
// Bad: generic map payload — no schema, no version, no stable key
Map<String, Object> event = Map.of(
    "type", "orderCreated",
    "data", "..."
);
// topic: events   key: null (random partition assignment)
```

### Example 3: Producer implementation

Title: Typed KafkaTemplate with explicit key; handle send failure
Description: Inject a typed `KafkaTemplate&lt;String, OrderCreatedEvent&gt;` so the compiler enforces the key/value contract. Always pass the aggregate's key as the Kafka record key. Return the `CompletableFuture` to the caller (or await it at a command boundary) so broker-side send failures are observable. Do not throw from a `whenComplete` callback and assume the caller will see it.

**Good example:**

```java
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.kafka.support.SendResult;
import org.springframework.stereotype.Service;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.CompletionException;

@Service
class OrderEventPublisher {

    private static final String TOPIC = "orders.created.v1";

    private final KafkaTemplate<String, OrderCreatedEvent> template;

    OrderEventPublisher(KafkaTemplate<String, OrderCreatedEvent> template) {
        this.template = template;
    }

    CompletableFuture<SendResult<String, OrderCreatedEvent>> publish(OrderCreatedEvent event) {
        return template.send(TOPIC, event.orderId(), event)
            .exceptionally(ex -> {
                throw new CompletionException("Kafka send failed for order: " + event.orderId(), ex);
            });
    }
}
```

**Bad example:**

```java
// Bad: raw KafkaTemplate<String, String> loses type safety;
// null key loses partition ordering; ignored CompletableFuture drops send errors
@Service
class OrderEventPublisher {
    @Autowired
    KafkaTemplate<String, String> template;

    void publish(OrderCreatedEvent event) {
        template.send("events", null, event.toString()); // no key, serialized via toString()
        // CompletableFuture discarded — broker errors silently lost
    }
}
```

### Example 4: Consumer implementation

Title: @KafkaListener with typed payload and thin handler
Description: Annotate the listener class with `@Component`. Declare `topics` and `groupId` on the `@KafkaListener` so the consumer group is explicit and testable. Accept the typed event record as the method parameter. Delegate all business logic to an application service — the listener method should only translate the Kafka message into a service call.

**Good example:**

```java
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.stereotype.Component;

@Component
class BillingEventListener {

    private final BillingService billingService;

    BillingEventListener(BillingService billingService) {
        this.billingService = billingService;
    }

    @KafkaListener(topics = "orders.created.v1", groupId = "billing-service-v1")
    void onOrderCreated(OrderCreatedEvent event) {
        billingService.createInvoice(event.orderId(), event.customerId());
    }
}
```

**Bad example:**

```java
// Bad: no groupId means a random group on each restart causing re-read from the beginning;
// String payload requires manual parsing; business logic mixed directly in listener
@KafkaListener(topics = "orders.created.v1")
void onMessage(String rawJson) {
    var orderId = rawJson.split(",")[0]; // fragile parsing
    // 50 lines of business logic inline ...
}
```

### Example 5: Error handling and dead-letter topic

Title: DefaultErrorHandler with backoff and DeadLetterPublishingRecoverer
Description: Configure a `DefaultErrorHandler` bean that retries with exponential back-off and then routes unrecoverable messages to a dead-letter topic via `DeadLetterPublishingRecoverer`. The recoverer automatically targets `{topic}.DLT` by default. Register the handler on the container factory so it applies to all listeners. Do not swallow exceptions inside the listener — let them propagate so the container's error handler can decide.

**Good example:**

```java
import org.apache.kafka.common.TopicPartition;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.kafka.listener.DeadLetterPublishingRecoverer;
import org.springframework.kafka.listener.DefaultErrorHandler;
import org.springframework.util.backoff.ExponentialBackOff;

@Configuration
class KafkaErrorConfig {

    @Bean
    DefaultErrorHandler errorHandler(KafkaTemplate<Object, Object> template) {
        var recoverer = new DeadLetterPublishingRecoverer(template,
            (record, ex) -> new TopicPartition(record.topic() + ".DLT", -1));

        var backOff = new ExponentialBackOff(500L, 2.0);
        backOff.setMaxElapsedTime(30_000L); // stop retrying after 30 s

        return new DefaultErrorHandler(recoverer, backOff);
    }
}
```

**Bad example:**

```java
// Bad: swallowing the exception causes acknowledgement of poison messages;
// they are never retried and never routed to a DLT
@KafkaListener(topics = "orders.created.v1", groupId = "billing-service-v1")
void onOrderCreated(OrderCreatedEvent event) {
    try {
        billingService.createInvoice(event.orderId(), event.customerId());
    } catch (Exception ignored) {
        // silent: message acknowledged, data loss guaranteed
    }
}
```

### Example 6: Idempotent consumer

Title: De-duplicate on eventId to survive retries and rebalances
Description: Kafka at-least-once delivery means a consumer can receive the same message more than once — on broker retries, after a rebalance, or when consuming from a DLT. Check the `eventId` against a de-duplication store (an in-memory set in dev/test; a database table or Redis in production) before processing. Persist the `eventId` inside the same transaction as the business side effect.

**Good example:**

```java
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.stereotype.Component;
import org.springframework.transaction.annotation.Transactional;
import java.util.Set;
import java.util.concurrent.ConcurrentHashMap;

@Component
class IdempotentBillingListener {

    private final Set<String> processedEventIds = ConcurrentHashMap.newKeySet();
    private final BillingService billingService;

    IdempotentBillingListener(BillingService billingService) {
        this.billingService = billingService;
    }

    @KafkaListener(topics = "orders.created.v1", groupId = "billing-service-v1")
    @Transactional
    void onOrderCreated(OrderCreatedEvent event) {
        if (!processedEventIds.add(event.eventId())) {
            return; // already processed — skip without error
        }
        billingService.createInvoice(event.orderId(), event.customerId());
    }
}
```

**Bad example:**

```java
@KafkaListener(topics = "orders.created.v1", groupId = "billing-service-v1")
void onOrderCreated(OrderCreatedEvent event) {
    // Bad: no idempotency guard — rebalance or retry doubles billing
    billingService.createInvoice(event.orderId(), event.customerId());
}
```

### Example 7: Integration testing

Title: @EmbeddedKafka with KafkaTestUtils for end-to-end listener tests
Description: Annotate the test class with `@SpringBootTest` and `@EmbeddedKafka` to start an in-process broker. Use `KafkaTestUtils.getRecords` to consume messages programmatically and assert on their values. This verifies the full serialization/deserialization path without a running Kafka cluster.

**Good example:**

```java
import org.apache.kafka.clients.consumer.Consumer;
import org.apache.kafka.clients.consumer.ConsumerRecords;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.kafka.core.ConsumerFactory;
import org.springframework.kafka.test.EmbeddedKafkaBroker;
import org.springframework.kafka.test.context.EmbeddedKafka;
import org.springframework.kafka.test.utils.KafkaTestUtils;

import static org.assertj.core.api.Assertions.assertThat;

@SpringBootTest
@EmbeddedKafka(topics = {"orders.created.v1"}, partitions = 1)
class OrderEventPublisherIT {

    @Autowired
    OrderEventPublisher publisher;

    @Autowired
    EmbeddedKafkaBroker broker;

    @Autowired
    ConsumerFactory<String, OrderCreatedEvent> consumerFactory;

    @Test
    void publish_sendsEventToTopic() {
        OrderCreatedEvent event = OrderCreatedEvent.of("order-1", "cust-1");
        publisher.publish(event);

        try (Consumer<String, OrderCreatedEvent> consumer = consumerFactory.createConsumer("test-group", "")) {
            broker.consumeFromAnEmbeddedTopic(consumer, "orders.created.v1");
            ConsumerRecords<String, OrderCreatedEvent> records = KafkaTestUtils.getRecords(consumer);
            assertThat(records.count()).isEqualTo(1);
            assertThat(records.iterator().next().value().orderId()).isEqualTo("order-1");
        }
    }
}
```

**Bad example:**

```java
// Bad: mocking KafkaTemplate proves nothing — does not test serialization or topic routing
@SpringBootTest
class OrderEventPublisherTest {

    @MockBean
    KafkaTemplate<String, OrderCreatedEvent> template;

    @Autowired
    OrderEventPublisher publisher;

    @Test
    void publish_callsTemplate() {
        publisher.publish(OrderCreatedEvent.of("o1", "c1"));
        verify(template).send(any(), any(), any()); // verifies Mockito glue only
    }
}
```

## Output Format

- **ANALYZE** Kafka code: event schema versioning, producer key strategy, listener group isolation, error handler registration, idempotency guards, and test coverage
- **CATEGORIZE** issues by impact (RELIABILITY for missing retries/DLT, CORRECTNESS for missing idempotency, MAINTAINABILITY for untyped schemas, SECURITY for untrusted topic name injection)
- **APPLY** Spring Kafka–aligned fixes: type the templates, key producers on the aggregate id, register DefaultErrorHandler with backoff and DLT, add eventId de-duplication
- **IMPLEMENT** changes so topic configs, serializers, and tests stay consistent
- **EXPLAIN** trade-offs (at-least-once vs exactly-once, fixed vs exponential backoff, in-process vs Testcontainers Kafka)
- **TEST** with `@EmbeddedKafka` for unit/integration; use Testcontainers for full-stack acceptance tests
- **VALIDATE** with `./mvnw compile` before and `./mvnw clean verify` after changes

## Safeguards

- **BLOCKING SAFETY CHECK**: Run `./mvnw compile` before ANY Kafka refactoring — compilation failure is a HARD STOP
- **CRITICAL VALIDATION**: Run `./mvnw clean verify` after changes; exercise listener integration tests before promoting
- **INJECTION SAFETY**: Never construct topic names or message headers from untrusted user input
- **ERROR HANDLING**: Never swallow exceptions inside a `@KafkaListener` — propagate so the container's error handler can retry or route to DLT
- **IDEMPOTENCY**: Always de-duplicate on `eventId` — Kafka's at-least-once guarantee means consumers must tolerate duplicates
- **KEY STRATEGY**: Always set the Kafka message key to the aggregate's natural key; null keys disable partition-level ordering
- **DLT MONITORING**: Set up alerting on the DLT topic — messages landing there indicate systematic processing failures
- **INCREMENTAL SAFETY**: Change one producer/consumer surface at a time; verify with `@EmbeddedKafka` tests between steps