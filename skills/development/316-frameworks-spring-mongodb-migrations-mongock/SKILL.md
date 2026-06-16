---
name: 316-frameworks-spring-mongodb-migrations-mongock
description: Use when you need to add or review Mongock MongoDB data migrations in a Spring Boot application — including Maven coordinates, Spring Data MongoDB drivers, migration scan packages, @ChangeUnit classes, lock/transaction settings, and Testcontainers verification. This should trigger for requests such as Add Mongock migrations in Spring Boot; Review Spring MongoDB data migrations; Configure Mongock change units for Spring Data MongoDB. Part of cursor-rules-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.16.0
---
# Spring - MongoDB migrations (Mongock)

Apply Mongock migration guidelines for Spring Boot and Spring Data MongoDB.

**What is covered in this Skill?**

- Mongock BOM, Spring Boot runner, and Spring Data MongoDB driver coordinates
- `mongock.migration-scan-package` configuration and startup execution
- Code-first `@ChangeUnit` migrations with `@Execution` and rollback hooks
- Locking, idempotency, transaction limits, and forward-only rollout discipline
- Integration tests with Testcontainers MongoDB
- Coordination with `@315-frameworks-spring-mongodb`

**Scope:** Apply recommendations based on the reference rules and good/bad examples.

## Constraints

Compile before Mongock or MongoDB migration changes; verify after changes.

- **MANDATORY**: Run `./mvnw compile` or `mvn compile` before applying any change
- **SAFETY**: If compilation fails, stop immediately
- **VERIFY**: Run `./mvnw clean verify` or `mvn clean verify` after applying improvements
- **BEFORE APPLYING**: Read the reference for detailed rules and good/bad patterns
- **EDGE CASE**: If the project Spring Data MongoDB version is not compatible with the selected Mongock driver, stop and ask whether to pin/upgrade Mongock or use a lower driver generation

## When to use this skill

- Add Mongock migrations in Spring Boot
- Review Spring MongoDB data migrations
- Configure Mongock change units for Spring Data MongoDB

## Workflow

1. **Read reference and inspect MongoDB setup**

Read `references/316-frameworks-spring-mongodb-migrations-mongock.md` and inspect `pom.xml`, Spring Boot version, MongoDB configuration, and existing `@315-frameworks-spring-mongodb` persistence patterns.

2. **Choose runner, driver, and execution policy**

Select Mongock coordinates compatible with the active Spring Data MongoDB generation, configure migration scan packages, and decide startup vs controlled-job execution.

3. **Apply framework-aligned migrations**

Implement/refactor `@ChangeUnit` classes with idempotent operations, explicit ordering, rollback hooks, and safe lock/transaction settings.

4. **Run verification and report results**

Execute build/tests, including Testcontainers-backed MongoDB migration checks where feasible, and summarize outcomes and follow-up risks.

## Reference

For detailed guidance, examples, and constraints, see [references/316-frameworks-spring-mongodb-migrations-mongock.md](references/316-frameworks-spring-mongodb-migrations-mongock.md).
