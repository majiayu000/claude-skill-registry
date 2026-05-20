---
name: micronaut
description: |
  Micronaut framework guardrails, patterns, and best practices for AI-assisted development.
  Use when working with Micronaut projects, or when the user mentions Micronaut.
  Provides compile-time DI, HTTP server/client, data access, and cloud-native guidelines.
license: MIT
metadata:
  author: samuel
  version: "1.0"
  category: framework
  language: java
  extensions: ".java"
---

# Micronaut Guide

> Applies to: Micronaut 4.x, Java 21+, Microservices, Serverless, CLI Applications, IoT

## Core Principles

1. **Compile-Time DI**: All dependency injection resolved at compile time -- no reflection at runtime
2. **GraalVM Native**: First-class native image support for fast startup and low memory
3. **Reactive by Default**: Built-in reactive programming with non-blocking I/O
4. **Cloud-Native**: Service discovery, distributed tracing, config management out of the box
5. **Fast Startup**: Sub-100ms startup makes it ideal for serverless and containers
6. **Standard Library**: Use `jakarta.inject` annotations, not Spring-specific ones

## Guardrails

### Dependency Injection

- Use constructor injection exclusively (compile-time verified)
- Annotate beans with `@Singleton`, `@Prototype`, or `@RequestScope`
- Use `@Factory` for third-party objects that cannot be annotated
- Use `@Requires` for conditional bean loading
- Never use `@Autowired` or Spring DI annotations
- Prefer interface-based injection for testability
- Avoid field injection (not compile-time verifiable)

### HTTP Controllers

- Annotate controllers with `@Controller("/path")`
- Use `@ExecuteOn(TaskExecutors.BLOCKING)` for JDBC/blocking operations
- Apply `@Validated` at class level for request validation
- Return `HttpResponse<T>` for status code control, direct type for 200 OK
- Use `@Status(HttpStatus.CREATED)` for POST endpoints
- Keep controllers thin -- delegate business logic to services
- Add OpenAPI annotations (`@Operation`, `@ApiResponse`) for all endpoints

### Data Access

- Use `@JdbcRepository` or `@MongoRepository` with dialect specification
- Extend `PageableRepository<Entity, ID>` for pagination support
- Use `@Query` for custom queries, prefer derived query methods when possible
- Apply `@Transactional` at service layer, not repository layer
- Use `@Transactional(readOnly = true)` for read-only operations
- Use Flyway or Liquibase for schema migrations (never `schema-generate: CREATE`)
- Always include rollback scripts for migrations

### DTOs and Serialization

- Use Java records for DTOs (immutable by default)
- Annotate all DTOs with `@Serdeable` (Micronaut serialization)
- Apply Jakarta validation annotations (`@NotBlank`, `@Email`, `@Size`)
- Never expose domain entities directly in API responses
- Use MapStruct with `componentModel = "jsr330"` for entity-DTO mapping
- Create separate request and response DTOs

### Error Handling

- Implement `ExceptionHandler<E, HttpResponse<T>>` for each exception type
- Return RFC 7807 Problem Details format for error responses
- Use `@Requires(classes = {...})` on exception handlers
- Log warnings/errors in exception handlers
- Never expose internal details (stack traces, SQL) in error responses

### Configuration

- Use `application.yml` with environment-specific overrides (`application-dev.yml`)
- Reference secrets via environment variables: `${ENV_VAR:default}`
- Never hardcode secrets, API keys, or passwords
- Use `@ConfigurationProperties` for type-safe configuration beans
- Enable health checks and Prometheus metrics for production

### Testing

- Use `@MicronautTest` for integration tests (starts embedded server)
- Use `@MockBean` for mocking dependencies in integration tests
- Use `@ExtendWith(MockitoExtension.class)` for unit tests
- Use Testcontainers for database integration tests
- Implement `TestPropertyProvider` for dynamic test configuration
- Test names describe behavior: `shouldCreateUserWhenEmailIsUnique`
- Coverage target: >80% for business logic, >60% overall

### Performance

- Use `@ExecuteOn(TaskExecutors.BLOCKING)` only for blocking operations
- Use reactive types (`Mono`, `Flux`) for non-blocking I/O when appropriate
- Enable AOT optimizations in `build.gradle` for production
- Use connection pooling (HikariCP) with tuned pool sizes
- Paginate all list endpoints (never return unbounded collections)

## Project Structure

```
myapp/
├── src/main/
│   ├── java/com/example/
│   │   ├── Application.java       # Entry point with @OpenAPIDefinition
│   │   ├── config/                 # @Factory, @ConfigurationProperties
│   │   ├── controller/            # @Controller classes
│   │   ├── service/               # Business logic interfaces
│   │   │   └── impl/              # Service implementations
│   │   ├── repository/            # @JdbcRepository interfaces
│   │   ├── domain/                # @MappedEntity classes
│   │   ├── dto/                   # @Serdeable records
│   │   ├── mapper/                # MapStruct @Mapper interfaces
│   │   └── exception/             # Custom exceptions + handlers
│   └── resources/
│       ├── application.yml        # Main config (with -dev.yml, -prod.yml overrides)
│       ├── db/migration/          # Flyway SQL files
│       └── logback.xml
├── src/test/java/com/example/     # Unit + integration tests
├── build.gradle                   # Micronaut Gradle plugin
└── settings.gradle
```

