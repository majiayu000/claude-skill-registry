---
name: gradle-dependency-management
description: |
  Manages Gradle dependencies using version catalogs, BOMs, and dependency constraints.
  Use when setting up dependency management, centralizing versions, resolving conflicts,
  or configuring multi-module dependency sharing. Triggers on "setup version catalog",
  "centralize dependencies", "resolve version conflict", or "configure Gradle BOM".
  Works with gradle/libs.versions.toml and includes Bill of Materials, dependency constraints,
  and Spring Boot/GCP BOM integration.

---

# Gradle Dependency Management

## Table of Contents

- [Purpose](#purpose)
- [When to Use](#when-to-use)
- [Quick Start](#quick-start)
- [Instructions](#instructions)
- [Examples](#examples)
- [Requirements](#requirements)
- [Commands](#commands)
- [See Also](#see-also)

## Purpose

Centralize and manage dependencies effectively across Gradle projects using version catalogs, BOMs, and dependency constraints. This skill helps you standardize versions, resolve conflicts, and maintain security across multi-module builds.

## When to Use

Use this skill when you need to:
- Centralize dependency versions across multi-module projects
- Create type-safe dependency references with version catalogs
- Resolve dependency version conflicts
- Enforce consistent dependency versions across a team
- Integrate Spring Boot or GCP BOMs for curated dependency sets
- Lock dependency versions for reproducible builds
- Manage transitive dependencies with constraints

## Quick Start

Create a version catalog in `gradle/libs.versions.toml`:

```toml
[versions]
spring-boot = "3.5.5"
junit = "5.11.0"

[libraries]
spring-boot-starter-web = { module = "org.springframework.boot:spring-boot-starter-web" }
junit-jupiter = { module = "org.junit.jupiter:junit-jupiter", version.ref = "junit" }

[bundles]
spring-boot-web = ["spring-boot-starter-web"]
testing = ["junit-jupiter"]

[plugins]
spring-boot = { id = "org.springframework.boot", version.ref = "spring-boot" }
```

Configure in `settings.gradle.kts`:

```kotlin
dependencyResolutionManagement {
    versionCatalogs {
        create("libs") {
            from(files("gradle/libs.versions.toml"))
        }
    }
}
```

Use in `build.gradle.kts`:

```kotlin
plugins {
    alias(libs.plugins.spring.boot)
}

dependencies {
    implementation(libs.spring.boot.starter.web)
    testImplementation(libs.bundles.testing)
}
```

## Instructions

### Step 1: Set Up Version Catalog

Create `gradle/libs.versions.toml` with your project's dependencies:

```toml
[versions]
spring-boot = "3.5.5"
spring-cloud = "2024.0.1"
spring-cloud-gcp = "6.1.1"
mapstruct = "1.6.3"
testcontainers = "1.21.0"
junit = "5.11.0"
mockito = "5.14.0"

[libraries]
# Spring Boot
spring-boot-starter-web = { module = "org.springframework.boot:spring-boot-starter-web" }
spring-boot-starter-actuator = { module = "org.springframework.boot:spring-boot-starter-actuator" }
spring-boot-starter-data-jpa = { module = "org.springframework.boot:spring-boot-starter-data-jpa" }
spring-boot-starter-test = { module = "org.springframework.boot:spring-boot-starter-test" }

# GCP
spring-cloud-gcp-starter = { module = "com.google.cloud:spring-cloud-gcp-starter" }
spring-cloud-gcp-pubsub = { module = "com.google.cloud:spring-cloud-gcp-starter-pubsub" }
google-cloud-secretmanager = { module = "com.google.cloud:google-cloud-secretmanager", version = "2.2.0" }

# Database
postgresql = { module = "org.postgresql:postgresql" }
flyway-core = { module = "org.flywaydb:flyway-core" }

# MapStruct
mapstruct = { module = "org.mapstruct:mapstruct", version.ref = "mapstruct" }
mapstruct-processor = { module = "org.mapstruct:mapstruct-processor", version.ref = "mapstruct" }

# Testing
junit-jupiter = { module = "org.junit.jupiter:junit-jupiter", version.ref = "junit" }
mockito-core = { module = "org.mockito:mockito-core", version.ref = "mockito" }
testcontainers-junit = { module = "org.testcontainers:junit-jupiter", version.ref = "testcontainers" }
testcontainers-postgresql = { module = "org.testcontainers:postgresql", version.ref = "testcontainers" }

[bundles]
spring-boot-web = ["spring-boot-starter-web", "spring-boot-starter-actuator"]
spring-data = ["spring-boot-starter-data-jpa", "postgresql", "flyway-core"]
gcp = ["spring-cloud-gcp-starter", "spring-cloud-gcp-pubsub", "google-cloud-secretmanager"]
testing = ["junit-jupiter", "mockito-core", "spring-boot-starter-test"]
testcontainers = ["testcontainers-junit", "testcontainers-postgresql"]

[plugins]
spring-boot = { id = "org.springframework.boot", version.ref = "spring-boot" }
spring-dependency-management = { id = "io.spring.dependency-management", version = "1.1.7" }
jib = { id = "com.google.cloud.tools.jib", version = "3.4.4" }
```

### Step 2: Configure in Settings File

Update `settings.gradle.kts` to use the version catalog:

```kotlin
dependencyResolutionManagement {
    versionCatalogs {
        create("libs") {
            from(files("gradle/libs.versions.toml"))
        }
    }
}

// For multi-module projects
rootProject.name = "supplier-charges"
include("shared-domain")
include("supplier-charges-hub")
```

### Step 3: Use in Build Scripts

In `build.gradle.kts`, use type-safe dependency references:

```kotlin
plugins {
    alias(libs.plugins.spring.boot)
    alias(libs.plugins.spring.dependency.management)
}

dependencies {
    // Single dependencies
    implementation(libs.spring.boot.starter.web)
    implementation(libs.mapstruct)
    annotationProcessor(libs.mapstruct.processor)

    // Bundles (groups of related dependencies)
    implementation(libs.bundles.spring.boot.web)
    implementation(libs.bundles.gcp)
    testImplementation(libs.bundles.testing)
    testImplementation(libs.bundles.testcontainers)
}
```

### Step 4: Manage BOMs for Curated Versions

Use Bill of Materials to control transitive dependencies:

```kotlin
// build.gradle.kts
dependencyManagement {
    imports {
        mavenBom("com.google.cloud:spring-cloud-gcp-dependencies:6.1.1")
        mavenBom("org.springframework.cloud:spring-cloud-dependencies:2024.0.1")
    }
}

dependencies {
    // No version needed - comes from BOM
    implementation("com.google.cloud:spring-cloud-gcp-starter")
    implementation("org.springframework.cloud:spring-cloud-config-client")
}
```

### Step 5: Resolve Conflicts with Constraints

Use dependency constraints to force specific versions without declaring the dependency:

```kotlin
dependencies {
    // Actual dependencies
    implementation("org.springframework.boot:spring-boot-starter-web")

    // Constraints - enforce versions of transitive dependencies
    constraints {
        implementation("org.bouncycastle:bcprov-jdk15on:1.70")
        implementation("ch.qos.logback:logback-core:1.5.19")
    }
}
```

To exclude a problematic transitive dependency:

```kotlin
dependencies {
    implementation("com.example:library:1.0") {
        exclude(group = "commons-logging", module = "commons-logging")
    }
}
```

## Examples

### Example 1: Multi-Module with Shared Catalog

```toml
# gradle/libs.versions.toml
[versions]
spring-boot = "3.5.5"

[libraries]
spring-boot-starter-web = { module = "org.springframework.boot:spring-boot-starter-web" }
spring-boot-starter-test = { module = "org.springframework.boot:spring-boot-starter-test" }

[plugins]
spring-boot = { id = "org.springframework.boot", version.ref = "spring-boot" }
```

```kotlin
// Root settings.gradle.kts
rootProject.name = "supplier-charges"

dependencyResolutionManagement {
    versionCatalogs {
        create("libs") {
            from(files("gradle/libs.versions.toml"))
        }
    }
}

include("shared-domain")
include("supplier-charges-hub")
include("supplier-charges-worker")
```

```kotlin
// shared-domain/build.gradle.kts
plugins {
    id("java-library")
}

dependencies {
    api(libs.spring.boot.starter.web)
}
```

```kotlin
// supplier-charges-hub/build.gradle.kts
plugins {
    alias(libs.plugins.spring.boot)
}

dependencies {
    implementation(project(":shared-domain"))
    testImplementation(libs.spring.boot.starter.test)
}
```

### Example 2: Resolving Dependency Conflicts

```kotlin
// When Spring Boot and external library have conflicting versions
dependencies {
    implementation("org.springframework.boot:spring-boot-starter-web")
    implementation("com.external:library:1.0")  // Uses old commons-lang3

    // Force the newer version
    constraints {
        implementation("org.apache.commons:commons-lang3:3.18.0")
    }
}

// Or use resolutionStrategy
configurations.all {
    resolutionStrategy {
        force("com.google.guava:guava:32.1.3-jre")
        force("org.apache.commons:commons-compress:1.26.0")
    }
}
```

### Example 3: Security-Focused Constraints

```toml
# gradle/libs.versions.toml with security-critical versions
[constraints]
bouncycastle = "1.70"           # Cryptography
logback = "1.5.19"              # Logging
jackson = "2.17.2"              # JSON processing
commons-lang3 = "3.18.0"        # Common utilities
```

```kotlin
// build.gradle.kts
dependencies {
    implementation("org.springframework.boot:spring-boot-starter-web")

    constraints {
        implementation("org.bouncycastle:bcprov-jdk15on:${libs.versions.bouncycastle.get()}")
        implementation("ch.qos.logback:logback-core:${libs.versions.logback.get()}")
        implementation("com.fasterxml.jackson.core:jackson-databind:${libs.versions.jackson.get()}")
        implementation("org.apache.commons:commons-lang3:${libs.versions.commons.lang3.get()}")
    }
}
```

### Example 4: Using Version Ref in BOM

```toml
# gradle/libs.versions.toml
[versions]
spring-cloud-gcp = "6.1.1"

[libraries]
spring-cloud-gcp-bom = { module = "com.google.cloud:spring-cloud-gcp-dependencies", version.ref = "spring-cloud-gcp" }
spring-cloud-gcp-starter = { module = "com.google.cloud:spring-cloud-gcp-starter" }
spring-cloud-gcp-pubsub = { module = "com.google.cloud:spring-cloud-gcp-starter-pubsub" }

[bundles]
gcp = ["spring-cloud-gcp-starter", "spring-cloud-gcp-pubsub"]
```

```kotlin
// build.gradle.kts
dependencyManagement {
    imports {
        mavenBom(libs.spring.cloud.gcp.bom.get().toString())
    }
}

dependencies {
    implementation(libs.bundles.gcp)
}
```

## Requirements

- Gradle 7.0+ (version catalogs stable since Gradle 7.0)
- `settings.gradle.kts` file in project root
- Spring Boot Gradle plugin for Spring Boot projects (optional but recommended)

## Commands

```bash
# List all dependencies
./gradlew dependencies

# Show dependency tree for specific configuration
./gradlew dependencies --configuration implementation

# Show why a dependency is included
./gradlew dependencyInsight --dependency spring-core

# Refresh dependencies (force re-download)
./gradlew build --refresh-dependencies

# Lock dependency versions for reproducibility
./gradlew dependencies --write-locks

# Verify against lock files
./gradlew dependencies --verify-locks

# Generate HTML dependency report
./gradlew htmlDependencyReport
```

## See Also

- [Gradle Version Catalogs Documentation](https://docs.gradle.org/current/userguide/platforms.html)
- [Spring Boot BOM Integration](https://docs.spring.io/spring-boot/docs/current/gradle-plugin/reference/)
- `gradle-performance-optimization` - Enable build cache for faster dependency resolution
- `gradle-troubleshooting` - Resolve dependency conflict issues
