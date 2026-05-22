---
name: quarkus
description: |
  Quarkus framework guardrails, patterns, and best practices for AI-assisted development.
  Use when working with Quarkus projects, or when the user mentions Quarkus.
  Provides CDI, RESTEasy, Panache, GraalVM native, and reactive guidelines.
license: MIT
metadata:
  author: samuel
  version: "1.0"
  category: framework
  language: java
  extensions: ".java"
---

# Quarkus Guide

> Applies to: Quarkus 3.x, Java 17+, Cloud-Native Microservices, GraalVM Native, Kubernetes

## Core Principles

1. **Kubernetes-Native**: Designed for containers, fast startup, low memory footprint
2. **Developer Joy**: Live reload via Dev Services, Dev UI, continuous testing
3. **Unified Reactive/Imperative**: Choose per-endpoint, both coexist in one app
4. **Build-Time Optimization**: Extensions process metadata at build time, not runtime
5. **GraalVM First-Class**: Native compilation with millisecond startup and minimal RSS
6. **Standards-Based**: MicroProfile, Jakarta EE, Vert.x, SmallRye under the hood

## Guardrails

### Project & Dependencies

- Use Quarkus BOM for version management (never pin individual Quarkus artifact versions)
- Add extensions via `./mvnw quarkus:add-extension` rather than editing pom.xml manually
- Run `./mvnw quarkus:dev` for live reload; never restart manually during development
- Use Dev Services (auto-provisioned containers) for databases, Kafka, Redis in dev/test
- Keep `application.properties` profile-aware: `%dev.`, `%test.`, `%prod.` prefixes

### CDI (Contexts and Dependency Injection)

- Use `@ApplicationScoped` for stateless services (one instance per app)
- Use `@RequestScoped` only when you need per-request state
- Prefer constructor injection or `@Inject` fields (constructor preferred for testability)
- Avoid `@Dependent` scope unless you need a new instance per injection point
- Use `@Startup` for beans that must initialize eagerly at boot
- Register beans for native with `@RegisterForReflection` only when reflection is required
- Produce CDI beans via `@Produces` methods for third-party objects

### RESTEasy Reactive Resources

- Use RESTEasy Reactive (`quarkus-resteasy-reactive`), not classic RESTEasy
- Return `Uni<T>` or `Multi<T>` for non-blocking I/O; plain types for blocking is acceptable
- Keep resource classes thin: validate input, delegate to service, map response
- Use `@Valid` on request parameters for Bean Validation
- Annotate with `@Produces(APPLICATION_JSON)` and `@Consumes(APPLICATION_JSON)`
- Use `@Path` versioning: `/api/v1/resource`
- Add OpenAPI annotations (`@Operation`, `@APIResponse`) on every endpoint
- Secure endpoints with `@RolesAllowed`, `@Authenticated`, or `@PermitAll`

### Panache ORM

- **Active Record** (`extends PanacheEntity`): good for simple CRUD entities
- **Repository** (`implements PanacheRepository<T>`): good for complex queries, better testability
- Use `Uni<T>` return types with `hibernate-reactive-panache` for non-blocking DB access
- Add custom finder methods on entity or repository (e.g., `findByEmail`)
- Use `@WithTransaction` on service methods that write, not on resources
- Set `quarkus.hibernate-orm.database.generation=validate` and manage schema via Flyway
- Always provide `@PrePersist` / `@PreUpdate` for audit timestamps

### Configuration

- Use `application.properties` with profile prefixes: `%dev.`, `%test.`, `%prod.`
- Inject config values with `@ConfigProperty(name = "key", defaultValue = "fallback")`
- Group related config with `@ConfigMapping` interfaces
- Never hardcode secrets; use `${ENV_VAR:default}` placeholder syntax
- Enable Dev Services for local containers: `quarkus.devservices.enabled=true`

### Error Handling

