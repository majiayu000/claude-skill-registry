---
name: 512-frameworks-micronaut-data
description: Use when you need data access with Micronaut Data — @MappedEntity, CrudRepository/PageableRepository, @Query with parameters, @Transactional services, projections, @Version, and @MicronautTest with TestPropertyProvider and Testcontainers. For raw java.sql access without generated repositories, use @511-frameworks-micronaut-jdbc. This should trigger for requests such as Review or implement Micronaut Data repositories and entities; Add transactions, pagination, or projections in Micronaut persistence layer. Part of cursor-rules-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.15.0-SNAPSHOT
---
# Micronaut Data Guidelines

Apply Micronaut Data patterns for relational repositories and safe SQL.

**What is covered in this Skill?**

- @MappedEntity, @Id, @GeneratedValue, @MappedProperty for column mapping
- @Repository interfaces extending CrudRepository / PageableRepository
- Derived finder methods and @Query with named parameters
- @Transactional on @Singleton services (readOnly where appropriate)
- Page and Pageable for list endpoints
- DTO/interface projections for read-heavy queries
- @Version for optimistic locking
- Integration tests: @MicronautTest + TestPropertyProvider + Testcontainers

**Scope:** Apply recommendations based on the reference rules and good/bad code examples.

## Constraints

Compile before persistence changes; verify the full build after.

- **MANDATORY**: Run `./mvnw compile` or `mvn compile` before applying any change
- **SAFETY**: If compilation fails, stop immediately
- **VERIFY**: Run `./mvnw clean verify` or `mvn clean verify` after applying improvements
- **BEFORE APPLYING**: Read the reference for detailed rules and examples
- **EDGE CASE**: If the user goal is ambiguous, stop and ask a clarifying question before editing files or running project-wide commands
- **EDGE CASE**: If required context, files, credentials, or tools are missing, report the blocker explicitly and ask whether to proceed with setup or fallback guidance
- **EDGE CASE**: If requested changes conflict with project constraints or safety boundaries, explain the conflict and ask for user confirmation on the preferred trade-off

## When to use this skill

- Review or implement Micronaut Data repositories and entities
- Add transactions, pagination, or projections in Micronaut persistence layer

## Workflow

1. **Read reference and assess project context**

Read `references/512-frameworks-micronaut-data.md` and inspect the current project setup before proposing changes.

2. **Gather scope and decide target improvements**

Identify requested outcomes, constraints, and the minimum safe set of changes to apply.

3. **Apply framework-aligned changes**

Implement or refactor configuration/code following the reference patterns and project conventions.

4. **Run verification and report results**

Execute appropriate build/tests and summarize what changed, what was verified, and any follow-up actions.

## Reference

For detailed guidance, examples, and constraints, see [references/512-frameworks-micronaut-data.md](references/512-frameworks-micronaut-data.md).
