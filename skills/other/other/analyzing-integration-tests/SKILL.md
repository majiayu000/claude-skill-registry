---
name: analyzing-integration-tests
description: Use when analyzing integration tests that verify component interactions, database access, and external service integration
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash(mkdir:*, ls:*)
  - Write(docs/unwind/**)
  - Edit(docs/unwind/**)
---

# Analyzing Integration Tests

**Output:** `docs/unwind/layers/integration-tests/` (folder with index.md + section files)

**Principles:** See `analysis-principles.md` - completeness, machine-readable, link to source, no commentary, incremental writes.

## Output Structure

```
docs/unwind/layers/integration-tests/
├── index.md           # Test summary, infrastructure overview
├── config.md          # Test containers, database setup
├── repository-tests.md # Database integration tests
├── api-tests.md       # API endpoint tests
├── external-tests.md  # External service integration tests
└── messaging-tests.md # Kafka/queue tests
```

For large codebases, split by integration type:
```
docs/unwind/layers/integration-tests/
├── index.md
├── config.md
├── database/
├── api/
└── messaging/
```

## Process (Incremental Writes)

**Step 1: Setup**
```bash
mkdir -p docs/unwind/layers/integration-tests/
```
Write initial `index.md`:
```markdown
# Integration Tests

## Sections
- [Configuration](config.md) - _pending_
- [Repository Tests](repository-tests.md) - _pending_
- [API Tests](api-tests.md) - _pending_
- [External Service Tests](external-tests.md) - _pending_
- [Messaging Tests](messaging-tests.md) - _pending_

## Summary
_Analysis in progress..._
```

**Step 2: Analyze and write config.md**
1. Find test containers, database setup, WireMock config
2. Write `config.md` immediately
3. Update `index.md`

**Step 3: Analyze and write repository-tests.md**
1. Find all database integration tests
2. Write `repository-tests.md` immediately
3. Update `index.md`

**Step 4: Analyze and write api-tests.md**
1. Find all API endpoint tests
2. Write `api-tests.md` immediately
3. Update `index.md`

**Step 5: Analyze and write external-tests.md** (if applicable)
1. Find external service integration tests
2. Write `external-tests.md` immediately
3. Update `index.md`

**Step 6: Analyze and write messaging-tests.md** (if applicable)
1. Find Kafka/queue tests
2. Write `messaging-tests.md` immediately
3. Update `index.md`

**Step 7: Finalize index.md**
Add integration summary table

## Output Format

```markdown
# Integration Tests

## Configuration

### Test Containers

[TestContainersConfig.java](https://github.com/owner/repo/blob/main/src/test/java/config/TestContainersConfig.java)

```java
@TestConfiguration
public class TestContainersConfig {

    @Container
    static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:14")
        .withDatabaseName("testdb")
        .withUsername("test")
        .withPassword("test");

    @Container
    static KafkaContainer kafka = new KafkaContainer(DockerImageName.parse("confluentinc/cp-kafka:7.0.0"));

    @DynamicPropertySource
    static void configureProperties(DynamicPropertyRegistry registry) {
        registry.add("spring.datasource.url", postgres::getJdbcUrl);
        registry.add("spring.kafka.bootstrap-servers", kafka::getBootstrapServers);
    }
}
```

### WireMock Setup

[WireMockConfig.java](https://github.com/owner/repo/blob/main/src/test/java/config/WireMockConfig.java)

```java
@TestConfiguration
public class WireMockConfig {

    @Bean
    public WireMockServer wireMockServer() {
        WireMockServer server = new WireMockServer(WireMockConfiguration.wireMockConfig().dynamicPort());
        server.start();
        return server;
    }
}
```

## Test Summary

| Integration | Tests | Status |
|-------------|-------|--------|
| Database | 15 | Passing |
| Kafka | 8 | Passing |
| Stripe API | 5 | Passing |
| Email Service | 3 | Passing |

## Repository Integration Tests

### UserRepositoryIT

[UserRepositoryIT.java](https://github.com/owner/repo/blob/main/src/test/java/repository/UserRepositoryIT.java)

```java
@DataJpaTest
@Testcontainers
@AutoConfigureTestDatabase(replace = NONE)
class UserRepositoryIT {

    @Container
    static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:14");

    @Autowired
    private UserRepository userRepository;

    @Test
    void findByEmail_existingUser_returnsUser() {
        User user = new User("test@example.com", "hash");
        userRepository.save(user);

        Optional<User> found = userRepository.findByEmail("test@example.com");

        assertThat(found).isPresent();
        assertThat(found.get().getEmail()).isEqualTo("test@example.com");
    }

    @Test
    void findByStatus_multipleUsers_returnsFiltered() {
        userRepository.save(new User("active@example.com", "hash", UserStatus.ACTIVE));
        userRepository.save(new User("suspended@example.com", "hash", UserStatus.SUSPENDED));

        List<User> active = userRepository.findByStatus(UserStatus.ACTIVE);

        assertThat(active).hasSize(1);
        assertThat(active.get(0).getEmail()).isEqualTo("active@example.com");
    }
}
```

[Continue for ALL repository tests...]

## API Integration Tests

### UserControllerIT

[UserControllerIT.java](https://github.com/owner/repo/blob/main/src/test/java/controller/UserControllerIT.java)

```java
@SpringBootTest(webEnvironment = RANDOM_PORT)
@Testcontainers
class UserControllerIT {

    @Autowired
    private TestRestTemplate restTemplate;

    @Test
    void createUser_validRequest_returnsCreated() {
        CreateUserRequest request = new CreateUserRequest("new@example.com", "password123", "New User");

        ResponseEntity<UserResponse> response = restTemplate.postForEntity(
            "/api/v1/users", request, UserResponse.class);

        assertThat(response.getStatusCode()).isEqualTo(HttpStatus.CREATED);
        assertThat(response.getBody().email()).isEqualTo("new@example.com");
    }
}
```

## External Service Tests

### StripeClientIT

[StripeClientIT.java](https://github.com/owner/repo/blob/main/src/test/java/client/StripeClientIT.java)

```java
@SpringBootTest
@AutoConfigureWireMock(port = 0)
class StripeClientIT {

    @Autowired
    private StripeClient stripeClient;

    @Test
    void charge_validToken_returnsSuccess() {
        stubFor(post(urlEqualTo("/v1/charges"))
            .willReturn(aResponse()
                .withStatus(200)
                .withBody("{\"id\": \"ch_123\", \"status\": \"succeeded\"}")));

        PaymentResult result = stripeClient.charge("tok_valid", Money.of(100, USD));

        assertThat(result.isSuccess()).isTrue();
    }
}
```

## Messaging Tests

### OrderEventIT

[OrderEventIT.java](https://github.com/owner/repo/blob/main/src/test/java/messaging/OrderEventIT.java)

```java
@SpringBootTest
@EmbeddedKafka(partitions = 1, topics = {"order-events"})
class OrderEventIT {

    @Autowired
    private OrderEventPublisher publisher;

    @Autowired
    private KafkaTemplate<String, Object> kafkaTemplate;

    @Test
    void publishOrderCreated_sendsToKafka() {
        Order order = createTestOrder();

        publisher.publishOrderCreated(order);

        // Verify message received
        ConsumerRecord<String, Object> record = KafkaTestUtils.getSingleRecord(consumer, "order-events");
        assertThat(record.value()).isInstanceOf(OrderCreatedEvent.class);
    }
}
```

## Unknowns

- [List anything unclear]
```

## Refresh Mode

If `docs/unwind/layers/integration-tests/` exists, compare current state and add `## Changes Since Last Review` section to `index.md`.
