---
name: spring-boot-event-driven-patterns
description: Implement Event-Driven Architecture (EDA) in Spring Boot using ApplicationEvent, @EventListener, and Kafka. Use for building loosely-coupled microservices with domain events, transactional event listeners, and distributed messaging patterns.
allowed-tools: Read, Write, Bash
category: backend
tags: [spring-boot, java, event-driven, eda, kafka, messaging, domain-events, microservices, spring-cloud-stream]
version: 1.1.0
---

# Spring Boot Event-Driven Patterns

## Overview

Implement Event-Driven Architecture (EDA) patterns in Spring Boot 3.x using domain events, ApplicationEventPublisher, @TransactionalEventListener, and distributed messaging with Kafka and Spring Cloud Stream.

## When to Use This Skill

Use this skill when building applications that require:
- Loose coupling between microservices through event-based communication
- Domain event publishing from aggregate roots in DDD architectures
- Transactional event listeners ensuring consistency after database commits
- Distributed messaging with Kafka for inter-service communication
- Event streaming with Spring Cloud Stream for reactive systems
- Reliability using the transactional outbox pattern
- Asynchronous communication between bounded contexts
- Event sourcing foundations with proper event sourcing patterns

## Setup and Configuration

### Required Dependencies

To implement event-driven patterns, include these dependencies in your project:

**Maven:**
```xml
<dependencies>
    <!-- Spring Boot Web -->
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-web</artifactId>
    </dependency>

    <!-- Spring Data JPA -->
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-data-jpa</artifactId>
    </dependency>

    <!-- Kafka for distributed messaging -->
    <dependency>
        <groupId>org.springframework.kafka</groupId>
        <artifactId>spring-kafka</artifactId>
    </dependency>

    <!-- Spring Cloud Stream -->
    <dependency>
        <groupId>org.springframework.cloud</groupId>
        <artifactId>spring-cloud-stream</artifactId>
        <version>4.0.4</version> // Use latest compatible version
    </dependency>

    <!-- Testing -->
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-test</artifactId>
        <scope>test</scope>
    </dependency>

    <!-- Testcontainers for integration testing -->
    <dependency>
        <groupId>org.testcontainers</groupId>
        <artifactId>testcontainers</artifactId>
        <version>1.19.0</version>
        <scope>test</scope>
    </dependency>
</dependencies>
```

**Gradle:**
```gradle
dependencies {
    // Spring Boot Web
    implementation 'org.springframework.boot:spring-boot-starter-web'

    // Spring Data JPA
    implementation 'org.springframework.boot:spring-boot-starter-data-jpa'

    // Kafka
    implementation 'org.springframework.kafka:spring-kafka'

    // Spring Cloud Stream
    implementation 'org.springframework.cloud:spring-cloud-stream:4.0.4'

    // Testing
    testImplementation 'org.springframework.boot:spring-boot-starter-test'
    testImplementation 'org.testcontainers:testcontainers:1.19.0'
}
```

### Basic Configuration

Configure your application for event-driven architecture:

```properties
# Server Configuration
server.port=8080

# Kafka Configuration
spring.kafka.bootstrap-servers=localhost:9092
spring.kafka.producer.key-serializer=org.apache.kafka.common.serialization.StringSerializer
spring.kafka.producer.value-serializer=org.springframework.kafka.support.serializer.JsonSerializer

# Spring Cloud Stream Configuration
spring.cloud.stream.kafka.binder.brokers=localhost:9092
```

## Core Patterns

### 1. Domain Events Design

Create immutable domain events for business domain changes:

```java
// Domain event base class
public abstract class DomainEvent {
    private final UUID eventId;
    private final LocalDateTime occurredAt;
    private final UUID correlationId;

    protected DomainEvent() {
        this.eventId = UUID.randomUUID();
        this.occurredAt = LocalDateTime.now();
        this.correlationId = UUID.randomUUID();
    }

    protected DomainEvent(UUID correlationId) {
        this.eventId = UUID.randomUUID();
        this.occurredAt = LocalDateTime.now();
        this.correlationId = correlationId;
    }

    // Getters
    public UUID getEventId() { return eventId; }
    public LocalDateTime getOccurredAt() { return occurredAt; }
    public UUID getCorrelationId() { return correlationId; }
}

// Specific domain events
public class ProductCreatedEvent extends DomainEvent {
    private final ProductId productId;
    private final String name;
    private final BigDecimal price;
    private final Integer stock;

    public ProductCreatedEvent(ProductId productId, String name, BigDecimal price, Integer stock) {
        super();
        this.productId = productId;
        this.name = name;
        this.price = price;
        this.stock = stock;
    }

    // Getters
    public ProductId getProductId() { return productId; }
    public String getName() { return name; }
    public BigDecimal getPrice() { return price; }
    public Integer getStock() { return stock; }
}
```

