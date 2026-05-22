---
name: java-test-engineer
description: "This skill should be used when the user asks to 'write unit tests', 'add integration tests', 'create property-based tests', 'fix failing test', 'improve test coverage', 'reduce mocking', 'test this class', 'add jqwik tests', or needs guidance on JUnit 5, Mockito, Spring Boot Test, property testing with jqwik, test patterns, mocking strategies, or test anti-patterns. Covers Java/Spring Boot testing best practices."
---

# Java Test Engineer Skill

Expert guidance for writing, reviewing, and fixing tests in Java/Spring Boot applications.

## Core Principles

### 1. Test Pyramid Strategy
- **Unit tests** (70%): Fast, isolated, no Spring context
- **Integration tests** (20%): Spring context, real dependencies where practical
- **E2E tests** (10%): Full system, use sparingly

### 2. Testability Over Mocking
Design code to be testable rather than relying on heavy mocking:
- Prefer constructor injection over field injection
- Extract pure functions from side-effectful code
- Use interfaces at boundaries, concrete classes internally
- Small, focused classes with single responsibility

### 3. Test Behavior, Not Implementation
- Test public API, not internal methods
- Avoid testing private methods directly
- Tests should survive refactoring if behavior unchanged

### 4. Property Tests > Example Tests (When Applicable)
Prefer property-based tests over example-based tests when:
- Testing pure functions with clear invariants
- Validating parsers, serializers, converters (round-trip)
- Business rules with mathematical properties
- Input validation with large input spaces

---

## Property-Based Testing (jqwik) - PREFERRED APPROACH

Property tests find edge cases you'd never think to write. Use them for any pure function or stateless logic.

### When to Use Property Tests
| Use Property Tests | Use Example Tests |
|-------------------|-------------------|
| Pure functions | Side effects (DB, HTTP) |
| Validation logic | Specific business scenarios |
| Parsers/serializers | Integration flows |
| Mathematical properties | UI interactions |
| Large input spaces | Small, enumerable cases |

### Maven Dependency
```xml
<dependency>
    <groupId>net.jqwik</groupId>
    <artifactId>jqwik</artifactId>
    <version>1.9.2</version>
    <scope>test</scope>
</dependency>
```

### Common Property Patterns

#### 1. Invariants - "This should always be true"
```java
@Property
void priceShouldNeverBeNegative(@ForAll @Positive int qty,
                                 @ForAll @Positive int unitPrice,
                                 @ForAll @IntRange(min = 0, max = 100) int discount) {
    var total = calculator.calculate(qty, unitPrice, discount);
    assertThat(total).isGreaterThanOrEqualTo(0);
}

@Property
void cprShouldAlwaysHave10Digits(@ForAll("validCprs") String cpr) {
    assertThat(cpr.replaceAll("-", "")).hasSize(10);
}
```

#### 2. Round-Trip / Symmetry - "Encode then decode = original"
```java
@Property
void serializeDeserializeShouldBeIdentity(@ForAll("users") User user) {
    var json = mapper.writeValueAsString(user);
    var restored = mapper.readValue(json, User.class);
    assertThat(restored).isEqualTo(user);
}

@Property
void encryptDecryptShouldBeIdentity(@ForAll String plaintext,
                                     @ForAll("keys") SecretKey key) {
    var encrypted = crypto.encrypt(plaintext, key);
    var decrypted = crypto.decrypt(encrypted, key);
    assertThat(decrypted).isEqualTo(plaintext);
}
```

#### 3. Idempotence - "Doing it twice = doing it once"
```java
@Property
void normalizeShouldBeIdempotent(@ForAll String input) {
    var once = normalizer.normalize(input);
    var twice = normalizer.normalize(once);
    assertThat(twice).isEqualTo(once);
}

@Property
void sortingTwiceShouldNotChange(@ForAll List<Integer> list) {
    var sorted = sort(list);
    var sortedAgain = sort(sorted);
    assertThat(sortedAgain).isEqualTo(sorted);
}
```

#### 4. Commutativity - "Order doesn't matter"
```java
@Property
void additionShouldBeCommutative(@ForAll int a, @ForAll int b) {
    assertThat(calculator.add(a, b)).isEqualTo(calculator.add(b, a));
}
```

#### 5. Test Oracle - "Compare with known-good implementation"
```java
@Property
void customSortShouldMatchJavaSort(@ForAll List<Integer> list) {
    var expected = new ArrayList<>(list);
    Collections.sort(expected);

    var actual = customSort.sort(list);
    assertThat(actual).isEqualTo(expected);
}
```

