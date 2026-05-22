---
name: architecture-design-review
description: Conducts comprehensive architecture design reviews including system design validation, architecture pattern assessment, quality attributes evaluation, technology stack review, and scalability analysis. Produces detailed review reports with findings, recommendations, and risk assessments. Use when reviewing software architecture designs, validating architecture decisions, assessing system scalability, evaluating technology choices, or when users mention architecture review, design assessment, technical review, or architecture validation.
---

# Architecture Design Review

Conduct systematic architecture design reviews to validate system design, assess quality attributes, evaluate technology choices, and identify risks before implementation.

## Review Process

Follow this structured approach for comprehensive architecture reviews:

## 1. Gather Architecture Documentation

Collect required materials:

**Required Documents:**

- Architecture diagrams (C4: Context, Container, Component)
- Architecture Decision Records (ADRs) with rationale and alternatives
- Technical specifications and non-functional requirements (performance, scalability, security)
- Data models, schemas, and API specifications
- Technology stack with justifications
- Deployment and infrastructure diagrams

**Context Information:**

- Business constraints (budget, timeline, compliance requirements)
- Performance targets (quantified: response time, throughput)
- Scalability goals (user growth, data volume projections)
- Security requirements (authentication model, data protection, compliance)
- Integration requirements (internal/external systems, APIs)

### 2. Assess Architecture Style and Patterns

Validate architecture style appropriateness:

**Style-Requirement Fit:**

- **Monolithic**: Small teams (<10), simple domains, <1000 users
- **Microservices**: Large teams (>20), complex domains, >100K users
- **Serverless**: Event-driven, variable load, stateless operations
- **Event-Driven**: Asynchronous workflows, loose coupling, high throughput

**Pattern Assessment:**

```
☐ Architecture style matches requirements (scale, team, complexity)
☐ Service boundaries align with business domains (DDD)
☐ Communication patterns appropriate (sync vs async)
☐ Data management strategy clear (per-service vs shared DB)
☐ Integration patterns documented (gateway, mesh, events)
☐ Deployment model specified (containers, VMs, serverless)
```

**Anti-Pattern Detection:**

- **Big Ball of Mud**: No structure, tight coupling, shared database
- **God Service**: Single service handling multiple domains
- **Chatty Communication**: Excessive inter-service calls (>5/request)
- **Distributed Monolith**: Services coupled through shared database
- **Golden Hammer**: Same technology for all problems

### 3. Evaluate Quality Attributes

**Scalability Assessment:**

- Horizontal scaling: Load balancers, stateless services, auto-scaling
- Database scaling: Sharding, read replicas, caching layers
- Capacity planning: Current load → projected load (document growth strategy)
- Cost implications: Baseline and peak infrastructure costs

**Performance Validation:**

- Response time budgets allocated per layer
- Caching strategy (CDN, Redis, application cache)
- Database optimization (indexes, connection pooling, query analysis)
- Async processing for long-running tasks (queues, background jobs)

**Security Review:**

```
☐ Authentication mechanism (OAuth 2.0, JWT, SAML)
☐ Authorization model (RBAC, ABAC, policy-based)
☐ API security (rate limiting, input validation, CORS)
☐ Data encryption (at-rest: AES-256, in-transit: TLS 1.3)
☐ Secret management (AWS Secrets Manager, HashiCorp Vault)
☐ Network security (VPC, security groups, WAF)
☐ Security headers (HSTS, CSP, X-Frame-Options)
```

**Availability & Reliability:**

- Multi-AZ/region deployment for high availability
- Circuit breakers prevent cascade failures
- Health checks and auto-recovery configured
- Backup/DR procedures (RPO < 1hr, RTO < 4hrs)
- Graceful degradation for non-critical features

### 4. Review Technology Stack

**Technology Fit Validation:**

- Backend framework matches use case (Spring Boot, Node.js, Django, Go)
- Database selection justified (PostgreSQL, MongoDB, Cassandra, Redis)
- Deployment platform appropriate (Kubernetes, ECS, Cloud Run)
- Assess alternatives considered and documented in ADRs

**Technology Risk Assessment:**

- **Vendor Lock-in**: Evaluate portability and migration complexity
- **Team Skills**: Document training needs and timeline
- **Community Support**: Check ecosystem maturity and long-term viability
- **Performance**: Validate technology meets requirements
- **Licensing**: Verify compliance with commercial use

### 5. Analyze Data Architecture

**Data Strategy Validation:**

- Database per service vs shared database (justify choice)
- SQL vs NoSQL selection with rationale
- Data partitioning and sharding strategy
- Data consistency model (strong vs eventual)
- Data ownership clearly assigned
- Cross-service queries minimized

### 6. Review Monitoring and Observability

**Observability Checklist:**

```
☐ Metrics: Application, infrastructure, business metrics
☐ Logging: Centralized aggregation with correlation IDs
☐ Tracing: Distributed tracing across services
☐ Alerting: Error rate, latency, availability thresholds
☐ Dashboards: Real-time visibility into system health
☐ On-call: Rotation and escalation procedures
```

### 7. Generate Review Report

**Report Structure:**

