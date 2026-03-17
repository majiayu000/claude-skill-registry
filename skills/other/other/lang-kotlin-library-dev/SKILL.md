---
name: lang-kotlin-library-dev
description: Kotlin-specific library development patterns. Use when creating Kotlin libraries, designing idiomatic Kotlin APIs with extension functions and DSLs, configuring Gradle Kotlin DSL (build.gradle.kts), managing multiplatform projects, testing with Kotest/JUnit, writing KDoc documentation, or publishing to Maven Central. Extends meta-library-dev with Kotlin tooling and ecosystem practices.
---

# Kotlin Library Development

Kotlin-specific patterns for library development. This skill extends `meta-library-dev` with Kotlin tooling, multiplatform capabilities, and ecosystem practices.

## This Skill Extends

- `meta-library-dev` - Foundational library patterns (API design, versioning, testing strategies)

For general concepts like semantic versioning, module organization principles, and testing pyramids, see the meta-skill first.

## This Skill Adds

- **Kotlin tooling**: Gradle Kotlin DSL, multiplatform configuration, compiler plugins
- **Kotlin idioms**: Extension functions, DSL design, sealed classes, inline functions
- **Kotlin ecosystem**: Maven Central publishing, KDoc, Dokka, multiplatform targets

## This Skill Does NOT Cover

- General library patterns - see `meta-library-dev`
- Android-specific library development - see Android skills
- Kotlin/JS frontend development - see frontend skills
- General Kotlin syntax - see `lang-kotlin-dev`

---

## Quick Reference

| Task | Command/Pattern |
|------|-----------------|
| New library | `gradle init --type kotlin-library` |
| Build | `./gradlew build` |
| Test | `./gradlew test` |
| Generate docs | `./gradlew dokkaHtml` |
| Publish (local) | `./gradlew publishToMavenLocal` |
| Publish (Maven Central) | `./gradlew publishToSonatype closeAndReleaseSonatypeStagingRepository` |
| Check API compatibility | `./gradlew apiCheck` (requires binary-compatibility-validator) |

---

## Gradle Kotlin DSL Structure

### build.gradle.kts (JVM Library)

```kotlin
plugins {
    kotlin("jvm") version "1.9.22"
    id("org.jetbrains.dokka") version "1.9.20"
    `maven-publish`
    signing
}

group = "com.example"
version = "1.0.0"

repositories {
    mavenCentral()
}

kotlin {
    jvmToolchain(17)

    compilerOptions {
        freeCompilerArgs.add("-Xjsr305=strict")
        allWarningsAsErrors.set(true)
    }
}

dependencies {
    implementation(kotlin("stdlib"))

    testImplementation(kotlin("test"))
    testImplementation("io.kotest:kotest-runner-junit5:5.8.0")
    testImplementation("io.kotest:kotest-assertions-core:5.8.0")
}

tasks.test {
    useJUnitPlatform()
}

java {
    withJavadocJar()
    withSourcesJar()
}

publishing {
    publications {
        create<MavenPublication>("maven") {
            from(components["java"])

            pom {
                name.set("My Kotlin Library")
                description.set("A brief description of what this library does")
                url.set("https://github.com/username/repo")

                licenses {
                    license {
                        name.set("The Apache License, Version 2.0")
                        url.set("http://www.apache.org/licenses/LICENSE-2.0.txt")
                    }
                }

                developers {
                    developer {
                        id.set("username")
                        name.set("Your Name")
                        email.set("email@example.com")
                    }
                }

                scm {
                    connection.set("scm:git:git://github.com/username/repo.git")
                    developerConnection.set("scm:git:ssh://github.com/username/repo.git")
                    url.set("https://github.com/username/repo")
                }
            }
        }
    }

    repositories {
        maven {
            name = "sonatype"
            url = uri("https://s01.oss.sonatype.org/service/local/staging/deploy/maven2/")
            credentials {
                username = project.findProperty("sonatypeUsername") as String?
                password = project.findProperty("sonatypePassword") as String?
            }
        }
    }
}

signing {
    sign(publishing.publications["maven"])
}
```

