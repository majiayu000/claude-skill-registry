---
name: lang-kotlin-dev
description: Foundational Kotlin patterns covering null safety, coroutines, data classes, extension functions, and Kotlin idioms. Use when writing Kotlin code or needing guidance on Kotlin development. This is the entry point for Kotlin development.
---

# Kotlin Development Fundamentals

## Overview

Kotlin is a modern, statically typed language targeting JVM, JavaScript, and native platforms. It emphasizes:

- **Null safety** at the type system level (nullable `T?` vs non-nullable `T`)
- **Concise syntax** with data classes, smart casts, and type inference
- **Coroutines** for structured asynchronous programming
- **Full Java interoperability** for gradual migration

**When to use this skill**: Writing Kotlin applications, Android development, migrating from Java, or learning Kotlin idioms.

## Skill Hierarchy

```
lang-kotlin-dev (foundational - THIS SKILL)
├── lang-kotlin-coroutines-eng (advanced concurrency patterns)
├── lang-kotlin-library-dev (library design and publishing)
├── lang-kotlin-patterns-eng (design patterns in Kotlin)
└── lang-kotlin-multiplatform-dev (KMP development)
```

## Quick Reference

| Pattern | When to Use | Key Syntax |
|---------|-------------|------------|
| Null Safety | Handling nullable types | `Type?`, `?.`, `!!`, `?:` |
| Data Classes | Value objects, DTOs | `data class User(val name: String)` |
| Sealed Classes | Restricted hierarchies | `sealed class Result<T>` |
| Extension Functions | Add methods to existing types | `fun String.isPalindrome()` |
| Scope Functions | Context-based operations | `let`, `run`, `with`, `apply`, `also` |
| Coroutines | Asynchronous programming | `suspend`, `launch`, `async` |
| Delegation | Property/class delegation | `by lazy`, `by` keyword |
| Type-Safe Builders | DSL construction | Lambda with receiver |

## Skill Routing

Route to specialized skills when:

- **lang-kotlin-coroutines-eng**: Deep coroutine patterns (Flow, channels, structured concurrency)
- **lang-kotlin-library-dev**: Building and publishing Kotlin libraries
- **lang-kotlin-patterns-eng**: Advanced design patterns and architectural patterns
- **lang-kotlin-multiplatform-dev**: Kotlin Multiplatform projects (KMP)

---

## Module System

Kotlin organizes code into packages and provides visibility modifiers to control access.

### 1.1 Package Declarations

```kotlin
// Package declaration at file top
package com.example.myapp.utils

// Package-level functions (not in a class)
fun helper(): String = "I'm package-level"

// Package-level properties
val VERSION = "1.0.0"
```

### 1.2 Imports

```kotlin
// Single import
import com.example.myapp.User

// Wildcard import (all public members)
import com.example.myapp.utils.*

// Aliased import (resolve naming conflicts)
import com.example.myapp.User as AppUser
import org.external.User as ExternalUser

// Import extension functions
import com.example.extensions.formatCurrency

// Import enum entries
import com.example.Status.ACTIVE
import com.example.Status.INACTIVE
```

### 1.3 Visibility Modifiers

```kotlin
// public (default) - visible everywhere
class PublicClass

// internal - visible within the same module
internal class ModuleClass

// private - visible within the file (top-level) or class
private class FilePrivateClass

class Example {
    public val publicProp = 1      // Visible everywhere
    internal val internalProp = 2   // Same module
    protected val protectedProp = 3 // Subclasses only
    private val privateProp = 4     // This class only
}
```

### 1.4 Object Declarations (Singletons)

```kotlin
// Singleton object
object Logger {
    fun log(message: String) = println(message)
}

// Usage
Logger.log("Hello")

// Companion object (static-like members)
class Factory {
    companion object {
        fun create(): Factory = Factory()
        const val TAG = "Factory"
    }
}

// Usage
val instance = Factory.create()
val tag = Factory.TAG
```

### 1.5 File Organization

```kotlin
// Filename: UserRepository.kt
package com.example.repository

// Multiple classes per file allowed (unlike Java)
data class User(val id: Int, val name: String)
data class UserDto(val id: Int, val displayName: String)

// Extension functions in same file
fun User.toDto() = UserDto(id, name)

// Top-level functions
fun findUserById(id: Int): User? = null
```

**Best Practices**:
- One primary class per file, named after the class
- Group related extension functions with their target type
- Use `internal` for module-private APIs in libraries

---

## 2. Null Safety

Kotlin's type system distinguishes between nullable and non-nullable types, eliminating most null pointer exceptions at compile time.

### 2.1 Nullable Types

```kotlin
// Non-nullable type (default)
var name: String = "Kotlin"
// name = null  // Compilation error

// Nullable type
var nullableName: String? = "Kotlin"
nullableName = null  // OK

// Function parameters
fun greet(name: String?) {
    // Must handle null case
}
```

### 2.2 Safe Call Operator (?.)

```kotlin
val length: Int? = nullableName?.length

// Chaining safe calls
val firstChar: Char? = nullableName?.uppercase()?.firstOrNull()

// Safe calls with let
nullableName?.let { name ->
    println("Name is $name")
}

// Safe call in chains
data class Person(val name: String, val address: Address?)
data class Address(val city: String?)

val city: String? = person?.address?.city
```

### 2.3 Elvis Operator (?:)

```kotlin
// Provide default value for null
val length: Int = nullableName?.length ?: 0

// Return early on null
fun processName(name: String?): String {
    val trimmed = name?.trim() ?: return "No name provided"
    return "Hello, $trimmed"
}

// Throw exception on null
val nonNullName = nullableName ?: throw IllegalArgumentException("Name required")

// Chaining with safe calls
val displayName = person?.name?.trim() ?: "Anonymous"
```

### 2.4 Not-Null Assertion (!!)

```kotlin
// Force unwrap - throws NPE if null
val length: Int = nullableName!!.length

// Use sparingly and only when certain
fun processSurelyNonNull(value: String?) {
    // Only if you're absolutely certain
    val definiteValue: String = value!!
}

// Better: Use assertion with reasoning
val config: Config = loadConfig()
    ?: error("Config must be initialized at startup")
```

**Warning**: Avoid `!!` in production code. Use proper null handling instead.

### 2.5 Safe Casts (as?)

```kotlin
// Safe cast returns null if cast fails
val stringValue: String? = value as? String

// Combined with elvis operator
val length: Int = (value as? String)?.length ?: 0

// Pattern matching alternative
when (value) {
    is String -> println("String of length ${value.length}")
    is Int -> println("Integer: $value")
    else -> println("Unknown type")
}
```

### 2.6 Null Safety Patterns

```kotlin
// Pattern 1: Early return with elvis
fun processUser(user: User?): Result {
    val validUser = user ?: return Result.Error("User not found")
    return Result.Success(validUser)
}

// Pattern 2: Smart casts after null check
fun printLength(value: String?) {
    if (value != null) {
        // value is smart-casted to String
        println(value.length)
    }
}

// Pattern 3: require/check for preconditions
fun processPositive(value: Int?) {
    requireNotNull(value) { "Value must not be null" }
    require(value > 0) { "Value must be positive" }
    // value is smart-casted to Int
}

// Pattern 4: Safe collection operations
val names: List<String?> = listOf("Alice", null, "Bob")
val nonNullNames: List<String> = names.filterNotNull()
val firstNonNull: String? = names.firstOrNull { it != null }
```

---

## 3. Data Classes

Data classes provide automatic implementation of `equals()`, `hashCode()`, `toString()`, and `copy()`.

### 2.1 Basic Data Classes

```kotlin
// Simple data class
data class User(
    val id: Long,
    val name: String,
    val email: String
)

// Automatic implementations
val user1 = User(1, "Alice", "alice@example.com")
val user2 = User(1, "Alice", "alice@example.com")

println(user1 == user2)  // true (structural equality)
println(user1.toString())  // User(id=1, name=Alice, email=alice@example.com)

// Destructuring
val (id, name, email) = user1
println("User $name has ID $id")
```

### 2.2 Copy Method

```kotlin
data class User(
    val id: Long,
    val name: String,
    val email: String,
    val isActive: Boolean = true
)

val user = User(1, "Alice", "alice@example.com")

// Create modified copy
val updatedUser = user.copy(email = "alice@newdomain.com")
val inactiveUser = user.copy(isActive = false)

// Copy preserves other fields
println(updatedUser.name)  // Alice
```

### 2.3 Data Classes with Validation

```kotlin
data class Email(val value: String) {
    init {
        require(value.contains("@")) { "Invalid email format" }
    }
}

data class User(
    val id: Long,
    val name: String,
    val email: Email
) {
    init {
        require(id > 0) { "ID must be positive" }
        require(name.isNotBlank()) { "Name cannot be blank" }
    }
}

// Usage
val user = User(1, "Alice", Email("alice@example.com"))
// val invalid = User(-1, "", Email("invalid"))  // Throws IllegalArgumentException
```

### 2.4 Data Classes with Computed Properties

