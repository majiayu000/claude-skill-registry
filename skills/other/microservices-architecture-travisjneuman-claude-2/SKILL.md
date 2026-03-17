---
name: microservices-architecture
description: Microservices architecture patterns and best practices. Use when designing distributed systems, breaking down monoliths, or implementing service communication.
---

# Microservices Architecture

Comprehensive guide for designing and implementing microservices-based systems.

## Microservices Fundamentals

### What are Microservices?

```
MICROSERVICES = Independently deployable services
               that do one thing well

Characteristics:
┌─────────────────────────────────────────┐
│ ✓ Single responsibility                 │
│ ✓ Own their data                        │
│ ✓ Independently deployable              │
│ ✓ Communicate via APIs                  │
│ ✓ Technology agnostic                   │
│ ✓ Owned by small teams                  │
└─────────────────────────────────────────┘
```

### Monolith vs Microservices

```
MONOLITH:
┌─────────────────────────────────────────┐
│           Single Application            │
│  ┌──────┬──────┬──────┬──────┐         │
│  │ Users│Orders│ Cart │Search│         │
│  └──────┴──────┴──────┴──────┘         │
│           Single Database               │
└─────────────────────────────────────────┘

MICROSERVICES:
┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐
│Users │  │Orders│  │ Cart │  │Search│
│ DB   │  │ DB   │  │ DB   │  │ DB   │
└──────┘  └──────┘  └──────┘  └──────┘
    │         │         │         │
    └─────────┴─────────┴─────────┘
              API Gateway
```

### When to Use Microservices

```
USE WHEN:
✓ Large, complex domain
✓ Need independent scaling
✓ Multiple teams working in parallel
✓ Different technology needs per service
✓ Fault isolation is critical
✓ Frequent, independent deployments

DON'T USE WHEN:
✗ Small team/application
✗ Simple domain
✗ Tight latency requirements
✗ Limited DevOps maturity
✗ Unclear domain boundaries
```

---

## Service Design

### Domain-Driven Design

```
BOUNDED CONTEXTS:
┌─────────────────┐  ┌─────────────────┐
│   Orders        │  │   Shipping      │
│  Context        │  │   Context       │
│ ┌─────────────┐ │  │ ┌─────────────┐ │
│ │ Order       │ │  │ │ Shipment    │ │
│ │ LineItem    │ │  │ │ Carrier     │ │
│ │ Customer(ID)│ │  │ │ Address     │ │
│ └─────────────┘ │  │ └─────────────┘ │
└─────────────────┘  └─────────────────┘

Each context has its own:
- Ubiquitous language
- Data model
- Business rules
```

### Service Boundaries

```
GOOD boundaries follow:
┌─────────────────────────────────────────┐
│ Business Capability                     │
│ - What the business does                │
│ - e.g., Payment Processing, Inventory   │
├─────────────────────────────────────────┤
│ Subdomain                               │
│ - Area of expertise                     │
│ - e.g., Pricing, Catalog, Customer      │
├─────────────────────────────────────────┤
│ Single Responsibility                   │
│ - Does one thing well                   │
│ - Can explain in one sentence           │
└─────────────────────────────────────────┘

BAD boundaries:
✗ Technical layers (UI service, DB service)
✗ CRUD operations (User CRUD service)
✗ Too granular (EmailSender service)
```

### Service Size Guidelines

```
Right-sized service:
- 2-pizza team can own it (5-8 people)
- Rewrite in 2-4 weeks if needed
- Clear, single business purpose
- Minimal external dependencies
- Own its data completely

Too big: Multiple teams needed, mixed concerns
Too small: Can't function independently
```

---

## Communication Patterns

### Synchronous (Request/Response)

