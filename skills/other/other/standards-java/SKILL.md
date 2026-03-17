---
name: standards-java
description: Java coding standards for enterprise applications. Includes naming conventions, modern Java features, design patterns, and recommended tooling.
type: context
applies_to: [java, maven, gradle, junit, spring, jakarta, quarkus, mockito, testcontainers, hibernate, jpa]
file_extensions: [".java"]
---

# Java Coding Standards

## Core Principles

1. **Simplicity**: Simple, understandable code
2. **Readability**: Readability over cleverness
3. **Maintainability**: Code that's easy to maintain
4. **Testability**: Code that's easy to test
5. **SOLID**: Follow SOLID principles for object-oriented design
6. **DRY**: Don't Repeat Yourself - but don't overdo it

## General Rules

- **Early Returns**: Use early returns to avoid nesting
- **Descriptive Names**: Meaningful names for classes, methods, and variables
- **Minimal Changes**: Only change relevant code parts
- **No Over-Engineering**: No unnecessary complexity
- **Immutability**: Prefer immutable objects where possible
- **Minimal Comments**: Code should be self-explanatory. No redundant comments!

## Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Classes | PascalCase | `UserService`, `OrderRepository` |
| Interfaces | PascalCase | `UserRepository`, `PaymentProcessor` |
| Methods | camelCase | `getUserById`, `calculateTotal` |
| Variables | camelCase | `firstName`, `totalAmount` |
| Constants | UPPER_SNAKE_CASE | `MAX_RETRY_COUNT`, `DEFAULT_TIMEOUT` |
| Packages | lowercase.dot.separated | `com.example.service`, `com.example.repository` |
| Test Classes | ClassNameTest | `UserServiceTest`, `OrderRepositoryTest` |
| Test Methods | descriptive_snake_case or camelCase | `shouldReturnUserWhenIdExists` |

## Project Structure

### Maven Project
```
myproject/
├── pom.xml
├── src/
│   ├── main/
│   │   ├── java/
│   │   │   └── com/example/myapp/
│   │   │       ├── Application.java        # Main entry point
│   │   │       ├── config/
│   │   │       │   └── AppConfig.java      # Configuration
│   │   │       ├── domain/
│   │   │       │   └── User.java           # Domain models
│   │   │       ├── repository/
│   │   │       │   └── UserRepository.java # Data access
│   │   │       ├── service/
│   │   │       │   └── UserService.java    # Business logic
│   │   │       └── controller/
│   │   │           └── UserController.java # REST endpoints
│   │   └── resources/
│   │       ├── application.properties
│   │       └── application-dev.properties
│   └── test/
│       ├── java/
│       │   └── com/example/myapp/
│       │       ├── service/
│       │       │   └── UserServiceTest.java
│       │       └── repository/
│       │           └── UserRepositoryTest.java
│       └── resources/
│           └── application-test.properties
└── README.md
```

### Gradle Project
```
myproject/
├── build.gradle or build.gradle.kts
├── settings.gradle or settings.gradle.kts
├── src/
│   ├── main/
│   │   └── java/...      # Same structure as Maven
│   └── test/
│       └── java/...      # Same structure as Maven
└── README.md
```

## Modern Java Features

> **Recommended:** Use the latest LTS for new projects (currently Java 21 or Java 25).

### Java 17 Features

#### Records (Immutable Data)
```java
// Replace verbose POJOs with records
public record User(String id, String name, String email) {
    // Compact constructor for validation
    public User {
        if (name == null || name.isBlank()) {
            throw new IllegalArgumentException("Name cannot be blank");
        }
    }

    // Custom methods allowed
    public String displayName() {
        return name.toUpperCase();
    }
}

// Usage
var user = new User("1", "John Doe", "john@example.com");
System.out.println(user.name()); // Auto-generated accessor
```

#### Sealed Classes (Restricted Hierarchies)
```java
// Define closed set of subclasses
public sealed interface Result<T>
    permits Success, Failure {
}

public record Success<T>(T value) implements Result<T> {}
public record Failure<T>(String error) implements Result<T> {}

// Pattern matching exhaustiveness
public <T> void handleResult(Result<T> result) {
    switch (result) {
        case Success<T> s -> System.out.println("Success: " + s.value());
        case Failure<T> f -> System.out.println("Error: " + f.error());
        // No default needed - compiler knows all cases
    }
}
```