#### 6. Metamorphic - "Related inputs should have related outputs"
```java
@Property
void doublingInputShouldDoubleOutput(@ForAll @Positive int qty,
                                      @ForAll @Positive int price) {
    var single = calculator.total(qty, price);
    var doubled = calculator.total(qty * 2, price);
    assertThat(doubled).isEqualTo(single * 2);
}
```

### Custom Arbitraries

For detailed patterns on custom arbitraries, constraining generation, statistics, and combining with JUnit 5, see: **[references/jqwik-arbitraries.md](references/jqwik-arbitraries.md)**

Quick example:
```java
@Provide
Arbitrary<Order> orders() {
    return Combinators.combine(
        Arbitraries.longs().greaterOrEqual(1),
        Arbitraries.of(OrderStatus.class),
        Arbitraries.lists(orderItems()).ofMinSize(1).ofMaxSize(10)
    ).as(Order::new);
}
```

---

## Unit Testing Patterns

### JUnit 5 Structure
```java
@ExtendWith(MockitoExtension.class)
class ServiceTest {
    @Mock Repository repo;
    @InjectMocks Service service;

    @Test
    void shouldDoSomething_whenCondition() {
        // given
        var input = createInput();
        when(repo.find(any())).thenReturn(Optional.of(entity));

        // when
        var result = service.process(input);

        // then
        assertThat(result).isEqualTo(expected);
        verify(repo).save(any());
    }
}
```

### Naming Convention
```
methodName_shouldExpectedBehavior_whenCondition
```
Examples:
- `calculateTotal_shouldApplyDiscount_whenCustomerIsPremium`
- `validateCpr_shouldThrowException_whenFormatInvalid`

### AssertJ Over JUnit Assertions
```java
// Prefer
assertThat(result).hasSize(3).contains("a", "b");
assertThat(exception).isInstanceOf(ValidationException.class)
    .hasMessageContaining("invalid");

// Avoid
assertEquals(3, result.size());
assertTrue(result.contains("a"));
```

### Testing Exceptions
```java
@Test
void shouldThrowWhenInvalid() {
    assertThatThrownBy(() -> service.process(null))
        .isInstanceOf(IllegalArgumentException.class)
        .hasMessageContaining("must not be null");
}

// Or with JUnit 5
var ex = assertThrows(ValidationException.class,
    () -> service.validate(input));
assertThat(ex.getErrors()).hasSize(2);
```

### Parameterized Tests
```java
@ParameterizedTest
@CsvSource({
    "100, 10, 90",    // normal discount
    "50, 0, 50",      // no discount
    "200, 25, 150"    // max discount
})
void shouldCalculateDiscount(int price, int discount, int expected) {
    assertThat(calculator.apply(price, discount)).isEqualTo(expected);
}

@ParameterizedTest
@MethodSource("invalidInputs")
void shouldRejectInvalidInput(String input, String expectedError) {
    assertThatThrownBy(() -> validator.validate(input))
        .hasMessageContaining(expectedError);
}

static Stream<Arguments> invalidInputs() {
    return Stream.of(
        Arguments.of(null, "must not be null"),
        Arguments.of("", "must not be empty"),
        Arguments.of("abc", "must be numeric")
    );
}
```

### Testing Either/Result Types (dk.oister.util.Either)

When testing code that returns `Either<E, T>`:

```java
@Test
void shouldReturnRightOnSuccess() {
    Either<OrderError, Order> result = service.createOrder(validRequest);

    // Assert success case
    assertThat(result.isRight()).isTrue();
    assertThat(result.getRight()).satisfies(order -> {
        assertThat(order.status()).isEqualTo(PENDING);
        assertThat(order.total()).isEqualTo(Money.of(100));
    });
}

@Test
void shouldReturnLeftOnValidationFailure() {
    Either<OrderError, Order> result = service.createOrder(invalidRequest);

    // Assert failure case
    assertThat(result.isLeft()).isTrue();
    assertThat(result.getLeft()).isInstanceOf(ValidationError.class);
    assertThat(result.getLeft().message()).contains("invalid");
}

// Pattern matching with fold
@Test
void shouldHandleBothCases() {
    var result = service.processOrder(request);

    String message = result.fold(
        error -> "Failed: " + error.message(),
        order -> "Success: " + order.id()
    );

    assertThat(message).startsWith("Success:");
}
```

**Property tests for Either composition:**
```java
@Property
void flatMapShouldPropagateLeft(@ForAll("validOrders") Either<OrderError, Order> first) {
    // Left should short-circuit
    Either<OrderError, Order> left = Either.left(new OrderError("error"));
    Either<OrderError, Order> result = left.flatMap(o -> first);

    assertThat(result.isLeft()).isTrue();
    assertThat(result.getLeft().message()).isEqualTo("error");
}

@Property
void mapShouldPreserveRight(@ForAll("orders") Order order) {
    Either<OrderError, Order> right = Either.right(order);
    Either<OrderError, Money> mapped = right.map(Order::total);

    assertThat(mapped.isRight()).isTrue();
    assertThat(mapped.getRight()).isEqualTo(order.total());
}
```

