---
name: Kotlin Null Safety
description: Use when kotlin's null safety system including nullable types, safe calls, Elvis operator, smart casts, and patterns for eliminating NullPointerExceptions while maintaining code expressiveness and clarity.
allowed-tools: []
---

# Kotlin Null Safety

## Introduction

Kotlin's null safety system eliminates NullPointerExceptions at compile time by
distinguishing between nullable and non-nullable types in the type system. This
approach makes null handling explicit and forces developers to consciously
handle potential null values.

Unlike Java where any reference can be null, Kotlin requires explicit
declaration of nullability with the `?` operator. The compiler enforces null
checks before dereferencing nullable values, preventing the vast majority of
null-related crashes that plague Java applications.

This skill covers nullable types, safe call operators, smart casts, nullability
in generic types, and patterns for designing null-safe APIs while maintaining
code clarity.

## Nullable Types

Nullable types explicitly indicate that a variable or property can hold null,
while non-nullable types provide compile-time guarantees of non-null values.

```kotlin
// Non-nullable types
var name: String = "Alice"
// name = null // Compilation error

// Nullable types
var nullableName: String? = "Bob"
nullableName = null // OK

// Function parameters
fun greet(name: String) {
    println("Hello, $name")
}

fun greetNullable(name: String?) {
    if (name != null) {
        println("Hello, $name")
    } else {
        println("Hello, guest")
    }
}

// greet(null) // Compilation error
greetNullable(null) // OK

// Nullable return types
fun findUser(id: Int): User? {
    return if (id > 0) User(id, "Alice") else null
}

data class User(val id: Int, val name: String)

// Nullable properties
class Person(
    val name: String,
    val email: String?,
    var phoneNumber: String?
)

// Collections with nullable elements
val nullableList: List<String?> = listOf("A", null, "B")
val listOfNullable: List<String>? = null

// Platform types from Java (String!)
// Treated as nullable for safety in Kotlin

// Nullable this
class Service {
    fun process() {
        val self: Service? = this
        self?.validate()
    }

    fun validate() {}
}
```

The `?` suffix makes a type nullable. Non-nullable types cannot be assigned null
without explicit nullability declaration, preventing accidental null references.

## Safe Call Operator

The safe call operator `?.` safely accesses properties and methods on nullable
references, returning null if the receiver is null instead of throwing NPE.

```kotlin
// Basic safe calls
val name: String? = "Alice"
val length: Int? = name?.length

val nullName: String? = null
val nullLength: Int? = nullName?.length // Returns null

// Chaining safe calls
data class Address(val street: String?, val city: String?)
data class Company(val address: Address?)
data class Employee(val company: Company?)

val employee: Employee? = Employee(Company(Address("Main St", "NYC")))

val city: String? = employee?.company?.address?.city
println(city) // "NYC"

val nullEmployee: Employee? = null
val nullCity: String? = nullEmployee?.company?.address?.city
println(nullCity) // null

// Safe calls with methods
fun processUser(user: User?) {
    user?.let { u ->
        println("Processing ${u.name}")
    }
}

// Safe calls with extension functions
fun String?.orDefault(default: String): String {
    return this ?: default
}

val result = nullName?.orDefault("Unknown")

// Safe calls in expressions
class Profile(val bio: String?)

fun displayBio(profile: Profile?) {
    val bioLength = profile?.bio?.length ?: 0
    println("Bio length: $bioLength")
}

// Safe calls with mutable properties
class Container {
    var value: String? = null

    fun updateValue() {
        value?.let { current ->
            value = current.uppercase()
        }
    }
}
```

Safe call chains short-circuit at the first null, making deeply nested optional
access clean and safe without multiple null checks.

## Elvis Operator and Null Coalescing

The Elvis operator `?:` provides default values for null expressions, enabling
concise fallback logic without verbose if-else statements.

