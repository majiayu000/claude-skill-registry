---
name: backend-design
description: Designs comprehensive backend systems including RESTful APIs, microservices, database architecture, authentication/authorization, caching strategies, message queues, and scalability patterns. Produces API specifications, database schemas, architecture diagrams, and implementation guides. Use when designing backend services, APIs, data models, distributed systems, authentication flows, or when users mention backend architecture, API design, database design, microservices, or server-side development.
---

# Backend Design

## Workflow

Follow this systematic design process:

1. **Requirements Analysis**
   - Gather functional requirements (features, operations)
   - Define non-functional requirements (performance, scalability, availability)
   - Identify constraints (budget, timeline, technology, compliance)

2. **Architecture Selection**
   - Choose architecture pattern (monolith, microservices, serverless)
   - Select technology stack based on requirements
   - Define service boundaries and responsibilities

3. **API Design**
   - Design RESTful endpoints with proper resource modeling
   - Define request/response schemas and contracts
   - Plan versioning strategy and documentation
   - See [api-design-guide.md](references/api-design-guide.md) for REST/GraphQL/gRPC patterns

4. **Database Design**
   - Model entities and relationships
   - Design schema with normalization
   - Plan indexing and partitioning strategies
   - See [database-design.md](references/database-design.md) for relational and NoSQL patterns

5. **Security Design**
   - Design authentication flow (OAuth 2.0, JWT)
   - Plan authorization model (RBAC, ABAC)
   - Define data encryption and protection strategy

6. **Scalability & Performance**
   - Design caching strategy (Redis, CDN)
   - Plan load balancing and auto-scaling
   - Define asynchronous processing with message queues

7. **Documentation**
   - Create API specifications (OpenAPI/Swagger)
   - Document architecture decisions with Mermaid diagrams
   - Provide implementation guidelines and roadmap

## Output Structure

Present your backend design with these sections:

1. **System Overview** - High-level architecture, components, technology stack
2. **API Specification** - Endpoints, schemas, authentication, OpenAPI docs
3. **Database Design** - ERD, schema, indexes, migration plan
4. **Architecture Decisions** - Service decomposition, communication patterns, consistency model
5. **Security Implementation** - Authentication/authorization flows, encryption
6. **Scalability Plan** - Load balancing, caching, database scaling, auto-scaling
7. **Deployment Architecture** - Containers, infrastructure, CI/CD, monitoring
8. **Implementation Roadmap** - Phases, milestones, dependencies, risks

## Core Principles

- **API-first approach** - Design and document APIs before implementation
- **Security by design** - Build authentication, authorization, and encryption from the start
- **Design for scalability** - Plan for growth with caching, load balancing, and horizontal scaling
- **Plan for failure** - Include error handling, retries, circuit breakers, and graceful degradation
- **Document thoroughly** - Create clear API specs, Mermaid architecture diagrams, and implementation guides

## Reference Files

Load additional resources based on specific needs:

- **Detailed Design Process**: See [backend-design-process.md](references/backend-design-process.md) for comprehensive step-by-step workflow with examples for API design, database modeling, authentication flows, and microservices patterns

- **API Design Guide**: See [api-design-guide.md](references/api-design-guide.md) when designing RESTful APIs, GraphQL schemas, or gRPC services - includes resource modeling, status codes, versioning strategies, and documentation

- **Database Design**: See [database-design.md](references/database-design.md) for detailed guidance on relational and NoSQL database design, normalization, indexing, partitioning, and replication strategies

- **Best Practices**: See [best-practices.md](references/best-practices.md) for API design, database optimization, security hardening, performance tuning, and reliability patterns

- **Common Patterns**: See [common-patterns.md](references/common-patterns.md) for code examples of repository pattern, service layer, dependency injection, and other architectural patterns

- **Example Projects**: See [examples.md](references/examples.md) for complete architecture examples including e-commerce systems, real-time chat applications, and microservices implementations
