---
name: event-driven-architecture
description: Event-driven architecture patterns with event sourcing, CQRS, and message-driven communication. Use when designing distributed systems, microservices communication, or systems requiring eventual consistency and scalability.
---

# Event-Driven Architecture Patterns

Expert guidance for designing, implementing, and operating event-driven systems with proven patterns for event sourcing, CQRS, message brokers, saga coordination, and eventual consistency management.

## When to Use This Skill

- Designing systems with asynchronous, decoupled communication
- Implementing event sourcing and CQRS patterns
- Building systems requiring eventual consistency and high scalability
- Managing distributed transactions across microservices
- Processing real-time event streams and data pipelines
- Implementing publish-subscribe or message queue architectures
- Designing reactive systems with complex event flows

## Core Principles

### 1. Events as First-Class Citizens
Events represent immutable facts that have occurred in the system. Use past tense naming (OrderCreated, PaymentProcessed) and include all necessary context.

### 2. Eventual Consistency
Systems achieve consistency over time rather than immediately. Trade strong consistency for higher availability and scalability.

### 3. Loose Coupling
Services communicate through events without direct dependencies, enabling independent evolution and deployment.

### 4. Asynchronous Communication
Operations don't block waiting for responses, improving system responsiveness and resilience.

### 5. Event-Driven Thinking
Design around what happened (events) rather than what to do (commands).

## Quick Reference

| Topic | Load reference |
| --- | --- |
| Event structure, types, and characteristics | `skills/event-driven-architecture/references/event-fundamentals.md` |
| Event sourcing pattern and implementation | `skills/event-driven-architecture/references/event-sourcing.md` |
| CQRS pattern with read/write separation | `skills/event-driven-architecture/references/cqrs.md` |
| Message brokers (RabbitMQ, Kafka, SQS/SNS) | `skills/event-driven-architecture/references/message-brokers.md` |
| Saga pattern for distributed transactions | `skills/event-driven-architecture/references/saga-pattern.md` |
| Choreography vs orchestration patterns | `skills/event-driven-architecture/references/choreography-orchestration.md` |
| Eventual consistency and conflict resolution | `skills/event-driven-architecture/references/eventual-consistency.md` |
| Best practices, anti-patterns, testing | `skills/event-driven-architecture/references/best-practices.md` |

## Workflow

### 1. Design Phase
- **Identify Events**: What business facts need to be captured?
- **Define Boundaries**: Which events are domain vs integration events?
- **Choose Patterns**: Event sourcing? CQRS? Sagas? Choreography or orchestration?
- **Select Technology**: Kafka for high throughput? RabbitMQ for routing? AWS managed services?

### 2. Implementation Phase
- **Event Schema**: Define versioned event structures with correlation IDs
- **Event Store**: Implement append-only storage with optimistic concurrency
- **Projections**: Create read models from events for query optimization
- **Handlers**: Ensure idempotent, at-least-once delivery handling
- **Sagas**: Implement compensating transactions for failures

### 3. Operation Phase
- **Monitoring**: Track event lag, processing time, failure rates
- **Replay**: Build capability to replay events for debugging/recovery
- **Versioning**: Support multiple event schema versions simultaneously
- **Scaling**: Partition by aggregate ID, scale consumers horizontally
- **Testing**: Test handlers in isolation with contract testing

## Common Mistakes

### Event Design Errors
- ❌ Using commands instead of events (CreateOrder vs OrderCreated)
- ❌ Mutable events or missing versioning
- ❌ Events without correlation/causation IDs
- ✓ Immutable, past-tense, self-contained events

### Consistency Issues
- ❌ Assuming immediate consistency across services
- ❌ Not handling duplicate event delivery
- ❌ Missing idempotency in handlers
- ✓ Design for eventual consistency, idempotent handlers

### Architecture Mistakes
- ❌ Synchronous event chains (waiting for responses)
- ❌ Events coupled to specific service implementations
- ❌ No compensation strategy for sagas
- ✓ Async fire-and-forget, domain-focused events, compensating transactions

### Operational Gaps
- ❌ No event replay capability
- ❌ Missing monitoring for event lag
- ❌ No schema registry or version management
- ✓ Replay-ready, monitored, schema-managed events

## Pattern Selection Guide

### Use Event Sourcing When:
- Need complete audit trail of all changes
- Temporal queries required ("state at time T")
- Multiple projections from same events
- Event replay for debugging/recovery

### Use CQRS When:
- High read:write ratio (10:1+)
- Complex query requirements
- Need to scale reads independently
- Different databases for read/write optimal

### Use Sagas When:
- Distributed transactions across services
- Need atomicity without 2PC
- Complex multi-step workflows
- Compensation logic required

### Choose Choreography When:
- Simple workflows (2-4 steps)
- High service autonomy desired
- Event-driven culture established
- No complex dependencies

### Choose Orchestration When:
- Complex workflows (5+ steps)
- Sequential dependencies
- Need centralized visibility
- Business logic in workflow

## Resources

- **Books**: "Designing Event-Driven Systems" (Stopford), "Versioning in an Event Sourced System" (Young)
- **Sites**: eventuate.io, event-driven.io, Martin Fowler's event sourcing articles
- **Tools**: Kafka, EventStoreDB, RabbitMQ, Axon Framework, MassTransit
- **Patterns**: Event Sourcing, CQRS, Saga, Outbox, CDC, Event Streaming