```kotlin
// Basic Elvis operator
val name: String? = null
val displayName = name ?: "Guest"
println(displayName) // "Guest"

// Elvis with safe calls
fun getUserCity(employee: Employee?): String {
    return employee?.company?.address?.city ?: "Unknown"
}

// Elvis with expressions
fun calculateTotal(subtotal: Double?, taxRate: Double?): Double {
    val sub = subtotal ?: 0.0
    val tax = taxRate ?: 0.15
    return sub * (1 + tax)
}

// Elvis with return/throw
fun requireName(name: String?): String {
    return name ?: throw IllegalArgumentException("Name required")
}

fun processUser(user: User?) {
    val u = user ?: return
    println("Processing ${u.name}")
}

// Chaining Elvis operators
fun findValidValue(
    primary: String?,
    secondary: String?,
    tertiary: String?
): String {
    return primary ?: secondary ?: tertiary ?: "default"
}

// Elvis with nullable properties
class Config {
    var timeout: Int? = null

    fun getTimeout(): Int {
        return timeout ?: 30000
    }
}

// Elvis in constructors
class Service(name: String?) {
    val serviceName: String = name ?: "DefaultService"
}

// Elvis with function calls
fun fetchFromCache(): String? = null
fun fetchFromNetwork(): String? = "data"

fun getData(): String {
    return fetchFromCache() ?: fetchFromNetwork() ?: "fallback"
}
```

The Elvis operator evaluates the right side only if the left side is null,
supporting lazy evaluation of default values.

## Smart Casts

Smart casts automatically cast nullable types to non-nullable after null checks,
eliminating redundant casts and improving code clarity.

```kotlin
// Smart cast after null check
fun printLength(text: String?) {
    if (text != null) {
        println(text.length) // text is smart-cast to String
    }
}

// Smart cast in expressions
fun processName(name: String?): Int {
    return if (name != null) {
        name.length // Smart-cast
    } else {
        0
    }
}

// Smart cast with return
fun requireUser(user: User?): User {
    if (user == null) {
        throw IllegalStateException("User required")
    }
    return user // Smart-cast to User
}

// Smart cast with Elvis
fun getLength(text: String?): Int {
    val nonNull = text ?: return 0
    return nonNull.length // Smart-cast
}

// Smart cast with when expressions
fun describe(obj: Any?): String {
    return when {
        obj == null -> "null"
        obj is String -> "String of length ${obj.length}"
        obj is Int -> "Int: $obj"
        else -> "Unknown type"
    }
}

// Smart cast with let
fun processNullable(value: String?) {
    value?.let { nonNull ->
        println(nonNull.uppercase()) // nonNull is String
    }
}

// Smart cast limitations
class Container(var value: String?) {
    fun process() {
        // Cannot smart-cast var properties
        if (value != null) {
            // println(value.length) // Compilation error
        }

        // Use local variable for smart cast
        val localValue = value
        if (localValue != null) {
            println(localValue.length) // OK
        }
    }
}

// Smart cast with contracts
fun requireNotNull(value: String?) {
    require(value != null)
    println(value.length) // Smart-cast after require
}
```

Smart casts work with immutable variables and val properties but not var
properties, which could change between the check and usage.

## Not-Null Assertion and Platform Types

The not-null assertion operator `!!` explicitly throws NPE if a value is null,
useful for cases where null is impossible but the compiler cannot verify.

```kotlin
// Not-null assertion operator
fun processName(name: String?) {
    val length = name!!.length // Throws NPE if name is null
    println("Length: $length")
}

// Use cases for !!
fun initializeFromConfig(config: Map<String, String>) {
    // We know these keys exist
    val apiKey = config["api_key"]!!
    val endpoint = config["endpoint"]!!

    println("Configured with $apiKey at $endpoint")
}

// Avoid chaining !!
val city = employee!!.company!!.address!!.city!! // Bad

// Better alternatives
val city2 = employee?.company?.address?.city
    ?: throw IllegalStateException("City required")

// Platform types from Java
class JavaInterop {
    fun useJavaApi() {
        val javaString = JavaClass.getString() // String! (platform type)

        // Treat as nullable for safety
        val length: Int? = javaString?.length

        // Or assert non-null
        val length2: Int = javaString!!.length

        // Or add explicit type
        val explicitString: String = JavaClass.getString()
    }
}

// Mocking platform types in tests
@Suppress("PLATFORM_CLASS_MAPPED_TO_KOTLIN")
fun mockJavaString(): java.lang.String? {
    return null
}

// lateinit for non-null initialization
class Service {
    lateinit var apiClient: ApiClient

    fun initialize(client: ApiClient) {
        apiClient = client
    }

    fun makeRequest() {
        if (::apiClient.isInitialized) {
            apiClient.request()
        }
    }
}

class ApiClient {
    fun request() {}
}

// Use !! sparingly and document assumptions
fun parseJson(json: String?): Data {
    // !! OK here because caller ensures non-null
    return Json.parse(json!!)
}

object Json {
    fun parse(json: String): Data = Data()
}

data class Data(val value: String = "")

class JavaClass {
    companion object {
        @JvmStatic
        fun getString(): String = ""
    }
}
```

