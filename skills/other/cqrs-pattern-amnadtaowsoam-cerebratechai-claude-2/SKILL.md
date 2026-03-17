---
name: CQRS Pattern
description: Implementing Command Query Responsibility Segregation for separating read and write operations in distributed systems.
---

# CQRS Pattern (Command Query Responsibility Segregation)

## Overview

CQRS separates write operations (commands) from read operations (queries) so each
can scale and evolve independently. It is often paired with event sourcing but
can be used with traditional persistence as well.

## Table of Contents

1. [What is CQRS](#what-is-cqrs)
2. [Commands vs Queries](#commands-vs-queries)
3. [Separate Read and Write Models](#separate-read-and-write-models)
4. [CQRS Without Event Sourcing](#cqrs-without-event-sourcing)
5. [CQRS With Event Sourcing](#cqrs-with-event-sourcing)
6. [Eventual Consistency](#eventual-consistency)
7. [Read Model Projections](#read-model-projections)
8. [Sync vs Async Projections](#sync-vs-async-projections)
9. [Command Handlers](#command-handlers)
10. [Query Handlers](#query-handlers)
11. [Database per Model](#database-per-model)
12. [Materialized Views](#materialized-views)
13. [Implementation Patterns](#implementation-patterns)
14. [When to Use CQRS](#when-to-use-cqrs)
15. [Anti-Patterns](#anti-patterns)

---

## What is CQRS

CQRS splits the write model (commands) from the read model (queries). This allows
different data shapes, storage, and scaling strategies for each side.

## Commands vs Queries

- **Command**: Intent to change state (CreateOrder).
- **Query**: Read-only data request (GetOrderSummary).

Commands should be validated and enforce invariants; queries should be optimized
for fast reads.

## Separate Read and Write Models

Write model:
- Validates business rules
- Produces state changes
- Often normalized

Read model:
- Denormalized for fast queries
- Can join data across aggregates

## CQRS Without Event Sourcing

Use traditional DB for writes and a separate read replica or view:
- Write: transactional DB
- Read: read-optimized replica or cache

## CQRS With Event Sourcing

Command side writes events. Read models are projections built from events:
- Clear audit log
- Rebuildable views
- Eventual consistency by design

## Eventual Consistency

Reads may lag behind writes:
- Communicate staleness to clients
- Use read-your-write when required
- Provide consistent "status" endpoints

## Read Model Projections

Projection handler example:
```typescript
interface OrderCreated {
  orderId: string;
  customerId: string;
  total: number;
}

function projectOrderCreated(event: OrderCreated) {
  // Upsert into read model
}
```

## Sync vs Async Projections

- **Synchronous**: Lower staleness, higher latency.
- **Asynchronous**: Higher throughput, eventual consistency.

Pick based on SLA and complexity.

## Command Handlers

Command handlers should:
- Validate input
- Enforce invariants
- Persist changes atomically
- Emit events if needed

## Query Handlers

Query handlers should:
- Use read-optimized storage
- Avoid heavy joins if possible
- Paginate and cache aggressively

## Database per Model

Common patterns:
- Write DB: PostgreSQL/MySQL
- Read DB: Elastic, Redis, or denormalized tables

## Materialized Views

Materialized views provide fast reads and can be refreshed by projections or ETL.

## Implementation Patterns

Node.js example structure:
```
src/
  commands/
  command-handlers/
  queries/
  query-handlers/
  read-models/
```

Python example:
```
app/
  commands/
  handlers/
  read_models/
```

## When to Use CQRS

Use when:
- Read/write workloads differ significantly.
- Read models require different shapes.
- Complex business rules on write side.

Avoid when:
- Simple CRUD is enough.
- Team cannot manage added complexity.

## Anti-Patterns

- Sharing the same ORM model for reads and writes.
- Over-separating models without need.
- Ignoring consistency requirements.

## Related Skills
- `09-microservices/event-sourcing`
- `04-database/database-optimization`

## Best Practices

### Command Design

- **Use intent-revealing names**: Commands should clearly express user intent
- **Validate commands**: Validate before processing
- **Keep commands small**: Single responsibility per command
- **Include command metadata**: Add timestamps, user IDs, etc.
- **Design for idempotency**: Commands should be safe to retry

### Query Design

- **Optimize for reads**: Denormalize data for fast queries
- **Use appropriate storage**: Choose storage based on query patterns
- **Implement caching**: Cache frequently accessed data
- **Paginate results**: Support large result sets
- **Use query models**: Separate models optimized for different use cases

### Read/Write Separation

- **Use separate databases**: Different storage for reads and writes
- **Scale independently**: Scale read and write sides separately
- **Handle eventual consistency**: Accept temporary inconsistency
- **Communicate staleness**: Inform users of data freshness
- **Use read-your-writes when needed**: For strong consistency requirements

### Eventual Consistency

- **Design for lag**: Assume reads may lag behind writes
- **Provide status indicators**: Show data freshness to users
- **Use cache invalidation**: Invalidate cache on updates
- **Implement sync projections**: For critical data that needs consistency
- **Monitor lag**: Track time between writes and read availability

### Command Handlers

- **Validate invariants**: Enforce business rules before persistence
- **Use transactions**: Ensure atomic state changes
- **Emit events**: Publish events after state changes
- **Handle errors gracefully**: Return appropriate error responses
- **Log command execution**: Track command processing for debugging

### Query Handlers

- **Use read-optimized storage**: Query from read replicas or caches
- **Avoid complex joins**: Denormalize data to reduce joins
- **Implement pagination**: Support large result sets efficiently
- **Cache aggressively**: Cache frequently accessed data
- **Monitor query performance**: Track slow queries

### Database Configuration

- **Choose appropriate databases**: Match database to workload
- **Configure replication**: Set up read replicas for query side
- **Implement connection pooling**: Optimize database connections
- **Use appropriate indexes**: Index for read patterns
- **Monitor database health**: Track performance and errors

### Projection Management

- **Make projections rebuildable**: Allow complete rebuild from source
- **Use incremental updates**: Update projections as events arrive
- **Handle projection failures**: Retry failed projections
- **Monitor projection lag**: Track how far behind projections are
- **Version projections**: Support multiple projection versions

### Testing

- **Test command handlers**: Verify validation and state changes
- **Test query handlers**: Verify query results and performance
- **Test consistency scenarios**: Test eventual consistency behavior
- **Test failure scenarios**: Test error handling and recovery
- **Performance test**: Measure throughput and latency

### Monitoring

- **Track command metrics**: Monitor command processing rates and failures
- **Track query metrics**: Monitor query performance and patterns
- **Monitor lag**: Track time between writes and read availability
- **Set up alerts**: Notify on anomalies or failures
- **Create dashboards**: Visualize CQRS system health

## Checklist

### Design
- [ ] Identify read/write workload differences
- [ ] Design command models
- [ ] Design query models
- [ ] Choose appropriate databases
- [ ] Define consistency requirements

### Command Side
- [ ] Implement command validation
- [ ] Set up command handlers
- [ ] Configure write database
- [ ] Implement event publishing
- [ ] Add command logging

### Query Side
- [ ] Design read models
- [ ] Set up read database/replica
- [ ] Implement query handlers
- [ ] Configure caching
- [ ] Add query logging

### Eventual Consistency
- [ ] Define acceptable lag
- [ ] Implement status indicators
- [ ] Set up cache invalidation
- [ ] Configure sync projections
- [ ] Monitor lag metrics

### Projections
- [ ] Design projection schemas
- [ ] Implement projection handlers
- [ ] Set up incremental updates
- [ ] Configure projection rebuilds
- [ ] Monitor projection lag

### Database Setup
- [ ] Configure write database
- [ ] Configure read database/replica
- [ ] Set up connection pooling
- [ ] Configure replication
- [ ] Optimize indexes

### Caching
- [ ] Identify cacheable data
- [ ] Configure cache strategy
- [ ] Set up cache invalidation
- [ ] Monitor cache hit rates
- [ ] Configure cache expiration

### Monitoring
- [ ] Set up command metrics
- [ ] Set up query metrics
- [ ] Configure lag monitoring
- [ ] Create dashboards
- [ ] Set up alerts

### Testing
- [ ] Write command handler tests
- [ ] Write query handler tests
- [ ] Test consistency scenarios
- [ ] Performance test
- [ ] Test failure scenarios

### Documentation
- [ ] Document command models
- [ ] Document query models
- [ ] Document consistency requirements
- [ ] Create runbooks
- [ ] Maintain API documentation