1. **Executive Summary**: Architecture style, overall assessment (Approved/Conditional/Not Approved), top strengths and concerns

2. **Findings**: Organized by severity (Critical/High/Medium/Low) with:
   - Description and impact
   - Recommendation with effort estimate
   - Priority (Must Fix / Should Fix / Consider)

3. **Risk Assessment**: Technical, resource, timeline, operational risks with mitigations

**Finding Format:**

```
Finding: [Clear description]
Severity: Critical | High | Medium | Low
Impact: [Specific consequences]
Recommendation: [Actionable solution]
Effort: [Time estimate]
Priority: Must Fix | Should Fix | Consider
```

## Reference Documentation

Load detailed guidance for specific review areas:

**Core Review Resources:**

- **[architecture-review-process.md](references/architecture-review-process.md)** - Complete review methodology with phase-by-phase checklists
- **[review-checklists.md](references/review-checklists.md)** - Comprehensive validation checklists for all architecture aspects
- **[quality-attributes.md](references/quality-attributes.md)** - Detailed assessment of scalability, performance, security, reliability, maintainability
- **[common-patterns-to-validate.md](references/common-patterns-to-validate.md)** - Validation criteria for architecture patterns (microservices, event-driven, serverless)
- **[anti-patterns.md](references/anti-patterns.md)** - Common design flaws with detection criteria and remediation
- **[review-report-template.md](references/review-report-template.md)** - Report structure with examples and severity classification
- **[review-severity-levels.md](references/review-severity-levels.md)** - Severity classification criteria (Critical/High/Medium/Low)
- **[best-practices-for-architecture-reviews.md](references/best-practices-for-architecture-reviews.md)** - Review methodology best practices

**API & Integration:**

- **[api-design.md](references/api-design.md)** - REST, GraphQL, gRPC design assessment

**Data Architecture:**

- **[data-management.md](references/data-management.md)** - Data strategy, ownership, synchronization, consistency patterns
- **[data-storage-strategy.md](references/data-storage-strategy.md)** - Database selection, partitioning, replication
- **[data-consistency.md](references/data-consistency.md)** - Consistency models and trade-offs
- **[data-scalability.md](references/data-scalability.md)** - Sharding, replication, caching strategies
- **[database-selection.md](references/database-selection.md)** - SQL vs NoSQL, technology selection criteria

**Security:**

- **[application-security.md](references/application-security.md)** - Security architecture including authentication, authorization, encryption, compliance
- **[authentication-and-authorization.md](references/authentication-and-authorization.md)** - Identity and access management patterns

**Scalability & Performance:**

- **[horizontal-scalability.md](references/horizontal-scalability.md)** - Horizontal scaling strategies and auto-scaling
- **[caching-strategy.md](references/caching-strategy.md)** - Cache layers, invalidation, CDN

**Reliability & Operations:**

- **[high-availability-design.md](references/high-availability-design.md)** - HA architecture, redundancy, failover
- **[fault-tolerance.md](references/fault-tolerance.md)** - Circuit breakers, retries, bulkheads, timeouts
- **[disaster-recovery.md](references/disaster-recovery.md)** - Backup, recovery procedures, RPO/RTO planning
- **[monitoring-and-observability.md](references/monitoring-and-observability.md)** - Metrics, logging, tracing, alerting

**Microservices:**

- **[service-boundaries-microservices.md](references/service-boundaries-microservices.md)** - Service decomposition, bounded contexts, domain boundaries

**Additional Topics:**

- **[external-integrations.md](references/external-integrations.md)** - Third-party API integration patterns
- **[testing-strategy.md](references/testing-strategy.md)** - Test coverage, integration testing, contract testing
- **[operational-readiness.md](references/operational-readiness.md)** - Production readiness checklist
- **[cost-analysis.md](references/cost-analysis.md)** - Infrastructure cost estimation and optimization
- **[infrastructure-costs.md](references/infrastructure-costs.md)** - Detailed cost breakdown by component
- **[infrastructure.md](references/infrastructure.md)** - Infrastructure design and deployment patterns
- **[risk-assessment.md](references/risk-assessment.md)** - Technical risk identification and mitigation

**Note**: For technology selection guidance (frameworks, databases, cloud platforms), reference the architecture-design skill.

## Critical Review Principles

**Focus on Architecture, Not Implementation:**

- Review designs and patterns, not code quality
- Validate decisions and trade-offs, not syntax
- Assess structure and boundaries, not variable names

**Be Specific with Findings:**
✅ "Circuit breaker missing on Order→Payment calls (avg 50 calls/sec). Add Resilience4j with 50% error threshold."
❌ "Need better error handling"

**Quantify Performance Requirements:**
✅ "API response time must be <200ms for 95th percentile at 1000 req/s"
❌ "API should be fast"

**Provide Actionable Recommendations:**
✅ "Split UserService into Authentication (identity) and Profile (data) services. Estimated 3-week effort. Use event bus for sync."
❌ "Consider improving service boundaries"

**Assess Based on Context:**

- Startup MVP has different requirements than enterprise system
- 100-user system doesn't need microservices complexity
- Evaluate appropriateness for scale, team, and timeline
