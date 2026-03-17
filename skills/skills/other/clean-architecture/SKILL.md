---
name: clean-architecture
description: Provides implementation patterns for Clean Architecture, Hexagonal Architecture (Ports & Adapters), and Domain-Driven Design in Java 21+ Spring Boot 3.5+ applications. Use when structuring layered architectures, separating domain logic from frameworks, implementing ports and adapters, creating entities/value objects/aggregates, or refactoring monolithic codebases for testability and maintainability.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Clean Architecture, Hexagonal Architecture & DDD for Spring Boot

## Overview

This skill provides comprehensive guidance for implementing Clean Architecture, Hexagonal Architecture (Ports & Adapters), and Domain-Driven Design tactical patterns in Java 21+ Spring Boot 3.5+ applications. It ensures clear separation of concerns, framework-independent domain logic, and highly testable codebases through proper layering and dependency management.

## When to Use

- Architecting new Spring Boot applications with clear separation of concerns
- Refactoring tightly coupled code into testable, layered architectures
- Implementing domain logic independent of frameworks and infrastructure
- Designing ports and adapters for swappable implementations
- Applying Domain-Driven Design tactical patterns (entities, value objects, aggregates)
- Creating testable business logic without Spring context dependencies
- Trigger phrases: **"implement clean architecture"**, **"ports and adapters pattern"**, **"separate domain from infrastructure"**, **"hexagonal architecture Spring Boot"**, **"DDD aggregate design"**

## Instructions

### 1. Understand the Core Concepts

#### Clean Architecture Layers (Dependency Rule)

Dependencies flow inward. Inner layers know nothing about outer layers.

| Layer | Responsibility | Spring Boot Equivalent |
|-------|---------------|----------------------|
| **Domain** | Entities, value objects, domain events, repository interfaces | `domain/` - no Spring annotations |
| **Application** | Use cases, application services, DTOs, ports | `application/` - @Service, @Transactional |
| **Infrastructure** | Frameworks, database, external APIs | `infrastructure/` - @Repository, @Entity |
| **Adapter** | Controllers, presenters, external gateways | `adapter/` - @RestController |

#### Hexagonal Architecture (Ports & Adapters)

- **Domain Core**: Pure Java business logic, no framework dependencies
- **Ports**: Interfaces defining contracts (driven and driving)
- **Adapters**: Concrete implementations (JPA, REST, messaging)

#### Domain-Driven Design Tactical Patterns

- **Entities**: Objects with identity and lifecycle (e.g., `Order`, `Customer`)
- **Value Objects**: Immutable, defined by attributes (e.g., `Money`, `Email`)
- **Aggregates**: Consistency boundary with root entity
- **Domain Events**: Capture significant business occurrences
- **Repositories**: Persistence abstraction, implemented in infrastructure

### 2. Organize Package Structure

Follow this feature-based package organization:

```
com.example.order/
├── domain/
│   ├── model/              # Entities, value objects
│   ├── event/              # Domain events
│   ├── repository/         # Repository interfaces (ports)
│   └── exception/          # Domain exceptions
├── application/
│   ├── port/in/            # Driving ports (use case interfaces)
│   ├── port/out/           # Driven ports (external service interfaces)
│   ├── service/            # Application services
│   └── dto/                # Request/response DTOs
├── infrastructure/
│   ├── persistence/        # JPA entities, repository adapters
│   └── external/           # External service adapters
└── adapter/
    └── rest/               # REST controllers
```

### 3. Implement the Domain Layer (Framework-Free)

The domain layer must have zero dependencies on Spring or any framework.

- Use Java records for immutable value objects with built-in validation
- Place business logic in entities, not services (Rich Domain Model)
- Define repository interfaces (ports) in the domain layer
- Use strongly-typed IDs to prevent ID confusion
- Implement domain events for decoupling side effects
- Use factory methods for entity creation to enforce invariants

### 4. Implement the Application Layer

- Create use case interfaces (driving ports) in `application/port/in/`
- Create external service interfaces (driven ports) in `application/port/out/`
- Implement application services with `@Service` and `@Transactional`
- Use DTOs for request/response, separate from domain models
- Publish domain events after successful operations

### 5. Implement the Infrastructure Layer (Adapters)

- Create JPA entities in `infrastructure/persistence/`
- Implement repository adapters that map between domain and JPA entities
- Use MapStruct or manual mappers for domain-JPA conversion
- Configure conditional beans for swappable implementations
- Keep infrastructure concerns isolated from domain logic

### 6. Implement the Adapter Layer (REST)

- Create REST controllers in `adapter/rest/`
- Inject use case interfaces, not implementations
- Use Bean Validation on DTOs
- Return proper HTTP status codes and responses
- Handle exceptions with global exception handlers

### 7. Apply Best Practices