- Create domain exceptions: `ResourceNotFoundException`, `DuplicateResourceException`
- Register JAX-RS `@Provider` classes implementing `ExceptionMapper<T>`
- Return structured error bodies: `{ title, status, detail, timestamp }`
- Map `ConstraintViolationException` to 400 with per-field error details
- Log at WARN for client errors, ERROR for unexpected failures

### Native Build Compatibility

- Avoid runtime reflection (use `@RegisterForReflection` when unavoidable)
- Avoid dynamic proxies and runtime bytecode generation
- Test native build regularly: `./mvnw verify -Pnative`
- Use `@BuildStep` extensions for build-time processing
- Prefer compile-time DI and annotation processors (MapStruct, Panache)
- Use `quarkus.native.container-build=true` to build without local GraalVM

## Project Structure

```
myproject/
├── src/main/java/com/example/
│   ├── resource/              # JAX-RS endpoints (thin controllers)
│   │   ├── UserResource.java
│   │   └── AuthResource.java
│   ├── service/               # Business logic
│   │   └── UserService.java
│   ├── repository/            # Panache repositories (optional if using active record)
│   │   └── UserRepository.java
│   ├── entity/                # JPA entities with Panache
│   │   └── User.java
│   ├── dto/                   # Request/response records
│   │   ├── UserRequest.java
│   │   └── UserResponse.java
│   ├── mapper/                # MapStruct mappers (compile-time, CDI-scoped)
│   │   └── UserMapper.java
│   ├── exception/             # Domain exceptions + ExceptionMappers
│   │   ├── ResourceNotFoundException.java
│   │   ├── DuplicateResourceException.java
│   │   └── ExceptionMappers.java
│   └── health/                # MicroProfile Health checks
│       └── DatabaseHealthCheck.java
├── src/main/resources/
│   ├── application.properties # Config with profile prefixes
│   └── db/migration/          # Flyway SQL migrations
│       └── V1__create_users.sql
├── src/main/docker/
│   ├── Dockerfile.jvm
│   └── Dockerfile.native
├── src/test/java/com/example/
│   ├── resource/              # @QuarkusTest integration tests
│   │   └── UserResourceTest.java
│   └── service/               # Unit tests with @InjectMock
│       └── UserServiceTest.java
└── pom.xml
```

- `resource/` -- Thin REST endpoints; input validation and response mapping only
- `service/` -- All business logic; transactional boundaries live here
- `repository/` -- Data access (skip if active record pattern suffices)
- `entity/` -- JPA entities; keep domain logic minimal, push to service
- `dto/` -- Java records for request/response; use Bean Validation annotations
- `mapper/` -- MapStruct interfaces with `componentModel = "cdi"`
- `exception/` -- Domain exceptions and JAX-RS ExceptionMapper providers
- `health/` -- MicroProfile HealthCheck implementations

## CDI Pattern

```java
@ApplicationScoped
public class UserService {

    @Inject
    UserRepository userRepository;

    @Inject
    UserMapper userMapper;

    @WithTransaction
    public Uni<UserResponse> createUser(UserRequest request) {
        return userRepository.existsByEmail(request.email())
            .flatMap(exists -> {
                if (exists) {
                    return Uni.createFrom().failure(
                        new DuplicateResourceException("User", "email", request.email()));
                }
                User user = userMapper.toEntity(request);
                return userRepository.persist(user).map(userMapper::toResponse);
            });
    }

    public Uni<UserResponse> getUserById(Long id) {
        return userRepository.findById(id)
            .onItem().ifNull().failWith(
                () -> new ResourceNotFoundException("User", "id", id))
            .map(userMapper::toResponse);
    }
}
```

## RESTEasy Resource Pattern