### gradle.properties

```properties
# Publishing configuration
signing.keyId=ABCD1234
signing.password=your-gpg-password
signing.secretKeyRingFile=/path/to/secring.gpg

sonatypeUsername=your-username
sonatypePassword=your-password

# Kotlin configuration
kotlin.code.style=official
kotlin.parallel.tasks.in.project=true

# Build optimizations
org.gradle.jvmargs=-Xmx2g -XX:MaxMetaspaceSize=512m
org.gradle.parallel=true
org.gradle.caching=true
```

---

## Multiplatform Configuration

### build.gradle.kts (Multiplatform)

```kotlin
plugins {
    kotlin("multiplatform") version "1.9.22"
    id("org.jetbrains.dokka") version "1.9.20"
    `maven-publish`
}

group = "com.example"
version = "1.0.0"

kotlin {
    // JVM target
    jvm {
        compilations.all {
            kotlinOptions.jvmTarget = "17"
        }
        testRuns["test"].executionTask.configure {
            useJUnitPlatform()
        }
    }

    // JavaScript target
    js(IR) {
        browser()
        nodejs()
    }

    // Native targets
    linuxX64()
    macosX64()
    macosArm64()
    mingwX64()

    // iOS targets
    iosX64()
    iosArm64()
    iosSimulatorArm64()

    sourceSets {
        // Common source set
        val commonMain by getting {
            dependencies {
                implementation("org.jetbrains.kotlinx:kotlinx-coroutines-core:1.7.3")
            }
        }

        val commonTest by getting {
            dependencies {
                implementation(kotlin("test"))
            }
        }

        // JVM-specific
        val jvmMain by getting {
            dependencies {
                implementation("org.jetbrains.kotlinx:kotlinx-coroutines-jdk8:1.7.3")
            }
        }

        val jvmTest by getting

        // JS-specific
        val jsMain by getting
        val jsTest by getting

        // Native shared
        val nativeMain by creating {
            dependsOn(commonMain)
        }

        val nativeTest by creating {
            dependsOn(commonTest)
        }

        // Configure all native targets
        val linuxX64Main by getting { dependsOn(nativeMain) }
        val macosX64Main by getting { dependsOn(nativeMain) }
        val macosArm64Main by getting { dependsOn(nativeMain) }
        val mingwX64Main by getting { dependsOn(nativeMain) }

        val iosX64Main by getting { dependsOn(nativeMain) }
        val iosArm64Main by getting { dependsOn(nativeMain) }
        val iosSimulatorArm64Main by getting { dependsOn(nativeMain) }
    }
}
```

### Hierarchical Source Set Structure

```
src/
├── commonMain/kotlin/
│   └── com/example/
│       └── Library.kt
├── commonTest/kotlin/
│   └── com/example/
│       └── LibraryTest.kt
├── jvmMain/kotlin/
│   └── com/example/
│       └── JvmSpecific.kt
├── jvmTest/kotlin/
├── jsMain/kotlin/
├── jsTest/kotlin/
├── nativeMain/kotlin/
│   └── com/example/
│       └── NativeSpecific.kt
└── nativeTest/kotlin/
```

---

## Idiomatic Kotlin API Design

### Extension Functions

**Use extension functions for fluent APIs:**
```kotlin
// Good: Extension function pattern
fun String.toSnakeCase(): String =
    this.replace(Regex("([a-z])([A-Z])"), "$1_$2").lowercase()

// Usage
val result = "HelloWorld".toSnakeCase() // "hello_world"

// Good: Extension on generic types
fun <T> List<T>.second(): T? = this.getOrNull(1)

// Good: Extension with receiver
inline fun <T> T.apply(block: T.() -> Unit): T {
    block()
    return this
}
```

### DSL Design

