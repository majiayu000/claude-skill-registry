---
name: architecture-review
description: Systematic evaluation of software architecture across scalability, maintainability, security, performance, reliability, and cost dimensions. Use when designing systems, reviewing technical approaches, evaluating patterns, making architectural decisions, or assessing technical debt.
---

# Architecture Review Skill

## Core Principle

**Architecture serves the future. Review for change, not just current needs.**

Software architecture is about making decisions that enable the system to evolve over time while meeting functional and non-functional requirements. A good architecture review doesn't just validate today's implementation—it evaluates how well the system will adapt to tomorrow's needs, scale with growth, and remain maintainable as requirements change.

**Effective architecture reviews are:**
- Multi-dimensional (technical, business, and team considerations)
- Trade-off aware (no perfect solutions, only informed choices)
- Context-driven (right architecture depends on constraints)
- Future-focused (optimizing for change and evolution)

---

## When to Use

Use this skill when:
- Designing new systems or major features
- Evaluating technical approaches before implementation
- Conducting design reviews or architecture board meetings
- Assessing technical debt and planning refactoring
- Making technology or pattern selection decisions
- Reviewing third-party integrations or vendor solutions
- Preparing for significant scaling events
- Investigating production issues with architectural root causes
- Onboarding to understand an existing system's design

---

## Architecture Review Dimensions

**Evaluate architecture across six critical dimensions:**

### 1. Scalability

**Definition:** The system's ability to handle increased load by adding resources.

**Key Questions:**
- Can the system scale horizontally (add more instances)?
- Can it scale vertically (increase instance size)?
- What are the bottlenecks at 10x, 100x, 1000x current load?
- How does the system handle traffic spikes?
- Are there single points of failure preventing scaling?

**Scalability Patterns:**

**Horizontal Scaling (Scale Out):**
- Stateless services that can be replicated
- Load balancing across multiple instances
- Database read replicas for read-heavy workloads
- Partitioning/sharding for write-heavy workloads

**Vertical Scaling (Scale Up):**
- Increasing CPU, memory, or storage on existing instances
- Simpler but has physical limits
- Often used for databases or memory-intensive workloads

**Auto-Scaling:**
- Dynamic resource allocation based on metrics
- CPU, memory, request rate, or custom metrics
- Scale-in policies to reduce costs during low traffic

**Review Checklist:**
- [ ] Services are stateless or state is externalized
- [ ] Database can scale (read replicas, sharding strategy)
- [ ] Caching layer for frequently accessed data
- [ ] Asynchronous processing for long-running tasks
- [ ] Rate limiting to protect against overload
- [ ] Connection pooling for database and external services
- [ ] No hardcoded capacity limits
- [ ] Performance testing validates scaling assumptions

**Red Flags:**
- Shared mutable state across instances
- Synchronous processing of batch operations
- Unbounded queues or buffers
- Hardcoded instance counts or capacity
- No caching strategy for expensive operations

### 2. Maintainability

**Definition:** The ease with which the system can be understood, modified, tested, and extended.

**Key Questions:**
- Can new developers understand the system quickly?
- How long does it take to implement common changes?
- Are components loosely coupled and highly cohesive?
- Is the code testable at all levels?
- Are there clear boundaries and interfaces?

**Maintainability Principles:**

**Low Coupling:**
- Components depend on abstractions, not concrete implementations
- Changes in one component don't cascade to others
- Clear, minimal interfaces between components

**High Cohesion:**
- Related functionality grouped together
- Single Responsibility Principle at all levels
- Clear purpose for each component

**Testability:**
- Unit tests for business logic
- Integration tests for component interactions
- Contract tests for external interfaces
- Dependency injection for test isolation

**Review Checklist:**
- [ ] Clear separation of concerns (presentation, business logic, data)
- [ ] Consistent naming conventions and code style
- [ ] Comprehensive documentation (architecture docs, ADRs, code comments)
- [ ] Modular design with well-defined boundaries
- [ ] Dependency injection or similar for loose coupling
- [ ] Automated tests with good coverage
- [ ] No circular dependencies between components
- [ ] Logging and debugging instrumentation

**Red Flags:**
- God objects or classes with too many responsibilities
- Tight coupling between layers or modules
- Inconsistent patterns across the codebase
- Lack of documentation or outdated docs
- Difficult to set up local development environment
- Tests require significant mocking or setup
- Business logic mixed with infrastructure concerns

