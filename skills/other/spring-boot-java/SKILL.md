---
name: spring-boot-java
description: |
  Spring Boot (Java) framework guardrails, patterns, and best practices.
  Use when working with Spring Boot Java projects, or when the user mentions Spring Boot.
  Provides JPA, Security, REST, WebFlux, and enterprise Java guidelines.
license: MIT
metadata:
  author: samuel
  version: "1.0"
  category: framework
  language: java
  extensions: ".java"
---

# Spring Boot (Java) Guide

> Applies to: Spring Boot 3.x, Java 17+, REST APIs, Microservices, Enterprise Applications

## Core Principles

1. **Convention Over Configuration**: Leverage Spring Boot auto-configuration; override only when necessary
2. **Layered Architecture**: Controller -> Service -> Repository with clear separation of concerns
3. **DTOs at Boundaries**: Never expose JPA entities in API responses; use records as DTOs
4. **Constructor Injection**: Use `@RequiredArgsConstructor` or explicit constructors; never field injection
5. **Externalized Config**: All configuration via `application.yml` with profile-specific overrides
6. **Database Migrations**: Schema changes through Flyway or Liquibase; never `ddl-auto=update` in production

## Guardrails

### Architecture Rules

- Controllers handle HTTP concerns only (validation, status codes, response mapping)
- Services contain business logic and transaction boundaries
- Repositories handle data access; use Spring Data JPA query derivation first
- Use `@Transactional(readOnly = true)` at service class level, `@Transactional` on write methods
- Keep `spring.jpa.open-in-view=false` to prevent lazy loading surprises
- Use `ProblemDetail` (RFC 7807) for all error responses

### Dependency Injection

- Prefer constructor injection with `@RequiredArgsConstructor` (Lombok) or explicit constructors
- Never use `@Autowired` on fields
- Use `@Bean` methods in `@Configuration` classes for third-party types
- One `@Configuration` class per concern (SecurityConfig, WebConfig, CacheConfig)

### REST API Conventions

- Versioned paths: `/api/v1/resources`
- Use proper HTTP methods: GET (read), POST (create), PUT (full update), PATCH (partial), DELETE
- Return `201 Created` with Location header for POST
- Return `204 No Content` for DELETE
- Always validate request bodies with `@Valid` and Jakarta Bean Validation
- Use `@PageableDefault` for list endpoints; never return unbounded collections
- Document APIs with SpringDoc OpenAPI annotations (`@Operation`, `@Tag`, `@ApiResponse`)

### Configuration

- Use `application.yml` over `application.properties`
- Environment-specific files: `application-dev.yml`, `application-prod.yml`
- Reference secrets via environment variables: `${DB_PASSWORD:default}`
- Configure HikariCP pool sizes explicitly (do not rely on defaults)
- Set `server.error.include-message=never` in production profiles

## Project Structure

```
myproject/
├── src/main/java/com/example/myproject/
│   ├── MyProjectApplication.java       # @SpringBootApplication entry point
│   ├── config/
│   │   ├── SecurityConfig.java         # Spring Security filter chain
│   │   └── WebConfig.java              # CORS, interceptors, converters
│   ├── controller/
│   │   └── UserController.java         # REST endpoints
│   ├── service/
│   │   ├── UserService.java            # Interface
│   │   └── impl/
│   │       └── UserServiceImpl.java    # Implementation
│   ├── repository/
│   │   └── UserRepository.java         # JpaRepository interface
│   ├── model/
│   │   ├── entity/
│   │   │   └── User.java              # JPA entity
│   │   └── dto/
│   │       ├── UserRequest.java        # Input record with validation
│   │       └── UserResponse.java       # Output record
│   ├── exception/
│   │   ├── GlobalExceptionHandler.java # @RestControllerAdvice
│   │   └── ResourceNotFoundException.java
│   └── mapper/
│       └── UserMapper.java             # MapStruct interface
├── src/main/resources/
│   ├── application.yml
│   ├── application-dev.yml
│   ├── application-prod.yml
│   └── db/migration/
│       └── V1__create_users_table.sql  # Flyway migration
├── src/test/java/com/example/myproject/
│   ├── controller/
│   │   └── UserControllerTest.java     # MockMvc tests
│   ├── service/
│   │   └── UserServiceTest.java        # Mockito unit tests
│   └── integration/
│       └── UserIntegrationTest.java    # Testcontainers
├── pom.xml
└── Dockerfile
```

