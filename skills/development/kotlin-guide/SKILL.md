---
name: kotlin-guide
description: |
  Kotlin language guardrails, patterns, and best practices for AI-assisted development.
  Use when working with Kotlin files (.kt, .kts), build.gradle.kts, or when the user mentions Kotlin.
  Provides null safety patterns, coroutine guidelines, data class conventions,
  and testing standards specific to this project's coding standards.
license: MIT
metadata:
  author: samuel
  version: "1.0"
  category: language
  language: kotlin
  extensions: ".kt,.kts"
---

# Kotlin Guide

> Applies to: Kotlin 1.9+, JVM 17+, Coroutines, Android, Server-side

## Core Principles

1. **Null Safety**: Leverage the type system to eliminate null pointer exceptions at compile time
2. **Conciseness**: Use data classes, scope functions, and destructuring to reduce boilerplate
3. **Coroutines for Concurrency**: Structured concurrency with coroutines, not raw threads
4. **Immutability by Default**: Prefer `val` over `var`, immutable collections over mutable
5. **Interop Awareness**: Write Kotlin-idiomatic code while maintaining clean Java interop boundaries

## Guardrails

### Version & Dependencies

- Use Kotlin 1.9+ with Gradle Kotlin DSL (`build.gradle.kts`)
- Target JVM 17+ for server-side, match Android minSdk for mobile
- Pin Kotlin and kotlinx library versions together (BOM alignment)
- Run `./gradlew dependencies` to audit transitive dependencies

### Code Style

