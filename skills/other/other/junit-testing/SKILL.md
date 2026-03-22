---
name: junit-testing
description: >
  JUnit 5 testing patterns including annotations, Mockito mocking, Spring Boot test slices,
  MockMvc, Testcontainers integration, and parameterized tests. Use when the user is writing
  Java tests, setting up test infrastructure, mocking dependencies, testing Spring controllers,
  or running integration tests with real databases. Trigger on any mention of JUnit, Mockito,
  @SpringBootTest, MockMvc, Testcontainers, or Java testing.
---

# JUnit 5 Testing Patterns

Patterns for writing effective unit, integration, and slice tests in Java.

## When to Use
- User is writing JUnit 5 tests
- User needs to mock dependencies with Mockito
- User asks about Spring Boot test slices (@WebMvcTest, @DataJpaTest)
- User wants integration tests with real databases (Testcontainers)
- User needs parameterized tests for multiple inputs

## Core Patterns

### JUnit 5 Annotations and Lifecycle

```java
import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

class UserServiceTest {
    private UserService userService;
    private UserRepository userRepository;

    @BeforeEach
    void setUp() {
        userRepository = new InMemoryUserRepository();
        userService = new UserService(userRepository);
    }

    @Test
    @DisplayName("creates a user with valid input")
    void createsUserWithValidInput() {
        User result = userService.createUser(new CreateUserRequest("Alice", "alice@example.com"));
        assertAll(
            () -> assertNotNull(result.getId()),
            () -> assertEquals("Alice", result.getName()),
            () -> assertEquals("alice@example.com", result.getEmail())
        );
    }

    @Test
    @DisplayName("throws when email is already taken")
    void throwsWhenEmailTaken() {
        userRepository.save(new User("Bob", "bob@example.com"));
        assertThrows(ConflictException.class,
            () -> userService.createUser(new CreateUserRequest("Bob2", "bob@example.com")));
    }

    @Nested
    @DisplayName("when user exists")
    class WhenUserExists {
        private User existingUser;

        @BeforeEach
        void setUp() {
            existingUser = userRepository.save(new User("Alice", "alice@example.com"));
        }

        @Test
        void findsById() {
            Optional<User> found = userService.findById(existingUser.getId());
            assertTrue(found.isPresent());
            assertEquals("Alice", found.get().getName());
        }
    }
}
```

### Mockito -- Mocking Dependencies

Isolate the unit under test by mocking its collaborators.

```java
import org.junit.jupiter.api.*;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.*;
import org.mockito.junit.jupiter.MockitoExtension;
import static org.mockito.Mockito.*;
import static org.junit.jupiter.api.Assertions.*;

@ExtendWith(MockitoExtension.class)
class OrderServiceTest {
    @Mock private OrderRepository orderRepository;
    @Mock private PaymentGateway paymentGateway;
    @InjectMocks private OrderService orderService;

    @Test
    @DisplayName("places order and charges payment")
    void placesOrderAndChargesPayment() {
        var order = new Order("product-1", 2, 29_99L);
        when(orderRepository.save(any(Order.class))).thenReturn(order);
        when(paymentGateway.charge(anyLong())).thenReturn(new PaymentResult(true, "txn-123"));

        assertNotNull(orderService.placeOrder(order));
        verify(paymentGateway).charge(29_99L);
        verify(orderRepository).save(order);
    }

    @Test
    @DisplayName("rolls back order when payment fails")
    void rollsBackWhenPaymentFails() {
        when(paymentGateway.charge(anyLong())).thenReturn(new PaymentResult(false, null));
        assertThrows(PaymentFailedException.class,
            () -> orderService.placeOrder(new Order("product-1", 1, 50_00L)));
        verify(orderRepository, never()).save(any());
    }
}
```

### @WebMvcTest -- Controller Slice Tests

Test controllers in isolation without starting the full application context. Only the web layer is loaded.

