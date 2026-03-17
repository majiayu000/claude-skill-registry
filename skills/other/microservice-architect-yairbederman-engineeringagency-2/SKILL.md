---
name: microservice-architect
description: Guide the planning of microservices architecture. Use when designing, planning, or architecting a system using microservices.
---

# Microservice Architecture

Guided workflow for planning and designing microservices architecture.

## When to Use

- Designing new microservices system
- Breaking down a monolith
- Adding services to existing architecture
- Evaluating service boundaries

## Service Decomposition

### Domain-Driven Design Approach

1. **Identify Bounded Contexts**
   - Each context = potential service
   - Clear business capability ownership
   - Independent data ownership

2. **Map Service Boundaries**
   ```
   ┌─────────────────┐  ┌─────────────────┐
   │  User Service   │  │  Order Service  │
   │                 │  │                 │
   │ • Registration  │  │ • Cart          │
   │ • Authentication│  │ • Checkout      │
   │ • Profile       │  │ • Order history │
   └─────────────────┘  └─────────────────┘
           │                    │
           └──────┬─────────────┘
                  ▼
   ┌─────────────────────────────────┐
   │      Notification Service       │
   │                                 │
   │ • Email                         │
   │ • SMS                           │
   │ • Push notifications            │
   └─────────────────────────────────┘
   ```

3. **Apply Single Responsibility**
   - One service = one business capability
   - Changes isolated to single service
   - Independent deployment

## Communication Patterns

### Synchronous (REST/gRPC)

| Use When | Avoid When |
|----------|------------|
| Need immediate response | High latency tolerance |
| Simple request-response | Fan-out to many services |
| Read operations | Long-running operations |

### Asynchronous (Events/Messages)

| Use When | Avoid When |
|----------|------------|
| Eventual consistency OK | Immediate consistency required |
| Decoupling needed | Simple request-response |
| Fan-out to multiple services | Low complexity |

### Event-Driven Architecture

```
┌──────────────┐    publish     ┌─────────────────┐
│ Order Service│ ──────────────▶│   Event Bus     │
└──────────────┘  OrderCreated  └─────────────────┘
                                       │
                       ┌───────────────┼───────────────┐
                       ▼               ▼               ▼
              ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
              │ Inventory    │ │ Notification │ │ Analytics    │
              │ Service      │ │ Service      │ │ Service      │
              └──────────────┘ └──────────────┘ └──────────────┘
```

## Data Management

### Database per Service

- Each service owns its data
- No shared databases
- Data duplication acceptable

### Data Consistency Patterns

| Pattern | Use Case |
|---------|----------|
| Saga | Distributed transactions |
| CQRS | Read/write separation |
| Event Sourcing | Audit trail, temporal queries |

### Saga Pattern Example

```
Order Saga:
1. Order Service → Create order (PENDING)
2. Payment Service → Charge payment
   ├── Success → Continue
   └── Failure → Compensate: Cancel order
3. Inventory Service → Reserve items
   ├── Success → Continue
   └── Failure → Compensate: Refund, Cancel order
4. Order Service → Confirm order (CONFIRMED)
```

## Resilience Patterns

### Circuit Breaker

```typescript
const circuitBreaker = new CircuitBreaker({
  failureThreshold: 5,      // Open after 5 failures
  successThreshold: 3,      // Close after 3 successes
  timeout: 30000,           // Half-open after 30s
  fallback: () => cachedResponse
})

const result = await circuitBreaker.execute(() => 
  externalService.call()
)
```

### Retry with Backoff

```typescript
const retryConfig = {
  maxRetries: 3,
  baseDelay: 1000,
  maxDelay: 10000,
  exponential: true,
  jitter: true
}
```

### Bulkhead Pattern

- Isolate resources per service
- Prevent cascade failures
- Limit concurrent requests

## Service Discovery

```yaml
# Kubernetes Service
apiVersion: v1
kind: Service
metadata:
  name: user-service
spec:
  selector:
    app: user-service
  ports:
    - port: 80
      targetPort: 3000
```

## Observability

### The Three Pillars

1. **Logging** - Structured, correlated logs
2. **Metrics** - RED metrics (Rate, Errors, Duration)
3. **Tracing** - Distributed request tracing

### Service Mesh Benefits

- mTLS between services
- Traffic management
- Observability built-in
- Retry/timeout policies

## Architecture Decision Checklist

Before finalizing architecture:

- [ ] Service boundaries clearly defined
- [ ] Data ownership per service established
- [ ] Communication patterns chosen
- [ ] Consistency requirements documented
- [ ] Failure scenarios identified
- [ ] Resilience patterns decided
- [ ] Observability strategy defined
- [ ] Deployment strategy planned
- [ ] Security boundaries established
