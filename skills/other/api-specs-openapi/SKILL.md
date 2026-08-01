---
name: api-specs-openapi
description: OpenAPI 3.1 specification, schema design, code generation
---

# OpenAPI Specification Patterns

> **Quick Guide:** Use OpenAPI 3.1 for API contracts. 3.1 is a superset of JSON Schema Draft 2020-12 -- use `type: ["string", "null"]` instead of `nullable: true`. Define all reusable schemas in `components/schemas` and reference with `$ref`. Always include `operationId` on every operation (it becomes the client method name). Use `openapi-typescript` to generate zero-runtime TypeScript types and `openapi-fetch` for a 6kb type-safe fetch client.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST use OpenAPI 3.1 syntax -- `type: ["string", "null"]` NOT the 3.0 `nullable: true` keyword)**

**(You MUST define reusable schemas in `components/schemas` and reference with `$ref` -- NO inline schema duplication)**

**(You MUST include `operationId` on every path operation -- it becomes the generated client method name)**

**(You MUST use `openapi-typescript` for type generation and import types with `import type` -- types are zero-runtime)**

</critical_requirements>

---

**Auto-detection:** OpenAPI, openapi, swagger, openapi-typescript, openapi-fetch, createClient, paths, components, schemas, operationId, $ref, discriminator, oneOf, allOf, anyOf, openapi: "3.1", spec-first, API contract, API specification, code generation, schema design

**When to use:**

- Defining API contracts before or alongside implementation (spec-first or code-first)
- Generating TypeScript types from an existing OpenAPI spec
- Building type-safe API clients with automatic request/response validation
- Documenting REST APIs for external or internal consumers
- Designing reusable schema components with `$ref` composition

**When NOT to use:**

- Internal-only endpoints with no external consumers and no documentation needs
- GraphQL APIs (use GraphQL schema tooling instead)
- Simple scripts or prototypes where formal contracts add overhead

**Key patterns covered:**

- OpenAPI 3.1 spec structure (info, paths, components, servers)
- Schema design with JSON Schema Draft 2020-12 alignment
- `$ref` composition, `oneOf`/`allOf`/`anyOf`, discriminators
- Path operations with parameters, request bodies, and responses
- TypeScript type generation with `openapi-typescript` v7
- Type-safe fetch client with `openapi-fetch`
- Spec-first vs code-first decision framework

**Detailed Resources:**

- [examples/core.md](examples/core.md) - Spec structure, schemas, paths, operations, `$ref` composition
- [examples/codegen.md](examples/codegen.md) - TypeScript type generation, `openapi-fetch` client
- [examples/validation.md](examples/validation.md) - Request/response validation, middleware patterns
- [reference.md](reference.md) - Decision frameworks, anti-patterns, quick-lookup tables

---

<philosophy>

## Philosophy

**The spec IS the contract.** An OpenAPI document is the single source of truth for your API's shape. Types, documentation, client SDKs, and server validation are all derived from it -- never maintained separately.

**OpenAPI 3.1 aligns with JSON Schema Draft 2020-12.** This means any valid JSON Schema is a valid OpenAPI schema. Use `type` arrays for nullable (`["string", "null"]`), `if/then/else` for conditional schemas, and standard JSON Schema vocabulary.

**Spec-first (design-first) is recommended** for stable, multi-consumer APIs. Define the contract first, get feedback from consumers via mocks, then implement. Code-first works for rapid prototypes where the spec is generated from annotations.

**Use spec-first when:**

- Multiple teams consume the API
- API is public or has external consumers
- Contract stability matters (breaking changes are expensive)
- You want mocks and docs before writing any code

**Use code-first when:**

- Rapid prototyping where the spec is generated from code annotations
- Single-team internal APIs where the implementation IS the contract
- Framework provides first-class OpenAPI generation from code annotations

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Spec Structure

Every OpenAPI 3.1 document has four required top-level fields: `openapi`, `info`, `paths` (or `webhooks`), and implicitly `components` for reusable schemas.