### 2. Aggregate Root with Event Publishing

Implement aggregates that publish domain events:

```java
@Entity
@Getter
@ToString
@EqualsAndHashCode(of = "id")
@NoArgsConstructor(access = AccessLevel.PROTECTED)
public class Product {
    @Id
    private ProductId id;
    private String name;
    private BigDecimal price;
    private Integer stock;

    @Transient
    private List<DomainEvent> domainEvents = new ArrayList<>();

    public static Product create(String name, BigDecimal price, Integer stock) {
        Product product = new Product();
        product.id = ProductId.generate();
        product.name = name;
        product.price = price;
        product.stock = stock;
        product.domainEvents.add(new ProductCreatedEvent(product.id, name, price, stock));
        return product;
    }

    public void decreaseStock(Integer quantity) {
        this.stock -= quantity;
        this.domainEvents.add(new ProductStockDecreasedEvent(this.id, quantity, this.stock));
    }

    public List<DomainEvent> getDomainEvents() {
        return new ArrayList<>(domainEvents);
    }

    public void clearDomainEvents() {
        domainEvents.clear();
    }
}
```

### 3. Application Event Publishing

Publish domain events from application services:

```java
@Service
@RequiredArgsConstructor
@Transactional
public class ProductApplicationService {
    private final ProductRepository productRepository;
    private final ApplicationEventPublisher eventPublisher;

    public ProductResponse createProduct(CreateProductRequest request) {
        Product product = Product.create(
            request.getName(),
            request.getPrice(),
            request.getStock()
        );

        productRepository.save(product);

        // Publish domain events
        product.getDomainEvents().forEach(eventPublisher::publishEvent);
        product.clearDomainEvents();

        return mapToResponse(product);
    }
}
```

### 4. Local Event Handling

Handle events with transactional event listeners:

```java
@Component
@RequiredArgsConstructor
public class ProductEventHandler {
    private final NotificationService notificationService;
    private final AuditService auditService;

    @TransactionalEventListener(phase = TransactionPhase.AFTER_COMMIT)
    public void onProductCreated(ProductCreatedEvent event) {
        auditService.logProductCreation(
            event.getProductId().getValue(),
            event.getName(),
            event.getPrice(),
            event.getCorrelationId()
        );

        notificationService.sendProductCreatedNotification(event.getName());
    }

    @TransactionalEventListener(phase = TransactionPhase.AFTER_COMMIT)
    public void onProductStockDecreased(ProductStockDecreasedEvent event) {
        notificationService.sendStockUpdateNotification(
            event.getProductId().getValue(),
            event.getQuantity()
        );
    }
}
```

### 5. Distributed Event Publishing

Publish events to Kafka for inter-service communication:

```java
@Component
@RequiredArgsConstructor
public class ProductEventPublisher {
    private final KafkaTemplate<String, Object> kafkaTemplate;

    public void publishProductCreatedEvent(ProductCreatedEvent event) {
        ProductCreatedEventDto dto = mapToDto(event);
        kafkaTemplate.send("product-events", event.getProductId().getValue(), dto);
    }

    private ProductCreatedEventDto mapToDto(ProductCreatedEvent event) {
        return new ProductCreatedEventDto(
            event.getEventId(),
            event.getProductId().getValue(),
            event.getName(),
            event.getPrice(),
            event.getStock(),
            event.getOccurredAt(),
            event.getCorrelationId()
        );
    }
}
```

### 6. Event Consumer with Spring Cloud Stream

Consume events using functional programming style:

```java
@Component
@RequiredArgsConstructor
public class ProductEventStreamConsumer {
    private final OrderService orderService;

    @Bean
    public Consumer<ProductCreatedEventDto> productCreatedConsumer() {
        return event -> {
            orderService.onProductCreated(event);
        };
    }

    @Bean
    public Consumer<ProductStockDecreasedEventDto> productStockDecreasedConsumer() {
        return event -> {
            orderService.onProductStockDecreased(event);
        };
    }
}
```

## Advanced Patterns

### Transactional Outbox Pattern

Ensure reliable event publishing with the outbox pattern:

