---
name: arch-ddd
description: Apply Domain-Driven Design (DDD) architecture to backend projects. Use for tasks like defining bounded contexts, aggregates and invariants, entities/value objects, domain services, repositories, domain events, application services, anti-corruption layers, and aligning code structure and APIs with domain language while avoiding anemic models.
---

# arch-ddd

Use this skill to design or refactor a backend system toward DDD (领域驱动设计) with clear boundaries and maintainable evolution.

## Core principles (practical)

- **Ubiquitous Language**: domain terms in code, APIs, and docs must match.
- **Bounded Contexts**: separate subdomains with explicit boundaries; integrate via contracts.
- **Aggregate**: the unit of consistency; enforce invariants inside the aggregate.
- **Application vs Domain**: application services orchestrate; domain model owns rules.
- **Ports & Adapters**: infrastructure depends on domain/application, not the other way around.

## Deliverables (what “good” looks like)

- A list of bounded contexts + their responsibilities and integration points.
- Aggregate definitions (root, entities, value objects) + invariants.
- Command/query use-cases mapped to application services.
- Repository interfaces (in domain/application) + infra implementations.
- Domain events for cross-context integration (outbox if needed).

## Workflow

1) Understand the domain
- Identify actors, key workflows, nouns/verbs, and business constraints.
- Extract invariants (must always be true) and policies (may change).

2) Split bounded contexts
- Group capabilities that change together.
- Define context boundaries and “ownership” of data/behaviors.
- For each boundary: define integration style (sync API, async events, file/batch).

3) Define aggregates
- Start from invariants and transactions, not tables.
- Choose one aggregate root per consistency boundary.
- Keep aggregates small; reference other aggregates by ID only.

4) Define application services (use cases)
- Each endpoint maps to a use-case (command/query).
- Commands: validate, load aggregate, execute domain behavior, persist, publish events.
- Queries: read-optimized models (can be denormalized) and avoid domain coupling.

5) Persistence strategy
- Repository interface returns aggregates; hide ORM/SQL details.
- Avoid cross-aggregate joins in write paths; consider read models for queries.
- Use domain IDs (string/ULID/UUID) consistently across layers.

6) Integration patterns
- Cross-context sync: explicit contract DTOs; add Anti-Corruption Layer (ACL) when mapping is non-trivial.
- Cross-context async: domain events; versioned payloads; idempotent consumers.

7) Testing approach
- Domain: fast unit tests around invariants and behaviors.
- Application: use-case tests with fakes for repositories/outbox.
- Integration: contract tests for APIs/events; DB tests only where needed.

## Anti-patterns to avoid

- “Everything is a service”: domain logic scattered in application/service layer.
- Anemic domain model: entities are just getters/setters.
- Aggregate too large: one aggregate per table or “user” becomes god object.
- Tight coupling to DB schema: domain types leak ORM annotations everywhere.

## Code organization (suggested)

- `domain/`: aggregates, entities, value objects, domain services, domain events, repository interfaces
- `application/`: use-cases, command/query handlers, DTOs, mappers, transaction boundary
- `infrastructure/`: DB/ORM, message bus, external clients, repository implementations
- `interfaces/` (or `api/`): controllers/routers, request/response models, auth