1. **Dependency Rule**: Domain has zero dependencies on Spring or other frameworks
2. **Immutable Value Objects**: Use Java records for value objects with built-in validation
3. **Rich Domain Models**: Place business logic in entities, not services
4. **Repository Pattern**: Domain defines interface, infrastructure implements
5. **Domain Events**: Decouple side effects from primary operations
6. **Constructor Injection**: Mandatory dependencies via final fields
7. **DTO Mapping**: Separate domain models from API contracts
8. **Transaction Boundaries**: Place @Transactional in application services

### 8. Write Tests

- **Domain Tests**: Pure unit tests without Spring context, fast execution
- **Application Tests**: Unit tests with mocked ports using Mockito
- **Infrastructure Tests**: Integration tests with @DataJpaTest and Testcontainers
- **Adapter Tests**: Controller tests with @WebMvcTest

## Examples

### Example 1: Domain Layer - Entity with Domain Events

```java
// domain/model/Order.java
public class Order {
    private final OrderId id;
    private final List<OrderItem> items;
    private Money total;
    private OrderStatus status;
    private final List<DomainEvent> domainEvents = new ArrayList<>();

    private Order(OrderId id, List<OrderItem> items) {
        this.id = id;
        this.items = new ArrayList<>(items);
        this.status = OrderStatus.PENDING;
        calculateTotal();
    }

    public static Order create(List<OrderItem> items) {
        validateItems(items);
        Order order = new Order(OrderId.generate(), items);
        order.domainEvents.add(new OrderCreatedEvent(order.id, order.total));
        return order;
    }

    public void confirm() {
        if (status != OrderStatus.PENDING) {
            throw new DomainException("Only pending orders can be confirmed");
        }
        this.status = OrderStatus.CONFIRMED;
    }

    public List<DomainEvent> getDomainEvents() {
        return List.copyOf(domainEvents);
    }

    public void clearDomainEvents() {
        domainEvents.clear();
    }
}
```

### Example 2: Domain Layer - Value Object with Validation

```java
// domain/model/Money.java (Value Object)
public record Money(BigDecimal amount, Currency currency) {
    public Money {
        if (amount.compareTo(BigDecimal.ZERO) < 0) {
            throw new DomainException("Amount cannot be negative");
        }
    }

    public static Money zero() {
        return new Money(BigDecimal.ZERO, Currency.getInstance("EUR"));
    }

    public Money add(Money other) {
        if (!this.currency.equals(other.currency)) {
            throw new DomainException("Currency mismatch");
        }
        return new Money(this.amount.add(other.amount), this.currency);
    }
}
```

### Example 3: Domain Layer - Repository Port

```java
// domain/repository/OrderRepository.java (Port)
public interface OrderRepository {
    Order save(Order order);
    Optional<Order> findById(OrderId id);
}
```

### Example 4: Application Layer - Use Case and Service

```java
// application/port/in/CreateOrderUseCase.java
public interface CreateOrderUseCase {
    OrderResponse createOrder(CreateOrderRequest request);
}

// application/dto/CreateOrderRequest.java
public record CreateOrderRequest(
    @NotNull UUID customerId,
    @NotEmpty List<OrderItemRequest> items
) {}

// application/service/OrderService.java
@Service
@RequiredArgsConstructor
@Transactional
public class OrderService implements CreateOrderUseCase {
    private final OrderRepository orderRepository;
    private final PaymentGateway paymentGateway;
    private final DomainEventPublisher eventPublisher;

    @Override
    public OrderResponse createOrder(CreateOrderRequest request) {
        List<OrderItem> items = mapItems(request.items());
        Order order = Order.create(items);

        PaymentResult payment = paymentGateway.charge(order.getTotal());
        if (!payment.successful()) {
            throw new PaymentFailedException("Payment failed");
        }

        order.confirm();
        Order saved = orderRepository.save(order);
        publishEvents(order);

        return OrderMapper.toResponse(saved);
    }

    private void publishEvents(Order order) {
        order.getDomainEvents().forEach(eventPublisher::publish);
        order.clearDomainEvents();
    }
}
```

### Example 5: Infrastructure Layer - JPA Entity and Adapter

```java
// infrastructure/persistence/OrderJpaEntity.java
@Entity
@Table(name = "orders")
public class OrderJpaEntity {
    @Id
    private UUID id;
    @Enumerated(EnumType.STRING)
    private OrderStatus status;
    private BigDecimal totalAmount;
    @OneToMany(cascade = CascadeType.ALL, orphanRemoval = true)
    private List<OrderItemJpaEntity> items;
}

// infrastructure/persistence/OrderRepositoryAdapter.java
@Component
@RequiredArgsConstructor
public class OrderRepositoryAdapter implements OrderRepository {
    private final OrderJpaRepository jpaRepository;
    private final OrderJpaMapper mapper;

    @Override
    public Order save(Order order) {
        OrderJpaEntity entity = mapper.toEntity(order);
        return mapper.toDomain(jpaRepository.save(entity));
    }

    @Override
    public Optional<Order> findById(OrderId id) {
        return jpaRepository.findById(id.value()).map(mapper::toDomain);
    }
}
```