The `!!` operator should be used sparingly and only when you have high
confidence the value is non-null, as it reintroduces crash potential.

## Nullability in Collections and Generics

Collections and generic types support nullability at both the container and
element levels, requiring clear distinction between nullable elements and
nullable collections.

```kotlin
// Nullable elements vs nullable collections
val listWithNulls: List<String?> = listOf("A", null, "B")
val nullableList: List<String>? = null

// Processing nullable elements
fun filterNulls(items: List<String?>): List<String> {
    return items.filterNotNull()
}

val filtered = filterNulls(listOf("A", null, "B"))
println(filtered) // [A, B]

// Nullable map values
val userIds: Map<String, Int?> = mapOf(
    "alice" to 1,
    "bob" to null,
    "charlie" to 3
)

fun getUserId(name: String): Int? {
    return userIds[name]
}

// Generic functions with nullable types
fun <T> firstOrNull(list: List<T>): T? {
    return list.firstOrNull()
}

// Generic constraints with nullability
fun <T : Any> nonNullable(value: T) {
    // T cannot be null
    println(value.toString())
}

// Nullable generic types
class Container<T>(val value: T?)

val stringContainer = Container<String>(null)
val intContainer = Container<Int>(42)

// Extension functions on nullable types
fun <T> List<T?>.filterNotNullAndMap(transform: (T) -> String): List<String> {
    return this.filterNotNull().map(transform)
}

val result = listOf(1, null, 3).filterNotNullAndMap { it.toString() }

// Nullable receivers
fun String?.isNullOrEmpty(): Boolean {
    return this == null || this.isEmpty()
}

val empty: String? = null
println(empty.isNullOrEmpty()) // true

// Sequences with nullable elements
fun processSequence(items: Sequence<String?>) {
    items
        .filterNotNull()
        .map { it.uppercase() }
        .forEach { println(it) }
}

// Generic variance and nullability
interface Producer<out T> {
    fun produce(): T?
}

interface Consumer<in T> {
    fun consume(item: T?)
}
```

Understanding the distinction between `List<String?>` (list of nullable strings)
and `List<String>?` (nullable list) is crucial for correct null handling.

## Designing Null-Safe APIs

Designing APIs with appropriate nullability improves usability and prevents
misuse by making null expectations explicit in the type system.

```kotlin
// Prefer non-nullable parameters
class UserRepository {
    fun save(user: User) {
        // user is guaranteed non-null
        println("Saving ${user.name}")
    }
}

// Use nullable returns for optional values
class UserService {
    fun findById(id: Int): User? {
        return if (id > 0) User(id, "Alice") else null
    }

    fun getAllUsers(): List<User> {
        // Return empty list, not null
        return emptyList()
    }
}

// Builder pattern with nullable accumulation
class QueryBuilder {
    private var table: String? = null
    private var where: String? = null
    private var orderBy: String? = null

    fun from(table: String) = apply { this.table = table }
    fun where(condition: String) = apply { this.where = condition }
    fun orderBy(column: String) = apply { this.orderBy = column }

    fun build(): String {
        val t = table ?: throw IllegalStateException("Table required")
        val w = where?.let { "WHERE $it" } ?: ""
        val o = orderBy?.let { "ORDER BY $it" } ?: ""

        return "SELECT * FROM $t $w $o".trim()
    }
}

// Nullable configuration with defaults
data class Config(
    val timeout: Int? = null,
    val retries: Int? = null,
    val debug: Boolean? = null
) {
    fun getTimeout() = timeout ?: 30000
    fun getRetries() = retries ?: 3
    fun isDebug() = debug ?: false
}

// Sealed classes for optional values
sealed class Result<out T> {
    data class Success<T>(val value: T) : Result<T>()
    data class Error(val message: String) : Result<Nothing>()
    object NotFound : Result<Nothing>()
}

fun findUser(id: Int): Result<User> {
    return when {
        id < 0 -> Result.Error("Invalid ID")
        id == 0 -> Result.NotFound
        else -> Result.Success(User(id, "Alice"))
    }
}

// Validation with nullable return
class Validator {
    fun validateEmail(email: String): String? {
        return if (email.contains("@")) {
            null // No error
        } else {
            "Invalid email format"
        }
    }
}

// Nullable callback parameters
class AsyncLoader {
    fun load(
        onSuccess: (User) -> Unit,
        onError: ((String) -> Unit)? = null
    ) {
        try {
            val user = User(1, "Alice")
            onSuccess(user)
        } catch (e: Exception) {
            onError?.invoke(e.message ?: "Unknown error")
        }
    }
}
```

