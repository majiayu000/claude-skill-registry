---
name: gradle-standards
description: >
  Gradle build configuration standards for Java projects. Covers version catalogs,
  dependency bundles, multi-module setup, BOM management, and common troubleshooting.
  Use when configuring Gradle builds or reviewing dependency management.
compatibility: Java projects using Gradle 8.x or 9.x
metadata:
  version: "2.0.0"
  technology: java
  category: build
  tags:
    - gradle
    - java
    - dependencies
    - build
---

# Gradle Standards

Standards for Gradle configuration in Java projects, including version catalogs, dependency bundles, and multi-module setup.

## When to use this skill

- Setting up a new Gradle project
- Adding or updating dependencies
- Configuring multi-module builds
- Troubleshooting dependency conflicts
- Migrating to version catalogs
- Cleaning up unused dependencies
- Optimizing build performance
- When asked for "gradle dependencies cleanup"

## Skill Contents

### Sections

- [When to use this skill](#when-to-use-this-skill) (L23-L33)
- [Quick Start](#quick-start) (L61-L89)
- [Key Principles](#key-principles) (L90-L102)
- [Version Alignment](#version-alignment) (L103-L130)
- [References](#references) (L131-L142)
- [Related Rules](#related-rules) (L143-L147)
- [Dependency Resolution Stack](#dependency-resolution-stack) (L148-L187)
- [Related Skills](#related-skills) (L188-L195)

### Available Resources

**📚 references/** - Detailed documentation
- [cleanup workflow](references/cleanup-workflow.md)
- [multi module](references/multi-module.md)
- [native dependency locking](references/native-dependency-locking.md)
- [optimization](references/optimization.md)
- [scope optimization](references/scope-optimization.md)
- [troubleshooting](references/troubleshooting.md)
- [unused detection](references/unused-detection.md)
- [version catalogs](references/version-catalogs.md)

---

## Quick Start

### 1. Version Centralization (Required)

All versions MUST be centralized in `gradle/libs.versions.toml`:

```toml
[versions]
spring-boot = "3.5.9"
grpc = "1.78.0"

[libraries]
spring-boot-starter-web = { module = "org.springframework.boot:spring-boot-starter-web", version.ref = "spring-boot" }
spring-boot-starter-actuator = { module = "org.springframework.boot:spring-boot-starter-actuator", version.ref = "spring-boot" }
```

### 2. Use in build.gradle

```groovy
dependencies {
    // ✅ CORRECT: Use version catalog with explicit dependencies
    implementation libs.spring.boot.starter.web
    implementation libs.spring.boot.starter.actuator

    // ❌ NEVER: Hardcode versions
    // implementation "org.springframework.boot:spring-boot-starter-web:3.5.9"
}
```

## Key Principles

| Principle | Description |
|-----------|-------------|
| **Centralize Versions** | All versions in `libs.versions.toml`, never inline |
| **Explicit Dependencies** | Declare each dependency explicitly for clarity |
| **Use Native Locking** | Use Gradle's native dependency locking (Gradle 9+ recommended) |
| **Never Downgrade** | Don't replace existing versions with older ones |
| **Trust BOMs** | Spring Boot BOM manages transitive dependencies |
| **Platform Over Enforce** | Use `platform()`, never `enforcedPlatform()` |
| **Use resolutionStrategy** | Use Gradle's native `resolutionStrategy` for version control |
| **Lock Dependencies** | Generate `gradle.lockfile` for ALL submodules (use `build --write-locks`) |

## Version Alignment

Use Gradle's native `resolutionStrategy` to ensure all modules in a library group use the same version:

```groovy
// build.gradle - Native Gradle version alignment
configurations.configureEach {
    resolutionStrategy {
        // Force specific versions for security or compatibility
        force libs.jackson.core
        force libs.jackson.databind

        // Align all modules in a group
        eachDependency { details ->
            if (details.requested.group == 'io.grpc') {
                details.useVersion libs.versions.grpc.get()
            }
        }
    }
}
```

This approach is preferred because:
- Subprojects can declare exactly what they need
- Dependencies are explicit and visible in build files
- No external plugins required (built into Gradle)
- First-class support in Gradle 9+

## References

| Reference | Description |
|-----------|-------------|
| [references/version-catalogs.md](references/version-catalogs.md) | Complete version catalog guide |
| [references/multi-module.md](references/multi-module.md) | Multi-module project setup |
| [references/native-dependency-locking.md](references/native-dependency-locking.md) | **Gradle native locking (Gradle 9+ recommended)** |
| [references/cleanup-workflow.md](references/cleanup-workflow.md) | Dependency cleanup process |
| [references/unused-detection.md](references/unused-detection.md) | Finding unused dependencies |
| [references/optimization.md](references/optimization.md) | Build optimization techniques |
| [references/troubleshooting.md](references/troubleshooting.md) | Common issues and solutions |

## Related Rules

- [java-gradle-best-practices](.cursor/rules/java-gradle-best-practices/java-gradle-best-practices.mdc) - Full Gradle configuration reference
- [java-versions-and-dependencies](.cursor/rules/java-versions-and-dependencies/java-versions-and-dependencies.mdc) - Version management policies

## Dependency Resolution Stack

```
┌─────────────────────────────────────────────────────────────────────┐
│  1. VERSION CATALOG (libs.versions.toml)                            │
│     Single source of truth for declared versions                    │
├─────────────────────────────────────────────────────────────────────┤
│  2. RESOLUTION STRATEGY (build.gradle)                              │
│     Use Gradle's native resolutionStrategy for:                     │
│     - force() for security fixes                                    │
│     - eachDependency for group alignment                            │
│     - dependencySubstitution for module replacement                 │
├─────────────────────────────────────────────────────────────────────┤
│  3. LOCK FILE (gradle.lockfile)                                     │
│     Native Gradle locking (Gradle 9+ recommended)                   │
│     Captures EXACT resolved versions                                │
│                                                                     │
│  ⚠️  CRITICAL: Multi-module projects need lockfiles for ALL modules │
│     Use: ./gradlew build --write-locks -x test                      │
│     NOT: ./gradlew dependencies --write-locks (root only!)          │
└─────────────────────────────────────────────────────────────────────┘
```

**Lock File:**
- [Native locking](references/native-dependency-locking.md) - Built-in, no plugins, recommended for Gradle 9+

**Multi-Module Lockfile Generation:**

```bash
# ✅ CORRECT: Generates lockfiles for ALL submodules
./gradlew build --write-locks -x test

# ❌ WRONG: Only generates for ROOT project
./gradlew dependencies --write-locks

# Verify coverage (lockfiles should ≈ build.gradle files)
find . -name "gradle.lockfile" | wc -l
find . -name "build.gradle" | wc -l
```

## Related Skills

| Skill | Purpose |
|-------|---------|
| `dependency-management` | Version catalogs and BOMs |
| `dependabot-security` | Security vulnerability fixes |
| `java-coverage` | JaCoCo configuration in Gradle |
| `java-testing` | Test configuration with Spock |
<!-- AUTO-GENERATED FILE - DO NOT EDIT DIRECTLY -->
<!-- Source: bitsoex/ai-code-instructions → java/skills/gradle-standards/SKILL.md -->
<!-- To modify, edit the source file and run the distribution workflow -->

