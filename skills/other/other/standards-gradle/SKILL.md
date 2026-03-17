---
name: standards-gradle
description: Gradle build tool standards focusing on Kotlin DSL. Covers project configuration, dependency management, and custom plugin/task development with Gradle 9 LTS.
type: context
applies_to: [gradle]
file_extensions: [".gradle.kts", ".gradle"]
---

# Gradle Coding Standards (Gradle 9 LTS)

This skill provides comprehensive guidance for Gradle build configuration using Kotlin DSL (`.gradle.kts`). It covers both everyday project configuration and advanced plugin/task development patterns based on Gradle 9 LTS.

## Core Principles

1. **Declarative over Imperative**: Prefer declarative configuration that describes what you want, not how to achieve it
2. **Type-Safe Configuration**: Use Kotlin DSL for type safety and IDE support
3. **Lazy Configuration**: Use Providers API to defer configuration until needed
4. **Build Cache Friendly**: Write tasks that support build caching for faster builds
5. **Configuration Cache Compatible**: Ensure build scripts work with configuration cache for optimal performance

---

## Section 1: Project Configuration

This section covers the common scenarios developers encounter when configuring Gradle projects: setting up build scripts, managing dependencies, applying plugins, and structuring multi-module projects.

### Build Script Basics

#### build.gradle.kts Structure

Organize your build script in a consistent, readable order:

```kotlin
// 1. Plugin declarations (always first)
plugins {
    java
    application
    id("com.github.johnrengelman.shadow") version "8.1.1"
}

// 2. Project properties and versioning
group = "com.example"
version = "1.0.0"

// 3. Repositories
repositories {
    mavenCentral()
}

// 4. Dependencies
dependencies {
    implementation("com.google.guava:guava:33.0.0-jre")
    testImplementation("org.junit.jupiter:junit-jupiter:5.10.2")
}

// 5. Java/Kotlin configuration
java {
    toolchain {
        languageVersion = JavaLanguageVersion.of(21)
    }
}

// 6. Task configuration
tasks {
    test {
        useJUnitPlatform()
    }

    jar {
        manifest {
            attributes("Main-Class" to "com.example.Main")
        }
    }
}
```

#### settings.gradle.kts Basics

```kotlin
// Root project name
rootProject.name = "my-project"

// Enable Gradle version catalogs (Gradle 9+)
enableFeaturePreview("TYPESAFE_PROJECT_ACCESSORS")

// Include subprojects
include("app")
include("lib")
include("common")

// Optional: Customize subproject location
project(":app").projectDir = file("applications/app")
```

#### Repository Configuration

```kotlin
repositories {
    // GOOD: Standard repositories first
    mavenCentral()

    // GOOD: Google repository for Android/Google libraries
    google()

    // GOOD: Custom repository with HTTPS
    maven {
        name = "CompanyRepo"
        url = uri("https://repo.company.com/maven")
        credentials {
            username = providers.gradleProperty("repoUser").orNull
            password = providers.gradleProperty("repoPassword").orNull
        }
    }
}

// BAD: Using HTTP instead of HTTPS (security risk)
// maven { url = uri("http://insecure-repo.com/maven") }

// BAD: Exposing credentials in build script
// maven {
//     url = uri("https://repo.company.com/maven")
//     credentials {
//         username = "hardcoded-user"  // Never do this!
//         password = "hardcoded-pass"  // Never do this!
//     }
// }
```

#### Script Organization Best Practices

```kotlin
// GOOD: Use extra properties for shared values
val mockitoVersion by extra("5.10.0")
val junitVersion by extra("5.10.2")

dependencies {
    testImplementation("org.mockito:mockito-core:$mockitoVersion")
    testImplementation("org.junit.jupiter:junit-jupiter:$junitVersion")
}

// GOOD: Extract complex configuration to functions
fun configureJavaToolchain() {
    java {
        toolchain {
            languageVersion = JavaLanguageVersion.of(21)
            vendor = JvmVendorSpec.ADOPTIUM
        }
    }
}

// Apply configuration
configureJavaToolchain()
```

### Gradle Build Phases

Understanding Gradle's build phases is essential for writing efficient build scripts and understanding when your code executes.

#### The Three Build Phases

Every Gradle build runs through three distinct phases in order:

1. **Initialization Phase** - Determines which projects participate in the build
2. **Configuration Phase** - Configures all projects and builds the task graph
3. **Execution Phase** - Executes the selected tasks

Understanding these phases helps you:
- Write faster builds (keep configuration phase light)
- Understand lazy evaluation and Provider API
- Make configuration cache work correctly
- Debug build script behavior

#### 1. Initialization Phase

**Purpose:** Determine project structure and which projects participate in the build.

**What runs:** `settings.gradle.kts` files

**What happens:**
- Gradle locates and reads `settings.gradle.kts`
- Determines root project and subprojects
- Creates `Project` instances for each project

**Example:**
```kotlin
// settings.gradle.kts (runs during initialization)
rootProject.name = "my-project"

println("Initialization phase")  // Prints during initialization

include("app")
include("lib")
include("common")

// Optional: Customize subproject directories
project(":app").projectDir = file("applications/app")
```

**Duration:** Very fast (typically < 100ms)

**Key Point:** You cannot access `Project` objects yet - they're being created.

#### 2. Configuration Phase

**Purpose:** Configure all tasks and build the task execution graph.

**What runs:** All `build.gradle.kts` files for participating projects