```java
@Path("/api/v1/users")
@Produces(MediaType.APPLICATION_JSON)
@Consumes(MediaType.APPLICATION_JSON)
@Tag(name = "Users", description = "User management APIs")
public class UserResource {

    @Inject
    UserService userService;

    @POST
    @Operation(summary = "Create a new user")
    @APIResponse(responseCode = "201", description = "User created")
    public Uni<Response> createUser(@Valid UserRequest request) {
        return userService.createUser(request)
            .map(user -> Response
                .created(URI.create("/api/v1/users/" + user.id()))
                .entity(user).build());
    }

    @GET
    @Path("/{id}")
    @RolesAllowed({"USER", "ADMIN"})
    @SecurityRequirement(name = "jwt")
    @Operation(summary = "Get user by ID")
    public Uni<UserResponse> getUserById(@PathParam("id") Long id) {
        return userService.getUserById(id);
    }
}
```

## Panache Entity Pattern

```java
@Entity
@Table(name = "users")
public class User extends PanacheEntity {

    @Column(nullable = false, unique = true)
    public String email;

    @Column(nullable = false)
    public String name;

    @Column(name = "created_at", updatable = false)
    public LocalDateTime createdAt;

    @PrePersist
    void onCreate() {
        createdAt = LocalDateTime.now();
    }

    // Panache active record queries
    public static Uni<User> findByEmail(String email) {
        return find("email", email).firstResult();
    }

    public static Uni<List<User>> findActive() {
        return list("active", true);
    }
}
```

## DTO Records with Validation

```java
public record UserRequest(
    @NotBlank(message = "Email is required")
    @Email(message = "Invalid email format")
    String email,

    @NotBlank(message = "Password is required")
    @Size(min = 8, max = 100, message = "Password must be 8-100 characters")
    String password,

    @NotBlank(message = "Name is required")
    @Size(min = 2, max = 100)
    String name
) {}

public record UserResponse(
    Long id, String email, String name,
    String role, boolean active, LocalDateTime createdAt
) {}
```

## Exception Mapper Pattern

```java
@Provider
public class ResourceNotFoundMapper
        implements ExceptionMapper<ResourceNotFoundException> {

    @Override
    public Response toResponse(ResourceNotFoundException e) {
        return Response.status(Response.Status.NOT_FOUND)
            .entity(Map.of(
                "title", "Resource Not Found",
                "status", 404,
                "detail", e.getMessage(),
                "timestamp", Instant.now().toString()))
            .build();
    }
}
```

## Configuration

```properties
# Application
quarkus.application.name=myproject
quarkus.http.port=8080

# Reactive datasource
quarkus.datasource.db-kind=postgresql
quarkus.datasource.username=${DB_USERNAME:postgres}
quarkus.datasource.password=${DB_PASSWORD:postgres}
quarkus.datasource.reactive.url=vertx-reactive:postgresql://localhost:5432/mydb

# JDBC (for Flyway migrations)
quarkus.datasource.jdbc.url=jdbc:postgresql://localhost:5432/mydb

# Hibernate
quarkus.hibernate-orm.database.generation=validate
quarkus.hibernate-orm.log.sql=true

# Flyway
quarkus.flyway.migrate-at-start=true
quarkus.flyway.locations=db/migration

# Dev Services
%dev.quarkus.datasource.devservices.enabled=true
%dev.quarkus.datasource.devservices.image-name=postgres:15-alpine

# Logging
quarkus.log.level=INFO
quarkus.log.category."com.example".level=DEBUG
%prod.quarkus.log.console.json=true

# JWT
mp.jwt.verify.publickey.location=publicKey.pem
mp.jwt.verify.issuer=https://example.com

# OpenAPI / Swagger
quarkus.smallrye-openapi.path=/api-docs
quarkus.swagger-ui.always-include=true

# Health
quarkus.smallrye-health.root-path=/health
```

## Testing Overview

### Standards

