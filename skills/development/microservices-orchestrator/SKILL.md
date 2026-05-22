---
name: microservices-orchestrator
description: Expert skill for designing, decomposing, and managing microservices architectures. Activates when users need help with microservices design, service decomposition, bounded contexts, API contracts, or transitioning from monolithic to microservices architectures.
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob]
---

# Microservices Orchestrator

Enterprise-grade skill for designing and managing microservices architectures at scale.

## When to Use

This skill should be used when:
- Designing a new microservices architecture from scratch
- Decomposing a monolithic application into microservices
- Defining service boundaries and bounded contexts
- Establishing inter-service communication patterns
- Designing API contracts and service interfaces
- Planning microservices deployment strategies
- Implementing service discovery and registration
- Designing data management across microservices

## Instructions

### Step 1: Analyze Current Architecture

First, understand the current system architecture and requirements:

1. **Identify the domain** - What business domain are we working with?
2. **Map current architecture** - Is this a greenfield project or migration?
3. **Gather requirements** - Scalability, performance, team structure
4. **Identify constraints** - Technology stack, compliance, existing integrations

Example analysis questions:
```markdown
## Architecture Analysis

### Business Domain
- What is the core business domain? (e.g., e-commerce, healthcare, fintech)
- What are the key business capabilities?
- Who are the main users and stakeholders?

### Current State
- Monolithic application or existing services?
- Current technology stack?
- Team size and structure?
- Deployment frequency and process?

### Requirements
- Expected traffic volume and growth?
- Performance requirements (latency, throughput)?
- Availability requirements (SLA)?
- Compliance requirements (HIPAA, PCI-DSS, GDPR)?

### Constraints
- Budget limitations?
- Timeline constraints?
- Technology preferences or mandates?
- Team skill levels?
```

### Step 2: Define Bounded Contexts

Apply Domain-Driven Design to identify service boundaries:

1. **Identify business capabilities** - What does the system do?
2. **Map bounded contexts** - Where do concepts have different meanings?
3. **Define context boundaries** - What data/logic belongs in each context?
4. **Identify relationships** - How do contexts interact?

Example bounded context mapping:
```typescript
/**
 * E-Commerce Platform - Bounded Contexts
 */

// 1. Product Catalog Context
interface ProductCatalogContext {
  responsibilities: [
    'Product information management',
    'Category management',
    'Search and discovery',
    'Product recommendations'
  ];
  entities: ['Product', 'Category', 'Brand', 'ProductVariant'];
  services: ['ProductService', 'CategoryService', 'SearchService'];
}

// 2. Order Management Context
interface OrderManagementContext {
  responsibilities: [
    'Order creation and tracking',
    'Order fulfillment',
    'Order history',
    'Returns and refunds'
  ];
  entities: ['Order', 'OrderItem', 'Return', 'Refund'];
  services: ['OrderService', 'FulfillmentService', 'ReturnService'];
}

// 3. Customer Context
interface CustomerContext {
  responsibilities: [
    'Customer profiles',
    'Authentication',
    'Preferences',
    'Customer support'
  ];
  entities: ['Customer', 'Account', 'Preference', 'SupportTicket'];
  services: ['CustomerService', 'AuthService', 'PreferenceService'];
}

// 4. Payment Context
interface PaymentContext {
  responsibilities: [
    'Payment processing',
    'Payment methods management',
    'Transaction history',
    'Refund processing'
  ];
  entities: ['Payment', 'PaymentMethod', 'Transaction'];
  services: ['PaymentService', 'RefundService'];
}

// 5. Inventory Context
interface InventoryContext {
  responsibilities: [
    'Stock management',
    'Warehouse operations',
    'Stock reservations',
    'Inventory forecasting'
  ];
  entities: ['InventoryItem', 'Warehouse', 'StockMovement'];
  services: ['InventoryService', 'WarehouseService'];
}
```

### Step 3: Design Service Interfaces

Define clear API contracts for each microservice:

1. **REST APIs** - Resource-based endpoints
2. **GraphQL APIs** - Flexible query interfaces
3. **Event interfaces** - Asynchronous communication
4. **gRPC** - High-performance RPC

