---
name: api-designer
description: Design RESTful APIs with best practices for consistency and usability
---

# API Designer

Expert guidance for designing clean, consistent REST APIs.

## REST Principles
- Use nouns for resources, verbs for actions
- Follow HTTP method semantics (GET, POST, PUT, DELETE)
- Return appropriate status codes
- Support content negotiation

## URL Design
- Use plural nouns for collections (/users, /posts)
- Nest resources logically (/users/123/posts)
- Use query parameters for filtering and pagination
- Keep URLs readable and predictable

## Response Format
- Use consistent JSON structure
- Include metadata for collections (total, page, etc.)
- Provide helpful error messages
- Support partial responses when needed

## Versioning
- Include version in URL or header
- Maintain backward compatibility
- Document breaking changes clearly
- Deprecate gracefully with notice periods

## Security
- Use HTTPS everywhere
- Implement proper authentication
- Validate all inputs
- Rate limit API endpoints
- Log security-relevant events

## Documentation
- Provide OpenAPI/Swagger specs
- Include request/response examples
- Document error codes and meanings
- Keep docs updated with changes
