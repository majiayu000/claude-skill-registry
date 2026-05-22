---
name: spring-boot-verify
description: Verify Spring Boot 4.x projects for correct dependencies, configuration, and migration readiness. Use when analyzing pom.xml, build.gradle, application.yml, discussing Spring Boot project setup, dependency versions, configuration validation, version compatibility, migration to Spring Boot 4, deprecated dependencies, or when user mentions "verify project", "check dependencies", "upgrade Spring Boot", "migration readiness", "Jackson 3", "@MockBean deprecated", or "Spring Security 7".
---

# Spring Boot 4.x Project Verification

Analyzes Spring Boot projects for dependency compatibility, configuration correctness, and migration readiness.

## Verification Workflow

1. **Detect Build System** → Find pom.xml or build.gradle, extract Spring Boot version
2. **Analyze Dependencies** → Check versions, find deprecated libraries, validate compatibility
3. **Validate Configuration** → Check application.yml/properties, security config, actuator settings
4. **Generate Report** → Structured markdown with severity levels and remediation code
5. **Lookup Docs** → Use Exa MCP to fetch latest Spring Boot 4.x documentation when needed

## Dependency Quick Reference

| Check | Severity | Action |
|-------|----------|--------|
| Spring Boot version < 4.0 | CRITICAL | Upgrade to 4.0.x |
| Jackson 2.x (`com.fasterxml`) | CRITICAL | Migrate to Jackson 3 (`tools.jackson`) |
| `javax.*` imports | CRITICAL | Migrate to `jakarta.*` namespace |
| `@MockBean` in tests | ERROR | Replace with `@MockitoBean` |
| Undertow server | ERROR | Switch to Tomcat or Jetty |
| Java version < 17 | ERROR | Minimum Java 17 required |
| Gradle version < 8.14 | ERROR | Upgrade Gradle (required for Kotlin 2.2/Boot 4) |
| `spring-boot-starter-web` | WARNING | Use `spring-boot-starter-webmvc` |
| Missing Virtual Threads | INFO | Enable with `spring.threads.virtual.enabled=true` |

## Configuration Quick Reference

| Check | Severity | Action |
|-------|----------|--------|
| Security `and()` chaining | CRITICAL | Convert to Lambda DSL closures |
| `antMatchers()` usage | ERROR | Replace with `requestMatchers()` |
| `authorizeRequests()` | ERROR | Replace with `authorizeHttpRequests()` |
| All actuator endpoints exposed | WARNING | Limit to health, info, metrics |
| 100% trace sampling | WARNING | Use 10% in production |

## Jakarta Namespace Migration

**Critical for Spring Boot 3+**: All `javax.*` packages must migrate to `jakarta.*`:

| Old Package | New Package |
|-------------|-------------|
| `javax.persistence.*` | `jakarta.persistence.*` |
| `javax.servlet.*` | `jakarta.servlet.*` |
| `javax.validation.*` | `jakarta.validation.*` |
| `javax.inject.*` | `jakarta.inject.*` |
| `javax.annotation.*` | `jakarta.annotation.*` |

Use Grep to find: `import\s+javax\.`

## Spring Boot 4 New Features

| Feature | Configuration | Benefit |
|---------|---------------|---------|
| **Virtual Threads** | `spring.threads.virtual.enabled=true` | High concurrency without WebFlux |
| **JSpecify Null-Safety** | Add `@NullMarked` to package-info | Framework-wide null contracts |
| **AOT Compilation** | Enabled by default | Faster startup times |

## JSpecify Annotations

Spring Framework 7 uses JSpecify for null-safety:

```java
@NullMarked  // Package or class level - all parameters/returns non-null by default
package com.example.myapp;

import org.jspecify.annotations.Nullable;

public class UserService {
    // @Nullable for parameters/returns that can be null
    public @Nullable User findById(Long id) { ... }
}
```

## Tools to Use

1. **Glob** → Find `**/pom.xml`, `**/build.gradle*`, `**/application.{yml,properties}`
2. **Grep** → Search for deprecated patterns (`@MockBean`, `com.fasterxml`, `.and()`, `import javax.`)
3. **Read** → Inspect build files and configuration
4. **Exa MCP** → Fetch latest Spring Boot 4.x docs: `mcp__exa__web_search_exa`

## Output Format

Generate verification reports with this structure:

```markdown
## Spring Boot 4.x Verification Report

### Summary
- **Project**: {name}
- **Boot Version**: {detected version}
- **Issues Found**: {n} Critical, {n} Errors, {n} Warnings

### Critical Issues / Errors / Warnings
[Issue details with code remediation]
```

## Detailed References

- **Workflow**: See [WORKFLOW.md](WORKFLOW.md) for step-by-step verification process
- **Migration Guide**: See [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md) for step-by-step migration from Boot 3.x to 4.0
- **Examples**: See [EXAMPLES.md](EXAMPLES.md) for sample verification outputs
- **Troubleshooting**: See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for detection issues
- **Dependencies**: See [references/DEPENDENCIES.md](references/DEPENDENCIES.md) for complete version matrix
- **Configuration**: See [references/CONFIGURATION.md](references/CONFIGURATION.md) for validation rules

## Critical Reminders

1. **Check Spring Boot version first** — Many issues are version-specific
2. **Jakarta namespace migration** — `javax.*` to `jakarta.*` (required for Boot 3+)
3. **Jackson 3 namespace change** — `com.fasterxml.jackson` to `tools.jackson`
4. **Security 7 Lambda DSL** — `and()` method removed, closures required
5. **Testing annotations changed** — `@MockBean` to `@MockitoBean`
6. **Virtual Threads** — Enable with `spring.threads.virtual.enabled=true` for Java 21+
7. **Gradle 8.14+** — Required for Kotlin 2.2 and Spring Boot 4 support
8. **Use official docs** — https://docs.spring.io/spring-boot/documentation.html

## Related Skills

- `spring-boot-security` — Deep security configuration verification
- `spring-boot-testing` — Testing patterns and coverage analysis
- `spring-boot-observability` — Actuator, metrics, and tracing setup
- `spring-boot-modulith` — Module structure verification
- `domain-driven-design` — DDD architecture patterns