**Type-safe builders for configuration:**
```kotlin
// DSL API
class HttpClient internal constructor() {
    var timeout: Long = 30_000
    var followRedirects: Boolean = true
    val headers: MutableMap<String, String> = mutableMapOf()

    fun header(name: String, value: String) {
        headers[name] = value
    }
}

// Builder function
fun httpClient(configure: HttpClient.() -> Unit): HttpClient {
    return HttpClient().apply(configure)
}

// Usage
val client = httpClient {
    timeout = 60_000
    followRedirects = false
    header("User-Agent", "MyApp/1.0")
}
```

**Nested DSL example:**
```kotlin
@DslMarker
annotation class HtmlDsl

@HtmlDsl
abstract class Tag(val name: String) {
    private val children = mutableListOf<Tag>()

    protected fun <T : Tag> initTag(tag: T, init: T.() -> Unit): T {
        tag.init()
        children.add(tag)
        return tag
    }
}

class HTML : Tag("html") {
    fun head(init: Head.() -> Unit) = initTag(Head(), init)
    fun body(init: Body.() -> Unit) = initTag(Body(), init)
}

class Head : Tag("head") {
    fun title(init: Title.() -> Unit) = initTag(Title(), init)
}

class Title : Tag("title")
class Body : Tag("body")

// Usage
fun html(init: HTML.() -> Unit): HTML = HTML().apply(init)

val page = html {
    head {
        title { }
    }
    body { }
}
```

### Sealed Classes for Type Safety

**Use sealed classes for restricted hierarchies:**
```kotlin
// Good: Sealed class for results
sealed interface Result<out T> {
    data class Success<T>(val value: T) : Result<T>
    data class Failure(val error: Throwable) : Result<Nothing>
}

// Exhaustive when expressions
fun <T> Result<T>.getOrThrow(): T = when (this) {
    is Result.Success -> value
    is Result.Failure -> throw error
}

// Good: Sealed class for events
sealed class NetworkEvent {
    data class Connected(val connectionId: String) : NetworkEvent()
    data class Disconnected(val reason: String) : NetworkEvent()
    data class MessageReceived(val message: String) : NetworkEvent()
    data object Reconnecting : NetworkEvent()
}
```

### Inline Functions for Performance

**Use inline for higher-order functions:**
```kotlin
// Good: Inline function with reified type
inline fun <reified T> Any.asOrNull(): T? = this as? T

// Usage without explicit type
val string: String? = someObject.asOrNull()

// Good: Inline with lambda
inline fun <T> measureTime(block: () -> T): Pair<T, Long> {
    val start = System.currentTimeMillis()
    val result = block()
    val time = System.currentTimeMillis() - start
    return result to time
}

// Good: Inline value classes for type safety
@JvmInline
value class UserId(val value: String)

@JvmInline
value class Email(val value: String)

// No runtime overhead, but type-safe
fun sendEmail(userId: UserId, email: Email) { }
```

### Operator Overloading

**Use operator functions judiciously:**
```kotlin
data class Vector(val x: Double, val y: Double) {
    operator fun plus(other: Vector) = Vector(x + other.x, y + other.y)
    operator fun minus(other: Vector) = Vector(x - other.x, y - other.y)
    operator fun times(scalar: Double) = Vector(x * scalar, y * scalar)
    operator fun unaryMinus() = Vector(-x, -y)
}

// Usage
val v1 = Vector(1.0, 2.0)
val v2 = Vector(3.0, 4.0)
val sum = v1 + v2
val scaled = v1 * 2.0
```

---

## Module Organization

### Standard Library Structure

```
my-kotlin-library/
├── build.gradle.kts
├── gradle.properties
├── settings.gradle.kts
├── src/
│   ├── main/kotlin/
│   │   └── com/example/library/
│   │       ├── Library.kt           # Public API
│   │       ├── Models.kt            # Data classes
│   │       ├── Extensions.kt        # Extension functions
│   │       ├── Dsl.kt              # DSL builders
│   │       └── internal/           # Internal implementation
│   │           └── Utils.kt
│   └── test/kotlin/
│       └── com/example/library/
│           ├── LibraryTest.kt
│           └── DslTest.kt
├── docs/
│   └── index.md
└── README.md
```

