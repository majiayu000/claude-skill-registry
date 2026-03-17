---
name: java-backend
description: Java backend development skill for Spring Boot 3.x microservices using Java 21, Spring Data JPA, and Modulith. Use when creating or modifying Java backend code including REST controllers, services, repositories, entities, DTOs, mappers, tests, or configuration. Covers feature development patterns, testing conventions, and microservice best practices.
---

# Java Backend Development

## Technology Stack

- **Java 21** - Use records, pattern matching, text blocks, virtual threads
- **Spring Boot 3.x** - Latest stable version
- **Spring Data JPA** - Hibernate ORM with PostgreSQL/MySQL
- **Spring Modulith** - Modular monolith structure
- **Maven/Gradle** - Build tool (prefer Gradle with Kotlin DSL)

## Project Structure

```
src/main/java/com/company/project/
├── module/                    # Spring Modulith modules
│   ├── order/
│   │   ├── Order.java         # Entity (aggregate root)
│   │   ├── OrderRepository.java
│   │   ├── OrderService.java
│   │   ├── OrderController.java
│   │   ├── dto/
│   │   │   ├── CreateOrderRequest.java
│   │   │   └── OrderResponse.java
│   │   └── mapper/
│   │       └── OrderMapper.java
│   └── package-info.java      # Module boundary
├── common/                    # Shared utilities
│   ├── exception/
│   │   ├── BusinessException.java
│   │   └── GlobalExceptionHandler.java
│   └── config/
└── Application.java
```

## Layer Conventions

### Entity Layer

```java
@Entity
@Table(name = "orders")
class Order {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Embedded
    private CustomerInfo customerInfo;

    @OneToMany(cascade = CascadeType.ALL, orphanRemoval = true)
    @JoinColumn(name = "order_id")
    private List<OrderItem> items = new ArrayList<>();

    @Enumerated(EnumType.STRING)
    private OrderStatus status;

    // Factory method
    public static Order create(CustomerInfo customer, List<OrderItem> items) {
        Order order = new Order();
        order.customerInfo = customer;
        order.items = items;
        order.status = OrderStatus.CREATED;
        return order;
    }

    // Business method
    public void cancel() {
        if (status != OrderStatus.CREATED) {
            throw new BusinessException("Cannot cancel order in status: " + status);
        }
        this.status = OrderStatus.CANCELLED;
    }
}
```

### Repository Layer

```java
interface OrderRepository extends JpaRepository<Order, Long> {

    @Query("SELECT o FROM Order o WHERE o.customerInfo.email = :email")
    List<Order> findByCustomerEmail(@Param("email") String email);

    @Modifying
    @Query("UPDATE Order o SET o.status = :status WHERE o.id = :id")
    int updateStatus(@Param("id") Long id, @Param("status") OrderStatus status);
}
```

### Service Layer

```java
@Service
@Transactional
class OrderService {

    private final OrderRepository orderRepository;
    private final OrderMapper orderMapper;

    public OrderResponse createOrder(CreateOrderRequest request) {
        Order order = orderMapper.toEntity(request);
        Order saved = orderRepository.save(order);
        return orderMapper.toResponse(saved);
    }

    @Transactional(readOnly = true)
    public OrderResponse getOrder(Long id) {
        return orderRepository.findById(id)
            .map(orderMapper::toResponse)
            .orElseThrow(() -> new NotFoundException("Order not found: " + id));
    }

    public void cancelOrder(Long id) {
        Order order = orderRepository.findById(id)
            .orElseThrow(() -> new NotFoundException("Order not found: " + id));
        order.cancel(); // Business logic in entity
    }
}
```

### Controller Layer

```java
@RestController
@RequestMapping("/api/v1/orders")
@RequiredArgsConstructor
class OrderController {

    private final OrderService orderService;

    @PostMapping
    ResponseEntity<OrderResponse> createOrder(@Valid @RequestBody CreateOrderRequest request) {
        return ResponseEntity.status(HttpStatus.CREATED)
            .body(orderService.createOrder(request));
    }

    @GetMapping("/{id}")
    ResponseEntity<OrderResponse> getOrder(@PathVariable Long id) {
        return ResponseEntity.ok(orderService.getOrder(id));
    }

    @PostMapping("/{id}/cancel")
    ResponseEntity<Void> cancelOrder(@PathVariable Long id) {
        orderService.cancelOrder(id);
        return ResponseEntity.noContent().build();
    }
}
```

