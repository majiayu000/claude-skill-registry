---
name: 512-frameworks-micronaut-data
description: Use when you need data access with Micronaut Data — @MappedEntity, CrudRepository/PageableRepository, @Query with parameters, @Transactional services, projections, @Version, and @MicronautTest with TestPropertyProvider and Testcontainers. For raw java.sql access without generated repositories, use @511-frameworks-micronaut-jdbc. Part of the skills-for-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.13.0
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

## When to use this skill

- Review or implement Micronaut Data repositories and entities
- Add transactions, pagination, or projections in Micronaut persistence layer

## Reference

For detailed guidance, examples, and constraints, see [references/512-frameworks-micronaut-data.md](references/512-frameworks-micronaut-data.md).
