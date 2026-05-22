---
name: 312-frameworks-spring-data-jdbc
description: Use when you need to use Spring Data JDBC with Java records — including entity design with records, repository pattern, immutable updates, aggregate relationships, custom queries, transaction management, and avoiding N+1 problems. This should trigger for requests such as Review Java code for Spring Data JDBC; Apply best practices for Spring Data JDBC in Java code. Part of cursor-rules-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.15.0-SNAPSHOT
---
# Spring Data JDBC with Records

Apply Spring Data JDBC guidelines with Java records.

**What is covered in this Skill?**

- Records for entity classes (immutable, constructor-friendly)
- @Table for naming when record name differs from the table name
- @Embedded to inline value-object columns into the parent row without a separate table
- Repository pattern
- Immutable updates with static factories for new rows and with* helpers for updates
- save() INSERT vs UPDATE semantics driven by @Id nullability
- Aggregate boundaries: one repository per aggregate root, Set for one-to-many inside the root, foreign keys between aggregates
- Custom queries with @Query and named parameters (no user-input concatenation)
- Transaction management (@Transactional on services; readOnly where appropriate)
- Single query loading (N+1 avoidance)

**Scope:** Apply recommendations based on the reference rules and good/bad code examples.

## Constraints

Before applying any Spring Data JDBC changes, ensure the project compiles. If compilation fails, stop immediately. After applying improvements, run full verification.

- **MANDATORY**: Run `./mvnw compile` or `mvn compile` before applying any change
- **SAFETY**: If compilation fails, stop immediately
- **VERIFY**: Run `./mvnw clean verify` or `mvn clean verify` after applying improvements
- **BEFORE APPLYING**: Read the reference for detailed rules and good/bad patterns
- **EDGE CASE**: If request scope is ambiguous, stop and ask a clarifying question before applying changes
- **EDGE CASE**: If required inputs, files, or tooling are missing, report what is missing and ask whether to proceed with setup guidance

## When to use this skill

- Review Java code for Spring Data JDBC
- Apply best practices for Spring Data JDBC in Java code

## Workflow

1. **Read reference and assess project context**

Read `references/312-frameworks-spring-data-jdbc.md` and inspect the current project setup before proposing changes.

2. **Gather scope and decide target improvements**

Identify requested outcomes, constraints, and the minimum safe set of changes to apply.

3. **Apply framework-aligned changes**

Implement or refactor configuration/code following the reference patterns and project conventions.

4. **Run verification and report results**

Execute appropriate build/tests and summarize what changed, what was verified, and any follow-up actions.

## Reference

For detailed guidance, examples, and constraints, see [references/312-frameworks-spring-data-jdbc.md](references/312-frameworks-spring-data-jdbc.md).