```kotlin
data class Rectangle(
    val width: Double,
    val height: Double
) {
    // Not part of equals/hashCode/toString
    val area: Double
        get() = width * height

    val perimeter: Double
        get() = 2 * (width + height)

    fun isSquare(): Boolean = width == height
}

val rect = Rectangle(4.0, 5.0)
println(rect.area)  // 20.0
```

### 2.5 Data Classes in Collections

```kotlin
data class User(val id: Long, val name: String)

// Set automatically uses equals/hashCode
val users = setOf(
    User(1, "Alice"),
    User(1, "Alice"),  // Duplicate, ignored
    User(2, "Bob")
)
println(users.size)  // 2

// Map keys
val userMap = mapOf(
    User(1, "Alice") to "admin",
    User(2, "Bob") to "user"
)

// Finding in collections
val alice = User(1, "Alice")
println(userMap[alice])  // admin
```

---

## 4. Sealed Classes and Interfaces

Sealed classes represent restricted hierarchies where all subclasses are known at compile time.

### 3.1 Basic Sealed Classes

```kotlin
// Sealed class for result types
sealed class Result<out T> {
    data class Success<T>(val data: T) : Result<T>()
    data class Error(val exception: Exception) : Result<Nothing>()
    data object Loading : Result<Nothing>()
}

// Exhaustive when expressions
fun <T> handleResult(result: Result<T>) {
    when (result) {
        is Result.Success -> println("Data: ${result.data}")
        is Result.Error -> println("Error: ${result.exception.message}")
        Result.Loading -> println("Loading...")
    }
    // No else branch needed - compiler knows all cases
}
```

### 3.2 Sealed Interfaces

```kotlin
sealed interface NetworkState

data class Connected(val speed: Int) : NetworkState
data class Disconnected(val reason: String) : NetworkState
data object Connecting : NetworkState

fun updateUI(state: NetworkState) {
    when (state) {
        is Connected -> showConnected(state.speed)
        is Disconnected -> showError(state.reason)
        Connecting -> showLoading()
    }
}
```

### 3.3 Nested Sealed Hierarchies

```kotlin
sealed class ApiResponse<out T> {
    data class Success<T>(val body: T) : ApiResponse<T>()

    sealed class Failure : ApiResponse<Nothing>() {
        data class HttpError(val code: Int, val message: String) : Failure()
        data class NetworkError(val exception: Exception) : Failure()
        data object Unauthorized : Failure()
    }

    data object Loading : ApiResponse<Nothing>()
}

fun <T> processResponse(response: ApiResponse<T>) {
    when (response) {
        is ApiResponse.Success -> handleSuccess(response.body)
        is ApiResponse.Failure.HttpError -> handleHttp(response.code)
        is ApiResponse.Failure.NetworkError -> handleNetwork(response.exception)
        ApiResponse.Failure.Unauthorized -> redirectToLogin()
        ApiResponse.Loading -> showSpinner()
    }
}
```

### 3.4 Sealed Classes for State Machines

```kotlin
sealed class OrderState {
    data object Created : OrderState()
    data class Confirmed(val confirmationId: String) : OrderState()
    data class Shipped(val trackingNumber: String) : OrderState()
    data class Delivered(val signature: String) : OrderState()
    data class Cancelled(val reason: String) : OrderState()
}

class Order(var state: OrderState) {
    fun confirm(confirmationId: String) {
        state = when (state) {
            is OrderState.Created -> OrderState.Confirmed(confirmationId)
            else -> throw IllegalStateException("Can only confirm created orders")
        }
    }

    fun ship(trackingNumber: String) {
        state = when (state) {
            is OrderState.Confirmed -> OrderState.Shipped(trackingNumber)
            else -> throw IllegalStateException("Can only ship confirmed orders")
        }
    }
}
```

### 3.5 Pattern: Railway-Oriented Programming

```kotlin
sealed class Either<out L, out R> {
    data class Left<L>(val value: L) : Either<L, Nothing>()
    data class Right<R>(val value: R) : Either<Nothing, R>()
}

// Extension functions for functional pipeline
fun <L, R, T> Either<L, R>.map(f: (R) -> T): Either<L, T> =
    when (this) {
        is Either.Left -> this
        is Either.Right -> Either.Right(f(value))
    }

fun <L, R, T> Either<L, R>.flatMap(f: (R) -> Either<L, T>): Either<L, T> =
    when (this) {
        is Either.Left -> this
        is Either.Right -> f(value)
    }

// Usage
fun validateEmail(email: String): Either<String, String> =
    if (email.contains("@")) Either.Right(email)
    else Either.Left("Invalid email")

fun validateLength(email: String): Either<String, String> =
    if (email.length >= 5) Either.Right(email)
    else Either.Left("Email too short")

val result = validateEmail("test@example.com")
    .flatMap { validateLength(it) }
    .map { it.lowercase() }
```

---

## 5. Extension Functions

Extension functions add new functions to existing classes without modifying their source code.

### 4.1 Basic Extensions

```kotlin
// Extend String
fun String.isPalindrome(): Boolean {
    val cleaned = this.lowercase().filter { it.isLetterOrDigit() }
    return cleaned == cleaned.reversed()
}

println("A man a plan a canal Panama".isPalindrome())  // true

// Extend nullable types
fun String?.orDefault(default: String): String = this ?: default

val name: String? = null
println(name.orDefault("Guest"))  // Guest
```

### 4.2 Extension Properties

```kotlin
// Read-only extension property
val String.wordCount: Int
    get() = split("\\s+".toRegex()).size

println("Hello world from Kotlin".wordCount)  // 4

// Extension property with backing field not allowed
// Must use get() or set()
var StringBuilder.lastChar: Char
    get() = this[length - 1]
    set(value) {
        this[length - 1] = value
    }
```

### 4.3 Generic Extensions

```kotlin
// Generic extension for any type
fun <T> T.print(): T {
    println(this)
    return this
}

"Hello".print().uppercase().print()

// Extension with type constraints
fun <T : Comparable<T>> List<T>.second(): T? =
    if (size >= 2) this[1] else null

// Extension for collections
fun <T> List<T>.secondOrNull(): T? =
    if (size >= 2) this[1] else null

println(listOf(1, 2, 3).secondOrNull())  // 2
```

### 4.4 Extensions on Companion Objects

```kotlin
class User(val name: String) {
    companion object {
        // Regular companion object function
    }
}

// Extension on companion object
fun User.Companion.fromJson(json: String): User {
    // Parse JSON and create User
    return User("Parsed from JSON")
}

// Usage
val user = User.fromJson("""{"name": "Alice"}""")
```

### 4.5 Scope-Limited Extensions

```kotlin
// Extension only visible in this scope
class HtmlBuilder {
    private fun String.escapeHtml(): String =
        replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")

    fun paragraph(text: String): String =
        "<p>${text.escapeHtml()}</p>"
}

// Extension not visible outside HtmlBuilder
```

### 4.6 Common Extension Patterns

```kotlin
// Collection extensions
fun <T> List<T>.splitAt(index: Int): Pair<List<T>, List<T>> =
    take(index) to drop(index)

fun <K, V> Map<K, V>.getOrThrow(key: K): V =
    this[key] ?: throw NoSuchElementException("Key $key not found")

// Validation extensions
fun String.requireNotBlank(fieldName: String): String {
    require(isNotBlank()) { "$fieldName cannot be blank" }
    return this
}

// Transformation extensions
fun String.toTitleCase(): String =
    split(" ").joinToString(" ") { word ->
        word.lowercase().replaceFirstChar { it.uppercase() }
    }

// Utility extensions
inline fun <T> T.applyIf(condition: Boolean, block: T.() -> Unit): T {
    if (condition) block()
    return this
}

val list = mutableListOf(1, 2, 3)
    .applyIf(someCondition) { add(4) }
```

---

## 6. Scope Functions

Scope functions execute a block of code within the context of an object.

### 5.1 let - Null Safety and Transformations

```kotlin
// Execute block if not null
val name: String? = "Alice"
name?.let {
    println("Name is $it")
    println("Length is ${it.length}")
}

// Transform and return result
val length = name?.let { it.length } ?: 0

// Chain operations
val result = getUserInput()
    ?.trim()
    ?.let { parseUserData(it) }
    ?.let { validateData(it) }
    ?.let { saveToDatabase(it) }

// Scope to new variable
val validatedEmail = email?.let { value ->
    if (value.contains("@")) value else null
}
```

### 5.2 run - Object Configuration and Computation

```kotlin
// Run on nullable receiver
val config: Config? = loadConfig()
val port = config?.run {
    validate()
    applyDefaults()
    port
} ?: 8080

// Compute with context
val hexColor = run {
    val r = (color shr 16) and 0xFF
    val g = (color shr 8) and 0xFF
    val b = color and 0xFF
    "#%02X%02X%02X".format(r, g, b)
}

// Scope local variables
val result = run {
    val a = computeA()
    val b = computeB()
    a + b
}
```

### 5.3 with - Multiple Operations on Same Object

```kotlin
// Non-extension function
val person = Person()
with(person) {
    name = "Alice"
    age = 30
    email = "alice@example.com"
    validate()
}

// Return value from with
val result = with(StringBuilder()) {
    append("Hello")
    append(" ")
    append("World")
    toString()
}

// Multiple property access
val info = with(user) {
    "Name: $name, Email: $email, Active: $isActive"
}
```

