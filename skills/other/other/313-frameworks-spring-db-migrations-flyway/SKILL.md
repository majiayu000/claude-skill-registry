---
name: 313-frameworks-spring-db-migrations-flyway
description: Use when you need to add or review Flyway database migrations in a Spring Boot application — Maven dependencies, db/migration scripts, spring.flyway.* configuration, baseline and validation, and alignment with JDBC or Spring Data JDBC. Part of the skills-for-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.14.0-SNAPSHOT
---
# Spring — Database migrations (Flyway)

Apply Flyway migration guidelines for Spring Boot.

**What is covered in this Skill?**

- flyway-core and database-specific Flyway modules (e.g. PostgreSQL) with Spring Boot BOM
- Versioned SQL under `src/main/resources/db/migration` (`V{version}__{description}.sql`)
- `spring.flyway.*` properties: locations, baseline-on-migrate, validate-on-migrate
- Optional Java migrations (`BaseJavaMigration`) for data backfills
- Forward-only discipline: do not rewrite applied migrations in shared environments
- Coordination with `@311-frameworks-spring-jdbc` and `@312-frameworks-spring-data-jdbc`

**Scope:** Apply recommendations based on the reference rules and good/bad examples.

## Constraints

Before applying Flyway or SQL changes, ensure the project compiles. After improvements, run full verification.

- **MANDATORY**: Run `./mvnw compile` or `mvn compile` before applying any change
- **SAFETY**: If compilation fails, stop immediately
- **VERIFY**: Run `./mvnw clean verify` or `mvn clean verify` after applying improvements
- **BEFORE APPLYING**: Read the reference for detailed rules and good/bad patterns

## When to use this skill

- Add or review Flyway migrations in a Spring Boot project
- Configure spring.flyway or db/migration layout

## Reference

For detailed guidance, examples, and constraints, see [references/313-frameworks-spring-db-migrations-flyway.md](references/313-frameworks-spring-db-migrations-flyway.md).
