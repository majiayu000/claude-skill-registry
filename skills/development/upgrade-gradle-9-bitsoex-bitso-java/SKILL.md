---
name: upgrade-gradle-9
description: >
  Upgrade from Gradle 8.x to Gradle 9.x with plugin compatibility updates.
  Required for Java 25 support. Includes plugin version mappings and migration patterns.
compatibility: Java projects using Gradle 8.x
metadata:
  version: "2.0.0"
  technology: java
  category: modernization
  tags:
    - gradle
    - gradle-9
    - build
    - plugins
    - upgrade
---

# Upgrade Gradle 9

Upgrade from Gradle 8.x to Gradle 9.x with all required plugin updates.

## When to Use

- **Recommended for all projects** - Gradle 9.2.1 is now the standard
- Upgrading to Java 25 (requires Gradle 9.x)
- Need Gradle 9 features
- Current Gradle 8.x plugins are deprecated
- When asked to "prepare for Gradle 9"

## Skill Contents

### Sections

- [When to Use](#when-to-use) (L23-L30)
- [Target Versions](#target-versions) (L49-L61)
- [Quick Start](#quick-start) (L62-L108)
- [References](#references) (L109-L114)
- [Plugin Migration Details](#plugin-migration-details) (L115-L156)
- [Related Skills](#related-skills) (L157-L162)

### Available Resources

**📚 references/** - Detailed documentation
- [plugin compatibility](references/plugin-compatibility.md)

---

## Target Versions

| Component | Gradle 8.x | Gradle 9.x | Notes |
|-----------|------------|------------|-------|
| **Gradle** | 8.14.3 | **9.2.1** | **Recommended** for all projects |
| **Lombok Plugin** | 8.14.2 | **9.2.0** | Freefair for Gradle 9.2.1 |
| **Spotless** | 6.x | **8.1.0** | Major bump |
| **SonarQube** | 6.x | **7.2.2.6593** | Major bump |
| **Develocity** | 0.1.x | **0.2.8** | Compatibility |
| **Flyway** | 10.x | **11.19.0** | If used |
| **jOOQ** | 9.x | **10.1.1** | If used |
| **Protobuf** | 0.9.x | **0.9.6** | Gradle 9 compatible |

## Quick Start

### 1. Update Gradle Wrapper

```bash
./gradlew wrapper --gradle-version=9.2.1
```

### 2. Update Plugin Versions

```toml
# gradle/libs.versions.toml
[plugins]
lombok = "io.freefair.lombok:9.2.0"
spotless = "com.diffplug.spotless:8.1.0"
sonarqube = "org.sonarqube:7.2.2.6593"
protobuf = "com.google.protobuf:0.9.6"
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
lombok = "io.freefair.lombok:9.2.0"
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

| Skill | Purpose |
|-------|---------|
| [upgrade-spring-boot-3-5](.claude/skills/upgrade-spring-boot-3-5/SKILL.md) | Upgrade Spring Boot first |
| [upgrade-java-25](.claude/skills/upgrade-java-25/SKILL.md) | Java 25 requires Gradle 9 |
<!-- AUTO-GENERATED FILE - DO NOT EDIT DIRECTLY -->
<!-- Source: bitsoex/ai-code-instructions → java/skills/upgrade-gradle-9/SKILL.md -->
<!-- To modify, edit the source file and run the distribution workflow -->