### Public API Organization

**Main library file (Library.kt):**
```kotlin
package com.example.library

// Public API exports
public fun createClient(): Client = ClientImpl()

public interface Client {
    fun connect(): Result<Unit>
    fun disconnect()
}

// Internal implementation
internal class ClientImpl : Client {
    override fun connect(): Result<Unit> = TODO()
    override fun disconnect() = TODO()
}
```

### Visibility Modifiers

```kotlin
// Public - part of API (default, but explicit is clearer)
public fun publicFunction() {}

// Internal - visible within module only
internal fun internalFunction() {}

// Private - visible within file only
private fun privateFunction() {}

// Protected - visible in class and subclasses
protected open class Base {
    protected fun protectedFunction() {}
}
```

---

## Testing with Kotest

### Test Structure

```kotlin
import io.kotest.core.spec.style.FunSpec
import io.kotest.core.spec.style.StringSpec
import io.kotest.core.spec.style.BehaviorSpec
import io.kotest.matchers.shouldBe
import io.kotest.matchers.shouldNotBe
import io.kotest.matchers.collections.shouldContain
import io.kotest.matchers.string.shouldStartWith

// String spec (simple)
class SimpleTest : StringSpec({
    "string length should be 5" {
        "hello".length shouldBe 5
    }

    "string should start with h" {
        "hello" shouldStartWith "h"
    }
})

// Fun spec (descriptive)
class CalculatorTest : FunSpec({
    test("addition should work correctly") {
        val result = 2 + 2
        result shouldBe 4
    }

    context("division") {
        test("dividing by non-zero should work") {
            10 / 2 shouldBe 5
        }

        test("dividing by zero should throw") {
            shouldThrow<ArithmeticException> {
                10 / 0
            }
        }
    }
})

// Behavior spec (BDD)
class ClientTest : BehaviorSpec({
    given("a connected client") {
        val client = createClient()
        client.connect()

        `when`("sending a message") {
            val result = client.send("test")

            then("it should succeed") {
                result shouldBe Success
            }
        }

        `when`("disconnecting") {
            client.disconnect()

            then("it should be disconnected") {
                client.isConnected shouldBe false
            }
        }
    }
})
```

### Property-Based Testing

```kotlin
import io.kotest.core.spec.style.FunSpec
import io.kotest.property.Arb
import io.kotest.property.arbitrary.*
import io.kotest.property.checkAll

class PropertyTest : FunSpec({
    test("string reverse is involutive") {
        checkAll<String> { str ->
            str.reversed().reversed() shouldBe str
        }
    }

    test("addition is commutative") {
        checkAll(Arb.int(), Arb.int()) { a, b ->
            a + b shouldBe b + a
        }
    }

    test("custom generator") {
        val emailArb = arbitrary { rs ->
            val name = Arb.string(5..10).bind()
            val domain = Arb.string(5..10).bind()
            "$name@$domain.com"
        }

        checkAll(emailArb) { email ->
            email shouldContain "@"
        }
    }
})
```

### JUnit Integration

```kotlin
import org.junit.jupiter.api.Test
import org.junit.jupiter.api.BeforeEach
import org.junit.jupiter.api.DisplayName
import org.junit.jupiter.params.ParameterizedTest
import org.junit.jupiter.params.provider.ValueSource
import kotlin.test.assertEquals
import kotlin.test.assertTrue

class JUnitTest {
    private lateinit var client: Client

    @BeforeEach
    fun setup() {
        client = createClient()
    }

    @Test
    @DisplayName("Client should connect successfully")
    fun `client should connect`() {
        val result = client.connect()
        assertTrue(result.isSuccess)
    }

    @ParameterizedTest
    @ValueSource(strings = ["hello", "world", "test"])
    fun `should handle various inputs`(input: String) {
        val result = process(input)
        assertTrue(result.isNotEmpty())
    }
}
```

---

## KDoc Documentation

### Documentation Style

