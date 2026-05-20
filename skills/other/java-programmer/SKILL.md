---
name: java-programmer
description: Java-specific tooling, documentation standards, testing practices, and modern idioms. Use when working with Java code or Java-based projects on the JVM.
---

# Java Programmer

## Purpose

This skill provides guidance on Java-specific tooling, documentation standards, testing practices, and modern Java idioms. Java is a statically-typed, object-oriented language with a massive ecosystem and strong backwards compatibility guarantees. This skill focuses on navigating the Java ecosystem effectively, writing maintainable Java code, and applying functional programming concepts within Java's constraints.

## When to Use This Skill

Use this skill when:
- Working with Java codebases (any version, but especially Java 8+)
- Making decisions about build tools, testing frameworks, or dependencies
- Writing Javadoc documentation
- Writing JUnit tests
- Applying functional programming patterns in Java
- Navigating the JVM ecosystem (choosing between JVM languages)

<core_philosophy>
## Core Philosophy

**For foundational software engineering principles, see the software-engineer skill. For OOP principles (SOLID, GoF patterns), see the object-oriented-programmer skill.**

### Java's Strengths and Constraints

Java excels in specific contexts but has limitations compared to more modern languages.

**Where Java shines:**
- **Enterprise systems** — Mature ecosystem, strong tooling, extensive libraries
- **Team stability** — Explicit types, verbose code, fewer "clever" tricks
- **Long-term maintenance** — Backwards compatibility, gradual evolution
- **JVM ecosystem** — Interop with Kotlin, Scala, Clojure, Groovy
- **Performance** — JIT compilation, mature garbage collectors, profiling tools

**Where Java struggles:**
- **Rapid prototyping** — Verbosity slows iteration
- **Functional programming** — Retrofitted features, verbose syntax
- **Type system** — Lacks algebraic data types, pattern matching (until recent versions)
- **Ceremony** — Boilerplate reduces signal-to-noise ratio

**Staff insight:** If you're writing Java professionally but prefer functional languages, focus on using modern Java features (streams, Optional, lambdas) to bring functional thinking into Java's constraints. Don't fight the language—work within its idioms.

### Documentation as Contract

Javadoc is more than comments—it's a contract between API and client. Treat it as seriously as the code itself.

**Quote to remember:** "Code is read more often than written." — Guido van Rossum. Documentation is read even more often than that.
</core_philosophy>

<type_annotations>
## Type Annotations and The Checker Framework Are Mandatory

Java's type system lacks many important guarantees. Type annotations with The Checker Framework enable compile-time verification of properties that the type system doesn't enforce.

**Why type annotations and static analysis matter:**
- **Critical for LLM-assisted development** — Explicit contracts enable better code generation and reasoning
- Eliminate entire classes of errors at compile time (NullPointerException, regex errors, format string bugs)
- Make API contracts machine-readable (not just documented in Javadoc)
- Enable static analysis to catch bugs before runtime
- Self-documenting code (contracts visible in signatures)

**The Checker Framework is mandatory for all new projects:**
- Use **JSpecify annotations** for nullness (`@Nullable`, `@NonNull` via defaults)
- JSpecify provides multi-tool compatibility (works with Checker Framework, IntelliJ, NullAway, etc.)
- Enable as many Checker Framework checkers as practical:
  - **Nullness Checker** (via JSpecify annotations) — Prevent NullPointerException
  - **Optional Checker** — Enforce proper Optional usage
  - **Regex Checker** — Verify regex string validity at compile time
  - **Format String Checker** — Verify printf/format string correctness
  - **Interning Checker** — Ensure string interning correctness
  - **Index Checker** — Prevent array bounds errors
  - **Lock Checker** — Verify lock usage and prevent race conditions
  - Additional checkers as applicable to domain

**Example with JSpecify nullness annotations:**
```java
import org.jspecify.annotations.Nullable;
// @NonNull is the default assumption (no annotation needed)

public class UserService {
    /**
     * Finds user by ID.
     *
     * @param id the user ID (must not be null, default assumption)
     * @return user if found, null otherwise
     */
    public @Nullable User findById(String id) {
        // Checker verifies: id cannot be null (default @NonNull)
        // Checker requires: callers handle possible null return
        return repository.findById(id).orElse(null);
    }

    /**
     * Gets user display name.
     *
     * @param user the user (must not be null, default assumption)
     * @return display name (never null, default assumption)
     */
    public String getDisplayName(User user) {
        // Checker verifies: user cannot be null
        // Checker enforces: return value cannot be null
        String name = user.getName();
        return name != null ? name : "Guest";
    }
}
```

**Example with other Checker Framework annotations:**
```java
import org.checkerframework.checker.regex.qual.Regex;
import org.checkerframework.checker.formatter.qual.FormatMethod;

public class ValidationService {
    /**
     * Validates input against pattern.
     *
     * @param input the input string
     * @param pattern the regex pattern (verified at compile time)
     * @return true if input matches pattern
     */
    public boolean matches(String input, @Regex String pattern) {
        // Checker verifies: pattern is valid regex at compile time
        return input.matches(pattern);
    }

    /**
     * Logs formatted message.
     *
     * @param format the format string (verified at compile time)
     * @param args the format arguments
     */
    @FormatMethod
    public void logFormatted(String format, Object... args) {
        // Checker verifies: format string matches args at compile time
        logger.info(String.format(format, args));
    }
}
```

**When to use annotations:**
- **Nullness (JSpecify):**
  - Mark `@Nullable` explicitly when null is permitted
  - Default assumption is `@NonNull` (no annotation needed)
  - Annotate parameters, return types, fields, generic type arguments