## DTO and Mapper Pattern

### Request DTO

```java
public record CreateOrderRequest(
    @NotBlank String customerEmail,
    @NotBlank String customerName,
    @NotEmpty List<OrderItemRequest> items
) {}

public record OrderItemRequest(
    @NotNull Long productId,
    @Min(1) int quantity
) {}
```

### Response DTO

```java
public record OrderResponse(
    Long id,
    String customerEmail,
    List<OrderItemResponse> items,
    OrderStatus status,
    BigDecimal totalAmount,
    Instant createdAt
) {}
```

### Mapper (using MapStruct)

```java
@Mapper(componentModel = "spring")
interface OrderMapper {

    @Mapping(target = "id", ignore = true)
    @Mapping(target = "status", constant = "CREATED")
    @Mapping(target = "createdAt", expression = "java(java.time.Instant.now())")
    Order toEntity(CreateOrderRequest request);

    OrderResponse toResponse(Order order);

    List<OrderResponse> toResponseList(List<Order> orders);
}
```

## Exception Handling

```java
@ControllerAdvice
class GlobalExceptionHandler {

    @ExceptionHandler(NotFoundException.class)
    ResponseEntity<ErrorResponse> handleNotFound(NotFoundException e) {
        return ResponseEntity.status(HttpStatus.NOT_FOUND)
            .body(new ErrorResponse("NOT_FOUND", e.getMessage()));
    }

    @ExceptionHandler(BusinessException.class)
    ResponseEntity<ErrorResponse> handleBusiness(BusinessException e) {
        return ResponseEntity.status(HttpStatus.UNPROCESSABLE_ENTITY)
            .body(new ErrorResponse("BUSINESS_ERROR", e.getMessage()));
    }

    @ExceptionHandler(MethodArgumentNotValidException.class)
    ResponseEntity<ErrorResponse> handleValidation(MethodArgumentNotValidException e) {
        List<String> errors = e.getBindingResult().getFieldErrors().stream()
            .map(error -> error.getField() + ": " + error.getDefaultMessage())
            .toList();
        return ResponseEntity.status(HttpStatus.BAD_REQUEST)
            .body(new ErrorResponse("VALIDATION_ERROR", String.join(", ", errors)));
    }
}

public record ErrorResponse(String code, String message) {}
```

## Testing Conventions

See [references/testing.md](references/testing.md) for detailed testing patterns.

### Unit Test Pattern

```java
@ExtendWith(MockitoExtension.class)
class OrderServiceTest {

    @Mock
    private OrderRepository orderRepository;

    @Mock
    private OrderMapper orderMapper;

    @InjectMocks
    private OrderService orderService;

    @Test
    void createOrder_shouldReturnOrderResponse() {
        // Given
        var request = new CreateOrderRequest("test@email.com", "John", List.of());
        var order = new Order();
        var expected = new OrderResponse(1L, "test@email.com", List.of(), OrderStatus.CREATED, null, null);

        when(orderMapper.toEntity(request)).thenReturn(order);
        when(orderRepository.save(order)).thenReturn(order);
        when(orderMapper.toResponse(order)).thenReturn(expected);

        // When
        var result = orderService.createOrder(request);

        // Then
        assertThat(result).isEqualTo(expected);
    }
}
```

## Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Entity | Noun, singular | `Order`, `OrderItem` |
| Repository | Entity + Repository | `OrderRepository` |
| Service | Entity + Service | `OrderService` |
| Controller | Entity + Controller | `OrderController` |
| Request DTO | Action + Entity + Request | `CreateOrderRequest` |
| Response DTO | Entity + Response | `OrderResponse` |
| Method (service) | Verb + Noun | `createOrder`, `findOrderByEmail` |
| Method (controller) | Verb + Noun | `createOrder`, `getOrder` |
| Exception | Descriptive noun | `OrderNotFoundException` |

## References

- **Testing patterns**: See [references/testing.md](references/testing.md) for unit, integration, and contract testing
- **API design**: See [references/api-design.md](references/api-design.md) for REST conventions and pagination
- **Configuration**: See [references/configuration.md](references/configuration.md) for Spring Boot config patterns