- Run `ktlint` before every commit (format + check)
- Run `detekt` for static analysis (complexity, code smells)
- Packages: lowercase, no underscores (`com.example.userservice`)
- Classes: `PascalCase` | Functions/properties: `camelCase` | Constants: `SCREAMING_SNAKE_CASE`
- Follow [Kotlin Coding Conventions](https://kotlinlang.org/docs/coding-conventions.html)

### Null Safety

- Never use `!!` (not-null assertion) in production code
- Use safe calls (`?.`), elvis (`?:`), and smart casts instead
- Nullable types only at API boundaries (deserialization, Java interop)
- Prefer `requireNotNull()` or `checkNotNull()` with meaningful messages over `!!`
- Use `?.let { }` for nullable transformations, not nested `if` checks

```kotlin
// BAD: crashes at runtime
val length = name!!.length

// GOOD: safe call with fallback
val length = name?.length ?: 0

// GOOD: explicit contract with clear error
val validName = requireNotNull(name) { "User name must not be null for ID=$id" }
```

### Coroutines

- Always use structured concurrency (`coroutineScope`, `supervisorScope`)
- Never use `GlobalScope` in production code
- Use `withContext(Dispatchers.IO)` for blocking I/O operations
- Always handle `CancellationException` correctly (rethrow, never swallow)
- Set timeouts with `withTimeout` or `withTimeoutOrNull` for external calls

```kotlin
// BAD: unstructured, leaks coroutines
GlobalScope.launch { fetchData() }

// GOOD: structured concurrency, respects parent lifecycle
coroutineScope {
    val user = async { userService.getUser(id) }
    val orders = async { orderService.getOrders(id) }
    UserWithOrders(user.await(), orders.await())
}
```

### Extension Functions

- Use extension functions to add behavior, not to bypass access control
- Keep extensions in a dedicated file (`StringExtensions.kt`, `DateExtensions.kt`)
- Do not add extensions to `Any` or overly generic types
- Prefer member functions for core behavior, extensions for utility/convenience
- Document extensions with `@receiver` KDoc tag when purpose is not obvious

## Project Structure

```
myproject/
├── app/                          # Application module or main entry
│   └── src/main/kotlin/
├── domain/                       # Business logic, entities, use cases
│   └── src/main/kotlin/
│       └── com/example/domain/
│           ├── model/            # Data classes, sealed classes
│           ├── repository/       # Repository interfaces
│           └── usecase/          # Business operations
├── data/                         # Data layer implementations
│   └── src/main/kotlin/
│       └── com/example/data/
│           ├── repository/       # Repository implementations
│           ├── remote/           # API clients, DTOs
│           └── local/            # Database, DAOs
├── presentation/                 # UI or API controllers
├── build.gradle.kts
├── settings.gradle.kts
└── gradle.properties
```

- `domain/` has zero framework dependencies (pure Kotlin)
- `data/` depends on `domain/`, implements repository interfaces
- `presentation/` depends on `domain/`, never imports from `data/` directly
- No circular module dependencies

## Key Patterns

### Data Classes & Value Classes

```kotlin
data class User(
    val id: UserId,
    val email: Email,
    val name: String,
    val role: Role = Role.VIEWER,
) {
    init {
        require(name.isNotBlank()) { "User name must not be blank" }
    }
}

// Value classes for type-safe IDs (zero runtime overhead)
@JvmInline
value class UserId(val value: String) {
    init { require(value.isNotBlank()) { "UserId must not be blank" } }
}
```

### Sealed Classes & Interfaces

```kotlin
sealed interface Result<out T> {
    data class Success<T>(val data: T) : Result<T>
    data class Failure(val error: AppError) : Result<Nothing>
}

sealed class AppError(val message: String) {
    data class NotFound(val resource: String, val id: String) :
        AppError("$resource with ID $id not found")
    data class Validation(val field: String, val reason: String) :
        AppError("Validation failed for $field: $reason")
    data class Unauthorized(val detail: String = "Authentication required") :
        AppError(detail)
}

// Exhaustive when expressions
fun <T> Result<T>.getOrThrow(): T = when (this) {
    is Result.Success -> data
    is Result.Failure -> throw error.toException()
}
```

### Scope Functions Quick Reference

| Function | Context | Returns | Use for |
|----------|---------|---------|---------|
| `let` | `it` | Lambda result | Nullable transforms, scoped vars |
| `run` | `this` | Lambda result | Compute value using object context |
| `with` | `this` | Lambda result | Operate on non-null object |
| `apply` | `this` | Object itself | Configure/build an object |
| `also` | `it` | Object itself | Side effects (logging, events) |

```kotlin
// apply: configure and return the object
val request = HttpRequest.Builder().apply {
    url(endpoint)
    header("Authorization", "Bearer $token")
    timeout(Duration.ofSeconds(30))
}.build()

// also: side effects without modifying the chain
val savedUser = userRepository.save(newUser).also { user ->
    logger.info("Created user: ${user.id}")
}
```

## Testing

### Standards

- Test files: `*Test.kt` in `src/test/kotlin/` (mirror source package)
- Use JUnit 5 with `@Test`, `@Nested`, `@DisplayName`
- Use MockK for mocking (idiomatic Kotlin, supports coroutines)
- Table-driven style with `@ParameterizedTest` and `@MethodSource`
- Coverage target: >80% for business logic, >60% overall
- Use `runTest` from `kotlinx-coroutines-test` for coroutine tests

### Unit Test Pattern

```kotlin
class UserServiceTest {
    private val userRepository = mockk<UserRepository>()
    private val eventBus = mockk<EventBus>(relaxed = true)
    private val service = UserService(userRepository, eventBus)

    @Nested
    @DisplayName("createUser")
    inner class CreateUser {
        @Test
        fun `creates user with valid input`() = runTest {
            coEvery { userRepository.save(any()) } returns mockUser
            val result = service.createUser(validInput)

            assertThat(result).isInstanceOf(Result.Success::class.java)
            coVerify { userRepository.save(any()) }
            coVerify { eventBus.publish(any<UserCreatedEvent>()) }
        }

        @Test
        fun `fails with blank name`() = runTest {
            val result = service.createUser(blankNameInput)

            assertThat(result).isInstanceOf(Result.Failure::class.java)
            coVerify(exactly = 0) { userRepository.save(any()) }
        }
    }
}
```

### Parameterized Tests

```kotlin
companion object {
    @JvmStatic
    fun emailCases() = listOf(
        Arguments.of("user@example.com", true),
        Arguments.of("invalid-email", false),
        Arguments.of("", false),
    )
}

@ParameterizedTest(name = "email \"{0}\" valid={1}")
@MethodSource("emailCases")
fun `validates email format`(email: String, expected: Boolean) {
    val result = runCatching { Email(email) }
    assertThat(result.isSuccess).isEqualTo(expected)
}
```

## Tooling

### Essential Commands

```bash
./gradlew build                    # Compile + test + check
./gradlew test                     # Run all tests
./gradlew test --tests "*.UserServiceTest"  # Specific test class
./gradlew koverReport              # Coverage report
./gradlew ktlintCheck              # Check formatting
./gradlew ktlintFormat             # Auto-fix formatting
./gradlew detekt                   # Static analysis
./gradlew dependencies             # Dependency tree
```

### Gradle Kotlin DSL Configuration

```kotlin
// build.gradle.kts
plugins {
    kotlin("jvm") version "1.9.22"
    id("org.jlleitschuh.gradle.ktlint") version "12.1.0"
    id("io.gitlab.arturbosch.detekt") version "1.23.4"
    id("org.jetbrains.kotlinx.kover") version "0.7.5"
}

kotlin { jvmToolchain(17) }

dependencies {
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-core:1.8.0")
    implementation("org.jetbrains.kotlinx:kotlinx-serialization-json:1.6.2")
    testImplementation(kotlin("test"))
    testImplementation("io.mockk:mockk:1.13.9")
    testImplementation("org.jetbrains.kotlinx:kotlinx-coroutines-test:1.8.0")
    testImplementation("org.assertj:assertj-core:3.25.1")
}

detekt {
    config.setFrom("detekt.yml")
    buildUponDefaultConfig = true
}

kover {
    verify { rule { minBound(80) } }
}
```

### Detekt Configuration

```yaml
# detekt.yml
complexity:
  LongMethod:
    threshold: 50
  CyclomaticComplexMethod:
    threshold: 10
  LargeClass:
    threshold: 300
  LongParameterList:
    functionThreshold: 5
    constructorThreshold: 8
style:
  ForbiddenComment:
    values:
      - "TODO(?!\\(#\\d+\\))" # TODOs require issue reference
  MagicNumber:
    ignoreNumbers: ["-1", "0", "1", "2"]
  MaxLineLength:
    maxLineLength: 120
potential-bugs:
  UnsafeCast:
    active: true
```

## References

For detailed patterns and examples, see:

- [references/patterns.md](references/patterns.md) -- Coroutine patterns, sealed class hierarchies, DSL builders, Flow patterns

## External References

- [Kotlin Coding Conventions](https://kotlinlang.org/docs/coding-conventions.html)
- [Kotlin Coroutines Guide](https://kotlinlang.org/docs/coroutines-guide.html)
- [MockK Documentation](https://mockk.io/)
- [ktlint](https://pinterest.github.io/ktlint/)
- [detekt](https://detekt.dev/)
- [Kover Coverage](https://github.com/Kotlin/kotlinx-kover)
- [Arrow (Functional Kotlin)](https://arrow-kt.io/)