```
REST:
┌──────┐  HTTP GET /users/123  ┌──────┐
│Client│ ─────────────────────>│Server│
│      │<───────────────────── │      │
└──────┘  { "name": "John" }   └──────┘

gRPC:
┌──────┐  Binary/Protobuf      ┌──────┐
│Client│ ─────────────────────>│Server│
│      │<───────────────────── │      │
└──────┘  Strongly typed       └──────┘

GraphQL:
┌──────┐  POST /graphql        ┌──────┐
│Client│ ─────────────────────>│Server│
│      │<───────────────────── │      │
└──────┘  Flexible queries     └──────┘
```

### Asynchronous (Event-Driven)

```
MESSAGE QUEUE:
┌────────┐      ┌─────────┐      ┌────────┐
│Producer│ ───> │  Queue  │ ───> │Consumer│
└────────┘      │(RabbitMQ│      └────────┘
                │ SQS)    │
                └─────────┘

EVENT STREAMING:
┌────────┐      ┌─────────┐      ┌────────┐
│Producer│ ───> │  Topic  │ ───> │Consumer│
└────────┘      │ (Kafka) │ ───> │Consumer│
                └─────────┘ ───> │Consumer│
                                 └────────┘
```

### Communication Comparison

| Pattern             | Use Case                   | Trade-offs             |
| ------------------- | -------------------------- | ---------------------- |
| **REST**            | CRUD, simple queries       | Simple, but chatty     |
| **gRPC**            | High performance, internal | Fast, but complex      |
| **GraphQL**         | Flexible client needs      | Flexible, but overhead |
| **Message Queue**   | Task processing            | Decoupled, but delay   |
| **Event Streaming** | Event sourcing, analytics  | Scalable, but complex  |

---

## Data Management

### Database per Service

```
SEPARATE DATABASES:
┌────────┐  ┌────────┐  ┌────────┐
│Users   │  │Orders  │  │Products│
│Service │  │Service │  │Service │
├────────┤  ├────────┤  ├────────┤
│PostgreSQL│ │MongoDB │  │MySQL   │
└────────┘  └────────┘  └────────┘

Benefits:
✓ Independent scaling
✓ Technology freedom
✓ No shared schema coupling
✓ Fault isolation

Challenges:
- No joins across services
- Eventual consistency
- Data duplication
```

### Data Consistency Patterns

```
SAGA PATTERN (Choreography):
┌──────┐      ┌──────┐      ┌──────┐
│Order │─────>│Payment│─────>│Ship  │
│Create│      │Process│      │Order │
└──────┘      └──────┘      └──────┘
    │             │             │
    └─────────────┴─────────────┘
    Each service publishes events
    that trigger next step

SAGA PATTERN (Orchestration):
           ┌────────────┐
           │Orchestrator│
           └────────────┘
          /      │      \
         ↓       ↓       ↓
    ┌──────┐ ┌──────┐ ┌──────┐
    │Order │ │Payment│ │Ship  │
    └──────┘ └──────┘ └──────┘
    Central coordinator manages flow
```

### Event Sourcing

```
Instead of storing current state:
┌────────────────────────────┐
│ Account: $500              │
└────────────────────────────┘

Store all events:
┌────────────────────────────┐
│ 1. AccountCreated $0       │
│ 2. Deposited $1000         │
│ 3. Withdrawn $300          │
│ 4. Withdrawn $200          │
│ Current: $500              │
└────────────────────────────┘

Benefits:
✓ Complete audit trail
✓ Temporal queries
✓ Event replay
✓ Natural fit for CQRS
```

---

## API Gateway

### Gateway Pattern

```
               ┌─────────────┐
               │ API Gateway │
               └──────┬──────┘
        ┌──────────┬──┴──┬──────────┐
        ↓          ↓     ↓          ↓
   ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐
   │Users   │ │Orders  │ │Products│ │Auth    │
   │Service │ │Service │ │Service │ │Service │
   └────────┘ └────────┘ └────────┘ └────────┘

Gateway responsibilities:
- Request routing
- Authentication/Authorization
- Rate limiting
- Load balancing
- Request/Response transformation
- Caching
- Monitoring
```

### BFF (Backend for Frontend)

