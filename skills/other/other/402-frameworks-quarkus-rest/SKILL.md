---
name: 402-frameworks-quarkus-rest
description: Use when you need to design, review, or improve REST APIs with Quarkus REST (Jakarta REST) — including resource classes, HTTP methods, status codes, request/response DTOs, Bean Validation, exception mappers, OpenAPI with SmallRye, content negotiation, pagination, sorting and filtering, API versioning, idempotency (Idempotency-Key), optimistic concurrency (ETag / If-Match), HTTP caching (Cache-Control), API deprecation (Sunset / Deprecation headers), RFC 7807 Problem Details, ISO-8601 for time in contracts, and security-aware boundaries. Part of the skills-for-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.13.0-SNAPSHOT
---
# Quarkus REST API Guidelines

Apply REST API design principles on Quarkus using Jakarta REST (JAX-RS).

**What is covered in this Skill?**

- Resource classes, @Path, HTTP method mapping, and resource URI design
- Status codes, Location headers, and Response building
- DTOs and Bean Validation at the boundary; ISO-8601 for date/time fields
- ExceptionMapper for consistent error JSON (RFC 7807 Problem Details)
- API versioning strategies (URI path, Accept header)
- Idempotency with Idempotency-Key header
- Optimistic concurrency: ETag, If-Match, If-None-Match
- HTTP caching with Cache-Control headers
- API deprecation: Sunset and Deprecation headers
- Pagination, sorting, and filtering query parameters
- OpenAPI documentation with SmallRye (MicroProfile OpenAPI)
- Reactive vs blocking considerations; @RunOnVirtualThread
- Security integration at the filter layer

**Scope:** Apply recommendations based on the reference rules and good/bad code examples.

## Constraints

Before applying REST changes, ensure the project compiles. After applying improvements, run full verification.

- **MANDATORY**: Run `./mvnw compile` or `mvn compile` before applying any change
- **PREREQUISITE**: Project must compile before applying REST API improvements
- **SAFETY**: If compilation fails, stop immediately
- **BLOCKING CONDITION**: Compilation errors must be resolved by the user before proceeding
- **VERIFY**: Run `./mvnw clean verify` or `mvn clean verify` after applying improvements
- **BEFORE APPLYING**: Read the reference for detailed rules and examples

## When to use this skill

- Review or improve JAX-RS resources in a Quarkus project
- Design HTTP APIs with validation and error handling on Quarkus
- Add API versioning, idempotency, ETag concurrency, or deprecation headers
- Implement pagination, sorting, or RFC 7807 Problem Details error responses

## Reference

For detailed guidance, examples, and constraints, see [references/402-frameworks-quarkus-rest.md](references/402-frameworks-quarkus-rest.md).
