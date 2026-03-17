---
name: microservices-patterns
description: Comprehensive microservices architecture patterns covering service decomposition, communication, data management, and resilience strategies. Use when designing distributed systems, breaking down monoliths, or implementing service-to-service communication.
---

# Microservices Architecture Patterns

Expert guidance for designing, implementing, and operating microservices architectures.

## When to Use This Skill

- Breaking down monolithic applications into services
- Designing distributed systems from scratch
- Implementing service communication patterns (sync/async)
- Managing data consistency across services
- Building resilient distributed systems
- Defining service boundaries and API contracts

## Core Principles

1. **Single Responsibility** - Each service has one reason to change
2. **Independent Deployability** - No coordination required for deployments
3. **Decentralized Data** - Each service owns its data exclusively
4. **Design for Failure** - Embrace failures, build resilience
5. **Automate Everything** - Deployment, scaling, and recovery

## Quick Reference

Load detailed patterns on-demand:

| Task | Load Reference |
| --- | --- |
| Define service boundaries and decompose monoliths | `skills/microservices-patterns/references/service-decomposition.md` |
| Implement service communication (sync/async) | `skills/microservices-patterns/references/communication-patterns.md` |
| Manage data consistency and transactions | `skills/microservices-patterns/references/data-management.md` |
| Build resilient systems (circuit breakers, retries) | `skills/microservices-patterns/references/resilience-patterns.md` |
| Add observability (tracing, logging, metrics) | `skills/microservices-patterns/references/observability.md` |
| Plan deployments and migrations | `skills/microservices-patterns/references/deployment-migration.md` |

## Workflow

### 1. Understand Requirements
- Map business capabilities and domains
- Assess scalability/resilience needs
- Identify team boundaries

### 2. Define Service Boundaries
Load `references/service-decomposition.md` for:
- Business capability decomposition
- DDD bounded contexts
- Service boundary validation

### 3. Design Communication
Load `references/communication-patterns.md` for:
- Synchronous: API Gateway, REST, gRPC
- Asynchronous: Message Queue, Pub/Sub, Event Sourcing

### 4. Manage Data
Load `references/data-management.md` for:
- Database per service pattern
- Saga distributed transactions
- CQRS read/write optimization

### 5. Build Resilience
Load `references/resilience-patterns.md` for:
- Circuit breakers
- Retry with exponential backoff
- Bulkhead isolation
- Rate limiting and timeouts

### 6. Add Observability
Load `references/observability.md` for:
- Distributed tracing
- Centralized logging
- Metrics and monitoring

### 7. Plan Deployment
Load `references/deployment-migration.md` for:
- Blue-Green, Canary, Rolling deployments
- Strangler Fig migration pattern

## Common Mistakes

1. **Distributed Monolith** - Tightly coupled, must deploy together
2. **Shared Database** - Multiple services accessing same database
3. **Chatty APIs** - Excessive synchronous service calls
4. **Missing Circuit Breakers** - No cascading failure protection
5. **No Observability** - Deploying without tracing/logging/metrics
6. **Ignoring Network Failures** - Assuming reliable network
7. **No API Versioning** - Breaking changes without versioning

**Fixes**: Load relevant reference files for detailed solutions.

## Resources

- **Books**: "Building Microservices" (Newman), "Microservices Patterns" (Richardson)
- **Sites**: microservices.io, martinfowler.com/microservices
- **Tools**: Kubernetes, Istio, Kafka, Kong, Jaeger, Prometheus
