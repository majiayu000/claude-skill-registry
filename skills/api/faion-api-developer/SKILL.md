---
name: faion-api-developer
description: "API development: REST, GraphQL, OpenAPI, versioning, auth, rate limiting."
user-invocable: false
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Task, AskUserQuestion, TodoWrite, Skill
---
> **Entry point:** `/faion-net` — invoke this skill for automatic routing to the appropriate domain.

# API Developer Skill

API design and development covering REST, GraphQL, OpenAPI specifications, authentication, and API best practices.

## Purpose

Handles API design, documentation, authentication, rate limiting, versioning, and API-specific patterns.

---

## Context Discovery

### Auto-Investigation

Detect API patterns from project:

| Signal | How to Check | What It Tells Us |
|--------|--------------|------------------|
| OpenAPI spec | `Glob("**/openapi.yaml")` or `Glob("**/swagger.*")` | API documented |
| GraphQL schema | `Glob("**/*.graphql")` | GraphQL API |
| DRF | `Grep("rest_framework", "**/settings.py")` | Django REST Framework |
| FastAPI | `Grep("fastapi", "**/requirements.txt")` | FastAPI used |
| Express routes | `Grep("app.get\|app.post\|router", "**/*.js")` | Express API |
| Auth middleware | `Grep("jwt\|oauth\|auth", "**/*.py")` | Auth patterns |

**Read existing patterns:**
- Check existing endpoints for conventions
- Read serializers/schemas for data patterns
- Check middleware for auth/rate limiting

### Discovery Questions

#### Q1: API Type

```yaml
question: "What type of API are you building?"
header: "Type"
multiSelect: false
options:
  - label: "REST API"
    description: "Resource-based HTTP endpoints"
  - label: "GraphQL API"
    description: "Query language, single endpoint"
  - label: "WebSocket/Real-time"
    description: "Bidirectional communication"
  - label: "RPC-style"
    description: "Action-based endpoints"
```

**Routing:**
- "REST" → api-rest-design, OpenAPI
- "GraphQL" → graphql-api-design
- "WebSocket" → websocket-design
- "RPC" → REST patterns adapted

#### Q2: API Consumers

```yaml
question: "Who will consume this API?"
header: "Consumers"
multiSelect: true
options:
  - label: "Own frontend (SPA/mobile)"
    description: "First-party clients"
  - label: "Third-party developers"
    description: "Public API, need docs"
  - label: "Internal services"
    description: "Microservices communication"
  - label: "Partners (B2B)"
    description: "Specific integrations"
```

**Context impact:**
- "Own frontend" → Simpler auth, less versioning
- "Third-party" → Full docs, versioning, rate limits
- "Internal" → Service auth, less public docs
- "Partners" → API keys, dedicated support

#### Q3: Authentication Needs

```yaml
question: "How should API authentication work?"
header: "Auth"
multiSelect: false
options:
  - label: "JWT tokens"
    description: "Stateless, self-contained tokens"
  - label: "Session-based"
    description: "Server-side sessions"
  - label: "API keys"
    description: "Simple key-based auth"
  - label: "OAuth 2.0"
    description: "Third-party auth flow"
  - label: "No auth needed"
    description: "Public API"
```

#### Q4: Documentation Approach

```yaml
question: "How should API be documented?"
header: "Docs"
multiSelect: false
options:
  - label: "OpenAPI/Swagger (auto-generated)"
    description: "Generate from code"
  - label: "OpenAPI (design-first)"
    description: "Write spec first, then implement"
  - label: "Markdown docs"
    description: "Manual documentation"
  - label: "GraphQL introspection"
    description: "Self-documenting schema"
```

---

## When to Use

- REST API design and implementation
- GraphQL API design
- OpenAPI/Swagger specifications
- API authentication (OAuth, JWT, API keys)
- API versioning strategies
- API rate limiting and throttling
- API error handling
- API testing
- API gateways
- API monitoring
- WebSocket APIs

## Methodologies

| Category | Methodology | File |
|----------|-------------|------|
| **REST APIs** |
| REST API design | RESTful principles, resource design | api-rest-design.md |
| REST API design alt | REST patterns and best practices | rest-api-design.md |
| **GraphQL** |
| GraphQL API basics | Schema, queries, mutations | api-graphql.md |
| GraphQL API design | Schema design, resolvers, federation | graphql-api-design.md |
| GraphQL API alt | GraphQL patterns | graphql-api.md |
| **OpenAPI** |
| OpenAPI spec | OpenAPI 3.x specification | api-openapi-spec.md |
| OpenAPI specification | Spec writing, code generation | openapi-specification.md |
| **API Patterns** |
| Contract-first API | Schema-first development | api-contract-first.md |
| Contract-first development | API-first approach | contract-first-development.md |
| API versioning | Version strategies (URL, header, media type) | api-versioning.md |
| API error handling | Error codes, error responses | api-error-handling.md |
| API authentication | OAuth 2.0, JWT, API keys | api-authentication.md |
| API rate limiting | Rate limiting strategies | api-rate-limiting.md |
| Rate limiting | Throttling patterns | rate-limiting.md |
| API gateway patterns | Gateway design, BFF pattern | api-gateway-patterns.md |
| API monitoring | Metrics, logging, tracing | api-monitoring.md |
| **Testing & Docs** |
| API testing | Integration testing, contract testing | api-testing.md |
| API documentation | API docs, Swagger UI | api-documentation.md |
| **Real-time** |
| WebSocket design | WebSocket patterns, real-time APIs | websocket-design.md |