Example API contract:
```typescript
/**
 * Order Service API Contract
 */

// REST API Endpoints
interface OrderServiceAPI {
  // Commands (mutations)
  'POST /orders': {
    request: CreateOrderRequest;
    response: OrderCreated;
    status: 201;
  };

  'PUT /orders/:id': {
    request: UpdateOrderRequest;
    response: OrderUpdated;
    status: 200;
  };

  'POST /orders/:id/cancel': {
    request: CancelOrderRequest;
    response: OrderCancelled;
    status: 200;
  };

  // Queries
  'GET /orders/:id': {
    response: OrderDetails;
    status: 200;
  };

  'GET /orders': {
    query: OrderSearchParams;
    response: OrderList;
    status: 200;
  };
}

// Event Interfaces (Async Communication)
interface OrderServiceEvents {
  // Events Published
  published: [
    'OrderCreated',
    'OrderUpdated',
    'OrderCancelled',
    'OrderFulfilled'
  ];

  // Events Consumed
  consumed: [
    'PaymentCompleted',
    'PaymentFailed',
    'InventoryReserved',
    'InventoryReservationFailed'
  ];
}

// Data Transfer Objects
interface CreateOrderRequest {
  customerId: string;
  items: Array<{
    productId: string;
    quantity: number;
    price: number;
  }>;
  shippingAddress: Address;
  paymentMethodId: string;
}

interface OrderCreated {
  orderId: string;
  customerId: string;
  items: OrderItem[];
  totalAmount: number;
  status: 'pending' | 'confirmed';
  createdAt: string;
}
```

### Step 4: Design Data Management Strategy

Determine data ownership and consistency patterns:

1. **Database per service** - Each service owns its data
2. **Shared database** - Multiple services share a database (anti-pattern)
3. **Saga pattern** - Distributed transactions
4. **Event sourcing** - Event-driven data persistence
5. **CQRS** - Command Query Responsibility Segregation

Example data management pattern:
```typescript
/**
 * Saga Pattern for Order Creation
 * Ensures data consistency across Order, Payment, and Inventory services
 */

class OrderCreationSaga {
  async execute(createOrderRequest: CreateOrderRequest) {
    let orderId: string;
    let reservationId: string;
    let paymentId: string;

    try {
      // Step 1: Create order (pending state)
      orderId = await this.orderService.createOrder({
        ...createOrderRequest,
        status: 'pending'
      });

      // Step 2: Reserve inventory
      reservationId = await this.inventoryService.reserveItems({
        orderId,
        items: createOrderRequest.items
      });

      // Step 3: Process payment
      paymentId = await this.paymentService.processPayment({
        orderId,
        amount: this.calculateTotal(createOrderRequest.items),
        paymentMethodId: createOrderRequest.paymentMethodId
      });

      // Step 4: Confirm order
      await this.orderService.confirmOrder(orderId);

      return { orderId, status: 'confirmed' };

    } catch (error) {
      // Compensating transactions (rollback)
      await this.compensate({
        orderId,
        reservationId,
        paymentId
      });

      throw new OrderCreationFailedError(error);
    }
  }

  private async compensate(context: any) {
    // Release inventory reservation
    if (context.reservationId) {
      await this.inventoryService.releaseReservation(context.reservationId);
    }

    // Refund payment
    if (context.paymentId) {
      await this.paymentService.refundPayment(context.paymentId);
    }

    // Cancel order
    if (context.orderId) {
      await this.orderService.cancelOrder(context.orderId);
    }
  }
}
```

### Step 5: Design Communication Patterns

Choose appropriate communication patterns:

1. **Synchronous** - REST, gRPC for request/response
2. **Asynchronous** - Message queues for events
3. **Hybrid** - Mix of both based on use case

Example communication design:
```typescript
/**
 * Communication Patterns
 */

// Synchronous - REST for direct queries
class ProductService {
  @Get('/products/:id')
  async getProduct(id: string): Promise<Product> {
    // Direct synchronous call - fast response needed
    return await this.productRepository.findById(id);
  }
}

// Asynchronous - Events for loosely coupled operations
class OrderService {
  async createOrder(request: CreateOrderRequest): Promise<Order> {
    // Create order
    const order = await this.orderRepository.create(request);

    // Publish event (asynchronous - don't wait for subscribers)
    await this.eventBus.publish(new OrderCreatedEvent({
      orderId: order.id,
      customerId: order.customerId,
      items: order.items,
      totalAmount: order.totalAmount
    }));

    return order;
  }
}

// Event handlers in other services
class InventoryService {
  @EventHandler(OrderCreatedEvent)
  async onOrderCreated(event: OrderCreatedEvent) {
    // Reserve inventory asynchronously
    await this.reserveInventory(event.items);
  }
}

class NotificationService {
  @EventHandler(OrderCreatedEvent)
  async onOrderCreated(event: OrderCreatedEvent) {
    // Send order confirmation email asynchronously
    await this.emailService.sendOrderConfirmation(event);
  }
}
```

