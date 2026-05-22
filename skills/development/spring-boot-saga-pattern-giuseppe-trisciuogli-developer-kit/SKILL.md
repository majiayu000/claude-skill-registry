---
name: spring-boot-saga-pattern
description: Implement distributed transactions using the Saga Pattern in Spring Boot microservices. Use when building microservices requiring transaction management across multiple services, handling compensating transactions, ensuring eventual consistency, or implementing choreography or orchestration-based sagas with Spring Boot, Kafka, or Axon Framework.
allowed-tools: Read, Write, Bash
category: backend
tags: [spring-boot, saga, distributed-transactions, choreography, orchestration, microservices]
version: 1.1.0
---

# Spring Boot Saga Pattern

## When to Use

Implement this skill when:

- Building distributed transactions across multiple microservices
- Needing to replace two-phase commit (2PC) with a more scalable solution
- Handling transaction rollback when a service fails in multi-service workflows
- Ensuring eventual consistency in microservices architecture
- Implementing compensating transactions for failed operations
- Coordinating complex business processes spanning multiple services
- Choosing between choreography-based and orchestration-based saga approaches

**Trigger phrases**: distributed transactions, saga pattern, compensating transactions, microservices transaction, eventual consistency, rollback across services, orchestration pattern, choreography pattern

## Overview

The **Saga Pattern** is an architectural pattern for managing distributed transactions in microservices. Instead of using a single ACID transaction across multiple databases, a saga breaks the transaction into a sequence of local transactions. Each local transaction updates its database and publishes an event or message to trigger the next step. If a step fails, the saga executes **compensating transactions** to undo the changes made by previous steps.

### Key Architectural Decisions

When implementing a saga, make these decisions:

1. **Approach Selection**: Choose between **choreography-based** (event-driven, decoupled) or **orchestration-based** (centralized control, easier to track)
2. **Messaging Platform**: Select Kafka, RabbitMQ, or Spring Cloud Stream
3. **Framework**: Use Axon Framework, Eventuate Tram, Camunda, or Apache Camel
4. **State Persistence**: Store saga state in database for recovery and debugging
5. **Idempotency**: Ensure all operations (especially compensations) are idempotent and retryable

## Two Approaches to Implement Saga

### Choreography-Based Saga

Each microservice publishes events and listens to events from other services. **No central coordinator**.

**Best for**: Greenfield microservice applications with few participants

**Advantages**:
- Simple for small number of services
- Loose coupling between services
- No single point of failure

**Disadvantages**:
- Difficult to track workflow state
- Hard to troubleshoot and maintain
- Complexity grows with number of services

### Orchestration-Based Saga

A **central orchestrator** manages the entire transaction flow and tells services what to do.

**Best for**: Brownfield applications, complex workflows, or when centralized control is needed

**Advantages**:
- Centralized visibility and monitoring
- Easier to troubleshoot and maintain
- Clear transaction flow
- Simplified error handling
- Better for complex workflows

**Disadvantages**:
- Orchestrator can become single point of failure
- Additional infrastructure component

## Implementation Steps

### Step 1: Define Transaction Flow

Identify the sequence of operations and corresponding compensating transactions:

```
Order → Payment → Inventory → Shipment → Notification
   ↓         ↓         ↓          ↓           ↓
Cancel    Refund    Release    Cancel      Cancel
```

### Step 2: Choose Implementation Approach

- **Choreography**: Spring Cloud Stream with Kafka or RabbitMQ
- **Orchestration**: Axon Framework, Eventuate Tram, Camunda, or Apache Camel

### Step 3: Implement Services with Local Transactions

Each service handles its local ACID transaction and publishes events or responds to commands.

### Step 4: Implement Compensating Transactions

Every forward transaction must have a corresponding compensating transaction. Ensure **idempotency** and **retryability**.

### Step 5: Handle Failure Scenarios

Implement retry logic, timeouts, and dead-letter queues for failed messages.

## Best Practices

### Design Principles

1. **Idempotency**: Ensure compensating transactions execute safely multiple times
2. **Retryability**: Design operations to handle retries without side effects
3. **Atomicity**: Each local transaction must be atomic within its service
4. **Isolation**: Handle concurrent saga executions properly
5. **Eventual Consistency**: Accept that data becomes consistent over time

### Service Design

- Use **constructor injection** exclusively (never field injection)
- Implement services as **stateless** components
- Store saga state in persistent store (database or event store)
- Use **immutable DTOs** (Java records preferred)
- Separate domain logic from infrastructure concerns

### Error Handling

- Implement **circuit breakers** for service calls
- Use **dead-letter queues** for failed messages
- Log all saga events for debugging and monitoring
- Implement **timeout mechanisms** for long-running sagas
- Design **semantic locks** to prevent concurrent updates

### Testing

- Test happy path scenarios
- Test each failure scenario and its compensation
- Test concurrent saga executions
- Test idempotency of compensating transactions
- Use Testcontainers for integration testing

### Monitoring and Observability

- Track saga execution status and duration
- Monitor compensation transaction execution
- Alert on stuck or failed sagas
- Use distributed tracing (Spring Cloud Sleuth, Zipkin)
- Implement health checks for saga coordinators

## Technology Stack

**Spring Boot 3.x** with dependencies:

**Messaging**: Spring Cloud Stream, Apache Kafka, RabbitMQ, Spring AMQP

**Saga Frameworks**: Axon Framework (4.9.0), Eventuate Tram Sagas, Camunda, Apache Camel

**Persistence**: Spring Data JPA, Event Sourcing (optional), Transactional Outbox Pattern

**Monitoring**: Spring Boot Actuator, Micrometer, Distributed Tracing (Sleuth + Zipkin)

## Anti-Patterns to Avoid

❌ **Tight Coupling**: Services directly calling each other instead of using events
❌ **Missing Compensations**: Not implementing compensating transactions for every step
❌ **Non-Idempotent Operations**: Compensations that cannot be safely retried
❌ **Synchronous Sagas**: Waiting synchronously for each step (defeats the purpose)
❌ **Lost Messages**: Not handling message delivery failures
❌ **No Monitoring**: Running sagas without visibility into their status
❌ **Shared Database**: Using same database across multiple services
❌ **Ignoring Network Failures**: Not handling partial failures gracefully

## When NOT to Use Saga Pattern

Do not implement this pattern when:

- Single service transactions (use local ACID transactions instead)
- Strong consistency is required (consider monolith or shared database)
- Simple CRUD operations without cross-service dependencies
- Low transaction volume with simple flows
- Team lacks experience with distributed systems

## References

For detailed information, consult the following resources:

- [Saga Pattern Definition](references/01-saga-pattern-definition.md)
- [Choreography-Based Implementation](references/02-choreography-implementation.md)
- [Orchestration-Based Implementation](references/03-orchestration-implementation.md)
- [Event-Driven Architecture](references/04-event-driven-architecture.md)
- [Compensating Transactions](references/05-compensating-transactions.md)
- [State Management](references/06-state-management.md)
- [Error Handling and Retry](references/07-error-handling-retry.md)
- [Testing Strategies](references/08-testing-strategies.md)
- [Common Pitfalls and Solutions](references/09-pitfalls-solutions.md)

See also [examples.md](references/examples.md) for complete implementation examples:

- E-Commerce Order Processing (orchestration with Axon Framework)
- Food Delivery Application (choreography with Kafka and Spring Cloud Stream)
- Travel Booking System (complex orchestration with multiple compensations)
- Banking Transfer System
- Real-world microservices patterns

