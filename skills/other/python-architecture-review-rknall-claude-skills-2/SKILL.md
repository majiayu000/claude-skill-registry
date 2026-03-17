---
name: "Python Backend Architecture Review"
description: "Comprehensive design architecture review for Python backend applications. Use this skill when users ask you to review, analyze, or provide feedback on backend architecture designs, system design documents, or Python application architecture. Covers scalability, security, performance, database design, API design, microservices patterns, deployment architecture, and best practices."
---

# Python Backend Architecture Review

This skill provides comprehensive architecture review capabilities for Python backend applications, covering all aspects of system design from infrastructure to code organization.

## When to Use This Skill

Activate this skill when the user requests:
- Review of a backend architecture design document
- Feedback on system design for a Python application
- Analysis of scalability patterns and approaches
- Security review of backend architecture
- Database design evaluation
- API design assessment
- Microservices architecture review
- Performance optimization recommendations
- Cloud infrastructure architecture review
- Code organization and project structure analysis

## Review Framework

### 1. Initial Analysis

When a user provides an architecture document or describes their system, begin by:

1. **Understanding Context**
   - Ask clarifying questions about:
     - Expected scale (users, requests/sec, data volume)
     - Performance requirements (latency, throughput)
     - Security and compliance requirements
     - Team size and expertise
     - Budget constraints
     - Timeline expectations

2. **Document Analysis**
   - If architecture diagrams or documents are provided, analyze:
     - Component relationships and boundaries
     - Data flow patterns
     - External dependencies
     - Technology stack choices
     - Deployment topology

### 2. Comprehensive Review Areas

Evaluate the architecture across these dimensions:

#### A. System Architecture & Design Patterns

**Evaluate:**
- Overall architectural style (monolith, microservices, serverless, hybrid)
- Service boundaries and responsibilities
- Communication patterns (sync/async, REST/GraphQL/gRPC)
- Event-driven architecture components
- CQRS and Event Sourcing patterns where applicable
- Domain-Driven Design principles
- Separation of concerns
- Dependency management

**Provide Feedback On:**
- Whether the chosen architecture matches the scale and complexity
- Over-engineering or under-engineering concerns
- Missing components or services
- Tight coupling issues
- Single points of failure
- Scalability bottlenecks

**Python-Specific Considerations:**
- Framework selection (FastAPI, Django, Flask, etc.)
- ASGI vs WSGI considerations
- Async/await patterns and usage
- Python's GIL impact on architecture decisions
- Multi-processing vs multi-threading strategies

#### B. Database Architecture

**Evaluate:**
- Database type selection (PostgreSQL, MySQL, MongoDB, Redis, etc.)
- Data modeling approach
- Normalization vs denormalization strategy
- Sharding and partitioning plans
- Read replicas and replication strategy
- Caching layers (Redis, Memcached)
- Database connection pooling
- Transaction management
- Data consistency models (strong, eventual)

**Provide Feedback On:**
- Schema design quality
- Index strategies
- Query optimization patterns
- N+1 query prevention
- Database migration strategy
- Backup and disaster recovery
- Multi-tenancy approaches if applicable
- Data retention and archival strategies

**Python-Specific Considerations:**
- ORM selection (SQLAlchemy, Django ORM, Tortoise ORM, etc.)
- Raw SQL vs ORM tradeoffs
- Async database drivers (asyncpg, motor, etc.)
- Migration tools (Alembic, Django migrations)

#### C. API Design & Communication

**Evaluate:**
- API design patterns (RESTful, GraphQL, gRPC)
- Endpoint structure and naming
- Request/response formats
- Versioning strategy
- Authentication and authorization
- Rate limiting and throttling
- API documentation approach
- Contract-first vs code-first design
- WebSocket usage for real-time features
- Message queue integration (RabbitMQ, Kafka, SQS)

**Provide Feedback On:**
- API consistency and conventions
- Error handling and status codes
- Pagination strategies
- Filtering and search capabilities
- Idempotency guarantees
- Backward compatibility approach
- GraphQL schema design if applicable
- gRPC service definitions if applicable

**Python-Specific Considerations:**
- FastAPI automatic OpenAPI generation
- Pydantic validation models
- Django REST Framework serializers
- GraphQL libraries (Strawberry, Graphene, Ariadne)
- gRPC-python code generation

#### D. Security Architecture

**Evaluate:**
- Authentication mechanisms (JWT, OAuth2, session-based)
- Authorization model (RBAC, ABAC, policy-based)
- API security (rate limiting, CORS, CSRF protection)
- Data encryption (at rest and in transit)
- Secrets management approach
- Network security (VPC, security groups, firewall rules)
- Input validation and sanitization
- SQL injection prevention
- XSS and CSRF protections
- Dependency vulnerability scanning
- Security headers implementation