### 5.4 apply - Object Configuration (Returns Receiver)

```kotlin
// Builder-style configuration
val person = Person().apply {
    name = "Alice"
    age = 30
    email = "alice@example.com"
}

// Chain multiple apply blocks
val request = HttpRequest().apply {
    url = "https://api.example.com"
    method = "POST"
}.apply {
    addHeader("Content-Type", "application/json")
    addHeader("Authorization", "Bearer $token")
}.apply {
    body = """{"data": "value"}"""
}

// Conditional configuration
val user = User().apply {
    name = "Alice"
    if (isAdmin) {
        role = "ADMIN"
        permissions = adminPermissions
    }
}
```

### 5.5 also - Side Effects (Returns Receiver)

```kotlin
// Logging and debugging
val result = processData(input)
    .also { println("Processed result: $it") }
    .also { log.debug("Result details: $it") }

// Validation before return
fun createUser(name: String): User {
    return User(name).also {
        require(it.isValid()) { "Invalid user" }
        saveToDatabase(it)
    }
}

// Multiple side effects
val file = File("output.txt")
    .also { it.createNewFile() }
    .also { it.setWritable(true) }
    .also { it.writeText("Hello") }
```

### 5.6 Choosing the Right Scope Function

```kotlin
// Decision guide:

// let - Transform nullable, introduce local scope
val length: Int = nullableString?.let { it.length } ?: 0

// run - Compute value using multiple statements
val total = run {
    val subtotal = items.sumOf { it.price }
    val tax = subtotal * 0.1
    subtotal + tax
}

// with - Multiple operations, focus on context
with(canvas) {
    drawLine(0, 0, width, height)
    drawCircle(width / 2, height / 2, 50)
}

// apply - Configure object, return it
val person = Person().apply {
    name = "Alice"
    age = 30
}

// also - Side effects, return object
val saved = user.also { repository.save(it) }
```

### 5.7 Nested Scope Functions

```kotlin
// Chaining different scope functions
val result = fetchUser(id)
    ?.let { user ->
        user.apply {
            lastLoginAt = Instant.now()
        }
    }
    ?.also { repository.save(it) }
    ?.let { user ->
        UserDto(user.id, user.name)
    }

// Complex transformations
val config = loadConfig()
    ?.run {
        validate()
        this
    }
    ?.apply {
        applyDefaults()
    }
    ?.also { logger.info("Config loaded: $it") }
    ?: DefaultConfig()
```

---

## 7. Collections and Sequences

Kotlin provides rich collection APIs with eager (collections) and lazy (sequences) evaluation.

### 6.1 Collection Basics

```kotlin
// List (immutable)
val numbers = listOf(1, 2, 3, 4, 5)
val empty = emptyList<Int>()

// MutableList
val mutable = mutableListOf(1, 2, 3)
mutable.add(4)
mutable.removeAt(0)

// Set (unique elements)
val uniqueNumbers = setOf(1, 2, 2, 3, 3)  // [1, 2, 3]
val mutableSet = mutableSetOf<String>()

// Map
val ages = mapOf("Alice" to 30, "Bob" to 25)
val mutableMap = mutableMapOf<String, Int>()
mutableMap["Charlie"] = 35
```

### 6.2 Collection Transformations

```kotlin
val numbers = listOf(1, 2, 3, 4, 5)

// map - Transform each element
val squared = numbers.map { it * it }  // [1, 4, 9, 16, 25]

// filter - Keep matching elements
val evens = numbers.filter { it % 2 == 0 }  // [2, 4]

// mapNotNull - Transform and filter nulls
val strings = listOf("1", "2", "abc", "3")
val parsed = strings.mapNotNull { it.toIntOrNull() }  // [1, 2, 3]

// flatMap - Transform and flatten
val nested = listOf(listOf(1, 2), listOf(3, 4))
val flattened = nested.flatMap { it }  // [1, 2, 3, 4]

// partition - Split into two lists
val (evens, odds) = numbers.partition { it % 2 == 0 }

// groupBy - Group into map
val byParity = numbers.groupBy { if (it % 2 == 0) "even" else "odd" }
// {odd=[1, 3, 5], even=[2, 4]}
```

### 6.3 Collection Aggregations

```kotlin
val numbers = listOf(1, 2, 3, 4, 5)

// sum, average, min, max
val sum = numbers.sum()  // 15
val avg = numbers.average()  // 3.0
val max = numbers.maxOrNull()  // 5

// sumOf - Transform then sum
val lengthSum = listOf("a", "bb", "ccc").sumOf { it.length }  // 6

// reduce - Combine elements
val product = numbers.reduce { acc, n -> acc * n }  // 120

// fold - Reduce with initial value
val sumPlus10 = numbers.fold(10) { acc, n -> acc + n }  // 25

// joinToString - Create string
val csv = numbers.joinToString(separator = ",")  // "1,2,3,4,5"
val custom = numbers.joinToString(
    separator = " | ",
    prefix = "[",
    postfix = "]",
    limit = 3,
    truncated = "..."
) { "Item $it" }
// [Item 1 | Item 2 | Item 3 | ...]
```

### 6.4 Collection Queries

```kotlin
val numbers = listOf(1, 2, 3, 4, 5)

// any, all, none
val hasEven = numbers.any { it % 2 == 0 }  // true
val allPositive = numbers.all { it > 0 }  // true
val noneNegative = numbers.none { it < 0 }  // true

// find, first, last
val firstEven = numbers.find { it % 2 == 0 }  // 2
val firstOrNull = numbers.firstOrNull { it > 10 }  // null
val last = numbers.last()  // 5

// take, drop, slice
val first3 = numbers.take(3)  // [1, 2, 3]
val without2 = numbers.drop(2)  // [3, 4, 5]
val middle = numbers.slice(1..3)  // [2, 3, 4]

// distinct, distinctBy
val duplicates = listOf(1, 2, 2, 3, 3, 3)
val unique = duplicates.distinct()  // [1, 2, 3]

data class Person(val name: String, val age: Int)
val people = listOf(Person("Alice", 30), Person("Bob", 30))
val byAge = people.distinctBy { it.age }  // [Person("Alice", 30)]
```

### 6.5 Sequences (Lazy Evaluation)

```kotlin
// Sequence - lazy evaluation
val sequence = sequenceOf(1, 2, 3, 4, 5)

// Convert to sequence for lazy evaluation
val numbers = listOf(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)

// Eager (collection) - all operations execute immediately
val eagerResult = numbers
    .map { println("map $it"); it * 2 }  // Prints 10 times
    .filter { println("filter $it"); it > 10 }  // Prints 10 times
    .take(2)  // Still processed all elements

// Lazy (sequence) - operations execute on demand
val lazyResult = numbers.asSequence()
    .map { println("map $it"); it * 2 }
    .filter { println("filter $it"); it > 10 }
    .take(2)  // Only processes until 2 elements found
    .toList()

// Generate infinite sequence
val naturalNumbers = generateSequence(1) { it + 1 }
val first100Even = naturalNumbers
    .filter { it % 2 == 0 }
    .take(100)
    .toList()

// Sequence from function
val fibonacci = sequence {
    var a = 0
    var b = 1
    while (true) {
        yield(a)
        val next = a + b
        a = b
        b = next
    }
}

val first10Fib = fibonacci.take(10).toList()
```

### 6.6 Collection Building

```kotlin
// buildList - Builder function
val squares = buildList {
    for (i in 1..5) {
        add(i * i)
    }
    if (someCondition) {
        add(100)
    }
}

// buildSet
val uniqueWords = buildSet {
    add("hello")
    add("world")
    add("hello")  // Duplicate ignored
}

// buildMap
val characterCounts = buildMap {
    for (char in "hello") {
        put(char, getOrDefault(char, 0) + 1)
    }
}

// associate - Build map from collection
val users = listOf(User(1, "Alice"), User(2, "Bob"))
val byId = users.associateBy { it.id }
val byName = users.associateBy({ it.name }, { it.id })
```

### 6.7 Advanced Collection Patterns

```kotlin
// Windowed - Sliding windows
val numbers = listOf(1, 2, 3, 4, 5)
val windows = numbers.windowed(size = 3, step = 1)
// [[1, 2, 3], [2, 3, 4], [3, 4, 5]]

// Chunked - Fixed-size groups
val chunks = numbers.chunked(2)  // [[1, 2], [3, 4], [5]]

// Zip - Combine two collections
val names = listOf("Alice", "Bob")
val ages = listOf(30, 25)
val pairs = names.zip(ages)  // [(Alice, 30), (Bob, 25)]
val combined = names.zip(ages) { name, age -> "$name is $age" }

// Union, intersect, subtract (Sets)
val set1 = setOf(1, 2, 3)
val set2 = setOf(2, 3, 4)
val union = set1 union set2  // [1, 2, 3, 4]
val intersect = set1 intersect set2  // [2, 3]
val subtract = set1 subtract set2  // [1]
```

---

## 8. Higher-Order Functions and Lambdas

Functions that take functions as parameters or return functions.

### 7.1 Lambda Syntax