#### Pattern Matching (instanceof)
```java
// Old way
if (obj instanceof String) {
    String s = (String) obj;
    System.out.println(s.toUpperCase());
}

// Modern way - pattern matching
if (obj instanceof String s) {
    System.out.println(s.toUpperCase());
}

// Pattern matching in switch
public String formatValue(Object obj) {
    return switch (obj) {
        case Integer i -> "Number: " + i;
        case String s -> "Text: " + s;
        case null -> "null";
        default -> "Unknown: " + obj;
    };
}
```

#### Text Blocks (Multi-line Strings)
```java
// Old way
String json = "{\n" +
              "  \"name\": \"John\",\n" +
              "  \"age\": 30\n" +
              "}";

// Modern way - text block
String json = """
    {
      "name": "John",
      "age": 30
    }
    """;
```

#### Switch Expressions
```java
// Old switch statement
String result;
switch (day) {
    case MONDAY:
    case FRIDAY:
        result = "Work";
        break;
    case SATURDAY:
    case SUNDAY:
        result = "Weekend";
        break;
    default:
        result = "Unknown";
}

// Modern switch expression
String result = switch (day) {
    case MONDAY, FRIDAY -> "Work";
    case SATURDAY, SUNDAY -> "Weekend";
    default -> "Unknown";
};
```

### Java 21 Features

#### Virtual Threads
```java
// Traditional platform threads - expensive, limited scalability
try (var executor = Executors.newFixedThreadPool(100)) {
    for (int i = 0; i < 10000; i++) {
        executor.submit(() -> fetchData());
    }
}

// Virtual threads - lightweight, millions possible
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    for (int i = 0; i < 10000; i++) {
        executor.submit(() -> fetchData());
    }
}

// Start virtual thread directly
Thread.startVirtualThread(() -> {
    // Task code
});

// Structured concurrency (preview in Java 21)
try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
    Future<String> user = scope.fork(() -> fetchUser(id));
    Future<List<Order>> orders = scope.fork(() -> fetchOrders(id));

    scope.join();           // Wait for all tasks
    scope.throwIfFailed();  // Throw if any failed

    return new UserDetails(user.resultNow(), orders.resultNow());
}
```

#### Sequenced Collections
```java
// New interfaces: SequencedCollection, SequencedSet, SequencedMap

// Get first and last elements
List<String> list = List.of("a", "b", "c");
String first = list.getFirst();  // "a"
String last = list.getLast();    // "c"

// Reversed view (not a copy!)
List<String> reversed = list.reversed();

// Works with Set
LinkedHashSet<String> set = new LinkedHashSet<>(List.of("a", "b", "c"));
set.addFirst("z");  // z, a, b, c
set.addLast("x");   // z, a, b, c, x

// Works with Map
LinkedHashMap<String, Integer> map = new LinkedHashMap<>();
map.putFirst("first", 1);
map.putLast("last", 99);
```

#### Pattern Matching for switch (finalized)
```java
// Pattern matching with null handling
String formatted = switch (obj) {
    case null -> "null";
    case Integer i -> "Number: " + i;
    case String s -> "Text: " + s;
    case List<?> list -> "List of " + list.size() + " items";
    default -> "Unknown";
};

// Guard patterns
String category = switch (value) {
    case Integer i when i < 0 -> "Negative";
    case Integer i when i == 0 -> "Zero";
    case Integer i -> "Positive";
    default -> "Not a number";
};
```

#### Record Patterns (finalized)
```java
record Point(int x, int y) {}
record Circle(Point center, int radius) {}

// Deconstruct records in patterns
static void printPoint(Object obj) {
    if (obj instanceof Point(int x, int y)) {
        System.out.println("x: " + x + ", y: " + y);
    }
}

// Nested deconstruction
static void printCircle(Object obj) {
    if (obj instanceof Circle(Point(int x, int y), int r)) {
        System.out.println("Circle at (" + x + ", " + y + ") with radius " + r);
    }
}

// In switch
static String describe(Object obj) {
    return switch (obj) {
        case Point(int x, int y) -> "Point at (" + x + ", " + y + ")";
        case Circle(Point(int x, int y), int r) ->
            "Circle at (" + x + ", " + y + ") radius " + r;
        default -> "Unknown shape";
    };
}
```

### Java 25 Features