- Use `@QuarkusTest` for integration tests (full CDI + HTTP stack)
- Use `@InjectMock` to mock CDI beans in integration tests
- Use `@TestSecurity(user = "test", roles = "ADMIN")` to bypass auth in tests
- Use REST-assured for HTTP endpoint assertions
- Use `@QuarkusTestResource` with Testcontainers for DB integration tests
- Test native with `./mvnw verify -Pnative` (runs `@NativeImageTest` classes)
- Use `@DisplayName` for readable test names describing behavior

### Integration Test

```java
@QuarkusTest
@DisplayName("UserResource")
class UserResourceTest {

    @Test
    @DisplayName("POST /api/v1/users - should create user")
    void shouldCreateUser() {
        given()
            .contentType(ContentType.JSON)
            .body(new UserRequest("test@example.com", "Password1!", "Test"))
        .when()
            .post("/api/v1/users")
        .then()
            .statusCode(201)
            .body("id", notNullValue())
            .body("email", equalTo("test@example.com"));
    }

    @Test
    @TestSecurity(user = "admin", roles = "ADMIN")
    @DisplayName("GET /api/v1/users - admin can list users")
    void adminCanListUsers() {
        given()
        .when()
            .get("/api/v1/users")
        .then()
            .statusCode(200);
    }
}
```

## Commands

```bash
# Create project
mvn io.quarkus.platform:quarkus-maven-plugin:3.6.0:create \
    -DprojectGroupId=com.example \
    -DprojectArtifactId=myproject \
    -Dextensions="resteasy-reactive-jackson,hibernate-reactive-panache,reactive-pg-client"

# Dev mode (live reload + Dev Services)
./mvnw quarkus:dev

# Run tests
./mvnw test

# Build JVM jar
./mvnw package

# Build native binary
./mvnw package -Pnative

# Build native in container (no local GraalVM)
./mvnw package -Pnative -Dquarkus.native.container-build=true

# Verify native (integration tests against native binary)
./mvnw verify -Pnative

# List available extensions
./mvnw quarkus:list-extensions

# Add extension
./mvnw quarkus:add-extension -Dextensions="openapi"

# Build container image
./mvnw package -Dquarkus.container-image.build=true

# Deploy to Kubernetes
./mvnw package -Dquarkus.kubernetes.deploy=true

# Lint / format
./mvnw compile           # Runs annotation processors
mvn checkstyle:check     # If checkstyle configured
```

## Best Practices Summary

### Do

- Use Dev Services for automatic local containers
- Use Panache for simpler data access patterns
- Use reactive types (`Uni`, `Multi`) for I/O-bound operations
- Use `@WithTransaction` on service methods (not resources)
- Configure for native compilation early; test regularly
- Use health checks (`@Liveness`, `@Readiness`, `@Wellness`)
- Use profile-based configuration (`%dev.`, `%test.`, `%prod.`)
- Use MapStruct (compile-time) over reflection-based mappers

### Do Not

- Mix blocking calls in reactive pipelines (use `@Blocking` annotation if needed)
- Use runtime reflection without `@RegisterForReflection`
- Hardcode configuration values (use `@ConfigProperty` or `@ConfigMapping`)
- Use synchronous JDBC APIs with reactive datasources
- Ignore native build compatibility until deployment time
- Put business logic in resource classes

## Advanced Topics

For detailed patterns and examples, see:

- [references/patterns.md](references/patterns.md) -- Reactive pipelines, Hibernate Reactive, testing strategies, GraalVM native, messaging, security, observability

## External References

- [Quarkus Documentation](https://quarkus.io/guides/)
- [Quarkus Extensions](https://quarkus.io/extensions/)
- [Panache Guide](https://quarkus.io/guides/hibernate-orm-panache)
- [RESTEasy Reactive Guide](https://quarkus.io/guides/resteasy-reactive)
- [SmallRye JWT](https://quarkus.io/guides/security-jwt)
- [Native Compilation](https://quarkus.io/guides/building-native-image)
- [Dev Services](https://quarkus.io/guides/dev-services)
- [MicroProfile Health](https://quarkus.io/guides/smallrye-health)
