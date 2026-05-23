---
name: standards-kotlin
description: Kotlin coding standards for modern applications. Includes naming conventions, coroutines, flows, modern Kotlin 2.3.0 features, and recommended tooling.
type: context
applies_to: [kotlin, gradle, maven, junit, kotest, kotlinx-coroutines, ktor, spring, mockk, testcontainers]
file_extensions: [".kt", ".kts"]
---

# Kotlin Coding Standards

## Core Principles

1. **Explicitness**: Explicit code over implicit magic
2. **Readability**: Readable code over clever tricks
3. **Null Safety**: Embrace Kotlin's null safety system
4. **Immutability**: Prefer `val` over `var`, immutable collections
5. **Expressiveness**: Use Kotlin's expressive features (data classes, sealed classes)
6. **DRY**: Don't Repeat Yourself - but keep it simple

## General Rules

- **Prefer `val` over `var`**: Immutability by default
- **Use data classes**: For simple data holders
- **Sealed classes/interfaces**: For type-safe state modeling
- **Early returns**: Avoid deep nesting
- **Descriptive names**: Clear, meaningful names
- **Minimal changes**: Only change relevant code
- **No over-engineering**: Keep it simple
- **Minimal comments**: Self-explanatory code. Comments for "why", not "what"

## Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Classes | PascalCase | `UserService`, `OrderRepository` |
| Interfaces | PascalCase | `UserRepository`, `PaymentProcessor` |
| Functions | camelCase | `getUserById`, `calculateTotal` |
| Properties | camelCase | `firstName`, `totalAmount` |
| Constants | UPPER_SNAKE_CASE | `MAX_RETRY_COUNT`, `DEFAULT_TIMEOUT` |
| Packages | lowercase.dot.separated | `com.example.service`, `com.example.repository` |
| Files | PascalCase.kt | `UserService.kt`, `OrderRepository.kt` |
| Test Classes | ClassNameTest | `UserServiceTest`, `OrderRepositoryTest` |
| Test Functions | backtick names | `` `should return user when id exists` `` |

## Project Structure

### Gradle Kotlin DSL Project (Recommended)
```
myproject/
├── build.gradle.kts
├── settings.gradle.kts
├── gradle.properties
├── src/
│   ├── main/
│   │   ├── kotlin/
│   │   │   └── com/example/myapp/
│   │   │       ├── Application.kt          # Main entry point
│   │   │       ├── config/
│   │   │       │   └── AppConfig.kt        # Configuration
│   │   │       ├── domain/
│   │   │       │   └── User.kt             # Domain models
│   │   │       ├── repository/
│   │   │       │   └── UserRepository.kt   # Data access
│   │   │       ├── service/
│   │   │       │   └── UserService.kt      # Business logic
│   │   │       └── api/
│   │   │           └── UserController.kt   # REST endpoints
│   │   └── resources/
│   │       ├── application.conf
│   │       └── logback.xml
│   └── test/
│       ├── kotlin/
│       │   └── com/example/myapp/
│       │       ├── service/
│       │       │   └── UserServiceTest.kt
│       │       └── repository/
│       │           └── UserRepositoryTest.kt
│       └── resources/
│           └── application-test.conf
└── README.md
```

### Maven Project (Alternative)
```
myproject/
├── pom.xml
├── src/
│   ├── main/
│   │   └── kotlin/...      # Same structure as Gradle
│   └── test/
│       └── kotlin/...      # Same structure as Gradle
└── README.md
```

## Modern Kotlin Features

> **Recommended:** Use Kotlin 2.3.0 (latest LTS) for new projects with K2 compiler enabled by default.

### K2 Compiler (Stable since 2.0)

The K2 compiler brings significant performance improvements and faster compilation times.

**Features:**
- Faster compilation (up to 2x)
- Better smart casts
- Improved type inference
- Unified architecture for all platforms

**Enabled by default in Kotlin 2.3.0** - no configuration needed.

### Data Classes

Use data classes for immutable data holders.

```kotlin
// Data class - automatic equals, hashCode, toString, copy, componentN
data class User(
    val id: String,
    val name: String,
    val email: String,
    val age: Int
)

// Usage
val user = User("1", "John Doe", "john@example.com", 30)

// Copy with changes
val updatedUser = user.copy(age = 31)

// Destructuring
val (id, name, email, age) = user
println("User: $name ($email)")
```

### Sealed Classes/Interfaces (Exhaustive When)

Use sealed classes for type-safe state modeling with exhaustive `when` expressions.

