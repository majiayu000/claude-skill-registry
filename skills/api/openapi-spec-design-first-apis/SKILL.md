---
name: openapi-spec-design-first-apis
version: "0.1"
description: >
  [STUB - Not implemented] OpenAPI 3.1.0 design-first API specifications as single source of truth.
  PROACTIVELY activate for: [TODO: Define on implementation].
  Triggers: [TODO: Define on implementation]
core-integration:
  techniques:
    primary: ["[TODO]"]
    secondary: []
  contracts:
    input: "[TODO]"
    output: "[TODO]"
  patterns: "[TODO]"
  rubrics: "[TODO]"
---

# OpenAPI Spec Design-First APIs

> **STUB: This skill is not yet implemented**
>
> This placeholder preserves the documented plugin structure.
> See parent plugin README for planned capabilities.

## Planned Capabilities

- **Design-First Approach**: API specification before implementation
- **OpenAPI 3.1.0 Compliance**: Latest specification features
- Schema component reuse and references
- Request/response examples
- Authentication scheme definitions
- API versioning strategies

## Example Structure

```yaml
openapi: 3.1.0
info:
  title: User API
  version: 1.0.0
paths:
  /users:
    get:
      summary: List users
      responses:
        '200':
          description: Success
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/User'
```

## Anti-Patterns

- API implementation before specification
- Inconsistent error response formats
- Missing authentication documentation

## Implementation Status

- [ ] Core implementation
- [ ] References documentation
- [ ] Output templates
- [ ] Integration tests
