---
name: designing-architecture
description: Guides software architecture decisions, design patterns, and system design principles. Use when designing systems, choosing patterns, or making architectural decisions.
license: MIT
compatibility: opencode
metadata:
  category: design
  audience: developers
---

# Designing Architecture

Principles and patterns for designing maintainable, scalable, and robust software systems.

## When to Use This Skill

- Designing new systems or features
- Choosing between architectural patterns
- Making technology decisions
- Reviewing system design
- Planning for scalability
- Refactoring legacy systems

---

## Core Architecture Principles

### SOLID Principles

| Principle | Summary | Violation Sign |
|-----------|---------|----------------|
| **S**ingle Responsibility | One reason to change | Class does too many things |
| **O**pen/Closed | Open for extension, closed for modification | Modifying existing code for new features |
| **L**iskov Substitution | Subtypes replaceable for base types | Overrides break parent behavior |
| **I**nterface Segregation | Small, focused interfaces | Classes implement unused methods |
| **D**ependency Inversion | Depend on abstractions | High-level modules depend on low-level |

### The Dependency Rule

```
Outer layers depend on inner layers, NEVER the reverse.

┌─────────────────────────────────────┐
│     Frameworks & Drivers           │  ← Database, Web, UI
├─────────────────────────────────────┤
│     Interface Adapters             │  ← Controllers, Presenters, Gateways
├─────────────────────────────────────┤
│     Application Business Rules     │  ← Use Cases
├─────────────────────────────────────┤
│     Enterprise Business Rules      │  ← Entities
└─────────────────────────────────────┘

Dependencies point INWARD only.
```

---

## Architectural Patterns

### Layered Architecture

```
┌─────────────────────────────────────┐
│     Presentation Layer             │  ← UI, API Controllers
├─────────────────────────────────────┤
│     Application Layer              │  ← Use Cases, Services
├─────────────────────────────────────┤
│     Domain Layer                   │  ← Business Logic, Entities
├─────────────────────────────────────┤
│     Infrastructure Layer           │  ← Database, External APIs
└─────────────────────────────────────┘
```

**Use when**: Traditional applications, clear separation needed
**Avoid when**: High-performance needs, event-driven systems

### Hexagonal Architecture (Ports & Adapters)

```
           ┌───────────────┐
           │   Primary     │
           │   Adapters    │  ← REST API, CLI, GraphQL
           └───────┬───────┘
                   │
        ┌──────────▼──────────┐
        │                     │
        │   ┌───────────┐     │
        │   │   Core    │     │
Primary │   │  Domain   │     │ Secondary
Ports   │   │  Logic    │     │ Ports
        │   └───────────┘     │
        │                     │
        └──────────┬──────────┘
                   │
           ┌───────▼───────┐
           │   Secondary   │
           │   Adapters    │  ← Database, Message Queue, External API
           └───────────────┘
```

**Use when**: Testability is critical, multiple interfaces needed
**Avoid when**: Simple CRUD applications

### Microservices Architecture

```
┌─────────┐  ┌─────────┐  ┌─────────┐
│ Service │  │ Service │  │ Service │
│    A    │  │    B    │  │    C    │
└────┬────┘  └────┬────┘  └────┬────┘
     │            │            │
     └────────────┴────────────┘
                  │
           ┌──────▼──────┐
           │   Message   │
           │    Bus      │
           └─────────────┘
```

**Use when**: Independent scaling, team autonomy, polyglot needs
**Avoid when**: Small teams, simple domains, tight coupling required

### Event-Driven Architecture

```
Event Source → Event Bus → Event Handlers
     │              │              │
     ▼              ▼              ▼
  Produces    Routes Events    Consumes
  Events      (Kafka, RabbitMQ)  Events
```

**Use when**: Async processing, decoupling, audit trails
**Avoid when**: Immediate consistency required, simple workflows

---

## Design Patterns

### Creational Patterns

| Pattern | Purpose | When to Use |
|---------|---------|-------------|
| **Factory** | Create objects without specifying class | Object creation logic is complex |
| **Builder** | Construct complex objects step-by-step | Many optional parameters |
| **Singleton** | Single instance globally | Shared resource (use sparingly) |
| **Dependency Injection** | Inject dependencies externally | Testability, loose coupling |

### Structural Patterns

| Pattern | Purpose | When to Use |
|---------|---------|-------------|
| **Adapter** | Convert interface to another | Integrating incompatible systems |
| **Decorator** | Add behavior dynamically | Extending functionality without inheritance |
| **Facade** | Simplified interface to complex system | Hiding complexity |
| **Repository** | Abstract data access | Separating domain from persistence |

### Behavioral Patterns

| Pattern | Purpose | When to Use |
|---------|---------|-------------|
| **Strategy** | Interchangeable algorithms | Multiple ways to do something |
| **Observer** | Notify dependents of changes | Event systems, reactive updates |
| **Command** | Encapsulate actions as objects | Undo/redo, queuing, logging |
| **Chain of Responsibility** | Pass request along handlers | Middleware, validation chains |

---

## Domain-Driven Design Concepts

### Strategic Design

