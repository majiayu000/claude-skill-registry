---
name: arcanea-architecture-patterns
description: Master software architecture patterns for scalable, maintainable systems. From monoliths to microservices, from MVC to hexagonal - choose the right structure for every challenge.
version: 2.0.0
author: Arcanea
tags: [architecture, patterns, design, scalability, structure, development]
triggers:
  - architecture
  - system design
  - structure
  - patterns
  - scalability
  - how to structure
---

# The Architecture Patterns Codex

> *"Architecture is the art of making the complex manageable. Choose patterns that reveal intent, not hide it."*

---

## The Architecture Philosophy

### Why Architecture Matters

```
CODE is what the system DOES.
ARCHITECTURE is what the system IS.

Bad architecture makes good code hard to write.
Good architecture makes bad code easy to fix.

Architecture decisions are expensive to change.
Choose wisely. Change reluctantly.
```

---

## The Pattern Categories

### Structural Patterns

```
╔═══════════════════════════════════════════════════════════════════╗
║                    STRUCTURAL PATTERNS                             ║
╠═══════════════════════════════════════════════════════════════════╣
║                                                                    ║
║   LAYERED          │ Horizontal separation of concerns            ║
║   HEXAGONAL        │ Ports and adapters, domain-centric           ║
║   CLEAN            │ Dependencies point inward                    ║
║   VERTICAL SLICE   │ Feature-based organization                   ║
║   MODULAR MONOLITH │ Bounded contexts in single deployment        ║
║                                                                    ║
╚═══════════════════════════════════════════════════════════════════╝
```

### Distributed Patterns

```
╔═══════════════════════════════════════════════════════════════════╗
║                    DISTRIBUTED PATTERNS                            ║
╠═══════════════════════════════════════════════════════════════════╣
║                                                                    ║
║   MICROSERVICES    │ Independent deployable services              ║
║   EVENT-DRIVEN     │ Async communication via events               ║
║   CQRS             │ Separate read and write models               ║
║   EVENT SOURCING   │ Store events, derive state                   ║
║   SAGA             │ Distributed transactions                     ║
║                                                                    ║
╚═══════════════════════════════════════════════════════════════════╝
```

---

## Pattern Deep Dives

### The Layered Architecture

```
┌─────────────────────────────────────┐
│         PRESENTATION LAYER          │ ← UI, Controllers, Views
├─────────────────────────────────────┤
│          APPLICATION LAYER          │ ← Use Cases, Services
├─────────────────────────────────────┤
│           DOMAIN LAYER              │ ← Business Logic, Entities
├─────────────────────────────────────┤
│        INFRASTRUCTURE LAYER         │ ← Database, External APIs
└─────────────────────────────────────┘

RULES:
• Dependencies flow DOWN only
• Each layer knows only layer below
• Domain layer has ZERO dependencies
```

**When to Use:**
```
✓ Traditional business applications
✓ CRUD-heavy systems
✓ Teams familiar with MVC patterns
✓ Moderate complexity

✗ Highly dynamic requirements
✗ Event-heavy systems
✗ Complex business logic
```

### The Hexagonal Architecture (Ports & Adapters)

```
                    ┌───────────────┐
                    │   PRIMARY     │
                    │   ADAPTERS    │
                    │ (Controllers) │
                    └───────┬───────┘
                            │
                    ┌───────▼───────┐
                    │               │
            ┌───────┤    PORTS      ├───────┐
            │       │  (Interfaces) │       │
            │       └───────┬───────┘       │
            │               │               │
            │       ┌───────▼───────┐       │
            │       │               │       │
            │       │    DOMAIN     │       │
            │       │   (Core)      │       │
            │       │               │       │
            │       └───────┬───────┘       │
            │               │               │
            │       ┌───────▼───────┐       │
            │       │               │       │
            └───────┤    PORTS      ├───────┘
                    │  (Interfaces) │
                    └───────┬───────┘
                            │
                    ┌───────▼───────┐
                    │  SECONDARY    │
                    │   ADAPTERS    │
                    │ (Repositories)│
                    └───────────────┘

CORE INSIGHT:
Domain knows nothing about the outside world.
Adapters translate between domain and infrastructure.
```

