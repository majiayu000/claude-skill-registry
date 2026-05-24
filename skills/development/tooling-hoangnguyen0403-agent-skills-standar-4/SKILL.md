---
name: Java Tooling Standards
description: Standards for build tools (Maven/Gradle) and static analysis.
metadata:
  labels: [java, tooling, maven, gradle, checkstyle]
  triggers:
    files: ['pom.xml', 'build.gradle', 'build.gradle.kts']
    keywords: [build, dependency, plugin, sdk, lint]
---

# Java Tooling Standards

## **Priority: P2 (RECOMMENDED)**

Standardized build and tooling configuration for consistent environments.

## Implementation Guidelines

- **JDK Management**: Use `.sdkmanrc` or `.java-version` to lock JDK versions (Target LTS: 17 or 21).
- **Maven**: Use `pom.xml` with `<dependencyManagement>` for version control. Use wrapper (`mvnw`).
- **Gradle**: Prefer Kotlin DSL (`build.gradle.kts`). Use version catalogs (`libs.versions.toml`). Use wrapper (`gradlew`).
- **Linter**: Use **Spotless** or **Checkstyle** (Google Style) to enforce formatting.
- **Static Analysis**: Integrate **SpotBugs** or **SonarLint** for deeper issue detection.
- **Docker**: Use multi-stage builds. Use `eclipse-temurin` or `distroless` images.

## Anti-Patterns

- **Global Installs**: Relying on system Maven/Gradle. Always use wrappers.
- **Fat Jars**: Avoid massive uber-jars if possible; prefer layered Docker images for caching.
- **Snapshot Dependencies**: Do not rely on `-SNAPSHOT` versions in production builds.

## Code

```kotlin
// build.gradle.kts (Gradle Kotlin DSL)
plugins {
    java
    id("com.diffplug.spotless") version "6.23.3"
}

java {
    toolchain {
        languageVersion.set(JavaLanguageVersion.of(21))
    }
}

spotless {
    java {
        googleJavaFormat()
    }
}
```

## Related Topics

language | best-practices | testing