### Step 6: Design Deployment and Infrastructure

Plan deployment architecture:

1. **Service discovery** - How services find each other
2. **API Gateway** - Single entry point for clients
3. **Load balancing** - Traffic distribution
4. **Service mesh** - Advanced traffic management, security
5. **Observability** - Monitoring, tracing, logging

Example infrastructure design:
```yaml
# Kubernetes Deployment Architecture

# API Gateway
apiVersion: v1
kind: Service
metadata:
  name: api-gateway
spec:
  type: LoadBalancer
  selector:
    app: kong-gateway
  ports:
    - port: 80
      targetPort: 8000
    - port: 443
      targetPort: 8443

---
# Order Service
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
        version: v1
    spec:
      containers:
      - name: order-service
        image: myregistry/order-service:v1.0
        ports:
        - containerPort: 8080
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: order-db-secret
              key: url
        - name: KAFKA_BROKERS
          value: "kafka-cluster:9092"
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 10
          periodSeconds: 5

---
# Service Mesh (Istio)
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: order-service
spec:
  hosts:
  - order-service
  http:
  - match:
    - headers:
        version:
          exact: canary
    route:
    - destination:
        host: order-service
        subset: v2
      weight: 10
    - destination:
        host: order-service
        subset: v1
      weight: 90
  - route:
    - destination:
        host: order-service
        subset: v1
```

## Best Practices

### Domain-Driven Design:
- ✅ Start with business capabilities, not technical components
- ✅ Use ubiquitous language within bounded contexts
- ✅ Keep services loosely coupled, highly cohesive
- ✅ Each service should own its data

### API Design:
- ✅ Design APIs that are backward compatible
- ✅ Use API versioning (URL, header, or content negotiation)
- ✅ Document APIs with OpenAPI/Swagger
- ✅ Implement proper error handling and status codes

### Data Management:
- ✅ Database per service pattern
- ✅ Use sagas for distributed transactions
- ✅ Implement eventual consistency where appropriate
- ✅ Consider event sourcing for audit trails

### Communication:
- ✅ Use synchronous for real-time queries
- ✅ Use asynchronous for long-running operations
- ✅ Implement circuit breakers and retries
- ✅ Use message queues for reliability

### Deployment:
- ✅ Implement service discovery
- ✅ Use API gateway for external access
- ✅ Deploy services independently
- ✅ Use container orchestration (Kubernetes)
- ✅ Implement service mesh for advanced patterns

### Observability:
- ✅ Distributed tracing (Jaeger, Zipkin)
- ✅ Centralized logging (ELK, Loki)
- ✅ Metrics and monitoring (Prometheus, Grafana)
- ✅ Health checks and readiness probes

## Common Mistakes to Avoid

- ❌ **Distributed monolith** - Services too tightly coupled
- ❌ **Shared database** - Multiple services sharing same database
- ❌ **Chatty services** - Too many inter-service calls
- ❌ **No API versioning** - Breaking changes affect all clients
- ❌ **Ignoring network failures** - No circuit breakers or retries
- ❌ **No monitoring** - Can't debug distributed systems
- ❌ **Premature microservices** - Starting with microservices before understanding domain
- ❌ **God service** - One service doing too much

✅ **Correct approach:**
- Start with a well-defined bounded context
- Each service has single responsibility
- Use API gateway for external clients
- Implement comprehensive observability
- Design for failure (circuit breakers, retries, timeouts)
- Version APIs from the start

## Examples

### Example 1: E-Commerce Platform Migration

**Scenario:** Migrate monolithic e-commerce platform to microservices

**Steps:**

1. **Identify Bounded Contexts:**
```markdown
- Product Catalog (product management, search)
- Order Management (orders, fulfillment)
- Customer Management (profiles, authentication)
- Payment Processing (payments, refunds)
- Inventory Management (stock, warehouses)
- Notification (emails, SMS)
```