**When to Use:**
```
✓ Domain-driven design projects
✓ Systems needing high testability
✓ Multiple input/output channels
✓ Long-lived business applications

✗ Simple CRUD applications
✗ Rapid prototypes
✗ Small teams with tight deadlines
```

### The Clean Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    FRAMEWORKS & DRIVERS                      │
│  ┌───────────────────────────────────────────────────────┐  │
│  │               INTERFACE ADAPTERS                       │  │
│  │  ┌─────────────────────────────────────────────────┐  │  │
│  │  │              APPLICATION LAYER                   │  │  │
│  │  │  ┌─────────────────────────────────────────┐   │  │  │
│  │  │  │            DOMAIN LAYER                  │   │  │  │
│  │  │  │         (Entities & Rules)              │   │  │  │
│  │  │  └─────────────────────────────────────────┘   │  │  │
│  │  │              (Use Cases)                        │  │  │
│  │  └─────────────────────────────────────────────────┘  │  │
│  │       (Controllers, Gateways, Presenters)              │  │
│  └───────────────────────────────────────────────────────┘  │
│          (Web, UI, DB, External Interfaces)                  │
└─────────────────────────────────────────────────────────────┘

THE DEPENDENCY RULE:
Dependencies point INWARD only.
Inner circles know nothing about outer circles.
```

### Vertical Slice Architecture

```
Traditional (Layered):           Vertical Slice:
┌──────────────────┐            ┌─────┬─────┬─────┐
│   Controllers    │            │  F  │  F  │  F  │
├──────────────────┤            │  E  │  E  │  E  │
│    Services      │            │  A  │  A  │  A  │
├──────────────────┤     →      │  T  │  T  │  T  │
│   Repositories   │            │  U  │  U  │  U  │
├──────────────────┤            │  R  │  R  │  R  │
│    Database      │            │  E  │  E  │  E  │
└──────────────────┘            │  1  │  2  │  3  │
                                └─────┴─────┴─────┘

INSIGHT:
Group by FEATURE, not by layer.
Each slice is independent and complete.
```

**When to Use:**
```
✓ Feature teams
✓ Rapid iteration
✓ Varying complexity per feature
✓ CQRS systems

✗ Highly shared logic
✗ Small applications
✗ Strong layer conventions required
```

---

## Distributed Architecture Patterns

### Microservices

```
┌─────────┐     ┌─────────┐     ┌─────────┐
│ Service │     │ Service │     │ Service │
│    A    │────▶│    B    │────▶│    C    │
└─────────┘     └─────────┘     └─────────┘
     │               │               │
     ▼               ▼               ▼
┌─────────┐     ┌─────────┐     ┌─────────┐
│  DB A   │     │  DB B   │     │  DB C   │
└─────────┘     └─────────┘     └─────────┘

PRINCIPLES:
1. Single responsibility per service
2. Own your data
3. Communicate via well-defined APIs
4. Deploy independently
5. Design for failure
```

**The Microservices Decision:**
```
CONSIDER MICROSERVICES WHEN:
• Multiple teams need autonomy
• Different scaling requirements per component
• Polyglot persistence needed
• Independent deployment critical
• Organization is distributed

AVOID MICROSERVICES WHEN:
• Small team (< 10 developers)
• Simple domain
• Tight deadlines
• Limited DevOps capability
• Unknown domain boundaries
```

### Event-Driven Architecture

```
┌──────────┐         ┌─────────────┐         ┌──────────┐
│ Producer │────────▶│ Event Bus   │────────▶│ Consumer │
└──────────┘         │ (Kafka/RMQ) │         └──────────┘
                     └─────────────┘
                           │
                     ┌─────┴─────┐
                     ▼           ▼
               ┌──────────┐ ┌──────────┐
               │ Consumer │ │ Consumer │
               └──────────┘ └──────────┘