```kotlin
// Sealed interface for result types
sealed interface Result<out T> {
    data class Success<T>(val data: T) : Result<T>
    data class Error(val message: String, val cause: Throwable? = null) : Result<Nothing>
    data object Loading : Result<Nothing>
}

// Exhaustive when - compiler ensures all cases are handled
fun <T> handleResult(result: Result<T>) {
    when (result) {
        is Result.Success -> println("Success: ${result.data}")
        is Result.Error -> println("Error: ${result.message}")
        Result.Loading -> println("Loading...")
        // No else needed - compiler knows all cases
    }
}

// Usage
val result: Result<User> = Result.Success(user)
handleResult(result)
```

### Inline Value Classes (Zero-Cost Wrappers)

Use inline value classes for type-safe wrappers without runtime overhead.

```kotlin
// Inline value class - no boxing overhead
@JvmInline
value class UserId(val value: String)

@JvmInline
value class Email(val value: String) {
    init {
        require(value.contains("@")) { "Invalid email" }
    }
}

// Usage - type-safe, no runtime cost
fun getUserById(id: UserId): User = TODO()
fun sendEmail(email: Email): Unit = TODO()

val userId = UserId("123")
val email = Email("user@example.com")
```

### Context Receivers (Experimental, 2.2+)

Context receivers allow implicit parameters for cleaner DSLs.

**Enable with:**
```kotlin
// build.gradle.kts
kotlin {
    compilerOptions {
        freeCompilerArgs.add("-Xcontext-receivers")
    }
}
```

**Usage:**
```kotlin
interface Logger {
    fun log(message: String)
}

// Function with context receiver
context(Logger)
fun processUser(user: User) {
    log("Processing user: ${user.name}")
    // ...
}

// Call with context
val logger = object : Logger {
    override fun log(message: String) = println(message)
}

with(logger) {
    processUser(user)
}
```

### Explicit Backing Fields (Experimental, 2.3)

Simplifies backing property pattern - define implementation type within property scope.

**Enable with:**
```kotlin
// build.gradle.kts
kotlin {
    compilerOptions {
        freeCompilerArgs.add("-Xexplicit-backing-fields")
    }
}
```

**Before:**
```kotlin
private val _users = MutableStateFlow<List<User>>(emptyList())
val users: StateFlow<List<User>> = _users
```

**After:**
```kotlin
val users: StateFlow<List<User>> field = MutableStateFlow(emptyList())
```

### UUID API (Experimental, 2.3)

Built-in UUID support without external dependencies.

**Enable with:**
```kotlin
@OptIn(ExperimentalUuidApi::class)
```

**Usage:**
```kotlin
import kotlin.uuid.Uuid
import kotlin.uuid.ExperimentalUuidApi

@OptIn(ExperimentalUuidApi::class)
fun generateUserId(): Uuid {
    return Uuid.generateV4()
}

@OptIn(ExperimentalUuidApi::class)
fun parseUserId(id: String): Uuid? {
    return Uuid.parseOrNull(id)
}

// V7 UUIDs (time-based, sortable)
@OptIn(ExperimentalUuidApi::class)
fun generateTimeBasedId(): Uuid {
    return Uuid.generateV7()
}
```

## Coroutines & Concurrency

### Structured Concurrency

Always use structured concurrency - never use `GlobalScope`.

```kotlin
import kotlinx.coroutines.*

// GOOD - Structured concurrency
suspend fun fetchUserData(userId: String): UserData = coroutineScope {
    val userDeferred = async { fetchUser(userId) }
    val ordersDeferred = async { fetchOrders(userId) }

    UserData(
        user = userDeferred.await(),
        orders = ordersDeferred.await()
    )
}

// BAD - GlobalScope leaks
fun fetchUserDataBad(userId: String) {
    GlobalScope.launch {  // Don't use GlobalScope!
        // ...
    }
}
```

### Dispatchers

Use appropriate dispatchers for different workloads.

```kotlin
// Dispatchers.Default - CPU-intensive work
withContext(Dispatchers.Default) {
    // Heavy computation
    processLargeDataset(data)
}

// Dispatchers.IO - I/O operations (network, disk)
withContext(Dispatchers.IO) {
    // Network call
    apiClient.fetchData()
}

// Dispatchers.Main - UI updates (Android/Desktop)
withContext(Dispatchers.Main) {
    updateUI(data)
}

// Dispatchers.Unconfined - Advanced use cases only
```

### launch vs async

```kotlin
// launch - fire and forget, returns Job
fun processInBackground() = coroutineScope {
    launch {
        // No result needed
        sendNotification()
    }
}

// async - returns Deferred<T>, await for result
suspend fun fetchMultipleResources() = coroutineScope {
    val users = async { fetchUsers() }
    val orders = async { fetchOrders() }

    CombinedData(
        users = users.await(),
        orders = orders.await()
    )
}
```