```kotlin
// Lambda expression
val sum: (Int, Int) -> Int = { a, b -> a + b }
println(sum(2, 3))  // 5

// Single parameter - implicit 'it'
val square: (Int) -> Int = { it * it }
println(square(5))  // 25

// No parameters
val greeting: () -> String = { "Hello" }
println(greeting())  // Hello

// Multiple statements
val process: (Int) -> Int = { value ->
    val doubled = value * 2
    val squared = doubled * doubled
    squared  // Last expression is return value
}
```

### 7.2 Function Types

```kotlin
// Function type notation
val operation: (Int, Int) -> Int = { a, b -> a + b }

// Nullable function type
val nullableOp: ((Int, Int) -> Int)? = null

// Function type with receiver
val stringBuilder: StringBuilder.() -> Unit = {
    append("Hello")
    append(" World")
}

// Higher-order function
fun calculate(a: Int, b: Int, op: (Int, Int) -> Int): Int {
    return op(a, b)
}

println(calculate(5, 3, { a, b -> a + b }))  // 8
println(calculate(5, 3) { a, b -> a * b })  // 15 (trailing lambda)
```

### 7.3 Trailing Lambda Syntax

```kotlin
// When last parameter is function, move outside parentheses
val numbers = listOf(1, 2, 3, 4, 5)

// Standard syntax
numbers.filter({ it % 2 == 0 })

// Trailing lambda
numbers.filter { it % 2 == 0 }

// Only lambda parameter - omit parentheses
numbers.forEach { println(it) }

// Multiple parameters with trailing lambda
numbers.fold(0) { acc, n -> acc + n }
```

### 7.4 Function References

```kotlin
// Top-level function reference
fun isEven(n: Int): Boolean = n % 2 == 0

val numbers = listOf(1, 2, 3, 4, 5)
val evens = numbers.filter(::isEven)

// Member function reference
class StringUtils {
    fun isPalindrome(s: String): Boolean {
        return s == s.reversed()
    }
}

val utils = StringUtils()
val words = listOf("level", "hello", "radar")
val palindromes = words.filter(utils::isPalindrome)

// Constructor reference
data class Person(val name: String, val age: Int)
val names = listOf("Alice", "Bob")
val people = names.map(::Person)  // Partial application not supported
```

### 7.5 Inline Functions

```kotlin
// Inline function - lambda code inlined at call site
inline fun <T> measureTime(block: () -> T): T {
    val start = System.currentTimeMillis()
    val result = block()
    val end = System.currentTimeMillis()
    println("Took ${end - start}ms")
    return result
}

// Usage - no lambda object created
val result = measureTime {
    Thread.sleep(100)
    42
}

// noinline - Don't inline specific lambda
inline fun complexOperation(
    inline operation: () -> Unit,
    noinline callback: () -> Unit
) {
    operation()
    storeCallback(callback)  // Can store noinline lambda
}

// crossinline - Lambda can't use non-local returns
inline fun runAsync(crossinline block: () -> Unit) {
    thread {
        block()  // Would fail without crossinline if block has return
    }
}
```

### 7.6 Returning Functions

```kotlin
// Function that returns function
fun makeMultiplier(factor: Int): (Int) -> Int {
    return { value -> value * factor }
}

val double = makeMultiplier(2)
val triple = makeMultiplier(3)

println(double(5))  // 10
println(triple(5))  // 15

// Closure captures variables
fun makeCounter(): () -> Int {
    var count = 0
    return { ++count }
}

val counter = makeCounter()
println(counter())  // 1
println(counter())  // 2
println(counter())  // 3
```

### 7.7 Common Higher-Order Function Patterns

```kotlin
// Retry pattern
inline fun <T> retry(
    times: Int = 3,
    delay: Long = 1000,
    block: () -> T
): T {
    repeat(times - 1) {
        try {
            return block()
        } catch (e: Exception) {
            Thread.sleep(delay)
        }
    }
    return block()  // Last attempt throws if fails
}

// Resource management
inline fun <T : AutoCloseable, R> T.use(block: (T) -> R): R {
    try {
        return block(this)
    } finally {
        close()
    }
}

// Memoization
fun <P, R> memoize(fn: (P) -> R): (P) -> R {
    val cache = mutableMapOf<P, R>()
    return { param ->
        cache.getOrPut(param) { fn(param) }
    }
}

val fibonacci = memoize<Int, Long> { n ->
    if (n <= 1) n.toLong()
    else fibonacci(n - 1) + fibonacci(n - 2)
}
```

---

## 9. Coroutines Basics

Kotlin coroutines provide asynchronous programming support with sequential-looking code.

### 8.1 Suspend Functions

```kotlin
import kotlinx.coroutines.*

// Suspend function - can only be called from coroutine or another suspend function
suspend fun fetchUser(id: Long): User {
    delay(1000)  // Non-blocking delay
    return User(id, "Alice")
}

suspend fun fetchPosts(userId: Long): List<Post> {
    delay(500)
    return listOf(Post(1, "Hello"), Post(2, "World"))
}

// Calling suspend functions
suspend fun loadUserData(id: Long): UserData {
    val user = fetchUser(id)  // Sequential execution
    val posts = fetchPosts(user.id)
    return UserData(user, posts)
}
```

### 8.2 Coroutine Builders

```kotlin
import kotlinx.coroutines.*

// launch - Fire and forget
fun main() = runBlocking {
    launch {
        delay(1000)
        println("World")
    }
    println("Hello")
    // Output: Hello, World (after 1 second)
}

// async - Return value
fun main() = runBlocking {
    val deferred = async {
        delay(1000)
        "Result"
    }
    println("Waiting...")
    val result = deferred.await()  // Suspend until result ready
    println(result)
}

// runBlocking - Bridge to coroutine world
fun main() {
    runBlocking {
        launch {
            delay(1000)
            println("Coroutine")
        }
        println("Main")
    }
    println("Done")
}
```

### 8.3 Concurrent Execution

```kotlin
suspend fun loadUserData(id: Long): UserData = coroutineScope {
    // Sequential (slow)
    val user = fetchUser(id)
    val posts = fetchPosts(id)

    // Concurrent (fast)
    val userDeferred = async { fetchUser(id) }
    val postsDeferred = async { fetchPosts(id) }

    UserData(
        user = userDeferred.await(),
        posts = postsDeferred.await()
    )
}

// Multiple concurrent operations
suspend fun loadDashboard(): Dashboard = coroutineScope {
    val user = async { fetchUser() }
    val notifications = async { fetchNotifications() }
    val messages = async { fetchMessages() }
    val stats = async { fetchStats() }

    Dashboard(
        user.await(),
        notifications.await(),
        messages.await(),
        stats.await()
    )
}
```

### 8.4 Coroutine Context and Dispatchers

```kotlin
import kotlinx.coroutines.*

// Dispatchers.Default - CPU-intensive work
launch(Dispatchers.Default) {
    val result = performHeavyComputation()
}

// Dispatchers.IO - I/O operations
launch(Dispatchers.IO) {
    val data = readFromDatabase()
}

// Dispatchers.Main - UI operations (Android/Desktop)
launch(Dispatchers.Main) {
    updateUI(data)
}

// Switch contexts
suspend fun fetchAndDisplay() {
    val data = withContext(Dispatchers.IO) {
        fetchFromNetwork()
    }
    withContext(Dispatchers.Main) {
        displayData(data)
    }
}
```

### 8.5 Structured Concurrency

```kotlin
// coroutineScope - Creates scope, suspends until all children complete
suspend fun processAll(items: List<Item>): List<Result> = coroutineScope {
    items.map { item ->
        async { processItem(item) }
    }.awaitAll()  // Waits for all to complete
}

// supervisorScope - Children failures don't cancel siblings
suspend fun fetchMultiple(): List<Data?> = supervisorScope {
    val results = listOf(
        async { fetchFromSource1() },
        async { fetchFromSource2() },  // If this fails...
        async { fetchFromSource3() }   // ...this still runs
    )

    results.map {
        try { it.await() }
        catch (e: Exception) { null }
    }
}

// Cancellation
val job = launch {
    repeat(1000) { i ->
        println("Job: $i")
        delay(500)
    }
}

delay(2000)
job.cancel()  // Cancel the job
job.join()    // Wait for cancellation to complete
```

### 8.6 Exception Handling in Coroutines

```kotlin
// try-catch in coroutines
suspend fun safeOperation(): Result<Data> {
    return try {
        val data = fetchData()
        Result.Success(data)
    } catch (e: Exception) {
        Result.Error(e)
    }
}

// CoroutineExceptionHandler
val handler = CoroutineExceptionHandler { _, exception ->
    println("Caught $exception")
}

val scope = CoroutineScope(Dispatchers.Default + handler)
scope.launch {
    throw Exception("Failed")
}

// supervisorScope with exception handling
suspend fun robustFetch(): List<Data?> = supervisorScope {
    val sources = listOf(source1, source2, source3)
    sources.map { source ->
        async {
            try {
                source.fetch()
            } catch (e: Exception) {
                logger.error("Failed to fetch from $source", e)
                null
            }
        }
    }.awaitAll()
}
```

### 8.7 Common Coroutine Patterns

