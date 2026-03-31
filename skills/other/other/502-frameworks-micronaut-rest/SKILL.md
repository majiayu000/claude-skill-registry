---
name: 502-frameworks-micronaut-rest
description: Use when you need to design, review, or improve REST APIs with Micronaut — including @Controller routes, HTTP status codes, DTOs, Bean Validation, exception handlers, pagination, idempotency, ETag/If-Match, caching headers, versioning, contract-first OpenAPI (OpenAPI Generator), optional runtime OpenAPI via micronaut-openapi, and security annotations. Part of the skills-for-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.13.0
---
# Micronaut REST API Guidelines

Apply REST design principles for Micronaut HTTP applications.

**What is covered in this Skill?**

- Semantic HTTP with @Get/@Post/@Put/@Patch/@Delete and HttpResponse status control
- Resource-oriented paths and stable DTO contracts
- @Valid on request bodies with Bean Validation
- Centralized error mapping (ExceptionHandler / problem JSON when applicable)
- Pagination with Pageable and bounded sizes
- OpenAPI contract file (API-first) and OpenAPI Generator for server stubs
- Security annotations (@Secured) on sensitive routes
- Idempotency-Key for retried writes
- ETag / If-Match for optimistic concurrency
- Cache-Control discipline
- API versioning patterns
- ISO-8601 time types in DTOs

**Scope:** Apply recommendations based on the reference rules and good/bad code examples.

## Constraints

Compile before REST refactors; verify after.

- **MANDATORY**: Run `./mvnw compile` or `mvn compile` before applying any change
- **SAFETY**: If compilation fails, stop immediately
- **VERIFY**: Run `./mvnw clean verify` or `mvn clean verify` after applying improvements
- **BEFORE APPLYING**: Read the reference for detailed rules and examples

## When to use this skill

- Review or improve Micronaut @Controller REST APIs
- Add validation, error handling, or align controllers with the OpenAPI contract on Micronaut HTTP layer

## Reference

For detailed guidance, examples, and constraints, see [references/502-frameworks-micronaut-rest.md](references/502-frameworks-micronaut-rest.md).