```
              Mobile App        Web App
                  │                │
                  ↓                ↓
          ┌────────────┐   ┌────────────┐
          │ Mobile BFF │   │  Web BFF   │
          └─────┬──────┘   └─────┬──────┘
                │                │
         ┌──────┴────────────────┴──────┐
         │         Internal APIs         │
         └───────────────────────────────┘

Each BFF:
- Optimized for its client
- Aggregates multiple services
- Handles client-specific logic
```

---

## Service Discovery

### Client-Side Discovery

```
┌──────┐     ┌──────────────┐
│Client│────>│Service       │────> Service A (192.168.1.10)
│      │     │Registry      │────> Service A (192.168.1.11)
│      │<────│(Consul, etcd)│────> Service A (192.168.1.12)
└──────┘     └──────────────┘

Client queries registry, then calls service directly.
Client handles load balancing.
```

### Server-Side Discovery

```
┌──────┐     ┌─────────────┐     ┌──────────────┐
│Client│────>│Load Balancer│────>│Service       │
│      │     │             │     │Registry      │
└──────┘     └─────────────┘     └──────────────┘
                                        │
                               ┌────────┴────────┐
                               ↓        ↓        ↓
                            Service  Service  Service

Load balancer handles discovery and routing.
Simpler for clients.
```

---

## Resilience Patterns

### Circuit Breaker

```
States:
┌────────┐    Failures    ┌────────┐
│ CLOSED │───────────────>│  OPEN  │
│(normal)│                │(reject)│
└────────┘                └────────┘
    ↑                          │
    │      Timeout             │
    │   ┌────────────┐         │
    └───│HALF-OPEN   │<────────┘
        │(test)      │
        └────────────┘

Implementation:
- Track failure count
- Open circuit after threshold
- Reject calls while open
- Periodically test with half-open
- Close circuit on success
```

### Retry Pattern

```typescript
async function withRetry<T>(
  fn: () => Promise<T>,
  maxAttempts: number = 3,
  backoff: number = 1000,
): Promise<T> {
  for (let attempt = 1; attempt <= maxAttempts; attempt++) {
    try {
      return await fn();
    } catch (error) {
      if (attempt === maxAttempts) throw error;

      // Exponential backoff with jitter
      const delay = backoff * Math.pow(2, attempt - 1);
      const jitter = delay * 0.1 * Math.random();
      await sleep(delay + jitter);
    }
  }
}
```

### Bulkhead Pattern

```
Isolate resources to prevent cascade:

┌─────────────────────────────────────┐
│           Service A                 │
│  ┌─────────┐  ┌─────────┐          │
│  │Thread   │  │Thread   │          │
│  │Pool 1   │  │Pool 2   │          │
│  │(Service │  │(Service │          │
│  │   B)    │  │   C)    │          │
│  └─────────┘  └─────────┘          │
└─────────────────────────────────────┘

If Service C is slow, only Pool 2 is affected.
Service B calls continue normally.
```

### Timeout Pattern

```typescript
async function withTimeout<T>(fn: () => Promise<T>, ms: number): Promise<T> {
  return Promise.race([
    fn(),
    new Promise<T>((_, reject) =>
      setTimeout(() => reject(new Error("Timeout")), ms),
    ),
  ]);
}

// Always set timeouts on external calls
const user = await withTimeout(
  () => userService.getUser(id),
  5000, // 5 second timeout
);
```

---

## Observability

### The Three Pillars

```
LOGS:
┌─────────────────────────────────────────┐
│ 2024-01-15 10:30:45 [INFO] OrderService │
│ Order created: { id: 123, user: 456 }   │
└─────────────────────────────────────────┘

METRICS:
┌─────────────────────────────────────────┐
│ order_created_total: 1523               │
│ order_processing_seconds: 0.234         │
│ active_connections: 45                  │
└─────────────────────────────────────────┘

TRACES:
┌─────────────────────────────────────────┐
│ [Request ID: abc123]                    │
│ ├─ Gateway: 2ms                         │
│ ├─ OrderService: 150ms                  │
│ │  ├─ UserService: 45ms                 │
│ │  └─ InventoryService: 80ms            │
│ └─ Total: 152ms                         │
└─────────────────────────────────────────┘
```