### Cancellation & Exception Handling

```kotlin
// Cancellation-aware code
suspend fun longRunningTask() = coroutineScope {
    repeat(100) { i ->
        ensureActive()  // Check for cancellation
        delay(100)
        println("Step $i")
    }
}

// Exception handling with supervisorScope
suspend fun fetchDataSafely(): Result<Data> = try {
    supervisorScope {
        val data = async { fetchData() }
        Result.Success(data.await())
    }
} catch (e: Exception) {
    Result.Error("Failed to fetch data", e)
}

// CoroutineExceptionHandler
val handler = CoroutineExceptionHandler { _, exception ->
    println("Caught exception: $exception")
}

val scope = CoroutineScope(SupervisorJob() + handler)
```

## Flow API

### StateFlow vs SharedFlow vs MutableStateFlow

```kotlin
// StateFlow - single value, always has current value, conflates updates
class UserViewModel {
    private val _userName = MutableStateFlow("")
    val userName: StateFlow<String> = _userName.asStateFlow()

    fun updateUserName(name: String) {
        _userName.value = name
    }
}

// SharedFlow - event stream, can replay, doesn't conflate
class EventBus {
    private val _events = MutableSharedFlow<Event>(
        replay = 0,      // Don't replay events
        extraBufferCapacity = 64
    )
    val events: SharedFlow<Event> = _events.asSharedFlow()

    suspend fun emit(event: Event) {
        _events.emit(event)
    }
}

// Hot vs Cold flows
// StateFlow/SharedFlow = Hot (emit regardless of collectors)
// flow { } = Cold (only emit when collected)
```

### Flow Operators

```kotlin
// Transform flows
val userNames: Flow<String> = users
    .map { it.name }
    .filter { it.isNotEmpty() }
    .distinctUntilChanged()

// Combine flows
val combinedData = combine(users, orders) { users, orders ->
    CombinedData(users, orders)
}

// FlatMap variants
val allOrders: Flow<Order> = users
    .flatMapConcat { user -> fetchOrders(user.id) }  // Sequential
    // .flatMapMerge { user -> fetchOrders(user.id) }  // Concurrent
    // .flatMapLatest { user -> fetchOrders(user.id) }  // Cancel previous

// Error handling
val safeData: Flow<Data> = dataFlow
    .catch { e -> emit(Data.Empty) }
    .retry(3)
```

### Flow Collection

```kotlin
// Collect in coroutine
lifecycleScope.launch {
    userViewModel.userName.collect { name ->
        updateUI(name)
    }
}

// collectLatest - cancel previous collection on new emission
lifecycleScope.launch {
    searchQuery.collectLatest { query ->
        // Cancelled if new query arrives
        val results = searchRepository.search(query)
        updateResults(results)
    }
}

// Single value
val user = userFlow.first()  // First value
val user = userFlow.firstOrNull()  // Or null if empty
```

### Flow Best Practices

1. **Single source of truth**: Expose `StateFlow`/`SharedFlow`, keep `MutableStateFlow`/`MutableSharedFlow` private
2. **Use `collectLatest` for UI**: Cancel previous work on new emissions
3. **Use `stateIn` for cold-to-hot conversion**:
```kotlin
val data: StateFlow<Data> = dataRepository.getData()
    .stateIn(
        scope = viewModelScope,
        started = SharingStarted.WhileSubscribed(5000),
        initialValue = Data.Empty
    )
```

## Null Safety

### Safe Calls, Elvis, and !! Operator

```kotlin
// Safe call (?.) - returns null if receiver is null
val length: Int? = name?.length

// Elvis operator (?:) - default value
val length: Int = name?.length ?: 0

// !! operator - throws NPE if null (use sparingly!)
val length: Int = name!!.length  // Only if you're 100% sure it's not null

// Safe cast (as?)
val user: User? = obj as? User

// let for null checks
name?.let { n ->
    println("Name: $n")
}
```

### lateinit vs lazy

```kotlin
// lateinit - non-null var, initialized later (must be var)
class MyClass {
    lateinit var repository: Repository

    fun init(repo: Repository) {
        repository = repo
    }

    // Check if initialized
    fun isInitialized() = ::repository.isInitialized
}

// lazy - initialized on first access (must be val)
class MyClass {
    val expensiveValue: String by lazy {
        // Computed only once, on first access
        computeExpensiveValue()
    }
}
```

### Nullable Types vs Optional

```kotlin
// GOOD - Use nullable types (Kotlin-native)
fun findUser(id: String): User? {
    return repository.findById(id)
}

// BAD - Don't use Java's Optional in Kotlin
fun findUserBad(id: String): Optional<User> {  // Avoid
    return Optional.ofNullable(repository.findById(id))
}

// When interoping with Java, convert at boundary
fun getUserFromJava(id: String): User? {
    return javaService.getUser(id).orElse(null)
}
```