#### Flexible Main Methods
```java
// No longer need public static void main(String[] args)

// Simple main - for beginners and scripts
void main() {
    System.out.println("Hello World");
}

// With arguments (if needed)
void main(String[] args) {
    System.out.println("Args: " + Arrays.toString(args));
}

// Instance main (access to instance fields/methods)
class App {
    private String message = "Hello";

    void main() {
        System.out.println(message);  // Access instance field
        greet();                       // Call instance method
    }

    void greet() {
        System.out.println("Welcome");
    }
}
```

#### Scoped Values (Alternative to ThreadLocal)
```java
// ThreadLocal (old way) - must be cleaned up manually
private static final ThreadLocal<User> CURRENT_USER = new ThreadLocal<>();

// Scoped Values (new way) - automatically cleaned up
public static final ScopedValue<User> CURRENT_USER = ScopedValue.newInstance();

// Set scoped value (automatically reverted when block exits)
ScopedValue.runWhere(CURRENT_USER, user, () -> {
    // Value is available here
    User currentUser = CURRENT_USER.get();
    processRequest(currentUser);
    // Value automatically cleared when block exits
});

// Inherited by virtual threads
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    ScopedValue.runWhere(CURRENT_USER, user, () -> {
        executor.submit(() -> {
            // Virtual thread inherits scoped value
            User u = CURRENT_USER.get();
            handleTask(u);
        });
    });
}
```

#### Primitive Pattern Matching (Preview)
```java
// Pattern matching now works with primitives

static String classify(int value) {
    return switch (value) {
        case 0 -> "zero";
        case int i when i > 0 -> "positive";
        case int i when i < 0 -> "negative";
    };
}

// Type patterns for primitives
Object obj = 42;
if (obj instanceof int i) {
    System.out.println("Integer: " + i);
}
```

#### Gatherers (Custom Stream Operations)
```java
// Create custom intermediate stream operations

// Built-in gatherers
Stream.of(1, 2, 3, 4, 5)
    .gather(Gatherers.windowFixed(2))  // [[1,2], [3,4], [5]]
    .toList();

Stream.of(1, 2, 3, 4, 5)
    .gather(Gatherers.windowSliding(2))  // [[1,2], [2,3], [3,4], [4,5]]
    .toList();

// Custom gatherer example (simplified)
var sumAndCount = Gatherer.of(
    () -> new long[2],  // [sum, count]
    (state, element, downstream) -> {
        state[0] += element;
        state[1]++;
        return true;
    },
    (state, downstream) -> {
        downstream.push(state[0] / (double) state[1]);
    }
);

double average = Stream.of(1, 2, 3, 4, 5)
    .gather(sumAndCount)
    .findFirst()
    .orElse(0.0);
```

## Code Organization

### Visibility Modifiers
```java
// Use the most restrictive visibility possible
public class UserService {
    private final UserRepository repository;  // private - internal state

    public UserService(UserRepository repository) {  // public - API
        this.repository = repository;
    }

    public User findById(String id) {  // public - API
        return validateAndFetch(id);
    }

    private User validateAndFetch(String id) {  // private - internal logic
        if (id == null || id.isBlank()) {
            throw new IllegalArgumentException("ID cannot be blank");
        }
        return repository.findById(id)
            .orElseThrow(() -> new UserNotFoundException(id));
    }
}
```

### SOLID Principles

**Single Responsibility Principle**
```java
// BAD - class does too much
public class UserService {
    public void createUser(User user) { /* ... */ }
    public void sendEmail(String to, String message) { /* ... */ }
    public void logActivity(String activity) { /* ... */ }
}

// GOOD - single responsibility
public class UserService {
    private final UserRepository repository;
    private final EmailService emailService;
    private final AuditService auditService;

    public void createUser(User user) {
        repository.save(user);
        emailService.sendWelcomeEmail(user);
        auditService.logUserCreation(user.id());
    }
}
```

**Dependency Inversion**
```java
// GOOD - depend on abstractions, not implementations
public class UserService {
    private final UserRepository repository;  // interface, not concrete class

    public UserService(UserRepository repository) {
        this.repository = repository;
    }
}
```

## Exception Handling

### Checked vs Unchecked
```java
// Checked exceptions for recoverable errors (use sparingly)
public class UserNotFoundException extends Exception {
    public UserNotFoundException(String userId) {
        super("User not found: " + userId);
    }
}

// Unchecked exceptions for programming errors (preferred)
public class InvalidUserIdException extends RuntimeException {
    public InvalidUserIdException(String userId) {
        super("Invalid user ID: " + userId);
    }
}
```

