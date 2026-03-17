---
name: system-design
description: Use when the Architect is designing system architecture, choosing technology stacks, defining data models, designing APIs, making scalability decisions, or updating ARCHITECTURE.md. Activates for any architecture design, technology evaluation, or system structure discussion.
version: 1.0.0
---

# System Design Expertise

## When This Applies

Apply this guidance when:
- Designing architecture for a new CR or project
- Updating ARCHITECTURE.md documents
- Choosing between technology approaches
- Defining data models, APIs, or component boundaries
- Making scalability or performance decisions

## Architecture Design Process

### Step 1: Understand Requirements

Before designing, extract from the CR:
- Functional requirements (what it must do)
- Non-functional requirements (performance, security, scalability)
- Constraints (existing tech stack, team expertise, timeline)
- Integration points (what it connects to)

### Step 2: Define Components

For each major feature:
1. Identify distinct responsibilities
2. Map to components (services, modules, layers)
3. Define interfaces between components
4. Minimize coupling, maximize cohesion

### Step 3: Choose Patterns

| Need | Pattern | When to Use |
|------|---------|-------------|
| Request/Response | REST API | Standard CRUD, simple interactions |
| Real-time | WebSocket / SSE | Live updates, notifications |
| Async processing | Message queue | Long-running tasks, decoupled systems |
| Data pipeline | Event-driven | Multiple consumers of same events |
| Simple app | Monolith | Small team, single deployment unit |
| Complex domains | Microservices | Independent scaling, team ownership |
| Read-heavy | CQRS | Separate read/write optimization |

### Step 4: Document

ARCHITECTURE.md should contain:
1. **Overview** — High-level system description and diagram (ASCII)
2. **Components** — Each component's responsibility and interfaces
3. **Data Model** — Entities, relationships, storage choices
4. **API Design** — Endpoints, request/response formats, auth
5. **Dependencies** — External services and libraries
6. **Decisions** — Key choices with rationale (ADR-style)

## API Design Guidelines

- Use consistent naming: `GET /resources`, `POST /resources`, `GET /resources/:id`
- Version APIs from the start: `/api/v1/...`
- Return consistent error formats with status codes and messages
- Document request/response schemas
- Design for backward compatibility

## Data Modeling Principles

- Normalize data to eliminate redundancy
- Define clear primary keys and relationships
- Plan for migrations from the start
- Consider read vs write patterns for storage choice
- Index fields that are frequently queried

## Scalability Considerations

- Identify potential bottlenecks early (database, network, compute)
- Design stateless services where possible
- Plan caching strategy (what to cache, invalidation)
- Consider horizontal vs vertical scaling for each component
- Define performance benchmarks and monitoring points
