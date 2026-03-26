---
name: 412-frameworks-quarkus-panache
description: Use when you need data access with Quarkus Hibernate ORM Panache — including PanacheEntity / PanacheEntityBase, PanacheRepository, named and HQL queries, DTO projections (project(Class)), pagination (Page.of()), N+1 avoidance (JOIN FETCH), optimistic locking (@Version / OptimisticLockException), @NamedQuery for validated reusable queries, transactions, @TestTransaction for test isolation, and immutable-friendly patterns. This is the Quarkus analogue to Spring Data for relational persistence. Part of the skills-for-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.13.0-SNAPSHOT
---
# Hibernate ORM with Panache

Apply Panache patterns for Hibernate ORM in Quarkus.

**What is covered in this Skill?**

- Active record (PanacheEntity) vs PanacheRepository — when to use each
- Parameterized HQL / Panache queries: positional (?1) and named (:param) — no unsafe concatenation
- @NamedQuery on entities for reusable, build-time validated queries
- DTO projections with project(Class) to avoid exposing managed entities
- Pagination with Page.of(pageIndex, pageSize) and query.count()
- N+1 avoidance with JOIN FETCH in HQL queries
- Optimistic locking with @Version and handling OptimisticLockException
- @Transactional application services
- @TestTransaction for automatic rollback in @QuarkusTest tests
- Mapping entities vs exposing DTOs at REST boundaries
- Pairing with `@411` for raw SQL when needed

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

## Reference

For detailed guidance, examples, and constraints, see [references/412-frameworks-quarkus-panache.md](references/412-frameworks-quarkus-panache.md).
