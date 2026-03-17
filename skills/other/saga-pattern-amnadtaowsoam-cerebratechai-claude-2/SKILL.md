---
name: Saga Pattern
description: Implementing distributed transactions across microservices using the Saga pattern with choreography and orchestration approaches.
---

# Saga Pattern

## Overview

The Saga pattern manages distributed transactions by coordinating a series of local
transactions across microservices with compensating actions for rollback. It avoids
global locks and is a common alternative to 2PC in microservice architectures.

## Table of Contents

1. [What is a Saga](#what-is-a-saga)
2. [ACID vs BASE](#acid-vs-base)
3. [Saga vs 2PC](#saga-vs-2pc)
4. [Choreography vs Orchestration](#choreography-vs-orchestration)
5. [Compensating Transactions](#compensating-transactions)
6. [Saga Execution Coordinator](#saga-execution-coordinator)
7. [Idempotency](#idempotency)
8. [Error Handling and Retries](#error-handling-and-retries)
9. [State Management](#state-management)
10. [Messaging Integration](#messaging-integration)
11. [Frameworks](#frameworks)
12. [Testing Sagas](#testing-sagas)
13. [Real-World Examples](#real-world-examples)

---

## What is a Saga

A Saga is a sequence of local transactions where each step publishes an event or
invokes the next step. If a step fails, previously completed steps are undone via
compensating actions.

Use Sagas when:
- A workflow spans multiple services and databases.
- You can tolerate eventual consistency.
- Compensations are possible for each step.

## ACID vs BASE

- **ACID**: Strong consistency within a single database transaction.
- **BASE**: Basically Available, Soft state, Eventually consistent.

Sagas favor BASE to avoid distributed locks and improve availability.

## Saga vs 2PC

2PC coordinates commits across services with a global transaction manager but
introduces lock contention and single points of failure. Sagas trade strong
consistency for availability and scalability.

## Choreography vs Orchestration

### Choreography (Event-driven)
- Services listen for events and act independently.
- Lower coupling but harder to visualize the full flow.

### Orchestration (Central Coordinator)
- A coordinator explicitly calls steps and decides next actions.
- Easier to manage state and retries.

## Compensating Transactions

Each local transaction should have a compensating action to undo effects:

- Reserve inventory -> release inventory
- Authorize payment -> void payment
- Create shipment -> cancel shipment

Compensation must be idempotent and safe to retry.

## Saga Execution Coordinator

The coordinator tracks workflow state, transitions, and timeouts. It can be:
- A dedicated service
- A workflow engine (Temporal, Camunda)
- A library within a service

## Idempotency

Every step and compensation must be idempotent to handle retries:
- Use idempotency keys per saga step
- Deduplicate events by sagaId + stepId
- Persist state before side effects

## Error Handling and Retries

- Use exponential backoff for transient failures.
- Use DLQ or poison queues for repeated failures.
- Classify errors as retryable vs non-retryable.
- Trigger compensation on non-retryable failure.

## State Management

Persist saga state in a durable store:
- Status per step (pending, completed, compensated)
- Correlation IDs across services
- Timestamps for timeouts and SLAs

Example state model:
```json
{
  "sagaId": "order-123",
  "steps": [
    {"name": "reserveInventory", "status": "completed"},
    {"name": "authorizePayment", "status": "failed"}
  ],
  "status": "compensating"
}
```

## Messaging Integration

Use message brokers (Kafka, RabbitMQ) for decoupling:
- Emit events after local commit.
- Ensure at-least-once delivery + idempotent handlers.
- Use outbox pattern to avoid lost events.

## Frameworks

- **Temporal**: Durable workflows, retries, visibility.
- **Camunda**: BPMN orchestration with compensation logic.
- **Axon**: Sagas in event-sourced systems.

## Testing Sagas

- Unit test step handlers and compensations.
- Integration test full saga flow with a test broker.
- Chaos test partial failures and replays.

## Real-World Examples

**E-commerce order flow**:
1. Reserve inventory
2. Authorize payment
3. Create shipment
4. Confirm order

On failure: cancel shipment -> void payment -> release inventory.

**Payment processing**:
1. Validate payment
2. Create ledger entry
3. Notify merchant

Compensation: reverse ledger entry if notification fails.

## Related Skills
- `09-microservices/event-driven`
- `09-microservices/event-sourcing`
- `08-messaging-queue/kafka-patterns`

## Best Practices

### Saga Design

- **Keep sagas short**: Long-running sagas increase complexity and risk
- **Use compensating transactions**: Ensure every step can be undone
- **Make compensations idempotent**: Compensations should be safe to retry
- **Design for eventual consistency**: Accept temporary inconsistency during saga execution
- **Use correlation IDs**: Track saga instances across services

### Orchestration vs Choreography

- **Use orchestration for complex workflows**: When you need centralized control
- **Use choreography for simple workflows**: When services can act independently
- **Mix patterns appropriately**: Some workflows may benefit from hybrid approaches
- **Document decision criteria**: Clear guidelines for when to use each pattern

### Error Handling

- **Classify errors**: Distinguish between retryable and non-retryable errors
- **Use exponential backoff**: Retry with increasing delays for transient failures
- **Implement dead letter queues**: Route permanently failed messages for analysis
- **Set appropriate timeouts**: Don't let sagas hang indefinitely
- **Log saga state**: Maintain detailed logs for debugging

### State Management

- **Persist saga state**: Store state in durable storage
- **Use optimistic concurrency**: Version checks to prevent conflicts
- **Implement timeout handling**: Clean up stuck sagas
- **Design for replay**: Allow sagas to be restarted from checkpoints
- **Audit state changes**: Track all state transitions

### Messaging

- **Use message brokers**: Decouple services with Kafka, RabbitMQ, etc.
- **Ensure at-least-once delivery**: Configure QoS appropriately
- **Use outbox pattern**: Prevent event loss during database transactions
- **Implement idempotent handlers**: Handle duplicate messages safely
- **Monitor message flow**: Track message throughput and latency

### Testing

- **Test individual steps**: Unit test each saga step and compensation
- **Test compensation flows**: Verify rollback logic works correctly
- **Test failure scenarios**: Chaos test partial failures
- **Test saga restart**: Verify sagas can recover from checkpoints
- **Test performance**: Measure saga execution time under load

### Production Considerations

- **Monitor saga execution**: Track active, completed, and failed sagas
- **Set up alerts**: Notify on saga failures or timeouts
- **Implement dashboards**: Visualize saga flow and state
- **Document runbooks**: Clear procedures for handling saga issues
- **Plan for scale**: Design sagas to handle increased load

## Checklist

### Saga Design
- [ ] Identify workflows that need distributed transactions
- [ ] Design compensating transactions for each step
- [ ] Define saga timeout and retry policies
- [ ] Choose orchestration or choreography approach
- [ ] Document saga flow and decision points

### State Management
- [ ] Design saga state model
- [ ] Choose durable storage for saga state
- [ ] Implement optimistic concurrency control
- [ ] Set up timeout handling
- [ ] Design saga restart mechanism

### Compensation Logic
- [ ] Define compensation for each step
- [ ] Ensure compensations are idempotent
- [ ] Test compensation flows
- [ ] Handle compensation failures
- [ ] Document compensation behavior

### Messaging Setup
- [ ] Configure message broker (Kafka/RabbitMQ)
- [ ] Set up topics/queues for saga events
- [ ] Configure message ordering guarantees
- [ ] Implement outbox pattern
- [ ] Set up dead letter queues

### Error Handling
- [ ] Classify error types (retryable/non-retryable)
- [ ] Configure retry policies with backoff
- [ ] Set up DLQ for failed messages
- [ ] Implement timeout handling
- [ ] Add comprehensive logging

### Orchestration Setup
- [ ] Choose orchestration framework (Temporal, Camunda, custom)
- [ ] Configure workflow definitions
- [ ] Set up saga coordinator
- [ ] Implement saga instance tracking
- [ ] Configure retry and timeout policies

### Choreography Setup
- [ ] Define event schemas
- [ ] Set up event subscriptions
- [ ] Implement event handlers
- [ ] Configure event ordering
- [ ] Set up correlation ID tracking

### Monitoring
- [ ] Set up metrics collection
- [ ] Configure dashboards for saga state
- [ ] Set up alerts for failures
- [ ] Track saga execution time
- [ ] Monitor message flow

### Testing
- [ ] Write unit tests for saga steps
- [ ] Test compensation flows
- [ ] Test failure scenarios
- [ ] Test saga restart and recovery
- [ ] Perform load testing

### Documentation
- [ ] Document saga flows
- [ ] Document compensation logic
- [ ] Create runbooks for common issues
- [ ] Document monitoring setup
- [ ] Maintain API documentation
