---
name: hexagonal-architecture
description: Design, implement, and maintain applications using hexagonal architecture (ports and adapters). Use when (1) designing new systems requiring clear separation between domain logic and infrastructure, (2) refactoring monolithic or tightly-coupled codebases toward cleaner boundaries, (3) reviewing architecture for dependency rule violations or layer leakage, (4) establishing testing strategies that isolate domain logic, or (5) evaluating whether hexagonal architecture suits a given problem domain.
---

# Hexagonal Architecture

Hexagonal architecture (Alistair Cockburn, 2005) isolates domain logic from infrastructure concerns through explicit boundaries called ports (interfaces the domain exposes or requires) and adapters (implementations that connect ports to the outside world).

## Core Invariants

These rules must hold throughout the codebase:

1. **Dependency rule**: All dependencies point inward. Domain knows nothing of adapters.
2. **Port ownership**: The domain defines port interfaces. Adapters implement them.
3. **Domain purity**: No framework imports, I/O operations, or infrastructure types in domain code.
4. **Adapter isolation**: Adapters never call each other directly; coordination happens through the domain.

## When Hexagonal Architecture Applies

**Strong fit:**
- Business logic complexity exceeds infrastructure complexity
- Multiple delivery mechanisms (API, CLI, queue consumers, scheduled jobs)
- Infrastructure likely to change (database migrations, vendor switches)
- Testability of domain logic is a priority
- Team scales beyond 2-3 engineers working on same codebase

**Poor fit:**
- CRUD-dominant applications with trivial business rules
- Prototypes or throwaway code
- Glue services that primarily transform and forward data
- Performance-critical paths where indirection cost matters

**Evaluate carefully:**
- Existing codebase with heavy framework coupling (high migration cost)
- Single delivery mechanism with stable infrastructure
- Small team with strong shared context

## Workflow

### 1. Domain Discovery

Before writing code, identify the bounded context:

1. **List domain operations** - What actions can actors perform? (e.g., "place order", "cancel subscription")
2. **Identify domain events** - What state changes matter to the business? (e.g., "order placed", "payment failed")
3. **Map external dependencies** - What does the domain need from the outside world? (databases, APIs, time, randomness)
4. **Enumerate delivery mechanisms** - How do actors interact with the system? (HTTP, CLI, message queues)

### 2. Port Design

Ports divide into two categories:

**Driving ports (primary)** - How the outside world invokes the domain:
- Application services / use cases
- Command handlers
- Query handlers

**Driven ports (secondary)** - What the domain needs from infrastructure:
- Repository interfaces
- External service gateways
- Notification dispatchers
- Clock/random abstractions

Design principles for ports:
- Name ports using domain language, not technical terms (`OrderRepository` not `PostgresOrderStore`)
- Keep port interfaces minimal—single responsibility per port
- Return domain types from ports, never infrastructure types
- Avoid leaking implementation details through port signatures

See [references/port-design.md](references/port-design.md) for detailed patterns.

### 3. Directory Structure

Canonical layout (language-agnostic):

```
src/
├── domain/                 # Pure business logic
│   ├── model/              # Entities, value objects, aggregates
│   ├── services/           # Domain services (stateless logic)
│   ├── events/             # Domain events
│   └── ports/              # Port interfaces (driven)
├── application/            # Use cases / application services
│   ├── commands/           # Write operations
│   ├── queries/            # Read operations
│   └── ports/              # Driving port interfaces (if separated)
├── adapters/               # Infrastructure implementations
│   ├── inbound/            # Driving adapters (HTTP, CLI, etc.)
│   │   ├── http/
│   │   └── cli/
│   └── outbound/           # Driven adapters (DB, APIs, etc.)
│       ├── persistence/
│       └── external/
└── config/                 # Composition root, DI wiring
```

Alternative flat structure for smaller projects:

```
src/
├── domain/
├── ports/
├── adapters/
└── main.py
```

### 4. Implementation Sequence

1. **Domain model first** - Entities, value objects, domain services. No dependencies.
2. **Define driven ports** - Repository interfaces, gateway interfaces.
3. **Implement application services** - Orchestrate domain logic, depend only on ports.
4. **Build driven adapters** - Database repositories, API clients. Implement port interfaces.
5. **Build driving adapters** - HTTP handlers, CLI commands. Call application services.
6. **Wire at composition root** - Dependency injection, configuration.

### 5. Testing Strategy

Layer-specific testing approach:

| Layer | Test Type | Dependencies | Purpose |
|-------|-----------|--------------|---------|
| Domain | Unit | None | Verify business rules in isolation |
| Application | Unit | Mocked ports | Verify orchestration logic |
| Adapters | Integration | Real infrastructure | Verify adapter correctness |
| System | E2E | Full stack | Verify wiring and contracts |

Key principle: Domain tests must run without any infrastructure. If a domain test requires a database connection, the architecture has leaked.

See [references/testing-strategies.md](references/testing-strategies.md) for implementation patterns.

### 6. Maintenance and Drift Detection

Architectural drift occurs when code violates the dependency rule over time. Detect and prevent drift through:

**Static analysis:**
- Import linting rules (domain must not import from adapters)
- Architecture fitness functions in CI
- Dependency analysis tools

**Code review checklist:**
- [ ] No infrastructure imports in domain/
- [ ] No domain types with ORM decorators or framework annotations
- [ ] Adapters implement port interfaces, not ad-hoc contracts
- [ ] New external dependencies introduced via ports, not direct calls

**Refactoring triggers:**
- Port interface grows beyond 5-7 methods (split by cohesion)
- Adapter requires domain knowledge to function (abstraction leak)
- Test requires infrastructure to verify domain rule (boundary violation)
- Same data transformation appears in multiple adapters (missing domain concept)

See [references/anti-patterns.md](references/anti-patterns.md) for common violations and remediation.

## Language-Specific Notes

Consult [references/language-specific.md](references/language-specific.md) for:
- Python: Protocol classes, ABC, structural vs nominal typing
- TypeScript: Interface patterns, dependency injection approaches
- Go: Interface satisfaction, package organisation
- Rust: Trait definitions, module boundaries

## Decision Records

When establishing hexagonal architecture in a project, document these decisions:

1. **Bounded context scope** - What's in, what's out
2. **Port granularity** - One repository per aggregate vs shared
3. **Error handling strategy** - Domain exceptions vs result types
4. **Event handling** - Sync vs async, in-process vs distributed
5. **Query model** - CQRS separation level (shared model, separate read model, separate store)
