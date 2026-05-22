---
name: gradle-testing-setup
description: |
  Configures comprehensive testing in Gradle including JUnit 5, TestContainers,
  test separation (unit vs integration), and code coverage with JaCoCo.
  Use when asked to "set up JUnit 5", "configure TestContainers", "separate integration tests",
  or "add code coverage".
  Works with build.gradle.kts, test source sets, and CI/CD configurations.
---

# Gradle Testing Setup

## Table of Contents

- [When to Use This Skill](#when-to-use-this-skill)
- [Quick Start](#quick-start)
- [Instructions](#instructions)
- [Examples](#examples)
- [Commands Reference](#commands-reference)
- [See Also](#see-also)

## When to Use This Skill

Use this skill when you need to:
- Set up JUnit 5 (Jupiter) testing framework
- Configure TestContainers for integration tests with real databases
- Separate unit tests from integration tests
- Measure code coverage with JaCoCo
- Enforce minimum code coverage thresholds
- Configure parallel test execution for faster test runs
- Set up test logging and reporting in CI/CD
- Create separate source sets for integration tests

## Quick Start

Add to `build.gradle.kts`:

```kotlin
dependencies {
    testImplementation("org.springframework.boot:spring-boot-starter-test")
    testImplementation("org.junit.jupiter:junit-jupiter")
    testImplementation("org.testcontainers:testcontainers:1.21.0")
    testImplementation("org.testcontainers:junit-jupiter:1.21.0")
    testImplementation("org.testcontainers:postgresql:1.21.0")

    testRuntimeOnly("org.junit.platform:junit-platform-launcher")
}

plugins {
    id("jacoco")
}

tasks.test {
    useJUnitPlatform()
}

tasks.jacocoTestReport {
    dependsOn(tasks.test)
    finalizedBy(tasks.jacocoTestCoverageVerification)
}

tasks.check {
    dependsOn(tasks.jacocoTestReport)
}
```

Run tests:

```bash
./gradlew test                    # Run unit tests
./gradlew test jacocoTestReport   # With coverage report
./gradlew integrationTest         # Run integration tests (if configured)
```

## Instructions

### Step 1: Configure JUnit 5 (Jupiter)

Add JUnit 5 dependencies:

```kotlin
dependencies {
    testImplementation("org.springframework.boot:spring-boot-starter-test")
    testImplementation("org.junit.jupiter:junit-jupiter:5.11.0")
    testRuntimeOnly("org.junit.platform:junit-platform-launcher:1.11.0")
}

tasks.test {
    useJUnitPlatform()
}
```

**Advanced JUnit 5 configuration**:

```kotlin
tasks.test {
    useJUnitPlatform {
        // Include/exclude tags
        includeTags("unit", "integration")
        excludeTags("slow", "manual")

        // Include/exclude by engine
        includeEngines("junit-jupiter")
        excludeEngines("junit-vintage")
    }

    // Filter tests by pattern
    filter {
        includeTestsMatching("*Test")
        includeTestsMatching("*Tests")
        excludeTestsMatching("*IntegrationTest")
    }

    // Parallel test execution
    maxParallelForks = Runtime.getRuntime().availableProcessors() / 2

    // System properties for tests
    systemProperty("junit.jupiter.execution.parallel.enabled", "true")
    systemProperty("junit.jupiter.execution.parallel.mode.default", "concurrent")

    // Detailed logging
    testLogging {
        events("passed", "skipped", "failed", "standardOut")
        showExceptions = true
        showStackTraces = true
        showCauses = true
        exceptionFormat = org.gradle.api.tasks.testing.logging.TestExceptionFormat.FULL
    }
}
```

### Step 2: Set Up TestContainers for Integration Tests

Add TestContainers dependencies:

```kotlin
dependencies {
    testImplementation("org.testcontainers:testcontainers:1.21.0")
    testImplementation("org.testcontainers:junit-jupiter:1.21.0")
    testImplementation("org.testcontainers:postgresql:1.21.0")
    testImplementation("org.testcontainers:gcloud:1.21.0")  // For Pub/Sub emulator
}

tasks.test {
    useJUnitPlatform()

    // Docker socket configuration
    systemProperty("testcontainers.reuse.enable", "true")
}
```

**Example integration test with TestContainers**:

```java
@SpringBootTest
@Testcontainers
class SupplierChargesIntegrationTest {

    @Container
    static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:15")
        .withDatabaseName("testdb")
        .withUsername("test")
        .withPassword("test");

    @Container
    static GenericContainer<?> pubsub = new GenericContainer<>("google/cloud-sdk:emulators")
        .withExposedPorts(8085)
        .withCommand("gcloud", "beta", "emulators", "pubsub", "start", "--host-port=0.0.0.0:8085");

    @DynamicPropertySource
    static void configureProperties(DynamicPropertyRegistry registry) {
        registry.add("spring.datasource.url", postgres::getJdbcUrl);
        registry.add("spring.datasource.username", postgres::getUsername);
        registry.add("spring.datasource.password", postgres::getPassword);
        registry.add("spring.cloud.gcp.pubsub.emulator-host",
            () -> "localhost:" + pubsub.getMappedPort(8085));
    }

    @Test
    void testDatabaseAndPubSub() {
        // Test with real PostgreSQL and Pub/Sub emulator
    }
}
```

### Step 3: Separate Unit and Integration Tests

Create separate source sets and tasks:

```kotlin
sourceSets {
    create("integrationTest") {
        java {
            srcDir("src/integrationTest/java")
            compileClasspath += sourceSets.main.get().output + sourceSets.test.get().output
            runtimeClasspath += sourceSets.main.get().output + sourceSets.test.get().output
        }
        resources {
            srcDir("src/integrationTest/resources")
        }
    }
}

// Create integration test task
val integrationTest = tasks.register<Test>("integrationTest") {
    description = "Run integration tests"
    group = "verification"

    testClassesDirs = sourceSets["integrationTest"].output.classesDirs
    classpath = sourceSets["integrationTest"].runtimeClasspath

    useJUnitPlatform()

    // Run after unit tests
    shouldRunAfter(tasks.test)

    // Logging
    testLogging {
        events("passed", "skipped", "failed")
    }
}

// Include integration tests in overall check
tasks.check {
    dependsOn(integrationTest)
}
```

**Directory structure**:

```
src/
├── main/
│   └── java/
├── test/                          # Unit tests
│   ├── java/
│   │   └── com/example/
│   │       ├── ServiceTest.java
│   │       └── ControllerTest.java
│   └── resources/
│       └── application-test.yml
└── integrationTest/               # Integration tests
    ├── java/
    │   └── com/example/
    │       └── ServiceIntegrationTest.java
    └── resources/
        └── application-integration.yml
```

### Step 4: Configure Code Coverage with JaCoCo

Add JaCoCo plugin and configuration:

```kotlin
plugins {
    id("jacoco")
}

jacoco {
    toolVersion = "0.8.12"
}

tasks.jacocoTestReport {
    dependsOn(tasks.test)

    reports {
        xml.required = true
        html.required = true
        csv.required = false

        xml.outputLocation = layout.buildDirectory.file("reports/jacoco/test/jacocoTestReport.xml")
        html.outputLocation = layout.buildDirectory.dir("reports/jacoco/test/html")
    }

    finalizedBy(tasks.jacocoTestCoverageVerification)
}

// Enforce coverage minimums
tasks.jacocoTestCoverageVerification {
    violationRules {
        // Overall coverage requirement
        rule {
            element = "BUNDLE"
            limit {
                minimum = BigDecimal("0.60")  // 60% minimum
            }
        }

        // Class-level requirements
        rule {
            element = "CLASS"
            excludes = listOf("**/config/*", "**/dto/*")
            limit {
                counter = "LINE"
                value = "COVEREDRATIO"
                minimum = BigDecimal("0.50")  // 50% per class
            }
        }

        // Method-level requirements
        rule {
            element = "METHOD"
            limit {
                counter = "LINE"
                value = "COVEREDRATIO"
                minimum = BigDecimal("0.40")  // 40% per method
            }
        }
    }
}

// Generate report after tests
tasks.test {
    finalizedBy(tasks.jacocoTestReport)
}

// Include in overall check
tasks.check {
    dependsOn(tasks.jacocoTestReport)
}
```

### Step 5: Configure Test Logging

Use prettier test output with test-logger plugin:

```kotlin
plugins {
    id("com.adarshr.test-logger") version "4.0.0"
}

testlogger {
    theme = "mocha"  // Options: plain, standard, mocha, standard-parallel, mocha-parallel
    showExceptions = true
    showStackTraces = true
    showFullStackTraces = false
    showCauses = true
    slowThreshold = 2000  // Warn for tests > 2 seconds
    showSummary = true
    showPassed = true
    showSkipped = true
    showFailed = true
    showStandardStreams = false
}
```

### Step 6: Configure Docker for TestContainers

Ensure Docker is properly configured:

```bash
# Verify Docker is running
docker ps

# On macOS with Docker Desktop
export TESTCONTAINERS_DOCKER_SOCKET_OVERRIDE=/var/run/docker.sock
export DOCKER_HOST=unix://${HOME}/.docker/run/docker.sock

# Run tests
./gradlew test
```

In `gradle.properties` for CI/CD:

```properties
org.gradle.logging.level=info
testcontainers.reuse.enable=true
```

## Examples

### Example: Running Different Test Suites

```bash
# Unit tests only
./gradlew test

# Integration tests only
./gradlew integrationTest

# All tests
./gradlew check

# With coverage report
./gradlew test jacocoTestReport

# Specific test class
./gradlew test --tests "com.example.ServiceTest"

# Tests matching pattern
./gradlew test --tests "*IntegrationTest"

# Single test method
./gradlew test --tests "com.example.ServiceTest.testMethod"

# Verbose output
./gradlew test --info

# Continuous mode (rerun on changes)
./gradlew test --continuous
```


For advanced examples including TestContainers integration, GitHub Actions with coverage reports, and CI coverage verification, see [references/advanced-examples.md](references/advanced-examples.md).

## Commands Reference

See [references/commands-and-troubleshooting.md](references/commands-and-troubleshooting.md) for complete command reference and troubleshooting guide.

## See Also

- [gradle-spring-boot-integration](../gradle-spring-boot-integration/SKILL.md) - Spring Boot test starters
- [gradle-performance-optimization](../gradle-performance-optimization/SKILL.md) - Parallel test execution
- [gradle-ci-cd-integration](../gradle-ci-cd-integration/SKILL.md) - CI/CD test reporting
- [JUnit 5 Documentation](https://junit.org/junit5/)
- [TestContainers Documentation](https://www.testcontainers.org/)