- Service interfaces are optional for small projects; use them when multiple implementations exist
- Place MapStruct mappers in a dedicated `mapper/` package
- Separate `entity/` and `dto/` under `model/` to reinforce the boundary

## Controller Pattern

```java
@RestController
@RequestMapping("/api/v1/users")
@RequiredArgsConstructor
@Tag(name = "Users", description = "User management APIs")
public class UserController {

    private final UserService userService;

    @PostMapping
    @Operation(summary = "Create a new user")
    @ApiResponse(responseCode = "201", description = "User created")
    @ApiResponse(responseCode = "409", description = "Email conflict")
    public ResponseEntity<UserResponse> createUser(
            @Valid @RequestBody UserRequest request) {
        UserResponse response = userService.createUser(request);
        return ResponseEntity.status(HttpStatus.CREATED).body(response);
    }

    @GetMapping("/{id}")
    @Operation(summary = "Get user by ID")
    public ResponseEntity<UserResponse> getUserById(@PathVariable Long id) {
        return ResponseEntity.ok(userService.getUserById(id));
    }

    @GetMapping
    @Operation(summary = "List users with pagination")
    public ResponseEntity<Page<UserResponse>> getAllUsers(
            @PageableDefault(size = 20, sort = "id") Pageable pageable) {
        return ResponseEntity.ok(userService.getAllUsers(pageable));
    }

    @DeleteMapping("/{id}")
    @PreAuthorize("hasRole('ADMIN')")
    @Operation(summary = "Delete user (admin only)")
    public ResponseEntity<Void> deleteUser(@PathVariable Long id) {
        userService.deleteUser(id);
        return ResponseEntity.noContent().build();
    }
}
```

## Service Pattern

```java
@Service
@RequiredArgsConstructor
@Slf4j
@Transactional(readOnly = true)
public class UserServiceImpl implements UserService {

    private final UserRepository userRepository;
    private final UserMapper userMapper;
    private final PasswordEncoder passwordEncoder;

    @Override
    @Transactional
    public UserResponse createUser(UserRequest request) {
        if (userRepository.existsByEmail(request.email())) {
            throw new DuplicateResourceException("User", "email", request.email());
        }

        User user = userMapper.toEntity(request);
        user.setPassword(passwordEncoder.encode(request.password()));
        User saved = userRepository.save(user);

        return userMapper.toResponse(saved);
    }

    @Override
    public UserResponse getUserById(Long id) {
        return userRepository.findById(id)
            .map(userMapper::toResponse)
            .orElseThrow(() -> new ResourceNotFoundException("User", "id", id));
    }

    @Override
    public Page<UserResponse> getAllUsers(Pageable pageable) {
        return userRepository.findAll(pageable).map(userMapper::toResponse);
    }

    @Override
    @Transactional
    public void deleteUser(Long id) {
        if (!userRepository.existsById(id)) {
            throw new ResourceNotFoundException("User", "id", id);
        }
        userRepository.deleteById(id);
    }
}
```

## Repository Pattern

```java
@Repository
public interface UserRepository extends JpaRepository<User, Long> {

    Optional<User> findByEmail(String email);

    boolean existsByEmail(String email);

    List<User> findByActiveTrue();

    Page<User> findByRole(User.Role role, Pageable pageable);

    @Query("SELECT u FROM User u WHERE u.active = true AND u.role = :role")
    List<User> findActiveUsersByRole(@Param("role") User.Role role);
}
```