---

## Mocking Best Practices

### When to Mock
- External services (HTTP clients, message queues)
- Time-dependent code (`Clock`)
- Randomness (`Random`, UUID generators)
- Database (only in unit tests)

### When NOT to Mock
- Value objects and DTOs
- Pure functions
- Your own code in integration tests
- Things you can use real instances of

### Mock Injection Patterns
```java
// Constructor injection - preferred
class Service {
    private final Repository repo;
    private final Clock clock;

    Service(Repository repo, Clock clock) {
        this.repo = repo;
        this.clock = clock;
    }
}

// In test
var clock = Clock.fixed(Instant.parse("2024-01-15T10:00:00Z"), ZoneId.UTC);
var service = new Service(mockRepo, clock);
```

### Verify Sparingly
```java
// Good: verify critical interactions
verify(emailService).send(any(Email.class));

// Bad: over-verification couples tests to implementation
verify(repo).findById(1L);
verify(mapper).toDto(any());
verify(validator).validate(any());
// These are implementation details
```

### Argument Captors
```java
@Captor ArgumentCaptor<Email> emailCaptor;

@Test
void shouldSendWelcomeEmail() {
    service.registerUser(user);

    verify(emailService).send(emailCaptor.capture());
    var email = emailCaptor.getValue();
    assertThat(email.getTo()).isEqualTo(user.getEmail());
    assertThat(email.getSubject()).contains("Welcome");
}
```

---

## Spring Boot Integration Tests

For detailed Spring Boot test configurations, MockMvc patterns, repository tests with Testcontainers, and security testing, see: **[references/spring-testing.md](references/spring-testing.md)**

Quick patterns:

```java
// Base test configuration (Spring Boot 3.4+)
@SpringBootTest
@ActiveProfiles("test")
@Transactional
abstract class BaseIntegrationTest {
    @Autowired protected MockMvc mockMvc;
    @MockitoBean protected ExternalService externalService;  // @MockBean deprecated in 3.4+
}

// Controller test with JWT
@WebMvcTest(UserController.class)
class UserControllerTest {
    @Test
    void shouldReturnUser() throws Exception {
        mockMvc.perform(get("/api/users/1")
                .with(jwt().authorities(new SimpleGrantedAuthority("ROLE_USER"))))
            .andExpect(status().isOk());
    }
}
```

---

## Async Testing Patterns

### CompletableFuture Testing
```java
@Test
void shouldCompleteWithinTimeout() {
    CompletableFuture<Order> future = service.processAsync(request);

    // Use assertj's completablefuture support
    assertThat(future)
        .succeedsWithin(Duration.ofSeconds(5))
        .satisfies(order -> assertThat(order.status()).isEqualTo(COMPLETED));
}

@Test
void shouldHandleAsyncFailure() {
    CompletableFuture<Order> future = service.processAsync(invalidRequest);

    assertThat(future)
        .failsWithin(Duration.ofSeconds(5))
        .withThrowableOfType(ExecutionException.class)
        .havingCause()
        .isInstanceOf(ValidationException.class);
}
```

### Awaitility for Polling Assertions
```java
// Maven: org.awaitility:awaitility:4.2.0

@Test
void shouldEventuallyUpdateStatus() {
    service.startAsyncProcess(orderId);

    await().atMost(Duration.ofSeconds(10))
        .pollInterval(Duration.ofMillis(500))
        .untilAsserted(() -> {
            var order = repo.findById(orderId).orElseThrow();
            assertThat(order.status()).isEqualTo(COMPLETED);
        });
}

@Test
void shouldPublishEventWithinTimeout() {
    service.processOrder(request);

    await().atMost(Duration.ofSeconds(5))
        .until(() -> eventCaptor.getEvents(), hasSize(1));

    assertThat(eventCaptor.getEvents().get(0))
        .isInstanceOf(OrderCreatedEvent.class);
}
```

### WebFlux Testing with WebTestClient
```java
@SpringBootTest(webEnvironment = WebEnvironment.RANDOM_PORT)
class ReactiveControllerTest {
    @Autowired WebTestClient webClient;

    @Test
    void shouldStreamOrders() {
        webClient.get().uri("/api/orders/stream")
            .accept(MediaType.TEXT_EVENT_STREAM)
            .exchange()
            .expectStatus().isOk()
            .expectBodyList(Order.class)
            .hasSize(3);
    }

    @Test
    void shouldHandleReactiveError() {
        webClient.get().uri("/api/orders/999")
            .exchange()
            .expectStatus().isNotFound()
            .expectBody()
            .jsonPath("$.error").isEqualTo("Order not found");
    }
}
```