**Provide Feedback On:**
- Authentication/authorization gaps
- Sensitive data exposure risks
- Missing security controls
- Overly permissive access
- Insecure defaults
- Lack of audit logging
- Missing security monitoring

**Python-Specific Considerations:**
- Usage of python-jose, PyJWT for token handling
- Password hashing with bcrypt, argon2
- Environment variable management (python-dotenv)
- Security middleware in frameworks
- SQLAlchemy parameterized queries

#### E. Scalability & Performance

**Evaluate:**
- Horizontal vs vertical scaling strategy
- Load balancing approach
- Auto-scaling configuration
- Caching strategy (application, database, CDN)
- Async processing for long-running tasks
- Background job processing (Celery, RQ, Dramatiq)
- Queue-based architectures
- Database read replicas
- Connection pooling
- Resource optimization

**Provide Feedback On:**
- Scalability bottlenecks
- Missing caching layers
- Inefficient data access patterns
- Synchronous operations that should be async
- Missing queue infrastructure
- Poor resource utilization
- Lack of performance monitoring

**Python-Specific Considerations:**
- ASGI server selection (Uvicorn, Hypercorn)
- Gunicorn worker configuration
- Celery worker configuration
- Async framework usage (asyncio best practices)
- Performance profiling tools (cProfile, py-spy)
- GIL workarounds for CPU-bound tasks

#### F. Observability & Monitoring

**Evaluate:**
- Logging strategy and centralization
- Metrics collection and aggregation
- Distributed tracing implementation
- Error tracking and alerting
- Health check endpoints
- Performance monitoring
- Business metrics tracking
- Log aggregation tools (ELK, Loki, CloudWatch)
- APM tools (DataDog, New Relic, Prometheus)

**Provide Feedback On:**
- Missing observability components
- Insufficient logging detail
- Lack of structured logging
- No distributed tracing
- Missing critical alerts
- No performance baselines
- Inadequate error tracking

**Python-Specific Considerations:**
- Structured logging libraries (structlog, python-json-logger)
- OpenTelemetry Python SDK
- Sentry integration
- StatsD/Prometheus client libraries
- Context propagation in async code

#### G. Deployment & Infrastructure

**Evaluate:**
- Containerization strategy (Docker)
- Orchestration approach (Kubernetes, ECS, etc.)
- CI/CD pipeline design
- Environment management (dev, staging, prod)
- Infrastructure as Code (Terraform, CloudFormation)
- Blue-green or canary deployment strategies
- Rollback procedures
- Configuration management
- Secret management in deployment

**Provide Feedback On:**
- Deployment complexity
- Missing automation
- Lack of environment parity
- No rollback strategy
- Insufficient testing in pipeline
- Manual deployment steps
- Missing infrastructure versioning

**Python-Specific Considerations:**
- Docker image optimization (multi-stage builds)
- Dependency management (pip, Poetry, PDM)
- Virtual environment handling in containers
- Python version management
- Compiled dependencies (wheel files)

#### H. Code Organization & Project Structure

**Evaluate:**
- Project directory structure
- Module and package organization
- Dependency injection patterns
- Configuration management
- Environment variable usage
- Testing strategy and organization
- Code reusability patterns
- Package/module boundaries

**Provide Feedback On:**
- Unclear module responsibilities
- Circular dependencies
- Poorly organized code structure
- Lack of separation between layers
- Missing configuration abstraction
- Hard-coded values
- Insufficient test coverage

**Python-Specific Considerations:**
- Package structure (src layout vs flat layout)
- __init__.py organization
- Import patterns and circular import prevention
- Type hints and mypy configuration
- Pydantic settings management
- pytest organization and fixtures

#### I. Data Flow & State Management

**Evaluate:**
- Request lifecycle and data flow
- State management approach
- Session management
- Cache invalidation strategy
- Event flow in event-driven systems
- Data transformation layers
- Data validation points

**Provide Feedback On:**
- Unclear data flow
- State synchronization issues
- Missing validation layers
- Inconsistent data transformation
- Cache coherence problems
- Session management issues

#### J. Resilience & Error Handling

**Evaluate:**
- Retry mechanisms and backoff strategies
- Circuit breaker patterns
- Timeout configurations
- Graceful degradation approach
- Error handling consistency
- Dead letter queue handling
- Bulkhead patterns
- Rate limiting and throttling

**Provide Feedback On:**
- Missing fault tolerance patterns
- Cascading failure risks
- Lack of timeouts
- No circuit breakers for external services
- Inconsistent error handling
- Missing retry logic
- No graceful degradation