EVENT TYPES:
• Domain Events: Something happened (OrderPlaced)
• Integration Events: Cross-boundary communication
• Commands: Request to do something
• Queries: Request for information
```

### CQRS (Command Query Responsibility Segregation)

```
┌─────────────────────────────────────────────┐
│                   Client                     │
└─────────────────┬───────────────────────────┘
                  │
        ┌─────────┴─────────┐
        ▼                   ▼
┌───────────────┐   ┌───────────────┐
│   COMMANDS    │   │    QUERIES    │
│   (Write)     │   │    (Read)     │
└───────┬───────┘   └───────┬───────┘
        │                   │
        ▼                   ▼
┌───────────────┐   ┌───────────────┐
│  Write Model  │   │  Read Model   │
│  (Normalized) │──▶│ (Optimized)   │
└───────────────┘   └───────────────┘

INSIGHT:
Reads and writes have different needs.
Optimize each independently.
```

---

## Architecture Decision Framework

### The SOLID Principles in Architecture

```
S - Single Responsibility
    Each component has one reason to change

O - Open/Closed
    Open for extension, closed for modification

L - Liskov Substitution
    Components should be replaceable

I - Interface Segregation
    Clients shouldn't depend on unused interfaces

D - Dependency Inversion
    Depend on abstractions, not concretions
```

### Choosing Your Architecture

```
START HERE:
┌────────────────────────────────────────────────────────────┐
│ What is your team size?                                    │
├────────────────────────────────────────────────────────────┤
│ < 5 developers  → Consider Modular Monolith               │
│ 5-15 developers → Consider Vertical Slices                │
│ 15+ developers  → Consider Microservices                  │
└────────────────────────────────────────────────────────────┘

THEN ASK:
□ How complex is the domain? (Simple → Layered)
□ How testable must it be? (High → Hexagonal/Clean)
□ How often does it change? (Often → Vertical Slices)
□ How independent are components? (Very → Microservices)
□ What are the scaling needs? (Variable → CQRS)
```

### The Strangler Fig Pattern

```
For migrating from legacy:

PHASE 1: Create new system alongside old
┌──────────┐     ┌──────────┐
│  Legacy  │     │   New    │
│  System  │     │  System  │
└──────────┘     └──────────┘

PHASE 2: Route new features to new system
┌──────────┐     ┌──────────┐
│  Legacy  │◀───▶│   New    │
│ (shrink) │     │ (grows)  │
└──────────┘     └──────────┘

PHASE 3: Migrate remaining features
             ┌──────────┐
             │   New    │
             │  System  │
             └──────────┘

PRINCIPLE: Never big-bang rewrite.
Gradually strangle the old with the new.
```

---

## Common Anti-Patterns

### The Big Ball of Mud
```
SYMPTOMS:
• No clear structure
• Everything depends on everything
• Changes have unpredictable effects
• Only original authors understand it

CAUSES:
• No upfront design
• Deadline pressure
• Lack of refactoring
• Knowledge silos

SOLUTION:
• Identify bounded contexts
• Extract modules gradually
• Establish clear interfaces
• Apply Strangler Fig
```

### The Distributed Monolith
```
SYMPTOMS:
• Microservices that must deploy together
• Shared databases
• Synchronous call chains
• Coupled release cycles

CAUSES:
• Wrong service boundaries
• Shared data without events
• Missing async patterns

SOLUTION:
• Merge tightly coupled services
• Introduce event-driven communication
• Apply domain-driven design
```

---

## Quick Reference

### Architecture Checklist
```
□ Clear separation of concerns
□ Dependencies point in one direction
□ Domain logic isolated
□ External dependencies abstracted
□ Components independently testable
□ Scaling strategy defined
□ Failure modes understood
□ Monitoring and observability planned
```

### Pattern Selection Matrix
```
| Need                    | Pattern              |
|-------------------------|----------------------|
| Simple CRUD             | Layered              |
| Complex domain          | Hexagonal/Clean      |
| Feature teams           | Vertical Slices      |
| Team autonomy           | Microservices        |
| Read/write separation   | CQRS                 |
| Audit trail             | Event Sourcing       |
| Distributed txns        | Saga                 |
| Legacy migration        | Strangler Fig        |
```

---

*"The best architecture is the one that makes the right thing easy and the wrong thing hard."*