## Tools

- **REST:** OpenAPI 3.x, Swagger, Postman
- **GraphQL:** Apollo Server, GraphQL Yoga, Hasura
- **Auth:** OAuth 2.0, JWT, Passport.js, Auth0
- **Testing:** Postman, REST Client, Hoppscotch
- **Documentation:** Swagger UI, Redoc, Stoplight
- **Gateways:** Kong, Tyk, API Gateway (AWS)

## Related Sub-Skills

| Sub-skill | Relationship |
|-----------|--------------|
| faion-python-developer | Django REST Framework, FastAPI |
| faion-javascript-developer | Express, Fastify, GraphQL |
| faion-backend-developer | API implementation in Go, Java, etc. |
| faion-testing-developer | API testing strategies |

## Integration

Invoked by parent skill `faion-software-developer` for API design and implementation work.

---

## Methodology Context & Decision Trees

### api-rest-design.md

**Required Context:**
- [ ] API consumers defined (frontend, third-party, internal)
- [ ] Data entities/resources modeled
- [ ] Authentication requirements known
- [ ] Versioning strategy decided

**Decision Tree:**
```
Start
├── Resources/entities clear?
│   └── NO → faion-ba-modeling (data-analysis) first
├── Consumers defined?
│   └── NO → faion-product-manager (stakeholder-analysis)
├── Auth requirements?
│   └── NO → See api-authentication.md
└── YES to all → Proceed with REST design
```

**If Missing:**
| Context | Skill/Methodology |
|---------|-------------------|
| Data model | faion-ba-modeling → data-analysis |
| Security needs | faion-software-architect → security-architecture |
| Consumer requirements | faion-product-manager → product-operations |

---

### graphql-api-design.md

**Required Context:**
- [ ] Data relationships understood (graph structure)
- [ ] Query patterns known
- [ ] N+1 awareness
- [ ] Client requirements (frontend framework)

**Decision Tree:**
```
Start
├── Complex relationships?
│   └── NO → Consider REST instead (simpler)
├── Multiple clients with different needs?
│   └── NO → REST may be sufficient
├── Need real-time subscriptions?
│   └── YES → GraphQL with subscriptions
└── Proceed with GraphQL
```

**If Missing:**
| Context | Skill/Methodology |
|---------|-------------------|
| Data relationships | faion-ba-modeling → data-analysis |
| Query optimization | faion-backend-systems → database-optimization |
| Frontend needs | faion-frontend-developer |

---

### api-authentication.md

**Required Context:**
- [ ] User types (end-user, service, admin)
- [ ] Session requirements (stateless vs stateful)
- [ ] Third-party auth needs (OAuth providers)
- [ ] Security compliance (OWASP, SOC2)

**Decision Tree:**
```
Start
├── Third-party login needed?
│   └── YES → OAuth 2.0 / OIDC
├── Service-to-service?
│   └── YES → API keys or mTLS
├── Need stateless?
│   └── YES → JWT tokens
├── Need session management?
│   └── YES → Session-based auth
└── Simple internal API → API keys
```

**If Missing:**
| Context | Skill/Methodology |
|---------|-------------------|
| Security requirements | faion-software-architect → security-architecture |
| Compliance needs | faion-devops-engineer → security-compliance |
| User types | faion-ba-core → stakeholder-analysis |

---

### api-versioning.md

**Required Context:**
- [ ] API maturity (new vs established)
- [ ] Breaking change frequency
- [ ] Client update capability
- [ ] Deprecation policy

**Decision Tree:**
```
Start
├── Public API with external clients?
│   └── YES → URL versioning (/v1/) recommended
├── Internal services only?
│   └── YES → Header versioning or no versioning
├── GraphQL?
│   └── YES → Schema evolution, no versioning needed
└── Frequent breaking changes → Media type versioning
```

**If Missing:**
| Context | Skill/Methodology |
|---------|-------------------|
| API consumers | faion-product-manager → stakeholder-analysis |
| Deprecation policy | faion-sdd-planning → spec-writing |

---

### api-rate-limiting.md

**Required Context:**
- [ ] Traffic patterns known
- [ ] Client tiers (free, paid, enterprise)
- [ ] Infrastructure capacity
- [ ] Burst vs sustained load

