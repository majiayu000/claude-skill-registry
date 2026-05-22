---
name: database-integration
description: >
  Database integration patterns for Java services using jOOQ and Flyway. Covers code generation,
  read/write splitting, migration guidelines, and version compatibility.
  Use when setting up or maintaining PostgreSQL integration.
compatibility: Java projects using Gradle with PostgreSQL
metadata:
  version: "1.0.0"
  technology: java
  category: infrastructure
  tags:
    - java
    - jooq
    - flyway
    - postgresql
    - database
---

# Database Integration

Database integration patterns for Java services using jOOQ and Flyway.

## When to use this skill

- Setting up jOOQ code generation
- Creating Flyway migrations
- Configuring read/write database splitting
- Resolving jOOQ version conflicts
- Reviewing SQL migration safety

## Skill Contents

### Sections

- [When to use this skill](#when-to-use-this-skill) (L24-L31)
- [Quick Start](#quick-start) (L51-L97)
- [Version Compatibility](#version-compatibility) (L98-L117)
- [References](#references) (L118-L124)
- [Related Rules](#related-rules) (L125-L129)
- [Related Skills](#related-skills) (L130-L135)

### Available Resources

**📚 references/** - Detailed documentation
- [flyway](references/flyway.md)
- [jooq](references/jooq.md)

---

## Quick Start

### 1. Add Dependencies

```toml
# gradle/libs.versions.toml
[versions]
postgresql = "42.7.8"
testcontainers = "1.21.4"
jooq = "3.19.28"  # Spring Boot 3.5.x BOM version
flyway = "11.7.2"

[libraries]
jooq = { module = "org.jooq:jooq", version.ref = "jooq" }
jooq-codegen = { module = "org.jooq:jooq-codegen", version.ref = "jooq" }
jooq-meta = { module = "org.jooq:jooq-meta", version.ref = "jooq" }

[plugins]
flyway = { id = "org.flywaydb.flyway", version.ref = "flyway" }
jooq = { id = "nu.studer.jooq", version = "9.0" }
```

### 2. Apply jOOQ Configuration

```groovy
// build.gradle
plugins {
    alias(libs.plugins.flyway)
    alias(libs.plugins.jooq)
}

apply from: "${project.rootDir}/gradle/jooq-config.gradle"

dependencies {
    implementation libs.jooq
    jooqGenerator libs.testcontainers.postgres,
            libs.postgres,
            libs.flyway.database.postgresql
}
```

### 3. Generate Code

```bash
./gradlew generateJooq
```

## Version Compatibility

### Java 21 (Gradle 8.x)

| Component | Version |
|-----------|---------|
| jOOQ | 3.19.28 |
| jOOQ Plugin | 9.0 |
| Flyway | 11.7.2 |
| PostgreSQL Driver | 42.7.8 |

### Java 25 (Gradle 9.x)

| Component | Version |
|-----------|---------|
| jOOQ | 3.20.10 |
| jOOQ Plugin | 10.1.1 |
| Flyway | 11.19.0 |
| PostgreSQL Driver | 42.7.8 |

## References

| Reference | Description |
|-----------|-------------|
| [references/jooq.md](references/jooq.md) | jOOQ setup, code generation, read/write splitting |
| [references/flyway.md](references/flyway.md) | Migration guidelines, locking, best practices |

## Related Rules

- `.cursor/rules/java-jooq.mdc` - Full jOOQ reference
- `.cursor/rules/java-flyway-migrations.mdc` - Flyway guidelines

## Related Skills

| Skill | Purpose |
|-------|---------|
| [gradle-standards](../gradle-standards/SKILL.md) | Gradle configuration |
| [java-testing](../java-testing/SKILL.md) | Testing database code |
<!-- AUTO-GENERATED FILE - DO NOT EDIT DIRECTLY -->
<!-- Source: bitsoex/ai-code-instructions → java/skills/database-integration/SKILL.md -->
<!-- To modify, edit the source file and run the distribution workflow -->

