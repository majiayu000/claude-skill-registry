---
name: spring-boot-data-ddd
description: Spring Boot 4 data layer implementation for Domain-Driven Design. Use when implementing JPA or JDBC aggregates, Spring Data repositories, transactional services, projections, or entity auditing. Covers aggregate roots with AbstractAggregateRoot, value object mapping, EntityGraph for N+1 prevention, and Spring Boot 4 specifics (JSpecify null-safety, AOT repositories). For DDD concepts and design decisions, see the domain-driven-design skill.
---

# Spring Boot Data Layer for DDD

Implements DDD tactical patterns with Spring Data JPA and Spring Data JDBC in Spring Boot 4.

## Technology Selection

| Choose | When |
|--------|------|
| **Spring Data JPA** | Complex queries, existing Hibernate expertise, need lazy loading |
| **Spring Data JDBC** | DDD-first design, simpler mapping, aggregate-per-table, no lazy loading |

Spring Data JDBC enforces aggregate boundaries naturally—recommended for new DDD projects.

## Core Workflow

1. **Define aggregate root** → Extend `AbstractAggregateRoot<T>` for domain events
2. **Map value objects** → Use `@Embedded` or `@Converter` for immutability
3. **Create repository interface** → One per aggregate root, extend appropriate base
4. **Implement service layer** → `@Transactional` on public methods, one aggregate per transaction
5. **Add projections** → Interface or record-based for read operations

## Quick Patterns

See [EXAMPLES.md](EXAMPLES.md) for complete working examples including:
- **Aggregate Root** with AbstractAggregateRoot and domain events (Java + Kotlin)
- **Repository with EntityGraph** for N+1 prevention
- **Transactional Service** with proper boundaries
- **Value Objects** (Strongly-typed IDs, Money pattern)
- **Projections** for efficient read operations
- **Auditing** with automatic timestamps

## Spring Boot 4 Specifics

- **JSpecify null-safety**: `@NullMarked` and `@Nullable` annotations
- **AOT Repository Compilation**: Enabled by default for faster startup
- **Jakarta EE 11**: All imports use `jakarta.*` namespace
- **ListCrudRepository**: New interface returning `List<T>` instead of `Iterable<T>`

## ListCrudRepository (Spring Data 3.1+)

New repository interface returning `List<T>` for better API ergonomics:

```java
// OLD: CrudRepository returns Iterable<T>
public interface UserRepository extends CrudRepository<User, Long> {
    Iterable<User> findAll();  // Requires conversion to List
}

// NEW: ListCrudRepository returns List<T>
public interface UserRepository extends ListCrudRepository<User, Long> {
    List<User> findAll();  // Direct List return
    List<User> findAllById(Iterable<Long> ids);  // Also List
}

// Can also extend both for full functionality
public interface UserRepository extends
    ListCrudRepository<User, Long>,
    ListPagingAndSortingRepository<User, Long> {
}
```

**Benefits**: No more `StreamSupport.stream(iterable.spliterator(), false).toList()` conversions.

## Detailed References

- **Examples**: See [EXAMPLES.md](EXAMPLES.md) for complete working code examples
- **Troubleshooting**: See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common issues and Boot 4 migration
- **Aggregates & Entities**: See [references/AGGREGATES.md](references/AGGREGATES.md) for complete patterns with value objects, typed IDs, auditing
- **Repositories & Queries**: See [references/REPOSITORIES.md](references/REPOSITORIES.md) for custom queries, projections, specifications
- **Transactions**: See [references/TRANSACTIONS.md](references/TRANSACTIONS.md) for propagation, isolation, cross-aggregate consistency

## Anti-Pattern Checklist

| Anti-Pattern | Fix |
|--------------|-----|
| `FetchType.EAGER` on associations | Use `LAZY` + `@EntityGraph` when needed |
| Returning entities from controllers | Convert to DTOs in service layer |
| `@Transactional` on private methods | Use public methods (proxy limitation) |
| Missing `readOnly = true` on queries | Add for read operations (performance) |
| Direct aggregate-to-aggregate references | Reference by ID only |
| Multiple aggregates in one transaction | Use domain events for eventual consistency |

## Critical Reminders

1. **One aggregate per transaction** — Cross-aggregate changes via domain events
2. **Repository per aggregate root** — Never for child entities
3. **Value objects are immutable** — No setters, return new instances
4. **Flush before events** — Call `repository.save()` before events dispatch
5. **Test with `@DataJpaTest`** — Use `TestEntityManager` for setup
