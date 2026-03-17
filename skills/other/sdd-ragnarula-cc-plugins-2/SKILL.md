---
name: distributed-systems
description: Use this skill when designing or reviewing distributed systems, microservices, event-driven architectures, or any system involving multiple networked components that must coordinate. Applies distributed systems thinking to specifications, designs, and implementations.
version: 0.1.0
---

# Distributed Systems Engineering

## When to Apply

Use this skill when the system involves:
- Multiple services communicating over a network
- Data that must be consistent across nodes
- Operations that span service boundaries
- Event-driven or message-based architectures
- Systems requiring high availability or fault tolerance

## Mindset

Distributed systems experts assume failure is normal and design for it.

**Questions to always ask:**
- What happens if this call fails halfway through?
- What happens if this message is delivered twice?
- What happens if these two operations happen concurrently?
- What happens during a network partition?
- What happens if this service is slow or unavailable?
- Where does authoritative state live?
- What are the consistency requirements - and are they actually needed?

**Assumptions to challenge:**
- "It won't fail" - Networks fail. Disks fail. Services fail.
- "It's fast enough" - Latency varies. P99 matters more than average.
- "Order is preserved" - Networks reorder. Clocks drift.
- "It only happens once" - Messages retry. Users double-click.
- "Clocks are synchronized" - They're not. Avoid wall-clock ordering across nodes.
- "The network is reliable" - It's not. Plan for partitions.

## Practices

### Idempotency
Every mutating operation needs an idempotency key. Store keys with results to return consistent responses on retry. Document how long keys are valid. **Don't** assume operations only execute once.

### Timeouts & Deadlines
Every network call needs a timeout. Propagate deadline budgets across service calls, leaving margin for retries. **Don't** make calls without timeouts or ignore deadline propagation.

### Retries & Circuit Breakers
Use exponential backoff with jitter. Set maximum retry limits. Implement circuit breakers to fail fast when downstream is unhealthy. Distinguish retryable errors from permanent failures. **Don't** retry infinitely, retry without backoff, or retry non-retryable errors.

### Consistency Model
Choose and document the consistency model: strong, eventual, causal. Design UIs to handle stale reads gracefully. Use read-your-writes where UX demands it. **Don't** assume "consistent" without specifying what kind, or promise stronger consistency than you deliver.

### Failure Handling
Design for partial failure. Use sagas with compensation logic for multi-step operations. Define degraded states and fallback behavior. **Don't** use distributed transactions across services, hold locks across network calls, or leave state inconsistent on failure.

### Event Design
Events are immutable facts, not commands. Include enough context to process independently. Design handlers to be idempotent and tolerate out-of-order delivery. **Don't** assume event ordering or require external lookups to process events.

### Service Boundaries
Services own their data. Communicate through APIs or events, not shared databases. Services should be independently deployable. **Don't** create distributed monoliths with tight coupling, shared databases, or synchronized deployments.

### Observability
Use distributed tracing with correlation IDs across all services. Measure latency percentiles (p50, p95, p99), not just averages. Alert on error rates and latency degradation. **Don't** rely on logs alone or measure only averages.

## Vocabulary

Use precise terminology:

| Instead of | Say |
|------------|-----|
| "consistent" | "strongly/eventually/causally consistent" |
| "fast" | "p99 latency < Xms" |
| "reliable" | "at-least-once delivery" / "exactly-once processing" |
| "available" | "99.9% availability" / "survives single-node failure" |
| "transaction" | "local transaction" / "saga" |
| "lock" | "optimistic locking" / "lease" |

## SDD Integration

**During Specification:**
- Ensure NFRs specify consistency model, latency percentiles, availability targets
- Flag vague terms like "fast", "reliable", "consistent"
- Ask about failure scenarios and acceptable degraded states

**During Design:**
- Verify idempotency strategy for each mutating operation
- Check that failure modes are documented per component
- Ensure retry policies and timeouts are specified
- Validate that the consistency model matches the architecture

**During Review:**
- Apply the mindset questions to each component
- Verify practices are followed
- Flag vocabulary violations