```kotlin
// Timeout
suspend fun fetchWithTimeout(id: Long): User? {
    return try {
        withTimeout(5000) {  // 5 second timeout
            fetchUser(id)
        }
    } catch (e: TimeoutCancellationException) {
        null
    }
}

// Retry with delay
suspend fun fetchWithRetry(maxAttempts: Int = 3): Data {
    repeat(maxAttempts - 1) { attempt ->
        try {
            return fetchData()
        } catch (e: Exception) {
            delay(1000 * (attempt + 1))  // Exponential backoff
        }
    }
    return fetchData()  // Last attempt
}

// Parallel processing with limit
suspend fun processInParallel(
    items: List<Item>,
    concurrency: Int = 10
): List<Result> = coroutineScope {
    items.chunked(concurrency).flatMap { chunk ->
        chunk.map { item ->
            async { processItem(item) }
        }.awaitAll()
    }
}
```

---

## 10. Kotlin Idioms

Idiomatic Kotlin patterns that make code more concise and expressive.

### 9.1 String Templates

```kotlin
val name = "Alice"
val age = 30

// Simple interpolation
val greeting = "Hello, $name!"

// Expressions in templates
val info = "Name: $name, Age: $age, Adult: ${age >= 18}"

// Multi-line strings
val json = """
    {
        "name": "$name",
        "age": $age,
        "address": {
            "city": "New York"
        }
    }
""".trimIndent()

// Raw strings with custom margin
val sql = """
    |SELECT *
    |FROM users
    |WHERE name = '$name'
    |AND age > $age
""".trimMargin()
```

### 9.2 Destructuring

```kotlin
// Data classes
data class User(val id: Long, val name: String, val email: String)
val user = User(1, "Alice", "alice@example.com")
val (id, name, email) = user

// Pairs and Triples
val pair = "key" to "value"
val (key, value) = pair

// In loops
val map = mapOf("a" to 1, "b" to 2, "c" to 3)
for ((key, value) in map) {
    println("$key -> $value")
}

// Component functions for custom types
class Range(val start: Int, val end: Int) {
    operator fun component1() = start
    operator fun component2() = end
}

val range = Range(1, 10)
val (start, end) = range
```

### 9.3 Smart Casts

```kotlin
// After type check, automatic cast
fun process(value: Any) {
    if (value is String) {
        // value is automatically String here
        println(value.length)
    }
}

// Smart cast with when
fun describe(obj: Any): String = when (obj) {
    is String -> "String of length ${obj.length}"
    is Int -> "Integer: $obj"
    is List<*> -> "List of size ${obj.size}"
    else -> "Unknown type"
}

// Smart cast after null check
fun printLength(str: String?) {
    if (str != null) {
        // str is automatically String (non-null)
        println(str.length)
    }
}

// Smart cast with require/check
fun process(value: Any) {
    require(value is String) { "Must be String" }
    // value is String here
    println(value.uppercase())
}
```

### 9.4 Named Arguments and Default Parameters

```kotlin
// Default parameters
fun createUser(
    name: String,
    age: Int = 18,
    email: String? = null,
    isActive: Boolean = true
) = User(name, age, email, isActive)

// Call with defaults
val user1 = createUser("Alice")
val user2 = createUser("Bob", age = 25)
val user3 = createUser("Charlie", email = "charlie@example.com", age = 30)

// Named arguments improve readability
val rect = Rectangle(
    width = 100.0,
    height = 50.0,
    color = Color.RED,
    borderWidth = 2.0
)

// Reordering with named arguments
fun formatDate(
    day: Int,
    month: Int,
    year: Int,
    separator: String = "-"
): String = "$year$separator$month$separator$day"

val date = formatDate(year = 2024, month = 3, day = 15)
```

### 9.5 Single Expression Functions

```kotlin
// Function with expression body
fun square(x: Int): Int = x * x

// Type inference
fun double(x: Int) = x * 2

// With when expression
fun sign(x: Int) = when {
    x > 0 -> "positive"
    x < 0 -> "negative"
    else -> "zero"
}

// With if expression
fun max(a: Int, b: Int) = if (a > b) a else b

// Chained calls
fun processName(name: String) = name
    .trim()
    .lowercase()
    .replaceFirstChar { it.uppercase() }
```

### 9.6 Operator Overloading

```kotlin
// Arithmetic operators
data class Point(val x: Int, val y: Int) {
    operator fun plus(other: Point) = Point(x + other.x, y + other.y)
    operator fun minus(other: Point) = Point(x - other.x, y - other.y)
    operator fun times(scale: Int) = Point(x * scale, y * scale)
}

val p1 = Point(1, 2)
val p2 = Point(3, 4)
val p3 = p1 + p2  // Point(4, 6)
val p4 = p1 * 2   // Point(2, 4)

// Comparison operators
data class Version(val major: Int, val minor: Int, val patch: Int) : Comparable<Version> {
    override fun compareTo(other: Version): Int {
        if (major != other.major) return major - other.major
        if (minor != other.minor) return minor - other.minor
        return patch - other.patch
    }
}

val v1 = Version(1, 2, 3)
val v2 = Version(1, 3, 0)
println(v1 < v2)  // true

// Index operators
class MutableGrid<T>(private val data: Array<Array<T>>) {
    operator fun get(row: Int, col: Int): T = data[row][col]
    operator fun set(row: Int, col: Int, value: T) {
        data[row][col] = value
    }
}

// Invoke operator
class Greeter(val greeting: String) {
    operator fun invoke(name: String) = "$greeting, $name!"
}

val greet = Greeter("Hello")
println(greet("Alice"))  // Hello, Alice!
```

### 9.7 Delegation

```kotlin
// Property delegation
class User {
    // Lazy initialization
    val expensiveData: Data by lazy {
        loadExpensiveData()
    }

    // Observable property
    var name: String by Delegates.observable("<no name>") { _, old, new ->
        println("Name changed from $old to $new")
    }

    // Veto changes
    var age: Int by Delegates.vetoable(0) { _, old, new ->
        new >= 0  // Only allow non-negative ages
    }
}

// Map delegation
class Config(map: Map<String, Any?>) {
    val host: String by map
    val port: Int by map
    val timeout: Long by map
}

val config = Config(mapOf(
    "host" to "localhost",
    "port" to 8080,
    "timeout" to 5000L
))

// Class delegation
interface Repository {
    fun save(data: Data)
    fun load(id: Long): Data
}

class CachingRepository(
    private val delegate: Repository,
    private val cache: Cache
) : Repository by delegate {
    // Override specific methods
    override fun load(id: Long): Data {
        return cache.get(id) ?: delegate.load(id).also {
            cache.put(id, it)
        }
    }
}
```

### 9.8 Type Aliases

```kotlin
// Type alias for complex types
typealias UserId = Long
typealias Predicate<T> = (T) -> Boolean
typealias StringMap = Map<String, String>

// Generic type alias
typealias ResultCallback<T> = (Result<T>) -> Unit

// Usage
fun findUser(id: UserId): User? = database.find(id)

fun filter(items: List<Int>, predicate: Predicate<Int>): List<Int> =
    items.filter(predicate)

val config: StringMap = mapOf("key" to "value")

// Type alias for function types
typealias ClickHandler = (View, Int) -> Unit

fun setClickListener(handler: ClickHandler) {
    // ...
}
```

---

## 11. Java Interoperability

Kotlin provides seamless interop with Java code.

### 10.1 Calling Java from Kotlin

```kotlin
// Java getter/setter accessed as properties
val list = ArrayList<String>()  // Java class
list.add("Kotlin")              // Java method
println(list.size)              // Java getSize() -> size property

// Java void methods
val file = File("test.txt")
file.createNewFile()  // Java void method

// Static methods
val sqrt = Math.sqrt(16.0)  // Java static method

// Object methods from Java
val stream = File("data.txt").inputStream()
```

### 10.2 Null Safety with Java

```kotlin
// Platform types (Type!) - nullable unknown
val javaString: String = getJavaString()  // May throw NPE if null

// Explicit nullable handling
val safeString: String? = getJavaString()
val length: Int = safeString?.length ?: 0

// Annotated Java code
// If Java uses @Nullable/@NotNull
val nullable: String? = getAnnotatedNullable()  // Kotlin knows it's nullable
val nonNull: String = getAnnotatedNonNull()     // Kotlin knows it's not null
```

### 10.3 Calling Kotlin from Java

```kotlin
// Kotlin code
class KotlinClass {
    // Becomes static method in Java
    companion object {
        @JvmStatic
        fun create(): KotlinClass = KotlinClass()
    }

    // Default parameters need @JvmOverloads
    @JvmOverloads
    fun greet(name: String, greeting: String = "Hello") =
        "$greeting, $name"
}

// Java usage
KotlinClass obj = KotlinClass.create();
String msg1 = obj.greet("Alice");
String msg2 = obj.greet("Bob", "Hi");
```

### 10.4 JVM Annotations