```kotlin
/**
 * Creates an HTTP client with the specified configuration.
 *
 * This function uses a DSL to configure the client. All settings
 * are optional and have sensible defaults.
 *
 * @param configure A lambda with receiver for configuring the client
 * @return A configured HTTP client instance
 *
 * @sample com.example.samples.basicClientExample
 * @see HttpClient for available configuration options
 * @since 1.0.0
 *
 * Example:
 * ```kotlin
 * val client = httpClient {
 *     timeout = 60_000
 *     followRedirects = false
 *     header("User-Agent", "MyApp/1.0")
 * }
 * ```
 */
fun httpClient(configure: HttpClient.() -> Unit): HttpClient {
    return HttpClient().apply(configure)
}

/**
 * Represents the result of an operation.
 *
 * @param T The type of the successful result value
 * @property value The result value if successful
 * @property error The error if failed
 *
 * @constructor Creates a result instance
 */
sealed class Result<out T> {
    /**
     * Represents a successful result.
     *
     * @property value The successful value
     */
    data class Success<T>(val value: T) : Result<T>()

    /**
     * Represents a failed result.
     *
     * @property error The error that caused the failure
     */
    data class Failure(val error: Throwable) : Result<Nothing>()
}
```

### Dokka Configuration

**build.gradle.kts:**
```kotlin
plugins {
    id("org.jetbrains.dokka") version "1.9.20"
}

tasks.dokkaHtml {
    outputDirectory.set(buildDir.resolve("dokka"))

    dokkaSourceSets {
        named("main") {
            moduleName.set("My Library")
            includes.from("docs/index.md")

            sourceLink {
                localDirectory.set(file("src/main/kotlin"))
                remoteUrl.set(
                    URL("https://github.com/user/repo/tree/main/src/main/kotlin")
                )
                remoteLineSuffix.set("#L")
            }

            externalDocumentationLink {
                url.set(URL("https://kotlinlang.org/api/latest/jvm/stdlib/"))
            }
        }
    }
}
```

---

## Publishing to Maven Central

### Setup Requirements

1. **Sonatype OSSRH Account**: Sign up at https://issues.sonatype.org
2. **GPG Key**: Generate and publish a GPG key
3. **Gradle Configuration**: Configure publishing plugin

### GPG Key Setup

```bash
# Generate key
gpg --gen-key

# List keys
gpg --list-keys

# Export public key
gpg --keyserver keyserver.ubuntu.com --send-keys YOUR_KEY_ID

# Export private key
gpg --export-secret-keys YOUR_KEY_ID > secring.gpg
```

### Publishing Plugin Configuration

**build.gradle.kts:**
```kotlin
plugins {
    `maven-publish`
    signing
    id("io.github.gradle-nexus.publish-plugin") version "1.3.0"
}

nexusPublishing {
    repositories {
        sonatype {
            nexusUrl.set(uri("https://s01.oss.sonatype.org/service/local/"))
            snapshotRepositoryUrl.set(
                uri("https://s01.oss.sonatype.org/content/repositories/snapshots/")
            )
            username.set(project.findProperty("sonatypeUsername") as String?)
            password.set(project.findProperty("sonatypePassword") as String?)
        }
    }
}

publishing {
    publications {
        create<MavenPublication>("maven") {
            from(components["java"])

            artifact(tasks["kotlinSourcesJar"])
            artifact(tasks["dokkaJavadocJar"])

            pom {
                name.set(project.name)
                description.set("Library description")
                url.set("https://github.com/user/repo")

                licenses {
                    license {
                        name.set("The Apache License, Version 2.0")
                        url.set("http://www.apache.org/licenses/LICENSE-2.0.txt")
                    }
                }

                developers {
                    developer {
                        id.set("userid")
                        name.set("User Name")
                        email.set("user@example.com")
                    }
                }

                scm {
                    connection.set("scm:git:git://github.com/user/repo.git")
                    developerConnection.set("scm:git:ssh://github.com/user/repo.git")
                    url.set("https://github.com/user/repo")
                }
            }
        }
    }
}

signing {
    sign(publishing.publications["maven"])
}

val dokkaJavadocJar by tasks.registering(Jar::class) {
    dependsOn(tasks.dokkaJavadoc)
    from(tasks.dokkaJavadoc.flatMap { it.outputDirectory })
    archiveClassifier.set("javadoc")
}

val kotlinSourcesJar by tasks.registering(Jar::class) {
    from(sourceSets["main"].allSource)
    archiveClassifier.set("sources")
}
```

