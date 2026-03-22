---
name: spring-boot-kotlin
description: |
  Spring Boot with Kotlin framework guardrails, patterns, and best practices.
  Use when working with Spring Boot Kotlin projects, or when the user mentions Spring Boot with Kotlin.
  Provides coroutine patterns, WebFlux, JPA, security, and idiomatic Kotlin-Spring guidelines.
license: MIT
metadata:
  author: samuel
  version: "1.0"
  category: framework
  language: kotlin
  extensions: ".kt"
---

# Spring Boot (Kotlin) Framework Guide

> Applies to: Spring Boot 3.x, Kotlin 1.9+, REST APIs, Microservices
> Use with: `.claude/skills/kotlin-guide/SKILL.md` for base Kotlin patterns

## When to Use

- **Enterprise Applications**: Proven enterprise-grade framework with vast ecosystem
- **Microservices**: Excellent with Spring Cloud for distributed systems
- **Existing Spring Ecosystem**: Leverage Spring libraries, security, data, cloud
- **Complex Business Logic**: Rich feature set for complex domains
- **Team Familiarity**: Teams with Java/Spring background transitioning to Kotlin

## When NOT to Use

- **Lightweight Services**: Consider Ktor for simpler, minimal-dependency services
- **Mobile Backend**: Ktor is more lightweight for mobile-only backends
- **Minimal Footprint**: Spring Boot has a larger memory and startup footprint

## Project Structure

```
myproject/
├── build.gradle.kts
├── settings.gradle.kts
├── src/
│   ├── main/
│   │   ├── kotlin/com/example/myproject/
│   │   │   ├── MyProjectApplication.kt
│   │   │   ├── config/
│   │   │   │   ├── SecurityConfig.kt
│   │   │   │   ├── WebConfig.kt
│   │   │   │   └── JwtProperties.kt
│   │   │   ├── controller/
│   │   │   │   └── UserController.kt
│   │   │   ├── service/
│   │   │   │   └── UserService.kt
│   │   │   ├── repository/
│   │   │   │   └── UserRepository.kt
│   │   │   ├── model/
│   │   │   │   ├── entity/User.kt
│   │   │   │   └── dto/UserDto.kt
│   │   │   ├── exception/
│   │   │   │   ├── GlobalExceptionHandler.kt
│   │   │   │   └── Exceptions.kt
│   │   │   └── security/
│   │   │       ├── JwtService.kt
│   │   │       ├── JwtAuthenticationFilter.kt
│   │   │       └── CurrentUser.kt
│   │   └── resources/
│   │       ├── application.yml
│   │       ├── application-dev.yml
│   │       └── db/migration/
│   └── test/kotlin/com/example/myproject/
│       ├── controller/
│       ├── service/
│       └── integration/
└── README.md
```

## Guardrails

### Spring-Kotlin Specific

- Use constructor injection (Kotlin default, no `@Autowired` needed)
- Never use `lateinit var` for dependencies -- constructor injection is idiomatic
- Use `@Transactional(readOnly = true)` for all read-only operations
- Use `@Valid` on all request body parameters for automatic validation
- Use Spring profiles (`application-{profile}.yml`) for environment config
- Never hardcode secrets in config files -- use `${ENV_VAR:default}` syntax
- Use `@ConfigurationProperties` data classes for type-safe configuration
- Prefer Kotlin data classes for DTOs with `@field:` annotation target for validation
- Use `open` modifier or `plugin.spring` (auto-opens `@Component` classes)

### Entity Design

- Use `data class` for JPA entities with `plugin.jpa` (auto-generates no-arg constructors)
- Prefer `val` for entity properties, use `copy()` for updates
- Use UUID or auto-generated IDs; nullable `val id: UUID? = null` for new entities
- Use `@CreationTimestamp` and `@UpdateTimestamp` for audit fields
- Keep entities in `model/entity/`, DTOs in `model/dto/`

### Service Layer

- Mark all service classes with `@Service`
- Use `@Transactional` for write operations, `@Transactional(readOnly = true)` for reads
- Throw domain-specific exceptions (`NotFoundException`, `ConflictException`)
- Return DTOs from services, never expose entities to controllers
- Use Kotlin null safety: repository methods return `T?` for nullable finds

### Controller Layer

- Use `@RestController` with `@RequestMapping` for base paths
- Return `ResponseEntity<T>` with explicit status codes
- Use `@Valid @RequestBody` for all incoming request bodies
- Use `@PreAuthorize` for method-level security
- Use `@PageableDefault` for pagination parameters

## Key Patterns

### Application Entry Point

