---
name: using-web-backend
description: Use when building web APIs, backend services, or encountering FastAPI/Django/Express/GraphQL questions, microservices architecture, authentication, or message queues - routes to 11 specialist skills rather than giving surface-level generic advice
---

# Using Web Backend Skills

## Overview

**This router directs you to specialized web backend skills. Each specialist provides deep expertise in their domain.**

**Core principle:** Different backend challenges require different specialist knowledge. Routing to the right skill gives better results than generic advice.

## When to Use

Use this router when encountering:

- **Framework-specific questions**: FastAPI, Django, Express implementation details
- **API design**: REST or GraphQL architecture, versioning, schema design
- **Architecture patterns**: Microservices, message queues, event-driven systems
- **Backend infrastructure**: Authentication, database integration, deployment
- **Testing & documentation**: API testing strategies, documentation approaches

## How to Access Reference Sheets

**IMPORTANT**: All reference sheets are located in the SAME DIRECTORY as this SKILL.md file.

When this skill is loaded from:
  `skills/using-web-backend/SKILL.md`

Reference sheets like `fastapi-development.md` are at:
  `skills/using-web-backend/fastapi-development.md`

NOT at:
  `skills/fastapi-development.md` ← WRONG PATH

When you see a link like `[fastapi-development.md](fastapi-development.md)`, read the file from the same directory as this SKILL.md.

---

## Quick Reference - Routing Table

| User Question Contains | Route To | Why |
|------------------------|----------|-----|
| FastAPI, Pydantic, async Python APIs | [fastapi-development.md](fastapi-development.md) | FastAPI-specific patterns, dependency injection, async |
| Django, ORM, views, middleware | [django-development.md](django-development.md) | Django conventions, ORM optimization, settings |
| Express, Node.js backend, middleware | [express-development.md](express-development.md) | Express patterns, error handling, async flow |
| REST API, endpoints, versioning, pagination | [rest-api-design.md](rest-api-design.md) | REST principles, resource design, hypermedia |
| GraphQL, schema, resolvers, N+1 | [graphql-api-design.md](graphql-api-design.md) | Schema design, query optimization, federation |
| Microservices, service mesh, boundaries | [microservices-architecture.md](microservices-architecture.md) | Service design, communication, consistency |
| Message queues, RabbitMQ, Kafka, events | [message-queues.md](message-queues.md) | Queue patterns, reliability, event-driven |
| JWT, OAuth2, API keys, auth | [api-authentication.md](api-authentication.md) | Auth patterns, token management, security |
| Database connections, ORM, migrations | [database-integration.md](database-integration.md) | Connection pooling, query optimization, migrations |
| API testing, integration tests, mocking | [api-testing.md](api-testing.md) | Testing strategies, contract testing, mocking |
| OpenAPI, Swagger, API docs | [api-documentation.md](api-documentation.md) | API docs (also see: muna-technical-writer) |

## Cross-References to Other Packs

**Before routing, check if these packs are more appropriate:**

- **Security concerns** → `ordis-security-architect` (threat modeling, OWASP, security patterns)
- **API usability/UX** → `lyra-ux-designer` (error messages, API ergonomics)
- **Python code patterns** → `axiom-python-engineering` (Python-specific engineering)
- **Documentation writing** → `muna-technical-writer` (technical writing, clarity)

## How to Route

**STOP: Do not attempt to answer web backend questions yourself.**

**Instead:**

1. **Identify the specialist domain** from the routing table above
2. **State which specialist skill you're using**: "I'll use the `[skill-name]` skill for this"
3. **Apply the specialist skill** to provide deep, expert guidance

## Red Flags - Using Generic Knowledge Instead of Specialists

If you catch yourself doing any of these, STOP and route to a specialist:

- ❌ "I'll answer all these diverse backend questions myself"
- ❌ Giving code examples from "general backend knowledge"
- ❌ Providing "competent but broad" answers across multiple domains
- ❌ Not mentioning specialized skills would give better guidance
- ❌ "The specialist skill isn't available right now, so I'll answer myself"

**All of these mean: You're being a jack-of-all-trades. Route to the specialist.**

## Rationalization Table

| Excuse | Reality |
|--------|---------|
| "I can handle this backend question myself" | Specialists provide deeper expertise than generic knowledge |
| "These are all backend topics" | Backend spans 11 distinct specialist domains |
| "I'll just give a quick answer" | Quick answers miss edge cases and production patterns |
| "The user didn't ask for specialized help" | Better results come from routing to specialists proactively |
| "Specialist skill not available, I'll answer instead" | State which skill would help, explain routing, guide user to install if needed |

## Example Routing

**User**: "I need to build a REST API with FastAPI. How should I structure my dependency injection?"

**Your response**:
"I'll use the [fastapi-development.md](fastapi-development.md) skill to help you structure dependency injection properly. This specialist skill covers FastAPI patterns in depth."

[Then apply fastapi-development skill]

**User**: "My GraphQL API has N+1 problems and we're splitting our monolith into microservices."

**Your response**:
"You have two distinct specialist areas:
1. GraphQL optimization → I'll use [graphql-api-design.md](graphql-api-design.md)
2. Microservices architecture → I'll use [microservices-architecture.md](microservices-architecture.md)

Let me address the GraphQL N+1 problem first with the graphql-api-design skill..."

[Apply each specialist skill to its domain]

## Why This Matters

**Without routing**: Surface-level answers covering multiple domains broadly
**With routing**: Deep expertise addressing edge cases, production patterns, and domain-specific best practices

Specialist skills = better results.

---

## Web Backend Specialist Skills Catalog

After routing, load the appropriate specialist skill for detailed guidance:

### Framework-Specific Skills

1. [fastapi-development.md](fastapi-development.md) - FastAPI patterns, dependency injection, async/await, Pydantic validation, background tasks
2. [django-development.md](django-development.md) - Django conventions, ORM optimization, middleware, settings, management commands
3. [express-development.md](express-development.md) - Express patterns, middleware chains, error handling, async flow control

### API Design Skills

4. [rest-api-design.md](rest-api-design.md) - REST principles, resource design, versioning, pagination, HATEOAS, HTTP semantics
5. [graphql-api-design.md](graphql-api-design.md) - GraphQL schema design, resolver patterns, N+1 query optimization, federation

### Architecture & Infrastructure

6. [microservices-architecture.md](microservices-architecture.md) - Service boundaries, communication patterns, distributed consistency, service mesh
7. [message-queues.md](message-queues.md) - Queue patterns, reliability guarantees, event-driven architecture, RabbitMQ/Kafka

### Cross-Cutting Concerns

8. [api-authentication.md](api-authentication.md) - JWT, OAuth2, API keys, token management, auth patterns
9. [database-integration.md](database-integration.md) - Connection pooling, query optimization, migrations, ORM patterns
10. [api-testing.md](api-testing.md) - Testing strategies, contract testing, integration tests, mocking
11. [api-documentation.md](api-documentation.md) - OpenAPI/Swagger, API documentation patterns, schema generation