```java
@Entity
@Table(name = "outbox_events")
@Getter
@Setter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class OutboxEvent {
    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;

    private String aggregateId;
    private String eventType;
    private String payload;
    private UUID correlationId;
    private LocalDateTime createdAt;
    private LocalDateTime publishedAt;
    private Integer retryCount;
}

@Component
@RequiredArgsConstructor
public class OutboxEventProcessor {
    private final OutboxEventRepository outboxRepository;
    private final KafkaTemplate<String, Object> kafkaTemplate;

    @Scheduled(fixedDelay = 5000)
    @Transactional
    public void processPendingEvents() {
        List<OutboxEvent> pendingEvents = outboxRepository.findByPublishedAtNull();

        for (OutboxEvent event : pendingEvents) {
            try {
                kafkaTemplate.send("product-events", event.getAggregateId(), event.getPayload());
                event.setPublishedAt(LocalDateTime.now());
                outboxRepository.save(event);
            } catch (Exception e) {
                event.setRetryCount(event.getRetryCount() + 1);
                outboxRepository.save(event);
            }
        }
    }
}
```

## Testing Strategies

### Unit Testing Domain Events

Test domain event publishing and handling:

```java
class ProductTest {
    @Test
    void shouldPublishProductCreatedEventOnCreation() {
        Product product = Product.create("Test Product", BigDecimal.TEN, 100);

        assertThat(product.getDomainEvents()).hasSize(1);
        assertThat(product.getDomainEvents().get(0))
            .isInstanceOf(ProductCreatedEvent.class);
    }
}

@ExtendWith(MockitoExtension.class)
class ProductEventHandlerTest {
    @Mock
    private NotificationService notificationService;

    @InjectMocks
    private ProductEventHandler handler;

    @Test
    void shouldHandleProductCreatedEvent() {
        ProductCreatedEvent event = new ProductCreatedEvent(
            ProductId.of("123"), "Product", BigDecimal.TEN, 100
        );

        handler.onProductCreated(event);

        verify(notificationService).sendProductCreatedNotification("Product");
    }
}
```

### Integration Testing with Testcontainers

Test Kafka integration with Testcontainers:

```java
@SpringBootTest
@Testcontainers
class KafkaEventIntegrationTest {
    @Container
    static KafkaContainer kafka = new KafkaContainer(DockerImageName.parse("confluentinc/cp-kafka:7.5.0"));

    @Autowired
    private ProductApplicationService productService;

    @DynamicPropertySource
    static void configureProperties(DynamicPropertyRegistry registry) {
        registry.add("spring.kafka.bootstrap-servers", kafka::getBootstrapServers);
    }

    @Test
    void shouldPublishEventToKafka() {
        CreateProductRequest request = new CreateProductRequest(
            "Test Product", BigDecimal.valueOf(99.99), 50
        );

        ProductResponse response = productService.createProduct(request);

        // Verify event was published
        verify(eventPublisher).publishProductCreatedEvent(any(ProductCreatedEvent.class));
    }
}
```

## Best Practices

### Event Design Guidelines

- **Use past tense naming**: ProductCreated, not CreateProduct
- **Keep events immutable**: All fields should be final
- **Include correlation IDs**: For tracing events across services
- **Serialize to JSON**: For cross-service compatibility

### Transactional Consistency

- **Use AFTER_COMMIT phase**: Ensures events are published after successful database transaction
- **Implement idempotent handlers**: Handle duplicate events gracefully
- **Add retry mechanisms**: For failed event processing

### Error Handling

- **Implement dead-letter queues**: For events that fail processing
- **Log all failures**: Include sufficient context for debugging
- **Set appropriate timeouts**: For event processing operations

### Performance Considerations

- **Batch event processing**: When handling high volumes
- **Use proper partitioning**: For Kafka topics
- **Monitor event latencies**: Set up alerts for slow processing

## Examples and References

See the following resources for comprehensive examples:

- [Complete working examples](references/examples.md)
- [Detailed implementation patterns](references/event-driven-patterns-reference.md)

## Troubleshooting

### Common Issues

**Events not being published:**
- Check transaction phase configuration
- Verify ApplicationEventPublisher is properly autowired
- Ensure transaction is committed before event publishing

**Kafka connection issues:**
- Verify bootstrap servers configuration
- Check network connectivity to Kafka
- Ensure proper serialization configuration

**Event handling failures:**
- Check for circular dependencies in event handlers
- Verify transaction boundaries
- Monitor for exceptions in event processing

### Debug Tips

- Enable debug logging for Spring events: `logging.level.org.springframework.context=DEBUG`
- Use correlation IDs to trace events across services
- Monitor event processing metrics in Actuator endpoints

---

This skill provides the essential patterns and best practices for implementing event-driven architectures in Spring Boot applications.