2. **Service Decomposition Strategy:**
```
Phase 1: Extract read-heavy services
- Product Catalog (high read, low write)
- Customer Profiles (read-heavy)

Phase 2: Extract transactional services
- Order Management (ACID transactions needed)
- Payment Processing (critical path)

Phase 3: Extract supporting services
- Inventory Management
- Notification Service
```

3. **Communication Pattern:**
```typescript
// Order → Payment: Synchronous (need immediate response)
const payment = await paymentService.processPayment({
  orderId,
  amount,
  paymentMethod
});

// Order → Notification: Asynchronous (fire and forget)
await eventBus.publish(new OrderCreatedEvent(order));
```

### Example 2: Healthcare Platform (HIPAA Compliant)

**Scenario:** Design microservices for electronic health records

**Bounded Contexts:**
```typescript
// 1. Patient Management Service
interface PatientService {
  responsibilities: [
    'Patient demographics (PHI)',
    'Patient registration',
    'Consent management'
  ];
  compliance: ['HIPAA', 'Audit logging', 'Encryption at rest'];
}

// 2. Clinical Data Service
interface ClinicalDataService {
  responsibilities: [
    'Medical records',
    'Lab results',
    'Prescriptions'
  ];
  compliance: ['HIPAA', 'Access controls', 'Data retention'];
}

// 3. Appointment Service
interface AppointmentService {
  responsibilities: [
    'Appointment scheduling',
    'Provider availability',
    'Reminders'
  ];
}

// 4. Billing Service
interface BillingService {
  responsibilities: [
    'Claims processing',
    'Insurance verification',
    'Payment processing'
  ];
  compliance: ['PCI-DSS for payments', 'HIPAA for claims'];
}
```

**Security Architecture:**
```typescript
// Zero-trust security model
class ServiceAuthMiddleware {
  async authenticate(request: Request) {
    // 1. Verify JWT token
    const token = this.extractToken(request);
    const claims = await this.jwtService.verify(token);

    // 2. Verify service identity (mTLS)
    const clientCert = request.socket.getPeerCertificate();
    await this.verifyCertificate(clientCert);

    // 3. Check access control (RBAC)
    const hasAccess = await this.rbacService.checkPermission(
      claims.userId,
      request.path,
      request.method
    );

    if (!hasAccess) {
      throw new ForbiddenError('Access denied');
    }

    // 4. Audit log
    await this.auditService.log({
      userId: claims.userId,
      action: `${request.method} ${request.path}`,
      timestamp: new Date(),
      ipAddress: request.ip
    });

    return claims;
  }
}
```

## Tips

- 💡 **Start small** - Don't decompose everything at once
- 💡 **Strangler fig pattern** - Gradually replace monolith
- 💡 **Use API gateway** - Single entry point simplifies client integration
- 💡 **Event-driven** - Reduces coupling between services
- 💡 **Automate deployment** - CI/CD is essential for microservices
- 💡 **Monitor everything** - Distributed tracing is crucial
- 💡 **Document APIs** - OpenAPI/Swagger from day one
- 💡 **Versioning strategy** - Plan for API evolution

## Related Skills/Commands

### Skills:
- `service-mesh-integrator` - Configure Istio/Linkerd
- `api-gateway-configurator` - Set up Kong/Tyk
- `event-driven-architect` - Design event-driven systems
- `distributed-tracing-setup` - Configure Jaeger/Zipkin

### Commands:
- `/dependency-graph` - Visualize service dependencies
- `/adr-create` - Document architecture decisions
- `/load-test-suite` - Test microservices performance

### Agents:
- `enterprise-architect` - High-level system design
- `distributed-systems-architect` - Deep microservices expertise
- `sre-consultant` - Reliability and monitoring

## Notes

**When to Use Microservices:**
- ✅ Large teams (10+ developers)
- ✅ Need to scale independently
- ✅ Different technology stacks needed
- ✅ Frequent deployments
- ✅ Complex business domain

**When NOT to Use Microservices:**
- ❌ Small team (< 5 developers)
- ❌ Simple domain
- ❌ Tight coupling between features
- ❌ Low traffic volume
- ❌ Startup/MVP phase

**Migration Strategy:**
- Start with 2-3 services (not 20)
- Extract read-heavy services first
- Establish observability before scaling
- Automate deployment and testing
- Keep monolith until confident

**Success Metrics:**
- Deployment frequency increased
- Mean time to recovery (MTTR) decreased
- Team autonomy increased
- Service availability (99.9%+)
- Independent scalability achieved