```kotlin
// @JvmName - Change JVM name
@file:JvmName("Utils")
package com.example

fun helper() { }
// Java: Utils.helper()

// @JvmStatic - Static method/field
object Singleton {
    @JvmStatic
    fun getInstance(): Singleton = this

    @JvmField
    val CONSTANT = 42
}

// @JvmOverloads - Generate overloads for default params
class User @JvmOverloads constructor(
    val name: String,
    val age: Int = 0,
    val email: String? = null
)
// Java can call: new User("Alice"), new User("Alice", 30), etc.

// @Throws - Declare checked exceptions
@Throws(IOException::class)
fun readFile(path: String): String {
    return File(path).readText()
}
```

### 10.5 SAM Conversions

```kotlin
// Java interface with single abstract method
// interface Runnable { void run(); }

// Kotlin lambda automatically converts
val runnable = Runnable { println("Running") }

// Java functional interfaces
val listener = ActionListener { event ->
    println("Action performed: $event")
}

// Explicit SAM constructor
val callback = Callback { result ->
    handleResult(result)
}
```

### 10.6 Handling Java Collections

```kotlin
// Java collections are mutable in Kotlin
val javaList: MutableList<String> = ArrayList()
javaList.add("Kotlin")

// Converting to Kotlin immutable
val kotlinList: List<String> = javaList.toList()

// Extension functions work on Java collections
val upperCased = javaList.map { it.uppercase() }

// Kotlin collection to Java
val kotlinSet = setOf(1, 2, 3)
val javaSet: java.util.Set<Int> = kotlinSet.toSet()
```

---

## 12. Best Practices

### 11.1 Prefer Immutability

```kotlin
// Use val instead of var
val name = "Alice"  // Preferred
var mutableName = "Bob"  // Use when mutation needed

// Immutable collections
val list = listOf(1, 2, 3)  // Preferred
val mutableList = mutableListOf(1, 2, 3)  // Use when mutation needed

// Immutable data classes
data class User(val id: Long, val name: String)

// Use copy() for changes
val user = User(1, "Alice")
val updated = user.copy(name = "Alicia")
```

### 11.2 Null Safety Best Practices

```kotlin
// Prefer non-null types
fun greet(name: String) {  // Preferred
    println("Hello, $name")
}

// Only use nullable when truly optional
fun findUser(id: Long): User?  // Returns null if not found

// Avoid !! operator
val user = getUser()!!  // Avoid - may throw NPE

// Better alternatives
val user = getUser() ?: return  // Early return
val user = getUser() ?: throw IllegalStateException("User required")
val name = getUser()?.name ?: "Unknown"
```

### 11.3 Scope Function Usage

```kotlin
// Use let for null safety and transformations
user?.let { u ->
    processUser(u)
    saveUser(u)
}

// Use apply for object configuration
val person = Person().apply {
    name = "Alice"
    age = 30
}

// Use also for side effects
val user = createUser().also {
    logger.info("Created user: ${it.id}")
    cache.put(it.id, it)
}

// Use run for complex computations
val result = run {
    val a = computeA()
    val b = computeB()
    combine(a, b)
}

// Use with for multiple operations on same object
with(canvas) {
    drawLine(0, 0, 100, 100)
    drawCircle(50, 50, 25)
}
```

### 11.4 Prefer Expressions Over Statements

```kotlin
// Use when expression
val result = when (status) {
    Status.SUCCESS -> handleSuccess()
    Status.ERROR -> handleError()
    Status.PENDING -> handlePending()
}

// Use if expression
val max = if (a > b) a else b

// Use try expression
val result = try {
    dangerousOperation()
} catch (e: Exception) {
    defaultValue
}
```

### 11.5 Leverage Type Inference

```kotlin
// Let compiler infer types when obvious
val name = "Alice"  // Type inferred as String
val numbers = listOf(1, 2, 3)  // List<Int>

// Specify type when it aids readability
val result: Result<User> = processUser()  // Clarity
val callback: (Int) -> Unit = { processValue(it) }  // Clarity
```

### 11.6 Use Extension Functions Wisely

```kotlin
// Good: Utility operations
fun String.isEmail(): Boolean = contains("@") && contains(".")

// Good: Domain-specific operations
fun User.isAdult(): Boolean = age >= 18

// Avoid: Extending too broadly
fun Any.doSomething() { }  // Too broad, avoid

// Avoid: Complex logic that should be in a class
// Long extension functions with many dependencies -> use class instead
```

---

## 13. Common Patterns

### 12.1 Builder Pattern

```kotlin
// Kotlin builder with DSL
class HttpRequest private constructor(
    val url: String,
    val method: String,
    val headers: Map<String, String>,
    val body: String?
) {
    class Builder {
        var url: String = ""
        var method: String = "GET"
        private val headers = mutableMapOf<String, String>()
        var body: String? = null

        fun header(key: String, value: String) = apply {
            headers[key] = value
        }

        fun build() = HttpRequest(url, method, headers, body)
    }
}

// Usage with apply
val request = HttpRequest.Builder().apply {
    url = "https://api.example.com"
    method = "POST"
    header("Content-Type", "application/json")
    body = """{"key": "value"}"""
}.build()

// Type-safe builder DSL
class Html {
    private val children = mutableListOf<Tag>()

    fun body(init: Body.() -> Unit) {
        children.add(Body().apply(init))
    }
}

class Body {
    fun p(text: String) {
        // Add paragraph
    }
}

// Usage
fun html(init: Html.() -> Unit): Html = Html().apply(init)

val page = html {
    body {
        p("Hello")
        p("World")
    }
}
```

### 12.2 Sealed Class for State

```kotlin
sealed class UiState<out T> {
    data object Idle : UiState<Nothing>()
    data object Loading : UiState<Nothing>()
    data class Success<T>(val data: T) : UiState<T>()
    data class Error(val exception: Exception) : UiState<Nothing>()
}

// State machine
class ViewModel {
    var state: UiState<User> = UiState.Idle
        private set

    suspend fun loadUser(id: Long) {
        state = UiState.Loading
        state = try {
            val user = repository.fetchUser(id)
            UiState.Success(user)
        } catch (e: Exception) {
            UiState.Error(e)
        }
    }
}

// Rendering based on state
fun render(state: UiState<User>) {
    when (state) {
        UiState.Idle -> showEmpty()
        UiState.Loading -> showSpinner()
        is UiState.Success -> showUser(state.data)
        is UiState.Error -> showError(state.exception)
    }
}
```

### 12.3 Repository Pattern

```kotlin
// Repository interface
interface UserRepository {
    suspend fun getUser(id: Long): User?
    suspend fun saveUser(user: User)
    suspend fun deleteUser(id: Long)
}

// Implementation with caching
class CachedUserRepository(
    private val api: UserApi,
    private val cache: Cache
) : UserRepository {

    override suspend fun getUser(id: Long): User? {
        return cache.get(id) ?: api.fetchUser(id)?.also {
            cache.put(id, it)
        }
    }

    override suspend fun saveUser(user: User) {
        api.saveUser(user)
        cache.put(user.id, user)
    }

    override suspend fun deleteUser(id: Long) {
        api.deleteUser(id)
        cache.remove(id)
    }
}
```

### 12.4 Validation with Result

```kotlin
sealed class ValidationResult<out T> {
    data class Valid<T>(val value: T) : ValidationResult<T>()
    data class Invalid(val errors: List<String>) : ValidationResult<Nothing>()
}

fun validateUser(
    name: String,
    email: String,
    age: Int
): ValidationResult<User> {
    val errors = mutableListOf<String>()

    if (name.isBlank()) errors.add("Name cannot be blank")
    if (!email.contains("@")) errors.add("Invalid email")
    if (age < 0) errors.add("Age must be positive")

    return if (errors.isEmpty()) {
        ValidationResult.Valid(User(name, email, age))
    } else {
        ValidationResult.Invalid(errors)
    }
}

// Usage
when (val result = validateUser(name, email, age)) {
    is ValidationResult.Valid -> saveUser(result.value)
    is ValidationResult.Invalid -> showErrors(result.errors)
}
```

---

## 14. Troubleshooting

### 13.1 NullPointerException

```kotlin
// Problem: Calling !! on null
val name = getName()!!  // NPE if getName() returns null

// Solution: Use safe operators
val name = getName() ?: "default"
val length = getName()?.length ?: 0

// Solution: Early return
val name = getName() ?: return
processName(name)
```

### 13.2 Type Mismatch

```kotlin
// Problem: Platform type confusion
val javaString: String = getJavaString()  // May be null

// Solution: Use nullable type
val javaString: String? = getJavaString()

// Problem: Collection variance
val list: List<Any> = listOf<String>("a")  // OK - covariant
val mutableList: MutableList<Any> = mutableListOf<String>("a")  // Error - invariant

// Solution: Use read-only List or explicit type
val list: List<Any> = mutableListOf<String>("a")  // OK
```

### 13.3 Coroutine Cancellation

```kotlin
// Problem: Ignoring cancellation
suspend fun process() {
    while (true) {
        // Expensive operation - can't cancel
        processItem()
    }
}

// Solution: Check isActive or use cancellable functions
suspend fun process() = coroutineScope {
    while (isActive) {
        processItem()
    }
}

// Or use delay which is cancellable
suspend fun process() {
    while (true) {
        processItem()
        delay(100)  // Cancellation point
    }
}
```

### 13.4 Memory Leaks with Coroutines

