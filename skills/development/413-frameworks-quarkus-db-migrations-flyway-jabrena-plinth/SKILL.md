---
name: 413-frameworks-quarkus-db-migrations-flyway
description: Use when you need to add or review Flyway database migrations in a Quarkus application — quarkus-flyway extension, db/migration scripts, quarkus.flyway.* configuration, migrate-at-start, and alignment with JDBC or Panache. This should trigger for requests such as Add or review Flyway migrations in a Quarkus project; Configure quarkus-flyway or db/migration layout. Part of cursor-rules-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.16.0
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
- **EDGE CASE**: If the user goal is ambiguous, stop and ask a clarifying question before editing files or running project-wide commands
- **EDGE CASE**: If required context, files, credentials, or tools are missing, report the blocker explicitly and ask whether to proceed with setup or fallback guidance
- **EDGE CASE**: If requested changes conflict with project constraints or safety boundaries, explain the conflict and ask for user confirmation on the preferred trade-off

## When to use this skill

- Add or review Flyway migrations in a Quarkus project
- Configure quarkus-flyway or db/migration layout

## Workflow

1. **Read reference and assess project context**

Read `references/413-frameworks-quarkus-db-migrations-flyway.md` and inspect the current project setup before proposing changes.

2. **Gather scope and decide target improvements**

Identify requested outcomes, constraints, and the minimum safe set of changes to apply.

3. **Apply framework-aligned changes**

Implement or refactor configuration/code following the reference patterns and project conventions.

4. **Run verification and report results**

Execute appropriate build/tests and summarize what changed, what was verified, and any follow-up actions.

## Reference

For detailed guidance, examples, and constraints, see [references/413-frameworks-quarkus-db-migrations-flyway.md](references/413-frameworks-quarkus-db-migrations-flyway.md).