- **Other Checker Framework annotations:**
  - Use `@Regex` for all regex pattern strings
  - Use `@FormatMethod` and format string annotations for printf-style methods
  - Use `@GuardedBy` for fields accessed under locks
  - Use domain-specific checkers as applicable

**Why both type annotations AND Javadoc:**
- Type annotations: Machine-readable contracts (compiler enforces)
- Javadoc: Human-readable context (explains why, when, edge cases)
- Example: Annotation says `@Nullable`, Javadoc explains when null is returned

**Maven/Gradle configuration:**
```xml
<!-- Maven: Add Checker Framework -->
<dependency>
    <groupId>org.checkerframework</groupId>
    <artifactId>checker-qual</artifactId>
    <version>3.42.0</version>
</dependency>
<dependency>
    <groupId>org.jspecify</groupId>
    <artifactId>jspecify</artifactId>
    <version>1.0.0</version>
</dependency>

<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-compiler-plugin</artifactId>
    <configuration>
        <compilerArgs>
            <arg>-Xplugin:ErrorProne</arg>
            <arg>-J--add-exports=jdk.compiler/com.sun.tools.javac.api=ALL-UNNAMED</arg>
            <arg>-J--add-exports=jdk.compiler/com.sun.tools.javac.code=ALL-UNNAMED</arg>
            <arg>-Xplugin:checkerframework -processor org.checkerframework.checker.nullness.NullnessChecker,org.checkerframework.checker.regex.RegexChecker,org.checkerframework.checker.formatter.FormatterChecker</arg>
        </compilerArgs>
    </configuration>
</plugin>
```

**CI/CD integration:**
- All Checker Framework checkers must run in CI/CD pipeline
- Builds fail on checker errors (no warnings mode)
- No exceptions for "I'll fix it later"

**Staff insight:** The Checker Framework is as important as comprehensive testing for code quality. JSpecify annotations provide nullness checking with multi-tool compatibility. Beyond nullness, use all applicable checkers (Regex, Format String, Index, Lock, etc.) to catch errors at compile time. Type annotations provide compile-time verification that tests and documentation cannot.
</type_annotations>

<version_targeting>
## Java Version Targeting: Use Latest Version Only