### 3. Security

**Definition:** Protection against unauthorized access, data breaches, and malicious attacks.

**Key Questions:**
- How is authentication and authorization handled?
- Are secrets and credentials properly managed?
- Is data encrypted at rest and in transit?
- How are inputs validated and sanitized?
- What is the threat model and attack surface?

**Security Layers:**

**Authentication (Who are you?):**
- JWT tokens, OAuth 2.0, SAML, API keys
- Multi-factor authentication for sensitive operations
- Session management and timeout policies

**Authorization (What can you do?):**
- Role-Based Access Control (RBAC)
- Attribute-Based Access Control (ABAC)
- Principle of least privilege
- Resource-level permissions

**Data Protection:**
- Encryption at rest (database, file storage)
- Encryption in transit (TLS/HTTPS)
- Key management (KMS, HSM, key rotation)
- Data masking for sensitive information

**Input Validation:**
- Whitelist validation of inputs
- Parameterized queries to prevent SQL injection
- Output encoding to prevent XSS
- Rate limiting to prevent abuse

**Review Checklist:**
- [ ] All endpoints require authentication where appropriate
- [ ] Authorization checked at service boundaries
- [ ] Secrets stored in vault/secrets manager, not code
- [ ] TLS for all external communication
- [ ] Database connections encrypted
- [ ] Input validation on all user-provided data
- [ ] SQL injection protection (parameterized queries)
- [ ] XSS protection (output encoding)
- [ ] CSRF protection for state-changing operations
- [ ] Dependency scanning for known vulnerabilities
- [ ] Security headers configured (CSP, HSTS, etc.)
- [ ] Audit logging for sensitive operations
- [ ] Regular security reviews and penetration testing

**Red Flags:**
- Secrets in code, configuration files, or version control
- Unauthenticated access to sensitive data
- Insufficient authorization checks
- Plain text storage of passwords or sensitive data
- Direct SQL query construction from user input
- Missing input validation
- Overly permissive access controls

### 4. Performance

**Definition:** The system's responsiveness, throughput, and resource efficiency under various load conditions.

**Key Questions:**
- What are the latency requirements for critical paths?
- What is the expected throughput (requests/sec)?
- How efficient is resource utilization (CPU, memory, I/O)?
- Are there expensive operations that could be optimized?
- How does performance degrade under load?

**Performance Patterns:**

**Caching:**
- In-memory caching (Redis, Memcached)
- HTTP caching (CDN, browser cache)
- Query result caching
- Cache invalidation strategy

**Database Optimization:**
- Proper indexing for frequent queries
- Query optimization (avoid N+1, use projections)
- Connection pooling
- Read replicas for read-heavy workloads

**Asynchronous Processing:**
- Message queues for background jobs
- Event-driven architecture
- Non-blocking I/O
- Batch processing for bulk operations

**Resource Optimization:**
- Lazy loading and pagination
- Compression for data transfer
- Efficient data structures and algorithms
- Resource pooling (connections, threads)

**Review Checklist:**
- [ ] Performance requirements defined (latency, throughput)
- [ ] Database queries optimized with proper indexes
- [ ] Caching strategy for expensive operations
- [ ] Asynchronous processing for long-running tasks
- [ ] Pagination for large data sets
- [ ] Connection pooling for databases and external services
- [ ] Static assets served via CDN
- [ ] Compression enabled for API responses
- [ ] No synchronous calls in critical paths
- [ ] Performance testing under realistic load
- [ ] Profiling data to identify bottlenecks
- [ ] Resource limits configured to prevent runaway processes

**Red Flags:**
- N+1 query problems
- Missing database indexes on query columns
- Synchronous processing of batch operations
- No caching strategy
- Large data transfers without pagination
- Expensive operations in tight loops
- Memory leaks or unbounded growth
- No performance testing or benchmarks

### 5. Reliability

**Definition:** The system's ability to function correctly under expected and unexpected conditions, including failure scenarios.

**Key Questions:**
- What happens when a component fails?
- Are there single points of failure?
- How quickly can the system recover from failures?
- Is data loss possible, and what are the recovery mechanisms?
- How are errors detected and handled?

**Reliability Patterns:**

**Fault Tolerance:**
- Circuit breakers for external dependencies
- Retry logic with exponential backoff
- Timeouts for all external calls
- Graceful degradation when dependencies fail

