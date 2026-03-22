---
name: ktor
description: |
  Ktor framework guardrails, patterns, and best practices for AI-assisted development.
  Use when working with Ktor projects, or when the user mentions Ktor.
  Provides coroutine-based routing, plugins, serialization, and server/client guidelines.
license: MIT
metadata:
  author: samuel
  version: "1.0"
  category: framework
  language: kotlin
  extensions: ".kt"
---

# Ktor Framework Guide

> Applies to: Ktor 2.x, Kotlin 1.9+, Microservices, REST APIs, WebSockets

## Overview

Ktor is a lightweight, asynchronous framework built by JetBrains for Kotlin. It leverages
coroutines for non-blocking I/O and provides a flexible plugin system for extensibility.

**Best For**: Microservices, lightweight APIs, real-time applications, Kotlin-native projects

**Key Characteristics**:
- Native Kotlin coroutines (non-blocking by default)
- Modular plugin architecture (install only what you use)
- Type-safe routing DSL
- Built-in test engine (`testApplication`)
- Multiple server engines: Netty, Jetty, CIO, Tomcat
- First-class WebSocket support
- Multiplatform HTTP client

## Core Principles

1. **Plugins Over Middleware**: Configure behavior via installable plugins, not middleware chains
2. **Coroutine-First**: All request handling is suspending; never block the event loop
3. **Type-Safe DSL**: Use Kotlin's type system for routing, configuration, and serialization
4. **Explicit Dependencies**: Wire services manually or via a lightweight DI container
5. **HOCON Configuration**: Use `application.conf` with environment variable overrides

## Project Structure

```
myapp/
├── src/main/kotlin/com/example/
│   ├── Application.kt              # Entry point, module composition
│   ├── plugins/                     # Plugin configuration (one file per plugin)
│   │   ├── Routing.kt
│   │   ├── Serialization.kt
│   │   ├── Security.kt
│   │   ├── StatusPages.kt
│   │   ├── Validation.kt
│   │   └── Databases.kt
│   ├── routes/                      # Route definitions (Route extensions)
│   │   ├── UserRoutes.kt
│   │   └── AuthRoutes.kt
│   ├── models/                      # Data models, DTOs, table definitions
│   │   ├── User.kt
│   │   └── Requests.kt
│   ├── services/                    # Business logic layer
│   │   └── UserService.kt
│   ├── repositories/                # Data access layer (Exposed)
│   │   └── UserRepository.kt
│   └── utils/                       # Utilities (JWT, hashing, etc.)
│       └── JwtUtils.kt
├── src/main/resources/
│   ├── application.conf             # HOCON configuration
│   └── logback.xml
├── src/test/kotlin/com/example/
│   ├── ApplicationTest.kt           # Integration tests with testApplication
│   └── services/UserServiceTest.kt  # Unit tests with MockK
├── build.gradle.kts
└── gradle.properties
```

**Conventions**:
- One plugin configuration per file in `plugins/`
- Routes defined as `Route` extension functions in `routes/`
- Services injected via constructor parameters (no global singletons)
- `models/` contains Exposed table objects, domain models, and serializable DTOs
- `repositories/` wraps all database access behind `suspend` functions

## Guardrails

### Application Module

- Define a single `Application.module()` that composes plugins in order
- Plugin install order matters: Serialization before Routing, StatusPages early
- Use `embeddedServer()` for simple apps, `EngineMain` for HOCON-driven startup
- Never put business logic in `Application.kt`

```kotlin
fun Application.module() {
    configureSerialization()   // ContentNegotiation first
    configureValidation()      // RequestValidation before routing
    configureSecurity()        // Authentication before protected routes
    configureStatusPages()     // Error handling catches all
    configureDatabases()       // Database connection pool
    configureRouting()         // Routes last (depends on all above)
}
```

### Configuration (HOCON)

- Use `application.conf` with environment variable overrides via `${?ENV_VAR}`
- Never hardcode secrets; always provide env var fallbacks
- Group related settings under namespaces (`database`, `jwt`, `server`)
- Access config via `environment.config.property("path").getString()`

```hocon
ktor {
    deployment { port = 8080, port = ${?PORT} }
    application { modules = [ com.example.ApplicationKt.module ] }
}
database {
    url = "jdbc:postgresql://localhost:5432/myapp"
    url = ${?DATABASE_URL}
    driver = "org.postgresql.Driver"
    user = ${?DATABASE_USER}
    password = ${?DATABASE_PASSWORD}
    maxPoolSize = 10
}
jwt {
    secret = ${?JWT_SECRET}
    issuer = "myapp"
    audience = "myapp-users"
    realm = "myapp"
    expirationMs = 3600000
}
```

### Serialization

- Use `kotlinx.serialization` with `ContentNegotiation` plugin
- Configure lenient parsing and unknown key ignoring for forward compatibility
- All DTOs must be `@Serializable` data classes
- Separate request DTOs from response DTOs from domain models