### Publishing Workflow

```bash
# 1. Build the project
./gradlew build

# 2. Publish to local Maven for testing
./gradlew publishToMavenLocal

# 3. Publish to Sonatype staging
./gradlew publishToSonatype

# 4. Close and release staging repository
./gradlew closeAndReleaseSonatypeStagingRepository

# Or all in one
./gradlew publishToSonatype closeAndReleaseSonatypeStagingRepository
```

---

## Binary Compatibility

### API Validation Plugin

**build.gradle.kts:**
```kotlin
plugins {
    id("org.jetbrains.kotlinx.binary-compatibility-validator") version "0.14.0"
}

apiValidation {
    ignoredProjects.add("test-utils")

    nonPublicMarkers.add("com.example.InternalApi")

    validationDisabled = false
}
```

### Usage

```bash
# Generate API dump
./gradlew apiDump

# Check API compatibility
./gradlew apiCheck
```

**Commit the API dump:**
```
my-library/
├── api/
│   └── my-library.api
```

---

## Anti-Patterns

### 1. Overusing Extension Functions

```kotlin
// Bad: Extension on Any
fun Any.doSomething() { }

// Good: Specific type
fun String.doSomething() { }
```

### 2. Breaking API with Default Parameters

```kotlin
// v1.0.0
fun connect(host: String, port: Int = 8080)

// v1.1.0 - WRONG! This is breaking
fun connect(host: String, port: Int = 8080, timeout: Long)

// v1.1.0 - Correct: Add overload or new default at end
fun connect(host: String, port: Int = 8080, timeout: Long = 30000)
```

### 3. Not Using Visibility Modifiers

```kotlin
// Bad: Everything public by default
class InternalHelper {
    fun helpfulMethod() { }
}

// Good: Explicit visibility
internal class InternalHelper {
    internal fun helpfulMethod() { }
}
```

### 4. Mutable Public Collections

```kotlin
// Bad: Mutable public property
val items: MutableList<String> = mutableListOf()

// Good: Immutable public interface
private val _items: MutableList<String> = mutableListOf()
val items: List<String> get() = _items

// Or use read-only collection
val items: List<String> = listOf()
```

---

## Common Dependencies

### Coroutines

```kotlin
dependencies {
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-core:1.7.3")
    testImplementation("org.jetbrains.kotlinx:kotlinx-coroutines-test:1.7.3")
}
```

### Serialization

```kotlin
plugins {
    kotlin("plugin.serialization") version "1.9.22"
}

dependencies {
    implementation("org.jetbrains.kotlinx:kotlinx-serialization-json:1.6.2")
}
```

### Testing

```kotlin
dependencies {
    testImplementation(kotlin("test"))
    testImplementation("io.kotest:kotest-runner-junit5:5.8.0")
    testImplementation("io.kotest:kotest-assertions-core:5.8.0")
    testImplementation("io.kotest:kotest-property:5.8.0")
    testImplementation("io.mockk:mockk:1.13.9")
}
```

---

## References

- `meta-library-dev` - Foundational library patterns
- [Kotlin Coding Conventions](https://kotlinlang.org/docs/coding-conventions.html)
- [Kotlin API Guidelines](https://kotlinlang.org/docs/api-guidelines-introduction.html)
- [Maven Central Publishing Guide](https://central.sonatype.org/publish/publish-guide/)
- [Dokka Documentation](https://kotlinlang.org/docs/dokka-introduction.html)
- [Kotest Documentation](https://kotest.io/)