Good API design minimizes nullability where possible, using empty collections
instead of null lists and sealed classes for richer optional value semantics.

## Best Practices

1. **Prefer non-nullable types by default** to maximize compile-time safety and
   reduce null checks throughout the codebase

2. **Use safe call operator `?.` for chaining** instead of multiple null checks
   to keep code concise and readable

3. **Provide defaults with Elvis operator `?:`** rather than verbose if-else
   chains for simple fallback scenarios

4. **Return empty collections instead of null** to simplify client code and
   eliminate null checks for collection results

5. **Leverage smart casts after null checks** to avoid redundant casts and let
   the compiler track non-null guarantees

6. **Minimize use of `!!` operator** and document assumptions when used, as it
   reintroduces crash potential

7. **Design APIs with explicit nullability** to communicate intent clearly and
   prevent misuse of nullable values

8. **Use lateinit for non-null deferred initialization** instead of nullable
   properties with manual null checks

9. **Apply nullable extensions** to provide utilities like `isNullOrEmpty()` for
   cleaner null handling in common scenarios

10. **Prefer sealed classes over nullable types** for richer semantics when
    representing success, error, and absent states

## Common Pitfalls

1. **Overusing nullable types** when values should never be null makes APIs
   harder to use and adds unnecessary checks

2. **Chaining `!!` operators** creates unclear crash points; use safe calls or
   explicit validation instead

3. **Ignoring platform types from Java** can cause NPEs; treat Java return
   values as nullable unless documented

4. **Using var properties for smart casts** fails because vars can change; use
   local val copies for smart casting

5. **Returning null collections** instead of empty collections forces clients to
   handle two separate cases unnecessarily

6. **Not considering nullability in equals/hashCode** can cause unexpected
   behavior in collections and comparisons

7. **Forgetting that safe calls return nullable types** leads to unexpected null
   values propagating through code

8. **Using nullable primary constructor parameters** without defaults makes
   object creation unnecessarily complex

9. **Creating deeply nested nullable structures** becomes unwieldy; flatten or
   use sealed classes for clarity

10. **Not documenting null semantics** in complex APIs leaves callers guessing
    when nulls are valid or what they represent

## When to Use This Skill

Use Kotlin null safety when building any Kotlin application to eliminate
NullPointerExceptions and make null handling explicit, including Android apps,
server-side services, and multiplatform projects.

Apply nullable types and safe call operators when working with data from
external sources like network APIs, databases, or user input where values may be
absent.

Employ Elvis operator and smart casts when handling optional configuration,
defaults, or fallback values to keep code concise and readable.

Leverage null-safe design patterns when building libraries or frameworks to
create APIs that are hard to misuse and clearly communicate expectations.

Use sealed classes and Result types for richer optional semantics in domain
models where null is insufficient to represent different states.

## Resources

- [Kotlin Null Safety Documentation](<https://kotlinlang.org/docs/null-safety.html>)
- [Idioms: Null Safety](<https://kotlinlang.org/docs/idioms.html#nullable-values>)
- [Kotlin Coding Conventions](<https://kotlinlang.org/docs/coding-conventions.html>)
- [Effective Kotlin](<https://kt.academy/book/effectivekotlin>)
- [Kotlin for Java Developers](<https://www.coursera.org/learn/kotlin-for-java-developers>)
