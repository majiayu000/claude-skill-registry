---
name: upgrade-spring-boot-3-5
description: >
  Upgrade Java services to Spring Boot 3.5.x with all required dependency updates.
  Use when projects need to upgrade from older Spring Boot versions to 3.5.9+.
compatibility: Java projects using Gradle with Spring Boot
metadata:
  version: "2.0.0"
  technology: java
  category: modernization
  tags:
    - spring-boot
    - upgrade
    - dependencies
---

# Upgrade Spring Boot 3.5.x

Upgrade Java services to Spring Boot 3.5.9 with all required dependency updates.

## When to Use

- Project uses Spring Boot 3.4.x or earlier
- Preparing for Spring Boot 4 (stay on latest or latest-1 patch of 3.5.x)
- Need features from Spring Boot 3.5.x
- Preparing for Java 25 upgrade (requires Spring Boot 3.5.x first)
- When asked to "upgrade to recommended versions"

## Skill Contents

### Sections

- [When to Use](#when-to-use) (L21-L28)
- [Target Versions](#target-versions) (L48-L62)
- [Version Unification](#version-unification) (L63-L68)
- [Quick Start](#quick-start) (L69-L127)
- [References](#references) (L128-L133)
- [Related Command](#related-command) (L134-L137)
- [Related Skills](#related-skills) (L138-L143)

### Available Resources

**📚 references/** - Detailed documentation
- [troubleshooting](references/troubleshooting.md)

---

## Target Versions

| Component | Version | Notes |
|-----------|---------|-------|
| **Spring Boot** | **3.5.9** | Latest (min 3.5.9) - preparing for Spring Boot 4 |
| **Spring Cloud** | **2025.0.0** | Required for Spring Boot 3.5.x |
| **Spring Dependency Management** | **1.1.7** | Required plugin version |
| **Gradle** | **9.2.1** | Recommended for all projects |
| **JUnit** | **5.14.2** | Testing (via BOM) |
| **Spock** | **2.4-groovy-4.0** | Groovy testing (use -groovy-5.0 for Java 25) |
| **JaCoCo** | **0.8.14** | Code coverage |
| **SonarQube Plugin** | **7.2.2.6593** | Code analysis |
| **bitso-rds-iam-authn** | **2.0.0** | If using RDS IAM |
| **bitso-commons-redis** | **4.2.1** | If using Redis |

## Version Unification

**CRITICAL**: Ensure Spring Boot version is defined in only ONE place.

See [version-centralization.md](.claude/skills/dependency-management/references/version-centralization.md) for details on avoiding multiple version definitions.

## Quick Start

### 1. Update Version Catalog

```toml
# gradle/libs.versions.toml
[versions]
springBoot = "3.5.9"
springCloud = "2025.0.0"  # CRITICAL for 3.5.x compatibility
spock = "2.4-groovy-4.0"

[plugins]
spring-boot = { id = "org.springframework.boot", version.ref = "springBoot" }
spring-dependency-management = { id = "io.spring.dependency-management", version = "1.1.7" }
```

### 2. Update Gradle Wrapper

```bash
./gradlew wrapper --gradle-version=9.2.1
```

### 3. Add JUnit Platform Launcher

Required for Gradle 9.x with JUnit 5.11+:

```groovy
subprojects {
    plugins.withType(JavaPlugin).configureEach {
        dependencies {
            testRuntimeOnly libs.junit.platform.launcher
        }
    }
}
```

### 4. Update Redis Libraries (if applicable)

Check if project uses Redis:

```bash
grep -r "bitso.commons:redis\|jedis" --include="*.gradle" --include="*.toml" .
```

If Redis is used, update:

```toml
[versions]
bitso-commons-redis = "4.2.1"
jedis4-utils = "3.0.0"
```

### 5. Validate

```bash
./gradlew clean build -x test
./gradlew test
```

## References

| Reference | Content |
|-----------|---------|
| [references/troubleshooting.md](references/troubleshooting.md) | Common issues and solutions |

## Related Command

This skill is referenced by: `/upgrade-to-recommended-versions` (see `java/commands/`)

## Related Skills

| Skill | Purpose |
|-------|---------|
| [upgrade-java-25](.claude/skills/upgrade-java-25/SKILL.md) | Java 25 upgrade (requires Spring Boot 3.5.x first) |
| [upgrade-gradle-9](.claude/skills/upgrade-gradle-9/SKILL.md) | Gradle 9 upgrade patterns |
<!-- AUTO-GENERATED FILE - DO NOT EDIT DIRECTLY -->
<!-- Source: bitsoex/ai-code-instructions → java/skills/upgrade-spring-boot-3-5/SKILL.md -->
<!-- To modify, edit the source file and run the distribution workflow -->