| Concept | Definition | Example |
|---------|------------|---------|
| **Bounded Context** | Explicit boundary for a domain model | Order context, Shipping context |
| **Ubiquitous Language** | Shared vocabulary between devs and domain experts | "Order", "Line Item", "Fulfillment" |
| **Context Map** | How bounded contexts relate | Customer shared between Sales and Support |

### Tactical Patterns

| Pattern | Purpose | Example |
|---------|---------|---------|
| **Entity** | Object with identity | User, Order |
| **Value Object** | Object without identity | Money, Address |
| **Aggregate** | Cluster of entities with root | Order + LineItems |
| **Domain Event** | Something that happened | OrderPlaced, PaymentReceived |
| **Repository** | Collection-like access to aggregates | OrderRepository |
| **Domain Service** | Logic that doesn't fit entities | PricingService |

---

## System Design Considerations

### Scalability Patterns

| Pattern | Description | Trade-off |
|---------|-------------|-----------|
| **Horizontal Scaling** | Add more instances | Statelessness required |
| **Vertical Scaling** | Bigger machines | Hardware limits |
| **Caching** | Store computed results | Cache invalidation |
| **Database Sharding** | Split data across DBs | Query complexity |
| **Read Replicas** | Separate read/write | Eventual consistency |
| **CDN** | Edge content delivery | Static content only |

### Resilience Patterns

| Pattern | Purpose | Implementation |
|---------|---------|----------------|
| **Circuit Breaker** | Prevent cascade failures | Fail fast when downstream is down |
| **Retry with Backoff** | Handle transient failures | Exponential delay between retries |
| **Bulkhead** | Isolate failures | Separate thread pools per dependency |
| **Timeout** | Bound waiting time | Max wait for responses |
| **Fallback** | Graceful degradation | Default behavior when service unavailable |

### Data Consistency Patterns

| Pattern | Consistency | Use When |
|---------|-------------|----------|
| **ACID Transactions** | Strong | Financial data, critical operations |
| **Saga** | Eventual | Distributed transactions |
| **Event Sourcing** | Eventual | Audit trails, complex state |
| **CQRS** | Eventual | Different read/write models |

---

## Technology Decision Framework

### When to Use a Database

| Need | Recommended | Avoid |
|------|-------------|-------|
| Relational data, ACID | PostgreSQL, MySQL | MongoDB |
| Document storage, flexible schema | MongoDB, DynamoDB | Relational |
| Key-value, high speed | Redis, Memcached | Relational |
| Time series | InfluxDB, TimescaleDB | Generic SQL |
| Graph relationships | Neo4j, Neptune | Relational (for complex) |
| Search | Elasticsearch, Meilisearch | Full table scans |

### When to Use Message Queues

| Need | Pattern |
|------|---------|
| Async processing | Queue (SQS, RabbitMQ) |
| Event broadcasting | Pub/Sub (SNS, Kafka) |
| Task scheduling | Delayed queues |
| Load leveling | Queue with workers |
| Event sourcing | Log-based (Kafka) |

---

## Architecture Decision Records (ADR)

### Template

```markdown
# ADR-001: [Title]

## Status
[Proposed | Accepted | Deprecated | Superseded by ADR-XXX]

## Context
[Why is this decision needed?]

## Decision
[What is the decision?]

## Consequences
### Positive
- [Benefit 1]
- [Benefit 2]

### Negative
- [Trade-off 1]
- [Trade-off 2]

## Alternatives Considered
1. [Alternative 1] - [Why rejected]
2. [Alternative 2] - [Why rejected]
```

---

## Anti-Patterns to Avoid

1. **Big Ball of Mud** - No clear structure, everything depends on everything
2. **Golden Hammer** - Using one pattern for all problems
3. **Premature Optimization** - Designing for scale before proving need
4. **Analysis Paralysis** - Over-designing, never shipping
5. **Distributed Monolith** - Microservices with tight coupling
6. **Anemic Domain Model** - Entities with only getters/setters
7. **God Object** - One class that does everything
8. **Leaky Abstraction** - Implementation details leak through interfaces

---

## Decision Checklist

Before finalizing an architecture decision, verify:

- [ ] Does it solve the actual problem?
- [ ] Is it the simplest solution that works?
- [ ] Can the team maintain it?
- [ ] Does it align with existing patterns?
- [ ] Is it testable?
- [ ] Can it evolve as requirements change?
- [ ] Are the trade-offs acceptable?
- [ ] Is the decision documented?

---

## Quick Reference

```
SOLID:
  S - Single Responsibility
  O - Open/Closed
  L - Liskov Substitution
  I - Interface Segregation
  D - Dependency Inversion

PATTERNS:
  Layered     → Simple, clear separation
  Hexagonal   → Testable, adaptable
  Microservices → Scalable, independent
  Event-Driven  → Decoupled, async

DDD BUILDING BLOCKS:
  Entity, Value Object, Aggregate
  Repository, Domain Event, Domain Service

SCALABILITY:
  Horizontal scaling, Caching, Sharding, CDN

RESILIENCE:
  Circuit Breaker, Retry, Bulkhead, Timeout
```
