---
name: 513-frameworks-micronaut-db-migrations-flyway
description: Use when you need to add or review Flyway database migrations in a Micronaut application — micronaut-flyway, db/migration scripts, flyway.datasources.* configuration, and alignment with JDBC or Micronaut Data. Part of the skills-for-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.14.0
---
# Micronaut — Database migrations (Flyway)

Apply Flyway migration guidelines for Micronaut.

**What is covered in this Skill?**

- `micronaut-flyway` with JDBC/Hikari and database drivers
- Versioned SQL under `src/main/resources/db/migration`
- `flyway.datasources.*` (per-datasource) configuration in YAML/properties
- Tests with Testcontainers and real migration chains
- Coordination with `@511-frameworks-micronaut-jdbc` and `@512-frameworks-micronaut-data`

**Scope:** Apply recommendations based on the reference rules and good/bad examples.

## Constraints

Before applying Flyway or SQL changes, ensure the project compiles. After improvements, run full verification.

- **MANDATORY**: Run `./mvnw compile` or `mvn compile` before applying any change
- **SAFETY**: If compilation fails, stop immediately
- **VERIFY**: Run `./mvnw clean verify` or `mvn clean verify` after applying improvements
- **BEFORE APPLYING**: Read the reference for detailed rules and good/bad patterns

## When to use this skill

- Add or review Flyway migrations in a Micronaut project
- Configure micronaut-flyway or db/migration layout

## Reference

For detailed guidance, examples, and constraints, see [references/513-frameworks-micronaut-db-migrations-flyway.md](references/513-frameworks-micronaut-db-migrations-flyway.md).
