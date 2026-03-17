---
name: microservices
description: |
    Microservice architecture patterns and practices based on Sam Newman's "Building Microservices" -- covering service decomposition, inter-service communication, data management, and operational patterns.
    USE FOR: microservice decomposition, inter-service communication, service mesh, API gateway, saga pattern, service discovery, distributed data management
    DO NOT USE FOR: monolithic architecture (use monoliths), event sourcing details (use event-driven), domain modeling (use domain-driven-design)
license: MIT
metadata:
  displayName: "Microservices"
  author: "Tyler-R-Kendrick"
compatibility: claude, copilot, cursor
references:
  - title: "Martin Fowler — Microservices Guide"
    url: "https://martinfowler.com/microservices/"
  - title: "Microservices — Wikipedia"
    url: "https://en.wikipedia.org/wiki/Microservices"
---

# Microservices Architecture

## Overview
Microservices architecture structures an application as a collection of loosely coupled, independently deployable services, each organized around a business capability. Each service owns its data, runs in its own process, and communicates over the network.

The canonical reference is Sam Newman's *Building Microservices* (O'Reilly, 2nd edition 2021), supplemented by *Monolith to Microservices* (Newman, 2019) for migration strategies.

**The First Rule of Microservices:** Don't start with microservices. Start with a monolith, understand your domain, and decompose when you have evidence that the benefits outweigh the operational costs. (See `dev/architecture/monoliths` for the monolith-first approach.)

## Service Decomposition

### By Business Capability
Align services to what the business does (e.g., Order Management, Inventory, Payments). This creates stable boundaries because business capabilities change less frequently than technical layers.

### By Subdomain (DDD-Aligned)
Use Domain-Driven Design bounded contexts as service boundaries (see `dev/architecture/domain-driven-design`):
- **Core subdomains** -- Your competitive advantage; build custom services.
- **Supporting subdomains** -- Necessary but not differentiating; simpler services or libraries.
- **Generic subdomains** -- Commodity; buy or use off-the-shelf (auth, email, payments).

### Decomposition Heuristics
| Heuristic | Description |
|-----------|-------------|
| **Single Responsibility** | Each service does one thing well |
| **Data ownership** | Each service owns its data; no shared databases |
| **Independent deployability** | Changing one service does not require deploying another |
| **Team alignment** | One team can own and operate the service end-to-end |
| **Bounded context boundary** | Service boundaries align with DDD bounded contexts |

## Inter-Service Communication

### Synchronous Communication

| Pattern | Protocol | When to Use |
|---------|----------|-------------|
| **Request/Response (REST)** | HTTP/JSON | Simple CRUD, external APIs, broad tooling support |
| **Request/Response (gRPC)** | HTTP/2 + Protobuf | Internal service-to-service; high throughput, strong typing, streaming |
| **GraphQL** | HTTP/JSON | Client-driven queries; aggregating multiple services for a frontend |

### Asynchronous Communication

| Pattern | Mechanism | When to Use |
|---------|-----------|-------------|
| **Event Notification** | Message broker (topic/pub-sub) | Decoupled notification; consumers decide what to do |
| **Event-Carried State Transfer** | Message broker with payload | Reduce synchronous callbacks; consumer has needed data |
| **Command Message** | Message broker (queue) | Tell a specific service to do something |
| **Async Request/Response** | Correlation ID + reply queue | Need a response but don't want to block |

**Rule of thumb:** Prefer asynchronous communication for inter-service calls. Use synchronous only when a real-time response is required (e.g., user-facing request/response).

### Communication Anti-Patterns
- **Distributed monolith** -- Services are "microservices" in name only; they deploy together, share databases, or cannot function independently.
- **Chatty interfaces** -- Excessive synchronous calls between services creating latency chains.
- **Shared database** -- Multiple services reading/writing the same tables destroys independent deployability.

## API Gateway

An API gateway sits between external clients and internal services, providing:
- **Request routing** -- Routes client requests to the appropriate microservice
- **Protocol translation** -- External REST to internal gRPC, for example
- **Authentication/Authorization** -- Centralized security enforcement
- **Rate limiting and throttling** -- Protect services from traffic spikes
- **Response aggregation** -- Combine responses from multiple services for a single client call

Common implementations: Kong, AWS API Gateway, Azure API Management, Envoy, NGINX, Ocelot (.NET).

## Service Mesh

A service mesh handles service-to-service networking concerns transparently via sidecar proxies:

```
┌──────────────────────┐    ┌──────────────────────┐
│  Service A           │    │  Service B           │
│  ┌────────────────┐  │    │  ┌────────────────┐  │
│  │ App Container  │  │    │  │ App Container  │  │
│  └───────┬────────┘  │    │  └───────▲────────┘  │
│          │           │    │          │           │
│  ┌───────▼────────┐  │    │  ┌───────┴────────┐  │
│  │ Sidecar Proxy  │──┼────┼─▶│ Sidecar Proxy  │  │
│  │ (Envoy)        │  │    │  │ (Envoy)        │  │
│  └────────────────┘  │    │  └────────────────┘  │
└──────────────────────┘    └──────────────────────┘
         Control Plane (Istio / Linkerd)
```