```kotlin
// Problem: GlobalScope launches never cleaned
GlobalScope.launch {
    // This lives forever
}

// Solution: Use proper scope
class ViewModel : CoroutineScope {
    private val job = Job()
    override val coroutineContext = Dispatchers.Main + job

    fun loadData() {
        launch {  // Tied to ViewModel lifecycle
            // ...
        }
    }

    fun onCleared() {
        job.cancel()  // Clean up when done
    }
}
```

### 13.5 Lazy Initialization Issues

```kotlin
// Problem: Lazy not thread-safe by default (it is by default, but showing pattern)
val data by lazy { expensiveComputation() }

// For truly thread-unsafe scenarios
val data by lazy(LazyThreadSafetyMode.NONE) {
    expensiveComputation()  // Only if guaranteed single-threaded
}

// Problem: Lazy val in data class
data class User(val name: String) {
    val computed by lazy { expensiveOp() }  // Not in equals/hashCode
}

// Solution: Make it explicit
data class User(val name: String) {
    fun getComputed() = computedValue
    private val computedValue by lazy { expensiveOp() }
}
```

---

## 15. Testing

Kotlin's testing ecosystem provides powerful frameworks with idiomatic DSL support, extension functions, and coroutine testing utilities.

### 13.1 JUnit 5 with Kotlin

```kotlin
import org.junit.jupiter.api.*
import org.junit.jupiter.api.Assertions.*

class CalculatorTest {
    private lateinit var calculator: Calculator

    @BeforeEach
    fun setUp() {
        calculator = Calculator()
    }

    @Test
    fun `should add two numbers`() {
        val result = calculator.add(2, 3)
        assertEquals(5, result)
    }

    @Test
    fun `should throw on division by zero`() {
        assertThrows<ArithmeticException> {
            calculator.divide(10, 0)
        }
    }

    @Test
    @DisplayName("Addition is commutative")
    fun additionIsCommutative() {
        assertEquals(
            calculator.add(2, 3),
            calculator.add(3, 2)
        )
    }

    // Parameterized tests
    @ParameterizedTest
    @ValueSource(ints = [1, 2, 3, 4, 5])
    fun `should be positive`(number: Int) {
        assertTrue(number > 0)
    }

    @ParameterizedTest
    @CsvSource(
        "1, 2, 3",
        "10, 20, 30",
        "-1, 1, 0"
    )
    fun `should add correctly`(a: Int, b: Int, expected: Int) {
        assertEquals(expected, calculator.add(a, b))
    }
}
```

### 13.2 Kotest Framework

```kotlin
import io.kotest.core.spec.style.*
import io.kotest.matchers.*
import io.kotest.matchers.collections.*
import io.kotest.matchers.string.*

// BehaviorSpec - BDD style
class UserServiceSpec : BehaviorSpec({
    Given("a new user") {
        val user = User("Alice", "alice@example.com")

        When("we save the user") {
            val saved = userService.save(user)

            Then("the user should have an ID") {
                saved.id shouldNotBe null
            }

            Then("the user should be retrievable") {
                val found = userService.findById(saved.id!!)
                found shouldBe saved
            }
        }
    }
})

// FunSpec - simple function-based tests
class CalculatorSpec : FunSpec({
    test("addition should work") {
        val result = Calculator().add(2, 3)
        result shouldBe 5
    }

    test("division by zero should throw") {
        shouldThrow<ArithmeticException> {
            Calculator().divide(10, 0)
        }
    }

    context("with positive numbers") {
        test("multiplication should be positive") {
            Calculator().multiply(2, 3) shouldBe 6
        }
    }
})

// StringSpec - minimal style
class StringUtilsSpec : StringSpec({
    "length should return string length" {
        "hello".length shouldBe 5
    }

    "startsWith should check prefix" {
        "hello" should startWith("hel")
    }

    "uppercase should convert to upper" {
        "hello".uppercase() shouldBe "HELLO"
    }
})

// DescribeSpec - Jasmine/Mocha style
class ListSpec : DescribeSpec({
    describe("a list") {
        val list = listOf(1, 2, 3)

        it("should have size 3") {
            list.size shouldBe 3
        }

        it("should contain 2") {
            list shouldContain 2
        }

        describe("when filtered") {
            val filtered = list.filter { it > 1 }

            it("should have size 2") {
                filtered.size shouldBe 2
            }

            it("should only contain values > 1") {
                filtered shouldContainExactly listOf(2, 3)
            }
        }
    }
})
```

### 13.3 Kotest Matchers

```kotlin
import io.kotest.matchers.*
import io.kotest.matchers.collections.*
import io.kotest.matchers.string.*
import io.kotest.matchers.types.*

// Equality and comparison
value shouldBe expected
value shouldNotBe unexpected
value shouldBeGreaterThan 5
value shouldBeLessThanOrEqual 10

// Null checks
value.shouldNotBeNull()
value.shouldBeNull()

// Type checks
value shouldBeInstanceOf<String>()
value.shouldBeTypeOf<User>()

// String matchers
str shouldStartWith "prefix"
str shouldEndWith "suffix"
str shouldContain "middle"
str shouldMatch "\\d+".toRegex()
str.shouldBeEmpty()
str.shouldBeBlank()

// Collection matchers
list shouldContain element
list shouldContainAll listOf(1, 2, 3)
list shouldContainExactly listOf(1, 2, 3)
list shouldHaveSize 5
list.shouldBeEmpty()
list.shouldBeSorted()

// Map matchers
map shouldContainKey "key"
map shouldContainValue 42
map shouldContainAll mapOf("a" to 1, "b" to 2)

// Exception matchers
shouldThrow<IllegalArgumentException> {
    validate(null)
}

val exception = shouldThrow<CustomException> {
    dangerousOperation()
}
exception.message shouldBe "Expected error"

// Boolean matchers
condition.shouldBeTrue()
condition.shouldBeFalse()

// Custom matchers
data class User(val name: String, val age: Int)

fun beAdult() = object : Matcher<User> {
    override fun test(value: User) = MatcherResult(
        value.age >= 18,
        { "User ${value.name} should be adult but was ${value.age}" },
        { "User ${value.name} should not be adult" }
    )
}

user should beAdult()
```

### 13.4 MockK - Mocking Library

```kotlin
import io.mockk.*
import io.mockk.impl.annotations.InjectMockKs
import io.mockk.impl.annotations.MockK
import io.mockk.junit5.MockKExtension

@ExtendWith(MockKExtension::class)
class UserServiceTest {
    @MockK
    private lateinit var repository: UserRepository

    @InjectMockKs
    private lateinit var service: UserService

    @Test
    fun `should find user by id`() {
        // Given
        val user = User(1, "Alice")
        every { repository.findById(1) } returns user

        // When
        val result = service.getUser(1)

        // Then
        result shouldBe user
        verify { repository.findById(1) }
    }

    @Test
    fun `should throw when user not found`() {
        // Given
        every { repository.findById(any()) } returns null

        // When/Then
        shouldThrow<UserNotFoundException> {
            service.getUser(999)
        }
    }

    @Test
    fun `should save user`() {
        // Given
        val user = User(0, "Bob")
        val slot = slot<User>()
        every { repository.save(capture(slot)) } answers { slot.captured.copy(id = 1) }

        // When
        val saved = service.createUser(user)

        // Then
        saved.id shouldBe 1
        saved.name shouldBe "Bob"
        verify(exactly = 1) { repository.save(any()) }
    }
}

// Relaxed mocks - return default values
val mock = mockk<UserRepository>(relaxed = true)

// Spy - partial mocking
val spy = spyk(RealUserService())
every { spy.generateId() } returns 42

// Mock extension functions
mockkStatic(String::toUpperCase)
every { "hello".toUpperCase() } returns "MOCKED"

// Mock objects
object Logger {
    fun log(message: String) = println(message)
}

mockkObject(Logger)
every { Logger.log(any()) } just Runs
verify { Logger.log("test") }
```

### 13.5 Coroutine Testing

