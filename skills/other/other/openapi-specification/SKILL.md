---
name: openapi-specification
description: OpenAPI 3.x specification design, schema patterns, and validation for REST API contracts. Use when creating or maintaining API specifications, generating documentation, or validating API contracts.
tags: [openapi, swagger, api, documentation, rest]
triggers:
  - openapi spec
  - swagger definition
  - api contract
  - api specification
  - oas design
---

# OpenAPI Specification

Design, validate, and maintain OpenAPI 3.x specifications for REST API contracts.
Covers schema patterns, security schemes, versioning, and code generation integration.

## When to Use This Skill

- Creating a new OpenAPI specification from scratch
- Adding endpoints or schemas to an existing spec
- Reviewing or validating an API contract for correctness
- Setting up code generation from OpenAPI definitions
- Designing reusable schema components for large APIs
- Implementing security schemes in API specifications
- Managing API versioning and deprecation

## Quick Reference

| Resource | Purpose | Load when |
|----------|---------|-----------|
| `references/spec-patterns.md` | Schema patterns, security schemes, validation, versioning, reusable components | Designing or reviewing specs |

---

## Workflow

```
Phase 1: Design       → Define API overview, resources, and operations
Phase 2: Schema       → Build data models with reusable components
Phase 3: Validate     → Lint and verify the spec for correctness
Phase 4: Integrate    → Generate docs, SDKs, and contract tests
```

---

## Phase 1: API Design

Start with a high-level design before writing the spec:

1. **Identify resources** -- what nouns does this API expose?
2. **Map operations** -- what CRUD and custom actions apply to each resource?
3. **Define relationships** -- how do resources reference each other?
4. **Plan authentication** -- what security schemes are needed?
5. **Set conventions** -- naming style, pagination, error format

### Spec Skeleton

```yaml
openapi: 3.1.0
info:
  title: [API Name]
  version: 1.0.0
  description: [What this API does]
paths:
  /resources:
    get:
      summary: List resources
      operationId: listResources
    post:
      summary: Create a resource
      operationId: createResource
  /resources/{id}:
    get:
      summary: Get a resource
      operationId: getResource
components:
  schemas: {}
  securitySchemes: {}
```

---

## Phase 2: Schema Design

Build data models using `components/schemas` for reuse:

- Use `$ref` to reference shared schemas -- never duplicate definitions
- Apply `allOf` for composition, `oneOf` / `anyOf` for polymorphism
- Add `example` values to every schema and property
- Use `required` arrays explicitly -- don't rely on implicit behavior
- Document nullable fields with `type: [string, "null"]` (3.1) or `nullable: true` (3.0)

---

## Phase 3: Validate

Run validation before committing any spec changes:

```bash
# Spectral (recommended)
spectral lint openapi.yaml

# Redocly
redocly lint openapi.yaml

# swagger-cli
swagger-cli validate openapi.yaml
```

### Common Validation Issues

| Issue | Fix |
|-------|-----|
| Missing `operationId` | Add unique operationId to every operation |
| Unused schema | Remove from components or add a `$ref` |
| Missing response `description` | Add description to every response code |
| Path parameter not in path | Match `{param}` in path with parameter definition |
| No `2xx` response defined | Add at least one success response per operation |

---

## Phase 4: Integrate

Use the validated spec to generate downstream artifacts:

- **Documentation**: Redoc, Swagger UI, Stoplight
- **Client SDKs**: openapi-generator, autorest, orval
- **Server stubs**: openapi-generator with server templates
- **Contract tests**: Schemathesis, Dredd, Prism

---

## Quality Checklist

- [ ] All paths have operationIds
- [ ] HTTP methods match resource actions (GET reads, POST creates, etc.)
- [ ] Every response has a description and schema
- [ ] Security requirements defined at operation or global level
- [ ] Examples provided for request and response bodies
- [ ] Consistent naming conventions (camelCase, snake_case -- pick one)
- [ ] Deprecation fields set on sunset endpoints
- [ ] Spec passes linter with zero errors

---

## Anti-Patterns

- Do not inline schemas -- use `$ref` to `components/schemas` for anything reused
- Do not mix API versions in a single spec file
- Do not use `200 OK` for create operations -- use `201 Created`
- Do not omit error response schemas -- document `4xx` and `5xx` consistently
- Do not use `additionalProperties: true` without clear justification