### Backing Properties (Standard Pattern)

Use underscore prefix for private mutable backing properties.

```kotlin
// Standard pattern for exposing read-only property
class UserRepository {
    private val _users = mutableListOf<User>()
    val users: List<User> get() = _users

    fun addUser(user: User) {
        _users.add(user)
    }
}

// StateFlow pattern
class UserViewModel {
    private val _state = MutableStateFlow<UiState>(UiState.Loading)
    val state: StateFlow<UiState> = _state.asStateFlow()

    fun updateState(newState: UiState) {
        _state.value = newState
    }
}

// Alternative: explicit backing fields (experimental, Kotlin 2.3+)
// Requires: -Xexplicit-backing-fields compiler flag
val users: StateFlow<List<User>> field = MutableStateFlow(emptyList())
```

## Scope Functions

Kotlin provides five scope functions: `let`, `run`, `with`, `apply`, `also`. Choose based on context object reference and return value.

| Function | Object Reference | Return Value | Use Case |
|----------|-----------------|--------------|----------|
| `let` | `it` | Lambda result | Null checks, transformations |
| `run` | `this` | Lambda result | Object configuration + computation |
| `with` | `this` | Lambda result | Group function calls on object |
| `apply` | `this` | Context object | Object initialization |
| `also` | `it` | Context object | Side effects |

### let - Null Checks & Transformations

```kotlin
// Null check with let
val length: Int? = name?.let { it.length }

// Chain with let
val result = value?.let { v ->
    processValue(v)
}?.let { processed ->
    saveResult(processed)
}

// Execute block only if non-null
user?.let { u ->
    println("User: ${u.name}")
    sendWelcomeEmail(u)
}

// Transform value
val uppercaseName = name?.let { it.uppercase() }
```

### apply - Object Initialization

```kotlin
// Object initialization (returns `this`)
val user = User().apply {
    name = "John Doe"
    email = "john@example.com"
    age = 30
}

// Configure and return
val intent = Intent(context, DetailActivity::class.java).apply {
    putExtra("id", userId)
    flags = Intent.FLAG_ACTIVITY_NEW_TASK
}

// Builder pattern style
val dialog = AlertDialog.Builder(context).apply {
    setTitle("Confirm")
    setMessage("Are you sure?")
    setPositiveButton("Yes") { _, _ -> confirm() }
}.create()
```

### also - Side Effects

```kotlin
// Side effects (returns `this`)
val numbers = mutableListOf(1, 2, 3).also {
    println("List created with ${it.size} elements")
}

// Debug chain
val result = processData(input)
    .also { println("Intermediate result: $it") }
    .transformData()
    .also { println("Final result: $it") }

// Multiple operations
val user = createUser().also {
    logUserCreation(it)
    sendWelcomeEmail(it)
}
```

### run - Computations

```kotlin
// Compute value (returns lambda result)
val result = run {
    val x = computeX()
    val y = computeY()
    x + y
}

// Null check with run
val result = service?.run {
    fetchData()
    processData()
}

// Replace multiple statements
val hexString = run {
    val color = getColor()
    Integer.toHexString(color)
}
```

### with - Multiple Calls on Object

```kotlin
// Group operations on object (returns lambda result)
val result = with(canvas) {
    drawCircle(centerX, centerY, radius)
    drawLine(startX, startY, endX, endY)
    drawText(text, x, y)
    save()
}

// Configure object
with(sharedPreferences.edit()) {
    putString("username", username)
    putInt("age", age)
    apply()
}

// Avoid repetition
val user = getUser()
with(user) {
    println("Name: $name")
    println("Email: $email")
    println("Age: $age")
}
```

### Scope Function Selection Guide

```kotlin
// Use let for null checks
value?.let { println(it) }

// Use apply for object initialization (returns object)
val config = Config().apply { timeout = 30 }

// Use also for side effects (returns object)
val list = getList().also { log("Size: ${it.size}") }

// Use run for computations (returns result)
val result = run { compute() }

// Use with for grouping calls (returns result)
val formatted = with(user) { "$name ($email)" }
```

## Collections & Sequences

### List vs MutableList

```kotlin
// Prefer immutable collections
val users: List<User> = listOf(user1, user2, user3)

// Mutable only when needed
val mutableUsers: MutableList<User> = mutableListOf()
mutableUsers.add(user4)

// Read-only view of mutable collection
val readOnlyView: List<User> = mutableUsers

// List.of() for Java interop (immutable)
val javaList = java.util.List.of(user1, user2)
```

