---
name: rest-api-design
description: "Define RESTful API behavior, HTTP methods, status codes, and endpoint conventions. This skill should be used when designing new API endpoints, establishing HTTP method conventions (GET, POST, PUT, DELETE), defining response status codes and error formats, creating API contract documentation, reviewing existing endpoints for REST compliance, and planning resource naming and URL structure."
---

# REST API Design

## Purpose
Define RESTful API behavior, HTTP methods, status codes, and endpoint conventions. This skill ensures consistent, standards-compliant API design that follows REST principles and provides predictable, well-documented interfaces for frontend consumption.

## When to Use
- When designing new API endpoints
- When establishing HTTP method conventions (GET, POST, PUT, DELETE)
- When defining response status codes and error formats
- When creating API contract documentation
- When reviewing existing endpoints for REST compliance
- When planning resource naming and URL structure

## When NOT to Use
- When working on frontend implementation
- When designing internal service-to-service communication
- When the API style has been decided as non-REST (GraphQL, gRPC)
- When implementing endpoint logic (use fastapi-architecture)
- When specifications haven't defined the API requirements

## Required Clarifications
1. What are the specific resource types and entities for the API?
2. What are the authentication and authorization requirements?
3. What are the performance and scalability requirements?
4. What are the versioning requirements for the API?

## Optional Clarifications
5. Are there existing API design patterns to follow in the codebase?
6. Are there specific error handling requirements?
7. What are the pagination and filtering needs?

## Responsibilities
- Define resource naming conventions (plural nouns, lowercase)
- Establish HTTP method semantics for CRUD operations
- Document standard response status codes
- Design error response format and error codes
- Plan pagination patterns for list endpoints
- Define query parameter conventions
- Establish request/response body structures
- Create API versioning strategy if needed

## Inputs
- Feature specifications with API requirements
- Data model definitions
- Authentication requirements
- Frontend consumption patterns
- Performance requirements
- Existing API conventions (if any)

## Outputs
- Endpoint URL patterns
- HTTP method assignments
- Status code mappings
- Error response schema
- Request/response body schemas
- API contract documentation (OpenAPI/Swagger)
- Pagination and filtering patterns

## Before Implementation

Gather context to ensure successful implementation:

| Source | Gather |
|--------|--------|
| **Codebase** | Existing structure, patterns, conventions to integrate with |
| **Conversation** | User's specific requirements, constraints, preferences |
| **Skill References** | Domain patterns from `references/` (REST standards, best practices, examples) |
| **User Guidelines** | Project-specific conventions, team standards |

Ensure all required context is gathered before implementing.
Only ask user for THEIR specific requirements (domain expertise is in this skill).

## Implementation Workflow
1. Assess API design requirements and resource types
2. Define resource naming conventions
3. Establish HTTP method semantics for CRUD operations
4. Document standard response status codes
5. Design error response format and error codes
6. Plan pagination patterns for list endpoints
7. Define query parameter conventions
8. Establish request/response body structures
9. Create API versioning strategy if needed
10. Validate against constraints and anti-patterns

## Output Checklist
- [ ] Endpoint URL patterns defined
- [ ] HTTP method assignments established
- [ ] Status code mappings documented
- [ ] Error response schema designed
- [ ] Request/response body schemas created
- [ ] API contract documentation created
- [ ] Pagination and filtering patterns defined
- [ ] Constraints respected

## Constraints
- Never use verbs in resource URLs (use nouns)
- Never return 200 OK for error conditions
- Never expose internal IDs or implementation details inappropriately
- Never ignore HTTP method semantics (GET must be safe and idempotent)
- Always use appropriate status codes (201 for creation, 204 for no content)
- Always provide consistent error response format
- Always document all endpoints in contracts

## Interaction With Other Skills
- **fastapi-architecture:** Implements REST conventions in FastAPI structure
- **api-client-design:** Consumes REST patterns for frontend API clients
- **spec-writing:** Incorporates REST conventions into specifications
- **jwt-authentication:** Coordinates with auth headers and 401/403 responses
- **relational-data-modeling:** Aligns resources with data model entities

## Anti-Patterns
- **Verb pollution:** Using verbs in URLs like /getUsers or /createTask
- **Status code abuse:** Using 200 for everything including errors
- **Inconsistent naming:** Mixing /user and /tasks (singular vs plural)
- **Over-nesting:** Deep URL hierarchies like /users/1/tasks/2/comments/3/replies
- **Method misuse:** Using POST for retrieval or GET for mutations
- **Missing pagination:** List endpoints without pagination support
- **Undocumented errors:** Error responses without clear codes or messages

## Security Best Practices
- Use HTTPS for all API endpoints
- Implement proper authentication and authorization
- Validate and sanitize all input parameters
- Implement rate limiting to prevent abuse
- Use proper CORS configuration
- Sanitize output to prevent information disclosure
- Implement proper error handling without exposing system details

## Documentation Resources
- [REST API Tutorial](https://restfulapi.net/)
- [HTTP Status Codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status)
- [OpenAPI Specification](https://spec.openapis.org/oas/v3.0.3)
- [JSON:API Specification](https://jsonapi.org/format/)
- [REST Best Practices](https://www.vinaysahni.com/best-practices-for-a-pragmatic-restful-api)

## Phase Applicability
Phase II only. Phase I uses console interface without HTTP API.