### Try-with-Resources
```java
// Automatic resource management
try (BufferedReader reader = new BufferedReader(new FileReader("file.txt"))) {
    String line = reader.readLine();
    // reader automatically closed
} catch (IOException e) {
    throw new UncheckedIOException(e);
}

// Multiple resources
try (var inputStream = new FileInputStream("in.txt");
     var outputStream = new FileOutputStream("out.txt")) {
    // Both automatically closed in reverse order
}
```

### Custom Exception Hierarchies
```java
// Base exception for domain
public class DomainException extends RuntimeException {
    public DomainException(String message) {
        super(message);
    }
}

// Specific exceptions
public class UserNotFoundException extends DomainException {
    public UserNotFoundException(String userId) {
        super("User not found: " + userId);
    }
}

public class InvalidEmailException extends DomainException {
    public InvalidEmailException(String email) {
        super("Invalid email: " + email);
    }
}
```

## Collections & Streams API

### When to Use Which Collection
```java
// List - ordered, allows duplicates
List<String> names = new ArrayList<>();

// Set - no duplicates
Set<String> uniqueNames = new HashSet<>();

// Map - key-value pairs
Map<String, User> userById = new HashMap<>();

// Prefer List.of(), Set.of(), Map.of() for immutable collections
List<String> immutableList = List.of("a", "b", "c");
Set<Integer> immutableSet = Set.of(1, 2, 3);
Map<String, Integer> immutableMap = Map.of("a", 1, "b", 2);
```

### Stream Best Practices
```java
// Filter and map
List<String> activeUserNames = users.stream()
    .filter(User::isActive)
    .map(User::name)
    .toList();  // Java 16+, or .collect(Collectors.toList())

// Find first
Optional<User> firstAdmin = users.stream()
    .filter(User::isAdmin)
    .findFirst();

// Reduce
int totalAge = users.stream()
    .mapToInt(User::age)
    .sum();

// Group by
Map<String, List<User>> usersByRole = users.stream()
    .collect(Collectors.groupingBy(User::role));

// Don't reuse streams (they're one-time use)
// BAD
var stream = users.stream();
stream.filter(...).toList();
stream.map(...).toList();  // IllegalStateException

// GOOD
users.stream().filter(...).toList();
users.stream().map(...).toList();
```

## Optional & Null Handling

### When to Use Optional
```java
// GOOD - Optional for return values (absence is expected)
public Optional<User> findUserById(String id) {
    return repository.findById(id);
}

// BAD - don't use Optional for parameters or fields
public void processUser(Optional<User> user) { /* avoid */ }
private Optional<User> currentUser;  /* avoid */

// GOOD - use null for parameters if optional
public void processUser(User user) {
    if (user != null) {
        // process
    }
}
```

### Optional Best Practices
```java
// Chain operations
String userName = userService.findUserById(id)
    .map(User::name)
    .map(String::toUpperCase)
    .orElse("UNKNOWN");

// Throw exception if absent
User user = userService.findUserById(id)
    .orElseThrow(() -> new UserNotFoundException(id));

// Execute action if present
userService.findUserById(id)
    .ifPresent(user -> emailService.sendWelcome(user));

// Don't use Optional.get() without checking
// BAD
Optional<User> maybeUser = findUser(id);
User user = maybeUser.get();  // NoSuchElementException if empty

// GOOD
User user = maybeUser.orElseThrow();  // More explicit
```

### Null Safety
```java
// Use Objects.requireNonNull for validation
public User(String id, String name) {
    this.id = Objects.requireNonNull(id, "id cannot be null");
    this.name = Objects.requireNonNull(name, "name cannot be null");
}

// Prefer Objects utilities
String result = Objects.requireNonNullElse(value, "default");
boolean equals = Objects.equals(a, b);  // null-safe equals
```

## Testing Fundamentals

### JUnit 5 Basics
```java
import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

class UserServiceTest {
    private UserService service;
    private UserRepository repository;

    @BeforeEach
    void setUp() {
        repository = new InMemoryUserRepository();
        service = new UserService(repository);
    }

    @Test
    void shouldReturnUserWhenIdExists() {
        // Given
        var user = new User("1", "John", "john@example.com");
        repository.save(user);

        // When
        var result = service.findById("1");

        // Then
        assertTrue(result.isPresent());
        assertEquals("John", result.get().name());
    }

    @Test
    void shouldThrowWhenIdIsNull() {
        assertThrows(IllegalArgumentException.class,
            () -> service.findById(null));
    }

    @ParameterizedTest
    @ValueSource(strings = {"", "  ", "\t"})
    void shouldThrowWhenIdIsBlank(String id) {
        assertThrows(IllegalArgumentException.class,
            () -> service.findById(id));
    }
}
```