### Sequence for Lazy Evaluation

Use `Sequence` for large collections or chained operations.

```kotlin
// List - eager evaluation (creates intermediate lists)
val result = users
    .filter { it.age > 18 }
    .map { it.name }
    .take(10)

// Sequence - lazy evaluation (no intermediate collections)
val result = users.asSequence()
    .filter { it.age > 18 }
    .map { it.name }
    .take(10)
    .toList()  // Terminal operation

// Generate infinite sequence
val fibonacci = generateSequence(1 to 1) { (a, b) -> b to a + b }
    .map { it.first }
    .take(10)
    .toList()
```

### Collection Operations

```kotlin
// Transform
val names = users.map { it.name }
val adults = users.filter { it.age >= 18 }
val groups = users.groupBy { it.department }

// Reduce/Fold
val totalAge = users.sumOf { it.age }
val oldest = users.maxByOrNull { it.age }
val names = users.fold("") { acc, user -> "$acc, ${user.name}" }

// Partition
val (adults, minors) = users.partition { it.age >= 18 }

// Associate
val userById = users.associateBy { it.id }
val nameToUser = users.associateWith { it.name }
```

### Loops on Ranges

```kotlin
// BAD - off-by-one prone
for (i in 0..n - 1) { }
for (i in 0 until n) { }  // Better but verbose

// GOOD - use ..< (Kotlin 1.7+)
for (i in 0..<n) { }

// Ranges
for (i in 1..10) { }        // 1 to 10 (inclusive)
for (i in 1..<10) { }       // 1 to 9 (exclusive end)
for (i in 10 downTo 1) { }  // 10 to 1 (descending)
for (i in 1..10 step 2) { } // 1, 3, 5, 7, 9

// Prefer higher-order functions over loops
// GOOD
val adults = users.filter { it.age >= 18 }

// Less idiomatic
val adults = mutableListOf<User>()
for (user in users) {
    if (user.age >= 18) {
        adults.add(user)
    }
}
```

## String Templates

Use string templates instead of concatenation.

```kotlin
// Simple variable - no braces needed
val message = "Hello, $name!"

// Expression - use braces
val message = "User $name has ${children.size} children"
val message = "${user.name} (${user.age} years old)"

// Property access
val message = "Length: ${text.length}"

// Function call
val message = "Result: ${compute()}"

// BAD - concatenation
val message = "Hello, " + name + "!"

// Multiline strings with templates
val json = """
{
    "name": "$name",
    "age": $age,
    "email": "$email"
}
""".trimIndent()

// Multi-dollar strings (Kotlin 2.0+) - escape $ in raw strings
val jsonSchema = $$"""
{
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "$${title ?: "unknown"}"
}
"""
```

## Extension Functions

Extension functions add functionality to existing classes without inheritance.

### When to Use Extensions

```kotlin
// GOOD - Add functionality to existing type
fun String.isValidEmail(): Boolean {
    return this.contains("@") && this.contains(".")
}

// Usage
val email = "user@example.com"
if (email.isValidEmail()) { }

// GOOD - Domain-specific operations
fun User.toDisplayString(): String {
    return "$name ($email)"
}

// GOOD - Collection transformations
fun List<User>.activeUsers(): List<User> {
    return filter { it.isActive }
}
```

### Extension Best Practices

```kotlin
// 1. Restrict visibility (prefer private/internal)
private fun String.sanitize(): String {
    return this.trim().lowercase()
}

// 2. Place extensions in same file as class (if you own it)
// User.kt
data class User(val name: String)

fun User.greet() = "Hello, $name"

// 3. Group related extensions in separate file
// StringExtensions.kt
fun String.isValidEmail(): Boolean { }
fun String.isValidUrl(): Boolean { }

// 4. Don't overuse - prefer member functions when appropriate
class User {
    // GOOD - core behavior as member
    fun activate() { }
}

// Extension for convenience
fun User.deactivate() { }
```

### Extension Properties

```kotlin
// Extension property (no backing field allowed)
val String.lastChar: Char?
    get() = this.lastOrNull()

val List<Int>.median: Double
    get() {
        val sorted = this.sorted()
        val middle = sorted.size / 2
        return if (sorted.size % 2 == 0) {
            (sorted[middle - 1] + sorted[middle]) / 2.0
        } else {
            sorted[middle].toDouble()
        }
    }

// Usage
println("Hello".lastChar)  // 'o'
println(listOf(1, 3, 2).median)  // 2.0
```

## When Expressions Advanced

### When with Guards (Kotlin 1.7+)