- `service/impl/` separates interface from implementation for testability
- `dto/` uses `@Serdeable` records for API request/response types
- `mapper/` bridges domain entities to DTOs via MapStruct
- `exception/` bundles custom exceptions with their `ExceptionHandler` implementations

## Compile-Time DI Patterns

### Singleton Bean

```java
@Singleton
@RequiredArgsConstructor
public class UserServiceImpl implements UserService {
    private final UserRepository userRepository;
    private final UserMapper userMapper;
    // Constructor injection -- resolved at compile time
}
```

### Factory for Third-Party Objects

```java
@Factory
public class SecurityBeans {
    @Singleton
    public BCryptPasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder(12);
    }
}
```

### Conditional Beans

```java
@Singleton
@Requires(env = "production")
public class ProductionEmailService implements EmailService { }

@Singleton
@Requires(env = "dev")
public class MockEmailService implements EmailService { }
```

## Controller Pattern

```java
@Controller("/api/users")
@Validated
@RequiredArgsConstructor
@ExecuteOn(TaskExecutors.BLOCKING)
@Secured(SecurityRule.IS_AUTHENTICATED)
@Tag(name = "Users", description = "User management endpoints")
public class UserController {

    private final UserService userService;

    @Post
    @Status(HttpStatus.CREATED)
    @Operation(summary = "Create a new user")
    @ApiResponse(responseCode = "201", description = "User created")
    @ApiResponse(responseCode = "409", description = "Email already exists")
    public HttpResponse<UserResponse> createUser(@Body @Valid UserRequest request) {
        UserResponse user = userService.createUser(request);
        return HttpResponse.created(user)
            .headers(h -> h.location(URI.create("/api/users/" + user.id())));
    }

    @Get("/{id}")
    @Operation(summary = "Get user by ID")
    public UserResponse getUserById(@PathVariable Long id) {
        return userService.getUserById(id);
    }

    @Get
    @Operation(summary = "List users with pagination")
    public PageResponse<UserResponse> getAllUsers(
            @QueryValue(defaultValue = "0") int page,
            @QueryValue(defaultValue = "20") int size) {
        return userService.getAllUsers(page, size);
    }

    @Put("/{id}")
    public UserResponse updateUser(@PathVariable Long id, @Body @Valid UserRequest request) {
        return userService.updateUser(id, request);
    }

    @Delete("/{id}")
    @Status(HttpStatus.NO_CONTENT)
    @Secured({"ROLE_ADMIN"})
    public void deleteUser(@PathVariable Long id) {
        userService.deleteUser(id);
    }
}
```

## Data Access Patterns

### Domain Entity

```java
@Serdeable
@MappedEntity("users")
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class User {
    @Id
    @GeneratedValue(GeneratedValue.Type.AUTO)
    private Long id;

    @Column("email")
    private String email;

    @Column("password")
    private String password;

    @DateCreated
    @Column("created_at")
    private Instant createdAt;

    @DateUpdated
    @Column("updated_at")
    private Instant updatedAt;
}
```

### Repository

```java
@JdbcRepository(dialect = Dialect.POSTGRES)
public interface UserRepository extends PageableRepository<User, Long> {

    Optional<User> findByEmail(String email);

    boolean existsByEmail(String email);

    List<User> findByActiveTrue();

    Page<User> findByRole(String role, Pageable pageable);

    @Query("UPDATE User u SET u.active = :active WHERE u.id = :id")
    void updateActiveStatus(Long id, boolean active);
}
```

### DTO Records

```java
@Serdeable
public record UserRequest(
    @NotBlank @Email @Size(max = 255) String email,
    @NotBlank @Size(min = 8, max = 100) String password,
    @NotBlank @Size(max = 100) String firstName,
    @NotBlank @Size(max = 100) String lastName
) {}

@Serdeable
public record UserResponse(
    Long id, String email, String firstName, String lastName,
    Boolean active, Instant createdAt, Instant updatedAt
) {}

@Serdeable
public record PageResponse<T>(
    List<T> content, int page, int size,
    long totalElements, int totalPages, boolean first, boolean last
) {
    public static <T> PageResponse<T> of(List<T> content, int page, int size, long total) {
        int totalPages = (int) Math.ceil((double) total / size);
        return new PageResponse<>(content, page, size, total, totalPages,
            page == 0, page >= totalPages - 1);
    }
}
```

## Configuration (application.yml)