**Capabilities:** Mutual TLS, traffic management, retries, circuit breaking, observability (distributed tracing, metrics), canary deployments.

**Implementations:** Istio, Linkerd, Consul Connect, AWS App Mesh.

## Saga Pattern -- Distributed Transactions

Since each microservice owns its data, distributed transactions (2PC) are impractical. The saga pattern manages data consistency across services through a sequence of local transactions with compensating actions.

### Choreography (Event-Driven)
Each service publishes events that trigger the next step. No central coordinator.

```
Order Service ──(OrderCreated)──▶ Payment Service
Payment Service ──(PaymentProcessed)──▶ Inventory Service
Inventory Service ──(InventoryReserved)──▶ Shipping Service

On failure:
Inventory Service ──(ReservationFailed)──▶ Payment Service (refund)
Payment Service ──(RefundProcessed)──▶ Order Service (cancel)
```

**Pros:** Simple, decoupled, no single point of failure.
**Cons:** Hard to understand the overall flow; debugging is difficult; risk of cyclic dependencies.

### Orchestration (Central Coordinator)
A saga orchestrator (process manager) coordinates the steps explicitly.

```
┌─────────────────┐
│ Saga Orchestrator│
│ (Order Saga)     │
└────┬───┬───┬────┘
     │   │   │
     ▼   ▼   ▼
  Payment  Inventory  Shipping
  Service  Service    Service
```

**Pros:** Clear flow, easier to understand and debug, centralized compensation logic.
**Cons:** Orchestrator is a coupling point; risk of becoming a "god service."

**Guidance:** Use choreography for simple sagas (2-3 steps). Use orchestration for complex flows (4+ steps or complex compensation).

## Distributed Data Management

| Pattern | Description |
|---------|-------------|
| **Database per Service** | Each service has its own database; no shared access |
| **API Composition** | Query multiple services and aggregate results |
| **CQRS** | Separate read and write models for different optimization (see `dev/architecture/event-driven`) |
| **Event Sourcing** | Store state changes as events; derive current state (see `dev/architecture/event-driven`) |
| **Saga** | Manage distributed transactions through compensating actions |
| **Outbox Pattern** | Reliably publish events by writing to a local outbox table within the same transaction |

## Service Discovery

Services need to find each other in a dynamic environment where instances come and go.

| Approach | Examples | Mechanism |
|----------|----------|-----------|
| **Client-side discovery** | Netflix Eureka, Consul | Client queries registry, picks instance |
| **Server-side discovery** | AWS ALB, Kubernetes Services | Load balancer/proxy routes to available instance |
| **DNS-based** | Consul DNS, Kubernetes CoreDNS | Resolve service name to IP(s) via DNS |

In Kubernetes environments, server-side discovery via Services and DNS is the default and usually sufficient.

## Resilience Patterns

| Pattern | Purpose |
|---------|---------|
| **Circuit Breaker** | Stop calling a failing service; fail fast and allow recovery |
| **Retry with Backoff** | Retry transient failures with exponential backoff and jitter |
| **Bulkhead** | Isolate failures to prevent cascading (separate thread pools / connections) |
| **Timeout** | Set explicit timeouts on all remote calls; never wait forever |
| **Fallback** | Provide degraded but functional response when a service is unavailable |
| **Health Check** | Expose liveness and readiness endpoints for orchestrators |

## When NOT to Use Microservices

Microservices introduce significant operational complexity. Do not use them when:

- **Your team is small** (< 8-10 developers) -- The overhead exceeds the benefit.
- **Your domain is not well understood** -- You will draw the wrong boundaries and create a distributed monolith.
- **You lack operational maturity** -- You need CI/CD, monitoring, distributed tracing, container orchestration, and on-call practices before microservices are viable.
- **Latency is critical** -- Every network hop adds latency; monoliths have zero network overhead for internal calls.
- **Strong consistency is required everywhere** -- Microservices embrace eventual consistency; if your domain requires ACID transactions across multiple entities, a monolith may be simpler.
- **You are building an MVP or prototype** -- Speed of iteration matters more than scalability at this stage.

## Tradeoffs Summary

| Benefit | Cost |
|---------|------|
| Independent deployability | Operational complexity (CI/CD per service, monitoring, tracing) |
| Technology heterogeneity | Polyglot overhead; harder to maintain standards |
| Team autonomy | Coordination overhead; contract management |
| Scalability per service | Network latency; serialization/deserialization cost |
| Fault isolation | Distributed failure modes (partial failures, network partitions) |
| Organizational alignment | Requires mature DevOps culture |

## Best Practices
- Design for failure from day one: circuit breakers, retries, timeouts, bulkheads.
- Own your data: one database per service, no shared database access.
- Make inter-service communication observable: distributed tracing (OpenTelemetry), centralized logging, metrics.
- Use consumer-driven contract testing (Pact, Spring Cloud Contract) to prevent breaking changes.
- Prefer asynchronous communication; use synchronous calls only when necessary.
- Keep services small enough to be owned by a single team, but large enough to justify the operational overhead.
- Deploy independently, test independently, fail independently.