```yaml
openapi: "3.1.0"
info:
  title: Jobs API
  version: "1.0.0"
  description: Job listings and applications
servers:
  - url: https://api.example.com/v1
paths:
  /jobs:
    get:
      operationId: listJobs
      # ...
components:
  schemas:
    Job:
      # ...
```

**Why good:** `operationId` becomes the client method name, `servers` enables environment switching, schemas in `components` are reusable via `$ref`

See [examples/core.md](examples/core.md) for complete spec with paths, parameters, and responses.

---

### Pattern 2: Schema Design with 3.1 Syntax

OpenAPI 3.1 uses JSON Schema Draft 2020-12. Key differences from 3.0: `nullable` is removed, use `type` arrays instead. `exclusiveMinimum`/`exclusiveMaximum` are numbers, not booleans.

```yaml
# 3.1 nullable syntax
type: ["string", "null"]

# NOT 3.0 syntax:
# type: string
# nullable: true
```

```yaml
components:
  schemas:
    Salary:
      type: object
      required: [min, max, currency]
      properties:
        min:
          type: integer
          minimum: 0
        max:
          type: integer
          minimum: 0
        currency:
          type: string
          minLength: 3
          maxLength: 3
          description: ISO 4217 currency code
```

**Why good:** aligns with standard JSON Schema, tooling ecosystem understands it natively, `required` array is explicit

See [examples/core.md](examples/core.md) for enum, format, and composition examples.

---

### Pattern 3: $ref Composition and Reuse

Define schemas once in `components/schemas`, reference everywhere with `$ref`. Use `allOf` to extend base schemas, `oneOf` for polymorphism with discriminators.

```yaml
components:
  schemas:
    PaginatedResponse:
      type: object
      required: [data, pagination]
      properties:
        pagination:
          $ref: "#/components/schemas/Pagination"

    JobListResponse:
      allOf:
        - $ref: "#/components/schemas/PaginatedResponse"
        - type: object
          properties:
            data:
              type: array
              items:
                $ref: "#/components/schemas/Job"
```

**Why good:** single source of truth, changes propagate automatically, generated types reflect composition

See [examples/core.md](examples/core.md) for `oneOf` with discriminator and `allOf` extension patterns.

---

### Pattern 4: Path Operations

Operations define HTTP methods on paths. Always include `operationId`, `tags`, parameter schemas, and all response codes.

```yaml
paths:
  /jobs/{jobId}:
    get:
      operationId: getJob
      tags: [Jobs]
      parameters:
        - name: jobId
          in: path
          required: true
          schema:
            type: string
            format: uuid
      responses:
        "200":
          description: Job details
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Job"
        "404":
          description: Job not found
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Error"
```

**Why good:** `operationId` drives codegen method names, explicit `404` response documents error cases, `format: uuid` aids validation

See [examples/core.md](examples/core.md) for query parameters, request bodies, and pagination.

---

### Pattern 5: TypeScript Type Generation

Use `openapi-typescript` v7 to generate zero-runtime types from your spec. Types are generated as `.d.ts` files and imported with `import type`.

```bash
npx openapi-typescript ./api/openapi.yaml -o ./api/schema.d.ts
```

```typescript
import type { paths, components } from "./api/schema.d.ts";

// Access schema types
type Job = components["schemas"]["Job"];
type Error = components["schemas"]["Error"];

// Access response types
type JobListResponse =
  paths["/jobs"]["get"]["responses"]["200"]["content"]["application/json"];
```

**Why good:** zero runtime cost, types stay in sync with spec, no manual interface maintenance

See [examples/codegen.md](examples/codegen.md) for CLI options, `redocly.yaml` multi-schema config, and programmatic API.

---

### Pattern 6: Type-Safe Fetch Client

Use `openapi-fetch` (6kb) for a type-safe client that infers request/response types from generated types. No codegen needed beyond the types.

```typescript
import createClient from "openapi-fetch";
import type { paths } from "./api/schema.d.ts";

const client = createClient<paths>({ baseUrl: "https://api.example.com/v1" });

// Fully typed -- path params, query, body, response
const { data, error } = await client.GET("/jobs/{jobId}", {
  params: { path: { jobId: "abc-123" } },
});

if (error) {
  // error is typed to the spec's error response schema
  console.error(error);
  return;
}
// data is typed to the spec's 200 response schema
console.log(data.title);
```