### Distributed Tracing

```
Trace Context Propagation:
┌──────┐  X-Trace-ID: abc  ┌──────┐
│API   │─────────────────>│Order │
│GW    │                   │Svc   │
└──────┘                   └──────┘
                              │
              X-Trace-ID: abc │
                              ↓
                           ┌──────┐
                           │User  │
                           │Svc   │
                           └──────┘

Tools: Jaeger, Zipkin, AWS X-Ray, Datadog
```

### Health Checks

```typescript
// Liveness: Is the service running?
app.get("/health/live", (req, res) => {
  res.status(200).json({ status: "alive" });
});

// Readiness: Is the service ready to handle traffic?
app.get("/health/ready", async (req, res) => {
  const dbHealthy = await checkDatabase();
  const cacheHealthy = await checkCache();

  if (dbHealthy && cacheHealthy) {
    res.status(200).json({ status: "ready" });
  } else {
    res.status(503).json({
      status: "not ready",
      checks: { database: dbHealthy, cache: cacheHealthy },
    });
  }
});
```

---

## Deployment

### Containerization

```dockerfile
# Dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY dist ./dist

USER node

EXPOSE 3000

CMD ["node", "dist/main.js"]
```

### Kubernetes Basics

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: order-service
spec:
  replicas: 3
  selector:
    matchLabels:
      app: order-service
  template:
    metadata:
      labels:
        app: order-service
    spec:
      containers:
        - name: order-service
          image: order-service:1.0.0
          ports:
            - containerPort: 3000
          resources:
            limits:
              cpu: "500m"
              memory: "256Mi"
          livenessProbe:
            httpGet:
              path: /health/live
              port: 3000
          readinessProbe:
            httpGet:
              path: /health/ready
              port: 3000
```

---

## Testing Strategies

### Test Pyramid for Microservices

```
              /\
             /  \  E2E Tests
            /────\  (Few, slow, brittle)
           /      \
          /────────\  Contract Tests
         /          \  (Service boundaries)
        /────────────\
       /              \  Integration Tests
      /────────────────\  (With dependencies)
     /                  \
    /────────────────────\  Unit Tests
   /                      \  (Many, fast, isolated)
  /________________________\
```

### Contract Testing

```typescript
// Consumer test (Order Service)
describe("User Service Contract", () => {
  it("returns user by ID", async () => {
    // Define expected interaction
    await provider.addInteraction({
      state: "user 123 exists",
      uponReceiving: "a request for user 123",
      withRequest: {
        method: "GET",
        path: "/users/123",
      },
      willRespondWith: {
        status: 200,
        body: {
          id: "123",
          name: like("John"),
          email: like("john@example.com"),
        },
      },
    });

    // Test passes if consumer expectations match
  });
});
```

---

## Best Practices

### DO:

- Start with a monolith, extract services later
- Define clear service boundaries
- Use asynchronous communication where possible
- Implement circuit breakers
- Centralize logging and monitoring
- Automate everything
- Design for failure
- Version your APIs

### DON'T:

- Create too many, too small services
- Share databases between services
- Make synchronous chains too deep
- Ignore distributed system complexities
- Couple services through shared libraries
- Skip contract testing
- Deploy without monitoring

---

## Migration Checklist

### Monolith to Microservices

- [ ] Map domain boundaries clearly
- [ ] Identify candidate services (start small)
- [ ] Establish CI/CD for new services
- [ ] Implement API gateway
- [ ] Set up service discovery
- [ ] Add distributed tracing
- [ ] Implement circuit breakers
- [ ] Extract first service (strangler fig pattern)
- [ ] Test extensively
- [ ] Monitor and iterate
