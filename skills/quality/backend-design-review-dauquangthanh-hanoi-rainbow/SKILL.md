---
name: backend-design-review
description: Conducts comprehensive backend design reviews covering API design quality, database architecture validation, microservices patterns assessment, integration strategies evaluation, security design review, and scalability analysis. Evaluates API specifications (REST, GraphQL, gRPC), database schemas, service boundaries, authentication/authorization flows, caching strategies, message queues, and deployment architectures. Identifies design flaws, security vulnerabilities, performance bottlenecks, and scalability issues. Produces detailed design review reports with severity-rated findings, architecture diagrams, and implementation recommendations. Use when reviewing backend system designs, validating API specifications, assessing database schemas, evaluating microservices architectures, reviewing integration patterns, or when users mention backend design review, API design validation, database design review, microservices assessment, or backend architecture evaluation.
---

# Backend Design Review

## Review Workflow

Follow this systematic review process:

## 1. Pre-Review Preparation

- Gather design documentation (architecture diagrams, API specs, database schemas, ADRs)
- Understand requirements (functional, non-functional, compliance)
- Define review scope and priorities
- Identify constraints (technology, budget, timeline)

### 2. API Design Review

- Evaluate RESTful resource modeling, HTTP method usage, status codes
- Review GraphQL schema design, type definitions, query patterns
- Assess gRPC service definitions and protobuf schemas
- Validate API versioning strategy and documentation
- Check authentication, authorization, and security measures

### 3. Database Design Validation

- Review data modeling, entity relationships, normalization
- Assess schema design, column types, constraints, indexes
- Evaluate query patterns and N+1 query prevention
- Check data integrity rules and referential integrity
- Review scalability approach (sharding, replicas, caching)

### 4. Architecture Assessment

- Evaluate service boundaries and decomposition
- Review communication patterns (sync/async, event-driven)
- Assess resilience patterns (circuit breakers, retries, timeouts)
- Check service discovery and load balancing design
- Validate data management and consistency strategies

### 5. Security Review

- Evaluate authentication mechanisms (OAuth 2.0, JWT)
- Review authorization model (RBAC, ABAC)
- Assess data protection (encryption at rest/transit, secrets)
- Check input validation and injection prevention
- Review security monitoring and audit logging

### 6. Performance & Scalability

- Assess caching strategy (layers, invalidation, TTL)
- Review database indexing and query optimization
- Evaluate horizontal/vertical scaling approach
- Check load balancing and auto-scaling design
- Review asynchronous processing patterns

### 7. Report Generation

- Categorize findings by severity (Critical, High, Medium, Low)
- Document detailed findings with examples
- Provide specific, actionable recommendations
- Create architecture improvement diagrams
- Define implementation roadmap and priorities

## Review Scope

### API Design Quality

- RESTful API assessment (resource modeling, HTTP methods, status codes, versioning)
- GraphQL schema review (types, resolvers, complexity, N+1 prevention)
- gRPC service review (protobuf definitions, streaming, error handling)
- API documentation quality (OpenAPI/Swagger completeness)
- API security design (authentication, authorization, rate limiting, validation)

### Database Architecture

- Data modeling (entity relationships, normalization, domain alignment)
- Schema design (tables, columns, constraints, indexes, partitioning)
- Query patterns (efficiency, index usage, N+1 prevention)
- Data integrity (referential integrity, constraints, validation)
- Scalability (sharding, read replicas, caching)

### Microservices Patterns

- Service boundaries (decomposition, bounded contexts, DDD alignment)
- Communication patterns (sync/async, event-driven, orchestration)
- Data management (database-per-service, eventual consistency, sagas)
- Service discovery (registry, load balancing)
- Resilience (circuit breakers, retries, timeouts, bulkheads)

### Integration Architecture

- Integration patterns (API, message queues, event streaming, webhooks)
- Message queue design (selection, schemas, DLQ, idempotency)
- Event streaming (event sourcing, CQRS, stream processing)
- External API integration (retry logic, circuit breakers, versioning)
- Batch processing (ETL, job scheduling, error handling)

### Security Architecture

- Authentication design (JWT, OAuth 2.0, session management)
- Authorization design (RBAC, ABAC, permission models)
- Data protection (encryption at rest/transit, secrets management)
- API security (validation, injection prevention, rate limiting)
- Security monitoring (audit logging, anomaly detection)

## Severity Levels

Use these severity ratings for findings:

- **🔴 Critical**: Security risks, data loss, broken functionality - must fix before implementation
- **🟠 High**: Significant flaws affecting scalability, performance, reliability - should fix before go-live
- **🟡 Medium**: Moderate issues or best practice deviations - address in next iteration
- **🟢 Low**: Minor improvements or optimizations - track for future improvements

## Report Structure

Present backend design review findings with:

1. **Executive Summary** - Project context, review date, overall assessment
2. **Review Scope** - What was reviewed, depth of review, focus areas
3. **Key Findings Summary** - Critical and high severity issues overview
4. **Detailed Findings** - Each finding with severity, description, impact, recommendations, examples
5. **Positive Observations** - Strengths and good design decisions
6. **Recommendations** - Prioritized improvements with implementation guidance
7. **Architecture Diagrams** - Current state and proposed improvements
8. **Action Items** - Specific tasks with owners, deadlines, and status tracking
9. **Next Steps** - Immediate actions, short-term tasks, follow-up review schedule

## Reference Files

Load detailed guidance based on specific review needs:

- **Review Process**: See [backend-design-review-process.md](references/backend-design-review-process.md) for comprehensive step-by-step review workflow covering API design, database validation, microservices assessment, security review, and performance evaluation with detailed checklists

- **API Design Patterns**: See [api-design-patterns.md](references/api-design-patterns.md) when reviewing RESTful APIs, GraphQL schemas, or gRPC services - includes resource modeling, HTTP methods, status codes, versioning strategies, authentication patterns, and common anti-patterns

- **Database Design Patterns**: See [database-design-patterns.md](references/database-design-patterns.md) for detailed guidance on data modeling, normalization, indexing strategies, query optimization, database scaling patterns, NoSQL patterns, and caching strategies

- **Microservices & Integration Patterns**: See [microservices-integration-patterns.md](references/microservices-integration-patterns.md) when reviewing microservices architecture, service boundaries, communication patterns, resilience patterns, message queues, event streaming, and distributed system designs

- **Report Template**: See [report-template.md](references/report-template.md) for complete report structure with sections for executive summary, findings, recommendations, architecture diagrams, and action items

- **Severity Levels**: See [severity-levels.md](references/severity-levels.md) for detailed severity rating criteria (Critical, High, Medium, Low) with examples and action requirements