```yaml
micronaut:
  application:
    name: myapp
  server:
    port: 8080
  security:
    authentication: bearer
    token:
      jwt:
        signatures:
          secret:
            generator:
              secret: ${JWT_SECRET}
              jws-algorithm: HS256
    intercept-url-map:
      - pattern: /health/**
        access: [isAnonymous()]
      - pattern: /api/**
        access: [isAuthenticated()]

datasources:
  default:
    url: jdbc:postgresql://localhost:5432/myapp
    username: ${DB_USERNAME:postgres}
    password: ${DB_PASSWORD:postgres}

flyway:
  datasources:
    default:
      enabled: true
      locations: classpath:db/migration

endpoints:
  health: { enabled: true, sensitive: false }
  prometheus: { enabled: true, sensitive: false }
```

## Error Handling Pattern

### Custom Exception

```java
public class ResourceNotFoundException extends RuntimeException {
    private final String resourceName;
    private final String fieldName;
    private final Object fieldValue;

    public ResourceNotFoundException(String resource, String field, Object value) {
        super(String.format("%s not found with %s: '%s'", resource, field, value));
        this.resourceName = resource;
        this.fieldName = field;
        this.fieldValue = value;
    }
    // getters
}
```

### Exception Handler

```java
@Singleton
@Produces
@Requires(classes = {ResourceNotFoundException.class, ExceptionHandler.class})
public class ResourceNotFoundExceptionHandler
    implements ExceptionHandler<ResourceNotFoundException, HttpResponse<ErrorResponse>> {

    @Override
    public HttpResponse<ErrorResponse> handle(HttpRequest request, ResourceNotFoundException ex) {
        ErrorResponse error = ErrorResponse.of(404, "Not Found", ex.getMessage(), request.getPath());
        return HttpResponse.notFound(error);
    }
}
```

## Testing Patterns

### Unit Test (Mockito)

```java
@ExtendWith(MockitoExtension.class)
@DisplayName("UserService")
class UserServiceTest {

    @Mock private UserRepository userRepository;
    @Mock private UserMapper userMapper;
    private UserServiceImpl userService;

    @BeforeEach
    void setUp() {
        userService = new UserServiceImpl(userRepository, userMapper);
    }

    @Test
    @DisplayName("should create user when email is unique")
    void shouldCreateUserWhenEmailIsUnique() {
        when(userRepository.existsByEmail("test@example.com")).thenReturn(false);
        when(userMapper.toEntity(any())).thenReturn(new User());
        when(userRepository.save(any())).thenReturn(new User());
        when(userMapper.toResponse(any())).thenReturn(expectedResponse);

        UserResponse result = userService.createUser(request);

        assertThat(result).isNotNull();
        verify(userRepository).save(any());
    }
}
```

### Integration Test (MicronautTest + Testcontainers)

```java
@MicronautTest
@Testcontainers
@TestInstance(TestInstance.Lifecycle.PER_CLASS)
class IntegrationTest implements TestPropertyProvider {

    @Container
    static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:15-alpine");

    @Inject @Client("/") HttpClient client;

    @Override
    public Map<String, String> getProperties() {
        postgres.start();
        return Map.of(
            "datasources.default.url", postgres.getJdbcUrl(),
            "datasources.default.username", postgres.getUsername(),
            "datasources.default.password", postgres.getPassword()
        );
    }

    @Test
    void healthEndpoint_shouldReturnUp() {
        var response = client.toBlocking().exchange(HttpRequest.GET("/health"), String.class);
        assertThat(response.status().getCode()).isEqualTo(200);
    }
}
```

## Build & Run Commands

```bash
./gradlew build                            # Build
MICRONAUT_ENVIRONMENTS=dev ./gradlew run   # Run (dev profile)
./gradlew test                             # Run tests
./gradlew test jacocoTestReport            # Tests + coverage report
./gradlew nativeCompile                    # GraalVM native image
./gradlew dockerBuild                      # Docker image
./gradlew dockerBuildNative                # Native Docker image
./gradlew clean build                      # Clean build
./gradlew check                            # Lint (checkstyle/spotbugs)
```

## Do's and Don'ts

### Do

- Use constructor injection (compile-time verified)
- Use `@Serdeable` for all DTOs
- Use `@ExecuteOn(TaskExecutors.BLOCKING)` for blocking operations
- Use `@Transactional` at the service layer
- Use validation annotations on DTOs
- Use native compilation for production deployments
- Use Micronaut Data for repositories
- Enable health checks and metrics

### Don't

- Don't use reflection-based libraries without GraalVM configuration
- Don't use `@Autowired` or Spring-specific annotations
- Don't block in reactive streams
- Don't expose internal details in error responses
- Don't skip DTO validation
- Don't use mutable DTOs (prefer records)
- Don't ignore compile-time warnings from annotation processors

## Advanced Topics

For detailed patterns and examples, see:

- [references/patterns.md](references/patterns.md) -- GraalVM native, messaging, security, advanced testing, deployment patterns

## External References

- [Micronaut Documentation](https://docs.micronaut.io/)
- [Micronaut Guides](https://guides.micronaut.io/)
- [Micronaut Data](https://micronaut-projects.github.io/micronaut-data/latest/guide/)
- [Micronaut Security](https://micronaut-projects.github.io/micronaut-security/latest/guide/)
- [GraalVM Native Image](https://www.graalvm.org/native-image/)