**Python-Specific Considerations:**
- tenacity library for retries
- asyncio timeout handling
- Exception hierarchy design
- Context managers for resource cleanup

### 3. Review Output Format

Structure your review as follows:

#### Executive Summary
- Overall architecture assessment (1-3 paragraphs)
- Key strengths identified
- Critical concerns requiring immediate attention
- Overall maturity and readiness assessment

#### Detailed Findings

For each review area, provide:

**[Area Name]**

**Strengths:**
- Bullet points of what's done well

**Concerns:**
- HIGH: Critical issues that must be addressed
- MEDIUM: Important issues that should be addressed
- LOW: Nice-to-have improvements

**Recommendations:**
- Specific, actionable recommendations
- Alternative approaches to consider
- Best practices to follow
- Python-specific library or tool suggestions

#### Architecture Patterns & Best Practices

Suggest proven patterns relevant to their use case:
- Specific design patterns (Repository, Factory, Strategy, etc.)
- Integration patterns
- Python-specific idioms
- Framework-specific best practices

#### Technology Stack Assessment

Review their chosen technologies:
- Appropriateness for the use case
- Team expertise considerations
- Community support and maturity
- Alternative options to consider
- Python package ecosystem recommendations

#### Scalability Roadmap

If the architecture needs to scale:
- Current limitations
- Scaling stages and triggers
- Migration strategies
- Cost projections at different scales

#### Security Checklist

Provide a specific security checklist:
- Authentication/authorization items
- Data protection items
- Network security items
- Compliance considerations (GDPR, HIPAA, etc.)
- Python security best practices

#### Next Steps & Priorities

Rank recommendations by:
1. Must-fix items (blocking issues)
2. Should-fix items (important for production)
3. Nice-to-have items (improvements)

Include estimated effort and dependencies.

### 4. Interactive Review Process

When conducting the review:

1. **Start with clarifying questions** if the architecture description is incomplete
2. **Ask about constraints** (budget, timeline, team size)
3. **Understand the domain** and specific business requirements
4. **Request diagrams or documentation** if not provided
5. **Provide incremental feedback** for large architectures
6. **Offer to dive deeper** into specific areas of concern
7. **Suggest example implementations** or reference architectures
8. **Provide code examples** for recommended patterns

### 5. Reference Resources

When relevant, reference:
- 12-Factor App principles
- Python package recommendations (awesome-python)
- Cloud provider best practices (AWS Well-Architected, etc.)
- Security frameworks (OWASP Top 10)
- Performance benchmarking resources
- Open-source reference implementations
- Python-specific resources (PEPs, Python Enhancement Proposals)

### 6. Tools & Automation Recommendations

Suggest tools for:
- Static analysis (Ruff, pylint, flake8, mypy)
- Security scanning (Bandit, Safety, Snyk)
- Performance profiling (cProfile, py-spy, scalene)
- Load testing (Locust, Artillery)
- Monitoring (Prometheus, Grafana, DataDog)
- Documentation (Sphinx, MkDocs)
- Dependency management (Poetry, PDM, pip-tools)
- Code formatting (Black, Ruff)

## Communication Style

When providing reviews:
- Be constructive and specific
- Explain the "why" behind recommendations
- Provide examples and code snippets
- Balance criticism with recognition of good practices
- Prioritize issues clearly
- Offer multiple solutions when applicable
- Consider the team's context and constraints
- Use clear, professional language
- Include Python code examples where helpful
- Reference Python documentation and PEPs

## Example Questions to Ask

Before starting a review, consider asking:

1. What is the expected scale of this system (users, requests, data)?
2. What are the critical performance requirements?
3. Are there specific compliance or security requirements?
4. What is the team's experience level with Python backend development?
5. What is the current development stage (design, prototype, production)?
6. Are there any existing systems this needs to integrate with?
7. What is the budget for infrastructure?
8. What is the timeline for deployment?
9. Are there any technology preferences or constraints?
10. What are the most critical features for the initial release?

## Deliverables

At the end of a review, you should have provided:

1. Executive summary with overall assessment
2. Detailed findings across all review areas
3. Prioritized list of recommendations
4. Security checklist
5. Scalability roadmap (if applicable)
6. Technology stack assessment
7. Next steps with effort estimates
8. Optional: Example code or architectural diagrams
9. Optional: Reference links and resources

## Continuous Improvement

After the initial review:
- Offer to review specific areas in more depth
- Provide guidance on implementing recommendations
- Help with specific technical challenges
- Review updated designs
- Answer follow-up questions

Remember: The goal is to help the user build a robust, scalable, secure, and maintainable Python backend system that meets their specific needs and constraints.
