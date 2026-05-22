---
name: java-spring-service
description: |
  Creates complete Spring Boot services following best practices and layered architecture. Use when building REST APIs, creating Spring services, setting up controllers, implementing repositories, adding Spring Boot applications, configuring dependency injection, creating RESTful endpoints, adding OpenAPI documentation, or building microservices. Works with Spring Boot 2.x and 3.x, Spring Data JPA, Spring Web, and Spring Security.
allowed-tools:
  - Read
  - Write
  - Glob
  - Bash
---

# Spring Boot Service Generator

## Table of Contents

- [Purpose](#purpose)
- [When to Use](#when-to-use)
- [Quick Start](#quick-start)
- [Instructions](#instructions)
- [Examples](#examples)
- [Requirements](#requirements)
- [Best Practices Checklist](#best-practices-checklist)
- [Output Format](#output-format)
- [Error Handling](#error-handling)

## Purpose

Generates complete, production-ready Spring Boot services following industry best practices: proper layered architecture (Controller/Service/Repository), dependency injection, exception handling with @ControllerAdvice, OpenAPI/Swagger documentation, configuration management, and comprehensive logging.

## When to Use

Use this skill when you need to:
- Create new Spring Boot REST APIs
- Generate CRUD services with JPA repositories
- Set up layered architecture (Controller/Service/Repository)
- Implement RESTful endpoints with proper HTTP methods
- Add OpenAPI/Swagger documentation
- Configure Spring Data JPA entities and repositories
- Create DTOs and mappers for API contracts
- Implement global exception handling with @ControllerAdvice
- Set up dependency injection with constructor injection
- Generate complete Spring Boot microservices
- Add pagination and sorting to endpoints
- Configure database migrations with Flyway
- Bootstrap new Spring Boot projects with best practices

## Quick Start
Describe the service you need and get a complete implementation:

```bash
# Create a complete CRUD service
Create a Spring Boot service for User management with CRUD operations

# Create a specific endpoint
Create a Spring Boot REST endpoint for processing orders
```

## Instructions

### Step 1: Understand Service Requirements
Identify what needs to be created:
- Entity/domain model (JPA entity)
- Repository layer (Spring Data)
- Service layer (business logic)
- Controller layer (REST API)
- DTOs (request/response objects)
- Exception handling
- Configuration
- API documentation

### Step 2: Generate Domain Model (Entity)
Create JPA entity with proper annotations:

```java
@Entity
@Table(name = "users")
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class User {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, length = 100)
    private String name;

    @Column(nullable = false, unique = true, length = 255)
    private String email;

    @Column(name = "phone_number", length = 20)
    private String phoneNumber;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private UserStatus status;

    @CreatedDate
    @Column(nullable = false, updatable = false)
    private LocalDateTime createdAt;

    @LastModifiedDate
    @Column(nullable = false)
    private LocalDateTime updatedAt;

    @Version
    private Long version;
}
```

**Key Annotations:**
- @Entity, @Table - JPA entity mapping
- @Id, @GeneratedValue - Primary key generation
- @Column - Column constraints and naming
- @Enumerated - Enum mapping
- @CreatedDate, @LastModifiedDate - Audit fields
- @Version - Optimistic locking
- @Data (Lombok) - Getters, setters, toString, equals, hashCode
- @Builder (Lombok) - Builder pattern

### Step 3: Create DTOs (Data Transfer Objects)
Separate internal models from API contracts:

```java
// Request DTO
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class CreateUserRequest {
    @NotBlank(message = "Name is required")
    @Size(min = 2, max = 100, message = "Name must be between 2 and 100 characters")
    private String name;

    @NotBlank(message = "Email is required")
    @Email(message = "Email must be valid")
    private String email;

    @Pattern(regexp = "^\\+?[1-9]\\d{1,14}$",
        message = "Phone number must be in E.164 format")
    private String phoneNumber;
}

// Response DTO
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class UserResponse {
    private Long id;
    private String name;
    private String email;
    private String phoneNumber;
    private UserStatus status;
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;
}

// Mapper
@Component
public class UserMapper {
    public User toEntity(CreateUserRequest request) {
        return User.builder()
            .name(request.getName())
            .email(request.getEmail())
            .phoneNumber(request.getPhoneNumber())
            .status(UserStatus.ACTIVE)
            .build();
    }

    public UserResponse toResponse(User user) {
        return UserResponse.builder()
            .id(user.getId())
            .name(user.getName())
            .email(user.getEmail())
            .phoneNumber(user.getPhoneNumber())
            .status(user.getStatus())
            .createdAt(user.getCreatedAt())
            .updatedAt(user.getUpdatedAt())
            .build();
    }
}
```

### Step 4: Create Repository Layer
Use Spring Data JPA for data access:

```java
@Repository
public interface UserRepository extends JpaRepository<User, Long> {

    Optional<User> findByEmail(String email);

    List<User> findByStatus(UserStatus status);

    @Query("SELECT u FROM User u WHERE u.name LIKE %:searchTerm% OR u.email LIKE %:searchTerm%")
    Page<User> searchUsers(@Param("searchTerm") String searchTerm, Pageable pageable);

    boolean existsByEmail(String email);

    @Modifying
    @Query("UPDATE User u SET u.status = :status WHERE u.id = :id")
    int updateUserStatus(@Param("id") Long id, @Param("status") UserStatus status);
}
```

**Key Features:**
- Extends JpaRepository for CRUD operations
- Custom query methods (findByEmail, findByStatus)
- @Query for complex queries
- Pagination support with Pageable
- @Modifying for update/delete queries

### Step 5: Create Service Layer
Implement business logic with transactions:

```java
@Service
@RequiredArgsConstructor
@Slf4j
public class UserService {
    private final UserRepository userRepository;
    private final UserMapper userMapper;
    private final ApplicationEventPublisher eventPublisher;

    @Transactional(readOnly = true)
    public UserResponse getUserById(Long id) {
        log.debug("Fetching user with id: {}", id);
        User user = userRepository.findById(id)
            .orElseThrow(() -> new UserNotFoundException(id));
        return userMapper.toResponse(user);
    }

    @Transactional(readOnly = true)
    public Page<UserResponse> getAllUsers(Pageable pageable) {
        log.debug("Fetching all users: page={}, size={}",
            pageable.getPageNumber(), pageable.getPageSize());
        return userRepository.findAll(pageable)
            .map(userMapper::toResponse);
    }

    @Transactional
    public UserResponse createUser(CreateUserRequest request) {
        log.info("Creating user: email={}", request.getEmail());

        if (userRepository.existsByEmail(request.getEmail())) {
            throw new DuplicateEmailException(request.getEmail());
        }

        User user = userMapper.toEntity(request);
        User savedUser = userRepository.save(user);

        eventPublisher.publishEvent(new UserCreatedEvent(savedUser));

        log.info("User created successfully: id={}", savedUser.getId());
        return userMapper.toResponse(savedUser);
    }

    @Transactional
    public UserResponse updateUser(Long id, UpdateUserRequest request) {
        log.info("Updating user: id={}", id);

        User user = userRepository.findById(id)
            .orElseThrow(() -> new UserNotFoundException(id));

        updateUserFields(user, request);
        User updatedUser = userRepository.save(user);

        log.info("User updated successfully: id={}", id);
        return userMapper.toResponse(updatedUser);
    }

    @Transactional
    public void deleteUser(Long id) {
        log.info("Deleting user: id={}", id);

        if (!userRepository.existsById(id)) {
            throw new UserNotFoundException(id);
        }

        userRepository.deleteById(id);
        log.info("User deleted successfully: id={}", id);
    }

    private void updateUserFields(User user, UpdateUserRequest request) {
        if (request.getName() != null) {
            user.setName(request.getName());
        }
        if (request.getPhoneNumber() != null) {
            user.setPhoneNumber(request.getPhoneNumber());
        }
    }
}
```

**Best Practices:**
- @Transactional for database operations
- readOnly = true for read operations (performance)
- Comprehensive logging with SLF4J
- Event publishing for decoupled architecture
- Proper exception handling
- Field-by-field updates for PATCH operations

### Step 6: Create Controller Layer
Expose REST API endpoints:

```java
@RestController
@RequestMapping("/api/v1/users")
@RequiredArgsConstructor
@Validated
@Tag(name = "User Management", description = "APIs for managing users")
public class UserController {
    private final UserService userService;

    @GetMapping("/{id}")
    @Operation(summary = "Get user by ID", description = "Retrieves a user by their unique identifier")
    @ApiResponses({
        @ApiResponse(responseCode = "200", description = "User found"),
        @ApiResponse(responseCode = "404", description = "User not found")
    })
    public ResponseEntity<UserResponse> getUser(
            @PathVariable @Positive Long id) {
        UserResponse user = userService.getUserById(id);
        return ResponseEntity.ok(user);
    }

    @GetMapping
    @Operation(summary = "Get all users", description = "Retrieves a paginated list of users")
    public ResponseEntity<Page<UserResponse>> getAllUsers(
            @RequestParam(defaultValue = "0") @Min(0) int page,
            @RequestParam(defaultValue = "20") @Min(1) @Max(100) int size,
            @RequestParam(defaultValue = "id") String sortBy,
            @RequestParam(defaultValue = "ASC") Sort.Direction direction) {

        Pageable pageable = PageRequest.of(page, size, Sort.by(direction, sortBy));
        Page<UserResponse> users = userService.getAllUsers(pageable);
        return ResponseEntity.ok(users);
    }

    @PostMapping
    @Operation(summary = "Create user", description = "Creates a new user")
    @ApiResponses({
        @ApiResponse(responseCode = "201", description = "User created"),
        @ApiResponse(responseCode = "400", description = "Invalid request"),
        @ApiResponse(responseCode = "409", description = "Email already exists")
    })
    public ResponseEntity<UserResponse> createUser(
            @Valid @RequestBody CreateUserRequest request) {
        UserResponse createdUser = userService.createUser(request);
        URI location = ServletUriComponentsBuilder
            .fromCurrentRequest()
            .path("/{id}")
            .buildAndExpand(createdUser.getId())
            .toUri();
        return ResponseEntity.created(location).body(createdUser);
    }

    @PutMapping("/{id}")
    @Operation(summary = "Update user", description = "Updates an existing user")
    public ResponseEntity<UserResponse> updateUser(
            @PathVariable @Positive Long id,
            @Valid @RequestBody UpdateUserRequest request) {
        UserResponse updatedUser = userService.updateUser(id, request);
        return ResponseEntity.ok(updatedUser);
    }

    @DeleteMapping("/{id}")
    @Operation(summary = "Delete user", description = "Deletes a user by ID")
    @ApiResponse(responseCode = "204", description = "User deleted")
    public ResponseEntity<Void> deleteUser(@PathVariable @Positive Long id) {
        userService.deleteUser(id);
        return ResponseEntity.noContent().build();
    }
}
```

**Key Features:**
- @RestController for REST endpoints
- @RequestMapping for base path and versioning
- OpenAPI annotations (@Operation, @ApiResponse)
- Proper HTTP status codes (200, 201, 204, 404, etc.)
- Request validation (@Valid, @Positive, @Min, @Max)
- Pagination and sorting support
- Location header for created resources

### Step 7: Create Global Exception Handler
Centralized exception handling:

```java
@RestControllerAdvice
@Slf4j
public class GlobalExceptionHandler {

    @ExceptionHandler(UserNotFoundException.class)
    public ResponseEntity<ErrorResponse> handleUserNotFound(
            UserNotFoundException ex, WebRequest request) {
        log.error("User not found: {}", ex.getMessage());
        ErrorResponse error = ErrorResponse.builder()
            .timestamp(LocalDateTime.now())
            .status(HttpStatus.NOT_FOUND.value())
            .error("Not Found")
            .message(ex.getMessage())
            .path(getRequestPath(request))
            .build();
        return ResponseEntity.status(HttpStatus.NOT_FOUND).body(error);
    }

    @ExceptionHandler(DuplicateEmailException.class)
    public ResponseEntity<ErrorResponse> handleDuplicateEmail(
            DuplicateEmailException ex, WebRequest request) {
        log.error("Duplicate email: {}", ex.getMessage());
        ErrorResponse error = ErrorResponse.builder()
            .timestamp(LocalDateTime.now())
            .status(HttpStatus.CONFLICT.value())
            .error("Conflict")
            .message(ex.getMessage())
            .path(getRequestPath(request))
            .build();
        return ResponseEntity.status(HttpStatus.CONFLICT).body(error);
    }

    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<ValidationErrorResponse> handleValidationErrors(
            MethodArgumentNotValidException ex, WebRequest request) {
        log.error("Validation failed: {}", ex.getMessage());

        Map<String, String> errors = ex.getBindingResult()
            .getFieldErrors()
            .stream()
            .collect(Collectors.toMap(
                FieldError::getField,
                error -> error.getDefaultMessage() != null
                    ? error.getDefaultMessage()
                    : "Invalid value"
            ));

        ValidationErrorResponse response = ValidationErrorResponse.builder()
            .timestamp(LocalDateTime.now())
            .status(HttpStatus.BAD_REQUEST.value())
            .error("Validation Failed")
            .message("Request validation failed")
            .path(getRequestPath(request))
            .errors(errors)
            .build();

        return ResponseEntity.badRequest().body(response);
    }

    @ExceptionHandler(Exception.class)
    public ResponseEntity<ErrorResponse> handleGenericException(
            Exception ex, WebRequest request) {
        log.error("Unexpected error occurred", ex);
        ErrorResponse error = ErrorResponse.builder()
            .timestamp(LocalDateTime.now())
            .status(HttpStatus.INTERNAL_SERVER_ERROR.value())
            .error("Internal Server Error")
            .message("An unexpected error occurred")
            .path(getRequestPath(request))
            .build();
        return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
            .body(error);
    }

    private String getRequestPath(WebRequest request) {
        return ((ServletWebRequest) request).getRequest().getRequestURI();
    }
}

@Data
@Builder
public class ErrorResponse {
    private LocalDateTime timestamp;
    private int status;
    private String error;
    private String message;
    private String path;
}

@Data
@Builder
public class ValidationErrorResponse extends ErrorResponse {
    private Map<String, String> errors;
}
```

### Step 8: Create Custom Exceptions
Domain-specific exceptions:

```java
public class UserNotFoundException extends RuntimeException {
    public UserNotFoundException(Long id) {
        super("User not found with ID: " + id);
    }
}

public class DuplicateEmailException extends RuntimeException {
    public DuplicateEmailException(String email) {
        super("User already exists with email: " + email);
    }
}
```

### Step 9: Add Configuration
Application configuration files:

**application.yml:**
```yaml
spring:
  application:
    name: user-service

  datasource:
    url: ${DATABASE_URL:jdbc:postgresql://localhost:5432/userdb}
    username: ${DATABASE_USERNAME:postgres}
    password: ${DATABASE_PASSWORD:password}
    driver-class-name: org.postgresql.Driver

  jpa:
    hibernate:
      ddl-auto: validate
    show-sql: false
    properties:
      hibernate:
        format_sql: true
        dialect: org.hibernate.dialect.PostgreSQLDialect
        jdbc:
          batch_size: 20
        order_inserts: true
        order_updates: true

  flyway:
    enabled: true
    locations: classpath:db/migration
    baseline-on-migrate: true

server:
  port: ${PORT:8080}
  error:
    include-message: always
    include-binding-errors: always

logging:
  level:
    root: INFO
    com.example.userservice: DEBUG
  pattern:
    console: "%d{yyyy-MM-dd HH:mm:ss} - %msg%n"

springdoc:
  api-docs:
    path: /api-docs
  swagger-ui:
    path: /swagger-ui.html
    enabled: true
```

**Java Config:**
```java
@Configuration
@EnableJpaAuditing
public class JpaConfig {
    // JPA auditing configuration
}

@Configuration
public class OpenApiConfig {
    @Bean
    public OpenAPI customOpenAPI() {
        return new OpenAPI()
            .info(new Info()
                .title("User Service API")
                .version("1.0")
                .description("API for managing users")
                .contact(new Contact()
                    .name("API Support")
                    .email("support@example.com")))
            .servers(List.of(
                new Server().url("http://localhost:8080")
                    .description("Development server")
            ));
    }
}
```

### Step 10: Add Database Migration
Flyway migration script:

**db/migration/V1__create_users_table.sql:**
```sql
CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    phone_number VARCHAR(20),
    status VARCHAR(20) NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    version BIGINT NOT NULL DEFAULT 0
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_status ON users(status);
```

## Examples

### Example 1: Complete CRUD Service

**Generated Structure:**
```
src/main/java/com/example/userservice/
├── UserServiceApplication.java
├── config/
│   ├── JpaConfig.java
│   └── OpenApiConfig.java
├── controller/
│   └── UserController.java
├── dto/
│   ├── CreateUserRequest.java
│   ├── UpdateUserRequest.java
│   └── UserResponse.java
├── entity/
│   └── User.java
├── exception/
│   ├── DuplicateEmailException.java
│   ├── UserNotFoundException.java
│   └── GlobalExceptionHandler.java
├── mapper/
│   └── UserMapper.java
├── repository/
│   └── UserRepository.java
└── service/
    └── UserService.java

src/main/resources/
├── application.yml
└── db/migration/
    └── V1__create_users_table.sql
```

### Example 2: Custom Service with Business Logic

**Requirement:** Order processing service with inventory validation

**Generated OrderService:**
```java
@Service
@RequiredArgsConstructor
@Slf4j
public class OrderService {
    private final OrderRepository orderRepository;
    private final InventoryService inventoryService;
    private final PaymentService paymentService;
    private final NotificationService notificationService;
    private final OrderMapper orderMapper;

    @Transactional
    public OrderResponse processOrder(CreateOrderRequest request) {
        log.info("Processing new order for customer: {}",
            request.getCustomerId());

        // Validate inventory
        validateInventoryAvailability(request.getItems());

        // Create order
        Order order = orderMapper.toEntity(request);
        order.setStatus(OrderStatus.PENDING);

        // Calculate total
        BigDecimal total = calculateOrderTotal(order);
        order.setTotal(total);

        // Save order
        Order savedOrder = orderRepository.save(order);

        // Process payment
        try {
            paymentService.processPayment(
                savedOrder.getId(),
                total,
                request.getPaymentDetails()
            );
            savedOrder.setStatus(OrderStatus.CONFIRMED);
        } catch (PaymentException e) {
            log.error("Payment failed for order: {}",
                savedOrder.getId(), e);
            savedOrder.setStatus(OrderStatus.PAYMENT_FAILED);
            throw e;
        }

        // Update inventory
        inventoryService.reserveItems(request.getItems());

        // Send confirmation
        notificationService.sendOrderConfirmation(savedOrder);

        log.info("Order processed successfully: orderId={}",
            savedOrder.getId());
        return orderMapper.toResponse(savedOrder);
    }

    private void validateInventoryAvailability(
            List<OrderItemRequest> items) {
        items.forEach(item -> {
            if (!inventoryService.isAvailable(
                    item.getProductId(),
                    item.getQuantity())) {
                throw new InsufficientInventoryException(
                    item.getProductId());
            }
        });
    }

    private BigDecimal calculateOrderTotal(Order order) {
        return order.getItems().stream()
            .map(item -> item.getPrice()
                .multiply(BigDecimal.valueOf(item.getQuantity())))
            .reduce(BigDecimal.ZERO, BigDecimal::add);
    }
}
```

## Requirements

### Dependencies (Maven pom.xml)

```xml
<parent>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-parent</artifactId>
    <version>3.2.0</version>
</parent>

<dependencies>
    <!-- Spring Boot Starters -->
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-web</artifactId>
    </dependency>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-data-jpa</artifactId>
    </dependency>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-validation</artifactId>
    </dependency>

    <!-- Database -->
    <dependency>
        <groupId>org.postgresql</groupId>
        <artifactId>postgresql</artifactId>
        <scope>runtime</scope>
    </dependency>
    <dependency>
        <groupId>org.flywaydb</groupId>
        <artifactId>flyway-core</artifactId>
    </dependency>

    <!-- OpenAPI/Swagger -->
    <dependency>
        <groupId>org.springdoc</groupId>
        <artifactId>springdoc-openapi-starter-webmvc-ui</artifactId>
        <version>2.3.0</version>
    </dependency>

    <!-- Lombok -->
    <dependency>
        <groupId>org.projectlombok</groupId>
        <artifactId>lombok</artifactId>
        <scope>provided</scope>
    </dependency>

    <!-- Testing -->
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-test</artifactId>
        <scope>test</scope>
    </dependency>
</dependencies>
```

### Running the Service

```bash
# Build
mvn clean package

# Run
java -jar target/user-service-1.0.0.jar

# Or with Maven
mvn spring-boot:run

# Access Swagger UI
open http://localhost:8080/swagger-ui.html

# Access API docs
curl http://localhost:8080/api-docs
```

## Best Practices Checklist

**Architecture:**
- [ ] Clear layer separation (Controller/Service/Repository)
- [ ] DTOs for API contracts (no entities in controllers)
- [ ] Dependency injection via constructor
- [ ] Single responsibility per class

**API Design:**
- [ ] RESTful endpoints with proper HTTP methods
- [ ] Correct HTTP status codes (200, 201, 204, 400, 404, etc.)
- [ ] API versioning (/api/v1/)
- [ ] Pagination for list endpoints
- [ ] Location header for POST requests

**Data Access:**
- [ ] @Transactional on service methods
- [ ] readOnly = true for read operations
- [ ] Proper exception handling (no empty catches)
- [ ] Database migrations with Flyway/Liquibase

**Validation:**
- [ ] Bean validation annotations (@NotNull, @Size, etc.)
- [ ] @Valid on request parameters
- [ ] Custom validators for complex rules
- [ ] Meaningful validation error messages

**Documentation:**
- [ ] OpenAPI/Swagger annotations
- [ ] API descriptions and examples
- [ ] README with setup instructions
- [ ] Code comments for complex logic

**Error Handling:**
- [ ] @RestControllerAdvice for global handling
- [ ] Custom exceptions for domain errors
- [ ] Consistent error response format
- [ ] Proper logging of errors

**Logging:**
- [ ] SLF4J with appropriate levels
- [ ] Structured logging (JSON in production)
- [ ] Log method entry/exit for important operations
- [ ] Log with context (IDs, user info)

**Security:**
- [ ] Input validation and sanitization
- [ ] No sensitive data in logs
- [ ] HTTPS in production
- [ ] Authentication/authorization if needed

## Output Format

When generating a Spring Boot service, provide:

1. **Project structure** with all files
2. **Complete code** for each layer
3. **Configuration files** (application.yml, pom.xml)
4. **Database migrations** (Flyway scripts)
5. **Setup instructions** for running the service
6. **API documentation** with example curl commands

Example output:
```markdown
## Generated Spring Boot Service: User Management

**Structure Created:**
- Entity: User
- Repository: UserRepository
- Service: UserService
- Controller: UserController
- DTOs: CreateUserRequest, UpdateUserRequest, UserResponse
- Exceptions: UserNotFoundException, DuplicateEmailException
- Global Exception Handler
- Configuration (JPA, OpenAPI)
- Database migration

**Endpoints:**
- GET /api/v1/users - List all users
- GET /api/v1/users/{id} - Get user by ID
- POST /api/v1/users - Create user
- PUT /api/v1/users/{id} - Update user
- DELETE /api/v1/users/{id} - Delete user

**Setup:**
1. Configure database in application.yml
2. Run: mvn spring-boot:run
3. Access Swagger UI: http://localhost:8080/swagger-ui.html

**Example Request:**
```bash
curl -X POST http://localhost:8080/api/v1/users \
  -H "Content-Type: application/json" \
  -d '{"name":"John Doe","email":"john@example.com"}'
```
```

## Error Handling

If service generation cannot be completed:

1. **Missing requirements:** Ask for entity details, fields, relationships
2. **Ambiguous business logic:** Request clarification on rules and validations
3. **Database type unclear:** Ask which database (PostgreSQL, MySQL, etc.)
4. **Spring version conflict:** Verify Spring Boot version requirements

Always provide complete, working code that follows Spring Boot best practices.