- Prefer Spring Data derived queries for simple lookups
- Use `@Query` with JPQL for joins and complex filters
- Use native queries only when JPQL is insufficient (bulk operations, database-specific functions)
- Always return `Optional` for single-entity lookups
- Use `Page`/`Slice` for paginated results

## JPA Entity

```java
@Entity
@Table(name = "users")
@Getter @Setter
@NoArgsConstructor @AllArgsConstructor @Builder
public class User {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, unique = true)
    private String email;

    @Column(nullable = false)
    private String password;

    @Column(nullable = false)
    @Enumerated(EnumType.STRING)
    @Builder.Default
    private Role role = Role.USER;

    @CreationTimestamp
    @Column(updatable = false)
    private LocalDateTime createdAt;

    @UpdateTimestamp
    private LocalDateTime updatedAt;

    public enum Role { USER, ADMIN }
}
```

## DTO Records with Validation

```java
// Request DTO
@Builder
public record UserRequest(
    @NotBlank(message = "Email is required")
    @Email(message = "Invalid email format")
    String email,

    @NotBlank(message = "Password is required")
    @Size(min = 8, max = 100)
    String password,

    @NotBlank(message = "Name is required")
    @Size(min = 2, max = 100)
    String name
) {}

// Response DTO
@Builder
public record UserResponse(
    Long id,
    String email,
    String name,
    String role,
    LocalDateTime createdAt
) {}
```

## Error Handling

```java
@RestControllerAdvice
@Slf4j
public class GlobalExceptionHandler {

    @ExceptionHandler(ResourceNotFoundException.class)
    public ProblemDetail handleNotFound(ResourceNotFoundException ex) {
        log.warn("Resource not found: {}", ex.getMessage());
        ProblemDetail problem = ProblemDetail.forStatusAndDetail(
            HttpStatus.NOT_FOUND, ex.getMessage());
        problem.setTitle("Resource Not Found");
        problem.setProperty("timestamp", Instant.now());
        return problem;
    }

    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ProblemDetail handleValidation(MethodArgumentNotValidException ex) {
        Map<String, String> errors = new HashMap<>();
        ex.getBindingResult().getAllErrors().forEach(error -> {
            String field = ((FieldError) error).getField();
            errors.put(field, error.getDefaultMessage());
        });
        ProblemDetail problem = ProblemDetail.forStatusAndDetail(
            HttpStatus.BAD_REQUEST, "Validation failed");
        problem.setTitle("Validation Error");
        problem.setProperty("timestamp", Instant.now());
        problem.setProperty("errors", errors);
        return problem;
    }

    @ExceptionHandler(Exception.class)
    public ProblemDetail handleUnexpected(Exception ex) {
        log.error("Unexpected error", ex);
        ProblemDetail problem = ProblemDetail.forStatusAndDetail(
            HttpStatus.INTERNAL_SERVER_ERROR, "An unexpected error occurred");
        problem.setTitle("Internal Server Error");
        problem.setProperty("timestamp", Instant.now());
        return problem;
    }
}
```

## Security Configuration

```java
@Configuration
@EnableWebSecurity
@EnableMethodSecurity  // enables @PreAuthorize for method-level access control
public class SecurityConfig {

    @Bean
    public SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
        return http
            .csrf(AbstractHttpConfigurer::disable)  // disable for stateless REST APIs
            .sessionManagement(session ->
                session.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
            .authorizeHttpRequests(auth -> auth
                .requestMatchers("/api-docs/**", "/swagger-ui/**").permitAll()
                .requestMatchers("/actuator/health", "/actuator/info").permitAll()
                .requestMatchers(HttpMethod.POST, "/api/v1/users").permitAll()
                .requestMatchers(HttpMethod.DELETE, "/api/v1/users/**").hasRole("ADMIN")
                .anyRequest().authenticated())
            .build();
    }

    @Bean
    public PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder(12);  // cost factor 12: security/performance balance
    }
}
```

## Testing Overview

### Unit Tests (Mockito)

