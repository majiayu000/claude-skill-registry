---
name: 413-frameworks-quarkus-db-migrations-flyway
description: Use when you need to add or review Flyway database migrations in a Quarkus application — quarkus-flyway extension, db/migration scripts, quarkus.flyway.* configuration, migrate-at-start, and alignment with JDBC or Panache. Part of the skills-for-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.14.0-SNAPSHOT
---
# Quarkus — Database migrations (Flyway)

Apply Flyway migration guidelines for Quarkus.

**What is covered in this Skill?**

- `quarkus-flyway` with `quarkus-jdbc-*` drivers
- Versioned SQL under `src/main/resources/db/migration`
- `quarkus.flyway.migrate-at-start`, locations, baseline options
- Multiple datasources (when applicable)
- Coordination with `@411-frameworks-quarkus-jdbc` and `@412-frameworks-quarkus-panache`

**Scope:** Apply recommendations based on the reference rules and good/bad examples.

## Constraints

Before applying Flyway or SQL changes, ensure the project compiles. After improvements, run full verification.

- **MANDATORY**: Run `./mvnw compile` or `mvn compile` before applying any change
- **SAFETY**: If compilation fails, stop immediately
- **VERIFY**: Run `./mvnw clean verify` or `mvn clean verify` after applying improvements
- **BEFORE APPLYING**: Read the reference for detailed rules and good/bad patterns

## When to use this skill

- Add or review Flyway migrations in a Quarkus project
- Configure quarkus-flyway or db/migration layout

## Reference

For detailed guidance, examples, and constraints, see [references/413-frameworks-quarkus-db-migrations-flyway.md](references/413-frameworks-quarkus-db-migrations-flyway.md).