**Why good:** 6kb with virtually zero runtime, no manual generics, path/query/body/response all type-checked against the spec

See [examples/codegen.md](examples/codegen.md) for middleware, auth headers, and error handling.

</patterns>

---

<decision_framework>

## Decision Framework

### Spec-First vs Code-First

```
Is this a public or multi-consumer API?
|-- YES --> Spec-first (design contract, get feedback, then implement)
+-- NO  --> Is this a rapid prototype?
    |-- YES --> Code-first (generate spec from annotations)
    +-- NO  --> Does your framework generate OpenAPI from code?
        |-- YES --> Code-first (framework handles spec generation)
        +-- NO  --> Spec-first (write the YAML, generate types)
```

### Schema Composition

```
Need to share fields across schemas?
|-- YES --> allOf with a base $ref schema
+-- NO  --> Need polymorphism (multiple possible shapes)?
    |-- YES --> oneOf with discriminator
    +-- NO  --> Need to combine constraints?
        |-- YES --> allOf (all must match)
        +-- NO  --> Simple schema with $ref for nested objects
```

### Type Generation Tooling

| Need                       | Tool                    | When                                        |
| -------------------------- | ----------------------- | ------------------------------------------- |
| TypeScript types from spec | `openapi-typescript` v7 | Always -- zero-runtime type generation      |
| Type-safe fetch client     | `openapi-fetch`         | Frontend or service-to-service calls        |
| Full SDK generation        | `@hey-api/openapi-ts`   | Need Zod schemas, query hooks, or full SDKs |
| Spec validation/linting    | Redocly CLI             | CI pipeline, pre-commit checks              |

</decision_framework>

---

<red_flags>

## RED FLAGS

**High Priority:**

- Using `nullable: true` -- removed in OpenAPI 3.1, use `type: ["string", "null"]`
- Duplicating schemas inline instead of using `$ref` to `components/schemas` -- creates drift
- Missing `operationId` on operations -- generated clients get ugly auto-generated names
- Manually maintaining TypeScript interfaces that mirror the spec -- use `openapi-typescript` to generate them
- Using `openapi: "3.0.x"` when 3.1 is available -- misses JSON Schema alignment

**Medium Priority:**

- Defining error responses without a shared `Error` schema -- inconsistent error shapes across endpoints
- Missing `required` array on object schemas -- all properties become optional by default
- Using `type: object` without `additionalProperties: false` when extra fields should be rejected
- Not documenting `4xx`/`5xx` responses -- consumers don't know what error shapes to expect

**Gotchas & Edge Cases:**

- `$ref` siblings are ignored in 3.0 but allowed in 3.1 -- `description` next to `$ref` now works in 3.1
- `exclusiveMinimum`/`exclusiveMaximum` changed from boolean (3.0) to number (3.1) -- `exclusiveMinimum: 0` means "greater than 0"
- `discriminator` does not affect validation -- it's a hint for code generators, not a constraint
- `discriminator.propertyName` must be a required string property at the same schema level
- Inline schemas inside `discriminator` `oneOf` are not considered -- only `$ref` entries work
- `openapi-typescript` generates `.d.ts` files -- these are type-only, no runtime code
- `openapi-fetch` `data` is only present for 2xx responses, `error` for 4xx/5xx -- always check which is defined
- Response bodies are consumed once -- clone the response if middleware needs to read it and pass it through
- `openapi-typescript` v7 uses `redocly.yaml` for multi-schema config -- globbing is deprecated

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md**

**(You MUST use OpenAPI 3.1 syntax -- `type: ["string", "null"]` NOT the 3.0 `nullable: true` keyword)**

**(You MUST define reusable schemas in `components/schemas` and reference with `$ref` -- NO inline schema duplication)**

**(You MUST include `operationId` on every path operation -- it becomes the generated client method name)**

**(You MUST use `openapi-typescript` for type generation and import types with `import type` -- types are zero-runtime)**

**Failure to follow these rules will cause schema drift, broken codegen, and type mismatches between spec and implementation.**

</critical_reminders>
