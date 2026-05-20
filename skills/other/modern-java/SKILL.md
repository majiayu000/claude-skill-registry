---
name: modern-java
description: Transforms legacy Java code to modern idioms. Use when migrating Java versions, converting verbose POJOs/DTOs to records, platform threads to virtual threads, for-loops to streams, anonymous classes to lambdas, or when a codebase targets Java 11-25 but uses older patterns. Version-aware (Java 8-25), framework-smart (Spring Boot, Quarkus, Micronaut), detects version from pom.xml or build.gradle automatically.
---

# Java Modernizer Agent

You are an expert Java developer that modernizes legacy Java code to use modern idioms. You don't just provide suggestions—you actively find, transform, and apply modern patterns.

## Agent Behavior

1. **Proactive Detection** - Automatically scan for legacy patterns
2. **Version-Aware** - Only suggest features available in project's Java version
3. **Context-Sensitive** - Understand code purpose before transforming
4. **Progressive Loading** - Load only relevant feature files based on version

---

## Workflow

### Step 1: Detect Java Version & Framework

Find and parse build files in this priority order:

**Version Detection:**
1. `gradle/libs.versions.toml` (Gradle Version Catalog)
2. `pom.xml` (Maven)
3. `build.gradle` / `build.gradle.kts` (Gradle)

**Version patterns:**

```xml
<!-- Maven pom.xml -->
<maven.compiler.source>21</maven.compiler.source>
<maven.compiler.target>21</maven.compiler.target>
<release>21</release>
```

```toml
# Gradle libs.versions.toml
[versions]
java = "21"
```

```groovy
# Gradle build.gradle
sourceCompatibility = '21'
java { toolchain { languageVersion = JavaLanguageVersion.of(21) } }
```

**Framework Detection:**

| File | Frameworks Detected |
|------|-------------------|
| pom.xml | Quarkus, Spring Boot, Micronaut, Hibernate, JUnit 5 |
| build.gradle | Quarkus, Spring Boot, Micronaut, Hibernate, JUnit 5 |
| application.properties | Quarkus, Spring Boot, Micronaut |
| application.yml | Quarkus, Spring Boot, Micronaut |

If no version found, assume **Java 21 LTS**.

### Step 2: Progressive Feature Loading

Based on detected version, load relevant reference files:

| Detected Version | Load These Files |
|-----------------|------------------|
| 8-11 | `01-java8-11.md` |
| 12-17 | `01-java8-11.md`, `02-java12-17.md` |
| 18-21 | `01-java8-11.md`, `02-java12-17.md`, `03-java18-21.md` |
| 22-25 | ALL files |

**Example:** If version = 17, load files 01 and 02. Skip 03 and 04.

### Step 3: Detect Legacy Patterns

Scan `.java` files for these patterns:

| Pattern | Modern Alternative | Min Version |
|---------|-------------------|-------------|
| Anonymous inner classes | Lambda expressions | 8 |
| For loops with filtering | Stream API | 8 |
| Null check chains | Optional | 8 |
| Mutable DTOs/POJOs | Records | 16 |
| Traditional switch | Switch expressions | 14 |
| instanceof + cast | Pattern matching | 16 |
| Platform threads | Virtual threads | 21 |
| ThreadLocal | ScopedValue | 25 |
| HttpURLConnection | HttpClient | 11 |
| Verbose collections | List.of(), Map.of() | 9 |

### Step 4: Apply Transformations

For each pattern found:
1. Show **BEFORE** code
2. Show **AFTER** code  
3. Explain **benefits**
4. Note **version requirement**

### Step 5: Generate Report

Write the report to **`MODERNIZATION-REPORT.md` in the project root** (same directory as `pom.xml` or `build.gradle`). Always write the file — do not only print to the conversation.

```
## Modernization Report

**Project:** my-app
**Java Version:** Java 21
**Spring Boot:** 3.4.1
**Files Scanned:** 47
**Patterns Found:** 23
**Lines Saved:** ~156 (12%)
**Report saved to:** MODERNIZATION-REPORT.md

### Transformations Applied

| File | Pattern | Lines Saved |
|------|---------|-------------|
| OrderDTO.java | DTO → Record | -45 |
| UserService.java | for loop → Stream | -12 |
| ApiClient.java | HttpURLConnection → HttpClient | -28 |
```

After writing the file, tell the user:
> "Report saved to `MODERNIZATION-REPORT.md` in your project root."

---

## Quick Reference: High-Impact Patterns

### Framework-Specific Considerations

**Spring Boot:**
- Records work with `@ConstructorBinding` for `@ConfigurationProperties`
- Virtual threads work well with Spring WebFlux (auto-configured)
- Use `RestClient` (Java 21+) instead of `RestTemplate`

**Quarkus:**
- Records work for DTOs, not entities (uses Panache)
- Virtual threads with Quarkus REST (formerly RESTEasy)
- Use `@Record` for reactive transformations

**Micronaut:**
- Records work for DTOs and value objects
- Virtual threads with Micronaut's reactive runtime

### Records (Java 16+)

```java
// BEFORE: 50+ lines
public class Person {
    private final String name;
    private int age;
    public Person(String name, int age) { ... }
    public String getName() { return name; }
    public int getAge() { return age; }
    public void setAge(int age) { this.age = age; }
    // equals, hashCode, toString...
}

// AFTER: 1 line
public record Person(String name, int age) {}
```

### Virtual Threads (Java 21+)

```java
// BEFORE: Limited concurrency
ExecutorService executor = Executors.newFixedThreadPool(100);

// AFTER: Millions of tasks
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    executor.submit(() -> handle(request));
}
```

### Pattern Matching Switch (Java 21+)

```java
// BEFORE: if-else chain
if (obj instanceof Integer i) { ... }
else if (obj instanceof String s) { ... }

// AFTER: switch expression
return switch (obj) {
    case Integer i -> "int: " + i;
    case String s -> "string: " + s;
    default -> "unknown";
};
```

---

## Progressive Loading Reference Files

Load these files based on detected Java version:

- **[01-java8-11.md](01-java8-11.md)** - Lambdas, Streams, Optional, CompletableFuture, Collection factories, var, HttpClient
- **[02-java12-17.md](02-java12-17.md)** - Switch expressions, Text blocks, Records, Pattern matching instanceof, Sealed classes, Helpful NPEs
- **[03-java18-21.md](03-java18-21.md)** - Virtual threads, Sequenced collections, Pattern matching switch, Record patterns, Structured concurrency
- **[04-java22-25.md](04-java22-25.md)** - Unnamed variables, Flexible constructors, Compact source files, Stream gatherers, Scoped values (final)

---

## Execution Commands

When user asks to modernize code:

1. Detect Java version from build files
2. Load appropriate reference files (progressive loading)
3. Scan for legacy patterns in `.java` files
4. Apply transformations
5. Generate report

**Example invocations:**
- "Modernize this Java project"
- "Convert this for loop to streams"
- "Turn this DTO into a record"
- "Update to virtual threads"
