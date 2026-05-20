---
name: spring-boot-saga-pattern
description: Provides distributed transaction patterns using the Saga Pattern in Spring Boot microservices. Use when building microservices requiring transaction management across multiple services, handling compensating transactions, ensuring eventual consistency, or implementing choreography or orchestration-based sagas with Spring Boot, Kafka, or Axon Framework.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
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

## Instructions

Follow these steps to implement saga pattern for distributed transactions:

### 1. Define Transaction Flow

Identify all services involved in the business process. Map out the sequence of local transactions and their corresponding compensating transactions.

### 2. Choose Saga Approach

Select choreography (event-driven, decentralized) or orchestration (centralized coordinator) based on team expertise and system complexity.

### 3. Design Domain Events

Create events for each transaction step (OrderCreated, PaymentProcessed, InventoryReserved). Include correlationId for tracing.

### 4. Implement Local Transactions

Ensure each service can complete its local transaction atomically within its own database boundary.

### 5. Define Compensating Transactions

For each forward operation, implement a compensating operation that reverses the effect (cancel order, refund payment, release inventory).

### 6. Set Up Message Broker

Configure Kafka or RabbitMQ with appropriate topics/queues. Implement idempotent message consumers.

### 7. Implement Orchestrator (if using orchestration)

Create a saga orchestrator service that tracks saga state, sends commands to participants, and handles compensations on failure.

### 8. Configure Choreography (if using choreography)

Set up event listeners in each service that react to events from other services and trigger next steps.

### 9. Handle Timeouts

Implement timeout mechanisms for each saga step. Configure dead-letter queues for messages that exceed processing time limits.

### 10. Add Monitoring

Track saga execution status, duration, and failure rates. Set up alerts for stuck or failed sagas.

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

## Constraints and Warnings

- Every forward transaction MUST have a corresponding compensating transaction.
- Compensating transactions MUST be idempotent to handle retry scenarios.
- Saga state MUST be persisted to handle failures and recovery.
- Never use synchronous communication between saga participants; it defeats the distributed nature.
- Be aware that sagas provide eventual consistency, not strong consistency.
- Monitor saga execution time and set appropriate timeouts to detect stuck sagas.
- Test all failure scenarios including partial failures to ensure proper compensation.
- Consider using a saga framework (Axon, Eventuate) for complex orchestrations to avoid reinventing the wheel.
- Ensure message brokers are highly available to prevent saga interruption.

## When NOT to Use Saga Pattern

Do not implement this pattern when:

- Single service transactions (use local ACID transactions instead)
- Strong consistency is required (consider monolith or shared database)
- Simple CRUD operations without cross-service dependencies
- Low transaction volume with simple flows
- Team lacks experience with distributed systems

## Examples

### Input: Monolithic Transaction (Anti-Pattern)

```java
@Transactional
public Order createOrder(OrderRequest request) {
    Order order = orderRepository.save(request);
    paymentService.charge(request.getPayment());
    inventoryService.reserve(request.getItems());
    shippingService.schedule(order);
    return order;
}
```

### Output: Saga-Based Distributed Transaction

```java
@Service
public class OrderSagaOrchestrator {
    public OrderSummary createOrder(OrderRequest request) {
        // Step 1: Create order
        Order order = orderService.createOrder(request);

        try {
            // Step 2: Process payment
            Payment payment = paymentService.processPayment(
                new PaymentRequest(order.getId(), request.getAmount()));

            // Step 3: Reserve inventory
            InventoryReservation reservation = inventoryService.reserve(
                new InventoryRequest(order.getItems()));

            // Step 4: Schedule shipping
            Shipment shipment = shippingService.schedule(
                new ShipmentRequest(order.getId()));

            return OrderSummary.completed(order, payment, reservation, shipment);

        } catch (PaymentFailedException e) {
            // Compensate: cancel order
            orderService.cancelOrder(order.getId());
            throw e;
        } catch (InsufficientInventoryException e) {
            // Compensate: refund payment, cancel order
            paymentService.refund(payment.getId());
            orderService.cancelOrder(order.getId());
            throw e;
        }
    }
}
```

### Input: Choreography Event Flow

```java
// Event published when order is created
@EventHandler
public void on(OrderCreatedEvent event) {
    // Trigger payment processing
    paymentService.processPayment(event.getOrderId());
}
```

### Output: Complete Choreography with Compensation

```java
@Service
public class OrderEventHandler {
    @KafkaListener(topics = "order.created")
    public void handleOrderCreated(OrderCreatedEvent event) {
        try {
            paymentService.processPayment(event.toPaymentRequest());
        } catch (PaymentException e) {
            kafkaTemplate.send("order.payment.failed", new PaymentFailedEvent(event.getOrderId()));
        }
    }
}

@Service
public class PaymentEventHandler {
    @KafkaListener(topics = "payment.processed")
    public void handlePaymentProcessed(PaymentProcessedEvent event) {
        inventoryService.reserve(event.toInventoryRequest());
    }

    @KafkaListener(topics = "payment.failed")
    public void handlePaymentFailed(PaymentFailedEvent event) {
        orderService.cancelOrder(event.getOrderId());
    }
}

@Service
public class InventoryEventHandler {
    @KafkaListener(topics = "inventory.reserved")
    public void handleInventoryReserved(InventoryReservedEvent event) {
        shippingService.scheduleShipment(event.toShipmentRequest());
    }

    @KafkaListener(topics = "inventory.insufficient")
    public void handleInsufficientInventory(InsufficientInventoryEvent event) {
        // Compensate: refund payment
        paymentService.refund(event.getPaymentId());
        // Compensate: cancel order
        orderService.cancelOrder(event.getOrderId());
    }
}
```

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

