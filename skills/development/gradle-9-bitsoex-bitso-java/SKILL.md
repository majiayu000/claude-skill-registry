---
name: gradle-9
description: >
  Upgrade from Gradle 8.x to Gradle 9.x with plugin compatibility updates.
  Required for Java 25 support. Includes plugin version mappings and migration patterns.
compatibility: Java projects using Gradle 8.x
metadata:
  version: "1.0.0"
  technology: java
  category: modernization
  tags:
    - gradle
    - gradle-9
    - build
    - plugins
---

# Gradle 9 Upgrade

Upgrade from Gradle 8.x to Gradle 9.x with all required plugin updates.

## When to Use

- Upgrading to Java 25 (requires Gradle 9.x)
- Need Gradle 9 features
- Current Gradle 8.x plugins are deprecated

## Skill Contents

### Sections

- [When to Use](#when-to-use) (L22-L27)
- [Target Versions](#target-versions) (L47-L59)
- [Quick Start](#quick-start) (L60-L105)
- [References](#references) (L106-L111)
- [Plugin Migration Details](#plugin-migration-details) (L112-L153)
- [Related Skills](#related-skills) (L154-L158)
- [Related Commands](#related-commands) (L159-L164)

### Available Resources

**📚 references/** - Detailed documentation
- [plugin compatibility](references/plugin-compatibility.md)

---

## Target Versions

| Component | Gradle 8.x | Gradle 9.x | Notes |
|-----------|------------|------------|-------|
| **Gradle** | 8.14.3 | **9.2.1** | Major version |
| **Lombok Plugin** | 8.14.2 | **9.1.0** | Freefair |
| **Spotless** | 6.x | **8.1.0** | Major bump |
| **SonarQube** | 6.x | **7.2.2.6593** | Major bump |
| **Develocity** | 0.1.x | **0.2.8** | Compatibility |
| **Flyway** | 10.x | **11.19.0** | If used |
| **jOOQ** | 9.x | **10.1.1** | If used |
| **Protobuf** | 0.9.x | **0.9.5** | If used |

## Quick Start

### 1. Update Gradle Wrapper

```bash
./gradlew wrapper --gradle-version=9.2.1
```

### 2. Update Plugin Versions

```toml
# gradle/libs.versions.toml
[plugins]
lombok = "io.freefair.lombok:9.1.0"
spotless = "com.diffplug.spotless:8.1.0"
sonarqube = "org.sonarqube:7.2.2.6593"
```

```groovy
// settings.gradle
plugins {
    id 'bitso.develocity' version "${develocityPluginVersion}"  // 0.2.8
    id 'org.sonarqube' version "${sonarqubePluginVersion}"      // 7.2.2.6593
}
```

### 3. Add JUnit Platform Launcher

Required for JUnit 5.11+ with Gradle 9:

```groovy
subprojects {
    plugins.withType(JavaPlugin).configureEach {
        dependencies {
            testRuntimeOnly 'org.junit.platform:junit-platform-launcher'
        }
    }
}
```

### 4. Validate

```bash
./gradlew clean build test
```

## References

| Reference | Content |
|-----------|---------|
| [references/plugin-compatibility.md](references/plugin-compatibility.md) | Plugin version mappings and known issues |

## Plugin Migration Details

### Lombok Plugin (Freefair)

```toml
# Old (Gradle 8.x)
lombok = "io.freefair.lombok:8.14.2"

# New (Gradle 9.x)
lombok = "io.freefair.lombok:9.1.0"
```

Requires Lombok 1.18.42 for Java 25 bytecode support:

```groovy
lombok {
    version = libs.versions.lombok.get()  // 1.18.42
}
```

### Spotless

```toml
# Old (Gradle 8.x)
spotless = "com.diffplug.spotless:6.x"

# New (Gradle 9.x)
spotless = "com.diffplug.spotless:8.1.0"
```

For Java 25 formatting, use palantir-java-format 2.74.0.

### SonarQube

```toml
# Old (Gradle 8.x)
sonarqube = "org.sonarqube:6.x"

# New (Gradle 9.x)
sonarqube = "org.sonarqube:7.2.2.6593"
```

## Related Skills

- `spring-boot-3-5` - Upgrade Spring Boot first
- `java-25` - Java 25 requires Gradle 9

## Related Commands

This skill is referenced by:

- [`/prepare-to-gradle-9`](../../commands/prepare-to-gradle-9.md) - Prepare for Gradle 9 upgrade
- [`/prepare-to-java-25`](../../commands/prepare-to-java-25.md) - Java 25 preparation (requires Gradle 9)
<!-- AUTO-GENERATED FILE - DO NOT EDIT DIRECTLY -->
<!-- Source: bitsoex/ai-code-instructions → java/skills/gradle-9/SKILL.md -->
<!-- To modify, edit the source file and run the distribution workflow -->