### Example 6: Adapter Layer - REST Controller

```java
// adapter/rest/OrderController.java
@RestController
@RequestMapping("/api/orders")
@RequiredArgsConstructor
public class OrderController {
    private final CreateOrderUseCase createOrderUseCase;

    @PostMapping
    public ResponseEntity<OrderResponse> createOrder(
            @Valid @RequestBody CreateOrderRequest request) {
        OrderResponse response = createOrderUseCase.createOrder(request);
        URI location = ServletUriComponentsBuilder
            .fromCurrentRequest()
            .path("/{id}")
            .buildAndExpand(response.id())
            .toUri();
        return ResponseEntity.created(location).body(response);
    }
}
```

### Example 7: Domain Tests (No Spring Context)

```java
class OrderTest {
    @Test
    void shouldCreateOrderWithValidItems() {
        List<OrderItem> items = List.of(
            new OrderItem(new ProductId(UUID.randomUUID()), 2, new Money("10.00", EUR))
        );

        Order order = Order.create(items);

        assertThat(order.getStatus()).isEqualTo(OrderStatus.PENDING);
        assertThat(order.getDomainEvents()).hasSize(1);
    }
}
```

### Example 8: Application Tests (Unit with Mocks)

```java
@ExtendWith(MockitoExtension.class)
class OrderServiceTest {
    @Mock OrderRepository orderRepository;
    @Mock PaymentGateway paymentGateway;
    @Mock DomainEventPublisher eventPublisher;

    @InjectMocks OrderService orderService;

    @Test
    void shouldCreateAndConfirmOrder() {
        when(paymentGateway.charge(any())).thenReturn(new PaymentResult(true, "tx-123"));
        when(orderRepository.save(any())).thenAnswer(i -> i.getArgument(0));

        OrderResponse response = orderService.createOrder(createRequest());

        assertThat(response.status()).isEqualTo(OrderStatus.CONFIRMED);
        verify(eventPublisher).publish(any(OrderCreatedEvent.class));
    }
}
```

## Best Practices

1. **Dependency Rule**: Domain has zero dependencies on Spring or other frameworks - this is the most critical principle
2. **Immutable Value Objects**: Use Java records for value objects with built-in validation in compact constructors
3. **Rich Domain Models**: Place business logic in entities, not services - avoid anemic domain models
4. **Repository Pattern**: Domain defines interface, infrastructure implements - never the reverse
5. **Domain Events**: Decouple side effects from primary operations using event-driven patterns
6. **Constructor Injection**: Mandatory dependencies via final fields with Lombok @RequiredArgsConstructor
7. **DTO Mapping**: Separate domain models from API contracts - never expose entities directly
8. **Transaction Boundaries**: Place @Transactional in application services, never in domain layer
9. **Factory Methods**: Use static factory methods like `Entity.create()` for entity construction with invariant enforcement
10. **Separate JPA Entities**: Keep domain entities separate from JPA entities with mappers between them

## Constraints and Warnings

### Critical Constraints

- **Domain Layer Purity**: Never add Spring annotations (`@Entity`, `@Autowired`, `@Component`) to domain classes
- **Dependency Direction**: Dependencies must only point inward (domain <- application <- infrastructure/adapter)
- **Framework Isolation**: All framework-specific code must stay in infrastructure and adapter layers

### Common Pitfalls to Avoid

- **Anemic Domain Model**: Entities with only getters/setters, logic in services - place business logic in entities
- **Framework Leakage**: `@Entity`, `@Autowired` in domain layer - keep domain framework-free
- **Lazy Loading Issues**: Exposing JPA entities through domain model - use mappers to convert
- **Circular Dependencies**: Between domain aggregates - use IDs instead of direct references
- **Missing Domain Events**: Direct service calls instead of events for cross-aggregate communication
- **Repository Misplacement**: Defining repository interfaces in infrastructure - they belong in domain
- **DTO Bypass**: Exposing domain entities directly in API - always use DTOs for external contracts

### Performance Considerations

- Separate JPA entities from domain models to avoid lazy loading issues
- Use read-only transactions for query operations
- Consider CQRS for complex read/write scenarios

## References

- `references/java-clean-architecture.md` - Java-specific patterns (records, sealed classes, strongly-typed IDs)
- `references/spring-boot-implementation.md` - Spring Boot integration (DI patterns, JPA mapping, transaction management)