```kotlin
// Guard conditions in when
sealed interface Status {
    data class Ok(val info: Info) : Status
    data class Error(val code: Int) : Status
}

fun handleStatus(status: Status): String {
    return when (status) {
        is Status.Ok if (status.info.isEmpty()) -> "no information"
        is Status.Ok -> "success: ${status.info}"
        is Status.Error if (status.code >= 500) -> "server error"
        is Status.Error -> "client error: ${status.code}"
    }
}

// Guard with multiple conditions
fun classify(value: Int): String {
    return when (value) {
        in 0..10 if (value % 2 == 0) -> "small even"
        in 0..10 -> "small odd"
        in 11..100 -> "medium"
        else -> "large"
    }
}
```

### When as Expression

```kotlin
// Prefer when as expression (not statement)
// GOOD
val result = when (x) {
    0 -> "zero"
    in 1..10 -> "small"
    else -> "large"
}

// BAD
var result: String
when (x) {
    0 -> result = "zero"
    in 1..10 -> result = "small"
    else -> result = "large"
}
```

## Generics Basics

### Generic Functions

```kotlin
// Generic function
fun <T> singletonList(item: T): List<T> {
    return listOf(item)
}

val list = singletonList(42)        // List<Int>
val names = singletonList("Alice")  // List<String>

// Multiple type parameters
fun <K, V> mapOf(key: K, value: V): Map<K, V> {
    return mapOf(key to value)
}

// Type constraints
fun <T : Comparable<T>> max(a: T, b: T): T {
    return if (a > b) a else b
}
```

### Generic Classes

```kotlin
// Generic class
class Box<T>(val value: T) {
    fun get(): T = value
}

val intBox = Box(42)
val stringBox = Box("hello")

// Multiple type parameters
class Pair<A, B>(val first: A, val second: B)

val pair = Pair(1, "one")
```

### Variance (in, out)

```kotlin
// out - covariant (producer)
interface Producer<out T> {
    fun produce(): T
}

// in - contravariant (consumer)
interface Consumer<in T> {
    fun consume(item: T)
}

// Example
class ListWrapper<out T>(private val list: List<T>) {
    fun get(index: Int): T = list[index]  // OK - produces T
    // fun add(item: T) { }  // Error - cannot consume T
}

// Covariance allows
val strings: Producer<String> = object : Producer<String> {
    override fun produce() = "Hello"
}
val anys: Producer<Any> = strings  // OK - String is subtype of Any
```

### Reified Type Parameters

```kotlin
// inline + reified for runtime type access
inline fun <reified T> isInstance(value: Any): Boolean {
    return value is T
}

val result = isInstance<String>("hello")  // true
val result2 = isInstance<Int>("hello")    // false

// Useful for type-safe casts
inline fun <reified T> Any.asOrNull(): T? {
    return this as? T
}

val str: String? = obj.asOrNull<String>()
```

## Formatting & Code Style

Follow Kotlin official coding conventions for consistent code formatting.

### Indentation & Braces

```kotlin
// 4 spaces (not tabs)
// Opening brace at line end (Java-style)
if (condition) {
    doSomething()
}

// Single-line if can omit braces
if (condition) return

// Multi-line conditions: indent by 4 spaces
if (!component.isSyncing &&
    !hasErrors()
) {
    proceed()
}
```

### Whitespace Rules

```kotlin
// Space around binary operators
val sum = a + b
val result = x * y

// NO space for range operator
for (i in 0..10) { }

// NO space for unary operators
val x = -5
val y = a++

// Space after control flow keywords
if (condition) { }
when (x) { }
for (i in list) { }

// NO space before ( in calls/constructors
foo(1, 2)
User(name, age)

// NO spaces around . or ?.
user.name
user?.email

// Space after //
// This is a comment
```

### Trailing Commas

Encouraged at declaration/call sites (makes diffs cleaner):

```kotlin
// Function parameters
fun process(
    name: String,
    age: Int,
    email: String,  // trailing comma
) { }

// Arguments
process(
    name = "John",
    age = 30,
    email = "john@example.com",  // trailing comma
)

// Collections
val list = listOf(
    "apple",
    "banana",
    "cherry",  // trailing comma
)
```

### Expression Bodies

Prefer expression bodies for simple functions:

```kotlin
// GOOD - expression body
fun double(x: Int) = x * 2

// BAD - block body for simple function
fun double(x: Int): Int {
    return x * 2
}

// Expression body with line break
fun longFunctionName(
    arg1: String,
    arg2: String
) = processArguments(arg1, arg2)
```

### Named Arguments

Use named arguments for clarity:

```kotlin
// Multiple parameters of same type
drawSquare(x = 10, y = 10, width = 100, height = 100)

// Boolean parameters
setVisibility(visible = true, animated = false)

// Skip default parameters
createUser(name = "John")  // age has default
```

