---
name: 313-frameworks-spring-db-migrations-flyway
description: Use when you need to add or review Flyway database migrations in a Spring Boot application — Maven dependencies, db/migration scripts, spring.flyway.* configuration, baseline and validation, and alignment with JDBC or Spring Data JDBC. This should trigger for requests such as Add or review Flyway migrations in a Spring Boot project; Configure spring.flyway or db/migration layout. Part of cursor-rules-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.15.0-SNAPSHOT
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
- **EDGE CASE**: If the user goal is ambiguous, stop and ask a clarifying question before editing files or running project-wide commands
- **EDGE CASE**: If required context, files, credentials, or tools are missing, report the blocker explicitly and ask whether to proceed with setup or fallback guidance
- **EDGE CASE**: If requested changes conflict with project constraints or safety boundaries, explain the conflict and ask for user confirmation on the preferred trade-off

## When to use this skill

- Add or review Flyway migrations in a Spring Boot project
- Configure spring.flyway or db/migration layout

## Workflow

1. **Read reference and assess project context**

Read `references/313-frameworks-spring-db-migrations-flyway.md` and inspect the current project setup before proposing changes.

2. **Gather scope and decide target improvements**

Identify requested outcomes, constraints, and the minimum safe set of changes to apply.

3. **Apply framework-aligned changes**

Implement or refactor configuration/code following the reference patterns and project conventions.

4. **Run verification and report results**

Execute appropriate build/tests and summarize what changed, what was verified, and any follow-up actions.

## Reference

For detailed guidance, examples, and constraints, see [references/313-frameworks-spring-db-migrations-flyway.md](references/313-frameworks-spring-db-migrations-flyway.md).