**High Availability:**
- Redundancy (multiple instances, multi-region)
- Health checks and automatic failover
- Load balancing across availability zones
- Database replication and automatic failover

**Data Durability:**
- Regular backups with tested restore procedures
- Point-in-time recovery capability
- Data validation and integrity checks
- Transaction management (ACID properties)

**Observability:**
- Comprehensive logging (errors, warnings, audit trail)
- Metrics and monitoring (uptime, latency, error rates)
- Distributed tracing for request flows
- Alerting on critical issues

**Review Checklist:**
- [ ] Circuit breakers for external service calls
- [ ] Retry logic with exponential backoff
- [ ] Timeouts configured for all operations
- [ ] Health check endpoints implemented
- [ ] Graceful shutdown and startup
- [ ] Database transactions for data consistency
- [ ] Regular backups with tested restore procedures
- [ ] Error handling for all failure scenarios
- [ ] Dead letter queues for failed messages
- [ ] Comprehensive logging with correlation IDs
- [ ] Monitoring and alerting configured
- [ ] Runbooks for common failure scenarios
- [ ] Chaos engineering or fault injection testing

**Red Flags:**
- No error handling for external service failures
- Missing timeouts on network calls
- Single points of failure (single database, single region)
- No health checks or monitoring
- Cascading failures possible
- No backup or disaster recovery plan
- Silent failures without logging or alerts
- Undefined behavior under partial failures

### 6. Cost Efficiency

**Definition:** The balance between system capabilities and operational expenses, optimizing for business value.

**Key Questions:**
- What are the infrastructure costs at current and projected scale?
- Are resources over-provisioned or under-utilized?
- Can costs be reduced without sacrificing requirements?
- What are the trade-offs between cost and other dimensions?
- How do architectural choices impact long-term costs?

**Cost Optimization Patterns:**

**Resource Right-Sizing:**
- Match instance types to workload requirements
- Auto-scaling to reduce waste during low traffic
- Spot/preemptible instances for non-critical workloads
- Reserved instances or savings plans for predictable usage

**Efficient Data Storage:**
- Object storage (S3) for archival data
- Data lifecycle policies (hot → warm → cold)
- Compression for large datasets
- Deduplicate redundant data

**Serverless and Pay-Per-Use:**
- Lambda/Functions for sporadic workloads
- API Gateway for API management
- Managed services to reduce operational overhead
- Pay only for actual usage, not idle capacity

**Caching and CDN:**
- Reduce database load with caching
- Reduce origin requests with CDN
- Lower data transfer costs

**Review Checklist:**
- [ ] Cost monitoring and budgets configured
- [ ] Resource tagging for cost allocation
- [ ] Auto-scaling policies to match demand
- [ ] Database instance sizes appropriate for load
- [ ] Unused resources identified and decommissioned
- [ ] Data retention policies to limit storage growth
- [ ] CDN for static assets to reduce egress costs
- [ ] Caching to reduce compute and database costs
- [ ] Reserved capacity for predictable workloads
- [ ] Cost impact documented in architecture decisions
- [ ] Regular cost reviews and optimization

**Red Flags:**
- Over-provisioned resources running 24/7
- No auto-scaling leading to idle capacity
- High data transfer costs without CDN
- Expensive database for simple use cases
- No cost monitoring or alerting
- Undefined data retention leading to unbounded storage growth
- Synchronous processing when async would be cheaper

---

## Architecture Patterns

**Common architecture patterns and when to use them:**

### Monolithic Architecture

**Description:** Single, unified application where all components run in the same process.

**When to Use:**
- Small to medium applications
- Early-stage products (MVP, prototyping)
- Team size < 10 developers
- Simple deployment requirements
- Low operational complexity tolerance

**Advantages:**
- Simpler development and testing
- Easier debugging (single process)
- Lower operational overhead
- Better performance (no network calls)
- Atomic transactions across components

**Disadvantages:**
- Difficult to scale specific components independently
- Longer build and deployment times
- Tight coupling between components
- Limited technology flexibility
- Scaling requires scaling entire application

**Review Considerations:**
- Is the codebase well-modularized internally?
- Are there clear boundaries between domains?
- Could components be extracted later if needed?
- Is the deployment pipeline efficient?

### Microservices Architecture

**Description:** Application composed of small, independent services communicating over network.

**When to Use:**
- Large, complex applications
- Multiple teams working independently
- Need to scale components independently
- Different technology stacks per service
- High availability requirements

