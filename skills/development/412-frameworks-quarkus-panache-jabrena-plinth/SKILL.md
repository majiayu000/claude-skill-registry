---
name: 412-frameworks-quarkus-panache
description: Use when you need data access with Quarkus Hibernate ORM Panache — including PanacheEntity / PanacheEntityBase, PanacheRepository, named queries, JPQL, native SQL, DTO projections (project(Class)), pagination (Page.of()), N+1 avoidance (JOIN FETCH), optimistic locking (@Version / OptimisticLockException), @NamedQuery for validated reusable queries, transactions, @TestTransaction for test isolation, and immutable-friendly patterns. This is the Quarkus analogue to Spring Data for relational persistence. This should trigger for requests such as Review Panache entities or repositories in Quarkus; Improve Hibernate ORM data access with Panache; Add DTO projections, JOIN FETCH, pagination, or optimistic locking to Panache queries; Fix N+1 query problems or add @Version concurrency control in Quarkus Panache. Part of cursor-rules-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.16.0
---
# Hibernate ORM with Panache

Apply Panache patterns for Hibernate ORM in Quarkus.

**What is covered in this Skill?**

- Active record (PanacheEntity) vs PanacheRepository — when to use each
- Parameterized JPQL / Panache queries: positional (?1) and named (:param) — no unsafe concatenation
- @NamedQuery on entities for reusable, build-time validated queries
- DTO projections with project(Class) to avoid exposing managed entities
- Pagination with Page.of(pageIndex, pageSize) and query.count()
- N+1 avoidance with JOIN FETCH in JPQL queries
- Optimistic locking with @Version and handling OptimisticLockException
- @Transactional application services
- @TestTransaction for automatic rollback in @QuarkusTest tests
- Mapping entities vs exposing DTOs at REST boundaries
- Native queries via Hibernate when you want controlled SQL in the same transaction; pairing with `@411` for JDBC when bypassing Hibernate at the boundary

**Scope:** Apply recommendations based on the reference rules and good/bad code examples.

## Constraints

Compile before persistence changes; verify after.

- **MANDATORY**: Run `./mvnw compile` or `mvn compile` before applying any change
- **PREREQUISITE**: Project must compile before applying Panache improvements
- **SAFETY**: If compilation fails, stop immediately
- **BLOCKING CONDITION**: Compilation errors must be resolved by the user before proceeding
- **VERIFY**: Run `./mvnw clean verify` or `mvn clean verify` after applying improvements
- **BEFORE APPLYING**: Read the reference for detailed rules and examples

## When to use this skill

- Review Panache entities or repositories in Quarkus
- Improve Hibernate ORM data access with Panache
- Add DTO projections, JOIN FETCH, pagination, or optimistic locking to Panache queries
- Fix N+1 query problems or add @Version concurrency control in Quarkus Panache

## Workflow

1. **Read reference and assess project context**

Read `references/412-frameworks-quarkus-panache.md` and inspect the current project setup before proposing changes.

2. **Gather scope and decide target improvements**

Identify requested outcomes, constraints, and the minimum safe set of changes to apply.

3. **Apply framework-aligned changes**

Implement or refactor configuration/code following the reference patterns and project conventions.

4. **Run verification and report results**

Execute appropriate build/tests and summarize what changed, what was verified, and any follow-up actions.

## Reference

For detailed guidance, examples, and constraints, see [references/412-frameworks-quarkus-panache.md](references/412-frameworks-quarkus-panache.md).