```kotlin
@SpringBootApplication
class MyProjectApplication

fun main(args: Array<String>) {
    runApplication<MyProjectApplication>(*args)
}
```

### Type-Safe Configuration

```kotlin
@ConfigurationProperties(prefix = "jwt")
data class JwtProperties(
    val secret: String,
    val expiration: Long,
)
```

```yaml
# application.yml
jwt:
  secret: ${JWT_SECRET:your-256-bit-secret-key-here}
  expiration: 86400000
```

### Entity with Data Class

```kotlin
@Entity
@Table(name = "users")
data class User(
    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    val id: UUID? = null,

    @Column(unique = true, nullable = false)
    val email: String,

    @Column(nullable = false)
    val passwordHash: String,

    @Column(nullable = false)
    val name: String,

    @Column(nullable = false)
    val role: String = "USER",

    @CreationTimestamp
    @Column(updatable = false)
    val createdAt: Instant? = null,

    @UpdateTimestamp
    val updatedAt: Instant? = null,
)
```

### DTO with Validation

```kotlin
data class CreateUserRequest(
    @field:NotBlank(message = "Email is required")
    @field:Email(message = "Invalid email format")
    val email: String,

    @field:NotBlank(message = "Password is required")
    @field:Size(min = 8, message = "Password must be at least 8 characters")
    val password: String,

    @field:NotBlank(message = "Name is required")
    @field:Size(min = 1, max = 100)
    val name: String,
)

data class UserResponse(
    val id: UUID,
    val email: String,
    val name: String,
    val role: String,
    val createdAt: Instant,
) {
    companion object {
        fun from(user: User): UserResponse = UserResponse(
            id = user.id!!,
            email = user.email,
            name = user.name,
            role = user.role,
            createdAt = user.createdAt!!,
        )
    }
}
```

### Repository

```kotlin
@Repository
interface UserRepository : JpaRepository<User, UUID> {
    fun findByEmail(email: String): User?
    fun existsByEmail(email: String): Boolean
}
```

### Service

```kotlin
@Service
class UserService(
    private val userRepository: UserRepository,
    private val passwordEncoder: PasswordEncoder,
) {
    @Transactional
    fun createUser(request: CreateUserRequest): UserResponse {
        if (userRepository.existsByEmail(request.email)) {
            throw ConflictException("Email already registered")
        }
        val user = User(
            email = request.email,
            passwordHash = passwordEncoder.encode(request.password),
            name = request.name,
        )
        return UserResponse.from(userRepository.save(user))
    }

    @Transactional(readOnly = true)
    fun getUserById(id: UUID): UserResponse {
        val user = userRepository.findById(id)
            .orElseThrow { NotFoundException("User not found: $id") }
        return UserResponse.from(user)
    }

    @Transactional
    fun updateUser(id: UUID, request: UpdateUserRequest): UserResponse {
        val user = userRepository.findById(id)
            .orElseThrow { NotFoundException("User not found: $id") }
        val updated = user.copy(
            name = request.name ?: user.name,
            email = request.email ?: user.email,
        )
        return UserResponse.from(userRepository.save(updated))
    }
}
```

### Controller

```kotlin
@RestController
@RequestMapping("/api")
class UserController(
    private val userService: UserService,
) {
    @PostMapping("/register")
    fun register(
        @Valid @RequestBody request: CreateUserRequest,
    ): ResponseEntity<UserResponse> {
        val user = userService.createUser(request)
        return ResponseEntity.status(HttpStatus.CREATED).body(user)
    }

    @GetMapping("/users/{id}")
    @PreAuthorize("hasRole('ADMIN') or @userSecurity.isOwner(#id, authentication)")
    fun getUser(@PathVariable id: UUID): ResponseEntity<UserResponse> {
        return ResponseEntity.ok(userService.getUserById(id))
    }

    @GetMapping("/users")
    @PreAuthorize("hasRole('ADMIN')")
    fun getAllUsers(
        @PageableDefault(size = 20) pageable: Pageable,
    ): ResponseEntity<Page<UserResponse>> {
        return ResponseEntity.ok(userService.getAllUsers(pageable))
    }
}
```

### Exception Handling