**What happens:**
- Applies plugins
- Evaluates all top-level code in build scripts
- Configures tasks (but doesn't execute them)
- Builds task dependency graph
- Prepares for execution

**Example:**
```kotlin
// build.gradle.kts (runs during configuration)

plugins {
    java  // Runs during configuration
}

version = "1.0.0"  // Runs during configuration

println("Configuration phase")  // Runs during configuration

tasks.register("myTask") {
    group = "custom"  // Runs during configuration
    description = "Example task"  // Runs during configuration

    println("Task configuration")  // Runs during configuration

    doLast {
        println("Task execution")  // Does NOT run during configuration!
    }
}

// This runs during configuration
val projectVersion = version
println("Project version: $projectVersion")

// BAD: Expensive work during configuration
// val allFiles = File("src").walkTopDown().toList()  // Slows every build!

// GOOD: Use providers for lazy evaluation
val sourceFiles: Provider<FileTree> = providers.provider {
    fileTree("src")  // Only evaluated when needed
}
```

**Duration:** Can be slow if not careful (seconds to minutes for large projects)

**Key Point:** Configuration runs on **every** build, even if no tasks execute. Keep it fast!

#### 3. Execution Phase

**Purpose:** Execute the selected tasks in dependency order.

**What runs:** Task actions (`doFirst`, `doLast`, `@TaskAction`)

**What happens:**
- Tasks execute in correct dependency order
- Task inputs are read
- Task outputs are generated
- Build artifacts are created

**Example:**
```kotlin
tasks.register("myTask") {
    // Configuration phase
    group = "custom"

    doFirst {
        // Execution phase - runs first
        println("Starting task")
    }

    doLast {
        // Execution phase - runs last
        println("Task completed")
    }
}

// Abstract task with @TaskAction
abstract class BuildTask : DefaultTask() {
    @get:InputDirectory
    abstract val sourceDir: DirectoryProperty

    @get:OutputDirectory
    abstract val outputDir: DirectoryProperty

    @TaskAction  // Execution phase
    fun build() {
        println("Building...")
        // Actual work happens here
    }
}
```

**Duration:** Depends on what tasks do (compile, test, package, etc.)

**Key Point:** Only requested tasks (and their dependencies) execute.

#### When Code Runs - Quick Reference

| Code Location | Phase | Example |
|---------------|-------|---------|
| `settings.gradle.kts` (top-level) | Initialization | `rootProject.name = "app"` |
| `build.gradle.kts` (top-level) | Configuration | `version = "1.0"` |
| `plugins {}` block | Configuration | `java` |
| `dependencies {}` block | Configuration | `implementation(...)` |
| `tasks.register { }` outer block | Configuration | `group = "custom"` |
| `tasks.register { }` inner block | Configuration | `dependsOn("other")` |
| Extension configuration blocks | Configuration | `java { toolchain { } }` |
| `doFirst { }` | Execution | `println("starting")` |
| `doLast { }` | Execution | `println("done")` |
| `@TaskAction` method | Execution | `fun execute() { }` |
| Provider.get() in doLast | Execution | `val v = provider.get()` |

#### Common Mistakes and Anti-Patterns

```kotlin
// ❌ BAD: Expensive I/O during configuration
tasks.register("badTask") {
    val files = File("src").listFiles()  // I/O during configuration - runs every build!
    println("Found ${files?.size} files")

    doLast {
        println("Processing ${files?.size} files")
    }
}

// ✅ GOOD: Defer work to execution
tasks.register("goodTask") {
    doLast {
        val files = File("src").listFiles()  // I/O during execution - only when task runs
        println("Found ${files?.size} files")
        println("Processing ${files.size} files")
    }
}

// ❌ BAD: Accessing task outputs during configuration
tasks.register("badConsumer") {
    val compileOutput = tasks.named("compileJava").get().outputs.files  // Not ready yet!

    doLast {
        println(compileOutput)
    }
}

// ✅ GOOD: Use providers to defer access
tasks.register("goodConsumer") {
    val compileOutput = tasks.named("compileJava").map { it.outputs.files }

    doLast {
        println(compileOutput.get())  // Resolved during execution
    }
}

// ❌ BAD: Network calls during configuration
tasks.register("badFetch") {
    val response = URL("https://api.example.com/version").readText()  // Slows every build!

    doLast {
        println("Version: $response")
    }
}

// ✅ GOOD: Use providers for network calls
tasks.register("goodFetch") {
    val response: Provider<String> = providers.provider {
        URL("https://api.example.com/version").readText()
    }

    doLast {
        println("Version: ${response.get()}")  // Only called during execution
    }
}

// ❌ BAD: Calling .get() on providers during configuration
tasks.register("badProvider") {
    val version = providers.gradleProperty("version").get()  // Eager evaluation!

    doLast {
        println("Version: $version")
    }
}

// ✅ GOOD: Defer .get() until execution
tasks.register("goodProvider") {
    val version = providers.gradleProperty("version")  // Lazy - not evaluated yet

    doLast {
        println("Version: ${version.get()}")  // Evaluated here
    }
}

// ❌ BAD: Mutating shared state during configuration
var counter = 0  // Global mutable state

tasks.register("bad1") {
    counter++  // Modifies global state during configuration
    doLast { println("Counter: $counter") }
}

tasks.register("bad2") {
    counter++  // Order-dependent!
    doLast { println("Counter: $counter") }
}

// ✅ GOOD: Use build services or task outputs for shared state
```

#### Why Build Phases Matter

**1. Build Performance**

Configuration phase runs on **every** build:
```bash
./gradlew tasks       # Configuration runs
./gradlew clean       # Configuration runs
./gradlew build       # Configuration runs
./gradlew --stop      # Configuration runs
```

Slow configuration = slow every command, even `./gradlew tasks`!

**2. Configuration Cache**

Configuration cache stores the result of configuration phase:
```bash
# First run: Configuration + execution
./gradlew build --configuration-cache
# Configuration phase: 5 seconds
# Execution phase: 30 seconds

# Second run: Execution only
./gradlew clean build --configuration-cache
# Configuration phase: 0 seconds (reused from cache!)
# Execution phase: 30 seconds
```

**Benefits:**
- Up to 90% faster builds (skip configuration entirely)
- Especially valuable for large projects

**Requirements:**
- Use Provider API (lazy evaluation)
- No mutable shared state
- No accessing `project` during execution
- Serializable configuration

**3. Up-to-Date Checks**

Tasks are up-to-date when:
- Inputs haven't changed
- Outputs exist and are valid

Input/output annotations are evaluated during:
- **Configuration:** Gradle determines task inputs/outputs
- **Execution:** Gradle checks if task needs to run

Proper annotations enable:
- Incremental builds
- Build cache
- `FROM-CACHE` and `UP-TO-DATE` optimizations

#### Best Practices for Build Phases

**Do:**
- ✅ Keep configuration phase fast (< 1 second per project ideal)
- ✅ Use `tasks.register()` for lazy task creation
- ✅ Use Provider API for lazy evaluation
- ✅ Defer expensive work to execution phase
- ✅ Use `@Input`/`@Output` annotations properly
- ✅ Test with `--configuration-cache` to catch issues

**Don't:**
- ❌ Perform I/O during configuration (file scanning, network calls)
- ❌ Use `tasks.create()` (eager - prefer `register()`)
- ❌ Call `.get()` on providers during configuration
- ❌ Access task outputs during configuration
- ❌ Mutate global/shared state during configuration
- ❌ Use `project` references in task actions

#### Debugging Build Phases

```bash
# See configuration time breakdown
./gradlew build --profile
# Open: build/reports/profile/profile-<timestamp>.html

# Measure configuration time
./gradlew build --configuration-cache --configuration-cache-problems=warn

# See what runs during configuration
./gradlew build --info | grep "Configuration"

# Test configuration cache compatibility
./gradlew build --configuration-cache
./gradlew clean build --configuration-cache  # Should show "Reusing configuration cache"
```

#### Example: Full Build Lifecycle

```kotlin
// settings.gradle.kts
println("1. Initialization phase: settings.gradle.kts")
rootProject.name = "lifecycle-demo"

// build.gradle.kts
println("2. Configuration phase: build.gradle.kts top-level")

plugins {
    java
    println("3. Configuration phase: plugins block")
}

println("4. Configuration phase: after plugins")

tasks.register("demo") {
    println("5. Configuration phase: task configuration")

    group = "demo"
    description = "Demonstrates build phases"

    doFirst {
        println("7. Execution phase: doFirst")
    }

    doLast {
        println("8. Execution phase: doLast")
    }
}

println("6. Configuration phase: after task registration")

// When you run: ./gradlew demo
// Output order:
// 1. Initialization phase: settings.gradle.kts
// 2. Configuration phase: build.gradle.kts top-level
// 3. Configuration phase: plugins block
// 4. Configuration phase: after plugins
// 5. Configuration phase: task configuration
// 6. Configuration phase: after task registration
// 7. Execution phase: doFirst
// 8. Execution phase: doLast
```

### Dependency Management

#### Dependency Configurations

```kotlin
dependencies {
    // GOOD: implementation - for internal dependencies (not exposed to consumers)
    implementation("com.google.guava:guava:33.0.0-jre")

    // GOOD: api - for dependencies exposed to consumers (libraries only)
    // Only available with java-library plugin
    api("org.apache.commons:commons-lang3:3.14.0")

    // GOOD: compileOnly - compile-time only (not packaged)
    compileOnly("org.projectlombok:lombok:1.18.30")

    // GOOD: runtimeOnly - runtime only (not on compile classpath)
    runtimeOnly("com.h2database:h2:2.2.224")

    // GOOD: testImplementation - for test code only
    testImplementation("org.junit.jupiter:junit-jupiter:5.10.2")
    testImplementation("org.mockito:mockito-core:5.10.0")

    // GOOD: testRuntimeOnly - test runtime only
    testRuntimeOnly("org.junit.platform:junit-platform-launcher")
}

// BAD: Using 'compile' (deprecated in Gradle 7+)
// dependencies {
//     compile("some:library:1.0")  // Use 'implementation' instead
// }

// BAD: Using 'runtime' (deprecated in Gradle 7+)
// dependencies {
//     runtime("some:library:1.0")  // Use 'runtimeOnly' instead
// }
```

#### Version Catalogs (Modern Gradle Approach)

**gradle/libs.versions.toml:**
```toml
[versions]
guava = "33.0.0-jre"
junit = "5.10.2"
mockito = "5.10.0"
kotlin = "2.0.0"

[libraries]
guava = { module = "com.google.guava:guava", version.ref = "guava" }
junit-jupiter = { module = "org.junit.jupiter:junit-jupiter", version.ref = "junit" }
junit-platform-launcher = { module = "org.junit.platform:junit-platform-launcher" }
mockito-core = { module = "org.mockito:mockito-core", version.ref = "mockito" }

[bundles]
testing = ["junit-jupiter", "mockito-core"]

[plugins]
kotlin-jvm = { id = "org.jetbrains.kotlin.jvm", version.ref = "kotlin" }
shadow = { id = "com.github.johnrengelman.shadow", version = "8.1.1" }
```

**build.gradle.kts:**
```kotlin
plugins {
    alias(libs.plugins.kotlin.jvm)
}

dependencies {
    // GOOD: Type-safe accessors from version catalog
    implementation(libs.guava)
    testImplementation(libs.bundles.testing)
    testRuntimeOnly(libs.junit.platform.launcher)
}

// Benefits:
// - Centralized version management
// - Type-safe accessors with IDE completion
// - Easy to share across multi-module projects
// - Prevents version conflicts
```

#### Dependency Constraints

```kotlin
dependencies {
    implementation("com.example:library:1.0")

    // GOOD: Force specific version to resolve conflicts
    constraints {
        implementation("org.slf4j:slf4j-api:2.0.9") {
            because("Earlier versions have security vulnerabilities")
        }
    }

    // GOOD: Align versions across dependency group
    constraints {
        implementation("org.springframework.boot:spring-boot-starter-web:3.2.0")
        implementation("org.springframework.boot:spring-boot-starter-data-jpa:3.2.0")
    }
}
```

#### Platform/BOM Dependencies

```kotlin
dependencies {
    // GOOD: Import BOM (Bill of Materials) for version alignment
    implementation(platform("org.springframework.boot:spring-boot-dependencies:3.2.0"))

    // Now you can omit versions - they come from the BOM
    implementation("org.springframework.boot:spring-boot-starter-web")
    implementation("org.springframework.boot:spring-boot-starter-data-jpa")

    // GOOD: For testing, use testImplementation(platform(...))
    testImplementation(platform("org.junit:junit-bom:5.10.2"))
    testImplementation("org.junit.jupiter:junit-jupiter")
}
```

#### Excluding Transitive Dependencies

```kotlin
dependencies {
    // GOOD: Exclude specific transitive dependency
    implementation("com.example:library:1.0") {
        exclude(group = "commons-logging", module = "commons-logging")
    }

    // GOOD: Exclude all transitive dependencies (rare case)
    implementation("com.example:utility:1.0") {
        isTransitive = false
    }

    // Replace excluded dependency with alternative
    implementation("org.slf4j:jcl-over-slf4j:2.0.9")
}

// GOOD: Exclude globally (affects all dependencies)
configurations.all {
    exclude(group = "commons-logging", module = "commons-logging")
}
```

#### Dependency Notation

```kotlin
dependencies {
    // GOOD: String notation (most common)
    implementation("com.google.guava:guava:33.0.0-jre")

    // GOOD: Map notation (when you need more control)
    implementation(group = "com.google.guava", name = "guava", version = "33.0.0-jre")

    // GOOD: With classifier
    implementation("net.java.dev.jna:jna:5.13.0:jpms")

    // GOOD: Local file dependency
    implementation(files("libs/custom-library.jar"))

    // GOOD: File tree dependency
    implementation(fileTree("libs") { include("*.jar") })

    // GOOD: Project dependency (multi-module)
    implementation(project(":common"))
}
```

### Plugin Configuration

#### Plugin Application

```kotlin
plugins {
    // GOOD: Core plugins (no version needed)
    java
    application

    // GOOD: External plugin with version
    id("com.github.johnrengelman.shadow") version "8.1.1"

    // GOOD: Kotlin plugin
    kotlin("jvm") version "2.0.0"

    // GOOD: Apply false (for root project in multi-module)
    id("org.springframework.boot") version "3.2.0" apply false
}

// BAD: Old apply() syntax (avoid in new code)
// apply(plugin = "java")  // Use plugins {} block instead
```

#### Using Version Catalogs with Plugins

```kotlin
// gradle/libs.versions.toml
// [plugins]
// kotlin-jvm = { id = "org.jetbrains.kotlin.jvm", version = "2.0.0" }
// shadow = { id = "com.github.johnrengelman.shadow", version = "8.1.1" }

plugins {
    // GOOD: Type-safe plugin declaration from catalog
    alias(libs.plugins.kotlin.jvm)
    alias(libs.plugins.shadow)
}
```

#### Common Plugins

**Java Plugin:**
```kotlin
plugins {
    java
}

java {
    // GOOD: Use Java toolchain (modern approach)
    toolchain {
        languageVersion = JavaLanguageVersion.of(21)
        vendor = JvmVendorSpec.ADOPTIUM
    }

    // GOOD: Configure compatibility (legacy approach)
    // sourceCompatibility = JavaVersion.VERSION_21
    // targetCompatibility = JavaVersion.VERSION_21

    // GOOD: Enable automatic module name for JPMS
    modularity.inferModulePath = true

    // GOOD: Generate sources and javadoc JARs
    withSourcesJar()
    withJavadocJar()
}
```

**Kotlin JVM Plugin:**
```kotlin
plugins {
    kotlin("jvm") version "2.0.0"
}

kotlin {
    // GOOD: Set JVM target
    jvmToolchain(21)

    // GOOD: Enable explicit API mode (libraries)
    explicitApi()

    // GOOD: Compiler options
    compilerOptions {
        freeCompilerArgs.add("-Xjsr305=strict")
        allWarningsAsErrors = true
    }
}
```

**Application Plugin:**
```kotlin
plugins {
    application
}

application {
    // GOOD: Set main class
    mainClass = "com.example.Main"

    // GOOD: Configure application name
    applicationName = "my-app"

    // GOOD: Set default JVM args
    applicationDefaultJvmArgs = listOf("-Xmx512m", "-Xms256m")
}

// Run with: ./gradlew run
// Package with: ./gradlew installDist
```

**Java Library Plugin:**
```kotlin
plugins {
    `java-library`  // Note the backticks for kebab-case
}

dependencies {
    // GOOD: Use 'api' for exposed dependencies
    api("org.apache.commons:commons-lang3:3.14.0")

    // GOOD: Use 'implementation' for internal dependencies
    implementation("com.google.guava:guava:33.0.0-jre")
}

// Consumers of this library get:
// - api dependencies on their compile classpath
// - implementation dependencies are hidden
```

#### Configuring Plugin Extensions

```kotlin
plugins {
    java
    jacoco
}

// GOOD: Configure extension in dedicated block
jacoco {
    toolVersion = "0.8.11"
    reportsDirectory = layout.buildDirectory.dir("reports/jacoco")
}

// GOOD: Configure task created by plugin
tasks.jacocoTestReport {
    dependsOn(tasks.test)
    reports {
        xml.required = true
        html.required = true
        csv.required = false
    }
}

// BAD: Accessing extension before plugin is applied
// jacoco { ... }  // Will fail if jacoco plugin not applied
// plugins { jacoco }  // Plugin should come first
```

#### Conditional Plugin Application

```kotlin
plugins {
    java
    if (project.hasProperty("enableKotlin")) {
        kotlin("jvm") version "2.0.0"
    }
}

// Alternative: Apply plugin conditionally
if (project.findProperty("coverage") == "true") {
    apply(plugin = "jacoco")
}
```

### Multi-Module Projects

#### Project Structure

```
my-project/
├── settings.gradle.kts         # Project structure definition
├── build.gradle.kts            # Root build script
├── gradle/
│   └── libs.versions.toml      # Shared version catalog
├── app/
│   ├── build.gradle.kts        # Application module
│   └── src/
├── lib/
│   ├── build.gradle.kts        # Library module
│   └── src/
└── common/
    ├── build.gradle.kts        # Shared code module
    └── src/
```

**settings.gradle.kts:**
```kotlin
rootProject.name = "my-project"

// Enable type-safe project accessors (Gradle 7+)
enableFeaturePreview("TYPESAFE_PROJECT_ACCESSORS")

include("app")
include("lib")
include("common")

// Optional: Nested modules
include("backend:api")
include("backend:service")
```

**Root build.gradle.kts:**
```kotlin
plugins {
    // GOOD: Apply plugins to all subprojects
    java apply false
    kotlin("jvm") version "2.0.0" apply false
}

// GOOD: Configure all projects (including root)
allprojects {
    group = "com.example"
    version = "1.0.0"

    repositories {
        mavenCentral()
    }
}

// GOOD: Configure only subprojects
subprojects {
    // Apply common configuration here
}
```

#### Convention Plugins (Recommended Approach)

Convention plugins encapsulate shared configuration in a type-safe, reusable way.

**buildSrc/build.gradle.kts:**
```kotlin
plugins {
    `kotlin-dsl`
}

repositories {
    mavenCentral()
}
```

**buildSrc/src/main/kotlin/java-conventions.gradle.kts:**
```kotlin
plugins {
    java
}

java {
    toolchain {
        languageVersion = JavaLanguageVersion.of(21)
    }
}

repositories {
    mavenCentral()
}

dependencies {
    testImplementation("org.junit.jupiter:junit-jupiter:5.10.2")
    testRuntimeOnly("org.junit.platform:junit-platform-launcher")
}

tasks.test {
    useJUnitPlatform()
}
```

**app/build.gradle.kts:**
```kotlin
plugins {
    id("java-conventions")  // Apply convention plugin
    application
}

application {
    mainClass = "com.example.app.Main"
}

dependencies {
    implementation(project(":lib"))
    implementation(project(":common"))
}
```

**lib/build.gradle.kts:**
```kotlin
plugins {
    id("java-conventions")  // Apply convention plugin
    `java-library`
}

dependencies {
    api(project(":common"))
    implementation("com.google.guava:guava:33.0.0-jre")
}
```

#### Cross-Module Dependencies

```kotlin
dependencies {
    // GOOD: Type-safe project accessor (with TYPESAFE_PROJECT_ACCESSORS)
    implementation(projects.common)
    implementation(projects.backend.api)

    // GOOD: String-based (works without feature preview)
    implementation(project(":common"))
    implementation(project(":backend:api"))

    // GOOD: Depend on specific configuration
    testImplementation(project(path = ":lib", configuration = "testFixtures"))
}
```

#### Shared Configuration Patterns

**Pattern 1: subprojects {} (Quick but limited)**
```kotlin
subprojects {
    apply(plugin = "java")

    java {
        toolchain {
            languageVersion = JavaLanguageVersion.of(21)
        }
    }

    dependencies {
        testImplementation("org.junit.jupiter:junit-jupiter:5.10.2")
    }
}

// BAD: Hard to override, not type-safe, mixes concerns
```

**Pattern 2: Convention Plugins (Recommended)**
```kotlin
// buildSrc/src/main/kotlin/java-library-conventions.gradle.kts
plugins {
    `java-library`
}

java {
    toolchain {
        languageVersion = JavaLanguageVersion.of(21)
    }
}

// GOOD: Type-safe, reusable, easy to override
// Modules apply with: plugins { id("java-library-conventions") }
```

#### buildSrc vs Included Builds vs Composite Builds

**buildSrc (For Convention Plugins):**
- Built automatically before main build
- Used for convention plugins and build logic
- Not published
- Changes require Gradle daemon restart

```
project/
├── buildSrc/
│   ├── build.gradle.kts
│   └── src/main/kotlin/
│       └── java-conventions.gradle.kts
└── build.gradle.kts
```

**Included Builds (For Build Logic Libraries):**
- Separate Gradle project included in your build
- Can be published independently
- Changes don't require daemon restart

**settings.gradle.kts:**
```kotlin
includeBuild("build-logic")

include("app")
include("lib")
```

**Composite Builds (For Multi-Repo Projects):**
- Combine multiple independent Gradle builds
- Each build has its own settings.gradle.kts

**settings.gradle.kts:**
```kotlin
includeBuild("../other-project")
```

#### Dependency Management Across Modules

**Using Version Catalogs (Recommended):**
```kotlin
// gradle/libs.versions.toml (at root)
[versions]
guava = "33.0.0-jre"

[libraries]
guava = { module = "com.google.guava:guava", version.ref = "guava" }

// All modules can use: implementation(libs.guava)
```

**Platform Projects (Alternative):**
```kotlin
// platform/build.gradle.kts
plugins {
    `java-platform`
}

dependencies {
    constraints {
        api("com.google.guava:guava:33.0.0-jre")
        api("org.slf4j:slf4j-api:2.0.9")
    }
}

// Other modules:
dependencies {
    implementation(platform(project(":platform")))
    implementation("com.google.guava:guava")  // Version from platform
}
```

### Gradle 9 Features

Gradle 9 is the latest LTS (Long-Term Support) release with significant improvements to performance, developer experience, and build reliability.

#### Configuration Cache (Stable in Gradle 9)

Configuration cache dramatically speeds up builds by caching the result of the configuration phase.

**Enable in gradle.properties:**
```properties
org.gradle.configuration-cache=true
```

**Or via command line:**
```bash
./gradlew build --configuration-cache
```

**Benefits:**
- Up to 90% faster for configuration-heavy builds
- Second builds reuse cached configuration
- Encourages better build practices

**Making Your Build Compatible:**
```kotlin
// GOOD: Use providers instead of direct property access
val myProperty: Provider<String> = providers.gradleProperty("myProp")

tasks.register("example") {
    doLast {
        println(myProperty.get())  // Lazy evaluation
    }
}

// BAD: Direct property access (breaks configuration cache)
// val value = project.findProperty("myProp")  // Evaluated at configuration time
```

#### Build Cache (Enhanced in Gradle 9)

**Enable in gradle.properties:**
```properties
org.gradle.caching=true
```

**Or via command line:**
```bash
./gradlew build --build-cache
```

**Configure cache:**
```kotlin
buildCache {
    local {
        isEnabled = true
        directory = file("${rootDir}/.gradle/build-cache")
        removeUnusedEntriesAfterDays = 30
    }

    remote<HttpBuildCache> {
        isEnabled = true
        url = uri("https://cache.example.com/")
        isPush = System.getenv("CI") == "true"  // Only push from CI
        credentials {
            username = providers.gradleProperty("cacheUser").orNull
            password = providers.gradleProperty("cachePassword").orNull
        }
    }
}
```

#### Improved Test Suites API

```kotlin
testing {
    suites {
        val test by getting(JvmTestSuite::class) {
            useJUnitJupiter("5.10.2")
        }

        // GOOD: Define integration test suite
        val integrationTest by registering(JvmTestSuite::class) {
            testType = TestSuiteType.INTEGRATION_TEST

            dependencies {
                implementation(project())
                implementation("org.testcontainers:junit-jupiter:1.19.3")
            }

            targets {
                all {
                    testTask.configure {
                        shouldRunAfter(test)
                    }
                }
            }
        }
    }
}

// Run with: ./gradlew integrationTest
```

#### Java Toolchains (Enhanced)

```kotlin
java {
    toolchain {
        // GOOD: Specify vendor
        vendor = JvmVendorSpec.ADOPTIUM
        languageVersion = JavaLanguageVersion.of(21)

        // GOOD: Gradle auto-downloads if not available
    }
}

// GOOD: Use different toolchain for specific task
tasks.register<JavaExec>("runWithJava17") {
    javaLauncher = javaToolchains.launcherFor {
        languageVersion = JavaLanguageVersion.of(17)
    }
}
```

#### Problems API (New in Gradle 8+, Refined in 9)

Better error reporting and problem aggregation:

```kotlin
// Gradle automatically collects and reports problems
// Your build output now shows:
// - Aggregated problems
// - Actionable error messages
// - Problem locations with file:line references

// No configuration needed - it just works better!
```

#### Isolated Projects (Experimental in Gradle 9)

Parallel configuration of subprojects for massive multi-module builds.

```properties
# gradle.properties
org.gradle.unsafe.isolated-projects=true
```

**Benefits:**
- Parallel configuration of independent projects
- Reduced configuration time for large builds
- Requires strict project isolation

#### Deprecated Features to Avoid

```kotlin
// BAD: compile, runtime configurations (removed in Gradle 8+)
// dependencies {
//     compile("some:library:1.0")  // Use 'implementation'
//     runtime("some:library:1.0")  // Use 'runtimeOnly'
// }

// BAD: Old task creation API (prefer register)
// tasks.create("myTask") { ... }  // Use tasks.register("myTask") { ... }

// BAD: Convention properties (use extensions)
// project.convention.plugins  // Use project.extensions

// BAD: Direct task execution during configuration
// tasks.named("build").get().execute()  // Never execute tasks during configuration
```

#### Performance Improvements in Gradle 9

1. **Faster dependency resolution** - Up to 40% faster for large dependency graphs
2. **Improved incremental compilation** - Better change detection for Java/Kotlin
3. **Enhanced file system watching** - More efficient change detection
4. **Better daemon memory management** - Reduced memory usage over time
5. **Optimized configuration cache** - Faster serialization/deserialization

#### Best Practices for Gradle 9

```kotlin
// GOOD: Enable all performance features
// gradle.properties:
org.gradle.caching=true
org.gradle.configuration-cache=true
org.gradle.parallel=true
org.gradle.vfs.watch=true

// GOOD: Use Java toolchains instead of sourceCompatibility
java {
    toolchain {
        languageVersion = JavaLanguageVersion.of(21)
    }
}

// GOOD: Use lazy task registration
tasks.register("myTask") {
    doLast { ... }
}

// GOOD: Use Provider API for task inputs
abstract class MyTask : DefaultTask() {
    @get:Input
    abstract val message: Property<String>

    @TaskAction
    fun execute() {
        println(message.get())
    }
}
```

---

## Section 2: Plugin/Task Development

This section covers advanced topics for developers building custom Gradle plugins and tasks: proper input/output handling, extensions, lazy configuration with Providers API, and build caching.

### Custom Tasks

#### Lazy vs Eager Task Registration

```kotlin
// BAD: Eager task creation (always executed during configuration)
tasks.create("eagerTask") {
    doLast {
        println("Task executed")
    }
}
// Problem: Task is configured immediately, slowing configuration phase

// GOOD: Lazy task registration (configured only when needed)
tasks.register("lazyTask") {
    doLast {
        println("Task executed")
    }
}
// Benefit: Task configured only if needed (e.g., when explicitly run)
```

#### Task Actions

```kotlin
// GOOD: Simple task with doLast
tasks.register("hello") {
    doLast {
        println("Hello from task")
    }
}

// GOOD: Multiple actions (executed in order)
tasks.register("multiAction") {
    doFirst {
        println("First action")
    }
    doLast {
        println("Last action")
    }
}

// GOOD: Named action (can be removed later if needed)
tasks.register("namedAction") {
    val myAction = Action<Task> {
        println("Named action")
    }
    doLast(myAction)
}
```

#### Abstract Task Classes (Recommended for Reusable Tasks)

```kotlin
import org.gradle.api.DefaultTask
import org.gradle.api.file.*
import org.gradle.api.provider.Property
import org.gradle.api.tasks.*

// GOOD: Abstract task with typed properties
abstract class ProcessFilesTask : DefaultTask() {

    @get:InputDirectory
    @get:PathSensitive(PathSensitivity.RELATIVE)
    abstract val inputDir: DirectoryProperty

    @get:OutputDirectory
    abstract val outputDir: DirectoryProperty

    @get:Input
    @get:Optional
    abstract val prefix: Property<String>

    init {
        // Set defaults
        prefix.convention("processed-")
    }

    @TaskAction
    fun process() {
        val input = inputDir.get().asFile
        val output = outputDir.get().asFile

        output.mkdirs()

        input.listFiles()?.forEach { file ->
            val processed = output.resolve("${prefix.get()}${file.name}")
            processed.writeText(file.readText().uppercase())
        }

        println("Processed ${input.listFiles()?.size ?: 0} files")
    }
}

// Register task with configuration
tasks.register<ProcessFilesTask>("processFiles") {
    inputDir = layout.projectDirectory.dir("src/data")
    outputDir = layout.buildDirectory.dir("processed")
    prefix = "PROCESSED-"
}
```

#### Input and Output Annotations

**Critical for up-to-date checking and caching:**

```kotlin
abstract class AdvancedTask : DefaultTask() {

    // GOOD: Input file
    @get:InputFile
    @get:PathSensitive(PathSensitivity.NONE)  // Content-only sensitivity
    abstract val inputFile: RegularFileProperty

    // GOOD: Input files
    @get:InputFiles
    @get:PathSensitive(PathSensitivity.RELATIVE)  // Path matters
    abstract val inputFiles: ConfigurableFileCollection

    // GOOD: Input directory
    @get:InputDirectory
    @get:PathSensitive(PathSensitivity.RELATIVE)
    abstract val inputDir: DirectoryProperty

    // GOOD: Input property (string, boolean, etc.)
    @get:Input
    abstract val message: Property<String>

    // GOOD: Optional input
    @get:Input
    @get:Optional
    abstract val optionalFlag: Property<Boolean>

    // GOOD: Output file
    @get:OutputFile
    abstract val outputFile: RegularFileProperty

    // GOOD: Output directory
    @get:OutputDirectory
    abstract val outputDir: DirectoryProperty

    // GOOD: Internal property (not an input/output)
    @get:Internal
    abstract val internalState: Property<String>

    @TaskAction
    fun execute() {
        // Task implementation
    }
}
```

**PathSensitivity options:**
- `NONE` - Only file content matters (not path or name)
- `NAME_ONLY` - File name matters
- `RELATIVE` - Relative path matters (most common)
- `ABSOLUTE` - Absolute path matters (rare)

#### Task Dependencies

```kotlin
// GOOD: Task depends on another task
tasks.register("taskA") {
    doLast { println("Task A") }
}

tasks.register("taskB") {
    dependsOn("taskA")  // taskA runs before taskB
    doLast { println("Task B") }
}

// GOOD: Multiple dependencies
tasks.register("taskC") {
    dependsOn("taskA", "taskB")
    doLast { println("Task C") }
}

// GOOD: Ordering without hard dependency
tasks.register("taskD") {
    mustRunAfter("taskB")  // If both run, D runs after B
    doLast { println("Task D") }
}

tasks.register("taskE") {
    shouldRunAfter("taskD")  // Ordering hint (not enforced)
    doLast { println("Task E") }
}

// GOOD: Finalization
tasks.register("taskF") {
    doLast { println("Task F") }
}

tasks.register("cleanup") {
    doLast { println("Cleanup") }
}

tasks.named("taskF") {
    finalizedBy("cleanup")  // cleanup always runs after taskF
}
```

#### Working Example: File Processing Task

```kotlin
abstract class TransformMarkdownTask : DefaultTask() {

    @get:InputFiles
    @get:PathSensitive(PathSensitivity.RELATIVE)
    abstract val markdownFiles: ConfigurableFileCollection

    @get:OutputDirectory
    abstract val htmlOutputDir: DirectoryProperty

    @get:Input
    abstract val title: Property<String>

    init {
        title.convention("Documentation")
    }

    @TaskAction
    fun transform() {
        val outputDir = htmlOutputDir.get().asFile
        outputDir.mkdirs()

        markdownFiles.forEach { mdFile ->
            val htmlFile = outputDir.resolve("${mdFile.nameWithoutExtension}.html")
            val content = mdFile.readText()

            htmlFile.writeText("""
                <!DOCTYPE html>
                <html>
                <head><title>${title.get()}</title></head>
                <body>
                    <pre>$content</pre>
                </body>
                </html>
            """.trimIndent())
        }

        logger.lifecycle("Transformed ${markdownFiles.files.size} markdown files")
    }
}

// Register and configure
tasks.register<TransformMarkdownTask>("transformMarkdown") {
    markdownFiles.from(fileTree("docs") { include("**/*.md") })
    htmlOutputDir = layout.buildDirectory.dir("html")
    title = "My Project Documentation"
}
```

#### Task Configuration Avoidance

```kotlin
// GOOD: Configure task only when needed
tasks.named<JavaCompile>("compileJava") {
    options.compilerArgs.add("-Xlint:unchecked")
}

// BAD: Getting task eagerly (forces configuration)
// val compileJava = tasks.getByName("compileJava")  // Avoid this

// GOOD: Lazy task reference
val compileJavaTask = tasks.named("compileJava")

// GOOD: Configure all tasks of type
tasks.withType<Test>().configureEach {
    useJUnitPlatform()
    maxParallelForks = Runtime.getRuntime().availableProcessors()
}
```

### Extension API

Extensions provide a DSL for configuring plugins. They're essential for creating user-friendly custom plugins.

#### Simple Extension

```kotlin
// Define extension (in buildSrc or custom plugin)
abstract class GreetingExtension {
    abstract val message: Property<String>
    abstract val times: Property<Int>

    init {
        // Set default values
        message.convention("Hello")
        times.convention(1)
    }
}

// Register extension in plugin
class GreetingPlugin : Plugin<Project> {
    override fun apply(project: Project) {
        // Create extension
        val extension = project.extensions.create("greeting", GreetingExtension::class.java)

        // Use extension to configure task
        project.tasks.register("greet") {
            doLast {
                repeat(extension.times.get()) {
                    println(extension.message.get())
                }
            }
        }
    }
}

// Usage in build.gradle.kts
plugins {
    id("greeting-plugin")
}

greeting {
    message = "Hello, Gradle!"
    times = 3
}
```

#### Extension Anti-Patterns

```kotlin
// BAD: Using plain variables instead of Property<T>
abstract class BadExtension {
    var message: String = "Hello"  // Not lazy, not compatible with config cache
    var times: Int = 1              // Cannot be wired to providers
}

// Problem: Breaks configuration cache, not lazy, no provider wiring

// GOOD: Always use Property<T>
abstract class GoodExtension {
    abstract val message: Property<String>
    abstract val times: Property<Int>
}

// BAD: Eager evaluation in extension
class BadPlugin : Plugin<Project> {
    override fun apply(project: Project) {
        val extension = project.extensions.create("bad", BadExtension::class.java)

        // Evaluates immediately during configuration!
        val msg = extension.message.get()  // BAD: Too early

        project.tasks.register("bad") {
            doLast { println(msg) }  // Value captured at configuration time
        }
    }
}

// GOOD: Lazy evaluation with providers
class GoodPlugin : Plugin<Project> {
    override fun apply(project: Project) {
        val extension = project.extensions.create("good", GoodExtension::class.java)

        project.tasks.register("good") {
            doLast {
                // Evaluated at execution time
                println(extension.message.get())
            }
        }
    }
}

// BAD: No default values
abstract class ExtensionWithoutDefaults {
    abstract val required: Property<String>
    // User MUST set this or build fails - poor UX
}

// GOOD: Provide sensible defaults
abstract class ExtensionWithDefaults {
    abstract val optional: Property<String>

    init {
        optional.convention("sensible-default")  // User can override if needed
    }
}
```

#### Extension with Nested Configuration

```kotlin
// Nested extension for database configuration
abstract class DatabaseExtension {
    abstract val host: Property<String>
    abstract val port: Property<Int>
    abstract val username: Property<String>
    abstract val password: Property<String>
}

// Main extension
abstract class AppExtension(objects: ObjectFactory) {
    // Simple properties
    abstract val appName: Property<String>
    abstract val version: Property<String>

    // Nested object (always created)
    val database: DatabaseExtension = objects.newInstance(DatabaseExtension::class.java)

    // Configure nested object with DSL
    fun database(action: Action<DatabaseExtension>) {
        action.execute(database)
    }

    init {
        appName.convention("MyApp")
        version.convention("1.0.0")
        database.port.convention(5432)
    }
}

// Usage in build.gradle.kts
app {
    appName = "CoolApp"
    version = "2.0.0"

    database {
        host = "localhost"
        port = 5432
        username = "admin"
        password = providers.gradleProperty("db.password").orElse("default")
    }
}
```

#### Extension with Named Domain Objects

For collections of similar configurations:

```kotlin
import org.gradle.api.NamedDomainObjectContainer

// Define a server configuration
abstract class ServerConfig(val name: String) {
    abstract val host: Property<String>
    abstract val port: Property<Int>

    init {
        port.convention(8080)
    }
}

// Extension with container
abstract class DeploymentExtension(objects: ObjectFactory) {
    // Container of servers
    val servers: NamedDomainObjectContainer<ServerConfig> =
        objects.domainObjectContainer(ServerConfig::class.java)

    // DSL method for configuring servers
    fun servers(action: Action<NamedDomainObjectContainer<ServerConfig>>) {
        action.execute(servers)
    }
}

// Usage in build.gradle.kts
deployment {
    servers {
        create("production") {
            host = "prod.example.com"
            port = 443
        }

        create("staging") {
            host = "staging.example.com"
            port = 8080
        }
    }
}

// Access servers in task
tasks.register("deployToProduction") {
    doLast {
        val prodServer = extensions.getByType<DeploymentExtension>()
            .servers.getByName("production")
        println("Deploying to ${prodServer.host.get()}:${prodServer.port.get()}")
    }
}
```

#### Extension Best Practices

```kotlin
abstract class WellDesignedExtension @Inject constructor(
    private val objects: ObjectFactory,
    private val providers: ProviderFactory
) {
    // GOOD: Use Property<T> for mutable configuration
    abstract val apiKey: Property<String>

    // GOOD: Provide sensible defaults
    abstract val timeout: Property<Int>

    // GOOD: Use Provider for derived values
    val apiUrl: Provider<String> = apiKey.map { key ->
        "https://api.example.com?key=$key"
    }

    // GOOD: Validate in finalizer (not during configuration)
    init {
        timeout.convention(30)

        // Validation happens when value is accessed
        apiKey.finalizeValueOnRead()
    }

    // GOOD: Provide configuration methods with clear names
    fun useDefaultCredentials() {
        apiKey.set(providers.environmentVariable("API_KEY"))
    }

    fun useCustomCredentials(key: String) {
        apiKey.set(key)
    }
}

// BAD: Using plain variables (not lazy)
// class BadExtension {
//     var apiKey: String = ""  // Not lazy, no defaults, no validation
// }
```

#### Connecting Extension to Tasks

```kotlin
abstract class PublishExtension {
    abstract val version: Property<String>
    abstract val repository: Property<String>

    init {
        version.convention("1.0.0")
        repository.convention("https://repo.example.com")
    }
}

class PublishPlugin : Plugin<Project> {
    override fun apply(project: Project) {
        val extension = project.extensions.create("publish", PublishExtension::class.java)

        project.tasks.register<PublishTask>("publish") {
            // GOOD: Wire extension properties to task properties
            version.set(extension.version)
            repository.set(extension.repository)
        }
    }
}

abstract class PublishTask : DefaultTask() {
    @get:Input
    abstract val version: Property<String>

    @get:Input
    abstract val repository: Property<String>

    @TaskAction
    fun publish() {
        println("Publishing version ${version.get()} to ${repository.get()}")
    }
}
```

### Providers API

The Providers API enables lazy configuration, which is essential for configuration cache and fast builds.

#### Provider<T> Basics

```kotlin
// GOOD: Provider wraps a value that's computed lazily
val messageProvider: Provider<String> = providers.provider {
    "Message computed at ${System.currentTimeMillis()}"
}

// Value is only computed when accessed
tasks.register("printMessage") {
    doLast {
        println(messageProvider.get())  // Computed here
    }
}

// GOOD: Provider from environment variable
val apiKeyProvider: Provider<String> = providers.environmentVariable("API_KEY")

// GOOD: Provider from system property
val debugProvider: Provider<String> = providers.systemProperty("debug")

// GOOD: Provider from gradle property
val versionProvider: Provider<String> = providers.gradleProperty("app.version")
```

#### Property<T> for Mutable Values

```kotlin
abstract class ConfigurableTask : DefaultTask() {
    // GOOD: Property<T> for task inputs (can be set and connected)
    @get:Input
    abstract val message: Property<String>

    @get:Input
    abstract val count: Property<Int>

    init {
        // Set default values
        message.convention("Default message")
        count.convention(1)
    }

    @TaskAction
    fun execute() {
        repeat(count.get()) {
            println(message.get())
        }
    }
}

// Configure task
tasks.register<ConfigurableTask>("configurable") {
    message.set("Hello from property")
    count.set(5)
}
```

#### Transforming Providers

```kotlin
// GOOD: map - transform provider value
val version: Provider<String> = providers.gradleProperty("version")
val fullVersion: Provider<String> = version.map { v ->
    "v$v-${System.currentTimeMillis()}"
}

// GOOD: flatMap - chain providers
val baseUrl: Provider<String> = providers.gradleProperty("baseUrl")
val apiUrl: Provider<String> = baseUrl.flatMap { base ->
    providers.provider { "$base/api/v1" }
}

// GOOD: orElse - provide fallback
val timeout: Provider<Int> = providers.gradleProperty("timeout")
    .map { it.toInt() }
    .orElse(30)

// GOOD: zip - combine two providers
val host: Provider<String> = providers.gradleProperty("host")
val port: Provider<Int> = providers.gradleProperty("port").map { it.toInt() }

val endpoint: Provider<String> = host.zip(port) { h, p ->
    "$h:$p"
}
```

#### Connecting Providers

```kotlin
abstract class SourceTask : DefaultTask() {
    @get:Input
    abstract val sourceMessage: Property<String>

    init {
        sourceMessage.convention("Source data")
    }

    @TaskAction
    fun execute() {
        println("Source: ${sourceMessage.get()}")
    }
}

abstract class TargetTask : DefaultTask() {
    @get:Input
    abstract val targetMessage: Property<String>

    @TaskAction
    fun execute() {
        println("Target: ${targetMessage.get()}")
    }
}

// GOOD: Connect provider from one task to another
val sourceTask = tasks.register<SourceTask>("source")

tasks.register<TargetTask>("target") {
    // Wire output from source to input of target
    targetMessage.set(sourceTask.flatMap { it.sourceMessage })
}
```

#### File and Directory Providers

```kotlin
abstract class FileTask : DefaultTask() {
    // GOOD: Use RegularFileProperty for files
    @get:OutputFile
    abstract val outputFile: RegularFileProperty

    // GOOD: Use DirectoryProperty for directories
    @get:OutputDirectory
    abstract val outputDir: DirectoryProperty

    @TaskAction
    fun execute() {
        // Get file and directory
        val file = outputFile.get().asFile
        val dir = outputDir.get().asFile

        file.writeText("Output content")
        println("Wrote to ${file.absolutePath}")
    }
}

tasks.register<FileTask>("fileTask") {
    // GOOD: Use layout.buildDirectory for build outputs
    outputFile.set(layout.buildDirectory.file("output.txt"))
    outputDir.set(layout.buildDirectory.dir("outputs"))
}

// GOOD: Map file providers
tasks.register("processFile") {
    val inputProvider: Provider<RegularFile> = layout.buildDirectory.file("input.txt")
    val outputProvider: Provider<RegularFile> = inputProvider.map { input ->
        layout.buildDirectory.file("processed-${input.asFile.name}").get()
    }
}
```

#### Collection Providers

```kotlin
abstract class CollectionTask : DefaultTask() {
    // GOOD: ListProperty for list of values
    @get:Input
    abstract val items: ListProperty<String>

    // GOOD: SetProperty for unique values
    @get:Input
    abstract val tags: SetProperty<String>

    // GOOD: MapProperty for key-value pairs
    @get:Input
    abstract val config: MapProperty<String, String>

    @TaskAction
    fun execute() {
        println("Items: ${items.get()}")
        println("Tags: ${tags.get()}")
        println("Config: ${config.get()}")
    }
}

tasks.register<CollectionTask>("collections") {
    // Set collections
    items.set(listOf("a", "b", "c"))
    items.add("d")  // Add single item

    tags.set(setOf("gradle", "kotlin"))
    tags.add("build")

    config.set(mapOf("env" to "prod", "region" to "us"))
    config.put("version", "1.0")
}
```

#### Common Anti-Patterns to Avoid

```kotlin
// BAD: Eager evaluation during configuration
// val version = project.findProperty("version") as String  // Evaluated immediately

// GOOD: Lazy evaluation with provider
val version: Provider<String> = providers.gradleProperty("version")

// BAD: Calling .get() during configuration phase
// tasks.register("bad") {
//     val msg = messageProvider.get()  // Forces evaluation too early
//     doLast { println(msg) }
// }

// GOOD: Call .get() only in task action
tasks.register("good") {
    doLast {
        println(messageProvider.get())  // Evaluated at execution time
    }
}

// BAD: Using plain variables in task configuration
// var myVar = "value"
// tasks.register("bad") {
//     doLast { println(myVar) }  // Captures current value, not lazy
// }

// GOOD: Using properties
abstract class GoodTask : DefaultTask() {
    @get:Input
    abstract val myProperty: Property<String>

    @TaskAction
    fun execute() {
        println(myProperty.get())  // Lazy, cached, compatible with config cache
    }
}
```

#### Provider Best Practices

```kotlin
// GOOD: Use providers for external inputs
val externalConfig: Provider<String> = providers.fileContents(
    layout.projectDirectory.file("config.txt")
).asText

// GOOD: Finalize values to catch configuration errors early
val criticalValue: Property<String> = objects.property(String::class.java)
criticalValue.finalizeValueOnRead()  // Value can't change after first read

// GOOD: Use conventions for defaults
val timeout: Property<Int> = objects.property(Int::class.java)
timeout.convention(30)  // Default value if not set

// GOOD: Validate provider values
val port: Provider<Int> = providers.gradleProperty("port")
    .map { it.toInt() }
    .map { p ->
        require(p in 1..65535) { "Port must be between 1 and 65535" }
        p
    }

// GOOD: Use providers.provider for expensive computations
val expensiveValue: Provider<String> = providers.provider {
    // This expensive computation only runs when needed
    Thread.sleep(100)
    "Computed value"
}
```

### Gradle Caching

Caching is essential for fast Gradle builds. There are two types of caching: **build cache** (task outputs) and **configuration cache** (build configuration).

#### Build Cache Basics

The build cache stores task outputs and reuses them when inputs haven't changed.

**Enable build cache (gradle.properties):**
```properties
org.gradle.caching=true
```

**Or via command line:**
```bash
./gradlew build --build-cache
```

**How it works:**
1. Gradle calculates cache key from task inputs
2. If cache hit: Reuses outputs, task shows "FROM-CACHE"
3. If cache miss: Executes task, stores outputs

#### Writing Cache-Compatible Tasks

```kotlin
import org.gradle.api.DefaultTask
import org.gradle.api.file.ConfigurableFileCollection
import org.gradle.api.file.DirectoryProperty
import org.gradle.api.provider.Property
import org.gradle.api.tasks.*

// GOOD: Cache-compatible task with proper annotations
@CacheableTask  // Mark class as cacheable (must import org.gradle.api.tasks.CacheableTask)
abstract class CacheableProcessTask : DefaultTask() {

    @get:InputFiles
    @get:PathSensitive(PathSensitivity.RELATIVE)
    abstract val inputFiles: ConfigurableFileCollection

    @get:Input
    abstract val processMode: Property<String>

    @get:OutputDirectory
    abstract val outputDir: DirectoryProperty

    @TaskAction
    fun process() {
        val output = outputDir.get().asFile
        output.mkdirs()

        inputFiles.forEach { file ->
            val processed = output.resolve(file.name)
            when (processMode.get()) {
                "uppercase" -> processed.writeText(file.readText().uppercase())
                "lowercase" -> processed.writeText(file.readText().lowercase())
            }
        }
    }
}

// BAD: Task that's not cacheable (no @CacheableTask, uses external state)
abstract class BadTask : DefaultTask() {
    @TaskAction
    fun execute() {
        val timestamp = System.currentTimeMillis()  // Non-deterministic!
        File("output.txt").writeText("Built at $timestamp")
    }
}
```

#### What Makes Tasks Cacheable

✅ **GOOD - Cacheable:**
- Deterministic outputs (same inputs → same outputs)
- All inputs properly annotated (@InputFiles, @Input, etc.)
- No external state (environment, timestamps, random)
- Uses Provider API for configuration
- Marked with @CacheableTask at class level
- Uses @PathSensitive for file inputs

❌ **BAD - Not Cacheable:**
- Non-deterministic (timestamps, random values, System.currentTimeMillis())
- Missing input/output annotations
- Depends on external state not declared as inputs
- Modifies state outside task outputs
- No @CacheableTask annotation at class level

#### Making Built-in Tasks Cacheable

```kotlin
// GOOD: Configure tasks to be cacheable
tasks.withType<Test>().configureEach {
    outputs.cacheIf { true }  // Enable caching for tests
}

// GOOD: Normalize file paths for cache portability
normalization {
    runtimeClasspath {
        ignore("META-INF/MANIFEST.MF")  // Ignore non-functional differences
    }
}
```

#### Configuration Cache

Configuration cache stores the configured task graph, eliminating configuration phase on subsequent builds.

**Enable configuration cache (gradle.properties):**
```properties
org.gradle.configuration-cache=true
org.gradle.configuration-cache.problems=warn  # Or 'fail'
```

**Or via command line:**
```bash
./gradlew build --configuration-cache
```

**Benefits:**
- Up to 90% faster builds (no configuration phase)
- Second build reuses cached configuration
- Encourages better build practices

#### Configuration Cache Compatibility

```kotlin
// GOOD: Configuration cache compatible
tasks.register("compatible") {
    val message: Provider<String> = providers.gradleProperty("message")

    doLast {
        println(message.get())  // Lazy evaluation
    }
}

// BAD: Not configuration cache compatible
// tasks.register("incompatible") {
//     val message = project.findProperty("message")  // Eager evaluation
//     doLast {
//         println(message)  // Captures project state at configuration time
//     }
// }

// GOOD: Use build services for shared state
interface MyBuildService : BuildService<BuildServiceParameters.None> {
    fun performWork() {
        println("Build service performing work")
    }
}

abstract class SharedStateTask : DefaultTask() {
    @get:Internal  // Build services are not inputs
    abstract val myService: Property<MyBuildService>

    @TaskAction
    fun execute() {
        myService.get().performWork()
    }
}

// Register the build service
val myServiceProvider = gradle.sharedServices.registerIfAbsent("myService", MyBuildService::class) {
    // Configure service parameters here if needed
}

// Wire service to task
tasks.register<SharedStateTask>("taskWithService") {
    myService.set(myServiceProvider)
}

// BAD: Using static/global state instead of build services
object BadSharedState {
    var counter = 0  // Mutable global state - not serializable!
}

// Problem: Breaks configuration cache, not thread-safe, not isolated

// BAD: Trying to share data via files without proper task dependencies
tasks.register("badProducer") {
    doLast {
        File("shared.txt").writeText("data")  // No output annotation!
    }
}

tasks.register("badConsumer") {
    doLast {
        val data = File("shared.txt").readText()  // No input annotation!
        println(data)
    }
}
// Problem: No dependency declared, may run in wrong order or break caching

// GOOD: Use task outputs/inputs or build services for shared state
```

#### Common Configuration Cache Issues

```kotlin
// PROBLEM: Accessing project at execution time
// tasks.register("bad") {
//     doLast {
//         println(project.name)  // Configuration cache error!
//     }
// }

// SOLUTION: Capture value during configuration
tasks.register("good") {
    val projectName = project.name  // Captured during configuration

    doLast {
        println(projectName)  // OK - uses captured value
    }
}

// PROBLEM: Using mutable shared state
// val sharedList = mutableListOf<String>()
// tasks.register("bad") {
//     doLast {
//         sharedList.add("item")  // Not serializable!
//     }
// }

// SOLUTION: Use build services or task outputs
abstract class GoodTask : DefaultTask() {
    @get:OutputFile
    abstract val outputFile: RegularFileProperty

    @TaskAction
    fun execute() {
        outputFile.get().asFile.appendText("item\n")
    }
}
```

#### Cache Debugging

```bash
# Check what's not cacheable
./gradlew build --build-cache --info | grep "Caching disabled"

# Explain why task wasn't cached
./gradlew help --task processFiles

# Clear build cache
rm -rf ~/.gradle/caches/build-cache-*
rm -rf .gradle/build-cache

# Check configuration cache problems
./gradlew build --configuration-cache --configuration-cache-problems=warn

# Rerun without cache to compare
./gradlew clean build --no-build-cache --no-configuration-cache
./gradlew clean build --build-cache --configuration-cache
```

#### Remote Build Cache

```kotlin
// settings.gradle.kts
buildCache {
    local {
        isEnabled = true
    }

    remote<HttpBuildCache> {
        url = uri("https://cache.example.com/")
        isPush = providers.environmentVariable("CI")
            .map { it == "true" }
            .getOrElse(false)

        credentials {
            username = providers.environmentVariable("CACHE_USER").orNull
            password = providers.environmentVariable("CACHE_PASSWORD").orNull
        }
    }
}

// Benefits:
// - Share cache across CI and developers
// - Dramatically faster CI builds
// - Consistent build performance
```

#### Cache Performance Tips

```kotlin
// GOOD: Use relative path sensitivity when possible
abstract class OptimizedTask : DefaultTask() {
    @get:InputFiles
    @get:PathSensitive(PathSensitivity.RELATIVE)  // Better cache hits
    abstract val sources: ConfigurableFileCollection
}

// GOOD: Exclude non-functional files
normalization {
    runtimeClasspath {
        ignore("**/*.txt")  // If .txt files don't affect behavior
        ignore("META-INF/MANIFEST.MF")
    }
}

// GOOD: Use file collections instead of file trees for better caching
val sources: ConfigurableFileCollection = objects.fileCollection()
sources.from(fileTree("src") { include("**/*.java") })

// GOOD: Split large tasks into smaller cacheable units
tasks.register("compileAll") {
    dependsOn("compileModule1", "compileModule2", "compileModule3")
}
// Each module compiled separately = better cache granularity
```

#### Measuring Cache Effectiveness

```bash
# Build scan (best way to analyze caching)
./gradlew build --scan

# The build scan shows:
# - Cache hit rate
# - Which tasks were cached
# - Why tasks were not cached
# - Performance timeline

# Enable with:
# plugins {
#     id("com.gradle.develocity") version "3.16"
# }
#
# develocity {
#     buildScan {
#         publishing.onlyIf { true }
#     }
# }
```

### Custom Plugins

Custom plugins encapsulate build logic for reuse across projects or modules.

#### Binary Plugin (Plugin<Project>)

```kotlin
// buildSrc/src/main/kotlin/GreetingPlugin.kt
import org.gradle.api.Plugin
import org.gradle.api.Project

class GreetingPlugin : Plugin<Project> {
    override fun apply(project: Project) {
        // Create extension for configuration
        val extension = project.extensions.create(
            "greeting",
            GreetingExtension::class.java
        )

        // Register task that uses extension
        project.tasks.register("greet") {
            group = "custom"
            description = "Prints a greeting message"

            doLast {
                repeat(extension.times.get()) {
                    println(extension.message.get())
                }
            }
        }
    }
}

// Extension for configuration
abstract class GreetingExtension {
    abstract val message: Property<String>
    abstract val times: Property<Int>

    init {
        message.convention("Hello from plugin")
        times.convention(1)
    }
}

// buildSrc/src/main/resources/META-INF/gradle-plugins/greeting.properties
implementation-class=GreetingPlugin

// Usage in build.gradle.kts:
// plugins {
//     id("greeting")
// }
//
// greeting {
//     message = "Hello, World!"
//     times = 3
// }
```

#### Precompiled Script Plugin (Recommended for Simple Plugins)

Easier approach using Kotlin DSL directly:

```kotlin
// buildSrc/src/main/kotlin/java-library-conventions.gradle.kts
plugins {
    `java-library`
    `maven-publish`
}

java {
    toolchain {
        languageVersion = JavaLanguageVersion.of(21)
    }
    withSourcesJar()
    withJavadocJar()
}

repositories {
    mavenCentral()
}

dependencies {
    testImplementation("org.junit.jupiter:junit-jupiter:5.10.2")
    testRuntimeOnly("org.junit.platform:junit-platform-launcher")
}

tasks.test {
    useJUnitPlatform()
}

publishing {
    publications {
        create<MavenPublication>("maven") {
            from(components["java"])
        }
    }
}

// Usage in build.gradle.kts:
// plugins {
//     id("java-library-conventions")
// }
```

#### Complete Plugin Example

```kotlin
// buildSrc/src/main/kotlin/DocumentationPlugin.kt
import org.gradle.api.*
import org.gradle.api.file.DirectoryProperty
import org.gradle.api.provider.Property
import org.gradle.api.tasks.*

class DocumentationPlugin : Plugin<Project> {
    override fun apply(project: Project) {
        // Register extension
        val extension = project.extensions.create(
            "documentation",
            DocumentationExtension::class.java
        )

        // Configure defaults from extension
        extension.sourceDir.convention(
            project.layout.projectDirectory.dir("docs")
        )
        extension.outputDir.convention(
            project.layout.buildDirectory.dir("docs")
        )

        // Register task
        project.tasks.register<GenerateDocsTask>("generateDocs") {
            sourceDir.set(extension.sourceDir)
            outputDir.set(extension.outputDir)
            format.set(extension.format)

            group = "documentation"
            description = "Generates documentation"
        }

        // Hook into build lifecycle
        project.tasks.named("build") {
            dependsOn("generateDocs")
        }
    }
}

abstract class DocumentationExtension {
    abstract val sourceDir: DirectoryProperty
    abstract val outputDir: DirectoryProperty
    abstract val format: Property<String>

    init {
        format.convention("html")
    }
}

abstract class GenerateDocsTask : DefaultTask() {
    @get:InputDirectory
    @get:PathSensitive(PathSensitivity.RELATIVE)
    abstract val sourceDir: DirectoryProperty

    @get:OutputDirectory
    abstract val outputDir: DirectoryProperty

    @get:Input
    abstract val format: Property<String>

    @TaskAction
    fun generate() {
        val output = outputDir.get().asFile
        output.mkdirs()

        sourceDir.get().asFileTree.forEach { file ->
            val outputFile = output.resolve("${file.nameWithoutExtension}.${format.get()}")
            outputFile.writeText("Generated from ${file.name}")
        }

        logger.lifecycle("Generated documentation in ${output.absolutePath}")
    }
}
```

#### Plugin with Build Service

For shared state across tasks:

```kotlin
import org.gradle.api.services.BuildService
import org.gradle.api.services.BuildServiceParameters

abstract class MetricsService : BuildService<BuildServiceParameters.None> {
    private val metrics = mutableMapOf<String, Long>()

    fun record(metric: String, value: Long) {
        metrics[metric] = value
    }

    fun report() {
        println("Build Metrics:")
        metrics.forEach { (key, value) ->
            println("  $key: $value")
        }
    }
}

class MetricsPlugin : Plugin<Project> {
    override fun apply(project: Project) {
        // Register build service
        val metricsService = project.gradle.sharedServices.registerIfAbsent(
            "metrics",
            MetricsService::class.java
        ) {}

        // Use service in tasks
        project.tasks.register<MetricsTask>("recordMetrics") {
            this.metricsService.set(metricsService)
        }

        // Report at end of build
        project.gradle.buildFinished {
            metricsService.get().report()
        }
    }
}

abstract class MetricsTask : DefaultTask() {
    @get:ServiceReference("metrics")
    abstract val metricsService: Property<MetricsService>

    @TaskAction
    fun record() {
        metricsService.get().record("task_count", 42)
    }
}
```

#### Testing Custom Plugins

```kotlin
// buildSrc/src/test/kotlin/GreetingPluginTest.kt
import org.gradle.testfixtures.ProjectBuilder
import org.junit.jupiter.api.Test
import org.junit.jupiter.api.Assertions.*

class GreetingPluginTest {

    @Test
    fun `plugin registers greet task`() {
        val project = ProjectBuilder.builder().build()
        project.pluginManager.apply("greeting")

        val task = project.tasks.findByName("greet")
        assertNotNull(task)
    }

    @Test
    fun `extension has default values`() {
        val project = ProjectBuilder.builder().build()
        project.pluginManager.apply("greeting")

        val extension = project.extensions.getByType(GreetingExtension::class.java)
        assertEquals("Hello from plugin", extension.message.get())
        assertEquals(1, extension.times.get())
    }

    @Test
    fun `can configure extension`() {
        val project = ProjectBuilder.builder().build()
        project.pluginManager.apply("greeting")

        val extension = project.extensions.getByType(GreetingExtension::class.java)
        extension.message.set("Custom message")
        extension.times.set(5)

        assertEquals("Custom message", extension.message.get())
        assertEquals(5, extension.times.get())
    }
}
```

#### Publishing Plugins

```kotlin
// buildSrc/build.gradle.kts (for publishing to plugin portal)
plugins {
    `kotlin-dsl`
    `maven-publish`
    id("com.gradle.plugin-publish") version "1.2.1"
}

group = "com.example"
version = "1.0.0"

gradlePlugin {
    website = "https://github.com/example/plugin"
    vcsUrl = "https://github.com/example/plugin"

    plugins {
        create("greetingPlugin") {
            id = "com.example.greeting"
            displayName = "Greeting Plugin"
            description = "A plugin that greets users"
            tags = listOf("greeting", "example")
            implementationClass = "com.example.GreetingPlugin"
        }
    }
}

publishing {
    repositories {
        maven {
            name = "Internal"
            url = uri("https://repo.company.com/maven")
        }
    }
}

// Publish with: ./gradlew publishPlugins
```

#### Plugin Best Practices

```kotlin
class WellDesignedPlugin : Plugin<Project> {
    override fun apply(project: Project) {
        // GOOD: Validate environment
        require(project.hasProperty("requiredProp")) {
            "Plugin requires 'requiredProp' property"
        }

        // GOOD: Use lazy registration
        val extension = project.extensions.create("wellDesigned", Extension::class.java)

        // GOOD: Register tasks lazily
        project.tasks.register("myTask") {
            // Configure with extension
        }

        // GOOD: Apply other plugins if needed
        project.pluginManager.apply("java")

        // GOOD: Configure other plugins
        project.plugins.withType<JavaPlugin> {
            project.java {
                toolchain {
                    languageVersion.set(JavaLanguageVersion.of(21))
                }
            }
        }

        // GOOD: Hook into lifecycle cleanly
        project.afterEvaluate {
            // Configuration that needs evaluated project
        }
    }
}

// BAD: Applying plugins eagerly
// project.apply(plugin = "java")  // Use pluginManager.apply()

// BAD: Configuring in constructor
// class BadPlugin : Plugin<Project> {
//     init {
//         // Plugin not yet applied!
//     }
// }
```

### Build Logic Reuse

There are multiple strategies for sharing build logic across projects and modules.

#### Strategy 1: buildSrc (Simplest)

Best for: Single repository, convention plugins, shared code within one project.

```
project/
├── buildSrc/
│   ├── build.gradle.kts
│   ├── settings.gradle.kts
│   └── src/
│       └── main/kotlin/
│           ├── java-conventions.gradle.kts
│           ├── kotlin-conventions.gradle.kts
│           └── MyCustomPlugin.kt
├── app/
│   └── build.gradle.kts
└── lib/
    └── build.gradle.kts
```

**buildSrc/build.gradle.kts:**
```kotlin
plugins {
    `kotlin-dsl`
}

repositories {
    mavenCentral()
    gradlePluginPortal()
}

dependencies {
    // Add dependencies needed by your plugins
    implementation("com.github.johnrengelman:shadow:8.1.1")
}
```

**buildSrc/settings.gradle.kts:**
```kotlin
rootProject.name = "buildSrc"

dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.PREFER_SETTINGS)
    repositories {
        mavenCentral()
        gradlePluginPortal()
    }
}
```

**buildSrc/src/main/kotlin/java-conventions.gradle.kts:**
```kotlin
plugins {
    java
}

java {
    toolchain {
        languageVersion = JavaLanguageVersion.of(21)
    }
}

repositories {
    mavenCentral()
}

dependencies {
    testImplementation("org.junit.jupiter:junit-jupiter:5.10.2")
}

tasks.test {
    useJUnitPlatform()
}
```

**Usage in app/build.gradle.kts:**
```kotlin
plugins {
    id("java-conventions")  // Automatically available
    application
}
```

**Pros:**
- Simple setup
- Automatically available to all modules
- Fast incremental builds

**Cons:**
- Tied to single project
- Changes require Gradle daemon restart
- Can't be versioned separately

#### Strategy 2: Included Builds (Flexible)

Best for: Multi-repo setups, versioned build logic, independent releases.

```
company-builds/
├── my-project/
│   ├── settings.gradle.kts  (includes build-logic)
│   ├── app/
│   └── lib/
└── build-logic/
    ├── settings.gradle.kts
    ├── build.gradle.kts
    └── src/
        └── main/kotlin/
            └── conventions/
                ├── java-conventions.gradle.kts
                └── kotlin-conventions.gradle.kts
```

**my-project/settings.gradle.kts:**
```kotlin
rootProject.name = "my-project"

// Include build-logic
includeBuild("../build-logic")

include("app")
include("lib")
```

**build-logic/settings.gradle.kts:**
```kotlin
rootProject.name = "build-logic"

dependencyResolutionManagement {
    repositories {
        mavenCentral()
        gradlePluginPortal()
    }
}
```

**build-logic/build.gradle.kts:**
```kotlin
plugins {
    `kotlin-dsl`
}

group = "com.example.build"
version = "1.0.0"

dependencies {
    implementation("com.github.johnrengelman:shadow:8.1.1")
}

gradlePlugin {
    plugins {
        register("javaConventions") {
            id = "com.example.java-conventions"
            implementationClass = "conventions.JavaConventionsPlugin"
        }
    }
}
```

**Usage in my-project/app/build.gradle.kts:**
```kotlin
plugins {
    id("com.example.java-conventions")
}
```

**Pros:**
- Independent versioning
- No daemon restart needed
- Shareable across projects
- Can be published

**Cons:**
- More complex setup
- Need to manage versions

#### Strategy 3: Published Plugins (Enterprise)

Best for: Many projects, organization-wide standards, versioned releases.

**Plugin Project Structure:**
```
gradle-plugins/
├── settings.gradle.kts
├── build.gradle.kts
└── src/
    └── main/
        ├── kotlin/
        │   └── com/example/plugins/
        │       └── JavaConventionsPlugin.kt
        └── resources/
            └── META-INF/gradle-plugins/
                └── com.example.java-conventions.properties
```

**build.gradle.kts:**
```kotlin
plugins {
    `kotlin-dsl`
    `maven-publish`
}

group = "com.example.gradle"
version = "1.0.0"

java {
    toolchain {
        languageVersion = JavaLanguageVersion.of(11)  // Wide compatibility
    }
}

publishing {
    repositories {
        maven {
            name = "Company"
            url = uri("https://repo.company.com/maven")
            credentials {
                username = System.getenv("REPO_USER")
                password = System.getenv("REPO_PASSWORD")
            }
        }
    }

    publications {
        create<MavenPublication>("plugin") {
            from(components["java"])
        }
    }
}
```

**Consumer settings.gradle.kts:**
```kotlin
pluginManagement {
    repositories {
        maven {
            url = uri("https://repo.company.com/maven")
        }
        gradlePluginPortal()
    }
}
```

**Consumer build.gradle.kts:**
```kotlin
plugins {
    id("com.example.java-conventions") version "1.0.0"
}
```

**Pros:**
- Enterprise-grade
- Versioned releases
- Change management
- Works across all projects

**Cons:**
- Most complex
- Release overhead
- Version management needed

#### Strategy 4: Composite Builds (Advanced)

Best for: Multiple independent projects that need to work together.

```
workspace/
├── project-a/
│   ├── settings.gradle.kts
│   └── build.gradle.kts
├── project-b/
│   ├── settings.gradle.kts
│   └── build.gradle.kts
└── shared-library/
    ├── settings.gradle.kts
    └── build.gradle.kts
```

**project-a/settings.gradle.kts:**
```kotlin
rootProject.name = "project-a"

// Include other project as composite build
includeBuild("../shared-library")
```

**project-a/build.gradle.kts:**
```kotlin
dependencies {
    // Depend on shared library
    implementation("com.example:shared-library:1.0.0")
    // Gradle substitutes with composite build automatically
}
```

**Pros:**
- Independent projects
- Source dependencies
- IDE integration
- Parallel development

**Cons:**
- Complex setup
- Dependency substitution rules needed

#### Choosing the Right Strategy

| Scenario | Recommended Strategy |
|----------|---------------------|
| Single repo, simple conventions | buildSrc |
| Multi-repo, same org | Included builds |
| Organization-wide standards | Published plugins |
| Multiple independent projects | Composite builds |
| Experimenting with new patterns | buildSrc → Included builds |

#### Convention Plugin Patterns

**Important:** Precompiled script plugins in buildSrc automatically get plugin IDs based on their file path. A file at `buildSrc/src/main/kotlin/conventions/java-base.gradle.kts` becomes plugin `id("conventions.java-base")`.

```kotlin
// Pattern 1: Pure configuration plugin
// Location: buildSrc/src/main/kotlin/conventions/java-base.gradle.kts
// Plugin ID: conventions.java-base (auto-generated from file path)
plugins {
    java
}

java {
    toolchain.languageVersion = JavaLanguageVersion.of(21)
}

// Pattern 2: Conditional configuration
// Location: buildSrc/src/main/kotlin/conventions/java-app.gradle.kts
// Plugin ID: conventions.java-app
plugins {
    id("conventions.java-base")  // References Pattern 1 by its auto-generated ID
    application
}

if (project.hasProperty("enableJacoco")) {
    apply(plugin = "jacoco")
}

// Pattern 3: Composed plugins
// conventions/java-library.gradle.kts
plugins {
    id("conventions.java-base")
    `java-library`
    `maven-publish`
}

publishing {
    publications {
        create<MavenPublication>("maven") {
            from(components["java"])
        }
    }
}
```

#### Sharing Configuration Files

```kotlin
// buildSrc/src/main/resources/checkstyle.xml
// buildSrc/src/main/kotlin/conventions.gradle.kts

plugins {
    checkstyle
}

checkstyle {
    configFile = file("${project.rootDir}/buildSrc/src/main/resources/checkstyle.xml")
    toolVersion = "10.12.5"
}

// All modules get consistent checkstyle configuration
```

#### Version Management for Shared Logic

```kotlin
// build-logic/build.gradle.kts
version = "1.2.0"  // Increment when making changes

// Consumers can pin versions
// settings.gradle.kts
pluginManagement {
    resolutionStrategy {
        eachPlugin {
            if (requested.id.id == "com.example.conventions") {
                useVersion("1.2.0")
            }
        }
    }
}
```

---

## Groovy → Kotlin DSL Migration Guide

This section helps developers migrate existing Groovy DSL build scripts to Kotlin DSL.

### Syntax Differences

This section provides side-by-side comparisons of common syntax patterns.

#### Basic Syntax Table

| Feature | Groovy DSL | Kotlin DSL |
|---------|------------|------------|
| **File name** | `build.gradle` | `build.gradle.kts` |
| **Settings file** | `settings.gradle` | `settings.gradle.kts` |
| **Assignment** | `version = '1.0'` | `version = "1.0"` |
| **String literals** | `'single'` or `"double"` | `"double"` only |
| **String interpolation** | `"Version $version"` | `"Version $version"` |
| **Method calls** | `implementation 'lib'` | `implementation("lib")` |
| **Configuration blocks** | `java { ... }` | `java { ... }` |
| **Task configuration** | `task myTask { ... }` | `tasks.register("myTask") { ... }` |

#### Assignment and Properties

**Groovy:**
```groovy
version = '1.0.0'
group = 'com.example'

ext.customProp = 'value'
ext {
    anotherProp = 'value'
}
```

**Kotlin:**
```kotlin
version = "1.0.0"
group = "com.example"

extra["customProp"] = "value"
// Or with type-safe accessor
val customProp by extra("value")
```

#### String Literals

**Groovy:**
```groovy
// Both work in Groovy
implementation 'com.google.guava:guava:33.0.0-jre'
implementation "com.google.guava:guava:33.0.0-jre"

// String interpolation
def myVersion = '1.0'
println "Version: $myVersion"
```

**Kotlin:**
```kotlin
// Only double quotes work in Kotlin
implementation("com.google.guava:guava:33.0.0-jre")

// String interpolation (same as Groovy)
val myVersion = "1.0"
println("Version: $myVersion")
```

#### Method Call Syntax

**Groovy (implicit parentheses):**
```groovy
// Groovy allows omitting parentheses
implementation 'com.google.guava:guava:33.0.0-jre'
testImplementation 'org.junit.jupiter:junit-jupiter:5.10.2'

// Configuration blocks
repositories {
    mavenCentral()
}
```

**Kotlin (explicit parentheses):**
```kotlin
// Kotlin requires parentheses for method calls
implementation("com.google.guava:guava:33.0.0-jre")
testImplementation("org.junit.jupiter:junit-jupiter:5.10.2")

// Configuration blocks (same)
repositories {
    mavenCentral()
}
```

#### Property Access vs Method Calls

**Groovy:**
```groovy
// Groovy uses property syntax for getters/setters
java {
    sourceCompatibility = JavaVersion.VERSION_21
    targetCompatibility = JavaVersion.VERSION_21
}

tasks.test {
    maxParallelForks = 4
}
```

**Kotlin:**
```kotlin
// Kotlin also uses property syntax
java {
    sourceCompatibility = JavaVersion.VERSION_21
    targetCompatibility = JavaVersion.VERSION_21
}

tasks.named<Test>("test") {
    maxParallelForks = 4
}
```

#### Collection Literals

**Groovy:**
```groovy
// List
def myList = ['item1', 'item2', 'item3']

// Map
def myMap = [key1: 'value1', key2: 'value2']
```

**Kotlin:**
```kotlin
// List
val myList = listOf("item1", "item2", "item3")

// Map
val myMap = mapOf("key1" to "value1", "key2" to "value2")
```

#### Configuration Delegation

**Groovy (implicit delegate):**
```groovy
tasks.create('myTask') {
    // 'doLast' resolves through task delegate
    doLast {
        println 'Task executed'
    }
}
```

**Kotlin (explicit receiver):**
```kotlin
tasks.register("myTask") {
    // 'this' refers to the task
    doLast {
        println("Task executed")
    }
}
```

### Plugin Application Conversion

#### Old apply Syntax to plugins Block

**Groovy (old style):**
```groovy
apply plugin: 'java'
apply plugin: 'application'
apply plugin: 'com.github.johnrengelman.shadow'

buildscript {
    repositories {
        gradlePluginPortal()
    }
    dependencies {
        classpath 'com.github.johnrengelman:shadow:8.1.1'
    }
}
```

**Kotlin (modern style):**
```kotlin
plugins {
    java
    application
    id("com.github.johnrengelman.shadow") version "8.1.1"
}

// No buildscript block needed for plugins from Gradle Plugin Portal
```

#### Core Plugins

**Groovy:**
```groovy
apply plugin: 'java'
apply plugin: 'java-library'
apply plugin: 'application'
apply plugin: 'groovy'
```

**Kotlin:**
```kotlin
plugins {
    java
    `java-library`  // Note backticks for kebab-case
    application
    groovy
}
```

#### Kotlin Plugins

**Groovy:**
```groovy
apply plugin: 'org.jetbrains.kotlin.jvm'

buildscript {
    dependencies {
        classpath 'org.jetbrains.kotlin:kotlin-gradle-plugin:2.0.0'
    }
}
```

**Kotlin:**
```kotlin
plugins {
    kotlin("jvm") version "2.0.0"
    // Short form for Kotlin plugins
    // Alternative: id("org.jetbrains.kotlin.jvm") version "2.0.0"
}
```

#### Applying Plugins Conditionally

**Groovy:**
```groovy
if (project.hasProperty('enableKotlin')) {
    apply plugin: 'org.jetbrains.kotlin.jvm'
}
```

**Kotlin:**
```kotlin
plugins {
    java
    if (project.hasProperty("enableKotlin")) {
        kotlin("jvm") version "2.0.0"
    }
}

// Alternative: Apply outside plugins block
if (project.findProperty("enableKotlin") == "true") {
    apply(plugin = "org.jetbrains.kotlin.jvm")
}
```

#### apply false for Root Projects

**Groovy:**
```groovy
plugins {
    id 'org.springframework.boot' version '3.2.0' apply false
}
```

**Kotlin:**
```kotlin
plugins {
    id("org.springframework.boot") version "3.2.0" apply false
}
```

### Dependency Declaration Differences

#### Basic Dependency Notation

**Groovy:**
```groovy
dependencies {
    implementation 'com.google.guava:guava:33.0.0-jre'
    testImplementation 'org.junit.jupiter:junit-jupiter:5.10.2'
    compileOnly 'org.projectlombok:lombok:1.18.30'
    runtimeOnly 'com.h2database:h2:2.2.224'
}
```

**Kotlin:**
```kotlin
dependencies {
    implementation("com.google.guava:guava:33.0.0-jre")
    testImplementation("org.junit.jupiter:junit-jupiter:5.10.2")
    compileOnly("org.projectlombok:lombok:1.18.30")
    runtimeOnly("com.h2database:h2:2.2.224")
}
```

#### Map Notation

**Groovy:**
```groovy
dependencies {
    implementation group: 'com.google.guava', name: 'guava', version: '33.0.0-jre'
    implementation([group: 'com.google.guava', name: 'guava', version: '33.0.0-jre'])
}
```

**Kotlin:**
```kotlin
dependencies {
    implementation(group = "com.google.guava", name = "guava", version = "33.0.0-jre")
    // Or stick with string notation (more common)
    implementation("com.google.guava:guava:33.0.0-jre")
}
```

#### Excluding Dependencies

**Groovy:**
```groovy
dependencies {
    implementation('com.example:library:1.0') {
        exclude group: 'commons-logging', module: 'commons-logging'
    }
}
```

**Kotlin:**
```kotlin
dependencies {
    implementation("com.example:library:1.0") {
        exclude(group = "commons-logging", module = "commons-logging")
    }
}
```

#### Platform/BOM Dependencies

**Groovy:**
```groovy
dependencies {
    implementation platform('org.springframework.boot:spring-boot-dependencies:3.2.0')
    implementation 'org.springframework.boot:spring-boot-starter-web'
}
```

**Kotlin:**
```kotlin
dependencies {
    implementation(platform("org.springframework.boot:spring-boot-dependencies:3.2.0"))
    implementation("org.springframework.boot:spring-boot-starter-web")
}
```

#### Project Dependencies

**Groovy:**
```groovy
dependencies {
    implementation project(':common')
    implementation project(path: ':lib', configuration: 'testFixtures')
}
```

**Kotlin:**
```kotlin
dependencies {
    implementation(project(":common"))
    implementation(project(path = ":lib", configuration = "testFixtures"))

    // With type-safe accessors (requires TYPESAFE_PROJECT_ACCESSORS)
    implementation(projects.common)
}
```

#### File Dependencies

**Groovy:**
```groovy
dependencies {
    implementation files('libs/custom.jar')
    implementation fileTree(dir: 'libs', include: '*.jar')
}
```

**Kotlin:**
```kotlin
dependencies {
    implementation(files("libs/custom.jar"))
    implementation(fileTree("libs") { include("*.jar") })
}
```

#### Configuration-Specific Dependencies

**Groovy:**
```groovy
configurations {
    integrationTestImplementation.extendsFrom testImplementation
    integrationTestRuntimeOnly.extendsFrom testRuntimeOnly
}

dependencies {
    integrationTestImplementation 'org.testcontainers:junit-jupiter:1.19.3'
}
```

**Kotlin:**
```kotlin
val integrationTestImplementation by configurations.creating {
    extendsFrom(configurations.testImplementation.get())
}

val integrationTestRuntimeOnly by configurations.creating {
    extendsFrom(configurations.testRuntimeOnly.get())
}

dependencies {
    integrationTestImplementation("org.testcontainers:junit-jupiter:1.19.3")
}
```

### Configuration Block Conversions

#### allprojects and subprojects

**Groovy:**
```groovy
allprojects {
    group = 'com.example'
    version = '1.0.0'

    repositories {
        mavenCentral()
    }
}

subprojects {
    apply plugin: 'java'

    dependencies {
        testImplementation 'org.junit.jupiter:junit-jupiter:5.10.2'
    }
}
```

**Kotlin:**
```kotlin
allprojects {
    group = "com.example"
    version = "1.0.0"

    repositories {
        mavenCentral()
    }
}

subprojects {
    apply(plugin = "java")

    dependencies {
        testImplementation("org.junit.jupiter:junit-jupiter:5.10.2")
    }
}
```

#### buildscript Block (Avoid in Modern Gradle)

**Groovy:**
```groovy
buildscript {
    repositories {
        gradlePluginPortal()
        mavenCentral()
    }

    dependencies {
        classpath 'org.jetbrains.kotlin:kotlin-gradle-plugin:2.0.0'
    }
}
```

**Kotlin (old way):**
```kotlin
buildscript {
    repositories {
        gradlePluginPortal()
        mavenCentral()
    }

    dependencies {
        classpath("org.jetbrains.kotlin:kotlin-gradle-plugin:2.0.0")
    }
}
```

**Kotlin (modern way - use plugins block instead):**
```kotlin
plugins {
    kotlin("jvm") version "2.0.0"
}
// No buildscript needed!
```

#### Task Configuration

**Groovy:**
```groovy
task myTask {
    doLast {
        println 'Task executed'
    }
}

tasks.withType(Test) {
    useJUnitPlatform()
}

tasks.named('build') {
    dependsOn 'myTask'
}
```

**Kotlin:**
```kotlin
tasks.register("myTask") {
    doLast {
        println("Task executed")
    }
}

tasks.withType<Test> {
    useJUnitPlatform()
}

tasks.named("build") {
    dependsOn("myTask")
}
```

#### Java Configuration

**Groovy:**
```groovy
java {
    sourceCompatibility = JavaVersion.VERSION_21
    targetCompatibility = JavaVersion.VERSION_21

    withSourcesJar()
    withJavadocJar()
}

compileJava {
    options.encoding = 'UTF-8'
}
```

**Kotlin:**
```kotlin
java {
    sourceCompatibility = JavaVersion.VERSION_21
    targetCompatibility = JavaVersion.VERSION_21

    withSourcesJar()
    withJavadocJar()
}

tasks.named<JavaCompile>("compileJava") {
    options.encoding = "UTF-8"
}
```

#### Publishing Configuration

**Groovy:**
```groovy
publishing {
    publications {
        maven(MavenPublication) {
            from components.java

            groupId = 'com.example'
            artifactId = 'my-library'
            version = '1.0.0'
        }
    }

    repositories {
        maven {
            url = 'https://repo.example.com/maven'
            credentials {
                username = project.findProperty('repoUser')
                password = project.findProperty('repoPassword')
            }
        }
    }
}
```

**Kotlin:**
```kotlin
publishing {
    publications {
        create<MavenPublication>("maven") {
            from(components["java"])

            groupId = "com.example"
            artifactId = "my-library"
            version = "1.0.0"
        }
    }

    repositories {
        maven {
            url = uri("https://repo.example.com/maven")
            credentials {
                username = providers.gradleProperty("repoUser").orNull
                password = providers.gradleProperty("repoPassword").orNull
            }
        }
    }
}
```

#### Testing Configuration

**Groovy:**
```groovy
test {
    useJUnitPlatform()

    testLogging {
        events 'passed', 'skipped', 'failed'
        exceptionFormat 'full'
    }

    maxParallelForks = Runtime.runtime.availableProcessors()
}
```

**Kotlin:**
```kotlin
tasks.named<Test>("test") {
    useJUnitPlatform()

    testLogging {
        events("passed", "skipped", "failed")
        exceptionFormat = org.gradle.api.tasks.testing.logging.TestExceptionFormat.FULL
    }

    maxParallelForks = Runtime.getRuntime().availableProcessors()
}
```

#### Extra Properties

**Groovy:**
```groovy
ext {
    springBootVersion = '3.2.0'
    junitVersion = '5.10.2'
}

ext.kotlinVersion = '2.0.0'

dependencies {
    implementation "org.springframework.boot:spring-boot-starter-web:$springBootVersion"
    testImplementation "org.junit.jupiter:junit-jupiter:$junitVersion"
}
```

**Kotlin:**
```kotlin
// Option 1: Using extra properties
extra["springBootVersion"] = "3.2.0"
extra["junitVersion"] = "5.10.2"

dependencies {
    implementation("org.springframework.boot:spring-boot-starter-web:${extra["springBootVersion"]}")
    testImplementation("org.junit.jupiter:junit-jupiter:${extra["junitVersion"]}")
}

// Option 2: Type-safe delegates (recommended)
val springBootVersion by extra("3.2.0")
val junitVersion by extra("5.10.2")

dependencies {
    implementation("org.springframework.boot:spring-boot-starter-web:$springBootVersion")
    testImplementation("org.junit.jupiter:junit-jupiter:$junitVersion")
}

// Option 3: Regular Kotlin variables (best for build script only)
val springBootVersion = "3.2.0"
val junitVersion = "5.10.2"

dependencies {
    implementation("org.springframework.boot:spring-boot-starter-web:$springBootVersion")
    testImplementation("org.junit.jupiter:junit-jupiter:$junitVersion")
}
```

### Common Migration Gotchas

#### 1. String Quotes - Single vs Double

**Problem:**
```kotlin
// ERROR: Single quotes don't work in Kotlin
implementation('com.google.guava:guava:33.0.0-jre')  // Compilation error!
```

**Solution:**
```kotlin
// Use double quotes in Kotlin
implementation("com.google.guava:guava:33.0.0-jre")  // Correct
```

**Why:** Kotlin only supports double quotes for strings. Single quotes are for `Char` type.

#### 2. Method Call Parentheses

**Problem:**
```kotlin
// ERROR: Missing parentheses
implementation "com.google.guava:guava:33.0.0-jre"  // Compilation error!
```

**Solution:**
```kotlin
// Always use parentheses for method calls
implementation("com.google.guava:guava:33.0.0-jre")  // Correct
```

**Why:** Kotlin requires explicit parentheses for method calls (no implicit syntax like Groovy).

#### 3. Plugin ID Strings - kotlin vs "kotlin"

**Problem:**
```kotlin
plugins {
    // ERROR: This doesn't work in Kotlin DSL
    kotlin("jvm") version 2.0.0  // Compilation error - version is not a string!
}
```

**Solution:**
```kotlin
plugins {
    // Correct: Version must be a string literal
    kotlin("jvm") version "2.0.0"  // Correct

    // Alternative explicit form
    id("org.jetbrains.kotlin.jvm") version "2.0.0"  // Also correct
}
```

**Why:** The `version` infix function expects a string parameter, not an expression.

#### 4. Accessing Task by Name - Type Safety

**Problem:**
```kotlin
// Groovy way (not type-safe)
tasks.getByName("test") {
    useJUnitPlatform()  // No type information!
}
```

**Solution:**
```kotlin
// Kotlin way (type-safe)
tasks.named<Test>("test") {
    useJUnitPlatform()  // Type-safe! 'this' is Test
}

// Or using getByName with cast
tasks.getByName<Test>("test") {
    useJUnitPlatform()
}
```

**Why:** Kotlin DSL encourages type-safe accessors for better IDE support and compile-time checks.

#### 5. Configuration Names with Hyphens

**Problem:**
```kotlin
plugins {
    // ERROR: Hyphens in plugin names need backticks
    java-library  // Compilation error!
}
```

**Solution:**
```kotlin
plugins {
    // Use backticks for kebab-case names
    `java-library`  // Correct
}
```

**Why:** Hyphens aren't valid in Kotlin identifiers, so backticks escape them.

#### 6. Assignment vs Method Calls in Configuration

**Problem:**
```kotlin
// Confusing when to use = vs method call
task {
    description = "My task"  // Property assignment
    group("custom")          // Method call?
}
```

**Solution:**
```kotlin
tasks.register("myTask") {
    description = "My task"  // Property assignment (setter)
    group = "custom"         // Also property assignment!

    // Both work, but property syntax is more common in Kotlin
    doLast {
        println("Task executed")
    }
}
```

**Why:** Kotlin has property syntax for getters/setters. Use `=` for properties, `()` for methods.

#### 7. Extra Properties Access

**Problem:**
```kotlin
// Groovy style (not type-safe)
ext.myVersion = "1.0"
println(ext.myVersion)  // Error in Kotlin!
```

**Solution:**
```kotlin
// Option 1: Map-style access
extra["myVersion"] = "1.0"
println(extra["myVersion"])

// Option 2: Type-safe delegate (recommended)
val myVersion by extra("1.0")
println(myVersion)

// Option 3: Regular Kotlin variable (simplest)
val myVersion = "1.0"
println(myVersion)
```

**Why:** Kotlin DSL uses `extra` property with map-style or delegate access for type safety.

#### 8. Delegate Ambiguity in Configuration Blocks

**Problem:**
```kotlin
// Ambiguous delegate in nested blocks
repositories {
    maven {
        // Is 'url' from repository or project?
        url = uri("https://example.com/maven")  // Unclear!
    }
}
```

**Solution:**
```kotlin
repositories {
    maven {
        // Explicitly use 'this' if ambiguous
        this.url = uri("https://example.com/maven")

        // Or use the receiver parameter name
        url = uri("https://example.com/maven")  // Usually clear from context
    }
}
```

**Why:** Kotlin DSL sometimes requires explicit receiver (`this`) to disambiguate nested scopes.

#### 9. String Interpolation in Configuration

**Problem:**
```kotlin
// Variable not interpolated correctly
val myVersion = "1.0"
dependencies {
    implementation("com.example:lib:$myVersion")  // OK
    implementation("com.example:lib:${project.version}")  // project not in scope!
}
```

**Solution:**
```kotlin
val myVersion = "1.0"
val projectVersion = project.version  // Capture outside if needed

dependencies {
    implementation("com.example:lib:$myVersion")  // OK
    implementation("com.example:lib:$projectVersion")  // OK
}
```

**Why:** Be aware of variable scope in configuration blocks. Capture values early if needed.

#### 10. Dynamic Properties

**Problem:**
```kotlin
// Groovy's dynamic properties don't work
project.myCustomProperty = "value"  // Error in Kotlin!
println(project.myCustomProperty)   // Error!
```

**Solution:**
```kotlin
// Use extra properties
extra["myCustomProperty"] = "value"
println(extra["myCustomProperty"])

// Or define extensions properly
abstract class MyExtension {
    abstract val myProperty: Property<String>
}

val myExt = extensions.create<MyExtension>("myExt")
myExt.myProperty.set("value")
```

**Why:** Kotlin is statically typed; use `extra` for dynamic properties or define proper extensions.

#### 11. Task Container Configuration

**Problem:**
```kotlin
// Groovy uses 'all' without explicit call
tasks.withType(Test) {  // Error in Kotlin
    useJUnitPlatform()
}
```

**Solution:**
```kotlin
// Kotlin requires type parameter and explicit methods
tasks.withType<Test> {
    useJUnitPlatform()
}

// Or with configureEach (lazy)
tasks.withType<Test>().configureEach {
    useJUnitPlatform()
}
```

**Why:** Kotlin DSL uses generic type parameters (`<Test>`) for type safety.

#### 12. Creating vs Registering Tasks

**Problem:**
```kotlin
// Old Groovy pattern (eager)
tasks.create("myTask") {
    doLast { println("Task") }
}
```

**Solution:**
```kotlin
// Modern Kotlin pattern (lazy)
tasks.register("myTask") {
    doLast { println("Task") }
}
```

**Why:** `register` is lazy (better for configuration cache), `create` is eager. Prefer `register` in modern Gradle.

#### Migration Checklist

When migrating from Groovy to Kotlin DSL:

- [ ] Change file extension: `.gradle` → `.gradle.kts`
- [ ] Replace single quotes with double quotes
- [ ] Add parentheses to all method calls
- [ ] Add type parameters where needed (`<Test>`, `<MavenPublication>`)
- [ ] Use backticks for kebab-case identifiers
- [ ] Replace `ext` with `extra` or delegates
- [ ] Use `tasks.register` instead of `tasks.create`
- [ ] Use `tasks.named<Type>` instead of `tasks.getByName`
- [ ] Replace `project.property` with `providers.gradleProperty`
- [ ] Test with configuration cache enabled

#### Automated Migration Tools

While manual migration is often best, these tools can help:

```bash
# IntelliJ IDEA has built-in Groovy → Kotlin conversion
# Right-click build.gradle → Convert Groovy to Kotlin

# Gradle also provides a migration guide
# https://docs.gradle.org/current/userguide/migrating_from_groovy_to_kotlin_dsl.html
```

---

## Recommended Tooling

| Tool | Purpose |
|------|---------|
| `gradle wrapper` | Use Gradle Wrapper for version consistency |
| `gradle init` | Initialize new projects with proper structure |
| `gradle build --scan` | Build scans for performance analysis |
| `gradle --configuration-cache` | Enable configuration cache for faster builds |
| `gradle --build-cache` | Enable build cache for incremental builds |

---

## References

- Gradle Official Documentation: https://docs.gradle.org/
- Gradle Kotlin DSL Primer: https://docs.gradle.org/current/userguide/kotlin_dsl.html
- Gradle Best Practices: https://docs.gradle.org/current/userguide/authoring_maintainable_build_scripts.html
- Configuration Cache: https://docs.gradle.org/current/userguide/configuration_cache.html
- Build Cache: https://docs.gradle.org/current/userguide/build_cache.html
