---
name: cqrs-event-sourcing
description: CQRS and Event Sourcing patterns for scalable, auditable systems with separated read/write models. Use when building audit-required systems, implementing temporal queries, or designing high-scale applications with complex domain logic.
---

# CQRS and Event Sourcing Patterns

Expert guidance for implementing Command Query Responsibility Segregation (CQRS) and Event Sourcing patterns to build scalable, auditable systems with complete historical tracking and optimized read/write models.

## When to Use This Skill

- Building systems requiring complete audit trails and compliance
- Implementing temporal queries ("show me the state at time T")
- Designing high-scale applications with complex domain logic
- Creating systems with significantly different read and write patterns
- Building event-driven architectures with historical replay capability
- Implementing systems requiring multiple read model projections
- Designing applications where understanding "what happened" is critical
- Building collaborative systems with conflict resolution needs

## Core Principles

### 1. Command Query Separation
Separate operations that change state (commands) from operations that read state (queries).

| Commands (Write) | Queries (Read) |
|-----------------|----------------|
| Express intent (CreateOrder, UpdatePrice) | Return data, never change state |
| Can be rejected (validation failures) | Can be cached and optimized |
| Return success/failure, not data | Multiple models for different needs |
| Change system state | Eventually consistent with writes |

### 2. Events as Source of Truth
Store state changes as immutable events rather than current state snapshots.

**Traditional**: Store what IS → `UPDATE users SET email = 'new@email.com'`
**Event Sourcing**: Store what HAPPENED → `APPEND UserEmailChanged event`

**Result**: Complete history, temporal queries, audit trail

### 3. Eventual Consistency
Accept temporary inconsistency between write and read models for scalability.

### 4. Domain-Driven Design Integration
- Aggregates enforce business invariants
- Events represent domain facts
- Commands express domain operations
- Bounded contexts define consistency boundaries

## Quick Reference

| Task | Load reference |
| --- | --- |
| CQRS implementation patterns | `skills/cqrs-event-sourcing/references/cqrs-patterns.md` |
| Event sourcing & snapshots | `skills/cqrs-event-sourcing/references/event-sourcing.md` |
| EventStoreDB & Axon Framework | `skills/cqrs-event-sourcing/references/event-store-tech.md` |
| Consistency patterns | `skills/cqrs-event-sourcing/references/consistency-patterns.md` |
| Best practices checklist | `skills/cqrs-event-sourcing/references/best-practices.md` |

## Workflow

1. **Identify** if CQRS/ES is appropriate (high audit, temporal, or scale needs)
2. **Design** commands expressing user intent
3. **Define** events as immutable facts (past tense naming)
4. **Implement** aggregates as consistency boundaries
5. **Create** projections optimized for specific query needs
6. **Handle** eventual consistency across bounded contexts

## Common Mistakes

- Using CQRS for simple CRUD applications (overkill)
- Large aggregates that span multiple consistency boundaries
- Modifying or deleting events after publication
- Skipping command validation before aggregate processing
- Missing idempotency in event handlers
- No versioning strategy for event schema evolution
- Tight coupling between aggregates (use ID references only)

## Resources

- **Books**: "Implementing Domain-Driven Design" (Vernon), "Event Sourcing & CQRS" (Betts et al)
- **Sites**: cqrs.wordpress.com, eventstore.com/blog, axoniq.io/resources
- **Tools**: EventStoreDB, Axon Framework, Marten, Eventuous
- **Patterns**: Event Sourcing, CQRS, Process Manager, Saga, Snapshot
