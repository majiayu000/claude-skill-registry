---
name: dev-philosophy
description: Development Philosophy & Standards. Use it everytime you plan or implement any code.
---

# Development Philosophy & Standards

## Architecture Principles

### Layering & Boundaries

- Domain-driven layers: Domain → Application → Infrastructure → Presentation
- Dependency rule: dependencies point inward (outer layers depend on inner)
- Domain layer has NO external dependencies (no frameworks, no database)
- Use ports & adapters (hexagonal architecture) for external integrations
- Keep business logic framework-agnostic

### Separation of Concerns

- Each module/class has ONE reason to change (Single Responsibility)
- Separate "what" (business rules) from "how" (implementation details)
- Use interfaces to define contracts, implementations to fulfill them

## SOLID Principles

- **S**RP: Single Responsibility - one class, one reason to change
- **O**CP: Open/Closed - open for extension, closed for modification
- **L**SP: Liskov Substitution - subtypes must be substitutable for base types
- **I**SP: Interface Segregation - many specific interfaces > one general
- **D**IP: Dependency Inversion - depend on abstractions, not concretions

## Design Patterns (When to Use)

### Creational

- **Factory Method**: When object creation logic is complex or varies
- **Abstract Factory**: When creating families of related objects
- **Builder**: When constructing complex objects step-by-step
- **Singleton**: RARELY - only for truly global state (prefer DI)

### Structural

- **Adapter**: When integrating incompatible interfaces
- **Decorator**: When adding behavior dynamically without subclassing
- **Facade**: When simplifying complex subsystem interfaces
- **Proxy**: For lazy loading, access control, or remote objects
- **Repository**: For abstracting data access layer

### Behavioral

- **Strategy**: When algorithms/behaviors should be interchangeable
- **Observer**: For event-driven communication between objects
- **Command**: For encapsulating requests as objects (undo/redo)
- **Template Method**: When algorithm structure is fixed but steps vary
- **State**: When object behavior changes based on internal state
- **Chain of Responsibility**: For processing requests through handler chain

### Architectural

- **MVC/MVVM**: Separating UI concerns
- **Service Layer**: Coordinating application operations
- **Unit of Work**: Managing transactions across repositories
- **CQRS**: Separating read/write operations when beneficial

## Code Quality Standards

### Naming & Clarity

- Names reveal intent: `getUsersByActiveStatus()` not `get()`
- Boolean functions: `isValid()`, `hasPermission()`, `canExecute()`
- Avoid mental mapping: use domain terms, not `x`, `temp`, `data`

### Function Design

- Small functions: 5-20 lines ideal, rarely >50
- One level of abstraction per function
- Maximum 3 parameters; use objects for more
- No side effects unless function name indicates it
- Command-query separation: do something OR return something, not both

### Class Design

- Small classes: <300 lines typical, rarely >500
- High cohesion: members work together toward single purpose
- Low coupling: minimal dependencies between classes
- Composition over inheritance
- Prefer immutability when possible

### Error Handling

- Use exceptions for exceptional cases
- Don't return null; use Optional/Maybe or empty collections
- Fail fast: validate early, fail clearly
- Specific exceptions > generic ones

## Testing Philosophy

### Test-Driven Development

- Red: Write failing test
- Green: Make it pass (simplest way)
- Refactor: Clean up while tests stay green

### Test Structure

- Arrange-Act-Assert pattern
- One assertion concept per test
- Test behavior, not implementation
- Mock external dependencies, not internal ones

### Test Coverage

- Unit tests: business logic, algorithms, utilities
- Integration tests: component interactions, database access
- E2E tests: critical user workflows
- Avoid testing framework code or trivial getters/setters

## Domain-Driven Design Concepts

### Strategic Design

- Bounded contexts: explicit boundaries between models
- Ubiquitous language: shared vocabulary between devs and domain experts
- Context mapping: define relationships between bounded contexts

### Tactical Design

- **Entities**: Objects with identity that persists over time
- **Value Objects**: Immutable objects defined by their attributes
- **Aggregates**: Cluster of entities/VOs with consistency boundary
- **Domain Events**: Record of something significant that happened
- **Services**: Operations that don't belong to entities/VOs
- **Repositories**: Access to aggregates (collection illusion)

## Refactoring Practices

### When to Refactor

- Before adding features (make it easy to add)
- When you see duplication (DRY principle)
- When code smells appear (long functions, large classes, etc.)
- During code review feedback

### Common Refactorings

- Extract method/function
- Extract class/interface
- Rename for clarity
- Replace magic numbers with named constants
- Replace conditionals with polymorphism
- Introduce parameter object

### Code Smells to Avoid

- Long methods (>20-30 lines)
- Large classes (>300 lines)
- Long parameter lists (>3 params)
- Duplicated code
- Dead code
- Primitive obsession
- Feature envy
- Inappropriate intimacy

## Agile & XP Practices

### Core Practices

- Continuous integration
- Small, frequent releases
- Collective code ownership
- Coding standards (this document)
- Sustainable pace

### Development Cycle

1. Pick smallest valuable increment
2. Write test first (if TDD)
3. Implement simplest solution
4. Refactor for quality
5. Integrate immediately
6. Get feedback

### Simplicity Rules (in order)

1. Passes all tests
2. Reveals intention (clear names, structure)
3. No duplication (DRY)
4. Fewest elements (minimal code)

## Dependency Management

### Dependency Injection

- Prefer constructor injection
- Use DI container/framework when beneficial
- Avoid service locator pattern (hidden dependencies)

### Inversion of Control

- Framework calls your code, not vice versa
- Define interfaces for extension points
- Plugin architecture where appropriate

## Performance Considerations

- **Premature optimization is evil** - make it work, then measure
- **But design for performance** - choose right data structures, algorithms
- Profile before optimizing - don't guess bottlenecks
- Cache strategically - at appropriate layer with clear invalidation

## Security Principles

- Never trust user input - validate and sanitize
- Principle of least privilege
- Defense in depth - multiple security layers
- Fail securely - errors shouldn't leak sensitive info
- Keep dependencies updated

## Anti-Patterns to Avoid

- God objects (classes that do everything)
- Spaghetti code (no clear structure)
- Golden hammer (using same solution for every problem)
- Cargo cult programming (copying without understanding)
- Shotgun surgery (one change requires many edits)
- Leaky abstractions (implementation details bleeding through)

## When to Break Rules

Rules are guidelines, not laws. Break them when:

- The alternative is clearly worse
- You understand WHY the rule exists
- You document the deviation and reasoning
- The team agrees it's the right tradeoff

## Priorities (in order)

1. **Correct** - Software must work
2. **Maintainable** - Others (future you) can understand/change it
3. **Flexible** - Can adapt to new requirements
4. **Efficient** - Performs adequately (not prematurely optimized)