### Mockito for Mocking
```java
import org.mockito.*;
import static org.mockito.Mockito.*;

class UserServiceTest {
    @Mock
    private UserRepository repository;

    @InjectMocks
    private UserService service;

    @BeforeEach
    void setUp() {
        MockitoAnnotations.openMocks(this);
    }

    @Test
    void shouldCallRepositoryWhenFindingUser() {
        // Given
        var user = new User("1", "John", "john@example.com");
        when(repository.findById("1")).thenReturn(Optional.of(user));

        // When
        var result = service.findById("1");

        // Then
        verify(repository).findById("1");
        assertTrue(result.isPresent());
        assertEquals("John", result.get().name());
    }
}
```

### Test Naming
```java
// Descriptive names - what scenario, what expected
@Test
void shouldReturnEmptyWhenUserNotFound() { }

@Test
void shouldThrowExceptionWhenEmailIsInvalid() { }

@Test
void shouldCalculateDiscountWhenUserIsVip() { }
```

## Build Tool Awareness

### Maven Dependencies (pom.xml)
```xml
<dependencies>
    <!-- Core dependencies -->
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-web</artifactId>
    </dependency>

    <!-- Test dependencies -->
    <dependency>
        <groupId>org.junit.jupiter</groupId>
        <artifactId>junit-jupiter</artifactId>
        <scope>test</scope>
    </dependency>
</dependencies>
```

### Gradle Dependencies (build.gradle.kts)
```kotlin
dependencies {
    // Core dependencies
    implementation("org.springframework.boot:spring-boot-starter-web")

    // Test dependencies
    testImplementation("org.junit.jupiter:junit-jupiter")
    testImplementation("org.mockito:mockito-core")
}
```

### Project Conventions
```java
// Maven standard directory layout
src/main/java       - Production code
src/main/resources  - Configuration files
src/test/java       - Test code
src/test/resources  - Test configuration

// Gradle uses same layout
// Package structure matches directory structure
// com.example.myapp.service -> src/main/java/com/example/myapp/service/
```

## Recommended Tooling

| Tool | Purpose |
|------|---------|
| `maven` or `gradle` | Build automation |
| `junit-jupiter` | Testing framework (JUnit 5) |
| `mockito` | Mocking framework |
| `checkstyle` | Code style checking |
| `spotbugs` | Static bug detection |
| `jacoco` | Code coverage |
| `maven-enforcer` | Dependency management rules |
| `testcontainers` | Integration testing with Docker |

## Production Best Practices

1. **Immutability** - Prefer records and final fields, reduces bugs
2. **Dependency Injection** - Constructor injection over field injection
3. **Fail Fast** - Validate inputs immediately, throw exceptions early
4. **Explicit over Implicit** - Clear code over clever code
5. **Resource Management** - Always use try-with-resources for I/O
6. **Optional for Return Types** - Signal absence without null
7. **Stream API** - Use streams for collection operations, but don't overuse
8. **Modern Java** - Use records, sealed classes, pattern matching
9. **Minimal Checked Exceptions** - Prefer unchecked for most cases
10. **Constructor Validation** - Validate in constructor or compact constructor (records)
11. **Descriptive Names** - Method names should explain intent
12. **Single Responsibility** - Classes and methods should do one thing
13. **Package by Feature** - Not by layer (service/repository/controller in same package)
14. **Logging** - Use SLF4J, structured logging, appropriate levels
15. **Configuration** - Externalize via application.properties, environment variables

## Comments - Less is More

```java
// BAD - redundant comment
// Get user from repository
User user = repository.findById(id);

// GOOD - self-explanatory code, no comment needed
User user = repository.findById(id);

// GOOD - comment explains WHY (not obvious)
// Rate limit: API allows max 100 requests per minute per client
rateLimiter.acquire();

// GOOD - comment documents constraint
/**
 * Processes payment. Amount must be positive.
 * @throws IllegalArgumentException if amount <= 0
 */
public void processPayment(BigDecimal amount) { }
```

---

## References

- Java Language Specification: https://docs.oracle.com/javase/specs/
- Effective Java by Joshua Bloch
- Clean Code by Robert C. Martin
