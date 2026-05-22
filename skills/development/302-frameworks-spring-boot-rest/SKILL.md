---
name: 302-frameworks-spring-boot-rest
description: Use when you need to design, review, or improve REST APIs with Spring Boot — including HTTP methods, resource URIs, status codes, DTOs, versioning, deprecation and sunset headers, content negotiation (JSON and vendor media types), ISO-8601 instants in DTOs, pagination/sorting/filtering, Bean Validation at the boundary, idempotency, ETag concurrency, HTTP caching, error handling, security, contract-first OpenAPI (OpenAPI Generator), controller advice, and problem details for errors. This should trigger for requests such as Review Java code for Spring Boot REST API; Apply best practices for Spring Boot REST API in Java code. Part of cursor-rules-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.15.0-SNAPSHOT
---
# Java REST API Design Principles

Apply REST API design principles for Spring Boot applications.

**What is covered in this Skill?**

- HTTP methods (GET, POST, PUT, PATCH, DELETE) — semantic consistency
- Resource URI design
- HTTP status codes
- Request/response DTOs with lean contracts
- API versioning (URI, header, or media type — applied consistently)
- Bean Validation at the boundary (@Valid/@Validated on controller inputs, 400 on failure)
- Pagination, sorting, and filtering (Page/Pageable with caps)
- ISO-8601 instants with offset (OffsetDateTime, Instant) in JSON contracts
- Content negotiation (JSON default; vendor media types when meaningful)
- Idempotency-Key support for POST creates; 409 Conflict for collisions
- ETag concurrency with If-Match/If-None-Match; 412 Precondition Failed / 304 Not Modified
- HTTP caching discipline (Cache-Control, ETag, Last-Modified)
- Deprecation and sunset headers (Deprecation, Sunset, Link rel="successor-version)"
- Error handling
- API security (TLS, authentication, authorization, input validation)
- API contract: OpenAPI file as source of truth for API-first (OpenAPI Generator)
- Controller advice and problem details (RFC 7807)

**Scope:** Apply recommendations based on the reference rules and good/bad code examples.

## Constraints

Before applying any REST API changes, ensure the project compiles. If compilation fails, stop immediately. After applying improvements, run full verification.

- **MANDATORY**: Run `./mvnw compile` or `mvn compile` before applying any change
- **SAFETY**: If compilation fails, stop immediately
- **VERIFY**: Run `./mvnw clean verify` or `mvn clean verify` after applying improvements
- **BEFORE APPLYING**: Read the reference for detailed rules and good/bad patterns
- **EDGE CASE**: If request scope is ambiguous, stop and ask a clarifying question before applying changes
- **EDGE CASE**: If required inputs, files, or tooling are missing, report what is missing and ask whether to proceed with setup guidance

## When to use this skill

- Review Java code for Spring Boot REST API
- Apply best practices for Spring Boot REST API in Java code

## Workflow

1. **Read reference and assess project context**

Read `references/302-frameworks-spring-boot-rest.md` and inspect the current project setup before proposing changes.

2. **Gather scope and decide target improvements**

Identify requested outcomes, constraints, and the minimum safe set of changes to apply.

3. **Apply framework-aligned changes**

Implement or refactor configuration/code following the reference patterns and project conventions.

4. **Run verification and report results**

Execute appropriate build/tests and summarize what changed, what was verified, and any follow-up actions.

## Reference

For detailed guidance, examples, and constraints, see [references/302-frameworks-spring-boot-rest.md](references/302-frameworks-spring-boot-rest.md).