## Testing Fundamentals

### JUnit 5 + kotlin.test

```kotlin
import kotlin.test.*
import org.junit.jupiter.api.*

class UserServiceTest {
    private lateinit var userService: UserService
    private lateinit var repository: UserRepository

    @BeforeEach
    fun setup() {
        repository = InMemoryUserRepository()
        userService = UserService(repository)
    }

    @Test
    fun `should return user when id exists`() {
        // Given
        val user = User("1", "John", "john@example.com", 30)
        repository.save(user)

        // When
        val result = userService.findById("1")

        // Then
        assertNotNull(result)
        assertEquals("John", result.name)
    }

    @Test
    fun `should return null when user not found`() {
        // When
        val result = userService.findById("999")

        // Then
        assertNull(result)
    }

    @ParameterizedTest
    @ValueSource(strings = ["", "  ", "\t"])
    fun `should throw when id is blank`(id: String) {
        assertFailsWith<IllegalArgumentException> {
            userService.findById(id)
        }
    }
}
```

### Mockk for Mocking

```kotlin
import io.mockk.*
import kotlin.test.*

class UserServiceTest {
    private val repository = mockk<UserRepository>()
    private val userService = UserService(repository)

    @Test
    fun `should call repository when finding user`() {
        // Given
        val user = User("1", "John", "john@example.com", 30)
        every { repository.findById("1") } returns user

        // When
        val result = userService.findById("1")

        // Then
        verify { repository.findById("1") }
        assertEquals("John", result?.name)
    }

    @Test
    fun `should handle repository exception`() {
        // Given
        every { repository.findById(any()) } throws RuntimeException("DB error")

        // When/Then
        assertFailsWith<RuntimeException> {
            userService.findById("1")
        }
    }
}
```

### Coroutines Testing

```kotlin
import kotlinx.coroutines.test.*
import kotlin.test.*

class UserViewModelTest {
    @Test
    fun `should fetch user on init`() = runTest {
        // Given
        val repository = FakeUserRepository()
        val viewModel = UserViewModel(repository)

        // When
        advanceUntilIdle()

        // Then
        assertEquals(UserState.Success(user), viewModel.state.value)
    }

    @Test
    fun `should emit loading state while fetching`() = runTest {
        // Given
        val repository = SlowUserRepository()
        val viewModel = UserViewModel(repository)
        val states = mutableListOf<UserState>()

        // Collect states
        backgroundScope.launch {
            viewModel.state.toList(states)
        }

        // When
        advanceUntilIdle()

        // Then
        assertEquals(
            listOf(UserState.Loading, UserState.Success(user)),
            states
        )
    }
}
```

## Build Tool Awareness

### Gradle Kotlin DSL (build.gradle.kts) - Recommended

```kotlin
// build.gradle.kts
plugins {
    kotlin("jvm") version "2.3.10"
    application
}

group = "com.example"
version = "1.0.0"

repositories {
    mavenCentral()
}

dependencies {
    // Kotlin standard library (automatically added in 2.3+)
    // implementation(kotlin("stdlib"))

    // Coroutines
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-core:1.8.0")

    // Testing
    testImplementation(kotlin("test"))
    testImplementation("org.junit.jupiter:junit-jupiter:5.10.0")
    testImplementation("io.mockk:mockk:1.13.8")
    testImplementation("org.jetbrains.kotlinx:kotlinx-coroutines-test:1.8.0")
}

kotlin {
    jvmToolchain(21)  // Use Java 21

    compilerOptions {
        freeCompilerArgs.add("-Xcontext-receivers")  // Enable experimental features
        freeCompilerArgs.add("-Xexplicit-backing-fields")
    }
}

tasks.test {
    useJUnitPlatform()
}

application {
    mainClass.set("com.example.ApplicationKt")
}
```

### Gradle Dependencies: implementation vs api

```kotlin
dependencies {
    // implementation - internal dependency, not exposed to consumers
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-core:1.8.0")

    // api - exposed to consumers (only in library modules)
    api("com.example:shared-models:1.0.0")

    // compileOnly - needed only at compile time
    compileOnly("org.jetbrains:annotations:24.0.0")

    // runtimeOnly - needed only at runtime
    runtimeOnly("com.h2database:h2:2.2.220")
}
```

### Maven (pom.xml) - Alternative

