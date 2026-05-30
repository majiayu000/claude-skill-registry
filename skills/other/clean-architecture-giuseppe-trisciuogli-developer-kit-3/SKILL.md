---
name: clean-architecture
description: Provides implementation patterns for Clean Architecture, Domain-Driven Design (DDD), and Hexagonal Architecture (Ports & Adapters) in NestJS/TypeScript applications. Use when structuring complex backend systems, designing domain layers with entities/value objects/aggregates, implementing ports and adapters, creating use cases, or refactoring from anemic models to rich domain models with dependency inversion.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Clean Architecture, DDD & Hexagonal Architecture for NestJS

## Overview

This skill provides comprehensive guidance for implementing Clean Architecture, Domain-Driven Design (DDD), and Hexagonal Architecture patterns in NestJS/TypeScript applications. It covers the architectural layers, tactical patterns, and practical implementation examples for building maintainable, testable, and loosely-coupled backend systems.

## When to Use

- Architecting complex NestJS applications with long-term maintainability
- Refactoring from tightly-coupled MVC to layered architecture
- Implementing rich domain models with business logic encapsulation
- Designing testable systems with swappable infrastructure
- Creating microservices with clear bounded contexts
- Separating business rules from framework code
- Implementing event-driven architectures with domain events

## Instructions

### 1. Understand the Architectural Layers

Clean Architecture organizes code into concentric layers where dependencies flow inward. Inner layers have no knowledge of outer layers:

```
+-------------------------------------+
|  Infrastructure (Frameworks, DB)    |  Outer layer - volatile
+-------------------------------------+
|  Adapters (Controllers, Repositories)|  Interface adapters
+-------------------------------------+
|  Application (Use Cases)            |  Business rules
+-------------------------------------+
|  Domain (Entities, Value Objects)   |  Core - most stable
+-------------------------------------+
```

The Hexagonal Architecture (Ports & Adapters) pattern complements this:
- **Ports**: Interfaces defining what the application needs
- **Adapters**: Concrete implementations of ports
- **Domain Core**: Pure business logic with zero dependencies

### 2. Learn DDD Tactical Patterns

Apply these patterns in your domain layer:
- **Entities**: Objects with identity and lifecycle
- **Value Objects**: Immutable, defined by attributes
- **Aggregates**: Consistency boundaries with aggregate roots
- **Domain Events**: Capture state changes
- **Repositories**: Abstract data access for aggregates

### 3. Organize Your Project Structure

Structure your NestJS project following Clean Architecture principles:

```
src/
+-- domain/                    # Inner layer - no external deps
|   +-- entities/              # Domain entities
|   +-- value-objects/         # Immutable value objects
|   +-- aggregates/            # Aggregate roots
|   +-- events/                # Domain events
|   +-- repositories/          # Repository interfaces (ports)
|   +-- services/              # Domain services
+-- application/               # Use cases - orchestration
|   +-- use-cases/             # Individual use cases
|   +-- ports/                 # Input/output ports
|   +-- dto/                   # Application DTOs
|   +-- services/              # Application services
+-- infrastructure/            # External concerns
|   +-- database/              # ORM config, migrations
|   +-- http/                  # HTTP clients
|   +-- messaging/             # Message queues
+-- adapters/                  # Interface adapters
    +-- http/                  # Controllers, presenters
    +-- persistence/           # Repository implementations
    +-- external/              # External service adapters
```

### 4. Implement the Domain Layer

Create pure domain objects with no external dependencies:

1. **Value Objects**: Immutable objects validated at construction
2. **Entities**: Objects with identity containing business logic
3. **Aggregates**: Consistency boundaries protecting invariants
4. **Repository Ports**: Interfaces defining data access contracts

### 5. Implement the Application Layer

Create use cases that orchestrate business logic:

1. Define input/output DTOs for each use case
2. Inject repository ports via constructor
3. Implement business workflows in the `execute` method
4. Keep use cases focused on a single responsibility

### 6. Implement Adapters

Create concrete implementations of ports:

1. **Persistence Adapters**: Map domain objects to/from ORM entities
2. **HTTP Adapters**: Controllers that transform requests to use case inputs
3. **External Service Adapters**: Integrate with third-party services

### 7. Configure Dependency Injection

Wire everything together in NestJS modules:

1. Register use cases as providers
2. Provide repository implementations using interface tokens
3. Import required infrastructure modules (TypeORM, etc.)

### 8. Apply Best Practices

Follow these principles throughout implementation:

1. **Dependency Rule**: Dependencies only point inward. Domain knows nothing about NestJS, TypeORM, or HTTP.
2. **Rich Domain Models**: Put business logic in entities, not services. Avoid anemic domain models.
3. **Immutability**: Value objects must be immutable. Create new instances instead of modifying.
4. **Interface Segregation**: Keep repository interfaces small and focused.
5. **Constructor Injection**: Use NestJS DI in outer layers only. Domain entities use plain constructors.
6. **Validation**: Validate at boundaries (DTOs) and enforce invariants in domain.
7. **Testing**: Domain layer tests require no NestJS testing module - pure unit tests.
8. **Transactions**: Keep transactions in the application layer, not domain.

## Examples

For detailed code examples covering all aspects of Clean Architecture implementation, see:

- **[references/examples.md](references/examples.md)** - Complete examples including:
  - Value Objects (Email, Money)
  - Entities with Business Logic (OrderItem)
  - Aggregate Roots with Domain Events (Order)
  - Repository Ports (Interfaces)
  - Use Cases (Application Layer)
  - Repository Adapters (Infrastructure)
  - Controller Adapters (HTTP)
  - Module Configuration (DI setup)

## Best Practices

For comprehensive guidance on Clean Architecture best practices, including:

- **Core Principles**: Dependency Rule, Rich Domain Models, Immutability, Interface Segregation
- **Testing Strategies**: Unit testing domain, integration testing application, E2E testing adapters
- **Performance Considerations**: Aggregate design, caching strategy, lazy loading

See **[references/best-practices.md](references/best-practices.md)**

## Constraints and Warnings

Important constraints, common pitfalls, and implementation warnings:

- **Architecture Constraints**: Dependency rule violations, domain purity requirements, interface location rules
- **Common Pitfalls**: Leaky abstractions, anemic domain models, wrong layer dependencies, missing ports
- **Implementation Warnings**: Mapping overhead, learning curve, boilerplate code, transaction boundaries
- **Performance Considerations**: Aggregate size, database queries, caching strategies

See **[references/constraints.md](references/constraints.md)**

## Quick Start

1. Read the architectural layers overview above
2. Review the [examples.md](references/examples.md) for implementation patterns
3. Study [best-practices.md](references/best-practices.md) for core principles
4. Check [constraints.md](references/constraints.md) to avoid common pitfalls
5. Start implementing your domain layer with pure TypeScript classes
6. Add application layer use cases to orchestrate business logic
7. Implement adapters for infrastructure concerns
8. Configure dependency injection in NestJS modules

## References

- `references/examples.md` - Complete code examples for all layers
- `references/best-practices.md` - Comprehensive best practices and principles
- `references/constraints.md` - Constraints, pitfalls, and warnings
