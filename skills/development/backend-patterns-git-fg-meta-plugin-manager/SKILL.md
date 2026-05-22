---
name: backend-patterns
description: "Apply backend patterns for server architecture, database interactions, and API structure. Use when designing backend systems. Not for frontend logic or simple scripts."
---

# Backend Patterns

<mission_control>
<objective>Apply backend architecture patterns for server design, database interactions, and API structure</objective>
<success_criteria>Backend system follows established patterns for scalability, maintainability, and security</success_criteria>
</mission_control>

<trigger>When designing server architecture, database interactions, or API structure. Not for: Frontend logic or simple scripts.</trigger>

<interaction_schema>
ANALYZE REQUIREMENTS → SELECT PATTERN → IMPLEMENT → VALIDATE
</interaction_schema>

Backend patterns for server architecture, database interactions, and API design.

## Core Concept

Backend patterns provide proven solutions for common architectural challenges:

- **Server architecture**: MVC, Layered architecture, Hexagonal (when justified)
- **Database interactions**: Repository pattern, Unit of Work, Data Mapper
- **API structure**: REST, GraphQL, RPC (select based on requirements)
- **Security**: Authentication, authorization, input validation, output sanitization

## Pattern Selection Matrix

| Requirement            | Recommended Pattern     | When to Use                                   |
| ---------------------- | ----------------------- | --------------------------------------------- |
| Simple CRUD API        | REST + MVC              | Standard web applications                     |
| Complex business logic | Layered architecture    | Domain complexity requires isolation          |
| Database abstraction   | Repository pattern      | Need testable data access layer               |
| Real-time features     | WebSocket + Events      | Live updates, notifications                   |
| High scalability       | Microservices (justify) | CLEAR team boundaries, independent deployment |

## Best Practices

- Prefer simplicity over enterprise patterns when justified
- Use repository pattern for testable database interactions
- Implement proper error handling and logging
- Validate all input and sanitize all output
- Use environment variables for configuration
- Implement proper authentication and authorization
- Design APIs with clear versioning strategy
- Use appropriate HTTP status codes
- Implement rate limiting for public APIs

---

## Dynamic Sourcing Protocol

<fetch_protocol>
**MANDATORY FETCH**: Before designing REST APIs, fetch the content from:

- https://restfulapi.net/ (REST principles and constraints)
- https://developer.mozilla.org/en-US/docs/Web/HTTP/Status (HTTP status codes)

**CONDITIONAL FETCH**: Fetch https://swagger.io/docs/specification/ only when documenting APIs with OpenAPI.

The local skill focuses on Seed System-specific backend patterns.
</fetch_protocol>

---

## Navigation

**Official Documentation**:

- REST API standards → https://restfulapi.net/
- HTTP status codes → https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
- OpenAPI specification → https://swagger.io/docs/specification/

**Local References**:

| If you need...            | Read...                         |
| ------------------------- | ------------------------------- |
| Seed System REST patterns | references/api-patterns.md      |
| Database patterns         | references/database-patterns.md |
| Security patterns         | references/security-patterns.md |

---

## Absolute Constraints

<critical_constraint>
MANDATORY: Validate all input at API boundaries
MANDATORY: Sanitize all output to prevent injection attacks
MANDATORY: Use repository pattern for database access (not inline queries)
MANDATORY: Implement proper error handling with appropriate status codes
MANDATORY: Use environment variables for sensitive configuration (never hardcode secrets)
MANDATORY: Implement rate limiting for public APIs

NEVER expose database errors directly to clients
NEVER trust client-side validation (server-side validation is mandatory)
NEVER hardcode secrets or credentials in code

Choose patterns based on actual requirements, not theoretical future needs. Start simple, add complexity only when justified.
</critical_constraint>

---

## Genetic Code

This component carries essential Seed System principles for context: fork isolation:

<critical_constraint>
MANDATORY: All components MUST be self-contained (zero .claude/rules dependency)
MANDATORY: Achieve 80-95% autonomy (0-5 AskUserQuestion rounds per session)
MANDATORY: Description MUST use What-When-Not format in third person
MANDATORY: No component references another component by name in description
MANDATORY: Progressive disclosure - references/ for detailed content
MANDATORY: Use XML for control (mission_control, critical_constraint), Markdown for data
No exceptions. Portability invariant must be maintained.
</critical_constraint>

**Delta Standard**: Good Component = Expert Knowledge − What Claude Already Knows

**Recognition Questions**:

- "Would Claude know this without being told?" → Delete (zero delta)
- "Can this work standalone?" → Fix if no (non-self-sufficient)
- "Did I read the actual file, or just see it in grep?" → Verify before claiming

---