```kotlin
fun Application.configureSerialization() {
    install(ContentNegotiation) {
        json(Json {
            prettyPrint = false          // disable in production
            isLenient = true
            ignoreUnknownKeys = true
            encodeDefaults = true
        })
    }
}
```

### Routing

- Define routes as `Route` extension functions (not inline in `configureRouting`)
- Group routes under versioned prefixes (`/api/v1/...`)
- Use `authenticate("scheme")` blocks to protect routes
- Parse path/query parameters with null-safe handling and validation
- Return appropriate HTTP status codes (`Created`, `NoContent`, `BadRequest`)

```kotlin
fun Route.userRoutes(userService: UserService) {
    route("/users") {
        post {
            val request = call.receive<CreateUserRequest>()
            val user = userService.createUser(request)
            call.respond(HttpStatusCode.Created, user)
        }
        authenticate("auth-jwt") {
            get {
                val limit = call.parameters["limit"]?.toIntOrNull() ?: 20
                val offset = call.parameters["offset"]?.toLongOrNull() ?: 0
                call.respond(userService.getAllUsers(limit, offset))
            }
            get("/{id}") {
                val id = call.parameters["id"]?.toLongOrNull()
                    ?: return@get call.respond(HttpStatusCode.BadRequest, "Invalid ID")
                call.respond(userService.getUserById(id))
            }
        }
    }
}
```

### Request Validation

- Install `RequestValidation` plugin for declarative input validation
- Validate all request DTOs before they reach service layer
- Return structured error messages via `ValidationResult.Invalid`
- Handle `RequestValidationException` in StatusPages

```kotlin
fun Application.configureValidation() {
    install(RequestValidation) {
        validate<CreateUserRequest> { req ->
            val errors = buildList {
                if (!req.email.contains("@")) add("Invalid email format")
                if (req.password.length < 8) add("Password must be at least 8 characters")
                if (req.name.isBlank()) add("Name is required")
            }
            if (errors.isNotEmpty()) ValidationResult.Invalid(errors)
            else ValidationResult.Valid
        }
    }
}
```

### Authentication (JWT)

- Use `Authentication` plugin with named JWT schemes
- Validate claims in the `validate` block; return `null` to reject
- Return structured error in `challenge` block (not raw strings)
- Extract claims from `JWTPrincipal` in routes, never parse tokens manually

```kotlin
fun Application.configureSecurity() {
    val config = environment.config
    install(Authentication) {
        jwt("auth-jwt") {
            realm = config.property("jwt.realm").getString()
            verifier(JWT.require(Algorithm.HMAC256(config.property("jwt.secret").getString()))
                .withAudience(config.property("jwt.audience").getString())
                .withIssuer(config.property("jwt.issuer").getString())
                .build())
            validate { credential ->
                val userId = credential.payload.getClaim("userId").asString()
                if (userId != null) JWTPrincipal(credential.payload) else null
            }
            challenge { _, _ ->
                call.respond(HttpStatusCode.Unauthorized,
                    ErrorResponse(401, "UNAUTHORIZED", "Token is not valid or has expired"))
            }
        }
    }
}
```

### Error Handling (StatusPages)

- Install `StatusPages` plugin to centralize exception-to-response mapping
- Define custom exception hierarchy (sealed class or separate classes)
- Never expose internal exception details to clients
- Always include a catch-all `Throwable` handler that logs and returns 500

```kotlin
@Serializable
data class ErrorResponse(val status: Int, val error: String, val message: String)

class NotFoundException(message: String) : RuntimeException(message)
class ConflictException(message: String) : RuntimeException(message)

fun Application.configureStatusPages() {
    install(StatusPages) {
        exception<NotFoundException> { call, cause ->
            call.respond(HttpStatusCode.NotFound,
                ErrorResponse(404, "NOT_FOUND", cause.message ?: "Resource not found"))
        }
        exception<RequestValidationException> { call, cause ->
            call.respond(HttpStatusCode.BadRequest,
                ErrorResponse(400, "VALIDATION_ERROR", cause.reasons.joinToString("; ")))
        }
        exception<Throwable> { call, cause ->
            call.application.environment.log.error("Unhandled exception", cause)
            call.respond(HttpStatusCode.InternalServerError,
                ErrorResponse(500, "INTERNAL_ERROR", "An unexpected error occurred"))
        }
    }
}
```

### Database (Exposed ORM)

- Use HikariCP connection pool with `newSuspendedTransaction` for coroutine safety
- Define tables as `object : LongIdTable("name")` in `models/`
- Wrap all DB calls in a `suspend dbQuery` helper
- Separate domain models from Exposed `ResultRow` mapping
- Use `SchemaUtils.create()` for dev; prefer migrations for production

