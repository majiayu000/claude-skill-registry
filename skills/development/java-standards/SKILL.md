---
name: java-standards
description: >
  Java service standards for Bitso projects. Covers tech stack requirements, project organization,
  code review guidelines, MapStruct usage, and build verification practices.
  Use when creating new Java services or reviewing existing code.
compatibility: Java projects using Gradle with Spring Boot
metadata:
  version: "1.0.0"
  technology: java
  category: standards
  tags:
    - java
    - standards
    - code-review
    - project-structure
    - mapstruct
---

# Java Standards

Java service standards for Bitso projects.

## When to use this skill

- Creating new Java services or modules
- Understanding project organization patterns
- Reviewing Java code for standards compliance
- Configuring MapStruct for object mapping
- Verifying builds after code changes

## Skill Contents

### Sections

- [When to use this skill](#when-to-use-this-skill) (L24-L31)
- [Tech Stack](#tech-stack) (L53-L66)
- [Project Organization](#project-organization) (L67-L82)
- [Build Verification](#build-verification) (L83-L96)
- [References](#references) (L97-L104)
- [Related Rules](#related-rules) (L105-L110)
- [Related Skills](#related-skills) (L111-L117)

### Available Resources

**📚 references/** - Detailed documentation
- [build verification](references/build-verification.md)
- [code review](references/code-review.md)
- [services](references/services.md)

---

## Tech Stack

| Component | Version | Notes |
|-----------|---------|-------|
| **Java** | 21 (LTS) | Current LTS version |
| **Gradle** | 8.14.3+ | Compatible with Java 21 |
| **Spring Boot** | 3.5.8 | CRITICAL - 3.4.x EOL end of 2025 |
| **Database Access** | jOOQ | For accessing PostgreSQL |
| **Databases** | PostgreSQL, Redis | Primary data stores |
| **Inter-service Communication** | gRPC | Standard protocol |
| **Object Mapping** | MapStruct | For DTO/domain mapping |

For Spring Boot upgrades, use `/upgrade-to-recommended-versions`.

## Project Organization

Projects should be organized with domain-based modules:

```text
root-project/
├── build.gradle
├── settings.gradle
├── docs/                    # Documentation
├── bitso-libs/              # Library modules
│   ├── <subdomain>/         # Domain logic
│   └── <subdomain-proto>/   # Protobuf definitions
└── bitso-services/          # Service modules
    └── <domain>/            # Spring Boot application
```

## Build Verification

After updating Java or Groovy code, verify changes:

```bash
# Run tests to verify changes
./gradlew test 2>&1 | grep -E "FAILED|Error" || echo "All tests passed"

# Or run full build with tests
./gradlew build 2>&1 | grep -E "FAILED|Error" || echo "Build successful"
```

If problems are found, fix them before committing.

## References

| Reference | Description |
|-----------|-------------|
| [references/services.md](references/services.md) | Tech stack, project structure, dependency management, MapStruct |
| [references/code-review.md](references/code-review.md) | Java 21 standards, coding style, var keyword usage |
| [references/build-verification.md](references/build-verification.md) | Build commands and verification practices |

## Related Rules

- `.cursor/rules/java-services-standards.mdc` - Full service standards
- `.cursor/rules/java-code-review-standards.mdc` - Code review guidelines
- `.cursor/rules/java-run-build-after-changes.mdc` - Build verification

## Related Skills

| Skill | Purpose |
|-------|---------|
| [gradle-standards](../gradle-standards/SKILL.md) | Gradle configuration |
| [grpc-standards](../grpc-standards/SKILL.md) | gRPC service implementation |
| [database-integration](../database-integration/SKILL.md) | jOOQ and Flyway |
<!-- AUTO-GENERATED FILE - DO NOT EDIT DIRECTLY -->
<!-- Source: bitsoex/ai-code-instructions → java/skills/java-standards/SKILL.md -->
<!-- To modify, edit the source file and run the distribution workflow -->

