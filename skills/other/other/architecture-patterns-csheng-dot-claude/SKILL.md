---
name: architecture-patterns
description: Architectural pattern guidance and layering principles. Use when architecture patterns guidance is required.
---
# Core Architecture Patterns

## Layered Architecture Pattern

### Three-Tier Structure Implementation

Apply layered architecture with strict separation of concerns:

1. Presentation Layer: User interface components
2. Business Logic Layer: Domain rules and operations
3. Data Access Layer: Database and external service interactions

Enforce unidirectional dependencies:
- Presentation Layer → Business Logic Layer
- Business Logic Layer → Data Access Layer
- Never allow reverse dependencies

### Domain Boundaries Enforcement

Separate domain logic from infrastructure:
- Keep business rules independent of frameworks
- Use dependency injection for infrastructure concerns
- Apply Domain-Driven Design principles
- Define clear bounded contexts for complex domains

Interface segregation requirements:
- Create specific interfaces for different client needs
- Avoid fat interfaces with multiple responsibilities
- Use repository pattern for data access abstraction
- Implement service interfaces for business operations

## Microservices Pattern Guidelines

### Service Decomposition Rules

Apply single responsibility principle at service level:
- Each service owns one business capability
- Design services around business domains
- Ensure loose coupling between services
- Implement high cohesion within services

Communication patterns enforcement:
- Prefer synchronous communication for critical operations
- Use asynchronous messaging for event-driven workflows
- Implement circuit breakers for resilience
- Apply API gateway pattern for external access

### Data Consistency Patterns

Implement eventual consistency where appropriate:
- Use saga pattern for distributed transactions
- Apply event sourcing for audit trails
- Implement CQRS for read/write separation
- Ensure data ownership boundaries are clear

## Event-Driven Architecture Implementation

### Event Design Principles

Design immutable, atomic events:
- Each event represents a single business fact
- Use past tense for event names (UserRegistered, OrderPlaced)
- Include all required data in the event payload
- Apply idempotency handling for duplicate events

Event handling patterns:
- Implement event handlers as pure functions
- Use correlation IDs for request tracing
- Apply dead letter queues for failed events
- Monitor and log event processing metrics

### Message Broker Integration

Configure reliable messaging infrastructure:
- Set up topic/exchange hierarchies
- Implement message versioning strategies
- Configure appropriate quality of service levels
- Apply backpressure handling for overload protection

# Enterprise Integration Patterns

## API Design Standards

### RESTful API Implementation

Follow REST architectural constraints:
- Use appropriate HTTP methods (GET, POST, PUT, DELETE)
- Implement proper status codes for all responses
- Apply resource-based URL naming conventions
- Use content negotiation for format handling

API documentation requirements:
- Generate OpenAPI/Swagger specifications
- Include comprehensive request/response examples
- Document error codes and handling procedures
- Provide authentication and authorization details

### GraphQL Integration Patterns

Schema-first development approach:
- Define clear type system with strong typing
- Implement proper resolver chains
- Apply authorization at field level
- Use data loaders to prevent N+1 queries

Performance optimization techniques:
- Implement query complexity analysis
- Apply query depth limiting
- Use persisted queries for frequently used operations
- Monitor and log query performance metrics

## Security Architecture Patterns

### Zero Trust Security Model

Implement defense-in-depth security:
- Apply least privilege access control
- Use mTLS for service-to-service communication
- Implement JWT/OIDC for authentication
- Apply API throttling and rate limiting

Security monitoring and auditing:
- Log all security-relevant events
- Implement intrusion detection systems
- Apply security information and event management (SIEM)
- Conduct regular security assessments

### Secure API Gateway Configuration

Apply API gateway security patterns:
- Implement request/response transformation
- Apply JSON Web Token validation
- Use web application firewall (WAF) rules
- Implement distributed tracing for security monitoring

# Architecture Quality Attributes

## Scalability Patterns

### Horizontal Scaling Implementation

Design for stateless services:
- Externalize session state using distributed caches
- Use database connection pooling efficiently
- Implement auto-scaling policies based on metrics
- Apply blue-green deployment strategies

Performance optimization techniques:
- Implement caching at multiple levels (CDN, application, database)
- Use read replicas for database scaling
- Apply asynchronous processing for non-critical operations
- Implement sharding strategies for large datasets

### Resilience and Fault Tolerance

Implement self-healing mechanisms:
- Use health checks for service monitoring
- Apply exponential backoff for retry logic
- Implement circuit breakers to prevent cascading failures
- Use chaos engineering for resilience testing

Disaster recovery planning:
- Implement multi-region deployment strategies
- Use backup and restore procedures
- Apply data replication across geographic locations
- Document and test recovery procedures

## Maintainability and Evolution

### Technical Debt Management

Apply architectural fitness functions:
- Define measurable quality metrics
- Implement automated architecture compliance checks
- Use architectural decision records (ADRs)
- Regularly review and refactor architectural decisions

Evolutionary architecture principles:
- Design for change with loose coupling
- Use abstraction layers to isolate volatility
- Implement feature flags for safe deployments
- Apply strangler fig pattern for legacy system migration

### Documentation and Communication

Maintain architectural documentation:
- Create context diagrams for system overviews
- Document data flows and integration points
- Maintain architectural decision records
- Provide deployment and runbooks

Cross-functional collaboration:
- Conduct regular architecture reviews
- Use pair programming for critical components
- Implement knowledge sharing practices
- Provide training on architectural standards
