---
name: Kotlin Tooling Standards
description: Build tools (Gradle KTS), Static Analysis (Detekt), and Testing standards.
metadata:
  labels: [kotlin, tooling, gradle, detekt, ktlint, testing]
  triggers:
    files: ['build.gradle.kts', 'libs.versions.toml', 'detekt.yml']
    keywords: [gradle, kts, detekt, mockk, junit]
---

# Kotlin Tooling Standards

## **Priority: P2 (RECOMMENDED)**

Consistent build and quality verification tools.

## Implementation Guidelines

- **Gradle DSL**: Use Kotlin DSL (`build.gradle.kts`) exclusively. It provides type safety and better IDE support.
- **Version Management**: Use Version Catalogs (`libs.versions.toml`).
- **Linter**: Use **Ktlint** for formatting and **Detekt** for complexity/code-smell analysis.
- **Testing**: Use **MockK** for mocking (first-class Kotlin support). Use **JUnit 5**.
- **Assertions**: Use **Truth** or **Kotest Assertions** for fluent reading.

## Anti-Patterns

- **Groovy Gradle**: Avoid legacy `build.gradle` files.
- **Mockito (Java)**: Avoid Mockito if possible; `when/then` syntax conflicts with Kotlin `when`. Use MockK (`every/verify`).
- **Hardcoded Versions**: Don't put versions in build files. Use the catalog.

## Code

For full `MockK` testing templates and `libs.versions.toml` setup:
[references/testing-tooling.md](references/testing-tooling.md)

```kotlin
// Modern Gradle KTS + Version Catalog
dependencies {
    implementation(libs.kotlin.stdlib)
    testImplementation(libs.mockk)
}

// Concise MockK Verify
verify(exactly = 1) { repo.getUser("1") }
```

## Related Topics

best-practices | testing