```kotlin
class NotFoundException(message: String) : RuntimeException(message)
class UnauthorizedException(message: String) : RuntimeException(message)
class ConflictException(message: String) : RuntimeException(message)

data class ErrorResponse(
    val timestamp: Instant = Instant.now(),
    val status: Int,
    val error: String,
    val message: String,
    val details: List<String>? = null,
)

@RestControllerAdvice
class GlobalExceptionHandler {
    @ExceptionHandler(NotFoundException::class)
    fun handleNotFound(ex: NotFoundException) = ResponseEntity
        .status(HttpStatus.NOT_FOUND)
        .body(ErrorResponse(status = 404, error = "NOT_FOUND", message = ex.message ?: "Not found"))

    @ExceptionHandler(MethodArgumentNotValidException::class)
    fun handleValidation(ex: MethodArgumentNotValidException): ResponseEntity<ErrorResponse> {
        val details = ex.bindingResult.fieldErrors.map { "${it.field}: ${it.defaultMessage}" }
        return ResponseEntity.status(HttpStatus.BAD_REQUEST)
            .body(ErrorResponse(status = 400, error = "VALIDATION_ERROR", message = "Validation failed", details = details))
    }
}
```

### Security Configuration

```kotlin
@Configuration
@EnableWebSecurity
@EnableMethodSecurity
class SecurityConfig(
    private val jwtAuthenticationFilter: JwtAuthenticationFilter,
) {
    @Bean
    fun securityFilterChain(http: HttpSecurity): SecurityFilterChain = http
        .csrf { it.disable() }
        .sessionManagement { it.sessionCreationPolicy(SessionCreationPolicy.STATELESS) }
        .authorizeHttpRequests { auth ->
            auth
                .requestMatchers("/api/register", "/api/login").permitAll()
                .requestMatchers("/health/**", "/actuator/**").permitAll()
                .anyRequest().authenticated()
        }
        .addFilterBefore(jwtAuthenticationFilter, UsernamePasswordAuthenticationFilter::class.java)
        .build()

    @Bean
    fun passwordEncoder(): PasswordEncoder = BCryptPasswordEncoder(12)
}
```

### Custom Annotation for Current User

```kotlin
@Target(AnnotationTarget.VALUE_PARAMETER)
@Retention(AnnotationRetention.RUNTIME)
@AuthenticationPrincipal
annotation class CurrentUser
```

## Coroutines Integration

Spring Boot supports Kotlin coroutines in controllers and services. Add these dependencies:

```kotlin
implementation("org.jetbrains.kotlinx:kotlinx-coroutines-core")
implementation("org.jetbrains.kotlinx:kotlinx-coroutines-reactor")
```

Suspend functions in controllers are automatically handled by Spring WebFlux:

```kotlin
@GetMapping("/users/{id}")
suspend fun getUser(@PathVariable id: UUID): ResponseEntity<UserResponse> {
    val user = userService.getUserById(id)
    return ResponseEntity.ok(user)
}
```

For detailed coroutine, WebFlux, testing, and advanced security patterns, see [references/patterns.md](references/patterns.md).

## Commands

```bash
# Development
./gradlew bootRun

# Build
./gradlew build

# Test
./gradlew test

# Test with coverage
./gradlew test jacocoTestReport

# Format (with ktlint)
./gradlew ktlintFormat

# Lint
./gradlew ktlintCheck

# Build JAR
./gradlew bootJar

# Run JAR
java -jar build/libs/myproject-0.0.1-SNAPSHOT.jar

# Docker build
docker build -t myproject .
```

## Best Practices

### DO

- Use data classes for DTOs and entities
- Use Kotlin null safety features (`?.`, `?:`, `requireNotNull`)
- Use `@Transactional(readOnly = true)` for read operations
- Use constructor injection (default in Kotlin)
- Use `@Valid` for request validation
- Use Spring profiles for environment configuration
- Use `@field:` annotation target for validation annotations on data class properties
- Use coroutines for async operations where beneficial

### DON'T

- Use `lateinit var` for dependencies (use constructor injection)
- Ignore null safety in Spring Data repositories
- Use `!!` operator without proper null checks
- Mix reactive and blocking code in the same call chain
- Store secrets in configuration files
- Expose JPA entities directly in controller responses

## References

For detailed patterns and examples, see:

- [references/patterns.md](references/patterns.md) -- WebFlux reactive patterns, JPA advanced patterns, testing, security advanced patterns

## External References

- [Spring Boot Documentation](https://docs.spring.io/spring-boot/docs/current/reference/html/)
- [Spring Kotlin Support](https://docs.spring.io/spring-framework/reference/languages/kotlin.html)
- [Spring Security](https://docs.spring.io/spring-security/reference/index.html)
- [Spring Data JPA](https://docs.spring.io/spring-data/jpa/docs/current/reference/html/)
- [Kotlin + Spring Boot Guide](https://spring.io/guides/tutorials/spring-boot-kotlin/)
