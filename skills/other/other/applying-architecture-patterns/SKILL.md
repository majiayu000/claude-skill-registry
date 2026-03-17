---
name: applying-architecture-patterns
description: Implement proven backend architecture patterns including Clean Architecture, Hexagonal Architecture, and Domain-Driven Design. Use when (1) designing new backend systems from scratch, (2) refactoring monolithic applications for better maintainability, (3) establishing architecture standards for a team, (4) migrating from tightly coupled to loosely coupled architectures, (5) implementing domain-driven design principles, (6) creating testable and mockable codebases, or (7) planning microservices decomposition.
---

# Applying Architecture Patterns

Apply Clean Architecture, Hexagonal Architecture, and Domain-Driven Design to build maintainable, testable, and scalable backend systems.

## Core Concepts

### Clean Architecture (Uncle Bob)

**Layers (dependency flows inward):**
- **Entities**: Core business models
- **Use Cases**: Application business rules
- **Interface Adapters**: Controllers, presenters, gateways
- **Frameworks & Drivers**: UI, database, external services

**Principles**: Dependencies point inward. Inner layers know nothing about outer layers. Business logic independent of frameworks.

### Hexagonal Architecture (Ports and Adapters)

**Components:**
- **Domain Core**: Business logic
- **Ports**: Interfaces defining interactions
- **Adapters**: Implementations (database, REST, message queue)

**Benefits**: Swap implementations easily, technology-agnostic core, clear separation of concerns.

### Domain-Driven Design (DDD)

**Strategic Patterns:**
- **Bounded Contexts**: Separate models for different domains
- **Context Mapping**: How contexts relate
- **Ubiquitous Language**: Shared terminology

**Tactical Patterns:**
- **Entities**: Objects with identity
- **Value Objects**: Immutable objects defined by attributes
- **Aggregates**: Consistency boundaries
- **Repositories**: Data access abstraction
- **Domain Events**: Things that happened

## Implementation Examples

Load the appropriate example file based on the pattern being implemented:

- **Clean Architecture**: See [examples/clean-architecture-example.md](examples/clean-architecture-example.md) for complete layered implementation with entities, use cases, repositories, and controllers
- **Hexagonal Architecture**: See [examples/hexagonal-example.md](examples/hexagonal-example.md) for ports and adapters with production and test implementations
- **DDD Tactical Patterns**: See [examples/ddd-example.md](examples/ddd-example.md) for value objects, entities, aggregates, and domain events

## Best Practices

1. **Dependency Rule**: Dependencies always point inward
2. **Interface Segregation**: Small, focused interfaces
3. **Business Logic in Domain**: Keep frameworks out of core
4. **Test Independence**: Core testable without infrastructure
5. **Bounded Contexts**: Clear domain boundaries
6. **Ubiquitous Language**: Consistent terminology
7. **Thin Controllers**: Delegate to use cases
8. **Rich Domain Models**: Behavior with data

## Common Pitfalls

- **Anemic Domain**: Entities with only data, no behavior
- **Framework Coupling**: Business logic depends on frameworks
- **Fat Controllers**: Business logic in controllers
- **Repository Leakage**: Exposing ORM objects
- **Missing Abstractions**: Concrete dependencies in core
- **Over-Engineering**: Clean architecture for simple CRUD