```xml
<project>
    <modelVersion>4.0.0</modelVersion>
    <groupId>com.example</groupId>
    <artifactId>myapp</artifactId>
    <version>1.0.0</version>

    <properties>
        <kotlin.version>2.3.10</kotlin.version>
        <kotlin.compiler.jvmTarget>21</kotlin.compiler.jvmTarget>
    </properties>

    <dependencies>
        <dependency>
            <groupId>org.jetbrains.kotlin</groupId>
            <artifactId>kotlin-stdlib</artifactId>
            <version>${kotlin.version}</version>
        </dependency>

        <dependency>
            <groupId>org.jetbrains.kotlinx</groupId>
            <artifactId>kotlinx-coroutines-core</artifactId>
            <version>1.8.0</version>
        </dependency>

        <dependency>
            <groupId>org.jetbrains.kotlin</groupId>
            <artifactId>kotlin-test-junit5</artifactId>
            <version>${kotlin.version}</version>
            <scope>test</scope>
        </dependency>
    </dependencies>

    <build>
        <sourceDirectory>src/main/kotlin</sourceDirectory>
        <testSourceDirectory>src/test/kotlin</testSourceDirectory>

        <plugins>
            <plugin>
                <groupId>org.jetbrains.kotlin</groupId>
                <artifactId>kotlin-maven-plugin</artifactId>
                <version>${kotlin.version}</version>
            </plugin>
        </plugins>
    </build>
</project>
```

## Recommended Tooling

| Tool | Purpose |
|------|---------|
| `gradle` | Build automation (Kotlin DSL recommended) |
| `kotlin-test` / `junit-jupiter` | Testing framework |
| `mockk` | Mocking library (Kotlin-native) |
| `ktlint` | Code formatting & linting |
| `detekt` | Static code analysis, code smells |
| `kotlinx-coroutines-test` | Coroutines testing utilities |
| `kotlinx-serialization` | JSON/protobuf serialization |
| `testcontainers` | Integration testing with Docker |
| `kotest` | Alternative testing framework (BDD-style) |

### ktlint Usage

```bash
# Install ktlint
brew install ktlint  # macOS
# Or download from: https://github.com/pinterest/ktlint

# Format code
ktlint -F "src/**/*.kt"

# Check code
ktlint "src/**/*.kt"

# Gradle plugin
# build.gradle.kts
plugins {
    id("org.jlleitschuh.gradle.ktlint") version "12.0.3"
}
```

### detekt Usage

```kotlin
// build.gradle.kts
plugins {
    id("io.gitlab.arturbosch.detekt") version "1.23.0"
}

detekt {
    buildUponDefaultConfig = true
    allRules = false
    config.setFrom(files("$projectDir/config/detekt.yml"))
}

dependencies {
    detektPlugins("io.gitlab.arturbosch.detekt:detekt-formatting:1.23.0")
}
```

## Production Best Practices

1. **Immutability by default** - Use `val` over `var`, immutable collections
2. **Null safety** - Embrace nullable types, avoid `!!` operator
3. **Sealed classes for state** - Type-safe state modeling with exhaustive `when`
4. **Structured concurrency** - Always use `coroutineScope`, never `GlobalScope`
5. **Flow for streams** - Use `StateFlow`/`SharedFlow` for reactive state
6. **Data classes for DTOs** - Automatic `equals`, `hashCode`, `toString`, `copy`
7. **Inline value classes** - Type-safe wrappers without runtime cost
8. **Explicit over implicit** - Clear, readable code over clever tricks
9. **Early returns** - Reduce nesting, improve readability
10. **Descriptive naming** - Functions and properties should explain intent
11. **Prefer expressions** - Use `when`, `if` as expressions when possible
12. **Use extension functions** - Add functionality without inheritance
13. **Coroutine cancellation** - Always handle cancellation properly
14. **Test coroutines properly** - Use `runTest` and `TestDispatcher`
15. **ktlint + detekt** - Automate code quality checks in CI

## Comments - Less is More

```kotlin
// BAD - redundant comment
// Get user from repository
val user = repository.findById(id)

// GOOD - self-explanatory code, no comment needed
val user = repository.findById(id)

// GOOD - comment explains WHY (not obvious)
// Rate limit: API allows max 100 requests per minute per client
rateLimiter.acquire()

// GOOD - KDoc for public API
/**
 * Fetches user by ID. Returns null if user not found.
 *
 * @param id User ID (non-blank)
 * @throws IllegalArgumentException if id is blank
 */
fun findUserById(id: String): User?
```

---

## References

- Kotlin Language Spec: https://kotlinlang.org/spec/
- Kotlin Coding Conventions: https://kotlinlang.org/docs/coding-conventions.html
- Kotlin Coroutines Guide: https://kotlinlang.org/docs/coroutines-guide.html
- Effective Kotlin by Marcin Moskała
- Kotlin in Action by Dmitry Jemerov & Svetlana Isakova
