---
name: clean-architecture
description: Clean Architecture principles and best practices from Robert C. Martin's book. This skill should be used when designing software systems, reviewing code structure, or refactoring applications to achieve better separation of concerns. Triggers on tasks involving layers, boundaries, dependency direction, entities, use cases, or system architecture.
---

# Clean Architecture Best Practices

Comprehensive guide to Clean Architecture principles for designing maintainable, testable software systems. Based on Robert C. Martin's "Clean Architecture: A Craftsman's Guide to Software Structure and Design." Contains 42 rules across 8 categories, prioritized by architectural impact.

## When to Apply

Reference these guidelines when:
- Designing new software systems or modules
- Structuring dependencies between layers
- Defining boundaries between business logic and infrastructure
- Reviewing code for architectural violations
- Refactoring coupled systems toward cleaner structure

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Dependency Direction | CRITICAL | `dep-` |
| 2 | Entity Design | CRITICAL | `entity-` |
| 3 | Use Case Isolation | HIGH | `usecase-` |
| 4 | Component Cohesion | HIGH | `comp-` |
| 5 | Boundary Definition | MEDIUM-HIGH | `bound-` |
| 6 | Interface Adapters | MEDIUM | `adapt-` |
| 7 | Framework Isolation | MEDIUM | `frame-` |
| 8 | Testing Architecture | LOW-MEDIUM | `test-` |

## Quick Reference

### 1. Dependency Direction (CRITICAL)

- [`dep-inward-only`](references/dep-inward-only.md) - Source dependencies point inward only
- [`dep-interface-ownership`](references/dep-interface-ownership.md) - Interfaces belong to clients not implementers
- [`dep-no-framework-imports`](references/dep-no-framework-imports.md) - Avoid framework imports in inner layers
- [`dep-data-crossing-boundaries`](references/dep-data-crossing-boundaries.md) - Use simple data structures across boundaries
- [`dep-acyclic-dependencies`](references/dep-acyclic-dependencies.md) - Eliminate cyclic dependencies between components
- [`dep-stable-abstractions`](references/dep-stable-abstractions.md) - Depend on stable abstractions not volatile concretions

### 2. Entity Design (CRITICAL)

- [`entity-pure-business-rules`](references/entity-pure-business-rules.md) - Entities contain only enterprise business rules
- [`entity-no-persistence-awareness`](references/entity-no-persistence-awareness.md) - Entities must not know how they are persisted
- [`entity-encapsulate-invariants`](references/entity-encapsulate-invariants.md) - Encapsulate business invariants within entities
- [`entity-value-objects`](references/entity-value-objects.md) - Use value objects for domain concepts
- [`entity-rich-not-anemic`](references/entity-rich-not-anemic.md) - Build rich domain models not anemic data structures

### 3. Use Case Isolation (HIGH)

- [`usecase-single-responsibility`](references/usecase-single-responsibility.md) - Each use case has one reason to change
- [`usecase-input-output-ports`](references/usecase-input-output-ports.md) - Define input and output ports for use cases
- [`usecase-orchestrates-not-implements`](references/usecase-orchestrates-not-implements.md) - Use cases orchestrate entities not implement business rules
- [`usecase-no-presentation-logic`](references/usecase-no-presentation-logic.md) - Use cases must not contain presentation logic
- [`usecase-explicit-dependencies`](references/usecase-explicit-dependencies.md) - Declare all dependencies explicitly in constructor
- [`usecase-transaction-boundary`](references/usecase-transaction-boundary.md) - Use case defines the transaction boundary

### 4. Component Cohesion (HIGH)

- [`comp-screaming-architecture`](references/comp-screaming-architecture.md) - Structure should scream the domain not the framework
- [`comp-common-closure`](references/comp-common-closure.md) - Group classes that change together
- [`comp-common-reuse`](references/comp-common-reuse.md) - Avoid forcing clients to depend on unused code
- [`comp-reuse-release-equivalence`](references/comp-reuse-release-equivalence.md) - Release components as cohesive units
- [`comp-stable-dependencies`](references/comp-stable-dependencies.md) - Depend in the direction of stability

### 5. Boundary Definition (MEDIUM-HIGH)

- [`bound-humble-object`](references/bound-humble-object.md) - Use humble objects at architectural boundaries
- [`bound-partial-boundaries`](references/bound-partial-boundaries.md) - Use partial boundaries when full separation is premature
- [`bound-boundary-cost-awareness`](references/bound-boundary-cost-awareness.md) - Weigh boundary cost against ignorance cost
- [`bound-main-component`](references/bound-main-component.md) - Treat main as a plugin to the application
- [`bound-defer-decisions`](references/bound-defer-decisions.md) - Defer framework and database decisions
- [`bound-service-internal-architecture`](references/bound-service-internal-architecture.md) - Services must have internal clean architecture

### 6. Interface Adapters (MEDIUM)

- [`adapt-controller-thin`](references/adapt-controller-thin.md) - Keep controllers thin
- [`adapt-presenter-formats`](references/adapt-presenter-formats.md) - Presenters format data for the view
- [`adapt-gateway-abstraction`](references/adapt-gateway-abstraction.md) - Gateways hide external system details
- [`adapt-mapper-translation`](references/adapt-mapper-translation.md) - Use mappers to translate between layers
- [`adapt-anti-corruption-layer`](references/adapt-anti-corruption-layer.md) - Build anti-corruption layers for external systems

### 7. Framework Isolation (MEDIUM)

- [`frame-domain-purity`](references/frame-domain-purity.md) - Domain layer has zero framework dependencies
- [`frame-orm-in-infrastructure`](references/frame-orm-in-infrastructure.md) - Keep ORM usage in infrastructure layer
- [`frame-web-in-infrastructure`](references/frame-web-in-infrastructure.md) - Web framework concerns stay in interface layer
- [`frame-di-container-edge`](references/frame-di-container-edge.md) - Dependency injection containers live at the edge
- [`frame-logging-abstraction`](references/frame-logging-abstraction.md) - Abstract logging behind domain interfaces

### 8. Testing Architecture (LOW-MEDIUM)

- [`test-tests-are-architecture`](references/test-tests-are-architecture.md) - Tests are part of the system architecture
- [`test-testable-design`](references/test-testable-design.md) - Design for testability from the start
- [`test-layer-isolation`](references/test-layer-isolation.md) - Test each layer in isolation
- [`test-boundary-verification`](references/test-boundary-verification.md) - Verify architectural boundaries with tests

## How to Use

Read individual reference files for detailed explanations and code examples:

- [Section definitions](references/_sections.md) - Category structure and impact levels
- [Rule template](assets/templates/_template.md) - Template for adding new rules

## Reference Files

| File | Description |
|------|-------------|
| [references/_sections.md](references/_sections.md) | Category definitions and ordering |
| [assets/templates/_template.md](assets/templates/_template.md) | Template for new rules |
| [metadata.json](metadata.json) | Version and reference information |