**Decision Tree:**
```
Start
├── Multi-tenant SaaS?
│   └── YES → Per-tenant rate limits
├── Public API?
│   └── YES → Tiered rate limiting
├── Internal only?
│   └── Consider circuit breakers instead
└── Define limits: requests/minute/hour/day
```

**If Missing:**
| Context | Skill/Methodology |
|---------|-------------------|
| Traffic analysis | faion-software-architect → performance-architecture |
| Pricing tiers | faion-product-manager → product-planning |
| Infrastructure | faion-devops-engineer → infrastructure |

---

### api-error-handling.md

**Required Context:**
- [ ] Error categories defined
- [ ] Client error display requirements
- [ ] Logging/monitoring setup
- [ ] Localization needs

**Decision Tree:**
```
Start
├── Public API?
│   └── YES → RFC 7807 Problem Details
├── Internal API?
│   └── Consistent error schema
├── Need debugging info?
│   └── DEV only, never in production
└── Always: structured errors, proper HTTP codes
```

**If Missing:**
| Context | Skill/Methodology |
|---------|-------------------|
| Error categories | faion-ba-core → requirements-analysis |
| Monitoring | faion-software-architect → observability-architecture |

---

### api-openapi-spec.md

**Required Context:**
- [ ] All endpoints defined
- [ ] Request/response schemas
- [ ] Auth schemes
- [ ] Examples for each endpoint

**Decision Tree:**
```
Start
├── Design-first approach?
│   └── YES → Write OpenAPI first, generate code
├── Code-first approach?
│   └── YES → Generate OpenAPI from code
├── Need code generation?
│   └── YES → Ensure strict typing in spec
└── OpenAPI 3.1 recommended (JSON Schema)
```

**If Missing:**
| Context | Skill/Methodology |
|---------|-------------------|
| Endpoint design | api-rest-design.md |
| Data schemas | faion-ba-modeling → data-analysis |

---

### websocket-design.md

**Required Context:**
- [ ] Real-time use case defined
- [ ] Message types/events
- [ ] Connection lifecycle
- [ ] Scale requirements (connections count)

**Decision Tree:**
```
Start
├── Need bidirectional?
│   └── NO → Consider SSE instead
├── High frequency updates?
│   └── YES → WebSocket with batching
├── Many concurrent connections?
│   └── YES → Consider dedicated WS server
└── Define: connect, message, disconnect flows
```

**If Missing:**
| Context | Skill/Methodology |
|---------|-------------------|
| Real-time requirements | faion-ba-core → requirements-analysis |
| Scale architecture | faion-software-architect → distributed-patterns |
| Infrastructure | faion-devops-engineer → infrastructure |

---

### api-gateway-patterns.md

**Required Context:**
- [ ] Number of backend services
- [ ] Client types (web, mobile, IoT)
- [ ] Cross-cutting concerns (auth, rate limit, logging)
- [ ] Traffic patterns

**Decision Tree:**
```
Start
├── Single backend service?
│   └── NO → Consider API gateway
├── Multiple client types with different needs?
│   └── YES → BFF pattern (Backend for Frontend)
├── Need aggregation across services?
│   └── YES → Gateway with composition
└── Cross-cutting: auth, rate limiting, caching
```

**If Missing:**
| Context | Skill/Methodology |
|---------|-------------------|
| Service architecture | faion-software-architect → microservices-architecture |
| Client requirements | faion-frontend-developer, faion-product-manager |

---

### api-testing.md

**Required Context:**
- [ ] API contracts defined
- [ ] Test data strategy
- [ ] CI/CD integration needs
- [ ] Contract testing requirements

**Decision Tree:**
```
Start
├── Contract testing needed?
│   └── YES → Use Pact or similar
├── Integration tests?
│   └── YES → Test against real/mock server
├── Performance testing?
│   └── YES → Load testing with k6, Artillery
└── Minimum: contract + integration tests
```

**If Missing:**
| Context | Skill/Methodology |
|---------|-------------------|
| API contracts | api-openapi-spec.md |
| Testing strategy | faion-testing-developer → integration-testing |
| CI/CD | faion-cicd-engineer → ci-cd-pipelines |

---

### api-monitoring.md

**Required Context:**
- [ ] SLOs defined (latency, availability)
- [ ] Alerting requirements
- [ ] Tracing needs
- [ ] Log aggregation setup

**Decision Tree:**
```
Start
├── SLOs defined?
│   └── NO → Define first (faion-software-architect)
├── Distributed system?
│   └── YES → Need distributed tracing
├── Need business metrics?
│   └── YES → Custom metrics + dashboards
└── Minimum: latency, errors, throughput (RED)
```

**If Missing:**
| Context | Skill/Methodology |
|---------|-------------------|
| SLOs | faion-software-architect → quality-attributes |
| Observability | faion-software-architect → observability-architecture |
| Alerting | faion-cicd-engineer → monitoring-alerting |

---

*faion-api-developer v1.1 | 19 methodologies | Context-aware*