All new Java projects must target the latest Java version or at least the latest LTS version. (Java 25 is the latest LTS release as of late 2025). You can find the latest version by reading [this Wikipedia article](https://en.wikipedia.org/wiki/Java_version_history). That article is also a good reference for new features you should look at adopting.

**Why Java 25+:**
- **Sealed classes** — Algebraic data types for eliminating invalid states
- **Pattern matching** — Type-safe destructuring (for instanceof, switch expressions)
- **Records** — Concise immutable data carriers
- **Text blocks** — Readable multi-line strings
- **Virtual threads** — Lightweight concurrency (Project Loom)
- **Modern APIs** — Collections.of(), Stream improvements, enhanced switch
- **LTS support** — Long-term support and security updates

**For existing projects:**
- Upgrade to Java 25+ as soon as practical
- Aggressively refactor and rewrite to use modern features (records, sealed classes, pattern matching)
- Don't maintain Java 8/11/17 projects indefinitely
- Use upgrades as opportunities to improve project design if possible.

**Staff insight:** Aggressive adoption of Java features is a philosophy. Java 25 has the features that make Java competitive with modern languages (sealed classes, pattern matching, records). Using older versions means missing critical type safety and expressiveness improvements. Upgrade aggressively.

### Respecting Third-Party Codebases

**The aggressive adoption philosophy applies ONLY to codebases you own.**

When contributing to open source projects or third-party codebases:
- **Respect the project's existing style and conventions**
- **Do not introduce new Java features unless the project explicitly targets that version**
- **Do not refactor existing code to use modern idioms unless requested**
- **Follow the project's contribution guidelines strictly**
- **Match the existing code style, even if it differs from your preferences**

**Why this matters:**
- **Stability** — OSS projects prioritize stability over bleeding-edge features
- **Community consensus** — Style changes require community agreement
- **Compatibility** — Projects may target older Java versions for user compatibility
- **Maintainability** — Consistency matters more than modernization in large codebases

**When you can suggest modernization:**
- File an issue proposing Java version upgrade with justification
- Propose style changes through project governance process
- Offer to help with migration if project agrees
- Never surprise maintainers with unsolicited rewrites

**Staff insight:** Your aggressive adoption philosophy is for codebases you control. When contributing to others' projects, you're a guest—respect the house rules. Propose improvements through proper channels, don't impose them through pull requests. Stability and community consensus matter more than your personal preferences in shared codebases.
</version_targeting>

<tooling_stack>
## Mandatory Tooling Stack

All new Java projects must use the following tools with CI/CD integration. Builds must fail on violations.

**Required tools:**

**Spotless (code formatting):**
- Enforces consistent formatting automatically
- Eliminates formatting debates
- Supports Google Java Format, Palantir, Eclipse formatters
- Runs during build, fails on violations
- Use for: All new projects (no exceptions)

**Checkstyle (code style enforcement):**
- Enforces coding standards beyond formatting
- Checks naming conventions, javadoc presence, complexity
- Use Checkstyle for semantic rules, Spotless for formatting
- Configuration files available in `./assets/checkstyle.xml`
- Use for: All new projects (no exceptions)

**SpotBugs (static analysis for bugs):**
- Detects common bug patterns (resource leaks, null dereferences, concurrency issues)
- Successor to FindBugs
- Must run in CI/CD pipeline
- Use for: All new projects (no exceptions)

**ErrorProne (Google's bug pattern checker):**
- Catches Java-specific bugs at compile time
- More sophisticated than SpotBugs (understands Java semantics deeply)
- Integrates into javac compilation
- Use for: All new projects (no exceptions)

**JaCoCo (code coverage):**
- Measures test coverage
- Enforces minimum coverage thresholds in CI/CD
- Use for: All projects with test suites

**JSpecify + Checker Framework (type annotations):**
- Already covered above
- Nullness checker via JSpecify
- Additional checkers (Regex, Format String, Index, Lock)

**Maven/Gradle configuration example:**

```xml
<!-- Maven pom.xml -->
<build>
    <plugins>
        <!-- Spotless for formatting -->
        <plugin>
            <groupId>com.diffplug.spotless</groupId>
            <artifactId>spotless-maven-plugin</artifactId>
            <version>2.43.0</version>
            <configuration>
                <java>
                    <googleJavaFormat>
                        <version>1.19.1</version>
                        <style>GOOGLE</style>
                    </googleJavaFormat>
                    <removeUnusedImports />
                    <formatAnnotations />
                </java>
            </configuration>
            <executions>
                <execution>
                    <goals>
                        <goal>check</goal>
                    </goals>
                    <phase>verify</phase>
                </execution>
            </executions>
        </plugin>

        <!-- Checkstyle -->
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-checkstyle-plugin</artifactId>
            <version>3.3.1</version>
            <configuration>
                <configLocation>checkstyle.xml</configLocation>
                <consoleOutput>true</consoleOutput>
                <failsOnError>true</failsOnError>
            </configuration>
            <executions>
                <execution>
                    <goals>
                        <goal>check</goal>
                    </goals>
                    <phase>verify</phase>
                </execution>
            </executions>
        </plugin>

        <!-- SpotBugs -->
        <plugin>
            <groupId>com.github.spotbugs</groupId>
            <artifactId>spotbugs-maven-plugin</artifactId>
            <version>4.8.3.0</version>
            <configuration>
                <effort>Max</effort>
                <threshold>Low</threshold>
                <failOnError>true</failOnError>
            </configuration>
            <executions>
                <execution>
                    <goals>
                        <goal>check</goal>
                    </goals>
                    <phase>verify</phase>
                </execution>
            </executions>
        </plugin>

        <!-- ErrorProne -->
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-compiler-plugin</artifactId>
            <version>3.12.1</version>
            <configuration>
                <release>25</release>
                <compilerArgs>
                    <arg>-XDcompilePolicy=simple</arg>
                    <arg>-Xplugin:ErrorProne</arg>
                </compilerArgs>
                <annotationProcessorPaths>
                    <path>
                        <groupId>com.google.errorprone</groupId>
                        <artifactId>error_prone_core</artifactId>
                        <version>2.24.1</version>
                    </path>
                </annotationProcessorPaths>
            </configuration>
        </plugin>

        <!-- JaCoCo -->
        <plugin>
            <groupId>org.jacoco</groupId>
            <artifactId>jacoco-maven-plugin</artifactId>
            <version>0.8.11</version>
            <executions>
                <execution>
                    <goals>
                        <goal>prepare-agent</goal>
                    </goals>
                </execution>
                <execution>
                    <id>check</id>
                    <goals>
                        <goal>check</goal>
                    </goals>
                    <configuration>
                        <rules>
                            <rule>
                                <element>PACKAGE</element>
                                <limits>
                                    <limit>
                                        <counter>LINE</counter>
                                        <value>COVEREDRATIO</value>
                                        <minimum>0.80</minimum>
                                    </limit>
                                </limits>
                            </rule>
                        </rules>
                    </configuration>
                </execution>
            </executions>
        </plugin>
    </plugins>
</build>
```

**CI/CD integration:**
- All tools must run in CI/CD pipeline (GitHub Actions, GitLab CI, Jenkins, etc.)
- Builds fail on any tool violations (no warnings mode)
- No exceptions for "I'll fix it later"
- Formatting (Spotless), style (Checkstyle), bugs (SpotBugs, ErrorProne), coverage (JaCoCo) all must pass

**Configuration files:**
- Example Checkstyle configuration: `./assets/checkstyle.xml` (reference this in your pom.xml/build.gradle)
- Customize as needed but maintain strict standards
- Share configurations across projects for consistency

**Staff insight:** Don't waste time debating formatting or choosing between tools. Use Spotless for formatting (automatic, no configuration needed), Checkstyle for semantic rules, SpotBugs + ErrorProne for bug detection, JaCoCo for coverage. These tools are mandatory, not optional. They catch errors early and enforce consistency.
</tooling_stack>

<jpms>
## Java Platform Module System (JPMS): Use When Practical

The Java Platform Module System (JPMS) should be used aggressively for new projects, but pragmatism is required due to ecosystem limitations.

**When to use JPMS:**
- New projects (default choice)
- Multi-module builds where encapsulation matters
- Libraries that want strong encapsulation
- Projects where you control all dependencies

**Why JPMS matters:**
- **Strong encapsulation** — Internal packages truly hidden (not just convention)
- **Explicit dependencies** — module-info.java declares dependencies
- **Compile-time verification** — Module system verifies dependencies
- **Better tooling** — jlink for custom runtime images

**Basic module-info.java example:**
```java
module com.example.myapp {
    requires java.sql;
    requires com.google.common; // Guava
    requires org.slf4j; // SLF4J

    exports com.example.myapp.api; // Public API
    // Internal packages not exported (truly encapsulated)
}
```

**The pragmatic problem: Third-party library adoption**

Many third-party libraries don't have proper module descriptors. This creates friction.

**Solutions for mixing modularized and non-modularized code:**

**1. Automatic modules (non-modularized JARs on module path):**
- Put non-modularized JAR on module path
- Becomes "automatic module" with derived name from JAR filename
- Exports all packages, reads all modules
- Works but fragile (module name derived from filename can change)

```java
module com.example.myapp {
    requires commons.lang3; // Automatic module (from commons-lang3-3.x.jar)
}
```

**2. Use --add-reads, --add-exports, --add-opens for opening up modules:**
```bash
java --add-reads com.example.myapp=ALL-UNNAMED \
     --add-exports java.base/sun.security.x509=ALL-UNNAMED \
     --add-opens java.base/java.lang=ALL-UNNAMED \
     -jar myapp.jar
```

- `--add-reads` — Allows module to read unnamed module (classpath)
- `--add-exports` — Export internal JDK packages to your code
- `--add-opens` — Allow reflective access to internal packages

**3. Split packages problem (fatal in JPMS):**
- Two modules cannot contain the same package
- If two dependencies have same package, JPMS fails
- Solution: Relocate packages (Maven Shade plugin) or abandon JPMS for that project

**4. When to pragmatically abandon JPMS:**
- Too many dependencies lack module descriptors
- Split package conflicts that can't be resolved
- Framework requires classpath (some older frameworks)
- Reflection-heavy code that fights JPMS encapsulation

**Don't force JPMS when it creates more problems than it solves.**

**Practical approach:**
1. Start with JPMS (aggressive adoption philosophy)
2. Use automatic modules for well-behaved non-modularized dependencies
3. Use --add-reads/--add-exports flags for problematic cases
4. If you hit split packages or too many problematic deps, switch to classpath
5. Revisit JPMS periodically as ecosystem improves

**Staff insight:** JPMS is excellent when it works (strong encapsulation, explicit dependencies) but the Java ecosystem hasn't fully adopted it. Start with JPMS, be prepared to fall back to classpath if third-party libraries cause too much pain. This is pragmatism, not failure—sometimes the tooling isn't ready for your philosophy.
</jpms>

<javadoc>
## Javadoc Is Mandatory

Comprehensive Javadoc documentation is not optional. Every public element must be documented.

### When to Write Javadoc

**Always document (required for all production code):**
- Public APIs (classes, interfaces, methods, fields)
- Package-level documentation (package-info.java)
- Non-obvious design decisions
- Preconditions, postconditions, invariants
- Thread safety guarantees
- Null handling contracts (explain when null is valid, even with annotations)

**Document private elements when:**
- Logic is non-obvious
- Future maintainers need context
- Design rationale should be preserved
- Usage patterns aren't clear from signature

**Every test must have Javadoc:**
- What behavior/requirement is being verified
- Why the test exists
- Special test data setup
- Known limitations

**Staff insight:** Junior developers under-document. Senior developers document the "why" and constraints, not just the "what." Assume future readers (including LLMs) need to understand intent, not just implementation. Comprehensive Javadoc is as important as comprehensive tests.

### Javadoc Formatting Standards

**HTML, not Markdown:**
- Use `<ul>` and `<li>` for lists (NOT Markdown bullets)
- Use `<p>` for paragraph breaks (with newline before tag)
- Use `<code>` and `{@code}` for inline code
- Use `<pre>` for code blocks
- Use `{@link}` for references to other types/methods

**Example:**
```java
/**
 * Processes user input and validates against business rules.
 * <p>
 * This method performs the following steps:
 * <ul>
 *   <li>Sanitizes input to remove malicious content</li>
 *   <li>Validates against {@link ValidationRule} set</li>
 *   <li>Returns {@link Result} containing validated data or errors</li>
 * </ul>
 * <p>
 * Thread safety: This method is thread-safe and can be called concurrently.
 *
 * @param input the user input to process (must not be null)
 * @param rules the validation rules to apply
 * @return validation result containing either data or errors
 * @throws IllegalArgumentException if input is null
 */
public Result<Data> processInput(String input, Set<ValidationRule> rules) {
    // implementation
}
```

### Documentation Content Philosophy

**Focus on the "why" and constraints:**
- Why does this class/method exist?
- What problems does it solve?
- What are its limitations?
- What are the preconditions/postconditions?
- What are the edge cases?
- What assumptions does it make?

**Avoid restating the obvious:**
```java
// BAD: Restates signature
/**
 * Gets the user name.
 * @return the user name
 */
public String getUserName() { ... }

// GOOD: Adds context
/**
 * Returns the user's display name for UI rendering.
 * <p>
 * This is not the username for authentication (see {@link #getLoginName()}).
 * Returns "Guest" if user is not authenticated.
 *
 * @return display name for current user, never null
 */
public String getUserName() { ... }
```

**Document design decisions:**
```java
/**
 * Cache implementation using weak references to allow garbage collection.
 * <p>
 * This cache prioritizes memory efficiency over hit rate. Entries may be
 * evicted at any time if memory pressure increases. For guaranteed retention,
 * use {@link StrongReferenceCache} instead.
 * <p>
 * Thread safety: This implementation is thread-safe using concurrent data
 * structures. However, cache size is approximate due to asynchronous cleanup.
 */
public class WeakReferenceCache<K, V> { ... }
```
</javadoc>

<junit_testing>
## JUnit Testing Practices

**For general testing philosophy and TDD principles, see the test-driven-development skill.** This section covers Java/JUnit-specific practices.

### JUnit Organization with @Nested

Use `@Nested` classes to create hierarchical test organization that mirrors domain concepts:

```java
@DisplayName("UserService")
class UserServiceTest {

    @Nested
    @DisplayName("when creating new users")
    class UserCreation {

        @Test
        @DisplayName("should generate unique ID for each user")
        void generatesUniqueIds() {
            // Given user creation scenario
            // When creating multiple users
            // Then each receives unique ID
        }

        @Test
        @DisplayName("should validate email format before creation")
        void validatesEmailFormat() {
            // Test implementation with descriptive assertion messages
        }
    }

    @Nested
    @DisplayName("when updating existing users")
    class UserUpdate {
        // Tests for update scenarios
    }
}
```

**Why this matters:**
- Test output reads like specifications ("UserService when creating new users should generate unique ID")
- Easy to find relevant tests
- Clear domain organization
- Documents system behavior hierarchically

### Assertion Best Practices

**Use Assertions class methods appropriately:**
```java
// GOOD: Use specific assertions
assertArrayEquals(expected, actual, "Byte arrays should match after serialization");
assertDoesNotThrow(() -> service.process(input), "Valid input should not throw exceptions");

// BAD: Manual comparison
assertTrue(Arrays.equals(expected, actual), "Arrays should be equal");

// BAD: Verbose try-catch
try {
    service.process(input);
} catch (Exception e) {
    fail("Should not throw exception");
}
```

**Write meaningful assertion messages:**
```java
// BAD: Restates assertion
assertEquals(expected, actual, "Values should be equal");

// GOOD: Explains why expectation exists
assertEquals(
    expectedTotal,
    invoice.getTotal(),
    "Invoice total should include all line items plus tax and exclude discounts for non-premium users"
);
```

**Staff insight:** Assertion messages are documentation. When a test fails, the message should help diagnose the root cause. Explain the business/technical reason for the expectation, not just the assertion itself.

### Mockito Best Practices

**Mock dependencies across architectural boundaries:**
- External systems (e.g., APIs, databases, file systems)
- Dependencies injected into the unit under test
- Don't mock the system under test itself
- Don't mock within the cohesive unit (e.g., private methods)
- See test-driven-development skill for mocking strategy based on architectural boundaries

**Use specific matchers:**
```java
// GOOD: Specific matching
when(repository.findById(eq(userId))).thenReturn(Optional.of(user));

// AVOID: Overly permissive
when(repository.findById(anyString())).thenReturn(Optional.of(user));

// LAST RESORT: When object equality doesn't work
when(service.process(any(Request.class))).thenReturn(response);
```

**Scope mocks carefully:**
- Don't share mocks across unrelated tests
- Setup mocks in smallest applicable scope
- Avoid lenient mode (indicates test design problem)
- Unnecessary stubbings cause failures—keep setup minimal

**If tempted to mock internals of the unit under test, refactor instead.**

### Test Documentation

Every test should have Javadoc explaining:
- What behavior/requirement it verifies
- Why this test is important
- Any special test data setup
- Known gaps or limitations

**Core testing principle (from test-driven-development skill):** Mock at architectural boundaries (external systems, injected dependencies), not internal implementation details.

```java
/**
 * Verifies that user creation fails when email is already registered.
 * <p>
 * This test ensures we maintain email uniqueness constraint per requirements
 * in USER-123. The test uses a pre-populated test user to simulate existing
 * registration.
 * <p>
 * Known limitation: Does not test case-sensitivity of email comparison
 * (covered separately in {@link #emailComparisonIsCaseInsensitive()}).
 */
@Test
@DisplayName("should reject duplicate email addresses")
void rejectsDuplicateEmails() {
    // Test implementation
}
```
</junit_testing>

<build_tools>
## Build Tools: Maven vs Gradle

### When to Use Maven

**Maven's strengths:**
- **Convention over configuration** — Standard directory structure, standard lifecycle
- **Stability** — Mature, well-understood, extensive plugin ecosystem
- **Simplicity** — Declarative XML, less flexibility means fewer ways to misconfigure
- **Corporate environments** — Often required/preferred in enterprises
- **Reproducibility** — Less flexibility reduces build variance

**Use Maven when:**
- Team values stability over flexibility
- Working in enterprise/corporate environment
- Project follows standard Java conventions
- Build requirements are straightforward
- Team is unfamiliar with Groovy/Kotlin

### When to Use Gradle

**Gradle's strengths:**
- **Flexibility** — Programmatic build scripts (Groovy or Kotlin DSL)
- **Performance** — Incremental builds, build caching, parallel execution
- **Multi-project builds** — Better support for complex project structures
- **Android** — Required for Android development
- **Modern features** — Composite builds, dependency locking, version catalogs

**Use Gradle when:**
- Need complex custom build logic
- Performance matters (large codebases, frequent builds)
- Multi-module projects with inter-dependencies
- Android development
- Team comfortable with Groovy/Kotlin

**Staff insight:** For greenfield projects with standard requirements, Maven is often sufficient and simpler. Gradle's flexibility has cost—it enables more complex (and more fragile) builds. Choose based on actual needs, not perceived sophistication.
</build_tools>

<modern_features>
## Modern Java Features: When to Use Them

### Streams (Java 8+)

**Use streams when:**
- Transforming collections declaratively
- Operations compose well (filter → map → reduce)
- Parallelism might help (use `parallelStream()` carefully)
- Code reads better than loops

**Avoid streams when:**
- Simple iteration suffices (don't force it)
- Debugging is important (stream debugging is harder)
- Performance-critical tight loops (measure first)
- Checked exceptions involved (awkward workarounds needed)

**Example transformation:**
```java
// Imperative (perfectly fine for simple cases)
List<String> names = new ArrayList<>();
for (User user : users) {
    if (user.isActive()) {
        names.add(user.getName());
    }
}

// Streams (clearer for this pattern)
List<String> names = users.stream()
    .filter(User::isActive)
    .map(User::getName)
    .collect(Collectors.toList());
```

**Staff insight:** Streams are a tool, not a requirement. Use them where they improve clarity. Don't reflexively convert every loop.

### Optional (Java 8+)

**Use Optional for:**
- Return types where absence is valid (not exceptional)
- Making API contracts explicit (nullable vs non-null)
- Chaining operations on potentially absent values

**Don't use Optional for:**
- Fields (use null or sentinel values)
- Method parameters (use overloading or builder pattern)
- Collections (empty collection is better than Optional<List>)
- Serialization (Optional is not Serializable)

**Example:**
```java
// GOOD: Return type making absence explicit
public Optional<User> findUserById(String id) {
    // Returns Optional.empty() if not found
}

// Usage
findUserById(id)
    .map(User::getEmail)
    .ifPresent(email -> sendNotification(email));

// BAD: Optional as field
public class User {
    private Optional<String> middleName; // Just use String, null is fine
}

// BAD: Optional as parameter
public void updateUser(Optional<String> newEmail) { ... } // Use overloading instead
```

**Staff insight:** Optional is for return values, not general null handling. It makes contracts explicit but shouldn't be used everywhere.

### Records (Java 14+, standard in 16+)

**Use records for:**
- Immutable data carriers (DTOs, value objects)
- Replacing verbose POJOs with boilerplate
- Domain modeling with value semantics

**Don't use records for:**
- Mutable entities
- Classes with behavior (use regular classes)
- When you need custom equals/hashCode logic
- JPA entities (records are final, JPA needs inheritance)

**Example:**
```java
// Traditional POJO (verbose)
public final class Point {
    private final int x;
    private final int y;

    public Point(int x, int y) {
        this.x = x;
        this.y = y;
    }

    public int getX() { return x; }
    public int getY() { return y; }

    @Override
    public boolean equals(Object o) { /* boilerplate */ }

    @Override
    public int hashCode() { /* boilerplate */ }
}

// Record (concise, same semantics)
public record Point(int x, int y) {
    // Optional: custom constructor for validation
    public Point {
        if (x < 0 || y < 0) {
            throw new IllegalArgumentException("Coordinates must be non-negative");
        }
    }
}
```

### Pattern Matching and Switch Expressions (Java 14+)

**Use pattern matching when:**
- Type checking and casting (instanceof with patterns)
- Replacing verbose if-else chains
- Switch statements with non-trivial logic

**Example:**
```java
// Old style (verbose)
if (shape instanceof Circle) {
    Circle circle = (Circle) shape;
    return Math.PI * circle.radius() * circle.radius();
} else if (shape instanceof Rectangle) {
    Rectangle rect = (Rectangle) shape;
    return rect.width() * rect.height();
}

// Pattern matching (concise)
return switch (shape) {
    case Circle c -> Math.PI * c.radius() * c.radius();
    case Rectangle r -> r.width() * r.height();
    default -> throw new IllegalArgumentException("Unknown shape");
};
```
</modern_features>

<functional_java>
## Functional Programming in Java

**For deeper FP philosophy and when functional approaches are clearer, see the functional-programmer skill.** This section covers Java-specific FP patterns.

### Embracing FP Within Java's Constraints

Java retrofitted functional features (lambdas, streams, Optional) onto an OO foundation. This creates friction but enables functional thinking within Java's idioms.

**What works well in Java:**
- Immutable data (final fields, records)
- Higher-order functions (via functional interfaces)
- Streams for collection transformations
- Optional for explicit absence

**What's awkward in Java:**
- Checked exceptions in lambdas (requires wrapping)
- No algebraic data types (until recent sealed types)
- Verbose lambda syntax for complex logic
- Limited type inference compared to Scala/Kotlin

**Staff insight:** Don't force pure FP in Java. Use functional features where they improve clarity (streams, immutability, Optional) but accept imperative code where it's clearer.

### Immutability Patterns

**Make fields final by default:**
```java
public class Configuration {
    private final String apiKey;
    private final int timeout;

    public Configuration(String apiKey, int timeout) {
        this.apiKey = apiKey;
        this.timeout = timeout;
    }

    // Getters only, no setters
}
```

**Use records for value objects:**
```java
public record Money(BigDecimal amount, Currency currency) {
    public Money add(Money other) {
        if (!this.currency.equals(other.currency)) {
            throw new IllegalArgumentException("Currency mismatch");
        }
        return new Money(this.amount.add(other.amount), this.currency);
    }
}
```

**Collections.unmodifiable* for defensive copying:**
```java
public class Order {
    private final List<LineItem> items;

    public Order(List<LineItem> items) {
        // Defensive copy + unmodifiable
        this.items = Collections.unmodifiableList(new ArrayList<>(items));
    }

    public List<LineItem> getItems() {
        return items; // Already unmodifiable, safe to return
    }
}
```

### Functional Interfaces and Lambdas

**Use standard functional interfaces:**
- `Function<T, R>` — Transformations
- `Predicate<T>` — Filtering
- `Consumer<T>` — Side effects
- `Supplier<T>` — Deferred computation

**Create custom functional interfaces when:**
- Standard interfaces don't match semantics
- Need checked exceptions (with custom handling)
- Domain-specific operations

```java
@FunctionalInterface
public interface Parser<T> {
    T parse(String input) throws ParseException;

    // Default methods allowed
    default Parser<T> withValidation(Predicate<T> validator) {
        return input -> {
            T result = this.parse(input);
            if (!validator.test(result)) {
                throw new IllegalArgumentException("Validation failed");
            }
            return result;
        };
    }
}
```
</functional_java>

<java_pitfalls>
## Java-Specific Pitfalls

### Null Handling

**The null problem:**
- Nulls permeate Java code
- NullPointerException is common
- Unclear from signatures what can be null

**Strategies:**
1. Use `Optional<T>` for return types (makes absence explicit)
2. Use `@NonNull`/`@Nullable` annotations (if using frameworks that support them)
3. Validate parameters early
4. Document null handling in Javadoc

**Don't fight null entirely—Java isn't Kotlin/Scala. Use defensive programming.**

### Exception Handling

**Checked vs unchecked:**
- Checked exceptions force handling (good for recoverable errors)
- Unchecked exceptions for programming errors (IllegalArgumentException, NullPointerException)
- Don't overuse checked exceptions (they pollute signatures)

**Common mistake:** Catching generic Exception and swallowing errors
```java
// BAD: Swallows all errors
try {
    doSomething();
} catch (Exception e) {
    // Silent failure
}

// GOOD: Specific exceptions, proper handling
try {
    doSomething();
} catch (IOException e) {
    logger.error("Failed to read file", e);
    throw new DataAccessException("Could not load configuration", e);
}
```

### Performance Considerations

**Premature optimization is still evil, but know the costs:**
- String concatenation in loops (use StringBuilder)
- Autoboxing in tight loops (int vs Integer)
- Stream overhead for small collections (profile first)
- Reflection overhead (cache Method/Field objects)

**Measure before optimizing. Modern JVMs are sophisticated.**
</java_pitfalls>

<common_mistakes>
## Common Mistakes from Other Language Backgrounds

<from_python>
### From Python

**Mistake: Dynamic typing habits**
- Java requires explicit types everywhere
- Type inference is limited (var for locals only)
- Use JSpecify annotations to make nullness explicit

**Mistake: Expecting duck typing**
- Java uses nominal typing (explicit interfaces)
- Implement interfaces explicitly, don't rely on structural compatibility
- Use interfaces and abstractions for polymorphism

**Mistake: Simple scripting patterns**
- Java requires classes for everything (no top-level functions)
- Boilerplate is expected (getters, constructors)
- Use records to reduce boilerplate for data classes
</from_python>

<from_cpp>
### From C/C++

**Mistake: Manual memory management thinking**
- Java has automatic garbage collection
- Don't worry about manual memory deallocation
- Trust the GC, but be aware of object retention (memory leaks via references)

**Mistake: Pointer arithmetic and low-level operations**
- Java has no pointers, no manual memory access
- Arrays are objects with bounds checking
- Use Java's higher-level abstractions

**Mistake: Multiple inheritance**
- Java has single inheritance only
- Use interfaces for multiple contracts
- Favor composition over inheritance
</from_cpp>

<from_javascript>
### From JavaScript

**Mistake: Prototype-based thinking**
- Java uses class-based inheritance
- No prototype chain manipulation
- Objects don't have dynamic properties

**Mistake: Loose typing and truthiness**
- Java is strongly typed
- No automatic type coercion (int vs double requires explicit cast)
- Booleans are not numbers (no truthiness)

**Mistake: Callback hell patterns**
- Java has checked exceptions (can't easily use callbacks everywhere)
- Use CompletableFuture for async operations
- Java 8+ has better functional support, but it's not JavaScript
</from_javascript>

<from_functional>
### From Functional Languages (Haskell, ML, Scala)

**Mistake: Expecting powerful type inference**
- Java's type inference is limited (local variables with var)
- Generics have type erasure (limitations at runtime)
- Must specify types explicitly in most contexts

**Mistake: Treating sealed classes as pure algebraic data types**
- Java 21+ has sealed classes that provide a form of algebraic data types
- Use sealed classes to eliminate boolean flags and enums that indicate object categories
- Pattern matching for instanceof (JEP 394) enables type-safe destructuring
- BUT: Don't abandon OOP patterns (Strategy, Visitor) in favor of pure pattern matching
- Sealed classes work best when combined with OOP idioms, not replacing them

**Example - Using sealed classes to replace category enums:**
```java
// BEFORE: Enum to indicate shape category
enum ShapeType { CIRCLE, RECTANGLE }

class Shape {
    private final ShapeType type;
    private final double radius; // only for circles
    private final double width, height; // only for rectangles

    // Awkward: fields only valid for certain types
}

// AFTER: Sealed classes eliminate the category enum
sealed interface Shape permits Circle, Rectangle {
    double area();
}

record Circle(double radius) implements Shape {
    public double area() { return Math.PI * radius * radius; }
}

record Rectangle(double width, double height) implements Shape {
    public double area() { return width * height; }
}
```

**Mistake: Using pattern matching to replace OOP patterns**
- Pattern matching for instanceof should NOT replace Strategy or Visitor patterns
- Strategy pattern is still the right choice for pluggable algorithms
- Visitor pattern is still appropriate for operations over stable hierarchies
- Use pattern matching for destructuring and type-safe casts, not general dispatch

**Example - When to use Strategy vs pattern matching:**
```java
// GOOD: Strategy pattern for pluggable behavior
interface PaymentStrategy {
    void processPayment(double amount);
}

class PaymentProcessor {
    private final PaymentStrategy strategy;

    public void process(double amount) {
        strategy.processPayment(amount); // OOP dispatch, strategy is pluggable
    }
}

// AVOID: Pattern matching for what should be polymorphic dispatch
class PaymentProcessor {
    public void process(Payment payment, double amount) {
        switch (payment) { // Anti-pattern: bypassing polymorphism
            case CreditCardPayment cc -> processCreditCard(cc, amount);
            case PayPalPayment pp -> processPayPal(pp, amount);
            default -> throw new IllegalArgumentException();
        }
    }
}

// GOOD: Pattern matching for destructuring and validation
public BigDecimal calculateTotal(Order order) {
    return switch (order) {
        case EmptyOrder() -> BigDecimal.ZERO;
        case SingleItemOrder(Item item) -> item.price();
        case MultiItemOrder(List<Item> items) ->
            items.stream()
                .map(Item::price)
                .reduce(BigDecimal.ZERO, BigDecimal::add);
    };
}
```

**Recognizing OO/FP equivalences to write better Java:**
- **Objects as closures:** Strategy pattern is higher-order functions in OOP form
- **Sealed classes as sum types:** Use to eliminate boolean flags and category enums
- **Streams as list comprehensions:** Functional collection processing in Java
- **Records as product types:** Immutable data carriers with value semantics

**Use functional concepts to enhance OOP, not replace it:**
- Sealed classes reduce invalid states (functional thinking)
- Strategy pattern for higher-order functions (OOP structure with FP benefits)
- Immutability by default (records, final fields)
- Pattern matching for destructuring (not general dispatch)

**Mistake: Purity everywhere**
- Java is not purely functional
- Side effects are common and expected
- Accept imperative patterns where they're clearer
- Use functional features (streams, immutability, sealed classes) to make OOP more expressive
</from_functional>

<from_kotlin>
### From Kotlin

**Mistake: Expecting null safety**
- Java has no compile-time null safety without annotations
- Use JSpecify + Checker Framework for null safety
- Can't rely on language-level nullness guarantees

**Mistake: Extension functions**
- Java has no extension functions
- Use static utility methods instead
- Can't add methods to existing classes (use composition/wrappers)

**Mistake: Data classes**
- Java requires verbose POJOs (or use records in Java 14+)
- Records help but are less flexible than Kotlin data classes
- No copy() method or destructuring
</from_kotlin>

**Staff insight:** Java is verbose, statically typed, and object-oriented. Don't fight these characteristics—work within them. Use modern Java features (streams, records, pattern matching) to reduce verbosity, but accept that Java will never be as concise as Python or as type-safe as Haskell. The Checker Framework and JSpecify annotations bridge some gaps.
</common_mistakes>

<related_skills>
## Related Skills

- **software-engineer** — Core engineering philosophy, system design, hexagonal architecture
- **object-oriented-programmer** — SOLID principles, GoF patterns, inheritance vs composition
- **functional-programmer** — When functional approaches are clearer
- **test-driven-development** — Testing philosophy and TDD principles
</related_skills>

<resources>
## Resources

- Java Version History: https://en.wikipedia.org/wiki/Java_version_history
- JSpecify Annotations: https://jspecify.dev/docs/user-guide/
- Checker Framework Manual: https://checkerframework.org/manual/
- Google Java Style Guide: https://google.github.io/styleguide/javaguide.html
- Local Checkstyle Configuration: `./assets/checkstyle.xml`
</resources>

## Summary

Java programming emphasizes:
- **Java 25+ only** — Target latest LTS, use modern features (sealed classes, pattern matching, records, virtual threads)
- **Type annotations everywhere** — JSpecify for nullness, Checker Framework for other properties (regex, format strings, locks, etc.)
- **Comprehensive Javadoc** — Mandatory for all production code, focus on "why" and constraints
- **Mandatory tooling stack** — Spotless, Checkstyle, SpotBugs, ErrorProne, JaCoCo (all in CI/CD)
- **JPMS when practical** — Start with modules, fall back to classpath if third-party libs cause problems
- **Testing as specification** — Use @Nested, @DisplayName, descriptive assertions with clear messages
- **Functional patterns enhance OO** — Sealed classes eliminate invalid states, Strategy pattern for higher-order functions, pattern matching for destructuring (not dispatch)
- **Build tool choice** — Maven for simplicity/stability, Gradle for flexibility/performance

**All new Java projects must use:**
- Java 25+ (latest LTS)
- JSpecify annotations for nullness
- Checker Framework with multiple checkers enabled (nullness, regex, format string, index, lock, etc.)
- Spotless (formatting), Checkstyle (style), SpotBugs (bugs), ErrorProne (bugs), JaCoCo (coverage)
- Comprehensive Javadoc on all public APIs and tests
- Maven or Gradle with CI/CD integration
- Builds fail on violations (no warnings mode)
- JPMS (module-info.java) unless third-party libraries prevent it

**Aggressive Java feature adoption philosophy:**
- Use sealed classes to eliminate category enums and invalid states
- Use pattern matching for destructuring (not for replacing OOP patterns like Strategy/Visitor)
- Recognize OO/FP equivalences (objects as closures, sealed classes as sum types)
- Don't abandon OOP for pure FP—use functional concepts to enhance object-oriented design

Java is a pragmatic language. Work within its idioms rather than fighting them. **Type annotations (JSpecify + Checker Framework), comprehensive Javadoc, and modern tooling are mandatory for all production code.** Document thoroughly—assume future maintainers (including LLMs) need to understand intent, not just implementation.
