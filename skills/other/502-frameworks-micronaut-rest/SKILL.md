---
name: 502-frameworks-micronaut-rest
description: Use when you need to design, review, or improve REST APIs with Micronaut — including @Controller routes, HTTP status codes, DTOs, Bean Validation, exception handlers, pagination, idempotency, ETag/If-Match, caching headers, versioning, contract-first OpenAPI (OpenAPI Generator), optional runtime OpenAPI via micronaut-openapi, and security annotations. This should trigger for requests such as Review or improve Micronaut @Controller REST APIs; Add validation, error handling, or align controllers with the OpenAPI contract on Micronaut HTTP layer. Part of cursor-rules-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.15.0-SNAPSHOT
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
- **EDGE CASE**: If request scope is ambiguous, stop and ask a clarifying question before applying changes
- **EDGE CASE**: If required inputs, files, or tooling are missing, report what is missing and ask whether to proceed with setup guidance

## When to use this skill

- Review or improve Micronaut @Controller REST APIs
- Add validation, error handling, or align controllers with the OpenAPI contract on Micronaut HTTP layer

## Workflow

1. **Read reference and assess project context**

Read `references/502-frameworks-micronaut-rest.md` and inspect the current project setup before proposing changes.

2. **Gather scope and decide target improvements**

Identify requested outcomes, constraints, and the minimum safe set of changes to apply.

3. **Apply framework-aligned changes**

Implement or refactor configuration/code following the reference patterns and project conventions.

4. **Run verification and report results**

Execute appropriate build/tests and summarize what changed, what was verified, and any follow-up actions.

## Reference

For detailed guidance, examples, and constraints, see [references/502-frameworks-micronaut-rest.md](references/502-frameworks-micronaut-rest.md).
