---
name: api-documentation
description: Guide writing clear, comprehensive API documentation that helps developers integrate
category: Communication Writing
---

# Skill: api-documentation

## What I do

I guide the creation of clear, developer-centric API documentation. I focus on technical accuracy, intuitive structure, and practical examples to ensure developers can integrate with services quickly and reliably.

## When to use me

- Writing OpenAPI (Swagger) or GraphQL schema documentation
- Creating developer portals, SDK guides, or integration tutorials
- Documenting authentication flows, error codes, and rate limits
- Writing API changelogs and migration guides for breaking changes

## Core principles

1.  **Technical Accuracy** — Every parameter, type, and endpoint must match the actual implementation exactly.
2.  **Context Before Mechanics** — Explain what an endpoint achieves and why to use it before detailing its parameters.
3.  **Consistency** — Use the same terminology, formatting, and data structures across all documented endpoints.
4.  **Clarity Through Examples** — Provide realistic request and response samples for every endpoint.
5.  **Standardised Errors** — Document every possible error code and the specific conditions that trigger them.

## Patterns & examples

### Endpoint Documentation Template
Every endpoint should follow a consistent structure:
- **Summary**: Concise one-line description of the action.
- **Description**: Detailed context, requirements, and side effects.
- **Authentication**: Required scopes, tokens, or headers.
- **Parameters**: Detailed table with types, constraints, and descriptions.
- **Request Body**: JSON example with realistic data.
- **Responses**: Success and error codes with examples.

### Example Request/Response
```http
POST /v1/users/register
Content-Type: application/json

{
  "email": "dev@example.com",
  "full_name": "Dev User"
}
```

## Anti-patterns to avoid

-   ❌ **Auto-generated fluff** — Relying purely on tools without adding descriptive context and use cases.
-   ❌ **Missing error states** — Documenting only the 200 OK response and leaving failures to guesswork.
-   ❌ **Stale examples** — Using field names or data structures that have been deprecated or removed.
-   ❌ **Internal jargon** — Using terms that only internal developers understand without explanation.

## KB Reference

`~/vaults/baphled/3. Resources/Knowledge Base/AI Development System/Skills/Communication-Writing/API Documentation.md`

## Related skills

-   `api-design` — Align documentation with API design best practices.
-   `documentation-writing` — Apply general technical writing standards.
-   `writing-style` — Maintain a professional and consistent voice.
-   `release-notes` — Document API changes and updates for consumers.