---

## Test Data Builders

For complete builder and mother patterns, see: **[references/test-data-builders.md](references/test-data-builders.md)**

Quick example:
```java
class UserBuilder {
    static UserBuilder aUser() { return new UserBuilder(); }
    UserBuilder asAdmin() { return withRoles(Role.ADMIN); }
    User build() { return new User(email, name, roles); }
}

// Usage
var admin = aUser().withEmail("admin@test.com").asAdmin().build();
```

---

## Test Anti-Patterns to Avoid

### 1. Test Interdependence
```java
// BAD: tests depend on execution order
static User sharedUser;

@Test void test1_createUser() { sharedUser = service.create(...); }
@Test void test2_updateUser() { service.update(sharedUser, ...); }

// GOOD: each test is independent
@Test void shouldCreateUser() { var user = service.create(...); }
@Test void shouldUpdateUser() {
    var user = service.create(...);
    service.update(user, ...);
}
```

### 2. Over-Mocking
```java
// BAD: mocking everything
@Mock Mapper mapper;
@Mock Validator validator;
@Mock Logger logger;

// GOOD: use real implementations where practical
var mapper = new UserMapper();  // stateless, fast
var validator = new UserValidator();
```

### 3. Testing Implementation Details
```java
// BAD: breaks when you refactor
verify(repo, times(1)).findById(any());
verify(cache).get(any());
verify(mapper).toEntity(any());

// GOOD: test observable behavior
assertThat(result.getName()).isEqualTo("expected");
```

### 4. Ignoring Edge Cases
```java
// Always test:
// - null inputs
// - empty collections
// - boundary values
// - error conditions
@ParameterizedTest
@NullAndEmptySource
@ValueSource(strings = {" ", "   "})
void shouldRejectInvalidInput(String input) {
    assertThatThrownBy(() -> service.process(input))
        .isInstanceOf(IllegalArgumentException.class);
}
```

### 5. Slow Tests
```java
// BAD: unnecessary Spring context
@SpringBootTest
class SimpleCalculatorTest { ... }

// GOOD: plain unit test
class SimpleCalculatorTest {
    Calculator calc = new Calculator();
    ...
}
```

---

## Debugging Test Failures

### Common Issues

1. **Flaky tests**: Usually caused by:
   - Time-dependent code (use `Clock`)
   - Shared mutable state
   - Race conditions in async code
   - Random data without seed

2. **Spring context failures**:
   - Check `@ActiveProfiles("test")`
   - Verify `@MockBean` for external dependencies
   - Check for duplicate bean definitions

3. **Database test issues**:
   - Verify `@Transactional` for rollback
   - Check isolation level
   - Use `@DirtiesContext` sparingly (slow)

### Test Isolation Checklist
- [ ] No shared mutable state between tests
- [ ] Database rolled back after each test
- [ ] Mocks reset with `@BeforeEach` or `MockitoExtension`
- [ ] No file system side effects
- [ ] Fixed time/random seeds where needed

---

## Test Coverage Guidelines

### What to Cover
- All public methods of services
- All controller endpoints (happy + error paths)
- Business logic edge cases
- Security boundaries
- Data validation

### What NOT to Obsess Over
- Getters/setters/constructors
- Configuration classes
- Framework code
- Trivial delegation methods

### Coverage Targets
- Line coverage: 70-80% (not a hard rule)
- Branch coverage: Focus on complex conditionals
- Mutation testing: Better metric than line coverage

---

## Test Execution Commands

```bash
# All tests
mvn test

# Single class
mvn test -Dtest=UserServiceTest

# Single method
mvn test -Dtest=UserServiceTest#shouldCreateUser

# By tag
mvn test -Dgroups=integration

# With coverage
mvn test jacoco:report

# Parallel execution
mvn test -DforkCount=2 -DreuseForks=true
```

---

## Reference Files

For detailed patterns, see:
- **[references/jqwik-arbitraries.md](references/jqwik-arbitraries.md)**: Custom arbitraries, constraining, statistics, shrinking
- **[references/spring-testing.md](references/spring-testing.md)**: Spring Boot integration, MockMvc, security testing
- **[references/test-data-builders.md](references/test-data-builders.md)**: Builder and Mother patterns for test data

---

## Checklist for New Tests

- [ ] Test name describes behavior, not method
- [ ] Follows given/when/then structure
- [ ] Uses AssertJ for assertions
- [ ] Independent of other tests
- [ ] Fast (unit < 100ms, integration < 5s)
- [ ] Covers happy path + key error cases
- [ ] No unnecessary mocking
- [ ] Cleans up resources (files, connections)
