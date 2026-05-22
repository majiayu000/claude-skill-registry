---
name: spring-boot-3-5
description: >
  Upgrade Java services to Spring Boot 3.5.x with all required dependency updates.
  Use when projects need to upgrade from older Spring Boot versions to 3.5.8+.
compatibility: Java projects using Gradle with Spring Boot
metadata:
  version: "1.0.0"
  technology: java
  category: modernization
  tags:
    - spring-boot
    - upgrade
    - dependencies
---

# Spring Boot 3.5.x Upgrade

Upgrade Java services to Spring Boot 3.5.8 with all required dependency updates.

## When to Use

- Project uses Spring Boot 3.4.x or earlier (3.4.x reached EOL)
- Need features from Spring Boot 3.5.x
- Preparing for Java 25 upgrade (requires Spring Boot 3.5.x first)

## Skill Contents

### Sections

- [When to Use](#when-to-use) (L21-L26)
- [Target Versions](#target-versions) (L46-L60)
- [⚠️ DO NOT Upgrade](#do-not-upgrade) (L61-L65)
- [Quick Start](#quick-start) (L66-L124)
- [References](#references) (L125-L130)
- [Related Command](#related-command) (L131-L134)
- [Related Skills](#related-skills) (L135-L139)

### Available Resources

**📚 references/** - Detailed documentation
- [troubleshooting](references/troubleshooting.md)

---

## Target Versions

| Component | Version | Notes |
|-----------|---------|-------|
| **Spring Boot** | **3.5.8** | CRITICAL - 3.4.x EOL |
| **Spring Cloud** | **2025.0.0** | Required for Spring Boot 3.5.x |
| **Spring Dependency Management** | **1.1.7** | Required plugin version |
| **Gradle** | **8.14.3** | Build tool |
| **JUnit** | **5.14.1** | Testing (via BOM) |
| **Spock** | **2.4-groovy-4.0** | Groovy testing |
| **JaCoCo** | **0.8.14** | Code coverage |
| **SonarQube Plugin** | **7.2.2.6593** | Code analysis |
| **bitso-rds-iam-authn** | **2.0.0** | If using RDS IAM |
| **bitso-commons-redis** | **4.2.1** | If using Redis |

## ⚠️ DO NOT Upgrade

- **protobuf**: Keep existing version (3.x → 4.x is breaking)
- **grpc**: Keep existing version

## Quick Start

### 1. Update Version Catalog

```toml
# gradle/libs.versions.toml
[versions]
springBoot = "3.5.8"
springCloud = "2025.0.0"  # CRITICAL for 3.5.x compatibility
spock = "2.4-groovy-4.0"

[plugins]
spring-boot = { id = "org.springframework.boot", version.ref = "springBoot" }
spring-dependency-management = { id = "io.spring.dependency-management", version = "1.1.7" }
```

### 2. Update Gradle Wrapper

```bash
./gradlew wrapper --gradle-version=8.14.3
```

### 3. Add JUnit Platform Launcher

Required for Gradle 8.14.3 with JUnit 5.11+:

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

This skill is referenced by: [`/upgrade-to-recommended-versions`](../../commands/upgrade-to-recommended-versions.md)

## Related Skills

The following skills in this category depend on Spring Boot 3.5.x:
- `java-25` - Java 25 upgrade (requires Spring Boot 3.5.x first)
- `gradle-9` - Gradle 9 upgrade patterns
<!-- AUTO-GENERATED FILE - DO NOT EDIT DIRECTLY -->
<!-- Source: bitsoex/ai-code-instructions → java/skills/spring-boot-3-5/SKILL.md -->
<!-- To modify, edit the source file and run the distribution workflow -->

