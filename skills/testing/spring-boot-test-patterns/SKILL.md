---
name: spring-boot-test-patterns
description: Comprehensive testing patterns for Spring Boot applications including unit, integration, slice, and container-based testing with JUnit 5, Mockito, Testcontainers, and performance optimization. Use when implementing robust test suites for Spring Boot applications.
category: testing
tags: [spring-boot, java, testing, junit5, mockito, testcontainers, integration-testing, unit-testing, test-slices]
version: 1.5.0
language: java
license: Complete terms in LICENSE.txt
allowed-tools: Read, Write, Bash
---

# Spring Boot Testing Patterns

## Overview

This skill provides comprehensive guidance for writing robust test suites for Spring Boot applications. It covers unit testing with Mockito, integration testing with Testcontainers, performance-optimized slice testing patterns, and best practices for maintaining fast feedback loops.

## When to Use This Skill

Use this skill when:
- Writing unit tests for services, repositories, or utilities
- Implementing integration tests with real databases using Testcontainers
- Setting up performance-optimized test slices (@DataJpaTest, @WebMvcTest)
- Configuring Spring Boot 3.5+ @ServiceConnection for container management
- Testing REST APIs with MockMvc, TestRestTemplate, or WebTestClient
- Optimizing test performance through context caching and container reuse
- Setting up CI/CD pipelines for integration tests
- Implementing comprehensive test strategies for monolithic or microservices applications

## Core Concepts

### Test Architecture Philosophy

Spring Boot testing follows a layered approach with distinct test types:

**1. Unit Tests**
- Fast, isolated tests without Spring context
- Use Mockito for dependency injection
- Focus on business logic validation
- Target completion time: < 50ms per test

**2. Slice Tests**
- Minimal Spring context loading for specific layers
- Use @DataJpaTest for repository tests
- Use @WebMvcTest for controller tests
- Use @WebFluxTest for reactive controller tests
- Target completion time: < 100ms per test

**3. Integration Tests**
- Full Spring context with real dependencies
- Use @SpringBootTest with @ServiceConnection containers
- Test complete application flows
- Target completion time: < 500ms per test

### Key Testing Annotations

**Spring Boot Test Annotations:**
- `@SpringBootTest`: Load full application context (use sparingly)
- `@DataJpaTest`: Load only JPA components (repositories, entities)
- `@WebMvcTest`: Load only MVC layer (controllers, @ControllerAdvice)
- `@WebFluxTest`: Load only WebFlux layer (reactive controllers)
- `@JsonTest`: Load only JSON serialization components

**Testcontainer Annotations:**
- `@ServiceConnection`: Wire Testcontainer to Spring Boot test (Spring Boot 3.5+)
- `@DynamicPropertySource`: Register dynamic properties at runtime
- `@Testcontainers`: Enable Testcontainers lifecycle management

## Dependencies

### Maven Dependencies

```xml
<dependencies>
    <!-- Spring Boot Test Starter -->
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-test</artifactId>
        <scope>test</scope>
    </dependency>

    <!-- Testcontainers -->
    <dependency>
        <groupId>org.testcontainers</groupId>
        <artifactId>junit-jupiter</artifactId>
        <version>1.19.0</version>
        <scope>test</scope>
    </dependency>
    <dependency>
        <groupId>org.testcontainers</groupId>
        <artifactId>postgresql</artifactId>
        <version>1.19.0</version>
        <scope>test</scope>
    </dependency>

    <!-- Additional Testing Dependencies -->
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-data-jpa</artifactId>
    </dependency>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-web</artifactId>
    </dependency>
</dependencies>
```

### Gradle Dependencies

```kotlin
dependencies {
    // Spring Boot Test Starter
    testImplementation("org.springframework.boot:spring-boot-starter-test")

    // Testcontainers
    testImplementation("org.testcontainers:junit-jupiter:1.19.0")
    testImplementation("org.testcontainers:postgresql:1.19.0")

    // Additional Dependencies
    implementation("org.springframework.boot:spring-boot-starter-data-jpa")
    implementation("org.springframework.boot:spring-boot-starter-web")
}
```

## Instructions

### Unit Testing Pattern

Test business logic with mocked dependencies:

```java
class UserServiceTest {

    @Mock
    private UserRepository userRepository;

    @InjectMocks
    private UserService userService;

    @BeforeEach
    void setUp() {
        MockitoAnnotations.openMocks(this);
    }

    @Test
    void shouldFindUserByIdWhenExists() {
        // Arrange
        Long userId = 1L;
        User user = new User();
        user.setId(userId);
        user.setEmail("test@example.com");

        when(userRepository.findById(userId)).thenReturn(Optional.of(user));

        // Act
        Optional<User> result = userService.findById(userId);

        // Assert
        assertThat(result).isPresent();
        assertThat(result.get().getEmail()).isEqualTo("test@example.com");
        verify(userRepository, times(1)).findById(userId);
    }
}
```

### Slice Testing Pattern

Use focused test slices for specific layers:

```java
// Repository test with minimal context
@DataJpaTest
@AutoConfigureTestDatabase(replace = AutoConfigureTestDatabase.Replace.NONE)
@TestContainerConfig
public class UserRepositoryIntegrationTest {

    @Autowired
    private UserRepository userRepository;

    @Test
    void shouldSaveAndRetrieveUserFromDatabase() {
        // Arrange
        User user = new User();
        user.setEmail("test@example.com");
        user.setName("Test User");

        // Act
        User saved = userRepository.save(user);
        userRepository.flush();

        Optional<User> retrieved = userRepository.findByEmail("test@example.com");

        // Assert
        assertThat(retrieved).isPresent();
        assertThat(retrieved.get().getName()).isEqualTo("Test User");
    }
}
```

### REST API Testing Pattern

Test controllers with MockMvc for faster execution:

```java
@SpringBootTest
@AutoConfigureMockMvc
@Transactional
public class UserControllerIntegrationTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private ObjectMapper objectMapper;

    @Autowired
    private UserService userService;

    @Test
    void shouldCreateUserAndReturn201() throws Exception {
        User user = new User();
        user.setEmail("newuser@example.com");
        user.setName("New User");

        mockMvc.perform(post("/api/users")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(user)))
            .andExpect(status().isCreated())
            .andExpect(jsonPath("$.id").exists())
            .andExpect(jsonPath("$.email").value("newuser@example.com"))
            .andExpect(jsonPath("$.name").value("New User"));
    }
}
```

### Testcontainers with @ServiceConnection

Configure containers with Spring Boot 3.5+:

```java
@TestConfiguration
public class TestContainerConfig {

    @Bean
    @ServiceConnection
    public PostgreSQLContainer<?> postgresContainer() {
        return new PostgreSQLContainer<>(DockerImageName.parse("postgres:16-alpine"))
            .withDatabaseName("testdb")
            .withUsername("test")
            .withPassword("test");
    }
}
```

## Examples

### Basic Unit Test

```java
@Test
void shouldCalculateTotalPrice() {
    // Arrange
    OrderItem item1 = new OrderItem();
    item1.setPrice(10.0);
    item1.setQuantity(2);

    OrderItem item2 = new OrderItem();
    item2.setPrice(15.0);
    item2.setQuantity(1);

    List<OrderItem> items = List.of(item1, item2);

    // Act
    double total = orderService.calculateTotal(items);

    // Assert
    assertThat(total).isEqualTo(35.0);
}
```

### Integration Test with Testcontainers

```java
@SpringBootTest
@TestContainerConfig
public class OrderServiceIntegrationTest {

    @Autowired
    private OrderService orderService;

    @Autowired
    private UserRepository userRepository;

    @MockBean
    private PaymentService paymentService;

    @Test
    void shouldCreateOrderWithRealDatabase() {
        // Arrange
        User user = new User();
        user.setEmail("customer@example.com");
        user.setName("John Doe");
        User savedUser = userRepository.save(user);

        OrderRequest request = new OrderRequest();
        request.setUserId(savedUser.getId());
        request.setItems(List.of(
            new OrderItemRequest(1L, 2),
            new OrderItemRequest(2L, 1)
        ));

        when(paymentService.processPayment(any())).thenReturn(true);

        // Act
        OrderResponse response = orderService.createOrder(request);

        // Assert
        assertThat(response.getOrderId()).isNotNull();
        assertThat(response.getStatus()).isEqualTo("COMPLETED");
        verify(paymentService, times(1)).processPayment(any());
    }
}
```

### Reactive Test Pattern

```java
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
@AutoConfigureWebTestClient
public class ReactiveUserControllerIntegrationTest {

    @Autowired
    private WebTestClient webTestClient;

    @Test
    void shouldReturnUserAsJsonReactive() {
        // Arrange
        User user = new User();
        user.setEmail("reactive@example.com");
        user.setName("Reactive User");

        // Act & Assert
        webTestClient.get()
            .uri("/api/users/1")
            .exchange()
            .expectStatus().isOk()
            .expectBody()
            .jsonPath("$.email").isEqualTo("reactive@example.com")
            .jsonPath("$.name").isEqualTo("Reactive User");
    }
}
```

## Best Practices

### 1. Choose the Right Test Type

Select appropriate test annotations based on scope:

```java
// Use @DataJpaTest for repository-only tests (fastest)
@DataJpaTest
public class UserRepositoryTest { }

// Use @WebMvcTest for controller-only tests
@WebMvcTest(UserController.class)
public class UserControllerTest { }

// Use @SpringBootTest only for full integration testing
@SpringBootTest
public class UserServiceFullIntegrationTest { }
```

### 2. Use @ServiceConnection for Container Management

Prefer `@ServiceConnection` over manual `@DynamicPropertySource` for cleaner code:

```java
// Good - Spring Boot 3.5+
@TestConfiguration
public class TestConfig {
    @Bean
    @ServiceConnection
    public PostgreSQLContainer<?> postgres() {
        return new PostgreSQLContainer<>(DockerImageName.parse("postgres:16-alpine"));
    }
}
```

### 3. Keep Tests Deterministic

Always initialize test data explicitly:

```java
// Good - Explicit setup
@BeforeEach
void setUp() {
    userRepository.deleteAll();
    User user = new User();
    user.setEmail("test@example.com");
    userRepository.save(user);
}

// Avoid - Depending on other tests
@Test
void testUserExists() {
    // Assumes previous test created a user
    Optional<User> user = userRepository.findByEmail("test@example.com");
    assertThat(user).isPresent();
}
```

### 4. Use Meaningful Assertions

Leverage AssertJ for readable, fluent assertions:

```java
// Good - Clear, readable assertions
assertThat(user.getEmail())
    .isEqualTo("test@example.com");

assertThat(users)
    .hasSize(3)
    .contains(expectedUser);

// Avoid - JUnit assertions
assertEquals("test@example.com", user.getEmail());
assertTrue(users.size() == 3);
```

### 5. Organize Tests by Layer

Group related tests in separate classes to optimize context caching:

```java
// Repository tests (uses @DataJpaTest)
public class UserRepositoryTest { }

// Controller tests (uses @WebMvcTest)
public class UserControllerTest { }

// Service tests (uses mocks, no context)
public class UserServiceTest { }

// Full integration tests (uses @SpringBootTest)
public class UserFullIntegrationTest { }
```

## Performance Optimization

### Context Caching Strategy

Maximize Spring context caching by grouping tests with similar configurations:

```java
// Group repository tests with same configuration
@DataJpaTest
@AutoConfigureTestDatabase(replace = AutoConfigureTestDatabase.Replace.NONE)
@TestContainerConfig
@TestPropertySource(properties = "spring.datasource.url=jdbc:postgresql:testdb")
public class UserRepositoryTest { }

// Group controller tests with same configuration
@WebMvcTest(UserController.class)
@AutoConfigureMockMvc
public class UserControllerTest { }
```

### Container Reuse Strategy

Reuse Testcontainers at JVM level for better performance:

```java
@Testcontainers
public class ContainerConfig {
    static final PostgreSQLContainer<?> POSTGRES = new PostgreSQLContainer<>(
        DockerImageName.parse("postgres:16-alpine"))
        .withDatabaseName("testdb")
        .withUsername("test")
        .withPassword("test");

    @BeforeAll
    static void startAll() {
        POSTGRES.start();
    }

    @AfterAll
    static void stopAll() {
        POSTGRES.stop();
    }
}
```

## Test Execution

### Maven Test Execution

```bash
# Run all tests
./mvnw test

# Run specific test class
./mvnw test -Dtest=UserServiceTest

# Run integration tests only
./mvnw test -Dintegration-test=true

# Run tests with coverage
./mvnw clean jacoco:prepare-agent test jacoco:report
```

### Gradle Test Execution

```bash
# Run all tests
./gradlew test

# Run specific test class
./gradlew test --tests UserServiceTest

# Run integration tests only
./gradlew integrationTest

# Run tests with coverage
./gradlew test jacocoTestReport
```

## CI/CD Configuration

### GitHub Actions Example

```yaml
name: Spring Boot Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:16-alpine
        env:
          POSTGRES_PASSWORD: test
          POSTGRES_USER: test
          POSTGRES_DB: testdb
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
    - uses: actions/checkout@v3

    - name: Set up JDK 17
      uses: actions/setup-java@v3
      with:
        java-version: '17'
        distribution: 'temurin'

    - name: Cache Maven dependencies
      uses: actions/cache@v3
      with:
        path: ~/.m2/repository
        key: ${{ runner.os }}-maven-${{ hashFiles('**/pom.xml') }}
        restore-keys: ${{ runner.os }}-maven-

    - name: Run tests
      run: ./mvnw test -Dspring.profiles.active=test
```

### Docker Compose for Local Testing

```yaml
version: '3.8'
services:
  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: testdb
      POSTGRES_USER: test
      POSTGRES_PASSWORD: test
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

## References

For detailed information, refer to the following resources:

- [API Reference](./references/api-reference.md) - Complete test annotations and utilities
- [Best Practices](./references/best-practices.md) - Testing patterns and optimization
- [Workflow Patterns](./references/workflow-patterns.md) - Complete integration test examples

## Related Skills

- **spring-boot-dependency-injection** - Unit testing patterns with constructor injection
- **spring-boot-rest-api-standards** - REST API patterns to test
- **spring-boot-crud-patterns** - CRUD patterns to test
- **unit-test-service-layer** - Advanced service layer testing techniques

## Performance Targets

- **Unit tests**: < 50ms per test
- **Slice tests**: < 100ms per test
- **Integration tests**: < 500ms per test
- **Maximize context caching** by grouping tests with same configuration
- **Reuse Testcontainers** at JVM level where possible

## Key Principles

1. Use test slices for focused, fast tests
2. Prefer @ServiceConnection on Spring Boot 3.5+
3. Keep tests deterministic with explicit setup
4. Mock external dependencies, use real databases
5. Avoid @DirtiesContext unless absolutely necessary
6. Organize tests by layer to optimize context reuse

This skill enables building comprehensive test suites that validate Spring Boot applications reliably while maintaining fast feedback loops for development.