```java
@ExtendWith(MockitoExtension.class)
@DisplayName("UserService")
class UserServiceTest {

    @Mock private UserRepository userRepository;
    @Mock private UserMapper userMapper;
    @Mock private PasswordEncoder passwordEncoder;
    @InjectMocks private UserServiceImpl userService;

    @Test
    @DisplayName("should create user with valid data")
    void shouldCreateUser() {
        when(userRepository.existsByEmail("test@example.com")).thenReturn(false);
        when(userMapper.toEntity(any())).thenReturn(new User());
        when(userRepository.save(any())).thenReturn(new User());
        when(userMapper.toResponse(any())).thenReturn(
            new UserResponse(1L, "test@example.com", "Test", "USER", null));

        UserResponse result = userService.createUser(
            new UserRequest("test@example.com", "Pass123!", "Test"));

        assertThat(result.email()).isEqualTo("test@example.com");
        verify(userRepository).save(any(User.class));
    }
}
```

### Integration Tests (Testcontainers + MockMvc)

```java
@SpringBootTest
@AutoConfigureMockMvc
@Testcontainers
class UserIntegrationTest {

    @Container
    static PostgreSQLContainer<?> postgres =
        new PostgreSQLContainer<>("postgres:15-alpine");

    @DynamicPropertySource
    static void configureProperties(DynamicPropertyRegistry registry) {
        registry.add("spring.datasource.url", postgres::getJdbcUrl);
        registry.add("spring.datasource.username", postgres::getUsername);
        registry.add("spring.datasource.password", postgres::getPassword);
    }

    @Autowired private MockMvc mockMvc;
    @Autowired private ObjectMapper objectMapper;

    @Test
    void shouldCreateUserViaApi() throws Exception {
        var request = new UserRequest("test@example.com", "Pass123!", "Test");
        mockMvc.perform(post("/api/v1/users")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(request)))
            .andExpect(status().isCreated())
            .andExpect(jsonPath("$.email").value("test@example.com"));
    }
}
```

## Commands

```bash
# Create project via Spring Initializr
# https://start.spring.io/

# Build
./mvnw clean package

# Run
./mvnw spring-boot:run

# Run with profile
./mvnw spring-boot:run -Dspring-boot.run.profiles=dev

# Test
./mvnw test

# Test with coverage
./mvnw verify

# Format (with spotless plugin)
./mvnw spotless:apply

# Static analysis
./mvnw checkstyle:check

# Build Docker image (Spring Boot Buildpacks)
./mvnw spring-boot:build-image

# Native executable (GraalVM)
./mvnw -Pnative native:compile
```

## Best Practices

| Do | Do Not |
|----|--------|
| Constructor injection (`@RequiredArgsConstructor`) | `@Autowired` on fields |
| `@Transactional(readOnly = true)` at class level | `@Transactional` without `readOnly` at class level |
| DTOs (records) for API input/output | Expose JPA entities in responses |
| MapStruct for entity-DTO mapping | Manual mapping boilerplate |
| Pagination for all list endpoints | Unbounded collection returns |
| ProblemDetail (RFC 7807) errors | Custom error formats |
| Flyway/Liquibase for migrations | `ddl-auto=update` in production |
| Testcontainers for integration tests | H2 as production substitute |
| `open-in-view=false` | Lazy loading outside transactions |
| JPA batch inserts (`hibernate.jdbc.batch_size`) | Individual saves in loops |

## Advanced Topics

For detailed patterns and advanced configurations, see:

- [references/patterns.md](references/patterns.md) -- JPA advanced patterns, Security with JWT, WebFlux reactive, testing strategies, Actuator, deployment

## External References

- [Spring Boot Documentation](https://docs.spring.io/spring-boot/docs/current/reference/html/)
- [Spring Data JPA](https://docs.spring.io/spring-data/jpa/docs/current/reference/html/)
- [Spring Security](https://docs.spring.io/spring-security/reference/)
- [Baeldung Spring Tutorials](https://www.baeldung.com/spring-tutorial)
- [MapStruct Documentation](https://mapstruct.org/documentation/stable/reference/html/)
- [Testcontainers](https://testcontainers.com/)