```kotlin
// Repository pattern with suspend functions
class UserRepository {
    private suspend fun <T> dbQuery(block: suspend () -> T): T =
        newSuspendedTransaction { block() }

    suspend fun findById(id: Long): User? = dbQuery {
        Users.select { Users.id eq id }.map(User::fromRow).singleOrNull()
    }

    suspend fun create(email: String, passwordHash: String, name: String): User = dbQuery {
        val id = Users.insertAndGetId {
            it[Users.email] = email
            it[Users.passwordHash] = passwordHash
            it[Users.name] = name
        }
        Users.select { Users.id eq id }.map(User::fromRow).single()
    }
}
```

### Service Layer

- Services receive repositories and utilities via constructor injection
- All public methods are `suspend` functions
- Throw domain exceptions (`NotFoundException`, `ConflictException`), not generic ones
- Services contain business logic; repositories contain data access only

### Coroutine Safety

- Never call blocking I/O without `withContext(Dispatchers.IO)`
- Use `withTimeout` for external service calls
- Handle `CancellationException` correctly (rethrow, never swallow)
- Use `supervisorScope` when child failures should not cancel siblings

## Testing

### Integration Tests (testApplication)

```kotlin
class ApplicationTest {
    @Test
    fun `create user returns 201`() = testApplication {
        application { module() }
        val client = createClient {
            install(ContentNegotiation) { json() }
        }
        val response = client.post("/api/users") {
            contentType(ContentType.Application.Json)
            setBody(CreateUserRequest("test@example.com", "password123", "Test"))
        }
        assertEquals(HttpStatusCode.Created, response.status)
    }
}
```

### Unit Tests (MockK)

```kotlin
class UserServiceTest {
    private val repo = mockk<UserRepository>()
    private val jwt = mockk<JwtUtils>()
    private val service = UserService(repo, jwt)

    @Test
    fun `createUser with existing email throws ConflictException`() = runBlocking {
        coEvery { repo.existsByEmail(any()) } returns true
        assertFailsWith<ConflictException> {
            service.createUser(CreateUserRequest("dup@test.com", "pass1234", "Dup"))
        }
    }

    @AfterTest fun teardown() { clearAllMocks() }
}
```

### Testing Standards

- Use `testApplication` for HTTP-level integration tests
- Use MockK with `coEvery`/`coVerify` for coroutine-aware mocking
- Test names describe behavior: `create user with duplicate email throws ConflictException`
- Use H2 in-memory database for integration tests
- Coverage target: >80% for services, >60% overall

## Commands

```bash
# Development
./gradlew run                              # Start dev server
./gradlew run -t                           # Auto-reload on changes

# Build
./gradlew build                            # Compile + test + check
./gradlew buildFatJar                      # Build executable fat JAR
java -jar build/libs/app.jar               # Run production JAR

# Test
./gradlew test                             # Run all tests
./gradlew test --tests "*.UserServiceTest" # Specific test class
./gradlew test --tests "*create user*"     # Tests matching pattern

# Quality
./gradlew ktlintCheck                      # Check formatting
./gradlew ktlintFormat                     # Auto-fix formatting
./gradlew detekt                           # Static analysis

# Dependencies
./gradlew dependencies                     # Full dependency tree
./gradlew clean                            # Clean build artifacts
```

## Do's and Don'ts

### Do
- Configure plugins in separate files under `plugins/`
- Use `suspend` functions for all database and external calls
- Use Route extension functions to define typed routes
- Use `kotlinx.serialization` for JSON (not Jackson/Gson)
- Use `newSuspendedTransaction` for coroutine-safe DB access
- Handle errors centrally with StatusPages
- Use `application.conf` with env var overrides
- Inject dependencies via constructor parameters

### Don't
- Block coroutines with synchronous I/O calls
- Use global mutable state without synchronization
- Expose internal exception messages to API clients
- Hardcode configuration values in source code
- Skip request validation on any user-facing endpoint
- Mix business logic into route handlers
- Use `GlobalScope` for request-scoped work
- Install plugins inside route blocks

## When to Use Ktor

**Choose Ktor when**: building lightweight microservices, Kotlin is your primary language,
you need fast startup times, you want fine-grained control over dependencies, building
real-time applications (WebSockets), or creating serverless functions.

**Consider alternatives when**: you need extensive enterprise integrations (Spring Boot),
team is more familiar with Spring, project requires complex security configurations, or
you need a large third-party library ecosystem.

## References

For detailed patterns, examples, and advanced topics, see:

- [references/patterns.md](references/patterns.md) -- Database integration, WebSocket patterns, testing strategies, deployment, Ktor client

## External References

- [Ktor Documentation](https://ktor.io/docs/welcome.html)
- [Ktor Server Plugins](https://ktor.io/docs/plugins.html)
- [Exposed ORM](https://github.com/JetBrains/Exposed)
- [kotlinx.serialization](https://github.com/Kotlin/kotlinx.serialization)
- [MockK](https://mockk.io/)
- [HikariCP](https://github.com/brettwooldridge/HikariCP)
- [Kotlin Coroutines](https://kotlinlang.org/docs/coroutines-guide.html)