```java
@WebMvcTest(UserController.class)
class UserControllerTest {
    @Autowired private MockMvc mockMvc;
    @MockBean private UserService userService;

    @Test
    @DisplayName("GET /api/v1/users/{id} returns user")
    void getUser() throws Exception {
        when(userService.findById("1"))
            .thenReturn(Optional.of(new UserResponse("1", "Alice", "alice@example.com")));

        mockMvc.perform(get("/api/v1/users/1"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.data.name").value("Alice"));
    }

    @Test
    @DisplayName("POST /api/v1/users validates request body")
    void validateCreateUser() throws Exception {
        mockMvc.perform(post("/api/v1/users")
                .contentType("application/json")
                .content("{\"name\":\"\",\"email\":\"not-an-email\"}"))
            .andExpect(status().isBadRequest());
    }
}
```

### Testcontainers -- Integration Tests with Real Databases

Spin up real database containers for integration tests. Tests are reliable and match production behavior.

```java
@SpringBootTest
@Testcontainers
class UserRepositoryIntegrationTest {
    @Container
    static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:16-alpine")
        .withDatabaseName("testdb").withUsername("test").withPassword("test");

    @DynamicPropertySource
    static void configureProperties(DynamicPropertyRegistry registry) {
        registry.add("spring.datasource.url", postgres::getJdbcUrl);
        registry.add("spring.datasource.username", postgres::getUsername);
        registry.add("spring.datasource.password", postgres::getPassword);
    }

    @Autowired private UserRepository userRepository;

    @Test
    @DisplayName("persists and retrieves a user")
    void persistsAndRetrieves() {
        User saved = userRepository.save(new User("Alice", "alice@example.com"));
        Optional<User> found = userRepository.findById(saved.getId());
        assertTrue(found.isPresent());
        assertEquals("Alice", found.get().getName());
    }
}
```

### Parameterized Tests

Run the same test logic with different inputs. Reduces duplication.

```java
class EmailValidatorTest {
    private final EmailValidator validator = new EmailValidator();

    @ParameterizedTest
    @CsvSource({"alice@example.com, true", "bob@test.org, true", "invalid, false", "@no-local.com, false"})
    void validatesEmail(String email, boolean expected) {
        assertEquals(expected, validator.isValid(email));
    }

    @ParameterizedTest
    @NullAndEmptySource
    @ValueSource(strings = {"   ", "\t"})
    void rejectsBlankEmails(String email) {
        assertFalse(validator.isValid(email));
    }

    @ParameterizedTest
    @MethodSource("validEmailProvider")
    void acceptsValidEmails(String email) { assertTrue(validator.isValid(email)); }

    static Stream<String> validEmailProvider() {
        return Stream.of("a@b.com", "user+tag@domain.co", "first.last@sub.domain.org");
    }
}
```

## Anti-Patterns

- **Testing implementation details** -- Verifying private method calls or internal state. Test behavior (inputs and outputs), not how the code achieves the result.
- **Overusing @SpringBootTest** -- Loads the entire application context. Slow. Use slice annotations (@WebMvcTest, @DataJpaTest) to load only what you need.
- **Not using @ExtendWith(MockitoExtension.class)** -- Forgetting this means @Mock and @InjectMocks annotations are silently ignored, leading to NullPointerException.
- **Sharing mutable state between tests** -- Tests must be independent. Use @BeforeEach to reset state. Never rely on test execution order.
- **Mocking everything including the class under test** -- Only mock collaborators. The class under test should use its real implementation.

## Quick Reference

| Category | Key APIs |
|----------|----------|
| Lifecycle | `@BeforeEach`, `@AfterEach`, `@BeforeAll`, `@AfterAll`, `@Nested` |
| Assertions | `assertEquals`, `assertTrue`, `assertThrows`, `assertAll`, `assertTimeout` |
| Mockito | `when().thenReturn()`, `verify()`, `any()`, `@Mock`, `@InjectMocks` |
| Slices | `@WebMvcTest` (controllers), `@DataJpaTest` (JPA), `@SpringBootTest` (full) |
| Parameterized | `@CsvSource`, `@ValueSource`, `@MethodSource`, `@NullAndEmptySource` |