**Advantages:**
- Independent deployment and scaling
- Technology flexibility per service
- Team autonomy and ownership
- Fault isolation (service failures don't cascade)
- Easier to understand individual services

**Disadvantages:**
- Increased operational complexity
- Network latency between services
- Distributed system challenges (consistency, tracing)
- More complex testing and debugging
- Data consistency across services

**Review Considerations:**
- Are service boundaries well-defined (bounded contexts)?
- How is inter-service communication handled (REST, gRPC, events)?
- What is the deployment and orchestration strategy?
- How are distributed transactions managed?
- Is there a service mesh or API gateway?
- How is observability implemented (tracing, logging)?

### Event-Driven Architecture

**Description:** Components communicate through asynchronous event messages, decoupling producers from consumers.

**When to Use:**
- Need for real-time data processing
- Complex workflows across multiple systems
- High decoupling required
- Asynchronous processing beneficial
- Event sourcing or audit trail requirements

**Advantages:**
- Loose coupling between components
- Scalable (process events independently)
- Resilient (events persist if consumer fails)
- Real-time processing capabilities
- Easy to add new event consumers

**Disadvantages:**
- Eventual consistency (not immediate)
- Complex debugging (events flow through system)
- Message ordering challenges
- Requires robust event infrastructure
- More difficult to reason about system state

**Review Considerations:**
- What event broker is used (Kafka, RabbitMQ, AWS SQS/SNS)?
- How are event schemas defined and versioned?
- What is the event retention policy?
- How is event ordering handled?
- Are there dead letter queues for failed events?
- How is eventual consistency managed?

### CQRS (Command Query Responsibility Segregation)

**Description:** Separate models for reading data (queries) and writing data (commands).

**When to Use:**
- Different read and write scalability requirements
- Complex domain logic for writes, simple reads
- Need for multiple read models (different views)
- Event sourcing implementation
- Performance optimization for read-heavy workloads

**Advantages:**
- Optimize read and write models independently
- Scale reads and writes separately
- Simpler query models for specific use cases
- Better performance for complex domains
- Enables event sourcing

**Disadvantages:**
- Increased complexity (two models)
- Eventual consistency between models
- More code to maintain
- Requires synchronization mechanism
- Steep learning curve

**Review Considerations:**
- Is the complexity justified by requirements?
- How is the read model synchronized from write model?
- What is the consistency model (eventual vs strong)?
- Are projections defined for different read use cases?
- How are read model failures handled?

### Layered (N-Tier) Architecture

**Description:** Application organized into layers with specific responsibilities (presentation, business logic, data access).

**When to Use:**
- Traditional enterprise applications
- Clear separation of concerns needed
- Team specialization by layer
- Standard CRUD operations
- Medium complexity applications

**Advantages:**
- Clear separation of concerns
- Easy to understand and test
- Modular design
- Reusable layers
- Enforces dependencies flow in one direction

**Disadvantages:**
- Can lead to unnecessary abstraction
- Performance overhead from layer traversal
- Changes often span multiple layers
- Risk of anemic domain model

**Review Considerations:**
- Are layer boundaries well-defined?
- Is there proper dependency management (no circular refs)?
- Does business logic reside in the correct layer?
- Are layers testable in isolation?

### API Gateway Pattern

**Description:** Single entry point for client requests, routing to appropriate backend services.

**When to Use:**
- Microservices architecture
- Multiple client types (web, mobile, IoT)
- Cross-cutting concerns (auth, rate limiting, logging)
- Need to aggregate multiple service calls
- API versioning and backward compatibility

**Advantages:**
- Single entry point for clients
- Centralized cross-cutting concerns
- Request aggregation (reduce client roundtrips)
- Protocol translation (REST to gRPC)
- API versioning and routing

**Disadvantages:**
- Single point of failure (need high availability)
- Can become a bottleneck
- Additional network hop
- Requires careful design to avoid coupling

**Review Considerations:**
- What gateway technology is used (AWS API Gateway, Kong, etc.)?
- How is high availability ensured?
- What cross-cutting concerns are handled?
- Is there request/response transformation?
- How is versioning managed?
- Are there rate limits and quotas?

---

## Architecture Review Process

**Step-by-step approach to conducting an architecture review:**

### Step 1: Understand Context and Requirements

**Gather Information:**
- Business requirements and goals
- Functional requirements (what the system does)
- Non-functional requirements (scalability, performance, security)
- Constraints (budget, timeline, team skills, regulatory)
- Existing systems and integration points

**Key Questions:**
- What problem is this system solving?
- Who are the users and what are their needs?
- What are the success metrics?
- What are the hard constraints?
- What can be changed later vs must be right now?

### Step 2: Document Current Architecture

**Create Architecture Diagrams:**
- System context diagram (external systems, users)
- Container diagram (applications, databases, services)
- Component diagram (major modules and their interactions)
- Deployment diagram (infrastructure, networking)

**Document Key Decisions:**
- Technology choices (languages, frameworks, databases)
- Architecture patterns used
- Integration patterns
- Data flow and storage strategy

### Step 3: Evaluate Against Review Dimensions

**For each dimension (scalability, maintainability, security, performance, reliability, cost):**
1. Review current implementation
2. Identify strengths
3. Identify weaknesses and risks
4. Assess alignment with requirements
5. Document findings with severity (critical, major, minor)

**Use the checklists provided in each dimension section above.**

### Step 4: Identify Trade-offs

**Every architectural decision involves trade-offs:**

**Example Trade-offs:**
- **Consistency vs Availability:** Strong consistency reduces availability (CAP theorem)
- **Performance vs Cost:** Caching improves performance but increases infrastructure costs
- **Flexibility vs Simplicity:** Microservices offer flexibility but add operational complexity
- **Security vs Usability:** Stricter security can impact user experience
- **Time to Market vs Technical Debt:** Quick implementation may incur debt

**Document:**
- Trade-offs made in current design
- Whether trade-offs align with priorities
- Alternative approaches and their trade-offs

### Step 5: Assess Technical Debt

**Identify Technical Debt:**
- Quick fixes or workarounds
- Outdated dependencies or technology
- Missing tests or documentation
- Known performance issues
- Security vulnerabilities
- Scalability bottlenecks

**Prioritize Debt:**
- **Critical:** Blocks future work or significant risk
- **High:** Slows development or moderate risk
- **Medium:** Manageable but should be addressed
- **Low:** Nice to fix but not urgent

### Step 6: Document Findings and Recommendations

**Structure:**
```markdown
# Architecture Review: [System Name]

## Executive Summary
- Overall assessment (Green/Yellow/Red)
- Key findings
- Critical recommendations

## Review Context
- System purpose
- Scope of review
- Reviewers and date

## Findings by Dimension
### Scalability
- Strengths: [...]
- Concerns: [...]
- Recommendations: [...]

### Maintainability
[...]

### Security
[...]

### Performance
[...]

### Reliability
[...]

### Cost
[...]

## Architecture Patterns Evaluation
- Current patterns used
- Alignment with requirements
- Alternative patterns considered

## Technical Debt Assessment
- High priority items
- Medium priority items
- Long-term improvements

## Risk Assessment
- Critical risks
- Mitigation strategies

## Recommendations Summary
1. [Priority 1 recommendation]
2. [Priority 2 recommendation]
...

## Action Items
- [ ] Owner: Task description (Due date)
```

### Step 7: Follow Up and Track Progress

**After the review:**
- Share findings with stakeholders
- Create tasks for recommendations
- Schedule follow-up review if needed
- Document decisions in ADRs (Architecture Decision Records)
- Update architecture documentation

---

## Common Anti-Patterns

**Architecture smells to watch for:**

### The Big Ball of Mud
**Symptom:** No discernible architecture, everything tightly coupled, spaghetti code.
**Impact:** Difficult to maintain, test, or extend. High risk of breaking changes.
**Remedy:** Identify bounded contexts, refactor into modules with clear interfaces.

### Premature Optimization
**Symptom:** Complex performance optimizations before understanding actual bottlenecks.
**Impact:** Increased complexity without proven benefit. Wastes development time.
**Remedy:** Measure first, optimize second. Focus on architectural scalability.

### Analysis Paralysis
**Symptom:** Over-engineering for hypothetical future requirements.
**Impact:** Delayed delivery, unnecessary complexity, wasted effort.
**Remedy:** Build for current requirements plus one level of known future growth. Use evolutionary architecture.

### Resume-Driven Development
**Symptom:** Technology choices based on trends rather than requirements.
**Impact:** Poor fit for problem, team unfamiliarity, unnecessary complexity.
**Remedy:** Choose technology based on requirements, team skills, and ecosystem maturity.

### Distributed Monolith
**Symptom:** Microservices that are tightly coupled and must be deployed together.
**Impact:** Complexity of microservices without the benefits. Worst of both worlds.
**Remedy:** Define proper service boundaries (bounded contexts), ensure independent deployability.

### God Service/Module
**Symptom:** Single service or module with too many responsibilities.
**Impact:** Difficult to understand, test, maintain. Becomes a bottleneck.
**Remedy:** Apply Single Responsibility Principle, split into cohesive components.

### Chatty Interfaces
**Symptom:** Excessive fine-grained communication between services or layers.
**Impact:** Poor performance, high latency, network congestion.
**Remedy:** Coarser-grained APIs, batch operations, caching, event-driven communication.

### Leaky Abstractions
**Symptom:** Implementation details exposed through interfaces, tight coupling to underlying technology.
**Impact:** Changes cascade across system, difficult to swap implementations.
**Remedy:** Design interfaces that hide implementation details, depend on abstractions not concretions.

### Not Invented Here (NIH) Syndrome
**Symptom:** Building everything from scratch instead of using proven libraries/services.
**Impact:** Wasted effort, more bugs, maintenance burden.
**Remedy:** Evaluate build vs buy, leverage ecosystem, focus on core business value.

### Golden Hammer
**Symptom:** Using the same solution for every problem regardless of fit.
**Impact:** Suboptimal solutions, forced fit leading to workarounds.
**Remedy:** Evaluate multiple approaches, choose technology based on problem characteristics.

---

## Integration with Other Skills

**Architecture review connects with several other skills:**

### Technical Lead Role
Architecture review is a core responsibility of technical leads. Use this skill when:
- Providing technical direction for the team
- Evaluating proposed designs from team members
- Making technology decisions
- Planning major initiatives

### ADR (Architecture Decision Records)
Document significant architectural decisions from reviews:
- Record the context and problem
- Explain the decision made
- Document alternatives considered
- Capture trade-offs and consequences

### Refactoring
Architecture review identifies technical debt:
- Prioritize refactoring efforts based on review findings
- Plan incremental improvements
- Balance refactoring with feature development

### Testing Strategy
Architecture impacts testing approach:
- Testability is a key maintainability factor
- Different patterns require different testing strategies
- Review should assess test coverage and approach

### Performance Optimization
Performance dimension of architecture review:
- Identify architectural performance issues
- Distinguish between architectural and implementation optimizations
- Guide profiling and optimization efforts

### Code Review
Architecture review complements code review:
- Code review validates implementation of architecture
- Architecture review validates the overall design
- Both ensure quality at different levels

---

## Quick Reference

### Pre-Review Checklist
- [ ] Understand business requirements and constraints
- [ ] Review existing documentation and diagrams
- [ ] Identify stakeholders and subject matter experts
- [ ] Define scope of review (full system vs specific component)
- [ ] Allocate sufficient time (4-8 hours for thorough review)

### Review Session Checklist
- [ ] Evaluate scalability (horizontal, vertical, bottlenecks)
- [ ] Evaluate maintainability (coupling, cohesion, testability)
- [ ] Evaluate security (authentication, authorization, data protection)
- [ ] Evaluate performance (latency, throughput, optimization)
- [ ] Evaluate reliability (fault tolerance, availability, monitoring)
- [ ] Evaluate cost (resource utilization, optimization opportunities)
- [ ] Assess architecture patterns alignment with requirements
- [ ] Identify technical debt and prioritize
- [ ] Document trade-offs made
- [ ] Assess risks and mitigation strategies

### Post-Review Checklist
- [ ] Document findings and recommendations
- [ ] Share with stakeholders
- [ ] Create action items with owners and deadlines
- [ ] Document decisions in ADRs
- [ ] Update architecture documentation
- [ ] Schedule follow-up review if needed

### Red Flags Summary
- Single points of failure
- No monitoring or observability
- Secrets in code or version control
- No error handling for failures
- Tight coupling between components
- Over-provisioned or under-utilized resources
- No scalability strategy
- Missing or outdated documentation
- No testing strategy
- Undefined security model

---

**Remember:** Architecture is about making informed trade-offs. There is no perfect architecture—only architecture that fits the current requirements and constraints while enabling future evolution. A good architecture review identifies these trade-offs explicitly, ensures alignment with priorities, and provides a roadmap for continuous improvement.