```kotlin
import kotlinx.coroutines.*
import kotlinx.coroutines.test.*
import org.junit.jupiter.api.Test

class CoroutineServiceTest {

    @Test
    fun `should fetch user data`() = runTest {
        val service = UserService()

        val user = service.fetchUser(1)

        user shouldNotBe null
        user.name shouldBe "Alice"
    }

    @Test
    fun `should handle concurrent requests`() = runTest {
        val service = UserService()

        val users = (1..10).map { id ->
            async { service.fetchUser(id) }
        }.awaitAll()

        users.size shouldBe 10
        users.all { it != null }.shouldBeTrue()
    }

    @Test
    fun `should timeout on slow operations`() = runTest {
        val service = SlowService()

        shouldThrow<TimeoutCancellationException> {
            withTimeout(1000) {
                service.verySlowOperation()
            }
        }
    }

    @Test
    fun `should advance time virtually`() = runTest {
        val service = TimedService()

        // Virtual time - no actual delay
        delay(5000)
        val result = service.checkStatus()

        result shouldBe "Ready"
    }

    @Test
    fun `should test flow emissions`() = runTest {
        val flow = flowOf(1, 2, 3, 4, 5)

        val results = mutableListOf<Int>()
        flow.collect { results.add(it) }

        results shouldContainExactly listOf(1, 2, 3, 4, 5)
    }

    @Test
    fun `should test flow transformations`() = runTest {
        val flow = (1..5).asFlow()
            .map { it * 2 }
            .filter { it > 5 }

        val results = flow.toList()

        results shouldContainExactly listOf(6, 8, 10)
    }

    @Test
    fun `should use test dispatcher`() = runTest {
        val dispatcher = StandardTestDispatcher(testScheduler)
        val scope = CoroutineScope(dispatcher)

        var completed = false
        scope.launch {
            delay(1000)
            completed = true
        }

        // Not completed yet - virtual time hasn't advanced
        completed.shouldBeFalse()

        // Advance virtual time
        advanceTimeBy(1000)

        // Now completed
        completed.shouldBeTrue()
    }
}

// Testing suspending functions
class SuspendFunctionTest {

    @Test
    fun `should test suspend function`() = runTest {
        suspend fun fetchData(): String {
            delay(100)
            return "data"
        }

        val result = fetchData()
        result shouldBe "data"
    }

    @Test
    fun `should verify mock suspend calls`() = runTest {
        val repository = mockk<UserRepository>()
        coEvery { repository.fetchUser(any()) } returns User(1, "Alice")

        val user = repository.fetchUser(1)

        user.name shouldBe "Alice"
        coVerify { repository.fetchUser(1) }
    }
}
```

### 13.6 kotlin.test Assertions

```kotlin
import kotlin.test.*

class KotlinTestExample {

    @Test
    fun `should use kotlin test assertions`() {
        // Equality
        assertEquals(5, 2 + 3)
        assertNotEquals(4, 2 + 3)

        // Boolean
        assertTrue(2 + 2 == 4)
        assertFalse(2 + 2 == 5)

        // Null checks
        assertNull(null)
        assertNotNull("value")

        // Exceptions
        assertFails {
            throw IllegalStateException()
        }

        assertFailsWith<IllegalArgumentException> {
            require(false) { "Validation failed" }
        }

        // Content equality
        assertContentEquals(listOf(1, 2, 3), listOf(1, 2, 3))

        // Custom message
        assertEquals(5, 2 + 3, "Addition should work")
    }
}
```

### 13.7 Property-Based Testing with Kotest

```kotlin
import io.kotest.core.spec.style.StringSpec
import io.kotest.property.*
import io.kotest.property.arbitrary.*

class PropertyBasedTest : StringSpec({

    "string length is never negative" {
        checkAll<String> { str ->
            str.length shouldBeGreaterThanOrEqual 0
        }
    }

    "reversing a list twice returns original" {
        checkAll<List<Int>> { list ->
            list.reversed().reversed() shouldBe list
        }
    }

    "addition is commutative" {
        checkAll<Int, Int> { a, b ->
            a + b shouldBe b + a
        }
    }

    "custom generators" {
        val emails = arbitrary {
            val name = Arb.string(5..10, Codepoint.alphanumeric()).bind()
            val domain = Arb.string(5..10, Codepoint.alphanumeric()).bind()
            "$name@$domain.com"
        }

        checkAll(emails) { email ->
            email shouldContain "@"
            email shouldEndWith ".com"
        }
    }

    "edge cases" {
        val config = PropTestConfig(iterations = 1000)

        checkAll(config, Arb.int()) { n ->
            val doubled = n * 2
            if (n >= 0) {
                doubled shouldBeGreaterThanOrEqual n
            } else {
                doubled shouldBeLessThanOrEqual n
            }
        }
    }
})
```

### 13.8 Test DSL Patterns

```kotlin
// Custom test DSL
class TestDsl {
    fun scenario(name: String, block: ScenarioContext.() -> Unit) {
        println("Scenario: $name")
        ScenarioContext().block()
    }
}

class ScenarioContext {
    fun given(description: String, block: () -> Unit) {
        println("  Given $description")
        block()
    }

    fun whenever(description: String, block: () -> Unit) {
        println("  When $description")
        block()
    }

    fun then(description: String, block: () -> Unit) {
        println("  Then $description")
        block()
    }
}

// Usage
class UserFlowTest : StringSpec({
    "user registration flow" {
        scenario("new user signs up") {
            var user: User? = null

            given("valid user details") {
                user = User(name = "Alice", email = "alice@example.com")
            }

            whenever("user submits registration") {
                user = userService.register(user!!)
            }

            then("user should receive confirmation email") {
                emailService.wasSent(user!!.email).shouldBeTrue()
            }

            then("user should have active account") {
                user!!.isActive.shouldBeTrue()
            }
        }
    }
})

// Fixture DSL
fun testWithUser(block: suspend (User) -> Unit) = runTest {
    val user = createTestUser()
    try {
        block(user)
    } finally {
        cleanup(user)
    }
}

// Usage
@Test
fun `should update user profile`() = testWithUser { user ->
    val updated = service.updateProfile(user.id, "New Name")
    updated.name shouldBe "New Name"
}

// Data builders with DSL
fun user(block: UserBuilder.() -> Unit): User {
    return UserBuilder().apply(block).build()
}

class UserBuilder {
    var name: String = "Test User"
    var email: String = "test@example.com"
    var age: Int = 30
    var roles: List<String> = emptyList()

    fun build() = User(name, email, age, roles)
}

// Usage in tests
@Test
fun `should validate admin user`() {
    val admin = user {
        name = "Admin"
        email = "admin@example.com"
        roles = listOf("ADMIN", "USER")
    }

    admin.isAdmin().shouldBeTrue()
}
```

### 13.9 Integration Testing Patterns

```kotlin
import org.testcontainers.containers.PostgreSQLContainer
import org.testcontainers.junit.jupiter.Container
import org.testcontainers.junit.jupiter.Testcontainers

@Testcontainers
class DatabaseIntegrationTest {

    companion object {
        @Container
        val postgres = PostgreSQLContainer<Nothing>("postgres:15").apply {
            withDatabaseName("testdb")
            withUsername("test")
            withPassword("test")
        }
    }

    @Test
    fun `should persist and retrieve user`() {
        val repository = UserRepository(postgres.jdbcUrl)
        val user = User(name = "Alice", email = "alice@example.com")

        val saved = repository.save(user)
        val found = repository.findById(saved.id)

        found shouldBe saved
    }
}

// HTTP client testing
@Test
fun `should call external API`() = runTest {
    val mockServer = MockWebServer()
    mockServer.enqueue(
        MockResponse()
            .setBody("""{"name": "Alice"}""")
            .setHeader("Content-Type", "application/json")
    )

    val client = HttpClient(mockServer.url("/"))
    val user = client.fetchUser(1)

    user.name shouldBe "Alice"
    mockServer.shutdown()
}
```

### 13.10 Test Organization Best Practices

```kotlin
// Nested tests for organization
@Nested
@DisplayName("User validation")
inner class UserValidation {

    @Test
    fun `should reject null name`() {
        shouldThrow<IllegalArgumentException> {
            User(name = null, email = "test@example.com")
        }
    }

    @Nested
    @DisplayName("Email validation")
    inner class EmailValidation {

        @Test
        fun `should reject invalid email format`() {
            shouldThrow<IllegalArgumentException> {
                User(name = "Alice", email = "invalid")
            }
        }

        @Test
        fun `should accept valid email`() {
            val user = User(name = "Alice", email = "alice@example.com")
            user.email shouldBe "alice@example.com"
        }
    }
}

// Tags for filtering tests
@Tag("integration")
@Tag("slow")
class SlowIntegrationTest {
    @Test
    fun `should complete long operation`() {
        // Long running test
    }
}

// Conditional test execution
@EnabledIf("customCondition")
fun customCondition(): Boolean = System.getenv("RUN_INTEGRATION") == "true"

@Test
fun `should run only in CI`() {
    // Only runs when condition is true
}
```

---

## 16. Cross-Cutting Patterns

For cross-language comparison and translation patterns, see:

- **patterns-concurrency-dev**: Coroutines, Flow, channels, structured concurrency
- **patterns-serialization-dev**: kotlinx.serialization, Jackson with Kotlin
- **patterns-metaprogramming-dev**: Annotations, reflection, DSL builders
- **patterns-testing-dev**: Test frameworks, mocking, property-based testing

---

## 17. Further Resources

### Specialized Skills
- **lang-kotlin-coroutines-eng**: Advanced Flow, channels, structured concurrency
- **lang-kotlin-library-dev**: Publishing libraries, API design
- **lang-kotlin-patterns-eng**: Design patterns and architectural patterns
- **lang-kotlin-multiplatform-dev**: Kotlin Multiplatform (KMP)

### Official Documentation
- Kotlin Language Reference: https://kotlinlang.org/docs/reference/
- Kotlin Coroutines Guide: https://kotlinlang.org/docs/coroutines-guide.html
- Kotlin Standard Library: https://kotlinlang.org/api/latest/jvm/stdlib/

### Style Guides
- Kotlin Coding Conventions: https://kotlinlang.org/docs/coding-conventions.html
- Android Kotlin Style Guide: https://developer.android.com/kotlin/style-guide
